# Mana & Burn · MB-EP11 «O dragão flanelinha» (Numot) · capa v2: só a carta, em tamanho de capa, com as letras por cima
# (pedido do fundador, 14/11/2026 02:52). Uso: python3 mb_ep11_capa.py <numot.png> <Bangers.ttf> <saida.png>
#   numot.png = Scryfall, Numot, the Devastator (Commander 2011) nº 215, imagem «png» (745×1040). Arte: Dan Dos Santos. © Wizards of the Coast.
#   Bangers.ttf = fonte da série (node_modules/@fontsource/bangers, convertida de woff2).
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H = 1080, 1920
YEL = (255, 216, 74); RED = (226, 59, 46); INK = (18, 14, 12); WHITE = (250, 246, 236)
card, fontp, out = sys.argv[1:4]
F = lambda s: ImageFont.truetype(fontp, s)
im = Image.new('RGBA', (W, H), INK + (255,))
c = Image.open(card).convert('RGBA')
c = c.resize((W, int(c.height * W / c.width)), Image.LANCZOS)            # carta na largura toda (1080×1508)
im.alpha_composite(c, (0, 210))
g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
for y in range(980, H):                                                   # escurece o texto de regras: as letras vivem aí, a arte fica livre
    gd.line((0, y, W, y), fill=INK + (int(235 * min(1, (y - 980) / 160)),))
gd2 = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(gd2).rectangle((0, 0, W, 300), fill=INK + (200,))
im.alpha_composite(g); im.alpha_composite(gd2.filter(ImageFilter.GaussianBlur(30)))
d = ImageDraw.Draw(im)
def txt(xy, s, size, fill, anchor='mm', stroke=10):
    d.text(xy, s, font=F(size), fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=INK)
txt((W / 2, 1185), 'O DRAGÃO QUE COME', 118, WHITE)                         # 1) frase
gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(gl).text((W / 2, 1395), 'TERRENO', font=F(290), fill=YEL + (190,), anchor='mm')
im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(26))); d = ImageDraw.Draw(im)
txt((W / 2, 1395), 'TERRENO', 290, YEL, stroke=14)                         # 2) foco
d.rounded_rectangle((W - 470, 860, W - 50, 960), 20, fill=RED, outline=INK, width=7)   # 3) selo sobre a arte
txt((W - 260, 911), '−2 POR PANCADA', 66, WHITE, stroke=5)
d.rectangle((0, 1572, W, H), fill=INK); d.line((0, 1572, W, 1572), fill=YEL, width=6)   # 4) faixa fixa da série
txt((60, 1619), 'MANA & BURN · EP. 11', 62, YEL, anchor='lm', stroke=0)
txt((W - 60, 1619), 'COMMANDER', 62, WHITE, anchor='rm', stroke=0)
im.convert('RGB').save(out)
im.convert('RGB').crop((0, 240, W, 1680)).save(out.replace('.png', '_grelha.png'))
