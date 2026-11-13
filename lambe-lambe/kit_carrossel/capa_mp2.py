"""Capa «Artistas de Magic» segundo o Master Prompt 2.0 (lambe-lambe/MASTER_PROMPT_ARTISTAS_2.md).
Sem fitas; arte original intacta (sem filtros), inteira, como protagonista; retrato P&B em recorte; papéis do kit.
python3 -I capa_mp2.py <config.json> <saida.png>"""
import sys, json, asyncio, cv2, numpy as np
sys.path.insert(0, '.')
from compor import colar, rasgo_alpha, camada, aplicar
from recorte_foto import recorte
C = json.load(open(sys.argv[1]))
rng = np.random.default_rng(3)
ed = cv2.imread('modelo_editorial.png'); cp = cv2.imread('modelo_capa.png')
W, H = 1080, 1350

# 1) parede: faixas laterais e de topo/fundo das imagens IA (sem as zonas das fitas)
wall = np.zeros((H, W, 3), np.uint8)
src = [cv2.imread(f'avon_{i}_1080.png') for i in (1, 2, 3, 4)]
def tira_v(img, x0, x1):  # faixa vertical do meio (y 260-1090), repetida em espelho
    t = img[430:1100, x0:x1]; t = np.vstack([t, t[::-1]]); return np.vstack([t, t])[:H]
wall[:, :60] = tira_v(src[1], W-60, W)[:, ::-1]
wall[:, W-60:] = tira_v(src[3], W-60, W)
wall[:40] = cv2.resize(np.hstack([src[i][0:26, 480:900] for i in (1, 2, 3)])[:, :W], (W, 40))
wall[H-40:] = cv2.resize(np.hstack([src[i][H-26:H, 300:720] for i in (1, 2, 3)])[:, :W], (W, 40))
# preencher o interior com rosa médio (fica tapado pela folha)
interior = np.zeros((H, W), np.uint8); interior[40:H-40, 60:W-60] = 255
wall[interior > 0] = cv2.GaussianBlur(wall, (0, 0), 30)[interior > 0]

# 2) folha principal de papel envelhecido
kraft_src = [cp[150:430, 480:1000], ed[255:495, 130:610], ed[700:1030, 700:990]]
def kraft(w, h, k=0):
    t = kraft_src[k % len(kraft_src)]
    t = cv2.resize(t, (w, h), interpolation=cv2.INTER_CUBIC).astype(np.float32)
    lf = cv2.resize(rng.normal(0, 1, (6, 5)).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC)[..., None]
    g = rng.normal(0, 6, (h, w, 1)).astype(np.float32)
    return np.clip(t * (1 + lf * 0.05) + g, 0, 255).astype(np.uint8)
FW, FH = 1000, 1290
folha = kraft(FW, FH, 0)
# amassado: relevo da pintura IA aplicado só à folha
rel = cv2.resize(cv2.cvtColor(cp[480:900, 120:960], cv2.COLOR_BGR2GRAY), (FW, FH)).astype(np.float32)
folha = np.clip(folha + np.clip(rel - cv2.GaussianBlur(rel, (0, 0), 2), -10, 10)[..., None] * 0.7, 0, 255).astype(np.uint8)
base = colar(wall, folha, rasgo_alpha(FW, FH, 16, 9), W/2, H/2+2, -0.4)

# 3) ilustração original: inteira, sem filtro, impressa com margem branca fina rasgada
art = cv2.imread(C['arte'])
aw = C.get('arte_larg', 940); ah = int(art.shape[0] * aw / art.shape[1])
art = cv2.resize(art, (aw, ah), interpolation=cv2.INTER_LANCZOS4)
AX, AY = C.get('arte_cx', 540), C.get('arte_topo', 505)
m = 14; margem = np.full((ah + 2*m, aw + 2*m, 3), 236, np.uint8)
base = colar(base, margem, rasgo_alpha(aw + 2*m, ah + 2*m, 9, 12), AX, AY + ah/2, C.get('arte_ang', 0.3))
base = colar(base, art, rasgo_alpha(aw, ah, 3, 13), AX, AY + ah/2, C.get('arte_ang', 0.3), sombra=False)

# 4) cabeçalho azul (recortado da peça IA) + nome num único papel
selo = ed[22:240, 55:485].copy(); hs = cv2.cvtColor(selo, cv2.COLOR_BGR2HSV)
sa = (((hs[..., 0] > 95) & (hs[..., 0] < 130) & (hs[..., 1] > 120)) * 255).astype(np.uint8)
sa = cv2.morphologyEx(sa, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
sa[:, :58] = 0
n, lab, st, _ = cv2.connectedComponentsWithStats(sa); sa = np.where(lab == 1 + np.argmax(st[1:, 4]), 255, 0).astype(np.uint8)
NP = C.get('nome_papel', [600, 290])
base = colar(base, kraft(NP[0], NP[1], 1), rasgo_alpha(NP[0], NP[1], 12, 21), 64 + NP[0]/2, 205 + NP[1]/2, -2.5)
base = colar(base, selo, sa, 270, 120, -1.5)

# 5) retrato P&B em recorte (só com foto fornecida pelo fundador)
if C.get('foto'):
    base = recorte(base, cv2.imread(C['foto']), cv2.imread(C['foto_mask'], 0), cx=C.get('foto_cx', 850), topo=40, alt=C.get('foto_alt', 470), ang=1.5)

# 6) estatística e subtítulo em pequenos recortes sobre cantos não focais da arte
SX, SY, SW, SH = C['stat_box']
base = colar(base, kraft(SW, SH, 2), rasgo_alpha(SW, SH, 9, 31), SX + SW/2, SY + SH/2, 2.5)
TX, TY, TW, TH = C['sub_box']
base = colar(base, kraft(TW, TH, 1), rasgo_alpha(TW, TH, 8, 33), TX + TW/2, TY + TH/2, -3)

# 7) rodapé preto carvão (faixa da peça IA, sem texto)
fx0, fy0, fx1, fy1 = 70, 1090, 1015, 1265
faixa = ed[fy0:fy1, fx0:fx1].copy()
fa = ((cv2.cvtColor(faixa, cv2.COLOR_BGR2HSV)[..., 2] < 85) * 255).astype(np.uint8)
fa = cv2.morphologyEx(fa, cv2.MORPH_CLOSE, np.ones((21, 21), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(fa); fa = np.where(lab == 1 + np.argmax(st[1:, 4]), 255, 0).astype(np.uint8)
v = cv2.cvtColor(faixa, cv2.COLOR_BGR2HSV)[..., 2]; claro_m = cv2.dilate((v > 110).astype(np.uint8)*255, np.ones((5,5),np.uint8)) & fa
faixa = cv2.inpaint(faixa, claro_m, 7, cv2.INPAINT_TELEA)
faixa = np.clip(faixa.astype(np.float32) * 0.85, 0, 255).astype(np.uint8)
base = colar(base, faixa, fa, 540, C.get('rodape_y', 1180), -0.8)

# 8) tipografia
RY = C.get('rodape_y', 1180)
tinta = f'''
<div class="e" data-w="{NP[0]-70}" style="left:100px;top:{232}px;font-family:AB;font-size:{C.get('nome_fs',104)}px;line-height:.95;color:#111;transform:rotate(-2.5deg);transform-origin:left;letter-spacing:-2px;-webkit-text-stroke:2px #111">{C['nome_html']}</div>
<svg class="e" style="left:110px;top:{205+NP[1]-48}px;transform:rotate(-2.5deg)" width="{NP[0]-110}" height="34"><path d="M8 24 C {NP[0]*.3} 12, {NP[0]*.6} 18, {NP[0]-120} 6" stroke="#E61E6E" stroke-width="11" fill="none" stroke-linecap="round"/></svg>
<div class="e" style="left:{SX+SW/2}px;top:{SY+26}px;transform:translateX(-50%) rotate(2.5deg);text-align:center;font-family:BC;text-transform:uppercase;font-size:{C.get('stat_fs1',36)}px;line-height:1;color:#111">{C['stat_pre']}<br><span style="font-family:AB;font-size:{C.get('stat_fs2',84)}px;color:#E61E6E;line-height:1.08">{C['stat_num']}</span><br>{C['stat_pos']}</div>
<div class="e" style="left:{TX+28}px;top:{TY+22}px;transform:rotate(-3deg);transform-origin:left;font-family:'PF';font-style:italic;font-weight:700;font-size:{C.get('sub_fs',40)}px;line-height:1.05;color:#2b2b2b">{C['subtitulo']}</div>
<svg class="e" style="left:{TX+30}px;top:{TY+TH-34}px;transform:rotate(-3deg)" width="{TW-80}" height="20"><path d="M4 14 C {TW*.3} 8, {TW*.55} 12, {TW-86} 4" stroke="#E61E6E" stroke-width="5" fill="none" stroke-linecap="round"/></svg>
'''
claro = f'''
<div class="e" data-w="840" style="left:540px;top:{RY-70}px;transform:translateX(-50%) rotate(-.8deg);text-align:center;font-family:RB;font-weight:800;font-size:{C.get('rod_fs',50)}px;line-height:1.08;color:#FFFFFF">{C['rodape_html']}</div>
<svg class="e" style="left:150px;top:{RY+66}px;transform:rotate(-.8deg)" width="780" height="20"><path d="M4 12 C 250 6, 520 10, 776 4" stroke="#E61E6E" stroke-width="5" fill="none" stroke-linecap="round"/></svg>
<div style="position:absolute;left:540px;transform:translateX(-50%) rotate(-.8deg);top:{RY+40}px;font-family:Geist;font-weight:500;font-size:15px;color:#BDB6AA;white-space:nowrap">{C['credito']}</div>
'''
import compor
compor.CSS += "@font-face{font-family:PF;src:url(fontes/playfair-display-latin-700-italic.woff2);font-style:italic;font-weight:700}\n.e y{color:#FFD84A;font-style:italic;font-weight:900}"
asyncio.run(camada(tinta, '_t.png')); asyncio.run(camada(claro, '_c.png'))
out = aplicar(base, '_t.png', '_c.png')
cv2.imwrite(sys.argv[2], out)
