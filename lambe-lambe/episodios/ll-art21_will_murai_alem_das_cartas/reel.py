"""LL-ART21 · Will Murai — Além das cartas. Reel documental 9:16 (piloto), só deste episódio.
Reutiliza as peças do kit Lambe-lambe (kit_carrossel/motor_padrao.py: selo, kraft, fitas, carta, faixa preta; fontes do
preparar_fontes.sh). Sem voz, sem música, sem IA, sem créditos externos: tipografia cinética + efeitos sintetizados próprios.
Uso: python3 -I reel.py <pasta_cartas> <saida.mp4>   ·   capa: python3 -I reel.py <pasta_cartas> <capa.png> --capa   (pasta com saheeli.png, clique.png, biomancer.png do Scryfall)
1080x1920, 30 fps, H.264 + AAC; termina com comum/outro/outro_binder_916.mp4."""
import sys, os, asyncio, subprocess, wave, cv2, numpy as np
CART, OUT = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(AQUI, '../../kit_carrossel')))
import motor_padrao as M
import compor
from compor import colar, rasgo_alpha
from playwright.async_api import async_playwright
W, H, FPS, DUR = 1080, 1920, 30, 54.0
FECHO = os.path.normpath(os.path.join(AQUI, '../../../comum/outro/outro_binder_916.mp4'))
CX = 500  # centro útil (zona segura: 140 px à direita)
C = {k: os.path.join(CART, k + '.png') for k in ('saheeli', 'clique', 'biomancer')}

# ---------------- peças ----------------
def matte(draw, w=1080, h=1350):
    k = np.zeros((h, w, 3), np.uint8); wb = draw(np.full_like(k, 255)).astype(np.float32); kb = draw(k).astype(np.float32)
    al = np.clip(1 - (wb - kb).mean(2) / 255, 0, 1)
    rgb = np.where(al[..., None] > .02, kb / np.maximum(al[..., None], 1e-3), 0)
    ys, xs = np.where(al > .02)
    return np.clip(rgb[ys.min():ys.max() + 1, xs.min():xs.max() + 1], 0, 255).astype(np.float32), al[ys.min():ys.max() + 1, xs.min():xs.max() + 1].astype(np.float32)

def carta(k, larg):
    return matte(lambda b: M.carta(b, C[k], 540, 675, larg, 0, fitas=((-1.0, -1.04, -45), (1.0, -1.04, 45)), fl=int(larg * .2)))

def lupa_credito():
    """ampliação controlada do rodapé da Saheeli Rai (o crédito impresso), numa impressão com fita: não tapa a carta"""
    c = cv2.imread(C['saheeli']); r = c[968:1018, 30:340]
    r = cv2.resize(r, None, fx=2.7, fy=2.7, interpolation=cv2.INTER_LANCZOS4)
    return matte(lambda b: M.impressa(b, r, 540, 400, r.shape[1], 0, fitas=((-.93, -1, -8), (.93, -1, 8)), seed=31)[0])

def kraft_peca(w, h, k=0, seed=0):
    return matte(lambda b: M.papel(b, 540 - w // 2, 675 - h // 2, w, h, 0, k, seed))

def creme(w, h, cor=(222, 232, 238), seed=5):
    r = np.random.default_rng(seed); p = np.zeros((h, w, 3), np.float32) + cor
    p += cv2.GaussianBlur(r.normal(0, 1, (h, w)).astype(np.float32), (0, 0), 1.5)[..., None] * 5
    a = rasgo_alpha(w, h, 7, seed).astype(np.float32) / 255
    return np.clip(p, 0, 255), a

SELO = matte(lambda b: M.selo(b, 540, 675, 1.0, 0))
FAIXA = matte(lambda b: M.rodape(b, 675, 0))

# ---------------- textos (fontes do kit, renderizados no Chrome numa só sessão) ----------------
CSS = compor.CSS.replace('#s{width:1080px;height:1350px', '#s{width:1080px;height:1920px') + \
    "@font-face{font-family:JP;src:local('Noto Serif CJK JP Black'),local('Noto Serif CJK SC Black'),local('Noto Serif CJK JP')}\n"
TXT = {}
def T(nome, html): TXT[nome] = html

async def _render_textos():
    cwd = os.getcwd(); os.chdir(M.KIT); out = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--allow-file-access-from-files'])
        pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        for nome, html in TXT.items():
            f = os.path.abspath('_ll21.html')
            open(f, 'w').write(f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body><div id='s'><div style='position:absolute;left:40px;top:40px'>{html}</div></div></body></html>")
            await pg.goto('file://' + f); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(120)
            await pg.locator('#s').screenshot(path='_ll21.png', omit_background=True)
            t = cv2.imread('_ll21.png', cv2.IMREAD_UNCHANGED).astype(np.float32); ys, xs = np.where(t[..., 3] > 3)
            t = t[ys.min():ys.max() + 1, xs.min():xs.max() + 1]; out[nome] = (t[..., :3], t[..., 3] / 255)
        await b.close()
    for f in ('_ll21.html', '_ll21.png'):
        if os.path.exists(f): os.remove(f)
    os.chdir(cwd); return out

big = lambda s, fs=110, cor='#111': f'<div class="e ab" style="position:relative;font-size:{fs}px;color:{cor}">{s}</div>'
rb = lambda s, fs=46, cor='#111': f'<div class="e rb" style="position:relative;font-size:{fs}px;color:{cor}">{s}</div>'
mao = lambda s, fs=54, cor='#111': f'<div class="e" style="position:relative;font-family:CB;font-size:{fs}px;color:{cor}">{s}</div>'
geist = lambda s, fs=22, cor='#2a2a2a': f'<div style="position:relative;font-family:Geist;font-weight:500;font-size:{fs}px;color:{cor}">{s}</div>'

T('conhece', big('VOCÊ CONHECE', 78) + big('ESTA ARTE.', 78, '#E61E6E'))
T('quem', big('MAS CONHECE', 78) + big('QUEM PINTOU?', 78, '#E61E6E'))
T('creditos', rb('Nos créditos da carta:', 40) + big('WILLIAN MURAI', 84))
T('site', rb('No site dele, assina:', 40) + big('WILL MURAI', 96, '#E61E6E'))
T('ilustrador', big('ILUSTRADOR', 96))
T('concept', big('E CONCEPT ARTIST', 64, '#E61E6E'))
T('brasil', '<div class="e" style="position:relative;font-family:CB;font-size:58px;color:#fff">Do Brasil</div>')
T('trabalhou', rb('Já trabalhou com', 52))
for k, s in (('wotc', 'WIZARDS OF THE COAST'), ('bliz', 'BLIZZARD'), ('phx', 'PHOENIX LABS')): T(k, big(s, 60))
T('n53', big('53', 150, '#E61E6E'))
T('n53b', rb('ilustrações diferentes creditadas<br>a Willian Murai no Scryfall', 36))
T('n53f', geist('Scryfall, consulta de 26/11/2026'))
T('antes', rb('Antes dos videogames,', 50) + rb('passou por:', 50))
for k, s, cor in (('t1', 'QUADRINHOS', '#111'), ('t2', 'PUBLICIDADE', '#111'), ('t3', 'EDITORAS', '#111')): T(k, big(s, 74, cor))
T('t4', big('VIDEOGAMES', 80, '#E61E6E'))
T('tf', geist('Fonte: entrevista a Shoutout LA'))
T('lado1', big('MAS EXISTE UM LADO', 64, '#fff'))
T('lado2', big('MAIS PESSOAL.', 96, '#FFD84A'))
T('ger1', rb('Ele é de', 52))
T('ger2', big('TERCEIRA GERAÇÃO', 66))
T('ger3', big('JAPONESA.', 100, '#E61E6E'))
T('nasc1', big('NASCEU E CRESCEU', 64))
T('nasc2', big('NO BRASIL.', 100, '#E61E6E'))
T('kanji', '<div style="position:relative;font-family:JP,\'Noto Serif CJK JP\',serif;font-weight:900;font-size:300px;line-height:1;color:#111">秀樹</div>')
T('hideki', big('HIDEKI', 110, '#E61E6E'))
T('avo', mao('o nome do meio, dado pela avó', 60))
T('url', geist('willmurai.com/about', 30, '#555'))
T('site1', rb('No próprio site, ele conta que<br>vem explorando a <b style="color:#E61E6E">cultura</b> e a<br><b style="color:#E61E6E">história dos antepassados</b>.', 50))
T('hom1', rb('E diz que o site é uma', 56))
T('hom2', big('HOMENAGEM', 92, '#E61E6E'))
T('hom3', rb('a essa herança.', 56))
for k, s in (('ink1', 'Momotaro'), ('ink2', 'Zen'), ('ink3', 'Chrysanthemum')): T(k, mao(s, 52))
T('inkf', geist('Títulos de desenhos da série Inktober (loja INPRNT do artista)'))
T('das1', big('DAS CARTAS DE MAGIC', 58))
T('das2', '<div class="e ab" style="position:relative;font-size:60px;line-height:1.25;padding-top:10px;color:#E61E6E">À PRÓPRIA HISTÓRIA.</div>')
T('nome', big('WILL MURAI', 100))
T('slogan', rb('Um artista, <y>muitos universos.</y>', 54))
T('alem', '<div class="e ab" style="position:relative;font-size:70px;line-height:1.25;padding-top:10px;color:#E61E6E">ALÉM DAS CARTAS</div>')
T('cred', '<div style="position:relative;font-family:Geist;font-weight:500;font-size:19px;line-height:1.35;color:#D9D2C4;text-align:center">'
          'Saheeli Rai (KLD 186) · Vendilion Clique (MM2 67) · Master Biomancer (GTC 176)<br>'
          'Arte: Willian Murai · © Wizards of the Coast · Conteúdo de fã não oficial<br>Fontes: willmurai.com, Scryfall</div>')

def em_papel(txt, pad=(50, 34), tipo='creme', k=0, seed=0):
    """texto impresso numa tira de papel (creme, kraft ou verde «Do Brasil»)"""
    rgb, a = txt; h, w = a.shape; PW, PH = w + 2 * pad[0], h + 2 * pad[1]
    if tipo == 'kraft':
        pr, pa = M.kraft(PW, PH, k, seed).astype(np.float32), rasgo_alpha(PW, PH, 9, 40 + seed).astype(np.float32) / 255
    elif tipo == 'verde':
        pr, pa = creme(PW, PH, (74, 158, 30), seed)
    else:
        pr, pa = creme(PW, PH, seed=seed)
    y, x = pad[1], pad[0]; A = a[..., None]
    pr[y:y + h, x:x + w] = pr[y:y + h, x:x + w] * (1 - A) + rgb * A
    return pr, pa

def na_faixa(txt):
    fr, fa = FAIXA; fr = fr.copy(); rgb, a = txt; h, w = a.shape; fh, fw = fa.shape
    s = min(1.0, (fw - 90) / w, (fh - 40) / h)
    if s < 1: rgb, a = cv2.resize(rgb, None, fx=s, fy=s), cv2.resize(a, None, fx=s, fy=s); h, w = a.shape
    y, x = (fh - h) // 2, (fw - w) // 2; A = a[..., None]
    fr[y:y + h, x:x + w] = fr[y:y + h, x:x + w] * (1 - A) + rgb * A
    return fr, fa

# ---------------- muro ----------------
def muro(seed=3):
    rng = np.random.default_rng(seed)
    tiras = [M.src[i][:, x0:x0 + 60] for i in (0, 1) for x0 in (0, 1020)]
    hp = np.zeros((H, W, 3), np.float32)
    for x in range(0, W, 60):
        t = tiras[rng.integers(4)].astype(np.float32); t = np.vstack([t, t[::-1]])[:H]
        if rng.random() < .5: t = t[:, ::-1]
        hp[:, x:x + 60] = (t - cv2.GaussianBlur(t, (0, 0), 6))[:, :min(60, W - x)]
    rosa = np.median(np.vstack([t.reshape(-1, 3) for t in tiras]), 0)
    m = np.zeros((H, W, 3), np.float32) + rosa
    lf = cv2.resize(rng.normal(0, 1, (8, 5)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)[..., None]
    gr = sum(cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), sg) * k for sg, k in ((1, 5), (3, 6), (12, 9)))[..., None]
    m = m * (1 + lf * .05) + gr + cv2.GaussianBlur(np.clip(hp, -30, 30), (0, 0), 2) * .18
    for i, x in enumerate((0, 50, W - 110, W - 60)):
        t = tiras[i % 4]; t = np.vstack([t, t[::-1], t])[:H].astype(np.float32)
        m[:, x:x + 60] = m[:, x:x + 60] * .55 + t * .45
    return np.clip(m, 0, 255).astype(np.float32)

# ---------------- animação ----------------
def cl(x): return min(1.0, max(0.0, x))
def ease(u): return u * u * (3 - 2 * u)
def mola(t): return float(np.exp(-8 * t) * np.cos(18 * t)) if t > 0 else 1.0

class E:
    def __init__(s, peca, cx, cy, t0, modo='bate', ang=0.0, esc=1.0, som=None):
        s.rgb, s.a = peca; s.cx, s.cy, s.t0, s.modo, s.ang, s.esc = cx, cy, t0, modo, ang, esc
        s.som = som if som is not None else {'bate': 'tapa', 'carimbo': 'carimbo', 'desliza': 'zip', 'revela': 'zip', 'surge': None}[modo]

def estado(e, t):
    u = t - e.t0
    if u < 0: return None
    if e.modo == 'bate':
        d = .16
        if u < d: k = cl(u / d); return 1.35 - .35 * k ** 2, 0, 0, k, 1
        return 1 + .03 * mola(u - d), 0, 0, 1, 1
    if e.modo == 'carimbo':
        d = .1
        if u < d: k = cl(u / d); return 1.7 - .7 * k, 0, 0, k, 1
        return 1 - .04 * mola(u - d), 0, 0, 1, 1
    if e.modo == 'desliza':
        k = ease(cl(u / .28)); return 1, -(1 - k) * 420, 0, cl(u / .12), 1
    if e.modo == 'revela':
        return 1, 0, 0, 1, ease(cl(u / .45))
    k = ease(cl(u / .3)); return 1, 0, (1 - k) * 30, k, 1  # surge

def pinta(out, e, t, cam):
    st = estado(e, t)
    if st is None: return
    sc, dx, dy, op, rev = st
    rgb, a = e.rgb, e.a
    if rev < 1:
        w = max(1, int(a.shape[1] * rev)); a = a.copy(); a[:, w:] = 0
    h, w = a.shape; s = sc * e.esc * cam[0]
    cx = (e.cx + dx - W / 2) * cam[0] + W / 2 + cam[1]; cy = (e.cy + dy - H / 2) * cam[0] + H / 2 + cam[2]
    Mx = cv2.getRotationMatrix2D((w / 2, h / 2), -e.ang, s); Mx[0, 2] += cx - w / 2; Mx[1, 2] += cy - h / 2
    x0, y0 = int(max(0, cx - w * s * .75 - 20)), int(max(0, cy - h * s * .75 - 20))
    x1, y1 = int(min(W, cx + w * s * .75 + 20)), int(min(H, cy + h * s * .75 + 20))
    if x1 <= x0 or y1 <= y0: return
    Mx[0, 2] -= x0; Mx[1, 2] -= y0
    R = cv2.warpAffine(rgb, Mx, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR)
    A = cv2.warpAffine(a, Mx, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR)[..., None] * op
    reg = out[y0:y1, x0:x1]
    if e.modo in ('bate', 'carimbo'):
        sh = cv2.GaussianBlur(A[..., 0], (0, 0), 10)
        sh = np.roll(sh, (12, 6), (0, 1))[..., None]
        reg *= 1 - sh * .28
    reg[:] = reg * (1 - A) + R * A

# ---------------- montagem ----------------
def cenas(TX):
    tx = lambda k: TX[k]
    P = lambda nome, **kw: em_papel(TX[nome], **kw)
    S = {}
    # 0–3 · gancho: a carta cai no muro; o selo bate
    S[0.0] = [E(carta('saheeli', 560), CX, 860, -.1, 'bate', -1.2), E(SELO, 300, 330, .9, 'carimbo', -3),
              E(P('conhece', seed=2), CX, 1420, 1.6, 'bate', 1.5)]
    # 3–6 · lupa no crédito
    S[3.0] = [E(carta('saheeli', 450), CX - 150, 690, 0, 'surge', -1.2, som=''), E(lupa_credito(), CX + 40, 1185, 3.25, 'bate', 2),
              E(P('quem', seed=3), CX, 1410, 4.1, 'bate', -1.5)]
    # 6–9 · Willian → Will
    S[6.0] = [E(carta('saheeli', 330), CX + 230, 560, 0, 'surge', 3, som=''), E(P('creditos', seed=4), CX - 40, 980, 6.15, 'bate', -1.5),
              E(P('site', tipo='kraft', k=1, seed=5), CX + 10, 1290, 7.5, 'bate', 1.5)]
    # 9–12 · ilustrador e concept artist, do Brasil
    S[9.0] = [E(tx('ilustrador'), CX, 760, 9.1, 'carimbo'), E(P('concept', seed=21), CX, 930, 9.75, 'desliza'),
              E(P('brasil', tipo='verde', seed=6), CX + 180, 1130, 10.6, 'bate', -4, som='carimbo')]
    # 12–15 · onde trabalhou (tipografia, sem logótipos)
    S[12.0] = [E(tx('trabalhou'), CX, 560, 12.1, 'surge'), E(P('wotc', tipo='kraft', k=0, seed=7), CX, 790, 12.55, 'bate', -2),
               E(P('bliz', tipo='kraft', k=1, seed=8), CX - 40, 1010, 13.25, 'bate', 1.5), E(P('phx', tipo='kraft', k=2, seed=9), CX + 30, 1230, 13.95, 'bate', -1)]
    # 15–18 · as cartas
    S[15.0] = [E(carta('clique', 330), CX - 300, 760, 15.05, 'bate', -4), E(carta('biomancer', 330), CX + 300, 760, 15.5, 'bate', 4),
               E(carta('saheeli', 340), CX, 720, 15.95, 'bate', 0), E(P('n53', pad=(40, 10), seed=22), CX - 330, 1250, 16.6, 'carimbo'),
               E(P('n53b', seed=10), CX + 130, 1250, 16.9, 'bate', 1, som='tapa'), E(P('n53f', pad=(24, 14), seed=23), CX + 130, 1420, 17.2, 'surge')]
    # 18–24 · linha do tempo
    linha = (np.full((900, 12, 3), (110, 30, 230), np.float32), np.ones((900, 12), np.float32))
    S[18.0] = [E(tx('antes'), CX, 430, 18.1, 'surge')] + \
        [E(P(k, tipo='kraft' if k != 't4' else 'creme', k=i, seed=11 + i), CX + (-60 if i % 2 else 40), 700 + i * 230, t0, 'bate', (-1.5, 1.5)[i % 2])
         for i, (k, t0) in enumerate((('t1', 18.75), ('t2', 19.85), ('t3', 20.95), ('t4', 22.1)))] + [E(P('tf', pad=(24, 14), seed=24), CX, 1500, 22.6, 'surge')]
    S[18.0].insert(1, E(linha, CX - 330, 1050, 18.5, 'surge', som=''))
    # 24–27 · virada
    S[24.0] = [E(na_faixa(tx('lado1')), CX, 820, 24.1, 'bate'), E(tx('lado2'), CX, 1010, 24.85, 'carimbo')]
    # 27–30 · terceira geração japonesa
    S[27.0] = [E(tx('ger1'), CX, 700, 27.05, 'surge'), E(tx('ger2'), CX, 830, 27.4, 'desliza'), E(P('ger3', seed=25), CX, 1030, 28.1, 'carimbo', som='revela')]
    # 30–33 · nasceu e cresceu no Brasil
    S[30.0] = [E(tx('nasc1'), CX, 800, 30.1, 'desliza'), E(P('nasc2', seed=26), CX, 1000, 30.75, 'carimbo'),
               E(P('brasil', tipo='verde', seed=6), CX + 200, 1230, 31.5, 'bate', -4, som='carimbo')]
    # 33–37 · Hideki
    S[33.0] = [E(P('kanji', pad=(70, 50), seed=14), CX, 760, 33.1, 'bate', -1.5), E(P('hideki', seed=27), CX, 1110, 33.85, 'carimbo', som='revela'),
               E(tx('avo'), CX, 1280, 34.7, 'revela')]
    # 37–41 · o site
    S[37.0] = [E(P('site1', pad=(60, 70), seed=15), CX, 900, 37.1, 'bate', -1), E(P('url', pad=(24, 14), seed=28), CX, 640, 37.6, 'surge'),
               E(SELO, CX - 210, 1240, 38.6, 'carimbo', -4)]
    # 41–45 · homenagem
    S[41.0] = [E(tx('hom1'), CX, 640, 41.1, 'surge'), E(P('hom2', seed=29), CX, 790, 41.55, 'carimbo', som='revela'), E(tx('hom3'), CX, 940, 42.1, 'surge'),
               E(P('ink1', tipo='kraft', k=0, seed=16), CX - 250, 1120, 42.8, 'bate', -5), E(P('ink2', tipo='kraft', k=1, seed=17), CX + 20, 1150, 43.25, 'bate', 3),
               E(P('ink3', tipo='kraft', k=2, seed=18), CX + 200, 1290, 43.7, 'bate', -2), E(P('inkf', pad=(24, 14), seed=30), CX, 1440, 44.1, 'surge')]
    # 45–50 · de volta às cartas
    S[45.0] = [E(carta('clique', 300), CX - 290, 760, 45.1, 'bate', -4), E(carta('saheeli', 300), CX, 730, 45.4, 'bate', 0),
               E(carta('biomancer', 300), CX + 290, 760, 45.7, 'bate', 4), E(P('das1', seed=19), CX, 1180, 46.5, 'bate', -1),
               E(P('das2', seed=31), CX, 1350, 47.5, 'carimbo')]
    # 50–54 · assinatura
    S[50.0] = [E(SELO, CX, 560, 50.05, 'carimbo', -2), E(tx('nome'), CX, 790, 50.4, 'carimbo', som='revela'), E(tx('slogan'), CX, 940, 51.0, 'revela'),
               E(carta('saheeli', 260), CX, 1180, 51.6, 'bate', -2), E(na_faixa(tx('cred')), CX, 1470, 52.1, 'bate')]
    return S

def camera(t, t0):
    u = t - t0; s = 1.0 + .012 * u / 4
    tr = [x for x in BATIDAS if 0 <= t - x < .25]
    j = 7 * (1 - (t - tr[-1]) / .25) if tr else 0
    return s, j * np.sin(t * 90), j * np.cos(t * 70)

# ---------------- som (sintetizado, sem bibliotecas externas) ----------------
SR = 48000
def ruido(n, seed): return np.random.default_rng(seed).normal(0, 1, n)
def env(n, at, dec): t = np.arange(n) / SR; return np.minimum(1, t / max(at, 1e-4)) * np.exp(-t / dec)
def lp(x, k):
    k = max(1, int(k)); return np.convolve(x, np.ones(k) / k, 'same')
def sfx(tipo, seed):
    n = int(SR * .6); t = np.arange(n) / SR
    if tipo == 'tapa':
        x = lp(ruido(n, seed), 6) * env(n, .002, .045) * .9 + np.sin(2 * np.pi * 95 * t) * env(n, .003, .08) * .8
    elif tipo == 'carimbo':
        x = np.sin(2 * np.pi * (70 + 60 * np.exp(-t * 30)) * t) * env(n, .002, .12) + lp(ruido(n, seed), 3) * env(n, .001, .02) * .6
    elif tipo == 'zip':
        x = ruido(n, seed) * env(n, .03, .09) * .35; x = x - lp(x, 12)
    elif tipo == 'revela':
        x = (np.sin(2 * np.pi * 880 * t) + .6 * np.sin(2 * np.pi * 1320 * t) + .3 * np.sin(2 * np.pi * 1760 * t)) * env(n, .004, .18) * .45
        x += np.sin(2 * np.pi * (70 + 60 * np.exp(-t * 30)) * t) * env(n, .002, .12) * .8
    elif tipo == 'corte':
        x = ruido(n, seed) * env(n, .12, .1) * .4; x = lp(x, 4) - lp(x, 40)
    else:
        return np.zeros(n)
    return x

def trilha(S):
    n = int(SR * DUR); a = np.zeros(n)
    amb = lp(ruido(n, 99), 30) * .05  # ar do muro, discreto
    a += amb
    def mix(x, t):
        i = int(t * SR); m = min(len(x), n - i)
        if m > 0: a[i:i + m] += x[:m]
    k = 0
    for t0, els in S.items():
        if t0 > 0: mix(sfx('corte', k), t0 - .08); k += 1
        for e in els:
            if e.som: mix(sfx(e.som, k), e.t0 + (.16 if e.modo == 'bate' else .1 if e.modo == 'carimbo' else 0)); k += 1
    a = np.tanh(a / np.max(np.abs(a)) * 3) / np.tanh(3)  # efeitos densos (compressão suave)
    a = a / np.max(np.abs(a)) * 10 ** (-6 / 20)  # pico −6 dBFS (bíblia)
    return a

if __name__ == '__main__':
    TX = asyncio.run(_render_textos())
    if '--capa' in sys.argv:  # capa 9:16: muro, selo azul, nome e carta inteira; sem retrato
        out = muro(5)
        BATIDAS = []
        for e in [E(SELO, CX, 470, -9, 'surge', -3), E(TX['nome'], CX, 650, -9, 'surge'),
                  E(em_papel(TX['alem'], seed=40), CX, 800, -9, 'surge', -1.5), E(carta('saheeli', 480), CX, 1230, -9, 'surge', 2)]:
            pinta(out, e, 0, (1, 0, 0))
        cv2.imwrite(OUT, np.clip(out, 0, 255).astype(np.uint8)); print('ok', OUT); sys.exit()
    S = cenas(TX)
    T0 = sorted(S)
    BATIDAS = [e.t0 + (.16 if e.modo == 'bate' else .1) for els in S.values() for e in els if e.modo in ('bate', 'carimbo')]
    MUROS = [muro(3 + i) for i in range(3)]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    wav = OUT.replace('.mp4', '_som.wav'); a = (trilha(S) * 32767).astype(np.int16)
    with wave.open(wav, 'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(a.tobytes())
    corpo = OUT.replace('.mp4', '_corpo.mp4')
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', corpo], stdin=subprocess.PIPE)
    chaves = {int(x * FPS) for x in (1.0, 2.5, 5.0, 8.5, 11.5, 14.5, 17.5, 23.0, 26.0, 29.5, 32.5, 36.0, 40.0, 44.5, 49.0, 53.5)}
    for i in range(int(DUR * FPS)):
        t = i / FPS; t0 = max(x for x in T0 if x <= t + 1e-6); ci = T0.index(t0)
        out = MUROS[ci % 3].copy(); cam = camera(t, t0)
        for e in S[t0]: pinta(out, e, t, cam)
        f = np.clip(out, 0, 255).astype(np.uint8); ff.stdin.write(f.tobytes())
        if i in chaves: cv2.imwrite(OUT.replace('.mp4', f'_f{i:04d}.jpg'), f, [cv2.IMWRITE_JPEG_QUALITY, 85])
    ff.stdin.close(); ff.wait()
    # loudness da casa (−14 LUFS, pico < −1 dBTP): ganho medido em duas passagens sobre o próprio som
    def lufs(cad):
        r = subprocess.run(['ffmpeg', '-nostats', '-i', wav, '-af', cad + ',ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
        return float(r.rsplit('I:', 1)[1].split('LUFS')[0])
    base = 'acompressor=threshold=-24dB:ratio=4:attack=5:release=120'
    g = 0.0
    for _ in range(3):
        cad = f'{base},volume={g:.2f}dB,alimiter=limit=0.63:level=false'
        g += -12.6 - lufs(cad)  # +1,4 LU: compensação medida no ficheiro final (AAC + fecho), QC de 26/11
    AUD = f'{base},volume={g:.2f}dB,alimiter=limit=0.63:level=false'
    # fecho do scanner (regra de todos os vídeos)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', corpo, '-i', FECHO, '-i', wav, '-filter_complex',
                    '[0:v]setsar=1[a];[1:v]scale=1080:1920,setsar=1,fps=30[b];[a][b]concat=n=2:v=1:a=0[v];'
                    '[2:a]%s,apad=whole_dur=%.3f,aresample=48000[s]' % (AUD, DUR + 3.867),
                    '-map', '[v]', '-map', '[s]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', OUT], check=True)
    os.remove(corpo)
    print('ok', OUT)
