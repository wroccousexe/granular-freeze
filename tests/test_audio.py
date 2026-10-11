import sys
import argparse
import hashlib
import json
import time
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description='Verify a GRANULAR FREEZE VST3 binary with real audio.')
parser.add_argument('--plugin', type=Path, default=ROOT / 'export' / 'GRANULAR FREEZE.vst3' / 'Contents' / 'x86_64-win' / 'GRANULAR FREEZE.vst3')
parser.add_argument('--output', type=Path, default=ROOT / 'audio-test')
args = parser.parse_args()
if (ROOT.parent / 'test-tools').exists():
    sys.path.insert(0, str(ROOT.parent / 'test-tools'))
import numpy as np
from pedalboard import load_plugin

PLUGIN = args.plugin.resolve()
if not PLUGIN.is_file():
    parser.error(f'VST3 binary not found: {PLUGIN}')
OUT = args.output.resolve()
OUT.mkdir(parents=True, exist_ok=True)

def rms(x):
    return float(np.sqrt(np.mean(np.asarray(x, dtype=np.float64) ** 2)))

def render(p, data, sr, block=256):
    y = p.process(data, sr, buffer_size=block, reset=False)
    assert y.shape == data.shape, (y.shape, data.shape)
    assert np.isfinite(y).all(), 'NaN or infinity in audio'
    return y

def tone(sr, seconds, freq=400):
    t = np.arange(round(sr * seconds)) / sr
    mono = (0.2 * np.sin(2 * np.pi * freq * t)).astype(np.float32)
    return np.stack([mono, mono])

def silence(sr, seconds):
    return np.zeros((2, round(sr * seconds)), dtype=np.float32)

def save_wav(name, data, sr):
    with wave.open(str(OUT / name), 'wb') as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(sr)
        f.writeframes((np.clip(data.T, -1, 1) * 32767).astype('<i2').tobytes())

results = []
for sr, block in [(44100, 64), (48000, 256), (96000, 128), (192000, 512)]:
    p = load_plugin(str(PLUGIN))
    p.capture = 0
    p.clear = 0
    p.wet = 1
    p.gain_db = 0
    render(p, silence(sr, 0.02), sr, block)
    p.capture = 1
    capture = render(p, tone(sr, 0.25), sr, block)
    start = time.perf_counter()
    frozen = render(p, silence(sr, 0.4), sr, block)
    elapsed = time.perf_counter() - start
    assert rms(capture[:, :round(sr * 0.14)]) < 1e-6, 'Audio emitted before capture completed'
    assert rms(frozen) > 0.005, 'Freeze did not persist after input stopped'
    assert np.max(np.abs(frozen)) < 1.01, 'Unexpected excessive output'
    assert np.max(np.abs(frozen[0] - frozen[1])) < 1e-5, 'Centered pan channels differ'
    p.pan = 0
    left = render(p, silence(sr, 0.3), sr, block)
    assert rms(left[1, -round(sr * 0.1):]) < 1e-6, 'Hard-left pan leaks right'
    assert rms(left[0, -round(sr * 0.1):]) > 0.005
    p.pan = 1
    right = render(p, silence(sr, 0.3), sr, block)
    assert rms(right[0, -round(sr * 0.1):]) < 1e-6, 'Hard-right pan leaks left'
    assert rms(right[1, -round(sr * 0.1):]) > 0.005
    p.enabled = 0
    stopped = render(p, silence(sr, 0.25), sr, block)
    assert rms(stopped[:, -round(sr * 0.1):]) < 1e-6, 'Disabled grains do not stop'
    p.enabled = 1
    resumed = render(p, silence(sr, 0.2), sr, block)
    assert rms(resumed) > 0.005, 'Re-enabling loses the captured buffer'
    p.clear = 1
    cleared = render(p, silence(sr, 0.2), sr, block)
    assert rms(cleared) < 1e-6, 'Clear does not silence freeze'
    p.clear = 0
    p.capture = 0
    render(p, silence(sr, 0.01), sr, block)
    p.capture = 1
    p.pan = 0.5
    recapture = render(p, tone(sr, 0.25, 800), sr, block)
    frozen2 = render(p, silence(sr, 0.3), sr, block)
    assert rms(frozen2) > 0.005, 'Second capture failed'
    p.wet = 0
    p.gain_db = -6
    dry_in = tone(sr, 0.25)
    dry = render(p, dry_in, sr, block)
    actual_gain_db = -60 + 66 * p.parameters['gain_db'].raw_value
    expected = dry_in[:, -round(sr * 0.1):] * (10 ** (actual_gain_db / 20))
    assert np.max(np.abs(dry[:, -round(sr * 0.1):] - expected)) < 1e-4, 'Dry path or gain mismatch'
    p.wet = 1
    p.gain_db = 0
    p.grain_ms = 150
    p.interval_ms = 1
    p.capture = 0
    render(p, silence(sr, 0.01), sr, block)
    p.capture = 1
    noise = np.random.default_rng(74).uniform(-0.2, 0.2, (2, round(sr * 0.25))).astype(np.float32)
    render(p, noise, sr, block)
    dense = render(p, silence(sr, 0.4), sr, block)
    assert rms(dense) > 0.0001, 'Dense-grain rendering failed'
    assert np.max(np.abs(dense)) < 1.01, 'Dense-grain output out of bounds'
    row = {'sample_rate': sr, 'block_size': block, 'freeze_rms': rms(frozen),
           'freeze_peak': float(np.max(np.abs(frozen))), 'render_400ms_seconds': elapsed,
           'checks': ['150ms capture', 'persistent freeze', 'stereo center', 'pan left/right',
                      'disable/resume', 'clear', 'second capture', 'dry path and gain', '64-voice density', 'finite audio']}
    results.append(row)
    if sr == 48000:
        demo = np.concatenate([capture, frozen, left, right, stopped, resumed, cleared, recapture, frozen2, dry, dense], axis=1)
        save_wav('GRANULAR-FREEZE-test.wav', demo, sr)
        save_wav('freeze-400Hz.wav', frozen, sr)
    print(json.dumps(row), flush=True)

(OUT / 'results.json').write_text(json.dumps({'plugin': PLUGIN.name, 'internal_name': p.name, 'binary_sha256': hashlib.sha256(PLUGIN.read_bytes()).hexdigest(), 'passed': True, 'results': results}, indent=2), encoding='utf-8')
print('ALL AUDIO CHECKS PASSED')
