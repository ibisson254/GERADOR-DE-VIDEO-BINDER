# Meta em Curto EP07 · Mundial 32 · capa v2 no modelo fixo (oraculo/CONTEXTO.md §7.3, 14/11/2026)
# Standalone (não precisa das saídas de áudio). Uso, a partir de qualquer pasta:
#   python3 -I ep07_capa.py /caminho/do/repo   -> EP07_CAPA.png + EP07_CAPA_grelha.png
# Fundo: cartas reais do Jund Sacrifice citado no episódio (já no repositório, Scryfall).
import sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
K = (sys.argv[1] if len(sys.argv) > 1 else '../..').rstrip('/') + '/'
W, H = 1080, 1920
BG = (5, 10, 16); EM = (16, 185, 129); PH = (0, 255, 65); WHITE = (236, 241, 245); AMBER = (255, 176, 32)
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'; MONOB = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
INTB = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
def F(p, s): return ImageFont.truetype(p, s)
def fit(d, s, path, size, maxw):
    while size > 20 and d.textlength(s, font=F(path, size)) > maxw: size -= 2
    return F(path, size)

# --- TUBO em «Confiante» (mesma geometria dos renders da série) ---
SCR = (492, 566, 740, 792); EYES = [(518, 615, 596, 702), (634, 615, 709, 702)]; LED = (592, 828)
def tubo_confiante():
    im = Image.open(K + 'oraculo/assets/tubo_mestra_916.png').convert('RGB'); d = ImageDraw.Draw(im, 'RGBA'); fs = F(MONO, 13)
    for i, x in enumerate(range(500, 736, 14)):                       # chuva de código no ecrã
        y0 = SCR[1] + (i * 37) % (SCR[3] - SCR[1])
        for k in range(5):
            yy = y0 - k * 15
            if SCR[1] + 8 < yy < SCR[3] - 14 and not any(e[0] - 6 < x < e[2] + 6 and e[1] - 8 < yy < e[3] + 4 for e in EYES):
                d.text((x, yy), '0123456789ABCDEF'[(i + k) % 16], font=fs, fill=(0, 255, 65, int(90 * (1 - k / 5))))
    for i, e in enumerate(EYES):                                        # pálpebras do Confiante
        h = (e[3] - e[1] + 4) * 0.22 * (0.4 if i == 1 else 1)
        d.rectangle((e[0] - 3, e[1] - 3, e[2] + 3, e[1] - 3 + h), fill=BG + (255,))
        d.line((e[0] - 3, e[1] - 3 + h, e[2] + 3, e[1] - 3 + h), fill=(16, 185, 129, 160), width=3)
    g = Image.new('RGBA', (120, 120), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((40, 40, 80, 80), fill=EM + (200,))
    g = g.filter(ImageFilter.GaussianBlur(14)); im.paste(g, (LED[0] - 60, LED[1] - 60), g)
    d.ellipse((LED[0] - 6, LED[1] - 6, LED[0] + 6, LED[1] + 6), fill=(120, 255, 190, 255))
    return im

def carta(p, w):
    c = Image.open(K + p).convert('RGBA'); return c.resize((w, int(w * c.height / c.width)), Image.LANCZOS)

im = Image.new('RGBA', (W, H), BG + (255,))
# fundo: leque das cartas do Jund Sacrifice, desfocado e escurecido
bgc = Image.new('RGBA', (W, H), (0, 0, 0, 0))
CARTAS = ['oraculo/ep02/cartas/biotech_specialist.png', 'oraculo/ep02/cartas/the_sackvillebagginses.png',
          'oraculo/ep04/cartas/umbral_collar_zealot.png', 'oraculo/ep02/cartas/lively_dirge.png']
for p, ang, x, y in zip(CARTAS, (14, 5, -5, -14), (-120, 160, 470, 760), (560, 470, 470, 560)):
    bgc.alpha_composite(carta(p, 420).rotate(ang, resample=Image.BICUBIC, expand=True), (x, y))
im.alpha_composite(bgc.filter(ImageFilter.GaussianBlur(3)))
im.alpha_composite(Image.new('RGBA', (W, H), BG + (170,)))
# TUBO confiante (a previsão está registada), bordas esbatidas
tb = tubo_confiante().convert('RGBA').crop((150, 380, 930, 1500)).resize((700, 1005), Image.LANCZOS)
m = Image.new('L', tb.size, 0); ImageDraw.Draw(m).ellipse((40, 30, tb.width - 40, tb.height + 300), fill=255)
tb.putalpha(m.filter(ImageFilter.GaussianBlur(45))); im.alpha_composite(tb, ((W - tb.width) // 2, 820))
d = ImageDraw.Draw(im, 'RGBA')
# 1) frase
FR = 'BRASILEIROS NO MUNDIAL'
d.text((W / 2, 330), FR, font=fit(d, FR, INTB, 112, 980), fill=WHITE, anchor='mm')
# 2) ponto focal: 6, com brilho
g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).text((W / 2, 610), '6', font=F(INTB, 460), fill=PH + (200,), anchor='mm')
im.alpha_composite(g.filter(ImageFilter.GaussianBlur(28))); d = ImageDraw.Draw(im, 'RGBA')
d.text((W / 2, 610), '6', font=F(INTB, 460), fill=PH, anchor='mm')
# 3) elemento de apoio: a pergunta do episódio em carimbo âmbar, junto do TUBO
st = Image.new('RGBA', (330, 150), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
sd.rounded_rectangle((6, 6, 324, 144), 20, outline=AMBER, width=8, fill=(30, 20, 4, 230))
sd.text((165, 75), 'TOP 8?', font=F(INTB, 84), fill=AMBER, anchor='mm')
im.alpha_composite(st.rotate(-10, resample=Image.BICUBIC, expand=True), (700, 900)); d = ImageDraw.Draw(im, 'RGBA')
# 4) faixa fixa da série
d.rectangle((0, 1572, W, 1662), fill=(5, 10, 16, 235)); d.line((0, 1572, W, 1572), fill=PH, width=4)
d.text((60, 1617), 'META EM CURTO · EP. 07', font=F(MONOB, 40), fill=PH, anchor='lm')
im.convert('RGB').save('EP07_CAPA.png')
im.convert('RGB').crop((0, 240, W, 1680)).save('EP07_CAPA_grelha.png')
print('ok')
