"""LL-MEME01 · «O que é a vida? A vida é uma maravilha» — Reel mudo 9:16 (o áudio entra pela biblioteca do Instagram).
Uso: python3 -I meme_vida.py <pasta_cartas> <pasta_frames>
Cena A (0–2,5 s): cinco comuns reais coladas no muro, uma a uma. Cena B (2,5–7 s): a última carta é a Sheoldred.
Zero créditos: PIL + numpy; cartas do Scryfall (não versionar)."""
import sys, os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, DUR, CORTE = 1080, 1920, 30, 7.0, 2.5
CART, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
GF = '/usr/share/fonts/truetype/google-fonts/ofl/'
F_MEME = GF + 'archivoblack/ArchivoBlack-Regular.ttf'
F_LAB = GF + 'anton/Anton-Regular.ttf'
PRETO, VERDE, ROSA, AMARELO = (5, 10, 16), (16, 185, 129), (230, 30, 110), (255, 205, 40)
rng = np.random.default_rng(7)

# ---------- muro rosa de lambe-lambe (procedural) ----------
def muro():
    base = np.zeros((H, W, 3), np.float32); base[:] = (226, 38, 112)
    lf = np.array(Image.fromarray((rng.random((6, 4)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255
    base *= (0.92 + 0.1 * lf)[..., None]
    base += rng.normal(0, 9, (H, W, 1))
    im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert('RGBA')
    # restos de cartazes antigos rasgados nas bordas
    for k in range(18):
        lado = k % 2; x = int(rng.integers(-40, 60)) if lado == 0 else int(rng.integers(W - 60, W + 40)); y = int(rng.integers(0, H))
        w, h = int(rng.integers(90, 170)), int(rng.integers(120, 300))
        c = tuple(int(v) for v in [(235, 225, 205), (28, 28, 32), (205, 185, 150), (245, 240, 228)][k % 4])
        p = papel(w, h, c, 200 + k).rotate(float(rng.uniform(-8, 8)), Image.BICUBIC, expand=True)
        im.alpha_composite(p, (x - p.width // 2, y - p.height // 2))
    im = im.convert('RGB').filter(ImageFilter.GaussianBlur(0.5))
    g = np.array(im, np.float32) + rng.normal(0, 6, (H, W, 1))
    return Image.fromarray(np.clip(g, 0, 255).astype(np.uint8))

def rasgo(w, h, amp=8, seed=1):
    r = np.random.default_rng(seed); m = Image.new('L', (w, h), 0); d = ImageDraw.Draw(m)
    pts = []
    for x in range(0, w + 1, 12): pts.append((x, r.integers(0, amp)))
    for y in range(0, h + 1, 12): pts.append((w - r.integers(0, amp), y))
    for x in range(w, -1, -12): pts.append((x, h - r.integers(0, amp)))
    for y in range(h, -1, -12): pts.append((r.integers(0, amp), y))
    d.polygon(pts, fill=255); return m

def papel(w, h, cor=(214, 190, 150), seed=1):
    r = np.random.default_rng(seed)
    a = np.zeros((h, w, 3), np.float32); a[:] = cor
    a += r.normal(0, 10, (h, w, 1))
    p = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA'); p.putalpha(rasgo(w, h, 10, seed)); return p

def sombra(img, off=(10, 14), blur=12, op=110):
    a = img.split()[-1].point(lambda v: v * op // 255)
    s = Image.new('RGBA', img.size, (0, 0, 0, 0)); s.putalpha(a)
    pad = blur * 3; S = Image.new('RGBA', (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
    S.paste(s, (pad, pad)); return S.filter(ImageFilter.GaussianBlur(blur)), pad, off

def colar(fundo, img, cx, cy, ang=0, esc=1.0, som=True):
    if esc != 1: img = img.resize((max(1, int(img.width * esc)), max(1, int(img.height * esc))), Image.LANCZOS)
    img = img.rotate(ang, Image.BICUBIC, expand=True)
    if som:
        S, pad, off = sombra(img)
        fundo.alpha_composite(S, (int(cx - S.width / 2 + off[0]), int(cy - S.height / 2 + off[1])))
    fundo.alpha_composite(img, (int(cx - img.width / 2), int(cy - img.height / 2)))

def carta(path, larg):
    c = Image.open(path).convert('RGBA'); h = int(c.height * larg / c.width)
    return c.resize((larg, h), Image.LANCZOS)

def fita(larg=150, alt=46, seed=1):
    r = np.random.default_rng(seed)
    a = np.zeros((alt, larg, 4), np.float32); a[..., :3] = (238, 232, 214); a[..., :3] += r.normal(0, 6, (alt, larg, 1)); a[..., 3] = 205
    f = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')
    m = rasgo(larg, alt, 6, seed); f.putalpha(Image.fromarray((np.array(m, np.float32) * 205 / 255).astype(np.uint8))); return f

def com_fitas(c, seed):
    """carta + fitas só nos cantos de cima (regra Lambe-lambe)"""
    pad = 40; T = Image.new('RGBA', (c.width + 2 * pad, c.height + 2 * pad), (0, 0, 0, 0)); T.paste(c, (pad, pad), c)
    for i, (x, ang) in enumerate(((pad + 10, 35), (pad + c.width - 10, -35))):
        f = fita(130, 40, seed + i).rotate(ang, Image.BICUBIC, expand=True)
        T.alpha_composite(f, (int(x - f.width / 2), int(pad + 6 - f.height / 2)))
    return T

def texto_meme(d, txt, cy, tam, larg_max=980):
    f = ImageFont.truetype(F_MEME, tam)
    while d.textlength(txt, font=f) > larg_max: tam -= 4; f = ImageFont.truetype(F_MEME, tam)
    d.text((W / 2, cy), txt, font=f, fill='white', anchor='mm', stroke_width=max(6, tam // 9), stroke_fill=PRETO)

def etiqueta(txt, cor, tam=64, cor_txt=PRETO, seed=3, padx=40, pady=22):
    f = ImageFont.truetype(F_LAB, tam); tmp = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    bb = tmp.textbbox((0, 0), txt, font=f); w, h = bb[2] - bb[0] + 2 * padx, bb[3] - bb[1] + 2 * pady
    p = papel(w, h, cor, seed); d = ImageDraw.Draw(p)
    d.text((w / 2, h / 2), txt, font=f, fill=cor_txt, anchor='mm'); return p

def faixa_credito(linhas):
    w, h = 940, 40 + 34 * len(linhas)
    p = papel(w, h, PRETO, 11); d = ImageDraw.Draw(p); f = ImageFont.truetype(F_LAB, 26)
    for i, l in enumerate(linhas): d.text((w / 2, 24 + 34 * i + 14), l, font=f, fill=(225, 218, 205), anchor='mm')
    d.line([(60, h - 10), (w - 60, h - 12)], fill=ROSA, width=4); return p

# ---------- material ----------
COMUNS = [('dmu_156.png', 'Bog Badger', 'Sam Burley'), ('dmu_41.png', 'Academy Wall', 'Adam Paquette'),
          ('dmu_128.png', 'Goblin Picker', 'Vladimir Krisetskiy'), ('dmu_69.png', 'Tidepool Turtle', 'Andrew Mar'),
          ('dmu_5.png', 'Argivian Phalanx', 'Josh Hass')]
POS = [(-170, -60, -9), (170, -90, 7), (-120, 120, 5), (190, 110, -6), (0, 20, -2)]
T_COMUM = [0.0, 0.45, 0.9, 1.35, 1.8]
MURO = muro().convert('RGBA')
cartas_c = [com_fitas(carta(os.path.join(CART, a), 500), 20 + i) for i, (a, _, _) in enumerate(COMUNS)]
rara = com_fitas(carta(os.path.join(CART, 'dmu_97.png'), 630), 99)
eti_comum = [etiqueta(f'COMUM ×{i+1}', (214, 190, 150), 66, PRETO, 30 + i) for i in range(5)]
eti_ultima = etiqueta('A ÚLTIMA CARTA DO BOOSTER', AMARELO, 58, PRETO, 77)
cred_a = faixa_credito(['Dominaria United (DMU): Bog Badger · Sam Burley | Academy Wall · Adam Paquette',
                        'Goblin Picker · Vladimir Krisetskiy | Tidepool Turtle · Andrew Mar',
                        'Argivian Phalanx · Josh Hass | © Wizards of the Coast'])
cred_b = faixa_credito(['Liliana of the Veil (DMU 97) · Martina Fačková · © Wizards of the Coast'])

def ease_slap(u):
    """0→1: cai de 1.18 para 1.0 com pequeno overshoot"""
    if u < 0: return None
    if u >= 1: return 1.0
    return 1.0 + 0.18 * (1 - u) ** 2 * math.cos(u * 6)

CX, CY = W / 2, 1000
cena_a_cache = {}

def quadro(t):
    if t < CORTE:
        f = MURO.copy(); d = ImageDraw.Draw(f)
        n = 0; shake = (0, 0)
        for i, t0 in enumerate(T_COMUM):
            u = (t - t0) / 0.14
            e = ease_slap(u) if t >= t0 else None
            if e is None: continue
            n = i + 1
            dx, dy, ang = POS[i]
            if u < 1.6: shake = (int(rng.integers(-5, 6)), int(rng.integers(-5, 6)))
            colar(f, cartas_c[i], CX + dx, CY + dy, ang, e)
        if n: colar(f, eti_comum[n - 1], W / 2, 1480, -2)
        colar(f, cred_a, W / 2, 1640, -0.6, som=False)
        texto_meme(d, 'O QUE É A VIDA?', 300, 104)
        if shake != (0, 0):
            g = Image.new('RGBA', (W, H), (0, 0, 0, 255)); g.alpha_composite(f, shake); f = g
        return f
    # cena B
    tb = t - CORTE
    f = MURO.copy()
    # pilha de comuns fica atrás, escurecida
    pil = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for i in range(5):
        dx, dy, ang = POS[i]; colar(pil, cartas_c[i], CX + dx, CY + 40 + dy, ang, 0.92)
    a = np.array(pil); a[..., :3] = (a[..., :3] * 0.45).astype(np.uint8); f.alpha_composite(Image.fromarray(a))
    e = ease_slap(tb / 0.16) or 1.0
    zoom = 1.0 + 0.035 * min(tb / 4.5, 1)
    colar(f, rara, CX, CY - 40, 1.5, e * zoom)
    if tb > 0.35:
        u = min((tb - 0.35) / 0.12, 1); colar(f, eti_ultima, W / 2, 1545, -3, 1.0 + 0.25 * (1 - u))
    colar(f, cred_b, W / 2, 1660, -0.6, som=False)
    d = ImageDraw.Draw(f)
    texto_meme(d, 'A VIDA É UMA', 250, 112); texto_meme(d, 'MARAVILHA', 380, 150)
    if tb < 2 / FPS:  # flash de 2 quadros no corte
        f = Image.blend(f, Image.new('RGBA', (W, H), (255, 255, 255, 255)), 0.75 if tb < 1 / FPS else 0.35)
    return f

N = int(DUR * FPS)
for k in range(N):
    quadro(k / FPS).convert('RGB').save(os.path.join(OUT, f'{k:04d}.jpg'), quality=93)
print('quadros:', N)
