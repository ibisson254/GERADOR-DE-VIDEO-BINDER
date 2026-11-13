"""Motor da série Artistas de Magic (Master Style Guide 2.0 + Autonomous Carousel Engine).
Peças: parede, folha, selo, impressões de arte com fita, cartas inteiras com fita, papéis, retrato, rodapé, tipografia."""
import sys, asyncio, cv2, numpy as np
sys.path.insert(0, '/home/claude/kit')
import compor
from compor import colar, rasgo_alpha, camada, aplicar
from recorte_foto import recorte
KIT = '/home/claude/kit/'
W, H = 1080, 1350
compor.CSS += ("@font-face{font-family:PF;src:url(fontes/playfair-display-latin-700-italic.woff2);font-style:italic;font-weight:700}\n"
               ".e y{color:#FFD84A;font-style:italic;font-weight:900}\n.e b{color:#E61E6E}")
ed = cv2.imread(KIT + 'modelo_editorial.png'); cp = cv2.imread(KIT + 'modelo_capa.png')
src = [cv2.imread(KIT + f'avon_{i}_1080.png') for i in (1, 2, 3, 4)]
_kraft = [cp[150:430, 480:1000], ed[255:495, 130:610], ed[700:1030, 700:990]]

def kraft(w, h, k=0, seed=0):
    r = np.random.default_rng(seed + k * 7)
    t = cv2.resize(_kraft[k % 3], (w, h), interpolation=cv2.INTER_CUBIC).astype(np.float32)
    lf = cv2.resize(r.normal(0, 1, (6, 5)).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC)[..., None]
    return np.clip(t * (1 + lf * .05) + r.normal(0, 6, (h, w, 1)), 0, 255).astype(np.uint8)

def fundo(seed=0):
    wall = np.zeros((H, W, 3), np.uint8)
    def tira(img, x0, x1):
        t = img[430:1100, x0:x1]; t = np.vstack([t, t[::-1]]); return np.vstack([t, t])[:H]
    wall[:, :60] = tira(src[1 + seed % 2], W - 60, W)[:, ::-1]
    wall[:, W - 60:] = tira(src[3 - seed % 2], W - 60, W)
    wall[:40] = cv2.resize(np.hstack([src[i][0:26, 480:900] for i in (1, 2, 3)])[:, :W], (W, 40))
    wall[H - 40:] = cv2.resize(np.hstack([src[i][H - 26:H, 300:720] for i in (1, 2, 3)])[:, :W], (W, 40))
    m = np.zeros((H, W), np.uint8); m[40:H - 40, 60:W - 60] = 255
    wall[m > 0] = cv2.GaussianBlur(wall, (0, 0), 30)[m > 0]
    FW, FH = 1000, 1290
    folha = kraft(FW, FH, 0, seed)
    rel = cv2.resize(cv2.cvtColor(cp[480:900, 120:960], cv2.COLOR_BGR2GRAY), (FW, FH)).astype(np.float32)
    if seed % 2: rel = rel[::-1]
    folha = np.clip(folha + np.clip(rel - cv2.GaussianBlur(rel, (0, 0), 2), -10, 10)[..., None] * .7, 0, 255).astype(np.uint8)
    return colar(wall, folha, rasgo_alpha(FW, FH, 16, 9 + seed), W / 2, H / 2 + 2, -0.4 + 0.15 * (seed % 3))

def selo(base, cx=270, cy=120, esc=1.0, ang=-1.5):
    s = ed[22:240, 55:485].copy(); hs = cv2.cvtColor(s, cv2.COLOR_BGR2HSV)
    a = (((hs[..., 0] > 95) & (hs[..., 0] < 130) & (hs[..., 1] > 120)) * 255).astype(np.uint8)
    a = cv2.morphologyEx(a, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8)); a[:, :58] = 0
    n, lab, st, _ = cv2.connectedComponentsWithStats(a); a = np.where(lab == 1 + np.argmax(st[1:, 4]), 255, 0).astype(np.uint8)
    if esc != 1: s = cv2.resize(s, None, fx=esc, fy=esc); a = cv2.resize(a, None, fx=esc, fy=esc)
    return colar(base, s, a, cx, cy, ang)

def fita(base, cx, cy, ang, larg=110):
    t = cv2.imread(KIT + 'kit_fita.png'); hsv = cv2.cvtColor(t, cv2.COLOR_BGR2HSV)
    rosa = (hsv[..., 1] > 85) & ((hsv[..., 0] > 135) | (hsv[..., 0] < 10))
    a = np.where(~rosa & (hsv[..., 2] > 120), 255, 0).astype(np.uint8)
    a = cv2.morphologyEx(a, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(a); a = np.where(lab == 1 + np.argmax(st[1:, 4]), 255, 0).astype(np.uint8)
    hs = cv2.cvtColor(t, cv2.COLOR_BGR2HSV); hs[..., 1] = (hs[..., 1] * .3).astype(np.uint8); t = cv2.cvtColor(hs, cv2.COLOR_HSV2BGR)
    a = (cv2.GaussianBlur(a, (0, 0), 1) * .88).astype(np.uint8)  # ligeiramente translúcida
    s = larg / t.shape[1]; t = cv2.resize(t, None, fx=s, fy=s); a = cv2.resize(a, None, fx=s, fy=s)
    # sombra de contacto curta
    sh = np.zeros_like(t); base = colar(base, sh, (cv2.GaussianBlur(a, (0, 0), 3) * .35).astype(np.uint8), cx + 2, cy + 4, ang, sombra=False)
    return colar(base, t, a, cx, cy, ang, sombra=False)

def arte(path, corte=0.0):
    a = cv2.imread(path); h, w = a.shape[:2]; d = int(w * corte)
    return a[d:h - d, d:w - d] if d else a

def impressa(base, img, cx, topo, larg, ang=0.0, fitas=((0, -1, -8),), margem=14, seed=12):
    """reprodução impressa: margem branca rasgada + arte intacta + fitas (dx relativo -1..1, dy -1 topo/1 base, ângulo)"""
    ah = int(img.shape[0] * larg / img.shape[1]); im = cv2.resize(img, (larg, ah), interpolation=cv2.INTER_LANCZOS4)
    cy = topo + ah / 2
    base = colar(base, np.full((ah + 2 * margem, larg + 2 * margem, 3), 238, np.uint8), rasgo_alpha(larg + 2 * margem, ah + 2 * margem, 8, seed), cx, cy, ang)
    base = colar(base, im, rasgo_alpha(larg, ah, 3, seed + 1), cx, cy, ang, sombra=False)
    for dx, dy, fa in fitas:
        base = fita(base, cx + dx * larg / 2, cy + dy * (ah / 2 + margem - 6), ang + fa)
    return base, ah

def carta(base, path, cx, cy, larg, ang=0.0, fitas=((0, -1, 4),)):
    c = cv2.imread(path); h = int(c.shape[0] * larg / c.shape[1]); c = cv2.resize(c, (larg, h), interpolation=cv2.INTER_AREA)
    a = np.zeros((h, larg), np.uint8); r = int(larg * .045)
    cv2.rectangle(a, (r, 0), (larg - r, h), 255, -1); cv2.rectangle(a, (0, r), (larg, h - r), 255, -1)
    for x, y in ((r, r), (larg - r, r), (r, h - r), (larg - r, h - r)): cv2.circle(a, (x, y), r, 255, -1)
    base = colar(base, c, cv2.GaussianBlur(a, (0, 0), .7), cx, cy, ang)
    for dx, dy, fa in fitas:
        base = fita(base, cx + dx * larg / 2, cy + dy * (h / 2 - 4), ang + fa)
    return base

def papel(base, x, y, w, h, ang=0, k=1, seed=0):
    return colar(base, kraft(w, h, k, seed), rasgo_alpha(w, h, 9, 40 + seed), x + w / 2, y + h / 2, ang)

def rodape(base, cy, ang=-0.8):
    fx0, fy0, fx1, fy1 = 70, 1090, 1015, 1265
    f = ed[fy0:fy1, fx0:fx1].copy()
    fa = ((cv2.cvtColor(f, cv2.COLOR_BGR2HSV)[..., 2] < 85) * 255).astype(np.uint8)
    fa = cv2.morphologyEx(fa, cv2.MORPH_CLOSE, np.ones((21, 21), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(fa); fa = np.where(lab == 1 + np.argmax(st[1:, 4]), 255, 0).astype(np.uint8)
    v = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)[..., 2]
    f = cv2.inpaint(f, cv2.dilate((v > 110).astype(np.uint8) * 255, np.ones((5, 5), np.uint8)) & fa, 7, cv2.INPAINT_TELEA)
    f = np.clip(f.astype(np.float32) * .85, 0, 255).astype(np.uint8)
    return colar(base, f, fa, 540, cy, ang)

def rodape_txt(cy, html, credito, fs=48):
    return (f'<div class="e" data-w="840" style="left:540px;top:{cy-70}px;transform:translateX(-50%) rotate(-.8deg);text-align:center;font-family:RB;font-weight:800;font-size:{fs}px;line-height:1.08;color:#fff">{html}</div>'
            f'<svg class="e" style="left:150px;top:{cy+66}px;transform:rotate(-.8deg)" width="780" height="20"><path d="M4 12 C 250 6, 520 10, 776 4" stroke="#E61E6E" stroke-width="5" fill="none" stroke-linecap="round"/></svg>'
            f'<div style="position:absolute;left:540px;transform:translateX(-50%) rotate(-.8deg);top:{cy+40}px;font-family:Geist;font-weight:500;font-size:15px;color:#BDB6AA;white-space:nowrap">{credito}</div>')

def traco(x, y, w, ang=-2, esp=10):
    return f'<svg class="e" style="left:{x}px;top:{y}px;transform:rotate({ang}deg)" width="{w}" height="34"><path d="M8 24 C {w*.3} 12, {w*.6} 18, {w-8} 6" stroke="#E61E6E" stroke-width="{esp}" fill="none" stroke-linecap="round"/></svg>'

def render(base, tinta, claro, saida):
    import os
    cwd = os.getcwd(); os.chdir(KIT)
    asyncio.run(camada(tinta, '_t.png')); asyncio.run(camada(claro, '_c.png'))
    out = aplicar(base, '_t.png', '_c.png'); os.chdir(cwd)
    cv2.imwrite(saida, out); return out
