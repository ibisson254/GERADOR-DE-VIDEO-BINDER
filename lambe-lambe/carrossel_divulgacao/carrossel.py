"""Carrossel Lambe-lambe · divulgação do BINDER Vision (5 slides 4:5, 1080x1350).
Uso: python3 -I carrossel.py <pasta_assets> <pasta_saida>
Assets: cartas/*.png, crop_scan.jpg, crop_result.jpg, logo_mark.png, fontes .ttf.
"""
import sys, os, random, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

A, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1350
PRETO, ESM, BRANCO = (5, 10, 16), (16, 185, 129), (245, 243, 238)
ROSA = (238, 150, 185)

def F(nome, t): return ImageFont.truetype(os.path.join(A, nome), t)
GB = lambda t: F("Geist-Bold.ttf", t)
GM = lambda t: F("Geist-Medium.ttf", t)
POP = lambda t: F("bangers-latin-400-normal.ttf", t)
MK = lambda t: F("marker.ttf", t)

# ---------- texturas ----------
def ruido(w, h, amp, blur=0, seed=0):
    r = np.random.default_rng(seed).normal(0, 1, (h, w))
    im = Image.fromarray(np.uint8(np.clip(128 + r * amp, 0, 255)))
    return im.filter(ImageFilter.GaussianBlur(blur)) if blur else im

def borda_rasgada(w, h, dente=10, seed=0):
    """Máscara de papel rasgado (L) w x h, com margem para os dentes."""
    rnd = random.Random(seed)
    pts = []
    def lado(x0, y0, x1, y1, n):
        for i in range(n):
            t = i / n
            x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t
            j = rnd.uniform(-dente, dente) * (0.4 + rnd.random())
            if x0 == x1: x += j
            else: y += j
            pts.append((x, y))
    m = dente * 2
    lado(m, m, w - m, m, w // 9); lado(w - m, m, w - m, h - m, h // 9)
    lado(w - m, h - m, m, h - m, w // 9); lado(m, h - m, m, m, h // 9)
    mk = Image.new("L", (w, h), 0); ImageDraw.Draw(mk).polygon(pts, fill=255)
    return mk.filter(ImageFilter.GaussianBlur(0.8))

def papel(w, h, cor, seed=0, dente=9, fibra=True, envelhecer=0.0):
    """Folha RGBA com borda rasgada, fibras brancas e grão."""
    pad = dente * 2
    W2, H2 = w + 2 * pad, h + 2 * pad
    mk = borda_rasgada(W2, H2, dente, seed)
    base = Image.new("RGB", (W2, H2), cor)
    g = ruido(W2, H2, 10, 0.6, seed)
    base = Image.blend(base, Image.merge("RGB", [g] * 3), 0.07)
    if envelhecer:
        manchas = ruido(W2 // 8, H2 // 8, 40, 2, seed + 5).resize((W2, H2))
        base = Image.composite(base, Image.new("RGB", (W2, H2), (230, 225, 210)),
                               manchas.point(lambda v: 255 if v < 150 else int(255 * (1 - envelhecer))))
    out = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
    if fibra:
        fib = mk.filter(ImageFilter.MaxFilter(5))
        out.paste(Image.new("RGBA", (W2, H2), (250, 248, 242, 255)), (0, 0), fib)
        inner = mk.filter(ImageFilter.MinFilter(3))
    else:
        inner = mk
    out.paste(base.convert("RGBA"), (0, 0), inner)
    return out, pad

def colar(fundo, folha, x, y, ang=0, sombra=True):
    f = folha.rotate(ang, resample=Image.BICUBIC, expand=True)
    if sombra:
        s = Image.new("RGBA", f.size, (0, 0, 0, 0))
        s.putalpha(f.split()[3].point(lambda a: int(a * 0.38)))
        s = s.filter(ImageFilter.GaussianBlur(9))
        fundo.alpha_composite(s, (int(x + 6), int(y + 10)))
    fundo.alpha_composite(f, (int(x), int(y)))
    return f.size

def fita(fundo, cx, cy, ang, seed=0, w=120, h=38):
    t = Image.new("RGBA", (w, h), (236, 228, 205, 165))
    d = ImageDraw.Draw(t)
    rnd = random.Random(seed)
    for xx in range(0, w, 3):  # pontas serrilhadas
        d.line([(xx, 0), (xx, rnd.randint(0, 3))], fill=(0, 0, 0, 0))
        d.line([(xx, h), (xx, h - rnd.randint(0, 3))], fill=(0, 0, 0, 0))
    for x0 in (0, w - 4):
        for yy in range(0, h, 4):
            d.rectangle([x0 + rnd.randint(0, 3), yy, x0 + 4, yy + 3], fill=(0, 0, 0, 0)) if x0 else \
            d.rectangle([0, yy, rnd.randint(0, 4), yy + 3], fill=(0, 0, 0, 0))
    t = t.rotate(ang, resample=Image.BICUBIC, expand=True)
    fundo.alpha_composite(t, (int(cx - t.width / 2), int(cy - t.height / 2)))

def muro(seed):
    rnd = random.Random(seed)
    m = Image.new("RGBA", (W, H), ROSA + (255,))
    # restos de cartazes antigos, desbotados
    for i in range(14):
        cor = rnd.choice([(250, 214, 92), (120, 205, 230), (250, 250, 245), (246, 120, 160), (255, 190, 120)])
        cor = tuple(int(c * 0.55 + r * 0.45) for c, r in zip(cor, ROSA))
        w, h = rnd.randint(160, 420), rnd.randint(120, 380)
        f, p = papel(w, h, cor, seed * 100 + i, dente=12, fibra=rnd.random() < .6)
        f.putalpha(f.split()[3].point(lambda a: int(a * 0.85)))
        colar(m, f, rnd.randint(-120, W - 100), rnd.randint(-120, H - 80), rnd.uniform(-8, 8), sombra=False)
        dd = ImageDraw.Draw(m)
        if rnd.random() < .5:  # letras de cartaz antigo
            dd.text((rnd.randint(0, W), rnd.randint(0, H)), rnd.choice(["SHOW", "LIQUIDA", "HOJE", "ALUGA", "FESTA", "VENDE"]),
                    font=POP(rnd.randint(50, 110)), fill=tuple(int(c * .8) for c in cor) + (90,))
    # cola escorrida e grão
    cola = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dc = ImageDraw.Draw(cola)
    for i in range(10):
        x = rnd.randint(0, W); y = rnd.randint(0, H)
        dc.line([(x, y), (x + rnd.randint(-10, 10), y + rnd.randint(60, 260))], fill=(255, 255, 255, 30), width=rnd.randint(4, 14))
    m.alpha_composite(cola.filter(ImageFilter.GaussianBlur(3)))
    g = ruido(W, H, 22, 0.7, seed)
    m = Image.blend(m, Image.merge("RGBA", [g, g, g, Image.new("L", (W, H), 255)]), 0.08)
    # tinta lascada
    lasca = ruido(W // 6, H // 6, 60, 1.2, seed + 9).resize((W, H)).point(lambda v: 255 if v > 205 else 0)
    m.paste(Image.new("RGBA", (W, H), (205, 196, 188, 255)), (0, 0), lasca.filter(ImageFilter.GaussianBlur(1)))
    return m

def carta(fundo, nome, cx, cy, largura, ang, seed):
    c = Image.open(os.path.join(A, "cartas", nome + ".png")).convert("RGBA")
    c = c.resize((largura, int(largura * c.height / c.width)), Image.LANCZOS)
    pad = 20
    f = Image.new("RGBA", (c.width + 2 * pad, c.height + 2 * pad), (0, 0, 0, 0)); f.alpha_composite(c, (pad, pad))
    r = f.rotate(ang, resample=Image.BICUBIC, expand=True)
    x, y = cx - r.width / 2, cy - r.height / 2
    colar(fundo, f, x, y, ang)
    # fita só nos cantos de cima
    a = math.radians(-ang)
    for sx in (-1, 1):
        dx, dy = sx * (c.width / 2 - 14), -(c.height / 2 - 6)
        px = cx + dx * math.cos(a) - dy * math.sin(a); py = cy + dx * math.sin(a) + dy * math.cos(a)
        fita(fundo, px, py, ang + sx * 38, seed + sx, w=110, h=34)
    return c.size

def texto_centro(d, cx, y, txt, fonte, cor, esp=1.18):
    for i, l in enumerate(txt.split("\n")):
        w = d.textlength(l, font=fonte)
        d.text((cx - w / 2, y + i * fonte.size * esp), l, font=fonte, fill=cor)

def etiqueta(fundo, txt, cx, cy, ang, seed, cor=(252, 250, 244), tinta=(20, 20, 24), t=46):
    f0 = MK(t); d0 = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    w = int(d0.textlength(txt, font=f0)) + 50; h = int(t * 1.6)
    f, p = papel(w, h, cor, seed, dente=6, fibra=False)
    ImageDraw.Draw(f).text((p + 25, p + h * .12), txt, font=f0, fill=tinta)
    r = f.rotate(ang, resample=Image.BICUBIC, expand=True)
    colar(fundo, f, cx - r.width / 2, cy - r.height / 2, ang)
    fita(fundo, cx, cy - r.height / 2 + 6, ang + 4, seed + 3, w=80, h=26)

def cartaz_pop(fundo, txt, x, y, w, h, ang, seed, cor=(255, 222, 60), t=104):
    f, p = papel(w, h, cor, seed, dente=10)
    d = ImageDraw.Draw(f)
    linhas = txt.split("\n"); fo = POP(t)
    tot = len(linhas) * t * 1.02
    for i, l in enumerate(linhas):
        lw = d.textlength(l, font=fo)
        xx = p + (w - lw) / 2; yy = p + (h - tot) / 2 + i * t * 1.02
        d.text((xx + 5, yy + 5), l, font=fo, fill=(236, 80, 140))
        d.text((xx, yy), l, font=fo, fill=PRETO)
    colar(fundo, f, x, y, ang)

def cartaz_binder(w, h, seed):
    f, p = papel(w, h, PRETO, seed, dente=10)
    return f, p

def logo(tam):
    return Image.open(os.path.join(A, "logo_mark.png")).convert("RGBA").resize((tam, tam), Image.LANCZOS)

def selo(fundo, txt, x, y, ang, seed):
    f, p = papel(330, 62, ESM, seed, dente=5, fibra=False)
    d = ImageDraw.Draw(f); fo = GB(28)
    d.text((p + (330 - d.textlength(txt, font=fo)) / 2, p + 15), txt, font=fo, fill=PRETO)
    colar(fundo, f, x, y, ang)

def creditos(fundo, txt, seed):
    fo = GM(21); d0 = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    linhas = txt.split("\n"); w = int(max(d0.textlength(l, font=fo) for l in linhas)) + 40
    h = int(len(linhas) * 28 + 26)
    f, p = papel(w, h, (250, 248, 242), seed, dente=4, fibra=False)
    d = ImageDraw.Draw(f)
    for i, l in enumerate(linhas): d.text((p + 20, p + 13 + i * 28), l, font=fo, fill=(40, 40, 46))
    colar(fundo, f, (W - w) / 2 - p, H - h - 40 - p, 0.4)

def seta(fundo, seed):
    etiqueta(fundo, "arrasta para o lado", W - 230, H - 120, -3, seed, cor=(16, 185, 129), tinta=PRETO, t=36)

def telemovel(img, alt):
    im = Image.open(os.path.join(A, img)).convert("RGBA")
    mk = Image.new("L", im.size, 0)
    ImageDraw.Draw(mk).rounded_rectangle([36, 40, im.width - 34, im.height - 38], 62, fill=255)
    im.putalpha(mk)
    return im.resize((int(alt * im.width / im.height), alt), Image.LANCZOS)

CRED = ("Lightning Bolt (STA, 2021) arte Anato Finnstark · Counterspell (MH2, 2021) arte Zack Stella\n"
        "Llanowar Elves (DOM, 2018) arte Chris Rahn · Sol Ring (C21, 2021) arte Mike Bierek\n"
        "© Wizards of the Coast. Conteúdo de fã não oficial.")

# ---------- slides ----------
def s1():
    m = muro(1)
    carta(m, "bolt", 195, 880, 300, -5, 11)
    carta(m, "counter", 540, 820, 300, 2, 12)
    carta(m, "solring", 885, 900, 300, 5, 13)
    cartaz_pop(m, "SUA COLEÇÃO\nPARECE ESTE MURO?", 70, 70, 900, 330, -2, 14, t=112)
    seta(m, 15)
    return m

def s2():
    m = muro(2)
    cartaz_pop(m, "TODA CARTA VEM\nCOM UMA PERGUNTA", 90, 60, 880, 280, 1.5, 21, cor=(250, 250, 245), t=96)
    carta(m, "elves", 270, 790, 320, -3, 22)
    carta(m, "bolt", 800, 760, 320, 4, 23)
    etiqueta(m, "Já tenho essa?", 250, 415, -6, 24)
    etiqueta(m, "Qual edição?", 830, 390, 5, 25)
    etiqueta(m, "Quanto vale?", 545, 1065, -2, 26, cor=(255, 222, 60))
    creditos(m, CRED, 27)
    return m

def slide_app(seed, img, titulo, sub, nota=None):
    m = muro(seed)
    f, p = cartaz_binder(900, 1180, seed + 1)
    d = ImageDraw.Draw(f)
    lg = logo(70); f.alpha_composite(lg, (p + 50, p + 46))
    d.text((p + 136, p + 58), "BINDER Vision", font=GB(40), fill=BRANCO)
    tel = telemovel(img, 760)
    f.alpha_composite(tel, (p + 900 - tel.width - 40, p + 300))
    # texto na coluna esquerda
    tx = p + 50
    yy = p + 170
    for l in titulo.split("\n"):
        d.text((tx, yy), l, font=GB(58), fill=BRANCO); yy += 68
    d.rectangle([tx, yy + 18, tx + 90, yy + 24], fill=ESM)
    yy += 52
    for l in sub.split("\n"):
        d.text((tx, yy), l, font=GM(36), fill=(200, 210, 222)); yy += 48
    if nota:
        d.text((tx, p + 1180 - 70), nota, font=GM(24), fill=(140, 150, 165))
    colar(m, f, 90 - p, 85 - p, -1)
    selo(m, "TELA REAL DO APP", 700, 1180, 3, seed + 4)
    fita(m, 160, 105, -35, seed + 5, 130, 40); fita(m, 920, 95, 35, seed + 6, 130, 40)
    return m

def s3():
    return slide_app(3, "crop_scan.jpg", "Aponte\na câmera.", "O app ajuda a\nidentificar\na carta.")

def s4():
    return slide_app(4, "crop_result.jpg", "Escolha a\nimpressão.", "E veja um\nvalor de\nreferência.",
                     nota="Valor estimado, não é oferta de compra.")

def s5():
    m = muro(5)
    carta(m, "counter", 190, 1080, 250, -8, 51)
    carta(m, "elves", 890, 1090, 250, 7, 52)
    f, p = cartaz_binder(820, 760, 53)
    d = ImageDraw.Draw(f)
    lg = logo(230); f.alpha_composite(lg, (p + (820 - 230) // 2, p + 60))
    texto_centro(d, p + 410, p + 320, "BINDER Vision", GB(78), BRANCO)
    texto_centro(d, p + 410, p + 430, "Escaneie suas cartas\ne organize seus decks.", GM(40), (200, 210, 222))
    # botão
    bw, bh = 560, 92; bx, by = p + (820 - bw) // 2, p + 590
    d.rounded_rectangle([bx, by, bx + bw, by + bh], 46, fill=ESM)
    texto_centro(d, p + 410, by + 24, "Beta para Android · link na bio", GB(36), PRETO)
    colar(m, f, 130 - p, 140 - p, 1.2)
    fita(m, 200, 150, -35, 54, 140, 42); fita(m, 880, 165, 35, 55, 140, 42)
    return m

for i, fn in enumerate([s1, s2, s3, s4, s5], 1):
    fn().convert("RGB").save(os.path.join(OUT, f"binder_lambe_carrossel_{i}.png"))
    print("ok", i)
