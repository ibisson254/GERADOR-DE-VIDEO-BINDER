"""Vince Vault · Ep. 0 piloto "Fechamento da semana" — animatic em fantoche (9:16, 30 fps).

Uso: python3 render.py <pasta referencias> <saida.mp4> [narracao.wav]
Sem narração: legendas das falas no ecrã (versão para aprovar o guião).
"""
import math, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

REF, OUT = sys.argv[1], sys.argv[2]
NARR = sys.argv[3] if len(sys.argv) > 3 else None
W, H, FPS = 1080, 1920, 30
F = '/usr/share/fonts/opentype/inter/'
def fnt(n, s): return ImageFont.truetype(F + n, s)
F_BLACK = lambda s: fnt('InterDisplay-Black.otf', s)
F_BOLD = lambda s: fnt('InterDisplay-Bold.otf', s)
F_MED = lambda s: fnt('Inter-SemiBoldItalic.otf', s)
VERDE, VERMELHO, AMBAR, BRANCO = (16, 185, 129), (239, 68, 68), (251, 191, 36), (245, 245, 250)

FONTE = 'Fonte: MTGStocks, Weekly Winners 2026-45 (06/11/2026) · preços TCGplayer, US$'

# ---------- recursos ----------
def load(p): return Image.open(p).convert('RGBA')
base = Image.open(f'{REF}/03_base_falar_916.jpg').convert('RGB').resize((W, H), Image.LANCZOS)
cen = Image.open(f'{REF}/05_cenario_pregao_mesas.jpg').convert('RGB').resize((W, H), Image.LANCZOS)
fundo = ImageEnhance.Brightness(cen.filter(ImageFilter.GaussianBlur(10))).enhance(0.45)
corr = Image.open(f'{REF}/05_cenario_pregao_corredor.jpg').convert('RGB').resize((W, H), Image.LANCZOS)
fundo2 = ImageEnhance.Brightness(corr.filter(ImageFilter.GaussianBlur(6))).enhance(0.6)
exp = {n: load(f'rec/exp_{n}.png') for n in ['confiante', 'rindo', 'chocado', 'euforico', 'pensativo', 'sarcastico', 'neutro']}
pisc = load('rec/pose_piscadela.png')
cartas = {k: load(f'cartas/{k}.png') for k in ['gandalf', 'plaza', 'elminster']}

# ---------- guião (tempos em s) ----------
CENAS = [
    # (inicio, fim, tipo, dados)
    (0.0, 4.6, 'gancho', {}),
    (4.6, 11.4, 'carta', dict(k='gandalf', rot='ALTA DA SEMANA', cor=VERDE, seta='▲',
                              num='+38%', sub='US$ 8,48 · 7 dias', exp='euforico')),
    (11.4, 16.6, 'carta', dict(k='plaza', rot='NO VERMELHO', cor=VERMELHO, seta='▼',
                               num='EM QUEDA', sub='US$ 4,52 · tendência de baixa', exp='chocado')),
    (16.6, 22.4, 'carta', dict(k='elminster', rot='NO RADAR', cor=AMBAR, seta='◆',
                               num='US$ 1,81', sub='testou o fundo e virou pra cima', exp='pensativo')),
    (22.4, 26.4, 'dip', {}),
    (26.4, 30.6, 'cta', {}),
]
DUR = CENAS[-1][1]
FALAS = [
    (0.2, 4.5, 'Fechamento da semana no pregão do Magic! Vince Vault, Multiverse Capital. Eu li os números.'),
    (4.7, 8.2, 'Rali do Gandalf, White Rider: alta de 38% em sete dias. Oito dólares e quarenta e oito.'),
    (8.2, 11.3, 'Demanda de Commander puxou o papel.'),
    (11.5, 16.5, 'No vermelho: Plaza of Heroes, do Commander da Marvel. Tendência de baixa, 4,52.'),
    (16.7, 22.3, 'No radar: Elminster, 1,81. Segundo o MTGStocks, testou o fundo e virou pra cima.'),
    (22.5, 24.0, 'Buy the dip!'),
    (24.0, 26.3, 'Calma... isso não é recomendação. É leitura de gráfico.'),
    (26.5, 30.5, 'Quer saber quanto vale a sua carteira? Escaneie suas cartas no BINDER Vision e veja o valor de referência.'),
]
TICKER = '   GANDALF, WHITE RIDER ▲ +38%   ·   PLAZA OF HEROES ▼ EM QUEDA   ·   ELMINSTER ◆ US$ 1,81   ·   '

# ---------- utilitários ----------
def ease(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3
def mola(t):  # entrada com ressalto
    t = max(0, min(1, t)); return 1 - math.exp(-6 * t) * math.cos(9 * t)

def texto_centro(d, y, txt, font, fill, stroke=0, sc=(0, 0, 0)):
    w = d.textlength(txt, font=font)
    d.text(((W - w) / 2, y), txt, font=font, fill=fill, stroke_width=stroke, stroke_fill=sc)

def quebra(d, txt, font, maxw):
    linhas, cur = [], ''
    for p in txt.split():
        t = (cur + ' ' + p).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: linhas.append(cur); cur = p
    linhas.append(cur); return linhas

def colar(img, spr, cx, by, escala=1.0, alpha=1.0, rot=0):
    s = spr
    if escala != 1.0: s = s.resize((max(1, int(s.width * escala)), max(1, int(s.height * escala))), Image.LANCZOS)
    if rot: s = s.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1: s = s.copy(); s.putalpha(s.getchannel('A').point(lambda v: int(v * alpha)))
    img.alpha_composite(s, (int(cx - s.width / 2), int(by - s.height)))

def sombra_carta(c, w):
    c = c.resize((w, int(c.height * w / c.width)), Image.LANCZOS)
    pad = 40
    sh = Image.new('RGBA', (c.width + 2 * pad, c.height + 2 * pad), (0, 0, 0, 0))
    m = Image.new('L', sh.size, 0); ImageDraw.Draw(m).rounded_rectangle((pad, pad + 14, pad + c.width, pad + c.height + 14), 26, fill=170)
    sh.putalpha(m.filter(ImageFilter.GaussianBlur(18)))
    sh.alpha_composite(c, (pad, pad)); return sh

CARTA_W = 520
CARTAS_S = {k: sombra_carta(v, CARTA_W) for k, v in cartas.items()}

def ticker(img, t):
    d = ImageDraw.Draw(img)
    d.rectangle((0, 200, W, 262), fill=(5, 10, 16, 235))
    d.line((0, 200, W, 200), fill=VERDE, width=2)
    f = F_BOLD(34); tw = d.textlength(TICKER, font=f)
    x = -(t * 160) % tw
    for k in range(3):
        xx = x - tw + k * tw
        # colorir por segmento
        cx = xx
        for seg in TICKER.split('·'):
            seg2 = seg + '·'
            cor = VERDE if '▲' in seg else VERMELHO if '▼' in seg else AMBAR if '◆' in seg else BRANCO
            d.text((cx, 211), seg2, font=f, fill=cor); cx += d.textlength(seg2, font=f)

def linha_fonte(img):
    d = ImageDraw.Draw(img); f = F_BOLD(26)
    d.rectangle((0, 1500, W, 1544), fill=(5, 10, 16, 210))
    texto_centro(d, 1506, FONTE, f, (200, 205, 215))

def legenda(img, t):
    for a, b, txt in FALAS:
        if a <= t < b:
            d = ImageDraw.Draw(img); f = F_BOLD(44)
            linhas = quebra(d, txt, f, 900)
            y0 = 1318 if t < 22.4 else 1360
            for i, l in enumerate(linhas):
                texto_centro(d, y0 + i * 58, l, f, BRANCO, stroke=5, sc=(5, 10, 16))
            return

def selo_vince(img):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((60, 300, 600, 400), 16, fill=(5, 10, 16, 220), outline=VERDE, width=3)
    d.text((88, 312), 'VINCE VAULT', font=F_BLACK(46), fill=BRANCO)
    d.text((90, 364), 'Multiverse Capital · personagem fictício', font=F_BOLD(24), fill=(170, 180, 195))

# ---------- cenas ----------
def cena_gancho(t, dt):
    z = 1.0 + 0.06 * (t / 4.6)
    im = base.resize((int(W * z), int(H * z)), Image.LANCZOS)
    ox, oy = (im.width - W) // 2, int((im.height - H) * 0.35)
    img = im.crop((ox, oy, ox + W, oy + H)).convert('RGBA')
    if t > 0.3: selo_vince(img)
    d = ImageDraw.Draw(img)
    a = ease((t - 0.1) / 0.4)
    if a > 0:
        texto_centro(d, 1580 - 30 * (1 - a), 'FECHAMENTO', F_BLACK(96), VERDE, stroke=6, sc=(5, 10, 16))
        texto_centro(d, 1680 - 30 * (1 - a), 'DA SEMANA', F_BLACK(96), BRANCO, stroke=6, sc=(5, 10, 16))
    return img

def cena_carta(t, dt, k, rot, cor, seta, num, sub, exp_n):
    img = fundo.copy().convert('RGBA'); ticker(img, t)
    d = ImageDraw.Draw(img)
    a = ease(dt / 0.35)
    # rótulo
    f = F_BLACK(64); tw = d.textlength(rot, font=f)
    x0 = (W - tw) / 2 - 30
    d.rounded_rectangle((x0, 300, x0 + tw + 60, 390), 14, fill=cor + (int(235 * a),))
    texto_centro(d, 308, rot, f, (5, 10, 16))
    # carta (inteira, nada por cima)
    s = CARTAS_S[k]
    y = 410 + int(60 * (1 - mola(dt / 0.7)))
    flut = 6 * math.sin(dt * 2.2)
    img.alpha_composite(s, (int((W - s.width) / 2), int(y + flut - 40)))
    # etiqueta de cotação
    b = ease((dt - 0.45) / 0.3)
    if b > 0:
        f1, f2 = F_BLACK(80), F_BOLD(36)
        txt = f'{seta} {num}'
        tw = d.textlength(txt, font=f1)
        yy = 1140 + int(20 * (1 - b))
        d.text(((W - tw) / 2, yy), txt, font=f1, fill=cor + (int(255 * b),), stroke_width=4, stroke_fill=(5, 10, 16))
        texto_centro(d, yy + 90, sub, f2, BRANCO, stroke=3, sc=(5, 10, 16))
    linha_fonte(img)
    # Vince reage, canto inferior direito
    c = ease((dt - 0.25) / 0.35)
    if c > 0:
        spr = exp[exp_n]
        sc = 560 / spr.width
        bob = 4 * math.sin(dt * 5)
        colar(img, spr, W - 230 + 200 * (1 - mola((dt - 0.25) / 0.6)), H + 10 + bob, sc * 0.75)
    return img

def cena_dip(t, dt):
    img = fundo2.copy().convert('RGBA')
    d = ImageDraw.Draw(img)
    if dt < 1.6:
        s = 1 + 0.08 * math.sin(dt * 14) * max(0, 1 - dt)
        colar(img, exp['euforico'], W / 2, H, 2.3 * s)
        f = F_BLACK(150)
        for i, w_ in enumerate(['BUY', 'THE DIP!']):
            texto_centro(d, 330 + i * 165, w_, f, VERDE if i else BRANCO, stroke=8, sc=(5, 10, 16))
    else:
        colar(img, exp['sarcastico'], W / 2, H, 2.3)
        g = ease((dt - 1.6) / 0.3)
        f = F_BLACK(78)
        d.rounded_rectangle((90, 360, W - 90, 640), 22, fill=(5, 10, 16, int(225 * g)), outline=AMBAR + (int(255 * g),), width=4)
        texto_centro(d, 400, 'NÃO É', f, AMBAR + (int(255 * g),))
        texto_centro(d, 490, 'RECOMENDAÇÃO.', f, BRANCO + (int(255 * g),))
        texto_centro(d, 585, 'É leitura de gráfico.', F_BOLD(40), (200, 205, 215, int(255 * g)))
    return img

def cena_cta(t, dt):
    img = fundo2.copy().convert('RGBA'); d = ImageDraw.Draw(img)
    x = W * 0.5 + 500 * (1 - mola(dt / 0.8))
    colar(img, pisc, x, H - 40, 1100 / pisc.height)
    a = ease((dt - 0.5) / 0.4)
    d.rounded_rectangle((70, 300, W - 70, 560), 24, fill=(5, 10, 16, int(230 * a)), outline=VERDE + (int(255 * a),), width=4)
    texto_centro(d, 330, 'QUANTO VALE', F_BLACK(84), BRANCO + (int(255 * a),))
    texto_centro(d, 425, 'A SUA CARTEIRA?', F_BLACK(84), VERDE + (int(255 * a),))
    texto_centro(d, 600, 'Escaneie no BINDER Vision', F_BOLD(46), BRANCO + (int(255 * a),), stroke=4, sc=(5, 10, 16))
    texto_centro(d, 660, 'e veja o valor de referência', F_BOLD(46), BRANCO + (int(255 * a),), stroke=4, sc=(5, 10, 16))
    texto_centro(d, 730, 'Estimativa, não oferta de compra.', F_BOLD(28), (190, 195, 205, int(255 * a)), stroke=3, sc=(5, 10, 16))
    return img

def quadro(t):
    for a, b, tipo, dd in CENAS:
        if a <= t < b or (tipo == 'cta' and t >= a):
            dt = t - a
            if tipo == 'gancho': img = cena_gancho(t, dt)
            elif tipo == 'carta': img = cena_carta(t, dt, dd['k'], dd['rot'], dd['cor'], dd['seta'], dd['num'], dd['sub'], dd['exp'])
            elif tipo == 'dip': img = cena_dip(t, dt)
            else: img = cena_cta(t, dt)
            # flash curto no corte
            if dt < 0.08 and a > 0:
                img = Image.blend(img, Image.new('RGBA', (W, H), (255, 255, 255, 255)), 0.35 * (1 - dt / 0.08))
            if NARR is None: legenda(img, t)
            return img.convert('RGB')

# ---------- trilha sintetizada (pregão: batida + baixo + bips de cotação) ----------
def trilha(dur, sr=48000):
    n = int(dur * sr); tt = np.arange(n) / sr; out = np.zeros(n)
    bpm = 118; beat = 60 / bpm
    for i in range(int(dur / beat) + 1):
        s = int(i * beat * sr)
        k = np.arange(int(0.25 * sr)) / sr
        kick = np.sin(2 * np.pi * (55 + 90 * np.exp(-k * 30)) * k) * np.exp(-k * 9)
        out[s:s + len(k)] += 0.55 * kick[:max(0, n - s)]
        hs = int((i * beat + beat / 2) * sr); hk = np.arange(int(0.05 * sr))
        hat = np.random.default_rng(i).standard_normal(len(hk)) * np.exp(-hk / sr * 80)
        out[hs:hs + len(hk)] += 0.12 * hat[:max(0, n - hs)]
    notas = [41.2, 41.2, 49.0, 36.7]
    for i in range(int(dur / (beat * 2)) + 1):
        s = int(i * beat * 2 * sr); f0 = notas[(i // 2) % 4]
        k = np.arange(int(beat * 1.9 * sr)) / sr
        bass = np.sign(np.sin(2 * np.pi * f0 * k)) * 0.5 + np.sin(2 * np.pi * f0 * 2 * k) * 0.3
        bass *= np.exp(-k * 1.5)
        out[s:s + len(k)] += 0.18 * bass[:max(0, n - s)]
    for a, b, *_ in CENAS[1:]:  # bip de cotação em cada corte
        s = int(a * sr); k = np.arange(int(0.18 * sr)) / sr
        bip = np.sin(2 * np.pi * 1760 * k) * np.exp(-k * 25)
        out[s:s + len(k)] += 0.25 * bip[:max(0, n - s)]
    fade = np.minimum(1, (dur - tt) / 0.6)
    out *= np.clip(fade, 0, 1) * 0.6
    return np.stack([out, out], 1)

if __name__ == '__main__':
    import wave
    a = trilha(DUR)
    a = (np.clip(a, -1, 1) * 32767).astype('<i2')
    with wave.open('trilha.wav', 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(48000); w.writeframes(a.tobytes())
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'corpo.mp4'], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(quadro(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    outro = sys.argv[4] if len(sys.argv) > 4 else '/home/claude/repo/comum/outro/outro_binder_916.mp4'
    # junta corpo + fecho, áudio da trilha (com narração, se houver) normalizado
    mix = '[1:a]volume=1[m]' if NARR is None else '[1:a]volume=0.35[m];[2:a]aresample=48000,volume=1[n];[m][n]amix=inputs=2:duration=first:normalize=0[m2]'
    lbl = '[m]' if NARR is None else '[m2]'
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-i', 'corpo.mp4', '-i', 'trilha.wav']
    if NARR: cmd += ['-i', NARR]
    cmd += ['-i', outro, '-filter_complex',
            f'{mix};{lbl}apad=pad_dur=4,loudnorm=I=-14:TP=-1.5:LRA=11[a];[0:v][{3 if NARR else 2}:v]concat=n=2:v=1:a=0[v]',
            '-map', '[v]', '-map', '[a]', '-shortest', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', OUT]
    subprocess.run(cmd, check=True)
    print('ok', OUT)
