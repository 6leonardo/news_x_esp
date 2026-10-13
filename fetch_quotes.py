#!/usr/bin/env python3
"""Legge quotes.conf, scarica le quotazioni da Yahoo Finance e scrive quotes.txt.

Una riga per simbolo: ETICHETTA|prezzo|variazione% rispetto alla chiusura precedente
(es. "MIB|50035|+0.58"). Un simbolo che fallisce viene saltato; se falliscono tutti
quotes.txt non viene modificato.
"""
import json, sys, urllib.parse, urllib.request

URL = "https://query1.finance.yahoo.com/v8/finance/chart/{}?range=5d&interval=1d"

def quote(symbol):
    req = urllib.request.Request(URL.format(urllib.parse.quote(symbol)),
                                 headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        res = json.load(r)["chart"]["result"][0]
    meta = res["meta"]
    price = meta["regularMarketPrice"]
    # chiusura precedente = ultima chiusura di un giorno (nel fuso della borsa) precedente a quello
    # della quotazione corrente: la candela di oggi puo' avere close vuoto o parziale
    off = meta.get("gmtoffset", 0)
    today = (meta["regularMarketTime"] + off) // 86400
    prev = meta.get("chartPreviousClose")
    for t, c in zip(res["timestamp"], res["indicators"]["quote"][0]["close"]):
        if c is not None and (t + off) // 86400 < today:
            prev = c
    pct = (price - prev) / prev * 100 if prev else 0.0
    return price, pct

def main():
    out = []
    for line in open("quotes.conf", encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        symbol, label, decimals = line.split()
        try:
            price, pct = quote(symbol)
        except Exception as e:
            print(f"{symbol}: {e}", file=sys.stderr)
            continue
        out.append(f"{label[:9]}|{price:.{int(decimals)}f}|{pct:+.2f}")
    if not out:
        sys.exit("nessuna quotazione: quotes.txt non modificato")
    with open("quotes.txt", "w", encoding="ascii") as f:
        f.write("\n".join(out) + "\n")
    print(f"{len(out)} quotazioni")

if __name__ == "__main__":
    main()
