"""LL-ART21 V3 · Will Murai, no padrão de vídeo do Lambe-lambe (modelo LL-ECO01; lambe-lambe/kit_video/motor_video.py).
Factos = os da V1/V2 (fontes.md, fontes_v2.md); cartas = cache do catalogo_cartas.py (54 ilustrações, Scryfall 26/11/2026).
Uso: python3 -I reel_v3.py <cache_catalogo> <saida.mp4> [--mudo]
Zero créditos externos; sem foto do artista; obras pessoais do artista não reproduzidas (só títulos em texto)."""
import sys, os, json
import cv2, numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(AQUI, '../../kit_video')))
import motor_video as V
from motor_video import Peca, T, caixa, peca_folha, peca_carta, peca_img, matte, PRETO, M, CW, CH

CACHE = os.path.abspath(sys.argv[1]); SAIDA = os.path.abspath(sys.argv[2])
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
t['g3'] = caixa(700, 110, CB('o nome do meio, dado pela avó', 60, PRETO, 700))
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
V.render_textos()

# lupa: crédito impresso da Vendilion Clique (MM2 67), ampliado 3×, sem alterar
vc = cv2.imread(png('Vendilion Clique'))
cred = cv2.resize(vc[975:1032, 18:300], None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
selo = matte(lambda b: M.selo(b, CW / 2, CH / 2, 1.3, -3))

L = []; ap = L.append
# 1 · gancho: a carta em tela cheia no quadro 0
ap(Peca(peca_carta(png('Vendilion Clique'), 470, -1.5), 540, 1000, 0, modo='fixa'))
ap(Peca(peca_folha(900, 270, 'creme', 1, -1.2, t['a1'], fitas=F2), 540, 500, .30, .40, de=(-80, -1500), rot0=-8))
ap(Peca(matte(lambda b: M.selo(b, CW / 2, CH / 2, .95, -3)), 810, 1610, .95, .22, modo='pop', ang=0, som='pop'))
ap(Peca(peca_folha(900, 160, 'preto', 2, 1.0, t['a2'], claro=True), 540, 1420, 1.45, .36, de=(0, 1400), rot0=6))
# 2 · o crédito
ap(Peca(peca_folha(1010, 1560, 'kraft', 6, -.6), 540, 945, 3.20, .40, de=(0, -1900), rot0=-4, z0=1.15, som='grande'))
ap(Peca(peca_folha(900, 160, 'creme', 7, 1.2, t['b1'], fitas=F2), 540, 500, 3.42, .34, de=(900, -200), rot0=12))
ap(Peca(peca_img(cred, 846, ang=-2, margem=22, fundo=(30, 22, 18), seed=8, fitas=((-1, -1, -40), (1, -1, 40))), 540, 790, 3.75, .34, de=(-900, 100), rot0=-10))
ap(Peca(matte(lambda b: V.tinta(np.ascontiguousarray(b), t['b_ring'], claro=True)), 540, 790, 4.20, .25, modo='carimbo', som='pop'))
ap(Peca(peca_folha(860, 170, 'amarelo', 9, 1.5, t['b2']), 540, 1050, 4.55, .30, de=(900, -100), rot0=10))
ap(Peca(peca_folha(920, 230, 'preto', 10, -1, t['b3'], claro=True), 540, 1330, 5.35, .32, de=(0, 1400), rot0=5))
# 3 · quem é
ap(Peca(peca_folha(1010, 1560, 'creme', 11, .7), 540, 950, 6.80, .40, de=(0, -1900), rot0=5, z0=1.15, som='grande'))
ap(Peca(peca_folha(900, 300, 'preto', 12, -1, t['c1'], claro=True), 540, 500, 7.02, .36, de=(-900, -200), rot0=-10))
ap(Peca(peca_folha(280, 110, 'verde', 13, -6, t['c_br'], claro=True), 830, 360, 7.55, .22, modo='pop', ang=-6, som='pop'))
ap(Peca(peca_folha(880, 200, 'kraft', 14, 1, t['c2'], fitas=F2), 540, 770, 7.85, .32, de=(900, 0), rot0=8))
ap(Peca(peca_folha(720, 100, 'creme', 15, -1, t['c3']), 540, 950, 8.55, .18, modo='carimbo', som='pop'))
for i, (k, y) in enumerate((('c4', 1075), ('c5', 1195), ('c6', 1315))):
    ap(Peca(peca_folha(780, 110, 'preto', 16 + i, (-1) ** i * 1.2, t[k], claro=True), 540, y, 8.85 + .32 * i, .28, de=(900 * (-1) ** i, 0), rot0=8 * (-1) ** i))
# 4 · o percurso
ap(Peca(peca_folha(1010, 1560, 'kraft', 19, -.5), 540, 945, 10.60, .40, de=(0, -1900), rot0=-5, z0=1.15, som='grande'))
ap(Peca(peca_folha(900, 230, 'creme', 20, -1.2, t['d1'], fitas=F2), 540, 450, 10.82, .34, de=(900, -300), rot0=10))
pos = ((360, 640), (700, 860), (380, 1080), (680, 1300))
SETAS = ((800, 748), (280, 968), (800, 1188))
for i, (k, (x, y)) in enumerate(zip(('d2', 'd3', 'd4', 'd5'), pos)):
    tipo = 'amarelo' if k == 'd5' else 'creme'
    ap(Peca(peca_folha(560, 130, tipo, 21 + i, (-1) ** i * 2, t[k]), x, y, 11.30 + .55 * i, .28, de=(-900 * (-1) ** i, 0), rot0=-10 * (-1) ** i))
    if i < 3:
        ap(Peca(peca_folha(180, 130, 'creme', 26 + i, 0, t['seta' if i % 2 == 0 else 'seta2']), SETAS[i][0], SETAS[i][1],
                11.55 + .55 * i, .18, modo='pop', som='nada'))
ap(Peca(peca_folha(780, 60, 'creme', 30, 0, t['d6']), 540, 1400, 13.05, .2, modo='carimbo', som='nada'))
# 5 · no Magic
ap(Peca(peca_folha(1010, 1560, 'creme', 31, .6), 540, 950, 14.30, .40, de=(0, -1900), rot0=-5, z0=1.15, som='grande'))
ap(Peca(peca_folha(780, 140, 'kraft', 32, -2, t['e1'], fitas=F2), 540, 380, 14.52, .32, de=(-900, -200), rot0=-10))
ap(Peca(peca_folha(960, 220, 'preto', 33, 1, t['e2'], claro=True), 540, 600, 14.90, .32, de=(900, 0), rot0=8))
slotA = ('Master Biomancer', 'Prime Speaker Zegana', 'Gideon, Battle-Forged')
slotB = ('Reflector Mage', "Nissa, Nature's Artisan", 'Wrath of God')
for i in range(3):
    ap(Peca(peca_carta(png(slotA[i]), 345, -3 + i * 1.5), 300, 1075, 15.55 + 1.0 * i, .30, de=(-800, -300), rot0=14))
    ap(Peca(peca_carta(png(slotB[i]), 345, 3 - i * 1.5), 780, 1085, 15.95 + 1.0 * i, .30, de=(800, -300), rot0=-14))
ap(Peca(peca_folha(780, 60, 'creme', 34, 0, t['e3']), 540, 1395, 15.3, .2, modo='carimbo', som='nada'))
# 6 · o lado pessoal
ap(Peca(peca_folha(1040, 1640, 'preto', 35, .4), 540, 955, 18.90, .40, de=(0, -1900), rot0=4, z0=1.15, som='grande'))
ap(Peca(peca_folha(940, 250, 'preto', 36, 0, t['f1'], claro=True), 540, 470, 19.15, .2, modo='carimbo', som='pop'))
ap(Peca(peca_folha(900, 260, 'creme', 37, -1.5, t['f2'], fitas=F2), 540, 820, 20.15, .34, de=(-900, -100), rot0=-10))
ap(Peca(peca_folha(900, 200, 'kraft', 38, 1.2, t['f3']), 540, 1130, 21.40, .32, de=(900, 100), rot0=8))
ap(Peca(peca_folha(280, 110, 'verde', 39, 5, t['c_br'], claro=True), 830, 1280, 21.95, .22, modo='pop', ang=5, som='pop'))
# 7 · Hideki
ap(Peca(peca_folha(1010, 1560, 'creme', 40, -.6), 540, 945, 23.10, .40, de=(0, -1900), rot0=-4, z0=1.15, som='grande'))
ap(Peca(peca_folha(680, 420, 'kraft', 41, -1, t['g1'], fitas=F2), 540, 640, 23.35, .34, de=(0, -1500), rot0=-8))
ap(Peca(peca_folha(780, 180, 'preto', 42, 1, t['g2'], claro=True), 540, 990, 24.05, .30, de=(900, 0), rot0=8))
ap(Peca(peca_folha(720, 130, 'creme', 43, -2, t['g3']), 540, 1170, 24.75, .2, modo='carimbo', som='pop'))
# 8 · a herança
ap(Peca(peca_folha(1010, 1560, 'kraft', 44, .7), 540, 950, 26.40, .40, de=(0, -1900), rot0=5, z0=1.15, som='grande'))
ap(Peca(peca_folha(940, 330, 'creme', 45, -1, t['h1'], fitas=F2), 540, 540, 26.62, .34, de=(-900, -200), rot0=-10))
ap(Peca(peca_folha(940, 240, 'preto', 46, 1, t['h2'], claro=True), 540, 860, 28.05, .32, de=(900, 0), rot0=8))
for i, (k, x, w) in enumerate((('h3', 240, 320), ('h4', 520, 200), ('h5', 800, 440))):
    ap(Peca(peca_folha(w, 110, 'creme', 47 + i, (-1) ** i * 4, t[k]), x if k != 'h5' else 780, 1090 + 40 * (i == 2), 29.0 + .25 * i, .2, modo='pop', ang=(-1) ** i * 4, som='pop'))
ap(Peca(peca_folha(880, 80, 'creme', 50, 0, t['h6']), 540, 1250, 29.5, .2, modo='carimbo', som='nada'))
# 9 · as 54, em ordem de lançamento
ap(Peca(peca_folha(1040, 1640, 'creme', 51, .4), 540, 955, 31.00, .40, de=(0, -1900), rot0=4, z0=1.15, som='grande'))
ap(Peca(peca_folha(960, 130, 'kraft', 52, -1, t['i1'], fitas=((-1, -1, -40), (1, -1, 40))), 540, 390, 31.22, .32, de=(-900, 0), rot0=-8))
cw, chh, gx, gy = 96, 134, 6, 7
x0 = 540 - (9 * cw + 8 * gx) / 2 + cw / 2; y0 = 480 + chh / 2
for k, c in enumerate(CAT):
    r, col = divmod(k, 9)
    im = cv2.imread(os.path.join(CACHE, 'cartas', c['ilustracao'] + '.png'), cv2.IMREAD_UNCHANGED)
    a = im[..., 3] if im.shape[2] == 4 else None
    ap(Peca(peca_img(im[..., :3], cw, a, fitas=()), x0 + col * (cw + gx), y0 + r * (chh + gy), 31.65 + .045 * k, .16, modo='pop',
            som='pop' if k % 9 == 0 else 'nada'))
ap(Peca(peca_folha(920, 200, 'preto', 53, 1, t['i2'], claro=True), 540, 1500, 34.30, .32, de=(0, 1400), rot0=5))
# 10 · assinatura
ap(Peca(peca_folha(1040, 1640, 'preto', 54, -.4), 540, 955, 36.20, .40, de=(0, -1900), rot0=-4, z0=1.15, som='grande'))
ap(Peca(selo, 540, 420, 36.45, .22, modo='pop', som='pop'))
ap(Peca(peca_folha(940, 340, 'preto', 55, 0, t['j1'], claro=True), 540, 760, 36.70, .2, modo='carimbo', som='pop'))
ap(Peca(peca_folha(880, 110, 'preto', 56, 0, t['j2'], claro=True), 540, 1010, 37.30, .2, modo='carimbo', som='pop'))
ap(Peca(peca_carta(png('Saheeli Rai'), 250, -4), 300, 1290, 37.55, .26, de=(-700, 200), rot0=-10))
ap(Peca(peca_carta(png('Master Biomancer'), 250, 0), 540, 1300, 37.75, .26, de=(0, 900), rot0=6))
ap(Peca(peca_carta(png('Vendilion Clique'), 250, 4), 780, 1290, 37.95, .26, de=(700, 200), rot0=10))
ap(Peca(peca_folha(920, 120, 'preto', 57, 0, t['j3'], claro=True), 540, 1555, 38.2, .25, modo='carimbo', som='nada'))
DUR = 40.6

V.render(L, DUR, SAIDA, audio='--mudo' not in sys.argv, abertura=(540, 1000), folha=())
V.folha_contacto(SAIDA, SAIDA.replace('.mp4', '_folha.jpg'), [0, 1.0, 2.2, 3.6, 5.0, 6.4, 7.6, 10.2, 12.8, 14.0, 16.3, 18.6, 20.3, 22.5, 24.5, 26.2, 28.4, 30.0, 33.0, 35.6, 37.0, 39.8, 41.5, 44.0])
print('ok', SAIDA)
