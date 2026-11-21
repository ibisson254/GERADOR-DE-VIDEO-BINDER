"""Camadas v2 da Lisa (21/11/2026): cabeça separada do corpo, olhar com direção e bocas redesenhadas.

Parte das camadas da prova (kit/prova_recorte/camadas.py: lisa_base.png sem boca, palpebra_*.png)
e NÃO redesenha a personagem: só separa, desloca a íris e troca as bocas provisórias por outras
mais finas e próximas do traço. Continua a ser arte-conceito (262 px de origem).

uso: python3 -I camadas_v2.py PASTA_PROVA PASTA_SAIDA
Saída: corpo.png, cabeca_<olhar>.png (c, e, d, cima), bocas/<X>.png, palpebra_50.png, palpebra_100.png,
       pivo.json (pivô do pescoço, no espaço 4x de 1048x2052).
"""
import json
import os
import shutil
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(os.path.join(OUT, 'bocas'), exist_ok=True)
base = Image.open(os.path.join(SRC, 'lisa_base.png')).convert('RGBA')
W, H = base.size
A = np.array(base)

# ---------------------------------------------------------------- 1) olhar: deslocar a íris
IRIS = [((567, 538), 47, 1.0), ((810, 615), 33, 0.72)]        # (centro, raio, fator de deslocamento)
OLHOS = [((590, 543), (90, 56)), ((825, 618), (50, 47))]      # abertura (a mesma das pálpebras)
yy, xx = np.mgrid[0:H, 0:W]


def disco(c, r, pena=4):
    d = np.sqrt((xx - c[0]) ** 2 + (yy - c[1]) ** 2)
    return np.clip((r + pena - d) / pena, 0, 1)


def elipse(c, ax):
    return (((xx - c[0]) / ax[0]) ** 2 + ((yy - c[1]) / ax[1]) ** 2) <= 1.0


bgr = cv2.cvtColor(A[:, :, :3], cv2.COLOR_RGB2BGR)
m_inp = np.zeros((H, W), np.uint8)
for c, r, _ in IRIS:
    m_inp |= (disco(c, r + 3) > 0.01).astype(np.uint8) * 255
vazio = cv2.cvtColor(cv2.inpaint(bgr, m_inp, 7, cv2.INPAINT_TELEA), cv2.COLOR_BGR2RGB)

OLHAR = {'c': (0, 0), 'e': (-20, 3), 'd': (18, 2), 'cima': (-10, -9)}   # e = para a esquerda do ecrã


def com_olhar(dx, dy):
    out = A.copy()
    if dx == 0 and dy == 0:
        return out
    abertura = np.zeros((H, W), bool)
    for c, ax in OLHOS:
        abertura |= elipse(c, ax)
    out[:, :, :3] = np.where((m_inp > 0)[..., None] & abertura[..., None], vazio, out[:, :, :3])
    for c, r, f in IRIS:
        sx, sy = int(round(dx * f)), int(round(dy * f))
        mask = disco(c, r)
        M = np.float32([[1, 0, sx], [0, 1, sy]])
        patch = cv2.warpAffine(A[:, :, :3], M, (W, H), flags=cv2.INTER_LINEAR)
        mk = cv2.warpAffine(mask.astype(np.float32), M, (W, H)) * abertura
        out[:, :, :3] = (patch * mk[..., None] + out[:, :, :3] * (1 - mk[..., None])).astype(np.uint8)
    return out


# ---------------------------------------------------------------- 2) cabeça separada do corpo
PIVO = (712, 872)          # base do pescoço, entre o queixo e os auscultadores
COSTURA = (812, 900)       # faixa de transição (y): acima é cabeça, abaixo é corpo
t = np.clip((yy - COSTURA[0]) / (COSTURA[1] - COSTURA[0]), 0, 1)      # 0 = cabeça, 1 = corpo
lateral = (xx > 360) & (xx < 1048)                                    # o braço/telefone à direita é corpo
cab_alpha = np.where(lateral, 1 - t, 0.0)
cab_alpha[yy < COSTURA[0]] = 1.0
corpo_alpha = 1 - cab_alpha

corpo = A.copy()
corpo[:, :, 3] = (A[:, :, 3] * corpo_alpha).astype(np.uint8)
Image.fromarray(corpo).save(os.path.join(OUT, 'corpo.png'))
for nome, (dx, dy) in OLHAR.items():
    c = com_olhar(dx, dy)
    c[:, :, 3] = (A[:, :, 3] * cab_alpha).astype(np.uint8)
    Image.fromarray(c).save(os.path.join(OUT, f'cabeca_{nome}.png'))

# ---------------------------------------------------------------- 3) bocas v2 (mais finas, tinta quente, menos «autocolante»)
CX, CY = 722, 690
TINTA = (46, 22, 30, 255)
INTERIOR = (92, 34, 46, 255)
LINGUA = (214, 120, 132, 255)
DENTES = (240, 232, 222, 255)
LW = 3


def tela():
    c = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    return c, ImageDraw.Draw(c)


def filtro(d):
    d.line([(733, 664), (729, CY - 3)], fill=TINTA, width=LW)


def omega(d, larg, alt):
    d.arc([CX - larg, CY - alt, CX, CY + alt], 15, 165, fill=TINTA, width=LW + 1)
    d.arc([CX, CY - alt, CX + larg, CY + alt], 15, 165, fill=TINTA, width=LW + 1)


def aberta(d, larg, alt, lingua=True, dentes=False, redonda=False):
    top = CY - 1
    if redonda:
        box = [CX - larg, top - alt * 0.25, CX + larg, top + alt * 1.25]
        d.ellipse(box, fill=INTERIOR, outline=TINTA, width=LW)
        if lingua and alt > 14:
            d.chord([CX - larg * 0.6, box[1] + alt * 0.7, CX + larg * 0.6, box[3] + alt * 0.3], 180, 360, fill=LINGUA)
            d.ellipse(box, outline=TINTA, width=LW)
        return
    pts = [(CX - larg, top), (CX - larg * 0.4, top + 2), (CX, top - 1), (CX + larg * 0.4, top + 2), (CX + larg, top),
           (CX + larg * 0.62, top + alt * 0.85), (CX, top + alt), (CX - larg * 0.62, top + alt * 0.85)]
    d.polygon(pts, fill=INTERIOR)
    if dentes:
        d.polygon([(CX - larg * 0.7, top + 1), (CX + larg * 0.7, top + 1), (CX + larg * 0.55, top + max(4, alt * 0.3)),
                   (CX - larg * 0.55, top + max(4, alt * 0.3))], fill=DENTES)
    if lingua and alt > 14:
        d.chord([CX - larg * 0.5, top + alt * 0.5, CX + larg * 0.5, top + alt * 1.25], 180, 360, fill=LINGUA)
    d.line(pts + [pts[0]], fill=TINTA, width=LW, joint='curve')


FORMAS = {
    'X': lambda d: omega(d, 30, 7), 'A': lambda d: omega(d, 26, 5),
    'B': lambda d: aberta(d, 25, 10, lingua=False, dentes=True),
    'C': lambda d: aberta(d, 29, 20), 'D': lambda d: aberta(d, 33, 30),
    'E': lambda d: aberta(d, 20, 19, redonda=True), 'F': lambda d: aberta(d, 11, 11, lingua=False, redonda=True),
    'G': lambda d: aberta(d, 24, 11, lingua=False, dentes=True), 'H': lambda d: aberta(d, 28, 24),
}
for k, f in FORMAS.items():
    c, d = tela()
    filtro(d)
    f(d)
    c = c.filter(ImageFilter.GaussianBlur(0.9))         # aproxima a dureza do traço à da ilustração ampliada
    c.save(os.path.join(OUT, 'bocas', f'{k}.png'))

for p in ('palpebra_50.png', 'palpebra_100.png'):
    shutil.copy(os.path.join(SRC, p), os.path.join(OUT, p))
json.dump({'pivo': PIVO, 'costura': COSTURA, 'olhar': OLHAR}, open(os.path.join(OUT, 'pivo.json'), 'w'))
print('ok')
