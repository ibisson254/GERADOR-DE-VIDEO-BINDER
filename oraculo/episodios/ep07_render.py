# Meta em Curto EP07 · Mundial 32 · render (derivado de ep04_render.py)
# Uso, numa pasta de trabalho com tl.json, words.json, led_env.npy e mix_final.wav (saídas de ep07_audio.py):
#   python3 ep07_render.py /caminho/do/kit             -> EP07_META_EM_CURTO.mp4
#   python3 ep07_render.py /caminho/do/kit stills 3 10 -> still_03.00.png ...
# O fecho é o ficheiro real comum/outro/outro_binder_916.mp4 (sem áudio; a trilha do episódio continua por baixo).
import json, math, subprocess, sys, numpy as np
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
EGG0, EGG1 = ws(43), ws(52)    # easter egg «2002» na chuva de código = ano do título mundial de Carlos Romão, 1.º brasileiro campeão
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
        for k, ch in enumerate('2002'): d.text((tcols[22]['x'], 1250 + k * 30), ch, font=fs, fill=mix_bg(PH, 90))
    return im, d
def term_finish(im):
    im = Image.composite(im, Image.new('RGB', (W, H), (0, 0, 0)), vig); im.paste(SCANL, (0, 0), SCANL); return im
def hud(d, t):
    a = led_amp(t)
    d.ellipse((80, 1676, 100, 1696), fill=(16, 185, 129, int(70 + 185 * a)))
    d.text((114, 1686), 'BINDER', font=F(MONOB, 28), fill=(16, 185, 129, 220), anchor='lm')
    d.text((W - 80, 1686), 'META EM CURTO · EP07', font=F(MONO, 26), fill=(150, 170, 175, 220), anchor='rm')
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



# ---------- EP07: dados (todas as fontes em ep07_mundial_fontes.txt) ----------
AMBER = (255, 176, 32)
BRA = [('DIEGO ALMEIDA', 'RC · América do Sul', False), ('MARCELO CAVALCANTE', 'Arena Championship 11', True),
       ('ISAEL FEITOSA', 'RC · América do Sul', False), ('RAFAEL KENJI MARQUES NISHIYAMA', 'RC · América do Sul', False),
       ('JOÃO QUEGE', 'RC · América do Sul', False), ('JOÃO JORGE SALES JUNIOR', 'RC · América do Sul', False)]
META = [('Mono-Green Landfall', 12.7, 53.4), ('Dimir Midrange', 8.9, 54.5), ('Dimir Uldaros', 8.3, 49.2),
        ('Izzet Spellementals', 7.5, 44.3), ('Jund Sacrifice', 7.4, 57.6), ('Orzhov Life Gain', 6.9, 53.6)]
SIL = ["......####......", ".....######.....", "....########....", "....########....", "....########....",
       ".....######.....", "......####......", "...##########...", "..############..", ".##############.",
       ".##############.", "################", "################"]
def silhueta(d, x, y, px=13, col=PH):
    for r, row in enumerate(SIL):
        for c, ch in enumerate(row):
            if ch == '#': d.rectangle((x + c * px, y + r * px, x + c * px + px - 2, y + r * px + px - 2), fill=mix_bg(col, 150))
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

# ---------- DENTRO ----------
def scene_arquivo(t):
    im, d = term_base(t, 22)
    t0 = DIVE_END - 0.1
    s1 = '> ARQUIVO: MAGIC WORLD CHAMPIONSHIP 32'
    d.text((80, 200), typed(s1, t0, t), font=fit(d, s1, MONOB, 38, 920), fill=PH)
    d.text((80, 258), typed('  ATLANTA · 13–15/11/2026 · MAGICCON', t0 + .3, t), font=F(MONO, 30), fill=EM)
    d.line((80, 312, 1000, 312), fill=(16, 185, 129, 90), width=2)
    d.text((80, 345), '134', font=F(INTB, 120), fill=WHITE); d.text((345, 412), 'CONVIDADOS', font=F(MONOB, 40), fill=GREY)
    d.text((80, 500), '8', font=F(INTB, 120), fill=PH); d.text((175, 567), 'VAGAS NO TOP 8', font=F(MONOB, 40), fill=GREY)
    if t >= ws(13) - .05: d.text((W / 2, 720), 'MUNDIAL 32', font=F(INTB, 110), fill=WHITE, anchor='ma')
    if t >= ws(24) - .05:
        d.rounded_rectangle((80, 900, 1000, 1080), 16, outline=EM, width=3, fill=(8, 20, 18, 255))
        d.text((110, 925), 'FORMATO 1 · DRAFT', font=F(MONOB, 34), fill=GREY)
        d.text((110, 975), 'STAR TREK', font=F(INTB, 64), fill=PH)
        if t >= ws(28) - .05: d.text((980, 1000), 'lança 13/11', font=F(MONOB, 34), fill=AMBER, anchor='rm')
    if t >= ws(37) - .05:
        d.rounded_rectangle((80, 1110, 1000, 1250), 16, outline=EM, width=3, fill=(8, 20, 18, 255))
        d.text((110, 1135), 'FORMATO 2 · CONSTRUÍDO', font=F(MONOB, 34), fill=GREY)
        d.text((110, 1180), 'STANDARD', font=F(INTB, 56), fill=WHITE)
        d.text((980, 1205), 'Top 8 em Standard', font=F(MONOB, 30), fill=EM, anchor='rm')
    fontes(d, ['convidados e formatos: magic.gg (lista sujeita a alterações)', 'Star Trek: lançamento 13/11/2026 (Wizards of the Coast)'])
    hud(d, t); return term_finish(im)
def scene_brasileiros(t):
    im, d = term_base(t, 18)
    d.text((80, 200), '> FICHAS DE JOGADOR · BRASIL', font=F(MONOB, 36), fill=PH)
    d.text((80, 252), '  6 de 134 convidados · origem do convite', font=F(MONO, 28), fill=EM)
    d.line((80, 300, 1000, 300), fill=(16, 185, 129, 90), width=2)
    rc_on, ac_on = t >= ws(43) - .05, t >= ws(48) - .05
    for i, (nome, conv, arena) in enumerate(BRA):
        if t < ws(38) + i * .18: continue
        cx, cy = 80 + (i % 2) * 470, 330 + (i // 2) * 335
        hi = (ac_on and arena) or (rc_on and not arena and not ac_on)
        d.rounded_rectangle((cx, cy, cx + 450, cy + 310), 14, outline=(EM if hi else (40, 80, 70)), width=(4 if hi else 2), fill=(8, 20, 18, 255))
        silhueta(d, cx + 160, cy + 20, 8)
        f = F(CONDB, 38); ls = wrap2(d, nome, f, 410)
        f = fit(d, max(ls, key=len), CONDB, 38, 410)
        for k, s in enumerate(ls): d.text((cx + 225, cy + 140 + k * 44), s, font=f, fill=WHITE, anchor='ma')
        d.text((cx + 225, cy + 262), conv, font=fit(d, conv, MONOB, 28, 410), fill=(PH if hi else GREY), anchor='ma')
        d.text((cx + 22, cy + 18), 'BRA', font=F(MONOB, 26), fill=EM)
    if rc_on and not ac_on: d.text((W / 2, 1352 - 18), '5 · REGIONAL CHAMPIONSHIP', font=F(MONOB, 34), fill=PH, anchor='ma')
    if ac_on: d.text((W / 2, 1352 - 18), '1 · ARENA CHAMPIONSHIP 11', font=F(MONOB, 34), fill=PH, anchor='ma')
    fontes(d, ['lista oficial de convidados: magic.gg (sujeita a alterações)'], 1400)
    hud(d, t); return term_finish(im)
def scene_sorteio(t):
    im, d = term_base(t, 16)
    d.text((80, 200), '> MODELO SEM HABILIDADE', font=F(MONOB, 36), fill=PH)
    d.text((80, 252), '  e se o Top 8 fosse sorteado?', font=F(MONO, 30), fill=EM)
    d.line((80, 304, 1000, 304), fill=(16, 185, 129, 90), width=2)
    cols, r, gx, gy = 14, 22, 66, 62
    x0 = (W - (cols - 1) * gx) / 2; bra = {17, 38, 59, 76, 101, 120}
    for i in range(134):
        x, y = x0 + (i % cols) * gx, 360 + (i // cols) * gy
        if t < ws(52) + i * .006: continue
        if i in bra: d.ellipse((x - r, y - r, x + r, y + r), fill=PH)
        else: d.ellipse((x - r + 6, y - r + 6, x + r - 6, y + r - 6), outline=(60, 110, 90), width=3)
    if t >= ws(54) - .05:
        y = 1010
        for k in range(8):
            x = 110 + k * 110; d.rounded_rectangle((x, y, x + 90, y + 90), 12, outline=AMBER, width=4)
            d.text((x + 45, y + 45), str(k + 1), font=F(MONOB, 36), fill=AMBER, anchor='mm')
    if t >= ws(68) - .05:
        k = eio((t - ws(68) + .05) / .3)
        d.text((W / 2, 1120), '31%', font=F(INTB, int(110 + 30 * k)), fill=WHITE, anchor='ma')
        if t < ws(73) - .05: d.text((W / 2, 1282), '1 − C(128,8) / C(134,8) = 0,314', font=F(MONO, 30), fill=GREY, anchor='ma')
    if t >= ws(73) - .05: stamp(d, 'MUNDIAL NÃO É SORTEIO', AMBER, ws(75), t, 1308, 40)
    fontes(d, ['cálculo nosso: 6 brasileiros em 134 convidados (magic.gg)', 'modelo sem habilidade · não é previsão'], 1384)
    hud(d, t); return term_finish(im)
def bars(d, t, y, title, idx, scale, hi, t0, thi, unit):
    d.text((80, y), title, font=F(MONOB, 32), fill=GREY); y += 50
    for k, row in enumerate(META):
        if t < t0 + k * .08: y += 56; continue
        nome, v = row[0], row[idx]; on = t >= thi and nome == hi
        d.text((80, y + 20), nome, font=fit(d, nome, CONDB, 34, 350), fill=(WHITE if on else (150, 170, 175)), anchor='lm')
        k2 = eio((t - t0 - k * .08) / .5); bw = (v / scale) * 400 * k2
        d.rectangle((450, y + 4, 450 + bw, y + 36), fill=(PH if on else (40, 110, 80)))
        d.text((450 + bw + 14, y + 20), f'{v:.1f}{unit}'.replace('.', ','), font=F(MONOB, 32), fill=(PH if on else GREY), anchor='lm')
        y += 56
    return y
def scene_meta(t):
    im, d = term_base(t, 14)
    d.text((80, 200), '> RELATÓRIO DO META · STANDARD', font=F(MONOB, 36), fill=PH)
    d.text((80, 252), '  1.810 listas · AC13 + Spotlight Fracture ×2', font=F(MONO, 28), fill=EM)
    d.line((80, 300, 1000, 300), fill=(16, 185, 129, 90), width=2)
    bars(d, t, 330, 'REPRESENTAÇÃO · % do field', 1, 13.0, 'Mono-Green Landfall', ws(78), ws(91) - .05, '%')
    if t >= ws(98) - .1:
        y = bars(d, t, 750, 'DESEMPENHO · % de vitórias', 2, 60.0, 'Jund Sacrifice', ws(98) - .1, ws(103) - .05, '%')
        x50 = 450 + 50 / 60 * 400
        for yy in range(800, 1130, 14): d.line((x50, yy, x50, yy + 7), fill=(255, 176, 32, 200), width=2)
        d.text((x50, 1140), '50%', font=F(MONO, 24), fill=AMBER, anchor='ma')
    if t >= ws(114) - .05: stamp(d, 'JUND: 2 TÍTULOS · HARTFORD E PEQUIM', PH, ws(114) - .05, t, 1230, 34)
    if t >= ws(120) - .05: d.text((W / 2, 1290), 'arquivo: META EM CURTO EP02 e EP04', font=F(MONO, 28), fill=GREY, anchor='ma')
    fontes(d, ['Frank Karsten, magic.gg · 05/11/2026', 'vitórias por partida, sem espelhos, byes e empates'], 1384)
    hud(d, t); return term_finish(im)

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

# ---------- timeline ----------
DIVE = TL['DIVE']; DIVE_END = DIVE + 0.45; EXIT = TL['EXIT']; EXIT_END = EXIT + 0.75
T_REV = ws(138) - 0.1; T_Q = ws(147) - 0.1; T_SIG = ws(156) - 0.15
def inside(t):
    if t < ws(38) - .1: return scene_arquivo(t)
    if t < ws(52) - .1: return scene_brasileiros(t)
    if t < ws(78) - .1: return scene_sorteio(t)
    return scene_meta(t)
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
def frame(t):
    if t >= OUT: return outro(t - OUT)
    if t >= OUT - 0.2:
        a = (t - (OUT - 0.2)) / 0.2; return Image.blend(frame_main(OUT - 0.21), outro(0), a)
    return frame_main(t)
def frame_main(t):
    if t < DIVE_END:
        if t < DIVE:
            im = tubo_frame(t, 'desconfiado' if t < ws(8) else 'confiante', zoom=1.0 + 0.04 * eio(t / 3.0))
            d = ImageDraw.Draw(im, 'RGBA')
            d.text((W / 2, 225), '6 BRASILEIROS', font=F(INTB, 100), fill=PH, anchor='ma')
            if t >= ws(2): d.text((W / 2, 345), '134 CONVIDADOS', font=F(INTB, 64), fill=WHITE, anchor='ma')
            if t >= ws(8): d.text((W / 2, 425), '8 VAGAS NO TOP 8', font=F(MONOB, 48), fill=AMBER, anchor='ma')
            note(d, 'fonte: lista de convidados do WC32, magic.gg')
            return subs(im, t, SUBY)
        k = eio((t - DIVE) / (DIVE_END - DIVE)); z = 1 + k * 4.2
        im = tubo_frame(t, 'analitico', zoom=z, cx=W / 2 + (SCX - W / 2) * min(1, k * 1.5), cy=H / 2 + (SCY - H / 2) * min(1, k * 1.5))
        if k > 0.6: im = Image.blend(im, scene_arquivo(t), (k - 0.6) / 0.4)
        return im
    if t < EXIT: return subs(inside(t), t)
    if t < EXIT_END:
        k = eio((t - EXIT) / (EXIT_END - EXIT)); z = 5.2 - 4.2 * k
        im = tubo_frame(t, 'confiante', zoom=z, cx=W / 2 + (SCX - W / 2) * (1 - k), cy=H / 2 + (SCY - H / 2) * (1 - k))
        if k < 0.35: im = Image.blend(inside(t), im, k / 0.35)
        return subs(im, t, SUBY)
    if t < T_REV:
        im = tubo_frame(t, 'confiante', zoom=1.0 + .03 * eio((t - EXIT_END) / 3)); d = ImageDraw.Draw(im, 'RGBA')
        if t >= TL['PREV']:
            k = eio((t - TL['PREV']) / .18); f = F(MONOB, int(34 + 10 * (1 - k)))
            s = 'PREVISÃO REGISTRADA · PR-WC32-01'; wd = d.textlength(s, font=f) + 44
            d.rounded_rectangle((W / 2 - wd / 2, 200, W / 2 + wd / 2, 256), 10, outline=AMBER, width=4)
            d.text((W / 2, 228), s, font=f, fill=AMBER, anchor='mm')
        if t >= ws(126) - .05: d.text((W / 2, 280), 'JUND SACRIFICE NO TOP 8', font=fit(d, 'JUND SACRIFICE NO TOP 8', INTB, 68, 940), fill=WHITE, anchor='ma')
        if t >= ws(131) - .05: meter(d, 374, 3 if t >= ws(132) - .05 else 0)
        if t >= ws(135) - .05: d.text((W / 2, 438), 'conferência: segunda 16/11 · critério: Top 8 oficial (magic.gg)', font=fit(d, 'conferência: segunda 16/11 · critério: Top 8 oficial (magic.gg)', COND, 30, 940), fill=(170, 190, 195), anchor='ma')
        note(d, 'previsão = opinião do TUBO, registada antes do torneio')
        return subs(im, t, SUBY)
    if t < T_Q:
        im = tubo_frame(t, 'desconfiado' if t >= ws(143) else 'analitico', zoom=1.0); d = ImageDraw.Draw(im, 'RGBA')
        d.text((W / 2, 230), 'OS DADOS ESCOLHEM O DECK.', font=fit(d, 'OS DADOS ESCOLHEM O DECK.', INTB, 70, 940), fill=GREY, anchor='ma')
        if t >= ws(143) - .05: d.text((W / 2, 330), 'NÃO QUEM PILOTA.', font=fit(d, 'NÃO QUEM PILOTA.', INTB, 84, 940), fill=PH, anchor='ma')
        note(d, 'leitura do TUBO')
        return subs(im, t, SUBY)
    if t < T_SIG:
        im = tubo_frame(t, 'analitico', zoom=1.0); d = ImageDraw.Draw(im, 'RGBA')
        d.text((W / 2, 215), 'Qual brasileiro chega ao Top 8?', font=fit(d, 'Qual brasileiro chega ao Top 8?', INTB, 56, 960), fill=WHITE, anchor='ma')
        nomes = ['Diego Almeida', 'Marcelo Cavalcante', 'Isael Feitosa', 'Rafael Kenji Marques', 'João Quege', 'João Jorge Sales Jr.']
        for i, n in enumerate(nomes):
            if t < ws(147) + i * .12: continue
            x, y = 70 + (i % 2) * 480, 296 + (i // 2) * 62
            on = t >= ws(153) - .05
            d.rounded_rectangle((x, y, x + 460, y + 52), 26, fill=((10, 52, 30, 255) if on else (15, 23, 42, 230)), outline=EM, width=3)
            d.text((x + 230, y + 26), n, font=fit(d, n, CONDB, 32, 420), fill=(PH if on else WHITE), anchor='mm')
        if t >= ws(153) - .05: note(d, 'comente o nome')
        return subs(im, t, SUBY)
    kz = eio((t - T_SIG) / 1.2)
    im = tubo_frame(t, 'confiante', zoom=1.0 + 0.22 * kz, cx=W / 2, cy=H / 2 + (SCY + 260 - H / 2) * kz)
    k = ease((t - T_SIG) / 0.4)
    im = top_card(im, [('META EM CURTO', F(INTB, 96), WHITE), ('com TUBO · BINDER Originals', F(MONO, 34), EM)], k, 225)
    return subs(im, t, SUBY)
if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[2] == 'capa':
        im = tubo_frame(12.0, 'confiante', zoom=1.0); d = ImageDraw.Draw(im, 'RGBA')
        d.text((W / 2, 120), '6 BRASILEIROS', font=F(INTB, 116), fill=WHITE, anchor='ma')
        d.text((W / 2, 262), 'NO MUNDIAL', font=F(INTB, 96), fill=PH, anchor='ma')
        d.text((W / 2, 380), 'A PREVISÃO DO TUBO', font=F(MONOB, 54), fill=AMBER, anchor='ma')
        d.text((W / 2, 1470), 'META EM CURTO · com TUBO', font=F(MONOB, 40), fill=WHITE, anchor='ma')
        im.convert('RGB').save('EP07_CAPA.png'); sys.exit()
    if len(sys.argv) > 2 and sys.argv[2] == 'stills':
        for tt in map(float, sys.argv[3:]): frame(tt).save(f'still_{tt:05.2f}.png')
        sys.exit()
    nf = int(round(TOTAL * FPS))
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-i', 'mix_final.wav', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
                          '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', '-shortest', 'EP07_META_EM_CURTO.mp4'],
                         stdin=subprocess.PIPE)
    for i in range(nf): p.stdin.write(frame(i / FPS).convert('RGB').tobytes())
    p.stdin.close(); p.wait(); print('done', nf)
