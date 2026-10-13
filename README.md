# news_x_esp

Titoli di ANSA in testo semplice per il display ESP8266
(`esp-w-display`). Una GitHub Action ogni 4 ore esegue `fetch_news.py` e
aggiorna `news.txt`: solo ASCII (accenti come `e'`), 150
caratteri a riga, al massimo 6 KB (`MAX_BYTES`). Feed in ordine: Top news,
Tecnologia, Scienza e Tecnica, Economia; si ferma alla prima notizia che sfora.

Il display scarica il file in HTTPS da
`https://raw.githubusercontent.com/<utente>/news_x_esp/main/news.txt`.

Repository pubblico: contiene solo titoli di notizie pubbliche, nessun segreto.

## Quotazioni (pagina viola)
`quotes.conf` elenca i simboli Yahoo Finance, l'etichetta sul display e i decimali (l'ordine
del file e' l'ordine sul display). `fetch_quotes.py` scrive `quotes.txt`, una riga per simbolo:
`ETICHETTA|prezzo|variazione%` rispetto alla chiusura precedente. L'Action `quotes.yml` gira
ogni ora. Per aggiungere o togliere un titolo basta modificare `quotes.conf`.
OpenAI e Anthropic non sono quotate e non hanno un simbolo.
