"""Descarrega do Scryfall as 3 cartas do LM-EP01 (Secret Lair Drop 2680–2682) para uma pasta local (não versionada).
uso: python3 -I cartas.py PASTA"""
import json, os, sys, urllib.request
AQUI = os.path.dirname(os.path.abspath(__file__))
pasta = sys.argv[1]; os.makedirs(pasta, exist_ok=True)
b = json.load(open(os.path.join(AQUI, 'cartas_scryfall.json')))
for nome, fn in (("Coat of Arms", "coat_of_arms"), ("Finale of Devastation", "finale_of_devastation"), ("Lathril, Blade of the Elves", "lathril")):
    c = b[nome][0]
    open(os.path.join(pasta, fn + "_png.png"), "wb").write(urllib.request.urlopen(urllib.request.Request(c["png"], headers={"User-Agent": "BINDER/1.0"})).read())
    print(nome, c["set"], c["num"], c["artist"])
