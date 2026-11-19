"""Prepara a Lisa (look 1) em camadas para a prova de estilo.

Gera:
  lisa_base.png      corpo recortado, sem boca (pelo reconstruído por inpainting)
  bocas/<X>.png      bocas provisórias A–H e X (formas de Rhubarb), mesmo tamanho da base
  palpebra_<n>.png   pálpebras para o piscar (0.5 e 1.0)
Coordenadas no espaço 4x do recorte (1048x2052).
"""
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw

SRC = 'look1_recorte_4x.png'
im = Image.open(SRC).convert('RGBA')
W, H = im.size
arr = np.array(im)

# 1) Tirar a legenda da prancha e o resto do papel junto ao telemóvel
arr[1800:, :, 3] = 0
rgb = arr[:, :, :3].astype(int)
lum = rgb.mean(axis=2)
sat = rgb.max(axis=2) - rgb.min(axis=2)
papel = (lum > 175) & (sat < 60)
zona = np.zeros_like(papel)
zona[640:1040, 905:] = True
zona[790:1045, 775:] = True
zona[700:800, 860:] = True
arr[papel & zona, 3] = 0
claro = np.zeros_like(papel)
claro[635:720, 985:] = True
arr[claro & (lum > 90), 3] = 0          # mancha rosa da prancha

# 2) Apagar a boca original (inpainting do pelo claro)
x0, y0, x1, y1 = 650, 668, 770, 730
bgr = cv2.cvtColor(arr[:, :, :3], cv2.COLOR_RGB2BGR)
reg = bgr[y0:y1, x0:x1]
g = cv2.cvtColor(reg, cv2.COLOR_BGR2GRAY)
mask_reg = (g < 212).astype(np.uint8) * 255
mask_reg = cv2.dilate(mask_reg, np.ones((5, 5), np.uint8), iterations=2)
mask = np.zeros(bgr.shape[:2], np.uint8)
mask[y0:y1, x0:x1] = mask_reg
out = cv2.inpaint(bgr, mask, 9, cv2.INPAINT_TELEA)
arr[:, :, :3] = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)
Image.fromarray(arr).save('lisa_base.png')

# 3) Bocas provisórias (Preston Blair / Rhubarb). Centro abaixo do nariz.
CX, CY = 722, 690
LINHA = (58, 26, 34, 255)
INTERIOR = (78, 22, 38, 255)
LINGUA = (226, 118, 140, 255)
DENTES = (246, 240, 232, 255)
os.makedirs('bocas', exist_ok=True)


def tela():
    c = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    return c, ImageDraw.Draw(c)


def filtro(d):
    # risco do nariz à boca (como no desenho original)
    d.line([(733, 662), (728, CY - 2)], fill=LINHA, width=4)


def omega(d, larg=34, alt=8):
    d.arc([CX - larg, CY - alt, CX, CY + alt], 10, 170, fill=LINHA, width=5)
    d.arc([CX, CY - alt, CX + larg, CY + alt], 10, 170, fill=LINHA, width=5)


def aberta(d, larg, alt, lingua=True, dentes=False, redonda=False):
    if redonda:
        box = [CX - larg, CY - alt * 0.4, CX + larg, CY + alt * 1.6]
        d.ellipse(box, fill=INTERIOR, outline=LINHA, width=5)
    else:
        top = CY - 2
        pts = [(CX - larg, top), (CX - larg * 0.45, top + 3), (CX, top - 2),
               (CX + larg * 0.45, top + 3), (CX + larg, top),
               (CX + larg * 0.7, top + alt * 0.8), (CX, top + alt),
               (CX - larg * 0.7, top + alt * 0.8)]
        d.polygon(pts, fill=INTERIOR, outline=LINHA)
        d.line(pts + [pts[0]], fill=LINHA, width=5, joint='curve')
        box = [CX - larg, top, CX + larg, top + alt]
    if dentes:
        d.rectangle([CX - larg * 0.55, box[1] + 4, CX + larg * 0.55, box[1] + 4 + max(5, alt * 0.22)], fill=DENTES)
    if lingua and alt > 16:
        d.ellipse([CX - larg * 0.45, box[1] + alt * 0.55, CX + larg * 0.45, box[1] + alt * 1.15], fill=LINGUA)
        # recortar a língua ao interior: redesenhar contorno por cima
        if redonda:
            d.ellipse(box, outline=LINHA, width=5)


formas = {
    'A': lambda d: omega(d, 30, 6),                      # M B P: fechada
    'X': lambda d: omega(d, 34, 8),                      # repouso
    'B': lambda d: aberta(d, 30, 12, lingua=False, dentes=True),   # K S T
    'C': lambda d: aberta(d, 36, 26),                    # EH AE
    'D': lambda d: aberta(d, 42, 40),                    # AA bem aberta
    'E': lambda d: aberta(d, 26, 24, redonda=True),      # AO ER
    'F': lambda d: aberta(d, 15, 14, lingua=False, redonda=True),  # UW OW W
    'G': lambda d: aberta(d, 30, 14, lingua=False, dentes=True),   # F V
    'H': lambda d: aberta(d, 34, 30),                    # L
}
for k, f in formas.items():
    c, d = tela()
    filtro(d)
    f(d)
    c.save(f'bocas/{k}.png')

# 4) Pálpebras: só cobrem os píxeis do olho (íris, branco, brilho) dentro da abertura
OLHOS = [((590, 543), (90, 56)), ((825, 618), (50, 47))]
PELO = (22, 17, 22, 255)
base = np.array(Image.open('lisa_base.png').convert('RGBA'))
lumb = base[:, :, :3].astype(int).mean(axis=2)
yy, xx = np.mgrid[0:H, 0:W]
for frac in (0.5, 1.0):
    lid = np.zeros((H, W), bool)
    for (cx, cy), (rx, ry) in OLHOS:
        dentro = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1
        olho = dentro
        ys = np.where(olho.any(axis=1))[0]
        topo, fundo = ys.min(), ys.max()
        corte = topo + (fundo - topo) * frac
        lid |= olho & (yy <= corte)
    m = cv2.GaussianBlur(lid.astype(np.uint8) * 255, (5, 5), 0)
    c = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    c.paste(Image.new('RGBA', (W, H), PELO), (0, 0), Image.fromarray(m))
    d = ImageDraw.Draw(c)
    for (cx, cy), (rx, ry) in OLHOS:
        if frac < 1.0:
            yb = cy - ry + 2 * ry * frac
            d.line([(cx - rx * 0.87, yb), (cx + rx * 0.87, yb)], fill=(6, 4, 6, 255), width=5)
        if frac == 1.0:
            d.arc([cx - rx * 0.8, cy - ry * 0.9, cx + rx * 0.8, cy + ry * 0.55], 20, 160, fill=(120, 108, 118, 255), width=4)
    c.save(f'palpebra_{int(frac * 100)}.png')
print('ok')
