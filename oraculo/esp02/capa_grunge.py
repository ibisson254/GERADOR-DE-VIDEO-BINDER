# Capa MC-ESP02 «A Taça respondeu» · estilo «cartaz grunge» (referência: capa do MC-EP08)
# Uso: python3 -I capa_grunge.py <repo> <pasta_fontes> <saida.png> [logo_magic.png]
import sys, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageChops

REPO, FONTS, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
random.seed(7); np.random.seed(7)
W, H = 1080, 1920
BG = (5, 10, 16)
LIME = (92, 255, 46)
LIME_D = (20, 120, 20)
WHITE = (240, 240, 234)
RED = (235, 40, 40)
INTB = '/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf'
ANTON = f'{FONTS}/Anton-Regular.ttf'
MARK = f'{FONTS}/PermanentMarker-Regular.ttf'
PIX = f'{FONTS}/VT323-Regular.ttf'
RUB = f'{FONTS}/RubikItalic.ttf'
CARD = f'{REPO}/oraculo/esp02/cartas'


def F(p, s, var=None):
    f = ImageFont.truetype(p, s)
    if var: f.set_variation_by_name(var)
    return f


def noise(w, h, scale, lo=0, hi=255):
    n = np.random.rand(max(2, h // scale), max(2, w // scale))
    im = Image.fromarray((n * 255).astype('uint8')).resize((w, h), Image.BICUBIC)
    return im


def grunge_alpha(alpha, holes=0.10, scale=5):
    """Abre falhas de tinta no alpha (textura de impressão gasta)."""
    w, h = alpha.size
    n = np.array(noise(w, h, scale)).astype(float) / 255
    n2 = np.array(noise(w, h, 40)).astype(float) / 255
    k = (n * 0.6 + n2 * 0.4)
    keep = (k > holes).astype(float)
    a = np.array(alpha).astype(float) * keep
    return Image.fromarray(a.astype('uint8'))


def torn_poly(x0, y0, x1, y1, amp=9, step=12):
    pts = []
    x = x0
    while x < x1: pts.append((x, y0 + random.uniform(-amp, amp))); x += random.uniform(step * .5, step * 1.5)
    y = y0
    while y < y1: pts.append((x1 + random.uniform(-amp, amp), y)); y += random.uniform(step * .5, step * 1.5)
    x = x1
    while x > x0: pts.append((x, y1 + random.uniform(-amp, amp))); x -= random.uniform(step * .5, step * 1.5)
    y = y1
    while y > y0: pts.append((x0 + random.uniform(-amp, amp), y)); y -= random.uniform(step * .5, step * 1.5)
    return pts


def paper(w, h, color, amp=10, dirt=40):
    """Tira de papel rasgado com textura."""
    pad = 30
    lay = Image.new('RGBA', (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    m = Image.new('L', lay.size, 0)
    ImageDraw.Draw(m).polygon(torn_poly(pad, pad, pad + w, pad + h, amp), fill=255)
    base = Image.new('RGB', lay.size, color)
    n = noise(*lay.size, 3); n2 = noise(*lay.size, 60)
    tex = ImageChops.multiply(n.convert('RGB'), n2.convert('RGB'))
    base = Image.blend(base, ImageChops.multiply(base, tex.point(lambda v: 255 - (255 - v) * dirt // 255).convert('RGB')), 1.0)
    lay.paste(base, (0, 0), m)
    # borda branca rasgada (fibra do papel)
    edge = m.filter(ImageFilter.MaxFilter(5)); edge = ImageChops.subtract(edge, m)
    lay.paste(Image.new('RGB', lay.size, (250, 250, 245)), (0, 0), edge.point(lambda v: v * 0.8))
    return lay


def shadow(layer, off=(10, 14), blur=14, op=180):
    a = layer.split()[-1].point(lambda v: v * op // 255)
    s = Image.new('RGBA', layer.size, (0, 0, 0, 0)); s.putalpha(a)
    s = s.filter(ImageFilter.GaussianBlur(blur))
    out = Image.new('RGBA', (layer.width + abs(off[0]) + 2 * blur, layer.height + abs(off[1]) + 2 * blur), (0, 0, 0, 0))
    out.alpha_composite(s, (blur + off[0], blur + off[1])); out.alpha_composite(layer, (blur, blur))
    return out, blur


def brush(w, h, color, density=60, angle=0):
    """Mancha de pincel seco (para tags e varridas)."""
    lay = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for i in range(density):
        y = random.uniform(h * .08, h * .92)
        x0 = random.uniform(-20, w * .12); x1 = random.uniform(w * .85, w + 20)
        d.line((x0, y + random.uniform(-8, 8), x1, y + random.uniform(-8, 8)), fill=color + (255,), width=random.randint(6, 22))
    a = lay.split()[-1]
    a = grunge_alpha(a.filter(ImageFilter.GaussianBlur(1)), holes=0.18, scale=3)
    lay.putalpha(a)
    return lay.rotate(angle, resample=Image.BICUBIC, expand=True)


def splatter(d, cx, cy, r, n, color):
    for _ in range(n):
        a = random.uniform(0, 2 * math.pi); dist = random.uniform(0, r) ** 1.0
        rr = random.uniform(1.5, 7) * (1 - dist / r) + 1
        x, y = cx + math.cos(a) * dist, cy + math.sin(a) * dist
        d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=color)


def card(slug, w):
    c = Image.open(f'{CARD}/{slug}.jpg').convert('RGBA')
    c = c.resize((w, int(w * c.height / c.width)), Image.LANCZOS)
    m = Image.new('L', c.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, c.width - 1, c.height - 1), int(w * .045), fill=255)
    c.putalpha(m); return c


def glow_outline(layer, color, grow=9, blur=16, strength=1.0):
    a = layer.split()[-1]
    big = a.filter(ImageFilter.MaxFilter(grow if grow % 2 else grow + 1))
    g = Image.new('RGBA', layer.size, color + (0,)); g.putalpha(big.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: min(255, int(v * 1.6 * strength))))
    line = Image.new('RGBA', layer.size, color + (0,)); line.putalpha(big)
    out = Image.new('RGBA', layer.size, (0, 0, 0, 0)); out.alpha_composite(g); out.alpha_composite(line); out.alpha_composite(layer)
    return out


def pad(layer, p):
    out = Image.new('RGBA', (layer.width + 2 * p, layer.height + 2 * p), (0, 0, 0, 0)); out.alpha_composite(layer, (p, p)); return out


im = Image.new('RGBA', (W, H), BG + (255,))
d = ImageDraw.Draw(im, 'RGBA')

# --- fundo: grelha fina + raios verdes + cartas reais desfocadas ---------------------------------
for x in range(0, W, 36): d.line((x, 0, x, H), fill=(16, 185, 129, 10))
for y in range(0, H, 36): d.line((0, y, W, y), fill=(16, 185, 129, 10))
rays = Image.new('RGBA', (W, H), (0, 0, 0, 0)); rd = ImageDraw.Draw(rays)
cx, cy = 540, 1150
for i in range(14):
    a0 = i * (2 * math.pi / 14) + random.uniform(-.08, .08); a1 = a0 + random.uniform(.10, .16)
    rd.polygon([(cx, cy), (cx + math.cos(a0) * 1600, cy + math.sin(a0) * 1600), (cx + math.cos(a1) * 1600, cy + math.sin(a1) * 1600)], fill=LIME_D + (random.randint(70, 120),))
rays.putalpha(grunge_alpha(rays.split()[-1], holes=.25, scale=4))
im.alpha_composite(rays.filter(ImageFilter.GaussianBlur(1.5)))
# fileira de comandantes ao fundo (as cartas reais do episódio, escurecidas)
row = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for i, s in enumerate(['jace', 'pantlaza', 'brass', 'shiko', 'jace', 'pantlaza']):
    c = card(s, 230); row.alpha_composite(c, (-70 + i * 205, 905))
row = row.filter(ImageFilter.GaussianBlur(2.2))
im.alpha_composite(row)
im.alpha_composite(Image.new('RGBA', (W, H), BG + (120,)))
# arte cinzenta no canto superior esquerdo (como a ilustração da referência)
art = Image.open(f'{CARD}/shiko.jpg').convert('L').crop((60, 100, 612, 520))
art = ImageOps.autocontrast(art).resize((520, 396), Image.LANCZOS).convert('RGBA')
fm = Image.new('L', art.size, 0); ImageDraw.Draw(fm).ellipse((-260, -200, 470, 380), fill=200)
art.putalpha(fm.filter(ImageFilter.GaussianBlur(60))); im.alpha_composite(art, (0, 0))
# vinheta
v = Image.new('L', (W, H), 0); ImageDraw.Draw(v).ellipse((-300, -200, W + 300, H + 250), fill=255)
vig = Image.new('RGBA', (W, H), (0, 0, 0, 255)); vig.putalpha(ImageOps.invert(v.filter(ImageFilter.GaussianBlur(160))).point(lambda x: int(x * .8)))
im.alpha_composite(vig)
# rasgões de papel escuro a cortar o fundo (camadas da referência)
for (y, ang) in [(500, -4), (1330, 3)]:
    p = paper(1300, 60, (14, 18, 22), amp=12, dirt=60).rotate(ang, resample=Image.BICUBIC, expand=True)
    im.alpha_composite(p, (-110, y))

d = ImageDraw.Draw(im, 'RGBA')

# --- topo: identidade do evento (no lugar do logo da referência) ---------------------------------
# logótipo do Magic (centro-topo): ficheiro fornecido pelo fundador (autorização dele, 16/11/2026), 4.º argumento opcional
if len(sys.argv) > 4:
    lg = Image.open(sys.argv[4]).convert('RGBA')
    lw = 410; lg = lg.resize((lw, int(lg.height * lw / lg.width)), Image.LANCZOS)
    sh = Image.new('RGBA', (lg.width + 120, lg.height + 120), (0, 0, 0, 0))
    sa = Image.new('L', sh.size, 0); sa.paste(lg.split()[-1], (60, 60))
    sh.putalpha(sa.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(22)).point(lambda v: min(255, v * 2)))
    lx, ly = (W - lg.width) // 2 - 95, 75
    im.alpha_composite(sh, (lx - 60, ly - 60)); im.alpha_composite(lg, (lx, ly))
# «META EM CURTO» a marcador, canto superior direito
mt = Image.new('RGBA', (360, 220), (0, 0, 0, 0)); md = ImageDraw.Draw(mt)
md.text((30, 10), 'META', font=F(MARK, 72), fill=WHITE)
md.text((40, 92), 'EM CURTO', font=F(MARK, 58), fill=LIME)
md.line((50, 178, 150, 172, 260, 160, 320, 150), fill=LIME, width=7, joint='curve')
mt = mt.rotate(7, resample=Image.BICUBIC, expand=True)
im.alpha_composite(mt, (720, 20))

# --- 1) frase em papel rasgado ---------------------------------------------------------------------
pw, ph = 1010, 196
pp = paper(pw, ph, (232, 232, 226), amp=11, dirt=70)
td = ImageDraw.Draw(pp)
txt = 'QUEM COMEÇA VENCE'
s = 150
while F(ANTON, s).getlength(txt) > pw - 70: s -= 2
tl = Image.new('RGBA', pp.size, (0, 0, 0, 0)); tld = ImageDraw.Draw(tl)
tld.text((pp.width / 2, pp.height / 2 - 18), txt, font=F(ANTON, s), fill=(12, 12, 12), anchor='mm')
tl = tl.transform(tl.size, Image.AFFINE, (1, 0.12, -0.12 * tl.height / 2, 0, 1, 0), resample=Image.BICUBIC)  # itálico falso
tl.putalpha(grunge_alpha(tl.split()[-1], holes=.08, scale=2))
pp.alpha_composite(tl)
# sublinhado verde de pincel
ul = brush(330, 26, LIME, density=9)
pp.alpha_composite(ul, (pp.width - 400, pp.height - 52))
pp = pp.rotate(-2.2, resample=Image.BICUBIC, expand=True)
sp, b = shadow(pp, (8, 12), 12, 200)
im.alpha_composite(sp, ((W - sp.width) // 2 + 4, 255 - b))

# --- 2) foco: 66% gigante, grunge ------------------------------------------------------------------
num = '66%'
fnum = F(RUB, 465, 'Black Italic')
nl = Image.new('RGBA', (W + 200, 620), (0, 0, 0, 0)); nd = ImageDraw.Draw(nl)
ncx, ncy = nl.width // 2 - 10, 300
nd.text((ncx + 14, ncy + 18), num, font=fnum, fill=(0, 0, 0, 255), anchor='mm', stroke_width=26, stroke_fill=(0, 0, 0, 255))  # sombra dura
nd.text((ncx, ncy), num, font=fnum, fill=(0, 0, 0, 255), anchor='mm', stroke_width=24, stroke_fill=(0, 0, 0, 255))
fill = Image.new('RGBA', nl.size, (0, 0, 0, 0)); fd = ImageDraw.Draw(fill)
fd.text((ncx, ncy), num, font=fnum, fill=LIME + (255,), anchor='mm')
# arranhões e manchas escuras dentro do número
fa = fill.split()[-1]
tex = np.array(noise(*nl.size, 4)).astype(float) / 255 * .55 + np.array(noise(*nl.size, 50)).astype(float) / 255 * .45
dark = (tex < .26)
arr = np.array(fill).astype(float)
arr[dark, 0] *= .25; arr[dark, 1] *= .45; arr[dark, 2] *= .25
# brilho em cima (como verniz)
grad = np.linspace(1.15, .82, nl.height)[:, None]
arr[..., :3] = np.clip(arr[..., :3] * grad[..., None], 0, 255)
fill = Image.fromarray(arr.astype('uint8'))
fill.putalpha(grunge_alpha(fa, holes=.05, scale=2))
nl.alpha_composite(fill)
# arranhões finos
sd = ImageDraw.Draw(nl)
for _ in range(26):
    x0 = random.uniform(150, nl.width - 150); y0 = random.uniform(110, 500); L = random.uniform(30, 120); a = random.uniform(-.5, .5)
    sd.line((x0, y0, x0 + math.cos(a) * L, y0 + math.sin(a) * L), fill=(10, 40, 10, 150), width=random.randint(2, 4))
nl.putalpha(ImageChops.multiply(nl.split()[-1], Image.new('L', nl.size, 255)))
# brilho por trás
g = Image.new('RGBA', nl.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
gd.text((ncx, ncy), num, font=fnum, fill=LIME + (150,), anchor='mm', stroke_width=30)
gl = g.filter(ImageFilter.GaussianBlur(40))
nl2 = Image.new('RGBA', nl.size, (0, 0, 0, 0)); nl2.alpha_composite(gl); nl2.alpha_composite(nl)
nl2 = nl2.rotate(3, resample=Image.BICUBIC)
im.alpha_composite(nl2, (-104, 415))
# troféu-coroa (no lugar da coroa da referência): contorno a verde em cima do «%»
cr = Image.new('RGBA', (200, 170), (0, 0, 0, 0)); crd = ImageDraw.Draw(cr)
crd.arc((40, 10, 160, 120), 0, 180, fill=LIME, width=10)
crd.line((40, 64, 160, 64), fill=LIME, width=10)
crd.arc((10, 30, 54, 84), 90, 270, fill=LIME, width=8); crd.arc((146, 30, 190, 84), -90, 90, fill=LIME, width=8)
crd.line((100, 120, 100, 145), fill=LIME, width=10); crd.line((70, 150, 130, 150), fill=LIME, width=10)
cr = cr.rotate(14, resample=Image.BICUBIC, expand=True)
pass  # sem coroa: o troféu já está no topo

# --- 3) TUBO (esquerda) + comandantes (direita) ----------------------------------------------------
tb = Image.open(f'{REPO}/oraculo/assets/tubo_mestra_916.png').convert('RGB').crop((190, 460, 870, 1450))
arr = np.array(tb).astype(int)
dist = np.sqrt(((arr - np.array([11, 19, 38])) ** 2).sum(-1))
alpha = np.clip((dist - 14) * 9, 0, 255).astype('uint8')
am = Image.fromarray(alpha).filter(ImageFilter.MedianFilter(5))
# fecha o recorte (preenche buracos escuros dentro do corpo: ecrã, ranhuras)
filled = am.point(lambda v: 255 if v > 60 else 0).filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.MinFilter(15))
tb = tb.convert('RGBA'); tb.putalpha(filled.filter(ImageFilter.GaussianBlur(1)))
tb = tb.resize((int(tb.width * .86), int(tb.height * .86)), Image.LANCZOS)
tb = glow_outline(pad(tb, 50), LIME, grow=5, blur=14, strength=.45)
tb = tb.rotate(4, resample=Image.BICUBIC)

# comandantes em leque, à direita (os dois precons do episódio: Ahoy Mateys e Jeskai Striker)
cards = Image.new('RGBA', (620, 820), (0, 0, 0, 0))
c2 = card('shiko', 320).rotate(-10, resample=Image.BICUBIC, expand=True)
c1 = card('brass', 350).rotate(7, resample=Image.BICUBIC, expand=True)
c2g = glow_outline(pad(c2, 30), LIME, grow=5, blur=10, strength=.3)
c1g = glow_outline(pad(c1, 30), LIME, grow=5, blur=10, strength=.4)
cards.alpha_composite(c2g, (170, 10)); cards.alpha_composite(c1g, (0, 120))
sc, b = shadow(cards, (14, 18), 18, 210)
im.alpha_composite(sc, (560 - b, 950 - b))
st, b = shadow(tb, (12, 16), 18, 200)
im.alpha_composite(st, (-60 - b, 880 - b))

# carimbo «50%» riscado junto ao TUBO (a previsão errada)
stp = Image.new('RGBA', (300, 130), (0, 0, 0, 0)); spd = ImageDraw.Draw(stp)
spd.rounded_rectangle((6, 6, 294, 124), 16, outline=RED, width=8, fill=(30, 6, 8, 220))
spd.text((150, 66), '50%', font=F(RUB, 96, 'Black Italic'), fill=RED, anchor='mm')
spd.line((26, 104, 274, 30), fill=RED, width=11)
stp.putalpha(grunge_alpha(stp.split()[-1], holes=.12, scale=2))
stp = stp.rotate(12, resample=Image.BICUBIC, expand=True)
pass  # o 50% fica só no autocolante (um elemento de apoio)

d = ImageDraw.Draw(im, 'RGBA')
# salpicos verdes
for (x, y, r, n) in [(90, 1240, 120, 70), (1010, 960, 90, 40), (980, 1460, 120, 60), (220, 700, 80, 30)]:
    splatter(d, x, y, r, n, LIME + (200,))

# --- autocolante: «EU DISSE 50% / ERREI A CONTA» ---------------------------------------------------
sk = paper(480, 165, (10, 12, 14), amp=10, dirt=30)
skd = ImageDraw.Draw(sk)
skd.text((56, 58), 'EU DISSE', font=F(PIX, 68), fill=WHITE, anchor='lm')
wx = 60 + F(PIX, 68).getlength('EU DISSE ')
skd.text((wx, 58), '50%', font=F(PIX, 68), fill=RED, anchor='lm')
skd.line((wx - 6, 66, wx + F(PIX, 68).getlength('50%') + 6, 48), fill=RED, width=8)
sl = Image.new('RGBA', sk.size, (0, 0, 0, 0)); sld = ImageDraw.Draw(sl)
sld.text((52, 128), 'ERREI A CONTA', font=F(RUB, 60, 'Black Italic'), fill=LIME, anchor='lm')
sl.putalpha(grunge_alpha(sl.split()[-1], holes=.08, scale=2))
sk.alpha_composite(sl)
sk = sk.rotate(3, resample=Image.BICUBIC, expand=True)
ssk, b = shadow(sk, (8, 12), 12, 200)
im.alpha_composite(ssk, (24 - b, 1440 - b))
# seta para o 66% … não: para os comandantes (onde a Taça respondeu)
ar = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ad = ImageDraw.Draw(ar)
pts = [(470 + t * 140, 1560 - 60 * math.sin(t * 1.4)) for t in [i / 20 for i in range(21)]]
ad.line(pts, fill=LIME, width=11, joint='curve')
ex, ey = pts[-1]; px, py = pts[-4]; a = math.atan2(ey - py, ex - px)
ad.polygon([(ex + math.cos(a) * 26, ey + math.sin(a) * 26), (ex + math.cos(a + 2.4) * 34, ey + math.sin(a + 2.4) * 34), (ex + math.cos(a - 2.4) * 34, ey + math.sin(a - 2.4) * 34)], fill=LIME)

# --- tag de pincel verde: «230 JOGOS REAIS» (o «placar» deste episódio) --------------------------
tg = brush(420, 220, LIME, density=60, angle=-4)
tgl = Image.new('RGBA', tg.size, (0, 0, 0, 0)); tgd = ImageDraw.Draw(tgl)
tgd.text((tg.width / 2 + 6, 88), '230 JOGOS', font=F(MARK, 58), fill=(8, 8, 8), anchor='mm')
tgd.text((tg.width / 2 + 6, 160), 'NA TAÇA', font=F(MARK, 58), fill=(8, 8, 8), anchor='mm')
tgl = tgl.rotate(-6, resample=Image.BICUBIC)
tg.alpha_composite(tgl)
im.alpha_composite(tg, (W - tg.width - 16, 1585))

# --- faixa fixa da série ---------------------------------------------------------------------------
fy = 1832
bx = 48
for i, hh in enumerate([22, 36, 50]):
    d.rectangle((bx + i * 18, fy + 22 - hh, bx + i * 18 + 12, fy + 22), fill=LIME)
d.text((bx + 72, fy), 'META EM CURTO · ESP. 02', font=F(INTB, 44), fill=WHITE, anchor='lm')
d.text((bx + 72 + F(INTB, 44).getlength('META EM CURTO · ESP. 02  '), fy), '× PRECONAUTA', font=F(INTB, 44), fill=(255, 190, 60), anchor='lm')
d.line((bx, fy + 46, 760, fy + 46), fill=LIME, width=4)

# grão final
gr = noise(W, H, 1).convert('RGBA'); gr.putalpha(18)
im.alpha_composite(gr)
im.convert('RGB').save(OUT)
im.convert('RGB').crop((0, 240, W, 1680)).save(OUT.replace('.png', '_grelha.png'))
print('ok', OUT)
