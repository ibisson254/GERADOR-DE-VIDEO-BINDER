"""Conde de Manaforte · Episódio 002 · O Tribunal Estético (Olivia Voldaren)
Gera os quadros 1080x1920 e envia ao ffmpeg.
Modelo para os próximos episódios: copiar, trocar caminhos, KEY, coordenadas, cenas, carimbos e emenda da música.
Uso: python3 montar_ep002.py [saida.mp4] [--preview t1,t2,...] [--audio-only]
"""
import sys, json, math, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

BASE = "/home/claude/conde"
W, H, FPS = 1080, 1920, 30
DUR = 47.5
INK = (17, 17, 17)
PAPER = (244, 240, 230)
GREY = (119, 115, 108)
BORDO = (118, 47, 50)

STAGE_Y = 352                     # topo do palco
STAGE_H = 792                     # arte inteira em largura total: 616x452 -> 1080x792
CAP_Y = 1372                      # centro da legenda (acima da UI do Instagram)

def font(name, size, var=None):
    path = {
        "bask": "/usr/share/fonts/truetype/baskerville/GFSBaskerville.otf",
        "lora": "/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf",
        "lorai": "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf",
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
F_STAMP = font("lora", 40, "Bold")
F_END = font("lora", 50, "Bold")
F_END2 = font("lorai", 34, "Italic")

# ------------------------------------------------------------------ assets
art = Image.open(f"{BASE}/ep002/art.jpg").convert("RGB")          # 616x452
AW, AH = art.size
card = Image.open(f"{BASE}/ep002/card.png").convert("RGBA")       # 745x1040
medal = Image.open(f"{BASE}/assets/medalhao.png").convert("RGBA")
_mm = Image.new("L", medal.size, 0)
ImageDraw.Draw(_mm).ellipse([4, 2, medal.width - 5, medal.height - 3], fill=255)
medal.putalpha(_mm.filter(ImageFilter.GaussianBlur(1.5)))
expr = {k: Image.open(f"{BASE}/assets/{k}.png").convert("RGB")
        for k in ("neutro", "desconfiado", "indignado", "admirado")}
words = json.load(open(f"{BASE}/ep002/audio/words_novo.json"))

def paper_bg():
    import random
    random.seed(3)
    bg = Image.new("RGB", (W, H), PAPER)
    n = Image.effect_noise((W // 2, H // 2), 18).resize((W, H), Image.BICUBIC)
    n = n.point(lambda v: 128 + (v - 128) * 0.35)
    bg = ImageChops.multiply(bg, Image.merge("RGB", (n, n, n)).point(lambda v: min(255, v + 120)))
    d = ImageDraw.Draw(bg)
    # cabeçalho editorial
    d.line([(60, 168), (W - 60, 168)], fill=INK, width=3)
    d.line([(60, 176), (W - 60, 176)], fill=INK, width=1)
    d.text((W // 2, 228), "O TRIBUNAL ESTÉTICO", font=F_TITLE, fill=INK, anchor="mm")
    d.text((W // 2, 292), "pareceres do Conde de Manaforte  ·  processo nº 002", font=F_SUB, fill=GREY, anchor="mm")
    d.line([(60, 330), (W - 60, 330)], fill=INK, width=1)
    return bg

BG = paper_bg()

def oval_inset(img, w, h, border=6):
    """Retrato numa moldura oval com filete duplo."""
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
    # textura de carimbo gasto
    n = Image.effect_noise((w, h), 50).point(lambda v: 255 if v > 45 else 0)
    a = ImageChops.multiply(im.getchannel("A"), n)
    im.putalpha(a)
    back = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(back).rounded_rectangle([4, 4, w - 5, h - 5], radius=14, fill=PAPER + (235,))
    back.alpha_composite(im)
    return back.rotate(rot, expand=True, resample=Image.BICUBIC)

ST_REU = stamp("RÉ · 2011", 360, 110, -7)
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

def art_view(cx, cy, z):
    """Arte enquadrada: z=1 mostra a arte inteira na largura do ecrã."""
    vw = AW / z
    vh = vw * STAGE_H / W
    x0 = min(max(cx - vw / 2, 0), AW - vw)
    y0 = min(max(cy - vh / 2, 0), max(0, AH - vh))
    if vh > AH:
        y0 = (AH - vh) / 2
    box = (x0, y0, x0 + vw, y0 + vh)
    im = art.transform((W, STAGE_H), Image.EXTENT, box, Image.BICUBIC)
    return im, box

def to_stage(box, ax, ay):
    x0, y0, x1, y1 = box
    return ((ax - x0) / (x1 - x0) * W, STAGE_Y + (ay - y0) / (y1 - y0) * STAGE_H)

def ink_ellipse(d, c, rx, ry, k, rot=-0.3):
    """Elipse traçada à mão, revelada progressivamente (k 0..1)."""
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

def ink_arrow(d, p0, p1, k):
    if k <= 0:
        return
    p = (lerp(p0[0], p1[0], k), lerp(p0[1], p1[1], k))
    d.line([p0, p], fill=INK, width=13)
    d.line([p0, p], fill=PAPER, width=6)
    if k > 0.95:
        ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
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

def magnifier(frame, src_box_fn, center, radius, mag, k):
    """Lupa crítica: ampliação circular com aro e cabo."""
    if k <= 0:
        return
    r = int(radius * (0.6 + 0.4 * k))
    cx, cy = center
    region = src_box_fn(cx, cy, r, mag)
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

def card_full(frame, alpha=1.0, highlight=None, hk=0.0):
    ch = STAGE_H - 10
    cw = int(card.width * ch / card.height)
    im = card.resize((cw, ch), Image.LANCZOS)
    x0, y0 = (W - cw) // 2, STAGE_Y + 5
    if highlight and hk > 0:
        d = ImageDraw.Draw(im)
        s = ch / card.height
        for (a, b, c, e) in highlight:
            d.rectangle([a * s, b * s, c * s, e * s], outline=PAPER + (255,), width=6)
            d.rectangle([a * s - 6, b * s - 6, c * s + 6, e * s + 6], outline=INK + (255,), width=6)
    if alpha < 1:
        a = im.getchannel("A").point(lambda v: int(v * alpha)); im.putalpha(a)
    frame.paste(im, (x0, y0), im)

def credit(d):
    d.text((W // 2, STAGE_Y + STAGE_H + 26),
           "Olivia Voldaren (Innistrad, 2011)  ·  Arte: Eric Deschamps  ·  © Wizards of the Coast",
           font=F_CRED, fill=GREY, anchor="mm")
    d.text((W // 2, STAGE_Y + STAGE_H + 56),
           "Conteúdo de fã não oficial, sem aprovação ou endosso da Wizards.",
           font=F_CRED, fill=GREY, anchor="mm")

# ------------------------------------------------------------------ legendas
KEY = {"2011.", "Voldaren.", "joelho.", "órfão.", "perna", "errado.", "vampiro.", "rascunho", "notável.", "réu", "Tribunal", "Draftsim,"}

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
    for ch in CHUNKS:
        if ch[0][1] - 0.05 <= t <= ch[-1][2] + 0.25:
            txt_parts = [(w[0], w) for w in ch]
            total = sum(d.textlength(p + " ", font=F_CAP) for p, _ in txt_parts) - d.textlength(" ", font=F_CAP)
            if total > W - 120:
                # duas linhas
                mid = len(txt_parts) // 2
                lines = [txt_parts[:mid], txt_parts[mid:]]
            else:
                lines = [txt_parts]
            for li, ln in enumerate(lines):
                lw = sum(d.textlength(p + " ", font=F_CAP) for p, _ in ln) - d.textlength(" ", font=F_CAP)
                x = (W - lw) / 2
                y = CAP_Y + (li - (len(lines) - 1) / 2) * 72
                for p, w in ln:
                    spoken = t >= w[1] - 0.04
                    col = BORDO if w[0] in KEY else INK
                    if not spoken:
                        col = (190, 184, 172)
                    d.text((x, y), p, font=F_CAP, fill=col, anchor="lm")
                    x += d.textlength(p + " ", font=F_CAP)
            return

# ------------------------------------------------------------------ cenas
KNEE = (215, 226)           # "joelho" sob a mão direita (coords art.jpg 616x452)
HAND = (194, 228)
GOBLET = (405, 112)
CROWD = (115, 395)
FOOT = (455, 405)

def scene_art(frame, t, cx, cy, z, inset=None, inset_k=1.0):
    im, box = art_view(cx, cy, z)
    frame.paste(im, (0, STAGE_Y))
    d = ImageDraw.Draw(frame)
    d.rectangle([0, STAGE_Y, W - 1, STAGE_Y + STAGE_H - 1], outline=INK, width=4)
    return box

def quote_box(f, text, src, k):
    if k <= 0:
        return
    box = Image.new("RGBA", (900, 230), (0, 0, 0, 0))
    d = ImageDraw.Draw(box)
    d.rounded_rectangle([0, 0, 899, 229], radius=10, fill=PAPER + (245,), outline=INK + (255,), width=4)
    d.rounded_rectangle([12, 12, 887, 217], radius=6, outline=INK + (255,), width=1)
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        d.text((450, 70 + i * 52), ln, font=F_LABEL, fill=INK, anchor="mm")
    d.text((450, 190), src, font=F_CRED, fill=GREY, anchor="mm")
    paste_center(f, box, W / 2, STAGE_Y + 150, alpha=k)

def lupa(f, box, center_art, mag, k, offset=(0, 0), radius=240):
    lc = to_stage(box, *center_art)

    def src(cx, cy, r, m):
        ax = box[0] + cx / W * (box[2] - box[0])
        ay = box[1] + (cy - STAGE_Y) / STAGE_H * (box[3] - box[1])
        half = r / m * (box[2] - box[0]) / W
        return art.transform((2 * r, 2 * r), Image.EXTENT, (ax - half, ay - half, ax + half, ay + half), Image.BICUBIC)

    magnifier(f, src, (lc[0] + offset[0], lc[1] + offset[1]), radius, mag, k)
    return lc

INSET_XY = (W - 168, STAGE_Y + STAGE_H - 150)     # canto inferior direito (o joelho está à esquerda)

def render_frame(t):
    f = BG.copy()
    d = ImageDraw.Draw(f)

    if t < 6.2:                                            # A · entrada do Conde
        k = prog(t, 0.0, 0.7)
        sc = lerp(1.06, 1.0, k) * lerp(1.0, 1.05, prog(t, 0.7, 6.2))
        mh = int(STAGE_H * 0.98 * sc)
        mw = int(medal.width * mh / medal.height)
        paste_center(f, medal.resize((mw, mh), Image.LANCZOS), W / 2, STAGE_Y + STAGE_H / 2, alpha=k)
        stamp_in(f, ST_REU, W / 2 + 250, STAGE_Y + STAGE_H - 110, t, 4.7)
    elif t < 7.4:                                          # B · a ré
        card_full(f, alpha=prog(t, 6.2, 6.5))
        credit(d)
    elif t < 15.3:                                         # C · composição
        box = scene_art(f, t, AW / 2, AH / 2, 1.0)
        d = ImageDraw.Draw(f)
        ink_arrow(d, to_stage(box, 40, 330), to_stage(box, 215, 270), prog(t, 8.3, 9.0))
        ink_arrow(d, to_stage(box, 590, 330), to_stage(box, 410, 270), prog(t, 8.7, 9.4))
        ink_arrow(d, to_stage(box, 300, 448), to_stage(box, 300, 345), prog(t, 9.1, 9.7))
        cc = to_stage(box, *CROWD)
        ink_ellipse(d, cc, 200, 110, prog(t, 10.45, 11.3), rot=2.6)
        if t > 11.0:
            label(d, (cc[0] + 40, cc[1] - 150), "mascarados")
        gc = to_stage(box, *GOBLET)
        ink_ellipse(d, gc, 95, 120, prog(t, 13.0, 13.8))
        if t > 13.5:
            label(d, (gc[0] - 10, gc[1] + 165), "a taça")
        credit(d)
    elif t < 17.05:                                        # D · elegância vampírica
        k = prog(t, 15.3, 17.05)
        scene_art(f, t, lerp(AW / 2, 300, k), lerp(AH / 2, 190, k), lerp(1.0, 1.15, k))
        paste_center(f, INSETS["admirado"], *INSET_XY, alpha=prog(t, 15.35, 15.65))
        credit(d)
    elif t < 20.55:                                        # E · a mão direita
        k = prog(t, 17.05, 18.6)
        box = scene_art(f, t, lerp(300, KNEE[0] + 40, k), lerp(190, KNEE[1], k), lerp(1.15, 1.7, k))
        d = ImageDraw.Draw(f)
        hc = to_stage(box, *HAND)
        ink_ellipse(d, (hc[0] + 15, hc[1] + 5), 150, 170, prog(t, 18.0, 18.7))
        if t > 18.5:
            label(d, (hc[0] + 60, hc[1] - 240), "a mão direita")
        paste_center(f, INSETS["neutro"], *INSET_XY)
        credit(d)
    elif t < 24.15:                                        # F · o joelho órfão (lupa)
        box = scene_art(f, t, KNEE[0] + 40, KNEE[1], 1.7)
        lc = lupa(f, box, KNEE, lerp(1.6, 2.0, prog(t, 23.3, 23.8)), prog(t, 20.6, 20.95), offset=(0, 0))
        d = ImageDraw.Draw(f)
        if t > 23.45:
            label(d, (lc[0] + 40, lc[1] - 330), "órfão.")
        paste_center(f, INSETS["desconfiado"], *INSET_XY)
        credit(d)
    elif t < 26.7:                                         # G · a perna desce reta
        box = scene_art(f, t, 330, 300, 1.25)
        d = ImageDraw.Draw(f)
        kc = to_stage(box, *KNEE)
        ink_ellipse(d, kc, 110, 120, 1.0)
        ink_arrow(d, to_stage(box, 330, 250), to_stage(box, FOOT[0] - 10, FOOT[1] - 15), prog(t, 24.4, 25.9))
        if t > 25.9:
            label(d, to_stage(box, 360, 215), "a perna")
        paste_center(f, INSETS["desconfiado"], *INSET_XY)
        credit(d)
    elif t < 32.6:                                         # H · o bastidor (Draftsim)
        scene_art(f, t, AW / 2, AH / 2, 1.0)
        quote_box(f, "O artista corrigiu as pernas…\n…e enviou o arquivo errado.",
                  "relato atribuído ao artista, segundo o Draftsim", prog(t, 26.75, 27.1))
        paste_center(f, INSETS["indignado"], *INSET_XY, alpha=prog(t, 30.8, 31.1))
        credit(d)
    elif t < 38.15:                                        # I · a carta diz
        hl = [(64, 698, 680, 856)]
        card_full(f, alpha=prog(t, 32.6, 32.9), highlight=hl, hk=prog(t, 33.1, 33.4))
        credit(d)
    elif t < 42.4:                                         # J · parecer
        scene_art(f, t, AW / 2, AH / 2, 1.0)
        stamp_in(f, ST_NOTAVEL, 230, STAGE_Y + 160, t, 38.85)
        d = ImageDraw.Draw(f)
        if t > 40.6:
            label(d, (W / 2 + 120, STAGE_Y + STAGE_H - 90), "salvem sempre duas vezes.")
        paste_center(f, INSETS["admirado"], *INSET_XY, alpha=prog(t, 38.2, 38.5)) if t < 40.5 else None
        credit(d)
    else:                                                  # K · fecho
        k = prog(t, 42.4, 42.75)
        mh = int(STAGE_H * 0.86)
        mw = int(medal.width * mh / medal.height)
        paste_center(f, medal.resize((mw, mh), Image.LANCZOS), W / 2, STAGE_Y + mh / 2 + 6, alpha=k)
        stamp_in(f, ST_PARECER, W / 2 + 230, STAGE_Y + mh - 60, t, 44.14)
        if t > 44.6:
            d.text((W / 2, STAGE_Y + STAGE_H + 40), "Comente o próximo réu", font=F_END, fill=INK, anchor="mm")

    caption(ImageDraw.Draw(f), t)
    ImageDraw.Draw(f).text((W // 2, 1530), "@binderthetrade", font=F_CRED, fill=GREY, anchor="mm")
    return f

# ------------------------------------------------------------------ áudio
STAMPS = [4.7, 38.85, 44.14]

def build_audio(path):
    """Narração + tema do Conde (emenda no compasso) com ducking + carimbos."""
    TEMA = f"{BASE}/audio/tema.mp3"
    CUT_A, CUT_B = 22.09, 4.45           # 20 batidas (~0,882 s) de recuo, no grid de onsets
    XF = 0.25
    parts = [
        f"[1:a]atrim=0:{CUT_A + XF / 2},asetpts=PTS-STARTPTS[ma]",
        f"[1:a]atrim={CUT_B - XF / 2}:30.05,asetpts=PTS-STARTPTS[mb]",
        f"[ma][mb]acrossfade=d={XF}:c1=tri:c2=tri,aresample=48000,aformat=channel_layouts=stereo,volume=-3dB[mus]",
        "[0:a]aresample=48000,aformat=channel_layouts=stereo,apad=pad_dur=3,asplit=2[vox][key]",
        "[mus][key]sidechaincompress=threshold=0.025:ratio=5:attack=25:release=450:makeup=1,"
        "volume='1+min(max((t-44.35)/0.4,0),1)':eval=frame[bed]",
    ]
    for i, s_ in enumerate(STAMPS):
        parts.append(f"aevalsrc='0.9*sin(2*PI*70*t)*exp(-18*t)+0.35*(random(0)-0.5)*exp(-40*t)':d=0.35:s=48000,"
                     f"aformat=channel_layouts=stereo,adelay={int(s_*1000)}|{int(s_*1000)},volume=0.6[st{i}]")
    mix = "".join(f"[st{i}]" for i in range(len(STAMPS)))
    parts.append(f"[vox][bed]{mix}amix=inputs={len(STAMPS)+2}:normalize=0:duration=longest,"
                 f"atrim=0:{DUR},afade=t=out:st={DUR-0.4}:d=0.4,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-i", f"{BASE}/ep002/audio/narracao.wav", "-i", TEMA,
                    "-filter_complex", ";".join(parts), "-map", "[a]", "-ar", "48000", "-ac", "2", path], check=True)

def main():
    args = sys.argv[1:]
    if "--preview" in args:
        ts = [float(x) for x in args[args.index("--preview") + 1].split(",")]
        for t in ts:
            render_frame(t).save(f"{BASE}/prev2/p_{t:05.2f}.png")
        return
    out = args[0] if args and not args[0].startswith("--") else f"{BASE}/Conde_Ep002_OliviaVoldaren_916.mp4"
    build_audio(f"{BASE}/ep002/audio/mix.wav")
    if "--audio-only" in args:
        return
    p = subprocess.Popen(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", f"{BASE}/ep002/audio/mix.wav",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
                         stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    for i in range(n):
        p.stdin.write(render_frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    print(out)

if __name__ == "__main__":
    main()
