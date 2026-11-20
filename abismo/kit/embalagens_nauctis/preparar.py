# ABISMO · recorte das imagens oficiais das embalagens dos decks de Commander de Nauctis (fundo branco → transparente).
# Uso (raiz do repositório):
#   python3 -I abismo/kit/embalagens_nauctis/preparar.py merfolk=<ficheiro> terrors=<ficheiro> blood=<ficheiro> seal=<ficheiro>
# Saída: abismo/kit/embalagens_nauctis/saida/<deck>.png (fora do Git: imagens © Wizards of the Coast, como as cartas).
# Origem: imagens de produto da Wizards (página «Collecting Nauctis: The Sunken Realm», 13/11/2026), enviadas pelo fundador
# a 20/11/2026 (1920×1080, fundo branco). Ver LEIA-ME.md. Não altera a arte: só remove o fundo branco ligado à borda e recorta.
import os, sys
import numpy as np
from PIL import Image, ImageFilter
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = f'{HERE}/saida'; os.makedirs(OUT, exist_ok=True)

def recortar(src, dst):
    im = Image.open(src).convert('RGB'); a = np.asarray(im).astype(np.int16); h, w = a.shape[:2]
    branco = (a.min(axis=2) >= 236) & ((a.max(axis=2) - a.min(axis=2)) <= 14)
    fundo = np.zeros((h, w), bool); q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if branco[y, x] and not fundo[y, x]: fundo[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if branco[y, x] and not fundo[y, x]: fundo[y, x] = True; q.append((y, x))
    while q:   # só o branco ligado à borda sai (o «13+» e os textos brancos da caixa ficam)
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yy, xx = y + dy, x + dx
            if 0 <= yy < h and 0 <= xx < w and branco[yy, xx] and not fundo[yy, xx]: fundo[yy, xx] = True; q.append((yy, xx))
    alfa = Image.fromarray(np.where(fundo, 0, 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    rgba = im.convert('RGBA'); rgba.putalpha(alfa)
    rgba = rgba.crop(rgba.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox())
    rgba.save(dst); print(dst, rgba.size)

if __name__ == '__main__':
    for arg in sys.argv[1:]:
        nome, src = arg.split('=', 1); recortar(src, f'{OUT}/{nome}.png')
