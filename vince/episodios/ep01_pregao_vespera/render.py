#!/usr/bin/env python3
"""VV-EP01 «O Pregão de Véspera» v2 — render (Vince Vault / Multiverse Capital, direção 2D).

Ritmo da bíblia (`vince/CONTEXTO.md` §3 e §7): imagens paradas, um corte a cada 3–6 s.
Movimento permitido e só este: empurrão de 2 % no 1.º quadro de cada pose nova; contador do
painel a chegar ao valor final uma vez por episódio. (Piscar: as poses do kit não têm olhos
fechados; não se usou.) Tudo o resto é corte.
Planos por função: conjunto (discurso), próximo (reação), painel (dados), carta
(identificação), telefone (conflito). A carta é a imagem oficial, inteira, sem nada por cima.

Uso: python3 render.py --kit <vince/kit/v1> --assets <pasta> --saida mudo.mp4 [--fotos 1.0,5.0]
"""
import argparse, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
CX = 470                      # centro da zona segura (140 px à direita ficam para a interface do Instagram)

CREME = (240, 230, 205)
CINZA = (205, 198, 178)
PRETO = (14, 14, 12)
BRANCO = (246, 244, 236)

FONT_B = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
FONT_XB = "/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf"
FONT_M = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
_fc = {}
def font(p, s):
    if (p, s) not in _fc:
        _fc[(p, s)] = ImageFont.truetype(p, s)
    return _fc[(p, s)]

def ease_out(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3

# ------------------------------------------------------------------ dados (ficha de factos)
CONSULTA = "12/11/2026, 17h30 (Lisboa)"
TAXA = 5.58                   # dólar comercial, fecho de 10/11/2026 (Metrópoles)

def _fmt(v):
    return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
def brl(v): return "R$ " + _fmt(v * TAXA)
def usd(v): return "US$ " + _fmt(v)

# ------------------------------------------------------------------ voz existente (voz.mp3, 1 geração de 12/11)
# (inicio_na_voz, fim_na_voz, inicio_no_video, texto) — só frases sustentadas pelos dados
FRASES = [
    (0.08, 1.83, 0.05, "Trezentos dólares!"),
    (10.67, 12.48, 3.80, "Trezentos dólares, meu amigo."),
    (12.68, 14.01, 7.55, "É o pregão do século!"),
    (14.37, 15.06, 9.58, "Buy the d—"),
    (15.59, 16.01, 11.30, "Fala."),
    (16.66, 17.60, 12.40, "Quantas vendas?"),
    (21.40, 23.38, 21.30, "O preço de mercado é essa venda."),
    (23.78, 25.57, 25.80, "E o anúncio mais barato hoje?"),
    (28.01, 29.47, 33.00, "Pré-venda não é mercado."),
    (33.34, 35.46, 36.70, "Quer saber quanto vale a sua pasta?"),
    (35.81, 37.60, 39.00, "Escaneia no BINDER Vision."),
]
TOQUE = 10.30                 # o telefone toca e corta o "Buy the d—" (a bateria da faixa pára aqui)
DUR = 40.90

# ------------------------------------------------------------------ kit
class Kit:
    def __init__(self, kit, assets):
        kit, assets = Path(kit), Path(assets)
        self.base = Image.open(kit / "cenario_916.png").convert("RGB")
        self.base_sem_tel = Image.open(assets / "cenario_sem_telefone.png").convert("RGB")
        self.pose = {n: Image.open(kit / f"vince_pose_{n}.png").convert("RGBA") for n in
                     ["pitch", "aponta", "testa", "confidencia", "bracos", "pega_telefone", "ao_telefone"]}
        self.tel_fora = Image.open(kit / "prop_telefone_fora.png").convert("RGBA")
        self.carta = Image.open(assets / "spock535.png").convert("RGBA")
        self.mesa_y = 1381

K = None
PAINEL = (178, 300, 902, 700)   # interior do quadro, medido no cenário

def painel(img, linhas):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = PAINEL
    med = []
    for txt, sz, cor, f in linhas:
        ff = font(f, sz)
        med.append((d.textbbox((0, 0), txt, font=ff), ff))
    esp = 14
    total = sum(bb[3] - bb[1] for bb, _ in med) + esp * (len(linhas) - 1)
    y = (y0 + y1) / 2 - total / 2
    for (txt, sz, cor, f), (bb, ff) in zip(linhas, med):
        d.text(((x0 + x1) / 2 - (bb[2] - bb[0]) / 2 - bb[0], y - bb[1]), txt, font=ff, fill=cor)
        y += bb[3] - bb[1] + esp

ESC = 1.25
BASE_Y = 1440

def cena(t_local, pose, linhas=None, telefone=True, tel_fora=False, cx=540, zoom=1.0, foco=(540, 960)):
    fundo = K.base if telefone and not tel_fora else K.base_sem_tel
    base = fundo.copy()
    if linhas:
        painel(base, linhas)
    tf = None
    if tel_fora:
        tf = K.tel_fora.resize((int(K.tel_fora.width * 0.31), int(K.tel_fora.height * 0.31)), Image.LANCZOS)
        base.paste(tf, (110, 1422 - tf.height), tf)
    if pose:
        p = K.pose[pose]
        s = ESC * (1 + 0.02 * (1 - ease_out(t_local / (4 / FPS))))   # empurrão de 2 % no 1.º quadro
        pr = p.resize((int(p.width * s), int(p.height * s)), Image.LANCZOS)
        base.paste(pr, (int(cx - pr.width / 2), int(BASE_Y - pr.height)), pr)
    base.paste(fundo.crop((0, K.mesa_y, W, H)), (0, K.mesa_y))
    if tf is not None:
        c = tf.crop((0, tf.height - 40, tf.width, tf.height))
        base.paste(c, (110, 1422 - 40), c)
    if zoom != 1.0:
        fx, fy = foco; cw, ch = W / zoom, H / zoom
        x0 = min(max(fx - cw / 2, 0), W - cw); y0 = min(max(fy - ch / 2, 0), H - ch)
        base = base.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.LANCZOS)
    return base

def _linha(d, txt, f, y, cor):
    bb = d.textbbox((0, 0), txt, font=f)
    d.text((CX - (bb[2] - bb[0]) / 2 - bb[0], y), txt, font=f, fill=cor)

def carta(t_local):
    img = Image.new("RGB", (W, H), (22, 24, 22))
    c = K.carta
    s = 1.02 * (1 + 0.02 * (1 - ease_out(t_local / (4 / FPS))))
    cr = c.resize((int(c.width * s), int(c.height * s)), Image.LANCZOS)
    img.paste(cr, (CX - cr.width // 2, 300), cr)
    d = ImageDraw.Draw(img)
    _linha(d, "Mr. Spock, Science Officer · Star Trek #535", font(FONT_XB, 40), 1388, CREME)
    _linha(d, "Mítica · Showcase · Surge Foil · arte de Grant Griffin", font(FONT_M, 30), 1440, CINZA)
    _linha(d, "Imagem: Scryfall · © Wizards of the Coast · Star Trek © CBS", font(FONT_M, 26), 1484, (165, 160, 146))
    return img

def legenda(img, t, y=1400, carta_no_ecra=False):
    for a, b, t0, txt in FRASES:
        if t0 - 0.02 <= t < t0 + (b - a) + 0.30:
            d = ImageDraw.Draw(img)
            f = font(FONT_B, 54)
            txt = txt.upper()
            bb = d.textbbox((0, 0), txt, font=f); w = bb[2] - bb[0]
            if w > 860:
                f = font(FONT_B, int(54 * 860 / w)); bb = d.textbbox((0, 0), txt, font=f); w = bb[2] - bb[0]
            yy = 228 if carta_no_ecra else y      # na carta, a legenda vai para cima dela, nunca por cima
            x = CX - w / 2 - bb[0]
            for ox, oy in ((-3, 0), (3, 0), (0, -3), (0, 3), (3, 3), (-3, -3)):
                d.text((x + ox, yy + oy), txt, font=f, fill=PRETO)
            d.text((x, yy), txt, font=f, fill=BRANCO)
            break
    return img

# ------------------------------------------------------------------ painéis
F_PEQ = 30

def p_gancho(l):
    v = 299.98 * ease_out(l / 0.8)           # o contador: uma única vez no episódio
    return [(usd(v), 104, CREME, FONT_B), ("≈ " + brl(v), 64, CREME, FONT_B),
            ("preço de mercado · TCGplayer (EUA)", F_PEQ, CINZA, FONT_M), (CONSULTA, F_PEQ, CINZA, FONT_M)]

P_MERCADO = [("PREÇO DE MERCADO", 46, CREME, FONT_B), (usd(299.98) + " = ÚLTIMA VENDA", 50, CREME, FONT_B),
             ("TCGplayer: vendas insuficientes", F_PEQ + 2, CREME, FONT_XB), ("para medir a volatilidade", F_PEQ + 2, CREME, FONT_XB),
             ("TCGplayer · " + CONSULTA, F_PEQ - 4, CINZA, FONT_M)]

P_ANUNCIO = [("MENOR ANÚNCIO", 46, CREME, FONT_B), (usd(154.99), 92, CREME, FONT_B), ("≈ " + brl(154.99), 54, CREME, FONT_B),
             ("MyTCGValue · " + CONSULTA, F_PEQ - 4, CINZA, FONT_M),
             ("anúncio é pedido, não venda · TCGplayer: US$ 159,98", F_PEQ - 6, CINZA, FONT_M)]

P_CONCLUSAO = [("TEM A CARTA?", 50, CREME, FONT_B), ("US$ 299,98 é a última venda,", 40, CREME, FONT_XB),
               ("não uma oferta.", 40, CREME, FONT_XB), ("NÃO TEM?", 50, CREME, FONT_B),
               ("O preço ainda não se formou.", 40, CREME, FONT_XB)]

P_CTA = [("QUANTO VALE", 78, CREME, FONT_B), ("A SUA PASTA?", 78, CREME, FONT_B)]

R_BRL = f"conversão: dólar comercial de 10/11/2026, R$ {TAXA:.2f}".replace(".", ",")

def com_rodape(img, txt, y=1300):
    d = ImageDraw.Draw(img)
    f = font(FONT_M, 30)
    bb = d.textbbox((0, 0), txt, font=f); w = bb[2] - bb[0]
    x = CX - w / 2
    d.rectangle((x - 16, y - 10, x + w + 16, y + 44), fill=(20, 22, 20))
    d.text((x - bb[0], y - bb[1]), txt, font=f, fill=CREME)
    return img

# ------------------------------------------------------------------ planos (3–6 s cada)
PANEL_Z, PANEL_F = 1.25, (596, 640)    # painel centrado em x=470 no ecrã, borda direita a 922 px (< 940)
PLANOS = [
    (0.00, 3.40, lambda t, l: com_rodape(cena(l, "aponta", p_gancho(l), cx=640, zoom=PANEL_Z, foco=PANEL_F), R_BRL)),  # painel · impacto
    (3.40, 7.30, lambda t, l: carta(l)),                                                                                # carta · identificação
    (7.30, 10.30, lambda t, l: cena(l, "pitch", p_gancho(9))),                                                          # conjunto · discurso
    (10.30, 14.00, lambda t, l: cena(l, "pega_telefone", telefone=False, cx=500, zoom=1.10, foco=(500, 1080))),        # telefone · conflito
    (14.00, 17.60, lambda t, l: cena(l, "ao_telefone", tel_fora=True, zoom=1.38, foco=(540, 1040))),                   # próximo · a resposta
    (17.60, 21.00, lambda t, l: cena(l, "testa", zoom=1.32, foco=(540, 1060))),                                        # próximo · reação
    (21.00, 25.50, lambda t, l: cena(l, "aponta", P_MERCADO, cx=640, zoom=PANEL_Z, foco=PANEL_F)),                     # painel · o dado
    (25.50, 29.00, lambda t, l: cena(l, "bracos", zoom=1.12, foco=(540, 1040))),                                       # conjunto · objeção
    (29.00, 32.80, lambda t, l: com_rodape(cena(l, "aponta", P_ANUNCIO, cx=640, zoom=PANEL_Z, foco=PANEL_F), R_BRL)),  # painel · o dado
    (32.80, 36.50, lambda t, l: cena(l, "confidencia", P_CONCLUSAO, zoom=1.22, foco=(597, 780))),                     # conjunto · conclusão
    (36.50, DUR, lambda t, l: cena(l, "aponta", P_CTA, cx=640)),                                                       # conjunto · ponte para o app
]
CARTA = 1

def quadro(t):
    for i, (a, b, fn) in enumerate(PLANOS):
        if a <= t < b:
            return legenda(fn(t, t - a), t, carta_no_ecra=(i == CARTA))
    return Image.new("RGB", (W, H), PRETO)

def main():
    global K
    ap = argparse.ArgumentParser()
    ap.add_argument("--kit", required=True); ap.add_argument("--assets", required=True)
    ap.add_argument("--saida", required=True); ap.add_argument("--fotos")
    a = ap.parse_args()
    K = Kit(a.kit, a.assets)
    if a.fotos:
        for s in a.fotos.split(","):
            quadro(float(s)).save(f"{a.saida}_{s}.png")
        return
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                           "-pix_fmt", "yuv420p", a.saida], stdin=subprocess.PIPE)
    for n in range(int(round(DUR * FPS))):
        ff.stdin.write(quadro(n / FPS).tobytes())
    ff.stdin.close(); ff.wait()

if __name__ == "__main__":
    main()
