# Meta em Curto ESP02 · A Taça respondeu · render (derivado de esp01_render.py)
# Continuação do ESP01 com os dados da Taça Preconauta (collab @preconautamtg; autorização em oraculo/autorizacoes/2026-11-13_preconauta_dados_2x2.md).
# Uso, numa pasta de trabalho com tl.json, words.json, led_env.npy e mix_final.wav (saídas de esp02_audio.py):
#   python3 esp02_render.py /caminho/do/kit             -> ESP02_META_EM_CURTO.mp4
#   python3 esp02_render.py /caminho/do/kit stills 3 10 -> still_03.00.png ...
#   python3 esp02_render.py /caminho/do/kit capa        -> ESP02_CAPA.png
import os, json, math, subprocess, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
K = (sys.argv[1] if len(sys.argv) > 1 else '../..').rstrip('/') + '/'
W, H, FPS = 1080, 1920, 30
TL = json.load(open('tl.json')); WORDS = json.load(open('words.json'))
TEMPO, LEAD = TL['TEMPO'], TL['LEAD']
TOTAL, OUT = TL['TOTAL'], TL['OUT_START']
PAUSES = TL['PAUSES']
def vt(x): return x / TEMPO + LEAD + sum(d for a, d in PAUSES if x >= a)
for w in WORDS: w['vs'] = vt(w['s']); w['ve'] = vt(w['e'])
def ws(i): return WORDS[i]['vs']
ENV = np.load('led_env.npy')
MASTER = Image.open(K + 'oraculo/assets/tubo_mestra_916.png').convert('RGB')
_fc = {}
def F(p, s):
    if (p, s) not in _fc: _fc[(p, s)] = ImageFont.truetype(p, s)
    return _fc[(p, s)]
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'; MONOB = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
COND = '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf'; CONDB = '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf'
INTB = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'; INTSB = '/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf'; INTM = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
BG = (5, 10, 16); EM = (16, 185, 129); PH = (0, 255, 65); WHITE = (236, 241, 245); GREY = (120, 140, 150); RED = (255, 64, 64)
DIMG = (70, 120, 95)
SCR = (492, 566, 740, 792); SCX, SCY = (SCR[0] + SCR[2]) / 2, (SCR[1] + SCR[3]) / 2
EYES = [(518, 615, 596, 702), (634, 615, 709, 702)]; LED = (592, 828)
rng = np.random.default_rng(13)
GLY = '0123456789ABCDEF#*+=<>/:'
def ease(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)
def eio(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3
def typed(s, t0, t, cps=40): return s[:int(max(0, t - t0) * cps)]
def fit(d, s, path, size, maxw):
    while size > 20:
        f = F(path, size)
        if d.textlength(s, font=f) <= maxw: return f
        size -= 2
    return F(path, size)
def led_amp(t):
    fi = int(round(t * FPS)); return min(1, float(ENV[fi]) if fi < len(ENV) else 0)

# ---------- FORA: TUBO ----------
rain_cols = [dict(x=x, y=rng.uniform(0, 300), v=rng.uniform(40, 90)) for x in range(500, 736, 14)]
def tubo_frame(t, expr='analitico', zoom=1.0, cx=None, cy=None, red_led=False):
    im = MASTER.copy(); d = ImageDraw.Draw(im, 'RGBA'); fs = F(MONO, 13)
    for c in rain_cols:
        y = SCR[1] + ((c['y'] + t * c['v']) % (SCR[3] - SCR[1] + 40)) - 20
        for k in range(5):
            yy = y - k * 15
            if SCR[1] + 8 < yy < SCR[3] - 14 and not any(e[0] - 6 < c['x'] < e[2] + 6 and e[1] - 8 < yy < e[3] + 4 for e in EYES):
                a = int(150 * (1 - k / 5) * (0.6 if expr != 'desconfiado' else 0.2))
                d.text((c['x'], yy), GLY[int(t * 8 + k + c['x']) % len(GLY)], font=fs, fill=(0, 255, 65, a))
    sy = SCR[1] + ((t * 120) % (SCR[3] - SCR[1]))
    d.rectangle((SCR[0] + 14, sy, SCR[2] - 14, sy + 5), fill=(16, 185, 129, 22))
    lid = 0.0; bt = t % 4.3
    if bt < 0.14 and expr != 'erro': lid = math.sin(bt / 0.14 * math.pi)
    if expr == 'desconfiado': lid = max(lid, 0.45)
    if expr == 'confiante': lid = max(lid, 0.22)
    if lid > 0.01:
        for i, e in enumerate(EYES):
            h = (e[3] - e[1] + 4) * lid
            if expr == 'confiante' and lid < 0.5 and i == 1: h *= 0.4
            if expr == 'desconfiado' and i == 0: h *= 0.55          # um olho semicerrado
            d.rectangle((e[0] - 3, e[1] - 3, e[2] + 3, e[1] - 3 + h), fill=BG + (255,))
            d.line((e[0] - 3, e[1] - 3 + h, e[2] + 3, e[1] - 3 + h), fill=(16, 185, 129, 160), width=3)
    if expr == 'erro': im = glitch_eyes(im, t)
    d = ImageDraw.Draw(im, 'RGBA')
    a = led_amp(t)
    d.ellipse((LED[0] - 7, LED[1] - 7, LED[0] + 7, LED[1] + 7), fill=(8, 40, 26, 255))
    if red_led:
        on = int(t * 6) % 2 == 0           # 3 piscadelas secas por segundo
        if on:
            glow = Image.new('RGBA', (120, 120), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
            gd.ellipse((40, 40, 80, 80), fill=(255, 40, 40, 220)); glow = glow.filter(ImageFilter.GaussianBlur(14))
            im.paste(glow, (LED[0] - 60, LED[1] - 60), glow)
            d.ellipse((LED[0] - 6, LED[1] - 6, LED[0] + 6, LED[1] + 6), fill=(255, 120, 120, 255))
        else:
            d.ellipse((LED[0] - 6, LED[1] - 6, LED[0] + 6, LED[1] + 6), fill=(70, 10, 10, 255))
    elif a > 0.03:
        glow = Image.new('RGBA', (120, 120), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
        gd.ellipse((40, 40, 80, 80), fill=(16, 185, 129, int(200 * a))); glow = glow.filter(ImageFilter.GaussianBlur(14))
        im.paste(glow, (LED[0] - 60, LED[1] - 60), glow)
        d.ellipse((LED[0] - 6, LED[1] - 6, LED[0] + 6, LED[1] + 6), fill=(120, 255, 190, int(80 + 175 * a)))
    z = max(1.0, zoom) * (1 + 0.008 * (1 + math.sin(t * 1.3)) / 2)
    if cx is None: cx, cy = W / 2, H / 2
    if expr == 'erro':                       # tremor
        r = np.random.default_rng(int(t * 30)); cx += r.uniform(-7, 7); cy += r.uniform(-5, 5); z = max(z, 1.012)
    if abs(z - 1) > 1e-4:
        cw, ch = W / z, H / z; x0 = min(max(cx - cw / 2, 0), W - cw); y0 = min(max(cy - ch / 2, 0), H - ch)
        im = im.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
    return im
def glitch_eyes(im, t):
    """Erro de sistema: olhos duplicados (separação verde/vermelho) + fatias deslocadas no ecrã."""
    box = (SCR[0] + 6, SCR[1] + 6, SCR[2] - 6, SCR[3] - 6)
    reg = im.crop(box); r, g, b = reg.split()
    off = 9 + int(4 * math.sin(t * 40))
    red = Image.merge('RGB', (r, Image.new('L', reg.size, 0), Image.new('L', reg.size, 0)))
    red = ImageChops.offset(red, off, 0)
    grn = Image.merge('RGB', (Image.new('L', reg.size, 0), g, b))
    grn = ImageChops.offset(grn, -off, 0)
    reg2 = ImageChops.add(red, grn)
    rr = np.random.default_rng(int(t * 30) + 7); arr = np.array(reg2)
    for _ in range(4):
        y0 = rr.integers(0, arr.shape[0] - 12); hh = rr.integers(4, 14); sh = rr.integers(-18, 18)
        arr[y0:y0 + hh] = np.roll(arr[y0:y0 + hh], sh, axis=1)
    im.paste(Image.fromarray(arr), box[:2])
    return im

# ---------- DENTRO: terminal ----------
TERM_BG = Image.new('RGB', (W, H), BG)
_sl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); _d = ImageDraw.Draw(_sl)
for y in range(0, H, 4): _d.line((0, y, W, y), fill=(0, 0, 0, 60))
vig = Image.new('L', (W, H), 0); vd = ImageDraw.Draw(vig); vd.ellipse((-300, -200, W + 300, H + 200), fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(220)); SCANL = _sl
tcols = [dict(x=x, y=rng.uniform(0, H), v=rng.uniform(60, 160)) for x in range(30, W, 46)]
EGG0, EGG1 = ws(33) - .1, ws(55) - .1    # easter egg «29» na chuva de código = número de duplas da 1.ª edição da Taça
def mix_bg(col, a):   # cor já misturada com o fundo (o alfa do texto não é respeitado pelo Pillow aqui)
    return tuple(int(BG[i] + (col[i] - BG[i]) * a / 255) for i in range(3))
def term_base(t, alpha=36):
    im = TERM_BG.copy(); d = ImageDraw.Draw(im, 'RGBA'); fs = F(MONO, 24)
    for c in tcols:
        y = (c['y'] + t * c['v']) % (H + 200) - 100
        for k in range(9):
            ch = GLY[int(t * 6 + k * 3 + c['x']) % len(GLY)]
            d.text((c['x'], y - k * 30), ch, font=fs, fill=mix_bg(PH, alpha * (1 - k / 9)))
    if EGG0 <= t < EGG1:
        for k, ch in enumerate('29'): d.text((tcols[22]['x'], 1250 + k * 30), ch, font=fs, fill=mix_bg(PH, 90))
    return im, d
def term_finish(im):
    im = Image.composite(im, Image.new('RGB', (W, H), (0, 0, 0)), vig); im.paste(SCANL, (0, 0), SCANL); return im
def hud(d, t):
    a = led_amp(t)
    d.ellipse((80, 1676, 100, 1696), fill=(16, 185, 129, int(70 + 185 * a)))
    d.text((114, 1686), 'BINDER', font=F(MONOB, 28), fill=(16, 185, 129, 220), anchor='lm')
    d.text((W - 80, 1686), 'META EM CURTO · ESPECIAL 02', font=F(MONO, 26), fill=(150, 170, 175, 220), anchor='rm')
def fontes(d, linhas, y=1384):
    """Linha(s) de fonte, ≥ 24 px de altura de letra (corrige o EP01)."""
    for i, s in enumerate(linhas):
        f = fit(d, s, COND, 34, W - 160)
        d.text((80, y + i * 44), s, font=f, fill=(150, 170, 175, 235))

# ---------- legendas palavra a palavra ----------
def chunks():
    out = []; cur = []
    for w in WORDS:
        cur.append(w)
        if w['t'][-1] in '.,:?!' or len(cur) >= 4: out.append(cur); cur = []
    if cur: out.append(cur)
    return out
CH = chunks()
def subs(im, t, y=1540):
    d = ImageDraw.Draw(im, 'RGBA')
    for c in CH:
        if c[0]['vs'] - 0.05 <= t <= c[-1]['ve'] + 0.12:
            f = F(MONOB, 50); txt = [w['t'].upper() for w in c]
            sp = d.textlength(' ', font=f); tot = sum(d.textlength(s, font=f) for s in txt) + sp * (len(txt) - 1)
            if tot > W - 160:
                f = fit(d, ' '.join(txt), MONOB, 50, W - 160); sp = d.textlength(' ', font=f)
                tot = sum(d.textlength(s, font=f) for s in txt) + sp * (len(txt) - 1)
            x = (W - tot) / 2
            d.rounded_rectangle((x - 24, y - 50, x + tot + 24, y + 28), 12, fill=(5, 10, 16, 210))
            for w, s in zip(c, txt):
                on = t >= w['vs'] - 0.03
                d.text((x, y), s, font=f, fill=(PH if on else (60, 90, 75)), anchor='ls'); x += d.textlength(s, font=f) + sp
            break
    return im
def top_card(im, lines, k=1.0, y=210):
    d = ImageDraw.Draw(im, 'RGBA')
    for s, font, col in lines:
        d.text((W / 2, y), s, font=font, fill=col + (int(255 * k),), anchor='ma'); y += font.size * 1.15
    return im



# ---------- ESP01: dados (fontes em fontes.txt) ----------
AMBER = (255, 176, 32)
EGGCOL = 22
def stamp(d, txt, col, t0, t, y, size=40):
    if t < t0: return
    k = eio((t - t0) / 0.18); f = F(MONOB, int(size + 14 * (1 - k)))
    wd = d.textlength(txt, font=f) + 50
    d.rounded_rectangle((W / 2 - wd / 2, y - 34, W / 2 + wd / 2, y + 34), 10, outline=col, width=4)
    d.text((W / 2, y), txt, font=f, fill=col, anchor='mm')
def wrap2(d, s, font, maxw):
    if d.textlength(s, font=font) <= maxw: return [s]
    p = s.split(); best = None
    for i in range(1, len(p)):
        a, b = ' '.join(p[:i]), ' '.join(p[i:]); m = max(d.textlength(a, font=font), d.textlength(b, font=font))
        if best is None or m < best[0]: best = (m, [a, b])
    return best[1]
# ---------- gancho: comandantes dos precons mais jogados da Taça (Scryfall) ----------
def _card(n):
    c = Image.open(K + f'oraculo/esp02/cartas/{n}.jpg').convert('RGB')
    m = Image.new('L', c.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, c.size[0] - 1, c.size[1] - 1), 26, fill=255)
    c = c.convert('RGBA'); c.putalpha(m); return c
CARTAS = [_card(n) for n in ('brass', 'jace', 'shiko', 'pantlaza')]
_cc = {}
def card_img(i, w, dim=0.0):
    key = (i, int(w), round(dim, 2))
    if key not in _cc:
        c = CARTAS[i]; h = int(w * c.height / c.width); r = c.resize((int(w), h), Image.LANCZOS)
        if dim > 0:
            dark = Image.new('RGBA', r.size, (5, 10, 16, 255)); a = r.getchannel('A')
            r = Image.blend(r, dark, dim); r.putalpha(a)
        if len(_cc) > 400: _cc.clear()
        _cc[key] = r
    return _cc[key]
GRID = [(55, 250), (555, 250), (55, 945), (555, 945)]; GW = 470            # 2×2 em ecrã inteiro (mesa de 4)
ROW = [(30, 92), (285, 92), (555, 92), (810, 92)]; RW = 240               # duas duplas por cima do TUBO
def glow_box(im, box, col=PH, r=26):
    g = Image.new('RGBA', im.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.rounded_rectangle(box, r, outline=col + (255,), width=16); g = g.filter(ImageFilter.GaussianBlur(14))
    im.alpha_composite(g); ImageDraw.Draw(im).rounded_rectangle(box, r, outline=col + (255,), width=6)
def pill(d, cx, cy, txt, col, size=44):
    f = F(MONOB, size); wd = d.textlength(txt, font=f) + 40
    d.rounded_rectangle((cx - wd / 2, cy - size * .75, cx + wd / 2, cy + size * .75), int(size * .75), fill=(5, 10, 16, 235), outline=col, width=4)
    d.text((cx, cy), txt, font=f, fill=col, anchor='mm')
def pop_text(d, cx, cy, txt, t0, t, size, col):
    if t < t0: return
    k = eio((t - t0) / 0.22); sz = int(size * (1.35 - 0.35 * k))
    f = F(INTB, sz)
    for dx, dy in ((6, 6), (-2, 6)): d.text((cx + dx, cy + dy), txt, font=f, fill=(0, 0, 0, 200), anchor='mm')
    d.text((cx, cy), txt, font=f, fill=col, anchor='mm')
NOMES = ['Ahoy Mateys', 'Multiverse Reforged', 'Jeskai Striker', 'Veloci-Ramp-Tor']
def hook(t):
    T50, TMOV, T66 = ws(2) - .05, ws(8) - .05, ws(9) - .05
    km = eio((t - TMOV) / 0.5) if t >= TMOV else 0.0
    base = tubo_frame(t, 'desconfiado' if t < TMOV else 'confiante').convert('RGBA')
    shade = Image.new('RGBA', base.size, (3, 6, 10, int(225 * (1 - km))))
    im = base.copy(); im.alpha_composite(shade); d = ImageDraw.Draw(im, 'RGBA')
    if km < 1:
        a = int(255 * max(0, 1 - km * 2.5))
        d.text((W / 2, 120), 'TAÇA PRECONAUTA · 2x2', font=F(MONOB, 50), fill=(200, 215, 220, a), anchor='mm')
        d.text((W / 2, 185), 'comandantes de precons mais jogados da Taça', font=F(COND, 30), fill=(140, 160, 165, a), anchor='mm')
    for i in range(4):
        t0 = 0.06 * i; ks = eio((t - t0 + 0.07) / 0.25)
        if ks <= 0: continue
        gx, gy = GRID[i]; rx, ry = ROW[i]
        w = GW + (RW - GW) * km; x = gx + (rx - gx) * km; y = gy + (ry - gy) * km
        sc = 1.18 - 0.18 * ks; w2 = w * sc; x -= (w2 - w) / 2; y -= (w2 - w) * 0.7
        dim = 0.6 if (t >= T66 and i >= 2) else 0.0
        c = card_img(i, w2, dim); im.alpha_composite(c, (int(x), int(y)))
        if t >= T66 and i < 2: glow_box(im, (int(x), int(y), int(x + c.width), int(y + c.height)))
        d = ImageDraw.Draw(im, 'RGBA')
        if km < 0.5 and ks > 0.6:
            f = F(CONDB, 30); s_ = NOMES[i]; wd = d.textlength(s_, font=f) + 30; cx = x + c.width / 2; cy = y + c.height - 60
            d.rounded_rectangle((cx - wd / 2, cy - 24, cx + wd / 2, cy + 24), 24, fill=(5, 10, 16, 230), outline=EM, width=3)
            d.text((cx, cy), s_, font=f, fill=WHITE, anchor='mm')
    if km >= 0.5:
        kk = eio((km - 0.5) / 0.5)
        pill(d, 280, 92 + int(RW * 1.4) + 4, 'COMEÇA', PH if t >= T66 else WHITE, int(24 + 8 * kk))
        pill(d, 800, 92 + int(RW * 1.4) + 4, 'EM 2º', GREY, int(24 + 8 * kk))
        d.text((540, 92 + int(RW * 0.7)), 'VS', font=F(MONOB, 34), fill=GREY, anchor='mm')
    if T50 <= t < TMOV + 0.25:
        d.rounded_rectangle((250, 800, 830, 1130), 40, fill=(3, 6, 10, 215), outline=WHITE, width=4)
        pop_text(d, W / 2, 935, '50%', T50, t, 230, WHITE)
        d.text((W / 2, 1085), 'a conta do TUBO', font=F(MONOB, 40), fill=GREY, anchor='mm')
        if t >= ws(5) - .05:       # «A Taça Preconauta respondeu»: risca
            k = eio((t - ws(5) + .05) / 0.25)
            d.line((290, 1000, 290 + 500 * k, 860), fill=RED, width=16)
    if t >= T66:                       # «66%» no ecrã do TUBO: o mergulho entra nele
        k = eio((t - T66) / 0.2); f = F(INTB, int(84 * (1.3 - .3 * k)))
        d.rounded_rectangle(SCR, 18, fill=(4, 14, 10, 235))
        d.text((SCX, SCY - 10), '66%', font=f, fill=PH, anchor='mm')
        d.text((SCX, SCY + 62), 'quem começa', font=F(MONOB, 24), fill=EM, anchor='mm')
    return im.convert('RGB')

# ---------- DENTRO ----------
def tile(d, x, y, w, h, num, lab, col, t0, t):
    if t < t0: return
    k = eio((t - t0) / 0.25)
    d.rounded_rectangle((x, y, x + w, y + h), 16, outline=col, width=3, fill=(8, 20, 18, 255))
    d.text((x + w / 2, y + h * 0.42), num, font=F(INTB, int(96 * (1.25 - .25 * k))), fill=col, anchor='mm')
    d.text((x + w / 2, y + h - 34), lab, font=F(MONOB, 28), fill=GREY, anchor='mm')
def bar(d, x, y, w, pct, col, lab, t0, t, h=64, ref=None):
    if t < t0: return
    k = eio((t - t0) / 0.45); fw = w * pct / 100 * k
    d.rounded_rectangle((x, y, x + w, y + h), 12, fill=(15, 23, 42, 255), outline=(40, 60, 70), width=2)
    if fw > 4: d.rounded_rectangle((x, y, x + fw, y + h), 12, fill=col)
    if ref is not None:
        rx = x + w * ref / 100
        for yy in range(int(y - 12), int(y + h + 12), 14): d.line((rx, yy, rx, yy + 7), fill=WHITE, width=3)
    d.text((x + 18, y + h / 2), lab, font=F(CONDB, 34), fill=WHITE, anchor='lm')
    d.text((x + w - 18, y + h / 2), f'{round(pct * k)}%', font=F(INTB, 44), fill=WHITE, anchor='rm')
def _print(n):
    im = Image.open(K + f'oraculo/esp02/comentarios/{n}.png').convert('RGB')
    return im.resize((920, round(im.height * 920 / im.width)), Image.LANCZOS)
PR_JOREL, PR_PRECO = _print('jorel_oliveira'), _print('preconautamtg_arvore')
def scan_print(im, pr, x, y, t0, t):
    """Print real de comentário (foto + texto), com entrada «scan» de cima para baixo."""
    if t < t0: return ImageDraw.Draw(im, 'RGBA')
    d = ImageDraw.Draw(im, 'RGBA'); k = eio((t - t0) / 0.7); ch = max(1, int(pr.height * k))
    d.rounded_rectangle((x - 8, y - 8, x + pr.width + 8, y + ch + 8), 18, fill=(255, 255, 255, 255))
    im.paste(pr.crop((0, 0, pr.width, ch)), (x, y)); d = ImageDraw.Draw(im, 'RGBA')
    if k < 1: d.rectangle((x, y + ch - 3, x + pr.width, y + ch + 3), fill=PH + (255,))
    d.rounded_rectangle((x - 8, y - 8, x + pr.width + 8, y + ch + 8), 18, outline=EM, width=4)
    return d
def tile_s(d, x, y, w, h, num, lab, col, t0, t):
    if t < t0: return
    k = eio((t - t0) / 0.25)
    d.rounded_rectangle((x, y, x + w, y + h), 16, outline=col, width=3, fill=(8, 20, 18, 255))
    d.text((x + w / 2, y + h * 0.40), num, font=F(INTB, int(76 * (1.25 - .25 * k))), fill=col, anchor='mm')
    d.text((x + w / 2, y + h - 30), lab, font=F(MONOB, 26), fill=GREY, anchor='mm')
def scene_fonte(t):
    im, d = term_base(t, 18)
    t0 = DIVE_END - 0.1
    s1 = '> ARQUIVO: A COMUNIDADE RESPONDEU'
    d.text((80, 200), typed(s1, t0, t), font=fit(d, s1, MONOB, 38, 920), fill=PH)
    d.text((80, 258), typed('  comentários no @binderthetrade · nov/2026', t0 + .3, t), font=F(MONO, 28), fill=EM)
    d.line((80, 312, 1000, 312), fill=(16, 185, 129, 90), width=2)
    if t >= DIVE_END + 0.1:
        d.rounded_rectangle((80, 330, 1000, 430), 16, outline=AMBER, width=3, fill=(20, 16, 8, 255))
        d.text((110, 345), 'TUBO · ESPECIAL 01', font=F(MONOB, 24), fill=AMBER)
        d.text((110, 378), '«Ninguém publica win rate de dupla. Ainda.»', font=fit(d, '«Ninguém publica win rate de dupla. Ainda.»', INTB, 40, 860), fill=WHITE)
    d = scan_print(im, PR_JOREL, 80, 458, ws(15) - .1, t)
    if t >= ws(15) - .05:
        k = eio((t - ws(15) + .05) / 0.3)
        d.line((110, 401, 110 + 860 * k, 401), fill=RED, width=5)
        d.rounded_rectangle((720, 338, 990, 372), 17, fill=(5, 40, 20, 255), outline=PH, width=3)
        d.text((855, 355), 'AGORA PUBLICAM', font=F(MONOB, 24), fill=PH, anchor='mm')
    d = scan_print(im, PR_PRECO, 80, 818, ws(17) - .1, t)
    tile_s(d, 80, 1130, 290, 190, '101', 'MATCHES', PH, ws(20) - .05, t)
    tile_s(d, 395, 1130, 290, 190, '230', 'JOGOS', PH, ws(24) - .05, t)
    tile_s(d, 710, 1130, 290, 190, '97', 'PRECONS', PH, ws(28) - .05, t)
    fontes(d, ['prints reais dos comentários · Taça Preconauta 1ª edição (taca.preconauta.com.br)', 'dados usados com autorização do @preconautamtg · a Taça está em andamento'], 1384)
    hud(d, t); return term_finish(im)
def scene_ordem(t):
    im, d = term_base(t, 14)
    d.text((80, 200), '> ORDEM DE TURNO · QUEM COMEÇA VENCE?', font=fit(d, '> ORDEM DE TURNO · QUEM COMEÇA VENCE?', MONOB, 36, 920), fill=PH)
    d.text((80, 252), '  jogos empatados não contam', font=F(MONO, 28), fill=EM)
    d.line((80, 304, 1000, 304), fill=(16, 185, 129, 90), width=2)
    if t >= ws(33) - .05:
        d.text((80, 350), 'JOGO 1 · ordem sorteada', font=F(MONOB, 34), fill=WHITE)
        d.text((80, 395), '70 jogos com vencedor', font=F(COND, 30), fill=GREY)
    bar(d, 80, 445, 920, 66, (16, 120, 80), 'quem começa', ws(42) - .05, t, ref=50)
    if t >= ws(42) + .3: d.text((80 + 920 * .5, 525), 'previsão do TUBO: 50%', font=F(MONO, 26), fill=GREY, anchor='ma')
    if t >= ws(48) - .05:
        d.text((80, 600), 'TODOS OS JOGOS', font=F(MONOB, 34), fill=WHITE)
        d.text((80, 645), '181 jogos com vencedor', font=F(COND, 30), fill=GREY)
    bar(d, 80, 695, 920, 59, (16, 100, 70), 'quem começa', ws(48) - .05, t, ref=50)
    if t >= ws(55) - .05:
        d.rounded_rectangle((80, 830, 1000, 1030), 16, outline=AMBER, width=3, fill=(20, 16, 8, 255))
        d.text((540, 900), '52 DE 101', font=F(INTB, 92), fill=WHITE, anchor='mm')
        d.text((540, 985), 'matches foram para o 3º jogo', font=F(CONDB, 38), fill=AMBER, anchor='mm')
    if t >= ws(56) - .05: stamp(d, 'MAIS DA METADE', AMBER, ws(56), t, 1080, 40)
    fontes(d, ['Taça Preconauta · no jogo 1 quem começa é sorteado', 'margem (cálculo nosso, 95%): jogo 1 entre 55% e 77%'], 1384)
    hud(d, t); return term_finish(im)
def deck_row(im, d, y, ci, nome, jogos, p1, p2, t1, t2, t):
    c = card_img(ci, 200); im.alpha_composite(c, (80, y)); d = ImageDraw.Draw(im, 'RGBA')
    d.text((310, y + 6), nome.upper(), font=F(INTB, 52), fill=WHITE)
    d.text((310, y + 72), f'{jogos} jogos na Taça', font=F(COND, 30), fill=GREY)
    bar(d, 310, y + 125, 690, p1, (16, 120, 80), 'começando', t1, t, h=58)
    bar(d, 310, y + 200, 690, p2, ((16, 120, 80) if p2 >= 50 else (150, 40, 50)), 'em 2º', t2, t, h=58)
    return d
def scene_decks(t):
    im, d = term_base(t, 14)
    d.text((80, 200), '> PRECONS MAIS JOGADOS · COMEÇANDO × EM 2º', font=fit(d, '> PRECONS MAIS JOGADOS · COMEÇANDO × EM 2º', MONOB, 36, 920), fill=PH)
    d.text((80, 252), '  começando = turnos 1 e 3 · em 2º = turnos 2 e 4', font=F(MONO, 26), fill=EM)
    d.line((80, 304, 1000, 304), fill=(16, 185, 129, 90), width=2)
    im = im.convert('RGBA'); d = ImageDraw.Draw(im, 'RGBA')
    if t >= ws(67) - .05: d = deck_row(im, d, 350, 0, 'Ahoy Mateys', 56, 72.4, 36.8, ws(70) - .05, ws(76) - .05, t)
    if t >= ws(81) - .05: d = deck_row(im, d, 690, 2, 'Jeskai Striker', 45, 70.8, 56.2, ws(83) - .05, ws(89) - .05, t)
    if t >= ws(85) - .05: stamp(d, 'ÚNICO DOS 6 MAIS JOGADOS ACIMA DE 50% EM 2º', PH, ws(85), t, 1010, 32)
    fontes(d, ['Taça Preconauta · % por jogo de cada jogador que usou o deck', 'top 6 em 2º: Scions 45% · Multiverse 48% · Counter Blitz 19% · Veloci 31%'], 1384)
    hud(d, t); return term_finish(im.convert('RGB'))

# ---------- timeline ----------
DIVE = TL['DIVE']; DIVE_END = DIVE + 0.45; EXIT = TL['EXIT']; EXIT_END = EXIT + 0.75
REV0, REV1 = TL['REV0'], TL['REV1']
T_Q = ws(119) - 0.1; T_SIG = ws(138) - 0.15
def inside(t):
    if t < ws(33) - .1: return scene_fonte(t)
    if t < ws(66) - .1: return scene_ordem(t)
    return scene_decks(t)
SUBY = 1530
def note(d, s):
    f = F(COND, 34); wd = d.textlength(s, font=f)
    d.rounded_rectangle((W / 2 - wd / 2 - 16, 1418, W / 2 + wd / 2 + 16, 1468), 8, fill=(5, 10, 16, 215))
    d.text((W / 2, 1443), s, font=f, fill=(170, 190, 195), anchor='mm')
def meter(d, y, n, lab='GRAU DE CERTEZA'):
    d.text((90, y + 20), lab, font=F(MONOB, 28), fill=GREY, anchor='lm')
    for s in range(5):
        x = 420 + s * 66
        d.rounded_rectangle((x, y, x + 56, y + 40), 7, fill=(EM if s < n else None), outline=EM, width=3)
    d.text((990, y + 20), f'{n} de 5', font=F(MONOB, 30), fill=EM, anchor='rm')
# ---------- OUTRO: ficheiro real do fecho ----------
def load_outro():
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', K + 'comum/outro/outro_binder_916.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                         capture_output=True).stdout
    n = len(raw) // (W * H * 3)
    return [Image.frombuffer('RGB', (W, H), raw[i * W * H * 3:(i + 1) * W * H * 3]) for i in range(n)]
OUTRO = None
def outro(t):
    global OUTRO
    if OUTRO is None: OUTRO = load_outro()
    return OUTRO[min(len(OUTRO) - 1, int(t * FPS))].copy()
def frame(t):
    if t >= OUT: return outro(t - OUT)
    if t >= OUT - 0.2:
        a = (t - (OUT - 0.2)) / 0.2; return Image.blend(frame_main(OUT - 0.21), outro(0), a)
    return frame_main(t)
def frame(t):
    if t >= OUT: return outro(t - OUT)
    if t >= OUT - 0.2:
        a = (t - (OUT - 0.2)) / 0.2; return Image.blend(frame_main(OUT - 0.21), outro(0), a)
    return frame_main(t)
def frame_main(t):
    if t < DIVE_END:
        if t < DIVE:
            return subs(hook(t), t, 1700 if t < ws(8) else SUBY)
        k = eio((t - DIVE) / (DIVE_END - DIVE)); z = 1 + k * 4.2
        im = hook(DIVE - 0.001).resize((int(W * z), int(H * z)), Image.LANCZOS)
        ox = int(SCX * z - (W / 2 + (SCX - W / 2) * min(1, k * 1.5))); oy = int(SCY * z - (H / 2 + (SCY - H / 2) * min(1, k * 1.5)))
        im = im.crop((ox, oy, ox + W, oy + H))
        if k > 0.6: im = Image.blend(im, scene_fonte(t), (k - 0.6) / 0.4)
        return im
    if t < EXIT: return subs(inside(t), t)
    if t < EXIT_END:
        k = eio((t - EXIT) / (EXIT_END - EXIT)); z = 5.2 - 4.2 * k
        im = tubo_frame(t, 'confiante', zoom=z, cx=W / 2 + (SCX - W / 2) * (1 - k), cy=H / 2 + (SCY - H / 2) * (1 - k))
        if k < 0.35: im = Image.blend(inside(t), im, k / 0.35)
        return subs(im, t, SUBY)
    if t < T_Q:
        err = ws(92) - .08 <= t < ws(95) - .05            # «Errei a conta» = Erro de sistema (bíblia)
        kp = eio((t - REV0) / (REV1 - REV0 + 0.4)) if t >= REV0 else 0.0   # corte seco: aproximação lenta, sem pausa morta
        im = tubo_frame(t, 'erro' if err else 'confiante', zoom=1.0 + .03 * eio((t - EXIT_END) / 3) + 0.05 * kp, red_led=err)
        d = ImageDraw.Draw(im, 'RGBA')
        if err:
            rr = np.random.default_rng(int(t * 30)); jx = int(rr.integers(-8, 8))
            d.text((W / 2 + jx, 140), 'ERREI A CONTA.', font=F(INTB, 72), fill=RED, anchor='mm')
            d.rounded_rectangle((120, 205, 960, 300), 14, fill=(5, 10, 16, 230), outline=(255, 64, 64, 200), width=3)
            d.text((150, 252), '> MODELO TUBO: 50%', font=F(MONOB, 34), fill=WHITE, anchor='lm')
            d.text((930, 252), 'REAL: 66%', font=F(MONOB, 34), fill=RED, anchor='rm')
            for _ in range(3):
                y0 = int(rr.integers(110, 300)); d.rectangle((120, y0, 960, y0 + int(rr.integers(2, 6))), fill=(255, 64, 64, 90))
        elif t >= ws(92) - .05:
            d.text((W / 2, 140), 'ERREI A CONTA.', font=F(INTB, 72), fill=AMBER, anchor='mm')
        if t >= ws(95) - .05: d.text((W / 2, 205), 'A DUPLA IGUALA A MESA.', font=fit(d, 'A DUPLA IGUALA A MESA.', INTB, 60, 960), fill=GREY, anchor='ma')
        if t >= ws(100) - .05: pop_text(d, W / 2, 305, 'A ORDEM DE TURNO DESEMPATA.', ws(100) - .05, t, 62, PH)
        if t >= ws(105) - .05:
            meter(d, 360, 4 if t >= ws(108) - .05 else 0)
            if t >= ws(111) - .05:
                s_ = '70 jogos sorteados · a Taça ainda está rolando'
                d.text((W / 2, 412), s_, font=fit(d, s_, COND, 30, 960), fill=(170, 190, 195), anchor='ma')
        note(d, 'leitura do TUBO sobre os dados da Taça Preconauta')
        return subs(im, t, SUBY)
    if t < T_SIG:
        im = tubo_frame(t, 'analitico', zoom=1.0); d = ImageDraw.Draw(im, 'RGBA')
        q = 'Qual precon você leva pra Taça?'
        d.text((W / 2, 130), q, font=fit(d, q, INTB, 64, 960), fill=WHITE, anchor='ma')
        ops = [('A', 'Ahoy Mateys', 125), ('B', 'Jeskai Striker', 128), ('C', 'Multiverse Reforged', 131)]
        for i, (l, s_, wi) in enumerate(ops):
            if t < ws(wi) - .05: continue
            y = 215 + i * 64; on = t >= ws(134) - .05
            d.rounded_rectangle((170, y, 910, y + 54), 27, fill=((10, 52, 30, 255) if on else (15, 23, 42, 230)), outline=EM, width=3)
            d.text((215, y + 27), l, font=F(MONOB, 36), fill=PH, anchor='mm')
            d.text((560, y + 27), s_, font=F(CONDB, 38), fill=(PH if on else WHITE), anchor='mm')
        if t >= ws(134) - .05: note(d, 'responda com a letra')
        return subs(im, t, SUBY)
    kz = eio((t - T_SIG) / 1.2)
    im = tubo_frame(t, 'confiante', zoom=1.0 + 0.22 * kz, cx=W / 2, cy=H / 2 + (SCY + 260 - H / 2) * kz)
    k = ease((t - T_SIG) / 0.4)
    im = top_card(im, [('META EM CURTO', F(INTB, 96), WHITE), ('com TUBO · BINDER Originals', F(MONO, 34), EM)], k, 225)
    return subs(im, t, SUBY)
if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[2] == 'capa':
        # Capa v3: um ponto focal (66%), uma frase, uma personagem. Tudo dentro do recorte 3:4 da grelha (y 240–1680).
        im = Image.new('RGBA', (W, H), BG + (255,))
        # fundo: leque de comandantes, escurecido e desfocado (textura «isto é Magic», sem competir com o texto)
        bgc = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        for ci, ang, x, y in [(0, 14, -120, 560), (1, 5, 160, 470), (2, -5, 470, 470), (3, -14, 760, 560)]:
            c = card_img(ci, 420).rotate(ang, resample=Image.BICUBIC, expand=True); bgc.alpha_composite(c, (x, y))
        bgc = bgc.filter(ImageFilter.GaussianBlur(3)); im.alpha_composite(bgc)
        dark = Image.new('RGBA', (W, H), BG + (170,)); im.alpha_composite(dark)
        # TUBO em «Erro de sistema» (a cara da série reage ao número)
        tb = tubo_frame(33.9, 'erro', zoom=1.0, red_led=True).convert('RGBA')
        tb = tb.crop((150, 380, 930, 1500)).resize((700, 1005), Image.LANCZOS)
        m = Image.new('L', tb.size, 0); ImageDraw.Draw(m).ellipse((40, 30, tb.width - 40, tb.height + 300), fill=255)
        tb.putalpha(m.filter(ImageFilter.GaussianBlur(45))); im.alpha_composite(tb, ((W - tb.width) // 2, 820))
        d = ImageDraw.Draw(im, 'RGBA')
        # 1) frase (uma linha, branca)
        d.text((W / 2, 330), 'QUEM COMEÇA VENCE', font=fit(d, 'QUEM COMEÇA VENCE', INTB, 112, 980), fill=WHITE, anchor='mm')
        # 2) ponto focal: 66% gigante, com brilho
        g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        gd.text((W / 2, 600), '66%', font=F(INTB, 400), fill=PH + (200,), anchor='mm'); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(28)))
        d = ImageDraw.Draw(im, 'RGBA')
        d.text((W / 2, 600), '66%', font=F(INTB, 400), fill=PH, anchor='mm')
        # 3) a correção: 50% riscado, como carimbo de erro ao lado do TUBO (não toca no ponto focal)
        st = Image.new('RGBA', (360, 150), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
        sd.rounded_rectangle((6, 6, 354, 144), 20, outline=RED, width=8, fill=(30, 6, 8, 230))
        sd.text((180, 75), '50%', font=F(INTB, 104), fill=RED, anchor='mm'); sd.line((30, 115, 330, 35), fill=RED, width=12)
        st = st.rotate(-10, resample=Image.BICUBIC, expand=True); im.alpha_composite(st, (690, 900))   # a previsão errada fica junto do TUBO
        d = ImageDraw.Draw(im, 'RGBA')
        # 4) assinatura fixa da série (mesma posição em todas as capas → o perfil orienta-se)
        d.rectangle((0, 1572, W, 1662), fill=(5, 10, 16, 235)); d.line((0, 1572, W, 1572), fill=PH, width=4)
        d.text((60, 1617), 'META EM CURTO · ESP. 02', font=F(MONOB, 40), fill=PH, anchor='lm')
        d.text((W - 60, 1617), '× PRECONAUTA', font=F(MONOB, 40), fill=AMBER, anchor='rm')
        im.convert('RGB').save('ESP02_CAPA.png')
        im.convert('RGB').crop((0, 240, W, 1680)).save('ESP02_CAPA_grelha.png')
        sys.exit()
    if len(sys.argv) > 2 and sys.argv[2] == 'capa_comunidade':
        # Variante «comunidade» do modelo de capa (CONTEXTO §7.3): o foco são os prints reais de quem comentou
        # (influenciador verificado, organizador da liga, liga/loja), para a prova social ler-se na grelha.
        im = Image.new('RGBA', (W, H), BG + (255,))
        d = ImageDraw.Draw(im, 'RGBA')
        # 1) frase
        d.text((W / 2, 300), 'A COMUNIDADE', font=F(INTB, 118), fill=WHITE, anchor='mm')
        d.text((W / 2, 420), 'CORRIGIU O TUBO', font=fit(d, 'CORRIGIU O TUBO', INTB, 118, 980), fill=PH, anchor='mm')
        # 2) foco: os três prints reais, empilhados como cartas
        prints = [(K + 'oraculo/esp01/comentario_diarioplaninauta.png', -2.0), (K + 'oraculo/esp02/comentarios/jorel_oliveira.png', 1.6),
                  (K + 'oraculo/esp02/comentarios/preconautamtg_arvore.png', -1.2)]
        y = 520
        for path, ang in prints:
            pr = Image.open(path).convert('RGB'); pr = pr.resize((940, round(pr.height * 940 / pr.width)), Image.LANCZOS)
            card = Image.new('RGBA', (pr.width + 24, pr.height + 24), (255, 255, 255, 255)); card.paste(pr, (12, 12))
            m = Image.new('L', card.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, card.width - 1, card.height - 1), 22, fill=255); card.putalpha(m)
            sh = Image.new('RGBA', (card.width + 80, card.height + 80), (0, 0, 0, 0))
            ImageDraw.Draw(sh).rounded_rectangle((40, 50, card.width + 40, card.height + 50), 26, fill=(0, 0, 0, 170))
            sh = sh.filter(ImageFilter.GaussianBlur(18)).rotate(ang, resample=Image.BICUBIC, expand=True)
            cr = card.rotate(ang, resample=Image.BICUBIC, expand=True)
            x = (W - cr.width) // 2
            im.alpha_composite(sh, (x - 40, y - 40)); im.alpha_composite(cr, (x, y))
            y += card.height - 30
        # 3) apoio: a correção do TUBO, sobre a linha de ações do último print (não tapa texto de ninguém)
        d = ImageDraw.Draw(im, 'RGBA')
        st = Image.new('RGBA', (500, 110), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
        sd.rounded_rectangle((4, 4, 496, 106), 22, fill=(30, 6, 8, 245), outline=RED, width=6)
        sd.text((250, 55), 'TUBO: 50% → 66%', font=fit(sd, 'TUBO: 50% → 66%', INTB, 50, 440), fill=WHITE, anchor='mm')
        st = st.rotate(-4, resample=Image.BICUBIC, expand=True); im.alpha_composite(st, (W - st.width - 30, y - 48))
        d = ImageDraw.Draw(im, 'RGBA')
        # 4) faixa fixa da série
        d.rectangle((0, 1572, W, 1662), fill=(5, 10, 16, 255)); d.line((0, 1572, W, 1572), fill=PH, width=4)
        d.text((60, 1617), 'META EM CURTO · ESP. 02', font=F(MONOB, 40), fill=PH, anchor='lm')
        d.text((W - 60, 1617), '× PRECONAUTA', font=F(MONOB, 40), fill=AMBER, anchor='rm')
        im.convert('RGB').save('ESP02_CAPA_COMUNIDADE.png')
        im.convert('RGB').crop((0, 240, W, 1680)).save('ESP02_CAPA_COMUNIDADE_grelha.png')
        sys.exit()
    if len(sys.argv) > 2 and sys.argv[2] == 'stills':
        for tt in map(float, sys.argv[3:]): frame(tt).save(f'still_{tt:05.2f}.png')
        sys.exit()
    nf = int(round(TOTAL * FPS))
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-i', 'mix_final.wav', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
                          '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', '-shortest', 'ESP02_META_EM_CURTO.mp4'],
                         stdin=subprocess.PIPE)
    for i in range(nf): p.stdin.write(frame(i / FPS).convert('RGB').tobytes())
    p.stdin.close(); p.wait(); print('done', nf)
