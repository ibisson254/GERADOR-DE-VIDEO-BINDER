# ABISMO · motor de modelos (Story, Reel, Carrossel) — identidade exclusiva de Nauctis: The Sunken Realm.
# Uso (a partir da raiz do repositório):
#   python3 -I abismo/motor/abismo.py abismo/publicacoes/<ID>            -> render do formato escolhido em post.json
#   python3 -I abismo/motor/abismo.py abismo/publicacoes/<ID> stills 0 5 -> quadros de controlo
# Reaproveita (não duplica): o gerador do fundo (expedicao/template/fundo.py, mesma semente do vídeo de referência),
# a música do fundador e os sons já gerados (expedicao/kit/), o logótipo oficial (manaburn/logo/logo_mark.png) e as
# fontes Inter do sistema. Custo por publicação: zero (Python + FFmpeg + Scryfall público). Sem voz por defeito.
import json, math, os, subprocess, sys, urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(f'{HERE}/../..')
sys.path.insert(0, f'{ROOT}/expedicao/template')
from fundo import Fundo
sys.path.insert(0, HERE)
from vida import Vida
POST = os.path.abspath(sys.argv[1]); MODE = sys.argv[2] if len(sys.argv) > 2 else 'render'
CFG = json.load(open(f'{POST}/post.json'))
ID = json.load(open(f'{HERE}/../identidade.json'))
FMT = CFG['formato']; MOD = json.load(open(f'{HERE}/../modelos/{FMT}.json'))
W, H = MOD['tamanho']; FPS = 30
OUT = f'{POST}/saida'; os.makedirs(OUT, exist_ok=True)

# ---------- identidade ----------
FD = ID['fontes']['pasta']
_fc = {}
def F(name, size):
    if (name, size) not in _fc: _fc[(name, size)] = ImageFont.truetype(FD + ID['fontes'][name], size)
    return _fc[(name, size)]
C = {k: tuple(v) for k, v in ID['cores'].items()}
EM, WHITE, YEL, INK = C['esmeralda'], C['branco'], C['amarelo'], C['tinta']
CHIP = {'ok': (EM, INK), 'mau': (C['condicao'], WHITE), 'info': ((255, 255, 255), INK)}
def ease(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)
def eout(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3
def lerp(a, b, k): return a + (b - a) * k
def fit(d, s, font, size, maxw, minsize=16):
    while size > minsize and d.textlength(s, font=F(font, size)) > maxw: size -= 1
    return F(font, size)
def text_center(d, txt, y, font, size, col, maxw=None, stroke=0, x=None):
    maxw = maxw or W - 120
    d.text((x or W / 2, y), txt, font=fit(d, txt, font, size, maxw), fill=col, anchor='mm', stroke_width=stroke, stroke_fill=INK)
def tracked(d, txt, y, font, size, col, track=0.16, x=None, maxw=None):
    maxw = maxw or W - 120
    while True:
        f = F(font, size); ws = [d.textlength(c, font=f) for c in txt]; tot = sum(ws) + size * track * (len(txt) - 1)
        if tot <= maxw or size < 14: break
        size -= 2
    x = (W - tot) / 2 if x is None else x
    for c, w in zip(txt, ws): d.text((x, y), c, font=f, fill=col, anchor='lm'); x += w + size * track
def wrap(d, txt, font, size, maxw):
    out, cur = [], ''
    for w_ in txt.split():
        s = (cur + ' ' + w_).strip()
        if d.textlength(s, font=F(font, size)) <= maxw: cur = s
        else: out.append(cur); cur = w_
    return out + [cur]

# ---------- carta (Scryfall público se faltar o PNG) ----------
def card_png(c):
    p = os.path.join(POST, c['png']) if not os.path.isabs(c['png']) else c['png']
    if not os.path.exists(p):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        req = urllib.request.Request(f'https://api.scryfall.com/cards/{c["set"].lower()}/{c["num"]}', headers={'User-Agent': 'BinderAbismo/1.0', 'Accept': 'application/json'})
        d = json.load(urllib.request.urlopen(req)); urllib.request.urlretrieve(d['image_uris']['png'], p)
    return p
_cards = {}
def card(c, w):
    k = (c['png'], int(w))
    if k not in _cards:
        if len(_cards) > 48: _cards.clear()
        im = Image.open(card_png(c)).convert('RGBA'); w = int(w); h = round(im.height * w / im.width)
        im = im.resize((w, h), Image.LANCZOS)
        m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=int(w * 0.045), fill=255)
        im.putalpha(Image.fromarray(np.minimum(np.array(im.getchannel('A')), np.array(m)))); _cards[k] = im
    return _cards[k]
def paste_card(im, c, x, y):
    pad = 78; s = Image.new('L', (c.width + 2 * pad, c.height + 2 * pad), 0)
    ImageDraw.Draw(s).rounded_rectangle((pad, pad + 14, pad + c.width, pad + c.height + 14), radius=int(c.width * 0.05), fill=150)
    im.paste((0, 0, 0), (int(x) - pad, int(y) - pad), s.filter(ImageFilter.GaussianBlur(26))); im.alpha_composite(c, (int(x), int(y)))
def silhouette(c, w, br):
    im = card(c, w); rgb = ImageEnhance.Brightness(im.convert('RGB')).enhance(br)
    rgb = Image.blend(rgb, Image.new('RGB', rgb.size, (30, 12, 50)), 0.3).convert('RGBA'); rgb.putalpha(im.getchannel('A')); return rgb
def glow(im, x, y, w, h, k):
    g = Image.new('RGBA', (int(w) + 260, int(h) + 260), (0, 0, 0, 0))
    ImageDraw.Draw(g).rounded_rectangle((130, 130, int(w) + 130, int(h) + 130), radius=40, fill=C['brilho'] + (150,))
    g = g.filter(ImageFilter.GaussianBlur(60)); g.putalpha(Image.fromarray((np.array(g.getchannel('A')) * k).astype(np.uint8)))
    im.alpha_composite(g, (int(x) - 130, int(y) - 130))
def entry_luz(c, r):
    a = np.array(c, np.float32); h, w = a.shape[:2]
    u = (np.arange(w)[None, :] / w + np.arange(h)[:, None] / h) / 2; edge = r * 1.35 - 0.15
    lit = np.clip((edge - u) / 0.18, 0, 1); band = np.exp(-((u - edge) / 0.035) ** 2) * (r < 1.05)
    a[..., :3] = a[..., :3] * (0.07 + 0.93 * lit[..., None]) + band[..., None] * 140
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

# ---------- fundo mestre (o do vídeo de referência, gerado pelo mesmo código) ----------
FUNDO = Fundo(seed=ID['fundo']['semente'])
def fundo(t, lotus=1.0, energy=0.6, pulse=0.0, glitch=0.0):
    im = FUNDO.frame(t, 'abismo', energy=energy, pulse=pulse, lotus=lotus, glitch=glitch, seed=int(t * 30))
    if (W, H) != (1080, 1920):   # 4:5: recorte central do 9:16 (o feixe horizontal fica a ~41% da altura)
        y0 = ID['fundo']['recorte_45_y']; im = im.crop((0, y0, 1080, y0 + H))
    return VIDA.aplicar(im, t, 0.0 if CFG.get('vida') is False else 1.0)
def zonas_calma():
    """hierarquia: a carta é o único destaque. Atrás dela e do texto, o movimento do fundo quase desaparece."""
    k = ID['vida']['calma']; mg = k['margem_px']
    if 'carta' not in MOD: return [(140, 120, W - 140, H - 120, k['carta'], mg)]
    if CFG.get('modo') == 'decks':   # sequência de decks: calma atrás do título, da carta e das etiquetas
        L = MOD['decks']; cw = W * L['slot_escala']
        return [(90, L['titulo_y'] - 80, W - 90, L['titulo_y'] + 190, k['texto'], mg),
                ((W - cw) / 2, L['slot_topo'], (W + cw) / 2, L['slot_topo'] + cw * 1040 / 745, k['carta'], mg),
                (90, L['chips_y'] - 20, W - 90, MOD['seguro']['legenda'] + 60, k['texto'], mg)]
    h = MOD['carta']; cw = W * h['escala']; S = MOD['seguro']
    return [((W - cw) / 2, h['topo'], (W + cw) / 2, h['topo'] + cw * 1040 / 745, k['carta'], mg),
            (90, h['topo_info'] + W * h['escala_info'] * 1040 / 745, W - 90, S['legenda'] + 60, k['texto'], mg)]
VIDA = Vida(W, H, dict(ID['vida'], _zonas=zonas_calma()), ID['musica']['periodo'])
def pulso(t, apos):
    """pulsação da carta no 1.º tempo de cada compasso (o mesmo instante em que as medusas contraem)."""
    pc = ID['vida']['pulso_carta']; u = t % (ID['vida']['pulso_batidas'] * ID['musica']['periodo'])
    return 1 + (pc['amplitude_apos_impacto'] if apos else pc['amplitude']) * math.exp(-u / pc['decaimento_s'])

LOGO = Image.open(f'{ROOT}/{ID["marca"]["logo"]}').convert('RGBA')
def logo_small(im, y=None):
    s = ID['marca']['tamanho_canto']; lg = LOGO.resize((s, s), Image.LANCZOS); a = np.array(lg); a[:, :, 3] = (a[:, :, 3] * ID['marca']['opacidade_canto']).astype(np.uint8)
    im.alpha_composite(Image.fromarray(a), (W - s - 40, y if y is not None else MOD['seguro']['topo'] - 18))

def meter(im, t_on, t, n=None):
    """medidor lateral: só a camada da carta; contador n/N só quando o post é uma sequência (CFG['sequencia']).
    "medidor": false no post.json desliga-o (carta sem camada do oceano, ex.: reimpressão dos decks de Commander)."""
    if CFG.get('medidor') is False: return
    d = ImageDraw.Draw(im, 'RGBA'); x = 44; y0, y1 = MOD['medidor']; seg = (y1 - y0) / 3
    d.line((x, y0, x, y1), fill=(255, 255, 255, 80), width=2)
    for i, nome in enumerate(ID['camadas']):
        y = y0 + seg * i; d.line((x - 8, y, x + 8, y), fill=(255, 255, 255, 120), width=2)
        on = nome == CFG['carta']['camada']
        lab = Image.new('RGBA', (220, 26), (0, 0, 0, 0)); ImageDraw.Draw(lab).text((2, 2), nome, font=F('semi', 18), fill=(255, 255, 255, 240 if on else 110))
        lab = lab.rotate(90, expand=True); im.alpha_composite(lab, (x + 12, int(y + seg / 2 - 110)))
    d.line((x - 8, y1, x + 8, y1), fill=(255, 255, 255, 120), width=2)
    li = ID['camadas'].index(CFG['carta']['camada']); yt = y0 + seg * (li + 0.5) if li < 2 else y1
    yk = lerp(y0, yt, eout((t - t_on) / 0.6))
    d.ellipse((x - 16, yk - 16, x + 16, yk + 16), fill=EM + (60,)); d.ellipse((x - 8, yk - 8, x + 8, yk + 8), fill=EM + (255,))
    seq = CFG.get('sequencia')
    if seq: d.text((x + 24, yk), f'{seq[0]}/{seq[1]}', font=F('black', 30), fill=EM + (255,), anchor='lm')

def ficha(im, t0, t, y):
    f = CFG['ficha']; k = eout((t - t0) / 0.2); d = ImageDraw.Draw(im, 'RGBA')
    txt = f'{f["nome"]} · {f["tipo"]} · {f["camada"]}'; tf = fit(d, txt, 'bold', 30, W - 260); w = d.textlength(txt, font=tf) + 48
    x = (W - w) / 2 - (1 - k) * 60
    d.rounded_rectangle((x, y, x + w, y + 58), radius=14, fill=INK + (int(215 * k),))
    d.text((x + 24, y + 29), txt, font=tf, fill=WHITE + (int(255 * k),), anchor='lm')

def painel(im, t0, chips_t, t, y0, titulo=None, chips=None):
    """o cartão informativo do vídeo de referência: fundo escuro, filete esmeralda, título, etiquetas."""
    ch = CFG['chamada']; titulo = titulo or ch['titulo']; chips = chips if chips is not None else ch['chips']
    d = ImageDraw.Draw(im, 'RGBA'); k = eout((t - t0) / 0.25)
    if k <= 0: return 0
    a = int(255 * k); dy = (1 - k) * 30; maxw = W - 240
    lines = wrap(d, titulo, 'black', 54, maxw); rows, row, rw = [], [], 0
    for c, tc in zip(chips, chips_t):
        cw_ = d.textlength(c[0], font=F('bold', 26)) + 36
        if row and rw + cw_ > maxw: rows.append(row); row, rw = [], 0
        row.append((c, tc, cw_)); rw += cw_ + 12
    if row: rows.append(row)
    hh = 44 + 62 * len(lines) + 56 * len(rows) + 18; f = CFG['ficha']
    d.rounded_rectangle((90, y0 + dy - 14, W - 90, y0 + dy + hh), radius=22, fill=INK + (int(200 * k),))
    d.rectangle((90, y0 + dy + 6, 96, y0 + dy + hh - 20), fill=EM + (a,))
    tracked(d, f'{f["nome"]} · {f["tipo"].upper()}', y0 + dy + 18, 'bold', 24, EM + (a,), track=0.08, x=120, maxw=maxw)
    y = y0 + dy + 44
    for ln in lines: d.text((120, y + 30), ln, font=F('black', 54), fill=WHITE + (a,), anchor='lm'); y += 62
    y += 6
    for r in rows:
        x = 120
        for (c, tc, cw_) in r:
            kk = eout((t - tc) / 0.2)
            if kk > 0:
                bg, fg = CHIP[c[1]]; sc = 0.85 + 0.15 * kk
                d.rounded_rectangle((x, y + (1 - sc) * 22, x + cw_ * sc, y + 44 - (1 - sc) * 22), radius=22, fill=bg + (int(240 * kk * k),))
                d.text((x + cw_ * sc / 2, y + 22), c[0], font=F('bold', int(26 * sc)), fill=fg + (int(255 * kk * k),), anchor='mm')
            x += cw_ + 12
        y += 56
    return hh

def credit(im, c, y):
    d = ImageDraw.Draw(im, 'RGBA'); s = f'{c["nome"]} · {c["colecao"]} · Arte: {c["artista"]} · © Wizards of the Coast'
    d.text((W / 2, y), s, font=fit(d, s, 'med', 19, W - 180), fill=(225, 238, 240, 205), anchor='mm')

def frase(im, t, y):
    """legenda de ecrã (sem voz): frases curtas presas à grelha, branco com palavras-chave a amarelo."""
    act = None
    for fr in CFG.get('frases', []):
        if fr['t'] <= t: act = fr
    if not act or t > act['t'] + act.get('dur', 99): return
    band = Image.new('L', (W, 190), 0); ImageDraw.Draw(band).rectangle((0, 40, W, 150), fill=120)
    im.paste(INK, (0, int(y - 95)), band.filter(ImageFilter.GaussianBlur(30)))
    d = ImageDraw.Draw(im, 'RGBA'); k = eout((t - act['t']) / 0.15); toks = act['texto'].split(); amar = set(act.get('amarelo', []))
    f = F('black', 58); sp = d.textlength(' ', font=f); ws = [d.textlength(s, font=f) for s in toks]; tot = sum(ws) + sp * (len(toks) - 1)
    if tot > W - 100: f = F('black', int(58 * (W - 100) / tot)); sp = d.textlength(' ', font=f); ws = [d.textlength(s, font=f) for s in toks]; tot = sum(ws) + sp * (len(toks) - 1)
    x = (W - tot) / 2
    for i, (s, w) in enumerate(zip(toks, ws)):
        d.text((x, y + 8 * (1 - k)), s, font=f, fill=(YEL if i in amar else WHITE) + (int(255 * k),), anchor='lm', stroke_width=5, stroke_fill=INK); x += w + sp

# ---------- música: cortes por batida da faixa do fundador (sem alterar a composição) ----------
def musica(dur_beats_plan):
    M = ID['musica']; P, OFF = M['periodo'], M['offset']; SR = 48000
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{ROOT}/{M["arquivo"]}', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    X = np.frombuffer(raw, np.float32).reshape(-1, 2)
    segs = []
    for b0, b1 in dur_beats_plan:
        s = X[int((OFF + b0 * P) * SR):int((OFF + b1 * P) * SR)].copy(); f = int(0.012 * SR)
        s[:f] *= np.linspace(0, 1, f)[:, None]; s[-f:] *= np.linspace(1, 0, f)[:, None]; segs.append(s)
    return np.concatenate(segs), P

def mix(mus, sfx_events, total, voz=None):
    SR = 48000; N = int(total * SR); out = np.zeros((N, 2), np.float32)
    m = mus[:N]; out[:len(m)] += m
    lib = {k: None for k in ('descida', 'glitch', 'swell')}
    for k in lib:
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{ROOT}/{ID["sons"][k]}', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
        lib[k] = np.frombuffer(raw, np.float32).reshape(-1, 2)
    g = ID['sons']['ganho']
    for t, k in sfx_events:
        x = lib[k] * g[k]; t0 = t - (len(x) / SR if k == 'swell' else 0); i = int(max(0, t0) * SR)
        if i < N: out[i:i + len(x)] += x[:N - i]
    tt = np.arange(N) / SR; out *= np.clip((total - tt) / 0.6, 0, 1)[:, None]
    p = f'{OUT}/mix_pre.wav'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', p], input=out.tobytes(), check=True)
    st = subprocess.run(['ffmpeg', '-v', 'info', '-i', p, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
    j = json.loads(st[st.rfind('{'):st.rfind('}') + 1])
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', p, '-af', f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true",
                    '-ar', str(SR), f'{OUT}/mix.wav'], check=True)

# ---------- linha do tempo dos modelos animados (em batidas da música) ----------
def timeline():
    M = MOD['momentos']; P = ID['musica']['periodo']
    T = {k: v * P for k, v in M.items()}
    T['chips'] = [T['info'] + (2 * i) * P for i in range(len(CFG['chamada']['chips']))]
    T['total'] = MOD['batidas_total'] * P
    for fr in CFG.get('frases', []): fr['t'] = fr['batida'] * P; fr['dur'] = fr.get('batidas', 6) * P
    return T

def assinatura(t, t_fim):
    """assinatura final: só recursos oficiais (logótipo) e texto real."""
    im = Image.new('RGBA', (W, H), INK + (255,)); g = Image.new('L', (W, H), 0); ImageDraw.Draw(g).ellipse((140, H * 0.16, 940, H * 0.58), fill=70)
    im.paste(EM, (0, 0), g.filter(ImageFilter.GaussianBlur(160))); k = eout((t - t_fim) / 0.35); s = int(240 * (0.8 + 0.2 * k))
    lg = LOGO.resize((s, s), Image.LANCZOS); im.alpha_composite(lg, (int(W / 2 - s / 2), int(H * 0.36 - s / 2)))
    d = ImageDraw.Draw(im, 'RGBA'); f = F('black', 100); w1 = d.textlength('BINDER ', font=f); w2 = d.textlength('Vision', font=f); xx = (W - w1 - w2) / 2; yy = H * 0.36 + 220
    d.text((xx, yy), 'BINDER ', font=f, fill=WHITE, anchor='lm'); d.text((xx + w1, yy), 'Vision', font=f, fill=EM, anchor='lm')
    for i, ln in enumerate(ID['marca']['assinatura']): text_center(d, ln, yy + 110 + i * 64, 'semi' if i < 2 else 'black', 42 if i < 2 else 48, (EM if i == 2 else WHITE))
    return im.convert('RGB')

def frame_anim(t, T):
    c = CFG['carta']; S = MOD['seguro']; hero = MOD['carta']
    cw = W * hero['escala']; ch_ = cw * 1040 / 745; x = (W - cw) / 2; y = hero['topo'] + 4 * math.sin(2 * math.pi * t / 3)
    lit = ease((t - T['impacto']) / 0.6) if t >= T['impacto'] else 0.0
    im = fundo(t, lotus=lit, energy=0.6, pulse=0.0, glitch=1.0 if any(0 <= t - u < 2.5 / FPS for u in (T['entrada'], T['impacto'])) else 0.0)
    d = ImageDraw.Draw(im, 'RGBA')
    if t >= T['fim']: return assinatura(t, T['fim'])
    if t < T['entrada']:      # gancho: promessa escrita desde o quadro 0 sobre a silhueta
        br = 0.16 + 0.45 * math.exp(-((t - 0.33) / 0.06) ** 2)
        paste_card(im, silhouette(c, cw, round(br, 2)), x, y)
        im = zoom(im, W / 2, y + ch_ / 2, lerp(1.0, 1.08, t / T['entrada']))
        d = ImageDraw.Draw(im, 'RGBA')
        for i, ln in enumerate(CFG['gancho']): text_center(d, ln, S['topo'] + 90 + i * 96, 'black', 86, WHITE, stroke=6)
        tracked(d, ID['etiqueta'], S['topo'] + 6, 'bold', 24, EM + (230,), track=0.2)
        logo_small(im); return im.convert('RGB')
    dt = t - T['entrada']; k_info = ease((t - T['info'] + 0.4) / 0.35)   # a carta encolhe antes: o painel chega no tempo certo sem sobrepor
    sc = lerp(hero['escala'], hero['escala_info'], k_info); y2 = lerp(hero['topo'], hero['topo_info'], k_info) + 4 * math.sin(2 * math.pi * t / 3)
    pz = pulso(t, t >= T['impacto']); y2 -= W * sc * 1040 / 745 * (pz - 1) / 2   # cresce a partir do centro
    cw2 = round(W * sc * pz / 2) * 2; ch2 = cw2 * 1040 / 745; x2 = (W - cw2) / 2
    if lit > 0: glow(im, x2, y2, cw2, ch2, lit * 0.6 * (0.75 + 12 * (pz - 1)))
    cc = card(c, cw2)
    paste_card(im, entry_luz(cc, dt / 0.95) if dt < 1.0 else cc, x2, y2)
    comp = CFG.get('comparacao')
    if comp and T.get('comparacao') is not None and t >= T['comparacao']:
        kk = eout((t - T['comparacao']) / 0.27) if t < T['comparacao_fim'] else 1 - ease((t - T['comparacao_fim']) / 0.2)
        if kk > 0:
            co = card(comp, W * 0.40).rotate(-9, expand=True, resample=Image.BICUBIC)
            paste_card(im, co, lerp(W + 40, W - co.width - 40, kk), lerp(H + 60, y2 + ch2 * 0.3, kk))
    ts = CFG.get('selo_batida', MOD['momentos']['impacto']) * ID['musica']['periodo']
    if CFG.get('impacto') and ts <= t < T['pergunta']:
        kk = eout((t - ts) / 0.22); s1, s2 = CFG['impacto']; bw = 640 * (0.85 + 0.15 * kk); yy = y2 + ch2 * 0.5
        d.rounded_rectangle((W / 2 - bw / 2, yy, W / 2 + bw / 2, yy + 150), radius=26, fill=EM + (int(245 * kk),))
        d.text((W / 2, yy + 58), s1, font=F('black', 72), fill=INK + (int(255 * kk),), anchor='mm')
        d.text((W / 2, yy + 118), s2, font=fit(d, s2, 'bold', 24, bw - 40), fill=INK + (int(230 * kk),), anchor='mm')
    meter(im, T['entrada'], t)
    logo_small(im)
    if t < T['info']:
        credit(im, c, y2 + ch2 + 22)
        if t >= T['ficha']: ficha(im, T['ficha'], t, min(S['base'] - 210, y2 + ch2 + 46))
    else:
        credit(im, c, y2 + ch2 + 22)
        yf = hero['topo_info'] + W * hero['escala_info'] * 1040 / 745   # posição final da carta: o painel não salta com a transição
        if t < T['pergunta']: painel(im, T['info'], T['chips'], t, yf + 58)
    if t >= T['pergunta']:
        d = ImageDraw.Draw(im, 'RGBA'); k = eout((t - T['pergunta']) / 0.3); p1, p2 = CFG['pergunta']
        text_center(d, p1, y2 + ch2 + 110, 'black', 66, WHITE + (int(255 * k),), stroke=5)
        if FMT == 'story':   # por baixo fica livre para o autocolante de enquete (posto na app, não no vídeo)
            text_center(d, p2, y2 + ch2 + 190, 'bold', 34, (220, 240, 235, int(255 * k)))
        else:
            text_center(d, p2, y2 + ch2 + 200, 'black', 78, YEL + (int(255 * k),), stroke=5)
    frase(im, t, S['legenda'])
    return im.convert('RGB')

def zoom(im, cx, cy, z):
    if z <= 1.001: return im
    w, h = W / z, H / z; x0 = min(max(cx - w / 2, 0), W - w); y0 = min(max(cy - h / 2, 0), H - h)
    return im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + w, y0 + h))

# ---------- modo "decks": vários decks no mesmo Reel (AB-04) ----------
# Mesmo fundo, vida, cartão, etiquetas, legendas, música e assinatura do modelo de uma carta. Cada deck ganha identidade
# própria só pelos pontos das suas cores de mana e pelo filete do espaço da carta; o resto é o sistema do ABISMO.
# Decks sem carta revelada mostram um espaço de carta vazio com «?» (nunca arte inventada).
CHIP['leitura'] = (None, WHITE)   # interpretação estratégica: contorno branco, sem preenchimento (≠ facto oficial)
def mana_cols(cores): return [tuple(MOD['decks']['cores_mana'][c]) for c in cores]
def dots(d, cores, x, y, r=13, a=255):
    for i, col in enumerate(mana_cols(cores)):
        cx = x + i * (2 * r + 8)
        d.ellipse((cx - r - 3, y - r - 3, cx + r + 3, y + r + 3), fill=INK + (int(a * 0.9),)); d.ellipse((cx - r, y - r, cx + r, y + r), fill=col + (a,))
    return len(cores) * (2 * r + 8) - 8
_slots = {}
def slot(dk, w):
    """espaço de carta ainda não revelada: vidro escuro, filete nas cores do deck, «?»."""
    k = (dk['nome'], int(w))
    if k in _slots: return _slots[k]
    w = int(w); h = round(w * 1040 / 745); r = int(w * 0.045); cols = mana_cols(dk['cores'])
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); g = np.zeros((h, w, 3), np.float32); yy = np.linspace(0, 1, h)[:, None]
    for i, col in enumerate(cols):   # gradiente vertical suave entre as cores do deck
        c0 = i / max(1, len(cols) - 1) if len(cols) > 1 else 0.5
        wgt = np.exp(-((yy - c0) / 0.45) ** 2); g += wgt[..., None] * np.array(col, np.float32)[None, None, :] * np.ones((1, w, 1))
    g = g / max(1e-6, g.max()) * 120
    base = Image.fromarray(np.clip(g * 0.35 + np.array(INK, np.float32) * 0.9, 0, 255).astype(np.uint8)).convert('RGBA')
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=r, fill=225); base.putalpha(m)
    im.alpha_composite(base); d = ImageDraw.Draw(im, 'RGBA')
    for i, col in enumerate(cols):   # filete: um segmento por cor
        y0 = i * h / len(cols); y1 = (i + 1) * h / len(cols)
        d.rectangle((0, y0, 7, y1), fill=col + (255,)); d.rectangle((w - 8, y0, w - 1, y1), fill=col + (255,))
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=r, outline=(255, 255, 255, 70), width=2)
    d.text((w / 2, h * 0.43), '?', font=F('black', int(w * 0.5)), fill=(255, 255, 255, 235), anchor='mm')
    fs = min(34, int(w * 0.072))
    for j, ln in enumerate(('CARTAS AINDA', 'NÃO REVELADAS')): d.text((w / 2, h * 0.74 + j * fs * 1.3), ln, font=F('bold', fs), fill=(225, 238, 240, 230), anchor='mm')
    m2 = Image.new('L', (w, h), 0); ImageDraw.Draw(m2).rounded_rectangle((0, 0, w - 1, h - 1), radius=r, fill=255)
    im.putalpha(Image.fromarray(np.minimum(np.array(im.getchannel('A')), np.array(m2)))); _slots[k] = im; return im

def chips_row(im, chips, chips_t, t, y, a_glob=1.0):
    """etiquetas centradas (mesmo desenho do cartão informativo); 'leitura' = contorno, para separar facto de interpretação."""
    d = ImageDraw.Draw(im, 'RGBA'); f = F('bold', 28); maxw = W - 160; rows, row, rw = [], [], 0
    for c, tc in zip(chips, chips_t):
        cw_ = d.textlength(c[0], font=f) + 40
        if row and rw + cw_ > maxw: rows.append((row, rw - 12)); row, rw = [], 0
        row.append((c, tc, cw_)); rw += cw_ + 12
    if row: rows.append((row, rw - 12))
    for r_, tot in rows:
        x = (W - tot) / 2
        for (c, tc, cw_) in r_:
            kk = eout((t - tc) / 0.2) * a_glob
            if kk > 0:
                bg, fg = CHIP[c[1]]; sc = 0.85 + 0.15 * kk; x0, x1 = x, x + cw_ * sc; y0, y1 = y + (1 - sc) * 24, y + 48 - (1 - sc) * 24
                if bg is None:
                    d.rounded_rectangle((x0, y0, x1, y1), radius=24, fill=INK + (int(170 * kk),), outline=fg + (int(235 * kk),), width=3)
                else:
                    d.rounded_rectangle((x0, y0, x1, y1), radius=24, fill=bg + (int(240 * kk),))
                d.text(((x0 + x1) / 2, y + 24), c[0], font=F('bold', int(28 * sc)), fill=fg + (int(255 * kk),), anchor='mm')
            x += cw_ + 12
        y += 60

def timeline_decks():
    P = ID['musica']['periodo']; T = {'total': MOD['batidas_total'] * P, 'impacto': MOD['momentos']['impacto'] * P}
    for k in ('entrada', 'resumo', 'fim'): T[k] = CFG['batidas'][k] * P
    for dk in CFG['decks']:
        dk['t0'] = dk['batida'] * P; dk['t1'] = dk['batida_fim'] * P
        dk['chips_t'] = [dk['t0'] + (dk.get('chips_batida', 2) + i) * P for i in range(len(dk['chips']))]
    fr = []
    for dk in CFG['decks']:
        if dk.get('frase'): fr.append(dict(dk['frase'], t=dk['t0'] + 0.5 * P, dur=(dk['batida_fim'] - dk['batida'] - 0.9) * P))
    CFG['frases'] = fr
    return T

def frame_decks(t, T):
    S = MOD['seguro']; L = MOD['decks']; P = ID['musica']['periodo']
    lit = ease((t - T['impacto']) / 0.6) if t >= T['impacto'] else 0.0
    gl = 1.0 if any(0 <= t - u < 2.5 / FPS for u in [T['impacto']] + [dk['t0'] for dk in CFG['decks']]) else 0.0
    im = fundo(t, lotus=lit, energy=0.6, pulse=0.0, glitch=gl)
    if t >= T['fim']: return assinatura(t, T['fim'])
    if t < T['entrada']:   # gancho: carta real (silhueta) + promessa escrita desde o quadro 0 + os 4 decks em pílulas
        c = CFG['gancho_carta']; hero = MOD['carta']; cw = W * hero['escala']; ch_ = cw * 1040 / 745; x = (W - cw) / 2; y = hero['topo'] + 4 * math.sin(2 * math.pi * t / 3)
        br = 0.16 + 0.45 * math.exp(-((t - 0.33) / 0.06) ** 2)
        paste_card(im, silhouette(c, cw, round(br, 2)), x, y)
        im = zoom(im, W / 2, y + ch_ / 2, lerp(1.0, 1.08, t / T['entrada'])); d = ImageDraw.Draw(im, 'RGBA')
        tracked(d, ID['etiqueta'], S['topo'] + 6, 'bold', 24, EM + (230,), track=0.2)
        for i, ln in enumerate(CFG['gancho']): text_center(d, ln, S['topo'] + 100 + i * 100, 'black', 92, YEL if i == len(CFG['gancho']) - 1 else WHITE, stroke=6)
        n = len(CFG['decks']); pw = 240; gap = 10; x0 = (W - n * pw - (n - 1) * gap) / 2; yp = S['legenda'] - 60
        for i, dk in enumerate(CFG['decks']):
            k = 1.0   # visíveis desde o quadro 0 (miniatura sem som: percebe-se que são 4 decks)
            xx = x0 + i * (pw + gap); d.rounded_rectangle((xx, yp - 34, xx + pw, yp + 34), radius=34, fill=INK + (int(220 * k),))
            d.text((xx + 30, yp), str(i + 1), font=F('black', 36), fill=EM + (int(255 * k),), anchor='mm')
            wd = dots(d, dk['cores'], 0, -100, r=9, a=0)   # largura das bolinhas
            dots(d, dk['cores'], xx + pw - 26 - wd + 9, yp, r=9, a=int(255 * k))
            d.text((xx + 54, yp), dk['guilda'], font=fit(d, dk['guilda'], 'bold', 26, pw - 54 - 26 - wd - 12), fill=WHITE + (int(255 * k),), anchor='lm')
        logo_small(im); return im.convert('RGB')
    if t >= T['resumo']: return resumo(im, t, T)
    dk = None
    for x in CFG['decks']:
        if x['t0'] <= t < x['t1']: dk = x
    if dk is None: logo_small(im); return im.convert('RGB')
    i = CFG['decks'].index(dk); n = len(CFG['decks']); dt = t - dk['t0']
    kin = eout(dt / 0.25); kout = 1 - ease((t - (dk['t1'] - 0.16)) / 0.16) if t > dk['t1'] - 0.16 else 1.0
    a = kin * kout; dx = (1 - kin) * 70 - (1 - kout) * 70
    d = ImageDraw.Draw(im, 'RGBA')
    # pílula: DECK n/N · guilda · cores
    lab = f'DECK {i + 1}/{n}'; f = F('black', 34); wl = d.textlength(lab, font=f); g = dk['guilda']; fg_ = F('bold', 31); wg = d.textlength(g, font=fg_)
    wd = len(dk['cores']) * 34 - 8; tw = 28 + wl + 22 + wg + 22 + wd + 28; xp = (W - tw) / 2 + dx; yp = L['pill_y']
    d.rounded_rectangle((xp, yp - 32, xp + tw, yp + 32), radius=32, fill=INK + (int(225 * a),))
    d.text((xp + 28, yp), lab, font=f, fill=EM + (int(255 * a),), anchor='lm')
    d.text((xp + 28 + wl + 22, yp), g, font=fg_, fill=WHITE + (int(255 * a),), anchor='lm')
    dots(d, dk['cores'], xp + 28 + wl + 22 + wg + 22 + 13, yp, r=13, a=int(255 * a))
    tracked(d, ' · '.join(L['nomes_mana'][c] for c in dk['cores']), yp + 56, 'semi', 24, (225, 238, 240, int(210 * a)), track=0.14)
    # título do deck (duas linhas, mesma escala para os 4)
    for j, ln in enumerate(dk['titulo']):
        ty = L['titulo_y'] + 40 + j * (L['titulo_tam'] + 4)
        d.text((W / 2 + dx, ty), ln, font=fit(d, ln, 'black', L['titulo_tam'], W - 140), fill=WHITE + (int(255 * a),), anchor='mm', stroke_width=6, stroke_fill=INK)
    # carta real ou espaço por revelar
    pz = pulso(t, t >= T['impacto']); cw = round(W * L['slot_escala'] * pz / 2) * 2; ch_ = cw * 1040 / 745
    x = (W - cw) / 2 + dx; y = L['slot_topo'] + 4 * math.sin(2 * math.pi * t / 3) - W * L['slot_escala'] * 1040 / 745 * (pz - 1) / 2
    if lit > 0 and dk['t0'] >= T['impacto'] - 1e-6: glow(im, x, y, cw, ch_, lit * 0.6 * (0.75 + 12 * (pz - 1)) * a)
    elif dk.get('carta'): glow(im, x, y, cw, ch_, 0.25 * a)
    cc = card(dk['carta'], cw) if dk.get('carta') else slot(dk, cw)
    if dt < 1.0: cc = entry_luz(cc, dt / 0.95)
    if a < 1: cc = cc.copy(); cc.putalpha(Image.fromarray((np.array(cc.getchannel('A')) * a).astype(np.uint8)))
    paste_card(im, cc, x, y)
    if dk.get('carta'): credit(im, dk['carta'], y + ch_ + 24)
    else:
        d = ImageDraw.Draw(im, 'RGBA'); s = dk.get('nota_slot', 'Wizards ainda não mostrou cartas deste deck')
        d.text((W / 2 + dx, y + ch_ + 26), s, font=fit(d, s, 'med', 22, W - 180), fill=(225, 238, 240, int(205 * a)), anchor='mm')
    chips_row(im, dk['chips'], dk['chips_t'], t, L['chips_y'], a_glob=kout)
    logo_small(im)
    frase(im, t, S['legenda'])
    return im.convert('RGB')

def resumo(im, t, T):
    """grelha 2×2 dos decks + o que ainda falta + pergunta (uma só ação)."""
    S = MOD['seguro']; d = ImageDraw.Draw(im, 'RGBA'); k0 = eout((t - T['resumo']) / 0.3); R = CFG['resumo']
    tracked(d, ID['etiqueta'], S['topo'] + 6, 'bold', 24, EM + (int(230 * k0),), track=0.2)
    for j, ln in enumerate(R['titulo']): text_center(d, ln, S['topo'] + 92 + j * 86, 'black', 78, WHITE + (int(255 * k0),), stroke=6)
    tw, th, gx, gy = 440, 300, 24, 24; x0 = (W - 2 * tw - gx) / 2; y0 = S['topo'] + 260
    for i, dk in enumerate(CFG['decks']):
        k = eout((t - T['resumo'] - 0.1 - i * 0.07) / 0.25)
        if k <= 0: continue
        xx = x0 + (i % 2) * (tw + gx); yy = y0 + (i // 2) * (th + gy) + (1 - k) * 30
        d.rounded_rectangle((xx, yy, xx + tw, yy + th), radius=24, fill=INK + (int(205 * k),))
        for j, col in enumerate(mana_cols(dk['cores'])):   # filete nas cores do deck
            h3 = (th - 40) / len(dk['cores']); d.rectangle((xx, yy + 20 + j * h3, xx + 7, yy + 20 + (j + 1) * h3), fill=col + (int(255 * k),))
        d.text((xx + 34, yy + 46), str(i + 1), font=F('black', 54), fill=EM + (int(255 * k),), anchor='lm')
        dots(d, dk['cores'], xx + tw - 34 - (len(dk['cores']) * 34 - 8) + 13, yy + 46, r=13, a=int(255 * k))
        for j, ln in enumerate(dk['titulo']):
            d.text((xx + 34, yy + 128 + j * 54), ln, font=fit(d, ln, 'black', 50, tw - 60), fill=WHITE + (int(255 * k),), anchor='lm')
        d.text((xx + 34, yy + th - 40), dk['guilda'], font=F('bold', 28), fill=(225, 238, 240, int(220 * k)), anchor='lm')
    yq = y0 + 2 * th + gy + 70; kq = eout((t - T['resumo'] - 0.9) / 0.3)
    if kq > 0:
        cw_ = d.textlength(R['selo'], font=F('bold', 30)) + 48
        d.rounded_rectangle(((W - cw_) / 2, yq - 26, (W + cw_) / 2, yq + 26), radius=26, fill=EM + (int(240 * kq),))
        d.text((W / 2, yq), R['selo'], font=F('bold', 30), fill=INK + (int(255 * kq),), anchor='mm')
    kp = eout((t - T['resumo'] - 1.5) / 0.3)
    if kp > 0:
        p1, p2 = CFG['pergunta']
        text_center(d, p1, yq + 110, 'black', 66, WHITE + (int(255 * kp),), stroke=5)
        text_center(d, p2, yq + 200, 'black', 78, YEL + (int(255 * kp),), stroke=5)
    logo_small(im); return im.convert('RGB')

def render_anim():
    if CFG.get('modo') == 'decks': return render_decks()
    T = timeline(); P = ID['musica']['periodo']
    if CFG.get('comparacao'):
        T['comparacao'] = CFG['comparacao']['batida'] * P; T['comparacao_fim'] = CFG['comparacao']['batida_fim'] * P
    som = CFG.get('audio', True)   # "audio": false → vídeo mudo (música posta pelo fundador no Instagram)
    if som:
        mus, _ = musica(MOD['musica'])
        sfx = [(T['entrada'], 'descida'), (T['impacto'], 'swell')] + [(t, 'glitch') for t, ch in zip(T['chips'], CFG['chamada']['chips']) if ch[1] == 'mau']
        mix(mus, sfx, T['total'])
    encode(frame_anim, T, som)

def render_decks():
    T = timeline_decks(); som = CFG.get('audio', True)
    if som:
        mus, _ = musica(MOD['musica'])
        sfx = [(dk['t0'], 'descida') for dk in CFG['decks']] + [(T['impacto'], 'swell')]
        sfx += [(tc, 'glitch') for dk in CFG['decks'] for tc, ch in zip(dk['chips_t'], dk['chips']) if ch[1] == 'mau']
        mix(mus, sfx, T['total'])
    encode(frame_decks, T, som)

def encode(frame_fn, T, som):
    n = int(round(T['total'] * FPS))
    aud = ['-i', f'{OUT}/mix.wav'] if som else []
    enc = ['-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-shortest'] if som else ['-an']
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          *aud, '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p',
                          *enc, '-movflags', '+faststart', f'{OUT}/{CFG["id"]}_{FMT}.mp4'], stdin=subprocess.PIPE)
    for fi in range(n): p.stdin.write(frame_fn(fi / FPS, T).tobytes())
    p.stdin.close(); p.wait(); print(f'{OUT}/{CFG["id"]}_{FMT}.mp4', round(T['total'], 2), 's')

# ---------- carrossel (4:5, PNG) ----------
def slide(s, i, n):
    im = fundo(2.0 + i * 0.7, lotus=1.0 if s['tipo'] != 'capa' else 0.6); d = ImageDraw.Draw(im, 'RGBA'); c = CFG['carta']
    S = MOD['seguro']
    tracked(d, f'{ID["etiqueta"]}  ·  {i + 1}/{n}', S['topo'], 'bold', 22, EM + (230,), track=0.2)
    logo_small(im, S['topo'] - 30)
    if s['tipo'] == 'capa':
        cw = W * 0.56; ch_ = cw * 1040 / 745; x = (W - cw) / 2; y = 330
        glow(im, x, y, cw, ch_, 0.55); paste_card(im, card(c, cw), x, y)
        for j, ln in enumerate(s['texto']): text_center(d, ln, 150 + j * 84, 'black', 78, WHITE, stroke=6)
        text_center(d, s.get('sub', ''), y + ch_ + 60, 'black', 50, YEL, stroke=4)
    elif s['tipo'] == 'carta':
        cw = W * 0.62; ch_ = cw * 1040 / 745; x = (W - cw) / 2; y = 120
        paste_card(im, card(c, cw), x, y); credit(im, c, y + ch_ + 24); ficha(im, -1, 1, y + ch_ + 56)
    elif s['tipo'] == 'habilidade':
        cw = W * 0.36; ch_ = cw * 1040 / 745; paste_card(im, card(c, cw), 70, 130)
        dd = ImageDraw.Draw(im, 'RGBA'); yy = 150
        for ln in wrap(dd, s['titulo'], 'black', 56, W - cw - 170): dd.text((cw + 110, yy), ln, font=F('black', 56), fill=WHITE, anchor='la'); yy += 64
        y0 = 130 + ch_ + 50
        for j, (txt, kind) in enumerate(s['itens']):
            bg, fg = CHIP[kind]; dd.rounded_rectangle((90, y0, W - 90, y0 + 92), radius=20, fill=INK + (215,))
            dd.rounded_rectangle((90, y0, 104, y0 + 92), radius=6, fill=bg + (255,))
            dd.text((130, y0 + 46), txt, font=fit(dd, txt, 'bold', 34, W - 260), fill=WHITE, anchor='lm'); y0 += 108
    elif s['tipo'] == 'comparacao':
        a, b = CFG['carta'], s['com']; cw = W * 0.40; ch_ = cw * 1040 / 745
        paste_card(im, card(a, cw), 70, 210); paste_card(im, card(b, cw), W - cw - 70, 210)
        credit(im, a, 210 + ch_ + 26); credit(im, b, 210 + ch_ + 54)
        dd = ImageDraw.Draw(im, 'RGBA'); text_center(dd, s['titulo'], 130, 'black', 52, WHITE, stroke=4)
        y0 = 210 + ch_ + 100
        for txt in s['linhas']: text_center(dd, txt, y0, 'bold', 36, WHITE); y0 += 56
    elif s['tipo'] == 'pergunta':
        cw = W * 0.40; ch_ = cw * 1040 / 745; x = (W - cw) / 2; glow(im, x, 200, cw, ch_, 0.5); paste_card(im, card(c, cw), x, 200)
        dd = ImageDraw.Draw(im, 'RGBA')
        for j, ln in enumerate(s['texto']): text_center(dd, ln, 200 + ch_ + 90 + j * 92, 'black', 70 if j == 0 else 80, WHITE if j == 0 else YEL, stroke=5)
        text_center(dd, ID['marca']['assinatura'][0], H - 150, 'semi', 32, (220, 240, 235))
        text_center(dd, 'BINDER Vision · ' + ID['marca']['assinatura'][2], H - 100, 'black', 38, EM)
    return im.convert('RGB')

if __name__ == '__main__':
    if FMT == 'carrossel':
        n = len(CFG['slides'])
        for i, s in enumerate(CFG['slides']): slide(s, i, n).save(f'{OUT}/{CFG["id"]}_carrossel_{i + 1:02d}.png')
        print(OUT)
    elif MODE == 'stills' and CFG.get('modo') == 'decks':
        T = timeline_decks()
        for s in sys.argv[3:]: frame_decks(float(s), T).save(f'{OUT}/still_{float(s):05.2f}.png')
    elif MODE == 'stills':
        T = timeline(); P = ID['musica']['periodo']
        if CFG.get('comparacao'): T['comparacao'] = CFG['comparacao']['batida'] * P; T['comparacao_fim'] = CFG['comparacao']['batida_fim'] * P
        for s in sys.argv[3:]: frame_anim(float(s), T).save(f'{OUT}/still_{float(s):05.2f}.png')
    else:
        render_anim()
        if FMT == 'reel':   # regra do fundador (15/11/2026): todo Reel do ABISMO sai com capa
            subprocess.run([sys.executable, '-I', f'{HERE}/capa.py', POST], check=True)
