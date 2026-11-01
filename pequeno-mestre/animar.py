#!/usr/bin/env python3
"""Pequeno Mestre · animador de recorte (1080x1920, 30 fps).

Uso (a partir da raiz do repositório):
  python3 pequeno-mestre/animar.py pequeno-mestre/ep01 SAIDA.mp4 [--quadros 2.0,30.5,...]

Lê <ep>/falas.json (falas e marcas em segundos da faixa de voz) e <ep>/voz.
Monta três planos (aberto, busto com lip-sync, mesa com as cartas), mistura a
voz com a música M1 (ducking) e normaliza para -14 LUFS / -1 dBTP.
Com --quadros só grava PNG desses instantes (pré-visualização).
"""
import json, math, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
REC = os.path.join(AQUI, "assets", "recortes")
CEN = os.path.join(AQUI, "assets", "cenario")
FONTE = os.path.join(AQUI, "fontes", "Baloo2-800.ttf")
MUSICA = os.path.join(AQUI, "assets", "audio", "M1_aventura_no_gramado.mp3")
W, H, FPS = 1080, 1920, 30
MARROM = (74, 46, 30)
CREME = (250, 240, 220)


# ---------- utilidades ----------
def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def rampa(t, a, d=0.5):
    """0 antes de a, sobe suave até 1 em a+d."""
    return ease((t - a) / d)


def carregar(nome, altura):
    im = Image.open(os.path.join(REC, nome + ".png")).convert("RGBA")
    im = im.crop(im.getbbox())
    w = round(im.width * altura / im.height)
    return im.resize((w, altura), Image.LANCZOS)


def colar(base, spr, cx, base_y, escala=1.0, rot=0.0, alpha=1.0, ancora="base"):
    """Cola spr com o centro horizontal em cx e a base (ou centro) em base_y."""
    if alpha <= 0.001:
        return
    s = spr
    if abs(escala - 1) > 1e-4:
        s = s.resize((max(1, round(s.width * escala)), max(1, round(s.height * escala))), Image.BILINEAR)
    if abs(rot) > 0.01:
        s = s.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 0.999:
        a = s.getchannel("A").point(lambda v: int(v * alpha))
        s = s.copy(); s.putalpha(a)
    x = round(cx - s.width / 2)
    y = round(base_y - s.height) if ancora == "base" else round(base_y - s.height / 2)
    base.alpha_composite(s, (x, y)) if (x >= 0 and y >= 0 and x + s.width <= base.width and y + s.height <= base.height) else _colar_cortado(base, s, x, y)


def _colar_cortado(base, s, x, y):
    camada = Image.new("RGBA", base.size, (0, 0, 0, 0))
    camada.paste(s, (x, y), s)
    base.alpha_composite(camada)


def fonte(px):
    return ImageFont.truetype(FONTE, px)


def legenda(img, texto, y, px=104, alpha=1.0):
    if alpha <= 0.01 or not texto:
        return
    camada = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(camada)
    f = fonte(px)
    linhas = texto.split("\n")
    for i, ln in enumerate(linhas):
        bw = d.textlength(ln, font=f)
        d.text(((W - bw) / 2, y + i * px * 1.05), ln, font=f, fill=(255, 255, 255, 255),
               stroke_width=12, stroke_fill=MARROM + (255,))
    if alpha < 1:
        camada.putalpha(camada.getchannel("A").point(lambda v: int(v * alpha)))
    img.alpha_composite(camada)


# ---------- cenários ----------
def fundo_aberto():
    e1 = Image.open(os.path.join(CEN, "E1_sala.jpg")).convert("RGBA")
    esc = H / e1.height                       # 1920/2304: sem distorção
    e1 = e1.resize((round(e1.width * esc), H), Image.LANCZOS)
    x0 = 400                                   # janela + canto + prateleira
    return e1.crop((x0, 0, x0 + W, H))


def fundo_zoom(caixa, blur):
    e1 = Image.open(os.path.join(CEN, "E1_sala.jpg")).convert("RGBA")
    c = e1.crop(caixa).resize((W, H), Image.LANCZOS)
    return c.filter(ImageFilter.GaussianBlur(blur)) if blur else c


# ---------- cartas (desenho próprio, sem moldura oficial) ----------
def sol(d, cx, cy, r, cor=(255, 214, 90)):
    for k in range(8):
        a = k * math.pi / 4
        d.line([(cx + math.cos(a) * r * 1.25, cy + math.sin(a) * r * 1.25),
                (cx + math.cos(a) * r * 1.7, cy + math.sin(a) * r * 1.7)], fill=cor, width=max(2, r // 4))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=cor)


def carta_base(w, h, titulo):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=26, fill=MARROM)
    d.rounded_rectangle([12, 12, w - 13, h - 13], radius=18, fill=(247, 236, 210))
    f = fonte(int(h * 0.085))
    d.text((26, 18), titulo, font=f, fill=MARROM)
    return im, d


def carta_planicie(w=350, h=490):
    im, d = carta_base(w, h, "PLANÍCIE")
    x0, y0, x1, y1 = 24, int(h * 0.15), w - 24, int(h * 0.62)
    arte = Image.new("RGBA", (x1 - x0, y1 - y0), (190, 225, 240, 255))
    da = ImageDraw.Draw(arte)
    sol(da, int(arte.width * 0.7), int(arte.height * 0.35), int(arte.height * 0.13))
    da.ellipse([-40, int(arte.height * 0.62), int(arte.width * 0.8), arte.height * 1.5], fill=(150, 196, 110))
    da.ellipse([int(arte.width * 0.35), int(arte.height * 0.7), arte.width + 60, arte.height * 1.6], fill=(126, 178, 92))
    im.paste(arte, (x0, y0))
    d.rectangle([x0, y0, x1, y1], outline=MARROM, width=4)
    cx, cy, r = w // 2, int(h * 0.8), int(h * 0.11)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 251, 235), outline=MARROM, width=5)
    sol(d, cx, cy, int(r * 0.42), cor=(236, 184, 60))
    return im


def pip(r, aceso):
    im = Image.new("RGBA", (r * 4, r * 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = r * 2
    if aceso:
        glow = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(glow).ellipse([c - r * 1.7, c - r * 1.7, c + r * 1.7, c + r * 1.7], fill=(255, 236, 150, 170))
        im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(r * 0.45)))
        d.ellipse([c - r, c - r, c + r, c + r], fill=(255, 252, 238), outline=MARROM, width=4)
        sol(d, c, c, int(r * 0.4), cor=(236, 184, 60))
    else:
        d.ellipse([c - r, c - r, c + r, c + r], fill=(205, 198, 186), outline=MARROM, width=4)
        sol(d, c, c, int(r * 0.4), cor=(170, 162, 150))
    return im


def carta_leao(leao, w=400, h=560):
    im, d = carta_base(w, h, "LEÃO")
    x0, y0, x1, y1 = 24, int(h * 0.15), w - 24, int(h * 0.66)
    arte = Image.new("RGBA", (x1 - x0, y1 - y0), (246, 214, 160, 255))
    l = leao.resize((round(leao.width * (arte.height * 0.9) / leao.height), round(arte.height * 0.9)), Image.LANCZOS)
    arte.alpha_composite(l, ((arte.width - l.width) // 2, arte.height - l.height))
    im.paste(arte, (x0, y0), arte)
    d.rectangle([x0, y0, x1, y1], outline=MARROM, width=4)
    f = fonte(int(h * 0.075))
    d.text((30, int(h * 0.71)), "Criatura", font=f, fill=MARROM)
    return im


# ---------- análise da voz ----------
def ler_audio(caminho, sr=48000):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", caminho, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def energia_por_quadro(voz, sr, n_quadros, offset):
    e = np.zeros(n_quadros)
    spf = sr / FPS
    for i in range(n_quadros):
        a = int((i / FPS - offset) * sr)
        if a < 0 or a >= len(voz):
            continue
        seg = voz[a:a + int(spf)]
        e[i] = np.sqrt(np.mean(seg ** 2)) if len(seg) else 0
    ref = np.percentile(e[e > 0], 95) if np.any(e > 0) else 1
    e = e / ref
    sm = e.copy()
    for i in range(1, len(sm)):           # suaviza (ataque rápido, queda lenta)
        sm[i] = max(e[i], sm[i - 1] * 0.55)
    return sm


# ---------- o episódio ----------
class Ep:
    def __init__(self, pasta):
        self.pasta = pasta
        cfg = json.load(open(os.path.join(pasta, "falas.json"), encoding="utf-8"))
        self.cfg = cfg
        self.OFF = cfg["offset_voz"]
        self.m = {k: v + self.OFF for k, v in cfg["marcas"].items()}
        self.falas = [(f["ini"] + self.OFF, f["fim"] + self.OFF, f["texto"]) for f in cfg["falas"]]
        self.fim_voz = self.falas[-1][1]
        self.DUR = self.fim_voz + 4.0
        self.N = int(self.DUR * FPS)

        # recortes
        self.bg_aberto = fundo_aberto()
        self.bg_busto = fundo_zoom((700, 380, 1782, 2304), 7)
        self.bg_mesa = fundo_zoom((700, 1150, 1349, 2304), 5)
        self.a2 = carregar("A2_corpo_inteiro_leao", 980)
        self.p1 = carregar("P1_movel_azulejos", 720)
        self.bocas = {k: carregar(n, 1420) for k, n in
                      [("B1", "B1_base_boca_fechada"), ("B2", "B2_boca_entreaberta"), ("B3", "B3_boca_A"),
                       ("B4", "B4_boca_O"), ("B5", "B5_piscar")]}
        self.a4 = carregar("A4_alegria", 1300)
        self.fila = [("D1_leao_lado", 150), ("D2_trex", 170), ("D3_girafa", 215),
                     ("D4_tigre", 150), ("D5_panda", 150), ("D6_elefante", 140)]
        self.fila = [(carregar(n, h), n) for n, h in self.fila]
        self.leao_frente = carregar("D1b_leao_frente", 360)
        self.dino = carregar("D2_trex", 420)
        self.leao_carta_img = carregar("D1b_leao_frente", 400)
        self.planicie = carta_planicie()
        self.carta_leao = carta_leao(self.leao_carta_img)
        self.pip_on, self.pip_off = pip(30, True), pip(30, False)
        self.orbe = pip(46, True)

        voz = os.path.join(pasta, cfg["voz"])
        self.sr = 48000
        self.voz = ler_audio(voz, self.sr)
        self.energia = energia_por_quadro(self.voz, self.sr, self.N, self.OFF)
        self.palavras_o = []   # intervalos com vogal "o/u" dominante (boca B4)

    # ---- planos ----
    def plano(self, t):
        m = self.m
        cortes = [(0, "aberto"), (self.OFF - 0.05, "busto"), (m["leao"] - 1.2, "mesa"),
                  (m["falta_mana"] + 1.3, "busto"), (m["do_terreno"] - 0.2, "mesa"),
                  (m["regra"] - 0.15, "busto"), (m["proximo_turno"] - 0.4, "mesa"),
                  (m["r1"] - 0.2, "busto"), (m["agora_sabe"] - 0.25, "alegria"),
                  (self.fim_voz + 0.5, "final")]
        atual, ini, ant = cortes[0][1], 0, None
        for i, (tc, nome) in enumerate(cortes):
            if t >= tc:
                ant = cortes[i - 1][1] if i else None
                atual, ini = nome, tc
        return atual, ini, ant

    def quadro(self, i):
        t = i / FPS
        nome, ini, ant = self.plano(t)
        img = self.desenha(nome, t, i)
        x = (t - ini) / 0.3                      # transição: dissolve de 0,3 s
        if ant and x < 1:
            img_ant = self.desenha(ant, t, i)
            img = Image.blend(img_ant, img, ease(x))
        return img

    def desenha(self, nome, t, i):
        return getattr(self, "p_" + nome)(t, i)

    def respira(self, t, amp=0.015):
        return 1 + amp * math.sin(2 * math.pi * t / 3.0)

    # plano aberto: o armário (P1, provisório), o menino e a fila
    def cena_aberta(self, t, fila_t0, entrada=True):
        img = self.bg_aberto.copy()
        colar(img, self.p1, 760, 1185)
        colar(img, self.a2, 300, 1640, escala=self.respira(t))
        x = 40
        pos = []
        for spr, _ in self.fila:
            pos.append(x + spr.width / 2); x += spr.width + 14
        desloc = (W - (x - 14 - 40)) / 2 - 40
        for k, (spr, _) in enumerate(self.fila):
            alvo = pos[k] + desloc
            if entrada:
                p = ease((t - fila_t0 - k * 0.38) / 0.55)
                if p <= 0:
                    continue
                cx = alvo + (1 - p) * 260
                hop = math.sin(min(1, p) * math.pi) * 40
            else:
                cx, hop = alvo, 0
            colar(img, spr, cx, 1800 - hop)
        return img

    def p_aberto(self, t, i):
        return self.cena_aberta(t, 0.2)

    def boca(self, i, t):
        e = self.energia[i] if i < len(self.energia) else 0
        piscar = (int(t * FPS) % int(3.4 * FPS)) < 3
        if e < 0.12:
            return "B5" if piscar else "B1"
        if e < 0.38:
            return "B2"
        return "B4" if (i // 4) % 5 == 2 else "B3"

    def p_busto(self, t, i):
        img = self.bg_busto.copy()
        b = self.bocas[self.boca(i, t)]
        colar(img, b, W / 2, H + 10, escala=1 + 0.008 * math.sin(2 * math.pi * t / 3.0))
        m = self.m
        if m["falta_mana"] < t < m["do_terreno"]:
            legenda(img, "MANA É\nENERGIA", 230, alpha=rampa(t, m["falta_mana"] + 2.3, 0.4))
        if m["regra"] - 0.5 < t < m["proximo_turno"]:
            legenda(img, "REGRA É\nREGRA", 230, alpha=rampa(t, m["regra"], 0.3))
        if t >= m["r1"] - 0.3:
            linhas = [(m["r1"], "TERRENO DÁ MANA"), (m["r2"], "VIRA PARA USAR"), (m["r3"], "UM POR TURNO")]
            for k, (tm, tx) in enumerate(linhas):
                legenda(img, tx, 170 + k * 112, px=92, alpha=rampa(t, tm, 0.35))
        return img

    def p_alegria(self, t, i):
        img = self.bg_busto.copy()
        ta = t - (self.m["agora_sabe"] - 0.25)
        rot = 2.5 * math.sin(2 * math.pi * 1.4 * ta) * min(1, ta / 0.6)
        colar(img, self.a4, W / 2, H + 20, rot=rot, escala=1 + 0.01 * math.sin(2 * math.pi * ta / 1.5))
        legenda(img, "ENSINA\nALGUÉM", 230, alpha=rampa(t, self.m["agora_sabe"] + 1.3, 0.4))
        return img

    def p_final(self, t, i):
        img = self.cena_aberta(t, 0, entrada=False)
        tf = t - (self.fim_voz + 0.5)
        a = rampa(tf, 0.2, 0.6)
        veu = Image.new("RGBA", img.size, (250, 240, 220, int(120 * a)))
        img.alpha_composite(veu)
        legenda(img, "Pequeno Mestre", 300, px=128, alpha=a)
        legenda(img, "BINDER Originals", 460, px=64, alpha=a)
        return img

    # plano da mesa: cartas e bichos, sem o menino (ele fala fora de quadro)
    def p_mesa(self, t, i):
        m = self.m
        img = self.bg_mesa.copy()
        # carta do leão + pips de custo
        lc_x, lc_y = 660, 1020
        entrada_leao = m["pronto"]
        sobe = rampa(t, entrada_leao, 0.8)
        lcx = lc_x + (540 - lc_x) * sobe
        lcy = lc_y + (1170 - lc_y) * sobe
        esc = 1 + 0.2 * sobe
        carta = self.carta_leao.copy()
        acesos = self.mana_paga(t)
        for k in range(2):
            p = self.pip_on if k < acesos else self.pip_off
            carta.alpha_composite(p, (carta.width - 140 + k * 72 - p.width // 2 + 24, 44 - p.height // 2 + 24))
        colar(img, carta, lcx, lcy, escala=esc)
        # leão de brinquedo
        hop = 0
        for tm in (m["leao"], m["pode_entrar"], m["pode_entrar"] + 0.5):
            hop = max(hop, math.sin(min(1, max(0, (t - tm) / 0.45)) * math.pi) * 60 if 0 <= t - tm <= 0.45 else 0)
        triste = rampa(t, m["nao_da"], 0.4) * (1 - rampa(t, m["do_terreno"] + 1, 0.5))
        escala_l = 1 - 0.06 * triste
        lx = 220 + (-90) * sobe
        colar(img, self.leao_frente, lx, 1110 - hop + 20 * triste, escala=escala_l)
        # terrenos
        for k, (cx, t_in) in enumerate([(290, m["do_terreno"] + 0.1), (790, m["joga_mais"])]):
            p = rampa(t, t_in, 0.6)
            if p <= 0:
                continue
            y = 1520 + (1 - p) * 800
            rot = -90 * self.virado(k, t)
            colar(img, self.planicie, cx, y, rot=rot, ancora="centro")
        # dinossauro com o segundo terreno (L7)
        if m["outro_terreno"] - 0.3 < t < m["regra"]:
            ent = rampa(t, m["outro_terreno"] - 0.3, 0.7) * (1 - rampa(t, m["nao_dino"] + 0.3, 0.8))
            dx = 1400 - 520 * ent
            colar(img, self.planicie, dx - 220, 1560, escala=0.75, rot=8, ancora="centro")
            colar(img, self.dino, dx, 1880)
        # orbes de mana
        for (t0, origem, pipk) in self.orbes():
            u = (t - t0) / 0.9
            if 0 <= u <= 1:
                x0, y0 = origem
                x1 = lcx + (self.carta_leao.width / 2 - 140 + pipk * 72 + 24) * esc
                y1 = lcy - self.carta_leao.height * esc + 68 * esc
                e = ease(u)
                x = x0 + (x1 - x0) * e
                y = y0 + (y1 - y0) * e - math.sin(e * math.pi) * 160
                colar(img, self.orbe, x, y, escala=1 - 0.3 * e, ancora="centro", alpha=min(1, u * 4))
        # luz do turno seguinte (escurece e volta, sem flash)
        d = math.sin(math.pi * min(1, max(0, (t - m["proximo_turno"]) / 1.2))) if t > m["proximo_turno"] else 0
        if d > 0:
            img.alpha_composite(Image.new("RGBA", img.size, (30, 20, 40, int(110 * d))))
        # legendas
        L = [("leao", "nao_da", None), ("falta_mana", "falta_mana_fim", "FALTA\nMANA"),
             ("do_terreno", "terreno_da_mana", "TERRENO"), ("terreno_da_mana", "vira", "TERRENO\nDÁ MANA"),
             ("vira", "uma_mana", "VIRA!"), ("uma_nao_chega", "outro_terreno", "UMA NÃO\nCHEGA"),
             ("um_por_turno", "regra", "UM POR\nTURNO"), ("proximo_turno", "desvira", "PRÓXIMO\nTURNO"),
             ("duas", "pronto", "DUAS!"), ("pode_entrar", "r1", "PODE\nENTRAR!")]
        mm = dict(m); mm["falta_mana_fim"] = m["falta_mana"] + 1.4
        for a, b, tx in L:
            if tx and mm[a] <= t < mm[b]:
                legenda(img, tx, 200, alpha=rampa(t, mm[a], 0.3))
        return img

    def virado(self, k, t):
        m = self.m
        if k == 0:
            return rampa(t, m["vira"], 0.6) * (1 - rampa(t, m["desvira"], 0.6)) + rampa(t, m["vira_os_dois"], 0.6)
        return rampa(t, m["vira_os_dois"], 0.6)

    def orbes(self):
        m = self.m
        return [(m["sai_mana"], (290, 1520), 0), (m["uma"], (290, 1520), 0), (m["duas"], (790, 1520), 1)]

    def mana_paga(self, t):
        m = self.m
        n = 0
        if m["sai_mana"] + 0.9 <= t < m["proximo_turno"] + 0.6:
            n = 1
        if t >= m["uma"] + 0.9:
            n = 1
        if t >= m["duas"] + 0.9:
            n = 2
        return n

    # ---------- som ----------
    def mixar(self, saida_wav):
        sr = self.sr
        n = int(self.DUR * sr)
        voz = np.zeros(n, np.float32)
        a = int(self.OFF * sr)
        v = self.voz[: max(0, n - a)]
        voz[a:a + len(v)] = v
        mus = ler_audio(MUSICA, sr)
        p1 = mus[int(3 * sr): int(45 * sr)]
        p2 = mus[int(85 * sr): int(120 * sr)]
        xf = int(2 * sr)
        r = np.linspace(0, 1, xf, dtype=np.float32)
        bed = np.concatenate([p1[:-xf], p1[-xf:] * (1 - r) + p2[:xf] * r, p2[xf:]])
        bed = bed[:n] if len(bed) >= n else np.pad(bed, (0, n - len(bed)))
        # envolvente da voz -> ducking
        env = np.abs(voz)
        k = int(0.08 * sr)
        env = np.convolve(env, np.ones(k) / k, mode="same")
        ativo = (env > 0.01).astype(np.float32)
        k2 = int(0.4 * sr)
        ativo = np.convolve(ativo, np.ones(k2) / k2, mode="same")
        ganho_db = -11 - 7 * np.clip(ativo * 2, 0, 1)
        bed = bed * (10 ** (ganho_db / 20)).astype(np.float32)
        fade = np.ones(n, np.float32)
        fade[: sr] = np.linspace(0, 1, sr)
        fl = int(1.5 * sr)
        fade[-fl:] = np.linspace(1, 0, fl)
        # plim suave quando a mana aparece
        sfx = np.zeros(n, np.float32)
        tt = np.arange(int(0.7 * sr)) / sr
        plim = (0.5 * np.sin(2 * np.pi * 1046.5 * tt) + 0.3 * np.sin(2 * np.pi * 1568 * tt)) * np.exp(-tt * 6) * 0.12
        for t0, _, _ in self.orbes():
            s = int((t0 + 0.85) * sr)
            sfx[s:s + len(plim)] += plim[: max(0, n - s)].astype(np.float32)
        mix = voz + bed * fade + sfx
        tmp = saida_wav + ".raw.wav"
        self._grava_wav(tmp, mix, sr)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af",
                        "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "2", saida_wav], check=True)
        os.remove(tmp)

    @staticmethod
    def _grava_wav(caminho, x, sr):
        import wave
        x = np.clip(x, -1, 1)
        with wave.open(caminho, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
            w.writeframes((x * 32767).astype("<i2").tobytes())


def main():
    pasta, saida = sys.argv[1], sys.argv[2]
    ep = Ep(pasta)
    if "--quadros" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--quadros") + 1].split(",")]
        for t in ts:
            ep.quadro(int(t * FPS)).convert("RGB").save(f"{saida}_{t:05.1f}.png")
        return
    with tempfile.TemporaryDirectory() as td:
        wav = os.path.join(td, "mix.wav")
        ep.mixar(wav)
        proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                                 "-r", str(FPS), "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "veryfast",
                                 "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest",
                                 "-movflags", "+faststart", saida], stdin=subprocess.PIPE)
        for i in range(ep.N):
            proc.stdin.write(ep.quadro(i).convert("RGB").tobytes())
            if i % 300 == 0:
                print(f"{i}/{ep.N}", flush=True)
        proc.stdin.close(); proc.wait()
    print("ok", saida)


if __name__ == "__main__":
    main()
