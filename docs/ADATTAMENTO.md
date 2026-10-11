# Dalla patch originale a RNBO

La patch selezionata è esattamente `III/009-GRANULAR_FREEZE.maxpat`, rispettando maiuscole e minuscole, con `III/granula.maxpat`. La copia originale resta in `original/`.

L'adattamento sostituisce gli oggetti Max non esportabili direttamente con un motore Gen dentro RNBO: buffer mono di 150 ms, fino a 64 grani, durata e punto di lettura controllabili, inviluppo Hann e panorama stereo a potenza costante. Aggiunge mix diretto, guadagno, Enabled/Clear e compensazione del livello dei grani sovrapposti. Mix e guadagno vengono smussati in 5 ms.

Non è un confronto campione per campione con l'originale: nella patch di riferimento alcuni collegamenti di inviluppo e avvio erano incompleti. Il risultato implementa il comportamento di cattura e granulazione previsto, rendendolo utilizzabile come effetto VST3.

Gli errori iniziali nella console Max erano legati al campo di salvataggio del CodeBox e ai metadati delle porte di `rnbo~`. Il codice è ora salvato nel campo `code`, i metadati sono stati generati da Max e i collegamenti stereo esterni ripristinati. Le verifiche sul modulo compilato confermano il percorso audio.
