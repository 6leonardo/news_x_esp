# news_x_esp

Titoli di ANSA "Ultima ora" in testo semplice per il display ESP8266
(`esp-w-display`). Una GitHub Action ogni 4 ore esegue `fetch_news.py` e
aggiorna `news.txt`: massimo 8 righe, solo ASCII (accenti come `e'`), 150
caratteri a riga.

Il display scarica il file in HTTPS da
`https://raw.githubusercontent.com/<utente>/news_x_esp/main/news.txt`.

Repository pubblico: contiene solo titoli di notizie pubbliche, nessun segreto.
