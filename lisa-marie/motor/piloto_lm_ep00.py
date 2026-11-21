"""LM-EP00 · Lisa Marie no Ar · piloto sem voz (Elas no Multiverso): as cinco mulheres da Alpha.

Motor de recorte (camadas de kit/prova_recorte) + filmagem urbana real (biblioteca_urbana/) +
troca de carta em rotação 3D no eixo Y (técnica do Meta em Curto, oraculo/motor/mc_render.py,
reimplementada aqui para não depender de código de outra frente) + SFX originais gerados por código.

uso:
  python3 -I lisa-marie/motor/piloto_lm_ep00.py --camadas DIR --cartas DIR [--clipes DIR] [--saida F.mp4]
             [--previa]   (só a folha de fotogramas, sem render)

--camadas: pasta com lisa_base.png, bocas/*.png, palpebra_50.png, palpebra_100.png (camadas.py)
--cartas:  pasta com as PNG do Scryfall (cartas.py)
--clipes:  pasta com os MP4 do manifesto (biblioteca_urbana/manifesto.csv). Um clipe em falta é
           substituído por um fundo provisório desenhado, assinalado no próprio quadro.
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
FPS, W, H = 30, 1080, 1920
SR = 48000

ap = argparse.ArgumentParser()
ap.add_argument('--camadas', required=True)
ap.add_argument('--cartas', required=True)
ap.add_argument('--clipes', default=os.path.join(RAIZ, 'lisa-marie', 'biblioteca_urbana', 'clipes'))
ap.add_argument('--saida', default='LM-EP00_piloto_916.mp4')
ap.add_argument('--previa', action='store_true')
ap.add_argument('--musica', default=None, help='MP3 com licença registada (manifesto); entra por baixo dos SFX')
ARGS = ap.parse_args()

# ---------------------------------------------------------------- paleta e tipos (IDENTIDADE_VISUAL.md)
CARVAO, MARFIM = (23, 21, 27), (243, 235, 221)
ROSA, PETROLEO, COBALTO = (239, 79, 145), (83, 191, 192), (82, 103, 168)
ANTON = '/usr/share/fonts/truetype/google-fonts/ofl/anton/Anton-Regular.ttf'
INTER_B = '/usr/share/fonts/opentype/inter/Inter-Bold.otf'
INTER_SB = '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
_fc = {}


def F(path, size):
    k = (path, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def eout(x):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** 3


# ---------------------------------------------------------------- guião (ficha: episodios/lm-ep00_.../ficha.md)
CARTAS = {
    'shivan': ('shivan_dragon.png', 'MELISSA A. BENSON', 'Shivan Dragon · Alpha, 1993'),
    'mind': ('mind_twist.png', 'JULIE BAROH', 'Mind Twist · Alpha, 1993'),
    'giant': ('giant_growth.png', 'SANDRA EVERINGHAM', 'Giant Growth · Alpha, 1993'),
    'time': ('time_walk.png', 'AMY WEBER', 'Time Walk · Alpha, 1993'),
}
# (início, fim, tipo, dados)
CENAS = [
    (0.00, 2.90, 'abre', {}),
    (2.90, 5.70, 'revela', {}),
    (5.70, 9.50, 'lisa_medio', {'fala': 'Peraí. Ela não era a única.', 'expr': 'curiosa', 'tarja': (6.0, 8.9)}),
    (9.50, 12.70, 'carta', {'k': 'mind', 'facto': 'Ainda estudava artes quando\nfez as primeiras cartas.'}),
    (12.70, 15.90, 'carta', {'k': 'giant', 'facto': '12 ilustrações\nsó na Alpha.'}),
    (15.90, 19.10, 'carta', {'k': 'time', 'facto': '16 ilustrações na Alpha:\na que mais pintou entre elas.'}),
    (19.10, 22.50, 'fay', {}),
    (22.50, 26.00, 'numero', {}),
    (26.00, 29.80, 'lisa_close', {'fala': 'Primeiro set. 1993.\nE elas já estavam lá.', 'expr': 'admiracao'}),
    (29.80, 34.00, 'lisa_cta', {'fala': 'Qual ilustradora você quer\nver no Elas no Multiverso?', 'sub': 'Conta nos comentários.'}),
]
DUR_CENAS = CENAS[-1][1]
FLIPS = [c[0] for c in CENAS if c[2] in ('carta', 'fay', 'numero')]

# ---------------------------------------------------------------- recursos
base = Image.open(os.path.join(ARGS.camadas, 'lisa_base.png')).convert('RGBA')
bocas = {k: Image.open(os.path.join(ARGS.camadas, 'bocas', f'{k}.png')) for k in 'ABCDEFGHX'}
palp = {50: Image.open(os.path.join(ARGS.camadas, 'palpebra_50.png')),
        100: Image.open(os.path.join(ARGS.camadas, 'palpebra_100.png'))}
cartas = {k: Image.open(os.path.join(ARGS.cartas, v[0])).convert('RGBA') for k, v in CARTAS.items()}
CW, CH = 745, 1040          # tamanho nativo do Scryfall: a carta nunca é ampliada

# ---------------------------------------------------------------- fundos urbanos (manifesto)
CLIPE = 'pexels_14957612_rua_chuva_semaforos.mp4'   # enviado pelo fundador a 21/11 (manifesto)
PLACAS = {   # placa -> ficheiro local do manifesto, início (s), enquadramento, tratamento
    'luzes': (CLIPE, 0.0, 1.00, {'blur': 7, 'exp': 0.50, 'sat': 0.70}),     # atrás das cartas: só luz
    'rua': (CLIPE, 6.0, 1.00, {'blur': 1.2, 'exp': 0.80, 'sat': 0.82}),     # Lisa, plano médio
    'chuva': (CLIPE, 14.0, 1.25, {'blur': 2.5, 'exp': 0.74, 'sat': 0.80}),  # grande plano: recorte mais apertado
}
PROVISORIO = set()


class Placa:
    """Lê um clipe em sequência (pipe do ffmpeg), já em 1080x1920 por cobertura, em loop."""

    def __init__(self, nome):
        self.nome = nome
        fich, self.ss, self.zoom, self.trat = PLACAS[nome]
        self.path = os.path.join(ARGS.clipes, fich)
        self.proc = None
        self.ok = os.path.exists(self.path)
        if not self.ok:
            PROVISORIO.add(nome)

    def abre(self):
        zw, zh = int(W * self.zoom) // 2 * 2, int(H * self.zoom) // 2 * 2
        vf = (f'scale={zw}:{zh}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},'
              f'eq=saturation={self.trat["sat"]}')
        self.proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-stream_loop', '-1', '-ss', str(self.ss), '-i', self.path,
                                      '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                                     stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    def quadro(self, t):
        if not self.ok:
            return provisorio(self.nome, t)
        if self.proc is None:
            self.abre()
        raw = self.proc.stdout.read(W * H * 3)
        im = Image.frombytes('RGB', (W, H), raw)
        return tratar(im, self.trat)


def tratar(im, trat):
    """Cidade subordinada: menos exposição, menos saturação, ligeira deriva para a paleta, vinheta."""
    a = np.asarray(im).astype(np.float32) * trat['exp']
    a = a * np.array([0.98, 0.95, 1.04]) + np.array([4, 2, 8])           # ar noturno frio-rosado, discreto
    a = np.clip(a * VINHETA[..., None], 0, 255).astype(np.uint8)
    out = Image.fromarray(a)
    if trat['blur']:
        out = out.filter(ImageFilter.GaussianBlur(trat['blur']))
    return out.convert('RGBA')


yy, xx = np.mgrid[0:H, 0:W]
VINHETA = (1 - 0.55 * (((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H * 0.45) / (H * 0.7)) ** 2)).clip(0.35, 1)
RNG = np.random.default_rng(7)
LUZES = [(RNG.uniform(0, 1), RNG.uniform(0, 1), RNG.uniform(14, 46), RNG.choice(3), RNG.uniform(-0.02, 0.02),
          RNG.uniform(0.3, 1.0)) for _ in range(46)]
COR_LUZ = [(255, 176, 92), (239, 79, 145), (83, 191, 192)]


def provisorio(nome, t):
    """Fundo PROVISÓRIO (sem filmagem real): luzes desfocadas desenhadas. Só para não parar o render."""
    w, h = W // 4, H // 4
    im = Image.new('RGB', (w, h), (14, 12, 20))
    d = ImageDraw.Draw(im, 'RGBA')
    for x, y, r, c, vx, a in LUZES:
        px = ((x + vx * t) % 1.0) * w
        py = (y * 0.8 + 0.15) * h
        col = COR_LUZ[c] + (int(70 * a),)
        d.ellipse((px - r / 4, py - r / 4, px + r / 4, py + r / 4), fill=col)
    im = im.filter(ImageFilter.GaussianBlur(5)).resize((W, H), Image.BICUBIC)
    a = np.clip(np.asarray(im).astype(np.float32) * VINHETA[..., None], 0, 255).astype(np.uint8)
    return Image.fromarray(a).convert('RGBA')


placas = {k: Placa(k) for k in PLACAS}

# ---------------------------------------------------------------- Lisa (recorte)
S_MED = 0.53            # plano médio: ~50% da altura (identidade: 35–55%); ampliação real ≈2,1× da origem
S_CLOSE = 0.74          # grande plano contido: ≈3× da origem (limite assumido, ver LEIA-ME)
PIVO = (base.width / 2, base.height)


def mat(*ops):
    M = np.eye(3)
    for op in ops:
        M = M @ op
    return M


def T(x, y): return np.array([[1, 0, x], [0, 1, y], [0, 0, 1]], float)
def Sc(s): return np.array([[s, 0, 0], [0, s, 0], [0, 0, 1]], float)


def R(deg):
    r = math.radians(deg)
    return np.array([[math.cos(r), -math.sin(r), 0], [math.sin(r), math.cos(r), 0], [0, 0, 1]], float)


def pinta(canvas, img, M):
    inv = np.linalg.inv(M)
    canvas.alpha_composite(img.transform((W, H), Image.AFFINE, tuple(inv[:2].ravel()), resample=Image.BICUBIC))


def piscar(tl, momentos, lento=False):
    for p in momentos:
        d = tl - p
        f = 2 if lento else 1
        if 0 <= d < f / FPS or (2 + f) / FPS <= d < (2 + 2 * f) / FPS:
            return 50
        if f / FPS <= d < (2 + f) / FPS:
            return 100
    return None


SOMBRA_CACHE = {}


def lisa_layer(boca='X', palpebra=None):
    im = base.copy()
    if palpebra:
        im.alpha_composite(palp[palpebra])
    im.alpha_composite(bocas[boca])
    return im


def sombra(img):
    """Separação discreta: sombra suave deslocada, sem contorno luminoso."""
    key = img.size
    if key not in SOMBRA_CACHE:
        a = base.split()[3].filter(ImageFilter.GaussianBlur(28))
        sh = Image.new('RGBA', base.size, (0, 0, 0, 0))
        sh.putalpha(a.point(lambda v: int(v * 0.55)))
        SOMBRA_CACHE[key] = sh
    return SOMBRA_CACHE[key]


def harmonizar(img, cor_media):
    """Puxa a ilustração 6% para a cor média do fundo, sem mudar as cores essenciais."""
    r, g, b, a = img.split()
    tint = Image.new('RGB', img.size, tuple(int(c) for c in cor_media))
    mix = Image.blend(Image.merge('RGB', (r, g, b)), tint, 0.06)
    out = mix.convert('RGBA')
    out.putalpha(a)
    return out


def desenha_lisa(frame, tl, s, x_dir, y_base, expr, boca='X', camera=(1.0, 540, 960), entrada=None):
    """x_dir: borda direita do recorte (fica fora do quadro, esconde o corte); y_base: base do recorte."""
    resp = 1 + 0.005 * math.sin(2 * math.pi * tl / 3.4)
    rot = 0.5 * math.sin(2 * math.pi * tl / 4.3)
    pal = None
    if expr == 'curiosa':
        rot += 2.6 * ease((tl - 0.5) / 0.5)                  # inclina a cabeça depois da fala entrar
        pal = piscar(tl, [1.6, 3.2])
    elif expr == 'admiracao':
        rot -= 1.8 * ease((tl - 0.9) / 0.7)
        pal = piscar(tl, [1.5], lento=True)
    elif expr == 'cta':
        rot += 1.5 * math.sin(2 * math.pi * tl / 2.6)
        pal = piscar(tl, [1.1, 3.4])
    pop = 1.0
    if entrada is not None:                                  # entrada VJ: sobe 60 px e assenta
        k = eout(tl / entrada)
        y_base += (1 - k) * 60
        pop = 0.985 + 0.015 * k
    z, cx, cy = camera
    C = mat(T(540, 960), Sc(z), T(-cx, -cy))
    L = mat(T(x_dir - base.width * s + PIVO[0] * s, y_base - base.height * s + PIVO[1] * s),
            Sc(s * resp * pop), R(rot), T(-PIVO[0], -PIVO[1]))
    pinta(frame, sombra(base), C @ T(-14, 18) @ L)
    cor = np.asarray(frame.convert('RGB').resize((8, 8))).reshape(-1, 3).mean(axis=0)
    pinta(frame, harmonizar(lisa_layer(boca, pal), cor), C @ L)
    # base escurecida: a ilustração assenta no plano (a cintura não termina num corte)
    grad = Image.new('L', (1, 360))
    for i in range(360):
        grad.putpixel((0, i), int(235 * (i / 359) ** 1.6))
    g = Image.new('RGBA', (W, 360), CARVAO + (255,))
    g.putalpha(grad.resize((W, 360)))
    frame.alpha_composite(g, (0, H - 360))


# ---------------------------------------------------------------- carta com troca 3D (eixo Y)
def _persp(pa, pb):
    A = []
    for (x, y), (X, Y) in zip(pa, pb):
        A.append([x, y, 1, 0, 0, 0, -X * x, -X * y])
        A.append([0, 0, 0, x, y, 1, -Y * x, -Y * y])
    return tuple(np.linalg.solve(np.array(A, float), np.array(pb).reshape(8)))


def painel_rot(frame, img, ang, cx, cy, escala=1.0):
    w0, h0 = int(img.width * escala), int(img.height * escala)
    src = img if escala == 1.0 else img.resize((w0, h0), Image.LANCZOS)
    a = math.radians(ang)
    ww = max(2, int(w0 * abs(math.cos(a))))
    persp = 0.12 * math.sin(a)                     # o lado que se afasta encolhe
    s2 = src.resize((ww, h0), Image.LANCZOS)
    hl, hr = h0 * (1 - max(0, persp)), h0 * (1 + min(0, persp))
    d = (h0 - hl) / 2, (h0 - hr) / 2
    co = _persp([(0, d[0]), (ww, d[1]), (ww, h0 - d[1]), (0, h0 - d[0])], [(0, 0), (ww, 0), (ww, h0), (0, h0)])
    out = s2.transform((ww, h0), Image.PERSPECTIVE, co, Image.BICUBIC)
    sh = Image.new('RGBA', (ww + 80, h0 + 80), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((40, 54, ww + 40, h0 + 54), 30, fill=(0, 0, 0, 165))
    frame.alpha_composite(sh.filter(ImageFilter.GaussianBlur(22)), (int(cx - ww / 2 - 40), int(cy - h0 / 2 - 40)))
    frame.alpha_composite(out, (int(cx - ww / 2), int(cy - h0 / 2)))


def flip(frame, ant, nova, t0, t, cx, cy, dur=0.34, escala=1.0):
    """Troca em rotação 3D no eixo Y: a antiga roda até 90°, a nova entra de −90° a 0°."""
    k = (t - t0) / dur
    if ant is None and k < 1:
        painel_rot(frame, nova, -90 + ease(k) * 90, cx, cy, escala)
        return
    if k >= 1:
        painel_rot(frame, nova, 0.0, cx, cy, escala)
    elif k < 0.5:
        painel_rot(frame, ant, ease(k * 2) * 90, cx, cy, escala)
    else:
        painel_rot(frame, nova, -90 + ease((k - .5) * 2) * 90, cx, cy, escala)


def painel_texto(linhas_titulo, corpo, rodape, cor=ROSA):
    """Painel tipográfico do tamanho de uma carta (para a troca 3D ser coerente)."""
    p = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(p)
    d.rounded_rectangle((0, 0, CW - 1, CH - 1), 34, fill=CARVAO + (246,), outline=cor + (255,), width=6)
    y = 120
    for s, sz, c in linhas_titulo:
        f = F(ANTON, sz)
        d.text((CW / 2, y), s, font=f, fill=c, anchor='ma')
        y += int(sz * 1.18)
    y += 30
    for s in corpo:
        d.text((CW / 2, y), s, font=F(INTER_SB, 40), fill=MARFIM, anchor='ma')
        y += 56
    d.text((CW / 2, CH - 70), rodape, font=F(INTER_SB, 22), fill=MARFIM + (170,), anchor='ma')
    return p


PAINEL_FAY = painel_texto([('FAY JONES', 120, ROSA)],
                          ['1 carta na Alpha.', '', 'Pintou-a a pedido', 'do sobrinho:', 'Richard Garfield,', 'o criador do jogo.'],
                          'Fonte: Wikipedia (Fay Jones, artista)', ROSA)
PAINEL_NUM = painel_texto([('5 DE 25', 190, ROSA), ('', 10, MARFIM), ('ARTISTAS DA ALPHA', 62, MARFIM), ('ERAM MULHERES', 62, MARFIM)],
                          ['Amy Weber · Fay Jones', 'Julie Baroh · Melissa A. Benson', 'Sandra Everingham'],
                          'Fontes: Wargamer; créditos das cartas no Scryfall', PETROLEO)


# ---------------------------------------------------------------- grafismos
def legenda_topo(frame, texto, t0, t, y=250, cor=MARFIM, size=92, destaque=()):
    """Legenda grande no topo (zona segura), palavra a palavra; nunca sobre olhos, boca ou carta."""
    d = ImageDraw.Draw(frame, 'RGBA')
    f = F(ANTON, size)
    linhas = texto.split('\n')
    k = (t - t0) / 0.35
    n_pal = sum(len(l.split()) for l in linhas)
    vis = int(min(n_pal, max(0, k * n_pal)) + 0.999) if k < 1 else n_pal
    i = 0
    for li, l in enumerate(linhas):
        pals = l.split()
        larg = d.textlength(l, font=f)
        x = W / 2 - larg / 2
        for p in pals:
            if i < vis:
                c = ROSA if p.strip('.,?!') in destaque else cor
                d.text((x + 4, y + 5), p, font=f, fill=(0, 0, 0, 150))
                d.text((x, y), p, font=f, fill=c)
            x += d.textlength(p + ' ', font=f)
            i += 1
        y += int(size * 1.08)
    return y


def etiqueta_nome(frame, nome, sub, t0, t, y):
    k = eout((t - t0) / 0.28)
    if k <= 0:
        return
    d = ImageDraw.Draw(frame, 'RGBA')
    f1, f2 = F(ANTON, 64), F(INTER_SB, 34)
    w1 = d.textlength(nome, font=f1)
    x = W / 2 - w1 / 2 - 26
    off = (1 - k) * 40
    d.rounded_rectangle((x, y + off, x + w1 + 52, y + 84 + off), 14, fill=ROSA + (int(255 * k),))
    d.text((W / 2, y + 8 + off), nome, font=f1, fill=CARVAO + (int(255 * k),), anchor='ma')
    d.text((W / 2, y + 104 + off), sub, font=f2, fill=MARFIM + (int(235 * k),), anchor='ma')


def facto(frame, texto, t0, t, y):
    k = eout((t - t0) / 0.3)
    if k <= 0:
        return
    d = ImageDraw.Draw(frame, 'RGBA')
    d.multiline_text((W / 2, y), texto, font=F(INTER_B, 44), fill=MARFIM + (int(255 * k),), anchor='ma',
                     align='center', spacing=10, stroke_width=3, stroke_fill=CARVAO + (int(200 * k),))


def fala_lisa(frame, texto, t0, t, box, sub=None):
    """Fala da Lisa sem voz: caixa com o rótulo LISA, junto da personagem, sem tapar o rosto."""
    k = eout((t - t0) / 0.25)
    if k <= 0:
        return
    x0, y0, _ = box
    d = ImageDraw.Draw(frame, 'RGBA')
    f = F(ANTON, 76)
    linhas = texto.split('\n')
    larg = max([d.textlength(l, font=f) for l in linhas] + ([d.textlength(sub, font=F(INTER_SB, 38))] if sub else []))
    x1 = min(W - 48, x0 + 40 + larg + 44)
    alt = len(linhas) * 86 + (64 if sub else 0) + 70
    off = (1 - k) * 30
    d.rounded_rectangle((x0, y0 + off, x1, y0 + alt + off), 26, fill=CARVAO + (int(225 * k),))
    d.rounded_rectangle((x0, y0 + off, x0 + 12, y0 + alt + off), 6, fill=ROSA + (int(255 * k),))
    d.text((x0 + 40, y0 + 18 + off), 'LISA', font=F(INTER_B, 28), fill=ROSA + (int(255 * k),))
    y = y0 + 54 + off
    for l in linhas:
        d.text((x0 + 40, y), l, font=f, fill=MARFIM + (int(255 * k),))
        y += 86
    if sub:
        d.text((x0 + 40, y + 6), sub, font=F(INTER_SB, 38), fill=PETROLEO + (int(255 * k),))


def tarja(frame, t0, t1, t):
    if not (t0 <= t < t1):
        return
    k = eout((t - t0) / 0.3) * (1 - eout((t - (t1 - 0.3)) / 0.3))
    d = ImageDraw.Draw(frame, 'RGBA')
    x = -640 + 700 * k
    d.rounded_rectangle((x, 1560, x + 640, 1700), 18, fill=CARVAO + (235,))
    d.rectangle((x + 600, 1560, x + 640, 1700), fill=ROSA)
    d.text((x + 90, 1578), 'LISA MARIE', font=F(ANTON, 58), fill=MARFIM)
    d.text((x + 92, 1650), 'NO AR · ELAS NO MULTIVERSO', font=F(INTER_B, 26), fill=PETROLEO)


def bug(frame):
    d = ImageDraw.Draw(frame, 'RGBA')
    d.rounded_rectangle((48, 150, 330, 206), 12, fill=CARVAO + (200,))
    d.ellipse((66, 170, 82, 186), fill=ROSA)
    d.text((96, 160), 'LISA MARIE NO AR', font=F(INTER_B, 26), fill=MARFIM + (230,))


def credito_carta(frame, a=200):
    ImageDraw.Draw(frame, 'RGBA').text((W / 2, 1878), 'Arte © Wizards of the Coast · conteúdo de fã não oficial',
                                       font=F(INTER_SB, 22), fill=MARFIM + (a,), anchor='mm')


def marca_provisorio(frame, nome):
    if nome in PROVISORIO:
        ImageDraw.Draw(frame, 'RGBA').text((W - 40, 100), 'FUNDO PROVISÓRIO · SEM CLIPE', font=F(INTER_B, 22),
                                           fill=(228, 215, 90, 220), anchor='ra')


GRAO = [Image.fromarray((np.random.default_rng(s).normal(128, 40, (H // 2, W // 2)).clip(0, 255)).astype(np.uint8))
        .resize((W, H)) for s in range(6)]


def grao(frame, f, forca=12):
    g = GRAO[f % len(GRAO)].convert('RGBA')
    g.putalpha(forca)
    return Image.alpha_composite(frame, g)


def glitch(frame, k):
    """Sintonia curta entre cena de carta e Lisa (2–3 quadros): deslocamento de faixas + scanlines."""
    a = np.asarray(frame).copy()
    rng = np.random.default_rng(int(k * 1000))
    for _ in range(6):
        y = rng.integers(0, H - 80)
        h = rng.integers(20, 80)
        a[y:y + h] = np.roll(a[y:y + h], int(rng.integers(-40, 40)), axis=1)
    a[::4] = (a[::4] * 0.7).astype(np.uint8)
    return Image.fromarray(a)


# ---------------------------------------------------------------- composição por cena
CARTA_CY = 905


def cena_de(t):
    for i, c in enumerate(CENAS):
        if c[0] <= t < c[1]:
            return i, c
    return len(CENAS) - 1, CENAS[-1]


def carta_ant(i):
    """Painel anterior (para a troca 3D)."""
    if i == 0:
        return None
    _, _, tp, dd = CENAS[i - 1]
    if tp in ('abre', 'revela'):
        return cartas['shivan']
    if tp == 'carta':
        return cartas[dd['k']]
    if tp == 'fay':
        return PAINEL_FAY
    return None


def frame(t, f):
    i, (a, b, tp, dd) = cena_de(t)
    tl = t - a
    if tp in ('abre', 'revela', 'carta', 'fay', 'numero'):
        im = placas['luzes'].quadro(t)
        if tp in ('abre', 'revela'):
            esc = 0.96 + 0.025 * (t / 5.7)                 # push lento; nunca acima do tamanho nativo
            painel_rot(im, cartas['shivan'], 0.0, W / 2, CARTA_CY, esc)
            if tp == 'abre':
                legenda_topo(im, 'O DRAGÃO MAIS\nFAMOSO DA ALPHA', -1.0, t, y=150, destaque=('DRAGÃO',))
            else:
                legenda_topo(im, 'FOI PINTADO\nPOR UMA MULHER.', a, t, y=150, destaque=('MULHER',))
                k = eout((tl - 0.25) / 0.3)                  # destaque do crédito impresso na carta
                if k > 0:
                    w0, h0 = CW * esc, CH * esc
                    x0, y0 = W / 2 - w0 / 2, CARTA_CY - h0 / 2
                    box = (x0 + 62 * esc, y0 + 930 * esc, x0 + 448 * esc, y0 + 978 * esc)
                    ImageDraw.Draw(im, 'RGBA').rounded_rectangle(box, 10, outline=ROSA + (int(255 * k),), width=6)
                etiqueta_nome(im, 'MELISSA A. BENSON', 'Shivan Dragon · Alpha, 1993', a + 0.55, t, 1455)
            credito_carta(im)
        else:
            nova = cartas[dd['k']] if tp == 'carta' else (PAINEL_FAY if tp == 'fay' else PAINEL_NUM)
            flip(im, carta_ant(i), nova, a, t, W / 2, CARTA_CY)
            if tp == 'carta':
                _, nome, sub = CARTAS[dd['k']]
                etiqueta_nome(im, nome, sub, a + 0.30, t, 1455)
                facto(im, dd['facto'], a + 0.75, t, 1625)
                credito_carta(im)
            if tp == 'numero':
                k = (tl - 0.34) / 0.25
                if 0 < k < 1:                                 # pulso discreto no número (revelação)
                    ImageDraw.Draw(im, 'RGBA').rounded_rectangle(
                        (W / 2 - CW / 2 - 12 * k, CARTA_CY - CH / 2 - 12 * k, W / 2 + CW / 2 + 12 * k,
                         CARTA_CY + CH / 2 + 12 * k), 40, outline=PETROLEO + (int(200 * (1 - k)),), width=8)
        marca_provisorio(im, 'luzes')
    elif tp == 'lisa_medio':
        im = placas['rua'].quadro(t)
        boca = 'E' if 0.35 <= tl < 0.75 else 'X'           # «Peraí»: surpresa contida, boca em «o»
        desenha_lisa(im, tl, S_MED, W + 8, H + 40, dd['expr'], boca, entrada=0.35)
        fala_lisa(im, dd['fala'], a + 0.30, t, (48, 800, 600))
        tarja(im, dd['tarja'][0], dd['tarja'][1], t)
        marca_provisorio(im, 'rua')
    elif tp == 'lisa_close':
        im = placas['chuva'].quadro(t)
        z = 1.0 + 0.04 * ease(tl / (b - a))
        desenha_lisa(im, tl, S_CLOSE, W + 160, H + 330, dd['expr'], 'X', camera=(z, 600, 1120))
        fala_lisa(im, dd['fala'], a + 0.35, t, (48, 330, 760))
        bug(im)
        marca_provisorio(im, 'chuva')
    else:                                                    # lisa_cta
        im = placas['rua'].quadro(t)
        boca = 'C' if 1.2 <= tl < 1.5 else 'X'
        desenha_lisa(im, tl, S_MED, W + 8, H + 40, 'cta', boca)
        fala_lisa(im, dd['fala'], a + 0.25, t, (48, 690, 1040), sub=dd['sub'])
        bug(im)
        marca_provisorio(im, 'rua')
    # sintonia nas entradas da Lisa
    for c in CENAS:
        if c[2].startswith('lisa') and 0 <= t - c[0] < 3 / FPS:
            im = glitch(im, t).convert('RGBA')
    return grao(im, f)


# ---------------------------------------------------------------- som original (sem voz, sem música)
def tt(d): return np.arange(int(d * SR)) / SR


def env(x, at, de): return np.minimum(1, x / max(at, 1e-4)) * np.exp(-x * de)


def sfx_whoosh(d=0.34):
    x = tt(d)
    n = np.random.default_rng(3).normal(0, 1, len(x))
    # ruído filtrado com varrimento (passa-banda grosseiro por média móvel variável)
    out = np.zeros_like(n)
    acc = 0.0
    for i in range(len(n)):
        a = 0.02 + 0.25 * (i / len(n))
        acc += a * (n[i] - acc)
        out[i] = acc
    return (out * np.sin(np.pi * x / d) * 0.55).astype(np.float32)


def sfx_tick(): x = tt(0.05); return (np.sin(2 * np.pi * 2400 * x) * np.exp(-x * 90) * 0.25).astype(np.float32)
def sfx_thump(): x = tt(0.6); return (np.sin(2 * np.pi * 58 * x * (1 - .25 * x)) * np.exp(-x * 7) * .8).astype(np.float32)


def sfx_sinal():
    x = tt(0.42)
    s = np.sin(2 * np.pi * 880 * x) * env(x, 0.005, 9) * (x < 0.16) + np.sin(2 * np.pi * 1320 * x) * env(np.maximum(x - 0.2, 0), 0.005, 9) * (x >= 0.2)
    return (s * 0.18).astype(np.float32)


def sfx_sintonia():
    x = tt(0.18)
    n = np.random.default_rng(9).normal(0, 1, len(x)) * 0.12
    return ((n + np.sin(2 * np.pi * (300 + 2400 * x) * x) * 0.08) * np.exp(-x * 12)).astype(np.float32)


def sfx_brilho():
    x = tt(0.9)
    return ((np.sin(2 * np.pi * 1760 * x) + 0.5 * np.sin(2 * np.pi * 2637 * x)) * env(x, 0.01, 5) * 0.07).astype(np.float32)


def audio(path, dur):
    mix = np.zeros(int(dur * SR) + SR, np.float32)

    def add(sig, t, g=1.0):
        i = int(t * SR)
        mix[i:i + len(sig)] += sig[:len(mix) - i] * g

    add(sfx_sinal(), 0.0)
    add(sfx_thump(), 2.90, 0.7)
    add(sfx_brilho(), 2.95)
    add(sfx_tick(), 3.45)
    for c in CENAS:
        if c[2].startswith('lisa'):
            add(sfx_sintonia(), c[0])
    for t0 in FLIPS:
        add(sfx_whoosh(), t0, 0.8)
        add(sfx_tick(), t0 + 0.30, 0.8)
    add(sfx_thump(), 22.84, 0.9)
    # cama de cidade muito baixa nas cenas da Lisa (ruído rosa filtrado), cola filmagem e ilustração
    rng = np.random.default_rng(11)
    for a, b, tp, _ in CENAS:
        if tp.startswith('lisa'):
            n = rng.normal(0, 1, int((b - a) * SR)).astype(np.float32)
            n = np.convolve(n, np.ones(200) / 200, mode='same') * 0.6
            fade = np.minimum(1, np.minimum(np.arange(len(n)), np.arange(len(n))[::-1]) / (0.25 * SR))
            add(n * fade, a, 0.5)
    mix = mix[:int(dur * SR)]
    mix = mix / max(1e-6, np.abs(mix).max()) * 0.5
    if ARGS.musica:
        raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', ARGS.musica, '-t', str(dur), '-ac', '1',
                                       '-ar', str(SR), '-f', 's16le', '-'])
        mus = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
        mus = np.pad(mus, (0, max(0, len(mix) - len(mus))))[:len(mix)]
        x = np.arange(len(mix)) / SR
        g = np.minimum(1, x / 0.4) * np.clip((dur - x) / 1.2, 0, 1)        # entra em 0,4 s, fade no fim do fecho
        g = g * np.where(x < DUR_CENAS, 0.55, 0.75)                          # sobe no fecho (sem voz por cima)
        mix = mix + mus / max(1e-6, np.abs(mus).max()) * g
    mix = mix / max(1e-6, np.abs(mix).max()) * 0.89
    with wave.open(path, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())


# ---------------------------------------------------------------- execução
if ARGS.previa:
    ts = [0.0, 3.6, 6.5, 9.65, 11.5, 14.0, 17.5, 20.5, 24.0, 28.0, 31.5]
    fr = []
    for t in ts:
        for p in placas.values():
            p.proc = None
        fr.append(frame(t, 0).convert('RGB').resize((270, 480)))
    folha = Image.new('RGB', (270 * 6, 480 * 2), CARVAO)
    for k, im in enumerate(fr):
        folha.paste(im, ((k % 6) * 270, (k // 6) * 480))
    folha.save(ARGS.saida.replace('.mp4', '_previa.jpg'), quality=88)
    print('prévia:', ARGS.saida.replace('.mp4', '_previa.jpg'), '| provisórios:', sorted(PROVISORIO) or 'nenhum')
    sys.exit(0)

corpo = ARGS.saida.replace('.mp4', '_corpo.mp4')
wav = ARGS.saida.replace('.mp4', '_sfx.wav')
proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}',
                         '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18',
                         '-pix_fmt', 'yuv420p', corpo], stdin=subprocess.PIPE)
n = int(round(DUR_CENAS * FPS))
for f in range(n):
    proc.stdin.write(frame(f / FPS, f).tobytes())
proc.stdin.close()
proc.wait()
outro = os.path.join(RAIZ, 'comum', 'outro', 'outro_binder_916.mp4')
dur_outro = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of',
                                           'csv=p=0', outro]).decode())
audio(wav, DUR_CENAS + dur_outro)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', corpo, '-i', outro, '-i', wav, '-filter_complex',
                '[0:v][1:v]concat=n=2:v=1:a=0[v];[2:a]loudnorm=I=-14:TP=-1.5:LRA=11[a]', '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset',
                'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest',
                '-movflags', '+faststart', ARGS.saida], check=True)
os.remove(corpo)
print('render:', ARGS.saida, f'| {DUR_CENAS + dur_outro:.2f} s | provisórios:', sorted(PROVISORIO) or 'nenhum')
json.dump({'provisorios': sorted(PROVISORIO), 'duracao': DUR_CENAS + dur_outro},
          open(ARGS.saida.replace('.mp4', '_render.json'), 'w'))
