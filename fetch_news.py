#!/usr/bin/env python3
"""Scarica l'RSS ANSA "Ultima ora" e scrive news.txt: un titolo ASCII per riga."""
import re, sys, unicodedata, urllib.request
import xml.etree.ElementTree as ET

FEED = "https://www.ansa.it/sito/notizie/topnews/topnews_rss.xml"
MAX_NEWS, MAX_LEN = 8, 150

# L'OLED ha solo caratteri ASCII: le vocali accentate diventano "e'", "a'", ...
ACCENTS = {"à": "a'", "è": "e'", "é": "e'", "ì": "i'", "ò": "o'", "ù": "u'",
           "À": "A'", "È": "E'", "É": "E'", "Ì": "I'", "Ò": "O'", "Ù": "U'",
           "’": "'", "‘": "'", "“": '"', "”": '"', "«": '"', "»": '"',
           "–": "-", "—": "-", "…": "..."}

def to_ascii(s):
    s = "".join(ACCENTS.get(c, c) for c in s)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s).strip()

def main():
    req = urllib.request.Request(FEED, headers={"User-Agent": "news_x_esp/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        root = ET.fromstring(r.read())
    titles = [to_ascii(i.findtext("title") or "")[:MAX_LEN] for i in root.iter("item")]
    titles = [t for t in titles if t][:MAX_NEWS]
    if not titles:
        sys.exit("nessun titolo nel feed: news.txt non modificato")
    with open("news.txt", "w", encoding="ascii") as f:
        f.write("\n".join(titles) + "\n")

if __name__ == "__main__":
    main()
