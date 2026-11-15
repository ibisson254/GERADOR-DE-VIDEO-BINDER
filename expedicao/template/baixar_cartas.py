# Expedição BINDER · descarrega do Scryfall os PNG listados em <episodio>/cards/creditos.json (set + número).
# Uso: python3 -I baixar_cartas.py <pasta_do_episodio>
# Os PNG não são versionados (pesam ~1 MB cada); o creditos.json é a lista canónica.
import json, sys, time, urllib.request
EP = sys.argv[1].rstrip('/')
C = json.load(open(f'{EP}/cards/creditos.json'))
H = {'User-Agent': 'BinderStudio/1.0', 'Accept': 'application/json'}
for fn, c in C.items():
    url = f'https://api.scryfall.com/cards/{c["set"].lower()}/{c["num"]}'
    d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=H)))
    img = d['image_uris']['png'] if 'image_uris' in d else d['card_faces'][0]['image_uris']['png']
    urllib.request.urlretrieve(img, f'{EP}/cards/{fn}'); print(fn); time.sleep(0.12)
