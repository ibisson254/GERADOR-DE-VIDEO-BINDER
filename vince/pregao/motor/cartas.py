"""Descarrega as imagens oficiais das cartas do episódio (Scryfall: só imagem e dados, nunca preço).
Uso: python3 -I cartas.py PASTA_SAIDA
Cria PASTA_SAIDA/<chave>.png e meta.json (nome, edição, número, artista).
"""
import json, sys, time, pathlib, urllib.request

CARTAS = {  # chave usada em dados.js -> edição/número no Scryfall
    "urza": "brc/2", "uchuulon": "clb/673", "picard": "trk/7", "overgrown": "trk/289", "watery": "trk/306",
    "hallowed": "trk/286", "blood": "trk/278", "steam": "trk/298", "breeding": "trk/279", "sacred": "trk/295",
    "godless": "trk/285", "temple": "trk/301", "stomping": "trk/299",
}
H = {"User-Agent": "BINDERStudio/1.0", "Accept": "application/json"}

out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
meta = {}
for k, p in CARTAS.items():
    c = json.load(urllib.request.urlopen(urllib.request.Request("https://api.scryfall.com/cards/" + p, headers=H)))
    urllib.request.urlretrieve(c["image_uris"]["png"], out / f"{k}.png")
    meta[k] = dict(name=c["name"], set=c["set"].upper(), set_name=c["set_name"], num=c["collector_number"],
                   artist=c["artist"], scryfall=c["scryfall_uri"].split("?")[0])
    time.sleep(0.12)
(out / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(meta), "cartas em", out)
