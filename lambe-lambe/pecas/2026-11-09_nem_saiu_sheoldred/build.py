"""Lambe-lambe · "Nem saiu e já tem preço" — Reel 9:16 (BINDER Vision).
Gera os quadros com PIL e envia-os ao ffmpeg. Uso: python3 -I build.py OUT_DIR
"""
import math, random, subprocess, sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

W, H, FPS = 1080, 1920, 30
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
HERE = os.path.dirname(os.path.abspath(__file__))
F_XB = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
F_BI = "/usr/share/fonts/opentype/inter/Inter-BlackItalic.otf"
F_MD = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
PINK = (240, 120, 172)
INK = (5, 10, 16)          # #050A10
EMER = (16, 185, 129)      # #10B981
PAPER = (244, 240, 230)

def font(p, s): return ImageFont.truetype(p, s)
def ease(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3

# ---------------------------------------------------------------- muro
def torn_mask(w, h, rng, amp=9, step=7):
    pts = []
    for x in range(0, w + 1, step): pts.append((x, rng.uniform(0, amp)))
    for y in range(0, h + 1, step): pts.append((w - rng.uniform(0, amp), y))
    for x in range(w, -1, -step): pts.append((x, h - rng.uniform(0, amp)))
    for y in range(h, -1, -step): pts.append((rng.uniform(0, amp), y))
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).polygon(pts, fill=255)
    return m

def grain(w, h, rng, s=14):
    return Image.fromarray(np.clip(128 + np.random.default_rng(rng.randint(0, 9999)).normal(0, s, (h, w)), 0, 255).astype(np.uint8))

def make_wall(seed=3, remnants=26):
    rng = random.Random(seed)
    base = np.zeros((H, W, 3), np.float32) + PINK
    n = np.random.default_rng(seed)
    low = Image.fromarray((n.random((24, 14)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
    base += (np.asarray(low, np.float32)[..., None] - 128) * 0.18
    wall = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")
    cols = [(255, 214, 0), (41, 197, 246), (250, 250, 245), (255, 107, 44), (190, 90, 150), (120, 200, 255)]
    for _ in range(remnants):  # restos de cartazes antigos
        w_, h_ = rng.randint(140, 420), rng.randint(120, 380)
        m = torn_mask(w_, h_, rng, amp=22, step=11)
        c = Image.new("RGBA", (w_, h_), cols[rng.randrange(len(cols))] + (0,))
        c.putalpha(m.point(lambda v: int(v * rng.uniform(0.25, 0.45))))
        dr = ImageDraw.Draw(c)
        for _ in range(rng.randint(1, 3)):
            y = rng.randint(10, h_ - 20)
            dr.rectangle([rng.randint(5, 30), y, rng.randint(60, w_ - 10), y + rng.randint(8, 22)], fill=(255, 255, 255, 40))
        c = c.rotate(rng.uniform(-8, 8), expand=True, resample=Image.BICUBIC)
        wall.alpha_composite(c, (rng.randint(-80, W - 60), rng.randint(-60, H - 60)))
    d = ImageDraw.Draw(wall)
    for _ in range(9):  # tags a marcador
        x, y = rng.randint(40, W - 200), rng.randint(80, H - 120)
        pts = [(x + i * 14 + rng.uniform(-6, 6), y + rng.uniform(-22, 22)) for i in range(rng.randint(5, 12))]
        d.line(pts, fill=(30, 30, 40, 70), width=rng.randint(4, 7), joint="curve")
    g = grain(W, H, rng, 16).convert("RGB")
    wall = Image.blend(wall.convert("RGB"), ImageChops.overlay(wall.convert("RGB"), g), 0.55)
    return wall.convert("RGBA")

# ---------------------------------------------------------------- cartazes
def halftone(w, h, color, step=16, r=4):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for yy in range(0, h, step):
        for xx in range((yy // step) % 2 * step // 2, w, step):
            rr = r * (0.4 + 0.6 * xx / w)
            d.ellipse([xx - rr, yy - rr, xx + rr, yy + rr], fill=color)
    return im

def tape(w=120, h=42, rng=None, ang=0):
    t = Image.new("RGBA", (w, h), (236, 228, 200, 170))
    m = torn_mask(w, h, rng or random.Random(1), amp=4, step=6)
    t.putalpha(ImageChops.multiply(t.getchannel("A"), m))
    return t.rotate(ang, expand=True, resample=Image.BICUBIC)

def poster(w, h, bg, lines, fg=INK, seed=0, dots=None, fnt=F_BI, peel=True):
    rng = random.Random(seed)
    p = Image.new("RGBA", (w, h), bg + (255,))
    if dots: p.alpha_composite(halftone(w, h, dots))
    d = ImageDraw.Draw(p)
    k = 1.0
    while k > 0.3:
        ok = sum(s * k for _, s in lines) * 1.12 <= h - 70 and all(d.textlength(t, font=font(fnt, int(s * k))) <= w - 70 for t, s in lines)
        if ok: break
        k -= 0.03
    total = sum(int(s * k) for _, s in lines) * 1.12
    y = (h - total) / 2 - 6
    for txt, s in lines:
        s = int(s * k); f = font(fnt, s)
        tw = d.textlength(txt, font=f)
        d.text(((w - tw) / 2, y), txt, font=f, fill=fg)
        y += s * 1.12
    for _ in range(4):  # rugas da cola
        x0 = rng.randint(0, w); d.line([(x0, 0), (x0 + rng.randint(-60, 60), h)], fill=(255, 255, 255, 38), width=2)
    p = Image.blend(p.convert("RGB"), ImageChops.overlay(p.convert("RGB"), grain(w, h, rng, 22).convert("RGB")), 0.5).convert("RGBA")
    m = torn_mask(w, h, rng)
    if peel:  # canto descolado em baixo à direita
        c = int(min(w, h) * 0.16)
        ImageDraw.Draw(m).polygon([(w, h - c), (w, h), (w - c, h)], fill=0)
        flap = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(flap).polygon([(w - c, h), (w, h - c), (w - c - 6, h - c - 6)], fill=(250, 248, 240, 255))
        p.putalpha(m); p.alpha_composite(flap)
    else:
        p.putalpha(m)
    ImageDraw.Draw(p).line([(0, 0), (w, 0)], fill=(255, 255, 255, 90), width=3)  # fibra
    out = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0))
    out.alpha_composite(p, (30, 30))
    out.alpha_composite(tape(110, 38, rng, rng.uniform(-30, -15)), (0, 4))
    out.alpha_composite(tape(110, 38, rng, rng.uniform(15, 30)), (w - 50, 4))
    return out

def with_shadow(img, off=(10, 14), blur=10, alpha=110):
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sh.putalpha(img.getchannel("A").point(lambda v: v * alpha // 255))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    out = Image.new("RGBA", (img.width + 40, img.height + 40), (0, 0, 0, 0))
    out.alpha_composite(sh, (20 + off[0], 20 + off[1])); out.alpha_composite(img, (20, 20))
    return out

def place(canvas, img, cx, cy, ang=0, scale=1.0, alpha=1.0):
    if scale != 1.0: img = img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))), Image.BICUBIC)
    if ang: img = img.rotate(ang, expand=True, resample=Image.BICUBIC)
    if alpha < 1: img.putalpha(img.getchannel("A").point(lambda v: int(v * alpha)))
    canvas.alpha_composite(img, (int(cx - img.width / 2), int(cy - img.height / 2))) if True else None

# ---------------------------------------------------------------- títulos (caixas brancas, como a referência)
def headline(lines, size=72, fg=INK, bg=(255, 255, 255), pad=(20, 10)):
    f = font(F_XB, size)
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    rows = []
    for t in lines:
        bb = tmp.textbbox((0, 0), t, font=f)
        rows.append((t, bb[2] - bb[0] + pad[0] * 2, int(size * 1.18) + pad[1]))
    w = max(r[1] for r in rows); h = sum(r[2] for r in rows) - 6 * (len(rows) - 1)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); y = 0
    for t, rw, rh in rows:
        d.rectangle([0, y, rw, y + rh], fill=bg + (255,))
        d.text((pad[0], y + pad[1] // 2), t, font=f, fill=fg)
        y += rh - 6
    return im

def put_headline(canvas, im, t_in, t, x=60, y=250, ang=-1.2):
    if t < t_in: return
    k = ease((t - t_in) / 0.12)
    place(canvas, im, x + im.width / 2, y + im.height / 2, ang, 1.12 - 0.12 * k)

# ---------------------------------------------------------------- recursos
rng0 = random.Random(7)
WALL = make_wall(3)
LOGO = Image.open(os.path.join(HERE, "logo.png")).convert("RGBA")
REC = [Image.open(os.path.join(HERE, "rec_frames", f)).convert("RGBA") for f in sorted(os.listdir(os.path.join(HERE, "rec_frames")))]

# Cartazes do hype (cena 1): (tempo de entrada, cx, cy, ângulo, cartaz)
HYPE = [
    ("VAI SUBIR!", (255, 214, 0), [("VAI", 120), ("SUBIR!", 120)], (255, 90, 30, 120)),
    ("COMPRA", (41, 197, 246), [("COMPRA", 92), ("ANTES QUE", 64), ("ACABE", 92)], None),
    ("PRÉ-VENDA", (250, 250, 245), [("PRÉ-", 110), ("VENDA", 110)], (230, 57, 70, 110)),
    ("R$ ???", (255, 107, 44), [("R$", 90), ("???", 150)], (255, 214, 0, 140)),
    ("HYPE", (255, 214, 0), [("HYPE", 150)], (41, 197, 246, 130)),
    ("ESPECULA", (250, 250, 245), [("CONFIA", 96), ("NO PAI", 96)], None),
    ("INVEST", (41, 197, 246), [("INVESTIMENTO", 54), ("GARANTIDO*", 60), ("*só que não", 34)], None),
    ("↑↑↑", (230, 57, 70), [("↑↑↑", 170)], None),
]
slots = [(250, 760, -6), (780, 700, 5), (300, 1180, 4), (790, 1150, -7), (540, 930, -2),
         (250, 1520, 6), (800, 1530, -4), (540, 1330, 3)]
sizes = [(420, 380), (400, 400), (400, 380), (380, 380), (460, 330), (420, 340), (420, 330), (330, 300)]
HYPE_P = []
for i, (k, bg, lines, dots) in enumerate(HYPE):
    fg = (255, 255, 255) if bg == (230, 57, 70) else INK
    pw, ph = sizes[i]
    HYPE_P.append(with_shadow(poster(pw, ph, bg, lines, fg, seed=i + 10, dots=dots)))
SLAP_T = [0.05 + i * 0.22 for i in range(len(HYPE_P))]

# Cartaz do gráfico (cena 2)
def chart_poster(prog):
    w, h = 820, 760
    p = Image.new("RGBA", (w, h), (255, 214, 0, 255))
    p.alpha_composite(halftone(w, h, (255, 140, 0, 120), 18, 5))
    d = ImageDraw.Draw(p)
    d.text((40, 30), "SHEOLDRED · VERSÃO KHAN", font=font(F_BI, 44), fill=INK)
    d.line([(70, 690), (760, 690)], fill=INK, width=8); d.line([(70, 690), (70, 130)], fill=INK, width=8)
    pts = [(80, 650), (190, 610), (290, 630), (390, 520), (480, 540), (570, 380), (660, 300), (760, 120), (840, -40)]
    n = 1 + prog * (len(pts) - 1)
    seg = pts[:int(n)] + ([tuple(np.add(pts[int(n) - 1], np.multiply(np.subtract(pts[min(int(n), len(pts) - 1)], pts[int(n) - 1]), n - int(n))))] if int(n) < len(pts) else [])
    if len(seg) > 1: d.line(seg, fill=(230, 57, 70), width=22, joint="curve")
    if prog > 0.35:  # carimbo
        st = Image.new("RGBA", (470, 120), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
        sd.rectangle([4, 4, 466, 116], outline=(230, 57, 70), width=8)
        sd.text((24, 22), "NEM LANÇOU", font=font(F_XB, 56), fill=(230, 57, 70))
        st = st.rotate(12, expand=True, resample=Image.BICUBIC)
        p.alpha_composite(st, (110, 360))
    p = Image.blend(p.convert("RGB"), ImageChops.overlay(p.convert("RGB"), grain(w, h, random.Random(5), 22).convert("RGB")), 0.5).convert("RGBA")
    rng = random.Random(42); m = torn_mask(w, h, rng, 12, 8)
    if prog >= 1.0:  # rasgo: o gráfico sai pelo topo
        ImageDraw.Draw(m).polygon([(600, 0), (w, 0), (w, 260), (780, 190), (700, 120)], fill=0)
    p.putalpha(m)
    out = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0)); out.alpha_composite(p, (30, 30))
    out.alpha_composite(tape(120, 40, rng, -24), (0, 4)); out.alpha_composite(tape(120, 40, rng, 22), (w - 60, 4))
    return with_shadow(out)

# Cartaz preto BINDER (cena 4)
def black_poster(w=940, h=1260):
    p = Image.new("RGBA", (w, h), INK + (255,))
    p = Image.blend(p.convert("RGB"), ImageChops.overlay(p.convert("RGB"), grain(w, h, random.Random(9), 30).convert("RGB")), 0.35).convert("RGBA")
    d = ImageDraw.Draw(p)
    for i in range(6):
        x0 = 80 + i * 150; d.line([(x0, 0), (x0 + 40, h)], fill=(255, 255, 255, 14), width=2)
    p.putalpha(torn_mask(w, h, random.Random(11), 12, 8))
    out = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0)); out.alpha_composite(p, (30, 30))
    r = random.Random(12)
    out.alpha_composite(tape(130, 42, r, -25), (0, 4)); out.alpha_composite(tape(130, 42, r, 25), (w - 70, 4))
    return with_shadow(out, alpha=140)
BLACK = black_poster()

def screen_card(fr):
    w, h = fr.size
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 34, fill=255)
    s = fr.copy(); s.putalpha(m)
    out = Image.new("RGBA", (w + 24, h + 24), (0, 0, 0, 0))
    ImageDraw.Draw(out).rounded_rectangle([0, 0, w + 23, h + 23], 44, fill=(28, 36, 48, 255))
    out.alpha_composite(s, (12, 12))
    return with_shadow(out, alpha=160, blur=14)

def sticker(text, size, bg, fg, ang=0, pad=(18, 10)):
    f = font(F_XB, size); d = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    bb = d.textbbox((0, 0), text, font=f)
    im = Image.new("RGBA", (bb[2] - bb[0] + pad[0] * 2, int(size * 1.2) + pad[1] * 2), bg + (255,))
    ImageDraw.Draw(im).text((pad[0], pad[1] - bb[1] // 2), text, font=f, fill=fg)
    return im.rotate(ang, expand=True, resample=Image.BICUBIC) if ang else im

def logo_paste(size=520):
    """Logo como lambe-lambe: papel claro rasgado com a logo impressa, fita nos cantos de cima."""
    w = h = size
    p = Image.new("RGBA", (w, h), PAPER + (255,))
    lg = LOGO.resize((int(w * 0.82), int(h * 0.82)), Image.LANCZOS)
    p.alpha_composite(lg, ((w - lg.width) // 2, (h - lg.height) // 2))
    p = Image.blend(p.convert("RGB"), ImageChops.overlay(p.convert("RGB"), grain(w, h, random.Random(21), 20).convert("RGB")), 0.45).convert("RGBA")
    d = ImageDraw.Draw(p)
    for x0 in (130, 300, 420): d.line([(x0, 0), (x0 + 30, h)], fill=(255, 255, 255, 50), width=2)
    m = torn_mask(w, h, random.Random(22), 10, 7); c = 70
    ImageDraw.Draw(m).polygon([(w, h - c), (w, h), (w - c, h)], fill=0)
    p.putalpha(m)
    ImageDraw.Draw(p).polygon([(w - c, h), (w, h - c), (w - c - 8, h - c - 8)], fill=(255, 255, 255, 255))
    out = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0)); out.alpha_composite(p, (30, 30))
    r = random.Random(23)
    out.alpha_composite(tape(120, 40, r, -26), (0, 4)); out.alpha_composite(tape(120, 40, r, 26), (w - 60, 4))
    return with_shadow(out, alpha=130)
LOGO_PASTE = logo_paste(660)

def printed_logo(size, rng):
    """Logo como tinta impressa: grão do papel, falhas de tinta e leve desacerto de registo."""
    lg = LOGO.resize((size, size), Image.LANCZOS)
    a = np.asarray(lg.getchannel("A"), np.float32)
    noise = np.asarray(grain(size, size, rng, 40), np.float32)
    holes = (np.random.default_rng(rng.randint(0, 999)).random((size, size)) < 0.012)
    a = a * np.clip(0.78 + (noise - 128) / 400, 0, 1); a[holes] *= 0.25
    lg.putalpha(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)))
    ghost = lg.copy(); ghost.putalpha(lg.getchannel("A").point(lambda v: v * 22 // 100))
    out = Image.new("RGBA", (size + 8, size + 8), (0, 0, 0, 0))
    out.alpha_composite(ghost, (6, 5)); out.alpha_composite(lg, (2, 2))
    return out

def logo_poster(w, h, seed, label=True):
    """Cartaz preto BINDER de lambe-lambe com a logo impressa (produto = cartaz preto)."""
    rng = random.Random(seed)
    p = Image.new("RGBA", (w, h), INK + (255,))
    p = Image.blend(p.convert("RGB"), ImageChops.overlay(p.convert("RGB"), grain(w, h, rng, 34).convert("RGB")), 0.4).convert("RGBA")
    ls = int(min(w, h * (0.72 if label else 0.9)) * 0.78)
    lg = printed_logo(ls, rng)
    ly = int(h * (0.08 if label else 0.06)) if label else (h - lg.height) // 2
    p.alpha_composite(lg, ((w - lg.width) // 2, ly))
    d = ImageDraw.Draw(p)
    if label:
        f = font(F_XB, int(w * 0.11)); t1, t2 = "BINDER ", "Vision"
        tw = d.textlength(t1 + t2, font=f); x = (w - tw) / 2; y = ly + lg.height + h * 0.02
        d.text((x, y), t1, font=f, fill=(245, 245, 240)); d.text((x + d.textlength(t1, font=f), y), t2, font=f, fill=EMER)
    for _ in range(5):  # rugas da cola
        x0 = rng.randint(0, w); d.line([(x0, 0), (x0 + rng.randint(-70, 70), h)], fill=(255, 255, 255, 20), width=2)
    m = torn_mask(w, h, rng, 10, 7); c = int(min(w, h) * 0.14)
    if rng.random() < 0.7:
        ImageDraw.Draw(m).polygon([(w, h - c), (w, h), (w - c, h)], fill=0)
        p.putalpha(m)
        ImageDraw.Draw(p).polygon([(w - c, h), (w, h - c), (w - c - 7, h - c - 7)], fill=(232, 228, 218, 255))
    else:
        p.putalpha(m)
    ImageDraw.Draw(p).line([(0, 2), (w, 2)], fill=(255, 255, 255, 60), width=3)
    out = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0)); out.alpha_composite(p, (30, 30))
    out.alpha_composite(tape(110, 38, rng, rng.uniform(-30, -18)), (0, 4)); out.alpha_composite(tape(110, 38, rng, rng.uniform(18, 30)), (w - 50, 4))
    return with_shadow(out, alpha=140)

def glue(img, wet):
    """Brilho de cola molhada que seca em ~0,5 s."""
    if wet <= 0: return img
    g = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(g); r = random.Random(img.width)
    for i in range(7):
        x = r.randint(-100, img.width); d.line([(x, 0), (x + 220, img.height)], fill=(255, 255, 255, int(30 * wet)), width=r.randint(18, 40))
    g.putalpha(ImageChops.multiply(g.getchannel("A"), img.getchannel("A")))
    out = img.copy(); out.alpha_composite(g.filter(ImageFilter.GaussianBlur(6))); return out

# cena 3: três cartazes BINDER colados por cima do caos
LP3 = [(logo_poster(380, 470, 31), 300, 820, -5), (logo_poster(400, 490, 32), 770, 1260, 6), (logo_poster(360, 450, 33, False), 280, 1420, 3)]
LP3_T = [4.55, 4.80, 5.05]
# cena 5: campanha de lambe-lambe — a mesma peça repetida em grelha
LP5 = []
for i in range(6):
    col, row = i % 2, i // 2
    LP5.append((logo_poster(400, 470, 50 + i), 255 + col * 420 + random.Random(i).randint(-12, 12), 790 + row * 470 + random.Random(i + 9).randint(-10, 10), random.Random(i + 3).uniform(-4, 4)))
LP5_T = [8.45 + i * 0.11 for i in range(6)]
PL_SMALL = printed_logo(110, random.Random(77))

H1 = headline(["Essa Sheoldred", "nem chegou às lojas…"], 74)
H2 = headline(["…e já tem preço:", "R$ 396,42."], 82)
H2b = headline(["Lança só dia 13/11."], 50, fg=(255, 255, 255), bg=INK)
H3 = headline(["Antes do hype, veja quanto", "vale a sua coleção."], 56)
H4 = headline(["Carta é pra jogar."], 84)
H4b = headline(["Não pra especular."], 84, fg=INK, bg=EMER)
SELO = sticker("TELA REAL DO APP", 30, EMER, INK, ang=90)
NOTA = sticker("Valor de referência no app · 09/11/2026 · estimativa", 28, PAPER, INK, ang=-1)
NOTA2 = sticker("valor de referência no BINDER Vision, 09/11/2026", 30, PAPER, INK, ang=-1.5)

T1, T2, T3, T4, T5 = 0.0, 2.55, 4.55, 5.45, 8.45
TEND = 10.55
REC_T0 = T4 + 0.12

def frame(t):
    c = WALL.copy()
    if True:
        # cena 1–3: cartazes do hype (varridos pelo redemoinho na cena 3)
        sweep = 0
        for i, P in enumerate(HYPE_P):
            if t < SLAP_T[i]: continue
            k = ease((t - SLAP_T[i]) / 0.1)
            cx, cy, a = slots[i]
            if sweep > 0:
                ang0 = math.atan2(cy - 960, cx - 540) + sweep * 2.2
                rad = math.hypot(cx - 540, cy - 960) + sweep * 1100
                cx, cy, a = 540 + rad * math.cos(ang0), 960 + rad * math.sin(ang0), a + sweep * 260
            place(c, P, cx, cy, a, (1.18 - 0.18 * k) * (1 - 0.45 * sweep), 1 - sweep * 0.9 if sweep else 1)
        if T2 <= t:
            pr = ease((t - T2 - 0.1) / 1.4)
            CP = chart_poster(1.0 if t > T2 + 1.65 else pr)
            k = ease((t - T2) / 0.1)
            if sweep > 0:
                place(c, CP, 540 + sweep * 900, 1050 - sweep * 300, 2 + sweep * 300, (1.0 - 0.5 * sweep), 1 - 0.9 * sweep)
            else:
                place(c, CP, 540, 1050, 2, 1.15 - 0.15 * k)
    if t >= T3:
        # cena 3: cartazes pretos BINDER colados por cima do hype
        for (P, x, y, a), ts in zip(LP3, LP3_T):
            if t < ts: continue
            k = ease((t - ts) / 0.1)
            place(c, glue(P, 1 - (t - ts) / 0.45), x, y, a, 1.2 - 0.2 * k)
    if t >= T4:
        # cena 4: cartaz preto BINDER + tela real do app
        k = ease((t - T4) / 0.12)
        if t < T5: place(c, glue(BLACK, 1 - (t - T4) / 0.6), 540, 1000, -1.0, 1.1 - 0.1 * k)
        if REC_T0 <= t < T5:
            idx = min(len(REC) - 1, int((t - REC_T0) * FPS))
            place(c, screen_card(REC[idx]), 470, 1030, 0.0, 0.95)
            place(c, SELO, 880, 1060, 0)
            place(c, NOTA, 470, 448, 0)
        if t < T5:
            put_headline(c, H3, T4 + 0.25, t, 60, 230)
            place(c, PL_SMALL, 880, 650, 0)
    if t >= T5:
        # cena 5: muro limpo, logo colada como lambe-lambe, veredito
        for (P, x, y, a), ts in zip(LP5, LP5_T):
            if t < ts: continue
            k = ease((t - ts) / 0.1)
            place(c, glue(P, 1 - (t - ts) / 0.45), x, y, a, 1.2 - 0.2 * k)
        put_headline(c, H4, T5 + 0.15, t, 60, 300, -1.5)
        put_headline(c, H4b, T5 + 0.55, t, 90, 430, 1.0)
    if t < T2:
        put_headline(c, H1, 0.0, t, 60, 250)
    elif t < T3:
        put_headline(c, H2, T2, t, 60, 250)
        put_headline(c, H2b, T2 + 0.5, t, 70, 470, 1.5)
        put_headline(c, NOTA2, T2 + 0.5, t, 70, 560, -1.0)
    return c.convert("RGB")

if __name__ == "__main__":
    n = int(round(TEND * FPS))
    if os.environ.get("PREVIEW"):
        for tt in [float(x) for x in os.environ["PREVIEW"].split(",")]:
            frame(tt).save(os.path.join(OUT, f"prev_{tt:05.2f}.jpg"), quality=85)
        sys.exit()
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", os.path.join(OUT, "corpo.mp4")], stdin=subprocess.PIPE)
    for i in range(n):
        ff.stdin.write(frame(i / FPS).tobytes())
    ff.stdin.close(); ff.wait()
    print("frames", n)
