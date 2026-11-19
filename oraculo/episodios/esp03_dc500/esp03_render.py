# Meta em Curto ESP03 · O mais jogado é o que mais vence? (Duel Commander 500) · render
# Derivado de oraculo/esp01/esp01_render.py (TUBO, terminal, grelha 2×2) e ep08b_render.py. O TUBO não é regenerado.
#
# Uso (a partir desta pasta):
#   python3 -I esp03_render.py <raiz do repo> previa        -> ESP03_PREVIA_TECNICA.mp4 (sem voz; trilha + SFX + fecho)
#   python3 -I esp03_render.py <raiz do repo> stills 0.5 2 ... -> still_XX.XX.png
#   python3 -I esp03_render.py <raiz do repo> capa          -> ESP03_CAPA.png + ESP03_CAPA_grelha.png
#
# Dados: dados/episodio.json (gerado à mão a partir de dados/resultado.md). Campo vazio ou ausente = marcador
# «[x]» no ecrã e marca de água «PRÉVIA TÉCNICA · SEM DADOS». Nenhum número é inventado: sem valor não há barra.
# Versão final (com voz): os tempos de BEAT passam a vir de words.json, como no ESP01; a ordem dos planos não muda.
import os, json, math, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
K = (sys.argv[1] if len(sys.argv) > 1 else '../../..').rstrip('/') + '/'
MODO = sys.argv[2] if len(sys.argv) > 2 else 'previa'
W, H, FPS = 1080, 1920, 30

# ---------- dados ----------
DJ = HERE + 'dados/episodio.json'
D = json.load(open(DJ, encoding='utf-8')) if os.path.exists(DJ) else {}
def v(k, fall=None):
    x = D.get(k)
    return x if x not in (None, '') else (fall if fall is not None else f'[{k}]')
SEM_DADOS = not D.get('confirmado', False)
IND = v('indicador', 'WIN RATE')           # «WIN RATE» ou «CONVERSÃO TOP 4», nunca os dois
DEN = v('denominador', 'partidas')         # «partidas» (win rate) ou «listas» (conversão)
VEREDITO = v('veredito', '[veredito]'); VER_OK = D.get('veredito_cor', 'verde') == 'verde'
FONTE = f"Dados: Duel Commander 500 (Farpas de Mana) · {v('per')}"
def frac(k):                               # valor numérico 0–1 só se existir
    x = D.get(k); return float(x) if isinstance(x, (int, float)) else None

# ---------- estilo (ESP01) ----------
_fc = {}
def F(p, s):
    if (p, s) not in _fc: _fc[(p, s)] = ImageFont.truetype(p, s)
    return _fc[(p, s)]
DJV = '/usr/share/fonts/truetype/dejavu/'
MONO, MONOB, COND = DJV + 'DejaVuSansMono.ttf', DJV + 'DejaVuSansMono-Bold.ttf', DJV + 'DejaVuSansCondensed.ttf'
INTB = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
if not os.path.exists(INTB): INTB = '/usr/share/fonts/opentype/inter/Inter-Black.otf'
BG = (5, 10, 16); EM = (16, 185, 129); PH = (0, 255, 65); WHITE = (236, 241, 245); GREY = (120, 140, 150); AMBER = (255, 176, 32)
SCR = (492, 566, 740, 792); SCX, SCY = (SCR[0] + SCR[2]) / 2, (SCR[1] + SCR[3]) / 2
EYES = [(518, 615, 596, 702), (634, 615, 709, 702)]; LED = (592, 828)
GLY = '0123456789ABCDEF#*+=<>/:'
rng = np.random.default_rng(503)
def ease(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)
def eio(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3
def typed(s, t0, t, cps=40): return s[:int(max(0, t - t0) * cps)]
def fit(d, s, path, size, maxw):
    while size > 20:
        if d.textlength(s, font=F(path, size)) <= maxw: return F(path, size)
        size -= 2
    return F(path, size)
def mix_bg(col, a): return tuple(int(BG[i] + (col[i] - BG[i]) * a / 255) for i in range(3))

# ---------- tempos (storyboard.md; na versão final vêm das palavras da voz) ----------
BEAT = dict(SCAN=0.30, B=1.00, Q=1.20, RISE=3.00, DIVE=3.40, IN_A=4.20, IN_B=8.00, HL_B=10.0,
            OUT1=12.0, OUT2=14.2, PAY=16.0, ASK=20.0, CLOSE=23.0, END=26.5)
VO = [  # (início, fim, texto) — legenda terminal da prévia = locução do cenário 1 (roteiro.md)
    (0.3, 1.0, 'O COMANDANTE MAIS JOGADO…'), (1.0, 3.0, '…NÃO É O QUE MAIS VENCE.'),
    (3.4, 5.6, f"{v('A')}: {v('nA')} LISTAS."), (5.6, 8.0, f"{v('qA')} DO META. {IND}: {v('iA')}."),
    (8.0, 10.0, f"{v('B')} APARECE BEM MENOS."), (10.0, 12.0, f"MAS VENCE {v('iB')}… EM {v('dB')} {DEN.upper()}."),
    (12.0, 14.2, 'POPULARIDADE MEDE QUEM ESCOLHE.'), (14.2, 16.0, f'{IND} MEDE QUEM GANHA.'),
    (16.6, 20.0, 'COM ESSA AMOSTRA, A DIFERENÇA AGUENTA.'),
    (20.0, 23.0, 'QUAL COMANDANTE VOCÊ ACHA QUE SÓ PARECE FORTE?'), (23.0, 26.5, 'PROBABILIDADE CALCULADA. HUMANOS, IMPREVISÍVEIS.')]

# ---------- TUBO (imagem-mestra, sem alterações) ----------
MASTER = Image.open(K + 'oraculo/assets/tubo_mestra_916.png').convert('RGB')
rain = [dict(x=x, y=rng.uniform(0, 300), v=rng.uniform(40, 90)) for x in range(500, 736, 14)]
def tubo_frame(t, expr='analitico', zoom=1.0, tela=None):
    im = MASTER.copy(); d = ImageDraw.Draw(im, 'RGBA'); fs = F(MONO, 13)
    if tela is None:
        for c in rain:
            y = SCR[1] + ((c['y'] + t * c['v']) % (SCR[3] - SCR[1] + 40)) - 20
            for k in range(5):
                yy = y - k * 15
                if SCR[1] + 8 < yy < SCR[3] - 14 and not any(e[0] - 6 < c['x'] < e[2] + 6 and e[1] - 8 < yy < e[3] + 4 for e in EYES):
                    d.text((c['x'], yy), GLY[int(t * 8 + k + c['x']) % len(GLY)], font=fs, fill=(0, 255, 65, int(150 * (1 - k / 5) * (0.6 if expr != 'desconfiado' else 0.2))))
    lid = 0.0; bt = t % 4.3
    if bt < 0.14: lid = math.sin(bt / 0.14 * math.pi)
    if expr == 'desconfiado': lid = max(lid, 0.45)
    if expr == 'confiante': lid = max(lid, 0.22)
    if lid > 0.01 and tela is None:
        for i, e in enumerate(EYES):
            h = (e[3] - e[1] + 4) * lid
            if expr == 'desconfiado' and i == 0: h *= 0.55
            if expr == 'confiante' and lid < 0.5 and i == 1: h *= 0.4
            d.rectangle((e[0] - 3, e[1] - 3, e[2] + 3, e[1] - 3 + h), fill=BG + (255,))
            d.line((e[0] - 3, e[1] - 3 + h, e[2] + 3, e[1] - 3 + h), fill=(16, 185, 129, 160), width=3)
    if tela:                                   # texto no ecrã do TUBO (substitui olhos e chuva)
        d.rounded_rectangle(SCR, 18, fill=(4, 14, 10, 240))
        for i, (s, sz, col) in enumerate(tela):
            d.text((SCX, SCY - 30 * (len(tela) - 1) + i * 60), s, font=fit(d, s, MONOB, sz, SCR[2] - SCR[0] - 30), fill=col, anchor='mm')
    d.ellipse((LED[0] - 6, LED[1] - 6, LED[0] + 6, LED[1] + 6), fill=(60, 200, 140, 200))
    z = zoom * (1 + 0.008 * (1 + math.sin(t * 1.3)) / 2)
    if abs(z - 1) > 1e-4:
        cw, ch = W / z, H / z; x0 = min(max(SCX - cw / 2, 0), W - cw); y0 = min(max(SCY - ch / 2, 0), H - ch)
        im = im.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
    return im

# ---------- terminal ----------
TERM_BG = Image.new('RGB', (W, H), BG)
SCANL = Image.new('RGBA', (W, H), (0, 0, 0, 0)); _d = ImageDraw.Draw(SCANL)
for y in range(0, H, 4): _d.line((0, y, W, y), fill=(0, 0, 0, 60))
VIG = Image.new('L', (W, H), 0); ImageDraw.Draw(VIG).ellipse((-300, -200, W + 300, H + 200), fill=255); VIG = VIG.filter(ImageFilter.GaussianBlur(220))
tcols = [dict(x=x, y=rng.uniform(0, H), v=rng.uniform(60, 160)) for x in range(30, W, 46)]
EGG = D.get('easter_egg')                    # ex.: {"txt": "...", "t0": 5.0, "t1": 11.0}; registar em comum/easter_eggs.md
def term_base(t, alpha=30):
    im = TERM_BG.copy(); d = ImageDraw.Draw(im, 'RGBA'); fs = F(MONO, 24)
    for c in tcols:
        y = (c['y'] + t * c['v']) % (H + 200) - 100
        for k in range(9): d.text((c['x'], y - k * 30), GLY[int(t * 6 + k * 3 + c['x']) % len(GLY)], font=fs, fill=mix_bg(PH, alpha * (1 - k / 9)))
    if EGG and EGG['t0'] <= t < EGG['t1']:
        for k, ch in enumerate(EGG['txt']): d.text((tcols[22]['x'], 1250 + k * 30), ch, font=fs, fill=mix_bg(PH, 90))
    return im, d
def term_finish(im):
    im = Image.composite(im, Image.new('RGB', (W, H), (0, 0, 0)), VIG); im.paste(SCANL, (0, 0), SCANL); return im
def hud(d):
    d.ellipse((80, 1676, 100, 1696), fill=EM + (220,)); d.text((114, 1686), 'BINDER', font=F(MONOB, 28), fill=EM + (220,), anchor='lm')
    d.text((W - 80, 1686), 'META EM CURTO · ESPECIAL', font=F(MONO, 26), fill=(150, 170, 175, 220), anchor='rm')
def fontes(d, linhas, y=1384):
    for i, s in enumerate(linhas): d.text((80, y + i * 44), s, font=fit(d, s, COND, 34, W - 160), fill=(150, 170, 175, 235))
def marca(d):
    if SEM_DADOS:
        s = 'PRÉVIA TÉCNICA · SEM DADOS · NÃO PUBLICAR'
        d.rounded_rectangle((W / 2 - 330, 22, W / 2 + 330, 70), 10, fill=(40, 28, 4, 230), outline=AMBER, width=2)
        d.text((W / 2, 46), s, font=F(MONOB, 26), fill=AMBER, anchor='mm')
def subs(im, t, y=1560):
    d = ImageDraw.Draw(im, 'RGBA')
    for a, b, s in VO:
        if a <= t < b:
            f = fit(d, s, MONOB, 46, W - 160); wd = d.textlength(s, font=f)
            if wd > W - 160: break
            d.rounded_rectangle((W / 2 - wd / 2 - 24, y - 48, W / 2 + wd / 2 + 24, y + 26), 12, fill=(5, 10, 16, 210))
            d.text((W / 2, y), typed(s, a, t, 60), font=f, fill=PH, anchor='ms'); break
    return im

# ---------- cartas (Scryfall, inteiras; marcador se ainda não há comandante) ----------
def carta(lado):
    p = D.get(f'carta_{lado}')
    if p and os.path.exists(HERE + p): c = Image.open(HERE + p).convert('RGB')
    else:
        c = Image.new('RGB', (488, 680), (14, 22, 30)); d = ImageDraw.Draw(c)
        d.rounded_rectangle((8, 8, 480, 672), 22, outline=(60, 80, 90), width=4)
        d.text((244, 300), f'CARTA {lado}', font=F(MONOB, 48), fill=GREY, anchor='mm')
        d.text((244, 370), 'Scryfall · inteira', font=F(MONO, 28), fill=(80, 100, 110), anchor='mm')
    m = Image.new('L', c.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, c.size[0] - 1, c.size[1] - 1), 24, fill=255)
    c = c.convert('RGBA'); c.putalpha(m); return c
CARD = {'A': carta('A'), 'B': carta('B')}
_cc = {}
def card_img(lado, w, dim=0.0):
    key = (lado, int(w), round(dim, 2))
    if key not in _cc:
        c = CARD[lado]; r = c.resize((int(w), int(w * c.height / c.width)), Image.LANCZOS)
        if dim > 0:
            a = r.getchannel('A'); r = Image.blend(r, Image.new('RGBA', r.size, BG + (255,)), dim); r.putalpha(a)
        if len(_cc) > 300: _cc.clear()
        _cc[key] = r
    return _cc[key]
def glow_box(im, box, col=PH, r=26):
    g = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).rounded_rectangle(box, r, outline=col + (255,), width=16)
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(14))); ImageDraw.Draw(im).rounded_rectangle(box, r, outline=col + (255,), width=6)

# ---------- gancho: grelha dupla (carta A · número A / número B · carta B) ----------
GW, GH = 440, 613
GRID = [(80, 250), (560, 250), (80, 900), (560, 900)]       # A, nº A, nº B, B
ROW = [(30, 92), (285, 92), (555, 92), (810, 92)]; RW = 240
def tile_num(w, h, big, small, small2, col, dim):
    im = Image.new('RGBA', (int(w), int(h)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 24, fill=(8, 16, 20, 245), outline=col, width=4)
    d.text((w / 2, h * 0.40), big, font=fit(d, big, INTB, int(w * 0.30), w - 40), fill=col, anchor='mm')
    d.text((w / 2, h * 0.62), small, font=fit(d, small, MONOB, int(w * 0.085), w - 40), fill=WHITE, anchor='mm')
    d.text((w / 2, h * 0.74), small2, font=fit(d, small2, MONO, int(w * 0.064), w - 40), fill=GREY, anchor='mm')
    if dim:
        a = im.getchannel('A'); im = Image.blend(im, Image.new('RGBA', im.size, BG + (255,)), dim); im.putalpha(a)
    return im
def hook(t):
    km = eio((t - BEAT['RISE']) / 0.4) if t >= BEAT['RISE'] else 0.0
    base = tubo_frame(t, 'desconfiado', tela=[(str(v('nA')), 70, PH), ('LISTAS', 26, EM)] if t >= BEAT['RISE'] + .2 else None).convert('RGBA')
    shade = Image.new('RGBA', base.size, (3, 6, 10, int(225 * (1 - km)))); im = base.copy(); im.alpha_composite(shade)
    d = ImageDraw.Draw(im, 'RGBA'); a = int(255 * max(0, 1 - km * 2.5))
    if a and t < BEAT['Q']:
        d.text((W / 2, 130), f"DUEL COMMANDER 500 · {v('per')}", font=fit(d, f"DUEL COMMANDER 500 · {v('per')}", MONOB, 44, W - 120), fill=(200, 215, 220, a), anchor='mm')
        d.text((W / 2, 192), FONTE, font=fit(d, FONTE, COND, 30, W - 120), fill=(150, 170, 175, a), anchor='mm')
    focoB = t >= BEAT['B']
    for i in range(4):
        ks = eio((t - 0.05 * i + 0.07) / 0.22)
        if ks <= 0: continue
        gx, gy = GRID[i]; rx, ry = ROW[i]; w = GW + (RW - GW) * km; x = gx + (rx - gx) * km; y = gy + (ry - gy) * km
        sc = 1.04 - 0.04 * ks; w2 = w * sc; x -= (w2 - w) / 2; y -= (w2 - w) * 0.7
        ladoA = i in (0, 1); dim = 0.6 if (focoB and ladoA and km < 1) else 0.0
        if i in (0, 3): c = card_img('A' if i == 0 else 'B', w2, dim)
        elif i == 1: c = tile_num(w2, w2 * GH / GW, str(v('nA')), 'LISTAS', f"{v('qA')} do meta", WHITE, dim)
        else: c = tile_num(w2, w2 * GH / GW, str(v('iB')), IND, f"em {v('dB')} {DEN}", PH, 0)
        im.alpha_composite(c, (int(x), int(y)))
        if km < 0.3 and ((not focoB and ladoA and t >= BEAT['SCAN'] + .3) or (focoB and not ladoA)):
            glow_box(im, (int(x), int(y), int(x + c.width), int(y + c.height)))
        if i == 0 and BEAT['SCAN'] <= t < BEAT['SCAN'] + .5:      # scan verde sobre a carta A
            sy = y + c.height * (t - BEAT['SCAN']) / .5; ImageDraw.Draw(im, 'RGBA').rectangle((x, sy - 4, x + c.width, sy + 4), fill=PH + (200,))
    d = ImageDraw.Draw(im, 'RGBA')
    if t >= BEAT['Q'] and km < 0.6:                # pergunta no topo: não tapa nenhuma carta
        q1, q2 = 'O MAIS JOGADO É', 'O QUE MAIS VENCE?'; f = F(INTB, 72); a = int(255 * (1 - km / 0.6)); n = int((t - BEAT['Q']) * 45)
        d.text((W / 2, 110), q1[:n], font=f, fill=WHITE + (a,), anchor='mm'); d.text((W / 2, 192), q2[:max(0, n - len(q1))], font=f, fill=PH + (a,), anchor='mm')
        d.text((W / 2, 1560), FONTE, font=fit(d, FONTE, COND, 30, W - 120), fill=(150, 170, 175, a), anchor='mm')
    marca(d); out = im.convert('RGB')
    if t >= BEAT['DIVE']:                       # mergulho no ecrã do TUBO
        z = 1 + 9 * ease((t - BEAT['DIVE']) / (BEAT['IN_A'] - BEAT['DIVE']))
        cw, ch = W / z, H / z; x0 = min(max(SCX - cw / 2, 0), W - cw); y0 = min(max(SCY - ch / 2, 0), H - ch); out = out.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
    return out

# ---------- dentro: provas ----------
BX0, BX1 = 120, 960                            # eixo único 0–100 %
def eixo(d, y0, y1):
    d.line((BX0, y1, BX1, y1), fill=GREY + (200,), width=2)
    for p in (0, 25, 50, 75, 100):
        x = BX0 + (BX1 - BX0) * p / 100; d.line((x, y0, x, y1), fill=(40, 60, 70, 255), width=1)
        d.text((x, y1 + 14), f'{p}%', font=F(MONO, 28), fill=GREY, anchor='ma')
def barra(d, y, val, txt, col, t0, t, ic=None, banda_t=None):
    if t < t0: return
    if val is None:                            # sem dado: contorno tracejado, sem comprimento inventado
        for x in range(BX0, BX1, 28): d.line((x, y, min(x + 14, BX1), y), fill=GREY, width=3); d.line((x, y + 70, min(x + 14, BX1), y + 70), fill=GREY, width=3)
        d.text((BX0 + 20, y + 35), txt, font=F(MONOB, 34), fill=GREY, anchor='lm'); return
    k = eio((t - t0) / 0.6); xe = BX0 + (BX1 - BX0) * val * k
    d.rectangle((BX0, y, xe, y + 70), fill=col + (255,)); d.text((min(xe + 16, BX1 - 200), y + 35), txt, font=F(MONOB, 34), fill=WHITE, anchor='lm')
    if ic and banda_t is not None and t >= banda_t:
        kb = eio((t - banda_t) / 0.8); a0, a1 = ic; xa = BX0 + (BX1 - BX0) * a0; xb = BX0 + (BX1 - BX0) * (a0 + (a1 - a0) * kb)
        d.rectangle((xa, y - 14, xb, y + 84), outline=WHITE + (230,), width=3)
def cabecalho(d, t, t0, s1, s2):
    d.text((80, 200), typed(s1, t0, t), font=fit(d, s1, MONOB, 38, 920), fill=PH)
    d.text((80, 256), typed(s2, t0 + .25, t), font=fit(d, s2, MONO, 28, 920), fill=EM); d.line((80, 310, 1000, 310), fill=(16, 185, 129, 90), width=2)
def scene_prova(t):
    im, d = term_base(t); im = im.convert('RGBA'); d = ImageDraw.Draw(im, 'RGBA')
    cabecalho(d, t, BEAT['IN_A'] - .1, '> DUEL COMMANDER 500 · POPULARIDADE × ' + IND, f"  {v('per')} · filtros: {v('filtros')}")
    if t >= BEAT['IN_A'] + .2:
        c = card_img('A', 300, 0.0 if t < BEAT['IN_B'] else 0.45); im.alpha_composite(c, (80, 360))
        d.text((410, 380), str(v('A')), font=fit(d, str(v('A')), MONOB, 40, 590), fill=WHITE)
        d.text((410, 440), f"{v('nA')} listas · {v('qA')} do meta", font=fit(d, f"{v('nA')} listas · {v('qA')} do meta", MONO, 34, 590), fill=EM)
        d.text((410, 494), f"{IND.lower()} {v('iA')} em {v('dA')} {DEN}", font=fit(d, f"{IND.lower()} {v('iA')} em {v('dA')} {DEN}", MONO, 34, 590), fill=EM)
    if t >= BEAT['IN_B'] + .2:
        c = card_img('B', 300); im.alpha_composite(c, (W - 380, 790))
        for i, s in enumerate((str(v('B')), f"{v('nB')} listas · {v('qB')} do meta", f"{IND.lower()} {v('iB')} em {v('dB')} {DEN}")):
            d.text((W - 410, 810 + i * 56), s, font=fit(d, s, MONOB if i == 0 else MONO, 40 if i == 0 else 34, 560), fill=WHITE if i == 0 else (PH if t >= BEAT['HL_B'] else EM), anchor='ra')
    y0 = 1150; eixo(d, y0 - 20, y0 + 190)
    barra(d, y0, frac('iA_v'), f"{v('A')} · {v('iA')}", (70, 110, 120), BEAT['IN_A'] + .8, t)
    barra(d, y0 + 100, frac('iB_v'), f"{v('B')} · {v('iB')}", EM if t < BEAT['HL_B'] else PH, BEAT['IN_B'] + .4, t)
    fontes(d, [FONTE, f"{IND.lower()} e listas tal como publicados no portal · extraído em {v('extraido')}"], 1430)
    hud(d); marca(d); return term_finish(im.convert('RGB'))
def scene_pagamento(t):
    im, d = term_base(t, 18); im = im.convert('RGBA'); d = ImageDraw.Draw(im, 'RGBA')
    cabecalho(d, t, BEAT['PAY'], '> A DIFERENÇA É REAL OU É AMOSTRA?', '  intervalo de 95 % · cálculo do BINDER sobre os dados do portal')
    y0 = 560; eixo(d, y0 - 20, y0 + 220)
    icA, icB = D.get('icA'), D.get('icB')
    barra(d, y0, frac('iA_v'), f"{v('A')} · {v('iA')}", (70, 110, 120), BEAT['PAY'], t, icA, BEAT['PAY'] + .8)
    barra(d, y0 + 120, frac('iB_v'), f"{v('B')} · {v('iB')}", PH, BEAT['PAY'], t, icB, BEAT['PAY'] + .8)
    if t >= BEAT['PAY'] + 1.8:
        k = eio((t - BEAT['PAY'] - 1.8) / .2); col = PH if VER_OK else AMBER; f = fit(d, VEREDITO, INTB, int(76 * (1.25 - .25 * k)), 900)
        wd = d.textlength(VEREDITO, font=f) + 70
        d.rounded_rectangle((W / 2 - wd / 2, 980, W / 2 + wd / 2, 1120), 18, outline=col, width=5, fill=(8, 20, 16, 240))
        d.text((W / 2, 1050), VEREDITO, font=f, fill=col, anchor='mm')
    fontes(d, [FONTE, 'faixa = intervalo de Wilson a 95 % (cálculo do BINDER)'], 1384)
    hud(d); marca(d); return term_finish(im.convert('RGB'))

# ---------- fora: TUBO ----------
def fora(t):
    if t < BEAT['OUT2']: im = tubo_frame(t, 'analitico', zoom=1 + 0.25 * (1 - eio((t - BEAT['OUT1']) / .6)))
    elif t < BEAT['PAY']: im = tubo_frame(t, 'desconfiado', tela=[('ESCOLHE', 48, WHITE), ('≠ GANHA', 48, PH)])
    elif t < BEAT['CLOSE']:
        im = tubo_frame(t, 'confiante', zoom=1 + 0.04 * ease((t - BEAT['ASK']) / 3))
        d = ImageDraw.Draw(im, 'RGBA'); q1, q2 = 'QUAL COMANDANTE', 'SÓ PARECE FORTE?'
        d.text((W / 2, 300), q1, font=F(INTB, 72), fill=WHITE, anchor='mm'); d.text((W / 2, 390), q2, font=F(INTB, 72), fill=PH, anchor='mm')
    else: im = tubo_frame(t, 'analitico')
    d = ImageDraw.Draw(im, 'RGBA'); marca(d); return im

def frame(t):
    if t < BEAT['IN_A']: im = hook(t)
    elif t < BEAT['OUT1']: im = scene_prova(t)
    elif t < BEAT['PAY']: im = fora(t)
    elif t < BEAT['ASK']: im = scene_pagamento(t)
    else: im = fora(t)
    if t >= 0.3: im = subs(im.convert('RGBA'), t, 1650 if t < BEAT['RISE'] else 1560).convert('RGB')
    return im

# ---------- áudio da prévia: trilha do TUBO + SFX do ESP01 (sem voz) ----------
def audio_previa(out='mix_previa.wav'):
    SR = 48000; N = int(BEAT['END'] * SR)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', K + 'oraculo/musica/tubo_tema.mp3', '-t', str(BEAT['END']), '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    M = np.zeros(N, np.float32); m = np.frombuffer(raw, np.float32)[:N]; M[:len(m)] = m
    t = np.arange(N) / SR; c = np.ones(N); j0, j1 = int(BEAT['PAY'] * SR), int((BEAT['PAY'] + .6) * SR); c[j0:j1] = 0   # corte seco = pagamento
    M *= c * np.clip((BEAT['END'] - t) / 1.2, 0, 1)
    def tt(d): return np.arange(int(d * SR)) / SR
    def thump(d=0.7, f0=58): x = tt(d); return (np.sin(2 * np.pi * f0 * x * (1 - .25 * x)) * np.exp(-x * 6) * .9).astype(np.float32)
    def modem(d=0.55):
        x = tt(d); fr = 900 + 1400 * ((x * 9) % 1); r = np.random.default_rng(2)
        return ((np.sin(2 * np.pi * np.cumsum(fr) / SR) * .18 + r.normal(0, 1, len(x)) * .08) * np.minimum(1, x / .03) * np.minimum(1, (d - x) / .12)).astype(np.float32)
    def click(d=0.18): x = tt(d); return (np.sin(2 * np.pi * 120 * x) * np.exp(-x * 30) * .7).astype(np.float32)
    def pop(d=0.13, f0=650, f1=1300): x = tt(d); return (np.sin(2 * np.pi * np.cumsum(f0 + (f1 - f0) * x / d) / SR) * np.exp(-x * 18) * .45).astype(np.float32)
    S = np.zeros(N, np.float32)
    def put(x, at, g): i = int(at * SR); n = min(len(x), N - i); S[i:i + n] += x[:n] * g
    put(thump(), 0, .8); [put(click(), .05 * k, .45) for k in range(4)]
    put(modem(), BEAT['SCAN'], .5); put(pop(), BEAT['SCAN'] + .3, .5); put(pop(f0=800, f1=1600), BEAT['B'], .5); put(pop(.09, 900, 1400), BEAT['B'] + .12, .4)
    put(modem(), BEAT['DIVE'], .55); put(click(), BEAT['IN_A'] + .8, .4); put(pop(), BEAT['HL_B'], .45)
    put(thump(.4, 70), BEAT['OUT1'], .35); put(click(), BEAT['OUT2'], .4); put(pop(f0=800, f1=1600), BEAT['PAY'] + 1.8, .5); put(thump(.4, 70), BEAT['ASK'], .3)
    import wave
    x = M * .9 + S; x = (x / max(1e-6, np.abs(x).max()) * .9 * 32767).astype(np.int16)
    with wave.open('mix_raw.wav', 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(x.tobytes())
    mm = subprocess.run(['ffmpeg', '-v', 'info', '-i', 'mix_raw.wav', '-af', 'loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
    js = json.loads(mm[mm.rfind('{'):mm.rfind('}') + 1])
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'mix_raw.wav', '-af', f"loudnorm=I=-14:TP=-2.2:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true",
                    '-ar', str(SR), '-ac', '2', out], check=True)
    return out

def render(out='ESP03_PREVIA_TECNICA.mp4'):
    nf = int(round(BEAT['END'] * FPS))
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'corpo.mp4'], stdin=subprocess.PIPE)
    for i in range(nf): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    a = audio_previa(); outro = K + 'comum/outro/outro_binder_916.mp4'   # o fecho não tem faixa de áudio: silêncio com a duração dele
    dur = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', outro], capture_output=True, text=True).stdout.strip()
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'corpo.mp4', '-i', a, '-i', outro, '-f', 'lavfi', '-t', dur, '-i', 'anullsrc=r=48000:cl=stereo', '-filter_complex',
                    '[0:v]fps=30,format=yuv420p,setsar=1[v0];[2:v]scale=1080:1920,fps=30,format=yuv420p,setsar=1[v1];'
                    '[1:a]aformat=sample_rates=48000:channel_layouts=stereo[a0];[3:a]aformat=sample_rates=48000:channel_layouts=stereo[a1];'
                    '[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]', '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18',
                    '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out], check=True)
    print(out)

def capa():
    im = Image.new('RGB', (W, H), BG)
    for lado, (x, y, r) in (('A', (-40, 300, -8)), ('B', (540, 420, 7))):
        c = card_img(lado, 600).rotate(r, expand=True, resample=Image.BICUBIC); im.paste(c, (x, y), c)
    im = im.filter(ImageFilter.GaussianBlur(14)); im = Image.blend(im, Image.new('RGB', (W, H), BG), 0.55).convert('RGBA')
    tubo = tubo_frame(0.5, 'desconfiado').crop((300, 420, 940, 1000)).resize((560, 507), Image.LANCZOS).convert('RGBA')
    m = Image.new('L', tubo.size, 0); ImageDraw.Draw(m).ellipse((40, 20, tubo.width - 40, tubo.height + 120), fill=255); tubo.putalpha(m.filter(ImageFilter.GaussianBlur(45)))
    im.alpha_composite(tubo, (260, 1040)); d = ImageDraw.Draw(im, 'RGBA')
    frase = D.get('capa_frase', 'POPULAR ≠ FORTE'); foco = str(v('capa_foco', v('iB')))
    d.text((W / 2, 350), frase, font=fit(d, frase, INTB, 110, W - 100), fill=WHITE, anchor='mm')
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g); ff = fit(gd, foco, INTB, 400, W - 80)
    gd.text((W / 2, 720), foco, font=ff, fill=PH + (255,), anchor='mm'); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(22))); im.alpha_composite(g)
    d = ImageDraw.Draw(im, 'RGBA'); d.rectangle((0, 1572, W, 1662), fill=(5, 10, 16, 235)); d.line((0, 1572, W, 1572), fill=EM + (255,), width=3)
    d.text((60, 1617), 'META EM CURTO · ESP. 03', font=F(MONOB, 48), fill=EM, anchor='lm')
    marca(d); im = im.convert('RGB'); im.save('ESP03_CAPA.png')
    g = im.crop((0, 240, W, 1680)); g.save('ESP03_CAPA_grelha.png'); g.resize((270, 360), Image.LANCZOS).save('ESP03_CAPA_grelha_mini.png')
    print('ESP03_CAPA.png, ESP03_CAPA_grelha.png, ESP03_CAPA_grelha_mini.png')

if __name__ == '__main__':
    if MODO == 'capa': capa()
    elif MODO == 'stills':
        for x in map(float, sys.argv[3:]): frame(x).save(f'still_{x:05.2f}.png')
    else: render()
