# Expedição BINDER · render 9:16 (1080x1920, 30 fps) a partir de episode.json + tl.json + mix_final.wav.
# Uso:
#   python3 -I render.py <pasta_do_episodio> <pasta_de_trabalho>              -> <ficheiro>.mp4 (com o fecho de marca)
#   python3 -I render.py <ep> <wk> stills 0 3 10 ...                          -> still_XX.XX.png
#   python3 -I render.py <ep> <wk> capas                                      -> capa_A.png, capa_B.png
# O motor só conhece os oito movimentos da BIBLIA §4 (plano de carta, troca de variante, punch-in, slide-in de
# comparação, pop-in de caixa, B-roll, respiração, fila de caixas) mais a abertura, o pagamento do Lotus e o fecho.
import json, math, os, subprocess, sys
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

EP, WK = sys.argv[1].rstrip('/'), sys.argv[2].rstrip('/')
MODE = sys.argv[3] if len(sys.argv) > 3 else 'video'
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(f'{HERE}/../..')
CFG = json.load(open(f'{EP}/episode.json')); TL = json.load(open(f'{WK}/tl.json'))
W, H, FPS = 1080, 1920, 30
TOTAL, OUT = TL['TOTAL'], TL['OUT_START']
EV = TL['eventos']; WORDS = TL['words']
CRED = json.load(open(f'{EP}/cards/creditos.json'))

# ---------- tipografia e cores (BINDER: preto #050A10, ardósia #0F172A, esmeralda #10B981) ----------
FD = '/usr/share/fonts/opentype/inter/'
_fc = {}
def F(name, size):
    if (name, size) not in _fc: _fc[(name, size)] = ImageFont.truetype(FD + name, size)
    return _fc[(name, size)]
BLK, XB, BOLD, SEMI, MED = 'InterDisplay-Black.otf', 'InterDisplay-ExtraBold.otf', 'Inter-Bold.otf', 'Inter-SemiBold.otf', 'Inter-Medium.otf'
EM = (16, 185, 129); WHITE = (240, 246, 248); YEL = (255, 214, 64); INK = (5, 10, 16)
def ease(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)
def eout(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3
def fit(d, s, font, size, maxw, minsize=16):
    while size > minsize and d.textlength(s, font=F(font, size)) > maxw: size -= 1
    return F(font, size)

# ---------- carta ----------
CW = int(W * 0.80); CX = (W - CW) // 2; CY = 176; S = CW / 745; CH = round(1040 * S)
_cards = {}
def card(name, w=CW):
    k = (name, w)
    if k not in _cards:
        im = Image.open(f'{EP}/cards/{name}').convert('RGBA'); h = round(im.height * w / im.width)
        im = im.resize((w, h), Image.LANCZOS)
        m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=int(w * 0.045), fill=255)
        a = np.minimum(np.array(im.getchannel('A')), np.array(m)); im.putalpha(Image.fromarray(a))
        _cards[k] = im
    return _cards[k]
_shadow = {}
def shadow(w, h, blur=26, alpha=150):
    k = (w, h)
    if k not in _shadow:
        pad = blur * 3; s = Image.new('L', (w + 2 * pad, h + 2 * pad), 0)
        ImageDraw.Draw(s).rounded_rectangle((pad, pad + 14, pad + w, pad + h + 14), radius=int(w * 0.05), fill=alpha)
        _shadow[k] = (s.filter(ImageFilter.GaussianBlur(blur)), pad)
    return _shadow[k]
def paste_card(im, c, x, y):
    sh, pad = shadow(c.width, c.height)
    im.paste((0, 0, 0), (int(x) - pad, int(y) - pad), sh)
    im.alpha_composite(c, (int(x), int(y)))
def bob(t): return 6 * math.sin(2 * math.pi * t / 3.0)

# ---------- fundo do oceano: gradiente por camada, raios de luz, partículas ----------
CAM = CFG['camadas']
def grad(top, base):
    y = np.linspace(0, 1, H)[:, None, None]
    g = (np.array(top)[None, None, :] * (1 - y) + np.array(base)[None, None, :] * y)
    return np.broadcast_to(g, (H, W, 3)).astype(np.float32)
GRAD = {k: grad(v['topo'], v['base']) for k, v in CAM.items()}
def rays_img():
    r = Image.new('L', (W, H), 0); d = ImageDraw.Draw(r)
    for x0, w0, a in ((120, 90, 70), (360, 140, 55), (640, 70, 60), (820, 120, 45), (980, 60, 40)):
        d.polygon([(x0, -10), (x0 + w0, -10), (x0 + w0 * 2.6 + 260, H * 0.85), (x0 + 140, H * 0.85)], fill=a)
    r = r.filter(ImageFilter.GaussianBlur(38))
    fade = np.linspace(1, 0, H)[:, None] ** 1.3
    return np.array(r, np.float32) / 255 * fade
RAYS = rays_img()
rng = np.random.default_rng(3)
PART = [dict(x=rng.uniform(0, W), y=rng.uniform(0, H), r=rng.uniform(1.5, 4.2), v=rng.uniform(10, 34), ph=rng.uniform(0, 6.3),
             a=rng.uniform(0.25, 0.8)) for _ in range(80)]

# camada ao longo do tempo: corte seco na abertura, cross-fade de 0,35 s nas respirações
SEG = []
for e in EV:
    if e['tipo'] in ('respiro', 'carta', 'caixa', 'lotus', 'fecho'):
        SEG.append((e['t'], CFG['blocos'][e['bloco']]['camada'], e['tipo'] == 'respiro'))
AB = [e for e in EV if e['tipo'] == 'abertura'][0]
def layer_at(t):
    if t < AB['t1']:
        if t < AB['silhueta']: return 'grande', None, 0
        if t < AB['titulo']: return 'abismo', None, 0
        return 'rasos', None, 0
    cur, prev, t0, fade = SEG[0][1], 'rasos', SEG[0][0], SEG[0][2]
    for (ts, lay, f) in SEG:
        if ts <= t:
            if lay != cur: prev, cur, t0, fade = cur, lay, ts, f
        else: break
    m = ease((t - t0) / 0.35) if fade else 1.0
    return cur, prev, m

def background(t):
    cur, prev, m = layer_at(t)
    g = GRAD[cur] if (prev is None or m >= 1) else GRAD[prev] * (1 - m) + GRAD[cur] * m
    ra = CAM[cur]['raios'] if (prev is None or m >= 1) else CAM[prev]['raios'] * (1 - m) + CAM[cur]['raios'] * m
    if ra > 0:
        sh = int(30 * math.sin(t * 0.35)); r = np.roll(RAYS, sh, axis=1) * (0.75 + 0.25 * math.sin(t * 0.9))
        g = g + r[:, :, None] * np.array([150, 230, 230], np.float32)[None, None, :] * 0.55 * ra
    im = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)).convert('RGBA')
    d = ImageDraw.Draw(im, 'RGBA'); pc = tuple(CAM[cur]['particula']); bio = CAM[cur].get('bio')
    for p in PART:
        x = (p['x'] + 14 * math.sin(t * 0.6 + p['ph'])) % W; y = (p['y'] - p['v'] * t) % H
        a = p['a'] * (0.6 + 0.4 * math.sin(t * 1.7 + p['ph'] * 3)) if bio else p['a'] * 0.7
        r = p['r'] * (1.3 if bio else 1)
        if bio: d.ellipse((x - r * 3, y - r * 3, x + r * 3, y + r * 3), fill=pc + (int(28 * a),))
        d.ellipse((x - r, y - r, x + r, y + r), fill=pc + (int(200 * a),))
    return im

# ---------- caixas: imagem oficial em products/; sem ela, cartão PRÉVIA (não publicável) ----------
BOXW = 640
def box_img(deck):
    info = CFG['caixas'][deck]; p = f'{EP}/{info["img"]}'
    if os.path.exists(p):
        im = Image.open(p).convert('RGBA'); h = round(im.height * BOXW / im.width)
        im = im.resize((BOXW, h), Image.LANCZOS); r = info.get('ret_subtitulo')
        rect = [v * BOXW / Image.open(p).width for v in r] if r else [40, h * 0.55, BOXW - 40, h * 0.7]
        return im, rect, True
    h = 900; im = Image.new('RGBA', (BOXW, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, BOXW - 1, h - 1), radius=26, fill=(9, 30, 44, 255), outline=(16, 185, 129, 255), width=4)
    for i in range(0, h, 6): d.line((6, i, BOXW - 6, i), fill=(14, 50, 66, 60))
    d.text((BOXW / 2, 90), 'DECK DE COMMANDER', font=F(SEMI, 30), fill=EM, anchor='mm')
    words = deck.upper().split(); lines = [' '.join(words[:2]), ' '.join(words[2:])] if len(words) > 2 else words
    y = 330; rect = [BOXW, 9999, 0, 0]
    for ln in lines:
        f = fit(d, ln, BLK, 96, BOXW - 70); bb = d.textbbox((BOXW / 2, y), ln, font=f, anchor='mm')
        d.text((BOXW / 2, y), ln, font=f, fill=WHITE, anchor='mm')
        rect = [min(rect[0], bb[0]), min(rect[1], bb[1]), max(rect[2], bb[2]), max(rect[3], bb[3])]; y += 118
    d.text((BOXW / 2, 640), 'NAUCTIS: THE SUNKEN REALM', font=F(SEMI, 28), fill=(170, 210, 220), anchor='mm')
    d.rounded_rectangle((60, 760, BOXW - 60, 850), radius=14, fill=(120, 30, 30, 255))
    d.text((BOXW / 2, 792), 'PRÉVIA · NÃO PUBLICAR', font=F(BOLD, 28), fill=WHITE, anchor='mm')
    d.text((BOXW / 2, 826), 'falta a imagem oficial da caixa', font=F(MED, 22), fill=(255, 220, 220), anchor='mm')
    return im, rect, False
_boxes = {}
def box(deck):
    if deck not in _boxes: _boxes[deck] = box_img(deck)
    return _boxes[deck]
def boxes_ok(): return all(box(d)[2] for d in CFG['caixas'])

# ---------- câmara (punch-in) ----------
def apply_cam(im, cx, cy, z):
    if z <= 1.001: return im
    w, h = W / z, H / z
    x0 = min(max(cx - w / 2, 0), W - w); y0 = min(max(cy - h / 2, 0), H - h)
    return im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + w, y0 + h))
def lerp_cam(a, b, k): return tuple(a[i] + (b[i] - a[i]) * k for i in range(3))
IDENT = (W / 2, H / 2, 1.0)
def card_rect_cam(r, by):
    x0, y0, x1, y1 = CX + r[0] * S, by + r[1] * S, CX + r[2] * S, by + r[3] * S
    z = min(1.6, 1010 / (x1 - x0), 760 / (y1 - y0))
    return ((x0 + x1) / 2, (y0 + y1) / 2, z)

# ---------- HUD: medidor de descida, logótipo, ficha, crédito, legenda ----------
LOGO = Image.open(f'{REPO}/manaburn/logo/logo_mark.png').convert('RGBA').resize((62, 62), Image.LANCZOS)
la = np.array(LOGO); la[:, :, 3] = (la[:, :, 3] * 0.6).astype(np.uint8); LOGO = Image.fromarray(la)
MY0, MY1 = 430, 1300
LAYERS = list(CAM.keys())
RESP = {CFG['blocos'][e['bloco']]['camada']: e['t'] for e in EV if e['tipo'] == 'respiro'}
FECHO_T = [e['t'] for e in EV if e['tipo'] == 'fecho'][0]
def meter_y(t):
    seg = (MY1 - MY0) / len(LAYERS); ts = [RESP.get(l, 0) for l in LAYERS] + [FECHO_T]
    if t < ts[0]: return MY0
    for i in range(len(LAYERS)):
        if t < ts[i + 1]: return MY0 + seg * (i + (t - ts[i]) / (ts[i + 1] - ts[i]))
    return MY1
_lab = {}
def vlabel(txt, col):
    k = (txt, col)
    if k not in _lab:
        f = F(SEMI, 17); tw = int(ImageDraw.Draw(Image.new('L', (1, 1))).textlength(txt, font=f)) + 4
        im = Image.new('RGBA', (tw, 24), (0, 0, 0, 0)); ImageDraw.Draw(im).text((2, 2), txt, font=f, fill=col)
        _lab[k] = im.rotate(90, expand=True)
    return _lab[k]
def draw_meter(im, t):
    d = ImageDraw.Draw(im, 'RGBA'); x = 44
    d.line((x, MY0, x, MY1), fill=(255, 255, 255, 70), width=2)
    seg = (MY1 - MY0) / len(LAYERS); cur = layer_at(t)[0] if t >= AB['t1'] else None
    for i, l in enumerate(LAYERS):
        y = MY0 + seg * i; d.line((x - 8, y, x + 8, y), fill=(255, 255, 255, 110), width=2)
        on = l == cur; lab = vlabel(CAM[l]['nome'], (255, 255, 255, 235) if on else (255, 255, 255, 110))
        im.alpha_composite(lab, (x + 10, int(y + seg / 2 - lab.height / 2)))
    d.line((x - 8, MY1, x + 8, MY1), fill=(255, 255, 255, 110), width=2)
    y = meter_y(t)
    d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=EM + (60,)); d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=EM + (255,))
def draw_logo(im): im.alpha_composite(LOGO, (W - 62 - 40, 232))
def ficha(im, f, t0, t):
    k = eout((t - t0) / 0.2); d = ImageDraw.Draw(im, 'RGBA')
    txt = f'{f["nome"]} · {f["tipo"]} · {f["camada"]}'; nf = F(BLK, 34); tf = fit(d, txt, BOLD, 30, 760)
    wn = d.textlength(f'Nº {f["n"]}', font=nf); wt = d.textlength(txt, font=tf); w = wn + wt + 70
    x = (W - w) / 2 - (1 - k) * 60; y = 1428
    d.rounded_rectangle((x, y, x + w, y + 58), radius=14, fill=(5, 10, 16, int(215 * k)))
    d.text((x + 22, y + 29), f'Nº {f["n"]}', font=nf, fill=EM + (int(255 * k),), anchor='lm')
    d.text((x + 44 + wn, y + 29), txt, font=tf, fill=WHITE + (int(255 * k),), anchor='lm')
def credit(im, name):
    c = CRED[name]; d = ImageDraw.Draw(im, 'RGBA')
    s = f'{c["name"]} · {c["setname"]} · Arte: {c["artist"]} · © Wizards of the Coast'
    f = fit(d, s, MED, 19, 900)
    d.text((W / 2, CY + CH + 22), s, font=f, fill=(225, 238, 240, 200), anchor='mm')

AMAR = set(CFG['legenda']['amarelo']); TROCA = CFG['legenda']['trocas']
def disp(i): return TROCA.get(str(i), WORDS[i]['w'])
CHUNKS = []
cur = []
for i, w in enumerate(WORDS):
    if w['cortada'] or disp(i) == '': continue
    cur.append(i); txt = disp(i)
    if len(cur) >= 4 or txt[-1] in '.:?!' or (txt[-1] == ',' and len(cur) >= 2): CHUNKS.append(cur); cur = []
if cur: CHUNKS.append(cur)
def subtitles(im, t):
    if t >= OUT: return
    act = None
    for c in CHUNKS:
        if WORDS[c[0]]['s'] - 0.05 <= t: act = c
        else: break
    if act is None or t > WORDS[act[-1]]['e'] + 0.7: return
    band = Image.new('L', (W, 190), 0); ImageDraw.Draw(band).rectangle((0, 40, W, 150), fill=120)
    band = band.filter(ImageFilter.GaussianBlur(30)); im.paste((5, 10, 16), (0, 1453), band)
    d = ImageDraw.Draw(im, 'RGBA'); f = F(BLK, 58)
    toks = [disp(i) for i in act]; sp = d.textlength(' ', font=f)
    widths = [d.textlength(s, font=f) for s in toks]; tot = sum(widths) + sp * (len(toks) - 1)
    if tot > 980: f = F(BLK, int(58 * 980 / tot)); sp = d.textlength(' ', font=f); widths = [d.textlength(s, font=f) for s in toks]; tot = sum(widths) + sp * (len(toks) - 1)
    x = (W - tot) / 2; y = 1548
    for i, s, w in zip(act, toks, widths):
        if WORDS[i]['s'] - 0.05 <= t:
            col = YEL if i in AMAR else WHITE
            d.text((x, y), s, font=f, fill=col, anchor='lm', stroke_width=5, stroke_fill=INK)
        x += w + sp

# ---------- cenas ----------
def ev_at(t):
    a = None
    for e in EV:
        if e['tipo'] in ('abertura', 'respiro', 'carta', 'caixa', 'lotus', 'fecho', 'marca') and e['t'] <= t: a = e
    return a

def scene_card(im, t, e, b, hud):
    """plano de carta + troca de variante + punch-in + slide-in de comparação; devolve a câmara."""
    img = b.get('carta'); cam_from, cam_to, cam_t = IDENT, IDENT, e['t']
    comp = None; comp_t0 = comp_t1 = None; selo = None; first_punch = None
    by = CY + bob(t)
    punches = [x['t'] for x in e['sub'] if 'punch' in x]
    first_punch = punches[0] if punches else None
    for x in e['sub']:
        if x['t'] > t:
            if x.get('fim_comparacao') and comp is not None and comp_t1 is None: comp_t1 = x['t']
            continue
        if 'variante' in x: img = x['variante']
        if 'punch' in x:
            now = IDENT if 'variante' in x else lerp_cam(cam_from, cam_to, ease((x['t'] - cam_t) / 0.24))
            cam_from, cam_to, cam_t = now, card_rect_cam(x['punch'], CY), x['t']
        elif 'variante' in x or 'comparacao' in x or 'selo' in x:
            cam_from, cam_to, cam_t = IDENT, IDENT, x['t']
        if 'comparacao' in x: comp, comp_t0, comp_t1 = x['comparacao'], x['t'], None
        if x.get('fim_comparacao'): comp_t1 = x['t']
        if 'selo' in x: selo = (x['selo'], x['t'])
    if comp is not None and comp_t1 is None: comp_t1 = e['t1'] - 0.2
    return img, by, (cam_from, cam_to, cam_t), comp, comp_t0, comp_t1, selo, first_punch

def draw_comp(im, name, t, t0, t1):
    if t < t0 or t >= t1 + 0.2: return
    k = eout((t - t0) / 0.27) if t < t1 else 1 - ease((t - t1) / 0.2)
    c = card(name, int(CW * 0.62)).rotate(10, expand=True, resample=Image.BICUBIC)
    fx, fy = 70, 600; sx, sy = -c.width - 40, H + 60
    x = sx + (fx - sx) * k; y = sy + (fy - sy) * k
    paste_card(im, c, x, y)

def lotus_scene(im, t, e, b):
    """silhueta (mesmo enquadramento da abertura) -> acende em bioluminescência; depois segue como plano de carta."""
    lit_t = [x['t'] for x in EV if x['tipo'] == 'lotus_acende'][0]
    by = CY + bob(t)
    if t < lit_t + 0.5:
        sil = silhouette(); paste_card(im, sil, CX, by)
        if t >= lit_t:
            k = ease((t - lit_t) / 0.5); c = card(b['carta_lit']).copy(); c.putalpha(Image.fromarray((np.array(c.getchannel('A')) * k).astype(np.uint8)))
            glow(im, by, k); im.alpha_composite(c, (CX, int(by)))
        return True
    return False
_glow = {}
def glow(im, by, k):
    if 'g' not in _glow:
        g = Image.new('RGBA', (CW + 240, CH + 240), (0, 0, 0, 0)); ImageDraw.Draw(g).rounded_rectangle((120, 120, CW + 120, CH + 120), radius=40, fill=(60, 255, 210, 150))
        _glow['g'] = g.filter(ImageFilter.GaussianBlur(60))
    g = _glow['g'].copy(); g.putalpha(Image.fromarray((np.array(g.getchannel('A')) * k).astype(np.uint8)))
    im.alpha_composite(g, (CX - 120, int(by) - 120))
_sil = {}
def silhouette():
    if 's' not in _sil:
        c = card(CFG['abertura']['silhueta']).copy(); rgb = ImageEnhance.Brightness(c.convert('RGB')).enhance(0.09)
        rgb = Image.blend(rgb, Image.new('RGB', rgb.size, (0, 40, 46)), 0.25); rgb = rgb.convert('RGBA'); rgb.putalpha(c.getchannel('A'))
        _sil['s'] = rgb
    return _sil['s']

def text_center(d, txt, y, font, size, col, maxw=980, stroke=0):
    f = fit(d, txt, font, size, maxw); d.text((W / 2, y), txt, font=f, fill=col, anchor='mm', stroke_width=stroke, stroke_fill=INK)

def hook_text(im, alpha=255):
    d = ImageDraw.Draw(im, 'RGBA'); g = CFG['gancho'].split(); half = (len(g) + 1) // 2
    for i, ln in enumerate((' '.join(g[:half]), ' '.join(g[half:]))):
        text_center(d, ln, 300 + i * 96, BLK, 86, WHITE + (alpha,), stroke=6)

def fila(im, t, t0, names=None, y=820, w=230, gap=18):
    items = names or []
    n = len(items); tot = n * w + (n - 1) * gap; x0 = (W - tot) / 2
    for i, it in enumerate(items):
        k = (t - t0 - i * 0.14) / 0.22
        if k <= 0: continue
        sc = 0.85 + 0.2 * math.sin(min(1, k) * math.pi * 0.75) if k < 1 else 1.0
        if isinstance(it, str) and it.endswith('.png'): c = card(it, int(w * sc))
        else: bi = box(it)[0]; c = bi.resize((int(w * sc), int(bi.height * w * sc / bi.width)), Image.LANCZOS)
        c = c.rotate(-6 + 4 * (i % 2), expand=True, resample=Image.BICUBIC)
        paste_card(im, c, x0 + i * (w + gap) + w / 2 - c.width / 2, y - c.height / 2)

def frame_main(t):
    e = ev_at(t); im = background(t); cam = IDENT; hud = dict(ficha=None, credit=None)
    b = CFG['blocos'][e['bloco']] if 'bloco' in e else None
    d = ImageDraw.Draw(im, 'RGBA')
    if e['tipo'] == 'abertura':
        if t < e['silhueta']:
            names = list(CFG['caixas'].keys()) if (CFG['abertura']['fila'] == 'caixas' and boxes_ok()) else CFG['abertura']['fila_alternativa']
            fila(im, t, -0.5, names, y=980, w=236)
        elif t < e['titulo']:
            z = 1 + 0.05 * (t - e['silhueta']) / max(0.1, e['titulo'] - e['silhueta'])
            paste_card(im, silhouette(), CX, CY + bob(t)); cam = (W / 2, CY + CH / 2, z)
        else:
            k = eout((t - e['titulo']) / 0.3); tt = CFG['titulo_formato']
            text_center(d, tt[0], 860, BLK, 104, WHITE + (int(255 * k),), stroke=0)
            d.line((W / 2 - 220 * k, 935, W / 2 + 220 * k, 935), fill=EM + (255,), width=4)
            text_center(d, tt[1], 990, SEMI, 40, (200, 235, 238, int(255 * k)))
    elif e['tipo'] == 'respiro':
        lay = b['camada']; k = eout((t - e['t']) / 0.3)
        r = 60 + 900 * ((t - e['t']) / 1.2); a = max(0, 1 - (t - e['t']) / 1.2)
        d.ellipse((W / 2 - r, 900 - r, W / 2 + r, 900 + r), outline=(200, 255, 245, int(120 * a)), width=4)
        text_center(d, CAM[lay]['nome'], 900 - 20 * (1 - k), BLK, 120, WHITE + (int(255 * k),))
    elif e['tipo'] in ('carta', 'lotus'):
        pending = e['tipo'] == 'lotus' and lotus_scene(im, t, e, b)
        img, by, (cf, ct, ctt), comp, c0, c1, selo, fp = scene_card(im, t, e, b, hud)
        if e['tipo'] == 'lotus' and img is None: img = b['carta_lit']
        if not pending:
            paste_card(im, card(img), CX, by)
            if comp: draw_comp(im, comp, t, c0, c1)
            if selo:
                k = eout((t - selo[1]) / 0.2); sd = ImageDraw.Draw(im, 'RGBA'); sc = 0.8 + 0.2 * k
                bw, bh = 420 * sc, 110 * sc; x, y = W / 2 - bw / 2, CY + CH - 260
                sd.rounded_rectangle((x, y, x + bw, y + bh), radius=18, fill=EM + (int(240 * k),))
                sd.text((W / 2, y + bh / 2), selo[0], font=F(BLK, int(62 * sc)), fill=INK + (int(255 * k),), anchor='mm')
            kk = ease((t - ctt) / 0.24); cam = lerp_cam(cf, ct, kk)
            hud['credit'] = comp if (comp and c0 <= t < c1) else img
        f0 = e['t'] if e['tipo'] == 'carta' else [x['t'] for x in EV if x['tipo'] == 'lotus_acende'][0]
        if b.get('ficha') and t >= f0 and (fp is None or t < fp): hud['ficha'] = (b['ficha'], f0)
    elif e['tipo'] == 'caixa':
        bi, rect, real = box(b['deck']); k = (t - e['t']) / 0.33
        sc = 0.85 + 0.2 * math.sin(min(1, k) * math.pi * 0.75) if k < 1 else 1.0
        bw = int(BOXW * sc); c = bi.resize((bw, int(bi.height * sc)), Image.LANCZOS).rotate(6, expand=True, resample=Image.BICUBIC)
        bx, byy = W / 2 - c.width / 2, 860 - c.height / 2 + bob(t) * 0.6
        paste_card(im, c, bx, byy)
        if t >= e['punch_t']:
            ang = math.radians(-6); rcx = (rect[0] + rect[2]) / 2 * sc - bw / 2; rcy = (rect[1] + rect[3]) / 2 * sc - bi.height * sc / 2
            px = W / 2 + rcx * math.cos(ang) - rcy * math.sin(ang); py = 860 + rcx * math.sin(ang) + rcy * math.cos(ang)
            cam = lerp_cam(IDENT, (px, py, 2.3), ease((t - e['punch_t']) / 0.22))
    elif e['tipo'] == 'fecho':
        if t < e['pergunta_t']:
            names = list(CFG['caixas'].keys()) if boxes_ok() else b['miniaturas']
            fila(im, t, e['t'], names, y=760, w=148 if len(names) > 4 else 236, gap=14)
            k = eout((t - e['t']) / 0.3)
            text_center(d, CFG['data_lancamento'], 1170, BLK, 150, WHITE + (int(255 * k),))
            text_center(d, CFG['set'].upper(), 1280, SEMI, 40, (200, 235, 238, int(255 * k)))
        else:
            mw, gap = 300, 30; x0 = (W - 3 * mw - 2 * gap) / 2
            for i, n in enumerate(b['miniaturas']):
                k = (t - e['pergunta_t'] - i * 0.08) / 0.2
                if k <= 0: continue
                c = card(n, mw); x = x0 + (i % 3) * (mw + gap); y = 300 + (i // 3) * (c.height + 34)
                paste_card(im, c, x, y + (1 - eout(k)) * 40)
                d = ImageDraw.Draw(im, 'RGBA'); d.ellipse((x - 18, y - 18, x + 62, y + 62), fill=EM + (255,), outline=INK + (255,), width=4)
                d.text((x + 22, y + 22), str(i + 1), font=F(BLK, 50), fill=INK, anchor='mm')
            k = eout((t - e['pergunta_t']) / 0.3); q = CFG['pergunta']
            p1, p2 = q.split('? ') if '? ' in q else (q, '')
            text_center(d, p1 + '?', 1250, BLK, 76, WHITE + (int(255 * k),), stroke=5)
            text_center(d, p2, 1345, BLK, 90, YEL + (int(255 * k),), stroke=5)
    im = apply_cam(im, *cam)
    # HUD (fora da câmara)
    if e['tipo'] == 'abertura' and t < e['titulo']: hook_text(im)
    if t >= AB['titulo']: draw_meter(im, t)
    draw_logo(im)
    if hud['credit'] and cam[2] <= 1.01: credit(im, hud['credit'])
    if hud['ficha']: ficha(im, hud['ficha'][0], hud['ficha'][1], t)
    subtitles(im, t)
    return im.convert('RGB')

_outro = []
def outro(t):
    if not _outro:
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{REPO}/comum/outro/outro_binder_916.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                             capture_output=True, check=True).stdout
        _outro.extend(np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3))
    i = min(len(_outro) - 1, int(round((t - OUT) * FPS)))
    return Image.fromarray(_outro[i])
def frame(t): return outro(t) if t >= OUT else frame_main(t)

def render_part(args):
    k, f0, f1 = args; path = f'{WK}/part_{k}.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
    for fi in range(f0, f1): p.stdin.write(frame(fi / FPS).tobytes())
    p.stdin.close(); p.wait(); return path

def capas():
    # A: silhueta do Lotus no escuro + gancho · B: as quatro caixas (ou, sem elas, as seis cartas) + "NAUCTIS: 6 ESPÉCIES"
    a = Image.fromarray(np.clip(GRAD['abismo'], 0, 255).astype(np.uint8)).convert('RGBA')
    paste_card(a, silhouette(), CX, CY); glow(a, CY, 0.35); hook_text(a); draw_logo(a)
    d = ImageDraw.Draw(a, 'RGBA'); text_center(d, 'EXPEDIÇÃO BINDER #01', 1560, BLK, 64, EM + (255,), stroke=4)
    a.convert('RGB').save(f'{WK}/capa_A.png')
    b = Image.fromarray(np.clip(GRAD['grande'], 0, 255).astype(np.uint8)).convert('RGBA')
    names = list(CFG['caixas'].keys()) if boxes_ok() else [x for x in CFG['blocos'][-1]['miniaturas']]
    if len(names) == 4: fila(b, 10, 0, names, y=900, w=240)
    else:
        mw, gap = 300, 30; x0 = (W - 3 * mw - 2 * gap) / 2
        for i, n in enumerate(names): paste_card(b, card(n, mw), x0 + (i % 3) * (mw + gap), 420 + (i // 3) * 450)
    d = ImageDraw.Draw(b, 'RGBA'); text_center(d, 'NAUCTIS:', 200 + 60, BLK, 120, WHITE + (255,), stroke=6)
    text_center(d, '6 ESPÉCIES', 1430, BLK, 140, YEL + (255,), stroke=7); text_center(d, 'EXPEDIÇÃO BINDER #01', 1560, BLK, 56, EM + (255,), stroke=4)
    draw_logo(b); b.convert('RGB').save(f'{WK}/capa_B.png')

if __name__ == '__main__':
    if MODE == 'stills':
        for s in sys.argv[4:]: frame(float(s)).save(f'{WK}/still_{float(s):05.2f}.png')
    elif MODE == 'capas': capas()
    else:
        n = int(round(TOTAL * FPS)); P = int(os.environ.get('PARTES', os.cpu_count() or 2)); step = math.ceil(n / P)
        with Pool(P) as pool: parts = pool.map(render_part, [(k, k * step, min(n, (k + 1) * step)) for k in range(P)])
        open(f'{WK}/parts.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
        out = f'{WK}/{CFG["ficheiro"]}.mp4'
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', f'{WK}/parts.txt', '-i', f'{WK}/mix_final.wav',
                        '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', out], check=True)
        print(out)
