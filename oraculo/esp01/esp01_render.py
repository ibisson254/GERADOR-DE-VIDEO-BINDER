# Meta em Curto ESP01 · A comunidade falou: Precon em dupla · render (derivado de ep07_render.py)
# Uso, numa pasta de trabalho com tl.json, words.json, led_env.npy e mix_final.wav (saídas de esp01_audio.py):
#   python3 esp01_render.py /caminho/do/kit             -> ESP01_META_EM_CURTO.mp4
#   python3 esp01_render.py /caminho/do/kit stills 3 10 -> still_03.00.png ...
#   python3 esp01_render.py /caminho/do/kit capa        -> ESP01_CAPA.png
# Comentário de @diarioplaninauta usado com autorização do fundador (oraculo/autorizacoes/2026-11-13_esp01_diarioplaninauta.md); sem foto de perfil.
import os, json, math, subprocess, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
K = (sys.argv[1] if len(sys.argv) > 1 else '../..').rstrip('/') + '/'
W, H, FPS = 1080, 1920, 30
TL = json.load(open('tl.json')); WORDS = json.load(open('words.json'))
TEMPO, LEAD = TL['TEMPO'], TL['LEAD']
TOTAL, OUT = TL['TOTAL'], TL['OUT_START']
PAUSES = TL['PAUSES']
def vt(x): return x / TEMPO + LEAD + sum(d for a, d in PAUSES if x >= a)
for w in WORDS: w['vs'] = vt(w['s']); w['ve'] = vt(w['e'])
def ws(i): return WORDS[i]['vs']
ENV = np.load('led_env.npy')
MASTER = Image.open(K + 'oraculo/assets/tubo_mestra_916.png').convert('RGB')
_fc = {}
def F(p, s):
    if (p, s) not in _fc: _fc[(p, s)] = ImageFont.truetype(p, s)
    return _fc[(p, s)]
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'; MONOB = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
COND = '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf'; CONDB = '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf'
INTB = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'; INTSB = '/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf'; INTM = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
BG = (5, 10, 16); EM = (16, 185, 129); PH = (0, 255, 65); WHITE = (236, 241, 245); GREY = (120, 140, 150); RED = (255, 64, 64)
DIMG = (70, 120, 95)
SCR = (492, 566, 740, 792); SCX, SCY = (SCR[0] + SCR[2]) / 2, (SCR[1] + SCR[3]) / 2
EYES = [(518, 615, 596, 702), (634, 615, 709, 702)]; LED = (592, 828)
rng = np.random.default_rng(13)
GLY = '0123456789ABCDEF#*+=<>/:'
def ease(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)
def eio(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3
def typed(s, t0, t, cps=40): return s[:int(max(0, t - t0) * cps)]
def fit(d, s, path, size, maxw):
    while size > 20:
        f = F(path, size)
        if d.textlength(s, font=f) <= maxw: return f
        size -= 2
    return F(path, size)
def led_amp(t):
    fi = int(round(t * FPS)); return min(1, float(ENV[fi]) if fi < len(ENV) else 0)

# ---------- FORA: TUBO ----------
rain_cols = [dict(x=x, y=rng.uniform(0, 300), v=rng.uniform(40, 90)) for x in range(500, 736, 14)]
def tubo_frame(t, expr='analitico', zoom=1.0, cx=None, cy=None, red_led=False):
    im = MASTER.copy(); d = ImageDraw.Draw(im, 'RGBA'); fs = F(MONO, 13)
    for c in rain_cols:
        y = SCR[1] + ((c['y'] + t * c['v']) % (SCR[3] - SCR[1] + 40)) - 20
        for k in range(5):
            yy = y - k * 15
            if SCR[1] + 8 < yy < SCR[3] - 14 and not any(e[0] - 6 < c['x'] < e[2] + 6 and e[1] - 8 < yy < e[3] + 4 for e in EYES):
                a = int(150 * (1 - k / 5) * (0.6 if expr != 'desconfiado' else 0.2))
                d.text((c['x'], yy), GLY[int(t * 8 + k + c['x']) % len(GLY)], font=fs, fill=(0, 255, 65, a))
    sy = SCR[1] + ((t * 120) % (SCR[3] - SCR[1]))
    d.rectangle((SCR[0] + 14, sy, SCR[2] - 14, sy + 5), fill=(16, 185, 129, 22))
    lid = 0.0; bt = t % 4.3
    if bt < 0.14 and expr != 'erro': lid = math.sin(bt / 0.14 * math.pi)
    if expr == 'desconfiado': lid = max(lid, 0.45)
    if expr == 'confiante': lid = max(lid, 0.22)
    if lid > 0.01:
        for i, e in enumerate(EYES):
            h = (e[3] - e[1] + 4) * lid
            if expr == 'confiante' and lid < 0.5 and i == 1: h *= 0.4
            if expr == 'desconfiado' and i == 0: h *= 0.55          # um olho semicerrado
            d.rectangle((e[0] - 3, e[1] - 3, e[2] + 3, e[1] - 3 + h), fill=BG + (255,))
            d.line((e[0] - 3, e[1] - 3 + h, e[2] + 3, e[1] - 3 + h), fill=(16, 185, 129, 160), width=3)
    if expr == 'erro': im = glitch_eyes(im, t)
    d = ImageDraw.Draw(im, 'RGBA')
    a = led_amp(t)
    d.ellipse((LED[0] - 7, LED[1] - 7, LED[0] + 7, LED[1] + 7), fill=(8, 40, 26, 255))
    if red_led:
        on = int(t * 6) % 2 == 0           # 3 piscadelas secas por segundo
        if on:
            glow = Image.new('RGBA', (120, 120), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
            gd.ellipse((40, 40, 80, 80), fill=(255, 40, 40, 220)); glow = glow.filter(ImageFilter.GaussianBlur(14))
            im.paste(glow, (LED[0] - 60, LED[1] - 60), glow)
            d.ellipse((LED[0] - 6, LED[1] - 6, LED[0] + 6, LED[1] + 6), fill=(255, 120, 120, 255))
        else:
            d.ellipse((LED[0] - 6, LED[1] - 6, LED[0] + 6, LED[1] + 6), fill=(70, 10, 10, 255))
    elif a > 0.03:
        glow = Image.new('RGBA', (120, 120), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
        gd.ellipse((40, 40, 80, 80), fill=(16, 185, 129, int(200 * a))); glow = glow.filter(ImageFilter.GaussianBlur(14))
        im.paste(glow, (LED[0] - 60, LED[1] - 60), glow)
        d.ellipse((LED[0] - 6, LED[1] - 6, LED[0] + 6, LED[1] + 6), fill=(120, 255, 190, int(80 + 175 * a)))
    z = max(1.0, zoom) * (1 + 0.008 * (1 + math.sin(t * 1.3)) / 2)
    if cx is None: cx, cy = W / 2, H / 2
    if expr == 'erro':                       # tremor
        r = np.random.default_rng(int(t * 30)); cx += r.uniform(-7, 7); cy += r.uniform(-5, 5); z = max(z, 1.012)
    if abs(z - 1) > 1e-4:
        cw, ch = W / z, H / z; x0 = min(max(cx - cw / 2, 0), W - cw); y0 = min(max(cy - ch / 2, 0), H - ch)
        im = im.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
    return im
def glitch_eyes(im, t):
    """Erro de sistema: olhos duplicados (separação verde/vermelho) + fatias deslocadas no ecrã."""
    box = (SCR[0] + 6, SCR[1] + 6, SCR[2] - 6, SCR[3] - 6)
    reg = im.crop(box); r, g, b = reg.split()
    off = 9 + int(4 * math.sin(t * 40))
    red = Image.merge('RGB', (r, Image.new('L', reg.size, 0), Image.new('L', reg.size, 0)))
    red = ImageChops.offset(red, off, 0)
    grn = Image.merge('RGB', (Image.new('L', reg.size, 0), g, b))
    grn = ImageChops.offset(grn, -off, 0)
    reg2 = ImageChops.add(red, grn)
    rr = np.random.default_rng(int(t * 30) + 7); arr = np.array(reg2)
    for _ in range(4):
        y0 = rr.integers(0, arr.shape[0] - 12); hh = rr.integers(4, 14); sh = rr.integers(-18, 18)
        arr[y0:y0 + hh] = np.roll(arr[y0:y0 + hh], sh, axis=1)
    im.paste(Image.fromarray(arr), box[:2])
    return im

# ---------- DENTRO: terminal ----------
TERM_BG = Image.new('RGB', (W, H), BG)
_sl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); _d = ImageDraw.Draw(_sl)
for y in range(0, H, 4): _d.line((0, y, W, y), fill=(0, 0, 0, 60))
vig = Image.new('L', (W, H), 0); vd = ImageDraw.Draw(vig); vd.ellipse((-300, -200, W + 300, H + 200), fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(220)); SCANL = _sl
tcols = [dict(x=x, y=rng.uniform(0, H), v=rng.uniform(60, 160)) for x in range(30, W, 46)]
EGG0, EGG1 = ws(46) - .1, ws(67) - .1    # easter egg «30» na chuva de código = vida inicial do Gigante de Duas Cabeças clássico (o de Commander dobra para 60)
def mix_bg(col, a):   # cor já misturada com o fundo (o alfa do texto não é respeitado pelo Pillow aqui)
    return tuple(int(BG[i] + (col[i] - BG[i]) * a / 255) for i in range(3))
def term_base(t, alpha=36):
    im = TERM_BG.copy(); d = ImageDraw.Draw(im, 'RGBA'); fs = F(MONO, 24)
    for c in tcols:
        y = (c['y'] + t * c['v']) % (H + 200) - 100
        for k in range(9):
            ch = GLY[int(t * 6 + k * 3 + c['x']) % len(GLY)]
            d.text((c['x'], y - k * 30), ch, font=fs, fill=mix_bg(PH, alpha * (1 - k / 9)))
    if EGG0 <= t < EGG1:
        for k, ch in enumerate('30'): d.text((tcols[22]['x'], 1250 + k * 30), ch, font=fs, fill=mix_bg(PH, 90))
    return im, d
def term_finish(im):
    im = Image.composite(im, Image.new('RGB', (W, H), (0, 0, 0)), vig); im.paste(SCANL, (0, 0), SCANL); return im
def hud(d, t):
    a = led_amp(t)
    d.ellipse((80, 1676, 100, 1696), fill=(16, 185, 129, int(70 + 185 * a)))
    d.text((114, 1686), 'BINDER', font=F(MONOB, 28), fill=(16, 185, 129, 220), anchor='lm')
    d.text((W - 80, 1686), 'META EM CURTO · ESPECIAL', font=F(MONO, 26), fill=(150, 170, 175, 220), anchor='rm')
def fontes(d, linhas, y=1384):
    """Linha(s) de fonte, ≥ 24 px de altura de letra (corrige o EP01)."""
    for i, s in enumerate(linhas):
        f = fit(d, s, COND, 34, W - 160)
        d.text((80, y + i * 44), s, font=f, fill=(150, 170, 175, 235))

# ---------- legendas palavra a palavra ----------
def chunks():
    out = []; cur = []
    for w in WORDS:
        cur.append(w)
        if w['t'][-1] in '.,:?!' or len(cur) >= 4: out.append(cur); cur = []
    if cur: out.append(cur)
    return out
CH = chunks()
def subs(im, t, y=1540):
    d = ImageDraw.Draw(im, 'RGBA')
    for c in CH:
        if c[0]['vs'] - 0.05 <= t <= c[-1]['ve'] + 0.12:
            f = F(MONOB, 50); txt = [w['t'].upper() for w in c]
            sp = d.textlength(' ', font=f); tot = sum(d.textlength(s, font=f) for s in txt) + sp * (len(txt) - 1)
            if tot > W - 160:
                f = fit(d, ' '.join(txt), MONOB, 50, W - 160); sp = d.textlength(' ', font=f)
                tot = sum(d.textlength(s, font=f) for s in txt) + sp * (len(txt) - 1)
            x = (W - tot) / 2
            d.rounded_rectangle((x - 24, y - 50, x + tot + 24, y + 28), 12, fill=(5, 10, 16, 210))
            for w, s in zip(c, txt):
                on = t >= w['vs'] - 0.03
                d.text((x, y), s, font=f, fill=(PH if on else (60, 90, 75)), anchor='ls'); x += d.textlength(s, font=f) + sp
            break
    return im
def top_card(im, lines, k=1.0, y=210):
    d = ImageDraw.Draw(im, 'RGBA')
    for s, font, col in lines:
        d.text((W / 2, y), s, font=font, fill=col + (int(255 * k),), anchor='ma'); y += font.size * 1.15
    return im



# ---------- ESP01: dados (fontes em fontes.txt) ----------
AMBER = (255, 176, 32)
EGGCOL = 22
def stamp(d, txt, col, t0, t, y, size=40):
    if t < t0: return
    k = eio((t - t0) / 0.18); f = F(MONOB, int(size + 14 * (1 - k)))
    wd = d.textlength(txt, font=f) + 50
    d.rounded_rectangle((W / 2 - wd / 2, y - 34, W / 2 + wd / 2, y + 34), 10, outline=col, width=4)
    d.text((W / 2, y), txt, font=f, fill=col, anchor='mm')
def wrap2(d, s, font, maxw):
    if d.textlength(s, font=font) <= maxw: return [s]
    p = s.split(); best = None
    for i in range(1, len(p)):
        a, b = ' '.join(p[:i]), ' '.join(p[i:]); m = max(d.textlength(a, font=font), d.textlength(b, font=font))
        if best is None or m < best[0]: best = (m, [a, b])
    return best[1]
SIL = ["......####......", ".....######.....", "....########....", "....########....", "....########....",
       ".....######.....", "......####......", "...##########...", "..############..", ".##############.",
       ".##############.", "################", "################"]
def silhueta(d, x, y, px=13, col=PH):
    for r, row in enumerate(SIL):
        for c, ch in enumerate(row):
            if ch == '#': d.rectangle((x + c * px, y + r * px, x + c * px + px - 2, y + r * px + px - 2), fill=mix_bg(col, 150))
COMENT = ['Existe um formato de torneio de Precon', 'que está se popularizando muito que é o', '2x2 (Precon em duplas). A própria',
          '@montcardshop já fez torneios valendo', '3k. Eu amo o formato Precon, mas acho', 'que para torneios grandes o 2x2 é o ideal', 'mesmo.']
def wrapw(d, s, font, maxw):
    out, cur = [], ''
    for w in s.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: out.append(cur); cur = w
    if cur: out.append(cur)
    return out

# ---------- DENTRO ----------
def scene_comentario(t):
    im, d = term_base(t, 18)
    t0 = DIVE_END - 0.1
    s1 = '> ARQUIVO: COMENTÁRIO DA COMUNIDADE'
    d.text((80, 200), typed(s1, t0, t), font=fit(d, s1, MONOB, 38, 920), fill=PH)
    d.text((80, 258), typed('  num post do @binderthetrade · novembro de 2026', t0 + .3, t), font=F(MONO, 28), fill=EM)
    d.line((80, 312, 1000, 312), fill=(16, 185, 129, 90), width=2)
    # ficha do autor: silhueta (sem foto de perfil)
    d.rounded_rectangle((80, 345, 1000, 520), 16, outline=EM, width=3, fill=(8, 20, 18, 255))
    silhueta(d, 110, 368, 10)
    d.text((300, 380), 'DIÁRIO PLANINAUTA', font=F(INTB, 54), fill=WHITE)
    d.text((300, 452), '@diarioplaninauta', font=F(MONOB, 34), fill=PH)
    # o comentário, palavra por palavra
    if t >= ws(15) - .3:
        d.rounded_rectangle((80, 550, 1000, 1080), 16, outline=(40, 80, 70), width=2, fill=(8, 16, 20, 255))
        f = F(COND, 40); full = ' '.join(COMENT); shown = typed(full, DIVE_END + 0.3, t, 60)
        y = 580
        for ln in wrapw(d, shown, f, 860):
            d.text((110, y), ln, font=f, fill=(200, 220, 215)); y += 54
        if t >= ws(29) - .05:      # «Precon em dupla é o ideal»
            stamp(d, '2x2 = IDEAL PARA TORNEIO GRANDE', PH, ws(29), t, 1010, 34)
    if t >= ws(39) - .05:          # «Montcard»
        d.rounded_rectangle((80, 1110, 1000, 1290), 16, outline=AMBER, width=3, fill=(20, 16, 8, 255))
        d.text((110, 1130), '@montcardshop', font=F(MONOB, 40), fill=WHITE)
        d.text((110, 1185), 'torneios de 2x2 valendo 3k', font=F(COND, 38), fill=(220, 200, 160))
        d.text((110, 1238), 'relato do comentário · não verificado', font=F(MONOB, 28), fill=AMBER)
    fontes(d, ['fonte: comentário público no @binderthetrade (nov/2026)'], 1384)
    hud(d, t); return term_finish(im)
def scene_regras(t):
    im, d = term_base(t, 16)
    d.text((80, 200), '> REGRAS · COMMANDER EM DUPLA', font=F(MONOB, 36), fill=PH)
    d.text((80, 252), '  Gigante de Duas Cabeças · versão oficial', font=F(MONO, 28), fill=EM)
    d.line((80, 304, 1000, 304), fill=(16, 185, 129, 90), width=2)
    if t >= ws(46) + .2:           # «Na versão oficial»
        d.rounded_rectangle((80, 340, 1000, 560), 16, outline=EM, width=3, fill=(8, 20, 18, 255))
        d.text((110, 362), 'POR JOGADOR', font=F(MONOB, 32), fill=GREY)
        d.text((110, 410), '1 DECK · 100 CARTAS', font=F(INTB, 72), fill=WHITE)
    if t >= ws(60) - .05:          # «A dupla divide»
        d.rounded_rectangle((80, 600, 1000, 900), 16, outline=PH, width=4, fill=(8, 24, 16, 255))
        d.text((110, 622), 'POR DUPLA · VIDA COMPARTILHADA', font=F(MONOB, 32), fill=GREY)
        k = eio((t - ws(63) + .05) / .3) if t >= ws(63) - .05 else 0
        if k > 0: d.text((W / 2, 680), '60', font=F(INTB, int(150 + 40 * k)), fill=PH, anchor='ma')
    if t >= ws(64) - .05:
        d.text((W / 2, 960), 'mesa comum de Commander: 40 por jogador', font=F(COND, 38), fill=(170, 190, 195), anchor='ma')
    fontes(d, ['Wizards Play Network: Noite de Commander · Gigante de Duas Cabeças', 'Commander: magic.wizards.com/formats/commander'], 1384)
    hud(d, t); return term_finish(im)
def pessoa(d, x, y, col, on):
    d.ellipse((x - 26, y - 70, x + 26, y - 18), fill=(col if on else None), outline=col, width=4)
    d.rounded_rectangle((x - 44, y - 10, x + 44, y + 60), 20, fill=(col if on else None), outline=col, width=4)
def scene_conta(t):
    im, d = term_base(t, 14)
    d.text((80, 200), '> MODELO SEM HABILIDADE', font=F(MONOB, 36), fill=PH)
    d.text((80, 252), '  todos com a mesma força · quem começa ganhando?', font=fit(d, '  todos com a mesma força · quem começa ganhando?', MONO, 28, 920), fill=EM)
    d.line((80, 304, 1000, 304), fill=(16, 185, 129, 90), width=2)
    # esquerda: mesa de 4
    d.rounded_rectangle((70, 340, 520, 1180), 18, outline=(40, 80, 70), width=2, fill=(8, 16, 20, 255))
    d.text((295, 362), 'MESA DE 4', font=F(MONOB, 38), fill=WHITE, anchor='ma')
    for i, (x, y) in enumerate([(200, 520), (390, 520), (200, 720), (390, 720)]):
        pessoa(d, x, y, (PH if i == 0 else (90, 130, 115)), i == 0 and t >= ws(70) - .05)
    if t >= ws(70) - .05: d.text((295, 830), '1 vencedor', font=F(MONO, 32), fill=GREY, anchor='ma')
    if t >= ws(72) - .05:
        k = eio((t - ws(72) + .05) / .3); d.text((295, 900), '25%', font=F(INTB, int(110 + 30 * k)), fill=WHITE, anchor='ma')
        d.text((295, 1080), '1 em 4', font=F(MONO, 30), fill=GREY, anchor='ma')
    # direita: 2 contra 2
    if t >= ws(79) - .05:
        d.rounded_rectangle((560, 340, 1010, 1180), 18, outline=EM, width=3, fill=(8, 22, 18, 255))
        d.text((785, 362), 'DOIS CONTRA DOIS', font=F(MONOB, 34), fill=WHITE, anchor='ma')
        for x, y in [(690, 520), (880, 520)]: pessoa(d, x, y, PH, True)
        d.text((785, 610), 'VS', font=F(MONOB, 34), fill=GREY, anchor='ma')
        for x, y in [(690, 720), (880, 720)]: pessoa(d, x, y, (90, 130, 115), False)
        if t >= ws(82) - .05:
            k = eio((t - ws(82) + .05) / .3); d.text((785, 900), '50%', font=F(INTB, int(110 + 30 * k)), fill=PH, anchor='ma')
            d.text((785, 1080), '1 em 2', font=F(MONO, 30), fill=GREY, anchor='ma')
    if t >= ws(87) - .05: stamp(d, 'ANTES DA PRIMEIRA CARTA', AMBER, ws(87), t, 1270, 36)
    fontes(d, ['cálculo nosso: chance de base, jogadores de força igual', 'modelo sem habilidade · não é win rate'], 1384)
    hud(d, t); return term_finish(im)
def scene_binario(t):
    im, d = term_base(t, 14)
    d.text((80, 200), '> RESULTADO DE CADA MESA', font=F(MONOB, 36), fill=PH)
    d.text((80, 252), '  o que o chaveamento precisa ler', font=F(MONO, 28), fill=EM)
    d.line((80, 304, 1000, 304), fill=(16, 185, 129, 90), width=2)
    d.text((80, 350), 'MESA DE 4', font=F(MONOB, 34), fill=GREY)
    for k, s_ in enumerate(['1º', '2º', '3º', '4º']):
        x = 80 + k * 230; d.rounded_rectangle((x, 400, x + 200, 520), 14, outline=(90, 130, 115), width=3)
        d.text((x + 100, 460), s_, font=F(INTB, 64), fill=(170, 190, 195), anchor='mm')
    d.text((80, 545), 'colocação · pontos por posição', font=F(COND, 32), fill=GREY)
    if t >= ws(93) - .05:
        d.text((80, 640), 'DOIS CONTRA DOIS', font=F(MONOB, 34), fill=PH)
        for k, (s_, c) in enumerate([('VITÓRIA', PH), ('DERROTA', RED)]):
            x = 80 + k * 470; d.rounded_rectangle((x, 690, x + 450, 830), 16, outline=c, width=4, fill=(8, 20, 18, 255))
            d.text((x + 225, 760), s_, font=F(INTB, 64), fill=c, anchor='mm')
        d.text((80, 855), 'binário · como no 1 contra 1', font=F(COND, 32), fill=GREY)
    if t >= ws(104) - .05: stamp(d, 'SUÍÇO: VITÓRIA OU DERROTA', PH, ws(104), t, 1010, 38)
    fontes(d, ['leitura do TUBO: o pareamento suíço foi feito para resultados V/D', 'empates continuam possíveis nos dois formatos'], 1384)
    hud(d, t); return term_finish(im)

# ---------- timeline ----------
DIVE = TL['DIVE']; DIVE_END = DIVE + 0.45; EXIT = TL['EXIT']; EXIT_END = EXIT + 0.75
REV0, REV1 = TL['REV0'], TL['REV1']
T_Q = ws(129) - 0.1; T_SIG = ws(149) - 0.15
def inside(t):
    if t < ws(46) - .1: return scene_comentario(t)
    if t < ws(67) - .1: return scene_regras(t)
    if t < ws(91) - .1: return scene_conta(t)
    return scene_binario(t)
SUBY = 1530
def note(d, s):
    f = F(COND, 34); wd = d.textlength(s, font=f)
    d.rounded_rectangle((W / 2 - wd / 2 - 16, 1418, W / 2 + wd / 2 + 16, 1468), 8, fill=(5, 10, 16, 215))
    d.text((W / 2, 1443), s, font=f, fill=(170, 190, 195), anchor='mm')
def meter(d, y, n, lab='GRAU DE CERTEZA'):
    d.text((90, y + 20), lab, font=F(MONOB, 28), fill=GREY, anchor='lm')
    for s in range(5):
        x = 420 + s * 66
        d.rounded_rectangle((x, y, x + 56, y + 40), 7, fill=(EM if s < n else None), outline=EM, width=3)
    d.text((990, y + 20), f'{n} de 5', font=F(MONOB, 30), fill=EM, anchor='rm')
# ---------- OUTRO: ficheiro real do fecho ----------
def load_outro():
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', K + 'comum/outro/outro_binder_916.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                         capture_output=True).stdout
    n = len(raw) // (W * H * 3)
    return [Image.frombuffer('RGB', (W, H), raw[i * W * H * 3:(i + 1) * W * H * 3]) for i in range(n)]
OUTRO = None
def outro(t):
    global OUTRO
    if OUTRO is None: OUTRO = load_outro()
    return OUTRO[min(len(OUTRO) - 1, int(t * FPS))].copy()
def frame(t):
    if t >= OUT: return outro(t - OUT)
    if t >= OUT - 0.2:
        a = (t - (OUT - 0.2)) / 0.2; return Image.blend(frame_main(OUT - 0.21), outro(0), a)
    return frame_main(t)
def frame_main(t):
    if t < DIVE_END:
        if t < DIVE:
            im = tubo_frame(t, 'desconfiado' if t < ws(11) else 'confiante', zoom=1.0 + 0.04 * eio(t / 3.0))
            d = ImageDraw.Draw(im, 'RGBA')
            d.text((290, 170), 'MESA DE 4', font=F(MONOB, 44), fill=GREY, anchor='ma')
            d.text((290, 225), '25%', font=F(INTB, 130), fill=WHITE, anchor='ma')
            if t >= ws(11) - .05:
                d.text((790, 170), 'EM DUPLA', font=F(MONOB, 44), fill=GREY, anchor='ma')
                d.text((790, 225), '50%', font=F(INTB, 130), fill=PH, anchor='ma')
            note(d, 'chance de base · jogadores de força igual')
            return subs(im, t, SUBY)
        k = eio((t - DIVE) / (DIVE_END - DIVE)); z = 1 + k * 4.2
        im = tubo_frame(t, 'analitico', zoom=z, cx=W / 2 + (SCX - W / 2) * min(1, k * 1.5), cy=H / 2 + (SCY - H / 2) * min(1, k * 1.5))
        if k > 0.6: im = Image.blend(im, scene_comentario(t), (k - 0.6) / 0.4)
        return im
    if t < EXIT: return subs(inside(t), t)
    if t < EXIT_END:
        k = eio((t - EXIT) / (EXIT_END - EXIT)); z = 5.2 - 4.2 * k
        im = tubo_frame(t, 'confiante', zoom=z, cx=W / 2 + (SCX - W / 2) * (1 - k), cy=H / 2 + (SCY - H / 2) * (1 - k))
        if k < 0.35: im = Image.blend(inside(t), im, k / 0.35)
        return subs(im, t, SUBY)
    if t < T_Q:
        im = tubo_frame(t, 'confiante', zoom=1.0 + .03 * eio((t - EXIT_END) / 3)); d = ImageDraw.Draw(im, 'RGBA')
        if t >= ws(107) - .05: d.text((W / 2, 140), 'PRECON IGUALA OS DECKS.', font=fit(d, 'PRECON IGUALA OS DECKS.', INTB, 72, 960), fill=GREY, anchor='ma')
        if t >= ws(111) - .05: d.text((W / 2, 225), 'A DUPLA IGUALA A MESA.', font=fit(d, 'A DUPLA IGUALA A MESA.', INTB, 84, 960), fill=PH, anchor='ma')
        if t >= ws(116) - .05:
            meter(d, 335, 3 if t >= ws(119) - .05 else 0)
            if t >= ws(122) - .05:
                s_ = 'win rate de 2x2 de Precon: nenhum publicado na nossa pesquisa (13/11)'
                d.text((W / 2, 392), s_, font=fit(d, s_, COND, 30, 960), fill=(170, 190, 195), anchor='ma')
        note(d, 'leitura do TUBO · opinião, não dado medido')
        return subs(im, t, SUBY)
    if t < T_SIG:
        im = tubo_frame(t, 'analitico', zoom=1.0); d = ImageDraw.Draw(im, 'RGBA')
        q = 'Torneio grande de Precon:'
        d.text((W / 2, 130), q, font=fit(d, q, INTB, 64, 960), fill=WHITE, anchor='ma')
        ops = [('A', 'mesa de 4', 133), ('B', 'dois contra dois', 137), ('C', 'depende do prêmio', 141)]
        for i, (l, s_, wi) in enumerate(ops):
            if t < ws(wi) - .05: continue
            y = 215 + i * 64; on = t >= ws(145) - .05
            d.rounded_rectangle((170, y, 910, y + 54), 27, fill=((10, 52, 30, 255) if on else (15, 23, 42, 230)), outline=EM, width=3)
            d.text((215, y + 27), l, font=F(MONOB, 36), fill=PH, anchor='mm')
            d.text((560, y + 27), s_, font=F(CONDB, 38), fill=(PH if on else WHITE), anchor='mm')
        if t >= ws(145) - .05: note(d, 'responda com a letra')
        return subs(im, t, SUBY)
    kz = eio((t - T_SIG) / 1.2)
    im = tubo_frame(t, 'confiante', zoom=1.0 + 0.22 * kz, cx=W / 2, cy=H / 2 + (SCY + 260 - H / 2) * kz)
    k = ease((t - T_SIG) / 0.4)
    im = top_card(im, [('META EM CURTO', F(INTB, 96), WHITE), ('com TUBO · BINDER Originals', F(MONO, 34), EM)], k, 225)
    return subs(im, t, SUBY)
if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[2] == 'capa':
        im = tubo_frame(12.0, 'confiante', zoom=1.0); d = ImageDraw.Draw(im, 'RGBA')
        d.text((W / 2, 110), 'PRECON EM DUPLA', font=F(INTB, 104), fill=WHITE, anchor='ma')
        d.text((W / 2, 240), '25% × 50%', font=F(INTB, 120), fill=PH, anchor='ma')
        d.text((W / 2, 400), 'O TUBO FEZ A CONTA', font=F(MONOB, 54), fill=AMBER, anchor='ma')
        d.text((W / 2, 1470), 'META EM CURTO · ESPECIAL', font=F(MONOB, 40), fill=WHITE, anchor='ma')
        im.convert('RGB').save('ESP01_CAPA.png'); sys.exit()
    if len(sys.argv) > 2 and sys.argv[2] == 'stills':
        for tt in map(float, sys.argv[3:]): frame(tt).save(f'still_{tt:05.2f}.png')
        sys.exit()
    nf = int(round(TOTAL * FPS))
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-i', 'mix_final.wav', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
                          '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', '-shortest', 'ESP01_META_EM_CURTO.mp4'],
                         stdin=subprocess.PIPE)
    for i in range(nf): p.stdin.write(frame(i / FPS).convert('RGB').tobytes())
    p.stdin.close(); p.wait(); print('done', nf)
