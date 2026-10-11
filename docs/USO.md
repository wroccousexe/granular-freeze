# Uso di GRANULAR FREEZE

## Cubase su Windows

Copiare l'intera cartella `GRANULAR FREEZE.vst3` in `C:\Program Files\Common Files\VST3`. Potrebbero servire i privilegi di amministratore. Riaprire Cubase o aggiornare la scansione nel gestore plugin e inserire l'effetto su una traccia audio stereo.

Il percorso diretto conserva entrambi i canali. La cattura usa il canale sinistro, come l'ingresso mono della patch originale; il freeze produce un'uscita stereo. La cattura è temporanea: riaprendo l'istanza occorre catturare nuovamente.

| Controllo | Funzione |
| --- | --- |
| Capture | Cattura i successivi 150 ms sul passaggio da 0 a 1 |
| Start_ms | Punto di lettura nel frammento, 0–149 ms |
| Grain_ms | Durata del grano, 1–150 ms |
| Pan | 0 sinistra, 0,5 centro, 1 destra |
| Interval_ms | Intervallo fra grani, 1–100 ms |
| Clear | Cancella il freeze sul passaggio da 0 a 1 |
| Wet | 0 diretto, 1 solo granulazione |
| Gain_dB | Guadagno di uscita, −60…+6 dB; valore iniziale −6 dB |
| Enabled | Avvia/arresta i nuovi grani mantenendo la cattura |

Per una seconda cattura riportare Capture a 0 prima di impostarlo a 1. Clear funziona allo stesso modo. Con Wet=1, prima della cattura non si sente il segnale diretto. Enabled=0 lascia terminare i grani già avviati.

La ripetizione regolare dei grani può cancellare frequenze di una sinusoide pura. Con 440 Hz, Grain_ms=50 e Interval_ms=10 il segnale può risultare quasi silenzioso dopo la transizione. Cambiare durata/intervallo o usare un segnale musicale più complesso. I test di persistenza usano 400/800 Hz; la prova ad alta densità usa rumore.

Il pannello VST3 è quello generico RNBO. L'interfaccia Max non viene trasferita automaticamente nel plugin.

## Test inclusi

`audio-test/GRANULAR-FREEZE-test.wav` contiene cattura, freeze, sinistra, destra, arresto, ripresa, Clear, seconda cattura, secondo freeze, diretto e alta densità. `freeze-400Hz.wav` è un breve freeze stereo isolato. `results.json` identifica il binario su cui sono state eseguite le verifiche.

Questi sono test digitali in un host VST3, senza modificare il progetto Cubase aperto.
