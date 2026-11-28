#!/usr/bin/env python3
"""Cartas do Scryfall para qualquer frente: PNG oficial + `creditos.json` + linha de créditos da legenda (27/11/2026).

Antes, cada episódio descarregava as cartas à mão ou com um script próprio (TUBO passo 2, Expedição `baixar_cartas.py`,
LL-ART21 `catalogo_cartas.py`...). Este junta o passo comum sem mudar o formato: o `creditos.json` tem as mesmas chaves do
da Expedição e do TUBO (name, set, setname, num, artist, uri, oracle, cost...) e mais `ano` e `illustration_id`.

Uso:
  python3 -I comum/ferramentas/cartas.py <pasta> "Sol Ring" "Opt|DOM" "Abyssal Lotus|NAU|234" [--nome ficheiro.png]...
    "Nome"              → impressão padrão do Scryfall (a mais recente com imagem em alta)
    "Nome|SET"          → essa coleção
    "Nome|SET|número"   → essa impressão exata (recomendado para o crédito ficar certo)
  python3 -I comum/ferramentas/cartas.py <pasta> --legenda   → só imprime as linhas de créditos do creditos.json existente

Grava em <pasta>/<slug>_<num>.png (versionar ou não segue a regra da frente: a Expedição não versiona, as outras sim) e
acrescenta a <pasta>/creditos.json. Não republica preços do Scryfall (termos de uso; constituição §4). Pausa de 0,1 s entre pedidos.
"""
import json, os, re, sys, time, unicodedata, urllib.parse, urllib.request

API = 'https://api.scryfall.com'
UA = {'User-Agent': 'BINDERStudio/1.0 (comum/ferramentas/cartas.py)', 'Accept': 'application/json'}


def get(url):
    time.sleep(0.1)
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))


def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '_', s).strip('_')[:40]


def carta(pedido):
    partes = [p.strip() for p in pedido.split('|')]
    if len(partes) == 3:
        return get(f'{API}/cards/{partes[1].lower()}/{urllib.parse.quote(partes[2])}')
    q = {'exact': partes[0]}
    if len(partes) == 2:
        q['set'] = partes[1].lower()
    return get(f'{API}/cards/named?' + urllib.parse.urlencode(q))


def face(d):
    """imagem e campos da frente (cartas de duas faces: 1.ª face)"""
    if 'image_uris' in d:
        return d, d['image_uris']
    f = d['card_faces'][0]
    return {**d, **{k: v for k, v in f.items() if k != 'image_uris'}}, f['image_uris']


def credito(c):
    return (f"{c['name']} ({c['setname']}, {c['ano']}), nº {c['num']}. Arte: {c['artist']}. © Wizards of the Coast.")


def main():
    a = sys.argv[1:]
    if not a or a[0].startswith('-'):
        print(__doc__); return 2
    pasta = os.path.abspath(a[0]); os.makedirs(pasta, exist_ok=True)
    cj = os.path.join(pasta, 'creditos.json')
    C = json.load(open(cj, encoding='utf-8')) if os.path.exists(cj) else {}
    if '--legenda' in a:
        for fn, c in C.items():
            print(f'{fn}: ' + (credito(c) if 'ano' in c else f"{c['name']} ({c['setname']}), nº {c['num']}. Arte: {c['artist']}."))
        return 0
    pedidos, nomes, i = [], [], 1
    while i < len(a):
        if a[i] == '--nome':
            nomes.append(a[i + 1]); i += 2
        else:
            pedidos.append(a[i]); i += 1
    for k, p in enumerate(pedidos):
        d, img = face(carta(p))
        fn = nomes[k] if k < len(nomes) else f"{slug(d['name'])}_{d['collector_number']}.png"
        destino = os.path.join(pasta, fn)
        if not os.path.exists(destino):
            req = urllib.request.Request(img['png'], headers={'User-Agent': UA['User-Agent']})
            with urllib.request.urlopen(req, timeout=120) as r, open(destino, 'wb') as fh:
                fh.write(r.read())
            time.sleep(0.1)
        C[fn] = {'name': d['name'], 'set': d['set'].upper(), 'setname': d['set_name'], 'num': d['collector_number'],
                 'ano': d.get('released_at', '')[:4], 'artist': d.get('artist'), 'illustration_id': d.get('illustration_id'),
                 'fe': d.get('frame_effects'), 'full_art': d.get('full_art'), 'border': d.get('border_color'),
                 'textless': d.get('textless'), 'promo': d.get('promo_types'), 'uri': d.get('scryfall_uri'),
                 'oracle': d.get('oracle_text'), 'cost': d.get('mana_cost')}
        print(f'{fn}: {credito(C[fn])}')
    with open(cj, 'w', encoding='utf-8') as fh:
        json.dump(C, fh, ensure_ascii=False, indent=1)
    print(f'{len(pedidos)} carta(s) · {cj}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
