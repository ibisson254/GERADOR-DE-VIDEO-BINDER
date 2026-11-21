"""Descarrega do Scryfall as imagens das cartas do LM-EP00 (Alpha) para uma pasta local (não versionada).
uso: python3 -I cartas.py PASTA"""
import json, os, sys, time, urllib.parse, urllib.request
H = {"User-Agent": "BINDER/1.0", "Accept": "application/json"}
pasta = sys.argv[1]; os.makedirs(pasta, exist_ok=True)
for n in ["Shivan Dragon", "Mind Twist", "Giant Growth", "Time Walk"]:
    c = json.load(urllib.request.urlopen(urllib.request.Request(
        "https://api.scryfall.com/cards/named?set=lea&exact=" + urllib.parse.quote(n), headers=H)))
    dest = os.path.join(pasta, n.lower().replace(" ", "_") + ".png")
    open(dest, "wb").write(urllib.request.urlopen(urllib.request.Request(c["image_uris"]["png"], headers={"User-Agent": "BINDER/1.0"})).read())
    print(n, "|", c["artist"], "|", c["set_name"], "→", dest); time.sleep(0.2)
