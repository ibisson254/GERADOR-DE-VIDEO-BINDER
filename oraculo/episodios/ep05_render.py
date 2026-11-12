# Meta em Curto EP05 · Star Trek, engenharia de um deck · render (derivado de ep04_render.py)
# Uso, numa pasta de trabalho com tl.json, words.json, led_env.npy e mix_final.wav (saídas de ep05_audio.py):
#   python3 ep05_render.py /caminho/do/kit             -> EP05_META_EM_CURTO.mp4
#   python3 ep05_render.py /caminho/do/kit stills 3 10 -> still_03.00.png ...
#   python3 ep05_render.py /caminho/do/kit capa        -> EP05_CAPA.png
# Os gráficos leem oraculo/ep05/resultados/*.json e dados/*.csv: o que está no ecrã é o que saiu das análises.
# O fecho é o ficheiro real comum/outro/outro_binder_916.mp4 (sem áudio; a trilha do episódio continua por baixo).
import csv, json, math, subprocess, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
K = (sys.argv[1] if len(sys.argv) > 1 else '../..').rstrip('/') + '/'
W, H, FPS = 1080, 1920, 30
TL = json.load(open('tl.json')); DW = json.load(open('words.json')); FAL = DW['falada']; TOK = DW['tokens']
TEMPO, LEAD = TL['TEMPO'], TL['LEAD']
TOTAL, OUT = TL['TOTAL'], TL['OUT_START']
def vt(x):
    y = x / TEMPO + LEAD
    for (i, g), c in zip(TL['PAUSAS'], TL['CORTES']):
        if x / TEMPO >= c: y += g
    return y
for w in FAL: w['vs'] = vt(w['s']); w['ve'] = vt(w['e'])
for w in TOK: w['vs'] = vt(w['s']); w['ve'] = vt(w['e'])
def ws(i): return FAL[i]['vs']
def we(i): return FAL[i]['ve']
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
EGG0, EGG1 = ws(13), ws(28)    # easter egg «1701-A» na chuva de código, ao lado da Enterprise-A
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
        for k, ch in enumerate('1701-A'): d.text((tcols[21]['x'], 560 + k * 30), ch, font=fs, fill=mix_bg(PH, 110))
    return im, d
def term_finish(im):
    im = Image.composite(im, Image.new('RGB', (W, H), (0, 0, 0)), vig); im.paste(SCANL, (0, 0), SCANL); return im
def hud(d, t):
    a = led_amp(t)
    d.ellipse((80, 1676, 100, 1696), fill=(16, 185, 129, int(70 + 185 * a)))
    d.text((114, 1686), 'BINDER', font=F(MONOB, 28), fill=(16, 185, 129, 220), anchor='lm')
    d.text((W - 80, 1686), 'META EM CURTO · EP05', font=F(MONO, 26), fill=(150, 170, 175, 220), anchor='rm')
def fontes(d, linhas, y=None):
    """Linha(s) de fonte, ≥ 24 px de altura de letra (corrige o EP01)."""
    y = y if y is not None else 1428 - (len(linhas) - 1) * 44
    for i, s in enumerate(linhas):
        f = F(COND, 34)
        if d.textlength(s, font=f) > 860: print('FONTE LONGA:', s, d.textlength(s, font=f))
        d.text((80, y + i * 44), s, font=f, fill=(150, 170, 175, 235))

# ---------- legendas palavra a palavra (cartões com número valem um só token) ----------
def chunks():
    out = []; cur = []
    for w in TOK:
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
            if tot > 860:
                f = fit(d, ' '.join(txt), MONOB, 50, 860); sp = d.textlength(' ', font=f)
                tot = sum(d.textlength(s, font=f) for s in txt) + sp * (len(txt) - 1)
            x = 510 - tot / 2
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




# ---------- EP05: dados (vêm das análises, não do código) ----------
AMBER = (255, 176, 32); SD = K + 'oraculo/ep05/'
PR = json.load(open(SD + 'resultados/prob.json')); GR = json.load(open(SD + 'resultados/grafo.json')); MX = json.load(open(SD + 'resultados/matriz.json'))
TRO = list(csv.DictReader(open(SD + 'dados/trofeus_sealed_untapped.csv')))
CARTA = Image.open(SD + 'cartas/uss_enterprise_a.png').convert('RGBA')
AB = PR['abertura']; SY = PR['sinergia']['T5_jogando']; SYD = PR['sinergia']['T5_comprando']
P_AB = AB['mitica_especifica_6']; P_T5 = SY['bomba_1_copia']; JOGOS = round(1 / (P_AB * P_T5 / 1e4))
assert JOGOS == 96
def br(v, c=1): return f'{v:.{c}f}'.replace('.', ',')
def head(d, a, b=None, t=None, t0=0):
    s = a if t is None else typed(a, t0, t)
    d.text((80, 226), s, font=fit(d, a, MONOB, 36, 860), fill=PH)
    if b: d.text((80, 276), b, font=fit(d, b, MONO, 28, 860), fill=EM)
    d.line((80, 322, 940, 322), fill=(16, 185, 129, 90), width=2)
def stamp(d, txt, col, t0, t, y, x=None):
    if t < t0: return
    x = W / 2 if x is None else x
    k = eio((t - t0) / 0.18); f = F(MONOB, int(40 + 14 * (1 - k)))
    wd = d.textlength(txt, font=f) + 50
    d.rounded_rectangle((x - wd / 2, y - 36, x + wd / 2, y + 36), 10, outline=col, width=4, fill=(5, 10, 16, 235))
    d.text((x, y), txt, font=f, fill=col, anchor='mm')
def card_scan(im, t0, t, cx, y, width):
    c = CARTA; h = int(width * c.height / c.width); c = c.resize((width, h), Image.LANCZOS)
    k = ease((t - t0) / 0.45)
    if k <= 0: return y + h
    x = int(cx - width / 2); rows = int(h * k)
    if rows > 0: im.paste(c.crop((0, 0, width, rows)), (x, y), c.crop((0, 0, width, rows)))
    d = ImageDraw.Draw(im, 'RGBA')
    if k < 1: d.rectangle((x - 10, y + rows - 3, x + width + 10, y + rows + 3), fill=(0, 255, 65, 230))
    d.rounded_rectangle((x - 6, y - 6, x + width + 6, y + h + 6), 22, outline=(16, 185, 129, 120), width=3)
    return y + h
CRED_C = ['U.S.S. Enterprise-A, Free Spirit · TRK 43', 'arte: Evan Shipard', 'Cartas © Wizards of the Coast · imagens via Scryfall', 'Star Trek © CBS · conteúdo de fã não oficial']
def scene_abrir(t):
    """A mítica específica: carta inteira, depois a conta e a grelha de 96 jogos."""
    im, d = term_base(t, 16)
    if t < ws(28) - .1:
        head(d, '> MÍTICA ESPECÍFICA · 1 DE 25', '6 boosters · sem a promo · colação oficial')
        yb = card_scan(im, DIVE_END - .15, t, W / 2, 346, 640); d = ImageDraw.Draw(im, 'RGBA')
        fontes(d, CRED_C); hud(d, t); return term_finish(im)
    head(d, '> ABRIR NÃO É JOGAR', 'até T5 · jogando primeiro · 40 cartas')
    d.text((80, 352), f'{br(P_AB)}%', font=F(INTB, 118), fill=WHITE); d.text((80, 486), 'ABRIR EM 6 BOOSTERS', font=F(MONOB, 30), fill=GREY)
    d.text((540, 380), '×', font=F(INTB, 86), fill=GREY, anchor='ma')
    d.text((620, 352), f'{br(P_T5)}%', font=F(INTB, 118), fill=WHITE); d.text((620, 486), 'VER ATÉ T5', font=F(MONOB, 30), fill=GREY)
    # grelha 12×8 = 96 jogos, um aceso
    x0, y0, c, g = 104, 556, 56, 18; ini = ws(31) - .05
    for i in range(96):
        r, q = divmod(i, 12); xx = x0 + q * (c + g); yy = y0 + r * (c + g)
        on = t >= ini + i * .004
        if on:
            lit = i == 51 and t >= ws(34)
            d.rounded_rectangle((xx, yy, xx + c, yy + c), 8, fill=(PH if lit else (14, 34, 30, 255)), outline=(PH if lit else (40, 90, 74, 255)), width=2)
    if t >= ws(34): d.text((W / 2, 1160), f'1 JOGO EM {JOGOS}', font=F(INTB, 104), fill=PH, anchor='ma')
    fontes(d, ['colação oficial (Wizards) · 6 boosters · sem a promo', '3,77% × 11/40 = 1,04%', 'premissa: taxa igual entre as 25 míticas'])
    hud(d, t); return term_finish(im)
def scene_arquivo(t):
    im, d = term_base(t, 22); t0 = ws(46) - .1
    head(d, '> ARQUIVO: MAGIC | STAR TREK (TRK)', 'PRÉ-RELEASE 6–12/11/2026 · SEALED · 6 BOOSTERS', t, t0)
    linhas = [('WIN RATE POR PAR', '---'), ('LISTAS DE TROFÉU', '0'), ('TORNEIOS DE SEALED', '0'), ('PARTIDAS REGISTRADAS', '0')]
    for i, (a, b) in enumerate(linhas):
        tc = ws(47) + i * .22; y = 372 + i * 92
        if t >= tc:
            d.text((90, y), a, font=F(MONOB, 40), fill=WHITE); d.text((930, y), b, font=F(MONOB, 48), fill=RED if t >= ws(51) else GREY, anchor='ra')
            d.line((90, y + 66, 930, y + 66), fill=(16, 185, 129, 50), width=2)
    stamp(d, 'SEM DADOS', RED, ws(51), t, 838)
    if t >= ws(54):
        d.text((W / 2, 960), 'DADO QUE NÃO EXISTE,', font=fit(d, 'DADO QUE NÃO EXISTE,', INTB, 74, 860), fill=GREY, anchor='ma')
    if t >= ws(58):
        d.text((W / 2, 1050), 'EU NÃO INVENTO.', font=fit(d, 'EU NÃO INVENTO.', INTB, 92, 860), fill=PH, anchor='ma')
    if t >= ws(61): d.text((W / 2, 1190), '→ SETS ANTERIORES: MÉTODO, NÃO PROVA', font=fit(d, '→ SETS ANTERIORES: MÉTODO, NÃO PROVA', MONOB, 36, 860), fill=AMBER, anchor='ma')
    fontes(d, ['TRK no Arena: 10/11/2026 · nas lojas: 13/11/2026', 'MTGMeta: sem jogos de TRK · consulta de 05/11/2026'])
    hud(d, t); return term_finish(im)
CORES_N = dict(WU='WU', UW='WU')
def trof_ord():
    dois = [x for x in TRO if len(x['cores']) == 2]; tres = [x for x in TRO if len(x['cores']) == 3]
    return sorted(dois, key=lambda x: (x['recorde'], x['cores'])) + sorted(tres, key=lambda x: (x['recorde'], x['cores']))
TR = trof_ord(); T2 = GR['trofeus']
def scene_trofeus(t):
    im, d = term_base(t, 12)
    head(d, f"> {T2['n']} LISTAS DE TROFÉU · SEALED", f"{T2['sets']} coleções · Arena · 7–0, 7–1 e 7–2")
    x0, y0, c, g = 80, 346, 73, 13; ini = ws(65)
    for i, x in enumerate(TR):
        r, q = divmod(i, 10); xx = x0 + q * (c + g); yy = y0 + r * (c + g)
        if t < ini + i * .012: continue
        tres = len(x['cores']) == 3; top = x['recorde'] in ('7-0', '7-1')
        cor_c = (AMBER if tres else EM) if t >= ws(75) else (60, 110, 96)
        cheio = t >= ws(81) and top
        d.rounded_rectangle((xx, yy, xx + c, yy + c), 9, fill=(cor_c if cheio else (12, 26, 26, 255)), outline=cor_c, width=3)
        d.text((xx + c / 2, yy + c / 2), x['cores'], font=F(MONOB, 29 if not tres else 26), fill=(BG if cheio else (190, 215, 205)), anchor='mm')
    y = 980
    if t >= ws(75):
        d.text((80, y), f"2 CORES", font=F(MONOB, 40), fill=EM); d.text((280, y), f"{T2['duas_cores']}", font=F(INTB, 50), fill=WHITE)
        if t >= ws(81): d.text((936, y + 6), f"{T2['duas_top']} com até 1 derrota", font=fit(d, 'xx com até 1 derrota', CONDB, 40, 500), fill=WHITE, anchor='ra')
    y += 74
    if t >= ws(81):
        d.text((80, y), f"3 CORES", font=F(MONOB, 40), fill=AMBER); d.text((280, y), f"{T2['tres_cores']}", font=F(INTB, 50), fill=WHITE)
        d.text((936, y + 6), f"{T2['tres_top']} com até 1 derrota", font=fit(d, 'xx com até 1 derrota', CONDB, 40, 500), fill=AMBER, anchor='ra')
    y += 74
    if t >= ws(75): d.text((80, y), f"17 TERRENOS: {T2['t17']} · 16 TERRENOS: {T2['t16']} · 18+: 0", font=fit(d, 'x' * 38, MONOB, 34, 860), fill=GREY)
    stamp(d, 'PADRÃO, NÃO CAUSA', AMBER, ws(92), t, 1248)
    fontes(d, ['Untapped.gg · Sealed do Arena · consulta 05/11/2026', 'SOS FIN EOE ECL DFT TMT BLB FDN DSK · 7–8 por set', 'só vencedores · sem grupo de controlo'])
    hud(d, t); return term_finish(im)
DRAFT = [('Azorius', 1), ('Dimir', 2), ('Gruul', 3), ('Izzet', 4), ('Golgari', 5), ('Selesnya', 6), ('Orzhov', 7), ('Rakdos', 8), ('Boros', 9), ('Simic', 10)]
SEALED = dict(Azorius=1, Golgari=2, Dimir=3, Izzet=4, Boros=5, Simic=6, Orzhov=7, Selesnya=8, Gruul=9, Rakdos=10)
def scene_draft(t):
    im, d = term_base(t, 14)
    head(d, '> MUNDIAL NÃO É PRÉ-RELEASE', 'Worlds 32 · Atlanta · 13–15/11 · Star Trek Draft + Standard')
    if t < ws(105) - .1:
        d.text((W / 2, 520), 'DRAFT', font=F(INTB, 150), fill=WHITE, anchor='ma')
        if t >= ws(102): d.text((W / 2, 700), '≠', font=F(INTB, 130), fill=AMBER, anchor='ma')
        if t >= ws(102): d.text((W / 2, 870), 'SEALED', font=F(INTB, 150), fill=PH, anchor='ma')
    else:
        k = ease((t - ws(105) + .1) / .4)
        d.text((80, 342), 'REALITY FRACTURE · RANKING POR WIN RATE', font=fit(d, 'REALITY FRACTURE · RANKING POR WIN RATE', MONOB, 32, 860), fill=WHITE)
        xa, xb, y0, st = 400, 690, 420, 84
        d.text((xa, 384), 'DRAFT', font=F(MONOB, 30), fill=GREY, anchor='ra'); d.text((xb, 384), 'SEALED', font=F(MONOB, 30), fill=GREY)
        foco = 'Gruul'
        for nome, ra in DRAFT:
            rb = SEALED[nome]; ya = y0 + (ra - 1) * st + 20; yb = y0 + (rb - 1) * st + 20
            mark = nome == foco and t >= ws(109)
            col = AMBER if mark else (46, 96, 84)
            d.line((xa + 12, ya, xa + 12 + (xb - xa - 24) * k, ya + (yb - ya) * k), fill=col, width=7 if mark else 3)
            c2 = AMBER if mark else (150, 175, 170)
            d.text((xa, ya), f'{ra}. {nome}', font=F(CONDB, 38 if mark else 34), fill=c2, anchor='rm')
            lab = f'{rb}. {nome}' if nome not in ('Izzet', 'Boros', 'Simic') else f'4–6. {nome}'
            if k > .9: d.text((xb, yb), lab, font=F(CONDB, 38 if mark else 34), fill=c2, anchor='lm')
    fontes(d, ['Draft: 17Lands via Portent Lab · Sealed: MTGMeta', 'compilado em note.com, 18/10/2026', 'Sealed: 2.226 a 5.660 jogos por par'])
    hud(d, t); return term_finish(im)
def barra(d, y, rot, val, cor, k, sub=None, h=82, x0=80, wmax=800, txt=None):
    d.text((x0, y), rot, font=fit(d, rot, CONDB, 38, 860), fill=WHITE)
    yb = y + 50
    d.rounded_rectangle((x0, yb, x0 + wmax, yb + h), 8, fill=(12, 26, 26, 255), outline=(30, 70, 60, 255), width=2)
    wd = wmax * val / 100 * k
    if wd > 6: d.rounded_rectangle((x0, yb, x0 + wd, yb + h), 8, fill=cor)
    s = txt or f'{br(val)}%'
    xt = x0 + wd + 14
    if xt + d.textlength(s, font=F(INTB, 54)) > x0 + wmax + 70: xt = x0 + wd - 14 - d.textlength(s, font=F(INTB, 54)); cor_t = BG
    else: cor_t = WHITE
    d.text((xt, yb + h / 2), s, font=F(INTB, 54), fill=cor_t, anchor='lm')
def scene_conta(t):
    im, d = term_base(t, 14)
    head(d, '> A CONTA', '40 cartas · até T5 · jogando primeiro · sem mulligan')
    v1, v7 = SY['bomba_1_copia'], SY['>=1_de_7']; p1, p4 = SY['unico_payoff_8_peças'], SY['4_payoffs_8_peças']
    barra(d, 352, '1 CARTA ÚNICA', v1, (90, 110, 110), 1.0)
    if t >= ws(121): barra(d, 520, '7 CARTAS COM A MESMA FUNÇÃO', v7, PH, eio((t - ws(127)) / .5))
    if t >= ws(136):
        d.text((80, 700), 'MOTOR = 1+ PAYOFF E 2+ PEÇAS', font=F(MONOB, 34), fill=AMBER); d.line((80, 750, 940, 750), fill=(255, 176, 32, 110), width=2)
        barra(d, 772, '1 PAYOFF + 8 PEÇAS', p1, AMBER, eio((t - ws(141)) / .4))
    if t >= ws(146): barra(d, 940, '4 PAYOFFS + 8 PEÇAS', p4, EM, eio((t - ws(146)) / .4))
    fontes(d, ['cálculo exato, conferido com 2 milhões de simulações', f"comprando primeiro: {br(SYD['bomba_1_copia'])} · {br(SYD['>=1_de_7'])} · {br(SYD['unico_payoff_8_peças'])} · {br(SYD['4_payoffs_8_peças'])}"])
    hud(d, t); return term_finish(im)
# grafo: posições à mão para ler em 9:16; pesos vêm de resultados/grafo.json
NOS = dict(dilemma=(205, 476, 'DILEMMA'), cemiterio=(470, 476, 'CEMITÉRIO'), borg=(340, 636, 'BORG'), klingon=(790, 476, 'KLINGON'), poder8=(750, 636, 'PODER 8'), beam=(790, 796, 'BEAM ME UP'),
           marcadores=(225, 910, 'MARCADORES'), nave=(370, 1044, 'SPACECRAFT'), landfall=(505, 910, 'LANDFALL'), federation=(190, 1186, 'FEDERATION'), snw=(725, 1186, 'STRANGE NEW WORLDS'))
ROT = {v['rotulo']: k for k, v in GR['mecanismos'].items()}
LIG = [(ROT[l['a']], ROT[l['b']], l['cartas']) for l in GR['ligacoes']]
FAM = [(('dilemma', 'cemiterio', 'borg'), EM, 'VALOR', (72, 396, 610, 700)), (('klingon', 'poder8', 'beam'), AMBER, 'CORPOS', (632, 396, 938, 860)), (('marcadores', 'nave', 'landfall'), (120, 200, 255), 'MESA', (72, 830, 640, 1104))]
assert sorted(sorted(ROT[x] for x in c) for c in GR['clusters']) == sorted(sorted(f[0]) for f in FAM)  # famílias = comunidades calculadas
def no(d, k, col, bg=(10, 22, 24, 255), on=True):
    x, y, s = NOS[k]; f = fit(d, s, CONDB, 36, 340); wd = d.textlength(s, font=f) + 34
    d.rounded_rectangle((x - wd / 2, y - 32, x + wd / 2, y + 32), 12, fill=bg, outline=col, width=3)
    d.text((x, y), s, font=f, fill=WHITE if on else GREY, anchor='mm')
def scene_grafo(t):
    im, d = term_base(t, 10)
    head(d, '> GRAFO DAS 306 CARTAS', 'ligação = cartas jogáveis nos dois mecanismos')
    fam = t >= ws(159)
    if fam:
        for ks, col, nome, bx in FAM:
            a = eio((t - ws(159)) / .35)
            d.rounded_rectangle(bx, 22, outline=col + (int(170 * a),), width=3, fill=col + (int(16 * a),))
            d.text((bx[0] + 18, bx[1] + 8), nome, font=F(MONOB, 28), fill=col)
    k_ = ease((t - ws(157)) / .5)
    foco = t >= ws(161)
    for a, b, n in LIG:
        if a not in NOS or b not in NOS: continue
        x0, y0, _ = NOS[a]; x1, y1, _ = NOS[b]
        par = {a, b} == {'dilemma', 'cemiterio'}
        wdt = int(2 + n * 1.2); col = (0, 255, 65, 255) if par and foco else (16, 185, 129, int((70 + n * 16) * (0.35 if foco else 1)))
        if k_ > 0: d.line((x0, y0, x0 + (x1 - x0) * k_, y0 + (y1 - y0) * k_), fill=col, width=wdt)
    for k in NOS:
        if k in ('federation', 'snw'): continue
        if t >= ws(151) + .03 * list(NOS).index(k): no(d, k, EM)
    iso = t >= ws(168)
    if t >= ws(151) + .4:
        no(d, 'federation', AMBER if iso else (60, 90, 80), on=iso); no(d, 'snw', AMBER if iso else (60, 90, 80), on=iso)
    if foco:
        x = (NOS['dilemma'][0] + NOS['cemiterio'][0]) / 2 - 90; d.rounded_rectangle((x - 118, 524, x + 118, 574), 10, fill=PH); d.text((x, 549), '10 CARTAS', font=F(MONOB, 32), fill=BG, anchor='mm')
    if iso: d.text((432, 1170), '0 LIGAÇÕES', font=F(MONOB, 28), fill=AMBER, anchor='ma')
    fontes(d, ['Oracle via Scryfall · notas: MTG Arena Zone, 11/2026', 'ligação: comuns e incomuns com nota ≥ 2,0', 'Não-criaturas fica fora: 108 das 306 cartas'])
    hud(d, t); return term_finish(im)
ROT_P = dict(BR='RAKDOS · KLINGON', RG='GRUUL · LANDFALL', BG='GOLGARI · CEMITÉRIO', WU='AZORIUS · SPACECRAFT', GW='SELESNYA · MARCADORES', UR='IZZET · NÃO-CRIATURA',
             GU='SIMIC · NOVOS MUNDOS*', WB='ORZHOV · BORG', RW='BOROS · PODER 8*', UB='DIMIR · DILEMMA')
def scene_pools(t):
    im, d = term_base(t, 10)
    rem = t >= ws(199) - .1
    if not rem:
        head(d, '> 40.000 POOLS SIMULADOS', 'motor ligado até T5 · deck-modelo · jogando primeiro')
        L = sorted(MX, key=lambda m: -m['motor_T5']); y = 340
        foco = {'BR': ws(189), 'WB': ws(193), 'UB': ws(197)}
        for i, m in enumerate(L):
            if t < ws(175) + i * .06: y += 98; continue
            on = t >= foco.get(m['par'], 1e9); col = PH if on and m['par'] == 'BR' else AMBER if on else (60, 110, 96)
            k = eio((t - ws(183)) / .6) if t >= ws(183) else 0
            d.text((80, y), ROT_P[m['par']], font=fit(d, ROT_P[m['par']], CONDB, 34, 480), fill=WHITE if on else (170, 195, 190))
            yb = y + 44; wd = 720 * m['motor_T5'] / 100 * k
            d.rounded_rectangle((80, yb, 800, yb + 34), 6, fill=(12, 26, 26, 255))
            if wd > 4: d.rounded_rectangle((80, yb, 80 + wd, yb + 34), 6, fill=col)
            if k > .95: d.text((930, yb + 17), f"{m['motor_T5']:.0f}%", font=F(INTB, 44), fill=WHITE if on else (170, 195, 190), anchor='rm')
            y += 98
        fontes(d, ['colação Wizards + Oracle · notas MTG Arena Zone', '* teto sem oponente · não é win rate'])
    else:
        head(d, '> REMOÇÕES ABERTAS POR POOL', 'a Wizards pede pelo menos 5 nas duas cores')
        L = sorted(MX, key=lambda m: -m['remocao_pool']); y = 346
        xl = 340; esc = 520 / 6.0
        for i, m in enumerate(L):
            nome = m['nome'].upper(); on = (m['par'] == 'BR' and t >= ws(204)) or (m['par'] == 'GU' and t >= ws(208))
            col = PH if on and m['par'] == 'BR' else AMBER if on else (60, 110, 96)
            d.text((80, y + 26), nome, font=F(CONDB, 40), fill=WHITE if on else (170, 195, 190), anchor='lm')
            k = eio((t - ws(199)) / .5); wd = m['remocao_pool'] * esc * k
            d.rounded_rectangle((xl, y + 4, xl + 520, y + 48), 6, fill=(12, 26, 26, 255))
            if wd > 4: d.rounded_rectangle((xl, y + 4, xl + wd, y + 48), 6, fill=col)
            y += 84
        xr = xl + 5 * esc
        d.line((xr, 336, xr, y - 26), fill=(255, 255, 255, 200), width=3); d.text((xr, y - 18), 'PEDIDO: 5', font=F(MONOB, 28), fill=WHITE, anchor='ma')
        k = eio((t - ws(199)) / .5)
        if k > .95:
            for i, m in enumerate(L):
                wd = m['remocao_pool'] * esc; yy = 346 + i * 84 + 26; s_ = br(m['remocao_pool']); xt = xl + wd + 12
                tw = d.textlength(s_, font=F(INTB, 38)); d.rounded_rectangle((xt - 4, yy - 22, xt + tw + 4, yy + 22), 6, fill=(5, 10, 16, 255))
                d.text((xt, yy), s_, font=F(INTB, 38), fill=WHITE, anchor='lm')
        fontes(d, ['guia de pré-release da Wizards, 30/10/2026', 'média por pool · remoção marcada à mão no Oracle'])
    stamp(d, 'MODELO, NÃO JOGO', AMBER, ws(211), t, 1262)
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
T_PREV = ws(236) - .12; T_Q = ws(254) - .12; T_SIG = ws(270) - .12
def inside(t):
    if t < ws(46) - .1: return scene_abrir(t)
    if t < ws(65) - .08: return scene_arquivo(t)
    if t < ws(97) - .08: return scene_trofeus(t)
    if t < ws(118) - .08: return scene_draft(t)
    if t < ws(151) - .08: return scene_conta(t)
    if t < ws(175) - .08: return scene_grafo(t)
    return scene_pools(t)
SUBY = 1530
def note(d, s):
    f = fit(d, s, COND, 34, 820); wd = d.textlength(s, font=f)
    d.rounded_rectangle((510 - wd / 2 - 16, 1418, 510 + wd / 2 + 16, 1468), 8, fill=(5, 10, 16, 215))
    d.text((510, 1443), s, font=f, fill=(170, 190, 195), anchor='mm')
def medidor(d, y, lab, n, val):
    d.text((90, y + 20), lab, font=fit(d, lab, CONDB, 30, 315), fill=WHITE, anchor='lm')
    for s in range(5):
        x = 420 + s * 66
        d.rounded_rectangle((x, y, x + 56, y + 40), 7, fill=(EM if s < n else None), outline=EM, width=3)
    d.text((930, y + 20), val, font=F(MONOB, 30), fill=EM, anchor='rm')
def frame(t):
    if t >= OUT: return outro(t - OUT)
    if t >= OUT - 0.2:
        a = (t - (OUT - 0.2)) / 0.2; return Image.blend(frame_main(OUT - 0.21), outro(0), a)
    return frame_main(t)
def frame_main(t):
    if t < DIVE_END:
        if t < DIVE:
            im = tubo_frame(t, 'desconfiado' if t < ws(6) else 'confiante', zoom=1.0 + 0.04 * eio(t / 3.0))
            d = ImageDraw.Draw(im, 'RGBA')
            d.text((W / 2, 226), 'ENTERPRISE-A', font=F(INTB, 88), fill=WHITE, anchor='ma')
            if t >= ws(6): d.text((W / 2, 322), f'{br(P_AB)}% DE ABRIR', font=F(INTB, 84), fill=PH, anchor='ma')
            note(d, 'colação oficial · 6 boosters · sem a promo')
            return subs(im, t, SUBY)
        k = eio((t - DIVE) / (DIVE_END - DIVE)); z = 1 + k * 4.2
        im = tubo_frame(t, 'analitico', zoom=z, cx=W / 2 + (SCX - W / 2) * min(1, k * 1.5), cy=H / 2 + (SCY - H / 2) * min(1, k * 1.5))
        if k > 0.6: im = Image.blend(im, scene_abrir(t), (k - 0.6) / 0.4)
        return im
    if t < EXIT: return subs(inside(t), t)
    if t < EXIT_END:
        k = eio((t - EXIT) / (EXIT_END - EXIT)); z = 5.2 - 4.2 * k
        im = tubo_frame(t, 'confiante', zoom=z, cx=W / 2 + (SCX - W / 2) * (1 - k), cy=H / 2 + (SCY - H / 2) * (1 - k))
        if k < 0.35: im = Image.blend(inside(t), im, k / 0.35)
        return subs(im, t, SUBY)
    if t < T_PREV:
        im = tubo_frame(t, 'confiante', zoom=1.0 + .03 * eio((t - EXIT_END) / 3))
        d = ImageDraw.Draw(im, 'RGBA')
        if t >= ws(216): d.text((W / 2, 232), 'NÃO A MAIOR BOMBA.', font=fit(d, 'NÃO A MAIOR BOMBA.', INTB, 76, 820), fill=GREY, anchor='ma')
        if t >= ws(226): d.text((W / 2, 330), 'O PRÓPRIO PLANO.', font=fit(d, 'O PRÓPRIO PLANO.', INTB, 90, 820), fill=PH, anchor='ma')
        note(d, 'leitura do TUBO, não regra do jogo')
        return subs(im, t, SUBY)
    if t < T_Q:
        im = tubo_frame(t, 'analitico', zoom=1.0); d = ImageDraw.Draw(im, 'RGBA')
        d.text((W / 2, 232), 'PREVISÃO REGISTRADA', font=fit(d, 'PREVISÃO REGISTRADA', MONOB, 48, 820), fill=AMBER, anchor='ma')
        if t >= ws(238): d.text((W / 2, 300), 'RAKDOS · TOP 3 DO SEALED', font=fit(d, 'RAKDOS · TOP 3 DO SEALED', INTB, 66, 830), fill=WHITE, anchor='ma')
        if t >= ws(244): d.text((W / 2, 388), '17Lands · até 01/12/2026', font=F(MONO, 34), fill=EM, anchor='ma')
        if t >= ws(248):
            d.rounded_rectangle((70, 1352, 945, 1466), 14, fill=(15, 23, 42, 238), outline=EM, width=2)
            d.text((508, 1362), 'GRAU DE CERTEZA · OPINIÃO DO TUBO', font=F(MONOB, 26), fill=GREY, anchor='ma'); medidor(d, 1404, 'SEM JOGOS DE TRK', 2, 'BAIXO')
        return subs(im, t, SUBY)
    if t < T_SIG:
        im = tubo_frame(t, 'analitico', zoom=1.0); d = ImageDraw.Draw(im, 'RGBA')
        im = top_card(im, [('Mítica fora do seu melhor par?', F(INTB, 56), WHITE)], 1.0, 232)
        d = ImageDraw.Draw(im, 'RGBA')
        chips = [('A · BOMBA', ws(260)), ('B · ESTRUTURA', ws(264)), ('C · SPLASH', ws(268))]
        f = F(MONOB, 29); y = 1385
        wds = [d.textlength(s, font=f) + 40 for s, _ in chips]; x = 510 - (sum(wds) + 2 * 12) / 2
        for (s, tt), wd in zip(chips, wds):
            on = t >= tt
            d.rounded_rectangle((x, y, x + wd, y + 68), 34, fill=(EM if on else (15, 23, 42, 230)), outline=EM, width=3)
            d.text((x + wd / 2, y + 34), s, font=f, fill=(BG if on else EM), anchor='mm'); x += wd + 12
        return subs(im, t, SUBY)
    kz = eio((t - T_SIG) / 1.2)
    im = tubo_frame(t, 'confiante', zoom=1.0 + 0.22 * kz, cx=W / 2, cy=H / 2 + (SCY + 260 - H / 2) * kz)
    k = ease((t - T_SIG) / 0.4)
    im = top_card(im, [('META EM CURTO', F(INTB, 96), WHITE), ('com TUBO · BINDER Originals', F(MONO, 34), EM)], k, 232)
    return subs(im, t, SUBY)
if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[2] == 'capa':
        im = tubo_frame(12.0, 'confiante', zoom=1.0); d = ImageDraw.Draw(im, 'RGBA')
        d.text((W / 2, 110), '1 JOGO EM 96', font=F(INTB, 112), fill=PH, anchor='ma')
        d.text((W / 2, 250), 'A CONTA DO SEALED', font=fit(d, 'A CONTA DO SEALED', INTB, 84, 900), fill=WHITE, anchor='ma')
        d.text((W / 2, 360), 'STAR TREK · PRÉ-RELEASE', font=F(MONOB, 54), fill=EM, anchor='ma')
        d.text((W / 2, 1470), 'META EM CURTO · com TUBO', font=F(MONOB, 40), fill=WHITE, anchor='ma')
        im.convert('RGB').save('EP05_CAPA.png'); sys.exit()
    if len(sys.argv) > 2 and sys.argv[2] == 'stills':
        for tt in map(float, sys.argv[3:]): frame(tt).save(f'still_{tt:05.2f}.png')
        sys.exit()
    nf = int(round(TOTAL * FPS))
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-i', 'mix_final.wav', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
                          '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', '-shortest', 'EP05_META_EM_CURTO.mp4'],
                         stdin=subprocess.PIPE)
    for i in range(nf): p.stdin.write(frame(i / FPS).convert('RGB').tobytes())
    p.stdin.close(); p.wait(); print('done', nf)
