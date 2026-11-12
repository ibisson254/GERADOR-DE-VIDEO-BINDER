"""Gera parede.jpg, papel.jpg e grao.png (texturas do padrão): python3 -I texturas.py"""
import numpy as np
from PIL import Image, ImageFilter
rng = np.random.default_rng(11)
def fbm(H, W, octs, base):
    out = np.zeros((H, W))
    for o in range(octs):
        f = base * 2**o; small = rng.random((f + 2, int(f * W / H) + 2))
        out += np.asarray(Image.fromarray((small * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), float) / 255 / (1.7**o)
    out -= out.min(); return out / out.max()
H, W = 1350, 1080
n = fbm(H, W, 7, 5); grit = fbm(H, W, 3, 120); chip = fbm(H, W, 6, 9)
wall = np.array([232, 40, 132], float) * (0.72 + 0.42 * n[..., None]) + (grit[..., None] - .5) * 55
m = chip > 0.80; wall[m] = wall[m] * 0.55 + np.array([246, 214, 226]) * 0.45
wall[chip < 0.12] *= 0.7
Image.fromarray(np.clip(wall, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.5)).save('parede.jpg', quality=92)
P = 1400; n = fbm(P, P, 7, 5); m = fbm(P, P, 3, 3)
paper = np.array([238, 226, 200], float) * (0.90 + 0.12 * n[..., None]) - (m[..., None] > 0.7) * np.array([10, 18, 30]) * (m[..., None] - 0.7) * 3
sp = rng.random((P, P)); paper[sp < 0.004] -= 60; paper[sp > 0.998] -= 25
Image.fromarray(np.clip(paper, 0, 255).astype(np.uint8)).save('papel.jpg', quality=92)
g = rng.random((P, P)); a = np.zeros((P, P, 4), np.uint8)
a[g < 0.06] = [30, 20, 25, 70]; a[g > 0.95] = [255, 250, 240, 90]; a[fbm(P, P, 5, 30) > 0.82] = [255, 248, 235, 60]
Image.fromarray(a).save('grao.png')
