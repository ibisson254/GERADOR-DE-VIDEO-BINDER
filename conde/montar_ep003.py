"""Conde de Manaforte · Episódio 003 · O Tribunal Estético (Voldaren Pariah // Abolisher of Bloodlines)
Copiado de montar_ep002.py; trocados caminhos, KEY, coordenadas, cenas, carimbos, flip, emenda da música e fecho.
Carta de dupla face: art_front/art_back (art_crop 626x457) e card_front/card_back (744x1040), Scryfall sld/1441.
Uso: python3 montar_ep003.py [saida.mp4] [--preview t1,t2,...] [--audio-only]
"""
import sys, json, math, subprocess, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

BASE = os.path.dirname(os.path.abspath(__file__))           # .../conde
KIT = os.path.dirname(BASE)                                 # raiz do repositório
EP = f"{BASE}/ep003"
W, H, FPS = 1080, 1920, 30
DUR = 47.3                        # episódio sem o fecho
OUT_LEN = 3.87                    # fecho do scanner (duração do outro_binder_916.mp4)
TOTAL = DUR + OUT_LEN
INK = (17, 17, 17)
PAPER = (244, 240, 230)
GREY = (119, 115, 108)
BORDO = (118, 47, 50)

STAGE_Y = 352                     # topo do palco
STAGE_H = round(1080 * 457 / 626) # 788: arte inteira em largura total (626x457 -> 1080x788)
CAP_Y = 1372                      # centro da legenda (acima da UI do Instagram)

def font(name, size, var=None):
    path = {
        "lora": "/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf",
        "lorai": "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf",
        "intb": "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf",
        "intsb": "/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf",
        "intm": "/usr/share/fonts/opentype/inter/Inter-Medium.otf",
    }[name]
    f = ImageFont.truetype(path, size)
    if var:
        f.set_variation_by_name(var)
    return f

F_TITLE = font("lora", 62, "Bold")
F_SUB = font("lorai", 30, "Italic")
F_CAP = font("lora", 58, "Bold")
F_CRED = font("lora", 22, "Regular")
F_LABEL = font("lorai", 36, "SemiBold Italic")
F_QUOTE = font("lorai", 34, "SemiBold Italic")
F_STAMP = font("lora", 40, "Bold")
F_END = font("lora", 44, "Bold")
F_END2 = font("lorai", 32, "Italic")

# ------------------------------------------------------------------ assets
ART = {"f": Image.open(f"{EP}/art_front.jpg").convert("RGB"),      # 626x457
       "b": Image.open(f"{EP}/art_back.jpg").convert("RGB")}
AW, AH = ART["f"].size
CARD = {"f": Image.open(f"{EP}/card_front.png").convert("RGBA"),   # 744x1040
        "b": Image.open(f"{EP}/card_back.png").convert("RGBA")}
medal = Image.open(f"{BASE}/assets/medalhao.png").convert("RGBA")
_mm = Image.new("L", medal.size, 0)
ImageDraw.Draw(_mm).ellipse([4, 2, medal.width - 5, medal.height - 3], fill=255)
medal.putalpha(_mm.filter(ImageFilter.GaussianBlur(1.5)))
expr = {k: Image.open(f"{BASE}/assets/{k}.png").convert("RGB")
        for k in ("neutro", "desconfiado", "indignado", "admirado")}
words = json.load(open(f"{EP}/audio/words_novo.json"))
LOGO = Image.open(f"{KIT}/manaburn/logo/logo_mark.png").convert("RGBA")
SCAN = [Image.open(f"{KIT}/comum/outro/scan/{i:03d}.jpg").convert("RGB") for i in range(45)]
OUTRO_MP4 = f"{KIT}/comum/outro/outro_binder_916.mp4"

def paper_bg():
    bg = Image.new("RGB", (W, H), PAPER)
    n = Image.effect_noise((W // 2, H // 2), 18).resize((W, H), Image.BICUBIC)
    n = n.point(lambda v: 128 + (v - 128) * 0.35)
    bg = ImageChops.multiply(bg, Image.merge("RGB", (n, n, n)).point(lambda v: min(255, v + 120)))
    d = ImageDraw.Draw(bg)
    d.line([(60, 168), (W - 60, 168)], fill=INK, width=3)
    d.line([(60, 176), (W - 60, 176)], fill=INK, width=1)
    d.text((W // 2, 228), "O TRIBUNAL ESTÉTICO", font=F_TITLE, fill=INK, anchor="mm")
    d.text((W // 2, 292), "pareceres do Conde de Manaforte  ·  processo nº 003", font=F_SUB, fill=GREY, anchor="mm")
    d.line([(60, 330), (W - 60, 330)], fill=INK, width=1)
    return bg

BG = paper_bg()

def oval_inset(img, w, h, border=6):
    im = img.resize((w, int(img.height * w / img.width)), Image.LANCZOS)
    top = max(0, (im.height - h) // 3)
    im = im.crop((0, top, w, top + h))
    out = Image.new("RGBA", (w + 2 * border + 12, h + 2 * border + 12), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    d.ellipse([0, 0, out.width - 1, out.height - 1], fill=PAPER + (255,), outline=INK + (255,), width=4)
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).ellipse([0, 0, w - 1, h - 1], fill=255)
    out.paste(im, (border + 6, border + 6), m)
    d.ellipse([border + 4, border + 4, border + w + 8, border + h + 8], outline=INK + (255,), width=3)
    return out

INSETS = {k: oval_inset(v, 236, 268) for k, v in expr.items()}

def stamp(text, w=360, h=150, rot=-8, color=BORDO):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, 4, w - 5, h - 5], radius=14, outline=color + (255,), width=7)
    d.rounded_rectangle([16, 16, w - 17, h - 17], radius=8, outline=color + (255,), width=2)
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        y = h / 2 + (i - (len(lines) - 1) / 2) * 46
        d.text((w / 2, y), ln, font=F_STAMP, fill=color + (255,), anchor="mm")
    n = Image.effect_noise((w, h), 50).point(lambda v: 255 if v > 45 else 0)
    im.putalpha(ImageChops.multiply(im.getchannel("A"), n))
    back = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(back).rounded_rectangle([4, 4, w - 5, h - 5], radius=14, fill=PAPER + (235,))
    back.alpha_composite(im)
    return back.rotate(rot, expand=True, resample=Image.BICUBIC)

ST_REU = stamp("RÉ · 2026", 360, 110, -7)
ST_RETIRADA = stamp("ACUSAÇÃO\nRETIRADA", 400, 170, 7)
ST_NOTAVEL = stamp("OBRA\nNOTÁVEL", 340, 170, 8)
ST_PARECER = stamp("PARECER\nEMITIDO", 380, 180, -9)

# ------------------------------------------------------------------ util
def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)

def prog(t, a, b):
    return ease((t - a) / (b - a)) if b > a else float(t >= a)

def lerp(a, b, k):
    return a + (b - a) * k

def wt(word, n=1):
    """Início da n-ésima ocorrência de uma palavra na narração."""
    c = 0
    for w in words:
        if w[0] == word:
            c += 1
            if c == n:
                return w[1]
    raise KeyError(word)

def art_view(face, cx, cy, z):
    """Arte enquadrada: z=1 mostra a arte inteira na largura do ecrã (sem corte lateral)."""
    vw = AW / z
    vh = vw * STAGE_H / W
    x0 = min(max(cx - vw / 2, 0), AW - vw)
    y0 = min(max(cy - vh / 2, 0), max(0, AH - vh))
    if vh > AH:
        y0 = (AH - vh) / 2
    box = (x0, y0, x0 + vw, y0 + vh)
    return ART[face].transform((W, STAGE_H), Image.EXTENT, box, Image.BICUBIC), box

def to_stage(box, ax, ay):
    x0, y0, x1, y1 = box
    return ((ax - x0) / (x1 - x0) * W, STAGE_Y + (ay - y0) / (y1 - y0) * STAGE_H)

def ink_ellipse(d, c, rx, ry, k, rot=-0.3):
    if k <= 0:
        return
    n = max(2, int(80 * k))
    pts = []
    for i in range(n + 1):
        a = rot + 2.15 * math.pi * k * i / n
        wob = 1 + 0.03 * math.sin(a * 3)
        pts.append((c[0] + rx * wob * math.cos(a), c[1] + ry * wob * math.sin(a)))
    d.line(pts, fill=INK, width=13, joint="curve")
    d.line(pts, fill=PAPER, width=6, joint="curve")

def ink_path(d, pts, k, head=True):
    """Seta de tinta ao longo de uma polilinha (revelada por k)."""
    if k <= 0:
        return
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    L = sum(seg) * k
    out = [pts[0]]
    for i, s in enumerate(seg):
        if L >= s:
            out.append(pts[i + 1]); L -= s
        else:
            f = L / s
            out.append((lerp(pts[i][0], pts[i + 1][0], f), lerp(pts[i][1], pts[i + 1][1], f)))
            break
    d.line(out, fill=INK, width=13, joint="curve")
    d.line(out, fill=PAPER, width=6, joint="curve")
    if head and k > 0.95:
        p, q0 = out[-1], out[-2]
        ang = math.atan2(p[1] - q0[1], p[0] - q0[0])
        for s in (-1, 1):
            q = (p[0] - 38 * math.cos(ang + s * 0.45), p[1] - 38 * math.sin(ang + s * 0.45))
            d.line([p, q], fill=INK, width=13)
            d.line([p, q], fill=PAPER, width=6)

def label(d, xy, text, anchor="mm"):
    x, y = xy
    bb = d.textbbox((x, y), text, font=F_LABEL, anchor=anchor)
    d.rounded_rectangle([bb[0] - 14, bb[1] - 8, bb[2] + 14, bb[3] + 8], radius=6, fill=PAPER, outline=INK, width=3)
    d.text((x, y), text, font=F_LABEL, fill=INK, anchor=anchor)

def paste_center(frame, im, cx, cy, alpha=1.0, scale=1.0):
    if scale != 1.0:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.LANCZOS)
    if im.mode != "RGBA":
        im = im.convert("RGBA")
    if alpha < 1:
        a = im.getchannel("A").point(lambda v: int(v * alpha))
        im = im.copy(); im.putalpha(a)
    frame.paste(im, (int(cx - im.width / 2), int(cy - im.height / 2)), im)

def stamp_in(frame, st, cx, cy, t, t0):
    if t < t0:
        return
    k = prog(t, t0, t0 + 0.18)
    paste_center(frame, st, cx, cy, alpha=k, scale=lerp(1.6, 1.0, k))

def magnifier(frame, region_fn, center, radius, mag, k):
    if k <= 0:
        return
    r = int(radius * (0.6 + 0.4 * k))
    cx, cy = center
    region = region_fn(cx, cy, r, mag)
    m = Image.new("L", (2 * r, 2 * r), 0)
    ImageDraw.Draw(m).ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=255)
    frame.paste(region.resize((2 * r, 2 * r), Image.LANCZOS).filter(ImageFilter.UnsharpMask(3, 120, 2)), (int(cx - r), int(cy - r)), m)
    d = ImageDraw.Draw(frame)
    d.ellipse([cx - r - 9, cy - r - 9, cx + r + 9, cy + r + 9], outline=INK, width=18)
    d.ellipse([cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3], outline=PAPER, width=5)
    ang = math.radians(48)
    h0 = (cx + (r + 14) * math.cos(ang), cy + (r + 14) * math.sin(ang))
    h1 = (cx + (r + 95) * math.cos(ang), cy + (r + 95) * math.sin(ang))
    d.line([h0, h1], fill=INK, width=40)
    d.line([h0, h1], fill=GREY, width=22)

def card_full(frame, face="f", alpha=1.0, highlight=None, hk=0.0, sx=1.0):
    """Carta inteira, rodapé visível. sx<1 encolhe na horizontal (flip 2D)."""
    c = CARD[face]
    ch = STAGE_H - 10
    cw = int(c.width * ch / c.height)
    im = c.resize((cw, ch), Image.LANCZOS)
    if highlight and hk > 0:
        d = ImageDraw.Draw(im)
        s = ch / c.height
        for (a, b, e, g) in highlight:
            d.rectangle([a * s, b * s, e * s, g * s], outline=PAPER + (255,), width=5)
            d.rectangle([a * s - 5, b * s - 5, e * s + 5, g * s + 5], outline=BORDO + (255,), width=5)
    if sx < 1.0:
        im = im.resize((max(2, int(cw * sx)), ch), Image.LANCZOS)
    if alpha < 1:
        a = im.getchannel("A").point(lambda v: int(v * alpha)); im.putalpha(a)
    frame.paste(im, ((W - im.width) // 2, STAGE_Y + 5), im)

def credit(d):
    for i, ln in enumerate([
            "Na tela: Voldaren Pariah // Abolisher of Bloodlines (Secret Lair Drop, 2026), nº 1441.",
            "Arte: Véronique Meignaud.  © Wizards of the Coast.",
            "Conteúdo de fã não oficial, sem aprovação ou endosso da Wizards."]):
        d.text((W // 2, STAGE_Y + STAGE_H + 24 + i * 29), ln, font=F_CRED, fill=GREY, anchor="mm")

# ------------------------------------------------------------------ legendas
KEY = {"Voldaren.", "terminado.", "Meignaud.", "três", "refeição.", "acusação.", "notável.", "Halloween.", "tinta.", "réu"}

def chunks():
    out, cur = [], []
    for w in words:
        cur.append(w)
        if w[0][-1] in ".:?" or (w[0][-1] == "," and len(cur) >= 2) or len(cur) >= 4:
            out.append(cur); cur = []
    if cur:
        out.append(cur)
    return out

CHUNKS = chunks()

def caption(d, t):
    for i, ch in enumerate(CHUNKS):
        nxt = CHUNKS[i + 1][0][1] - 0.05 if i + 1 < len(CHUNKS) else 1e9
        if ch[0][1] - 0.05 <= t <= min(ch[-1][2] + 0.25, nxt):
            parts = [(w[0], w) for w in ch]
            total = sum(d.textlength(p + " ", font=F_CAP) for p, _ in parts) - d.textlength(" ", font=F_CAP)
            lines = [parts[:len(parts) // 2], parts[len(parts) // 2:]] if total > W - 120 else [parts]
            for li, ln in enumerate(lines):
                lw = sum(d.textlength(p + " ", font=F_CAP) for p, _ in ln) - d.textlength(" ", font=F_CAP)
                x = (W - lw) / 2
                y = CAP_Y + (li - (len(lines) - 1) / 2) * 72
                for p, w in ln:
                    col = BORDO if w[0] in KEY else INK
                    if t < w[1] - 0.04:
                        col = (190, 184, 172)
                    d.text((x, y), p, font=F_CAP, fill=col, anchor="lm")
                    x += d.textlength(p + " ", font=F_CAP)
            return

# ------------------------------------------------------------------ coordenadas (art_crop 626x457, medidas na grelha)
FACE_F = (385, 108)        # rosto da frente
FACE_B = (325, 170)        # rosto do verso (olhos ~y150, boca ~y210)
RIBBON = [(20, 150), (110, 120), (200, 95), (290, 110), (360, 112)]   # fita vermelha da esquerda até ao rosto
BRIGHT = (515, 240)        # zona de contraluz (fundo claro à direita)
WEB = (150, 205)           # teia de fitas vermelhas
HL_SAC = [(58, 712, 575, 790)]       # "Sacrifice three other creatures: Transform this creature." (card 744x1040)
HL_ART = [(36, 960, 350, 1010)]      # rodapé: R 1441 · SLD · Véronique Meignaud
INSET_XY = (W - 168, STAGE_Y + STAGE_H - 150)

# tempos (ancorados na narração)
T_ART1 = wt("Meus") + 2.3                 # fim da abertura (sai o medalhão)
T_REU = wt("2026.") + 0.1
T_NAME = wt("Voldaren") - 0.15
T_MAIS = wt("Mais") - 0.1
T_ANAL = wt("Vista") - 0.15
T_CARD = wt("Mas") - 0.15
T_FLIP = wt("vira")
T_FLIP_END = T_FLIP + 0.5
T_BACK = wt("E") - 0.1                    # "E o rosto..."
T_DERRETE = wt("Derrete.")
T_MARMORE = wt("Mármore")
T_ARTISTA = wt("artista") - 0.2
T_TEXTO = wt("E", 2) - 0.1                # "E o texto da carta esclarece"
T_ORACLE = wt("sacrifique") - 0.1
T_OU = wt("Ou") - 0.1
T_FLAVOR = wt("Está") - 0.1
T_RETIRA = wt("O", 2) - 0.1               # "O Tribunal retira a acusação."
T_ACUSA = wt("acusação.")
T_MONO = wt("monóculo,") - 0.08
T_PARECER = wt("Parecer:") - 0.15
T_NOTAVEL = wt("notável.")
T_FELIZ = wt("Feliz") - 0.15
T_QUAL = wt("Qual") - 0.3
T_EMITIDO = wt("Tribunal", 4) - 0.05

def scene_art(frame, face, cx=None, cy=None, z=1.0):
    im, box = art_view(face, AW / 2 if cx is None else cx, AH / 2 if cy is None else cy, z)
    frame.paste(im, (0, STAGE_Y))
    ImageDraw.Draw(frame).rectangle([0, STAGE_Y, W - 1, STAGE_Y + STAGE_H - 1], outline=INK, width=4)
    return box

def quote_box(f, text, src, k, cy=None):
    if k <= 0:
        return
    lines = text.split("\n")
    h = 90 + 50 * len(lines)
    box = Image.new("RGBA", (940, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(box)
    d.rounded_rectangle([0, 0, 939, h - 1], radius=10, fill=PAPER + (245,), outline=INK + (255,), width=4)
    d.rounded_rectangle([12, 12, 927, h - 13], radius=6, outline=INK + (255,), width=1)
    for i, ln in enumerate(lines):
        d.text((470, 52 + i * 50), ln, font=F_QUOTE, fill=INK, anchor="mm")
    d.text((470, h - 34), src, font=F_CRED, fill=GREY, anchor="mm")
    paste_center(f, box, W / 2, cy or (STAGE_Y + STAGE_H - h / 2 - 30), alpha=k)

def lupa(f, face, box, center_art, mag, k, radius=230, offset=(0, 0)):
    lc = to_stage(box, *center_art)
    src_im = ART[face]

    def region(cx, cy, r, m):
        ax = box[0] + (cx - offset[0]) / W * (box[2] - box[0])
        ay = box[1] + (cy - offset[1] - STAGE_Y) / STAGE_H * (box[3] - box[1])
        half = r / m * (box[2] - box[0]) / W
        return src_im.transform((2 * r, 2 * r), Image.EXTENT, (ax - half, ay - half, ax + half, ay + half), Image.BICUBIC)

    magnifier(f, region, (lc[0] + offset[0], lc[1] + offset[1]), radius, mag, k)
    return lc

def egg_III(d, cx, cy):
    """Easter egg: três traços bordô = os três sacrifícios."""
    for i in range(3):
        x = cx + i * 20
        d.line([(x, cy - 24), (x, cy + 24)], fill=BORDO, width=7)

def render_frame(t):
    f = BG.copy()
    d = ImageDraw.Draw(f)

    if t < T_ART1:                                           # A · entrada do Conde
        k = prog(t, 0.0, 0.6)
        sc = lerp(1.06, 1.0, k)
        mh = int(STAGE_H * 0.98 * sc)
        mw = int(medal.width * mh / medal.height)
        paste_center(f, medal.resize((mw, mh), Image.LANCZOS), W / 2, STAGE_Y + STAGE_H / 2, alpha=k)
    elif t < T_NAME:                                         # B · a ré (arte da frente) + carimbo
        scene_art(f, "f")
        paste_center(f, INSETS["neutro"], *INSET_XY, alpha=prog(t, T_ART1, T_ART1 + 0.3))
        stamp_in(f, ST_REU, 250, STAGE_Y + 120, t, T_REU)
        credit(d)
    elif t < T_MAIS:                                         # C · o nome (carta inteira)
        card_full(f, "f", alpha=prog(t, T_NAME, T_NAME + 0.25))
        credit(d)
    elif t < T_ANAL:                                         # D · "mais uma Voldaren"
        scene_art(f, "f")
        d = ImageDraw.Draw(f)
        paste_center(f, INSETS["desconfiado"], *INSET_XY)
        if t > T_MAIS + 0.35:
            label(d, (300, STAGE_Y + STAGE_H - 70), "cf. processo nº 002")
        credit(d)
    elif t < T_CARD:                                         # E · composição
        box = scene_art(f, "f")
        d = ImageDraw.Draw(f)
        bc = to_stage(box, *BRIGHT)
        tc = wt("contra")
        ink_ellipse(d, bc, 170, 210, prog(t, tc, tc + 0.7), rot=2.9)
        if t > tc + 0.5:
            label(d, (bc[0] - 20, bc[1] + 250), "contraluz")
        tw = wt("teia")
        if t > tw - 0.1:
            label(d, to_stage(box, WEB[0], WEB[1] + 70), "teia de sangue")
        to = wt("leva")
        ink_path(d, [to_stage(box, *p) for p in RIBBON], prog(t, to, to + 1.0))
        tr = wt("rosto.")
        ink_ellipse(d, to_stage(box, *FACE_F), 105, 120, prog(t, tr - 0.1, tr + 0.5))
        credit(d)
    elif t < T_BACK:                                         # F · o Tribunal vira a carta (flip 2D)
        if t < T_FLIP:
            card_full(f, "f", alpha=prog(t, T_CARD, T_CARD + 0.2))
        else:
            k = (t - T_FLIP) / (T_FLIP_END - T_FLIP)
            if k < 0.5:
                card_full(f, "f", sx=max(0.01, math.cos(k * math.pi)))
            elif k < 1:
                card_full(f, "b", sx=max(0.01, -math.cos(k * math.pi)))
            else:
                card_full(f, "b")
        credit(d)
    elif t < T_ARTISTA:                                      # G · o rosto do verso (lupa)
        box = scene_art(f, "b")
        mag = lerp(1.45, 1.7, prog(t, T_DERRETE - 0.1, T_DERRETE + 0.4))
        lc = lupa(f, "b", box, FACE_B, mag, prog(t, T_BACK + 0.15, T_BACK + 0.5), offset=(-120, -10))
        d = ImageDraw.Draw(f)
        paste_center(f, INSETS["indignado"], *INSET_XY, alpha=prog(t, T_BACK, T_BACK + 0.3))
        if t > T_DERRETE:
            label(d, (180, STAGE_Y + 80), "derrete.")
        if t > T_MARMORE:
            label(d, (230, STAGE_Y + STAGE_H - 60), "mármore molhado")
        credit(d)
    elif t < T_TEXTO:                                        # H · a artista (rodapé da carta)
        card_full(f, "b", highlight=HL_ART, hk=prog(t, wt("Véronique") - 0.1, wt("Véronique") + 0.2))
        credit(d)
    elif t < T_ORACLE + 1.6:                                 # I · o texto da carta (Oracle no próprio cartão)
        card_full(f, "f", alpha=prog(t, T_TEXTO, T_TEXTO + 0.2), highlight=HL_SAC, hk=prog(t, T_ORACLE - 0.2, T_ORACLE + 0.1))
        credit(d)
    elif t < T_OU:                                           # I2 · citação Oracle sobre a arte
        scene_art(f, "f")
        quote_box(f, "“Sacrifice three other creatures:\nTransform this creature.”", "Oracle · Scryfall", prog(t, T_ORACLE + 1.6, T_ORACLE + 1.9))
        credit(d)
    elif t < T_FLAVOR:                                       # J · ou seja: não está inacabado
        k = prog(t, T_OU, T_FLAVOR)
        box = scene_art(f, "b", lerp(AW / 2, FACE_B[0], k), lerp(AH / 2, FACE_B[1], k), lerp(1.0, 1.35, k))
        d = ImageDraw.Draw(f)
        ink_ellipse(d, to_stage(box, *FACE_B), 200, 230, prog(t, wt("inacabado.") - 0.1, wt("inacabado.") + 0.5))
        paste_center(f, INSETS["desconfiado"], *INSET_XY)
        credit(d)
    elif t < T_RETIRA:                                       # K · "no meio da refeição" (flavor)
        box = scene_art(f, "b", FACE_B[0], FACE_B[1], 1.35)
        quote_box(f, "“Before feeding, she spins\na web of blood and malice.”", "texto de ambientação da frente · Scryfall",
                  prog(t, T_FLAVOR + 0.2, T_FLAVOR + 0.5))
        credit(d)
    elif t < T_PARECER:                                      # L · acusação retirada (+ easter egg III)
        scene_art(f, "f")
        stamp_in(f, ST_RETIRADA, 300, STAGE_Y + 150, t, T_ACUSA + 0.05)
        d = ImageDraw.Draw(f)
        if T_ACUSA + 0.25 < t < T_ACUSA + 1.25:
            egg_III(d, 520, STAGE_Y + 70)
        if t > T_MONO:
            paste_center(f, INSETS["neutro"], *INSET_XY, alpha=prog(t, T_MONO, T_MONO + 0.25))
        credit(d)
    elif t < T_FELIZ:                                        # M · parecer: obra notável
        scene_art(f, "f")
        paste_center(f, INSETS["admirado"], *INSET_XY, alpha=prog(t, T_PARECER, T_PARECER + 0.3))
        stamp_in(f, ST_NOTAVEL, 230, STAGE_Y + 160, t, T_NOTAVEL + 0.05)
        credit(d)
    elif t < T_QUAL:                                         # N · Halloween: a máscara da tinta
        scene_art(f, "b")
        paste_center(f, INSETS["admirado"], *INSET_XY)
        credit(d)
    else:                                                    # O · fecho do Conde
        k = prog(t, T_QUAL, T_QUAL + 0.35)
        mh = int(STAGE_H * 0.86)
        mw = int(medal.width * mh / medal.height)
        paste_center(f, medal.resize((mw, mh), Image.LANCZOS), W / 2, STAGE_Y + mh / 2 + 6, alpha=k)
        stamp_in(f, ST_PARECER, W / 2 + 230, STAGE_Y + mh - 60, t, T_EMITIDO)
        if t > T_QUAL + 0.4:
            d.text((W / 2, STAGE_Y + STAGE_H + 20), "A · inacabado    ou    B · transformação?", font=F_END, fill=INK, anchor="mm")
            d.text((W / 2, STAGE_Y + STAGE_H + 76), "responda no comentário fixado", font=F_END2, fill=GREY, anchor="mm")

    caption(ImageDraw.Draw(f), t)
    ImageDraw.Draw(f).text((W // 2, 1530), "@binderthetrade", font=F_CRED, fill=GREY, anchor="mm")
    return f

# ------------------------------------------------------------------ fecho do scanner
def outro_frame(t):
    """Reconstrução do fecho (quadros reais de comum/outro/scan/ + logótipo), como oraculo/episodios/ep02_render.py.
    Só é usada se comum/outro/outro_binder_916.mp4 não existir."""
    BGD, EM, WHITE = (5, 10, 16), (16, 185, 129), (236, 241, 245)
    eio = lambda x: 1 - (1 - min(1, max(0, x))) ** 3
    if t < 1.5:
        return SCAN[min(44, int(t * 30))].copy()
    im = Image.new("RGB", (W, H), BGD); d = ImageDraw.Draw(im, "RGBA")
    v = eio((t - 1.5) / 0.6); size = int(60 + 260 * v)
    lg = LOGO.resize((size, size), Image.LANCZOS).rotate(-140 * (1 - v), resample=Image.BICUBIC)
    im.paste(lg, (int(W / 2 - lg.width / 2), int(760 - lg.height / 2)), lg)
    q = ease((t - 1.9) / 0.3); r = ease((t - 2.1) / 0.3)
    d.text((W / 2, 1000 + (1 - q) * 20), "BINDER Vision", font=font("intb", 92), fill=WHITE + (int(255 * q),), anchor="ma")
    d.text((W / 2, 1130), "Escaneie suas cartas e organize seus decks.", font=font("intm", 38), fill=(190, 200, 210, int(255 * q)), anchor="ma")
    d.text((W / 2, 1250), "Disponível no Google Play · Link na bio", font=font("intsb", 40), fill=EM + (int(255 * r),), anchor="ma")
    if t > 3.4:
        im = Image.blend(im, Image.new("RGB", (W, H), (0, 0, 0)), min(1, (t - 3.4) / 0.47))
    return im

def frame_at(t):
    return render_frame(t) if t < DUR else outro_frame(t - DUR)

# ------------------------------------------------------------------ áudio
BEAT = 0.88236                        # 68 batidas/min (meio-tempo de ~136 BPM), medido no tema
CUT_A = 22.09                         # ponto de emenda no grid do Ep. 002
CUT_B = CUT_A - 8 * BEAT              # recuo de 8 batidas: tema 44,16 s -> 51,2 s (cobre episódio + fecho)

def stamps():
    return [T_REU, T_ACUSA + 0.05, T_NOTAVEL + 0.05, T_EMITIDO]

def build_audio(path):
    TEMA = f"{BASE}/musica/tema.mp3"
    XF = 0.25
    st = stamps()
    rise = words[-1][2] + 0.1
    parts = [
        f"[1:a]atrim=0:{CUT_A + XF / 2},asetpts=PTS-STARTPTS[ma]",
        f"[1:a]atrim={CUT_B - XF / 2},asetpts=PTS-STARTPTS[mb]",
        f"[ma][mb]acrossfade=d={XF}:c1=tri:c2=tri,aresample=48000,aformat=channel_layouts=stereo,volume=-3dB,apad=pad_dur=2[mus]",
        f"[0:a]aresample=48000,aformat=channel_layouts=stereo,apad=pad_dur={OUT_LEN + 3},asplit=2[vox][key]",
        "[mus][key]sidechaincompress=threshold=0.025:ratio=5:attack=25:release=450:makeup=1,"
        f"volume='1+min(max((t-{rise:.2f})/0.4,0),1)':eval=frame[bed]",
    ]
    for i, s_ in enumerate(st):
        parts.append(f"aevalsrc='0.9*sin(2*PI*70*t)*exp(-18*t)+0.35*(random(0)-0.5)*exp(-40*t)':d=0.35:s=48000,"
                     f"aformat=channel_layouts=stereo,adelay={int(s_*1000)}|{int(s_*1000)},volume=0.6[st{i}]")
    mix = "".join(f"[st{i}]" for i in range(len(st)))
    parts.append(f"[vox][bed]{mix}amix=inputs={len(st)+2}:normalize=0:duration=longest,"
                 f"atrim=0:{TOTAL},afade=t=out:st={TOTAL-0.6}:d=0.6,loudnorm=I=-14:TP=-2.2:LRA=11[a]")
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-i", f"{EP}/audio/narracao.wav", "-i", TEMA,
                    "-filter_complex", ";".join(parts), "-map", "[a]", "-ar", "48000", "-ac", "2", path], check=True)

def main():
    args = sys.argv[1:]
    if "--preview" in args:
        os.makedirs(f"{BASE}/prev2", exist_ok=True)
        for t in [float(x) for x in args[args.index("--preview") + 1].split(",")]:
            frame_at(t).save(f"{BASE}/prev2/p_{t:05.2f}.png")
        return
    out = args[0] if args and not args[0].startswith("--") else f"{BASE}/saida/Conde_Ep003_VoldarenPariah_916.mp4"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    mixp = f"{EP}/audio/mix.wav"
    build_audio(mixp)
    if "--audio-only" in args:
        return
    usa_mp4 = os.path.exists(OUTRO_MP4)
    corpo = out.replace(".mp4", "_corpo.mp4") if usa_mp4 else out
    n = int(round((DUR if usa_mp4 else TOTAL) * FPS))
    p = subprocess.Popen(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", mixp, "-map", "0:v", "-map", "1:a",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", corpo],
                         stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame_at(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    if usa_mp4:      # fecho oficial: concatena o vídeo, o áudio da mistura cobre os 3,87 s
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", corpo, "-i", OUTRO_MP4, "-i", mixp,
                        "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0,fps=30,format=yuv420p[v]", "-map", "[v]", "-map", "2:a",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                        "-shortest", "-movflags", "+faststart", out], check=True)
    print(out)

if __name__ == "__main__":
    main()
