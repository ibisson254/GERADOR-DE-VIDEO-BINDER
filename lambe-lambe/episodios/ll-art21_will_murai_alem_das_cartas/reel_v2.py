"""LL-ART21 V2 · Will Murai — o artista por trás das cartas. Reel documental 9:16, só deste episódio.
Evolui reel.py (V1, intacto): importa dele as peças e a animação (matte, em_papel, na_faixa, muro, E, pinta, camera, sfx, trilha)
e o kit (motor_padrao: carta, selo, kraft, faixa; recorte_foto: foto P&B). Nenhum motor genérico novo.
O que muda na V2: 54 ilustrações do catálogo Scryfall (cartas-herói, galeria por mundo, montagem com contador, mosaico final),
foto do artista (só na versão privada), render por cenas com cache e folha de contacto.

Uso:
  python3 -I catalogo_cartas.py <cache>                       # catálogo + PNG oficiais (uma vez)
  python3 -I reel_v2.py <cache> <saida.mp4> [--foto foto.png mascara.png] [--cenas 3,7] [--capa capa.png]
  <cache> = pasta com catalogo.json e cartas/<illustration_id>.png. Sem --foto sai a versão sem retrato (publicável).
1080x1920, 30 fps, H.264 + AAC; termina com comum/outro/outro_binder_916.mp4."""
import sys, os, json, hashlib, subprocess, wave, asyncio, shutil
import cv2, numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
CACHE, OUT = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
arg = sys.argv[3:]
FOTO = (os.path.abspath(arg[arg.index('--foto') + 1]), os.path.abspath(arg[arg.index('--foto') + 2])) if '--foto' in arg else None
SO_CENAS = {int(x) for x in arg[arg.index('--cenas') + 1].split(',')} if '--cenas' in arg else None
CAPA = os.path.abspath(arg[arg.index('--capa') + 1]) if '--capa' in arg else None
VAR = 'foto' if FOTO else 'semfoto'

# V1 como biblioteca: o bloco __main__ de reel.py não corre ao importar
_argv = sys.argv; sys.argv = ['reel.py', CACHE, OUT]; sys.path.insert(0, AQUI)
import reel as V1
sys.argv = _argv
M = V1.M
from recorte_foto import recorte
from compor import rasgo_alpha
W, H, FPS = V1.W, V1.H, V1.FPS
CX = V1.CX
ROSA, AMAR = '#E61E6E', '#FFD84A'
MEM = os.path.join(os.path.dirname(OUT), '_cache_v2'); os.makedirs(MEM, exist_ok=True)

CAT = json.load(open(os.path.join(CACHE, 'catalogo.json')))
POR_NOME = {x['nome']: x for x in CAT}
def png(nome):
    f = os.path.join(CACHE, 'cartas', POR_NOME[nome]['ilustracao'] + '.png')
    if not os.path.exists(f): sys.exit(f'falta a imagem de {nome}: {f} (correr catalogo_cartas.py)')
    return f
FALTAM = [x['nome'] for x in CAT if not os.path.exists(os.path.join(CACHE, 'cartas', x['ilustracao'] + '.png'))]
if FALTAM: sys.exit('imagens em falta: ' + ', '.join(FALTAM))

# ---------------- peças com cache em disco ----------------
def guardado(chave, fazer):
    f = os.path.join(MEM, hashlib.md5(chave.encode()).hexdigest()[:16] + '.npz')
    if os.path.exists(f):
        z = np.load(f); return z['rgb'], z['a']
    rgb, a = fazer(); np.savez(f, rgb=rgb.astype(np.float32), a=a.astype(np.float32)); return rgb, a

def carta(nome, larg):
    """carta inteira do Scryfall, fita só nos cantos de cima (largura da fita = 20 % da carta), rodapé livre"""
    return guardado(f'carta|{nome}|{larg}|v1', lambda: V1.matte(
        lambda b: M.carta(b, png(nome), 540, 675, larg, 0, fitas=((-1.0, -1.04, -45), (1.0, -1.04, 45)), fl=max(34, int(larg * .2)))))

def carta_nua(nome, larg):
    """mosaico final: carta inteira sem fita (pequena demais para a fita ser legível)"""
    return guardado(f'nua|{nome}|{larg}|v1', lambda: V1.matte(lambda b: M.carta(b, png(nome), 540, 675, larg, 0, fitas=())))

def lupa(nome, caixa):
    """ampliação do crédito impresso no rodapé da carta (a carta continua inteira ao lado)"""
    y0, y1, x0, x1 = caixa
    def f():
        r = cv2.imread(png(nome))[y0:y1, x0:x1]; r = cv2.resize(r, None, fx=2.6, fy=2.6, interpolation=cv2.INTER_LANCZOS4)
        return V1.matte(lambda b: M.impressa(b, r, 540, 400, r.shape[1], 0, fitas=((-.93, -1, -8), (.93, -1, 8)), seed=31)[0])
    return guardado(f'lupa|{nome}|{caixa}|v1', f)

def retrato(alt, seed=4):
    """foto enviada pelo fundador, em recorte P&B do kit (escala uniforme: sem deformação)"""
    f, m = cv2.imread(FOTO[0]), cv2.imread(FOTO[1], 0)
    k = hashlib.md5(open(FOTO[0], 'rb').read() + open(FOTO[1], 'rb').read()).hexdigest()
    return guardado(f'foto|{k}|{alt}|{seed}', lambda: V1.matte(lambda b: recorte(b, f, m, 540, 1350 - alt - 120, alt, 0, seed=seed)))

SELO, FAIXA = V1.SELO, V1.FAIXA

def etiqueta(txt, seed=90):
    """etiqueta preta pequena (contador): papel rasgado preto com o texto branco"""
    rgb, a = txt; h, w = a.shape; PW, PH = w + 56, h + 30
    pr, pa = V1.creme(PW, PH, (22, 16, 14), seed); A = a[..., None]
    pr[15:15 + h, 28:28 + w] = pr[15:15 + h, 28:28 + w] * (1 - A) + rgb * A
    return pr, pa

# ---------------- textos (fontes do kit, Chrome) ----------------
V1.TXT.clear(); T = V1.T
big, rb, mao, geist = V1.big, V1.rb, V1.mao, V1.geist
bc = lambda s, fs=44, cor='#111': f'<div class="e bc" style="position:relative;font-size:{fs}px;color:{cor}">{s}</div>'

T('h1', big('VOCÊ JÁ VIU', 82) + big('ESTA ARTE.', 82, ROSA))
T('h2', big('MAS SABE', 78) + big('QUEM PINTOU?', 78, ROSA))
T('creditos', rb('Nos créditos das cartas:', 40) + big('WILLIAN MURAI', 84))
T('site', rb('No site dele, assina:', 40) + big('WILL MURAI', 96, ROSA))
T('este', big('ESTE É ELE.', 76, '#fff'))
T('nomegrande', big('WILL', 170) + big('MURAI', 170, ROSA))
T('ilustrador', big('ILUSTRADOR', 84))
T('concept', big('E CONCEPT ARTIST', 58, ROSA))
T('brasil', '<div class="e" style="position:relative;font-family:CB;font-size:58px;color:#fff">Do Brasil</div>')
T('calif', rb('Brasileiro; em 2021, vivia<br>na Califórnia (EUA).', 40))
T('califf', geist('Fontes: willmurai.com/about · Threadless (2021) · Polymanga'))
T('trabalhou', rb('Já trabalhou com', 52))
for k, s in (('wotc', 'WIZARDS OF THE COAST'), ('bliz', 'BLIZZARD'), ('phx', 'PHOENIX LABS')): T(k, big(s, 60))
T('trabf', geist('Fonte: willmurai.com/about'))
T('antes', rb('Antes dos videogames,', 50) + rb('passou por:', 50))
for k, s in (('t1', 'QUADRINHOS'), ('t2', 'PUBLICIDADE'), ('t3', 'EDITORAS')): T(k, big(s, 74))
T('t4', big('VIDEOGAMES', 80, ROSA))
T('tf', geist('Fonte: entrevista a Shoutout LA'))
T('magic1', rb('E no Magic?', 56))
T('magic2', big('54 ILUSTRAÇÕES', 84, ROSA))
T('magic3', rb('creditadas a ele no Scryfall.', 44))
T('magic4', rb('Vamos ver <b>todas.</b>', 52))
T('volta1', rb('De volta às cartas:', 54))
T('volta2', big('FALTAM 46.', 110, ROSA))

HEROIS = ['Master Biomancer', 'Prime Speaker Zegana', 'Reflector Mage', 'Gideon, Battle-Forged', "Nissa, Nature's Artisan", 'Wrath of God']
GALERIA = [('Ravnica · 2012–2013', ['Blustersquall', 'Boros Elite', 'Frontline Medic', 'Scion of Vitu-Ghazi', 'Fluxcharger', 'Lavinia of the Tenth']),
           ('Theros · 2013–2014', ['Anax and Cymede', 'Battlewise Hoplite', 'Archetype of Courage', 'Hero of Iroas', 'Banishing Light', 'Dreadbringer Lampads']),
           ('Tarkir · 2014–2015', ['Jeering Instigator|KTK', 'Mardu Woe-Reaper', 'Valorous Stance', 'Ojutai Exemplars', 'Dragon Tempest', "Ojutai's Command"]),
           ('Zendikar · 2015–2016', ['Inspired Charge', 'Lifespring Druid', 'Hero of Goma Fada', 'Comparative Analysis', 'Untamed Hunger', 'Akoum Flameseeker']),
           ('Innistrad · 2016', ['Macabre Waltz', 'Triskaidekaphobia', 'Stensia Masquerade']),
           ('Magic Origins · 2015', ['Kytheon, Hero of Akros', 'Aspiring Aeronaut'])]
MONTAGEM = [['Brainstorm'], ['Banisher Priest'], ['Divination', "Heroes' Podium"], ['Aspect of Gorgon'], ['Nightmarish End'],
            ['Impulsive Charge', 'Spirit Bonds'], ['Aeronaut Tinkerer'], ['Jeering Instigator|UGIN'], ['Wandering Champion', 'Dragonscale General'],
            ['Sandcrafter Mage'], ['Negate'], ['Arjun, the Shifting Flame', 'Nausea'], ['Kynaios and Tiro of Meletis']]
# duas ilustrações diferentes de Jeering Instigator (KTK 113 e UGIN 113): o nome leva o set
for x in CAT:
    if x['nome'] == 'Jeering Instigator': POR_NOME[f"Jeering Instigator|{x['set']}"] = x
GANCHO = ['Vendilion Clique', 'Saheeli Rai']
_todas = GANCHO + HEROIS + [c for _, g in GALERIA for c in g] + [c for g in MONTAGEM for c in g]
assert len(_todas) == len(set(_todas)) == len(CAT), (len(_todas), len(set(_todas)), len(CAT))
assert {POR_NOME[n]['ilustracao'] for n in _todas} == {x['ilustracao'] for x in CAT}, 'catálogo e montagem não coincidem'
ORDEM = {n: i + 1 for i, n in enumerate(_todas)}  # nº da ilustração no contador = ordem de aparição

def ficha_txt(n):
    x = POR_NOME[n]; return f"{x['set_nome']} · {x['ano']} · nº {x['numero']}"
for i, n in enumerate(HEROIS):
    T(f'hl{i}', rb(n.split('|')[0], 46) + geist(ficha_txt(n), 24))
for k in range(1, 55): T(f'n{k}', bc(f'{k} / 54', 56, '#fff'))
for i, (rot, _) in enumerate(GALERIA): T(f'g{i}', mao(rot, 60))
T('m54', big('54', 200, ROSA))
T('m54b', big('ILUSTRAÇÕES', 74))
T('m54c', rb('em 53 cartas de Magic · de 2012 a 2016', 34))
T('m54f', geist('Scryfall, consulta de 26/11/2026 · 53 cartas, uma delas com duas faces ilustradas'))
T('lado1', big('MAS EXISTE UM LADO', 64, '#fff'))
T('lado2', big('MAIS PESSOAL.', 96, AMAR))
T('ger1', rb('Ele é de', 52))
T('ger2', big('TERCEIRA GERAÇÃO', 66))
T('ger3', big('JAPONESA.', 100, ROSA))
T('nasc1', big('NASCEU E CRESCEU', 64))
T('nasc2', big('NO BRASIL.', 100, ROSA))
T('kanji', '<div style="position:relative;font-family:JP,\'Noto Serif CJK JP\',serif;font-weight:900;font-size:290px;line-height:1;color:#111">秀樹</div>')
T('hideki', big('HIDEKI', 110, ROSA))
T('avo', mao('o nome do meio, dado pela avó', 60))
T('avo2', rb('A avó foi a primeira da família<br>a ir do Japão para o Brasil.', 42))
T('rota', mao('do Japão ao Brasil', 60))
T('avof', geist('Fontes: willmurai.com/about · entrevista à Threadless'))
T('url', geist('willmurai.com/about', 30, '#555'))
T('site1', rb('No próprio site, ele conta que<br>vem explorando a <b>cultura</b> e a<br><b>história dos antepassados</b>.', 50))
T('hom1', rb('E diz que o site é uma', 56))
T('hom2', big('HOMENAGEM', 92, ROSA))
T('hom3', rb('a essa herança.', 56))
for k, s in (('ink1', 'Momotaro'), ('ink2', 'Zen'), ('ink3', 'Chrysanthemum')): T(k, mao(s, 52))
T('inkf', geist('Títulos de desenhos da série Inktober (loja INPRNT do artista)'))
T('nome', big('WILL MURAI', 104))
T('capa54', rb('<b>54 ilustrações</b> nas cartas de Magic', 46))
T('por1', rb('o artista por trás', 50))
T('por2', big('DAS CARTAS.', 92, ROSA))
cred = ('Arte das cartas: Willian Murai · © Wizards of the Coast · Conteúdo de fã não oficial<br>'
        '54 ilustrações: Scryfall (26/11/2026) · Fontes: willmurai.com, Shoutout LA, Threadless, Polymanga')
if FOTO: cred += '<br>Foto: reprodução, enviada pelo fundador (via @magic.cg) · uso privado até autorização'
T('cred', '<div style="position:relative;font-family:Geist;font-weight:500;font-size:19px;line-height:1.4;color:#D9D2C4;text-align:center">' + cred + '</div>')
T('alem', '<div class="e ab" style="position:relative;font-size:62px;line-height:1.1;padding-top:10px;color:#111;text-align:center">O ARTISTA POR TRÁS<br><span style="color:#E61E6E">DAS CARTAS</span></div>')

def textos():
    chave = hashlib.md5((V1.CSS + json.dumps(V1.TXT, sort_keys=True)).encode()).hexdigest()[:16]
    f = os.path.join(MEM, f'textos_{chave}.npz')
    if os.path.exists(f):
        z = np.load(f); return {k[:-4]: (z[k], z[k[:-4] + '_a']) for k in z.files if k.endswith('_rgb')}
    tx = asyncio.run(V1._render_textos())
    np.savez(f, **{k + '_rgb': v[0] for k, v in tx.items()}, **{k + '_a': v[1] for k, v in tx.items()}); return tx

# ---------------- elementos com nome (a chave do cache de cada cena) ----------------
class E(V1.E):
    def __init__(s, nome, peca, cx, cy, t0, modo='bate', ang=0.0, esc=1.0, som=None, treme=True):
        super().__init__(peca, cx, cy, t0, modo, ang, esc, som); s.nome, s.treme = nome, treme
    fim = None  # contador: sai quando o seguinte já está carimbado
    def chave(s):  # inclui o conteúdo da peça: texto ou imagem novos invalidam a cena
        h = hashlib.md5(s.a[::3, ::3].tobytes() + s.rgb[::5, ::5].tobytes()).hexdigest()[:10]
        return f'{s.nome}|{h}|{s.cx:.1f}|{s.cy:.1f}|{s.t0:.3f}|{s.modo}|{s.ang}|{s.esc}|{s.som}|{s.fim}'

def cenas(TX):
    tx = lambda k: TX[k]
    P = lambda nm, **kw: V1.em_papel(TX[nm], **kw)
    S = []  # (t0, muro, [E])
    def cena(t0, els, muro=None): S.append((t0, len(S) % 3 if muro is None else muro, els))
    # 0–2,4 · gancho: quadro 0 = Vendilion Clique inteira já colada; o selo carimba; a pergunta
    cena(0.0, [E('c:Vendilion Clique', carta('Vendilion Clique', 560), CX, 800, -.2, 'bate', -1.5, som=''),
               E('selo', SELO, 290, 300, .45, 'carimbo', -3), E('h1', P('h1', seed=2), CX, 1410, 1.0, 'bate', 1.5)])
    # 2,4–5,4 · lupa no crédito impresso (descoberta: 2,7 s)
    cena(2.4, [E('c:Vendilion Clique', carta('Vendilion Clique', 440), CX - 160, 680, 0, 'surge', -1.5, som=''),
               E('lupa', lupa('Vendilion Clique', (962, 1010, 28, 300)), CX + 40, 1170, 2.55, 'bate', 2),
               E('h2', P('h2', seed=3), CX, 1405, 3.5, 'bate', -1.5)])
    # 5,4–8,4 · Willian → Will (a Saheeli entra como segunda prova)
    cena(5.4, [E('c:Saheeli Rai', carta('Saheeli Rai', 340), CX + 220, 560, 5.45, 'bate', 3),
               E('creditos', P('creditos', seed=4), CX - 40, 980, 5.9, 'bate', -1.5),
               E('site', P('site', tipo='kraft', k=1, seed=5), CX + 10, 1290, 7.1, 'bate', 1.5)])
    t = 8.4
    # 8,4–13,4 · quem é: com foto, o retrato entra aqui (depois do nome); sem foto, o nome vira cartaz
    if FOTO:
        cena(t, [E('foto', retrato(600), CX, 660, t + .03, 'bate', -2), E('este', V1.na_faixa(tx('este')), CX, 1060, t + .7, 'carimbo', -1),
                 E('ilustrador', P('ilustrador', seed=41), CX - 20, 1235, t + 1.5, 'bate', 1.5),
                 E('concept', P('concept', seed=21), CX + 10, 1372, t + 2.1, 'desliza'),
                 E('brasil', P('brasil', tipo='verde', seed=6), CX - 270, 420, t + 2.9, 'bate', -6, som='carimbo')])
    else:
        cena(t, [E('nomegrande', P('nomegrande', pad=(60, 40), seed=43), CX, 680, t + .03, 'bate', -1.5),
                 E('ilustrador', P('ilustrador', seed=41), CX - 20, 1090, t + .9, 'bate', 1.5),
                 E('concept', P('concept', seed=21), CX + 10, 1230, t + 1.5, 'desliza'),
                 E('brasil', P('brasil', tipo='verde', seed=6), CX + 230, 380, t + 2.3, 'bate', -6, som='carimbo')])
    t += 4.2
    # 13,4–16,8 · onde trabalhou (tipografia, sem logótipos)
    cena(t, [E('trabalhou', tx('trabalhou'), CX, 560, t + .03, 'surge'), E('wotc', P('wotc', tipo='kraft', k=0, seed=7), CX, 790, t + .45, 'bate', -2),
             E('bliz', P('bliz', tipo='kraft', k=1, seed=8), CX - 40, 1010, t + 1.1, 'bate', 1.5),
             E('phx', P('phx', tipo='kraft', k=2, seed=9), CX + 30, 1230, t + 1.75, 'bate', -1),
             E('trabf', P('trabf', pad=(24, 14), seed=44), CX, 1400, t + 2.2, 'surge')])
    t += 3.4
    # 16,8–21,6 · linha do tempo
    linha = (np.full((900, 12, 3), (110, 30, 230), np.float32), np.ones((900, 12), np.float32))
    els = [E('antes', tx('antes'), CX, 430, t + .03, 'surge'), E('linha', linha, CX - 330, 1050, t + .4, 'surge', som='')]
    for i, (k, d) in enumerate((('t1', .6), ('t2', 1.5), ('t3', 2.4), ('t4', 3.3))):
        els.append(E(k, P(k, tipo='kraft' if k != 't4' else 'creme', k=i, seed=11 + i), CX + (-60 if i % 2 else 40), 700 + i * 230, t + d, 'bate', (-1.5, 1.5)[i % 2]))
    els.append(E('tf', P('tf', pad=(24, 14), seed=24), CX, 1500, t + 3.8, 'surge')); cena(t, els)
    t += 4.8
    cont = lambda n, t0: E(f'n{ORDEM[n]}', etiqueta(tx(f'n{ORDEM[n]}')), 800, 290, t0, 'carimbo', -1.2, som='', treme=False)
    # ponte para as cartas: o número antes da galeria
    cena(t, [E('magic1', tx('magic1'), CX, 540, t + .03, 'surge'), E('magic2', V1.na_faixa(tx('magic2')), CX, 700, t + .5, 'carimbo', -1, som='revela'),
             E('magic3', tx('magic3'), CX, 860, t + 1.0, 'surge'),
             E('c:g1', carta('Vendilion Clique', 260), CX - 150, 1120, t + 1.5, 'bate', -3), cont('Vendilion Clique', t + 1.5),
             E('c:g2', carta('Saheeli Rai', 260), CX + 150, 1140, t + 1.8, 'bate', 3), cont('Saheeli Rai', t + 1.8),
             E('magic4', P('magic4', tipo='kraft', k=1, seed=45), CX, 1440, t + 2.3, 'bate', 2)])
    t += 3.4
    # A · cartas-herói: uma de cada vez, grande e inteira, com etiqueta (nome, set, ano, nº) fora da arte
    for i, n in enumerate(HEROIS):
        els = [E(f'c:{n}', carta(n, 600), CX + (-12, 14)[i % 2], 830, t, ('bate', 'desliza')[i % 2] if i else 'bate', (-2, 2.5, -1, 1.5, -2.5, 1)[i]),
               E(f'hl{i}', P(f'hl{i}', tipo='kraft', k=i % 3, seed=60 + i), CX, 1360, t + .45, 'bate', (1.5, -1.5)[i % 2], som='zip' if i % 2 else 'tapa'),
               cont(n, t)]
        cena(t, els); t += 1.45
    # lado pessoal (antes da galeria: a galeria cresce até ao clímax e o nome fecha em cima dela)
    cena(t, [E('lado1', V1.na_faixa(tx('lado1')), CX, 820, t + .03, 'bate'), E('lado2', tx('lado2'), CX, 1010, t + .7, 'carimbo')]); t += 2.4
    cena(t, [E('ger1', tx('ger1'), CX, 700, t + .05, 'surge'), E('ger2', tx('ger2'), CX, 830, t + .35, 'desliza'),
             E('ger3', P('ger3', seed=25), CX, 1030, t + .95, 'carimbo', som='revela')]); t += 2.6
    cena(t, [E('nasc1', tx('nasc1'), CX, 720, t + .03, 'desliza'), E('nasc2', P('nasc2', seed=26), CX, 920, t + .7, 'carimbo'),
             E('calif', P('calif', tipo='kraft', k=2, seed=42), CX - 40, 1180, t + 1.4, 'bate', 1),
             E('califf', P('califf', pad=(24, 14), seed=49), CX, 1340, t + 2.0, 'surge'),
             E('brasil2', P('brasil', tipo='verde', seed=6), CX + 230, 540, t + 2.3, 'bate', -4, som='carimbo')]); t += 3.1
    cena(t, [E('kanji', P('kanji', pad=(70, 50), seed=14), CX, 720, t + .03, 'bate', -1.5), E('hideki', P('hideki', seed=27), CX, 1070, t + .8, 'carimbo', som='revela'),
             E('avo', tx('avo'), CX, 1240, t + 1.5, 'revela')]); t += 3.1
    els = [E('avo2', P('avo2', pad=(50, 40), seed=46), CX, 840, t + .03, 'bate', -1), E('avof', P('avof', pad=(24, 14), seed=47), CX, 1040, t + .8, 'surge')]
    if FOTO: els.append(E('foto2', retrato(420, 9), CX + 40, 1330, t + 1.3, 'bate', 3))
    else: els.append(E('rota', P('rota', tipo='kraft', k=0, seed=50), CX - 60, 1230, t + 1.3, 'bate', 4, som='carimbo'))
    cena(t, els); t += 2.8
    cena(t, [E('site1', P('site1', pad=(60, 70), seed=15), CX, 900, t + .03, 'bate', -1), E('url', P('url', pad=(24, 14), seed=28), CX, 640, t + .6, 'surge'),
             E('selo2', SELO, CX - 210, 1240, t + 1.4, 'carimbo', -4)]); t += 3.3
    cena(t, [E('hom1', tx('hom1'), CX, 640, t + .03, 'surge'), E('hom2', P('hom2', seed=29), CX, 790, t + .5, 'carimbo', som='revela'), E('hom3', tx('hom3'), CX, 940, t + 1.0, 'surge'),
             E('ink1', P('ink1', tipo='kraft', k=0, seed=16), CX - 250, 1120, t + 1.6, 'bate', -5), E('ink2', P('ink2', tipo='kraft', k=1, seed=17), CX + 20, 1150, t + 2.0, 'bate', 3),
             E('ink3', P('ink3', tipo='kraft', k=2, seed=18), CX + 200, 1290, t + 2.4, 'bate', -2), E('inkf', P('inkf', pad=(24, 14), seed=30), CX, 1440, t + 2.8, 'surge')]); t += 3.6
    cena(t, [E('volta1', tx('volta1'), CX, 700, t + .03, 'surge'), E('volta2', V1.na_faixa(tx('volta2')), CX, 880, t + .5, 'carimbo', -1, som='revela')]); t += 2.0
    # B · galeria de cartazes por mundo (2×3, 1×3, 1×2): cartas a colar em sequência
    for gi, (rot, cartas) in enumerate(GALERIA):
        n = len(cartas); els = [E(f'g{gi}', P(f'g{gi}', tipo='kraft', k=gi % 3, seed=70 + gi), CX - 140, 380, t, 'bate', -2)]
        if n == 6: larg, pos = 280, [(CX + dx, y) for y in (780, 1220) for dx in (-300, 0, 300)]
        elif n == 3: larg, pos = 280, [(CX - 310, 880), (CX, 960), (CX + 310, 880)]
        else: larg, pos = 400, [(CX - 215, 920), (CX + 215, 920)]
        for j, (c, (x, y)) in enumerate(zip(cartas, pos)):
            t0 = t + .3 + j * .27
            els.append(E(f'c:{c}', carta(c, larg), x, y, t0, 'bate', ((-3, 2, -1.5, 2.5, -2, 1.5)[j]), som='tapa' if j % 2 == 0 else 'zip'))
            els.append(cont(c, t0))
        cena(t, els); t += .3 + n * .27 + .9
    # C · montagem de portfólio: alternância de cartas sozinhas e em pares, contador a subir
    for gi, grupo in enumerate(MONTAGEM):
        if len(grupo) == 1:
            c = grupo[0]; els = [E(f'c:{c}', carta(c, 560), CX + (-15, 15)[gi % 2], 860, t, 'bate', (-2, 2)[gi % 2], som=('tapa', 'zip')[gi % 2])]
            d = .55
        else:
            els = [E(f'c:{c}', carta(c, 400), CX + (-215, 215)[j], 860 + (0, 40)[j], t + j * .22, 'bate', (-3, 3)[j]) for j, c in enumerate(grupo)]
            els += [cont(c, t + j * .22) for j, c in enumerate(grupo)]
            d = .85
        if len(grupo) == 1: els.append(cont(grupo[0], t))
        cena(t, els); t += d
    # D · grande revelação: as 54 em ordem de lançamento, coladas em sequência; depois o número
    ordem = sorted(_todas, key=lambda n: (POR_NOME[n]['ano'], CAT.index(POR_NOME[n])))
    els = []
    lg, cols, dx, dy, y0 = 92, 9, 97, 134, 700
    for i, n in enumerate(ordem):
        r, c = divmod(i, cols); nlin = cols if r < len(ordem) // cols else len(ordem) % cols
        x = CX - (nlin - 1) * dx / 2 + c * dx
        els.append(E(f'm:{n}', carta_nua(n, lg), x, y0 + r * dy, t + .15 + i * .055, 'bate', 0, som='tapa' if i % 4 == 0 else '', treme=False))
    tf = t + .15 + len(ordem) * .055
    els += [E('m54', P('m54', pad=(40, 6), seed=80), CX - 290, 380, tf + .1, 'carimbo', -2, som='revela'),
            E('m54b', tx('m54b'), CX + 150, 360, tf + .55, 'carimbo', -1),
            E('m54c', tx('m54c'), CX, 525, tf + .95, 'surge'),
            E('m54f', P('m54f', pad=(20, 10), seed=81), CX, 592, tf + 1.4, 'surge')]
    cena(t, els, muro=1); t = tf + 2.9
    # assinatura: o nome fica colado às cartas que o espectador acabou de ver
    els = [E('nome', tx('nome'), CX, 560 if FOTO else 470, t + .03, 'carimbo', som='revela'), E('por1', tx('por1'), CX, 680 if FOTO else 600, t + .6, 'surge'),
           E('por2', P('por2', seed=48), CX, 800 if FOTO else 730, t + 1.0, 'carimbo')]
    if FOTO: els.insert(0, E('foto3', retrato(300, 11), CX, 330, t + .05, 'bate', -3))
    else: els.insert(0, E('selo3', SELO, CX, 290, t + .05, 'carimbo', -2))
    for j, c in enumerate(('Vendilion Clique', 'Saheeli Rai', 'Gideon, Battle-Forged')):
        els.append(E(f'f:{c}', carta(c, 260), CX + (j - 1) * 285, 1130 if FOTO else 1090, t + 1.5 + j * .25, 'bate', (-4, 0, 4)[j]))
    els.append(E('cred', V1.na_faixa(tx('cred')), CX, 1440, t + 2.5, 'bate'))
    cena(t, els); t += 5.1
    for _, _, els in S:  # um contador de cada vez
        cs = sorted((e for e in els if e.nome[0] == 'n' and e.nome[1:].isdigit()), key=lambda e: e.t0)
        for a, b in zip(cs, cs[1:]): a.fim = b.t0 + .034
    return S, t

# ---------------- render por cenas (cada cena num segmento com cache) ----------------
def render_cena(i, t0, t1, muro, els, seg, MUROS, batidas):
    V1.BATIDAS = batidas
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', str(FPS), seg + '.tmp.mp4'], stdin=subprocess.PIPE)
    for f in range(round(t0 * FPS), round(t1 * FPS)):
        t = f / FPS; out = MUROS[muro].copy(); cam = V1.camera(t, t0)
        for e in els:
            if e.fim is None or t < e.fim: V1.pinta(out, e, t, cam)
        ff.stdin.write(np.clip(out, 0, 255).astype(np.uint8).tobytes())
    ff.stdin.close(); ff.wait(); os.replace(seg + '.tmp.mp4', seg)

def capa(TX, saida):
    out = V1.muro(5); V1.BATIDAS = []
    P = lambda nm, **kw: V1.em_papel(TX[nm], **kw)
    F = bool(FOTO)
    els = [E('selo', SELO, CX - 220, 300, -9, 'surge', -3), E('nome', TX['nome'], CX, 470, -9, 'surge'),
           E('alem', P('alem', seed=40), CX, 640, -9, 'surge', -1.5)]
    if F: els.append(E('foto', retrato(420, 4), CX, 975, -9, 'surge', -2))
    y, lg = (1390, 250) if F else (1080, 280)
    for j, c in enumerate(('Vendilion Clique', 'Saheeli Rai', 'Gideon, Battle-Forged')):
        els.append(E('c', carta(c, lg), CX + (j - 1) * (lg + 28), y + (0, -24, 0)[j], -9, 'surge', (-4, 0, 4)[j]))
    if not F: els.append(E('capa54', P('capa54', tipo='kraft', k=1, seed=51), CX, 1400, -9, 'surge', 1.5))
    for e in els: V1.pinta(out, e, 0, (1, 0, 0))
    cv2.imwrite(saida, np.clip(out, 0, 255).astype(np.uint8)); print('capa', saida)

if __name__ == '__main__':
    TX = textos()
    if CAPA: capa(TX, CAPA)
    S, DUR = cenas(TX)
    V1.DUR = DUR
    if '--roteiro' in arg:  # mapa de cenas para a ficha (sem render)
        for i, (t0, _, els) in enumerate(S):
            print(f"{i:02d} {t0:6.2f} " + ' '.join(f"{e.nome}@{e.t0:.2f}" for e in els if not e.nome.startswith(('n', 'm:')) or not e.nome[1:].isdigit() and not e.nome.startswith('m:')))
        print('fim', round(DUR, 2)); sys.exit()
    batidas = [e.t0 + (.16 if e.modo == 'bate' else .1) for _, _, els in S for e in els if e.modo in ('bate', 'carimbo') and e.treme]
    MUROS = [V1.muro(3 + i) for i in range(3)]
    segs = []
    for i, (t0, muro, els) in enumerate(S):
        t1 = S[i + 1][0] if i + 1 < len(S) else DUR
        k = hashlib.md5(f'{VAR}|{t0:.3f}|{t1:.3f}|{muro}|v2|'.encode() + '\n'.join(e.chave() for e in els).encode()
                        + str([b for b in batidas if t0 - .3 <= b < t1]).encode()).hexdigest()[:12]
        seg = os.path.join(MEM, f'cena{i:02d}_{k}.mp4'); segs.append(seg)
        if os.path.exists(seg) and (SO_CENAS is None or i not in SO_CENAS): continue
        print(f'cena {i:02d} · {t0:6.2f}–{t1:6.2f} s · {len(els)} elementos', flush=True)
        render_cena(i, t0, t1, muro, els, seg, MUROS, batidas)
    lst = os.path.join(MEM, f'lista_{VAR}.txt'); open(lst, 'w').write(''.join(f"file '{s}'\n" for s in segs))
    corpo = OUT.replace('.mp4', '_corpo.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', corpo], check=True)
    # som: efeitos sintetizados de reel.py (tapa, carimbo, zip, revela, corte) nos tempos de cada entrada
    SD = {t0: els for t0, _, els in S}
    wav = OUT.replace('.mp4', '_som.wav'); a = (V1.trilha(SD) * 32767).astype(np.int16)
    with wave.open(wav, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(V1.SR); w.writeframes(a.tobytes())
    # efeitos com pico ≤ −6 dBFS de amostra no ficheiro final (bíblia do Lambe-lambe); compressão densa para ~ −14 LUFS (QC); pico verdadeiro < −1 dBTP
    def lufs(cad):
        r = subprocess.run(['ffmpeg', '-nostats', '-i', wav, '-af', cad + ',ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
        return float(r.rsplit('I:', 1)[1].split('LUFS')[0])
    # reamostrar ANTES de limitar (a reamostragem depois do limitador criava picos de −4 dBFS) e cortar o agudo
    # que o AAC faz transbordar; limite 0,42 → pico final ≈ −6,3 dBFS depois do AAC (medido em 26/11/2026)
    base = 'aresample=48000,acompressor=threshold=-32dB:ratio=12:attack=2:release=250:makeup=8'
    lim = 'lowpass=f=11000:poles=2,alimiter=limit=0.42:level=false:attack=3:release=60,alimiter=limit=0.42:level=false:attack=0.5,lowpass=f=15000'
    g = 14.0
    for _ in range(3):
        g = min(20.0, g + (-14.3 - lufs(f'{base},volume={g:.2f}dB,{lim}')))
    AUD = f'{base},volume={g:.2f}dB,{lim}'
    print('som do corpo:', round(lufs(AUD), 1), 'LUFS (ganho', round(g, 1), 'dB)')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', corpo, '-i', V1.FECHO, '-i', wav, '-filter_complex',
                    '[0:v]setsar=1[a];[1:v]scale=1080:1920,setsar=1,fps=30[b];[a][b]concat=n=2:v=1:a=0[v];'
                    '[2:a]%s,apad=whole_dur=%.3f[s]' % (AUD, DUR + 3.867),
                    '-map', '[v]', '-map', '[s]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', OUT], check=True)
    os.remove(corpo)
    r = subprocess.run(['ffmpeg', '-nostats', '-i', OUT, '-t', f'{DUR:.2f}', '-vn', '-af', 'astats=measure_overall=Peak_level:measure_perchannel=0', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    pk = float(r.rsplit('Peak level dB:', 1)[1].split()[0]); print(f'pico de amostra no ficheiro final: {pk:.1f} dBFS', '(OK)' if pk <= -6 else '(ACIMA DE −6 dBFS)')
    # folha de contacto: 2 quadros por segundo, páginas de 8×4 (para ver o vídeo inteiro a olho)
    folha = OUT.replace('.mp4', '_folha_%02d.jpg')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', OUT, '-vf', "fps=2,scale=180:320,drawtext=text='%{pts\\:hms}':x=4:y=4:fontsize=16:fontcolor=white:box=1:boxcolor=black@0.6,tile=8x4",
                    '-q:v', '3', folha], check=True)
    print('ok', OUT, f'{DUR:.2f} s + fecho')
