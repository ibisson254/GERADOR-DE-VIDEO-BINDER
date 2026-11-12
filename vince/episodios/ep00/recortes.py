"""Recorta o Vince do fundo cinza (flood fill a partir das bordas) para animar em fantoche."""
import sys
from collections import deque
import numpy as np
from PIL import Image, ImageFilter

REF = sys.argv[1]  # pasta vince/referencias
OUT = sys.argv[2]


def recortar(img, tol=26):
    a = np.asarray(img.convert('RGB')).astype(int)
    h, w, _ = a.shape
    # cor do fundo: mediana das bordas
    borda = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    bg = np.median(borda, axis=0)
    dist = np.abs(a - bg).max(axis=2)
    cand = dist < tol
    fundo = np.zeros((h, w), bool)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if cand[y, x] and not fundo[y, x]:
                fundo[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if cand[y, x] and not fundo[y, x]:
                fundo[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and cand[ny, nx] and not fundo[ny, nx]:
                fundo[ny, nx] = True; q.append((ny, nx))
    alpha = Image.fromarray(np.where(fundo, 0, 255).astype('uint8'))
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    rgba = img.convert('RGBA'); rgba.putalpha(alpha)
    return rgba.crop(rgba.getbbox())


grid = Image.open(f'{REF}/02_expressoes_C.png')
W, H = grid.size
nomes = [['neutro', 'confiante', 'rindo'], ['furioso', 'chocado', 'desesperado'], ['sarcastico', 'pensativo', 'euforico']]
for r in range(3):
    for c in range(3):
        cel = grid.crop((c * W // 3, r * H // 3, (c + 1) * W // 3, (r + 1) * H // 3))
        recortar(cel).save(f'{OUT}/exp_{nomes[r][c]}.png')
recortar(Image.open(f'{REF}/04_pose_piscadela.jpg')).save(f'{OUT}/pose_piscadela.png')
recortar(Image.open(f'{REF}/04_pose_andar.jpg')).save(f'{OUT}/pose_andar.png')
print('ok')
