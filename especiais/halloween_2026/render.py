"""BINDER Originals · Especial de Halloween · Innistrad × Duskmourn: O Julgamento do Horror — render das imagens.
Precisa de: tl.json (tl.py), linhas.json (vozes.py), mb_frames/ (render_mb.py), cartas em CARTAS, kit em KIT.
uso: python3 render.py                 -> kit.mp4 (sem áudio, até ao corte do kit; o fecho entra no build)
     python3 render.py stills 3 25 61  -> stills/still_03.00.jpg ...
"""
import json, math, sys, subprocess, pathlib, re, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageOps
W, H, FPS = 1080, 1920, 30
KIT = '/root/repo/'; CARTAS = '/root/work/cards/'; FONTS = '/root/work/fonts/'
TL = json.load(open('tl.json')); LIN = json.load(open('linhas.json'))
FALAS = TL['falas']; CENAS = TL['cenas']; PREVIA = TL['previa']
_fc = {}
def F(p, s, var=None):
    k = (p, s, var)
    if k not in _fc:
        f = ImageFont.truetype(p, s)
        if var: f.set_variation_by_name(var)
        _fc[k] = f
    return _fc[k]
GEIST = FONTS + 'Geist-Bold.ttf'; GEISTM = FONTS + 'Geist-Medium.ttf'; BANG = FONTS + 'bangers-latin-400-normal.ttf'
COMIC = FONTS + 'comic-neue-latin-700-normal.ttf'
LORA = '/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf'; LORAI = '/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'; MONOB = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
INTSB = '/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf'; INTB = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
INTM = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
BG = (5, 10, 16); EM = (16, 185, 129); PH = (0, 255, 65); WHITE = (236, 241, 245); YEL = (255, 216, 74)
IVORY = (244, 240, 230); INK = (17, 17, 17); BORDO = (118, 47, 50); GRAVURA = (119, 115, 108)
RED = (255, 90, 78); BURNC = (200, 53, 43); MANAC = (46, 140, 138)
def ease(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)
def eio(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3
def lerp(a, b, q): return a + (b - a) * q
def L(name): return Image.open(CARTAS + name).convert('RGBA')

# ---------------- assets ----------------
CARD = {k: L(k + '.png') for k in ['emrakul', 'valgavoth', 'huntmaster', 'mindskinner', 'moorland', 'annex', 'toxrill', 'hullbreaker']}
CARD['annex_rot'] = CARD['annex'].rotate(-90, expand=True)          # Room: lê-se deitada
ART = {k: Image.open(CARTAS + k + '_art.jpg').convert('RGB') for k in
       ['emrakul', 'valgavoth', 'huntmaster', 'mindskinner', 'moorland', 'annex', 'bloodline', 'arabella', 'island']}
META = json.load(open(CARTAS + 'meta.json'))
TUBO = Image.open(KIT + 'oraculo/assets/tubo_mestra_916.png').convert('RGB')
CONDE = {k: Image.open(KIT + f'conde/assets/{k}.png').convert('RGB') for k in ['neutro', 'desconfiado', 'admirado', 'indignado']}
LOGO = Image.open(KIT + 'manaburn/logo/logo_mark.png').convert('RGBA')
def cred(k, extra=''):
    m = META[k]; return f"{m['name']} ({m['set_name']}, {m['year']}), nº {m['num']}. Arte: {m['artist']}.{extra}"

# ---------------- texto ----------------
def parse(s):   # '*palavra*' = destaque; devolve palavras como listas de segmentos [(texto, destaque)]
    words = []; key = False
    for tok in s.split(' '):
        segs = []
        for part in tok.split('*'):
            if part: segs.append((part, key))
            key = not key
        key = not key            # o último split não alterna
        if segs: words.append(segs)
    return words
def wtxt(w): return ''.join(x for x, _ in w)
def wrap(d, words, font, maxw):
    lines = [[]]
    for w in words:
        test = ' '.join(wtxt(x) for x in lines[-1] + [w])
        if lines[-1] and d.textlength(test, font=font) > maxw: lines.append([w])
        else: lines[-1].append(w)
    return lines
def caption(im, s, st, bottom=1480, maxw=940, nchars=None, x0=None):
    """st: dict(font, col, key, stroke, scol). nchars: quantos caracteres já 'digitados' (TUBO)."""
    d = ImageDraw.Draw(im); f = st['font']; words = parse(s)
    lines = wrap(d, words, f, maxw); lh = int(f.size * 1.18)
    y = bottom - lh * len(lines); shown = 0; ops = []; stop = False
    for ln in lines:
        txt = ' '.join(wtxt(w) for w in ln); x = (W - d.textlength(txt, font=f)) / 2 if x0 is None else x0
        for w in ln:
            for seg, k in w + [(' ', False)]:
                t = seg
                if nchars is not None:
                    if shown >= nchars: stop = True; break
                    t = seg[:max(0, nchars - shown)]; shown += len(seg)
                if t.strip(): ops.append((x, y, t, k))
                x += d.textlength(seg, font=f)
            if stop: break
        if stop: break
        y += lh
    sw = st.get('stroke', 0)
    if sw:   # 1.º os contornos, depois o miolo: o contorno de uma palavra não come a anterior
        for x, y, t, k in ops: d.text((x, y), t, font=f, fill=st['scol'], stroke_width=sw, stroke_fill=st['scol'])
    for x, y, t, k in ops: d.text((x, y), t, font=f, fill=st['key'] if k else st['col'])
ST_MB = dict(font=F(GEIST, 47), col=(255, 255, 255), key=YEL, stroke=10, scol=(0, 0, 0))
ST_KD = dict(font=F(LORAI, 50, 'Bold Italic'), col=IVORY, key=(217, 164, 65), stroke=5, scol=(10, 8, 6))
ST_KI = dict(font=F(LORA, 46, 'Bold'), col=INK, key=BORDO, stroke=0)
ST_T = dict(font=F(MONOB, 40), col=PH, key=WHITE, stroke=6, scol=BG)

def fala_em(t, cena=None):
    best = None
    for f in FALAS:
        if f['start'] - 0.02 <= t < f['start'] + f['dur'] + 0.25 and (cena is None or f['cena'] == cena): best = f
    return best
def falando(t, f): return f and f['start'] <= t < f['start'] + f['dur']
def pill(d, xy, txt, font, bg, fg, pad=(14, 6), r=8, anchor='l'):
    x, y = xy; w = d.textlength(txt, font=font); h = font.size
    if anchor == 'c': x -= (w + 2 * pad[0]) / 2
    d.rounded_rectangle((x, y, x + w + 2 * pad[0], y + h + 2 * pad[1] + 4), r, fill=bg)
    d.text((x + pad[0], y + pad[1]), txt, font=font, fill=fg); return x + w + 2 * pad[0]
def previa_tag(im, f, bottom):
    if f and f.get('previa'):
        d = ImageDraw.Draw(im, 'RGBA'); s = 'PRÉVIA · voz pendente'
        pill(d, (W / 2, bottom + 10), s, F(INTSB, 22), (150, 20, 20, 220), (255, 235, 235), anchor='c')
def marca_previa(im):
    if not PREVIA: return
    d = ImageDraw.Draw(im, 'RGBA'); pill(d, (W - 60 - 230, 64), 'PRÉVIA · não publicar', F(INTSB, 24), (170, 20, 20, 230), (255, 255, 255))

# ---------------- fundos ----------------
def cover(img, w, h):
    s = max(w / img.width, h / img.height); im = img.resize((int(img.width * s) + 1, int(img.height * s) + 1), Image.LANCZOS)
    x = (im.width - w) // 2; y = (im.height - h) // 2; return im.crop((x, y, x + w, y + h))
def tint(img, col, sat=0.25, k=0.55):
    g = ImageOps.grayscale(img).convert('RGB'); img = Image.blend(g, img, sat)
    return Image.blend(img, Image.new('RGB', img.size, col), k)
_bg = {}
def bg_innistrad(art, w=W, h=H):
    k = ('i', art, w, h)
    if k not in _bg: _bg[k] = tint(cover(ART[art], w, h).filter(ImageFilter.GaussianBlur(22)), (16, 24, 38), 0.2, 0.55)
    return _bg[k].copy()
def bg_dusk(art, w=W, h=H):
    k = ('d', art, w, h)
    if k not in _bg:
        im = tint(cover(ART[art], w, h).filter(ImageFilter.GaussianBlur(22)), (58, 8, 10), 0.45, 0.5)
        d = ImageDraw.Draw(im, 'RGBA')
        for y in range(0, h, 4): d.line((0, y, w, y), fill=(0, 0, 0, 55))
        _bg[k] = im
    return _bg[k].copy()
VIG = Image.new('L', (W, H), 0); ImageDraw.Draw(VIG).ellipse((-260, -160, W + 260, H + 160), fill=255); VIG = VIG.filter(ImageFilter.GaussianBlur(200))
def vignette(im, strength=1.0):
    dark = Image.new('RGB', (W, H), (0, 0, 0)); m = VIG if strength >= 1 else VIG.point(lambda v: int(255 - (255 - v) * strength))
    return Image.composite(im, dark, m)
def vhs_lines(im, t, x0=0, x1=W, n=5, seed=0):
    d = ImageDraw.Draw(im, 'RGBA'); r = np.random.default_rng(int(t * 30) + seed)
    for _ in range(n):
        y = int(r.uniform(0, H)); d.line((x0, y, x1, y), fill=(255, 255, 255, int(r.uniform(15, 50))), width=int(r.integers(1, 3)))
def glitch(im, t, amount=1.0):
    r = np.random.default_rng(int(t * 60)); a = np.array(im)
    for _ in range(int(10 * amount)):
        y0 = int(r.integers(0, H - 40)); hh = int(r.integers(6, 60)); sh = int(r.integers(-60, 60) * amount)
        a[y0:y0 + hh] = np.roll(a[y0:y0 + hh], sh, axis=1)
    im = Image.fromarray(a); R_, G_, B_ = im.split(); off = int(12 * amount)
    return Image.merge('RGB', (ImageChops.offset(R_, off, 0), G_, ImageChops.offset(B_, -off, 0)))
def fog(im, t, y0, y1, seed=1, alpha=70):
    lay = Image.new('L', (W // 4, (y1 - y0) // 4), 0); d = ImageDraw.Draw(lay); r = np.random.default_rng(seed)
    for k in range(9):
        cx = (r.uniform(0, 1) * W / 4 + t * r.uniform(6, 16)) % (W / 4 + 120) - 60; cy = r.uniform(0, (y1 - y0) / 4)
        rx, ry = r.uniform(60, 130), r.uniform(10, 26); d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=int(alpha))
    lay = lay.filter(ImageFilter.GaussianBlur(10)).resize((W, y1 - y0), Image.BICUBIC)
    white = Image.new('RGB', (W, y1 - y0), (200, 212, 225)); reg = im.crop((0, y0, W, y1))
    im.paste(Image.composite(white, reg, lay), (0, y0))

def paste_card(im, card, x, y, w, glow=None):
    c = card.resize((int(w), int(round(card.height * w / card.width))), Image.LANCZOS)
    if glow:
        g = Image.new('RGBA', (c.width + 80, c.height + 80), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        gd.rounded_rectangle((40, 40, 40 + c.width, 40 + c.height), 24, fill=glow); g = g.filter(ImageFilter.GaussianBlur(18))
        im.paste(g, (int(x) - 40, int(y) - 40), g)
    sh = Image.new('RGBA', (c.width + 40, c.height + 40), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((20, 26, 20 + c.width, 26 + c.height), 22, fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(10)); im.paste(sh, (int(x) - 20, int(y) - 20), sh)
    im.paste(c, (int(x), int(y)), c); return (x, y, c.width, c.height)
def hl_rects(im, box, rects, q, card_w, card_h):
    """destaques do kit: contorno amarelo à volta das linhas do Oracle (nunca por cima do texto)."""
    if q <= 0: return
    d = ImageDraw.Draw(im, 'RGBA'); x, y, w, h = box
    for i, (rx, ry, rw, rh) in enumerate(rects):
        qq = min(1, max(0, q * len(rects) - i))
        if qq <= 0: continue
        X0 = x + rx / card_w * w - 4; Y0 = y + ry / card_h * h - 3; X1 = X0 + (rw / card_w * w + 8) * qq; Y1 = y + (ry + rh) / card_h * h + 3
        d.rounded_rectangle((X0, Y0, X1, Y1), 5, outline=YEL + (255,), width=4)

# ---------------- elementos comuns ----------------
PONTOS = [('veredito1', 'I'), ('veredito2', 'D'), ('veredito3', 'D'), ('veredito4', 'I'), ('erro', 'I')]
CEN = {c['nome']: c for c in CENAS}
def placar(t):
    i = d_ = 0; last = None
    for nome, who in PONTOS:
        c = CEN[nome]
        if t >= c['a'] + 0.35:
            if who == 'I': i += 1
            else: d_ += 1
            last = (who, c['a'] + 0.35)
    return i, d_, last
def draw_placar(im, t, y=222, x=60, big=False):
    d = ImageDraw.Draw(im, 'RGBA'); i, dd, last = placar(t); s = 1.5 if big else 1.0
    fI = F(LORA, int(30 * s), 'Bold'); fD = F(MONOB, int(28 * s)); fN = F(BANG, int(46 * s))
    flash = last and 0 <= t - last[1] < 0.5
    hgt = int(54 * s); wI = d.textlength('INNISTRAD', font=fI) + 30; wD = d.textlength('DUSKMOURN', font=fD) + 30; wN = int(60 * s)
    if big: x = (W - (wI + wN * 2 + int(40 * s) + wD)) / 2
    d.rectangle((x, y, x + wI, y + hgt), fill=(24, 32, 46, 235)); d.text((x + 15, y + hgt / 2), 'INNISTRAD', font=fI, fill=IVORY, anchor='lm')
    xx = x + wI
    for k, (n, col) in enumerate(((i, IVORY), (dd, (255, 120, 110)))):
        hot = flash and ((last[0] == 'I') == (k == 0))
        d.rectangle((xx, y, xx + wN, y + hgt), fill=(YEL + (255,)) if hot else (10, 12, 16, 240))
        d.text((xx + wN / 2, y + hgt / 2 + 2), str(n), font=fN, fill=(10, 10, 10) if hot else col, anchor='mm'); xx += wN
        if k == 0: d.rectangle((xx, y, xx + int(40 * s), y + hgt), fill=(10, 12, 16, 240)); d.text((xx + 20 * s, y + hgt / 2), '×', font=fN, fill=YEL, anchor='mm'); xx += int(40 * s)
    d.rectangle((xx, y, xx + wD, y + hgt), fill=(70, 12, 14, 235)); d.text((xx + 15, y + hgt / 2), 'DUSKMOURN', font=fD, fill=(255, 205, 200), anchor='lm')
def bug(im):
    d = ImageDraw.Draw(im, 'RGBA'); fa = F(BANG, 34); fb = F(GEIST, 17)
    w = d.textlength('BINDER ORIGINALS', font=fa); d.rectangle((60, 140, 60 + w + 28, 182), fill=(20, 18, 16, 200)); d.text((74, 145), 'BINDER ORIGINALS', font=fa, fill=(242, 235, 218))
    w2 = d.textlength('ESPECIAL DE HALLOWEEN', font=fb); d.rectangle((60, 182, 60 + w2 + 28, 208), fill=(122, 30, 30, 255)); d.text((74, 186), 'ESPECIAL DE HALLOWEEN', font=fb, fill=(255, 255, 255))
def rodape_wotc(im, y=1500, col=(220, 220, 220)):
    d = ImageDraw.Draw(im, 'RGBA'); d.text((W / 2, y), '© Wizards of the Coast · Conteúdo de fã não oficial, sem endosso da Wizards', font=F(INTM, 20), fill=col + (200,), anchor='ma')
def nametag(im, t, t0, x, y, nome, sub, col, dur=2.6, font=None):
    q = ease((t - t0) / 0.25) * (1 - ease((t - t0 - dur) / 0.3))
    if q <= 0.01: return
    d = ImageDraw.Draw(im, 'RGBA'); f1 = font or F(BANG, 44); f2 = F(GEIST, 22)
    w = max(d.textlength(nome, font=f1), d.textlength(sub, font=f2)) + 36; xo = x - (1 - q) * 40
    d.rectangle((xo, y, xo + w, y + 92), fill=(12, 12, 14, int(225 * q))); d.rectangle((xo, y, xo + 8, y + 92), fill=col + (int(255 * q),))
    d.text((xo + 22, y + 6), nome, font=f1, fill=(255, 255, 255, int(255 * q))); d.text((xo + 22, y + 58), sub, font=f2, fill=(210, 210, 210, int(255 * q)))

# ---------------- PIP do Burn / Mana (quadros do kit) ----------------
_mbc = {}
def mb_frame(n):
    p = pathlib.Path(f'mb_frames/{n:05d}.jpg')
    if not p.exists(): return None
    if n not in _mbc:
        if len(_mbc) > 40: _mbc.clear()
        _mbc[n] = Image.open(p).convert('RGB')
    return _mbc[n]
PIPC = {'B': (560, 720, 520), 'M': (520, 690, 500)}
MASK = Image.new('L', (200, 200), 0); ImageDraw.Draw(MASK).ellipse((0, 0, 199, 199), fill=255)
def pip(im, t, f, x=850, y=140):
    if not f or f['quem'] not in 'BM': return
    fr = mb_frame(int(round(t * FPS)))
    if fr is None: return
    cx, cy, s = PIPC[f['quem']]; face = fr.crop((cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2)).resize((200, 200), Image.LANCZOS)
    q = ease((t - f['start'] + 0.1) / 0.2); d = ImageDraw.Draw(im, 'RGBA'); col = BURNC if f['quem'] == 'B' else MANAC
    yy = y - (1 - q) * 30
    d.ellipse((x - 8, yy - 8, x + 208, yy + 208), fill=col + (int(255 * q),))
    im.paste(face, (x, int(yy)), MASK.point(lambda v: int(v * q)))
    nm = 'BURN' if f['quem'] == 'B' else 'MANA'
    pill(d, (x + 100, yy + 196), nm, F(BANG, 30), col + (int(255 * q),), (255, 255, 255), anchor='c')

# ---------------- TUBO (do ep02_render.py, sem mudar o personagem) ----------------
SCR = (492, 566, 740, 792); SCX, SCY = (SCR[0] + SCR[2]) / 2, (SCR[1] + SCR[3]) / 2
EYES = [(518, 615, 596, 702), (634, 615, 709, 702)]; LEDP = (592, 828)
GLY = '0123456789ABCDEF#*+=<>/:'; rng = np.random.default_rng(13)
rain_cols = [dict(x=x, y=rng.uniform(0, 300), v=rng.uniform(40, 90)) for x in range(500, 736, 14)]
def led_amp(t):
    f = fala_em(t)
    if not f or f['quem'] != 'T' or not falando(t, f): return 0.0
    e = LIN[f['id']].get('env30') or []
    if e:
        i = int((t - f['start']) * 30); return float(e[i]) if i < len(e) else 0.0
    return 0.55 + 0.45 * math.sin(t * 23) * math.sin(t * 7.1)      # PRÉVIA: piscar sintético (sem áudio)
def glitch_eyes(im, t):
    box = (SCR[0] + 6, SCR[1] + 6, SCR[2] - 6, SCR[3] - 6); reg = im.crop(box); r, g, b = reg.split()
    off = 9 + int(4 * math.sin(t * 40)); z = Image.new('L', reg.size, 0)
    reg2 = ImageChops.add(ImageChops.offset(Image.merge('RGB', (r, z, z)), off, 0), ImageChops.offset(Image.merge('RGB', (z, g, b)), -off, 0))
    rr = np.random.default_rng(int(t * 30) + 7); arr = np.array(reg2)
    for _ in range(4):
        y0 = rr.integers(0, arr.shape[0] - 12); hh = rr.integers(4, 14); sh = rr.integers(-18, 18); arr[y0:y0 + hh] = np.roll(arr[y0:y0 + hh], sh, axis=1)
    im.paste(Image.fromarray(arr), box[:2]); return im
def tubo_frame(t, expr='analitico', zoom=1.0, cx=None, cy=None, red_led=False):
    im = TUBO.copy(); d = ImageDraw.Draw(im, 'RGBA'); fs = F(MONO, 13)
    for c in rain_cols:
        y = SCR[1] + ((c['y'] + t * c['v']) % (SCR[3] - SCR[1] + 40)) - 20
        for k in range(5):
            yy = y - k * 15
            if SCR[1] + 8 < yy < SCR[3] - 14 and not any(e[0] - 6 < c['x'] < e[2] + 6 and e[1] - 8 < yy < e[3] + 4 for e in EYES):
                d.text((c['x'], yy), GLY[int(t * 8 + k + c['x']) % len(GLY)], font=fs, fill=(0, 255, 65, int(150 * (1 - k / 5) * (0.6 if expr != 'desconfiado' else 0.2))))
    lid = 0.0; bt = t % 4.3
    if bt < 0.14 and expr != 'erro': lid = math.sin(bt / 0.14 * math.pi)
    if expr == 'desconfiado': lid = max(lid, 0.45)
    if expr == 'confiante': lid = max(lid, 0.22)
    if lid > 0.01:
        for i, e in enumerate(EYES):
            h = (e[3] - e[1] + 4) * lid
            if expr == 'confiante' and lid < 0.5 and i == 1: h *= 0.4
            if expr == 'desconfiado' and i == 0: h *= 0.55
            d.rectangle((e[0] - 3, e[1] - 3, e[2] + 3, e[1] - 3 + h), fill=BG + (255,)); d.line((e[0] - 3, e[1] - 3 + h, e[2] + 3, e[1] - 3 + h), fill=(16, 185, 129, 160), width=3)
    if expr == 'erro': im = glitch_eyes(im, t)
    d = ImageDraw.Draw(im, 'RGBA'); a = led_amp(t)
    d.ellipse((LEDP[0] - 7, LEDP[1] - 7, LEDP[0] + 7, LEDP[1] + 7), fill=(8, 40, 26, 255))
    if red_led:
        if int(t * 6) % 2 == 0:
            g = Image.new('RGBA', (120, 120), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((40, 40, 80, 80), fill=(255, 40, 40, 220)); g = g.filter(ImageFilter.GaussianBlur(14))
            im.paste(g, (LEDP[0] - 60, LEDP[1] - 60), g); d.ellipse((LEDP[0] - 6, LEDP[1] - 6, LEDP[0] + 6, LEDP[1] + 6), fill=(255, 120, 120, 255))
        else: d.ellipse((LEDP[0] - 6, LEDP[1] - 6, LEDP[0] + 6, LEDP[1] + 6), fill=(70, 10, 10, 255))
    elif a > 0.03:
        g = Image.new('RGBA', (120, 120), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((40, 40, 80, 80), fill=(16, 185, 129, int(200 * a))); g = g.filter(ImageFilter.GaussianBlur(14))
        im.paste(g, (LEDP[0] - 60, LEDP[1] - 60), g); d.ellipse((LEDP[0] - 6, LEDP[1] - 6, LEDP[0] + 6, LEDP[1] + 6), fill=(120, 255, 190, int(80 + 175 * a)))
    z = max(1.0, zoom) * (1 + 0.008 * (1 + math.sin(t * 1.3)) / 2)
    if cx is None: cx, cy = W / 2, H / 2
    if expr == 'erro':
        r = np.random.default_rng(int(t * 30)); cx += r.uniform(-7, 7); cy += r.uniform(-5, 5); z = max(z, 1.012)
    if abs(z - 1) > 1e-4:
        cw, ch = W / z, H / z; x0 = min(max(cx - cw / 2, 0), W - cw); y0 = min(max(cy - ch / 2, 0), H - ch)
        im = im.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
    return im
TERM_BG = Image.new('RGB', (W, H), BG); SCANL = Image.new('RGBA', (W, H), (0, 0, 0, 0)); _d = ImageDraw.Draw(SCANL)
for y in range(0, H, 4): _d.line((0, y, W, y), fill=(0, 0, 0, 60))
tcols = [dict(x=x, y=rng.uniform(0, H), v=rng.uniform(60, 160)) for x in range(30, W, 46)]
def mix_bg(col, a): return tuple(int(BG[i] + (col[i] - BG[i]) * a / 255) for i in range(3))
EGG = None
def term_base(t, alpha=36):
    im = TERM_BG.copy(); d = ImageDraw.Draw(im, 'RGBA'); fs = F(MONO, 24)
    for c in tcols:
        y = (c['y'] + t * c['v']) % (H + 200) - 100
        for k in range(9): d.text((c['x'], y - k * 30), GLY[int(t * 6 + k * 3 + c['x']) % len(GLY)], font=fs, fill=mix_bg(PH, alpha * (1 - k / 9)))
    if EGG and EGG[0] <= t < EGG[1]:      # easter egg: «13» (o custo da Emrakul) na chuva de código
        for k, ch in enumerate('13'): d.text((tcols[19]['x'], 1100 + k * 30), ch, font=fs, fill=mix_bg(PH, 95))
    return im, d
def term_finish(im):
    im = Image.composite(im, Image.new('RGB', (W, H), (0, 0, 0)), VIG); im.paste(SCANL, (0, 0), SCANL); return im
def hud(d, t):
    a = led_amp(t); d.ellipse((80, 1676, 100, 1696), fill=(16, 185, 129, int(70 + 185 * a)))
    d.text((114, 1686), 'BINDER', font=F(MONOB, 28), fill=(16, 185, 129, 220), anchor='lm')
    d.text((W - 80, 1686), 'ORIGINALS · HALLOWEEN', font=F(MONO, 26), fill=(150, 170, 175, 220), anchor='rm')
def typed(s, t0, t, cps=40): return s[:int(max(0, t - t0) * cps)]
def tubo_caption(im, t, f, bottom=1600):
    if not f: return
    clean = f['legenda'].replace('*', ''); cps = max(14, len(clean) / max(0.6, f['dur'] * 0.85))
    caption(im, f['legenda'], ST_T, bottom=bottom, maxw=900, nchars=int(max(0, t - f['start']) * cps)); previa_tag(im, f, bottom)

# ---------------- cenas ----------------
def frame_innistrad(im, art, box, t0, t, label, sub):
    x, y, w, h = box; a = ART[art].resize((int(w), int(h)), Image.LANCZOS)
    d = ImageDraw.Draw(im, 'RGBA')
    d.rectangle((x - 26, y - 26, x + w + 26, y + h + 26), outline=IVORY + (230,), width=3)
    d.rectangle((x - 16, y - 16, x + w + 16, y + h + 16), outline=IVORY + (160,), width=1)
    for cx, cy in ((x - 26, y - 26), (x + w + 26, y - 26), (x - 26, y + h + 26), (x + w + 26, y + h + 26)):
        d.polygon([(cx, cy - 12), (cx + 12, cy), (cx, cy + 12), (cx - 12, cy)], fill=IVORY + (240,))
    im.paste(a, (int(x), int(y)))
    d.text((W / 2, y + h + 50), label, font=F(LORA, 44, 'Bold'), fill=IVORY, anchor='ma')
    d.text((W / 2, y + h + 104), sub, font=F(LORAI, 26, 'Italic'), fill=(190, 196, 205), anchor='ma')
def frame_polaroid(im, art, box, t, label, ang=-2.2):
    x, y, w, h = box; a = ART[art].resize((int(w), int(h)), Image.LANCZOS)
    pol = Image.new('RGBA', (int(w) + 52, int(h) + 150), (236, 230, 216, 255)); pol.paste(a, (26, 26))
    pd = ImageDraw.Draw(pol); pd.text((pol.width / 2, h + 50), label, font=F(COMIC, 46), fill=(40, 30, 30), anchor='ma')
    pol = pol.rotate(ang, resample=Image.BICUBIC, expand=True)
    im.paste(pol, (int(W / 2 - pol.width / 2), int(y - 26)), pol)
    d = ImageDraw.Draw(im, 'RGBA')
    for tx, ty, rot in ((W / 2 - 300, y - 40, 12), (W / 2 + 230, y - 34, -10)):
        tp = Image.new('RGBA', (150, 46), (230, 220, 180, 170)).rotate(rot, expand=True); im.paste(tp, (int(tx), int(ty)), tp)
def vhs_hud(im, t, t0):
    d = ImageDraw.Draw(im, 'RGBA')
    if int(t * 2) % 2 == 0: d.ellipse((70, 262, 96, 288), fill=(255, 40, 40, 255))
    d.text((108, 258), 'REC', font=F(MONOB, 34), fill=(255, 255, 255))
    s = 59 + int(t - t0); hh = 23 + s // 60; mm = (59 + s // 60) % 60
    d.text((W - 70, 258), f'31.10 · {hh % 24:02d}:{mm:02d}:{s % 60:02d}', font=F(MONOB, 32), fill=(255, 255, 255), anchor='ra')
    d.text((70, 1560), 'PLAY ▶', font=F(MONOB, 32), fill=(255, 255, 255, 220))

def cena_abre_i(t, c):
    p = (t - c['a']) / (c['b'] - c['a']); im = bg_innistrad('moorland'); d = ImageDraw.Draw(im, 'RGBA')
    g = Image.new('RGBA', (700, 700), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((150, 150, 550, 550), fill=(220, 232, 245, 70)); g = g.filter(ImageFilter.GaussianBlur(80))
    im.paste(g, (W - 640, 120), g)
    fog(im, t, 1340, 1700, 3, 80); fog(im, t, 200, 520, 5, 50)
    s = 1 + 0.03 * p; w = 980 * s; h = w * 457 / 626; x = (W - w) / 2; y = 450 - (h - 980 * 457 / 626) / 2
    frame_innistrad(im, 'moorland', (x, y, w, h), c['a'], t, 'INNISTRAD', 'o horror gótico'); y_lab = 450 + 980 * 457 / 626
    im = vignette(im)
    d = ImageDraw.Draw(im, 'RGBA'); d.text((W / 2, 1318), cred('moorland'), font=F(INTM, 19), fill=(200, 205, 212), anchor='ma')
    f = fala_em(t, 'abre_i')
    if f: caption(im, f['legenda'], ST_KD, bottom=1530); previa_tag(im, f, 1530)
    if t - c['a'] < 0.5: im = Image.blend(Image.new('RGB', (W, H), (0, 0, 0)), im, ease((t - c['a']) / 0.5))
    return im
def cena_abre_d(t, c):
    p = (t - c['a']) / (c['b'] - c['a']); im = bg_dusk('island'); vhs_lines(im, t)
    w = 940 * (1 + 0.025 * p); h = w * 457 / 626
    frame_polaroid(im, 'island', ((W - w) / 2, 440, w, h), t, 'DUSKMOURN')
    vhs_hud(im, t, c['a']); im = vignette(im, 0.8)
    d = ImageDraw.Draw(im, 'RGBA'); d.text((W / 2, 1330), cred('island'), font=F(INTM, 19), fill=(230, 210, 205), anchor='ma')
    f = fala_em(t, 'abre_d')
    if f: caption(im, f['legenda'], ST_KD, bottom=1530); previa_tag(im, f, 1530)
    if t - c['a'] < 0.3: im = glitch(im, t, 1.2 * (1 - (t - c['a']) / 0.3))
    return im
def cena_titulo(t, c):
    p = t - c['a']; im = bg_innistrad('emrakul'); dr = bg_dusk('valgavoth')
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([(W * 0.62, 0), (W, 0), (W, H), (W * 0.38, H)], fill=255)
    im = Image.composite(dr, im, m); im = vignette(im)
    d = ImageDraw.Draw(im, 'RGBA')
    d.text((W / 2, 560), 'BINDER ORIGINALS', font=F(INTSB, 34), fill=EM, anchor='ma')
    d.text((W / 2, 606), 'ESPECIAL DE HALLOWEEN', font=F(INTM, 28), fill=(205, 210, 215), anchor='ma')
    q1 = eio(p / 0.25); q2 = eio((p - 0.18) / 0.25); q3 = eio((p - 0.4) / 0.3)
    fI = F(LORA, int(126 * (2 - q1)), 'Bold'); d.text((W / 2, 690), 'INNISTRAD', font=fI, fill=IVORY + (int(255 * q1),), anchor='ma')
    d.text((W / 2, 850), '×', font=F(BANG, 110), fill=YEL + (int(255 * q2),), anchor='ma')
    fD = F(MONOB, int(108 * (2 - q2))); d.text((W / 2 + 5, 990), 'DUSKMOURN', font=fD, fill=(255, 40, 40, int(170 * q2)), anchor='ma')
    d.text((W / 2, 990), 'DUSKMOURN', font=fD, fill=(255, 235, 230, int(255 * q2)), anchor='ma')
    d.text((W / 2, 1180), 'O JULGAMENTO', font=F(BANG, 104), fill=YEL + (int(255 * q3),), anchor='ma', stroke_width=5, stroke_fill=(17, 17, 17))
    d.text((W / 2, 1290), 'DO HORROR', font=F(BANG, 104), fill=YEL + (int(255 * q3),), anchor='ma', stroke_width=5, stroke_fill=(17, 17, 17))
    d.text((W / 2, 1440), 'com Mana & Burn · Conde de Manaforte · TUBO', font=F(INTM, 28), fill=(225, 225, 225, int(255 * q3)), anchor='ma')
    if p < 0.12: im = Image.blend(im, Image.new('RGB', (W, H), (255, 255, 255)), 0.8 * (1 - p / 0.12))
    return im
def cena_sofa(t, c):
    n = int(round(t * FPS)); fr = mb_frame(n)
    im = fr.copy() if fr else Image.new('RGB', (W, H), (40, 30, 30))
    if c['nome'] == 'sofa1':
        b1 = next(f for f in FALAS if f['id'] == 'B1'); m1 = next(f for f in FALAS if f['id'] == 'M1')
        nametag(im, t, b1['start'] + 0.2, 560, 560, 'BURN', 'quer banir tudo', BURNC, dur=2.3)
        nametag(im, t, m1['start'] + 0.15, 520, 430, 'MANA', 'sabe todas as regras · "Lê a carta"', MANAC, dur=2.6)
    if c['nome'] == 'sofa2':
        b9 = next(f for f in FALAS if f['id'] == 'B9'); q = ease((t - b9['start']) / 0.3)
        if q > 0 and t < TL['T_SLAM']:
            d = ImageDraw.Draw(im, 'RGBA'); y = 330 - (1 - q) * 30
            d.rectangle((60, y, W - 60, y + 196), fill=(10, 10, 12, int(232 * q))); d.rectangle((60, y, W - 60, y + 8), fill=YEL + (int(255 * q),))
            d.text((W / 2, y + 30), 'INNISTRAD OU DUSKMOURN?', font=F(BANG, 66), fill=YEL + (int(255 * q),), anchor='ma')
            d.text((W / 2, y + 112), 'Qual destes mundos sobreviverias a visitar?', font=F(GEIST, 36), fill=(255, 255, 255, int(255 * q)), anchor='ma')
    if c['nome'] == 'zero':
        r = np.random.default_rng(n); dx, dy = r.uniform(-10, 10), r.uniform(-8, 8)
        im = ImageChops.offset(im, int(dx), int(dy))
    if t - c['a'] < 0.1: im = Image.blend(im, Image.fromarray(np.random.default_rng(n).integers(0, 255, (H, W, 3), dtype=np.uint8)), 0.7)
    return im

CAT = {
 'cat1': dict(n='1/5', titulo='CRIATURAS MAIS ATERRADORAS', A='emrakul', B='valgavoth', artA='emrakul', artB='valgavoth'),
 'cat2': dict(n='2/5', titulo='GÓTICO × PSICOLÓGICO', A='huntmaster', B='mindskinner', artA='huntmaster', artB='mindskinner'),
 'cat3': dict(n='3/5', titulo='ATMOSFERA E AMBIENTAÇÃO', A='moorland', B='annex', artA='moorland', artB='annex'),
}
# layout por fala: ('dual', foco) ou ('solo', lado, destaques [x,y,w,h] no PNG da carta)
LAY = {
 'B3': ('dual', 'A'), 'M2': ('solo', 'A', [(38, 753, 600, 29), (38, 781, 606, 31)]), 'B4': ('dual', 'B'), 'M3': ('dual', 'B'),
 'M4': ('solo', 'A', [(45, 832, 575, 32), (45, 864, 540, 32)]), 'B5': ('dual', 'B'),
 'M5': ('solo', 'B', [(40, 713, 560, 31), (40, 746, 570, 34), (40, 777, 470, 34)]),
 'M6': ('dual', 'B'), 'B7': ('solo', 'B', [(540, 522, 440, 184)]),
}
def rects_for(lay, side, key):
    if lay == 'dual': return [(40, 440, 480), (560, 440, 480)]
    return None
def cena_cat(t, c):
    k = CAT[c['nome']]; im = bg_innistrad(k['artA']); dr = bg_dusk(k['artB']); m = Image.new('L', (W, H), 0)
    ImageDraw.Draw(m).rectangle((W // 2, 0, W, H), fill=255); im = Image.composite(dr, im, m); vhs_lines(im, t, W // 2, W, 3)
    d = ImageDraw.Draw(im, 'RGBA'); d.line((W // 2, 0, W // 2, H), fill=(0, 0, 0, 160), width=4)
    im = vignette(im, 0.8); d = ImageDraw.Draw(im, 'RGBA')
    bug(im); draw_placar(im, t, y=230)
    d.text((60, 300), f"{k['n']} · {k['titulo']}", font=F(BANG, 52), fill=YEL, stroke_width=4, stroke_fill=(17, 17, 17))
    d.text((60, 368), 'INNISTRAD: ' + cred(k['A']), font=F(INTM, 18), fill=(225, 228, 235))
    d.text((60, 392), 'DUSKMOURN: ' + cred(k['B']), font=F(INTM, 18), fill=(240, 220, 215))
    f = fala_em(t, c['nome']); key = f['id'] if f else None
    lay = LAY.get(key, ('dual', None))
    # transição entre layouts: 0,22 s a partir do início da fala
    prev = None
    if f:
        idx = [x['id'] for x in FALAS if x['cena'] == c['nome']].index(key)
        if idx > 0: prev = LAY.get([x['id'] for x in FALAS if x['cena'] == c['nome']][idx - 1])
    q = ease((t - f['start'] + 0.05) / 0.22) if f else 1
    def boxes(L_):
        if L_ is None or L_[0] == 'dual':
            fo = L_[1] if L_ else None
            return {'A': (40, 452 - (14 if fo == 'A' else 0), 480), 'B': (560, 452 - (14 if fo == 'B' else 0), 480)}
        side = L_[1]; other = 'B' if side == 'A' else 'A'
        if k[side] == 'annex' and side == 'B': bx = {side: (130, 540, 820)}
        else: bx = {side: (240, 440, 600)}
        bx[other] = (W / 2 - 60, 1150, 0.0)          # some
        return bx
    b0 = boxes(prev) if prev else boxes(('dual', None)); b1 = boxes(lay)
    if not f or (t - f['start']) > 0.3: b0 = b1
    for side in ('A', 'B'):
        x = lerp(b0[side][0], b1[side][0], q); y = lerp(b0[side][1], b1[side][1], q); w = lerp(b0[side][2], b1[side][2], q)
        if w < 30: continue
        key_img = k[side] + ('_rot' if (k[side] == 'annex' and lay[0] == 'solo') else '')
        card = CARD[key_img]
        glow = None
        if f and lay[1] == side: glow = ((255, 216, 74, 120) if side == 'A' else (255, 70, 60, 130))
        box = paste_card(im, card, x, y, w, glow)
        if lay[0] == 'solo' and lay[1] == side and q >= 1:
            hl_rects(im, box, lay[2], (t - f['start'] - 0.35) / 0.8, card.width, card.height)
    if lay[0] == 'dual':
        dd = ImageDraw.Draw(im, 'RGBA')
        dd.text((280, 1150), 'INNISTRAD', font=F(LORA, 40, 'Bold'), fill=IVORY, anchor='ma')
        dd.text((800, 1150), 'DUSKMOURN', font=F(MONOB, 38), fill=(255, 150, 140), anchor='ma')
    rodape_wotc(im, 1505)
    if f: caption(im, f['legenda'], ST_MB, bottom=1480); pip(im, t, f)
    if t - c['a'] < 0.12: im = Image.blend(im, Image.new('RGB', (W, H), (0, 0, 0)), 1 - (t - c['a']) / 0.12)
    return im

def tubo_overlay_power(im, t, t0):
    p = t - t0
    if p < 0.16:
        d = ImageDraw.Draw(im, 'RGBA'); hh = 4 + 900 * (p / 0.16) ** 2
        d.rectangle((0, 0, W, H), fill=(0, 0, 0, int(255 * (1 - p / 0.16))))
        d.rectangle((0, H / 2 - hh / 2, W, H / 2 + hh / 2), fill=(220, 255, 235, int(200 * (1 - p / 0.16))))
    return im
VEREDITO = {'veredito1': ('PONTO → INNISTRAD', IVORY, 'Ameaça direta ao seu turno'),
            'veredito2': ('PONTO → DUSKMOURN', (255, 120, 110), 'Medo do que não se vê (Wizards)'),
            'veredito3': ('PONTO → DUSKMOURN', (255, 120, 110), 'O plano inteiro é uma casa'),
            'veredito4': ('PONTO → INNISTRAD', IVORY, 'Parecer do Conde')}
def cena_tubo(t, c):
    nome = c['nome']; f = fala_em(t, nome)
    expr = {'tubo': 'analitico', 'erro': 'erro', 'fecho_tubo': 'analitico'}.get(nome, 'confiante')
    im = tubo_frame(t, expr, zoom=1.0, red_led=(nome == 'erro')); d = ImageDraw.Draw(im, 'RGBA')
    if nome == 'tubo':
        nametag(im, t, c['a'] + 0.3, 60, 300, 'TUBO', 'juiz computacional · Terminal Unificado de Balanço e Otimização', EM, dur=2.4)
        if t > c['a'] + 1.4: draw_placar(im, t, y=1440, big=True)
    elif nome.startswith('veredito'):
        draw_placar(im, t, y=250, big=True)
        lbl, col, why = VEREDITO[nome]; q = eio((t - c['a'] - 0.3) / 0.18)
        if q > 0:
            s = 1 + 0.6 * (1 - q); fnt = F(MONOB, int(56 * s)); w = d.textlength(lbl, font=fnt) + 50
            st = Image.new('RGBA', (int(w), int(110 * s)), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
            sd.rectangle((0, 0, st.width - 1, st.height - 1), outline=col + (255,), width=6, fill=(5, 10, 16, 200))
            sd.text((st.width / 2, st.height / 2), lbl, font=fnt, fill=col, anchor='mm'); st = st.rotate(-4, expand=True, resample=Image.BICUBIC)
            im.paste(st, (int(W / 2 - st.width / 2), 390), st)
            d = ImageDraw.Draw(im, 'RGBA'); d.text((W / 2, 1450), why, font=F(MONO, 30), fill=(150, 170, 175), anchor='ma')
    elif nome == 'erro':
        draw_placar(im, t, y=250, big=True)
        q = ease((t - c['a'] - 0.2) / 0.25)
        if q > 0:
            d.rectangle((70, 380, W - 70, 520), fill=(30, 4, 6, int(235 * q)), outline=(255, 64, 64, int(255 * q)), width=4)
            d.text((96, 396), 'MODELO TUBO · ERRO', font=F(MONOB, 32), fill=(255, 90, 90, int(255 * q)))
            d.text((96, 440), 'EDHREC (29/10/2026): DUSKMOURN 3 × 2', font=F(MONO, 28), fill=(235, 220, 220, int(255 * q)))
            d.text((96, 478), 'TRIBUNAL BINDER:    INNISTRAD 3 × 2', font=F(MONO, 28), fill=(235, 220, 220, int(255 * q)))
        q2 = ease((t - c['a'] - 1.2) / 0.3)
        if q2 > 0:
            y = 1430; d.text((80, y), 'GRAU DE CERTEZA', font=F(MONOB, 26), fill=(150, 170, 175, int(255 * q2)))
            for i in range(5): d.rectangle((420 + i * 64, y - 2, 470 + i * 64, y + 28), fill=(EM + (int(255 * q2),)) if i < 2 else (40, 50, 58, int(255 * q2)))
            d.text((80, y + 44), 'Innistrad: cartas desde 2011 · Duskmourn: desde 2024', font=F(MONO, 24), fill=(150, 170, 175, int(255 * q2)))
    elif nome == 'fecho_tubo':
        q = ease((t - c['a']) / 0.3)
        d.rectangle((60, 250, W - 60, 470), fill=(5, 10, 16, int(220 * q)), outline=EM + (int(255 * q),), width=3)
        d.text((W / 2, 272), 'BINDER ORIGINALS', font=F(INTB, 54), fill=WHITE + (int(255 * q),), anchor='ma')
        d.text((W / 2, 350), 'Mana & Burn · Conde de Manaforte · TUBO', font=F(INTSB, 34), fill=EM + (int(255 * q),), anchor='ma')
        d.text((W / 2, 405), 'três séries, um universo · @binderthetrade', font=F(INTM, 26), fill=(180, 190, 200, int(255 * q)), anchor='ma')
    if f and f['quem'] == 'T': tubo_caption(im, t, f, bottom=1640 if nome in ('erro',) else 1620)
    im = tubo_overlay_power(im, t, c['a']) if nome in ('tubo', 'veredito1', 'veredito2', 'veredito3', 'veredito4') and t - c['a'] < 0.16 else im
    if nome == 'erro' and t - c['a'] < 0.2: im = glitch(im, t, 1.0)
    return im

ARTBOX = (40, 420, 1000, 730)
ANOT = {'K1': [('ell', 0.565, 0.31, 0.11, 0.15), ('arrow', 0.30, 0.80, 0.13, 0.56)],
        'K2': [('ell', 0.33, 0.17, 0.20, 0.19), ('line', 0.14, 0.66, 0.73, 0.50)],
        'K3': [('ell', 0.33, 0.17, 0.20, 0.19)]}
CONDE_EXPR = {'K1': 'desconfiado', 'K2': 'admirado', 'K3': 'neutro'}
def ink(d, kind, args, q, box):
    x, y, w, h = box
    if kind == 'ell':
        cx, cy, rx, ry = x + args[0] * w, y + args[1] * h, args[2] * w, args[3] * h; n = int(80 * q)
        pts = [(cx + rx * math.cos(-math.pi / 2 + 2 * math.pi * 1.08 * i / 80), cy + ry * math.sin(-math.pi / 2 + 2 * math.pi * 1.08 * i / 80)) for i in range(n)]
        if len(pts) > 1: d.line(pts, fill=INK, width=11, joint='curve'); d.line(pts, fill=IVORY, width=4, joint='curve')
    else:
        x0, y0, x1, y1 = x + args[0] * w, y + args[1] * h, x + args[2] * w, y + args[3] * h
        xe, ye = lerp(x0, x1, q), lerp(y0, y1, q)
        d.line((x0, y0, xe, ye), fill=INK, width=11); d.line((x0, y0, xe, ye), fill=IVORY, width=4)
        if kind == 'arrow' and q >= 1:
            a = math.atan2(y1 - y0, x1 - x0)
            for s in (1, -1):
                hx, hy = x1 - 34 * math.cos(a + s * 0.5), y1 - 34 * math.sin(a + s * 0.5)
                d.line((x1, y1, hx, hy), fill=INK, width=11); d.line((x1, y1, hx, hy), fill=IVORY, width=4)
OVAL = Image.new('L', (190, 230), 0); ImageDraw.Draw(OVAL).ellipse((0, 0, 189, 229), fill=255)
def cena_conde(t, c):
    im = Image.new('RGB', (W, H), IVORY); d = ImageDraw.Draw(im, 'RGBA')
    d.line((60, 240, 800, 240), fill=INK, width=3); d.line((60, 248, 800, 248), fill=INK, width=1)
    d.text((60, 258), 'O TRIBUNAL ESTÉTICO', font=F(LORA, 54, 'Bold'), fill=INK)
    d.line((60, 330, 800, 330), fill=INK, width=1); d.line((60, 338, 800, 338), fill=INK, width=3)
    d.text((60, 350), '4/5 · design artístico · parecer especial', font=F(LORAI, 28, 'Italic'), fill=BORDO)
    f = fala_em(t, 'cat4'); key = f['id'] if f else 'K1'
    art = 'arabella' if key == 'K1' else 'bloodline'
    x, y, w, h = ARTBOX; a = ART[art].resize((w, h), Image.LANCZOS); im.paste(a, (x, y))
    d = ImageDraw.Draw(im, 'RGBA'); d.rectangle((x - 2, y - 2, x + w + 2, y + h + 2), outline=INK, width=3)
    side = 'DUSKMOURN' if art == 'arabella' else 'INNISTRAD'
    d.text((800, 352), side, font=F(LORA, 28, 'Bold'), fill=BORDO, anchor='ra')
    d.text((x, y + h + 18), cred(art), font=F(LORAI, 21, 'Italic'), fill=GRAVURA)
    d.text((x, y + h + 46), '© Wizards of the Coast · Conteúdo de fã não oficial', font=F(LORAI, 21, 'Italic'), fill=GRAVURA)
    if f:
        q = (t - f['start'] - 0.4) / 1.1
        for kind, *args in ANOT.get(key, []):
            ink(d, kind, args, max(0, min(1, q)), ARTBOX); q -= 0.9
        if key == 'K3':
            qs = eio((t - f['start'] - 0.2) / 0.2)
            if qs > 0:
                s = 1 + 0.5 * (1 - qs); fnt = F(LORA, int(58 * s), 'Bold'); lbl = 'PARECER · INNISTRAD'
                st = Image.new('RGBA', (int(d.textlength(lbl, font=fnt) + 60), int(110 * s)), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
                sd.rectangle((0, 0, st.width - 1, st.height - 1), outline=BORDO, width=7); sd.rectangle((10, 10, st.width - 11, st.height - 11), outline=BORDO, width=2)
                sd.text((st.width / 2, st.height / 2), lbl, font=fnt, fill=BORDO, anchor='mm'); st = st.rotate(7, expand=True, resample=Image.BICUBIC)
                im.paste(st, (int(W / 2 - st.width / 2 + 120), int(y + h - st.height - 30)), st)
    ex = CONDE[CONDE_EXPR.get(key, 'neutro')].resize((190, int(190 * 394 / 352)), Image.LANCZOS).crop((0, 0, 190, 230))
    d = ImageDraw.Draw(im, 'RGBA'); ox, oy = 850, 150
    d.ellipse((ox - 10, oy - 10, ox + 200, oy + 240), outline=INK, width=3); d.ellipse((ox - 4, oy - 4, ox + 194, oy + 234), outline=INK, width=1)
    im.paste(ex, (ox, oy), OVAL)
    k1 = next(x for x in FALAS if x['id'] == 'K1')
    nametag(im, t, k1['start'] - 0.2, 60, 1238, 'CONDE DE MANAFORTE', 'crítico de arte · O Tribunal Estético · a voz da abertura', BORDO, dur=2.8, font=F(LORA, 40, 'Bold'))
    if f: caption(im, f['legenda'], ST_KI, bottom=1490); previa_tag(im, f, 1490)
    if t - c['a'] < 0.25:      # entrada em tinta (de preto para marfim)
        im = Image.blend(Image.new('RGB', (W, H), (0, 0, 0)), im, ease((t - c['a']) / 0.25))
    return im

SALT = [('#26', 'Toxrill, the Corrosive', 2.33, 'VOW·2021', 'toxrill'), ('#63', 'Hullbreaker Horror', 2.00, 'VOW·2021', 'hullbreaker'),
        ('#69', 'Emrakul, the Promised End', 1.98, 'EMN·2016', 'emrakul')]
def cena_terminal(t, c):
    p = t - c['a']
    if p < 0.6:   # mergulho no tubo
        im = tubo_frame(t, 'analitico', zoom=1 + 4.5 * ease(p / 0.6) ** 2, cx=SCX, cy=SCY)
        if p > 0.45: im = Image.blend(im, Image.new('RGB', (W, H), BG), (p - 0.45) / 0.15)
        return im
    im, d = term_base(t)
    d.text((80, 200), typed('> ARQUIVO: SALT SCORE · EDHREC', c['a'] + 0.6, t), font=F(MONOB, 34), fill=PH)
    d.text((80, 250), typed('  Top 100 Saltiest Cards of 2026', c['a'] + 1.0, t), font=F(MONO, 28), fill=EM)
    y = 330; d.text((80, y), typed('INNISTRAD', c['a'] + 1.2, t), font=F(MONOB, 32), fill=IVORY)
    for i, (rk, nm, sc, st, _) in enumerate(SALT):
        tq = ease((t - c['a'] - 1.4 - i * 0.35) / 0.35); yy = y + 52 + i * 52
        if tq <= 0: continue
        d.text((80, yy), f'{rk}  {nm}', font=F(MONO, 27), fill=mix_bg(WHITE, int(255 * tq)))
        bw = int(200 * sc / 4 * tq); d.rectangle((700, yy + 4, 700 + bw, yy + 28), fill=EM)
        d.text((710 + 200, yy), f'{sc:.2f}'.replace('.', ','), font=F(MONOB, 27), fill=mix_bg(PH, int(255 * tq)))
    yy = y + 52 * 4 + 20
    if t > c['a'] + 2.6:
        d.text((80, yy), 'DUSKMOURN', font=F(MONOB, 32), fill=(255, 120, 110))
        d.text((80, yy + 52), typed('—  0 cartas no top 100', c['a'] + 2.8, t), font=F(MONO, 27), fill=(255, 150, 140))
    if t > c['a'] + 3.2:
        d.text((80, yy + 120), 'CONTAGEM: INNISTRAD 3 · DUSKMOURN 0', font=F(MONOB, 30), fill=PH)
    for i, (_, _, _, _, k) in enumerate(SALT):   # cartas: entrada «scan» linha a linha, inteiras no fim
        t0 = c['a'] + 1.5 + i * 0.35; q = ease((t - t0) / 0.6)
        if q <= 0: continue
        cw = 300; card = CARD[k].resize((cw, int(CARD[k].height * cw / CARD[k].width)), Image.LANCZOS)
        hh = int(card.height * q); x = 45 + i * 335; yc = 820
        im.paste(card.crop((0, 0, cw, hh)), (x, yc), card.crop((0, 0, cw, hh)))
        if q < 1: ImageDraw.Draw(im).line((x - 6, yc + hh, x + cw + 6, yc + hh), fill=PH, width=3)
    d = ImageDraw.Draw(im, 'RGBA')
    d.text((80, 1262), 'fonte: EDHREC, Top 100 Saltiest Cards of 2026 (voto) · 0 a 4', font=F(MONO, 24), fill=(150, 170, 175))
    d.text((80, 1296), 'set da 1.ª impressão: Scryfall · consulta 30/10/2026', font=F(MONO, 24), fill=(150, 170, 175))
    d.text((80, 1330), 'Cartas © Wizards of the Coast · imagens via Scryfall', font=F(MONO, 24), fill=(150, 170, 175))
    hud(d, t)
    im = term_finish(im); f = fala_em(t, 'cat5')
    if f: tubo_caption(im, t, f, bottom=1600)
    return im

def cena(t):
    for c in CENAS:
        if c['a'] <= t < c['b']: return c
    return CENAS[-1]
def render(t):
    c = cena(t); n = c['nome']
    if n == 'abre_i': im = cena_abre_i(t, c)
    elif n == 'abre_d': im = cena_abre_d(t, c)
    elif n == 'titulo': im = cena_titulo(t, c)
    elif n in ('sofa1', 'zero', 'sofa2'): im = cena_sofa(t, c)
    elif n in CAT: im = cena_cat(t, c)
    elif n == 'cat4': im = cena_conde(t, c)
    elif n == 'cat5': im = cena_terminal(t, c)
    else: im = cena_tubo(t, c)
    marca_previa(im); return im

if __name__ == '__main__':
    c5 = CEN['cat5']; EGG = (c5['a'] + 1.0, c5['a'] + 2.0)
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        pathlib.Path('stills').mkdir(exist_ok=True)
        for s in sys.argv[2:]:
            render(float(s)).save(f'stills/still_{float(s):06.2f}.jpg', quality=88); print('still', s)
        sys.exit()
    n = int(round(TL['FIM_KIT'] * FPS)); out = 'kit.mp4'
    pr = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(n):
        pr.stdin.write(render(i / FPS).convert('RGB').tobytes())
        if i % 300 == 0: print('quadro', i, '/', n, flush=True)
    pr.stdin.close(); pr.wait(); print('ok', out, n, 'quadros')
