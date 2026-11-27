"""LL-ART21 V4 · Will Murai, no padrão de vídeo do Lambe-lambe (refino da V3, pedido do fundador 26/11 23:27).
Foto do artista em cartaz P&B fotocopiado; cartas uma de cada vez, grandes, coladas umas por cima das outras, recortadas à mão (margem branca
cortada à tesoura, carta inteira por dentro).
Factos = os da V1/V2 (fontes.md, fontes_v2.md); cartas = cache do catalogo_cartas.py (54 ilustrações, Scryfall 26/11/2026).
Uso: python3 -I reel_v4.py <cache_catalogo> <saida.mp4> [--foto retrato.png] [--mudo]   (sem --foto: versão sem retrato)
Zero créditos externos; obras pessoais do artista não reproduzidas (só títulos em texto)."""
import sys, os, json
import cv2, numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(AQUI, '../../kit_video')))
import motor_video as V
from motor_video import Peca, T, caixa, peca_folha, peca_carta, peca_img, matte, PRETO, M, CW, CH

ARG = [a for a in sys.argv[1:]]
CACHE = os.path.abspath(ARG[0]); SAIDA = os.path.abspath(ARG[1])
FOTO = os.path.abspath(ARG[ARG.index('--foto') + 1]) if '--foto' in ARG else None
FUNDO = 'verde' if '--verde' in ARG else 'preto'      # --verde: cartazes de fundo verde-esmeralda do LL-ECO01 (fundador, 26/11 23:56)
CAT = json.load(open(os.path.join(CACHE, 'catalogo.json')))
def png(nome, s=None):
    x = [c for c in CAT if c['nome'] == nome and (s is None or c['set'] == s)][0]
    return os.path.join(CACHE, 'cartas', x['ilustracao'] + '.png')

F2 = ((-.94, -1, -40), (.94, -1, 40))
def RB(txt, fs, cor=PRETO, w=880): return T(txt, fs, cor, 'RB', 'font-weight:900;font-style:italic;', w=w)
def CB(txt, fs, cor=PRETO, w=600): return f'<div class="e" style="position:relative;font-family:CB;font-size:{fs}px;line-height:1;color:{cor};text-align:center;width:{w}px">{txt}</div>'
def GE(txt, fs=22, cor='#2a2a2a', w=900): return f'<div style="position:relative;font-family:Geist;font-weight:500;font-size:{fs}px;line-height:1.35;color:{cor};text-align:center;width:{w}px">{txt}</div>'

t = {}
t['a1'] = caixa(860, 240, T('Você já viu<br>esta arte.', 92, w=860))
t['a2'] = caixa(880, 130, T('Mas sabe quem <span class="k">pintou?</span>', 62, '#fff', w=880))
t['b1'] = caixa(860, 130, T('Nos créditos da carta:', 54, w=860))
t['b_ring'] = caixa(860, 220, V.svg(860, 220, '<ellipse cx="617" cy="95" rx="205" ry="40" fill="none" stroke="#E61E6E" stroke-width="8" transform="rotate(-2 617 95)"/>'))
t['b2'] = caixa(860, 150, T('Willian Murai', 88, w=860, extra='white-space:nowrap;'))
t['b3'] = caixa(900, 190, '<div style="text-align:center"><div style="font-family:RB;font-weight:800;font-size:40px;color:#fff">No site dele, assina:</div>'
                 '<div style="font-family:AB;font-size:96px;line-height:1.05;color:#10B981;text-transform:uppercase;letter-spacing:-1px">Will Murai</div></div>')
t['c1'] = caixa(900, 200, T('Will<br>Murai', 120, '#fff', w=900))
t['c_br'] = caixa(260, 90, CB('Do Brasil', 62, '#fff', 260))
t['c2'] = caixa(860, 170, T('Ilustrador e<br><span class="k">concept artist</span>', 70, w=860))
t['c3'] = caixa(700, 90, RB('Já trabalhou com', 52, PRETO, 700))
for k, s in (('c4', 'Wizards of the Coast'), ('c5', 'Blizzard'), ('c6', 'Phoenix Labs')):
    t[k] = caixa(760, 100, T(s, 52, '#fff', w=760, extra='white-space:nowrap;'))
t['d1'] = caixa(880, 200, T('Antes dos videogames,<br>passou por:', 66, w=880))
for k, s in (('d2', 'Quadrinhos'), ('d3', 'Publicidade'), ('d4', 'Editoras'), ('d5', 'Videogames')):
    t[k] = caixa(560, 110, T(s, 70, PRETO, w=560))
t['seta'] = caixa(170, 120, V.svg(170, 120, '<path d="M14 20 C 70 20, 120 40, 140 96" stroke="#E61E6E" stroke-width="11" fill="none" stroke-linecap="round"/>'
                                   '<path d="M112 86 L142 104 L156 70" stroke="#E61E6E" stroke-width="11" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'))
t['seta2'] = caixa(170, 120, V.svg(170, 120, '<path d="M156 20 C 100 20, 50 40, 30 96" stroke="#E61E6E" stroke-width="11" fill="none" stroke-linecap="round"/>'
                                    '<path d="M58 86 L28 104 L14 70" stroke="#E61E6E" stroke-width="11" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'))
t['d6'] = caixa(760, 50, GE('Fonte: entrevista de Will Murai à Shoutout LA', 22))
t['e1'] = caixa(760, 110, T('E no Magic?', 84, w=760))
t['e2'] = caixa(900, 180, '<div style="text-align:center"><div style="font-family:AB;font-size:92px;line-height:1;color:#FFD84A;letter-spacing:-2px;white-space:nowrap">54 ILUSTRAÇÕES</div>'
                 '<div style="margin-top:12px;font-family:RB;font-weight:800;font-size:40px;color:#fff">creditadas a ele no Scryfall</div></div>')
t['e3'] = caixa(760, 50, GE('Contagem por ilustração no Scryfall, 26/11/2026', 22))
t['f1'] = caixa(900, 230, T('Mas existe um lado<br><span style="color:#FFD84A">mais pessoal.</span>', 84, '#fff', w=900))
t['f2'] = caixa(900, 220, T('Ele é de<br><span class="k">terceira geração<br>japonesa.</span>', 74, w=900))
t['f3'] = caixa(880, 170, T('Nasceu e cresceu<br>no Brasil.', 72, PRETO, w=880))
t['g1'] = caixa(640, 380, '<div style="font-family:JP,\'Noto Serif CJK JP\',serif;font-weight:900;font-size:300px;line-height:1;color:#111;text-align:center">秀樹</div>')
t['g2'] = caixa(760, 150, T('Hideki', 130, '#fff', w=760))
t['g3'] = caixa(700, 110, CB('o nome do meio, dado pela avó', 50, PRETO, 700))
t['h1'] = caixa(900, 300, T('No próprio site, ele conta que explora a <span class="k">cultura e a história</span> dos antepassados.', 58, w=900))
t['h2'] = caixa(900, 210, T('E diz que o site é uma <span class="g">homenagem</span> a essa herança.', 60, '#fff', w=900))
for k, s, w in (('h3', 'Momotaro', 300), ('h4', 'Zen', 180), ('h5', 'Chrysanthemum', 420)):
    t[k] = caixa(w, 90, CB(s, 62, PRETO, w))
t['h6'] = caixa(860, 70, GE('Títulos da série Inktober na loja do artista (INPRNT) · fonte: willmurai.com/about', 21, w=860))
t['i1'] = caixa(900, 120, T('54 ilustrações · 2012 a 2016', 50, w=900, extra='white-space:nowrap;'))
t['i2'] = caixa(900, 170, T('Das cartas de Magic<br><span class="g">à própria história.</span>', 66, '#fff', w=900))
t['j1'] = caixa(900, 300, T('Will<br>Murai', 170, '#fff', w=900))
t['j2'] = caixa(860, 90, RB('Um artista, muitos universos.', 54, '#FFD84A', 860))
t['j3'] = caixa(900, 110, GE('Cartas: ilustrações de Willian Murai · © Wizards of the Coast. Fontes: Scryfall (26/11/2026), willmurai.com/about, Shoutout LA.<br>'
                            'Obras pessoais do artista não reproduzidas. Sem afiliação com a Wizards of the Coast.', 19, '#C9C2B4', 900))

t['c_br2'] = caixa(260, 90, CB('Do Brasil', 62, PRETO, 260))
t['este'] = caixa(620, 110, RB('Este é ele.', 64, PRETO, 620))
t['e0'] = caixa(900, 120, T('E no Magic? <span style="color:#FFD84A">54 ilustrações.</span>', 54, '#fff', w=900, extra='white-space:nowrap;'))
t['p0'] = caixa(900, 120, T('E as outras <span class="k">42?</span>', 80, w=900))
t['p1'] = caixa(900, 120, T('Uma por cima da outra:', 58, w=900))
HEROI = [('Master Biomancer', 'Ravnica · Gatecrash', '2013'), ('Prime Speaker Zegana', 'Ravnica · Gatecrash', '2013'),
         ('Reflector Mage', 'Zendikar · Oath of the Gatewatch', '2016'), ('Gideon, Battle-Forged', 'Magic Origins', '2015'),
         ("Nissa, Nature's Artisan", 'Kaladesh', '2016'), ('Wrath of God', 'From the Vault: Annihilation', '2014')]
for i, (n, s_, a) in enumerate(HEROI):
    t[f'hr{i}'] = caixa(860, 80, f'<div style="text-align:center;font-family:RB;font-weight:900;font-style:italic;font-size:40px;color:#fff;white-space:nowrap">'
                                f'{i + 4}/54 · {n}</div>')
EXTRA = [('Saheeli Rai', 2, 'Saheeli Rai'), ('Brainstorm', 3, 'Brainstorm · a mais antiga no Scryfall (2012)'),
         ('Ojutai Exemplars', 10, 'Ojutai Exemplars'), ("Ojutai's Command", 11, "Ojutai's Command"), ('Kynaios and Tiro of Meletis', 12, 'Kynaios and Tiro of Meletis')]
for n, num, rot in EXTRA:
    t['tag_' + n] = caixa(300, 200, f'<div class="e" style="position:relative;font-family:CB;font-size:46px;line-height:1;color:#050A10;text-align:center;width:280px;white-space:normal">{num}/54<br><span style="font-size:32px">{rot}</span></div>')
V.render_textos()

# ------------------------------------------------------------------ peças novas
carta_recortada = V.peca_carta_recortada   # no kit desde o LL-ART21 V4

def retrato(alt, seed=4):
    """foto enviada pelo fundador: cartaz P&B fotocopiado (recorte_foto do kit, máscara retangular: sem recortar a pessoa)"""
    sys.path.insert(0, V.KIT); from recorte_foto import recorte
    f = cv2.imread(FOTO); m = np.full(f.shape[:2], 255, np.uint8)
    cwd = os.getcwd(); os.chdir(V.KIT)
    try: P = matte(lambda b: recorte(b, f, m, CW / 2, CH / 2 - alt / 2, alt, 0, borda=20, seed=seed))
    finally: os.chdir(cwd)
    return P

vc = cv2.imread(png('Vendilion Clique'))
cred = cv2.resize(vc[975:1032, 18:300], None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
selo = lambda e=.95, a=-3: matte(lambda b: M.selo(b, CW / 2, CH / 2, e, a))
COB = lambda tipo, seed, t0, ang=.6: Peca(peca_folha(1010, 1560, tipo, seed, ang), 540, 950, t0, .40, de=(0, -1900), rot0=5 * np.sign(ang or 1), z0=1.15, som='grande')

L = []; ap = L.append
# 1 · gancho: a carta recortada em tela cheia no quadro 0
ap(Peca(carta_recortada(png('Vendilion Clique'), 520, -1.5, 1), 540, 1010, 0, modo='fixa'))
ap(Peca(peca_folha(900, 270, 'creme', 1, -1.2, t['a1'], fitas=F2), 540, 470, .30, .40, de=(-80, -1500), rot0=-8))
ap(Peca(peca_folha(900, 160, 'preto', 2, 1.0, t['a2'], claro=True), 540, 1440, 1.45, .36, de=(0, 1400), rot0=6))
ap(Peca(selo(.85), 830, 1610, 1.95, .22, modo='pop', som='pop'))
# 2 · o crédito
ap(COB('kraft', 6, 3.20, -.6))
ap(Peca(peca_folha(900, 160, 'creme', 7, 1.2, t['b1'], fitas=F2), 540, 500, 3.42, .34, de=(900, -200), rot0=12))
ap(Peca(peca_img(cred, 846, ang=-2, margem=22, fundo=(30, 22, 18), seed=8, fitas=((-1, -1, -40), (1, -1, 40))), 540, 790, 3.75, .34, de=(-900, 100), rot0=-10))
ap(Peca(matte(lambda b: V.tinta(np.ascontiguousarray(b), t['b_ring'], claro=True)), 540, 790, 4.20, .25, modo='carimbo', som='pop'))
ap(Peca(peca_folha(860, 170, 'amarelo', 9, 1.5, t['b2']), 540, 1050, 4.55, .30, de=(900, -100), rot0=10))
ap(Peca(peca_folha(920, 230, 'preto', 10, -1, t['b3'], claro=True), 540, 1330, 5.35, .32, de=(0, 1400), rot0=5))
# 3 · quem é (com foto: o retrato é o cartaz principal)
ap(COB('creme', 11, 6.80, .7))
if FOTO:
    ap(Peca(retrato(560), 540, 700, 7.02, .40, de=(0, -1500), rot0=-6))
    ap(Peca(peca_folha(640, 120, 'amarelo', 58, -3, t['este']), 330, 1030, 7.75, .2, modo='carimbo', som='pop'))
    ap(Peca(peca_folha(900, 300, 'preto', 12, -1, t['c1'], claro=True), 540, 1240, 8.20, .34, de=(900, 0), rot0=8))
    ap(Peca(peca_folha(280, 110, 'verde', 13, -6, t['c_br'], claro=True), 830, 1095, 8.70, .22, modo='pop', ang=-6, som='pop'))
    ap(Peca(peca_folha(880, 200, 'kraft', 14, 1, t['c2'], fitas=F2), 540, 1470, 9.20, .32, de=(-900, 0), rot0=-8))
else:
    ap(Peca(peca_folha(900, 300, 'preto', 12, -1, t['c1'], claro=True), 540, 560, 7.02, .36, de=(-900, -200), rot0=-10))
    ap(Peca(peca_folha(280, 110, 'verde', 13, -6, t['c_br'], claro=True), 830, 420, 7.55, .22, modo='pop', ang=-6, som='pop'))
    ap(Peca(peca_folha(880, 200, 'kraft', 14, 1, t['c2'], fitas=F2), 540, 860, 7.95, .32, de=(900, 0), rot0=8))
def carta_info(nome, x, y, larg, t0, ang, seed, lado=1):
    """carta recortada + autocolante amarelo ao lado com nº e nome (fora da carta)"""
    ap(Peca(carta_recortada(png(nome), larg, ang, seed), x, y, t0, .30, de=(-900 * lado, 300), rot0=10 * lado))
    ap(Peca(peca_folha(300, 210, 'amarelo', seed + 300, 4 * lado, t['tag_' + nome]), x + lado * (larg / 2 + 165), y - 40, t0 + .3, .2, modo='pop', ang=4 * lado, som='pop'))

# 4 · com quem trabalhou (+ Saheeli Rai: trabalho para a Wizards)
ap(COB('kraft', 59, 10.40, -.5))
ap(Peca(peca_folha(720, 100, 'creme', 15, -1, t['c3']), 540, 420, 10.62, .18, modo='carimbo', som='pop'))
for i, (k, y) in enumerate((('c4', 545), ('c5', 670), ('c6', 795))):
    ap(Peca(peca_folha(780, 120, 'preto', 16 + i, (-1) ** i * 1.2, t[k], claro=True), 540, y, 10.85 + .3 * i, .26, de=(900 * (-1) ** i, 0), rot0=8 * (-1) ** i))
carta_info('Saheeli Rai', 380, 1170, 360, 11.75, -2, 71)
# 5 · o percurso (+ Brainstorm, a ilustração mais antiga dele no Scryfall)
ap(COB('creme', 19, 12.90, -.5))
ap(Peca(peca_folha(900, 230, 'kraft', 20, -1.2, t['d1'], fitas=F2), 540, 420, 13.12, .34, de=(900, -300), rot0=10))
for i, (k, (x, y)) in enumerate(zip(('d2', 'd3', 'd4', 'd5'), ((330, 600), (750, 715), (330, 830), (750, 945)))):
    ap(Peca(peca_folha(480, 120, 'amarelo' if k == 'd5' else 'creme', 21 + i, (-1) ** i * 2, t[k]), x, y, 13.55 + .42 * i, .26, de=(-900 * (-1) ** i, 0), rot0=-10 * (-1) ** i))
ap(Peca(peca_folha(780, 60, 'creme', 30, 0, t['d6']), 540, 1035, 15.0, .2, modo='carimbo', som='nada'))
carta_info('Brainstorm', 380, 1305, 280, 15.3, 2, 72)
# 6 · no Magic: seis cartas-herói, uma de cada vez, grandes, coladas por cima
ap(COB('kraft', 31, 16.40, .6))
ap(Peca(peca_folha(960, 140, 'preto', 33, -1, t['e0'], claro=True), 540, 360, 16.62, .30, de=(-900, 0), rot0=-8))
for i, (n, _, _) in enumerate(HEROI):
    t0 = 17.10 + 1.05 * i
    ap(Peca(carta_recortada(png(n), 600, (-2.5, 2, -1, 3, -2, 1.5)[i], 10 + i), 540 + (-14, 12, -6, 16, -10, 8)[i], 1000, t0, .30,
            de=((-900, -500), (900, -400), (-700, 600), (800, 500), (0, -1500), (-900, 0))[i], rot0=(12, -12, 9, -10, 7, -8)[i]))
    ap(Peca(peca_folha(860, 90, 'preto', 60 + i, (-1) ** i * .8, t[f'hr{i}'], claro=True), 540, 1475, t0 + .25, .18, modo='carimbo', som='nada'))
ap(Peca(peca_folha(780, 60, 'creme', 34, 0, t['e3']), 540, 455, 17.0, .2, modo='carimbo', som='nada'))
# 7 · o lado pessoal (+ Ojutai Exemplars)
ap(Peca(peca_folha(1040, 1640, FUNDO, 35, .4), 540, 955, 23.60, .40, de=(0, -1900), rot0=4, z0=1.15, som='grande'))
ap(Peca(peca_folha(940, 250, 'preto', 36, 0, t['f1'], claro=True), 540, 410, 23.85, .2, modo='carimbo', som='pop'))
ap(Peca(peca_folha(900, 260, 'creme', 37, -1.5, t['f2'], fitas=F2), 540, 665, 24.65, .34, de=(-900, -100), rot0=-10))
ap(Peca(peca_folha(900, 200, 'kraft', 38, 1.2, t['f3']), 540, 890, 25.55, .32, de=(900, 100), rot0=8))
ap(Peca(peca_folha(280, 110, 'amarelo', 39, 5, t['c_br2']) if FUNDO == 'verde' else peca_folha(280, 110, 'verde', 39, 5, t['c_br'], claro=True), 830, 1015, 26.0, .22, modo='pop', ang=5, som='pop'))
carta_info('Ojutai Exemplars', 380, 1280, 320, 26.3, -2, 73)
# 8 · Hideki (+ Ojutai's Command)
ap(COB('creme', 40, 27.80, -.6))
ap(Peca(peca_folha(680, 420, 'kraft', 41, -1, t['g1'], fitas=F2), 540, 540, 28.05, .34, de=(0, -1500), rot0=-8))
ap(Peca(peca_folha(780, 180, 'preto', 42, 1, t['g2'], claro=True), 540, 850, 28.6, .30, de=(900, 0), rot0=8))
ap(Peca(peca_folha(720, 130, 'creme', 43, -2, t['g3']), 540, 1000, 29.1, .2, modo='carimbo', som='pop'))
carta_info("Ojutai's Command", 700, 1265, 300, 29.6, 2, 74, lado=-1)
# 9 · a herança (+ Kynaios and Tiro of Meletis)
ap(COB('kraft', 44, 31.10, .7))
ap(Peca(peca_folha(940, 330, 'creme', 45, -1, t['h1'], fitas=F2), 540, 435, 31.32, .34, de=(-900, -200), rot0=-10))
ap(Peca(peca_folha(940, 240, 'preto', 46, 1, t['h2'], claro=True), 540, 700, 32.4, .32, de=(900, 0), rot0=8))
for i, (k, x, w) in enumerate((('h3', 240, 320), ('h4', 520, 200), ('h5', 780, 440))):
    ap(Peca(peca_folha(w, 110, 'creme', 47 + i, (-1) ** i * 4, t[k]), x, 885 + 30 * (i == 2), 33.1 + .2 * i, .2, modo='pop', ang=(-1) ** i * 4, som='pop'))
ap(Peca(peca_folha(880, 80, 'creme', 50, 0, t['h6']), 540, 995, 33.6, .2, modo='carimbo', som='nada'))
carta_info('Kynaios and Tiro of Meletis', 380, 1295, 300, 33.9, -2, 75)
# 10 · as outras 47: uma por cima da outra, em ordem de lançamento
ap(COB('creme', 51, 35.70, .4))
ap(Peca(peca_folha(900, 130, 'kraft', 52, -1, t['p0'], fitas=F2), 540, 360, 35.92, .30, de=(-900, 0), rot0=-8))
usadas = {'Vendilion Clique'} | {n for n, _, _ in HEROI} | {n for n, _, _ in EXTRA}
assert len(CAT) - len(usadas) == 42, len(CAT) - len(usadas)
resto = [c for c in CAT if c['nome'] not in usadas]
rng = np.random.default_rng(7)
for k, c in enumerate(resto):
    t0 = 36.25 + .125 * k
    ap(Peca(carta_recortada(os.path.join(CACHE, 'cartas', c['ilustracao'] + '.png'), 560, rng.uniform(-5, 5), 100 + k, fitas=False),
            540 + rng.uniform(-30, 30), 1000 + rng.uniform(-20, 20), t0, .10, de=(rng.uniform(-300, 300), rng.uniform(-400, 400)), rot0=rng.uniform(-10, 10),
            z0=1.12, som='pop' if k % 4 == 0 else 'nada'))
tfim = 36.25 + .125 * len(resto)
ap(Peca(peca_folha(920, 200, 'preto', 53, 1, t['i2'], claro=True), 540, 1470, tfim + .15, .30, de=(0, 1400), rot0=5))
# 11 · assinatura
ts = tfim + 1.6
ap(Peca(peca_folha(1040, 1640, FUNDO, 54, -.4), 540, 955, ts, .40, de=(0, -1900), rot0=-4, z0=1.15, som='grande'))
if FOTO:
    ap(Peca(retrato(430, 9), 540, 640, ts + .25, .34, de=(0, -1500), rot0=6))
    ap(Peca(selo(.8, -6), 830, 380, ts + .7, .22, modo='pop', som='pop'))
    ap(Peca(peca_folha(940, 340, 'preto', 55, 0, t['j1'], claro=True), 540, 1080, ts + .9, .2, modo='carimbo', som='pop'))
    ap(Peca(peca_folha(880, 110, 'preto', 56, 0, t['j2'], claro=True), 540, 1310, ts + 1.5, .2, modo='carimbo', som='pop'))
else:
    ap(Peca(selo(1.3), 540, 420, ts + .25, .22, modo='pop', som='pop'))
    ap(Peca(peca_folha(940, 340, 'preto', 55, 0, t['j1'], claro=True), 540, 760, ts + .5, .2, modo='carimbo', som='pop'))
    ap(Peca(peca_folha(880, 110, 'preto', 56, 0, t['j2'], claro=True), 540, 1010, ts + 1.1, .2, modo='carimbo', som='pop'))
    ap(Peca(carta_recortada(png('Saheeli Rai'), 330, -3, 70), 540, 1300, ts + 1.4, .28, de=(0, 900), rot0=6))
ap(Peca(peca_folha(920, 120, 'preto', 57, 0, t['j3'], claro=True), 540, 1555, ts + 2.0, .25, modo='carimbo', som='nada'))
DUR = ts + 3.6
# ritmo (fundador, 27/11 00:04: máximo 45 s com fecho): tudo antes da pilha das 47 fica 18 % mais rápido; a pilha mantém 0,125 s por carta
K, CORTE = (.82, 35.7) if '--lento' not in ARG else (1.0, 35.7)
for p in L:
    if p.t0 < CORTE - 1e-6:
        p.t0 *= K
        if p.modo == 'bate': p.dur *= .9 if K < 1 else 1
    else:
        p.t0 += CORTE * K - CORTE
    p.assenta = p.t0 + p.dur + .8
DUR += CORTE * K - CORTE
print('duração sem fecho', round(DUR, 2))
V.render(L, DUR, SAIDA, audio='--mudo' not in sys.argv, abertura=(540, 1010), folha=())
tt = [x * K for x in (0, 1.2, 2.3, 4.8, 6.5, 8.5, 10.0, 12.0, 15.0, 16.9, 17.4, 18.5, 19.5, 20.6, 21.7, 22.8, 25.0, 27.0, 29.5, 33.0, 35.2)] + [DUR - 8, DUR - 6, DUR - 4.5, DUR - 2.5, DUR - .3, DUR + 1]
V.folha_contacto(SAIDA, SAIDA.replace('.mp4', '_folha.jpg'), tt)
print('ok', SAIDA)
