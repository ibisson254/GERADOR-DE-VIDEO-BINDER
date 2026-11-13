#!/usr/bin/env python3
"""PREGÃO MAGIC — renderizador de quadros (1080x1920, 30 fps).

Uso: python3 render.py SAIDA.mp4 [--de S --ate S] [--quadros 1,2,3 --png DIR]
Os quadros vão em stream (rawvideo) para o ffmpeg; o áudio é montado à parte (audio.py).
Fontes Geist: npm pack geist (OFL) -> FONTES (variável de ambiente GEIST_DIR).
"""
import json, math, os, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

AQUI = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
B = 60 / 184.5703          # batida da música
BAR = 4 * B
GEIST = os.environ.get("GEIST_DIR", "/tmp/geist/package/dist/fonts")
DUR = 43.0                  # sem o fecho (3,87 s) -> 46,87 s no total

# Paleta BINDER + vermelho de queda
PRETO = (5, 10, 16); ARDOSIA = (15, 23, 42); VERDE = (16, 185, 129)
VERDE_CL = (110, 231, 183); VERM = (239, 68, 68); VERM_CL = (252, 165, 165)
BRANCO = (241, 245, 249); CINZA = (148, 163, 184); AMBAR = (251, 191, 36)

D = json.load(open(os.path.join(AQUI, "dados.json")))
CAMBIO = D["cambio"]["usd_brl"]

_fc = {}
def F(peso, tam, mono=False):
    k = (peso, tam, mono)
    if k not in _fc:
        p = f"{GEIST}/geist-mono/GeistMono-{peso}.ttf" if mono else f"{GEIST}/geist-sans/Geist-{peso}.ttf"
        _fc[k] = ImageFont.truetype(p, tam)
    return _fc[k]

def brl(usd):
    v = round(usd * CAMBIO)
    return f"R$ {v:,}".replace(",", ".")

def usd(v):
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"US$ {s}"

# ---------- easing ----------
def cl(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, t0, d): return cl((t - t0) / d) if d > 0 else (1.0 if t >= t0 else 0.0)
def eo3(x): return 1 - (1 - x) ** 3
def eo5(x): return 1 - (1 - x) ** 5
def ei3(x): return x ** 3
def eback(x, s=1.9): x -= 1; return x * x * ((s + 1) * x + s) + 1
def lerp(a, b, x): return a + (b - a) * x

# ---------- recursos ----------
CARTAS = {}
for k in ["uthros", "moonshadow", "watery_lcars", "steam_lcars", "watery_trk", "dark_matter"]:
    CARTAS[k] = Image.open(os.path.join(AQUI, "cartas", f"{k}.png")).convert("RGBA")
ARTE = {}
for k in CARTAS:
    a = Image.open(os.path.join(AQUI, "cartas", f"{k}_art.jpg")).convert("RGB") if os.path.exists(os.path.join(AQUI, "cartas", f"{k}_art.jpg")) else None
    if a is not None:
        r = max(W * 1.25 / a.width, H * 1.15 / a.height)
        a = a.resize((int(a.width * r), int(a.height * r)), Image.LANCZOS).filter(ImageFilter.GaussianBlur(26))
        ARTE[k] = a
# arte do Steam Vents LCARS (não descarregada à parte): usa-se o recorte da própria carta
if "steam_lcars" not in ARTE:
    c = CARTAS["steam_lcars"].convert("RGB").crop((60, 120, 684, 600))
    r = max(W * 1.25 / c.width, H * 1.15 / c.height)
    ARTE["steam_lcars"] = c.resize((int(c.width * r), int(c.height * r)), Image.LANCZOS).filter(ImageFilter.GaussianBlur(26))

_cc = {}
def carta(k, larg, rot=0.0, rapido=False):
    larg = max(8, int(larg))
    key = (k, larg, round(rot, 1), rapido)
    if key in _cc: return _cc[key]
    im = CARTAS[k]
    h = int(im.height * larg / im.width)
    im = im.resize((larg, h), Image.BILINEAR if rapido else Image.LANCZOS)
    if abs(rot) > 0.05:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    if len(_cc) > 400: _cc.clear()
    _cc[key] = im
    return im

def sombra(cv, im, cx, cy, alpha=150, blur=28, dy=24):
    a = im.split()[3].point(lambda v: v * alpha // 255)
    s = Image.new("RGBA", im.size, (0, 0, 0, 0)); s.putalpha(a)
    pad = blur * 2
    big = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    big.paste(s, (pad, pad), s)
    big = big.filter(ImageFilter.GaussianBlur(blur))
    cv.alpha_composite(big, (int(cx - big.width / 2), int(cy - big.height / 2 + dy)))

def por_carta(cv, k, cx, cy, larg, rot=0.0, alpha=1.0, rapido=False, brilho=None, sh=True):
    im = carta(k, larg, rot, rapido)
    if alpha < 1:
        im = im.copy(); im.putalpha(im.split()[3].point(lambda v: int(v * alpha)))
    if sh: sombra(cv, im, cx, cy, int(150 * alpha))
    if brilho:  # aura colorida atrás da carta (não toca na carta)
        g = Image.new("RGBA", (im.width + 160, im.height + 160), (0, 0, 0, 0))
        dg = ImageDraw.Draw(g)
        dg.rounded_rectangle((80, 80, 80 + im.width, 80 + im.height), 40, fill=brilho[0] + (int(brilho[1] * alpha),))
        g = g.filter(ImageFilter.GaussianBlur(40))
        cv.alpha_composite(g, (int(cx - g.width / 2), int(cy - g.height / 2)))
    cv.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
    return im.size

# ---------- fundo ----------
def fundo(t, tom=None, arte=None, arte_alpha=0.0, dx=0.0, grade=True):
    cv = Image.new("RGBA", (W, H), PRETO + (255,))
    if arte and arte_alpha > 0:
        a = ARTE[arte]
        ox = int((W - a.width) / 2 + dx - 30 * math.sin(t * 0.6)); oy = int((H - a.height) / 2 + 20 * math.cos(t * 0.5))
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); lay.paste(a, (ox, oy))
        lay.putalpha(int(255 * arte_alpha))
        cv.alpha_composite(lay)
        cv.alpha_composite(Image.new("RGBA", (W, H), PRETO + (150,)))
    if tom:
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dg = ImageDraw.Draw(g)
        dg.ellipse((-200, 300, W + 200, 1700), fill=tom + (60,))
        cv.alpha_composite(g.filter(ImageFilter.GaussianBlur(160)))
    if grade:
        d = ImageDraw.Draw(cv)
        off = (t * 40) % 90
        for x in range(0, W + 90, 90):
            d.line((x - off, 0, x - off, H), fill=(30, 41, 59, 70), width=1)
        for y in range(0, H + 90, 90):
            d.line((0, y + off, W, y + off), fill=(30, 41, 59, 70), width=1)
    return cv

TICKER = ("UTHROS RESEARCH CRAFT ▲  ·  MOONSHADOW ▲ +93%  ·  WATERY GRAVE LCARS ▼ −74,7%  ·  "
          "STEAM VENTS LCARS ▼ −60,7%  ·  SHOCKLANDS ▼ MÍNIMA HISTÓRICA  ·  MUNDIAL 32  ·  ")

def ticker(cv, t, y, vel=160, cor=None, alpha=200):
    d = ImageDraw.Draw(cv)
    d.rectangle((0, y, W, y + 54), fill=(10, 16, 28, alpha))
    d.line((0, y, W, y), fill=(51, 65, 85, 255)); d.line((0, y + 54, W, y + 54), fill=(51, 65, 85, 255))
    f = F("Medium", 26, True)
    tw = d.textlength(TICKER, font=f)
    x = -((t * vel) % tw)
    while x < W:
        cx = x
        for parte in TICKER.split("  ·  "):
            if not parte: continue
            c = VERDE if "▲" in parte else (VERM if "▼" in parte else CINZA)
            d.text((cx, y + 12), parte, font=f, fill=(cor or c) + (255,))
            cx += d.textlength(parte + "  ·  ", font=f)
        x += tw

# ---------- texto ----------
def texto_c(cv, txt, cx, y, fonte, cor, alpha=1.0, escala=1.0, sombra_txt=True, glow=None, anchor="mt"):
    if alpha <= 0: return
    if abs(escala - 1) > 0.01:
        f2 = ImageFont.truetype(fonte.path, max(6, int(fonte.size * escala)))
    else:
        f2 = fonte
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    if glow:
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dg = ImageDraw.Draw(g)
        dg.text((cx, y), txt, font=f2, fill=glow + (200,), anchor=anchor)
        lay.alpha_composite(g.filter(ImageFilter.GaussianBlur(18)))
    if sombra_txt:
        d.text((cx + 3, y + 5), txt, font=f2, fill=(0, 0, 0, 200), anchor=anchor)
    d.text((cx, y), txt, font=f2, fill=cor + (255,), anchor=anchor)
    if alpha < 1:
        lay.putalpha(lay.split()[3].point(lambda v: int(v * alpha)))
    cv.alpha_composite(lay)

def chip(cv, txt, cx, y, cor, alpha=1.0, tam=30):
    if alpha <= 0: return
    f = F("Bold", tam, True)
    d0 = ImageDraw.Draw(cv)
    tw = d0.textlength(txt, font=f)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((cx - tw / 2 - 22, y, cx + tw / 2 + 22, y + tam + 24), 10, fill=cor + (235,))
    d.text((cx, y + 11), txt, font=f, fill=PRETO + (255,), anchor="mt")
    if alpha < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * alpha)))
    cv.alpha_composite(lay)

def fonte_linha(cv, txt, alpha=1.0, y=1488):
    texto_c(cv, txt, 470, y, F("Medium", 25, True), CINZA, alpha, sombra_txt=False)

def linhas(cv, ls, cx, y, fonte, cor, alpha=1.0, esp=1.25):
    for i, l in enumerate(ls):
        texto_c(cv, l, cx, y + i * fonte.size * esp, fonte, cor, alpha)

# ---------- gráfico ----------
def serie(seed, n, ini, fim, ruido=0.08):
    rnd = random.Random(seed)
    v = []
    for i in range(n):
        x = i / (n - 1)
        base = ini + (fim - ini) * (x ** 1.6 if fim > ini else 1 - (1 - x) ** 0.5)
        v.append(base + (rnd.random() - 0.5) * ruido * max(ini, fim) * (1 - x * 0.6))
    v[0] = ini; v[-1] = fim
    return v

def grafico(cv, vals, p, cor, caixa, espessura=7, area=True):
    if p <= 0: return
    x0, y0, x1, y1 = caixa
    lo, hi = min(vals), max(vals)
    n = len(vals); k = max(2, int(1 + (n - 1) * p))
    pts = [(x0 + (x1 - x0) * i / (n - 1), y1 - (y1 - y0) * (vals[i] - lo) / (hi - lo + 1e-9)) for i in range(k)]
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    if area and len(pts) > 1:
        d.polygon(pts + [(pts[-1][0], y1), (pts[0][0], y1)], fill=cor + (40,))
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dg = ImageDraw.Draw(g)
    dg.line(pts, fill=cor + (255,), width=espessura * 3, joint="curve")
    lay.alpha_composite(g.filter(ImageFilter.GaussianBlur(12)))
    d.line(pts, fill=cor + (255,), width=espessura, joint="curve")
    ex, ey = pts[-1]
    d.ellipse((ex - 12, ey - 12, ex + 12, ey + 12), fill=BRANCO + (255,))
    cv.alpha_composite(lay)

def flash(cv, a, cor=(255, 255, 255)):
    if a > 0: cv.alpha_composite(Image.new("RGBA", (W, H), cor + (int(255 * cl(a)),)))

def tremor(t, t0, forca=18, dur=0.25):
    p = prog(t, t0, dur)
    if p <= 0 or p >= 1: return 0, 0
    a = forca * (1 - p)
    return int(a * math.sin(t * 90)), int(a * math.cos(t * 77))

def deslocar(cv, dx, dy):
    if dx == 0 and dy == 0: return cv
    out = Image.new("RGBA", (W, H), PRETO + (255,)); out.alpha_composite(cv, (0, 0)) if False else out.paste(cv, (dx, dy))
    return out

def blur_mov(cv, quant):
    """whip pan: desfoque horizontal por média de deslocamentos"""
    if quant < 2: return cv
    a = np.asarray(cv.convert("RGB")).astype(np.float32)
    acc = np.zeros_like(a); n = 7
    for i in range(n):
        s = int((i - n // 2) * quant / n)
        acc += np.roll(a, s, axis=1)
    return Image.fromarray((acc / n).astype(np.uint8)).convert("RGBA")

def zoom_img(cv, z, cx=W / 2, cy=H / 2):
    if abs(z - 1) < 0.002: return cv
    w2, h2 = W / z, H / z
    box = (cx - w2 / 2, cy - h2 / 2, cx + w2 / 2, cy + h2 / 2)
    return cv.transform((W, H), Image.EXTENT, box, Image.BILINEAR)

def glitch(cv, forca, seed):
    if forca <= 0: return cv
    rnd = random.Random(seed)
    a = np.asarray(cv.convert("RGB")).copy()
    for _ in range(int(6 * forca) + 1):
        y = rnd.randrange(0, H - 60); h = rnd.randrange(8, 60); s = rnd.randrange(-80, 80)
        a[y:y + h] = np.roll(a[y:y + h], int(s * forca), axis=1)
    r = np.roll(a[..., 0], int(10 * forca), axis=1)
    a[..., 0] = r
    return Image.fromarray(a).convert("RGBA")

# ---------- linha do tempo ----------
# tempos em segundos do vídeo (grelha da música: B = 0,325 s, compasso = 1,30 s)
T = dict(
    burst=0.0, smash=B, pct=2 * B, graf=3 * B, nome=4 * B, preco=6 * B,
    whip=8 * B, alta_tease=8 * B + 0.16, titulo=12 * B,
    altas=16 * B, uthros=18 * B, moon=34 * B,
    quedas=50 * B, watery=52 * B, steam=68 * B, shock=78 * B,
    radar=86 * B, binder=102 * B, fecho_txt=118 * B, fim=DUR,
)

SRC_TCG = "Fonte: TCGplayer, preço de mercado NM · conversão R$ 5,59 (10/11)"

def bloco_carta(cv, t, k, t0, cor, chip_txt, nome, edicao, pct_txt, antes, depois, causa, fonte, periodo,
                entrada="queda", seed=1, larg=540, cy=950, preco_ini=None, fim=None, causa_t=None):
    """Plano-padrão de revelação: carta, nome, cotação, variação, causa, fonte."""
    tl = t - t0
    # entrada da carta
    if entrada == "queda":
        p = eo5(prog(t, t0, 0.32)); y = lerp(-700, cy, p); rot = lerp(-8, 0, p); s = 1.0
    elif entrada == "zoom":
        p = eo5(prog(t, t0, 0.45)); y = cy; rot = 0; s = lerp(2.4, 1.0, p)
    else:  # match: já está no lugar
        y = cy; rot = 0; s = 1.0
    push = 1 + 0.035 * cl(tl / 5)               # push-in lento
    tp0 = t0 + 4 * B; tc0 = causa_t if causa_t is not None else t0 + 8 * B
    for tb in (tp0, tc0):                       # punch na revelação do número e da causa
        pb = prog(t, tb, 0.3)
        if 0 < pb < 1: push *= 1 + 0.07 * (1 - eo3(pb))
    l = larg * s * push
    dx, dy = tremor(t, t0 + (0.3 if entrada == "queda" else 0), 22)
    por_carta(cv, k, 540 + dx, y + dy, l, rot, rapido=(tl < 0.5 and entrada != "match"), brilho=(cor, 120))
    # topo: chip + variação + nome
    chip(cv, chip_txt, 540, 236, cor, alpha=eo3(prog(t, t0 + 0.05, 0.15)), tam=28)
    tp = t0 + 4 * B
    pp = prog(t, tp, 0.22)
    if pp > 0:
        texto_c(cv, pct_txt, 540, 300, F("Black", 132), cor, escala=lerp(1.9, 1.0, eback(pp)), alpha=cl(pp * 3), glow=cor)
    texto_c(cv, nome, 540, 448, F("Bold", 50), BRANCO, alpha=eo3(prog(t, t0 + 0.12, 0.2)))
    texto_c(cv, edicao, 540, 510, F("Regular", 27, True), CINZA, alpha=eo3(prog(t, t0 + 0.2, 0.2)))
    # base: cotação -> causa
    ytop = cy + larg * 1.3978 / 2 + 22
    tc = causa_t if causa_t is not None else t0 + 8 * B
    pc = prog(t, tp, 0.6)
    out_p = 1 - prog(t, tc - 0.12, 0.12)
    if pc > 0 and out_p > 0:
        ini = preco_ini if preco_ini is not None else antes
        v = lerp(ini, depois, eo3(pc))
        txt_a = antes if isinstance(antes, str) else usd(antes)
        texto_c(cv, f"{txt_a}  →  {usd(v)}", 540, ytop, F("Bold", 50, True), BRANCO, alpha=out_p * cl(pc * 4))
        texto_c(cv, periodo, 540, ytop + 64, F("Medium", 30, True), cor, alpha=out_p * cl(pc * 4))
    pk = prog(t, tc, 0.25)
    if pk > 0:
        for i, l in enumerate(causa):
            texto_c(cv, l, 540, ytop + i * 50 + lerp(30, 0, eo3(pk)), F("SemiBold", 38), BRANCO if i else cor, alpha=eo3(pk))
    fonte_linha(cv, fonte, alpha=eo3(prog(t, t0 + 0.3, 0.3)), y=1500)

def quadro(t):
    # ---------------- BLOCO A ----------------
    if t < T["whip"]:
        cv = fundo(t, VERM, "watery_lcars", 0.35 if t >= T["smash"] else 0.0)
        if t < T["smash"]:
            # explosão de quatro cartas reais
            p = eback(prog(t, 0, B * 0.9), 1.4)
            for i, (k, ang, dist, rot) in enumerate([("uthros", -125, 250, -12), ("moonshadow", -55, 250, 10),
                                                     ("steam_lcars", 135, 260, 9), ("watery_lcars", 45, 260, -8)]):
                a = math.radians(ang)
                cx = 540 + math.cos(a) * dist * p; cy = 900 + math.sin(a) * dist * p * 1.35
                por_carta(cv, k, cx, cy, lerp(200, 400, p), rot * p, rapido=True)
            flash(cv, 1 - prog(t, 0, 0.1))
            ticker(cv, t, 120); ticker(cv, t + 3, 1745)
            return cv
        # smash: Watery Grave LCARS em destaque
        ticker(cv, t, 120); ticker(cv, t + 3, 1745)
        s = 1 + 0.02 * (t - T["smash"])
        g = serie(7, 40, 43.41, 10.99, 0.12)
        grafico(cv, g, eo3(prog(t, T["graf"], 0.7)), VERM, (60, 640, 1020, 1300), 8)
        dx, dy = tremor(t, T["pct"], 26)
        por_carta(cv, "watery_lcars", 540 + dx, 960 + dy, 560 * s, brilho=(VERM, 130))
        pp = prog(t, T["pct"], 0.2)
        if pp > 0:
            texto_c(cv, "−74,7%", 540, 250, F("Black", 150), VERM, escala=lerp(2.2, 1.0, eback(pp)), glow=VERM, alpha=cl(pp * 3))
            texto_c(cv, "EM 7 DIAS", 540, 410, F("Bold", 36, True), VERM_CL, alpha=eo3(prog(t, T["pct"] + 0.15, 0.2)))
        pn = prog(t, T["nome"], 0.2)
        if pn > 0:
            ytop = 960 + 560 * 1.3978 / 2 + 22
            texto_c(cv, "WATERY GRAVE · LCARS", 540, ytop, F("Bold", 46), BRANCO, alpha=eo3(pn))
            texto_c(cv, f"{usd(43.41)} → {usd(10.99)}", 540, ytop + 62, F("Bold", 36, True), VERM_CL, alpha=eo3(prog(t, T["preco"], 0.2)))
        cv = deslocar(cv, 0, 0)
        flash(cv, 0.7 * (1 - prog(t, T["smash"], 0.08)), VERM)
        return cv
    if t < T["titulo"]:
        # whip pan -> Uthros: "e outra mais que triplicou"
        cv = fundo(t, VERDE, "uthros", 0.35)
        ticker(cv, t, 120); ticker(cv, t + 3, 1745)
        pw = prog(t, T["whip"], 0.22)
        off = lerp(1100, 0, eo5(pw))
        g = serie(3, 40, 2.0, 7.26, 0.1)
        grafico(cv, g, eo3(prog(t, T["whip"] + 0.1, 0.8)), VERDE, (60, 640, 1020, 1300), 8)
        por_carta(cv, "uthros", 540 + off, 960, 560, brilho=(VERDE, 130), rapido=pw < 1)
        pp = prog(t, T["alta_tease"] + B, 0.2)
        if pp > 0:
            texto_c(cv, "MAIS DE 3×", 540, 250, F("Black", 140), VERDE, escala=lerp(2.0, 1.0, eback(pp)), glow=VERDE, alpha=cl(pp * 3))
            texto_c(cv, "EM UM MÊS", 540, 410, F("Bold", 36, True), VERDE_CL, alpha=eo3(prog(t, T["alta_tease"] + B + 0.15, 0.2)))
        ytop = 960 + 560 * 1.3978 / 2 + 22
        texto_c(cv, "QUEM SOBE, QUEM CAI — E POR QUÊ", 540, ytop + 10, F("Bold", 38), BRANCO, alpha=eo3(prog(t, T["whip"] + 2 * BAR / 2, 0.2)))
        cv = blur_mov(cv, 260 * (1 - pw) if pw < 1 else 0)
        return cv
    if t < T["altas"]:
        # título com as cartas da pauta
        cv = fundo(t, ARDOSIA)
        ticker(cv, t, 120); ticker(cv, t + 3, 1745)
        p = eback(prog(t, T["titulo"], 0.3))
        texto_c(cv, "PREGÃO", 540, 330, F("Black", 190), BRANCO, escala=lerp(1.5, 1, p), alpha=cl(p * 2))
        texto_c(cv, "MAGIC", 540, 520, F("Black", 190), VERDE, escala=lerp(1.5, 1, p), alpha=cl(p * 2), glow=VERDE)
        texto_c(cv, "A BOLSA ABRIU · 13/11/2026", 540, 745, F("Bold", 36, True), CINZA, alpha=eo3(prog(t, T["titulo"] + 0.2, 0.2)))
        for i, k in enumerate(["uthros", "moonshadow", "watery_lcars", "steam_lcars"]):
            pi = eo5(prog(t, T["titulo"] + 0.1 + i * B / 2, 0.3))
            por_carta(cv, k, 160 + i * 253, lerp(1700, 1080, pi), 236, [-4, 2, -2, 4][i])
        # seta verde que sobe e leva ao bloco seguinte
        pa = prog(t, T["altas"] - 0.35, 0.35)
        if pa > 0:
            d = ImageDraw.Draw(cv); y = lerp(1400, -200, ei3(pa))
            d.polygon([(540, y), (470, y + 110), (515, y + 110), (515, y + 400), (565, y + 400), (565, y + 110), (610, y + 110)], fill=VERDE + (255,))
        return cv
    # ---------------- BLOCO B · ALTAS ----------------
    if t < T["uthros"]:
        cv = fundo(t, VERDE)
        p = prog(t, T["altas"], 2 * B)
        d = ImageDraw.Draw(cv)
        y = lerp(1700, 300, eo3(p))
        d.polygon([(540, y), (430, y + 170), (500, y + 170), (500, 1920), (580, 1920), (580, y + 170), (650, y + 170)], fill=VERDE + (255,))
        texto_c(cv, "AS ALTAS", 540, 820, F("Black", 150), BRANCO, escala=lerp(1.6, 1, eback(prog(t, T["altas"], 0.2))), glow=VERDE)
        texto_c(cv, "▲", 540, 1010, F("Black", 90, True), VERDE_CL, alpha=eo3(prog(t, T["altas"] + 0.1, 0.2)))
        return zoom_img(cv, 1 + 2.5 * ei3(prog(t, T["uthros"] - 0.2, 0.2)), 540, 420)
    if t < T["moon"]:
        cv = fundo(t, VERDE, "uthros", 0.45)
        ticker(cv, t, 120)
        bloco_carta(cv, t, "uthros", T["uthros"], VERDE, "▲ ALTA", "UTHROS RESEARCH CRAFT",
                    "Commander: Edge of Eternities · #7", "MAIS DE 3×",
                    "< US$ 2", 7.26,
                    ["Star Trek trouxe as naves", "Spacecraft de volta + comandantes", "de artefato de Reality Fracture"],
                    SRC_TCG, "meados de out → 13/11 · ≈ R$ 11 → " + brl(7.26),
                    entrada="zoom", preco_ini=2.0)
        pm = prog(t, T["moon"] - 0.15, 0.15)   # flash azul->preto do símbolo de mana (match cut)
        flash(cv, 0.35 * pm, (59, 130, 246))
        return cv
    if t < T["quedas"]:
        cv = fundo(t, VERDE, "moonshadow", 0.45)
        ticker(cv, t, 120)
        # match cut: mesma posição e escala; a carta de causa entra depois e a Moonshadow abre espaço
        tc = T["moon"] + 8 * B
        pk = eo5(prog(t, tc, 0.35))
        if pk <= 0:
            bloco_carta(cv, t, "moonshadow", T["moon"], VERDE, "▲ ALTA", "MOONSHADOW",
                        "Lorwyn Eclipsed · #110", "+93%", 14.0, 27.0, [], SRC_TCG,
                        "lançamento de Reality Fracture (out) → 12/11 · " + brl(14) + " → " + brl(27),
                        entrada="match", causa_t=tc + 10)
            flash(cv, 0.5 * (1 - prog(t, T["moon"], 0.1)), (255, 255, 255))
        else:
            # plano de causa: as duas cartas inteiras, lado a lado (paralaxe)
            chip(cv, "▲ ALTA · POR QUÊ?", 540, 236, VERDE, tam=28)
            texto_c(cv, "+93%", 540, 300, F("Black", 132), VERDE, glow=VERDE)
            por_carta(cv, "moonshadow", lerp(540, 300, pk), 930 + 10 * math.sin(t), lerp(540, 400, pk), lerp(0, -3, pk), brilho=(VERDE, 100))
            por_carta(cv, "dark_matter", lerp(1300, 770, pk), 990 - 10 * math.sin(t), 360, lerp(10, 4, pk), brilho=(AMBAR, 90))
            texto_c(cv, "+", 540, 900, F("Black", 90), AMBAR, alpha=pk)
            yb = 1290
            texto_c(cv, "Modern: o Rakdos Moonshadow", 540, yb, F("SemiBold", 40), BRANCO, alpha=pk)
            texto_c(cv, "ganhou Dark Matter Manipulator", 540, yb + 52, F("SemiBold", 40), BRANCO, alpha=pk)
            texto_c(cv, "(Reality Fracture)", 540, yb + 104, F("Regular", 32, True), AMBAR, alpha=pk)
            fonte_linha(cv, SRC_TCG, y=1500)
        # saída: speed ramp + zoom para o bloco das quedas
        pz = prog(t, T["quedas"] - 0.25, 0.25)
        return zoom_img(cv, 1 + 1.2 * ei3(pz))
    # ---------------- BLOCO C · QUEDAS ----------------
    if t < T["watery"]:
        cv = fundo(t, VERM)
        p = prog(t, T["quedas"], 2 * B)
        d = ImageDraw.Draw(cv)
        y = lerp(-300, 1100, ei3(p))
        d.polygon([(540, y + 170), (430, y), (500, y), (500, -1920), (580, -1920), (580, y), (650, y)], fill=VERM + (255,))
        texto_c(cv, "AS QUEDAS", 540, 820, F("Black", 150), BRANCO, escala=lerp(0.6, 1, eback(prog(t, T["quedas"], 0.15))), glow=VERM)
        texto_c(cv, "▼", 540, 1010, F("Black", 90, True), VERM_CL, alpha=eo3(prog(t, T["quedas"] + 0.1, 0.2)))
        cv = glitch(cv, 1 - prog(t, T["quedas"], 0.3), int(t * 30))
        flash(cv, 0.8 * (1 - prog(t, T["quedas"], 0.08)), VERM)
        return cv
    if t < T["steam"]:
        cv = fundo(t, VERM, "watery_lcars", 0.45)
        ticker(cv, t, 120)
        g = serie(11, 40, 43.41, 10.99, 0.1)
        grafico(cv, g, eo3(prog(t, T["watery"] + 4 * B, 0.9)), VERM, (40, 620, 1040, 1320), 6)
        bloco_carta(cv, t, "watery_lcars", T["watery"], VERM, "▼ QUEDA", "WATERY GRAVE · LCARS",
                    "Star Trek · #393 · showcase, não foil", "−74,7%", 43.41, 10.99,
                    ["Caiu quando Star Trek chegou", "às mesas no pré-lançamento", "(lançamento oficial: hoje, 13/11)"],
                    "Fonte: TCGplayer (via The Index), mercado NM · 06/11 → 13/11", "06/11 → 13/11 · " + brl(43.41) + " → " + brl(10.99),
                    entrada="queda")
        return cv
    if t < T["shock"]:
        cv = fundo(t, VERM, "steam_lcars", 0.45)
        ticker(cv, t, 120)
        g = serie(5, 40, 27.42, 10.78, 0.1)
        grafico(cv, g, eo3(prog(t, T["steam"] + 0.2, 0.9)), VERM, (40, 620, 1040, 1320), 6)
        bloco_carta(cv, t, "steam_lcars", T["steam"], VERM, "▼ QUEDA", "STEAM VENTS · LCARS",
                    "Star Trek · #398 · showcase, não foil", "−60,7%", 27.42, 10.78, [],
                    "Fonte: TCGplayer (via The Index), mercado NM · 06/11 → 13/11", "06/11 → 13/11 · " + brl(27.42) + " → " + brl(10.78),
                    entrada="match", causa_t=T["shock"] + 10)
        flash(cv, 0.45 * (1 - prog(t, T["steam"], 0.1)), (255, 255, 255))
        return cv
    if t < T["radar"]:
        cv = fundo(t, VERM, "watery_trk", 0.4)
        ticker(cv, t, 120)
        p = eo5(prog(t, T["shock"], 0.35))
        por_carta(cv, "watery_trk", 540, lerp(1500, 940, p), 500, brilho=(VERM, 100))
        chip(cv, "▼ CONTEXTO", 540, 236, VERM, tam=28)
        texto_c(cv, "AS 10 SHOCKLANDS", 540, 300, F("Black", 84), BRANCO, alpha=eo3(prog(t, T["shock"] + 0.1, 0.2)))
        texto_c(cv, "NO MENOR PREÇO DA HISTÓRIA", 540, 400, F("Bold", 44), VERM_CL, alpha=eo3(prog(t, T["shock"] + 0.25, 0.2)))
        texto_c(cv, "todas abaixo de US$ 10", 540, 1310, F("Bold", 46, True), BRANCO, alpha=eo3(prog(t, T["shock"] + 2 * B, 0.2)))
        texto_c(cv, "com a nova reimpressão em Star Trek", 540, 1376, F("SemiBold", 36), CINZA, alpha=eo3(prog(t, T["shock"] + 3 * B, 0.2)))
        fonte_linha(cv, "Fonte: Draftsim (10/11) · ilustração: Watery Grave, Star Trek #306", y=1500)
        pz = prog(t, T["radar"] - 0.2, 0.2)
        return zoom_img(cv, 1 - 0.5 * ei3(pz)) if pz > 0 else cv
    # ---------------- BLOCO D · RADAR ----------------
    if t < T["binder"]:
        cv = fundo(t, ARDOSIA)
        ticker(cv, t, 120)
        cx, cy, R = 540, 900, 330
        d = ImageDraw.Draw(cv)
        for r in (R, R * 0.66, R * 0.33):
            d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=VERDE + (110,), width=3)
        d.line((cx - R, cy, cx + R, cy), fill=VERDE + (70,), width=2); d.line((cx, cy - R, cx, cy + R), fill=VERDE + (70,), width=2)
        ang = (t - T["radar"]) * 3.2
        sw = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sw)
        for i in range(30):
            a0 = math.degrees(ang) - i * 2
            ds.pieslice((cx - R, cy - R, cx + R, cy + R), a0 - 2, a0, fill=VERDE + (int(120 * (1 - i / 30)),))
        cv.alpha_composite(sw)
        # alvos: duas cartas pequenas inteiras que "acendem" quando a varredura passa
        for k, (bx, by, aa) in {"uthros": (cx - 150, cy - 90, 0.6), "watery_trk": (cx + 160, cy + 80, 3.4)}.items():
            on = eo3(prog(t, T["radar"] + aa / 3.2, 0.25))
            if on > 0:
                por_carta(cv, k, bx, by, 170 * on + 1, 0, brilho=(VERDE, 140))
        chip(cv, "RADAR DO FIM DE SEMANA", 540, 236, VERDE, tam=28)
        texto_c(cv, "MUNDIAL 32", 540, 300, F("Black", 110), BRANCO, alpha=eo3(prog(t, T["radar"] + 0.1, 0.2)), glow=VERDE)
        texto_c(cv, "+ MagicCon: Atlanta · este fim de semana", 540, 440, F("SemiBold", 36), CINZA, alpha=eo3(prog(t, T["radar"] + 0.3, 0.2)))
        texto_c(cv, "Star Trek em destaque.", 540, 1270, F("Bold", 46), BRANCO, alpha=eo3(prog(t, T["radar"] + 4 * B, 0.2)))
        texto_c(cv, "Atenção às naves e às shocklands", 540, 1336, F("SemiBold", 38), VERDE_CL, alpha=eo3(prog(t, T["radar"] + 6 * B, 0.2)))
        texto_c(cv, "que aparecerem no top 8.", 540, 1386, F("SemiBold", 38), VERDE_CL, alpha=eo3(prog(t, T["radar"] + 6 * B, 0.2)))
        fonte_linha(cv, "Radar não é previsão nem recomendação · Fonte: TCGplayer (12/11)", y=1500)
        # pulsos na batida forte (a cada 2 compassos): zoom curto + clarão verde
        z = 1.0
        for kb in (8, 12):
            pb = prog(t, T["radar"] + kb * B, 0.35)
            if 0 < pb < 1: z = 1 + 0.07 * (1 - eo3(pb)); flash(cv, 0.18 * (1 - pb), VERDE)
        return zoom_img(cv, z, 540, 900)
    # ---------------- BLOCO E · FECHO ----------------
    if t < T["fecho_txt"]:
        cv = fundo(t, VERDE, "watery_trk", 0.3)
        p = eo5(prog(t, T["binder"], 0.35))
        cy = 900
        seq = ["watery_trk", "uthros", "moonshadow", "steam_lcars", "watery_lcars"]
        idx = int(cl((t - T["binder"] - 2 * BAR) / BAR, 0, 9)) if t >= T["binder"] + 2 * BAR else 0
        k_atual = seq[idx % len(seq)]
        por_carta(cv, k_atual, 540, cy, lerp(700, 560, p), brilho=(VERDE, 110))
        if idx > 0: flash(cv, 0.35 * (1 - prog(t, T["binder"] + (idx + 1) * BAR, 0.08)), (255, 255, 255))
        # linha de leitura (efeito gráfico, não é ecrã do app)
        ps = (t - T["binder"] - 0.4) / 1.3
        if ps > 0:
            hy = 560 * 1.3978
            y = cy - hy / 2 + (ps % 1) * hy
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
            dl.rectangle((230, y - 3, 850, y + 3), fill=VERDE + (230,))
            lay = lay.filter(ImageFilter.GaussianBlur(6)); cv.alpha_composite(lay)
            dl = ImageDraw.Draw(cv); dl.line((230, y, 850, y), fill=VERDE_CL + (255,), width=2)
        texto_c(cv, "E A SUA PASTA,", 540, 260, F("Black", 84), BRANCO, alpha=eo3(prog(t, T["binder"] + 0.1, 0.2)))
        texto_c(cv, "QUANTO VALE HOJE?", 540, 360, F("Black", 84), VERDE, alpha=eo3(prog(t, T["binder"] + 0.3, 0.2)), glow=VERDE)
        texto_c(cv, "Escaneie no BINDER Vision", 540, 1330, F("Bold", 50), BRANCO, alpha=eo3(prog(t, T["binder"] + 4 * B, 0.2)))
        texto_c(cv, "Beta grátis no Google Play · link na bio", 540, 1400, F("Medium", 32, True), VERDE_CL, alpha=eo3(prog(t, T["binder"] + 6 * B, 0.2)))
        return cv
    cv = fundo(t, ARDOSIA, grade=True)
    ticker(cv, t, 120)
    t_rec = T["fecho_txt"] + 2 * BAR
    if t < t_rec:
        a = eo3(prog(t, T["fecho_txt"], 0.25))
        texto_c(cv, "PREGÃO MAGIC", 540, 380, F("Black", 96), BRANCO, alpha=a)
        texto_c(cv, "fechou · 13/11/2026", 540, 500, F("Bold", 40, True), VERDE, alpha=a)
        ls = ["Preços: estimativas de mercado (TCGplayer,", "cópias NM em inglês), não ofertas de compra.",
              "Conversão a R$ 5,59 (dólar comercial, 10/11).", "Não é recomendação de compra ou venda.",
              "", "Fontes: TCGplayer · The Index · MTGStocks", "Draftsim · NerdSnack · Brasil 61", "Imagens das cartas: Scryfall · © Wizards of the Coast"]
        for i, l in enumerate(ls):
            texto_c(cv, l, 540, 700 + i * 58, F("Medium", 34), CINZA if i < 4 else BRANCO, alpha=eo3(prog(t, T["fecho_txt"] + 0.1 + i * 0.05, 0.25)))
        return cv
    # recapitulação para guardar: as quatro cartas com a variação
    chip(cv, "GUARDE ESTE PREGÃO · 13/11", 540, 250, VERDE, tam=28)
    itens = [("uthros", "MAIS DE 3×", VERDE), ("moonshadow", "+93%", VERDE), ("watery_lcars", "−74,7%", VERM), ("steam_lcars", "−60,7%", VERM)]
    for i, (k, pct, cor) in enumerate(itens):
        pi = eback(prog(t, t_rec + i * B, 0.3), 1.3)
        cx = 290 + (i % 2) * 500; cy = 560 + (i // 2) * 560
        por_carta(cv, k, cx, cy + lerp(80, 0, pi), 300 * cl(pi, 0.01, 1.2), alpha=cl(pi), brilho=(cor, 90))
        texto_c(cv, pct, cx, cy + 225, F("Black", 52), cor, alpha=cl(pi))
    fonte_linha(cv, "Estimativas TCGplayer (NM) · não é recomendação", y=1500)
    return cv

def main():
    args = sys.argv[1:]
    saida = args[0]
    de = float(args[args.index("--de") + 1]) if "--de" in args else 0.0
    ate = float(args[args.index("--ate") + 1]) if "--ate" in args else DUR
    if "--quadros" in args:
        pasta = args[args.index("--png") + 1]; os.makedirs(pasta, exist_ok=True)
        for s in args[args.index("--quadros") + 1].split(","):
            tt = float(s); quadro(tt).convert("RGB").save(f"{pasta}/q_{tt:06.2f}.png")
        return
    n0, n1 = int(round(de * FPS)), int(round(ate * FPS))
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                           "-pix_fmt", "yuv420p", saida], stdin=subprocess.PIPE)
    for n in range(n0, n1):
        ff.stdin.write(quadro(n / FPS).convert("RGB").tobytes())
        if n % 60 == 0: print(f"{n/FPS:5.1f}s", flush=True)
    ff.stdin.close(); ff.wait()

if __name__ == "__main__":
    main()
