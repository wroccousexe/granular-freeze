# GRANULAR FREEZE

Effetto di granular freeze stereo per Windows/Cubase, realizzato in Max 9 con RNBO 1.3.3. Cattura 150 ms del canale sinistro e li riproduce con fino a 64 grani, inviluppo Hann e panorama a potenza costante.

Il punto di partenza è esattamente `III/009-GRANULAR_FREEZE.maxpat` e la subpatch `III/granula.maxpat` del materiale originale. Il plugin si chiama **GRANULAR FREEZE**. È un adattamento RNBO/Gen del comportamento della patch, con mix diretto, controllo del livello e parametri automatizzabili.

## Materiale incluso

| Cartella | Contenuto |
| --- | --- |
| `patches/` | Patch Max completa e patch RNBO autonome, con nome GRANULAR FREEZE |
| `src/` | Codice Gen del motore granulare |
| `original/` | Patch di riferimento e dipendenza `pan2.maxpat` |
| `tests/` | Test audio del VST3 e dipendenze Python |
| `audio-test/` | WAV di esempio e risultati delle verifiche |
| `docs/` | Uso in Cubase, esportazione e note sull'adattamento |
| `licenses/` | Avvertenze originali dell'export RNBO e provenienza dei file |

## Stato

La precedente compilazione VST3 ha superato i test audio a 44,1 / 48 / 96 / 192 kHz. I risultati indicano esplicitamente il modulo verificato e il suo SHA-256. La nuova esportazione con nome interno GRANULAR FREEZE deve ancora essere compilata e verificata. La prova nel progetto Cubase dell'utente non è stata effettuata.

Il VST3 compilato resta per ora nella copia locale: il README dell'export RNBO 1.3.3 richiede un'autorizzazione Steinberg per la distribuzione di questi binari. Pubblicare la patch RNBO non equivale a fornire il sorgente completo del plugin compilato dal servizio cloud. Vedi [note sulle licenze](licenses/NOTICE.md).

## Uso rapido

1. Aprire `patches/GRANULAR_FREEZE_RNBO.maxpat` in Max con RNBO.
2. Esportare il plugin Windows x64 come **GRANULAR FREEZE** seguendo [la procedura](docs/EXPORT.md).
3. Copiare l'intera cartella `GRANULAR FREEZE.vst3` in `C:\Program Files\Common Files\VST3` e aggiornare la scansione di Cubase.
4. Inserire l'effetto su una traccia stereo. Portare Capture da 0 a 1 mentre passa il segnale: dopo 150 ms inizia la granulazione.

Con Wet=1, prima della cattura l'uscita è silenziosa. Per catturare di nuovo, portare Capture a 0 e poi a 1. [Controlli e dettagli](docs/USO.md).

## Ripetere le verifiche

Con Python 3.10 o successivo, dalla cartella del repository:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r tests/requirements.txt
.\.venv\Scripts\python.exe tests/test_audio.py --plugin "C:\Program Files\Common Files\VST3\GRANULAR FREEZE.vst3\Contents\x86_64-win\GRANULAR FREEZE.vst3" --output audio-test
```

Il test verifica cattura, persistenza, stereo, panorama, arresto/ripresa, Clear, seconda cattura, segnale diretto/guadagno, alta densità e campioni finiti. I WAV sintetici consentono di ascoltare il risultato senza distribuire materiale musicale di terzi.
