# Esportazione Windows VST3

Ambiente della prima compilazione: Windows x64, Max 9.0.0, RNBO 1.3.3. È necessario un Max con RNBO autorizzato e una connessione per l'esportazione tramite il servizio Cycling '74.

1. Aprire `patches/GRANULAR_FREEZE_RNBO.maxpat`.
2. Aprire l'oggetto `rnbo~` con doppio clic.
3. Aprire il pannello Export e scegliere Audio Plugin Export.
4. Verificare il nome `GRANULAR FREEZE`, il formato VST3 e Windows x64. Impostare una cartella di destinazione.
5. Avviare Export e attendere la conferma della compilazione.
6. Conservare l'intera cartella `.vst3` e il README delle licenze generato insieme al binario.
7. Eseguire `tests/test_audio.py` sul modulo `.vst3` in `Contents/x86_64-win` prima di distribuirlo o installarlo.

Il progetto include sia l'host Max sia la patch `.rnbopat`. La cartella di esportazione viene scelta sul computer che apre il progetto; non è fissata a un percorso personale.

L'export cloud fornisce un modulo compilato, non un progetto C++ completo del wrapper. Per una compilazione locale servono l'export C++ RNBO, il relativo runtime e un wrapper compatibile, oltre alle condizioni di licenza applicabili. Questi componenti non sono inclusi nel materiale attuale.
