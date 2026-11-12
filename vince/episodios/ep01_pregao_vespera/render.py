#!/usr/bin/env python3
"""VV-EP01 «O Pregão de Véspera» — render do vídeo (Multiverse Capital / Vince Vault).

Composição por camadas a partir do kit 2D (vince/kit/v1), cortes na batida da faixa,
placas de tipografia, legenda palavra a palavra e boca sincronizada nos grandes planos.
Saída: quadros 1080x1920 a 30 fps enviados ao ffmpeg (vídeo mudo); o áudio é misturado
por mistura.py.

Uso: python3 render.py --kit <vince/kit/v1> --assets <pasta> --saida video.mp4 [--so 0-40]
"""
import argparse, json, math, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
CX = 470          # centro da zona segura (140 px à direita reservados à interface do Instagram)
LARG_UTIL = 820
DUR = 40.0

# --- paleta (bíblia §3 e EDICAO.md §3.5) ---
CREME = (240, 230, 205)
PRETO = (14, 14, 12)
VERM = (178, 38, 34)
PAREDE = (137, 142, 128)
BRANCO = (246, 244, 236)
TINTA = (24, 26, 24)

FONT_B = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
FONT_XB = "/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf"
FONT_M = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
_fc = {}
def font(path, size):
    k = (path, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]

def ease_out(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3

# ---------------------------------------------------------------- dados do guião
# Frases da voz (segmentos medidos em voz.mp3) e onde entram no vídeo.
# (inicio_na_voz, fim_na_voz, inicio_no_video, texto)
FRASES = [
    (0.08, 1.83, 0.05, "Trezentos dólares!"),
    (2.21, 5.68, 1.90, "Num Spock de Star Trek que nem saiu da caixa."),
    (5.94, 7.43, 5.55, "Primeiro lugar do ranking!"),
    (7.69, 10.21, 7.25, "E a carta só chega nas lojas dia treze."),
    (10.67, 12.48, 10.40, "Trezentos dólares, meu amigo."),
    (12.68, 14.01, 12.45, "É o pregão do século!"),
    (14.37, 15.06, 15.55, "Buy the d—"),
    (15.59, 16.01, 17.25, "Fala."),
    (16.66, 17.60, 18.25, "Quantas vendas?"),
    (18.16, 18.58, 20.15, "Uma?"),
    (19.24, 20.13, 21.75, "Uma venda."),
    (20.46, 20.90, 22.95, "Uma."),
    (21.40, 23.38, 23.90, "O preço de mercado é essa venda."),
    (23.78, 25.57, 26.20, "E o anúncio mais barato hoje?"),
    (26.04, 27.45, 28.30, "Cento e sessenta."),
    (28.01, 29.47, 30.20, "Pré-venda não é mercado."),
    (29.92, 32.76, 31.95, "O preço de verdade nasce quando a carta chega."),
    (33.34, 35.46, 35.20, "Quer saber quanto vale a sua pasta?"),
    (35.81, 37.60, 37.60, "Escaneia no BINDER Vision."),
]

def _sil(w):
    w = w.lower()
    return max(1, sum(1 for i, c in enumerate(w) if c in "aeiouáéíóúâêôãõà" and (i == 0 or w[i-1] not in "aeiouáéíóúâêôãõà")))

def palavras_temporizadas():
    out = []
    for fi, (a, b, t0, txt) in enumerate(FRASES):
        ws = txt.split()
        pes = [_sil(w) for w in ws]
        tot = sum(pes); dur = b - a; t = t0
        for w, p in zip(ws, pes):
            d = dur * p / tot
            out.append((t, t + d, w, fi))
            t += d
    return out

PALAVRAS = palavras_temporizadas()

# ---------------------------------------------------------------- assets
class Kit:
    def __init__(self, kit, assets):
        kit, assets = Path(kit), Path(assets)
        self.base = Image.open(kit / "cenario_916.png").convert("RGB")
        self.base_sem_tel = Image.open(assets / "cenario_sem_telefone.png").convert("RGB")
        self.pose = {n: Image.open(kit / f"vince_pose_{n}.png").convert("RGBA") for n in
                     ["pitch", "aponta", "choque", "bracos", "testa", "confidencia", "dinheiro", "pega_telefone", "ao_telefone"]}
        self.cabeca = {n: Image.open(kit / f"vince_{n}.png").convert("RGBA") for n in
                       ["cabeca_neutra", "boca_a", "boca_o", "olhos_fechados", "olhos_lado"]}
        self.tel_fora = Image.open(kit / "prop_telefone_fora.png").convert("RGBA")
        self.carta = Image.open(assets / "spock535.png").convert("RGBA")
        self.logo = Image.open(Path(__file__).resolve().parents[3] / "manaburn" / "logo" / "logo_mark.png").convert("RGBA")
        # frente da mesa (tapa a base do tronco); recortada do cenário
        self.mesa_y = 1381
        self.desk = self.base.crop((0, self.mesa_y, W, H))
        self.desk_sem_tel = self.base_sem_tel.crop((0, self.mesa_y, W, H))
        self.env = np.load(assets / "env_voz.npy")  # envelope RMS da voz no relógio do vídeo, 100 Hz

K = None

# ---------------------------------------------------------------- painel (quadro da parede)
PAINEL = (178, 300, 902, 700)  # área interior do quadro, medida no cenário

def desenha_painel(img, linhas):
    """linhas: lista de (texto, tamanho, cor, peso). Centrado no painel."""
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = PAINEL
    alturas = []
    for txt, sz, cor, peso in linhas:
        f = font(FONT_B if peso == "b" else FONT_M, sz)
        bb = d.textbbox((0, 0), txt, font=f)
        alturas.append((bb, f))
    total = sum(bb[3] - bb[1] for bb, _ in alturas) + 18 * (len(linhas) - 1)
    y = (y0 + y1) / 2 - total / 2
    for (txt, sz, cor, peso), (bb, f) in zip(linhas, alturas):
        w = bb[2] - bb[0]
        d.text(((x0 + x1) / 2 - w / 2 - bb[0], y - bb[1]), txt, font=f, fill=cor)
        y += bb[3] - bb[1] + 18

# ---------------------------------------------------------------- personagem
ESC_POSE = 1.25
BASE_Y = 1440  # base do recorte (escondida pela mesa)

def cola_pose(img, nome, t_local, cx=540, escala=ESC_POSE):
    p = K.pose[nome]
    # entrada: 3 % maior, assenta em 120 ms; respiração contínua 1,000–1,012 em 2,4 s
    entrada = 1 + 0.03 * (1 - ease_out(t_local / 0.12))
    resp = 1 + 0.006 * (1 - math.cos(2 * math.pi * t_local / 2.4))
    s = escala * entrada
    w = int(p.width * s); h = int(p.height * s * resp)
    pr = p.resize((w, h), Image.LANCZOS)
    img.paste(pr, (int(cx - w / 2), int(BASE_Y - h)), pr)

def cena(t_local, pose, painel=None, telefone=True, zoom=1.0, foco=(540, 1000), cx=540, tel_fora=False):
    base = (K.base if telefone and not tel_fora else K.base_sem_tel).copy()
    if painel:
        desenha_painel(base, painel)
    if tel_fora:
        tf = K.tel_fora.resize((int(K.tel_fora.width * 0.31), int(K.tel_fora.height * 0.31)), Image.LANCZOS)
        base.paste(tf, (110, 1422 - tf.height), tf)
    if pose:
        cola_pose(base, pose, t_local, cx=cx)
    base.paste(K.desk if (telefone and not tel_fora) else K.desk_sem_tel, (0, K.mesa_y))
    if tel_fora:
        tf = K.tel_fora.resize((int(K.tel_fora.width * 0.31), int(K.tel_fora.height * 0.31)), Image.LANCZOS)
        # a base do telefone fica à frente da linha da mesa
        corte = tf.crop((0, tf.height - 40, tf.width, tf.height))
        base.paste(corte, (110, 1422 - 40), corte)
    # deriva lenta de câmara (1–2 % ao longo do plano)
    z = zoom * (1 + 0.012 * min(t_local / 6.0, 1.0))
    return enquadra(base, z, foco)

def enquadra(img, z, foco):
    if abs(z - 1) < 1e-3:
        return img
    fx, fy = foco
    cw, ch = W / z, H / z
    x0 = min(max(fx - cw / 2, 0), W - cw); y0 = min(max(fy - ch / 2, 0), H - ch)
    return img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.LANCZOS)

def env_em(t):
    i = int(t * 100)
    return float(K.env[i]) if 0 <= i < len(K.env) else 0.0

def boca(t):
    e = env_em(t)
    if e > 0.55: return "boca_a"
    if e > 0.18: return "boca_o"
    return "cabeca_neutra"

def grande_plano(t, t_local, olhar_lado=False):
    """Cabeça a falar, com boca sincronizada ao envelope da voz e piscar."""
    fundo = enquadra(K.base_sem_tel, 1.7, (540, 820))
    peca = boca(t)
    if olhar_lado and peca == "cabeca_neutra":
        peca = "olhos_lado"
    # piscar de 2 quadros a cada ~4,6 s (relógio global)
    if (t % 4.6) < 2 / FPS and peca == "cabeca_neutra":
        peca = "olhos_fechados"
    c = K.cabeca[peca]
    entrada = 1 + 0.03 * (1 - ease_out(t_local / 0.12))
    resp = 1 + 0.006 * (1 - math.cos(2 * math.pi * t_local / 2.4))
    s = 2.05 * entrada * (1 + 0.012 * min(t_local / 6, 1))
    w, h = int(c.width * s), int(c.height * s * resp)
    cr = c.resize((w, h), Image.LANCZOS)
    fundo.paste(cr, (540 - w // 2, 1560 - h + int(0.04 * h)), cr)
    return fundo

# ---------------------------------------------------------------- placas de tipografia
def texto_centrado(d, txt, f, y, cor, cx=CX):
    bb = d.textbbox((0, 0), txt, font=f)
    d.text((cx - (bb[2] - bb[0]) / 2 - bb[0], y - bb[1]), txt, font=f, fill=cor)
    return bb[3] - bb[1]

def cabe(txt, path, alvo_w, max_sz):
    sz = max_sz
    while sz > 40:
        f = font(path, sz)
        bb = f.getbbox(txt)
        if bb[2] - bb[0] <= alvo_w:
            return f
        sz -= 6
    return font(path, sz)

def placa(t_local, fundo, linhas, rodape=None, cor_rodape=None, entra=True):
    """linhas: [(texto, altura_max_px, cor)] — a primeira é a palavra-chave."""
    img = Image.new("RGB", (W, H), fundo)
    camada = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    fs = [cabe(txt, FONT_B, LARG_UTIL, sz) for txt, sz, _ in linhas]
    alts = [d.textbbox((0, 0), txt, font=f)[3] - d.textbbox((0, 0), txt, font=f)[1] for (txt, _, _), f in zip(linhas, fs)]
    total = sum(alts) + 34 * (len(linhas) - 1)
    y = 880 - total / 2
    for (txt, _, cor), f, a in zip(linhas, fs, alts):
        texto_centrado(d, txt, f, y, cor)
        y += a + 34
    if entra:
        # desfoque direcional à entrada (3 quadros) e assentamento
        k = 1 - ease_out(t_local / 0.12)
        if k > 0.02:
            dx = int(90 * k)
            camada = camada.transform(camada.size, Image.AFFINE, (1, 0, -dx, 0, 1, 0))
            camada = camada.filter(ImageFilter.BoxBlur(int(1 + 26 * k)))
    img.paste(camada, (0, 0), camada)
    if rodape:
        d2 = ImageDraw.Draw(img)
        f = font(FONT_M, 28)
        yy = 1290
        for r in rodape:
            texto_centrado(d2, r, f, yy, cor_rodape or (190, 185, 170))
            yy += 44
    return img

def placa_carta(t_local):
    img = Image.new("RGB", (W, H), PRETO)
    c = K.carta
    s = 1.02 * (1 + 0.03 * (1 - ease_out(t_local / 0.12))) * (1 + 0.015 * min(t_local / 2, 1))
    cr = c.resize((int(c.width * s), int(c.height * s)), Image.LANCZOS)
    img.paste(cr, (CX - cr.width // 2, 780 - cr.height // 2), cr)
    d = ImageDraw.Draw(img)
    texto_centrado(d, "Mr. Spock, Science Officer · TRK #535", font(FONT_XB, 40), 1345, CREME)
    texto_centrado(d, "Showcase · Surge Foil · arte: Grant Griffin", font(FONT_M, 30), 1400, (190, 185, 170))
    texto_centrado(d, "Imagem: Scryfall · © Wizards of the Coast · © CBS", font(FONT_M, 26), 1446, (150, 146, 134))
    return img

def placa_cta(t_local):
    img = Image.new("RGB", (W, H), (5, 10, 16))
    lg = K.logo
    s = 0.62 * (1 + 0.03 * (1 - ease_out(t_local / 0.12))) * (1 + 0.02 * min(t_local / 2.4, 1))
    lr = lg.resize((int(lg.width * s), int(lg.height * s)), Image.LANCZOS)
    img.paste(lr, (CX - lr.width // 2, 560 - lr.height // 2), lr)
    d = ImageDraw.Draw(img)
    texto_centrado(d, "QUANTO VALE", font(FONT_B, 110), 930, CREME)
    texto_centrado(d, "A SUA PASTA?", font(FONT_B, 110), 1060, CREME)
    texto_centrado(d, "Escaneie no BINDER Vision", font(FONT_XB, 50), 1230, (16, 185, 129))
    return img

# ---------------------------------------------------------------- legenda palavra a palavra
def legenda(img, t, y=1390):
    passadas = [i for i, p in enumerate(PALAVRAS) if p[0] - 0.02 <= t]
    if not passadas:
        return img
    idx = max(passadas)
    fi = PALAVRAS[idx][3]
    da_frase = [i for i, p in enumerate(PALAVRAS) if p[3] == fi]
    pos = idx - da_frase[0]
    ini = da_frase[0] + pos - (pos % 3)
    g2 = [PALAVRAS[i] for i in range(ini, min(ini + 3, da_frase[-1] + 1))]
    if t > g2[-1][1] + 0.25:
        return img
    d = ImageDraw.Draw(img)
    f = font(FONT_B, 64)
    txts = [p[2].upper() for p in g2]
    larg = [d.textbbox((0, 0), w, font=f)[2] for w in txts]
    esp = 22
    tot = sum(larg) + esp * (len(txts) - 1)
    x = CX - tot / 2
    for (a, b, w, _), tw, lw in zip(g2, txts, larg):
        ativo = a - 0.02 <= t < b + 0.05
        if ativo:
            d.rectangle((x - 10, y - 8, x + lw + 10, y + 74), fill=CREME)
            d.text((x, y), tw, font=f, fill=PRETO)
        else:
            for ox, oy in ((-3, 0), (3, 0), (0, -3), (0, 3)):
                d.text((x + ox, y + oy), tw, font=f, fill=PRETO)
            d.text((x, y), tw, font=f, fill=BRANCO)
        x += lw + esp
    return img

# ---------------------------------------------------------------- linha de fonte pequena em cena
def etiqueta(img, linhas, y=760):
    d = ImageDraw.Draw(img)
    f = font(FONT_M, 28)
    for i, l in enumerate(linhas):
        bb = d.textbbox((0, 0), l, font=f)
        w = bb[2] - bb[0]
        x = 540 - w / 2
        d.rectangle((x - 14, y + i * 44 - 6, x + w + 14, y + i * 44 + 36), fill=(20, 22, 20))
        d.text((x, y + i * 44), l, font=f, fill=CREME)
    return img

FONTE_MERC = "TCGplayer · preço de mercado · 12/11/2026"
ESTIM = "estimativa, não oferta de compra"

def painel_preco(valor):
    return [("US$ " + valor, 120, CREME, "b"), (FONTE_MERC, 26, (205, 198, 178), "m"), (ESTIM, 26, (205, 198, 178), "m")]

def conta(t_local, alvo=299.98, dur=0.8):
    v = alvo * ease_out(t_local / dur)
    return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ---------------------------------------------------------------- lista de planos
# (inicio, fim, função(t, t_local), legenda?)
def P(a, b, fn, leg=True):
    return (a, b, fn, leg)

RANK = [("1º  SPOCK #535   US$ 299,98", 44, CREME, "b"), ("2º  PICARD #497   US$ 297,99", 40, (205, 198, 178), "b"),
        ("3º  KIRK #542   US$ 168,99", 40, (205, 198, 178), "b"), ("TCGIndex (preços TCGplayer) · 12/11/2026", 24, (190, 185, 170), "m"),
        (ESTIM, 24, (190, 185, 170), "m")]

PLANOS = [
    P(0.00, 1.71, lambda t, l: cena(l, "aponta", painel=painel_preco(conta(l)), cx=600, zoom=1.15, foco=(540, 900))),
    P(1.71, 3.42, lambda t, l: placa_carta(l), leg=False),
    P(3.42, 4.28, lambda t, l: placa(l, PRETO, [("NEM SAIU", 300, CREME), ("DA CAIXA", 150, CREME)]), leg=False),
    P(4.28, 5.55, lambda t, l: cena(l, "pitch", painel=painel_preco("299,98"), zoom=1.0)),
    P(5.55, 7.25, lambda t, l: placa(l, CREME, [("1º", 620, PRETO), ("NO RANKING", 120, PRETO)],
                                     rodape=["TCGIndex · preços TCGplayer · 12/11/2026"], cor_rodape=(90, 86, 76)), leg=False),
    P(7.25, 8.96, lambda t, l: cena(l, "aponta", painel=RANK, cx=640, zoom=1.12, foco=(540, 850))),
    P(8.96, 10.24, lambda t, l: placa(l, PRETO, [("13/11", 420, CREME), ("CHEGA ÀS LOJAS", 96, CREME)],
                                      rodape=["Lançamento: Wizards of the Coast"]), leg=False),
    P(10.24, 11.10, lambda t, l: grande_plano(t, l)),
    P(11.10, 12.40, lambda t, l: cena(l, "dinheiro", painel=painel_preco("299,98"), zoom=1.08, foco=(540, 1050))),
    P(12.40, 13.80, lambda t, l: placa(l, PRETO, [("PREGÃO", 260, CREME), ("DO SÉCULO", 170, CREME)]), leg=False),
    P(13.80, 14.65, lambda t, l: cena(l, "pitch", painel=painel_preco("299,98"), zoom=1.05)),
    P(14.65, 15.50, lambda t, l: cena(l, "dinheiro", painel=painel_preco("299,98"), zoom=1.12, foco=(540, 1000))),
    P(15.50, 16.28, lambda t, l: placa(l, CREME, [("BUY THE D—", 260, PRETO)]), leg=False),
    # a bateria pára: o telefone toca
    P(16.28, 16.90, lambda t, l: cena(l, "choque", zoom=1.0)),
    P(16.90, 18.21, lambda t, l: cena(l, "pega_telefone", telefone=False, cx=500, zoom=1.04)),
    P(18.21, 19.90, lambda t, l: cena(l, "ao_telefone", tel_fora=True, zoom=1.22, foco=(540, 1080))),
    P(19.90, 20.70, lambda t, l: placa(l, PRETO, [("QUANTAS", 220, CREME), ("VENDAS?", 220, CREME)]), leg=False),
    P(20.70, 21.60, lambda t, l: cena(l, "ao_telefone", tel_fora=True, zoom=1.45, foco=(540, 1020))),
    P(21.60, 23.40, lambda t, l: placa(l, VERM, [("1", 760, CREME), ("VENDA", 200, CREME)],
                                      rodape=["TCGplayer, 12/11/2026: venda mais baixa", "= venda mais alta = US$ 299,98"], cor_rodape=(245, 215, 205)), leg=False),
    P(23.40, 24.30, lambda t, l: cena(l, "testa", zoom=1.06)),
    P(24.30, 26.00, lambda t, l: cena(l, "aponta", painel=[("PREÇO DE MERCADO", 64, CREME, "b"), ("US$ 299,98", 100, CREME, "b"),
                                                          ("= 1 VENDA", 64, CREME, "b"), (FONTE_MERC, 24, (205, 198, 178), "m")],
                                     cx=640, zoom=1.12, foco=(540, 850))),
    P(26.00, 27.30, lambda t, l: grande_plano(t, l, olhar_lado=True)),
    P(27.30, 28.20, lambda t, l: cena(l, "bracos", zoom=1.1, foco=(540, 1060))),
    P(28.20, 30.00, lambda t, l: placa(l, PRETO, [("ANÚNCIO MAIS BARATO", 92, CREME), ("US$ 159,98", 210, CREME),
                                                  ("≈ R$ 893", 110, CREME)],
                                      rodape=["TCGplayer · 12/11/2026 · " + ESTIM, "conversão: dólar comercial de 10/11 (R$ 5,58)"]), leg=False),
    P(30.00, 31.00, lambda t, l: cena(l, "confidencia", zoom=1.08, foco=(540, 1060))),
    P(31.00, 32.40, lambda t, l: placa(l, CREME, [("PRÉ-VENDA", 230, PRETO), ("≠ MERCADO", 210, PRETO)]), leg=False),
    P(32.40, 33.60, lambda t, l: grande_plano(t, l)),
    P(33.60, 34.90, lambda t, l: cena(l, "confidencia", zoom=1.0)),
    P(34.90, 36.40, lambda t, l: cena(l, "aponta", painel=[("QUANTO VALE", 90, CREME, "b"), ("A SUA PASTA?", 90, CREME, "b")], cx=640, zoom=1.1, foco=(540, 850))),
    P(36.40, 37.50, lambda t, l: grande_plano(t, l)),
    P(37.50, 40.00, lambda t, l: placa_cta(l), leg=False),
]

# etiquetas de fonte em planos de cena que mostram números no painel já estão no painel.

def quadro(t):
    for a, b, fn, leg in PLANOS:
        if a <= t < b:
            img = fn(t, t - a)
            if leg:
                img = legenda(img, t)
            return img
    return Image.new("RGB", (W, H), PRETO)

def main():
    global K
    ap = argparse.ArgumentParser()
    ap.add_argument("--kit", required=True); ap.add_argument("--assets", required=True)
    ap.add_argument("--saida", required=True); ap.add_argument("--so", default=None)
    ap.add_argument("--fotos", default=None, help="só exporta PNG destes tempos, separados por vírgula")
    a = ap.parse_args()
    K = Kit(a.kit, a.assets)
    if a.fotos:
        for s in a.fotos.split(","):
            quadro(float(s)).save(f"{a.saida}_{s}.png")
        return
    t0, t1 = (0.0, DUR) if not a.so else map(float, a.so.split("-"))
    n0, n1 = int(round(t0 * FPS)), int(round(t1 * FPS))
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                           "-pix_fmt", "yuv420p", a.saida], stdin=subprocess.PIPE)
    for n in range(n0, n1):
        ff.stdin.write(quadro(n / FPS).tobytes())
        if n % 150 == 0:
            print(f"{n / FPS:5.1f}s", file=sys.stderr, flush=True)
    ff.stdin.close(); ff.wait()

if __name__ == "__main__":
    main()
