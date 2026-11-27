# MC-EP09 · capa «bandeira» (pedido do fundador, 27/11/2026 16:14): bandeira de Portugal em tecido, cartas reais do
# campeão, logótipo real da Mercadia e o TUBO. Sem logótipos da Wizards nem verso de carta (Política de Conteúdo de Fãs).
# Uso: python3 -I capa_bandeira.py <raiz do repo> <bandeira.png (flag-icons pt 4x3, MIT, renderizada)> <saída.png>
import sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

K = sys.argv[1].rstrip('/') + '/'; E = K + 'oraculo/episodios/ep09_mercadia_cedh/'
W, H = 1080, 1920
BG = np.array([5, 10, 16], np.float32); PH = (0, 255, 65); EM = (16, 185, 129); WHITE = (240, 243, 245)
INT = '/usr/share/fonts/opentype/inter/'
def F(n, s): return ImageFont.truetype(INT + n, s)
rng = np.random.default_rng(9)

# ---------- 1 · bandeira em tecido (ondas + sombras de dobras), recortada para a esfera armilar ficar em cima à esquerda ----------
fl = Image.open(sys.argv[2]).convert('RGB').resize((2400, 1800), Image.LANCZOS)
fa = np.asarray(fl).astype(np.float32)
# correção de cor: vermelho e verde oficiais mais profundos (não o RGB puro do SVG)
red = (fa[..., 0] > 200) & (fa[..., 1] < 60); grn = (fa[..., 1] > 80) & (fa[..., 0] < 40)
fa[red] = [196, 18, 36]; fa[grn] = [0, 102, 52]
FH = 1080                                                              # zona da bandeira no ecrã
yy, xx = np.mgrid[0:FH, 0:W].astype(np.float32); u = xx / W; v = yy / FH
ph = 2 * np.pi * (u * 1.1 + v * .45)
disp = 26 * np.sin(ph + 1.1) + 13 * np.sin(2 * np.pi * (u * 2.4 - v * .6) + .4) + 6 * np.sin(2 * np.pi * (u * 4.7 + v * 1.9))
gx = np.gradient(disp, axis=1) + .6 * np.gradient(disp, axis=0)
S = 0.62                                                               # px do ecrã por px da bandeira; esfera (960,900) → (300, 400)
fx = 960 + (xx - 300) / S + disp * 1.9; fy = 900 + (yy - 400) / S + disp * 1.0
cloth = fa[np.clip(fy, 0, 1799).astype(int), np.clip(fx, 0, 2399).astype(int)]
shade = 1 + np.clip(gx, -4, 4) * .21
cloth = cloth * shade[..., None] * (1 - .22 * (0.5 + 0.5 * np.sin(ph + 2.7)))[..., None]
cloth += rng.normal(0, 4, cloth.shape[:2])[..., None]
can = np.zeros((H, W, 3), np.float32) + BG; can[:FH] = np.clip(cloth, 0, 255)
# a bandeira dissolve-se no fundo escuro (gradiente vertical + vinheta lateral)
g = np.clip((1060 - np.arange(H)) / 420, 0, 1).astype(np.float32) ** 1.3
lat = 1 - .35 * (np.abs(np.arange(W) - W / 2) / (W / 2)) ** 2
m = g[:, None] * lat[None, :]
can = BG + (can - BG) * m[..., None] * .92
im = Image.fromarray(np.clip(can, 0, 255).astype(np.uint8)).convert('RGBA')

# ---------- 2 · chuva de código do TUBO, muito ténue, só na zona escura ----------
lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay); fm = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 24)
GLY = '0123456789ABCDEF#*+=<>/:'
for x in range(14, W, 30):
    y0 = rng.uniform(700, 1700); n = int(rng.integers(6, 16))
    for k in range(n):
        y = y0 - k * 28
        if y > 760: dl.text((x, y), GLY[int(rng.integers(0, len(GLY)))], font=fm, fill=PH + (int(38 * (1 - k / n)),))
im.alpha_composite(lay)

# ---------- 3 · cartas do campeão em leque, com sombra ----------
def carta(f, w):
    c = Image.open(E + 'cartas/' + f).convert('RGB'); c = c.resize((w, int(w * c.height / c.width)), Image.LANCZOS)
    mk = Image.new('L', c.size, 0); ImageDraw.Draw(mk).rounded_rectangle((0, 0, c.width - 1, c.height - 1), int(w * .045), fill=255)
    c = c.convert('RGBA'); c.putalpha(mk); return c
def pousa(c, ang, cx, cy):
    r = c.rotate(ang, expand=True, resample=Image.BICUBIC)
    sh = Image.new('RGBA', (r.width + 120, r.height + 120), (0, 0, 0, 0)); a = r.getchannel('A')
    sh.paste((0, 0, 0, 190), (60, 80), a); sh = sh.filter(ImageFilter.GaussianBlur(26))
    im.alpha_composite(sh, (int(cx - r.width / 2 - 60), int(cy - r.height / 2 - 60)))
    im.alpha_composite(r, (int(cx - r.width / 2), int(cy - r.height / 2)))
pousa(carta('tymna.png', 330), 10, 880, 540)
pousa(carta('thrasios.png', 370), -5, 640, 610)

# ---------- 4 · tipografia ----------
d = ImageDraw.Draw(im)
def txt(xy, s, f, fill, anchor='la', sombra=True):
    if sombra:
        sl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sl).text((xy[0] + 4, xy[1] + 6), s, font=f, fill=(0, 0, 0, 200), anchor=anchor)
        im.alpha_composite(sl.filter(ImageFilter.GaussianBlur(6)))
    ImageDraw.Draw(im).text(xy, s, font=f, fill=fill, anchor=anchor)
M = 72
txt((M, 930), 'OFFICIAL P9Q SIDE QUEST · cEDH', F('Inter-Bold.otf', 34), (230, 236, 238))
txt((M, 972), 'SÓ ELE LEVOU', F('InterDisplay-Black.otf', 112), WHITE)
txt((M, 1088), 'E GANHOU.', F('InterDisplay-Black.otf', 112), PH)
# selo «1 DE 39» sobre as cartas
d = ImageDraw.Draw(im); bx, by = 64, 700
d.rounded_rectangle((bx, by, bx + 360, by + 150), 22, fill=(6, 16, 14, 245), outline=PH, width=6)
d.text((bx + 180, by + 62), '1 DE 39', font=F('InterDisplay-Black.otf', 76), fill=PH, anchor='mm')
d.text((bx + 180, by + 122), 'THRASIOS + TYMNA', font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 28), fill=WHITE, anchor='mm')
# loja: logótipo real + nome (local do torneio, sem «×»)
lg = Image.open(E + 'terceiros/mercadia_logo.png').convert('RGBA').resize((132, 132), Image.LANCZOS)
ring = Image.new('RGBA', (148, 148), (0, 0, 0, 0)); ImageDraw.Draw(ring).ellipse((2, 2, 145, 145), outline=(176, 138, 58, 255), width=4)
ly = 1250; im.alpha_composite(ring, (M - 8, ly - 8)); im.alpha_composite(lg, (M, ly))
txt((M + 160, ly + 20), 'cEDH NA', F('Inter-Bold.otf', 34), (200, 212, 216), sombra=False)
txt((M + 160, ly + 58), 'MERCADIA GAMES', F('InterDisplay-Black.otf', 52), WHITE, sombra=False)
# linha de informação com ícones desenhados
d = ImageDraw.Draw(im); y = 1408; f = F('Inter-SemiBold.otf', 31)
def pin(x, y):
    d.ellipse((x, y, x + 26, y + 26), outline=PH, width=4); d.polygon([(x + 3, y + 18), (x + 23, y + 18), (x + 13, y + 36)], fill=PH); d.ellipse((x + 8, y + 8, x + 18, y + 18), fill=(6, 16, 14))
def cal(x, y):
    d.rounded_rectangle((x, y + 4, x + 30, y + 34), 4, outline=PH, width=4); d.line((x, y + 13, x + 30, y + 13), fill=PH, width=4)
    for k in (8, 22): d.line((x + k, y, x + k, y + 8), fill=PH, width=4)
def gente(x, y):
    d.ellipse((x + 8, y, x + 22, y + 14), fill=PH); d.pieslice((x, y + 16, x + 30, y + 46), 180, 360, fill=PH)
def taca(x, y):
    d.pieslice((x + 2, y - 10, x + 28, y + 20), 0, 180, fill=PH); d.rectangle((x + 13, y + 18, x + 17, y + 28), fill=PH); d.rectangle((x + 6, y + 28, x + 24, y + 33), fill=PH)
for j, (ic, s) in enumerate(((pin, 'LISBOA · PORTUGAL'), (cal, '22.11.2026'), (gente, '39 JOGADORES'), (taca, '5 RODADAS + MESA FINAL'))):
    yy_ = y + j * 40; ic(M + 2, yy_ - 4); d.text((M + 52, yy_ + 14), s, font=f, fill=(226, 232, 235), anchor='lm')

# ---------- 5 · TUBO (imagem-mestra, sem alterações) a espreitar em baixo à direita ----------
tubo = Image.open(K + 'oraculo/assets/tubo_mestra_916.png').convert('RGBA').crop((230, 380, 1010, 1080)).resize((420, 377), Image.LANCZOS)
mk = Image.new('L', tubo.size, 0); ImageDraw.Draw(mk).ellipse((80, 30, tubo.width - 80, tubo.height + 200), fill=255); tubo.putalpha(mk.filter(ImageFilter.GaussianBlur(40)))
im.alpha_composite(tubo, (W - 400, 1200))

# ---------- 6 · faixa fixa da série (CONTEXTO §7.3) ----------
d = ImageDraw.Draw(im); d.rectangle((0, 1572, W, 1662), fill=(5, 10, 16, 245)); d.line((0, 1572, W, 1572), fill=EM, width=4)
d.text((60, 1617), 'META EM CURTO · EP. 09', font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 50), fill=EM, anchor='lm')
# grão final leve (une bandeira, cartas e texto)
a = np.asarray(im.convert('RGB')).astype(np.float32); a += rng.normal(0, 2.2, a.shape[:2])[..., None]
out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
out.save(sys.argv[3]); gr = out.crop((0, 240, W, 1680)); gr.save(sys.argv[3].replace('.png', '_grelha.png'))
print(sys.argv[3])
