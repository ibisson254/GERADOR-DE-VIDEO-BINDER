"""LL-ART21 V4 · capa do Reel (1080×1920) e recorte da grelha (1080×1440, conteúdo entre y 240 e 1680).
Uso: python3 -I capa_v4.py <cache_catalogo> <pasta_saida> [--foto retrato.png] [--verde]"""
import sys, os, json
import cv2, numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(AQUI, '../../kit_video')))
import motor_video as V
from motor_video import Peca, T, caixa, peca_folha, matte, PRETO, M, CW, CH

ARG = sys.argv[1:]
CACHE, OUT = os.path.abspath(ARG[0]), os.path.abspath(ARG[1]); os.makedirs(OUT, exist_ok=True)
FOTO = os.path.abspath(ARG[ARG.index('--foto') + 1]) if '--foto' in ARG else None
FUNDO = 'verde' if '--verde' in ARG else 'kraft'
CAT = json.load(open(os.path.join(CACHE, 'catalogo.json')))
png = lambda n: os.path.join(CACHE, 'cartas', [c for c in CAT if c['nome'] == n][0]['ilustracao'] + '.png')
F2 = ((-.94, -1, -40), (.94, -1, 40))

t = {'t1': caixa(900, 240, T('Quem pintou<br><span class="k">estas cartas?</span>', 86, w=900)),
     't2': caixa(900, 200, T('Will Murai', 116, '#fff', w=900, extra='white-space:nowrap;')),
     't3': caixa(300, 140, f'<div class="e" style="position:relative;font-family:CB;font-size:54px;line-height:1;color:{PRETO};text-align:center;width:290px;white-space:normal">54 ilustrações<br><span style="font-size:36px">no Magic</span></div>'),
     't4': caixa(260, 90, f'<div class="e" style="position:relative;font-family:CB;font-size:60px;color:{PRETO};text-align:center;width:260px">Do Brasil</div>')}
V.render_textos()

def retrato(alt, seed=4):
    sys.path.insert(0, V.KIT); from recorte_foto import recorte
    f = cv2.imread(FOTO); m = np.full(f.shape[:2], 255, np.uint8); cwd = os.getcwd(); os.chdir(V.KIT)
    try: return matte(lambda b: recorte(b, f, m, CW / 2, CH / 2 - alt / 2, alt, 0, borda=20, seed=seed))
    finally: os.chdir(cwd)

P = []
P.append((peca_folha(1010, 1440, FUNDO, 80, .4), 540, 960))
P.append((peca_folha(920, 260, 'creme', 81, -1.2, t['t1'], fitas=F2), 540, 410))
if FOTO:
    for i, (n, a) in enumerate((('Brainstorm', 7), ('Saheeli Rai', -6), ('Vendilion Clique', -1.5))):
        P.append((V.peca_carta_recortada(png(n), 400, a, 90 + i), 320 + (i - 2) * 12, 905 + (i - 2) * 10))
    P.append((retrato(330, 9), 775, 830))
    P.append((peca_folha(300, 150, 'amarelo', 82, 5, t['t3']), 800, 1085))
else:
    for i, (n, a) in enumerate((('Brainstorm', 8), ('Saheeli Rai', -7), ('Vendilion Clique', -1.5))):
        P.append((V.peca_carta_recortada(png(n), 470, a, 90 + i), 460 + (i - 2) * 14, 900 + (i - 2) * 8))
    P.append((peca_folha(300, 150, 'amarelo', 82, 6, t['t3']), 895, 1110))
P.append((peca_folha(920, 230, 'preto', 83, 1, t['t2'], claro=True), 540, 1335))
P.append((matte(lambda b: M.selo(b, CW / 2, CH / 2, .95, -4)), 300, 1530))
P.append((peca_folha(280, 110, 'amarelo', 84, -5, t['t4']), 790, 1530))

b = V.muro()
for i, (pc, x, y) in enumerate(P):
    p = Peca(pc, x, y, 0, modo='fixa'); b = V.desenha(b, p, p.estado(0))
b = np.clip(b, 0, 255).astype(np.uint8)
var = ('foto' if FOTO else 'semfoto') + ('_verde' if FUNDO == 'verde' else '')
cv2.imwrite(os.path.join(OUT, f'll-art21_v4_capa_{var}_1080x1920.png'), b)
cv2.imwrite(os.path.join(OUT, f'll-art21_v4_capa_{var}_grelha_1080x1440.png'), b[240:1680])
print('ok', var)
