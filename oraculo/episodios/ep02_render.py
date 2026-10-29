# Meta em Curto EP02 · render (derivado de ep01_render.py / ep01_render_v2.py)
# Uso, numa pasta de trabalho com tl.json, words.json, led_env.npy e mix_final.wav (saídas de ep02_audio.py):
#   python3 ep02_render.py /caminho/do/kit            -> EP02_META_EM_CURTO.mp4
#   python3 ep02_render.py /caminho/do/kit stills 3 10 -> still_03.00.png ...
import json, math, subprocess, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
K = (sys.argv[1] if len(sys.argv) > 1 else '../..').rstrip('/') + '/'
W, H, FPS = 1080, 1920, 30
TL = json.load(open('tl.json')); WORDS = json.load(open('words.json'))
TEMPO, LEAD, PAUSE_AT, PAUSE = TL['TEMPO'], TL['LEAD'], TL['PAUSE_AT'], TL['PAUSE']
TOTAL, OUT = TL['TOTAL'], TL['OUT_START']
def vt(x): return x / TEMPO + LEAD + (PAUSE if x >= PAUSE_AT else 0)
for w in WORDS: w['vs'] = vt(w['s']); w['ve'] = vt(w['e'])
def ws(i): return WORDS[i]['vs']
ENV = np.load('led_env.npy')
MASTER = Image.open(K + 'oraculo/assets/tubo_mestra_916.png').convert('RGB')
LOGO = Image.open(K + 'manaburn/logo/logo_mark.png').convert('RGBA')
SCAN = [Image.open(K + f'comum/outro/scan/{i:03d}.jpg').convert('RGB') for i in range(45)]
CD = K + 'oraculo/ep02/cartas/'
CARDS = {k: Image.open(CD + k + '.png').convert('RGBA') for k in
         ['biotech_specialist', 'the_sackvillebagginses', 'lively_dirge', 'united_battlefront', 'treasure']}
LISTA = json.load(open(K + 'oraculo/episodios/ep02_listas.json'))
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
EGG0, EGG1 = 8.0, 9.0          # easter egg «11-0» na chuva de código (segundos do vídeo)
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
        for k, ch in enumerate('11-0'): d.text((tcols[21]['x'], 1180 + k * 30), ch, font=fs, fill=mix_bg(PH, 80))
    return im, d
def term_finish(im):
    im = Image.composite(im, Image.new('RGB', (W, H), (0, 0, 0)), vig); im.paste(SCANL, (0, 0), SCANL); return im
def hud(d, t):
    a = led_amp(t)
    d.ellipse((80, 1676, 100, 1696), fill=(16, 185, 129, int(70 + 185 * a)))
    d.text((114, 1686), 'BINDER', font=F(MONOB, 28), fill=(16, 185, 129, 220), anchor='lm')
    d.text((W - 80, 1686), 'META EM CURTO · EP02', font=F(MONO, 26), fill=(150, 170, 175, 220), anchor='rm')
def fontes(d, linhas, y=1384):
    """Linha(s) de fonte, ≥ 24 px de altura de letra (corrige o EP01)."""
    for i, s in enumerate(linhas):
        f = fit(d, s, COND, 34, W - 160)
        d.text((80, y + i * 44), s, font=f, fill=(150, 170, 175, 235))
def header(d, t, t0, sub='STANDARD · 23–25 OUT 2026 · SCG CON HARTFORD'):
    d.text((80, 200), typed('> ARQUIVO: MAGIC SPOTLIGHT: FRACTURE', t0, t), font=F(MONOB, 34), fill=PH)
    d.text((80, 252), typed('  ' + sub, t0 + 0.5, t), font=F(MONO, 28), fill=EM)
    d.line((80, 306, 1000, 306), fill=(16, 185, 129, 90), width=2)

# silhueta pixelizada (nunca um rosto)
SIL = ["......####......", ".....######.....", "....########....", "....########....", "....########....",
       ".....######.....", "......####......", "...##########...", "..############..", ".##############.",
       ".##############.", "################", "################"]
def silhueta(d, x, y, px=13, col=PH):
    for r, row in enumerate(SIL):
        for c, ch in enumerate(row):
            if ch == '#': d.rectangle((x + c * px, y + r * px, x + c * px + px - 2, y + r * px + px - 2), fill=col + (150,))
def ficha(d, t, x, t0, nome, linhas, destaque):
    k = eio((t - t0) / 0.4)
    if k <= 0: return
    a = int(255 * k)
    d.rounded_rectangle((x, 360, x + 450, 1270), 18, outline=(16, 185, 129, int(160 * k)), width=3, fill=(8, 20, 18, int(200 * k)))
    d.text((x + 24, 384), 'FICHA DE JOGADOR', font=F(MONOB, 24), fill=GREY + (a,))
    silhueta(d, x + 121, 440, col=(PH if destaque else EM))
    f = fit(d, nome, INTB, 64, 400)
    d.text((x + 225, 640), nome, font=f, fill=WHITE + (a,), anchor='ma')
    y = 740
    for s, col in linhas:
        tt = t0 + 0.3 + (y - 740) / 400
        ff = fit(d, s, CONDB, 34, 400)
        d.text((x + 225, y), typed(s, tt, t, 60), font=ff, fill=col + (a,), anchor='ma'); y += 66
def scene_fichas(t):
    im, d = term_base(t, 24); header(d, t, DIVE_END)
    ficha(d, t, 70, ws(16), 'VON STANGE', [('JUND SACRIFICE', PH), ('SEED 3', WHITE), ('11-0 NO ARRANQUE', WHITE),
                                           ('SUÍÇO: 12-2-1 (1 ID)', GREY), ('CAMPEÃO RC CHIBA 2023', EM), ('ESTE TORNEIO: 1.º', PH)], True)
    ficha(d, t, 560, ws(20), 'OTT', [('JESKAI ARTIFACTS', WHITE), ('SEED 1', PH if t >= ws(24) else WHITE),
                                     ('MELHOR DO SUÍÇO', GREY), ('ESTE TORNEIO: 2.º', WHITE)], False)
    fontes(d, ['fonte: Star City Games · relato da final (25/10/2026)', 'seeds, campanha e título anterior: SCG'])
    hud(d, t); return term_finish(im)

def card_scan(im, key, t0, t, cx, y, width):
    """Carta oficial inteira (Scryfall), revelada linha a linha como num scan."""
    c = CARDS[key]; h = int(width * c.height / c.width); c = c.resize((width, h), Image.LANCZOS)
    k = ease((t - t0) / 0.55)
    if k <= 0: return y + h
    x = int(cx - width / 2); rows = int(h * k)
    if rows > 0: im.paste(c.crop((0, 0, width, rows)), (x, y), c.crop((0, 0, width, rows)))
    d = ImageDraw.Draw(im, 'RGBA')
    if k < 1:
        d.rectangle((x - 10, y + rows - 3, x + width + 10, y + rows + 3), fill=(0, 255, 65, 230))
        d.rectangle((x - 10, y + rows - 14, x + width + 10, y + rows + 14), fill=(0, 255, 65, 40))
    d.rounded_rectangle((x - 6, y - 6, x + width + 6, y + h + 6), 22, outline=(16, 185, 129, 120), width=3)
    return y + h
def cred(nome, sc, n, artista): return [f'{nome} · {sc} {n} · arte: {artista}', 'Cartas © Wizards of the Coast · imagens via Scryfall']
CRED = {k: cred(*v) for k, v in {
    'united_battlefront': ('United Battlefront', 'TDM', '32', 'Darren Tan'),
    'biotech_specialist': ('Biotech Specialist', 'EOE', '214', 'Alexandre Honoré'),
    'the_sackvillebagginses': ('The Sackville-Bagginses', 'HOB', '83', 'Denman Rooke'),
    'lively_dirge': ('Lively Dirge', 'OTJ', '93', 'Warren Mahy'),
    'treasure': ('Treasure (ficha)', 'THOB', '12', 'Leonardo Santanna')}.items()}
def scene_card(t, key, t0, title, caps):
    im, d = term_base(t, 16)
    d.text((80, 200), title, font=F(MONOB, 34), fill=PH)
    d.line((80, 252, 1000, 252), fill=(16, 185, 129, 90), width=2)
    yb = card_scan(im, key, t0, t, W / 2, 285, 650)
    d = ImageDraw.Draw(im, 'RGBA')
    y = yb + 20
    for s, tc, col in caps:
        if t >= tc:
            f = fit(d, s, MONOB, 40, W - 160)
            d.text((W / 2, y), typed(s, tc, t, 55), font=f, fill=col, anchor='ma')
        y += 54
    fontes(d, CRED[key])
    hud(d, t); return term_finish(im)
def scene_lista(t):
    im, d = term_base(t, 12); L = LISTA['von_stange']
    d.text((80, 200), '> LISTA · VON STANGE · JUND SACRIFICE', font=F(MONOB, 34), fill=PH)
    d.text((80, 252), '  60 cartas no principal · 1.º lugar', font=F(MONO, 28), fill=EM)
    d.line((80, 306, 1000, 306), fill=(16, 185, 129, 90), width=2)
    grupos = list(L['principal'].items())
    cols = [grupos[:4], grupos[4:]]
    fn = F(CONDB, 32); fh = F(MONOB, 26)
    i = 0
    for ci, col in enumerate(cols):
        x = 80 if ci == 0 else 600; y = 336
        for g, cartas in col:
            if t >= ws(35) + i * 0.025: d.text((x, y), g, font=fh, fill=GREY)
            y += 44; i += 1
            for n, nome in cartas:
                if t >= ws(35) + i * 0.025:
                    key = nome in L['chave']
                    f = fit(d, f'{n} {nome}', CONDB, 32, 470 if ci == 0 else 410)
                    d.text((x, y), f'{n} {nome}', font=f, fill=(PH if key else DIMG))
                    if key: d.text((x - 30, y), '▶', font=F(MONOB, 26), fill=PH)
                y += 44; i += 1
            y += 14
    fontes(d, ['fonte: Star City Games · lista do campeão (25/10/2026)', 'a verde: as três cartas do motor'])
    hud(d, t); return term_finish(im)
def scene_tesouro(t):
    im, d = term_base(t, 16)
    d.text((80, 200), '> A CONTA DO SACRIFÍCIO', font=F(MONOB, 34), fill=PH)
    d.line((80, 252, 1000, 252), fill=(16, 185, 129, 90), width=2)
    yb = card_scan(im, 'treasure', ws(57), t, W / 2, 285, 560)
    d = ImageDraw.Draw(im, 'RGBA'); y = yb + 24
    linhas = [('TESOURO = ARTEFATO + FICHA', ws(58), WHITE),
              ('ARTEFATO → BIOTECH: 2 DE DANO', ws(61), EM),
              ('FICHA → SACKVILLE: PERDE 1', ws(61) + 0.35, EM)]
    for s, tc, col in linhas:
        if t >= tc: d.text((W / 2, y), typed(s, tc, t, 60), font=fit(d, s, MONOB, 40, W - 160), fill=col, anchor='ma')
        y += 56
    if t >= ws(63):
        k = eio((t - ws(63)) / 0.3)
        d.text((W / 2, y + 6), '= 3', font=F(INTB, int(70 + 30 * k)), fill=PH, anchor='ma')
    fontes(d, ['texto Oracle: Biotech Specialist, The Sackville-Bagginses, Treasure', 'Cartas © Wizards of the Coast · imagens via Scryfall'])
    hud(d, t); return term_finish(im)

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

# ---------- OUTRO (quadros reais do scanner + logótipo; outro_binder_916.mp4 não está no repositório) ----------
def outro(t):
    if t < 1.5: return SCAN[min(44, int(t * 30))].copy()
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im, 'RGBA')
    v = eio((t - 1.5) / 0.6); size = int(60 + 260 * v)
    lg = LOGO.resize((size, size), Image.LANCZOS).rotate(-140 * (1 - v), resample=Image.BICUBIC)
    im.paste(lg, (int(W / 2 - lg.width / 2), int(760 - lg.height / 2)), lg)
    q = ease((t - 1.9) / 0.3); r = ease((t - 2.1) / 0.3)
    d.text((W / 2, 1000 + (1 - q) * 20), 'BINDER Vision', font=F(INTB, 92), fill=WHITE + (int(255 * q),), anchor='ma')
    d.text((W / 2, 1130), 'Escaneie suas cartas e organize seus decks.', font=F(INTM, 38), fill=(190, 200, 210, int(255 * q)), anchor='ma')
    d.text((W / 2, 1250), 'Disponível no Google Play · Link na bio', font=F(INTSB, 40), fill=EM + (int(255 * r),), anchor='ma')
    if t > 3.4: im = Image.blend(im, Image.new('RGB', (W, H), (0, 0, 0)), min(1, (t - 3.4) / 0.47))
    return im

# ---------- timeline ----------
DIVE = TL['DIVE']; DIVE_END = DIVE + 0.45; EXIT = TL['EXIT']; EXIT_END = EXIT + 0.75; ERR = TL['ERR']
T_BF = ws(26) - 0.1; T_LISTA = ws(35) - 0.1; T_BIO = ws(44) - 0.1; T_SACK = ws(51) - 0.1; T_TES = ws(57) - 0.1; T_DIRGE = ws(64) - 0.1
T_MESA = ws(87); T_Q = ws(91) - 0.05; T_SIG = ws(112) - 0.15
def inside(t):
    if t < T_BF: return scene_fichas(t)
    if t < T_LISTA:
        return scene_card(t, 'united_battlefront', ws(26), '> A MESA DO OTT', [
            ('ACELERAÇÃO', ws(30), WHITE), ('UNITED BATTLEFRONT', ws(31), PH), ('FICHAS DE CONSTRUCT ENORMES', ws(33), WHITE)])
    if t < T_BIO: return scene_lista(t)
    if t < T_SACK:
        return scene_card(t, 'biotech_specialist', ws(44), '> PEÇA 1 · BIOTECH SPECIALIST', [
            ('SACRIFICAS UM ARTEFATO', ws(46), WHITE), ('→ 2 DE DANO AO OPONENTE', ws(48), PH)])
    if t < T_TES:
        return scene_card(t, 'the_sackvillebagginses', ws(51), '> PEÇA 2 · THE SACKVILLE-BAGGINSES', [
            ('SACRIFICAS UMA FICHA', ws(52), WHITE), ('→ OPONENTE PERDE 1 DE VIDA', ws(54), PH)])
    if t < T_DIRGE: return scene_tesouro(t)
    return scene_card(t, 'lively_dirge', ws(66), '> O TUTOR · LIVELY DIRGE', [
        ('+{1}: 1 CARTA DO DECK → CEMITÉRIO', ws(68), WHITE),
        ('+{2}: VOLTAM ATÉ 2 CRIATURAS (VM ≤ 4)', ws(72), WHITE),
        ('BIOTECH 2 + SACKVILLE 2 = 4', ws(74), PH)])
def frame(t):
    if t >= OUT: return outro(t - OUT)
    if t >= OUT - 0.4:
        a = (t - (OUT - 0.4)) / 0.4; return Image.blend(frame_main(OUT - 0.41), outro(0), a)
    return frame_main(t)
def frame_main(t):
    if t < DIVE_END:
        if t < DIVE:
            im = tubo_frame(t, 'desconfiado' if t < ws(12) else 'confiante', zoom=1.0 + 0.04 * eio(t / 3.0))
            d = ImageDraw.Draw(im, 'RGBA')
            for x0, lab, tl_, val, tv, col in [(285, 'MESA', ws(6), 'OTT', ws(8), WHITE), (795, 'TÍTULO', ws(13), 'VON STANGE', ws(15), PH)]:
                if t >= tl_: d.text((x0, 130), lab, font=F(INTSB, 46), fill=GREY, anchor='ma')
                if t >= tv:
                    k = eio((t - tv) / 0.25)
                    f = fit(d, val, INTB, 110, 470)
                    d.text((x0, 190 + (1 - k) * 20), val, font=f, fill=col + (int(255 * k),), anchor='ma')
            if t >= ws(13): d.line((W / 2, 140, W / 2, 330), fill=(120, 140, 150, 120), width=2)
            return subs(im, t, 1640)
        k = eio((t - DIVE) / (DIVE_END - DIVE)); z = 1 + k * 4.2
        im = tubo_frame(t, 'analitico', zoom=z, cx=W / 2 + (SCX - W / 2) * min(1, k * 1.5), cy=H / 2 + (SCY - H / 2) * min(1, k * 1.5))
        if k > 0.6: im = Image.blend(im, scene_fichas(t), (k - 0.6) / 0.4)
        return im
    if t < EXIT: return subs(inside(t), t)
    if t < EXIT_END:
        k = eio((t - EXIT) / (EXIT_END - EXIT)); z = 5.2 - 4.2 * k
        im = tubo_frame(t, 'analitico', zoom=z, cx=W / 2 + (SCX - W / 2) * (1 - k), cy=H / 2 + (SCY - H / 2) * (1 - k))
        if k < 0.35: im = Image.blend(inside(t), im, k / 0.35)
        return subs(im, t, 1640)
    if t < T_Q:
        err = ERR <= t < T_MESA + 0.6
        im = tubo_frame(t, 'erro' if err else 'analitico', zoom=1.0, red_led=err)
        d = ImageDraw.Draw(im, 'RGBA')
        if t < T_MESA:
            d.rounded_rectangle((80, 120, 1000, 430), 16, fill=(5, 10, 16, 230), outline=((255, 64, 64, 200) if err else (16, 185, 129, 160)), width=3)
            d.text((110, 150), '> MODELO TUBO', font=F(MONOB, 34), fill=(RED if err else PH))
            d.text((110, 215), typed('VENCEDOR PROVÁVEL = MESA MAIOR', ws(77), t, 50), font=F(MONOB, 36), fill=WHITE)
            if t >= ws(80): d.text((110, 280), typed('→ OTT', ws(80), t, 30), font=F(INTB, 70), fill=WHITE)
            if err:
                rr = np.random.default_rng(int(t * 30))
                d.text((110 + rr.integers(-6, 6), 365), 'ERRO: ELE CONTOU O DANO', font=F(MONOB, 34), fill=RED)
                for _ in range(3):
                    y0 = int(rr.integers(130, 420)); d.rectangle((80, y0, 1000, y0 + int(rr.integers(2, 6))), fill=(255, 64, 64, 90))
        else:
            k = eio((t - T_MESA) / 0.3)
            im = top_card(im, [('MESA ≠ VIDA', F(INTB, 130), PH), ('leitura do TUBO, não regra do jogo', F(MONO, 34), GREY)], k, 170)
        return subs(im, t, 1640)
    if t < T_SIG:
        im = tubo_frame(t, 'analitico', zoom=1.0); d = ImageDraw.Draw(im, 'RGBA')
        im = top_card(im, [('O que decidiu a final?', F(INTB, 70), WHITE)], 1.0, 120)
        d = ImageDraw.Draw(im, 'RGBA')
        d.text((W / 2, 230), 'GRAU DE CERTEZA', font=F(MONOB, 32), fill=GREY, anchor='ma')
        for i, (lab, n, val) in enumerate([('MOTOR DAS CARTAS', 4, 'ALTO'), ('O QUE DECIDIU A FINAL', 1, 'BAIXO')]):
            y = 290 + i * 78
            d.text((90, y + 20), lab, font=F(CONDB, 32), fill=WHITE, anchor='lm')
            for s in range(5):
                x = 560 + s * 66
                d.rounded_rectangle((x, y, x + 56, y + 40), 7, fill=(EM if s < n else None), outline=EM, width=3)
            d.text((W - 80, y + 20), val, font=F(MONOB, 32), fill=EM, anchor='rm')
        chips = [('A · MESA TARDE', ws(96)), ('B · DIRGE', ws(103)), ('C · PILOTAGEM', ws(109))]
        f = F(MONOB, 32); y = 1460
        wds = [d.textlength(s, font=f) + 48 for s, _ in chips]; x = (W - sum(wds) - 2 * 18) / 2
        for (s, tt), wd in zip(chips, wds):
            on = t >= tt
            d.rounded_rectangle((x, y, x + wd, y + 68), 34, fill=(EM if on else (15, 23, 42, 230)), outline=EM, width=3)
            d.text((x + wd / 2, y + 34), s, font=f, fill=(BG if on else EM), anchor='mm'); x += wd + 18
        return subs(im, t, 1640)
    kz = eio((t - T_SIG) / 1.2)
    im = tubo_frame(t, 'confiante', zoom=1.0 + 0.22 * kz, cx=W / 2, cy=H / 2 + (SCY + 260 - H / 2) * kz)
    k = ease((t - T_SIG) / 0.4)
    im = top_card(im, [('META EM CURTO', F(INTB, 96), WHITE), ('com TUBO · BINDER Originals', F(MONO, 34), EM)], k)
    return subs(im, t, 1640)
if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[2] == 'stills':
        for tt in map(float, sys.argv[3:]): frame(tt).save(f'still_{tt:05.2f}.png')
        sys.exit()
    nf = int(round(TOTAL * FPS))
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-i', 'mix_final.wav', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
                          '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', '-shortest', 'EP02_META_EM_CURTO.mp4'],
                         stdin=subprocess.PIPE)
    for i in range(nf): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('done', nf)
