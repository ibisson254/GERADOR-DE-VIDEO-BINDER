# Expedição BINDER · render v3 (retenção) 9:16 1080x1920 30 fps, a partir de episode.json + tl_<V>.json + mix_final_<V>.wav.
# Uso (a partir de expedicao/):
#   python3 -I template/render.py <ep> <trabalho> [A|B]                  -> <ficheiro da versão>.mp4
#   python3 -I template/render.py <ep> <trabalho> A stills 0 3 10 ...    -> still_A_XX.XX.png
#   python3 -I template/render.py <ep> <trabalho> A capas                -> capa_A.png, capa_B.png
# Estrutura (BIBLIA §4–§5): gancho com indício da carta-pagamento -> descobertas numeradas (cada uma com uma entrada
# própria: arte, scanner, panorâmica, giro, luz) que passam a «modo habilidade» com chamada em PT-BR -> camadas ->
# revelação no drop -> data e decks -> pergunta (A) -> scanner real do BINDER Vision -> cartão final.
import json, math, os, subprocess, sys
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

EP, WK = sys.argv[1].rstrip('/'), sys.argv[2].rstrip('/')
VER = sys.argv[3] if len(sys.argv) > 3 else 'A'
MODE = sys.argv[4] if len(sys.argv) > 4 else 'video'
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(f'{HERE}/../..')
sys.path.insert(0, HERE)
from fundo import Fundo
CFG = json.load(open(f'{EP}/episode.json')); TL = json.load(open(f'{WK}/tl_{VER}.json'))
W, H, FPS = 1080, 1920, 30
TOTAL = TL['TOTAL']; EV = TL['eventos']; WORDS = TL['words']
CRED = json.load(open(f'{EP}/cards/creditos.json'))
BLOC = CFG['blocos']; CAM = CFG['camadas']

# ---------- tipografia e cores (BINDER: preto #050A10, esmeralda #10B981; formato: sinal #FF2A2A) ----------
FD = '/usr/share/fonts/opentype/inter/'
_fc = {}
def F(name, size):
    if (name, size) not in _fc: _fc[(name, size)] = ImageFont.truetype(FD + name, size)
    return _fc[(name, size)]
BLK, BOLD, SEMI, MED = 'InterDisplay-Black.otf', 'Inter-Bold.otf', 'Inter-SemiBold.otf', 'Inter-Medium.otf'
EM = (16, 185, 129); WHITE = (240, 246, 248); YEL = (255, 214, 64); INK = (5, 10, 16); RED = (255, 64, 64)
def ease(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)
def eout(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3
def fit(d, s, font, size, maxw, minsize=16):
    while size > minsize and d.textlength(s, font=F(font, size)) > maxw: size -= 1
    return F(font, size)
def lerp(a, b, k): return a + (b - a) * k

# ---------- cartas ----------
_src = {}; _cards = {}
def src(name):
    if name not in _src: _src[name] = Image.open(f'{EP}/cards/{name}').convert('RGBA')
    return _src[name]
def card(name, w):
    w = int(w); k = (name, w)
    if k not in _cards:
        if len(_cards) > 60: _cards.clear()
        im = src(name); h = round(im.height * w / im.width)
        im = im.resize((w, h), Image.LANCZOS if w > 400 else Image.BILINEAR)
        m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=int(w * 0.045), fill=255)
        im.putalpha(Image.fromarray(np.minimum(np.array(im.getchannel('A')), np.array(m))))
        _cards[k] = im
    return _cards[k]
_shadow = {}
def shadow(w, h, blur=26, alpha=150):
    k = (w // 4, h // 4)
    if k not in _shadow:
        pad = blur * 3; s = Image.new('L', (w + 2 * pad, h + 2 * pad), 0)
        ImageDraw.Draw(s).rounded_rectangle((pad, pad + 14, pad + w, pad + h + 14), radius=int(w * 0.05), fill=alpha)
        _shadow[k] = (s.filter(ImageFilter.GaussianBlur(blur)), pad)
    return _shadow[k]
def paste_card(im, c, x, y, shade=True):
    if shade:
        sh, pad = shadow(c.width, c.height); im.paste((0, 0, 0), (int(x) - pad, int(y) - pad), sh)
    im.alpha_composite(c, (int(x), int(y)))
def bob(t): return 6 * math.sin(2 * math.pi * t / 3.0)
# enquadramentos: plano (80%), habilidade (62%, sobe), herói (88%, só a carta-pagamento)
FULL = (0.80, 176); ABIL = (0.62, 166); HERO = (0.84, 150)
def geom(scale, top): cw = W * scale; return cw, (W - cw) / 2, top, cw * 1040 / 745

# ---------- fundo ----------
FUNDO = Fundo()
BEATS = TL['BEATS']; ENV = TL['ENV']
MAIN = [e for e in EV if e['tipo'] in ('abertura', 'respiro', 'carta', 'lotus', 'decks', 'pergunta', 'scanner', 'cartao')]
AB = [e for e in EV if e['tipo'] == 'abertura'][0]
LIT = ([e['t'] for e in EV if e['tipo'] == 'lotus_acende'] or [1e9])[0]
SEG = [(e['t'], BLOC[e['bloco']]['camada'], e['tipo'] == 'respiro' or BLOC[e['bloco']].get('entra_camada', False))
       for e in EV if 'bloco' in e]
def layer_at(t):
    if t < AB['t1']: return 'abismo', None, 1.0
    cur, prev, t0, fade = SEG[0][1], 'abismo', SEG[0][0], SEG[0][2]
    for (ts, lay, f) in SEG:
        if ts <= t:
            if lay != cur: prev, cur, t0, fade = cur, lay, ts, f
        else: break
    m = ease((t - t0) / 0.35) if fade else 1.0
    return cur, prev, m
CORTES = sorted(set([e['t'] for e in MAIN if e['tipo'] in ('respiro', 'carta', 'lotus', 'decks', 'pergunta')] +
                    [x['t'] for e in EV for x in e.get('sub', []) if 'comparacao' in x]))
RESP_T = [e['t'] for e in EV if e['tipo'] == 'respiro']
def background(t):
    import bisect
    cur, prev, m = layer_at(t)
    energy = ENV[min(len(ENV) - 1, int(t * FPS))]
    j = bisect.bisect_right(BEATS, t) - 1
    pulse = math.exp(-(t - BEATS[j]) / 0.12) * (1.0 if j % 4 == 0 else 0.45) if j >= 0 else 0
    lotus = ease((t - LIT) / 0.6) if t >= LIT else 0.0
    k = bisect.bisect_right(CORTES, t) - 1
    glitch = 1.0 if (k >= 0 and t - CORTES[k] < 2.5 / FPS) else 0.0
    sinal = 0.0; seed = int(t * FPS)
    for rt in RESP_T:
        if 0 <= t - rt < 0.75: sinal = 1 - ease((t - rt) / 0.75); seed = int(rt * 100)
    if cur == 'abismo' and sinal == 0 and j >= 0 and j % 4 == 0 and t - BEATS[j] < 0.22 and AB['t1'] < t < LIT:
        sinal = 0.4 * (1 - (t - BEATS[j]) / 0.22); seed = j
    return FUNDO.frame(t, cur, prev if m < 1 else None, m, energy, pulse, lotus, glitch, sinal, seed)

# ---------- câmara ----------
IDENT = (W / 2, H / 2, 1.0)
def apply_cam(im, cx, cy, z):
    if z <= 1.001: return im
    w, h = W / z, H / z
    x0 = min(max(cx - w / 2, 0), W - w); y0 = min(max(cy - h / 2, 0), H - h)
    return im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + w, y0 + h))
def lcam(a, b, k): return tuple(a[i] + (b[i] - a[i]) * k for i in range(3))

# ---------- silhueta e brilho da carta-pagamento ----------
_sil = {}
def silhouette(name, w, bright=0.12):
    k = (name, int(w), round(bright, 2))
    if k not in _sil:
        if len(_sil) > 20: _sil.clear()
        c = card(name, w); rgb = ImageEnhance.Brightness(c.convert('RGB')).enhance(bright)
        rgb = Image.blend(rgb, Image.new('RGB', rgb.size, (30, 12, 50)), 0.3).convert('RGBA'); rgb.putalpha(c.getchannel('A'))
        _sil[k] = rgb
    return _sil[k]
_glow = {}
def glow(im, x, y, w, h, k, col=(255, 120, 170)):
    key = (int(w), int(h), col)
    if key not in _glow:
        g = Image.new('RGBA', (int(w) + 260, int(h) + 260), (0, 0, 0, 0))
        ImageDraw.Draw(g).rounded_rectangle((130, 130, int(w) + 130, int(h) + 130), radius=40, fill=col + (150,))
        _glow[key] = g.filter(ImageFilter.GaussianBlur(60))
    g = _glow[key].copy(); g.putalpha(Image.fromarray((np.array(g.getchannel('A')) * k).astype(np.uint8)))
    im.alpha_composite(g, (int(x) - 130, int(y) - 130))

# ---------- HUD ----------
LOGO = Image.open(f'{REPO}/manaburn/logo/logo_mark.png').convert('RGBA')
LOGO_S = LOGO.resize((62, 62), Image.LANCZOS); la = np.array(LOGO_S); la[:, :, 3] = (la[:, :, 3] * 0.6).astype(np.uint8); LOGO_S = Image.fromarray(la)
def draw_logo(im): im.alpha_composite(LOGO_S, (W - 62 - 40, 232))
MY0, MY1 = 430, 1300; LAYERS = list(CAM.keys()); SEGH = (MY1 - MY0) / len(LAYERS)
DISC = {}   # n -> (y no medidor, tempo em que a descoberta entra)
for e in EV:
    if 'bloco' in e and BLOC[e['bloco']].get('ficha'):
        f = BLOC[e['bloco']]['ficha']; n = f['n']
        y = MY1 if n == 6 else MY0 + SEGH * ((n - 1) // 2) + SEGH * (1 + (n - 1) % 2) / 3
        DISC[n] = (y, e['t'])
_lab = {}
def vlabel(txt, col):
    k = (txt, col)
    if k not in _lab:
        f = F(SEMI, 18); tw = int(ImageDraw.Draw(Image.new('L', (1, 1))).textlength(txt, font=f)) + 4
        i2 = Image.new('RGBA', (tw, 26), (0, 0, 0, 0)); ImageDraw.Draw(i2).text((2, 2), txt, font=f, fill=col)
        _lab[k] = i2.rotate(90, expand=True)
    return _lab[k]
def draw_meter(im, t):
    d = ImageDraw.Draw(im, 'RGBA'); x = 44
    d.line((x, MY0, x, MY1), fill=(255, 255, 255, 80), width=2)
    cur = layer_at(t)[0]
    for i, l in enumerate(LAYERS):
        y = MY0 + SEGH * i; d.line((x - 8, y, x + 8, y), fill=(255, 255, 255, 120), width=2)
        on = l == cur; lab = vlabel(CAM[l]['nome'], (255, 255, 255, 240) if on else (255, 255, 255, 120))
        im.alpha_composite(lab, (x + 12, int(y + SEGH / 2 - lab.height / 2)))
    d.line((x - 8, MY1, x + 8, MY1), fill=(255, 255, 255, 120), width=2)
    pos, prevy, n_on, t_on = MY0, MY0, 0, -9
    for n in sorted(DISC):
        y, tn = DISC[n]
        found = t >= tn
        d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(EM + (255,)) if found else (255, 255, 255, 70))
        if found: prevy, pos, n_on, t_on = pos, y, n, tn
    yk = lerp(prevy, pos, eout((t - t_on) / 0.45)) if n_on else MY0
    d.ellipse((x - 16, yk - 16, x + 16, yk + 16), fill=EM + (60,)); d.ellipse((x - 8, yk - 8, x + 8, yk + 8), fill=EM + (255,))
    if n_on:
        k = eout((t - t_on) / 0.3); d.text((x + 24 + 8 * (1 - k), yk), f'{n_on}/6', font=F(BLK, 30), fill=EM + (int(255 * k),), anchor='lm')
def credit(im, name, y):
    c = CRED[name]; d = ImageDraw.Draw(im, 'RGBA')
    s = f'{c["name"]} · {c["setname"]} · Arte: {c["artist"]} · © Wizards of the Coast'
    d.text((W / 2, y), s, font=fit(d, s, MED, 19, 900), fill=(225, 238, 240, 205), anchor='mm')
def ficha(im, f, t0, t, y=1428):
    k = eout((t - t0) / 0.2); d = ImageDraw.Draw(im, 'RGBA')
    txt = f'{f["nome"]} · {f["tipo"]} · {f["camada"]}'; nf = F(BLK, 34); tf = fit(d, txt, BOLD, 30, 740)
    lab = f'{f["n"]}/6'; wn = d.textlength(lab, font=nf); wt = d.textlength(txt, font=tf); w = wn + wt + 70
    x = (W - w) / 2 - (1 - k) * 60
    d.rounded_rectangle((x, y, x + w, y + 58), radius=14, fill=(5, 10, 16, int(215 * k)))
    d.text((x + 22, y + 29), lab, font=nf, fill=EM + (int(255 * k),), anchor='lm')
    d.text((x + 44 + wn, y + 29), txt, font=tf, fill=WHITE + (int(255 * k),), anchor='lm')
def tracked(d, txt, y, font, size, col, track=0.12, maxw=1000, x=None):
    while True:
        f = F(font, size); ws = [d.textlength(c, font=f) for c in txt]; tot = sum(ws) + size * track * (len(txt) - 1)
        if tot <= maxw or size < 16: break
        size -= 2
    x = (W - tot) / 2 if x is None else x
    for c, w in zip(txt, ws): d.text((x, y), c, font=f, fill=col, anchor='lm'); x += w + size * track
def text_center(d, txt, y, font, size, col, maxw=980, stroke=0):
    d.text((W / 2, y), txt, font=fit(d, txt, font, size, maxw), fill=col, anchor='mm', stroke_width=stroke, stroke_fill=INK)
def wrap(d, txt, font, size, maxw):
    words = txt.split(); lines = []; cur = ''
    for w_ in words:
        s = (cur + ' ' + w_).strip()
        if d.textlength(s, font=F(font, size)) <= maxw: cur = s
        else: lines.append(cur); cur = w_
    return lines + [cur]
CHIPC = {'ok': (EM, INK), 'mau': ((200, 40, 48), WHITE), 'info': ((255, 255, 255), INK)}
def painel(im, b, e, t, y0):
    """chamada gráfica em PT-BR: identidade, a habilidade numa frase, fichas (verificadas na ficha de factos)."""
    ch = b['chamada']; f = b['ficha']; d = ImageDraw.Draw(im, 'RGBA')
    k = eout((t - e['chamada_t']) / 0.25)
    if k <= 0: return
    a = int(255 * k); dy = (1 - k) * 30
    lines = wrap(d, ch['titulo'], BLK, 54, 840)
    rows, row, rw = [], [], 0
    for (c, tc) in zip(ch['chips'], e['chips_t']):
        cw_ = d.textlength(c[0], font=F(BOLD, 26)) + 36
        if row and rw + cw_ > 840: rows.append(row); row, rw = [], 0
        row.append((c, tc, cw_)); rw += cw_ + 12
    if row: rows.append(row)
    hh = 44 + 62 * len(lines) + 56 * len(rows) + 18
    d.rounded_rectangle((90, y0 + dy - 14, W - 90, y0 + dy + hh), radius=22, fill=(5, 10, 16, int(200 * k)))
    d.rectangle((90, y0 + dy + 6, 96, y0 + dy + hh - 20), fill=EM + (a,))
    tracked(d, f'{f["n"]}/6 · {f["nome"]} · {f["tipo"].upper()}', y0 + dy + 18, BOLD, 24, EM + (a,), track=0.08, x=120, maxw=820)
    y = y0 + dy + 44
    for ln in lines:
        d.text((120, y + 30), ln, font=F(BLK, 54), fill=WHITE + (a,), anchor='lm'); y += 62
    y += 6
    for r in rows:
        x = 120
        for (c, tc, cw_) in r:
            kk = eout((t - tc) / 0.2)
            if kk > 0:
                bg, fg = CHIPC[c[1]]; sc = 0.85 + 0.15 * kk
                d.rounded_rectangle((x, y + (1 - sc) * 22, x + cw_ * sc, y + 44 - (1 - sc) * 22), radius=22, fill=bg + (int(240 * kk * k),))
                d.text((x + cw_ * sc / 2, y + 22), c[0], font=F(BOLD, int(26 * sc)), fill=fg + (int(255 * kk * k),), anchor='mm')
            x += cw_ + 12
        y += 56

AMAR = set(CFG['legenda']['amarelo']); TROCA = CFG['legenda']['trocas']
def disp(i): return TROCA.get(str(i), WORDS[i]['w'])
CHUNKS = []; cur_ = []
for i, w in enumerate(WORDS):
    if w['cortada'] or disp(i) == '': continue
    cur_.append(i); txt = disp(i)
    if len(cur_) >= 4 or txt[-1] in '.:?!' or (txt[-1] == ',' and len(cur_) >= 2): CHUNKS.append(cur_); cur_ = []
if cur_: CHUNKS.append(cur_)
def subtitles(im, t):
    act = None
    for c in CHUNKS:
        if WORDS[c[0]]['s'] - 0.05 <= t: act = c
        else: break
    if act is None or t > WORDS[act[-1]]['e'] + 0.6: return
    band = Image.new('L', (W, 190), 0); ImageDraw.Draw(band).rectangle((0, 40, W, 150), fill=120)
    im.paste((5, 10, 16), (0, 1453), band.filter(ImageFilter.GaussianBlur(30)))
    d = ImageDraw.Draw(im, 'RGBA'); f = F(BLK, 58)
    toks = [disp(i) for i in act]; sp = d.textlength(' ', font=f)
    widths = [d.textlength(s, font=f) for s in toks]; tot = sum(widths) + sp * (len(toks) - 1)
    if tot > 980:
        f = F(BLK, int(58 * 980 / tot)); sp = d.textlength(' ', font=f); widths = [d.textlength(s, font=f) for s in toks]; tot = sum(widths) + sp * (len(toks) - 1)
    x = (W - tot) / 2
    for i, s, w in zip(act, toks, widths):
        if WORDS[i]['s'] - 0.05 <= t:
            d.text((x, 1548), s, font=f, fill=YEL if i in AMAR else WHITE, anchor='lm', stroke_width=5, stroke_fill=INK)
        x += w + sp

# ---------- entradas de carta (cada descoberta tem a sua) ----------
def card_dark(c, k):
    if k >= 0.999: return c
    a = np.array(c, np.float32); a[..., :3] *= (0.08 + 0.92 * k); return Image.fromarray(a.astype(np.uint8))
def entry_luz(c, r):
    """faixa de luz diagonal que acende a carta (Tecton)."""
    a = np.array(c, np.float32); h, w = a.shape[:2]
    u = (np.arange(w)[None, :] / w + np.arange(h)[:, None] / h) / 2
    edge = r * 1.35 - 0.15
    lit = np.clip((edge - u) / 0.18, 0, 1); band = np.exp(-((u - edge) / 0.035) ** 2) * (r < 1.05)
    a[..., :3] = a[..., :3] * (0.07 + 0.93 * lit[..., None]) + band[..., None] * 140
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
def draw_scanframe(d, x, y, w, h, k):
    L = 70; c = EM + (int(255 * k),); th = 6
    for (px, py, sx, sy) in ((x, y, 1, 1), (x + w, y, -1, 1), (x, y + h, 1, -1), (x + w, y + h, -1, -1)):
        d.line((px, py, px + sx * L, py), fill=c, width=th); d.line((px, py, px, py + sy * L), fill=c, width=th)

def scene_carta(im, t, e, b):
    """devolve (câmara, hud) depois de desenhar a carta, a comparação e o selo."""
    hud = {}
    t0 = e['t']; tch = e.get('chamada_t', 1e9)
    k_ab = ease((t - tch) / 0.35) if t >= tch else 0.0
    sc = lerp(FULL[0], ABIL[0], k_ab); top = lerp(FULL[1], ABIL[1], k_ab)
    cw, x, y, ch_ = geom(sc, top); y += bob(t)
    name = b['carta']; c = card(name, cw); cam = IDENT; est = b.get('estilo')
    dt = t - t0
    if est == 'arte' and dt < 1.3:
        fx, fy = b['foco']; z = lerp(2.1, 1.0, eout(dt / 1.3))
        cam = (lerp(x + fx * cw / 745, W / 2, eout(dt / 1.3)), lerp(y + fy * cw / 745, H / 2, eout(dt / 1.3)), z)
    if est == 'pan' and dt < 1.9:
        (fx, fy), (gx, gy) = b['foco'], b['foco2']
        if dt < 1.5:
            kk = ease(dt / 1.5); cam = (x + lerp(fx, gx, kk) * cw / 745, y + lerp(fy, gy, kk) * cw / 745, 1.9)
        else:
            kk = eout((dt - 1.5) / 0.4); cam = lcam((x + gx * cw / 745, y + gy * cw / 745, 1.9), IDENT, kk)
    if est == 'scan' and dt < 0.9:
        rv = eout(dt / 0.75); hpx = int(c.height * rv)
        if hpx > 0:
            part = c.crop((0, 0, c.width, hpx)); paste_card(im, part, x, y, shade=False)
        d = ImageDraw.Draw(im, 'RGBA'); ly = y + hpx
        if rv < 1:
            for g_, a_ in ((18, 40), (8, 90), (2, 255)): d.rectangle((x - 20, ly - g_, x + cw + 20, ly + g_), fill=EM + (a_,))
        draw_scanframe(d, x - 24, y - 24, cw + 48, c.height + 48, 1 - max(0, (dt - 0.6) / 0.3))
    elif est == 'flip' and dt < 0.45:
        kk = eout(dt / 0.45); sx = max(0.02, math.sin(math.pi / 2 * kk)); w2 = max(4, int(cw * sx))
        c2 = card_dark(c.resize((w2, c.height), Image.BILINEAR), 0.35 + 0.65 * kk)
        paste_card(im, c2, x + (cw - w2) / 2, y)
    elif est == 'luz' and dt < 1.0:
        paste_card(im, entry_luz(c, dt / 0.95), x, y); cam = (W / 2, y + c.height / 2, lerp(1.08, 1.0, eout(dt / 1.0)))
    else:
        paste_card(im, c, x, y)
    # comparação (entra do canto inferior direito, inclinada)
    comp = None
    for s in e['sub']:
        if 'comparacao' in s and t >= s['t']:
            t1 = next((z['t'] for z in e['sub'] if z.get('fim_comparacao') and z['t'] > s['t']), e['t1'] - 0.2)
            comp = (s['comparacao'], s['t'], t1)
    if comp and t < comp[2] + 0.2:
        nm, c0, c1 = comp; kk = eout((t - c0) / 0.27) if t < c1 else 1 - ease((t - c1) / 0.2)
        cc = card(nm, W * 0.40).rotate(-9, expand=True, resample=Image.BICUBIC)
        fx, fy = W - cc.width - 40, y + ch_ * 0.30; sx, sy = W + 40, H + 60
        paste_card(im, cc, lerp(sx, fx, kk), lerp(sy, fy, kk))
        if c0 <= t < c1: hud['credit'] = (nm, y + ch_ + 22)
    hud.setdefault('credit', (name, y + ch_ + 22))
    # selo
    for s in e['sub']:
        if 'selo' in s and t >= s['t']:
            kk = eout((t - s['t']) / 0.22); d = ImageDraw.Draw(im, 'RGBA'); s1, s2 = s['selo']
            bw = 640 * (0.85 + 0.15 * kk); yy = y + ch_ * 0.52
            d.rounded_rectangle((W / 2 - bw / 2, yy, W / 2 + bw / 2, yy + 150), radius=26, fill=EM + (int(245 * kk),))
            d.text((W / 2, yy + 58), s1, font=F(BLK, 74), fill=INK + (int(255 * kk),), anchor='mm')
            d.text((W / 2, yy + 118), s2, font=fit(d, s2, BOLD, 24, bw - 40), fill=INK + (int(230 * kk),), anchor='mm')
    hud['painel_y'] = y + ch_ + 58 - bob(t)
    fic0 = t0 + {'arte': 1.3, 'pan': 1.9, 'luz': 0.8}.get(est, 0.4)
    if b.get('ficha') and fic0 <= t < tch: hud['ficha'] = (b['ficha'], fic0)
    return cam, hud

def scene_lotus(im, t, e, b):
    cw, x, y, ch_ = geom(*HERO); y += bob(t) * 0.5
    nm = b['carta_lit']
    if t < LIT:   # silhueta no mesmo enquadramento do gancho, a câmara desce devagar
        z = lerp(1.0, 1.06, (t - e['t']) / max(0.1, LIT - e['t']))
        paste_card(im, silhouette(nm, cw, 0.12 + 0.05 * math.sin(t * 6)), x, y)
        return (W / 2, y + ch_ / 2, z), {}
    tch = e['chamada_t']
    if t < tch:
        kk = ease((t - LIT) / 0.5)
        glow(im, x, y, cw, ch_, kk * (0.75 + 0.25 * math.sin((t - LIT) * 3)))
        paste_card(im, silhouette(nm, cw, 0.12), x, y)
        c = card(nm, cw).copy(); c.putalpha(Image.fromarray((np.array(c.getchannel('A')) * kk).astype(np.uint8)))
        im.alpha_composite(c, (int(x), int(y)))
        z = lerp(1.0, 1.04, (t - LIT) / max(0.1, tch - LIT))
        return (W / 2, y + ch_ / 2, z), {'ficha': (b['ficha'], LIT), 'credit': (nm, y + ch_ + 22), 'ficha_y': min(1428, y + ch_ + 46)}
    # modo habilidade: a carta do herói encolhe para o enquadramento das outras
    k_ab = ease((t - tch) / 0.35)
    sc = lerp(HERO[0], ABIL[0], k_ab); top = lerp(HERO[1], ABIL[1], k_ab)
    b2 = dict(b, carta=nm); e2 = dict(e)
    cw2, x2, y2, ch2 = geom(sc, top); y2 += bob(t)
    glow(im, x2, y2, cw2, ch2, 0.5)
    fake = dict(e2); fake['chamada_t'] = -1
    # desenha como plano de carta já em modo habilidade, com a escala interpolada
    global FULL
    saved = FULL; FULL = (sc, top)
    cam, hud = scene_carta(im, t, dict(e, chamada_t=tch), dict(b2, estilo=None, ficha=b['ficha']))
    FULL = saved
    return cam, hud

def scene_decks(im, t, e, b):
    d = ImageDraw.Draw(im, 'RGBA'); k = eout((t - e['t']) / 0.25); a = int(255 * k)
    text_center(d, CFG['data_lancamento'], 470, BLK, 150, WHITE + (a,), stroke=4)
    text_center(d, CFG['set'].upper(), 575, SEMI, 38, (210, 235, 240, a))
    tracked(d, f'{len(b["decks"])} DECKS DE COMMANDER', 700, BOLD, 30, EM + (a,), track=0.18)
    for i, nm in enumerate(b['decks']):
        kk = eout((t - e['t'] - 0.15 - i * TL['P']) / 0.2)
        if kk <= 0: continue
        y = 760 + i * 128; x0 = 110 + (1 - kk) * 80
        d.rounded_rectangle((x0, y, x0 + 860, y + 106), radius=18, fill=(8, 14, 26, int(225 * kk)), outline=(255, 255, 255, int(40 * kk)), width=2)
        d.rectangle((x0, y + 14, x0 + 8, y + 92), fill=EM + (int(255 * kk),))
        d.text((x0 + 40, y + 53), nm.upper(), font=fit(d, nm.upper(), BLK, 50, 620), fill=WHITE + (int(255 * kk),), anchor='lm')
        d.text((x0 + 830, y + 53), 'COMMANDER', font=F(BOLD, 20), fill=(170, 210, 220, int(220 * kk)), anchor='rm')

GRID = dict(mw=290, gap=25, y1=250, y2=760)
def grid(im, t, t0, minis, label=True):
    d = ImageDraw.Draw(im, 'RGBA'); mw, gap = GRID['mw'], GRID['gap']; x0 = (W - 3 * mw - 2 * gap) / 2
    for i, (n, nome) in enumerate(minis):
        k = eout((t - t0 - i * 0.07) / 0.22)
        if k <= 0: continue
        c = card(n, mw); x = x0 + (i % 3) * (mw + gap); y = (GRID['y1'] if i < 3 else GRID['y2']) + (1 - k) * 40
        paste_card(im, c, x, y)
        d = ImageDraw.Draw(im, 'RGBA')
        d.ellipse((x - 20, y - 20, x + 70, y + 70), fill=EM + (255,), outline=INK + (255,), width=5)
        d.text((x + 25, y + 25), str(i + 1), font=F(BLK, 56), fill=INK, anchor='mm')
        if label: d.text((x + mw / 2, y + c.height + 26), nome, font=fit(d, nome, BOLD, 24, mw), fill=WHITE + (int(255 * k),), anchor='mm')

SCAN = CFG['scanner']; SCAN_DIR = os.path.abspath(f'{EP}/{SCAN["pasta"]}')
_scan = {}
def scan_frame(i):
    i = max(SCAN['quadros'][0], min(SCAN['quadros'][1], int(i)))
    if i not in _scan: _scan[i] = Image.open(f'{SCAN_DIR}/{i:03d}.jpg').convert('RGBA')
    return _scan[i]
def scene_scanner(im, t, e):
    """gravação real do scanner (comum/outro/scan), reduzida para dar lugar a um título fora do telemóvel."""
    dt = t - e['t']; q0, q1 = SCAN['quadros']; speed = 15 if e.get('destaque') else 30
    fr = scan_frame(q0 + dt * speed); sc = 0.78
    im.alpha_composite(fr.resize((int(W * sc), int(H * sc)), Image.BICUBIC), (int(W * (1 - sc) / 2), 330))
    d = ImageDraw.Draw(im, 'RGBA'); k = eout(dt / 0.25)
    if e.get('destaque'):
        if dt < 2.2: text_center(d, 'ESCANEIE SUAS CARTAS', 300, BLK, 68, WHITE + (int(255 * k),))
        else: text_center(d, 'E ORGANIZE SEUS DECKS', 300 + 20 * (1 - eout((dt - 2.2) / 0.2)), BLK, 68, EM + (255,))
    else:
        tracked(d, 'BINDER VISION · SCANNER', 300, BOLD, 30, EM + (int(255 * k),), track=0.2)

def scene_cartao(im, t, e):
    dt = t - e['t']; d = ImageDraw.Draw(im, 'RGBA')
    g = Image.new('L', (W, H), 0); ImageDraw.Draw(g).ellipse((140, 300, 940, 1100), fill=70)
    im.paste(EM, (0, 0), g.filter(ImageFilter.GaussianBlur(160)))
    k = eout(dt / 0.35); s = int(250 * (0.8 + 0.2 * k))
    lg = LOGO.resize((s, s), Image.LANCZOS).rotate(-90 * (1 - k), resample=Image.BICUBIC)
    im.alpha_composite(lg, (int(W / 2 - lg.width / 2), int(600 - lg.height / 2)))
    d = ImageDraw.Draw(im, 'RGBA'); f = F(BLK, 108); w1 = d.textlength('BINDER ', font=f); w2 = d.textlength('Vision', font=f)
    x = (W - w1 - w2) / 2; a = int(255 * eout((dt - 0.1) / 0.3))
    d.text((x, 860), 'BINDER ', font=f, fill=(255, 255, 255, a), anchor='lm'); d.text((x + w1, 860), 'Vision', font=f, fill=EM + (a,), anchor='lm')
    l1, l2, l3 = CFG['cartao_final'][1:]
    a2 = int(255 * eout((dt - 0.3) / 0.3))
    text_center(d, l1, 985, SEMI, 44, (255, 255, 255, a2))
    text_center(d, l2, 1055, SEMI, 40, (190, 245, 220, a2))
    if e.get('instalar'):
        a3 = int(255 * eout((dt - 0.5) / 0.3)); bw = 640
        d.rounded_rectangle((W / 2 - bw / 2, 1150, W / 2 + bw / 2, 1260), radius=55, fill=EM + (a3,))
        d.text((W / 2, 1205), 'BAIXE O BINDER VISION', font=F(BLK, 46), fill=INK + (a3,), anchor='mm')
        text_center(d, l3, 1320, BLK, 50, (255, 255, 255, a3))
    else:
        text_center(d, l3, 1140, BLK, 50, EM + (a2,))
    if t > TOTAL - 0.3:   # fecho a preto
        im.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * (t - (TOTAL - 0.3)) / 0.3))))

def hook(im, t, d):
    cw, x, y, ch_ = geom(*HERO); fl = CFG['abertura'].get('flash', 0.33)
    br = 0.16 + 0.5 * math.exp(-((t - fl) / 0.06) ** 2) + 0.04 * math.sin(t * 7)
    if abs(t - fl) < 0.12: glow(im, x, y, cw, ch_, 0.6 * math.exp(-((t - fl) / 0.06) ** 2))
    paste_card(im, silhouette(CFG['abertura']['silhueta'], cw, round(br, 2)), x, y + bob(t) * 0.5)
    return (W / 2, y + ch_ / 2, lerp(1.0, 1.12, ease(t / max(0.1, AB['t1']))))

def ev_at(t):
    a = None
    for e in MAIN:
        if e['t'] <= t: a = e
    return a

def frame(t):
    e = ev_at(t); b = BLOC[e['bloco']] if 'bloco' in e else None
    if e['tipo'] in ('scanner', 'cartao'):
        im = Image.new('RGBA', (W, H), INK + (255,))
        scene_scanner(im, t, e) if e['tipo'] == 'scanner' else scene_cartao(im, t, e)
        return im.convert('RGB')
    im = background(t); cam = IDENT; hud = {}
    d = ImageDraw.Draw(im, 'RGBA')
    if e['tipo'] == 'abertura': cam = hook(im, t, d)
    elif e['tipo'] == 'respiro':
        lay = b['camada']; k = eout((t - e['t']) / 0.28); idx = LAYERS.index(lay) + 1
        if b.get('pista_lotus'):   # indício: a carta-pagamento lá em baixo, quase invisível
            cw, x, y, ch_ = geom(0.34, 1180); paste_card(im, silhouette(CFG['abertura']['silhueta'], cw, 0.22 + 0.1 * math.sin(t * 9)), x, y, shade=False)
        tracked(d, CAM[lay]['nome'], 900 + 26 * (1 - k), BLK, 112, WHITE + (int(255 * k),), track=0.16)
        tracked(d, f'{idx:02d} / {len(CAM):02d}', 800, BOLD, 36, (255, 52, 52, int(255 * k)), track=0.22)
    elif e['tipo'] == 'carta': cam, hud = scene_carta(im, t, e, b)
    elif e['tipo'] == 'lotus': cam, hud = scene_lotus(im, t, e, b)
    elif e['tipo'] == 'decks': scene_decks(im, t, e, b)
    elif e['tipo'] == 'pergunta':
        grid(im, t, e['t'], b['miniaturas'])
        d = ImageDraw.Draw(im, 'RGBA'); k = eout((t - e['t'] - 0.3) / 0.3)
        text_center(d, b['texto'][0], 1290, BLK, 70, WHITE + (int(255 * k),), stroke=5)
        text_center(d, b['texto'][1], 1385, BLK, 84, YEL + (int(255 * k),), stroke=5)
    im = apply_cam(im, *cam)
    if e['tipo'] == 'abertura':
        d = ImageDraw.Draw(im, 'RGBA'); g = CFG['gancho'].split(); half = (len(g) + 1) // 2
        tracked(d, CFG['tag_serie'], 236, BOLD, 24, EM + (230,), track=0.2)
        for i, ln in enumerate((' '.join(g[:half]), ' '.join(g[half:]))):
            text_center(d, ln, 330 + i * 98, BLK, 88, WHITE + (255,), stroke=6)
    if e['tipo'] not in ('abertura',): draw_meter(im, t)
    draw_logo(im)
    if hud.get('credit') and cam[2] <= 1.01: credit(im, *hud['credit'])
    if hud.get('ficha'): ficha(im, hud['ficha'][0], hud['ficha'][1], t, hud.get('ficha_y', 1428))
    if e['tipo'] in ('carta', 'lotus') and b.get('chamada') and t >= e.get('chamada_t', 1e9): painel(im, b, e, t, hud.get('painel_y', 1160))
    subtitles(im, t)
    return im.convert('RGB')

def render_part(args):
    k, f0, f1 = args; path = f'{WK}/part_{VER}_{k}.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
    for fi in range(f0, f1): p.stdin.write(frame(fi / FPS).tobytes())
    p.stdin.close(); p.wait(); return path

def capas():
    a = FUNDO.frame(2.0, 'abismo', energy=0.7)
    cw, x, y, ch_ = geom(*HERO); paste_card(a, silhouette(CFG['abertura']['silhueta'], cw, 0.16), x, y)
    d = ImageDraw.Draw(a, 'RGBA'); g = CFG['gancho'].split(); half = (len(g) + 1) // 2
    for i, ln in enumerate((' '.join(g[:half]), ' '.join(g[half:]))): text_center(d, ln, 330 + i * 98, BLK, 88, WHITE, stroke=6)
    text_center(d, 'EXPEDIÇÃO BINDER #01', 1560, BLK, 64, EM, stroke=4); draw_logo(a)
    a.convert('RGB').save(f'{WK}/capa_A.png')
    bq = FUNDO.frame(2.0, 'grande', energy=0.6); grid(bq, 10, 0, BLOC[-1]['miniaturas'], label=False)
    d = ImageDraw.Draw(bq, 'RGBA'); text_center(d, 'NAUCTIS: 6 ESPÉCIES', 1330, BLK, 100, YEL, stroke=7)
    text_center(d, 'EXPEDIÇÃO BINDER #01', 1460, BLK, 56, EM, stroke=4); draw_logo(bq)
    bq.convert('RGB').save(f'{WK}/capa_B.png')

if __name__ == '__main__':
    if MODE == 'stills':
        for s in sys.argv[5:]: frame(float(s)).save(f'{WK}/still_{VER}_{float(s):05.2f}.png')
    elif MODE == 'capas': capas()
    else:
        n = int(round(TOTAL * FPS)); Pn = int(os.environ.get('PARTES', os.cpu_count() or 2)); step = math.ceil(n / Pn)
        with Pool(Pn) as pool: parts = pool.map(render_part, [(k, k * step, min(n, (k + 1) * step)) for k in range(Pn)])
        open(f'{WK}/parts_{VER}.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
        out = f'{WK}/{CFG["versoes"][VER]["ficheiro"]}.mp4'
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', f'{WK}/parts_{VER}.txt', '-i', f'{WK}/mix_final_{VER}.wav',
                        '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-shortest', '-movflags', '+faststart', out], check=True)
        print(out)
