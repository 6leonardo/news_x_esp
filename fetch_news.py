#!/usr/bin/env python3
"""Scarica l'RSS ANSA "Ultima ora" e scrive news.txt: un titolo ASCII per riga."""
import re, sys, unicodedata, urllib.request
import xml.etree.ElementTree as ET

# Ordine esatto: prima tutte le notizie del primo feed, poi quelle del secondo, ecc.
FEEDS = ["https://www.ansa.it/sito/notizie/topnews/topnews_rss.xml",
         "https://www.ansa.it/canale_tecnologia/notizie/tecnologia_rss.xml",
         "https://www.ansa.it/canale_scienza_tecnica/notizie/scienzaetecnica_rss.xml",
         "https://www.ansa.it/sito/notizie/economia/economia_rss.xml"]
MAX_BYTES = 6 * 1024   # dimensione massima di news.txt (newline inclusi)
MAX_LEN = 150          # lunghezza massima di un titolo

# L'OLED ha solo caratteri ASCII: le vocali accentate diventano "e'", "a'", ...
ACCENTS = {"à": "a'", "è": "e'", "é": "e'", "ì": "i'", "ò": "o'", "ù": "u'",
           "À": "A'", "È": "E'", "É": "E'", "Ì": "I'", "Ò": "O'", "Ù": "U'",
           "’": "'", "‘": "'", "“": '"', "”": '"', "«": '"', "»": '"',
           "–": "-", "—": "-", "…": "..."}

def to_ascii(s):
    s = "".join(ACCENTS.get(c, c) for c in s)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s).strip()

def feed_titles(path):
    req = urllib.request.Request(path, headers={"User-Agent": "news_x_esp/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        root = ET.fromstring(r.read())
    return [t for t in (to_ascii(i.findtext("title") or "")[:MAX_LEN] for i in root.iter("item")) if t]

def main():
    feeds = []
    for path in FEEDS:
        try:
            feeds.append(feed_titles(path))
        except Exception as e:  # un feed rotto non blocca gli altri
            print(f"feed {path}: {e}", file=sys.stderr)
    # in ordine, senza doppioni
    ordered, seen = [], set()
    for titles in feeds:
        for t in titles:
            if t not in seen:
                seen.add(t)
                ordered.append(t)
    if not ordered:
        sys.exit("nessun titolo nei feed: news.txt non modificato")
    # prende le notizie in ordine finche' stanno nel budget; alla prima che sfora si ferma
    out, size = [], 0
    for t in ordered:
        if size + len(t) + 1 > MAX_BYTES:
            break
        out.append(t)
        size += len(t) + 1
    with open("news.txt", "w", encoding="ascii") as f:
        f.write("\n".join(out) + "\n")
    print(f"{len(out)} notizie, {size} byte")

if __name__ == "__main__":
    main()
