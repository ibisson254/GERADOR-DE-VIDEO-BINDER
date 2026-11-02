# Meta em Curto EP04 · Jund em Pequim · render (derivado de ep04_render.py; cartas e lista como no ep02_render.py)
# Uso, numa pasta de trabalho com tl.json, words.json, led_env.npy e mix_final.wav (saídas de ep04_audio.py):
#   python3 ep04_render.py /caminho/do/kit             -> EP04_META_EM_CURTO.mp4
#   python3 ep04_render.py /caminho/do/kit stills 3 10 -> still_03.00.png ...
# O fecho é o ficheiro real comum/outro/outro_binder_916.mp4 (sem áudio; a trilha do episódio continua por baixo).
import json, math, subprocess, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
K = (sys.argv[1] if len(sys.argv) > 1 else '../..').rstrip('/') + '/'
W, H, FPS = 1080, 1920, 30
TL = json.load(open('tl.json')); WORDS = json.load(open('words.json'))
TEMPO, LEAD = TL['TEMPO'], TL['LEAD']
TOTAL, OUT = TL['TOTAL'], TL['OUT_START']
def vt(x): return x / TEMPO + LEAD
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
EGG0, EGG1 = ws(44), ws(54)    # easter egg «BOLSÃO» na chuva de código, ao lado da Sackville-Bagginses
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
        for k, ch in enumerate('BOLSÃO'): d.text((tcols[20]['x'], 1000 + k * 30), ch, font=fs, fill=mix_bg(PH, 90))
    return im, d
def term_finish(im):
    im = Image.composite(im, Image.new('RGB', (W, H), (0, 0, 0)), vig); im.paste(SCANL, (0, 0), SCANL); return im
def hud(d, t):
    a = led_amp(t)
    d.ellipse((80, 1676, 100, 1696), fill=(16, 185, 129, int(70 + 185 * a)))
    d.text((114, 1686), 'BINDER', font=F(MONOB, 28), fill=(16, 185, 129, 220), anchor='lm')
    d.text((W - 80, 1686), 'META EM CURTO · EP04', font=F(MONO, 26), fill=(150, 170, 175, 220), anchor='rm')
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



# ---------- EP04: dados ----------
AMBER = (255, 176, 32)
LISTA = json.load(open(K + 'oraculo/episodios/ep04_lista.json'))
CARDS = {k: Image.open(K + f'oraculo/{p}/cartas/{k}.png').convert('RGBA') for k, p in
         dict(biotech_specialist='ep02', the_sackvillebagginses='ep02', treasure='ep02', lively_dirge='ep02',
              umbral_collar_zealot='ep04', obsessive_pursuit='ep04').items()}
def cred(nome, sc, n, artista): return [f'{nome} · {sc} {n} · arte: {artista}', 'Cartas © Wizards of the Coast · imagens via Scryfall']
CRED = {k: cred(*v) for k, v in {
    'biotech_specialist': ('Biotech Specialist', 'EOE', '214', 'Alexandre Honoré'),
    'the_sackvillebagginses': ('The Sackville-Bagginses', 'HOB', '83', 'Denman Rooke'),
    'treasure': ('Treasure (ficha)', 'THOB', '12', 'Leonardo Santanna'),
    'lively_dirge': ('Lively Dirge', 'OTJ', '93', 'Warren Mahy'),
    'umbral_collar_zealot': ('Umbral Collar Zealot', 'SOC', '227', 'Dmitry Burmak'),
    'obsessive_pursuit': ('Obsessive Pursuit', 'TLA', '112', 'Ichiko Milk Tei')}.items()}
TOP8 = [('1.º', 'JUND', True), ('2.º', 'U-B-R-G FLING', False), ('3.º', 'JUND SACRIFICE', True), ('4.º', 'MONO-GREEN COMBO', False),
        ('5.º', 'DIMIR MIDRANGE', False), ('6.º', 'MONO-GREEN LANDFALL', False), ('7.º', 'IZZET COMBO', False), ('8.º', 'JUND SACRIFICE', True)]
SIL = ["......####......", ".....######.....", "....########....", "....########....", "....########....",
       ".....######.....", "......####......", "...##########...", "..############..", ".##############.",
       ".##############.", "################", "################"]
def silhueta(d, x, y, px=13, col=PH):
    for r, row in enumerate(SIL):
        for c, ch in enumerate(row):
            if ch == '#': d.rectangle((x + c * px, y + r * px, x + c * px + px - 2, y + r * px + px - 2), fill=mix_bg(col, 150))
def stamp(d, txt, col, t0, t, y):
    if t < t0: return
    k = eio((t - t0) / 0.18); f = F(MONOB, int(40 + 14 * (1 - k)))
    wd = d.textlength(txt, font=f) + 50
    d.rounded_rectangle((W / 2 - wd / 2, y - 34, W / 2 + wd / 2, y + 34), 10, outline=col, width=4)
    d.text((W / 2, y), txt, font=f, fill=col, anchor='mm')
def card_scan(im, key, t0, t, cx, y, width):
    """Carta oficial inteira (Scryfall), revelada linha a linha como num scan."""
    c = CARDS[key]; h = int(width * c.height / c.width); c = c.resize((width, h), Image.LANCZOS)
    k = ease((t - t0) / 0.45)
    if k <= 0: return y + h
    x = int(cx - width / 2); rows = int(h * k)
    if rows > 0: im.paste(c.crop((0, 0, width, rows)), (x, y), c.crop((0, 0, width, rows)))
    d = ImageDraw.Draw(im, 'RGBA')
    if k < 1:
        d.rectangle((x - 10, y + rows - 3, x + width + 10, y + rows + 3), fill=(0, 255, 65, 230))
    d.rounded_rectangle((x - 6, y - 6, x + width + 6, y + h + 6), 22, outline=(16, 185, 129, 120), width=3)
    return y + h

# ---------- DENTRO ----------
def scene_arquivo(t):
    im, d = term_base(t, 22)
    t0 = DIVE_END - 0.1
    d.text((80, 200), typed('> ARQUIVO: MAGIC SPOTLIGHT: FRACTURE', t0, t), font=fit(d, '> ARQUIVO: MAGIC SPOTLIGHT: FRACTURE', MONOB, 38, 920), fill=PH)
    d.text((80, 258), typed('  PEQUIM · STANDARD · 31/10–01/11/2026', t0 + .3, t), font=F(MONO, 30), fill=EM)
    d.line((80, 312, 1000, 312), fill=(16, 185, 129, 90), width=2)
    d.text((80, 345), '869', font=F(INTB, 120), fill=WHITE); d.text((340, 412), 'JOGADORES', font=F(MONOB, 40), fill=GREY)
    if t < ws(24) - .1:
        for s_, i_, f_, c_, y_ in [('MAGIC SPOTLIGHT', 19, F(INTB, 92), WHITE, 620), ('FRACTURE', 21, F(INTB, 120), PH, 740),
                                   ('PEQUIM', 22, F(MONOB, 72), WHITE, 930), ('STANDARD', 23, F(MONOB, 72), EM, 1040)]:
            if t >= ws(i_) - .05: d.text((W / 2, y_), s_, font=f_, fill=c_, anchor='ma')
    if t >= ws(24) - .1:
        k = eio((t - ws(24) + .1) / .35); x0 = 200
        d.rounded_rectangle((x0, 510, x0 + 680, 1330), 18, outline=EM, width=3, fill=(8, 20, 18, 255))
        d.text((x0 + 28, 536), 'FICHA DE JOGADOR', font=F(MONOB, 28), fill=GREY)
        silhueta(d, x0 + 236, 590, col=PH)
        if k >= .5:
            d.text((x0 + 340, 790), 'mo que', font=F(INTB, 96), fill=WHITE, anchor='ma')
            d.text((x0 + 340, 915), '1.º LUGAR', font=F(MONOB, 44), fill=PH, anchor='ma')
        if t >= ws(28): d.text((x0 + 340, 985), 'JUND SACRIFICE', font=F(CONDB, 56), fill=PH, anchor='ma')
        if t >= ws(30):
            kk = eio((t - ws(30)) / .3)
            d.text((x0 + 340, 1080), 'CAMPANHA', font=F(MONOB, 32), fill=GREY, anchor='ma')
            d.text((x0 + 340, 1130), '16–2', font=F(INTB, int(100 + 50 * kk)), fill=WHITE, anchor='ma')
    fontes(d, ['jogadores: PlayMTG no X (31/10/2026)', 'resultado: MTGGoldfish, dados do Melee (consulta 02/11/2026)'])
    hud(d, t); return term_finish(im)
def scene_card(t, key, t0, title, caps, width=640):
    im, d = term_base(t, 16)
    d.text((80, 200), title, font=F(MONOB, 34), fill=PH)
    d.line((80, 252, 1000, 252), fill=(16, 185, 129, 90), width=2)
    yb = card_scan(im, key, t0, t, W / 2, 280, width)
    d = ImageDraw.Draw(im, 'RGBA'); y = yb + 22
    for s, tc, col in caps:
        if t >= tc: d.text((W / 2, y), typed(s, tc, t, 55), font=fit(d, s, MONOB, 44, W - 160), fill=col, anchor='ma')
        y += 58
    fontes(d, CRED[key]); hud(d, t); return term_finish(im)
def scene_conta(t):
    im, d = term_base(t, 16)
    d.text((80, 200), '> A CONTA DO SACRIFÍCIO', font=F(MONOB, 34), fill=PH)
    d.line((80, 252, 1000, 252), fill=(16, 185, 129, 90), width=2)
    yb = card_scan(im, 'treasure', ws(54), t, W / 2, 280, 480)
    d = ImageDraw.Draw(im, 'RGBA'); y = yb + 24
    for s, tc, col in [('ARTEFATO → BIOTECH: 2 DE DANO', ws(54), EM), ('FICHA → SACKVILLE: PERDE 1', ws(55), EM)]:
        if t >= tc: d.text((W / 2, y), typed(s, tc, t, 60), font=fit(d, s, MONOB, 42, W - 160), fill=col, anchor='ma')
        y += 58
    if t >= ws(57):
        k = eio((t - ws(57)) / .3)
        d.text((W / 2, y + 2), '2 + 1 = 3', font=F(INTB, int(70 + 26 * k)), fill=PH, anchor='ma')
    if t >= ws(65): stamp(d, 'MANA → MUNIÇÃO', AMBER, ws(65), t, 1100 if False else y + 150 - 8)
    fontes(d, CRED['treasure']); hud(d, t); return term_finish(im)
def scene_lista(t):
    im, d = term_base(t, 12); L = LISTA
    d.text((80, 200), '> LISTA · MO QUE · JUND SACRIFICE', font=F(MONOB, 34), fill=PH)
    d.text((80, 252), '  60 cartas no principal · 1.º lugar · 16–2', font=F(MONO, 28), fill=EM)
    d.line((80, 306, 1000, 306), fill=(16, 185, 129, 90), width=2)
    g = list(L['principal'].items()); cols = [g[:2], g[2:]]
    verde = t >= ws(96); fh = F(MONOB, 28); i = 0; ls = 46
    for ci, col in enumerate(cols):
        x = 110 if ci == 0 else 590; y = 330
        for nome_g, cartas in col:
            if t >= ws(86) + i * .02: d.text((x - 30, y), nome_g, font=fh, fill=GREY)
            y += ls; i += 1
            for n, nome in cartas:
                if t >= ws(86) + i * .02:
                    key = verde and nome in L['chave']; s = f'{n} {nome}'
                    d.text((x, y), s, font=fit(d, s, CONDB, 34, 430 if ci == 0 else 350), fill=(PH if key else (150, 190, 170)))
                    if key: d.text((x - 32, y + 3), '▶', font=F(MONOB, 26), fill=PH)
                y += ls; i += 1
            y += 12
    fontes(d, ['lista: MTGGoldfish, dados do Melee · Hartford: Star City Games', 'a verde: as 7 não-terrenos com 4 cópias nas duas listas'], 1330 + 26)
    hud(d, t); return term_finish(im)
def scene_top8(t):
    im, d = term_base(t, 18)
    d.text((80, 200), '> TOP 8 · PEQUIM · STANDARD', font=F(MONOB, 36), fill=PH)
    d.line((80, 256, 1000, 256), fill=(16, 185, 129, 90), width=2)
    y = 292; mark = t >= ws(113)
    for i, (p, nome, j) in enumerate(TOP8):
        if t >= ws(109) + i * .1:
            on = j and mark
            if on: d.rounded_rectangle((70, y - 8, 945, y + 76), 10, fill=(10, 52, 30, 255), outline=EM, width=3)
            d.text((100, y + 34), p, font=F(MONOB, 40), fill=(PH if on else GREY), anchor='lm')
            d.text((210, y + 34), nome, font=fit(d, nome, CONDB, 48, 700), fill=(WHITE if on else (150, 170, 175)), anchor='lm')
            if i == 0 and t >= ws(122): d.text((930, y + 34), 'TROFÉU', font=F(MONOB, 34), fill=PH, anchor='rm')
        y += 96
    if mark: d.text((W / 2, 1076), '3 DE 8', font=F(INTB, 130), fill=PH, anchor='ma')
    fontes(d, ['fonte: MTGGoldfish, dados do Melee (consulta 02/11/2026)', 'nomes dos arquétipos como no MTGGoldfish'], 1270)
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
T_Q = ws(138) - 0.1; T_SIG = ws(155) - 0.15
def inside(t):
    if t < ws(34) - .1: return scene_arquivo(t)
    if t < ws(44) - .1: return scene_card(t, 'biotech_specialist', ws(34), '> O MOTOR · 1 de 2', [('ARTEFATO SACRIFICADO = 2 DE DANO', ws(41), EM)])
    if t < ws(54) - .1: return scene_card(t, 'the_sackvillebagginses', ws(44), '> O MOTOR · 2 de 2', [('FICHA SACRIFICADA = OPONENTE PERDE 1', ws(52), EM)])
    if t < ws(67) - .1: return scene_conta(t)
    if t < ws(72) - .1: return scene_card(t, 'lively_dirge', ws(67), '> A RECUPERAÇÃO', [('DEVOLVE ATÉ 2 CRIATURAS · VM TOTAL ≤ 4', ws(69), EM)])
    if t < ws(78) - .1: return scene_card(t, 'umbral_collar_zealot', ws(72), '> O MOTOR PRECISA DE SAÍDA', [('SACRIFICA CRIATURA OU ARTEFATO', ws(75), EM)])
    if t < ws(86) - .1: return scene_card(t, 'obsessive_pursuit', ws(78), '> PRESSÃO NO ATAQUE', [('X = PERMANENTES SACRIFICADOS NO TURNO', ws(81), EM)])
    if t < ws(109) - .1: return scene_lista(t)
    return scene_top8(t)
SUBY = 1530
def note(d, s):
    f = F(COND, 34); wd = d.textlength(s, font=f)
    d.rounded_rectangle((W / 2 - wd / 2 - 16, 1418, W / 2 + wd / 2 + 16, 1468), 8, fill=(5, 10, 16, 215))
    d.text((W / 2, 1443), s, font=f, fill=(170, 190, 195), anchor='mm')
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
            d.text((W / 2, 225), '869 JOGADORES', font=F(INTB, 96), fill=WHITE, anchor='ma')
            if t >= ws(6): d.text((W / 2, 335), '1 CAMPEÃO', font=F(INTB, 72), fill=PH, anchor='ma')
            note(d, 'fonte: PlayMTG no X · 31/10/2026')
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
    if t < T_Q:
        im = tubo_frame(t, 'confiante', zoom=1.0 + .03 * eio((t - EXIT_END) / 3))
        d = ImageDraw.Draw(im, 'RGBA')
        if t >= ws(125): d.text((W / 2, 225), 'NÃO A MAIOR MESA.', font=fit(d, 'NÃO A MAIOR MESA.', INTB, 76, 800), fill=GREY, anchor='ma')
        if t >= ws(132): d.text((W / 2, 320), 'O QUE SACRIFICAR.', font=fit(d, 'O QUE SACRIFICAR.', INTB, 84, 800), fill=PH, anchor='ma')
        note(d, 'leitura do TUBO, não regra do jogo')
        return subs(im, t, SUBY)
    if t < T_SIG:
        im = tubo_frame(t, 'analitico', zoom=1.0); d = ImageDraw.Draw(im, 'RGBA')
        im = top_card(im, [('Qual peça você remove primeiro?', F(INTB, 52), WHITE)], 1.0, 225)
        d = ImageDraw.Draw(im, 'RGBA')
        d.text((W / 2, 292), 'GRAU DE CERTEZA', font=F(MONOB, 28), fill=GREY, anchor='ma')
        for i, (lab, n, val) in enumerate([('TEXTO DAS CARTAS', 5, 'ALTO'), ('PILOTAGEM (SEM VOD)', 1, 'BAIXO')]):
            y = 330 + i * 54
            d.text((90, y + 20), lab, font=fit(d, lab, CONDB, 30, 315), fill=WHITE, anchor='lm')
            for s in range(5):
                x = 420 + s * 66
                d.rounded_rectangle((x, y, x + 56, y + 40), 7, fill=(EM if s < n else None), outline=EM, width=3)
            d.text((930, y + 20), val, font=F(MONOB, 30), fill=EM, anchor='rm')
        chips = [('A · BIOTECH', ws(146)), ('B · SACKVILLE', ws(149)), ('C · ZEALOT', ws(151))]
        f = F(MONOB, 30); y = 1385
        wds = [d.textlength(s, font=f) + 44 for s, _ in chips]; x = (W - sum(wds) - 2 * 16) / 2
        for (s, tt), wd in zip(chips, wds):
            on = t >= tt
            d.rounded_rectangle((x, y, x + wd, y + 68), 34, fill=(EM if on else (15, 23, 42, 230)), outline=EM, width=3)
            d.text((x + wd / 2, y + 34), s, font=f, fill=(BG if on else EM), anchor='mm'); x += wd + 16
        return subs(im, t, SUBY)
    kz = eio((t - T_SIG) / 1.2)
    im = tubo_frame(t, 'confiante', zoom=1.0 + 0.22 * kz, cx=W / 2, cy=H / 2 + (SCY + 260 - H / 2) * kz)
    k = ease((t - T_SIG) / 0.4)
    im = top_card(im, [('META EM CURTO', F(INTB, 96), WHITE), ('com TUBO · BINDER Originals', F(MONO, 34), EM)], k, 225)
    return subs(im, t, SUBY)
if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[2] == 'capa':
        im = tubo_frame(12.0, 'confiante', zoom=1.0); d = ImageDraw.Draw(im, 'RGBA')
        d.text((W / 2, 110), 'JUND SACRIFICE', font=F(INTB, 112), fill=WHITE, anchor='ma')
        d.text((W / 2, 250), '3 NO TOP 8', font=F(INTB, 96), fill=PH, anchor='ma')
        d.text((W / 2, 360), '1 TROFÉU · PEQUIM', font=F(MONOB, 54), fill=EM, anchor='ma')
        d.text((W / 2, 1470), 'META EM CURTO · com TUBO', font=F(MONOB, 40), fill=WHITE, anchor='ma')
        im.convert('RGB').save('EP04_CAPA.png'); sys.exit()
    if len(sys.argv) > 2 and sys.argv[2] == 'stills':
        for tt in map(float, sys.argv[3:]): frame(tt).save(f'still_{tt:05.2f}.png')
        sys.exit()
    nf = int(round(TOTAL * FPS))
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-i', 'mix_final.wav', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
                          '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', '-shortest', 'EP04_META_EM_CURTO.mp4'],
                         stdin=subprocess.PIPE)
    for i in range(nf): p.stdin.write(frame(i / FPS).convert('RGB').tobytes())
    p.stdin.close(); p.wait(); print('done', nf)
