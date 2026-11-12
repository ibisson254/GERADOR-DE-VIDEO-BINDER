# Meta em Curto EP03 · Arquivo Competitivo · render (derivado de ep02_render.py)
# Uso, numa pasta de trabalho com tl.json, words.json, led_env.npy e mix_final.wav (saídas de ep03_audio.py):
#   python3 ep03_render.py /caminho/do/kit             -> EP03_META_EM_CURTO.mp4
#   python3 ep03_render.py /caminho/do/kit stills 3 10 -> still_03.00.png ...
# O fecho é o ficheiro real comum/outro/outro_binder_916.mp4 (sem áudio; a trilha do episódio continua por baixo).
import json, math, subprocess, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
K = (sys.argv[1] if len(sys.argv) > 1 else '../..').rstrip('/') + '/'
W, H, FPS = 1080, 1920, 30
TL = json.load(open('tl.json')); WORDS = json.load(open('words.json'))
TEMPO, LEAD = TL['TEMPO'], TL['LEAD']
TOTAL, OUT = TL['TOTAL'], TL['OUT_START']
def vt(x): return x / TEMPO + LEAD
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
EGG0, EGG1 = 8.0, 9.0          # easter egg «LOAM» na chuva de código (segundos do vídeo)
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
        for k, ch in enumerate('LOAM'): d.text((tcols[21]['x'], 1180 + k * 30), ch, font=fs, fill=mix_bg(PH, 80))
    return im, d
def term_finish(im):
    im = Image.composite(im, Image.new('RGB', (W, H), (0, 0, 0)), vig); im.paste(SCANL, (0, 0), SCANL); return im
def hud(d, t):
    a = led_amp(t)
    d.ellipse((80, 1676, 100, 1696), fill=(16, 185, 129, int(70 + 185 * a)))
    d.text((114, 1686), 'BINDER', font=F(MONOB, 28), fill=(16, 185, 129, 220), anchor='lm')
    d.text((W - 80, 1686), 'META EM CURTO · EP03', font=F(MONO, 26), fill=(150, 170, 175, 220), anchor='rm')
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



# ---------- DENTRO: o arquivo ----------
AMBER = (255, 176, 32)
def header(d, t, t0):
    d.text((80, 200), typed('> ARQUIVO COMPETITIVO', t0, t), font=F(MONOB, 40), fill=PH)
    d.text((80, 258), typed('  FIM DE SEMANA · 31/10–01/11/2026', t0 + 0.4, t), font=F(MONO, 30), fill=EM)
    d.line((80, 312, 1000, 312), fill=(16, 185, 129, 90), width=2)
IDX = [('01', 'PITTSBURGH', 'LEGACY · VINTAGE'), ('02', 'PEQUIM', 'STANDARD'),
       ('03', 'TAIPEI', 'FORMATO ?'), ('04', 'SÃO PAULO', 'COMMANDER')]
def estado(i, t):
    if i == 0 and t >= ws(37): return ('VERIFICADO', EM)
    if i == 1 and t >= ws(63): return ('VERIFICADO', EM)
    if i == 2 and t >= ws(77): return ('INCOMPLETO', AMBER)
    if i == 3: return ('FORA DO ARQUIVO', GREY)
    return ('...', DIMG)
def indice(d, t, cur):
    y = 340
    for i, (n, cid, fmt) in enumerate(IDX):
        on = i == cur
        col = PH if on else (WHITE if i < cur else DIMG)
        if on: d.rounded_rectangle((60, y - 8, 1020, y + 52), 10, fill=(10, 40, 24, 255))
        if on: d.text((70, y + 22), '▶', font=F(MONOB, 26), fill=PH, anchor='lm')
        d.text((104, y + 22), f'{n} {cid}', font=F(MONOB, 34), fill=col, anchor='lm')
        d.text((470, y + 22), fmt, font=F(MONO, 28), fill=(col if on else GREY), anchor='lm')
        s, sc = estado(i, t)
        d.text((1000, y + 22), s, font=F(MONOB, 26), fill=sc, anchor='rm')
        y += 66
def painel(d, title, sub, t0, t):
    d.rounded_rectangle((60, 630, 1020, 1350), 18, outline=(16, 185, 129, 150), width=3, fill=(8, 20, 18, 255))
    f = fit(d, title, INTB, 60, 880)
    d.text((W / 2, 668), title, font=f, fill=WHITE, anchor='ma')
    d.text((W / 2, 748), typed(sub, t0, t, 50), font=F(MONO, 30), fill=EM, anchor='ma')
def stamp(d, txt, col, t0, t, y=1270):
    if t < t0: return
    k = eio((t - t0) / 0.18); f = F(MONOB, int(40 + 14 * (1 - k)))
    wd = d.textlength(txt, font=f) + 50
    d.rounded_rectangle((W / 2 - wd / 2, y - 34, W / 2 + wd / 2, y + 34), 10, outline=col, width=4)
    d.text((W / 2, y), txt, font=f, fill=col, anchor='mm')
def money(v): return 'US$ ' + f'{v:,}'.replace(',', '.')
def scene_pitt(t):
    im, d = term_base(t, 22); header(d, t, DIVE_END - 0.2); indice(d, t, 0)
    painel(d, 'ETERNAL WEEKEND', 'AMÉRICA DO NORTE · 29/10–01/11', ws(15), t)
    for j, (lab, val, i0, ich, champ) in enumerate([('LEGACY', 50000, 17, 20, (10000, 33)), ('VINTAGE', 20000, 25, 28, (5000, 36))]):
        y = 830 + j * 190
        if t >= ws(i0): d.text((100, y), lab, font=F(MONOB, 36), fill=WHITE)
        if t >= ws(ich):
            k = eio((t - ws(ich)) / 0.5); bw = int(560 * val / 50000 * k)
            d.rectangle((100, y + 56, 100 + bw, y + 104), fill=EM)
            d.text((100 + bw + 18, y + 80), money(int(val * k)) + ('+' if k >= 1 else ''), font=F(MONOB, 36), fill=PH, anchor='lm')
            d.text((100, y + 116), 'em prêmios', font=F(MONO, 26), fill=GREY)
        if t >= ws(champ[1]):
            d.text((980, y), '1.º ' + money(champ[0]), font=F(INTB, 44), fill=WHITE, anchor='ra')
    stamp(d, '✓ VERIFICADO', EM, ws(37), t)
    fontes(d, ['fonte: Pastimes (organizador) · prêmios · consulta 01/11/2026', 'datas: magic.gg · Eternal Weekend 2026'])
    hud(d, t); return term_finish(im)
def scene_pequim(t):
    im, d = term_base(t, 22); header(d, t, -9); indice(d, t, 1)
    painel(d, 'MAGIC SPOTLIGHT: FRACTURE', 'STANDARD · PEQUIM · 31/10–01/11', ws(38), t)
    if t >= ws(43):
        k = eio((t - ws(43)) / (ws(48) - ws(43) + 0.3)); n = int(869 * k)
        d.text((W / 2, 800), str(n), font=F(INTB, 190), fill=PH, anchor='ma')
        d.text((W / 2, 1000), 'JOGADORES', font=F(MONOB, 34), fill=GREY, anchor='ma')
    if t >= ws(49): d.text((W / 2, 1060), typed('PRÊMIOS: ' + money(50000), ws(49), t, 50), font=F(MONOB, 40), fill=WHITE, anchor='ma')
    if t >= ws(54):
        d.text((W / 2, 1128), typed('TOP 8 → CONVITE · PRO TOUR TÓQUIO', ws(54), t, 50), font=fit(d, 'TOP 8 → CONVITE · PRO TOUR TÓQUIO', MONOB, 38, 860), fill=EM, anchor='ma')
        for s in range(8):
            on = t >= ws(56) + s * 0.12; x = W / 2 - 4 * 70 + s * 70 + 8
            d.rounded_rectangle((x, 1182, x + 54, 1214), 6, fill=(PH if on else None), outline=EM, width=3)
    stamp(d, '✓ VERIFICADO', EM, ws(63), t, 1278)
    fontes(d, ['fonte: Kadou Events (organizador) · prêmio e convites · 01/11/2026', 'jogadores: PlayMTG no X · 31/10/2026'])
    hud(d, t); return term_finish(im)
def scene_taipei(t):
    im, d = term_base(t, 22); header(d, t, -9); indice(d, t, 2)
    painel(d, 'MIT CHAMPIONSHIP', 'TAIPEI · 31/10–01/11', ws(64), t)
    rows = [('EVENTO', 'CONFIRMADO', 67, EM), ('FORMATO', '???', 74, AMBER), ('PREMIAÇÃO', '???', 76, AMBER)]
    y = 850
    for lab, val, i0, col in rows:
        if t >= ws(i0):
            d.text((120, y), lab, font=F(MONOB, 44), fill=WHITE)
            blink = col == AMBER and t >= ws(77) and int(t * 4) % 2 == 0 and t < ws(79)
            d.text((960, y), val, font=F(MONOB, 48), fill=(RED if blink else col), anchor='ra')
            if col == AMBER and t >= ws(80):
                k = eio((t - ws(80)) / 0.35)
                d.line((110, y + 28, 110 + 860 * k, y + 28), fill=RED, width=5)
        y += 100
    if t >= ws(77): stamp(d, 'SEM FONTE', RED, ws(77), t, 1180)
    if t >= ws(82): d.text((W / 2, 1268), typed('→ NÃO ENTRA NO TUBO', ws(82), t, 40), font=F(MONOB, 40), fill=AMBER, anchor='ma')
    fontes(d, ['fonte: magic.gg · calendário (31/10–01/11/2026)', 'formato e premiação desta edição: sem fonte publicada'])
    hud(d, t); return term_finish(im)

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

# ---------- timeline ----------
DIVE = TL['DIVE']; DIVE_END = DIVE + 0.45; EXIT = TL['EXIT']; EXIT_END = EXIT + 0.75
T_PEQ = ws(38) - 0.1; T_TAI = ws(64) - 0.1
T_SP = EXIT_END; T_Q = ws(103) - 0.1; T_SIG = ws(118) - 0.15
def inside(t):
    if t < T_PEQ: return scene_pitt(t)
    if t < T_TAI: return scene_pequim(t)
    return scene_taipei(t)
def frame(t):
    if t >= OUT: return outro(t - OUT)
    if t >= OUT - 0.2:
        a = (t - (OUT - 0.2)) / 0.2; return Image.blend(frame_main(OUT - 0.21), outro(0), a)
    return frame_main(t)
def frame_main(t):
    if t < DIVE_END:
        if t < DIVE:
            im = tubo_frame(t, 'desconfiado' if t < ws(9) else 'confiante', zoom=1.0 + 0.04 * eio(t / 3.0))
            d = ImageDraw.Draw(im, 'RGBA')
            if t >= ws(0):
                k = eio((t - ws(0)) / 0.25)
                d.text((W / 2, 150 + (1 - k) * 20), '4 EVENTOS', font=F(INTB, 130), fill=WHITE + (int(255 * k),), anchor='ma')
            if t >= ws(9):
                k = eio((t - ws(9)) / 0.25)
                d.text((W / 2, 320), '→ 3 NO ARQUIVO', font=F(INTB, 84), fill=PH + (int(255 * k),), anchor='ma')
            return subs(im, t, 1640)
        k = eio((t - DIVE) / (DIVE_END - DIVE)); z = 1 + k * 4.2
        im = tubo_frame(t, 'analitico', zoom=z, cx=W / 2 + (SCX - W / 2) * min(1, k * 1.5), cy=H / 2 + (SCY - H / 2) * min(1, k * 1.5))
        if k > 0.6: im = Image.blend(im, scene_pitt(t), (k - 0.6) / 0.4)
        return im
    if t < EXIT: return subs(inside(t), t)
    if t < EXIT_END:
        k = eio((t - EXIT) / (EXIT_END - EXIT)); z = 5.2 - 4.2 * k
        im = tubo_frame(t, 'analitico', zoom=z, cx=W / 2 + (SCX - W / 2) * (1 - k), cy=H / 2 + (SCY - H / 2) * (1 - k))
        if k < 0.35: im = Image.blend(inside(t), im, k / 0.35)
        return subs(im, t, 1640)
    if t < T_Q:
        im = tubo_frame(t, 'confiante' if t >= ws(99) else 'analitico', zoom=1.0)
        d = ImageDraw.Draw(im, 'RGBA')
        d.text((W / 2, 110), 'SÃO PAULO · COMMANDFEST', font=fit(d, 'SÃO PAULO · COMMANDFEST', INTB, 70, 940), fill=WHITE, anchor='ma')
        d.text((W / 2, 200), 'COMMANDER · 31/10–01/11/2026', font=F(MONO, 34), fill=GREY, anchor='ma')
        if t >= ws(95): stamp(d, 'FORA DO ARQUIVO', GREY, ws(95), t, 300)
        if t >= ws(99):
            k = eio((t - ws(99)) / 0.25)
            d.text((W / 2, 372), 'NÃO DA ATENÇÃO', font=F(MONOB, 44), fill=PH + (int(255 * k),), anchor='ma')
        d.text((80, 1500), 'fonte: magic.gg · calendário', font=F(COND, 34), fill=(150, 170, 175, 235))
        return subs(im, t, 1640)
    if t < T_SIG:
        im = tubo_frame(t, 'analitico', zoom=1.0); d = ImageDraw.Draw(im, 'RGBA')
        im = top_card(im, [('Qual analiso primeiro?', F(INTB, 74), WHITE)], 1.0, 120)
        d = ImageDraw.Draw(im, 'RGBA')
        blink = int(t * 2) % 2 == 0
        d.text((W / 2, 232), 'RESULTADOS: AGUARDANDO' + (' █' if blink else '  '), font=F(MONOB, 34), fill=EM, anchor='ma')
        d.text((W / 2, 290), 'campeões · Top 8 · listas', font=F(MONO, 32), fill=GREY, anchor='ma')
        chips = [('A · LEGACY', ws(112)), ('B · STANDARD', ws(114)), ('C · VINTAGE', ws(116))]
        f = F(MONOB, 32); y = 1460
        wds = [d.textlength(s, font=f) + 48 for s, _ in chips]; x = (W - sum(wds) - 2 * 18) / 2
        for (s, tt), wd in zip(chips, wds):
            on = t >= tt
            d.rounded_rectangle((x, y, x + wd, y + 68), 34, fill=(EM if on else (15, 23, 42, 230)), outline=EM, width=3)
            d.text((x + wd / 2, y + 34), s, font=f, fill=(BG if on else EM), anchor='mm'); x += wd + 18
        return subs(im, t, 1640)
    kz = eio((t - T_SIG) / 1.2)
    im = tubo_frame(t, 'confiante', zoom=1.0 + 0.22 * kz, cx=W / 2, cy=H / 2 + (SCY + 260 - H / 2) * kz)
    k = ease((t - T_SIG) / 0.4)
    im = top_card(im, [('META EM CURTO', F(INTB, 96), WHITE), ('com TUBO · BINDER Originals', F(MONO, 34), EM)], k)
    return subs(im, t, 1640)
if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[2] == 'stills':
        for tt in map(float, sys.argv[3:]): frame(tt).save(f'still_{tt:05.2f}.png')
        sys.exit()
    nf = int(round(TOTAL * FPS))
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-i', 'mix_final.wav', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
                          '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', '-shortest', 'EP03_META_EM_CURTO.mp4'],
                         stdin=subprocess.PIPE)
    for i in range(nf): p.stdin.write(frame(i / FPS).convert('RGB').tobytes())
    p.stdin.close(); p.wait(); print('done', nf)

