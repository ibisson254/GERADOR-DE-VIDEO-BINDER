"""LL-ART21 V2 · catálogo das ilustrações de Willian Murai no Scryfall, com cache das imagens oficiais.
Uso: python3 -I catalogo_cartas.py <cache>   → <cache>/scryfall_bruto.json, catalogo.json, cartas/<illustration_id>.png
     python3 -I catalogo_cartas.py <cache> --md catalogo.md   → também a tabela para a pasta do episódio
Consulta artist:"Willian Murai" com unique=prints (todas as impressões, com paginação) e unique=art (conferência).
Uma ilustração = um illustration_id do Scryfall; cada face de uma carta de duas faces conta à parte.
Reimpressões da mesma arte não contam como ilustração nova. O PNG usado é o da 1.ª impressão com imagem em alta."""
import json, os, sys, time, urllib.request, urllib.parse, collections, datetime

CACHE = os.path.abspath(sys.argv[1]); os.makedirs(os.path.join(CACHE, 'cartas'), exist_ok=True)
UA = {'User-Agent': 'BINDERStudio/1.0 (lambe-lambe LL-ART21)', 'Accept': 'application/json'}

def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60))

def consulta(unique):
    q = urllib.parse.urlencode({'q': 'artist:"Willian Murai"', 'unique': unique, 'order': 'released', 'dir': 'asc',
                                'include_extras': 'true', 'include_variations': 'true'})
    u, cartas, paginas = 'https://api.scryfall.com/cards/search?' + q, [], 0
    while u:
        d = get(u); cartas += d['data']; paginas += 1; u = d['next_page'] if d.get('has_more') else None; time.sleep(.12)
    return {'total_cards': d['total_cards'], 'paginas': paginas, 'data': cartas}

bruto = os.path.join(CACHE, 'scryfall_bruto.json')
if not os.path.exists(bruto):
    json.dump({'consulta': datetime.date.today().isoformat(), 'prints': consulta('prints'), 'art': consulta('art')}, open(bruto, 'w'))
B = json.load(open(bruto)); P = B['prints']['data']

g = collections.OrderedDict()
for c in P:
    for i, f in enumerate(c['card_faces'] if 'card_faces' in c and 'illustration_id' not in c else [c]):
        if 'Murai' not in f.get('artist', ''): continue
        g.setdefault(f['illustration_id'], []).append(dict(card=c, face=f, fi=i, img=f.get('image_uris') or c.get('image_uris')))

def preferida(p):  # 1.ª impressão com imagem em alta; promos e produtos especiais só se não houver outra
    c = p['card']
    return (not c.get('highres_image'), c.get('promo', False), c['released_at'])

cat = []
for iid, ps in g.items():
    o = min(ps, key=lambda p: p['card']['released_at']); v = min(ps, key=preferida); c, f = o['card'], o['face']
    cat.append(dict(ilustracao=iid, nome=f['name'], carta=c['name'], set=c['set'].upper(), set_nome=c['set_name'], set_tipo=c['set_type'],
                    numero=c['collector_number'], ano=c['released_at'][:4], artista=f['artist'], impressoes=len(ps),
                    outras=sorted({f"{p['card']['set'].upper()} {p['card']['collector_number']}" for p in ps} - {f"{c['set'].upper()} {c['collector_number']}"}),
                    video=f"{v['card']['set'].upper()} {v['card']['collector_number']}", video_png=v['img']['png'], scryfall=v['card']['scryfall_uri'].split('?')[0],
                    highres=v['card'].get('highres_image'), moldura=v['card']['frame'], borda=v['card']['border_color'],
                    tipo=f.get('type_line', c.get('type_line')), raridade=c['rarity']))
json.dump(cat, open(os.path.join(CACHE, 'catalogo.json'), 'w'), ensure_ascii=False, indent=1)

falhas = []
for x in cat:
    f = os.path.join(CACHE, 'cartas', x['ilustracao'] + '.png')
    if os.path.exists(f) and os.path.getsize(f) > 10000: continue
    try:
        open(f, 'wb').write(urllib.request.urlopen(urllib.request.Request(x['video_png'], headers=UA), timeout=60).read()); time.sleep(.1)
    except Exception as e: falhas.append(f"{x['nome']}: {e}")
ok = sum(os.path.getsize(os.path.join(CACHE, 'cartas', x['ilustracao'] + '.png')) > 10000 for x in cat
         if os.path.exists(os.path.join(CACHE, 'cartas', x['ilustracao'] + '.png')))
print(f"Scryfall {B['consulta']}: unique=prints {B['prints']['total_cards']} ({B['prints']['paginas']} páginas) · unique=art {B['art']['total_cards']} · "
      f"ilustrações distintas (por face) {len(cat)} · imagens em cache {ok}/{len(cat)}" + (' · FALHAS: ' + '; '.join(falhas) if falhas else ''))
if falhas: sys.exit(1)

if '--md' in sys.argv:
    md = sys.argv[sys.argv.index('--md') + 1]
    L = [f"# LL-ART21 V2 · Catálogo das ilustrações de Willian Murai (Scryfall, consulta de {B['consulta']})", '',
         f"Consulta `artist:\"Willian Murai\"` na API do Scryfall, com paginação: **{B['prints']['total_cards']} impressões** (`unique=prints`, "
         f"{B['prints']['paginas']} páginas) e **{B['art']['total_cards']} cartas com arte distinta** (`unique=art`). Agrupando por `illustration_id` "
         f"e contando cada face: **{len(cat)} ilustrações distintas** (a única diferença é a Kytheon, Hero of Akros // Gideon, Battle-Forged: "
         "as duas faces são de Murai e são duas ilustrações). Reimpressões da mesma arte não contam. As duas Jeering Instigator (KTK 113 e UGIN 113) "
         "são ilustrações diferentes.", '',
         'Todas as ilustrações foram usadas no Reel V2 (`reel_v2.py`). Imagem: PNG oficial do Scryfall da impressão da coluna «No vídeo» '
         '(745×1040, inteiro, sem corte nem filtro). Crédito do artista no Scryfall: «Willian Murai» em todas; © Wizards of the Coast. Ano = ano da 1.ª impressão.', '',
         '| # | Ilustração (nome da face) | Edição (1.ª impressão) | Nº | Ano | Impressões | No vídeo | Uso no Reel | Observação visual | illustration_id |',
         '|---|---|---|---|---|---|---|---|---|---|']
    uso = json.load(open(os.path.join(CACHE, 'uso_v2.json'))) if os.path.exists(os.path.join(CACHE, 'uso_v2.json')) else {}
    for i, x in enumerate(cat, 1):
        obs = 'alta resolução' if x['highres'] else 'resolução baixa'
        obs += f", moldura {x['moldura']}"
        if x['set_tipo'] not in ('expansion', 'core', 'masters', 'draft_innovation', 'commander', 'duel_deck', 'from_the_vault'):
            obs += f", produto especial ({x['set_tipo']})"
        L.append(f"| {i} | [{x['nome']}]({x['scryfall']}) | {x['set_nome']} ({x['set']}) | {x['numero']} | {x['ano']} | {x['impressoes']} | {x['video']} | "
                 f"{uso.get(x['ilustracao'], '—')} | {obs} | `{x['ilustracao']}` |")
    L += ['', 'URL da imagem oficial: `video_png` em `catalogo.json` (gerado por `catalogo_cartas.py`; as imagens não são versionadas).', '']
    open(md, 'w').write('\n'.join(L)); print('tabela', md)
