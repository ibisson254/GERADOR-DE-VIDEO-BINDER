"""Reconstrói o fecho de marca (3,87 s, 1080x1920, 30 fps, sem áudio) igual ao oraculo/episodios/ep02_render.py:
quadros reais do scanner (comum/outro/scan/) + logótipo. Usado porque comum/outro/outro_binder_916.mp4 não está
no repositório nem no Drive (29/10/2026). Nunca redesenha a tela do app: os 45 quadros são a gravação real.
uso: python3 fecho_scanner.py /caminho/do/repo saida.mp4
"""
import sys, subprocess, pathlib
from PIL import Image, ImageDraw, ImageFont
K = sys.argv[1].rstrip('/') + '/'; OUT = sys.argv[2]
W, H, FPS, DUR = 1080, 1920, 30, 3.87
LOGO = Image.open(K + 'manaburn/logo/logo_mark.png').convert('RGBA')
SCAN = [Image.open(K + f'comum/outro/scan/{i:03d}.jpg').convert('RGB') for i in range(45)]
INTB = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'; INTSB = '/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf'
INTM = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
BG = (5, 10, 16); EM = (16, 185, 129); WHITE = (236, 241, 245)
def ease(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)
def eio(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3
def outro(t):
    if t < 1.5:
        im = SCAN[min(44, int(t * 30))].copy()
        return im if im.size == (W, H) else im.resize((W, H), Image.LANCZOS)
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im, 'RGBA')
    v = eio((t - 1.5) / 0.6); size = int(60 + 260 * v)
    lg = LOGO.resize((size, size), Image.LANCZOS).rotate(-140 * (1 - v), resample=Image.BICUBIC)
    im.paste(lg, (int(W / 2 - lg.width / 2), int(760 - lg.height / 2)), lg)
    q = ease((t - 1.9) / 0.3); r = ease((t - 2.1) / 0.3)
    d.text((W / 2, 1000 + (1 - q) * 20), 'BINDER Vision', font=ImageFont.truetype(INTB, 92), fill=WHITE + (int(255 * q),), anchor='ma')
    d.text((W / 2, 1130), 'Escaneie suas cartas e organize seus decks.', font=ImageFont.truetype(INTM, 38), fill=(190, 200, 210, int(255 * q)), anchor='ma')
    d.text((W / 2, 1250), 'Disponível no Google Play · Link na bio', font=ImageFont.truetype(INTSB, 40), fill=EM + (int(255 * r),), anchor='ma')
    if t > 3.4: im = Image.blend(im, Image.new('RGB', (W, H), (0, 0, 0)), min(1, (t - 3.4) / 0.47))
    return im
d = pathlib.Path('fecho_frames'); d.mkdir(exist_ok=True)
n = int(round(DUR * FPS))
for i in range(n): outro(i / FPS).save(d / f'{i:04d}.png')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', str(d / '%04d.png'), '-c:v', 'libx264',
                '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', str(FPS), OUT], check=True)
print('ok', OUT, n, 'quadros')
