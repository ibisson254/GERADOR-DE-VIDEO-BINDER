"""LM-EP01 · prévia de piloto · Elas no Multiverso: «Quem cria o visual de Magic?»

Secret Lair x Global Fund for Women: Their Magic Is Limitless (2026). Lisa em recorte v2 (cabeça separada,
olhar com direção, bocas v2) sobre filmagem urbana real, boca pelo Rhubarb, troca de carta em 3D (eixo Y),
voz PROVISÓRIA local (não publicável) e música de biblioteca com licença registada.

uso:
  python3 -I lisa-marie/motor/lm_ep01.py --camadas DIR(camadas_v2) --cartas DIR --voz DIR --clipes DIR
         [--musica F.mp3] [--saida F.mp4] [--previa]
"""
import argparse
import json
import math
import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, '..', '..'))
EP = os.path.join(RAIZ, 'lisa-marie', 'episodios', 'lm-ep01_previa_quem_cria_o_visual')
FPS, W, H, SR = 30, 1080, 1920, 44100

ap = argparse.ArgumentParser()
ap.add_argument('--camadas', required=True)
ap.add_argument('--cartas', required=True)
ap.add_argument('--voz', required=True)
ap.add_argument('--clipes', required=True)
ap.add_argument('--musica', default=None)
ap.add_argument('--saida', default='LM-EP01_previa_916.mp4')
ap.add_argument('--previa', action='store_true')
ARGS = ap.parse_args()

CARVAO, MARFIM = (23, 21, 27), (243, 235, 221)
ROSA, PETROLEO = (239, 79, 145), (83, 191, 192)
ANTON = '/usr/share/fonts/truetype/google-fonts/ofl/anton/Anton-Regular.ttf'
INTER_B = '/usr/share/fonts/opentype/inter/Inter-Bold.otf'
INTER_SB = '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
_fc = {}


def F(p, s):
    if (p, s) not in _fc:
        _fc[(p, s)] = ImageFont.truetype(p, s)
    return _fc[(p, s)]


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def eout(x):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** 3


# ---------------------------------------------------------------- linha do tempo a partir da voz
FALAS = {f['id']: f for f in json.load(open(os.path.join(EP, 'falas.json')))}
DUR = json.load(open(os.path.join(ARGS.voz, 'duracoes.json')))
CENAS_ORDEM = ['gancho', 'lisa_apresenta', 'carta_gariba', 'detalhe_felothar', 'detalhe_escudo', 'lisa_leitura',
               'flip_colecao', 'alinhamento', 'lisa_close', 'lisa_cta']
GAP, PAD_CENA = 0.16, 0.30
t = 0.15
CENAS, LINHAS = [], []
for nome in CENAS_ORDEM:
    ini = 0.0 if nome == 'gancho' else t
    if nome != 'gancho':
        t += PAD_CENA
    for fid, f in FALAS.items():
        if f['cena'] == nome:
            LINHAS.append((t, t + DUR[fid], fid))
            t += DUR[fid] + GAP
    CENAS.append([ini, None, nome])
for i in range(len(CENAS)):
    CENAS[i][1] = CENAS[i + 1][0] if i + 1 < len(CENAS) else t + 0.45
DUR_CENAS = CENAS[-1][1]


def cena_de(tt):
    for i, (a, b, n) in enumerate(CENAS):
        if a <= tt < b:
            return i, a, b, n
    a, b, n = CENAS[-1]
    return len(CENAS) - 1, a, b, n


def linhas_da(nome):
    return [l for l in LINHAS if FALAS[l[2]]['cena'] == nome]


def linha_em(tt):
    for a, b, fid in LINHAS:
        if a <= tt < b + 0.12:
            return a, b, fid
    return None


# bocas: Rhubarb por fala, com fusão de segmentos < 2 quadros (evita «tremor» de boca)
CUES = {}
for fid in FALAS:
    raw = json.load(open(os.path.join(ARGS.voz, fid + '.json')))['mouthCues']
    lim = []
    for c in raw:
        if lim and c['end'] - c['start'] < 2 / FPS:
            lim[-1]['end'] = c['end']
        else:
            lim.append(dict(c))
    CUES[fid] = lim


def boca_em(tt):
    l = linha_em(tt)
    if not l:
        return 'X'
    a, b, fid = l
    r = tt - a
    for c in CUES[fid]:
        if c['start'] <= r < c['end']:
            return c['value']
    return 'X'


# ---------------------------------------------------------------- recursos
CAM = ARGS.camadas
corpo = Image.open(os.path.join(CAM, 'corpo.png')).convert('RGBA')
cabecas = {k: Image.open(os.path.join(CAM, f'cabeca_{k}.png')).convert('RGBA') for k in ('c', 'e', 'd', 'cima')}
bocas = {k: Image.open(os.path.join(CAM, 'bocas', f'{k}.png')) for k in 'ABCDEFGHX'}
palp = {50: Image.open(os.path.join(CAM, 'palpebra_50.png')), 100: Image.open(os.path.join(CAM, 'palpebra_100.png'))}
PIVO = tuple(json.load(open(os.path.join(CAM, 'pivo.json')))['pivo'])
BW, BH = corpo.size
carta = {k: Image.open(os.path.join(ARGS.cartas, f'{k}_png.png')).convert('RGBA')
         for k in ('coat_of_arms', 'finale_of_devastation', 'lathril')}
CW, CH = 744, 1040

# ---------------------------------------------------------------- cidade (manifesto: Pexels 14957612)
CLIPE = os.path.join(ARGS.clipes, 'pexels_14957612_rua_chuva_semaforos.mp4')
yy, xx = np.mgrid[0:H, 0:W]
VINHETA = (1 - 0.55 * (((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H * 0.45) / (H * 0.7)) ** 2)).clip(0.35, 1)


class Placa:
    def __init__(self, ss, zoom, blur, exp, sat):
        self.ss, self.zoom, self.blur, self.exp, self.sat, self.proc, self.ultimo = ss, zoom, blur, exp, sat, None, None

    def quadro(self):
        if not os.path.exists(CLIPE):
            raise SystemExit('falta o clipe do manifesto: ' + CLIPE)
        if self.proc is None:
            zw, zh = int(W * self.zoom) // 2 * 2, int(H * self.zoom) // 2 * 2
            vf = f'scale={zw}:{zh}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},eq=saturation={self.sat}'
            self.proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-stream_loop', '-1', '-ss', str(self.ss), '-i', CLIPE,
                                          '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        raw = self.proc.stdout.read(W * H * 3)
        a = np.frombuffer(raw, np.uint8).reshape(H, W, 3).astype(np.float32) * self.exp
        a = a * np.array([0.98, 0.95, 1.04]) + np.array([4, 2, 8])
        a = a * VINHETA[..., None]
        hi = a.max(axis=2, keepdims=True)                    # controla pontos de luz: comprime os realces
        a = np.where(hi > 200, 200 + (a - 200) * 0.45, a)
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
        if self.blur:
            im = im.filter(ImageFilter.GaussianBlur(self.blur))
        return im.convert('RGBA')


PLACAS = {
    'luzes': Placa(0.0, 1.00, 7, 0.50, 0.68),
    'rua_a': Placa(6.0, 1.00, 1.4, 0.78, 0.80),
    'rua_b': Placa(11.0, 1.10, 1.6, 0.76, 0.80),
    'rua_c': Placa(17.5, 1.00, 1.4, 0.78, 0.80),
    'chuva': Placa(14.0, 1.25, 2.4, 0.72, 0.78),
}


# ---------------------------------------------------------------- matrizes e pintura
def T(x, y): return np.array([[1, 0, x], [0, 1, y], [0, 0, 1]], float)
def Sc(s): return np.array([[s, 0, 0], [0, s, 0], [0, 0, 1]], float)


def R(deg):
    r = math.radians(deg)
    return np.array([[math.cos(r), -math.sin(r), 0], [math.sin(r), math.cos(r), 0], [0, 0, 1]], float)


def pinta(canvas, img, M):
    inv = np.linalg.inv(M)
    canvas.alpha_composite(img.transform((W, H), Image.AFFINE, tuple(inv[:2].ravel()), resample=Image.BICUBIC))


SOMBRA = None


def sombra():
    global SOMBRA
    if SOMBRA is None:
        a = Image.alpha_composite(corpo, cabecas['c']).split()[3].filter(ImageFilter.GaussianBlur(28))
        SOMBRA = Image.new('RGBA', corpo.size, (0, 0, 0, 0))
        SOMBRA.putalpha(a.point(lambda v: int(v * 0.5)))
    return SOMBRA


def harmoniza(img, cor):
    r, g, b, a = img.split()
    mix = Image.blend(Image.merge('RGB', (r, g, b)), Image.new('RGB', img.size, tuple(int(c) for c in cor)), 0.06).convert('RGBA')
    mix.putalpha(a)
    return mix


def env_voz():
    with wave.open(os.path.join(ARGS.voz, 'mix_voz.wav')) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)
    e = np.array([np.sqrt((a[int(f / FPS * SR):int((f + 1) / FPS * SR)] ** 2).mean() + 1e-9)
                  for f in range(int(DUR_CENAS * FPS) + 2)])
    e = np.nan_to_num(e)
    e = np.convolve(e / (e.max() or 1), np.ones(3) / 3, mode='same')
    return e


def piscar(tl, momentos):
    for p in momentos:
        d = tl - p
        if 0 <= d < 1 / FPS or 3 / FPS <= d < 4 / FPS:
            return 50
        if 1 / FPS <= d < 3 / FPS:
            return 100
    return None


def lisa(frame, f, tl, s, x_dir, y_base, olhar, cab_rot, piscadas, entrada=None, camera=(1.0, 540, 960)):
    """Corpo + cabeça (rotação própria no pescoço) + boca (Rhubarb) + pálpebras."""
    tt = f / FPS
    resp = 1 + 0.005 * math.sin(2 * math.pi * tt / 3.4)
    rot_corpo = 0.35 * math.sin(2 * math.pi * tt / 4.6)
    fala = ENV[min(f, len(ENV) - 1)] if linha_em(tt) else 0.0
    rot_cab = cab_rot + 1.2 * fala * math.sin(2 * math.pi * tt * 1.6)   # acento discreto com a voz
    if entrada is not None:
        k = eout(tl / entrada)
        y_base += (1 - k) * 70
    z, cx, cy = camera
    C = T(540, 960) @ Sc(z) @ T(-cx, -cy)
    L = T(x_dir - BW * s + BW / 2 * s, y_base - BH * s + BH * s) @ Sc(s * resp) @ R(rot_corpo) @ T(-BW / 2, -BH)
    cor = np.asarray(frame.convert('RGB').resize((8, 8))).reshape(-1, 3).mean(axis=0)
    pinta(frame, sombra(), C @ T(-14, 18) @ L)
    pinta(frame, harmoniza(corpo, cor), C @ L)
    cab = cabecas[olhar].copy()
    p = piscar(tl, piscadas)
    if p:
        cab.alpha_composite(palp[p])
    cab.alpha_composite(bocas[boca_em(tt)])
    Lc = L @ T(PIVO[0], PIVO[1]) @ R(rot_cab) @ T(-PIVO[0], -PIVO[1])
    pinta(frame, harmoniza(cab, cor), C @ Lc)
    g = Image.new('RGBA', (W, 300), CARVAO + (255,))
    grad = Image.linear_gradient('L').resize((W, 300)).point(lambda v: int(225 * (v / 255) ** 1.6))
    g.putalpha(grad)
    frame.alpha_composite(g, (0, H - 300))


# ---------------------------------------------------------------- cartas, troca 3D e destaques
def _persp(pa, pb):
    A = []
    for (x, y), (X, Y) in zip(pa, pb):
        A += [[x, y, 1, 0, 0, 0, -X * x, -X * y], [0, 0, 0, x, y, 1, -Y * x, -Y * y]]
    return tuple(np.linalg.solve(np.array(A, float), np.array(pb).reshape(8)))


def painel(frame, img, ang, cx, cy, esc=1.0, sombra_a=165):
    w0, h0 = int(img.width * esc), int(img.height * esc)
    src = img if esc == 1.0 else img.resize((w0, h0), Image.LANCZOS)
    a = math.radians(ang)
    ww = max(2, int(w0 * abs(math.cos(a))))
    persp = 0.12 * math.sin(a)
    s2 = src.resize((ww, h0), Image.LANCZOS) if ww != w0 else src
    if ang:
        hl, hr = h0 * (1 - max(0, persp)), h0 * (1 + min(0, persp))
        d = (h0 - hl) / 2, (h0 - hr) / 2
        s2 = s2.transform((ww, h0), Image.PERSPECTIVE,
                          _persp([(0, d[0]), (ww, d[1]), (ww, h0 - d[1]), (0, h0 - d[0])], [(0, 0), (ww, 0), (ww, h0), (0, h0)]),
                          Image.BICUBIC)
    sh = Image.new('RGBA', (ww + 80, h0 + 80), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((40, 54, ww + 40, h0 + 54), int(30 * esc), fill=(0, 0, 0, sombra_a))
    frame.alpha_composite(sh.filter(ImageFilter.GaussianBlur(22)), (int(cx - ww / 2 - 40), int(cy - h0 / 2 - 40)))
    frame.alpha_composite(s2, (int(cx - ww / 2), int(cy - h0 / 2)))


def flip(frame, ant, nova, t0, tt, cx, cy, esc=1.0, dur=0.34):
    k = (tt - t0) / dur
    if k >= 1:
        painel(frame, nova, 0, cx, cy, esc)
    elif k < 0.5:
        painel(frame, ant, ease(k * 2) * 90, cx, cy, esc)
    else:
        painel(frame, nova, -90 + ease((k - .5) * 2) * 90, cx, cy, esc)


def anel(frame, cx, cy, r, k, cor=PETROLEO, larg=7):
    if k <= 0:
        return
    d = ImageDraw.Draw(frame, 'RGBA')
    rr = r * (0.85 + 0.15 * eout(k))
    d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=cor + (int(235 * min(1, k * 2)),), width=larg)


def detalhe(frame, img, box, cx, cy, escala):
    """Ampliação de detalhe da carta (até 1,6×), com moldura; nunca esconde de que carta é."""
    c = img.crop(box)
    c = c.resize((int(c.width * escala), int(c.height * escala)), Image.LANCZOS)
    m = Image.new('L', c.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, c.width - 1, c.height - 1), 28, fill=255)
    sh = Image.new('RGBA', (c.width + 80, c.height + 80), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((40, 54, c.width + 40, c.height + 54), 28, fill=(0, 0, 0, 170))
    frame.alpha_composite(sh.filter(ImageFilter.GaussianBlur(22)), (int(cx - c.width / 2 - 40), int(cy - c.height / 2 - 40)))
    frame.paste(c, (int(cx - c.width / 2), int(cy - c.height / 2)), m)
    return (cx - c.width / 2, cy - c.height / 2, escala, box)


# ---------------------------------------------------------------- textos
def legenda(frame, txt, t0, tt, y=150, size=66, cor=MARFIM, destaque=()):
    d = ImageDraw.Draw(frame, 'RGBA')
    f = F(ANTON, size)
    while max(d.textlength(l, font=f) for l in txt.split('\n')) > W - 90:
        size -= 2
        f = F(ANTON, size)
    k = eout((tt - t0) / 0.2)
    for l in txt.split('\n'):
        x = W / 2 - d.textlength(l, font=f) / 2
        for p in l.split():
            c = ROSA if p.strip('.,?!:') in destaque else cor
            d.text((x + 3, y + 4 + (1 - k) * 10), p, font=f, fill=(0, 0, 0, int(150 * k)))
            d.text((x, y + (1 - k) * 10), p, font=f, fill=c + (int(255 * k),))
            x += d.textlength(p + ' ', font=f)
        y += int(size * 1.12)


def fala_lisa(frame, txt, t0, tt, x0, y0, size=58):
    k = eout((tt - t0) / 0.2)
    if k <= 0:
        return
    d = ImageDraw.Draw(frame, 'RGBA')
    f = F(ANTON, size)
    linhas = txt.split('\n')
    larg = max(d.textlength(l, font=f) for l in linhas)
    x1 = min(W - 40, x0 + 40 + larg + 40)
    alt = len(linhas) * int(size * 1.13) + 66
    off = (1 - k) * 24
    d.rounded_rectangle((x0, y0 + off, x1, y0 + alt + off), 24, fill=CARVAO + (int(225 * k),))
    d.rounded_rectangle((x0, y0 + off, x0 + 10, y0 + alt + off), 5, fill=ROSA + (int(255 * k),))
    d.text((x0 + 36, y0 + 14 + off), 'LISA', font=F(INTER_B, 24), fill=ROSA + (int(255 * k),))
    y = y0 + 46 + off
    for l in linhas:
        d.text((x0 + 36, y), l, font=f, fill=MARFIM + (int(255 * k),))
        y += int(size * 1.13)


def etiqueta(frame, nome, funcao, sub, t0, tt, y, x=None):
    k = eout((tt - t0) / 0.28)
    if k <= 0:
        return
    d = ImageDraw.Draw(frame, 'RGBA')
    f1, f2, f3 = F(ANTON, 58), F(INTER_B, 32), F(INTER_SB, 28)
    w1 = d.textlength(nome, font=f1)
    cx = W / 2 if x is None else x
    off = (1 - k) * 30
    d.rounded_rectangle((cx - w1 / 2 - 24, y + off, cx + w1 / 2 + 24, y + 78 + off), 12, fill=ROSA + (int(255 * k),))
    d.text((cx, y + 7 + off), nome, font=f1, fill=CARVAO + (int(255 * k),), anchor='ma')
    d.text((cx, y + 96 + off), funcao, font=f2, fill=PETROLEO + (int(255 * k),), anchor='ma')
    if sub:
        d.text((cx, y + 140 + off), sub, font=f3, fill=MARFIM + (int(220 * k),), anchor='ma')


def chips(frame, itens, t0, tt, y):
    d = ImageDraw.Draw(frame, 'RGBA')
    f = F(INTER_B, 34)
    larg = [d.textlength(s, font=f) + 48 for s in itens]
    x = W / 2 - (sum(larg) + 16 * (len(itens) - 1)) / 2
    for i, (s, w) in enumerate(zip(itens, larg)):
        k = eout((tt - t0 - 0.18 * i) / 0.25)
        if k > 0:
            d.rounded_rectangle((x, y + (1 - k) * 20, x + w, y + 62 + (1 - k) * 20), 31,
                                fill=CARVAO + (int(230 * k),), outline=PETROLEO + (int(255 * k),), width=3)
            d.text((x + w / 2, y + 31 + (1 - k) * 20), s, font=f, fill=MARFIM + (int(255 * k),), anchor='mm')
        x += w + 16


def tarja(frame, t0, t1, tt):
    if not (t0 <= tt < t1):
        return
    k = eout((tt - t0) / 0.3) * (1 - eout((tt - (t1 - 0.3)) / 0.3))
    d = ImageDraw.Draw(frame, 'RGBA')
    x = -640 + 700 * k
    d.rounded_rectangle((x, 1590, x + 640, 1730), 18, fill=CARVAO + (235,))
    d.rectangle((x + 600, 1590, x + 640, 1730), fill=ROSA)
    d.text((x + 90, 1608), 'LISA MARIE', font=F(ANTON, 58), fill=MARFIM)
    d.text((x + 92, 1680), 'NO AR · ELAS NO MULTIVERSO', font=F(INTER_B, 26), fill=PETROLEO)


def bug(frame):
    d = ImageDraw.Draw(frame, 'RGBA')
    d.rounded_rectangle((48, 150, 330, 206), 12, fill=CARVAO + (200,))
    d.ellipse((66, 170, 82, 186), fill=ROSA)
    d.text((96, 160), 'LISA MARIE NO AR', font=F(INTER_B, 26), fill=MARFIM + (230,))


def rodape(frame, txt='Arte © Wizards of the Coast · conteúdo de fã não oficial'):
    ImageDraw.Draw(frame, 'RGBA').text((W / 2, 1878), txt, font=F(INTER_SB, 22), fill=MARFIM + (190,), anchor='mm')


def aviso(frame):
    ImageDraw.Draw(frame, 'RGBA').text((W / 2, 92), 'VOZ PROVISÓRIA SINTÉTICA · PRÉVIA NÃO PUBLICÁVEL', font=F(INTER_B, 22),
                                       fill=(228, 215, 90, 210), anchor='mm')


GRAO = [Image.fromarray(np.random.default_rng(s).normal(128, 40, (H // 2, W // 2)).clip(0, 255).astype(np.uint8)).resize((W, H))
        for s in range(6)]


def grao(frame, f):
    g = GRAO[f % 6].convert('RGBA')
    g.putalpha(12)
    return Image.alpha_composite(frame, g)


# ---------------------------------------------------------------- composição
DROP = 'Secret Lair × Global Fund for Women · 2026'


def frame(f):
    tt = f / FPS
    i, a, b, nome = cena_de(tt)
    tl = tt - a
    ls = linhas_da(nome)
    l = linha_em(tt)
    txt = FALAS[l[2]]['tela'] if l else None
    t_txt = l[0] if l else 0
    coat = carta['coat_of_arms']

    if nome == 'gancho':
        im = PLACAS['luzes'].quadro()
        esc = 0.80 + 0.02 * (tt / b)
        painel(im, coat, 0, 420, 760, esc)
        lisa(im, f, tl - 0.9, 0.45, W + 8, H + 30, 'cima' if tt < ls[0][1] - 1.0 else 'c', 3.5 if tt < ls[0][1] - 1.0 else 0.8,
             [2.2, 4.4], entrada=0.4) if tt >= 0.9 else None
        if txt:
            fala_lisa(im, txt, t_txt, tt, 40, 1215, size=50)
        rodape(im)
    elif nome == 'lisa_apresenta':
        im = PLACAS['rua_a'].quadro()
        painel(im, coat, 0, 250, 450, 0.40, sombra_a=140)
        lisa(im, f, tl, 0.53, W + 8, H + 40, 'e' if tl < 1.4 else 'c', 2.0 if tl < 1.4 else 0.0, [1.9, 4.6])
        if txt:
            fala_lisa(im, txt, t_txt, tt, 40, 690)
        tarja(im, a + 0.35, ls[0][1] + 0.2, tt)
        if l and l[2] == 'L03':
            chips(im, ['ILUSTRAÇÃO', 'DIREÇÃO DE ARTE', 'DESIGN GRÁFICO'], l[0] + 0.5, tt, 1590)
    elif nome in ('carta_gariba', 'detalhe_felothar', 'detalhe_escudo'):
        im = PLACAS['luzes'].quadro()
        if nome == 'carta_gariba':
            esc = 0.93 + 0.03 * (tl / (b - a))
            cx0, cy0 = W / 2, 905
            painel(im, coat, 0, cx0, cy0, esc)
            if l and l[2] == 'L05':                     # exército e escudo, os dois problemas
                k = (tt - l[0] - 0.3) / 0.4
                ox, oy = cx0 - CW * esc / 2, cy0 - CH * esc / 2
                anel(im, ox + 490 * esc, oy + 390 * esc, 165 * esc, k)
                anel(im, ox + 75 * esc, oy + 455 * esc, 95 * esc, k - 0.4, ROSA)
                anel(im, ox + 668 * esc, oy + 440 * esc, 85 * esc, k - 0.6, ROSA)
            etiqueta(im, 'CAROLINE GARIBA', 'ilustradora · Brasil', 'Coat of Arms · ' + DROP, a + 0.35, tt, 1420)
            if l and l[2] == 'L05':
                pass
        elif nome == 'detalhe_felothar':
            detalhe(im, coat, (80, 70, 540, 580), W / 2, 930, 1.55 + 0.05 * (tl / (b - a)))
            etiqueta(im, 'FELOTHAR', 'personagem da carta', None, a + 0.4, tt, 1450)
        else:
            ox, oy, e, box = detalhe(im, coat, (300, 170, 744, 610), W / 2, 930, 1.55)
            anel(im, ox + (490 - box[0]) * e, oy + (390 - box[1]) * e, 175 * e, (tl - 0.4) / 0.5)
            etiqueta(im, 'ANH NGUYEN', 'designer gráfica · embalagem e produto', 'elemento gráfico no escudo', a + 0.6, tt, 1450)
        if txt:
            legenda(im, txt, t_txt, tt, y=170)
        rodape(im)
    elif nome == 'lisa_leitura':
        im = PLACAS['rua_b'].quadro()
        painel(im, coat, 0, 250, 450, 0.40, sombra_a=140)
        k = (tl - 0.3) / 0.4
        anel(im, 250 - CW * 0.2 + 490 * 0.4, 450 - CH * 0.2 + 390 * 0.4, 72, k, larg=5)
        olh = 'e' if tl < 1.1 else ('d' if tl < 1.7 else 'c')            # olha a carta, pensa, volta à câmara
        lisa(im, f, tl, 0.53, W + 8, H + 40, olh, 2.4 if tl < 1.1 else (-1.2 if tl < 1.7 else 0.5), [2.4])
        if txt:
            fala_lisa(im, txt, t_txt, tt, 40, 690)
    elif nome == 'flip_colecao':
        im = PLACAS['luzes'].quadro()
        t_mid = a + (b - a) * 0.52
        cx0, cy0 = W / 2, 905
        if tt < t_mid:
            flip(im, coat, carta['finale_of_devastation'], a, tt, cx0, cy0, 0.93)
            anel(im, cx0 - CW * 0.465 + 140 * 0.93, cy0 - CH * 0.465 + 380 * 0.93, 125, (tt - a - 0.5) / 0.4)
            etiqueta(im, 'JULIE DILLON', 'ilustradora', 'Finale of Devastation', a + 0.35, tt, 1420)
        else:
            flip(im, carta['finale_of_devastation'], carta['lathril'], t_mid, tt, cx0, cy0, 0.93)
            anel(im, cx0 - CW * 0.465 + 650 * 0.93, cy0 - CH * 0.465 + 500 * 0.93, 115, (tt - t_mid - 0.5) / 0.4)
            etiqueta(im, 'MAGALI VILLENEUVE', 'ilustradora', 'Lathril, Blade of the Elves', t_mid + 0.35, tt, 1420)
        if txt:
            legenda(im, txt, t_txt, tt, y=170)
        rodape(im)
    elif nome == 'alinhamento':
        im = PLACAS['luzes'].quadro()
        for j, k in enumerate(('coat_of_arms', 'finale_of_devastation', 'lathril')):
            kk = eout((tl - 0.12 * j) / 0.35)
            painel(im, carta[k], 0, 190 + 350 * j, 880 + (1 - kk) * 60, 0.44)
        if txt:
            legenda(im, txt, t_txt, tt, y=300, size=84, destaque=('coleção.',))
        kk = eout((tl - 0.8) / 0.3)
        if kk > 0:
            d = ImageDraw.Draw(im, 'RGBA')
            d.text((W / 2, 1250), 'Direção de arte: Stephanie Cheung (mentora)', font=F(INTER_B, 34), fill=MARFIM + (int(255 * kk),), anchor='ma')
            d.text((W / 2, 1300), 'com Anh Nguyen (mentorada) · equipe de 8 mulheres da Wizards', font=F(INTER_SB, 28), fill=PETROLEO + (int(255 * kk),), anchor='ma')
        rodape(im)
    elif nome == 'lisa_close':
        im = PLACAS['chuva'].quadro()
        z = 1.0 + 0.04 * ease(tl / (b - a))
        lisa(im, f, tl, 0.74, W + 160, H + 330, 'c', -1.5, [1.4], camera=(z, 600, 1120))
        if txt:
            fala_lisa(im, txt, t_txt, tt, 40, 330)
        bug(im)
    else:
        im = PLACAS['rua_c'].quadro()
        lisa(im, f, tl, 0.53, W + 8, H + 40, 'c', 1.5 * math.sin(2 * math.pi * tl / 2.8), [1.0, 3.0])
        if txt:
            fala_lisa(im, txt, t_txt, tt, 40, 760)
        bug(im)
    aviso(im)
    return grao(im, f)


# ---------------------------------------------------------------- áudio: voz provisória + música licenciada
def monta_voz():
    tot = np.zeros(int((DUR_CENAS + 6) * SR), np.float32)
    for a, b, fid in LINHAS:
        with wave.open(os.path.join(ARGS.voz, fid + '.wav')) as w:
            v = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        i = int(a * SR)
        tot[i:i + len(v)] += v[:len(tot) - i]
    with wave.open(os.path.join(ARGS.voz, 'mix_voz.wav'), 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(tot[:int(DUR_CENAS * SR)], -1, 1) * 32767).astype(np.int16).tobytes())
    return tot


def sfx(tot):
    def tt_(d): return np.arange(int(d * SR)) / SR
    x = tt_(0.3)
    wh = np.random.default_rng(3).normal(0, 1, len(x))
    wh = np.convolve(wh, np.ones(40) / 40, mode='same') * np.sin(np.pi * x / 0.3) * 0.25
    tk = np.sin(2 * np.pi * 2400 * tt_(0.05)) * np.exp(-tt_(0.05) * 90) * 0.12
    xs = tt_(0.42)
    sinal = (np.sin(2 * np.pi * 880 * xs) * (xs < 0.14) + np.sin(2 * np.pi * 1320 * xs) * (xs >= 0.2)) * np.exp(-xs * 6) * 0.09

    def add(s, t0, g=1.0):
        i = int(t0 * SR)
        tot[i:i + len(s)] += (s * g)[:len(tot) - i]

    add(sinal, 0.0)
    for a, b, n in CENAS:
        if n == 'flip_colecao':
            add(wh, a)
            add(wh, a + (b - a) * 0.52)
        if n in ('carta_gariba', 'detalhe_felothar', 'detalhe_escudo', 'alinhamento', 'lisa_apresenta', 'lisa_leitura', 'lisa_close', 'lisa_cta'):
            add(tk, a + 0.3)
    return tot


def audio(path, dur):
    voz = sfx(monta_voz())[:int(dur * SR)]
    voz = np.pad(voz, (0, max(0, int(dur * SR) - len(voz))))
    mix = voz.copy()
    if ARGS.musica:
        raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', ARGS.musica, '-t', str(dur), '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'])
        m = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
        m = np.pad(m, (0, max(0, len(mix) - len(m))))[:len(mix)]
        x = np.arange(len(mix)) / SR
        ev = np.abs(voz)
        ev = np.convolve(ev, np.ones(int(0.25 * SR)) / (0.25 * SR), mode='same')
        duck = np.where(ev > 0.01, 0.14, 0.30)                      # música baixa por baixo da voz
        duck = np.convolve(duck, np.ones(int(0.2 * SR)) / (0.2 * SR), mode='same')
        g = duck * np.minimum(1, x / 0.4) * np.clip((dur - x) / 1.2, 0, 1)
        g = np.where(x >= DUR_CENAS, 0.5 * np.clip((dur - x) / 1.2, 0, 1), g)  # sobe no fecho
        mix = mix + m / max(1e-6, np.abs(m).max()) * g
    mix = mix / max(1e-6, np.abs(mix).max()) * 0.85
    with wave.open(path, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())


monta_voz()
ENV = env_voz()

if ARGS.previa:
    marcos = [0.0] + [round((x[0] + x[1]) / 2, 2) for x in LINHAS]
    fr = []
    for tt in marcos:
        for p in PLACAS.values():
            p.proc = None
        fr.append(frame(int(tt * FPS)).convert('RGB').resize((216, 384)))
    n = len(fr)
    folha = Image.new('RGB', (216 * 7, 384 * ((n + 6) // 7)), CARVAO)
    for k, im in enumerate(fr):
        folha.paste(im, ((k % 7) * 216, (k // 7) * 384))
    folha.save(ARGS.saida.replace('.mp4', '_previa.jpg'), quality=88)
    print('prévia ok', f'{DUR_CENAS:.2f} s', [(round(a, 2), n) for a, b, n in CENAS])
    sys.exit(0)

corpo_mp4 = ARGS.saida.replace('.mp4', '_corpo.mp4')
wav = ARGS.saida.replace('.mp4', '_audio.wav')
proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS),
                         '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', corpo_mp4],
                        stdin=subprocess.PIPE)
for f in range(int(round(DUR_CENAS * FPS))):
    proc.stdin.write(frame(f).tobytes())
proc.stdin.close()
proc.wait()
outro = os.path.join(RAIZ, 'comum', 'outro', 'outro_binder_916.mp4')
d_out = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', outro]))
audio(wav, DUR_CENAS + d_out)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', corpo_mp4, '-i', outro, '-i', wav, '-filter_complex',
                '[0:v][1:v]concat=n=2:v=1:a=0[v];[2:a]loudnorm=I=-15:TP=-2:LRA=11[a]', '-map', '[v]', '-map', '[a]',
                '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                '-ar', '48000', '-shortest', '-movflags', '+faststart', ARGS.saida], check=True)
os.remove(corpo_mp4)
json.dump({'duracao': DUR_CENAS + d_out, 'cenas': [(round(a, 2), round(b, 2), n) for a, b, n in CENAS],
           'linhas': [(round(a, 2), round(b, 2), fid) for a, b, fid in LINHAS]},
          open(ARGS.saida.replace('.mp4', '_render.json'), 'w'), indent=1)
print('render:', ARGS.saida, f'{DUR_CENAS + d_out:.2f} s')
