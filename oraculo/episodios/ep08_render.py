# Meta em Curto EP08 · Mundial 32 · prestação de contas · render (derivado de ep07_render.py)
# Uso, numa pasta de trabalho com tl.json, words.json, led_env.npy e mix_final.wav (saídas de ep08_audio.py):
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
EGG0, EGG1 = ws(87), ws(98)    # easter egg «MOCS» na chuva de código = Schütz venceu o Magic Online Champions Showcase (2024, temporada 1; Ultimate Guard)
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
    d.text((W - 80, 1686), 'META EM CURTO · EP08', font=F(MONO, 26), fill=(150, 170, 175, 220), anchor='rm')
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

# ---------- DENTRO ----------
def scene_arquivo(t):
    im, d = term_base(t, 22); t0 = DIVE_END - 0.1
    s1 = '> ARQUIVO: MAGIC WORLD CHAMPIONSHIP 32'
    d.text((80, 200), typed(s1, t0, t), font=fit(d, s1, MONOB, 38, 920), fill=PH)
    d.text((80, 258), typed('  PRESTAÇÃO DE CONTAS · 16/11/2026', t0 + .3, t), font=F(MONO, 30), fill=EM)
    d.line((80, 312, 1000, 312), fill=(16, 185, 129, 90), width=2)
    if t >= ws(16) - .05: d.text((W / 2, 380), 'MUNDIAL 32', font=F(INTB, 110), fill=WHITE, anchor='ma')
    if t >= ws(20) - .05: d.text((W / 2, 520), 'STANDARD · TOP 8 DE DOMINGO, 15/11', font=fit(d, 'STANDARD · TOP 8 DE DOMINGO, 15/11', MONOB, 40, 940), fill=GREY, anchor='ma')
    for i, k in enumerate(['01', '02', '03']):
        if t < ws(13) + .3 + i * .2: continue
        y = 660 + i * 150; pid, pub, _, _ = PREVS[k]
        d.rounded_rectangle((80, y, 1000, y + 120), 14, outline=(EM if pub == 'pública' else (40, 80, 70)), width=3, fill=(8, 20, 18, 255))
        d.text((110, y + 60), pid, font=F(MONOB, 44), fill=WHITE, anchor='lm')
        d.text((560, y + 40), pub.upper(), font=F(MONOB, 28), fill=(AMBER if pub == 'pública' else GREY), anchor='lm')
        d.text((560, y + 82), 'registrada 10/11', font=F(MONO, 26), fill=GREY, anchor='lm')
    fontes(d, ['previsões registradas no EP07, antes do torneio', 'critérios e fonte: magic.gg (definidos em 10/11)'])
    hud(d, t); return term_finish(im)
def caixa_original(im, d, t, k, t0):
    pid, pub, txt, est = PREVS[k]
    header(d, f'> ARQUIVO: {pid} · registrada 10/11', f'  estado: {est if t >= STAMPS[["01", "03", "02"].index(k)] else "PENDENTE"} · previsão {pub}')
    if t < t0: return 330
    f = F(CONDB, 44); ls = wrapn(d, '«' + txt + '»', f, 840); h = 70 + len(ls) * 54
    d.rounded_rectangle((80, 330, 1000, 330 + h), 14, outline=(150, 170, 175), width=2, fill=(10, 16, 22, 255))
    d.text((100, 346), 'TEXTO ORIGINAL · NÃO EDITADO', font=F(MONOB, 24), fill=AMBER)
    for i, s_ in enumerate(ls): d.text((110, 386 + i * 54), s_, font=f, fill=WHITE)
    return 330 + h + 30
def carimbo(d, t, k, y=1290):
    i = ['01', '03', '02'].index(k); est = PREVS[k][3]
    stamp(d, est, PH if est == 'CONFIRMADA' else RED, STAMPS[i], t, y, 54)
    if t >= STAMPS[i] + .25:
        s_ = 'evidência: D · dado oficial (magic.gg) · muda o placar? sim'
        d.text((W / 2, y + 52), s_, font=fit(d, s_, COND, 30, 940), fill=(170, 190, 195), anchor='ma')
def scene_prev01(t):
    im, d = term_base(t, 14); y = caixa_original(im, d, t, '01', ws(25) - .1)
    if t >= ws(32) - .1:
        for j, (sl, dx) in enumerate([('smaug_the_magnificent', 0), ('torch_the_tower', 1), ('greedy_freebooter', 2)]):
            if t < ws(32) - .1 + j * .12: continue
            c = carta(sl, 270); im.paste(c, (95 + dx * 300, y + 10)); d = ImageDraw.Draw(im, 'RGBA')
        d.text((W / 2, y + 400), 'ABE SCHNAKE · EUA · JUND SACRIFICE · TOP 8', font=fit(d, 'ABE SCHNAKE · EUA · JUND SACRIFICE · TOP 8', MONOB, 34, 940), fill=PH, anchor='ma')
    carimbo(d, t, '01', 1270)
    fontes(d, ['Top 8 e cartas-chave: magic.gg, 15/11/2026 · cartas: Scryfall'], 1400)
    hud(d, t); return term_finish(im)
def scene_prev03(t):
    im, d = term_base(t, 14); y = caixa_original(im, d, t, '03', ws(37) - .1)
    if t >= ws(44) - .05:
        k = eio((t - ws(44) + .05) / .3)
        d.text((W / 2, y + 30), '0', font=F(INTB, int(260 + 60 * k)), fill=PH, anchor='ma')
        d.text((W / 2, y + 400), 'JOGADORES DE IZZET SPELLEMENTALS EM 128', font=fit(d, 'JOGADORES DE IZZET SPELLEMENTALS EM 128', MONOB, 34, 940), fill=GREY, anchor='ma')
        d.text((W / 2, y + 450), 'antes do Mundial: 7,5% do field (Karsten, 05/11)', font=F(MONO, 28), fill=GREY, anchor='ma')
    carimbo(d, t, '03', 1270)
    fontes(d, ['metagame do Standard do WC32: magic.gg (128 listas)'], 1400)
    hud(d, t); return term_finish(im)
def scene_prev02(t):
    im, d = term_base(t, 14); y = caixa_original(im, d, t, '02', ws(53) - .1)
    if t >= ws(59) - .2:
        y0 = y
        for k, (nome, n, p) in enumerate(META):
            if t < ws(59) - .2 + k * .07: continue
            yy = y0 + k * 62; on = nome == 'Jund Sacrifice'
            d.text((80, yy + 22), f'{k + 1}.', font=F(MONOB, 30), fill=(RED if on else GREY), anchor='lm')
            d.text((130, yy + 22), nome, font=fit(d, nome, CONDB, 32, 340), fill=(WHITE if on else (150, 170, 175)), anchor='lm')
            bw = p / 19 * 380 * eio((t - ws(59) + .2 - k * .07) / .5)
            d.rectangle((490, yy + 6, 490 + bw, yy + 38), fill=(RED if on else (40, 110, 80)))
            d.text((490 + bw + 12, yy + 22), f'{p:.1f}%'.replace('.', ','), font=F(MONOB, 30), fill=(RED if on else GREY), anchor='lm')
            if k == 2: d.line((80, yy + 52, 1000, yy + 52), fill=AMBER, width=3); d.text((1000, yy + 56), 'linha do top 3', font=F(MONO, 22), fill=AMBER, anchor='ra')
    carimbo(d, t, '02', 1290)
    fontes(d, ['% de jogadores no Standard do WC32: magic.gg (128 listas)'], 1400)
    hud(d, t); return term_finish(im)
def scene_top8(t, champ=False):
    im, d = term_base(t, 14)
    header(d, '> TOP 8 · MUNDIAL 32', '  8 jogadores · 8 decks diferentes')
    for i, (n, pais, deck) in enumerate(TOP8):
        if t < ws(67) + i * .1: continue
        x, y = 80 + (i % 2) * 470, 330 + (i // 2) * 230; hi = champ and i == 1; ja = deck == 'Jund Sacrifice'
        d.rounded_rectangle((x, y, x + 450, y + 205), 14, outline=(PH if hi else (AMBER if ja else (40, 80, 70))), width=(5 if hi else 3), fill=(8, 20, 18, 255))
        d.text((x + 22, y + 22), pais, font=F(MONOB, 26), fill=EM)
        d.text((x + 225, y + 80), n, font=fit(d, n, CONDB, 40, 410), fill=WHITE, anchor='ma')
        d.text((x + 225, y + 140), deck, font=fit(d, deck, MONOB, 30, 410), fill=(PH if hi else (AMBER if ja else GREY)), anchor='ma')
    if t >= ws(73) - .05: d.text((W / 2, 1270), '8 ARQUÉTIPOS DIFERENTES', font=fit(d, '8 ARQUÉTIPOS DIFERENTES', INTB, 70, 940), fill=WHITE, anchor='ma')
    fontes(d, ['Top 8 e decks: magic.gg (Day Two Highlights, Top 8 Players and Decks)'], 1400)
    hud(d, t); return term_finish(im)
def scene_campeao(t):
    im, d = term_base(t, 10)
    header(d, '> CAMPEÃO DO MUNDO · WC32', '  Atlanta · 15/11/2026')
    if t < ws(80) - .1:
        k = (t - ws(76)) * 3
        d.text((W / 2, 700), '? ? ?', font=F(INTB, 200), fill=mix_bg(PH, int(120 + 100 * abs(math.sin(k)))), anchor='mm')
    elif t < ws(87) - .1:
        k = eio((t - ws(80) + .1) / .45); w_ = int(540 + 40 * k); ph = FOTO.resize((w_, int(w_ * FOTO.height / FOTO.width)), Image.LANCZOS)
        ph = ph.crop((0, 0, w_, min(ph.height, 820)))
        im.paste(ph, ((W - w_) // 2, 330)); d = ImageDraw.Draw(im, 'RGBA')
        d.rectangle(((W - w_) // 2 - 3, 327, (W + w_) // 2 + 3, 330 + ph.height + 3), outline=PH, width=4)
        d.text((W / 2, 1175), 'STEFAN SCHÜTZ', font=F(INTB, 92), fill=WHITE, anchor='ma')
        if t >= ws(82) - .05: d.text((W / 2, 1290), 'ÁUSTRIA · IZZET MISSION', font=F(MONOB, 44), fill=PH, anchor='ma')
    elif t < ws(98) - .1:
        th = FOTO.resize((150, int(150 * FOTO.height / FOTO.width)), Image.LANCZOS).crop((0, 0, 150, 170)); im.paste(th, (850, 330)); d = ImageDraw.Draw(im, 'RGBA')
        d.rectangle((848, 328, 1002, 502), outline=PH, width=3)
        d.text((80, 330), '2 / 128', font=F(INTB, 150), fill=PH)
        d.text((80, 500), 'jogadores com Izzet Mission · 1,6% do field', font=fit(d, 'jogadores com Izzet Mission · 1,6% do field', MONO, 30, 920), fill=GREY)
        verde = {'Anthropological Mission'} if t >= ws(95) else set()
        lista_col(d, t, 110, 560, LISTA[:1], ws(87), 400, verde, ls=40, fs=30)
        lista_col(d, t, 600, 560, LISTA[1:], ws(87) + .2, 380, verde, ls=40, fs=30)
    else:
        k = eio((t - ws(98) + .1) / .4); c = carta('anthropological_mission', int(460 + 40 * k))
        im.paste(c, ((W - c.width) // 2, 330)); d = ImageDraw.Draw(im, 'RGBA')
        y = 330 + c.height + 20
        d.text((W / 2, y), '4 CÓPIAS NA LISTA CAMPEÃ', font=F(MONOB, 38), fill=PH, anchor='ma')
        if t >= ws(107) - .05: d.text((W / 2, y + 60), 'STAR TREK (TRK) · Nº 46', font=F(MONOB, 34), fill=AMBER, anchor='ma')
    if t >= ws(98) - .1: fontes(d, ['campeão: magic.gg · carta: Scryfall (TRK 46, arte de Pablo Mendoza)', '«entrou no formato uma semana antes»: magic.gg (Day Two)'], 1384)
    elif t >= ws(87) - .1: fontes(d, ['lista: Melee via MTGTop8 · 2 de 128: metagame oficial, magic.gg'], 1400)
    else: fontes(d, ['campeão: magic.gg · foto usada com autorização do jogador'], 1400)
    hud(d, t); return term_finish(im)

# ---------- timeline ----------
DIVE = TL['DIVE']; DIVE_END = DIVE + 0.45; EXIT = TL['EXIT']; EXIT_END = EXIT + 0.75
SUBY = 1530
T_Q = ws(145) - 0.1; T_SIG = ws(156) - 0.15
def inside(t):
    if t < ws(25) - .1: return scene_arquivo(t)
    if t < ws(37) - .1: return scene_prev01(t)
    if t < ws(53) - .1: return scene_prev03(t)
    if t < ws(67) - .1: return scene_prev02(t)
    if t < ws(76) - .1: return scene_top8(t)
    return scene_campeao(t)
def frame_main(t):
    if t < DIVE_END:
        if t < DIVE:
            im = tubo_frame(t, 'desconfiado' if t >= ws(8) else 'analitico', zoom=1.0 + 0.04 * eio(t / 3.0))
            d = ImageDraw.Draw(im, 'RGBA')
            d.text((W / 2, 140), '3 PREVISÕES', font=F(INTB, 96), fill=WHITE, anchor='ma')
            if t >= ws(6) - .05: d.text((W / 2, 255), '2 ACERTOS', font=F(INTB, 96), fill=PH, anchor='ma')
            if t >= ws(8) - .05: d.text((W / 2, 370), 'NENHUM ERA O CAMPEÃO', font=fit(d, 'NENHUM ERA O CAMPEÃO', MONOB, 54, 960), fill=AMBER, anchor='ma')
            note(d, 'previsões do TUBO registradas em 10/11 · Mundial 32')
            return subs(im, t, SUBY)
        k = eio((t - DIVE) / (DIVE_END - DIVE)); z = 1 + k * 4.2
        im = tubo_frame(t, 'analitico', zoom=z, cx=W / 2 + (SCX - W / 2) * min(1, k * 1.5), cy=H / 2 + (SCY - H / 2) * min(1, k * 1.5))
        if k > 0.6: im = Image.blend(im, scene_arquivo(t), (k - 0.6) / 0.4)
        return im
    if t < EXIT:
        if TL['REV0'] <= t < TL['REV1']:          # corte seco: aproximação lenta à foto
            im = inside(t); kz = (t - TL['REV0']) / (TL['REV1'] - TL['REV0']); z = 1 + 0.035 * kz
            cw, ch = W / z, H / z; return subs(im.resize((W, H), Image.LANCZOS, box=((W - cw) / 2, 500 - 500 / z, (W + cw) / 2, 500 - 500 / z + ch)), t)
        return subs(inside(t), t)
    if t < EXIT_END:
        k = eio((t - EXIT) / (EXIT_END - EXIT)); z = 5.2 - 4.2 * k
        im = tubo_frame(t, 'analitico', zoom=z, cx=W / 2 + (SCX - W / 2) * (1 - k), cy=H / 2 + (SCY - H / 2) * (1 - k))
        if k < 0.35: im = Image.blend(inside(t), im, k / 0.35)
        return subs(im, t, SUBY)
    if t < T_Q:
        expr = 'confiante' if t >= ws(141) - .05 else ('desconfiado' if t >= ws(129) else 'analitico')
        im = tubo_frame(t, expr, zoom=1.0); d = ImageDraw.Draw(im, 'RGBA')
        if t < ws(141) - .05:
            s1, s2 = 'OS DADOS ESCOLHEM O DECK.', 'NÃO QUEM PILOTA.'
            d.text((W / 2, 110), 'EP07 · leitura do TUBO', font=F(MONO, 30), fill=GREY, anchor='ma')
            d.text((W / 2, 155), s1, font=fit(d, s1, INTB, 58, 940), fill=GREY, anchor='ma')
            d.text((W / 2, 230), s2, font=fit(d, s2, INTB, 58, 940), fill=GREY, anchor='ma')
            if t >= ws(131) - .05:
                for yy, s_ in ((190, s1), (265, s2)):
                    f = fit(d, s_, INTB, 58, 940); wd = d.textlength(s_, font=f); d.line((W / 2 - wd / 2, yy, W / 2 + wd / 2, yy), fill=RED, width=7)
                d.text((W / 2, 315), 'QUEM PILOTA ESCOLHEU', font=F(INTB, 64), fill=PH, anchor='ma')
                d.text((W / 2, 392), 'O DECK QUE OS DADOS NÃO VIAM', font=fit(d, 'O DECK QUE OS DADOS NÃO VIAM', MONOB, 44, 960), fill=WHITE, anchor='ma')
            note(d, 'tese revista · não é previsão registrada, não muda o placar')
        else:
            d.text((W / 2, 170), 'PLACAR', font=F(MONOB, 44), fill=GREY, anchor='ma')
            d.text((W / 2, 220), '2 / 3', font=F(INTB, 160), fill=PH, anchor='ma')
            for i, (pid, ok) in enumerate([('01', True), ('03', True), ('02', False)]):
                x = 120 + i * 290; d.rounded_rectangle((x, 420, x + 260, 480), 30, fill=(15, 23, 42, 230), outline=(EM if ok else RED), width=3)
                d.text((x + 130, 450), f'{pid} {"✔" if ok else "✘"}', font=F(MONOB, 36), fill=(PH if ok else RED), anchor='mm')
            note(d, 'PR-WC32-01 (pública) e 03 confirmadas · 02 refutada')
        return subs(im, t, SUBY)
    if t < T_SIG:
        im = tubo_frame(t, 'analitico', zoom=1.0); d = ImageDraw.Draw(im, 'RGBA')
        q1, q2 = 'Você levaria ao Mundial um deck', 'que só 2 jogadores levaram?'
        d.text((W / 2, 170), q1, font=fit(d, q1, INTB, 60, 960), fill=WHITE, anchor='ma')
        d.text((W / 2, 250), q2, font=fit(d, q2, INTB, 60, 960), fill=PH, anchor='ma')
        for i, s_ in enumerate(['SIM', 'NÃO']):
            if t < ws(152) + i * .12: continue
            x = 250 + i * 320; on = t >= ws(155) - .05
            d.rounded_rectangle((x, 350, x + 260, 420), 35, fill=((10, 52, 30, 255) if on else (15, 23, 42, 230)), outline=EM, width=3)
            d.text((x + 130, 385), s_, font=F(MONOB, 40), fill=(PH if on else WHITE), anchor='mm')
        if t >= ws(155) - .05: note(d, 'responda SIM ou NÃO')
        return subs(im, t, SUBY)
    kz = eio((t - T_SIG) / 1.2)
    im = tubo_frame(t, 'confiante', zoom=1.0 + 0.22 * kz, cx=W / 2, cy=H / 2 + (SCY + 260 - H / 2) * kz)
    k = ease((t - T_SIG) / 0.4)
    im = top_card(im, [('META EM CURTO', F(INTB, 96), WHITE), ('com TUBO · BINDER Originals', F(MONO, 34), EM)], k, 225)
    return subs(im, t, SUBY)
def capa():
    im = Image.new('RGBA', (W, H), BG + (255,))
    bgc = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for sl, ang, x, y in [('ral_crackling_wit', 12, -110, 560), ('anthropological_mission', 0, 300, 470), ('into_the_flood_maw', -12, 700, 560)]:
        c = carta(sl, 440).convert('RGBA').rotate(ang, resample=Image.BICUBIC, expand=True); bgc.alpha_composite(c, (x, y))
    bgc = bgc.filter(ImageFilter.GaussianBlur(3)); im.alpha_composite(bgc); im.alpha_composite(Image.new('RGBA', (W, H), BG + (175,)))
    # TUBO confiante (acertou 2 de 3), à esquerda; foto do campeão à direita (elemento de apoio)
    tb = tubo_frame(12.0, 'confiante', zoom=1.0).convert('RGBA').crop((150, 380, 930, 1500)).resize((560, 804), Image.LANCZOS)
    m = Image.new('L', tb.size, 0); ImageDraw.Draw(m).ellipse((30, 25, tb.width - 30, tb.height + 250), fill=255)
    tb.putalpha(m.filter(ImageFilter.GaussianBlur(40))); im.alpha_composite(tb, (-10, 820))
    ph = FOTO.resize((470, int(470 * FOTO.height / FOTO.width)), Image.LANCZOS).crop((0, 0, 470, 640)).convert('RGBA')
    pm = Image.new('L', ph.size, 255); pd = ImageDraw.Draw(pm)
    for i in range(80): pd.line((0, ph.height - 1 - i, ph.width, ph.height - 1 - i), fill=int(255 * i / 80))
    ph.putalpha(pm); im.alpha_composite(ph, (560, 905))
    d = ImageDraw.Draw(im, 'RGBA')
    d.rounded_rectangle((585, 1470, 1010, 1540), 12, fill=(5, 10, 16, 230), outline=PH, width=3)
    d.text((797, 1505), 'SÓ 2 EM 128 JOGARAM', font=fit(d, 'SÓ 2 EM 128 JOGARAM', MONOB, 32, 400), fill=PH, anchor='mm')
    d.text((W / 2, 330), 'DECK DO CAMPEÃO', font=fit(d, 'DECK DO CAMPEÃO', INTB, 112, 980), fill=WHITE, anchor='mm')
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.text((W / 2, 610), '1,6%', font=F(INTB, 360), fill=PH + (200,), anchor='mm'); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(28)))
    d = ImageDraw.Draw(im, 'RGBA'); d.text((W / 2, 610), '1,6%', font=F(INTB, 360), fill=PH, anchor='mm')
    d.rectangle((0, 1572, W, 1662), fill=(5, 10, 16, 235)); d.line((0, 1572, W, 1572), fill=PH, width=4)
    d.text((60, 1617), 'META EM CURTO · EP. 08', font=F(MONOB, 40), fill=PH, anchor='lm')
    d.text((W - 60, 1617), 'PLACAR 2/3', font=F(MONOB, 40), fill=AMBER, anchor='rm')
    im.convert('RGB').save('EP08_CAPA.png'); im.convert('RGB').crop((0, 240, W, 1680)).save('EP08_CAPA_grelha.png')
if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[2] == 'capa': capa(); sys.exit()
    if len(sys.argv) > 2 and sys.argv[2] == 'stills':
        for tt in map(float, sys.argv[3:]): frame(tt).save(f'still_{tt:05.2f}.png')
        sys.exit()
    nf = int(round(TOTAL * FPS))
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-i', 'mix_final.wav', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
                          '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', '-shortest', 'EP08_META_EM_CURTO.mp4'],
                         stdin=subprocess.PIPE)
    for i in range(nf): p.stdin.write(frame(i / FPS).convert('RGB').tobytes())
    p.stdin.close(); p.wait(); print('done', nf)
