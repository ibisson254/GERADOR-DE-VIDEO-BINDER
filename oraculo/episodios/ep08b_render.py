# Meta em Curto EP08B v2 · corte «campeão primeiro» · render (derivado de ep08_render.py e do gancho do MC-ESP01)
# Abertura padrão do TUBO (fundador, 16/11): quadro 0 = cartas reais ligadas ao pagamento, em ecrã inteiro.
# Uso, numa pasta de trabalho com tl.json, words.json, led_env.npy e mix_final.wav (saídas de ep08b_audio.py):
#   python3 ep08_render.py /caminho/do/kit             -> EP08_META_EM_CURTO.mp4
#   python3 ep08_render.py /caminho/do/kit stills 3 10 -> still_03.00.png ...
# O fecho é o ficheiro real comum/outro/outro_binder_916.mp4 (sem áudio; a trilha do episódio continua por baixo).
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
EGG0, EGG1 = ws(26), ws(36)    # easter egg «MOCS» na chuva de código = Schütz venceu o Magic Online Champions Showcase (2024, temporada 1; Ultimate Guard)
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
        for k, ch in enumerate('MOCS'): d.text((tcols[22]['x'], 1250 + k * 30), ch, font=fs, fill=mix_bg(PH, 90))
    return im, d
def term_finish(im):
    im = Image.composite(im, Image.new('RGB', (W, H), (0, 0, 0)), vig); im.paste(SCANL, (0, 0), SCANL); return im
def hud(d, t):
    a = led_amp(t)
    d.ellipse((80, 1676, 100, 1696), fill=(16, 185, 129, int(70 + 185 * a)))
    d.text((114, 1686), 'BINDER', font=F(MONOB, 28), fill=(16, 185, 129, 220), anchor='lm')
    d.text((W - 80, 1686), 'META EM CURTO · EP08B', font=F(MONO, 26), fill=(150, 170, 175, 220), anchor='rm')
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



def foto_quadrada(im_, lado):
    w, h = im_.size; m = min(w, h); x = (w - m) // 2; y = max(0, int((h - m) * 0.25))
    return im_.crop((x, y, x + m, y + m)).resize((lado, lado), Image.LANCZOS)
SIL = ["......####......", ".....######.....", "....########....", "....########....", "....########....",
       ".....######.....", "......####......", "...##########...", "..############..", ".##############.",
       ".##############.", "################", "################"]
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

def lista_col(d, t, x, y, grupos, t0, wmax, verde=(), ls=40, fs=32):
    i = 0
    for g, cartas in grupos:
        if t >= t0 + i * .015: d.text((x - 26, y), g, font=F(MONOB, 26), fill=GREY)
        y += ls; i += 1
        for n, nome in cartas:
            if t >= t0 + i * .015:
                on = nome in verde; s_ = f'{n} {nome}'
                d.text((x, y), s_, font=fit(d, s_, CONDB, fs, wmax), fill=(PH if on else (150, 190, 170)))
                if on: d.text((x - 28, y + 3), '▶', font=F(MONOB, 22), fill=PH)
            y += ls; i += 1
        y += 10
    return y
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

# ---------- EP08: dados (fontes em oraculo/ep08/fontes.txt) ----------
AMBER = (255, 176, 32)
CARD = {}
def carta(slug, w):
    k = (slug, w)
    if k not in CARD:
        im_ = Image.open(K + f'oraculo/ep08/cartas/{slug}.jpg').convert('RGB'); CARD[k] = im_.resize((w, int(w * im_.height / im_.width)), Image.LANCZOS)
    return CARD[k]
FOTO = Image.open(K + 'oraculo/ep08/fotos/stefan_schutz.jpg').convert('RGB').crop((620, 40, 1300, 1080))   # autorização: oraculo/autorizacoes/2026-11-16_ep08_foto_campeao.md
TOP8 = [('Charis Kikidis', 'GRE', 'Izzet Prowess'), ('Stefan Schütz', 'AUT', 'Izzet Mission'), ('Arne Huschenbeth', 'ALE', 'Azorius Control'),
        ('Kellen Pastore', 'EUA', 'Boros Pixie'), ('Abe Schnake', 'EUA', 'Jund Sacrifice'), ('Shuhei Nakamura', 'JAP', 'Azorius Momo'),
        ('Eduardo Sajgalik', 'CAN', 'Selesnya Michelangelo'), ('James Drake', 'AUS', 'Selesnya Landfall')]
META = [('Boros Pixie', 24, 18.8), ('Selesnya Landfall', 19, 14.8), ('Dimir Control', 10, 7.8), ('Selesnya Michelangelo', 9, 7.0),
        ('Mono-Green Landfall', 8, 6.3), ('Dimir Midrange', 8, 6.3), ('Jund Sacrifice', 7, 5.5)]
LISTA = [('INSTANTÂNEAS E FEITIÇOS · 30', [(4, 'Flashback'), (4, 'Opt'), (4, 'Sleight of Hand'), (3, 'Into the Flood Maw'), (2, 'Consult the Star Charts'),
          (2, "Long River's Pull"), (2, 'Spell Pierce'), (2, 'Spell Snare'), (2, 'Torch the Tower'), (1, 'Burst Lightning'), (1, 'Fire Magic'),
          (1, 'Impractical Joke'), (1, 'Sear'), (1, 'Traumatic Critique')]),
         ('OUTRAS MÁGICAS · 8', [(4, 'Anthropological Mission'), (3, 'Ral, Crackling Wit'), (1, 'Engineered Explosives')]),
         ('TERRENOS · 22', [(6, 'Island'), (4, 'Riverpyre Verge'), (4, 'Spirebluff Canal'), (4, 'Steam Vents'), (2, 'Great Hall of the Biblioplex'),
          (1, 'Multiversal Passage'), (1, 'Stormcarved Coast')])]
PREVS = {'01': ('PR-WC32-01', 'pública', 'Jund Sacrifice terá pelo menos um jogador no Top 8 do Magic World Championship 32', 'CONFIRMADA'),
         '03': ('PR-WC32-03', 'registo', 'Izzet Spellementals terá menos de 5% do Standard do World Championship 32', 'CONFIRMADA'),
         '02': ('PR-WC32-02', 'registo', 'Jund Sacrifice será um dos 3 arquétipos mais jogados no Standard do World Championship 32', 'REFUTADA')}
STAMPS = TL['STAMPS']
def wrapn(d, s, font, maxw):
    out, cur = [], ''
    for w_ in s.split():
        c = (cur + ' ' + w_).strip()
        if d.textlength(c, font=font) <= maxw: cur = c
        else: out.append(cur); cur = w_
    return out + [cur]
def header(d, s1, s2):
    d.text((80, 200), s1, font=fit(d, s1, MONOB, 36, 920), fill=PH)
    d.text((80, 252), s2, font=fit(d, s2, MONO, 28, 920), fill=EM)
    d.line((80, 300, 1000, 300), fill=(16, 185, 129, 90), width=2)


# ---------- EP08B: abertura padrão (modelo do MC-ESP01, fundador 16/11) ----------
# Grelha 2×2 em ecrã inteiro sobre o TUBO escurecido: foto do jogador + 3 cartas da lista, selo em cada quadro;
# destaque = contorno verde a brilhar + o resto escurece + caixa de número grande; depois os quadros sobem para
# uma fila por cima do TUBO e o vídeo mergulha no ecrã dele (lista do deck dentro do tubo).
STAMPS = TL['STAMPS']; DIVE = TL['DIVE']; DIVE_END = DIVE + 0.45; EXIT = TL['EXIT']; EXIT_END = EXIT + 0.75
def _rounded(c):
    m = Image.new('L', c.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, c.size[0] - 1, c.size[1] - 1), 26, fill=255)
    c = c.convert('RGBA'); c.putalpha(m); return c
_fw = FOTO.width; QUADROS = [_rounded(FOTO.crop((0, 0, _fw, int(_fw * 88 / 63)))),
        _rounded(Image.open(K + 'oraculo/ep08/cartas/anthropological_mission.jpg').convert('RGB')),
        _rounded(Image.open(K + 'oraculo/ep08/cartas/ral_crackling_wit.jpg').convert('RGB')),
        _rounded(Image.open(K + 'oraculo/ep08/cartas/into_the_flood_maw.jpg').convert('RGB'))]
SELOS = ['CAMPEÃO', '4 cópias', '3 cópias', '3 cópias']
_cc = {}
def card_img(i, w, dim=0.0):
    key = (i, int(w), round(dim, 2))
    if key not in _cc:
        c = QUADROS[i]; h = int(w * 88 / 63); r_ = c.resize((int(w), h), Image.LANCZOS)
        if dim > 0:
            dark = Image.new('RGBA', r_.size, (5, 10, 16, 255)); a_ = r_.getchannel('A'); r_ = Image.blend(r_, dark, dim); r_.putalpha(a_)
        if len(_cc) > 400: _cc.clear()
        _cc[key] = r_
    return _cc[key]
GRID = [(55, 250), (555, 250), (55, 945), (555, 945)]; GW = 470
ROW = [(30, 92), (285, 92), (555, 92), (810, 92)]; RW = 240
def glow_box(im, box, col=PH, r=26):
    g = Image.new('RGBA', im.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.rounded_rectangle(box, r, outline=col + (255,), width=16); g = g.filter(ImageFilter.GaussianBlur(14))
    im.alpha_composite(g); ImageDraw.Draw(im).rounded_rectangle(box, r, outline=col + (255,), width=6)
def pill(d, cx, cy, txt, col, size=40):
    f = F(MONOB, size); wd = d.textlength(txt, font=f) + 40
    d.rounded_rectangle((cx - wd / 2, cy - size * .75, cx + wd / 2, cy + size * .75), int(size * .75), fill=(5, 10, 16, 235), outline=col, width=4)
    d.text((cx, cy), txt, font=f, fill=col, anchor='mm')
def pop_text(d, cx, cy, txt, t0, t, size, col):
    if t < t0: return
    k = eio((t - t0) / 0.22); f = F(INTB, int(size * (1.35 - 0.35 * k)))
    for dx, dy in ((6, 6), (-2, 6)): d.text((cx + dx, cy + dy), txt, font=f, fill=(0, 0, 0, 200), anchor='mm')
    d.text((cx, cy), txt, font=f, fill=col, anchor='mm')
def hook(t):
    T_MI, T_16, TMOV = STAMPS[1] - .05, STAMPS[2] - .05, STAMPS[3] - .05
    km = eio((t - TMOV) / 0.5) if t >= TMOV else 0.0
    base = tubo_frame(t, 'desconfiado' if t < TMOV else 'confiante').convert('RGBA')
    im = base.copy(); im.alpha_composite(Image.new('RGBA', base.size, (3, 6, 10, int(225 * (1 - km))))); d = ImageDraw.Draw(im, 'RGBA')
    if km < 1:
        a = int(255 * max(0, 1 - km * 2.5))
        d.text((W / 2, 120), 'CAMPEÃO DO MUNDO · MAGIC', font=F(MONOB, 50), fill=(200, 215, 220, a), anchor='mm')
        d.text((W / 2, 185), 'Mundial 32 · Standard · 15/11/2026 · foto autorizada pelo jogador', font=F(COND, 30), fill=(140, 160, 165, a), anchor='mm')
    for i in range(4):
        ks = eio((t - 0.06 * i + 0.07) / 0.25)
        if ks <= 0: continue
        gx, gy = GRID[i]; rx, ry = ROW[i]
        w = GW + (RW - GW) * km; x = gx + (rx - gx) * km; y = gy + (ry - gy) * km
        sc = 1.18 - 0.18 * ks; w2 = w * sc; x -= (w2 - w) / 2; y -= (w2 - w) * 0.7
        lit = (T_MI <= t < TMOV and i == 0) or (t >= TMOV and i == 1)
        dim = 0.0 if (t < T_MI or lit) else (0.62 if t < TMOV else 0.5)
        c = card_img(i, w2, dim); im.alpha_composite(c, (int(x), int(y)))
        if lit: glow_box(im, (int(x), int(y), int(x + c.width), int(y + c.height)))
        d = ImageDraw.Draw(im, 'RGBA')
        if km < 0.5 and ks > 0.6:
            sel = SELOS[i] if not (i == 0 and t >= T_MI) else 'IZZET MISSION'
            pill(d, x + c.width / 2, y + c.height - 66, sel, PH if lit else (WHITE if dim == 0 else GREY), 34 if i == 0 else 38)
    if T_16 <= t < TMOV:
        d.rounded_rectangle((230, 800, 850, 1130), 40, fill=(3, 6, 10, 215), outline=WHITE, width=4)
        pop_text(d, W / 2, 935, '1,6%', T_16, t, 210, WHITE)
        d.text((W / 2, 1085), '2 em 128 jogadores', font=F(MONOB, 44), fill=GREY, anchor='mm')
    if t >= TMOV:                      # a carta-nome entra no ecrã do TUBO: o mergulho entra nela
        k = eio((t - TMOV) / 0.25); cw = int((SCR[2] - SCR[0] - 40) * (0.6 + 0.4 * k))
        d.rounded_rectangle(SCR, 18, fill=(4, 14, 10, 235))
        c = card_img(1, cw * 0.72); im.alpha_composite(c, (int(SCX - c.width / 2), int(SCY - c.height / 2)))
    return im.convert('RGB')

# ---------- DENTRO: a lista campeã ----------
def scene_lista(t):
    im, d = term_base(t, 10); t0 = DIVE_END - 0.1
    s1 = '> LISTA CAMPEÃ · IZZET MISSION'
    d.text((80, 200), typed(s1, t0, t), font=fit(d, s1, MONOB, 38, 920), fill=PH)
    d.text((80, 258), typed('  Stefan Schütz · 1.º no Mundial 32 · 60 cartas', t0 + .3, t), font=F(MONO, 28), fill=EM)
    d.line((80, 312, 1000, 312), fill=(16, 185, 129, 90), width=2)
    verde = {'Anthropological Mission'}
    lista_col(d, t, 90, 345, LISTA[:1], t0 + .2, 460, verde, ls=40, fs=30)
    lista_col(d, t, 590, 345, LISTA[1:], t0 + .4, 420, verde, ls=40, fs=30)
    if t >= ws(26) - .3:
        k = eio((t - ws(26) + .3) / .35); c = carta('anthropological_mission', int(300 + 20 * k))
        im.paste(c, (640, 860)); d = ImageDraw.Draw(im, 'RGBA'); d.rectangle((637, 857, 643 + c.width, 863 + c.height), outline=PH, width=4)
    if t >= ws(27) - .05:
        d.text((90, 1000), 'STAR TREK (TRK 46)', font=F(MONOB, 38), fill=AMBER)
        d.text((90, 1055), 'entrou no formato', font=F(MONO, 32), fill=WHITE)
        d.text((90, 1100), '1 semana antes do Mundial', font=F(MONO, 32), fill=WHITE)
    fontes(d, ['lista: Melee via MTGTop8 · carta: Scryfall (TRK 46, arte de Pablo Mendoza)', '«uma semana antes»: magic.gg (Day Two Highlights)'], 1384)
    hud(d, t); return term_finish(im)
SUBY = 1530
T_Q = ws(53) - 0.1; T_SIG = ws(64) - 0.15
PRV = [('01', 'Jund no Top 8', True, 42), ('03', 'Spellementals < 5%', True, 42), ('02', 'Jund no top 3', False, 44)]
def frame_main(t):
    if t < DIVE_END:
        if t < DIVE: return subs(hook(t), t, 1700 if t < STAMPS[3] - .05 else SUBY)
        k = eio((t - DIVE) / (DIVE_END - DIVE)); z = 1 + k * 4.2
        im = hook(DIVE - 0.001).resize((int(W * z), int(H * z)), Image.LANCZOS)
        ox = int(SCX * z - (W / 2 + (SCX - W / 2) * min(1, k * 1.5))); oy = int(SCY * z - (H / 2 + (SCY - H / 2) * min(1, k * 1.5)))
        im = im.crop((ox, oy, ox + W, oy + H))
        if k > 0.6: im = Image.blend(im, scene_lista(t), (k - 0.6) / 0.4)
        return im
    if t < EXIT: return subs(scene_lista(t), t)
    if t < EXIT_END:
        k = eio((t - EXIT) / (EXIT_END - EXIT)); z = 5.2 - 4.2 * k
        im = tubo_frame(t, 'analitico', zoom=z, cx=W / 2 + (SCX - W / 2) * (1 - k), cy=H / 2 + (SCY - H / 2) * (1 - k))
        if k < 0.35: im = Image.blend(scene_lista(t), im, k / 0.35)
        return subs(im, t, SUBY)
    if t < T_Q:
        expr = 'confiante' if t >= ws(49) - .05 else ('desconfiado' if t >= ws(44) else 'analitico')
        im = tubo_frame(t, expr, zoom=1.0); d = ImageDraw.Draw(im, 'RGBA')
        if t < ws(49) - .05:
            d.text((W / 2, 90), 'MINHAS 3 PREVISÕES', font=F(INTB, 70), fill=WHITE, anchor='ma')
            for i, (pid, txt, ok, wi) in enumerate(PRV):
                y = 180 + i * 64; x0 = 130
                d.rounded_rectangle((x0, y, W - x0, y + 58), 29, fill=(15, 23, 42, 230), outline=(40, 80, 70), width=2)
                d.text((x0 + 30, y + 29), f'{pid} · {txt}', font=fit(d, f'{pid} · {txt}', MONOB, 32, 600), fill=WHITE, anchor='lm')
                if t >= STAMPS[4 if ok else 5]:
                    d.text((W - x0 - 30, y + 29), '✔' if ok else '✘', font=F(MONOB, 40), fill=(PH if ok else RED), anchor='rm')
            if t >= ws(44) - .05:
                d.text((W / 2, 375), 'NENHUMA ERA O CAMPEÃO', font=fit(d, 'NENHUMA ERA O CAMPEÃO', MONOB, 44, 960), fill=AMBER, anchor='ma')
            note(d, 'previsões registradas em 10/11, antes do Mundial · dados: magic.gg')
        else:
            d.text((W / 2, 170), 'PLACAR', font=F(MONOB, 44), fill=GREY, anchor='ma')
            d.text((W / 2, 220), '2 / 3', font=F(INTB, 160), fill=PH, anchor='ma')
            note(d, 'PR-WC32-01 (pública) e 03 confirmadas · 02 refutada')
        return subs(im, t, SUBY)
    if t < T_SIG:
        im = tubo_frame(t, 'analitico', zoom=1.0); d = ImageDraw.Draw(im, 'RGBA')
        q1, q2 = 'Você levaria ao Mundial um deck', 'que só 2 jogadores levaram?'
        d.text((W / 2, 170), q1, font=fit(d, q1, INTB, 60, 960), fill=WHITE, anchor='ma')
        d.text((W / 2, 250), q2, font=fit(d, q2, INTB, 60, 960), fill=PH, anchor='ma')
        for i, s_ in enumerate(['SIM', 'NÃO']):
            if t < ws(60) + i * .12: continue
            x = 250 + i * 320; on = t >= ws(63) - .05
            d.rounded_rectangle((x, 350, x + 260, 420), 35, fill=((10, 52, 30, 255) if on else (15, 23, 42, 230)), outline=EM, width=3)
            d.text((x + 130, 385), s_, font=F(MONOB, 40), fill=(PH if on else WHITE), anchor='mm')
        if t >= ws(63) - .05: note(d, 'responda SIM ou NÃO')
        return subs(im, t, SUBY)
    kz = eio((t - T_SIG) / 1.2)
    im = tubo_frame(t, 'confiante', zoom=1.0 + 0.22 * kz, cx=W / 2, cy=H / 2 + (SCY + 260 - H / 2) * kz)
    k = ease((t - T_SIG) / 0.4)
    im = top_card(im, [('META EM CURTO', F(INTB, 96), WHITE), ('com TUBO · BINDER Originals', F(MONO, 34), EM)], k, 225)
    return subs(im, t, SUBY)
def capa():
    im = Image.new('RGBA', (W, H), BG + (255,))
    for sl, ang, x, y in [('ral_crackling_wit', 10, -40, 860), ('into_the_flood_maw', -10, 640, 860)]:
        c = carta(sl, 430).convert('RGBA').rotate(ang, resample=Image.BICUBIC, expand=True); im.alpha_composite(c, (x, y))
    c = carta('anthropological_mission', 480).convert('RGBA'); im.alpha_composite(c, ((W - c.width) // 2, 800))
    ph = FOTO.resize((300, int(300 * FOTO.height / FOTO.width)), Image.LANCZOS).crop((0, 0, 300, 360)).convert('RGBA')
    im.alpha_composite(ph, (W - 340, 420)); d = ImageDraw.Draw(im, 'RGBA'); d.rectangle((W - 343, 417, W - 37, 783), outline=PH, width=4)
    d.text((70, 330), 'O DECK CAMPEÃO', font=fit(d, 'O DECK CAMPEÃO', INTB, 96, 620), fill=WHITE, anchor='lm')
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.text((70, 600), '1,6%', font=F(INTB, 250), fill=PH + (200,), anchor='lm'); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(24)))
    d = ImageDraw.Draw(im, 'RGBA'); d.text((70, 600), '1,6%', font=F(INTB, 250), fill=PH, anchor='lm')
    d.text((W - 190, 810), 'CAMPEÃO', font=F(MONOB, 30), fill=PH, anchor='ma')
    d.rectangle((0, 1572, W, 1662), fill=(5, 10, 16, 235)); d.line((0, 1572, W, 1572), fill=PH, width=4)
    d.text((60, 1617), 'META EM CURTO · MUNDIAL 32', font=F(MONOB, 40), fill=PH, anchor='lm')
    d.text((W - 60, 1617), '2 EM 128', font=F(MONOB, 40), fill=AMBER, anchor='rm')
    im.convert('RGB').save('EP08B_CAPA.png'); im.convert('RGB').crop((0, 240, W, 1680)).save('EP08B_CAPA_grelha.png')
if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[2] == 'capa': capa(); sys.exit()
    if len(sys.argv) > 2 and sys.argv[2] == 'stills':
        for tt in map(float, sys.argv[3:]): frame(tt).save(f'still_{tt:05.2f}.png')
        sys.exit()
    nf = int(round(TOTAL * FPS))
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-i', 'mix_final.wav', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
                          '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', '-shortest', 'EP08B_META_EM_CURTO.mp4'],
                         stdin=subprocess.PIPE)
    for i in range(nf): p.stdin.write(frame(i / FPS).convert('RGB').tobytes())
    p.stdin.close(); p.wait(); print('done', nf)
