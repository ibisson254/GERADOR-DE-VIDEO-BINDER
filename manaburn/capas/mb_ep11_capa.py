# Mana & Burn · MB-EP11 «O dragão flanelinha» (Numot) · capa no modelo de um ponto focal (adaptado do Meta em Curto, CONTEXTO §7.3)
# Uso: python3 mb_ep11_capa.py <quadro_10s.png> <numot.png> <Bangers.ttf> <saida.png>
#   quadro_10s.png = quadro do kit (manaburn/index.html com o episode.js/data.js de ep10_numot) a 10,0 s: Burn de braços no ar, Mana ao lado.
#   Bangers.ttf = fonte da série (node_modules/@fontsource/bangers, convertida de woff2).
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H = 1080, 1920
YEL = (255, 216, 74); RED = (226, 59, 46); INK = (18, 14, 12); WHITE = (250, 246, 236)
fr, card, fontp, out = sys.argv[1:5]
F = lambda s: ImageFont.truetype(fontp, s)
im = Image.new('RGBA', (W, H), INK + (255,))
cena = Image.open(fr).convert('RGBA').crop((0, 300, W, 1290))          # sem tarja nem legenda do quadro
cena = cena.resize((int(W * 1.12), int(cena.height * 1.12)), Image.LANCZOS)
im.alpha_composite(cena, ((W - cena.width) // 2, 1680 - cena.height + 40))
g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
for y in range(0, 1000):                                                   # escurece o topo para o texto
    a = 255 if y < 640 else int(255 * max(0, 1 - (y - 640) / 360))
    gd.line((0, y, W, y), fill=INK + (a,))
im.alpha_composite(g)
d = ImageDraw.Draw(im)
def txt(xy, s, size, fill, anchor='mm', stroke=10):
    d.text(xy, s, font=F(size), fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=INK)
txt((W / 2, 330), 'O DRAGÃO QUE COME', 118, WHITE)                          # 1) frase
gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(gl).text((W / 2, 545), 'TERRENO', font=F(300), fill=YEL + (190,), anchor='mm')
im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(26))); d = ImageDraw.Draw(im)
txt((W / 2, 545), 'TERRENO', 300, YEL, stroke=14)                          # 2) foco
c = Image.open(card).convert('RGBA'); c = c.resize((300, int(c.height * 300 / c.width)), Image.LANCZOS)
c = c.rotate(-9, resample=Image.BICUBIC, expand=True)
sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((W - c.width - 70, 720, W, 1280), fill=INK + (215,))
im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(40)))              # sombra: esconde a TV repetida atrás da carta
im.alpha_composite(c, (W - c.width - 25, 760))                           # 3) apoio: o Numot
d = ImageDraw.Draw(im)
d.rounded_rectangle((W - 330, 1150, W - 40, 1230), 16, fill=RED, outline=INK, width=6)
txt((W - 185, 1192), '−2 POR PANCADA', 50, WHITE, stroke=4)
d.rectangle((0, 1572, W, H), fill=INK); d.line((0, 1572, W, 1572), fill=YEL, width=6)   # 4) faixa fixa da série
txt((60, 1619), 'MANA & BURN · EP. 11', 62, YEL, anchor='lm', stroke=0)
txt((W - 60, 1619), 'COMMANDER', 62, WHITE, anchor='rm', stroke=0)
im.convert('RGB').save(out)
im.convert('RGB').crop((0, 240, W, 1680)).save(out.replace('.png', '_grelha.png'))
