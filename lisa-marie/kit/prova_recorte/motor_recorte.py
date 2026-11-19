"""Motor de recorte da Lisa (prova de estilo, custo zero).

Entrada: lisa_base.png, bocas/*.png, palpebra_*.png (camadas.py), fundo.png, tarja.png,
bug.png, fala.wav e boca.json (Rhubarb Lip Sync, reconhecedor fonético).
Saída: prova_lisa_recorte.mp4 (1080x1920, 30 fps).
"""
import json
import math
import subprocess
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

FPS, W, H = 30, 1080, 1920
AUDIO = 'fala.wav'
DUR = 5.8
CORTE = 2.40                       # plano médio -> grande plano (na pausa da fala)

base = Image.open('lisa_base.png').convert('RGBA')
bocas = {k: Image.open(f'bocas/{k}.png') for k in 'ABCDEFGHX'}
palp = {50: Image.open('palpebra_50.png'), 100: Image.open('palpebra_100.png')}
fundo = Image.open('fundo.png').convert('RGBA')
tarja = Image.open('tarja.png').convert('RGBA')
bug = Image.open('bug.png').convert('RGBA')
cues = json.load(open('boca.json'))['mouthCues']

# envelope da voz (para o balanço da cabeça ao falar)
with wave.open(AUDIO) as w:
    sr, n, ch = w.getframerate(), w.getnframes(), w.getnchannels()
    a = np.frombuffer(w.readframes(n), dtype=np.int16).astype(float)
    if ch > 1:
        a = a.reshape(-1, ch).mean(axis=1)
env = []
for f in range(int(DUR * FPS)):
    s = a[int(f / FPS * sr): int((f + 1) / FPS * sr)]
    env.append(np.sqrt((s ** 2).mean()) if len(s) else 0.0)
env = np.array(env)
env = np.convolve(env / (env.max() or 1), np.ones(3) / 3, mode='same')

LEG = [(0.00, 0.54, 'OI!'), (0.99, 2.24, 'EU SOU A LISA MARIE.'),
       (2.48, 4.63, 'ISSO AQUI É UM TESTE DE BOCA.'), (4.76, 5.80, 'CURTIU?')]
import glob
anton = (glob.glob('/usr/share/fonts/**/Anton*.ttf', recursive=True) + [None])[0]
inter = (glob.glob('/usr/share/fonts/**/Inter*.ttf', recursive=True) + glob.glob('/usr/share/fonts/**/DejaVuSans.ttf', recursive=True))[0]
f_leg = ImageFont.truetype(anton, 88)
f_aviso = ImageFont.truetype(inter, 26)
PISCAR = [1.30, 3.70, 5.20]


def boca(t):
    for c in cues:
        if c['start'] <= t < c['end']:
            return c['value']
    return 'X'


def palpebra(t):
    for p in PISCAR:
        d = t - p
        if 0 <= d < 1 / FPS or 3 / FPS <= d < 4 / FPS:
            return 50
        if 1 / FPS <= d < 3 / FPS:
            return 100
    return None


def mat_t(tx, ty):
    return np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]], float)


def mat_s(s):
    return np.array([[s, 0, 0], [0, s, 0], [0, 0, 1]], float)


def mat_r(deg):
    r = math.radians(deg)
    return np.array([[math.cos(r), -math.sin(r), 0], [math.sin(r), math.cos(r), 0], [0, 0, 1]], float)


def pinta(canvas, img, M):
    inv = np.linalg.inv(M)
    layer = img.transform((W, H), Image.AFFINE, tuple(inv[:2].ravel()), resample=Image.BICUBIC)
    canvas.alpha_composite(layer)


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def camera(t):
    if t < CORTE:                       # plano médio com push-in lento
        z = 1.0 + 0.035 * (t / CORTE)
        return z, 540, 960
    u = (t - CORTE) / (DUR - CORTE)     # grande plano no rosto
    return 1.50 + 0.05 * u, 722 + 8 * u, 770


S = 0.82                                 # escala do recorte 4x no estúdio
LX, LY = 1080 - base.width * S, 300      # borda direita do recorte na borda do quadro
PIVOT = (base.width / 2, base.height)    # balanço a partir da cintura

proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba',
                         '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', AUDIO,
                         '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
                         '-c:a', 'aac', '-b:a', '192k', '-af', 'apad', '-t', str(DUR),
                         '-movflags', '+faststart', 'prova_lisa_recorte.mp4'], stdin=subprocess.PIPE)

for f in range(int(DUR * FPS)):
    t = f / FPS
    z, cx, cy = camera(t)
    C = mat_t(540, 960) @ mat_s(z) @ mat_t(-cx, -cy)

    frame = Image.new('RGBA', (W, H), (23, 21, 27, 255))
    pinta(frame, fundo, C @ mat_t(540, 960) @ mat_s(1.0 + 0.02 * (z - 1)) @ mat_t(-540, -960))

    lisa = base.copy()
    p = palpebra(t)
    if p:
        lisa.alpha_composite(palp[p])
    lisa.alpha_composite(bocas[boca(t)])

    resp = 1 + 0.006 * math.sin(2 * math.pi * t / 3.2)
    rot = 0.6 * math.sin(2 * math.pi * t / 4.1) + 1.2 * env[f] * math.sin(2 * math.pi * t * 1.7)
    bob = -10 * env[f]
    L = (mat_t(LX + PIVOT[0] * S, LY + PIVOT[1] * S + bob) @ mat_s(S * resp) @ mat_r(rot)
         @ mat_t(-PIVOT[0], -PIVOT[1]))
    pinta(frame, lisa, C @ L)

    d = ImageDraw.Draw(frame)
    if t < CORTE:                                   # tarja entra da esquerda
        k = ease((t - 0.35) / 0.35)
        if k > 0:
            frame.alpha_composite(tarja, (int(-1080 + 1080 * k), 1580))
    else:                                           # identificador no canto
        frame.alpha_composite(bug, (48, 180))
    if CORTE <= t < CORTE + 2 / FPS:                # transição: flash curto de sinal
        flash = Image.new('RGBA', (W, H), (239, 79, 145, 90))
        frame.alpha_composite(flash)
        for y in range(0, H, 6):
            d.line([(0, y), (W, y)], fill=(0, 0, 0, 70))

    for a0, a1, txt in LEG:
        if a0 <= t < a1:
            y = 1380 if t >= CORTE else 1420
            tw = d.textlength(txt, font=f_leg)
            if tw > 960:
                txt = txt.replace(' É ', '\nÉ ')
            d.multiline_text((540, y), txt, font=f_leg, fill=(243, 235, 221, 255), anchor='mm',
                             align='center', stroke_width=7, stroke_fill=(23, 21, 27, 255), spacing=6)
    d.text((540, 88), 'PROVA DE ESTILO · VOZ PROVISÓRIA SINTÉTICA · CUSTO ZERO', font=f_aviso,
           fill=(243, 235, 221, 150), anchor='mm')
    proc.stdin.write(frame.tobytes())

proc.stdin.close()
proc.wait()
print('render ok', proc.returncode)
