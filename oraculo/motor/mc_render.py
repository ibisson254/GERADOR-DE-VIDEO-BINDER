# Meta em Curto · motor de edição padrão (desde 19/11/2026) — derivado do MC-ESP03 (v4 + capa v2).
# Padrão descrito em oraculo/CONTEXTO.md §7.4. O TUBO não é regenerado; a imagem-mestra não se altera.
#
# Uso:  python3 -I oraculo/motor/mc_render.py <raiz do repo> <pasta do episódio> <modo> [...]
#   stills 0.5 3 12 ...   -> still_XX.XX.png (rever em folha de contacto ANTES do render)
#   previa                -> ESP_PREVIA_SEM_VOZ.mp4 (trilha + SFX, sem voz)
#   final <voz_montada.wav> -> MC_FINAL.mp4 (voz montada por mc_voz.py, já com atempo)
#   capa                  -> CAPA.png + CAPA_grelha.png + CAPA_grelha_mini.png (§7.3)
# Tudo o que é do episódio vem de <pasta>/dados/episodio.json (modelo comentado: oraculo/motor/episodio_modelo.json).
import os, json, math, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
K = (sys.argv[1] if len(sys.argv) > 1 else '.').rstrip('/') + '/'
HERE = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else '.').rstrip('/') + '/'
MODO = sys.argv[3] if len(sys.argv) > 3 else 'previa'
ARGS = sys.argv[4:]
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
FONTE = D.get('linha_fonte', f"Dados: {v('fonte')} · {v('per')}")
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
def _tempo(x):
    """Tempo em segundos ou ancorado a uma frase da voz: "@3" = início da frase 3, "@3+0.2" / "@3-0.1" com desvio, "@3>" = fim."""
    if not isinstance(x, str) or not x.startswith('@'): return x
    import re
    m = re.match(r'@(\d+)(>?)([+-][\d.]+)?$', x); k, fim, off = int(m.group(1)), m.group(2), float(m.group(3) or 0)
    vt = D.get('voz_tempos') or []
    return (vt[k][1] if fim else vt[k][0]) + off
for _k, _v in list(D.get('beats', {}).items()): D['beats'][_k] = _tempo(_v)
for _p in D.get('seq', []):
    for _j, _x in enumerate(_p):
        if isinstance(_x, str) and _x.startswith('@'): _p[_j] = _tempo(_x)
        if isinstance(_x, list):
            for _jj, _xx in enumerate(_x):
                if isinstance(_xx, str) and _xx.startswith('@'): _x[_jj] = _tempo(_xx)
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
def _desfoque_local(im, g, caixa, raio, com_original=False):
    """Compõe em im a camada g desfocada, desfocando só a zona desenhada (caixa) com margem de 3,5×raio+12 px.
    Igual píxel a píxel ao desfoque do quadro inteiro (fora da margem a camada é transparente e o desfoque não chega lá),
    mas ~20× mais barato (26/11/2026, missão de engenharia; conferido em mc_render_regressao.py)."""
    m = int(raio * 3.5) + 12
    x0, y0 = max(0, int(caixa[0]) - m), max(0, int(caixa[1]) - m)
    x1, y1 = min(im.width, int(math.ceil(caixa[2])) + m), min(im.height, int(math.ceil(caixa[3])) + m)
    if x1 <= x0 or y1 <= y0: return
    reg = g.crop((x0, y0, x1, y1))
    im.alpha_composite(reg.filter(ImageFilter.GaussianBlur(raio)), (x0, y0))
    if com_original: im.alpha_composite(reg, (x0, y0))
def glow_box(im, box, col=PH, r=26):
    g = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).rounded_rectangle(box, r, outline=col + (255,), width=16)
    _desfoque_local(im, g, box, 14); ImageDraw.Draw(im).rounded_rectangle(box, r, outline=col + (255,), width=6)

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
    d.rounded_rectangle((60, 540, 1020, 1250), 22, fill=(5, 10, 16, 228))     # painel legível por cima da chuva
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
    s = D.get('selo_fonte', 'FONTE: [fonte · @conta]'); ImageDraw.Draw(im, 'RGBA').text((x0, y + 32), s, font=fit(d, s, CONDB if os.path.exists(CONDB) else COND, 32, 930 - x0), fill=(235, 240, 242, a), anchor='lm')
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
    legenda_topo(im, D.get('pergunta_gancho', '[PERGUNTA DO GANCHO]'), 0.0, max(t, .3))
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
        s = D.get('definicao', ''); d.rounded_rectangle((110, 1330, 970, 1392), 12, fill=(5, 10, 16, 230)); d.text((540, 1360), s, font=fit(d, s, COND, 36, 860), fill=(190, 205, 210), anchor='mm')
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
        s = (D.get('pergunta_rotulos') or {}).get(lado) or f"{D['i' + lado]} · {D['n' + lado]} decks"; d.text((x, 1235), s, font=fit(d, s, MONOB, 40, 420), fill=WHITE, anchor='mm')
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

# ---------- v4 (19/11, 17h30): chuva estilo Matrix visível no fundo, TUBO a falar depois das cartas,
# carta entra no ecrã do TUBO e o vídeo mergulha (como nos episódios antigos) ----------
mcols = [dict(x=x, y=rng.uniform(-H, H), v=rng.uniform(160, 360), n=int(rng.integers(14, 30))) for x in range(10, W, 26)]
def term_base(t, alpha=30):
    """Fundo do terminal com chuva de código verde a descer (estilo Matrix): cabeça clara, cauda a desvanecer."""
    im = TERM_BG.copy(); d = ImageDraw.Draw(im); fs = F(MONOB, 26)
    for c in mcols:
        yh = (c['y'] + t * c['v']) % (H + 600) - 300
        for k in range(c['n']):
            y = yh - k * 30
            if -30 < y < H:
                ch = GLY[int(t * 9 + k * 5 + c['x'] * 0.37) % len(GLY)] if k else GLY[int(t * 20 + c['x']) % len(GLY)]
                col = (170, 255, 190) if k == 0 else PH
                a = 235 if k == 0 else int(150 * (1 - k / c['n']) + 20)
                d.text((c['x'], y), ch, font=fs, fill=mix_bg(col, a))
    if EGG and EGG['t0'] <= t < EGG['t1']:
        for k, ch in enumerate(EGG['txt']): d.text((mcols[20]['x'], 1250 + k * 30), ch, font=fs, fill=mix_bg(PH, 160))
    return im, ImageDraw.Draw(im, 'RGBA')
ENV = None
def _led(im, t):
    if ENV is None: return
    fi = int(t * FPS); a = min(1, float(ENV[fi])) if fi < len(ENV) else 0
    if a < 0.04: return
    g = Image.new('RGBA', (120, 120), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((40, 40, 80, 80), fill=(16, 185, 129, int(220 * a)))
    g = g.filter(ImageFilter.GaussianBlur(14)); im.paste(g, (LED[0] - 60, LED[1] - 60), g)
    ImageDraw.Draw(im).ellipse((LED[0] - 7, LED[1] - 7, LED[0] + 7, LED[1] + 7), fill=(140, 255, 200))
def tubo_falando(t, expr, zoom=1.0, tela=None):
    im = tubo_frame(t, expr, tela=tela); _led(im, t)
    if abs(zoom - 1) > 1e-3:
        cw, ch = W / zoom, H / zoom; x0 = min(max(SCX - cw / 2, 0), W - cw); y0 = min(max(SCY - ch / 2, 0), H - ch)
        im = im.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
    return im.convert('RGBA')

def cena_tubo_abertura(t, i):
    """Depois das cartas, o TUBO aparece a falar; as cartas saem da posição do gancho (sem salto); a carta-herói voa
    para o ecrã do TUBO com rasto e acende ao entrar; mergulho."""
    p = SEQ[i]; t0 = p[0]; t_voo, t_mergulho, t_fim = p[2], p[3], SEQ[i + 1][0]
    im = tubo_falando(t, 'confiante')
    k = eio((t - t0) / .45)
    grade = SEQ[i - 1][1] == 'gancho_grade' if i > 0 else False
    if grade:
        pos = {'A': [GRADE_POS['A'], (80, 560, 220)], 'B': [GRADE_POS['B'], (800, 600, 180)], 'C': [GRADE_POS['C'], (860, 1500, 120)]}
        if t < t0 + .45:                                              # o número e a pergunta saem a desvanecer
            kf = 1 - k; tl = tile_num(370, 420, D['grade'].get('numero', ''), D['grade'].get('unidade', ''), D['grade'].get('contexto', ''), PH, 0, D['grade'].get('rotulo', ''))
            a = tl.getchannel('A').point(lambda v: int(v * kf)); tl.putalpha(a); im.alpha_composite(tl, (650, int(440 - 80 * k)))
    elif i > 0 and SEQ[i - 1][1] == 'mosaico':                       # MC-EP09 v3: as duas cartas do campeão saem do mosaico
        pos = {'A': [(85, 560, 430), (80, 560, 220)], 'C': [(565, 560, 430), (820, 600, 180)]}
    else:
        pos = {'A': [(70, 452, 470), (80, 560, 200)], 'B': [(540, 452, 470), (800, 560, 200)]}
    for lado in [l for l in ('C', 'B', 'A') if l in pos]:
        (x0, y0, w0), (x1, y1, w1) = pos[lado]; x, y, w = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k, w0 + (w1 - w0) * k
        esc = 0.0 if lado == 'A' else 0.45
        if lado != 'A' and t >= t_voo:                                # as de apoio saem quando o herói voa
            kk = 1 - ease((t - t_voo) / .3)
            if kk <= 0: continue
            c = card_img(lado, w, esc); a = c.getchannel('A').point(lambda v, kk=kk: int(v * kk)); c = c.copy(); c.putalpha(a); im.alpha_composite(c, (int(x), int(y))); continue
        if lado == 'A' and t >= t_voo:                                # voa para o ecrã do TUBO, com rasto
            kv = ease((t - t_voo) / (t_mergulho - t_voo)); sw = SCR[2] - SCR[0] - 40
            def at(q): ww = w1 + (sw * .55 - w1) * q; return x1 + (SCX - ww / 2 - x1) * q, y1 + (SCY - ww * 0.7 - y1) * q, ww
            for g_, a_ in ((0.18, 50), (0.09, 95)):                    # rasto: duas cópias fantasma atrás
                if kv - g_ > 0:
                    gx, gy, gw = at(max(0, kv - g_)); gc = card_img('A', gw); al = gc.getchannel('A').point(lambda v, a_=a_: int(v * a_ / 255)); gc = gc.copy(); gc.putalpha(al)
                    im.alpha_composite(gc, (int(gx), int(gy)))
            x, y, w = at(kv)
        c = card_img(lado, w, esc); im.alpha_composite(c, (int(x), int(y)))
        if lado == 'A': glow_box(im, (int(x), int(y), int(x + c.width), int(y + c.height)))
    if t_mergulho - .12 <= t < t_mergulho + .1:                       # flash verde no ecrã quando a carta entra
        kf = 1 - abs(t - (t_mergulho - .01)) / .11; fl = Image.new('RGBA', im.size, (0, 0, 0, 0))
        ImageDraw.Draw(fl).rectangle(SCR, fill=PH + (int(85 * max(0, kf)),)); _desfoque_local(im, fl, SCR, 18)
    if t < t_voo + 0.05:
        f = fala(t); legenda_topo(im, f[1] if f else '', f[0] if f else 0, t)
    out = im.convert('RGB')
    if t >= t_mergulho:                                               # mergulho no ecrã
        z = 1 + 9 * ease((t - t_mergulho) / (t_fim - t_mergulho))
        cw, ch = W / z, H / z; x0 = min(max(SCX - cw / 2, 0), W - cw); y0 = min(max(SCY - ch / 2, 0), H - ch)
        out = out.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
    return out

_cena_tubo_v3 = cena_tubo
def cena_tubo(t, i):
    """TUBO: entra a sair do ecrã (zoom-out do terminal) e fala com o LED a pulsar."""
    p = SEQ[i]; expr, tela_t = p[2], (p[3] if len(p) > 3 else None)
    k = (t - p[0]) / .5; z = 1 + 7 * (1 - eio(k)) if k < 1 else 1 + 0.04 * ease((t - p[0] - .5) / 3)
    if i > 0 and SEQ[i - 1][1] == 'tubo': z = 1 + 0.04 * ease((t - p[0]) / 3)
    tela = [('ESCOLHE', 48, WHITE), ('≠ GANHA', 48, PH)] if (tela_t and t >= tela_t) else None
    e2 = p[4] if (len(p) > 4 and tela_t and t >= tela_t) else expr
    im = tubo_falando(t, e2, zoom=z, tela=tela)
    f = fala(t); legenda_topo(im, f[1] if f else '', f[0] if f else 0, t)
    marca(ImageDraw.Draw(im, 'RGBA')); return im.convert('RGB')
CENAS['tubo'] = cena_tubo; CENAS['tubo_abertura'] = cena_tubo_abertura

_cena_carta_v3 = cena_carta
def cena_carta(t, i):
    """Primeira carta depois do mergulho: sai do ecrã do TUBO (cresce a partir do centro) em vez de rodar."""
    p = SEQ[i]
    if i > 0 and SEQ[i - 1][1] == 'tubo_abertura' and t < p[0] + 0.4:
        k = eio((t - p[0]) / .4); im = fundo(t); w = 160 + 400 * k; cy = 448 + 560 * 1.396 / 2
        c = card_img(p[2], w); im.alpha_composite(c, (int(540 - w / 2), int(cy - c.height / 2)))
        f = fala(t); legenda_topo(im, f[1] if f else '', f[0] if f else 0, t); selo_fonte(im)
        marca(ImageDraw.Draw(im, 'RGBA')); return im.convert('RGB')
    return _cena_carta_v3(t, i)
CENAS['carta'] = cena_carta

def frame(t):
    i = plano_em(t); p = SEQ[i]
    if p[1] not in ('tubo', 'tubo_abertura') and i > 0 and SEQ[i - 1][1] == 'tubo' and t < p[0] + 0.45:
        k = ease((t - p[0]) / .45); prev = SEQ[i - 1]                 # mergulho no ecrã antes de voltar aos dados
        im = tubo_falando(t, prev[4] if len(prev) > 4 else prev[2], zoom=1 + 9 * k)
        return im.convert('RGB')
    return CENAS[p[1]](t, i)

# ---------- cenas genéricas novas (MC-PAU02, 23/11/2026): grelha 2×2 com número, créditos de terceiros, barras,
# linha do tempo, previsão registada, pergunta com uma carta, fecho com créditos. Todo o texto vem do episodio.json ----------
def selo_txt(im, s, a=255):
    d = ImageDraw.Draw(im, 'RGBA'); y = 1462
    d.rounded_rectangle((80, y, 940, y + 64), 14, fill=(8, 16, 20, int(235 * a / 255)), outline=(200, 40, 40, a), width=3)
    d.text((100, y + 32), s, font=fit(d, s, CONDB if os.path.exists(CONDB) else COND, 32, 830), fill=(235, 240, 242, a), anchor='lm')
for _l in ('C',):
    if D.get('carta_' + _l) and os.path.exists(HERE + D['carta_' + _l]):
        _c = Image.open(HERE + D['carta_' + _l]).convert('RGB'); _m = Image.new('L', _c.size, 0)
        ImageDraw.Draw(_m).rounded_rectangle((0, 0, _c.size[0] - 1, _c.size[1] - 1), 24, fill=255); _c = _c.convert('RGBA'); _c.putalpha(_m); CARD[_l] = _c
TERC = {}
for _k, _f in (D.get('terceiros') or {}).items():                 # imagens que dependem de autorização (recortes circulares)
    if _f and os.path.exists(HERE + _f): TERC[_k] = Image.open(HERE + _f).convert('RGBA')
def circulo(im, key, cx, cy, diam, k=1.0, contorno=PH):
    if key not in TERC or k <= 0: return False
    dd = max(2, int(diam * (0.85 + 0.15 * k))); c = TERC[key].resize((dd, dd), Image.LANCZOS)
    a = c.getchannel('A').point(lambda x: int(x * min(1, k))); c.putalpha(a)
    g = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((cx - dd / 2 - 6, cy - dd / 2 - 6, cx + dd / 2 + 6, cy + dd / 2 + 6), outline=contorno + (int(255 * min(1, k)),), width=8)
    _desfoque_local(im, g, (cx - dd / 2 - 10, cy - dd / 2 - 10, cx + dd / 2 + 10, cy + dd / 2 + 10), 10, com_original=True); im.alpha_composite(c, (int(cx - dd / 2), int(cy - dd / 2))); return True
def topo_fala(im, t):
    f = fala(t); return legenda_topo(im, f[1] if f else '', f[0] if f else 0, t)

GRADE_POS = {'A': (60, 440, 560), 'N': (650, 440, 370), 'B': (650, 900, 175), 'C': (845, 900, 175)}   # herói · número · apoio
def cena_gancho_grade(t, i):
    """Quadro 0 (modelo do MC-EP08B): carta-herói grande a acender; número ao lado; duas cartas de apoio pequenas e escurecidas."""
    im = fundo(t); g = D.get('grade', {}); h = lambda w: int(w * 1.396)
    # herói: entra no quadro 0 com «tum» (escala 1,12 → 1 em 0,25 s) e fica aceso
    x, y, w = GRADE_POS['A']; k = eio(t / .25); w2 = w * (1.12 - .12 * k); xx, yy = x - (w2 - w) / 2, y - (h(w2) - h(w)) / 2
    c = card_img('A', w2); im.alpha_composite(c, (int(xx), int(yy))); glow_box(im, (int(xx), int(yy), int(xx + c.width), int(yy + c.height)))
    if t < .12:                                                       # flash do impacto
        fl = Image.new('RGBA', im.size, (255, 255, 255, int(90 * (1 - t / .12)))); im.alpha_composite(fl)
    d = ImageDraw.Draw(im, 'RGBA'); r = g.get('heroi', '')
    if r:
        f = fit(d, r, MONOB, 40, 540); wd = d.textlength(r, font=f) + 40
        d.rounded_rectangle((x + w / 2 - wd / 2, y + h(w) + 22, x + w / 2 + wd / 2, y + h(w) + 86), 12, fill=(8, 20, 16, 245), outline=PH, width=4)
        d.text((x + w / 2, y + h(w) + 54), r, font=f, fill=PH, anchor='mm')
    # número: aparece em BEAT['NUM'] com «pop»
    if t >= BEAT['NUM']:
        x, y, w = GRADE_POS['N']; kn = eio((t - BEAT['NUM']) / .22); hh = 420
        tl = tile_num(w, hh, g.get('numero', ''), g.get('unidade', ''), g.get('contexto', ''), PH, 0, g.get('rotulo', ''))
        tl = tl.resize((max(2, int(w * (0.85 + .15 * kn))), max(2, int(hh * (0.85 + .15 * kn)))))
        im.alpha_composite(tl, (int(x + (w - tl.width) / 2), int(y + (hh - tl.height) / 2)))
    # apoio: entram em BEAT['HLB'], já escurecidas (contexto, não protagonistas)
    for j, lado in enumerate(('B', 'C')):
        ka = eio((t - BEAT['HLB'] - .08 * j) / .25)
        if ka <= 0: continue
        x, y, w = GRADE_POS[lado]; c = card_img(lado, w, 0.45); a = c.getchannel('A').point(lambda v, ka=ka: int(v * ka)); c = c.copy(); c.putalpha(a)
        im.alpha_composite(c, (int(x), int(y + 30 * (1 - ka))))
    legenda_topo(im, D.get('pergunta_gancho', ''), 0.0, max(t, .3))
    selo_txt(im, D.get('selo_fonte', '')); return im.convert('RGB')

def cena_creditos(t, i):
    """Cartão «quem fez»: duas imagens de terceiros em círculo, nomes e ficha do evento (D['creditos'])."""
    p = SEQ[i]; im = fundo(t); cr = D.get('creditos', {}); d = ImageDraw.Draw(im, 'RGBA')
    d.rounded_rectangle((60, 470, 1020, 1400), 26, fill=(5, 10, 16, 225), outline=(16, 185, 129, 120), width=3)
    s = cr.get('titulo', ''); d.text((540, 530), s, font=fit(d, s, MONOB, 44, 860), fill=EM, anchor='mm')
    for j, (key, cx) in enumerate(cr.get('pessoas', [])):
        pass
    for j, item in enumerate(cr.get('itens', [])):
        cx = 300 if j == 0 else 780; k = eio((t - p[0] - 0.15 * j) / 0.35)
        ok = circulo(im, item['img'], cx, 790, 330, k); d = ImageDraw.Draw(im, 'RGBA')
        if not ok:                                                   # sem autorização: só texto
            d.ellipse((cx - 165, 625, cx + 165, 955), outline=(60, 80, 90), width=4)
        d.text((cx, 1010), item['nome'], font=fit(d, item['nome'], INTB, 50, 420), fill=WHITE + (int(255 * k),), anchor='mm')
        if item.get('sub'): d.text((cx, 1062), item['sub'], font=fit(d, item['sub'], MONO, 32, 420), fill=(170, 190, 195, int(255 * k)), anchor='mm')
    d.text((540, 790), '×', font=F(INTB, 90), fill=PH, anchor='mm')
    ke = eio((t - (p[2] if len(p) > 2 else p[0] + 0.5)) / 0.3)
    if ke > 0:                                                       # camada própria: em RGBA o ImageDraw não mistura alfa
        lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        for j, s in enumerate(cr.get('evento', [])):
            dl.text((540, 1180 + j * 64), s, font=fit(dl, s, MONOB if j == 0 else COND, 46 if j == 0 else 38, 880), fill=tuple((PH if j == 0 else WHITE)[:3]) + (int(255 * ke),), anchor='mm')
        im.alpha_composite(lay)
    topo_fala(im, t); selo_txt(im, cr.get('selo', D.get('selo_fonte', ''))); return im.convert('RGB')

def cena_barras(t, i):
    """Barras de representação de um evento (D['barras']): linhas destacadas a verde; carimbo opcional (p[2] = tempo)."""
    p = SEQ[i]; im = fundo(t); b = D.get('barras', {}); d = ImageDraw.Draw(im, 'RGBA')
    d.rounded_rectangle((60, 440, 1020, 1430), 26, fill=(5, 10, 16, 228))
    d.text((90, 490), b.get('titulo', ''), font=fit(d, b.get('titulo', ''), MONOB, 40, 700), fill=EM, anchor='lm')
    for j, key in enumerate(b.get('cantos', [])): circulo(im, key, 870 + j * 92, 490, 80, 1.0, contorno=EM)
    d = ImageDraw.Draw(im, 'RGBA'); rows = b.get('linhas', []); mx = max(r[1] for r in rows); y = 580
    for j, (nome, n) in enumerate(rows):
        k = eio((t - p[0] - 0.08 * j) / 0.5); hl = any(x in nome for x in b.get('destaque', []))
        col = PH if hl else (90, 130, 140)
        d.text((90, y), nome, font=fit(d, nome, MONOB, 38, 560), fill=WHITE if hl else (190, 205, 210))
        d.rectangle((90, y + 50, 90 + 640 * n / mx * k, y + 86), fill=col + (255,))
        d.text((990, y + 68), str(n), font=F(MONOB, 46), fill=WHITE, anchor='rm'); y += 118
    d.text((90, y + 4), b.get('rodape', ''), font=fit(d, b.get('rodape', ''), COND, 34, 860), fill=GREY)
    if len(p) > 2 and t >= p[2]:                                     # carimbo do campeão com a carta
        k = eio((t - p[2]) / 0.25); c = card_img('C', 200); im.alpha_composite(c, (int(800 + 60 * (1 - k)), 1110))
        d = ImageDraw.Draw(im, 'RGBA'); s1, s2 = b.get('carimbo', ['', ''])
        f = F(INTB, int(64 * (1.25 - .25 * k))); wd = max(d.textlength(s1, font=f), d.textlength(s2, font=F(MONOB, 38))) + 60
        d.rounded_rectangle((90, 1150, 90 + wd, 1330), 18, fill=(8, 20, 16, 245), outline=PH, width=5)
        d.text((120, 1205), s1, font=f, fill=PH, anchor='lm'); d.text((120, 1285), s2, font=F(MONOB, 38), fill=WHITE, anchor='lm')
    topo_fala(im, t); selo_txt(im, b.get('selo', D.get('selo_fonte', ''))); return im.convert('RGB')

def cena_linha_tempo(t, i):
    """Linha do tempo vertical (D['linha_tempo']['marcos'] = [[data, texto, cor]]); p[2] = tempo da frase-tese no fim."""
    p = SEQ[i]; im = fundo(t); lt = D.get('linha_tempo', {}); d = ImageDraw.Draw(im, 'RGBA')
    d.rounded_rectangle((60, 440, 1020, 1430), 26, fill=(5, 10, 16, 228))
    d.text((90, 490), lt.get('titulo', ''), font=fit(d, lt.get('titulo', ''), MONOB, 40, 860), fill=EM, anchor='lm')
    ms = lt.get('marcos', []); y0, step = 600, 170; x = 160
    d.line((x, y0, x, y0 + step * (len(ms) - 1)), fill=(60, 90, 100), width=6)
    for j, (dt, txt, cor) in enumerate(ms):
        k = eio((t - p[0] - 0.35 * j) / 0.3)
        if k <= 0: continue
        col = {'verde': PH, 'ambar': AMBER, 'cinza': (150, 170, 175)}.get(cor, WHITE); y = y0 + step * j
        r = 22 + (6 * math.sin(t * 6) if cor == 'ambar' else 0)
        d.ellipse((x - r, y - r, x + r, y + r), fill=col + (int(255 * k),))
        d.text((x + 60, y - 26), dt, font=F(INTB, 52), fill=col + (int(255 * k),), anchor='lm')
        d.text((x + 60, y + 34), txt, font=fit(d, txt, MONO, 34, 760), fill=(210, 222, 226, int(255 * k)), anchor='lm')
    if len(p) > 2 and t >= p[2]:
        k = eio((t - p[2]) / 0.22); s = lt.get('tese', ''); f = fit(d, s, INTB, int(76 * (1.2 - .2 * k)), 820); wd = d.textlength(s, font=f) + 70
        d.rounded_rectangle((540 - wd / 2, 1250, 540 + wd / 2, 1380), 18, fill=(30, 22, 4, 245), outline=AMBER, width=5)
        d.text((540, 1315), s, font=f, fill=AMBER, anchor='mm')
    topo_fala(im, t); selo_txt(im, lt.get('selo', '')); return im.convert('RGB')

def cena_previsao(t, i):
    """TUBO confiante com o cartão da previsão registada (D['previsao'])."""
    p = SEQ[i]; pv = D.get('previsao', {})
    k = (t - p[0]) / .5; z = 1 + 7 * (1 - eio(k)) if k < 1 else 1 + 0.04 * ease((t - p[0] - .5) / 3)
    im = tubo_falando(t, 'confiante', zoom=z, tela=[(pv.get('tela1', 'PREVISÃO'), 46, WHITE), (pv.get('tela2', 'REGISTRADA'), 46, PH)] if t >= p[0] + .5 else None)
    if t >= p[0] + .6:
        kc = eio((t - p[0] - .6) / .3); d = ImageDraw.Draw(im, 'RGBA'); y = 1250 + 60 * (1 - kc)
        d.rounded_rectangle((90, y, 990, y + 200), 22, fill=(5, 12, 14, int(245 * kc)), outline=PH + (int(255 * kc),), width=5)
        for j, s in enumerate(pv.get('linhas', [])):
            d.text((540, y + 60 + j * 80), s, font=fit(d, s, INTB if j == 0 else MONOB, 58 if j == 0 else 36, 840), fill=(PH if j == 0 else WHITE) + (int(255 * kc),), anchor='mm')
    topo_fala(im, t); return im.convert('RGB')

def cena_pergunta1(t, i):
    """Uma carta grande e a pergunta binária (D['pergunta1'] = {'sim': ..., 'nao': ...})."""
    p = SEQ[i]; im = fundo(t); k = eio((t - p[0]) / .35); pq = D.get('pergunta1', {})
    c = card_img('A', 470); c2 = c.rotate((1 - k) * 5, expand=True, resample=Image.BICUBIC); im.alpha_composite(c2, (int(540 - c2.width / 2), int(470 + 60 * (1 - k))))
    d = ImageDraw.Draw(im, 'RGBA')
    for j, (s, col, x) in enumerate(((pq.get('sim', 'SIM'), AMBER, 300), (pq.get('nao', 'NÃO'), PH, 780))):
        kk = eio((t - p[0] - .3 - .12 * j) / .25)
        d.rounded_rectangle((x - 200, 1170, x + 200, 1300), 22, fill=(8, 16, 20, int(245 * kk)), outline=col + (int(255 * kk),), width=5)
        d.text((x, 1235), s, font=fit(d, s, INTB, 60, 360), fill=col + (int(255 * kk),), anchor='mm')
    topo_fala(im, t); return im.convert('RGB')

def cena_tubo_fecho(t, i):
    """Fecho com o TUBO e uma faixa de créditos por baixo (D['creditos_fecho'])."""
    p = SEQ[i]; expr = p[2] if len(p) > 2 else 'analitico'
    im = tubo_falando(t, expr, zoom=1 + 0.04 * ease((t - p[0]) / 3)); d = ImageDraw.Draw(im, 'RGBA')
    ls = D.get('creditos_fecho', []); k = eio((t - p[0] - .3) / .4)
    if ls:
        d.rounded_rectangle((60, 1300, 1020, 1330 + 54 * len(ls)), 18, fill=(5, 10, 16, int(225 * k)))
        for j, s in enumerate(ls): d.text((540, 1340 + j * 54), s, font=fit(d, s, COND, 36, 900), fill=(220, 232, 236, int(255 * k)), anchor='mm')
    topo_fala(im, t); return im.convert('RGB')
_GAL = {}
def _gal(f, w):
    k = (f, int(w))
    if k not in _GAL:
        c = Image.open(HERE + f).convert('RGB'); h = int(w * c.size[1] / c.size[0]); c = c.resize((int(w), h), Image.LANCZOS)
        m = Image.new('L', c.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, c.size[0] - 1, c.size[1] - 1), 14, fill=255)
        c = c.convert('RGBA'); c.putalpha(m); _GAL[k] = c
    return _GAL[k]

def cena_lista(t, i):
    """Lista numerada que entra linha a linha (D['lista'] = {'titulo','linhas':[[n, texto, sub]], 'destaque': n, 'selo'})."""
    p = SEQ[i]; im = fundo(t); L = D.get('lista', {}); d = ImageDraw.Draw(im, 'RGBA')
    d.rounded_rectangle((60, 440, 1020, 1430), 26, fill=(5, 10, 16, 228))
    d.text((90, 490), L.get('titulo', ''), font=fit(d, L.get('titulo', ''), MONOB, 40, 860), fill=EM, anchor='lm')
    rows = L.get('linhas', []); y = 560; dur = max(.12, (L.get('janela', 2.4)) / max(1, len(rows)))
    for j, (n, txt, sub) in enumerate(rows):
        k = eio((t - p[0] - dur * j) / .2)
        if k <= 0: break
        hl = str(n) == str(L.get('destaque', '')); col = PH if hl else WHITE
        d.text((90 + 30 * (1 - k), y), str(n), font=F(MONOB, 46), fill=(PH if hl else GREY) + (int(255 * k),))
        d.text((170 + 30 * (1 - k), y - 2), txt, font=fit(d, txt, INTB, 44, 520), fill=col + (int(255 * k),))
        d.text((990, y + 26), sub, font=fit(d, sub, MONO, 30, 300), fill=(170, 190, 195, int(255 * k)), anchor='rm'); y += 104
    topo_fala(im, t); selo_txt(im, L.get('selo', D.get('selo_fonte', ''))); return im.convert('RGB')

def cena_galeria(t, i):
    """Grelha 3×2 de cartas reais (D['galeria'] = {'titulo','cartas':[ficheiros],'carimbo':[l1,l2],'selo'}); p[2] = tempo do carimbo."""
    p = SEQ[i]; im = fundo(t); G = D.get('galeria', {}); d = ImageDraw.Draw(im, 'RGBA')
    d.text((540, 470), G.get('titulo', ''), font=fit(d, G.get('titulo', ''), MONOB, 40, 900), fill=EM, anchor='mm')
    w = 290
    for j, f in enumerate(G.get('cartas', [])[:6]):
        k = eio((t - p[0] - .1 * j) / .3)
        if k <= 0: continue
        c = _gal(f, w); x = 75 + (j % 3) * (w + 20); y = 520 + (j // 3) * (int(w * 1.396) + 20) + 40 * (1 - k)
        a = c.getchannel('A').point(lambda v, k=k: int(v * k)); c2 = c.copy(); c2.putalpha(a); im.alpha_composite(c2, (int(x), int(y)))
    if len(p) > 2 and t >= p[2]:
        k = eio((t - p[2]) / .25); d = ImageDraw.Draw(im, 'RGBA'); s1, s2 = G.get('carimbo', ['', ''])
        f = F(INTB, int(96 * (1.3 - .3 * k))); wd = max(d.textlength(s1, font=f), d.textlength(s2, font=F(MONOB, 40))) + 80
        d.rounded_rectangle((540 - wd / 2, 1020, 540 + wd / 2, 1240), 22, fill=(8, 20, 16, 245), outline=PH, width=6)
        d.text((540, 1095), s1, font=f, fill=PH, anchor='mm'); d.text((540, 1190), s2, font=F(MONOB, 40), fill=WHITE, anchor='mm')
    topo_fala(im, t); selo_txt(im, G.get('selo', D.get('selo_fonte', ''))); return im.convert('RGB')
CENAS.update(lista=cena_lista, galeria=cena_galeria)
CENAS.update(gancho_grade=cena_gancho_grade, creditos=cena_creditos, barras=cena_barras, linha_tempo=cena_linha_tempo,
             previsao=cena_previsao, pergunta1=cena_pergunta1, tubo_fecho=cena_tubo_fecho)

# ---------- cenas de deck (MC-EP09, 27/11/2026): impressão da lista completa de 100 cartas (CONTEXTO §6.4) e combo com
# cartas reais + passos verificados no Oracle. Todo o texto vem do episodio.json ----------
def cena_decklist(t, i):
    """Impressão da lista inteira em 2 colunas (D['decklist'] = {'titulo','sub','colunas':[[[grupo,[cartas]],...],...],
    'chave':[cartas a verde],'carimbo':[l1,l2],'selo'}); a lista desce como papel de impressora; p[2] = tempo do carimbo."""
    p = SEQ[i]; im = fundo(t); L = D.get('decklist', {}); d = ImageDraw.Draw(im, 'RGBA')
    d.rounded_rectangle((60, 440, 1020, 1440), 26, fill=(5, 10, 16, 232))
    d.text((90, 486), L.get('titulo', ''), font=fit(d, L.get('titulo', ''), MONOB, 38, 900), fill=EM, anchor='lm')
    d.text((90, 532), L.get('sub', ''), font=fit(d, L.get('sub', ''), MONO, 28, 900), fill=GREY, anchor='lm')
    d.line((90, 562, 990, 562), fill=(16, 185, 129, 90), width=2)
    t_fim = SEQ[i + 1][0] if i + 1 < len(SEQ) else p[0] + 5; win0, win1, ls = 578, 1424, 37
    chave = set(L.get('chave', []))
    lay = Image.new('RGBA', (W, win1 - win0), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    alt = []
    for col in L.get('colunas', []): alt.append(sum(ls + 8 + ls * len(c) for _, c in col))
    desl = max(0, max(alt or [0]) - (win1 - win0)) * ease((t - p[0] - 0.5) / max(0.5, t_fim - p[0] - 1.0))
    for ci, col in enumerate(L.get('colunas', [])):
        x = 104 if ci == 0 else 566; y = 4 - desl; n = 0
        for g, cartas in col:
            if t >= p[0] + n * .006: dl.text((x - 14, y), g, font=F(MONOB, 26), fill=GREY)
            y += ls; n += 1
            for nome in cartas:
                if -ls < y < win1 - win0 and t >= p[0] + n * .006:
                    on = nome in chave
                    dl.text((x, y), nome, font=fit(dl, nome, CONDB, 30, 430), fill=(PH if on else (150, 190, 170)))
                    if on: dl.text((x - 26, y + 4), '▶', font=F(MONOB, 22), fill=PH)
                y += ls; n += 1
            y += 8
    fade = Image.new('L', lay.size, 255); fd = ImageDraw.Draw(fade)
    for k in range(40): fd.line((0, k, W, k), fill=int(255 * k / 40)); fd.line((0, lay.height - 1 - k, W, lay.height - 1 - k), fill=int(255 * k / 40))
    a = Image.composite(lay.getchannel('A'), Image.new('L', lay.size, 0), fade); lay.putalpha(a); im.alpha_composite(lay, (0, win0))
    if len(p) > 2 and t >= p[2]:
        k = eio((t - p[2]) / .25); d = ImageDraw.Draw(im, 'RGBA'); s1, s2 = L.get('carimbo', ['', ''])
        f = F(INTB, int(92 * (1.3 - .3 * k))); f2 = F(MONOB, 38); wd = max(d.textlength(s1, font=f), d.textlength(s2, font=f2)) + 80
        d.rounded_rectangle((540 - wd / 2, 900, 540 + wd / 2, 1110), 22, fill=(8, 20, 16, 248), outline=PH, width=6)
        d.text((540, 970), s1, font=f, fill=PH, anchor='mm'); d.text((540, 1060), s2, font=f2, fill=WHITE, anchor='mm')
    topo_fala(im, t); selo_txt(im, L.get('selo', D.get('selo_fonte', ''))); return im.convert('RGB')

_CB = {}
def _carta_f(f, w):
    k = (f, int(w))
    if k not in _CB:
        c = Image.open(HERE + f).convert('RGB'); c = c.resize((int(w), int(w * c.size[1] / c.size[0])), Image.LANCZOS)
        m = Image.new('L', c.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, c.size[0] - 1, c.size[1] - 1), int(w * .05), fill=255)
        c = c.convert('RGBA'); c.putalpha(m); _CB[k] = c
    return _CB[k]
def cena_combo(t, i):
    """Uma ou duas cartas reais grandes + passos que entram com a voz (D['combo'][p[2]] = {'titulo','cartas':[ficheiros],
    'passos':[[t, texto, 'verde'|'branco']], 'selo'}); tempos dos passos absolutos ou âncoras à voz."""
    p = SEQ[i]; im = fundo(t); C = D.get('combo', {}).get(p[2], {}); d = ImageDraw.Draw(im, 'RGBA')
    d.text((540, 468), C.get('titulo', ''), font=fit(d, C.get('titulo', ''), MONOB, 40, 920), fill=EM, anchor='mm')
    cs = C.get('cartas', []); w = 430 if len(cs) > 1 else 500
    xs = [70, 580] if len(cs) > 1 else [290]
    for j, f in enumerate(cs):
        k = eio((t - p[0] - .12 * j) / .3)
        if k <= 0: continue
        c = _carta_f(f, w); a = c.getchannel('A').point(lambda v, k=k: int(v * k)); c2 = c.copy(); c2.putalpha(a)
        im.alpha_composite(c2, (xs[j], int(510 + 50 * (1 - k))))
    if len(cs) > 1 and t >= p[0] + .3: ImageDraw.Draw(im, 'RGBA').text((540, 510 + int(w * 1.396) // 2), '+', font=F(INTB, 120), fill=PH, anchor='mm')
    passos = [(_tempo(a), s, c) for a, s, c in C.get('passos', [])]; vis = [x for x in passos if t >= x[0]]
    if vis:
        d = ImageDraw.Draw(im, 'RGBA'); y0 = 510 + int(w * 1.396) + 24; h = 62 * len(passos) + 30
        d.rounded_rectangle((70, y0, 1010, y0 + h), 20, fill=(5, 12, 14, 240), outline=(16, 185, 129, 160), width=3)
        for j, (a, s, cor) in enumerate(vis):
            k = eio((t - a) / .2); col = PH if cor == 'verde' else ((150, 170, 175) if cor == 'cinza' else WHITE)
            d.text((100 + 20 * (1 - k), y0 + 46 + 62 * j), s, font=fit(d, s, CONDB, 40, 880), fill=col + (int(255 * k),), anchor='lm')
    topo_fala(im, t); selo_txt(im, C.get('selo', D.get('selo_fonte', ''))); return im.convert('RGB')
CENAS.update(decklist=cena_decklist, combo=cena_combo)

# ---------- gancho em mosaico + ficha do evento com mapa (MC-EP09 v2, 27/11/2026). Todo o texto e imagens vêm do
# episodio.json; cenas usadas só por episódios que as pedem (regressão dos outros intacta) ----------
_ART = {}
def _arte(f, w, h):
    k = (f, w, h)
    if k not in _ART:
        a = Image.open(HERE + f).convert('RGB'); r = max(w / a.width, h / a.height)
        a = a.resize((max(w, int(a.width * r + .5)), max(h, int(a.height * r + .5))), Image.LANCZOS)
        x0, y0 = (a.width - w) // 2, (a.height - h) // 2; _ART[k] = a.crop((x0, y0, x0 + w, y0 + h))
    return _ART[k]
_TILE = {}
def _tile(j, w, h, dim):
    """Mosaico: arte do(s) comandante(s) do jogador j (dupla = diagonal), cantos arredondados; dim 0–1 = apagado."""
    k = (j, w, h, round(dim, 1))
    if k not in _TILE:
        artes = D['mosaico']['jogadores'][j][1]; t_ = _arte(artes[0], w, h).copy()
        if len(artes) > 1:
            b = _arte(artes[1], w, h); m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).polygon([(w * .62, 0), (w, 0), (w, h), (w * .38, h)], fill=255)
            t_.paste(b, (0, 0), m); ImageDraw.Draw(t_).line((w * .62, 0, w * .38, h), fill=(5, 10, 16), width=4)
        if dim > 0:
            g = t_.convert('L').convert('RGB'); t_ = Image.blend(t_, g, min(1, dim * 1.2)); t_ = Image.blend(t_, Image.new('RGB', (w, h), BG), .78 * dim)
        m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), 12, fill=255)
        t_ = t_.convert('RGBA'); t_.putalpha(m)
        if len(_TILE) > 400: _TILE.clear()
        _TILE[k] = t_
    return _TILE[k]
def cena_mosaico(t, i):
    """Gancho: os comandantes reais de todos os jogadores num mosaico; um scanner apaga-os um a um e só fica o campeão,
    que salta para ecrã cheio (cartas inteiras) e leva o carimbo. p = [t0, 'mosaico', scan0, scan1, zoom, carimbo]."""
    p = SEQ[i]; M = D['mosaico']; js = M['jogadores']; n = len(js); cam = M['campeao']
    s0, s1, tz, tc = p[2], p[3], p[4], p[5]
    im = fundo(t); cols = M.get('colunas', 6); tw, th, gp = 150, 118, 12; gx, gy = 60, 452
    rows = (n + cols - 1) // cols
    pos = []
    for j in range(n):
        r_, c_ = divmod(j, cols); nr = min(cols, n - r_ * cols); off = (cols - nr) * (tw + gp) / 2
        pos.append((gx + off + c_ * (tw + gp), gy + r_ * (th + gp)))
    yl = gy - 20 + (rows * (th + gp) + 40) * ease((t - s0) / max(.1, s1 - s0))   # linha do scanner
    kz = eio((t - tz) / .45)
    vivos = 0
    for j, (x, y) in enumerate(pos):
        ke = eio(t / .35 - j * .004) if t < .5 else 1.0                       # quadro 0 já mostra o mosaico inteiro
        ccy = y + th / 2; dim = 0.0
        if j != cam and t >= s0: dim = min(1, max(0, (yl - ccy) / 40))
        if dim < .5: vivos += 1
        if j == cam and kz > 0: continue
        tl = _tile(j, tw, th, dim)
        if kz > 0: a = tl.getchannel('A').point(lambda v: int(v * (1 - .7 * kz))); tl = tl.copy(); tl.putalpha(a)
        sc = 1.12 - .12 * ke
        if sc != 1: tl = tl.resize((int(tw * sc), int(th * sc)), Image.BILINEAR)
        im.alpha_composite(tl, (int(x + (tw - tl.width) / 2), int(y + (th - tl.height) / 2)))
        if 0 < dim < 1 and j != cam:                                          # corte vermelho quando o scanner passa
            dd = ImageDraw.Draw(im, 'RGBA'); dd.rounded_rectangle((x, y, x + tw, y + th), 12, outline=(230, 60, 60, int(220 * (1 - dim))), width=4)
    d = ImageDraw.Draw(im, 'RGBA')
    if s0 <= t < s1 + .15 and kz <= 0:                                        # feixe do scanner
        for k_ in range(18): d.line((50, yl - k_ * 3, 1030, yl - k_ * 3), fill=PH + (int(120 * (1 - k_ / 18) ** 2),), width=3)
        d.line((50, yl, 1030, yl), fill=(200, 255, 220, 255), width=4)
    x, y = pos[cam]
    if kz <= 0:                                                                # campeão: brilho a pulsar no mosaico
        pul = .5 + .5 * math.sin(t * 9) if t >= s0 else 0
        tl = _tile(cam, tw, th, 0); im.alpha_composite(tl, (int(x), int(y)))
        if t >= s0: glow_box(im, (int(x) - 4, int(y) - 4, int(x + tw) + 4, int(y + th) + 4), r=14); d = ImageDraw.Draw(im, 'RGBA'); d.rounded_rectangle((x - 4, y - 4, x + tw + 4, y + th + 4), 14, outline=PH + (int(150 + 105 * pul),), width=6)
    else:                                                                      # salta para ecrã cheio: as duas cartas inteiras
        im.alpha_composite(Image.new('RGBA', im.size, (5, 10, 16, int(150 * kz))))
        cw = 430; ch = int(cw * 1.396); cyc = 560 + ch / 2
        for q, (lado, cx) in enumerate((('A', 300), ('C', 780))):
            kq = eio((t - tz - .06 * q) / .45)
            w_ = tw + (cw - tw) * kq; h_ = w_ * 1.396
            xx = (x + tw / 2) + (cx - (x + tw / 2)) * kq - w_ / 2; yy = (y + th / 2) + (cyc - (y + th / 2)) * kq - h_ / 2
            c = card_img(lado, w_); im.alpha_composite(c, (int(xx), int(yy)))
            if kq >= 1: glow_box(im, (int(xx), int(yy), int(xx + c.width), int(yy + c.height)))
        if tz <= t < tz + .1: im.alpha_composite(Image.new('RGBA', im.size, (255, 255, 255, int(110 * (1 - (t - tz) / .1)))))
    if kz <= 0 or t < tc:                                                      # contador 39 → 1
        d = ImageDraw.Draw(im, 'RGBA'); vv = vivos if t >= s0 else n; a_ = int(255 * (1 - kz))
        s_ = f"{vv}"; f = F(INTB, 96); r_ = M.get('contador', 'DE {n} AINDA NA DISPUTA').format(n=n)
        d.rounded_rectangle((60, 1378, 1020, 1452), 18, fill=(5, 12, 14, int(235 * a_ / 255)), outline=(PH if vv == 1 else EM) + (a_,), width=4)
        d.text((100, 1416), s_, font=F(INTB, 64), fill=(PH if vv == 1 else WHITE) + (a_,), anchor='lm')
        d.text((100 + d.textlength(s_ + ' ', font=F(INTB, 64)), 1418), r_, font=fit(d, r_, MONOB, 38, 760), fill=(200, 215, 220, a_), anchor='lm')
    if t >= tc:                                                                # carimbo «CAMPEÃO»
        k = eio((t - tc) / .22); s1_, s2_ = M.get('carimbo', ['CAMPEÃO', ''])
        f = F(INTB, 120); f2 = F(MONOB, 40); dd = ImageDraw.Draw(im)
        wd = int(max(dd.textlength(s1_, font=f), dd.textlength(s2_, font=f2)) + 90)
        lay = Image.new('RGBA', (wd + 40, 270), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        dl.rounded_rectangle((20, 20, wd + 20, 250), 26, fill=(8, 20, 16, 250), outline=PH + (255,), width=8)
        dl.text((wd / 2 + 20, 98), s1_, font=f, fill=PH + (255,), anchor='mm'); dl.text((wd / 2 + 20, 202), s2_, font=f2, fill=WHITE + (255,), anchor='mm')
        sc = 1.45 - .45 * k; lay = lay.rotate(-4 * (1 - k) - 2, expand=True, resample=Image.BICUBIC)
        lay = lay.resize((int(lay.width * sc), int(lay.height * sc)), Image.BILINEAR)
        a = lay.getchannel('A').point(lambda v: int(v * min(1, k * 1.5))); lay.putalpha(a); im.alpha_composite(lay, (int(540 - lay.width / 2), int(1300 - lay.height / 2)))
    topo_fala(im, t); selo_txt(im, M.get('selo', D.get('selo_fonte', ''))); return im.convert('RGB')

_MAPA = {}
def cena_evento(t, i):
    """Ficha do evento: mapa (Natural Earth) com o país em destaque e o alfinete na cidade, cidade em grande e o cartão
    da loja com as linhas do evento. p = [t0, 'evento', t_alfinete, t_cartao]; D['evento'] = {...}."""
    p = SEQ[i]; E = D['evento']; t0, tp, tcart = p[0], p[2], p[3]
    im = fundo(t); d = ImageDraw.Draw(im, 'RGBA')
    if 'g' not in _MAPA: _MAPA['g'] = json.load(open(HERE + E['mapa'], encoding='utf-8'))['paises']
    G = _MAPA['g']; lo0, lo1, la0, la1 = E.get('caixa', [-10.2, -5.6, 36.6, 42.4]); cl = math.cos(math.radians((la0 + la1) / 2))
    bx0, by0, bw, bh = 70, 450, 470, 600; sc = min(bw / ((lo1 - lo0) * cl), bh / (la1 - la0))
    zoom = 1 + .06 * ease((t - t0) / 6)
    cxm, cym = bx0 + bw / 2, by0 + bh / 2
    def P(lo, la):
        x = bx0 + (lo - lo0) * cl * sc; y = by0 + (la1 - la) * sc
        return (cxm + (x - cxm) * zoom, cym + (y - cym) * zoom)
    km = eio((t - t0) / .6)
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    dl.rounded_rectangle((bx0 - 10, by0 - 10, bx0 + bw + 10, by0 + bh + 10), 22, fill=(5, 12, 16, 235), outline=(16, 185, 129, 110), width=3)
    for nome, rings in G.items():
        foco = nome == E.get('pais_mapa', 'Portugal')
        for r in rings:
            pts = [P(lo, la) for lo, la in r]
            if foco: dl.polygon(pts, fill=(16, 185, 129, int(95 * km)), outline=PH + (int(255 * km),))
            else: dl.polygon(pts, fill=(22, 34, 40, int(255 * km)), outline=(70, 100, 105, int(200 * km)))
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((bx0 - 8, by0 - 8, bx0 + bw + 8, by0 + bh + 8), 20, fill=255)
    lay.putalpha(Image.composite(lay.getchannel('A'), Image.new('L', im.size, 0), m)); im.alpha_composite(lay)
    d = ImageDraw.Draw(im, 'RGBA'); d.text((bx0 + 14, by0 + bh - 16), E.get('credito_mapa', 'Mapa: Natural Earth'), font=F(COND, 22), fill=(120, 140, 150, int(220 * km)), anchor='ls')
    if t >= tp:                                                                # alfinete com ressalto e ondas
        px, py = P(*E['alfinete']); kp = (t - tp) / .35
        drop = 0 if kp >= 1 else (1 - eio(kp)) * 120; bounce = 0 if kp < 1 else -10 * math.exp(-(t - tp - .35) * 10) * math.sin((t - tp - .35) * 30)
        for q in range(3):
            rr = ((t - tp) * 1.2 - q * .33) % 1.0
            if t - tp > q * .33: d.ellipse((px - 90 * rr, py - 36 * rr, px + 90 * rr, py + 36 * rr), outline=PH + (int(220 * (1 - rr)),), width=4)
        yy = py - drop + bounce; d.ellipse((px - 30, yy - 92, px + 30, yy - 32), fill=(230, 60, 60, 255), outline=WHITE + (255,), width=5)
        d.polygon([(px - 22, yy - 50), (px + 22, yy - 50), (px, yy)], fill=(230, 60, 60, 255)); d.ellipse((px - 11, yy - 73, px + 11, yy - 51), fill=WHITE + (255,))
    # cidade em grande à direita do mapa
    kc = eio((t - tp - .05) / .35)
    if kc > 0:
        lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay); xr = 590
        dl.text((xr + 30 * (1 - kc), 600), E.get('cidade', ''), font=fit(dl, E.get('cidade', ''), INTB, 116, 440), fill=WHITE + (255,), anchor='lm')
        dl.text((xr + 30 * (1 - kc), 700), E.get('pais', ''), font=fit(dl, E.get('pais', ''), MONOB, 54, 420), fill=PH + (255,), anchor='lm')
        for j, s in enumerate(E.get('lado', [])):
            kj = eio((t - tp - .3 - .15 * j) / .3)
            dl.text((xr, 800 + j * 62), s, font=fit(dl, s, CONDB, 40, 420), fill=(200, 215, 220, int(255 * kj)), anchor='lm')
        a = lay.getchannel('A').point(lambda v: int(v * kc)); lay.putalpha(a); im.alpha_composite(lay)
    # cartão da loja e do evento
    kk = eio((t - tcart) / .4)
    if kk > 0:
        y0 = 1080 + 60 * (1 - kk); lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        dl.rounded_rectangle((60, y0, 1020, y0 + 360), 26, fill=(8, 18, 16, 248), outline=PH + (255,), width=5)
        tem_logo = 'loja' in TERC
        xl = 260 if tem_logo else 100
        dl.text((xl, y0 + 78), E.get('loja', ''), font=fit(dl, E.get('loja', ''), INTB, 86, 1000 - xl), fill=WHITE + (255,), anchor='lm')
        for j, (s, cor) in enumerate(E.get('linhas', [])):
            kj = eio((t - tcart - .35 - .3 * j) / .25)
            col = PH if cor == 'verde' else (AMBER if cor == 'ambar' else (215, 226, 230))
            dl.text((100 if j else xl, y0 + 160 + j * 64), typed(s, tcart + .35 + .3 * j, t, 70), font=fit(dl, s, CONDB if j == 0 else COND, 42 if j == 0 else 38, 880 if j else 1000 - xl), fill=col + (int(255 * kj),), anchor='lm')
        a = lay.getchannel('A').point(lambda v: int(v * kk)); lay.putalpha(a); im.alpha_composite(lay)
        if tem_logo: circulo(im, 'loja', 160, y0 + 80, 150, kk, contorno=PH)
    topo_fala(im, t); selo_txt(im, E.get('selo', D.get('selo_fonte', ''))); return im.convert('RGB')
CENAS.update(mosaico=cena_mosaico, evento=cena_evento)

def _logo_circ(key, d, k, anel=(176, 138, 58)):
    """Logótipo (recorte circular do fundador) com revelação em máscara circular e anel fino na cor da marca; sem rodar,
    sem brilho, proporção intacta. k 0–1."""
    if key not in TERC: return None
    src = TERC[key]; c = src.resize((d, d), Image.LANCZOS); kk = eio(k)
    m = Image.new('L', (d * 2, d * 2), 0); rr = d * (.15 + .85 * kk)
    ImageDraw.Draw(m).ellipse((d - rr, d - rr, d + rr, d + rr), fill=255); m = m.resize((d, d), Image.LANCZOS)
    a = Image.composite(c.getchannel('A'), Image.new('L', (d, d), 0), m); c = c.copy(); c.putalpha(a)
    out = Image.new('RGBA', (d + 16, d + 16), (0, 0, 0, 0)); out.alpha_composite(c, (8, 8))
    if kk > .05: ImageDraw.Draw(out).ellipse((5, 5, d + 10, d + 10), outline=anel + (int(230 * kk),), width=4)
    return out
def cena_evento_v3(t, i):
    """Ficha do evento numa só composição (MC-EP09 v3): loja (logótipo + nome) → evento → cidade/país com mapa → data →
    números do torneio. p = [t0, 'evento_v3', t_logo, t_mapa, t_alfinete, t_num1, t_num2, t_realce]; D['evento'] (chaves *_v3)."""
    p = SEQ[i]; E = D['evento']; t0, tl, tm, tp, tn1, tn2, tr = p[0], p[2], p[3], p[4], p[5], p[6], p[7]
    im = fundo(t); kp = eio((t - t0) / .3)
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    dl.rounded_rectangle((60, 440, 1020, 1440), 28, fill=(5, 12, 14, int(238 * kp)), outline=(16, 185, 129, int(140 * kp)), width=3)
    dl.line((100, 790, 980, 790), fill=(16, 185, 129, int(70 * kp)), width=2); im.alpha_composite(lay)
    # 1 · loja: logótipo (máscara circular) + nome
    lg = _logo_circ('loja', 270, (t - tl) / .45) if t >= tl else None
    if lg is not None:
        im.alpha_composite(lg, (92, 472))
        if tr <= t < tr + .6:                                             # realce quando a voz diz o nome da loja
            kr = (t - tr) / .6; g = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((92 + 4 - 14 * kr, 472 + 4 - 14 * kr, 92 + 282 + 14 * kr, 472 + 282 + 14 * kr), outline=(176, 138, 58, int(200 * (1 - kr))), width=4)
            im.alpha_composite(g)
    xl = 400 if 'loja' in TERC else 100; d = ImageDraw.Draw(im, 'RGBA')
    kn = eio((t - tl - .2) / .3)
    if kn > 0:
        lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        for j, w_ in enumerate(E.get('loja_linhas', [E.get('loja', '')])):
            dl.text((xl + 24 * (1 - kn), 548 + j * 100), w_, font=fit(dl, w_, INTB, 104, 1000 - xl), fill=WHITE + (255,), anchor='lm')
        ev = E.get('evento_v3', ''); ke = eio((t - tl - .55) / .3)
        if ke > 0: dl.text((xl, 728), typed(ev, tl + .55, t, 60), font=fit(dl, ev, MONOB, 38, 1000 - xl), fill=PH + (int(255 * ke),), anchor='lm')
        a = lay.getchannel('A').point(lambda v: int(v * kn)); lay.putalpha(a); im.alpha_composite(lay)
    # 2 · onde: mapa pequeno + cidade/país + data
    if 'g' not in _MAPA: _MAPA['g'] = json.load(open(HERE + E['mapa'], encoding='utf-8'))['paises']
    G = _MAPA['g']; lo0, lo1, la0, la1 = E.get('caixa', [-10.2, -5.6, 36.6, 42.4]); cl = math.cos(math.radians((la0 + la1) / 2))
    bx0, by0, bw, bh = 100, 822, 300, 380; sc = min(bw / ((lo1 - lo0) * cl), bh / (la1 - la0))
    ox = bx0 + (bw - (lo1 - lo0) * cl * sc) / 2
    def P(lo, la): return (ox + (lo - lo0) * cl * sc, by0 + (la1 - la) * sc)
    km = eio((t - tm) / .5)
    if km > 0:
        lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        dl.rounded_rectangle((bx0 - 8, by0 - 8, bx0 + bw + 8, by0 + bh + 8), 18, fill=(8, 18, 20, 255), outline=(16, 185, 129, 90), width=2)
        for nome, rings in G.items():
            foco = nome == E.get('pais_mapa', 'Portugal')
            for r in rings:
                pts = [P(lo, la) for lo, la in r]
                dl.polygon(pts, fill=(16, 185, 129, 110) if foco else (24, 36, 42, 255), outline=PH + (255,) if foco else (70, 100, 105, 200))
        m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((bx0 - 6, by0 - 6, bx0 + bw + 6, by0 + bh + 6), 16, fill=255)
        lay.putalpha(Image.composite(lay.getchannel('A').point(lambda v: int(v * km)), Image.new('L', im.size, 0), m)); im.alpha_composite(lay)
        d = ImageDraw.Draw(im, 'RGBA'); d.text((bx0 + 10, by0 + bh - 8), E.get('credito_mapa', ''), font=F(COND, 20), fill=(120, 140, 150, int(220 * km)), anchor='ls')
    if t >= tp:
        px, py = P(*E['alfinete']); kq = (t - tp) / .3; d = ImageDraw.Draw(im, 'RGBA')
        drop = 0 if kq >= 1 else (1 - eio(kq)) * 90; bounce = 0 if kq < 1 else -8 * math.exp(-(t - tp - .3) * 10) * math.sin((t - tp - .3) * 30)
        for q in range(2):
            rr = ((t - tp) * 1.1 - q * .45) % 1.0
            if t - tp > q * .45: d.ellipse((px - 60 * rr, py - 24 * rr, px + 60 * rr, py + 24 * rr), outline=PH + (int(200 * (1 - rr)),), width=3)
        yy = py - drop + bounce; d.ellipse((px - 22, yy - 68, px + 22, yy - 24), fill=(230, 60, 60, 255), outline=WHITE + (255,), width=4)
        d.polygon([(px - 16, yy - 38), (px + 16, yy - 38), (px, yy)], fill=(230, 60, 60, 255)); d.ellipse((px - 8, yy - 54, px + 8, yy - 38), fill=WHITE + (255,))
    kc = eio((t - tp - .05) / .35)
    if kc > 0:
        lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay); xr = 450
        dl.text((xr + 24 * (1 - kc), 880), E.get('cidade', ''), font=fit(dl, E.get('cidade', ''), INTB, 112, 540), fill=WHITE + (255,), anchor='lm')
        dl.text((xr + 24 * (1 - kc), 975), E.get('pais', ''), font=fit(dl, E.get('pais', ''), MONOB, 52, 520), fill=PH + (255,), anchor='lm')
        kd = eio((t - tp - .4) / .3)
        dl.text((xr, 1090), E.get('data_v3', ''), font=fit(dl, E.get('data_v3', ''), INTB, 76, 520), fill=(236, 241, 245, int(255 * kd)), anchor='lm')
        a = lay.getchannel('A').point(lambda v: int(v * kc)); lay.putalpha(a); im.alpha_composite(lay)
    # 3 · números do torneio (dois blocos)
    d = ImageDraw.Draw(im, 'RGBA')
    for j, (tt_, (big, sub)) in enumerate(zip((tn1, tn2), E.get('numeros_v3', []))):
        k = eio((t - tt_) / .25)
        if k <= 0: continue
        x0 = 100 if j == 0 else 545; w = 435 if j == 0 else 435; y0 = 1236 + 20 * (1 - k)
        d.rounded_rectangle((x0, y0, x0 + w, y0 + 170), 20, fill=(8, 20, 16, int(250 * k)), outline=(PH if j == 0 else EM) + (int(255 * k),), width=4)
        fb = fit(d, big, INTB, int(84 * (1.12 - .12 * k)), w - 40); d.text((x0 + w / 2, y0 + 66), big, font=fb, fill=(PH if j == 0 else WHITE) + (int(255 * k),), anchor='mm')
        d.text((x0 + w / 2, y0 + 136), sub, font=fit(d, sub, MONOB, 34, w - 30), fill=(200, 215, 220, int(255 * k)), anchor='mm')
    topo_fala(im, t); selo_txt(im, E.get('selo', D.get('selo_fonte', ''))); return im.convert('RGB')
CENAS.update(evento_v3=cena_evento_v3)

# ---------- acabamento (MC-EP09 v2): abalo de câmara nos impactos e transição rápida entre cenas; só com
# D['abalos'] / D['transicoes'] (os outros episódios não mudam) ----------
_frame_base = frame
def frame(t):
    im = _frame_base(t)
    tr = D.get('transicoes')
    if tr:
        i = plano_em(t); p = SEQ[i]; dur = tr.get('dur', .16)
        if i > 0 and p[0] <= t < p[0] + dur and p[1] not in tr.get('sem', []) and SEQ[i - 1][1] not in tr.get('sem', []):
            k = (t - p[0]) / dur; prev = _frame_base(p[0] - 1 / FPS)
            sh = int(W * .18 * (1 - eio(k))); nv = Image.new('RGB', (W, H), BG)
            nv.paste(im.crop((0, 0, W - sh, H)), (sh, 0)) if sh else nv.paste(im)
            a = prev.crop((0, 0, W, H)).filter(ImageFilter.BoxBlur(6)); im = Image.blend(a, nv, eio(k) * .85 + .15)
    for ta, amp in D.get('abalos', []):
        ta = _tempo(ta) if isinstance(ta, str) else ta
        if ta <= t < ta + .35:
            e = math.exp(-(t - ta) * 12) * amp; dx, dy = int(e * math.sin((t - ta) * 90)), int(e * math.cos((t - ta) * 77))
            if dx or dy:
                z = 1.0 + .02 * e / max(1, amp); bw, bh = int(W * z), int(H * z); big = im.resize((bw, bh), Image.BILINEAR)
                im = big.crop(((bw - W) // 2 - dx, (bh - H) // 2 - dy, (bw - W) // 2 - dx + W, (bh - H) // 2 - dy + H))
    return im

# ---------- áudio da prévia: trilha do TUBO + SFX do ESP01 (sem voz) ----------
OUTRO = None
def _dur_outro():
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', K + 'comum/outro/outro_binder_916.mp4'], capture_output=True, text=True).stdout)
def _sfx_cues(put, tt, SR, base):
    """Deixas de efeitos do episódio: D['sfx'] = [[tempo|@âncora, nome, ganho], ...]. O nome procura primeiro um ficheiro
    em D['sfx_banco'] (efeitos gravados, p. ex. ElevenLabs, com autorização) e, se não houver, o efeito sintetizado."""
    rng_ = np.random.default_rng(11)
    def ir(d=.6, dec=7.0):
        x = tt(d); return (rng_.normal(0, 1, len(x)) * np.exp(-x * dec)).astype(np.float32)
    def verb(x, mix=.25, d=.6, dec=7.0):
        r = np.convolve(x, ir(d, dec))[:len(x) + int(d * SR)] * (mix / 30); y = np.zeros(len(r), np.float32); y[:len(x)] += x; return (y + r).astype(np.float32)
    def lp(x, n): return np.convolve(x, np.ones(n) / n, 'same').astype(np.float32)
    def impacto(d=1.2):
        x = tt(d); sub = np.sin(2 * np.pi * (48 + 60 * np.exp(-x * 18)) * x) * np.exp(-x * 3.2)
        crack = rng_.normal(0, 1, len(x)) * np.exp(-x * 45); body = lp(rng_.normal(0, 1, len(x)), 8) * np.exp(-x * 9)
        return verb((sub * .95 + crack * .45 + body * .5).astype(np.float32), .35, .9, 5)
    def riser(d=1.0):
        x = tt(d); n = rng_.normal(0, 1, len(x)); e = (x / d) ** 2.2
        hp = n - lp(n, int(40 - 34 * 1)); tone = np.sin(2 * np.pi * np.cumsum(220 + 900 * (x / d) ** 2) / SR) * .18
        return ((hp * .35 + tone) * e).astype(np.float32)
    def scan(d=2.0):
        x = tt(d); fr = 600 + 2400 * x / d; s_ = np.sin(2 * np.pi * np.cumsum(fr) / SR) * (.5 + .5 * np.sign(np.sin(2 * np.pi * 14 * x)))
        return (s_ * .16 * np.minimum(1, x / .05) * np.minimum(1, (d - x) / .1) + lp(rng_.normal(0, 1, len(x)), 3) * .05).astype(np.float32)
    def tique(d=.05):
        x = tt(d); return (np.sin(2 * np.pi * 2600 * x) * np.exp(-x * 140) * .5 + rng_.normal(0, 1, len(x)) * np.exp(-x * 300) * .2).astype(np.float32)
    def carimbo(d=.5):
        x = tt(d); return verb((np.sin(2 * np.pi * 95 * x) * np.exp(-x * 22) * .9 + lp(rng_.normal(0, 1, len(x)), 4) * np.exp(-x * 60) * .7).astype(np.float32), .3, .5, 8)
    def woosh(d=.35):
        x = tt(d); n = rng_.normal(0, 1, len(x)); e = np.sin(np.pi * x / d) ** 2; k = (1 + 20 * (1 - x / d)).astype(int)
        y = np.array([0.0] * len(x), np.float32); acc = 0.0
        for j in range(len(x)): acc += (n[j] - acc) / (k[j] if k[j] > 0 else 1); y[j] = acc
        return (y * e * 1.6).astype(np.float32)
    def alfinete(d=.6):
        x = tt(d); return verb((np.sin(2 * np.pi * 1320 * x) * np.exp(-x * 9) * .35 + np.sin(2 * np.pi * 1980 * x) * np.exp(-x * 12) * .2 + np.sin(2 * np.pi * 70 * x) * np.exp(-x * 25) * .6).astype(np.float32), .4, .8, 5)
    def papel(d=2.0):
        x = tt(d); n = rng_.normal(0, 1, len(x)); step = (np.sin(2 * np.pi * 22 * x) > .6).astype(np.float32)
        motor = np.sin(2 * np.pi * 180 * x + 2 * np.sin(2 * np.pi * 22 * x)) * .08
        return ((lp(n, 3) - lp(n, 30)) * step * .3 + motor) * np.minimum(1, x / .08) * np.minimum(1, (d - x) / .15)
    def carta(d=.22):
        x = tt(d); n = rng_.normal(0, 1, len(x)); return ((n - lp(n, 6)) * np.exp(-x * 28) * .6 + np.sin(2 * np.pi * 160 * x) * np.exp(-x * 40) * .3).astype(np.float32)
    def brilho(d=1.4):
        x = tt(d); y = np.zeros(len(x), np.float32)
        for q, f0 in enumerate((1046.5, 1318.5, 1568.0, 2093.0)):
            xx = np.clip(x - q * .07, 0, None); y += (np.sin(2 * np.pi * f0 * xx + 1.5 * np.sin(2 * np.pi * f0 * 1.41 * xx) * np.exp(-xx * 4)) * np.exp(-xx * 3.5) * (x >= q * .07)).astype(np.float32) * .18
        return verb(y, .45, 1.0, 3.5)
    def ui(d=.12):
        x = tt(d); return (np.sin(2 * np.pi * np.cumsum(900 + 700 * x / d) / SR) * np.exp(-x * 25) * .4 + np.sin(2 * np.pi * 1800 * x) * np.exp(-x * 60) * .15).astype(np.float32)
    def fecho(d=1.5):
        x = tt(d); return verb((np.sin(2 * np.pi * 55 * x) * np.exp(-x * 2.5) * .8 + np.sin(2 * np.pi * 110 * x) * np.exp(-x * 4) * .3).astype(np.float32), .4, 1.2, 3)
    sint = dict(base, impacto=impacto, riser=riser, scan=scan, tique=tique, carimbo=carimbo, woosh=woosh, alfinete=alfinete,
                papel=papel, carta=carta, brilho=brilho, ui=ui, fecho=fecho)
    banco = {}
    for nome, f in (D.get('sfx_banco') or {}).items():
        if os.path.exists(HERE + f):
            raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', HERE + f, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
            x = np.frombuffer(raw, np.float32).copy(); banco[nome] = (x / max(1e-6, np.abs(x).max())).astype(np.float32)
    for c in D['sfx']:
        at, nome, g = _tempo(c[0]), c[1], c[2]; dur = c[3] if len(c) > 3 else None
        if nome in banco: x = banco[nome][:int(dur * SR)] if dur else banco[nome]
        else: x = sint[nome](dur) if dur else sint[nome]()
        if dur and nome in banco:
            fade = min(len(x), int(.08 * SR)); x = x.copy(); x[-fade:] *= np.linspace(1, 0, fade)
        put(np.asarray(x, np.float32), at, g)

def audio_previa(out='mix_previa.wav', sem_sfx=False):
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
    def stamp(d=0.18): x = tt(d); return (np.sin(2 * np.pi * 120 * x) * np.exp(-x * 30) * .7 + np.random.default_rng(4).normal(0, 1, len(x)) * np.exp(-x * 80) * .25).astype(np.float32)
    def whoosh(d=0.45):
        x = tt(d); r = np.random.default_rng(7).normal(0, 1, len(x)); e = np.sin(np.pi * x / d) ** 2
        lp = np.convolve(r, np.ones(24) / 24, 'same'); return (lp * e * .9).astype(np.float32)
    S = np.zeros(N, np.float32)
    def put(x, at, g): i = int(at * SR); n = min(len(x), N - i); S[i:i + n] += x[:n] * g
    if D.get('sfx'):                                            # MC-EP09 v2: lista de deixas nos dados (efeito ligado a cada movimento)
        _sfx_cues(put, tt, SR, dict(thump=thump, modem=modem, click=click, pop=pop, stamp=stamp, whoosh=whoosh))
    elif D.get('grade', {}).get('heroi'):                         # abertura do MC-EP08B: «tum» + carimbo na carta-herói no quadro 0
        put(thump(), 0, .9); put(stamp(), 0, .6); put(pop(), BEAT['NUM'], .55); put(click(), BEAT['HLB'], .4); put(click(), BEAT['HLB'] + .08, .3)
        if 'VOO' in BEAT: put(whoosh(), BEAT['VOO'], .6)
        put(stamp(), BEAT['DIVE'] - .05, .5)
    else:
        put(thump(), 0, .8); [put(click(), .04 * k, .45) for k in range(4)]
        put(modem(), BEAT['SCAN'], .5); put(pop(), BEAT['NUM'], .5); put(pop(f0=800, f1=1600), BEAT['HLB'], .5); put(click(), BEAT['Q'], .35)
    put(modem(), BEAT['DIVE'], .55); put(click(), BEAT['POP_BAR'], .35); put(pop(), BEAT['POP_A'], .45); put(pop(.09, 900, 1400), BEAT['POP_B'], .4)
    put(click(), BEAT['PERF_A'], .4); put(pop(f0=800, f1=1600), BEAT['PERF_B'], .5); put(click(), BEAT['PERF_DEN'], .4)
    put(thump(.4, 70), BEAT['LEIT'], .35); put(click(), BEAT['LEIT2'], .4)
    put(pop(), BEAT['DIF_PT'], .45); put(pop(f0=800, f1=1600), BEAT['DIF_VER'], .5); put(click(), BEAT['DIF_NOTA'], .3)
    put(click(), BEAT['ASK'], .4); put(thump(.4, 70), BEAT['CLOSE'], .3)
    import wave
    global _SFX; _SFX = S.copy()                                  # o audio_final junta os SFX sem ducking
    x = M * .9 + (0 if sem_sfx else S); x = (x / max(1e-6, np.abs(x).max()) * .9 * 32767).astype(np.int16)
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
    mix_trilha = audio_previa('so_trilha.wav', sem_sfx=True); Sfx = np.zeros(N, np.float32); Sfx[:min(N, len(_SFX))] = _SFX[:N]
    Sfx *= 0.6 * np.abs(V).max() / max(1e-6, np.abs(Sfx).max())        # SFX à parte, sem ducking (como no MC-EP08B): pico a 60 % do pico da voz
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', mix_trilha, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    M = np.zeros(N, np.float32); m = np.frombuffer(raw, np.float32)[:N]; M[:len(m)] = m
    env = np.convolve((np.abs(V) > 0.01).astype(np.float32), np.ones(int(.25 * SR)) / int(.25 * SR), 'same')
    duck = 10 ** (-12 * np.clip(env * 3, 0, 1) / 20)
    x = V * 1.0 + M * 0.55 * duck + Sfx; x = (x / max(1e-6, np.abs(x).max()) * .9 * 32767).astype(np.int16)
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

def render(out='MC_PREVIA_SEM_VOZ.mp4', audio=None):
    # Uma só codificação (26/11/2026, missão de engenharia): os quadros entram em bruto no mesmo grafo de filtros que junta
    # o fecho (antes: corpo.mp4 a CRF 18 e depois tudo recodificado outra vez). Mesmos filtros e parâmetros; menos uma
    # geração de compressão e ~13 s a menos por episódio. O fecho não tem faixa de áudio: silêncio com a duração dele.
    nf = int(round(BEAT['END'] * FPS)); outro = K + 'comum/outro/outro_binder_916.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', outro,
                          '-filter_complex', '[0:v]fps=30,format=yuv420p,setsar=1[v0];[1:v]scale=1080:1920,fps=30,format=yuv420p,setsar=1[v1];[v0][v1]concat=n=2:v=1:a=0[v]',
                          '-map', '[v]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', 'video_so.mp4'], stdin=subprocess.PIPE)
    for i in range(nf): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close()
    if p.wait(): raise SystemExit('ffmpeg falhou ao codificar o vídeo')
    a = audio or audio_previa()
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'video_so.mp4', '-i', a, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                    '-shortest', '-movflags', '+faststart', out], check=True)
    print(out)

if __name__ == '__main__':
    if MODO == 'final':
        _r = subprocess.run(['ffmpeg', '-v', 'error', '-i', ARGS[0], '-ac', '1', '-ar', '48000', '-f', 'f32le', '-'], capture_output=True).stdout
        _v = np.frombuffer(_r, np.float32); _h = 48000 // FPS
        _e = np.array([np.sqrt((_v[j * _h:(j + 1) * _h] ** 2).mean()) for j in range(len(_v) // _h)])
        ENV = _e / (np.percentile(_e[_e > 0.005], 95) if (_e > 0.005).any() else 1)
        render(D.get('saida', 'MC_FINAL.mp4'), audio_final(ARGS[0]))
    elif MODO == 'stills':
        for x in map(float, ARGS): frame(x).save(f'still_{x:05.2f}.png')
    elif MODO == 'previa': render(D.get('saida_previa', 'MC_PREVIA_SEM_VOZ.mp4'))

# ---------- capa v2 (19/11, 17h30): mesmo modelo §7.3, mais contraste e hierarquia ----------
def capa_v2():
    im = Image.new('RGB', (W, H), BG)
    for lado, y0, y1 in (('A', 0, 980), ('B', 900, 1920)):                               # arte das cartas reais ao fundo
        c = CARD[lado].convert('RGB'); cw, ch = c.size; art = c.crop((int(cw * .08), int(ch * .11), int(cw * .92), int(ch * .55)))
        hh = y1 - y0; ww = int(art.width * hh / art.height); art = art.resize((ww, hh), Image.LANCZOS); im.paste(art, ((W - ww) // 2, y0))
    im = im.filter(ImageFilter.GaussianBlur(6)); im = Image.blend(im, Image.new('RGB', (W, H), BG), 0.55)
    rain, _ = term_base(3.7); im = Image.blend(im, rain, 0.28).convert('RGBA')               # chuva de código por cima
    vg = Image.new('L', (W, H), 0); ImageDraw.Draw(vg).ellipse((-200, 200, W + 200, H - 100), fill=255)
    im = Image.composite(im, Image.new('RGBA', (W, H), BG + (255,)), vg.filter(ImageFilter.GaussianBlur(160)))
    d = ImageDraw.Draw(im, 'RGBA')
    l1, l2 = D.get('capa_l1', '[FRASE]'), D.get('capa_l2', '')                      # frase: 2 linhas, 3 palavras
    f1 = fit(d, l1, INTB, 150, 900); f2 = fit(d, l2, INTB, 118, 900)
    for txt, f, y, col in ((l1, f1, 330, WHITE), (l2, f2, 470, PH)):
        d.text((W / 2 + 5, y + 6), txt, font=f, fill=(0, 0, 0, 200), anchor='mm'); d.text((W / 2, y), txt, font=f, fill=col, anchor='mm')
    foco = str(D.get('capa_foco') or v('iA'))
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g); ff = fit(gd, foco, INTB, 330, 960)
    gd.text((W / 2, 790), foco, font=ff, fill=PH + (255,), anchor='mm')
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(34))); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(10))); im.alpha_composite(g)
    d = ImageDraw.Draw(im, 'RGBA'); s = D.get('capa_unidade', '')
    d.text((W / 2, 975), s, font=F(MONOB, 46), fill=(220, 235, 230, 255), anchor='mm')
    tubo = tubo_frame(0.5, 'desconfiado').crop((230, 380, 1010, 1080)).resize((640, 574), Image.LANCZOS).convert('RGBA')
    m = Image.new('L', tubo.size, 0); ImageDraw.Draw(m).ellipse((110, 50, tubo.width - 110, tubo.height + 220), fill=255); tubo.putalpha(m.filter(ImageFilter.GaussianBlur(55)))
    im.alpha_composite(tubo, (220, 1010))
    d = ImageDraw.Draw(im, 'RGBA'); d.rectangle((0, 1572, W, 1662), fill=(5, 10, 16, 240)); d.line((0, 1572, W, 1572), fill=EM + (255,), width=4)
    d.text((60, 1617), D.get('faixa', 'META EM CURTO · EP. NN'), font=F(MONOB, 50), fill=EM, anchor='lm')
    if D.get('faixa_collab'): d.text((W - 60, 1617), D['faixa_collab'], font=F(MONOB, 50), fill=AMBER, anchor='rm')
    im = im.convert('RGB'); im.save('CAPA.png')
    gr = im.crop((0, 240, W, 1680)); gr.save('CAPA_grelha.png'); gr.resize((270, 360), Image.LANCZOS).save('CAPA_grelha_mini.png')
    print('CAPA.png, CAPA_grelha.png, CAPA_grelha_mini.png')
if __name__ == '__main__' and MODO == 'capa': capa_v2()
