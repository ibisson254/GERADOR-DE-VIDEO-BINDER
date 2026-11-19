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
UNID = D.get('unidade_pop', 'LISTAS')           # unidade de popularidade tal como o portal a escreve
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

# ---------- tempos (storyboard.md v2; na versão final vêm das palavras da voz) ----------
BEAT = dict(SCAN=0.30, NUM=1.00, HLB=1.60, Q=2.00, RISE=3.00, DIVE=3.40,
            POP=4.00, POP_BAR=4.50, POP_A=5.60, POP_B=7.20,
            PERF=8.50, PERF_A=9.00, PERF_B=10.40, PERF_DEN=12.00,
            LEIT=13.50, LEIT2=15.00, DIF=16.50, DIF_PT=17.20, DIF_IC=18.00, DIF_VER=19.00, DIF_NOTA=20.20,
            ASK=21.50, CLOSE=24.50, CLOSE2=26.00, END=27.50)
BEAT.update(D.get('beats', {}))                 # versão final: tempos vindos da voz (dados/episodio.json)
CEN = D.get('cenario', 'B_fora_margem')       # B_fora_margem · dentro_margem · A_melhor (dados/calcular.py)
LEITURA = {'B_fora_margem': 'MESMO COM A MARGEM DE ERRO, ELE FICA À FRENTE.',
           'dentro_margem': 'COM ESSA AMOSTRA, A DIFERENÇA CABE NA MARGEM DE ERRO.',
           'A_melhor': 'DESTA VEZ, A MULTIDÃO FEZ A CONTA.',
           'A_melhor_margem': 'MAS ESSA VANTAGEM CABE NA MARGEM DE ERRO.'}[CEN]
VO = [  # (início, fim, texto) — legenda terminal; na prévia = locução planeada (roteiro.md v2)
    (3.0, 4.0, f"{v('A')}: {v('nA')} LISTAS."), (4.0, 5.6, f"O MAIS JOGADO DO PORTAL, {v('qA')} DO META."),
    (5.6, 7.2, 'POPULARIDADE: QUEM ESCOLHE.'), (7.2, 8.5, f"{v('B')}: SÓ {v('nB')} LISTAS."),
    (8.5, 10.4, f"{IND}: {v('A')}, {v('iA')}."), (10.4, 12.0, f"{v('B')}, {v('iB')}."),
    (12.0, 13.5, f"EM {v('dA')} E {v('dB')} {DEN.upper()}."),
    (13.5, 15.0, 'POPULARIDADE MEDE QUEM ESCOLHE.'), (15.0, 16.5, f'{IND} MEDE QUEM GANHA.'),
    (17.2, 19.0, f"A DIFERENÇA: {v('dif')}."), (19.0, 21.5, LEITURA),
    (21.5, 24.5, str(v('pergunta', '[PERGUNTA LIGADA À DESCOBERTA]')).upper()),
    (24.5, 27.5, 'PROBABILIDADE CALCULADA. HUMANOS, IMPREVISÍVEIS.')]
if D.get('vo'): VO = [tuple(x) for x in D['vo']]   # texto final vem dos dados aprovados (roteiro.md)

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
def fontes(d, linhas, y=1350):
    for i, s in enumerate(linhas): d.text((80, y + i * 46), s, font=fit(d, s, COND, 36, 860), fill=(160, 180, 185, 240))
def marca(d):
    if SEM_DADOS or D.get('previa'):
        s = 'PRÉVIA TÉCNICA · SEM DADOS · NÃO PUBLICAR' if SEM_DADOS else D.get('previa')
        d.rounded_rectangle((W / 2 - 330, 22, W / 2 + 330, 70), 10, fill=(40, 28, 4, 230), outline=AMBER, width=2)
        d.text((W / 2, 46), s, font=F(MONOB, 26), fill=AMBER, anchor='mm')
def subs(im, t, y=1560):
    d = ImageDraw.Draw(im, 'RGBA')
    for a, b, s in VO:
        if a <= t < b:
            f = fit(d, s, MONOB, 44, 860); wd = d.textlength(s, font=f)
            if wd > 860: break
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

# ---------- gancho: grelha 2×2 (carta A · popularidade A / desempenho B · carta B) ----------
GW, GH = 400, 557
GRID = [(100, 375), (530, 375), (100, 940), (530, 940)]       # A, pop A, desempenho B, B
ROW = [(30, 92), (285, 92), (555, 92), (810, 92)]; RW = 240
def tile_num(w, h, big, unit, ctx, col, dim, rotulo):
    im = Image.new('RGBA', (int(w), int(h)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 24, fill=(8, 16, 20, 245), outline=col, width=4)
    d.text((w / 2, h * 0.13), rotulo, font=fit(d, rotulo, MONOB, int(w * 0.075), w - 40), fill=GREY, anchor='mm')
    d.text((w / 2, h * 0.42), big, font=fit(d, big, INTB, int(w * 0.30), w - 40), fill=col, anchor='mm')
    d.text((w / 2, h * 0.64), unit, font=fit(d, unit, MONOB, int(w * 0.10), w - 40), fill=WHITE, anchor='mm')
    d.text((w / 2, h * 0.78), ctx, font=fit(d, ctx, MONOB, int(w * 0.075), w - 40), fill=(170, 190, 195), anchor='mm')
    if dim:
        a = im.getchannel('A'); im = Image.blend(im, Image.new('RGBA', im.size, BG + (255,)), dim); im.putalpha(a)
    return im
def hook(t):
    km = eio((t - BEAT['RISE']) / 0.4) if t >= BEAT['RISE'] else 0.0
    tela = [(str(v('nA')), 70, PH), (UNID, 30, EM)] if t >= BEAT['RISE'] + .2 else None
    base = tubo_frame(t, 'desconfiado', tela=tela).convert('RGBA')
    shade = Image.new('RGBA', base.size, (3, 6, 10, int(225 * (1 - km)))); im = base.copy(); im.alpha_composite(shade)
    d = ImageDraw.Draw(im, 'RGBA'); a = int(255 * max(0, 1 - km * 2.5))
    if a and t < BEAT['Q']:
        s = f"DUEL COMMANDER 500 · {v('per')}"; d.text((W / 2, 300), s, font=fit(d, s, MONOB, 46, 860), fill=(200, 215, 220, a), anchor='mm')
    if a: d.text((515, 1522), FONTE, font=fit(d, FONTE, COND, 34, 820), fill=(160, 180, 185, a), anchor='mm')
    focoB = t >= BEAT['HLB']
    for i in range(4):                          # as quatro peças já estão no quadro 0; só assentam (escala 1,05 → 1)
        ks = eio((t + 0.12 - 0.04 * i) / 0.3)
        gx, gy = GRID[i]; rx, ry = ROW[i]; w = GW + (RW - GW) * km; x = gx + (rx - gx) * km; y = gy + (ry - gy) * km
        sc = 1.05 - 0.05 * ks; w2 = w * sc; x -= (w2 - w) / 2; y -= (w2 - w) * 0.7
        ladoA = i in (0, 1); dim = 0.55 if (focoB and ladoA and km < 1) else 0.0
        numon = t >= BEAT['NUM']
        if i in (0, 3): c = card_img('A' if i == 0 else 'B', w2, dim)
        elif i == 1: c = tile_num(w2, w2 * GH / GW, str(v('nA')) if numon else '', UNID, str(D.get('ctxA', f"{v('qA')} do meta")), WHITE, dim, D.get('rotulo_A', 'MAIS JOGADO'))
        else: c = tile_num(w2, w2 * GH / GW, str(v('iB')) if numon else '', IND, f"em {v('dB')} {DEN}", PH, 0, D.get('rotulo_B', 'MAIOR ' + IND))
        im.alpha_composite(c, (int(x), int(y)))
        if km < 0.3 and ((not focoB and ladoA and t >= BEAT['SCAN'] + .5) or (focoB and not ladoA)):
            glow_box(im, (int(x), int(y), int(x + c.width), int(y + c.height)))
        if i == 0 and BEAT['SCAN'] <= t < BEAT['SCAN'] + .5:
            sy = y + c.height * (t - BEAT['SCAN']) / .5; ImageDraw.Draw(im, 'RGBA').rectangle((x, sy - 4, x + c.width, sy + 4), fill=PH + (200,))
    d = ImageDraw.Draw(im, 'RGBA')
    if t >= BEAT['Q'] and km < 0.6:
        q1, q2 = 'O MAIS JOGADO É', 'O QUE MAIS VENCE?'; f = F(INTB, 68); a = int(255 * (1 - km / 0.6)); n = int((t - BEAT['Q']) * 60)
        d.text((W / 2, 262), q1[:n], font=f, fill=WHITE + (a,), anchor='mm'); d.text((W / 2, 337), q2[:max(0, n - len(q1))], font=f, fill=PH + (a,), anchor='mm')
    marca(d); out = im.convert('RGB')
    if t >= BEAT['DIVE']:
        z = 1 + 9 * ease((t - BEAT['DIVE']) / (BEAT['POP'] - BEAT['DIVE']))
        cw, ch = W / z, H / z; x0 = min(max(SCX - cw / 2, 0), W - cw); y0 = min(max(SCY - ch / 2, 0), H - ch)
        out = out.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
    return out

# ---------- dentro: três painéis, cada um com a sua grandeza e a sua unidade ----------
def titulo(d, t, t0, s1, s2):
    d.text((80, 250), typed(s1, t0, t, 50), font=F(MONOB, 56), fill=PH)
    d.text((80, 322), typed(s2, t0 + .2, t, 60), font=fit(d, s2, COND, 38, 860), fill=EM)
    d.line((80, 376, 940, 376), fill=(16, 185, 129, 110), width=2)
def tracejado(d, box, col=GREY):
    x0, y0, x1, y1 = box
    for x in range(int(x0), int(x1), 26): d.line((x, y0, min(x + 13, x1), y0), fill=col, width=3); d.line((x, y1, min(x + 13, x1), y1), fill=col, width=3)
    for y in range(int(y0), int(y1), 26): d.line((x0, y, x0, min(y + 13, y1)), fill=col, width=3); d.line((x1, y, x1, min(y + 13, y1)), fill=col, width=3)
def scene_pop(t):
    im, d = term_base(t); im = im.convert('RGBA'); d = ImageDraw.Draw(im, 'RGBA')
    titulo(d, t, BEAT['POP'] - .1, '> POPULARIDADE', f"{UNID.lower()} registados no portal · {v('per')}")
    top = D.get('pop_top') or [[f'[comandante {i + 1}]', None] for i in range(5)]
    nomes = [r[0] for r in top]
    if D.get('B') and D['B'] not in nomes: top = top + [['…', None], [D['B'], int(str(D.get('nB', '0')).replace('.', '') or 0)]]
    mx = max([r[1] for r in top if r[1]] or [1]); y = 640; passo = 110 if len(top) <= 5 else 96
    for j, (nome, n) in enumerate(top):
        rowA = (D.get('A') == nome) or (j == 0 and not D.get('A')); rowB = D.get('B') == nome; row2 = D.get('pop_hl2') == nome and t >= BEAT.get('POP_2', 99)
        col = PH if (rowA and t >= BEAT['POP_A']) else (AMBER if (rowB and t >= BEAT['POP_B']) else (WHITE if row2 else (90, 130, 140)))
        if nome == '…': d.text((80, y - 6), '…', font=F(MONOB, 40), fill=GREY); y += 40; continue
        d.text((80, y), nome, font=fit(d, nome, MONOB, 38, 600), fill=WHITE if (rowA or rowB) else (190, 205, 210))
        yb = y + 48; k = eio((t - BEAT['POP_BAR'] - 0.08 * j) / 0.6)
        if n is None: tracejado(d, (80, yb, 680, yb + 34)); d.text((935, yb + 17), '[n]', font=F(MONOB, 40), fill=GREY, anchor='rm')
        elif k > 0:
            d.rectangle((80, yb, 80 + 600 * n / mx * k, yb + 34), fill=col + (255,))
            d.text((935, yb + 17), f'{n:,}'.replace(',', '.'), font=F(MONOB, 42), fill=WHITE, anchor='rm')
        y += passo
    d.text((80, y + 6), f'escala: número de {UNID.lower()} (0 à esquerda)', font=F(COND, 34), fill=GREY)
    for lado, t0, x in (('A', BEAT['POP_A'], 760), ('B', BEAT['POP_B'], 760)):
        if t >= t0 and (lado == 'A') == (t < BEAT['POP_B']):
            k = eio((t - t0) / .3); c = card_img(lado, 170); im.alpha_composite(c, (int(x + 40 * (1 - k)), 392)); d = ImageDraw.Draw(im, 'RGBA')
    fontes(d, [FONTE, f"extraído em {v('extraido')} · {UNID.lower()} ≠ jogadores ≠ partidas"])
    hud(d); marca(d); return term_finish(im.convert('RGB'))
COLX = {'A': 300, 'B': 720}; BASE, ALT = 1150, 440
def scene_perf(t):
    im, d = term_base(t); im = im.convert('RGBA'); d = ImageDraw.Draw(im, 'RGBA')
    titulo(d, t, BEAT['PERF'] - .1, '> DESEMPENHO', f"{IND.lower()} · {v('universo', 'só os 20 com mais partidas')}")
    top = BASE - ALT
    for p in (0, 50, 100):                       # eixo 0–100 %, linha de 50 % tracejada
        y = BASE - ALT * p / 100
        if p == 50:
            for x in range(110, 920, 24): d.line((x, y, x + 12, y), fill=GREY, width=2)
        else: d.line((110, y, 920, y), fill=(60, 80, 90), width=2)
        d.text((100, y), f'{p}%', font=F(MONOB, 34), fill=GREY, anchor='rm')
    lider = 'A' if (frac('iA_v') or 0) >= (frac('iB_v') or 1) else 'B'    # o verde vai para quem tem o valor mais alto
    for lado, t0 in (('A', BEAT['PERF_A']), ('B', BEAT['PERF_B'])):
        col = PH if lado == lider else (110, 150, 160)
        if t < t0: continue
        cx = COLX[lado]; c = card_img(lado, 160); im.alpha_composite(c, (int(cx - 80), 400)); d = ImageDraw.Draw(im, 'RGBA')
        val = frac(f'i{lado}_v'); k = eio((t - t0) / .6)
        if val is None: tracejado(d, (cx - 110, top, cx + 110, BASE))
        else: d.rectangle((cx - 110, BASE - ALT * val * k, cx + 110, BASE), fill=col + (255,))
        yv = BASE - ALT * (val or 1) * k - 60 if val is not None else top - 60
        d.text((cx, max(yv, 668)), str(v(f'i{lado}')), font=F(INTB, 72), fill=col if val is not None else GREY, anchor='mm')
        nm = str(D.get('curto' + lado) or v(lado)); d.text((cx, BASE + 40), nm, font=fit(d, nm, MONOB, 42, 380), fill=WHITE, anchor='mm')
        if t >= BEAT['PERF_DEN']:
            s = f"em {v('d' + lado)} {DEN}"; kd = eio((t - BEAT['PERF_DEN']) / .25)
            d.rounded_rectangle((cx - 190, BASE + 75, cx + 190, BASE + 135), 12, outline=AMBER, width=3)
            d.text((cx, BASE + 105), s, font=fit(d, s, MONOB, int(40 + 8 * (1 - kd)), 380), fill=AMBER, anchor='mm')
    fontes(d, [FONTE, D.get('fonte_perf', f"{IND.lower()} tal como publicado no portal · extraído em {v('extraido')}")])
    hud(d); marca(d); return term_finish(im.convert('RGB'))
def scene_dif(t):
    im, d = term_base(t, 18); im = im.convert('RGBA'); d = ImageDraw.Draw(im, 'RGBA')
    titulo(d, t, BEAT['DIF'], '> A DIFERENÇA É REAL?', D.get('dif_titulo', f"{v('B')} − {v('A')}, em pontos de {IND.lower()}"))
    lo, hi, dv = D.get('dif_lo'), D.get('dif_hi'), D.get('dif_v')
    R = 0.5 if dv is None else min(0.5, max(0.2, math.ceil(max(abs(lo), abs(hi)) * 10 + 0.5) / 10))   # escala simétrica, nunca < ±20 pp
    X0, X1, Y = 140, 920, 720; xz = (X0 + X1) / 2; sx = lambda val: xz + (X1 - xz) * val / R
    d.line((X0, Y, X1, Y), fill=(80, 100, 110), width=3)
    for p in (-R, -R / 2, 0, R / 2, R):
        d.line((sx(p), Y - 14, sx(p), Y + 14), fill=GREY, width=2); d.text((sx(p), Y + 50), f'{p * 100:+.0f}'.replace('+0', '0'), font=F(MONOB, 34), fill=GREY, anchor='mm')
    d.line((xz, Y - 120, xz, Y + 20), fill=WHITE, width=4); d.text((xz, Y - 150), 'SEM DIFERENÇA', font=F(MONOB, 32), fill=WHITE, anchor='mm')
    if dv is None:
        if t >= BEAT['DIF_PT']: tracejado(d, (xz - 200, Y - 40, xz + 200, Y + 40)); d.text((xz, Y + 120), '[diferença e margem]', font=F(MONOB, 40), fill=GREY, anchor='mm')
    else:
        if t >= BEAT['DIF_IC']:
            k = eio((t - BEAT['DIF_IC']) / .8); a0, a1 = sx(dv + (lo - dv) * k), sx(dv + (hi - dv) * k)
            d.rectangle((a0, Y - 30, a1, Y + 30), fill=(16, 185, 129, 120), outline=EM, width=3)
        if t >= BEAT['DIF_PT']:
            d.ellipse((sx(dv) - 20, Y - 20, sx(dv) + 20, Y + 20), fill=WHITE); d.text((sx(dv) + 70, Y - 70), str(v('dif')), font=F(INTB, 64), fill=WHITE, anchor='mm')
    d.text((80, 880), 'ponto = diferença · faixa = margem de 95 %', font=F(COND, 38), fill=(170, 190, 195))
    if t >= BEAT['DIF_VER']:
        k = eio((t - BEAT['DIF_VER']) / .2); col = PH if VER_OK else AMBER; f = fit(d, VEREDITO, INTB, int(66 * (1.2 - .2 * k)), 880)
        wd = d.textlength(VEREDITO, font=f) + 70
        d.rounded_rectangle((W / 2 - wd / 2, 960, W / 2 + wd / 2, 1090), 18, outline=col, width=5, fill=(8, 20, 16, 240)); d.text((W / 2, 1025), VEREDITO, font=f, fill=col, anchor='mm')
    if t >= BEAT['DIF_NOTA']:
        for i, s in enumerate(D.get('nota', ('aproximado: jogos entre os dois contam', 'nos dois lados da conta'))):
            d.text((W / 2, 1170 + i * 50), s, font=F(MONOB, 36), fill=AMBER, anchor='mm')
    fontes(d, [FONTE, 'margem: intervalo de Newcombe a 95 % · cálculo do BINDER'])
    hud(d); marca(d); return term_finish(im.convert('RGB'))
def scene_ask(t):
    im, d = term_base(t, 14); im = im.convert('RGBA'); d = ImageDraw.Draw(im, 'RGBA')
    k = eio((t - BEAT['ASK']) / .35)
    for lado, x in (('A', 90), ('B', 530)):
        c = card_img(lado, 400, 0.0); im.alpha_composite(c, (int(x + (1 - k) * (-60 if lado == 'A' else 60)), 560))
    d = ImageDraw.Draw(im, 'RGBA'); d.text((510, 840), '×', font=F(INTB, 100), fill=PH, anchor='mm')
    q = str(v('pergunta', '[pergunta ligada à descoberta]')).upper(); f = F(INTB, 60); linhas = wrapw(d, q, f, 860)[:3]
    for i, s in enumerate(linhas): d.text((W / 2, 280 + i * 76), s, font=f, fill=WHITE if i < len(linhas) - 1 else PH, anchor='mm')
    for lado, x in (('A', 290), ('B', 730)):
        s = f"{v('i' + lado)} · {v('n' + lado)} {UNID.lower()}"; d.text((x, 1215), s, font=fit(d, s, MONOB, 38, 390), fill=(190, 205, 210), anchor='mm')
    hud(d); marca(d); return term_finish(im.convert('RGB'))
def wrapw(d, s, font, maxw):
    out, cur = [], ''
    for w_ in s.split():
        tt = (cur + ' ' + w_).strip()
        if d.textlength(tt, font=font) <= maxw: cur = tt
        else: out.append(cur); cur = w_
    if cur: out.append(cur)
    return out

# ---------- fora: TUBO, só duas vezes e com funções diferentes ----------
INCERTO = CEN in ('dentro_margem', 'A_melhor_margem')
EXPR_LEIT = 'desconfiado' if INCERTO else 'confiante'
def fora(t):
    if t < BEAT['DIF']:                          # leitura: sai do terminal (zoom-out) e escreve a regra no ecrã
        z = 1 + 0.6 * (1 - eio((t - BEAT['LEIT']) / .6))
        tela = [('ESCOLHE', 48, WHITE), ('≠ GANHA', 48, PH)] if t >= BEAT['LEIT2'] else None
        im = tubo_frame(t, 'analitico' if t < BEAT['LEIT2'] else EXPR_LEIT, zoom=z, tela=tela)
    else:                                        # fecho: assinatura; muda de expressão no «Humanos»
        im = tubo_frame(t, 'analitico' if t < BEAT['CLOSE2'] else ('desconfiado' if INCERTO else 'confiante'),
                        zoom=1 + 0.06 * ease((t - BEAT['CLOSE']) / 3))
    d = ImageDraw.Draw(im, 'RGBA'); marca(d); return im

def frame(t):
    if t < BEAT['POP']: im = hook(t)
    elif t < BEAT['PERF']: im = scene_pop(t)
    elif t < BEAT['LEIT']: im = scene_perf(t)
    elif t < BEAT['DIF']: im = fora(t)
    elif t < BEAT['ASK']: im = scene_dif(t)
    elif t < BEAT['CLOSE']: im = scene_ask(t)
    else: im = fora(t)
    if t >= BEAT['RISE']: im = subs(im.convert('RGBA'), t, 1490).convert('RGB')
    return im


# ---------- v3 (19/11, 17h30): hierarquia da referência do fundador — legenda grande no topo, carta grande ao centro,
# número em caixa por baixo, troca de carta com rotação 3D, provas reais do portal, selo de fonte sempre visível ----------
CARD['L'] = None
if D.get('carta_L') and os.path.exists(HERE + D['carta_L']):
    _c = Image.open(HERE + D['carta_L']).convert('RGB'); _m = Image.new('L', _c.size, 0)
    ImageDraw.Draw(_m).rounded_rectangle((0, 0, _c.size[0] - 1, _c.size[1] - 1), 24, fill=255); _c = _c.convert('RGBA'); _c.putalpha(_m); CARD['L'] = _c
def _prova(n):
    p = HERE + 'capturas/' + n
    return Image.open(p).convert('RGB') if os.path.exists(p) else None
LOGO, MATRIZ, TOP5 = _prova('recorte_cabecalho_portal.png'), _prova('recorte_matriz.png'), _prova('recorte_galeria_top5.png')
TL = D.get('voz_tempos') or []

def fundo(t):
    im, d = term_base(t, 22); return im.convert('RGBA')
def selo_fonte(im, a=255):
    d = ImageDraw.Draw(im, 'RGBA'); y = 1462
    d.rounded_rectangle((80, y, 940, y + 64), 14, fill=(8, 16, 20, int(235 * a / 255)), outline=(200, 40, 40, a), width=3)
    if LOGO:
        lg = LOGO.resize((int(LOGO.width * 54 / LOGO.height), 54), Image.LANCZOS); im.paste(lg, (90, y + 5)); x0 = 90 + lg.width + 14
    else: x0 = 100
    s = 'FONTE: portal Duel Commander 500 · @farpasdemana'; ImageDraw.Draw(im, 'RGBA').text((x0, y + 32), s, font=fit(d, s, CONDB if os.path.exists(CONDB) else COND, 32, 930 - x0), fill=(235, 240, 242, a), anchor='lm')
CONDB = '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf'
def legenda_topo(im, txt, t0, t, verde=()):
    """Legenda da narração no topo (estilo da referência): Inter Black, caixa escura, números a verde."""
    if not txt: return 236
    d = ImageDraw.Draw(im, 'RGBA'); f = F(INTB, 62); linhas = wrapw(d, txt, f, 860)[:3]
    if len(linhas) == 3: f = F(INTB, 54); linhas = wrapw(d, txt, f, 860)[:3]
    k = eio((t - t0) / 0.18); lh = f.size * 1.12; h = lh * len(linhas) + 40; y0 = 236 + 10 * (1 - k)
    wmax = max(d.textlength(l, font=f) for l in linhas)
    d.rounded_rectangle((540 - wmax / 2 - 30, y0, 540 + wmax / 2 + 30, y0 + h), 18, fill=(5, 10, 16, int(225 * k)))
    for i, l in enumerate(linhas):
        x = 540 - d.textlength(l, font=f) / 2; y = y0 + 20 + i * lh
        for w_ in l.split(' '):
            col = PH if any(ch.isdigit() for ch in w_) or w_.strip('?:,.') in verde else WHITE
            d.text((x + 3, y + 3), w_, font=f, fill=(0, 0, 0, int(160 * k))); d.text((x, y), w_, font=f, fill=col + (int(255 * k),))
            x += d.textlength(w_ + ' ', font=f)
    return y0 + h
def fala(t):
    for a, b, s in TL:
        if a - 0.05 <= t < b + 0.25: return a, s
    return None
def carta_flip(im, lado_ant, lado, t0, t, w, cx, cy, dur=0.32):
    """Troca de carta com rotação 3D no eixo Y (referência): a antiga roda até 90°, a nova entra de −90° a 0°."""
    k = (t - t0) / dur
    if lado_ant is None or k >= 1: _carta_rot(im, lado, 0.0, w, cx, cy); return
    if k < 0.5: _carta_rot(im, lado_ant, ease(k * 2) * 90, w, cx, cy)
    else: _carta_rot(im, lado, -90 + ease((k - .5) * 2) * 90, w, cx, cy)
def _carta_rot(im, lado, ang, w, cx, cy):
    c = card_img(lado, w); h = c.height; a = math.radians(ang)
    ww = max(2, int(w * math.cos(a))); persp = 0.12 * math.sin(a)        # o lado que se afasta encolhe
    src = c.resize((ww, h), Image.LANCZOS)
    hl, hr = h * (1 - max(0, persp)), h * (1 + min(0, persp))
    out = Image.new('RGBA', (ww, h), (0, 0, 0, 0)); d = (h - hl) / 2, (h - hr) / 2
    coeffs = _persp([(0, d[0]), (ww, d[1]), (ww, h - d[1]), (0, h - d[0])], [(0, 0), (ww, 0), (ww, h), (0, h)])
    out = src.transform((ww, h), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
    sh = Image.new('RGBA', (ww + 60, h + 60), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((30, 40, ww + 30, h + 40), 24, fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(18)); im.alpha_composite(sh, (int(cx - ww / 2 - 30), int(cy - h / 2 - 30)))
    im.alpha_composite(out, (int(cx - ww / 2), int(cy - h / 2)))
def _persp(pa, pb):
    A = []
    for (x, y), (X, Y) in zip(pa, pb):
        A.append([x, y, 1, 0, 0, 0, -X * x, -X * y]); A.append([0, 0, 0, x, y, 1, -Y * x, -Y * y])
    B = np.array(pb).reshape(8); r = np.linalg.solve(np.array(A, float), B); return tuple(r)
def caixa_num(im, big, sub, t0, t, y, col=PH, rot=''):
    d = ImageDraw.Draw(im, 'RGBA'); k = eio((t - t0) / 0.22)
    fb = F(INTB, int(118 * (1.15 - .15 * k))); wb = d.textlength(big, font=fb); fs = F(MONOB, 40); ws_ = d.textlength(sub, font=fs)
    w = max(wb, ws_) + 80; x0 = 540 - w / 2
    d.rounded_rectangle((x0, y, x0 + w, y + 190), 22, fill=(5, 12, 14, 240), outline=col, width=5)
    d.text((540, y + 72), big, font=fb, fill=col, anchor='mm'); d.text((540, y + 152), sub, font=fs, fill=WHITE, anchor='mm')
    if rot:
        fr = F(INTB, 54); wr = d.textlength(rot, font=fr) + 40
        d.rounded_rectangle((x0 + w - wr / 2 - 10, y - 40, x0 + w + wr / 2 - 10, y + 30), 16, fill=col)
        d.text((x0 + w - 10, y - 5), rot, font=fr, fill=BG, anchor='mm')
def prova(im, img, t0, t, y, label, w=900):
    if img is None or t < t0: return
    k = eio((t - t0) / 0.35); s = img.resize((w, int(img.height * w / img.width)), Image.LANCZOS); s = s.crop((0, 0, w, min(s.height, 350)))
    yy = int(y + 120 * (1 - k)); x = (W - w) // 2; d = ImageDraw.Draw(im, 'RGBA')
    d.rounded_rectangle((x - 10, yy - 54, x + w + 10, yy + s.height + 10), 16, fill=(240, 240, 240, int(255 * k)))
    d.text((x + 6, yy - 28), label, font=F(MONOB, 30), fill=(30, 30, 30, int(255 * k)), anchor='lm')
    im.paste(s, (x, yy))

SEQ = D.get('seq', [])   # [[t, plano, args...]] — ver dados/episodio.json
def plano_em(t):
    cur = None
    for i, p in enumerate(SEQ):
        if t >= p[0]: cur = i
    return cur

def cena_gancho(t):
    im = fundo(t); d = ImageDraw.Draw(im, 'RGBA')
    k = [eio((t + 0.15 - 0.05 * i) / 0.25) for i in range(3)]
    for i, (lado, x) in enumerate((('A', 70), ('B', 540))):
        c = card_img(lado, 470 * (1.04 - .04 * k[i])); im.alpha_composite(c, (int(x + (470 - c.width) / 2), 452))
        if t >= (0.5 if lado == 'A' else 1.6):
            glow_box(im, (int(x), 452, int(x + 470), 452 + c.height))
    if MATRIZ is not None:
        s = MATRIZ.resize((900, int(MATRIZ.height * 900 / MATRIZ.width)), Image.LANCZOS); y = 1130
        d.rounded_rectangle((80, y - 10, 1000, y + 330), 16, fill=(240, 240, 240, 255)); im.paste(s.crop((0, 0, 900, 320)), (90, y))
        if t >= 1.8: glow_box(im, (80, y - 10, 1000, y + 330), col=(220, 50, 50), r=16)
    legenda_topo(im, 'O MAIS JOGADO É O QUE MAIS VENCE?', 0.0, max(t, .3))
    selo_fonte(im); marca(ImageDraw.Draw(im, 'RGBA')); return im.convert('RGB')

def cena_carta(t, i):
    p = SEQ[i]; lado, big, sub, rot = p[2], p[3], p[4], p[5] if len(p) > 5 else ''
    prev = SEQ[i - 1][2] if i > 0 and SEQ[i - 1][1] == 'carta' else ('A' if i > 0 else None)
    extra = p[6] if len(p) > 6 else None                      # prova a meio do plano: [t, 'top5'|'matriz', rótulo]
    im = fundo(t); com_prova = extra and t >= extra[0]
    kp = eio((t - extra[0]) / .35) if com_prova else 0
    w = 560 - 150 * kp; cy = 448 + w * 1.396 / 2           # carta inteira, sempre acima da caixa ou da prova
    carta_flip(im, prev, lado, p[0], t, w, 540, cy)
    if not com_prova:
        if t >= p[0] + 0.3: caixa_num(im, big, f'{sub} · {rot}' if rot else sub, p[0] + .3, t, 1250)
    else: prova(im, {'top5': TOP5, 'matriz': MATRIZ}[extra[1]], extra[0], t, 1092, extra[2])
    f = fala(t); legenda_topo(im, f[1] if f else '', f[0] if f else 0, t)
    selo_fonte(im); marca(ImageDraw.Draw(im, 'RGBA')); return im.convert('RGB')

def cena_duas(t, i):
    p = SEQ[i]; im = fundo(t); k = eio((t - p[0]) / .35); d = ImageDraw.Draw(im, 'RGBA')
    for lado, x, s1, s2 in (('A', 80, D['iA'], D['dA'] + ' partidas'), ('B', 545, D['iB'], D['dB'] + ' partidas')):
        c = card_img(lado, 455); im.alpha_composite(c, (int(x + (1 - k) * (-80 if lado == 'A' else 80)), 470))
        d = ImageDraw.Draw(im, 'RGBA'); cx = x + 227
        d.rounded_rectangle((cx - 210, 1120, cx + 210, 1300), 18, fill=(5, 12, 14, 240), outline=PH if lado == 'A' else (110, 150, 160), width=4)
        d.text((cx, 1180), s1, font=F(INTB, 84), fill=PH if lado == 'A' else WHITE, anchor='mm')
        d.text((cx, 1260), s2, font=fit(d, s2, MONOB, 40, 390), fill=AMBER if t >= p[0] + 1.2 else WHITE, anchor='mm')
    if len(p) > 2 and t >= p[2]:
        s = 'win rate = vitórias ÷ (vitórias + derrotas)'; d.text((540, 1360), s, font=fit(d, s, COND, 36, 860), fill=(190, 205, 210), anchor='mm')
    f = fala(t); legenda_topo(im, f[1] if f else '', f[0] if f else 0, t)
    selo_fonte(im); marca(d); return im.convert('RGB')

def cena_dif(t, i):
    im = scene_dif(t).convert('RGBA'); d = ImageDraw.Draw(im, 'RGBA')
    d.rectangle((0, 220, W, 400), fill=BG + (255,))                 # o título do painel dá lugar à legenda
    f = fala(t); legenda_topo(im, f[1] if f else 'A DIFERENÇA É REAL?', f[0] if f else SEQ[i][0], t)
    d = ImageDraw.Draw(im, 'RGBA'); d.rectangle((0, 1420, W, 1560), fill=BG + (255,)); selo_fonte(im)
    return im.convert('RGB')

def cena_pergunta(t, i):
    p = SEQ[i]; im = fundo(t); k = eio((t - p[0]) / .35)
    for lado, x in (('A', 80), ('B', 545)):
        c = card_img(lado, 455); ang = (1 - k) * (6 if lado == 'A' else -6)
        c2 = c.rotate(ang, expand=True, resample=Image.BICUBIC); im.alpha_composite(c2, (int(x + (1 - k) * (-100 if lado == 'A' else 100)), 520))
    d = ImageDraw.Draw(im, 'RGBA'); d.text((540, 840), '×', font=F(INTB, 120), fill=PH, anchor='mm')
    for lado, x in (('A', 307), ('B', 772)):
        s = f"{D['i' + lado]} · {D['n' + lado]} decks"; d.text((x, 1235), s, font=fit(d, s, MONOB, 40, 420), fill=WHITE, anchor='mm')
    f = fala(t); legenda_topo(im, f[1] if f else '', f[0] if f else 0, t)
    selo_fonte(im); marca(d); return im.convert('RGB')

def cena_tubo(t, i):
    p = SEQ[i]; expr, tela_t = p[2], (p[3] if len(p) > 3 else None)
    z = 1 + 0.25 * (1 - eio((t - p[0]) / .5)) + 0.04 * ease((t - p[0]) / 3)
    tela = [('ESCOLHE', 48, WHITE), ('≠ GANHA', 48, PH)] if (tela_t and t >= tela_t) else None
    e2 = p[4] if (len(p) > 4 and tela_t and t >= tela_t) else expr
    im = tubo_frame(t, e2, zoom=z, tela=tela).convert('RGBA')
    f = fala(t); legenda_topo(im, f[1] if f else '', f[0] if f else 0, t)
    marca(ImageDraw.Draw(im, 'RGBA')); return im.convert('RGB')

CENAS = dict(gancho=lambda t, i: cena_gancho(t), carta=cena_carta, duas=cena_duas, dif=cena_dif, pergunta=cena_pergunta, tubo=cena_tubo)
def frame(t):
    i = plano_em(t); return CENAS[SEQ[i][1]](t, i)

# ---------- áudio da prévia: trilha do TUBO + SFX do ESP01 (sem voz) ----------
OUTRO = None
def _dur_outro():
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', K + 'comum/outro/outro_binder_916.mp4'], capture_output=True, text=True).stdout)
def audio_previa(out='mix_previa.wav'):
    SR = 48000; TOT = BEAT['END'] + _dur_outro(); N = int(TOT * SR)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', K + 'oraculo/musica/tubo_tema.mp3', '-t', str(TOT), '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    M = np.zeros(N, np.float32); m = np.frombuffer(raw, np.float32)[:N]; M[:len(m)] = m
    t = np.arange(N) / SR; c = np.ones(N); j0, j1 = int(BEAT['DIF'] * SR), int((BEAT['DIF'] + .6) * SR); c[j0:j1] = 0   # corte seco = pagamento
    M *= c * np.clip((TOT - t) / 1.5, 0, 1)       # a trilha acompanha o fecho e só termina com ele
    def tt(d): return np.arange(int(d * SR)) / SR
    def thump(d=0.7, f0=58): x = tt(d); return (np.sin(2 * np.pi * f0 * x * (1 - .25 * x)) * np.exp(-x * 6) * .9).astype(np.float32)
    def modem(d=0.55):
        x = tt(d); fr = 900 + 1400 * ((x * 9) % 1); r = np.random.default_rng(2)
        return ((np.sin(2 * np.pi * np.cumsum(fr) / SR) * .18 + r.normal(0, 1, len(x)) * .08) * np.minimum(1, x / .03) * np.minimum(1, (d - x) / .12)).astype(np.float32)
    def click(d=0.18): x = tt(d); return (np.sin(2 * np.pi * 120 * x) * np.exp(-x * 30) * .7).astype(np.float32)
    def pop(d=0.13, f0=650, f1=1300): x = tt(d); return (np.sin(2 * np.pi * np.cumsum(f0 + (f1 - f0) * x / d) / SR) * np.exp(-x * 18) * .45).astype(np.float32)
    S = np.zeros(N, np.float32)
    def put(x, at, g): i = int(at * SR); n = min(len(x), N - i); S[i:i + n] += x[:n] * g
    put(thump(), 0, .8); [put(click(), .04 * k, .45) for k in range(4)]
    put(modem(), BEAT['SCAN'], .5); put(pop(), BEAT['NUM'], .5); put(pop(f0=800, f1=1600), BEAT['HLB'], .5); put(click(), BEAT['Q'], .35)
    put(modem(), BEAT['DIVE'], .55); put(click(), BEAT['POP_BAR'], .35); put(pop(), BEAT['POP_A'], .45); put(pop(.09, 900, 1400), BEAT['POP_B'], .4)
    put(click(), BEAT['PERF_A'], .4); put(pop(f0=800, f1=1600), BEAT['PERF_B'], .5); put(click(), BEAT['PERF_DEN'], .4)
    put(thump(.4, 70), BEAT['LEIT'], .35); put(click(), BEAT['LEIT2'], .4)
    put(pop(), BEAT['DIF_PT'], .45); put(pop(f0=800, f1=1600), BEAT['DIF_VER'], .5); put(click(), BEAT['DIF_NOTA'], .3)
    put(click(), BEAT['ASK'], .4); put(thump(.4, 70), BEAT['CLOSE'], .3)
    import wave
    x = M * .9 + S; x = (x / max(1e-6, np.abs(x).max()) * .9 * 32767).astype(np.int16)
    with wave.open('mix_raw.wav', 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(x.tobytes())
    mm = subprocess.run(['ffmpeg', '-v', 'info', '-i', 'mix_raw.wav', '-af', 'loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
    js = json.loads(mm[mm.rfind('{'):mm.rfind('}') + 1])
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'mix_raw.wav', '-af', f"loudnorm=I=-14:TP=-2.2:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true",
                    '-ar', str(SR), '-ac', '2', out], check=True)
    return out

def audio_final(voz, out='mix_final.wav'):
    """Voz (já com atempo da série) + trilha com ducking −12 dB sob a voz + os mesmos SFX. Pausas da ficha inseridas."""
    import wave
    SR = 48000; N = int((BEAT['END'] + _dur_outro()) * SR); cfg = D['voz']
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', voz, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    vz = np.frombuffer(raw, np.float32).copy(); V = np.zeros(N, np.float32)
    cortes = [0.0] + [a for a, _ in cfg['pausas']] + [len(vz) / SR]; desloc = cfg['lead']
    for k in range(len(cortes) - 1):
        a, b = int(cortes[k] * SR), int(cortes[k + 1] * SR); i = int((cortes[k] + desloc) * SR); n = min(b - a, N - i)
        if n > 0: V[i:i + n] = vz[a:a + n]
        if k < len(cfg['pausas']): desloc += cfg['pausas'][k][1]
    V *= 10 ** (cfg.get('ganho_db', 0) / 20)
    mix_trilha = audio_previa('so_trilha_sfx.wav')
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', mix_trilha, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    M = np.zeros(N, np.float32); m = np.frombuffer(raw, np.float32)[:N]; M[:len(m)] = m
    env = np.convolve((np.abs(V) > 0.01).astype(np.float32), np.ones(int(.25 * SR)) / int(.25 * SR), 'same')
    duck = 10 ** (-12 * np.clip(env * 3, 0, 1) / 20)
    x = V * 1.0 + M * 0.55 * duck; x = (x / max(1e-6, np.abs(x).max()) * .9 * 32767).astype(np.int16)
    with wave.open('mix_raw.wav', 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(x.tobytes())
    mm = subprocess.run(['ffmpeg', '-v', 'info', '-i', 'mix_raw.wav', '-af', 'loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
    js = json.loads(mm[mm.rfind('{'):mm.rfind('}') + 1])
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'mix_raw.wav', '-af', f"loudnorm=I=-14:TP=-2.2:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true",
                    '-ar', str(SR), '-ac', '2', 'mix_ln.wav'], check=True)
    mm = subprocess.run(['ffmpeg', '-v', 'info', '-i', 'mix_ln.wav', '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    import re
    i_lufs = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', mm)[-1]); tp = float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', mm)[-1])
    g = min(-14.0 - i_lufs, -1.5 - tp)              # acerta −14 LUFS sem passar −1,5 dBTP
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'mix_ln.wav', '-af', f'volume={g:.2f}dB', out], check=True)
    return out

def render(out='ESP03_PREVIA_TECNICA.mp4', audio=None):
    nf = int(round(BEAT['END'] * FPS))
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'corpo.mp4'], stdin=subprocess.PIPE)
    for i in range(nf): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    a = audio or audio_previa(); outro = K + 'comum/outro/outro_binder_916.mp4'   # o fecho não tem faixa de áudio: silêncio com a duração dele
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'corpo.mp4', '-i', outro, '-filter_complex',
                    '[0:v]fps=30,format=yuv420p,setsar=1[v0];[1:v]scale=1080:1920,fps=30,format=yuv420p,setsar=1[v1];[v0][v1]concat=n=2:v=1:a=0[v]',
                    '-map', '[v]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', 'video_so.mp4'], check=True)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'video_so.mp4', '-i', a, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                    '-shortest', '-movflags', '+faststart', out], check=True)
    print(out)

def capa():
    im = Image.new('RGB', (W, H), BG)
    for lado, (x, y, r) in (('A', (-40, 300, -8)), ('B', (540, 420, 7))):
        c = card_img(lado, 600).rotate(r, expand=True, resample=Image.BICUBIC); im.paste(c, (x, y), c)
    im = im.filter(ImageFilter.GaussianBlur(14)); im = Image.blend(im, Image.new('RGB', (W, H), BG), 0.55).convert('RGBA')
    tubo = tubo_frame(0.5, 'desconfiado' if INCERTO or not D.get('cenario') else 'confiante').crop((300, 420, 940, 1000)).resize((560, 507), Image.LANCZOS).convert('RGBA')
    m = Image.new('L', tubo.size, 0); ImageDraw.Draw(m).ellipse((40, 20, tubo.width - 40, tubo.height + 120), fill=255); tubo.putalpha(m.filter(ImageFilter.GaussianBlur(45)))
    im.alpha_composite(tubo, (260, 1040)); d = ImageDraw.Draw(im, 'RGBA')
    frase = D.get('capa_frase') or {'B_fora_margem': 'POPULAR ≠ FORTE', 'dentro_margem': 'AMOSTRA CURTA', 'A_melhor': 'O HYPE ACERTOU', 'A_melhor_margem': 'LIDERA POR POUCO'}.get(D.get('cenario'), 'MAIS JOGADO, MAIS FORTE?')
    foco = str(D.get('capa_foco') or (v('iA') if CEN.startswith('A_melhor') else v('iB')))
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
    elif MODO == 'final':                     # python3 -I esp03_render.py <raiz> final <voz_atempo.wav>
        render('ESP03_META_EM_CURTO.mp4', audio_final(sys.argv[3]))
    elif MODO == 'stills':
        for x in map(float, sys.argv[3:]): frame(x).save(f'still_{x:05.2f}.png')
    else: render()
