"""Motor de vídeo do Lambe-lambe (padrão desde 26/11/2026, decisão do fundador): o vídeo do LL-ECO01 como modelo de todos os vídeos.
Linguagem: muro rosa; cada cena começa com um cartaz grande colado por cima do anterior; peças (papel com texto, cartas, logos,
autocolantes) voam e batem no muro com mola e sombra; câmara com recuo de abertura (objeto em tela cheia no quadro 0) e tremor
em cada impacto; efeitos sintetizados próprios (pico −6 dBFS); fecho oficial do scanner. Peças assentes são «cozidas» no muro.

Uso num episódio (script próprio na pasta do episódio):
    import sys; sys.path.insert(0, '<raiz>/lambe-lambe/kit_video'); import motor_video as V
    t = {'a': V.caixa(860, 200, V.T('Texto', 80))}; V.render_textos()
    L = [V.Peca(V.peca_carta(png, 460), 540, 990, 0, modo='fixa'), V.Peca(V.peca_folha(1010, 1560, 'creme', 6), 540, 945, 2.4, .4, de=(0, -1900), som='grande'), ...]
    V.render(L, dur, 'saida.mp4', audio=True)
Modos de peça: 'bate' (voa e cola), 'pop' (autocolante), 'carimbo' (texto carimbado), 'fixa' (já está no muro).
Tipos de papel: creme, kraft, preto, amarelo, verde. Zona segura do texto: y 280–1500, x 80–1000 (Stories e Reels).
Regras: carta inteira, sem filtro, fita só nos cantos de cima, nada sobre a arte ou o rodapé; zero créditos externos."""
import sys, os, json, asyncio, subprocess, wave
import cv2, numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, '../..'))
KIT = os.path.join(RAIZ, 'lambe-lambe/kit_carrossel')
sys.path.insert(0, KIT)
_cwd = os.getcwd()
import motor_padrao as M          # muda o cwd para o kit (fontes relativas)
os.chdir(_cwd)
from compor import colar, rasgo_alpha, aplicar, CSS, navegador
FECHO = os.path.join(RAIZ, 'comum/outro/outro_binder_916.mp4')
MAGIC = os.path.join(RAIZ, 'comum/marcas/magic_logo_recortado.png')
PLAY = os.path.join(RAIZ, 'comum/marcas/google_play_badge_ptbr.png')

PRETO, VERDE, ROSA, AMAR = '#050A10', '#10B981', '#E61E6E', '#FFD84A'

# ------------------------------------------------------------------ texto (Playwright, uma sessão para todas as camadas)
_FILA = []
def html_camada(html, w, h):
    """regista uma camada de texto; devolve índice. Renderização em lote por render_textos()."""
    _FILA.append((html, w, h)); return len(_FILA) - 1
_TX = {}
def render_textos():
    from playwright.async_api import async_playwright
    async def go():
        async with async_playwright() as p:
            b = await p.chromium.launch(**navegador())
            pg = await b.new_page(viewport={"width": 1080, "height": 1920})
            for i, (html, w, h) in enumerate(_FILA):
                if i in _TX: continue
                f = os.path.join(KIT, f'_eco_{os.getpid()}_{i}.html'); o = os.path.join(KIT, f'_eco_{os.getpid()}_{i}.png')
                css = CSS.replace('#s{width:1080px;height:1350px', f'#s{{width:{w}px;height:{h}px')
                open(f, 'w').write(f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{css}"
                                   "@font-face{font-family:JP;src:local('Noto Serif CJK JP Black'),local('Noto Serif CJK JP')}.e y{color:#FFD84A;font-style:italic;font-weight:900}.g{color:#10B981}.k{color:#E61E6E}</style></head>"
                                   f"<body><div id='s'>{html}</div></body></html>")
                await pg.set_viewport_size({"width": w, "height": h})
                await pg.goto("file://" + f); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(120)
                await pg.locator("#s").screenshot(path=o, omit_background=True)
                _TX[i] = cv2.imread(o, cv2.IMREAD_UNCHANGED); os.remove(f); os.remove(o)
            await b.close()
    asyncio.run(go())

# aplicar(base, None, claro) não está previsto no kit: versão local só para tinta clara
def _aplicar_claro(base, claro_png):
    out = base.astype(np.float32)
    t = cv2.imread(claro_png, cv2.IMREAD_UNCHANGED).astype(np.float32)
    a = cv2.GaussianBlur(t[..., 3] / 255.0, (0, 0), 0.6)[..., None]; c = t[..., :3]
    lum = cv2.GaussianBlur(base.astype(np.float32).mean(2), (0, 0), 1)
    tex = 0.9 + 0.4 * ((lum - cv2.GaussianBlur(lum, (0, 0), 4)) / 255.0)[..., None]
    return np.clip(out * (1 - a) + np.clip(c * tex, 0, 255) * a, 0, 255).astype(np.uint8)
def tinta(base, idx, claro=False):
    t = _TX[idx]; h, w = base.shape[:2]
    if t.shape[:2] != (h, w): t = cv2.resize(t, (w, h))
    f = os.path.join(KIT, f'_eco_{os.getpid()}_tmp.png'); cv2.imwrite(f, t)
    out = _aplicar_claro(base, f) if claro else aplicar(base, f)
    os.remove(f); return out

# ------------------------------------------------------------------ peças (RGBA) pelo método «matte» do motor_story
CW, CH = 1080, 1920
def matte(draw, cw=CW, ch=CH):
    k = np.zeros((ch, cw, 3), np.uint8); w = np.full_like(k, 255)
    kb = draw(k).astype(np.float32); wb = draw(w).astype(np.float32)
    al = np.clip(1 - (wb - kb).mean(2) / 255, 0, 1)
    rgb = np.where(al[..., None] > .02, kb / np.maximum(al[..., None], 1e-3), 0)
    ys, xs = np.where(al > .02); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    # deslocamento do centro da peça em relação ao centro do canvas (para posicionar no mundo)
    off = ((x0 + x1) / 2 - cw / 2, (y0 + y1) / 2 - ch / 2)
    return np.clip(rgb[y0:y1, x0:x1], 0, 255).astype(np.float32), al[y0:y1, x0:x1].astype(np.float32), off

def folha(base, w, h, tipo='creme', seed=0, ang=0.0, cx=CW / 2, cy=CH / 2):
    """papel de cartaz: kraft (modelos aprovados), creme (folha do carrossel clareada) ou preto BINDER (#050A10 com grão)"""
    r = np.random.default_rng(seed)
    if tipo == 'preto':
        p = np.zeros((h, w, 3), np.float32) + (16, 10, 5)
        k = M.kraft(w, h, seed % 3, seed).astype(np.float32).mean(2, keepdims=True)
        p += (k - k.mean()) * .10 + r.normal(0, 3.5, (h, w, 1))
    else:
        p = M.kraft(w, h, seed % 3, seed).astype(np.float32)
        if tipo == 'creme':
            p = p * .35 + np.array((214, 230, 238), np.float32) * .65   # papel cartaz creme, com a fibra do kraft
        elif tipo == 'amarelo':
            p = p * .30 + np.array((40, 200, 248), np.float32) * .70
        elif tipo == 'verde':
            p = p * .16 + np.array((122, 182, 12), np.float32) * .84
    return colar(base, np.clip(p, 0, 255).astype(np.uint8), rasgo_alpha(w, h, 12 if w > 400 else 7, 50 + seed), cx, cy, ang)

def peca_folha(w, h, tipo, seed, ang=0.0, tx=None, claro=False, fitas=()):
    def d(b):
        b = folha(b, w, h, tipo, seed, ang)
        if tx is not None: b = tinta(b, tx, claro)
        for dx, dy, fa in fitas: b = M.fita(b, CW / 2 + dx * w / 2, CH / 2 + dy * (h / 2 - 6), ang + fa, 120)
        return b
    return matte(d)

def peca_carta(path, larg, ang=0.0, fl=80):
    return matte(lambda b: M.carta(b, path, CW / 2, CH / 2, larg, ang, fitas=((-1.0, -1.04, -45), (1.0, -1.04, 45)), fl=fl))

def peca_img(img_bgr, larg, alpha=None, ang=0.0, margem=0, fundo=(238, 240, 240), seed=5, fitas=((0, -1, -6),)):
    """logo/ícone impresso: imagem intacta sobre papel (margem branca rasgada) e fita, como a «impressa» do kit"""
    h = int(img_bgr.shape[0] * larg / img_bgr.shape[1]); im = cv2.resize(img_bgr, (larg, h), interpolation=cv2.INTER_AREA)
    a = np.full((h, larg), 255, np.uint8) if alpha is None else cv2.resize(alpha, (larg, h), interpolation=cv2.INTER_AREA)
    def d(b):
        if margem:
            b = colar(b, np.full((h + 2 * margem, larg + 2 * margem, 3), fundo, np.uint8), rasgo_alpha(larg + 2 * margem, h + 2 * margem, 6, seed), CW / 2, CH / 2, ang)
        b = colar(b, im, a, CW / 2, CH / 2, ang, sombra=not margem)
        for dx, dy, fa in fitas: b = M.fita(b, CW / 2 + dx * larg / 2, CH / 2 + dy * (h / 2 + margem - 6), ang + fa, 110)
        return b
    return matte(d)

# ------------------------------------------------------------------ carta recortada à mão (padrão das cartas grandes, 26/11/2026)
def peca_carta_recortada(path, larg, ang=0.0, seed=1, margem=16, fitas=True):
    """carta inteira dentro de uma margem branca cortada à tesoura (segmentos retos irregulares) + fita nos cantos de cima"""
    im = cv2.imread(path, cv2.IMREAD_UNCHANGED); h = int(im.shape[0] * larg / im.shape[1])
    im = cv2.resize(im, (larg, h), interpolation=cv2.INTER_AREA)
    rgb, a = im[..., :3], (im[..., 3] if im.shape[2] == 4 else np.full((h, larg), 255, np.uint8))
    rng = np.random.default_rng(seed); W2, H2 = larg + 2 * margem + 20, h + 2 * margem + 20
    cx0, cy0 = W2 / 2, H2 / 2; pts = []
    for (x0, y0), (x1, y1) in (((-1, -1), (1, -1)), ((1, -1), (1, 1)), ((1, 1), (-1, 1)), ((-1, 1), (-1, -1))):
        for k in range(4):                      # 4 cortes de tesoura por lado
            u = k / 4 + rng.uniform(-.03, .03)
            x = cx0 + (x0 + (x1 - x0) * u) * (larg / 2 + margem) + rng.uniform(-margem * .45, margem * .45)
            y = cy0 + (y0 + (y1 - y0) * u) * (h / 2 + margem) + rng.uniform(-margem * .45, margem * .45)
            pts.append((x, y))
    msk = np.zeros((H2, W2), np.uint8); cv2.fillPoly(msk, [np.array(pts, np.int32)], 255, cv2.LINE_AA)
    papel = (cv2.resize(cv2.imread(os.path.join(KIT, 'kit_papel.png')), (W2, H2)).astype(np.float32) * .3 + np.array((236, 240, 242)) * .7).astype(np.uint8)
    def d(b):
        b = colar(b, papel, msk, CW / 2, CH / 2, ang)
        b = colar(b, rgb, a, CW / 2, CH / 2, ang, sombra=False)
        if fitas:
            for dx, fa in ((-1, -40), (1, 40)):
                b = M.fita(b, CW / 2 + dx * (larg / 2 + margem) * np.cos(np.deg2rad(ang)) + 0, CH / 2 - (h / 2 + margem - 4) + dx * (larg / 2) * np.sin(np.deg2rad(ang)), ang + fa, 120)
        return b
    return matte(d)

# ------------------------------------------------------------------ ícones (desenho conceitual, não telas do app)
def svg(w, h, corpo):
    return f'<svg style="position:absolute;left:0;top:0" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{corpo}</svg>'
PIN = ('<path d="M{x} {y} c-38 0 -66 28 -66 64 c0 48 66 112 66 112 s66 -64 66 -112 c0 -36 -28 -64 -66 -64z" fill="{c}"/>'
       '<circle cx="{x}" cy="{yc}" r="24" fill="#F2EDE2"/>')
def pin(x, y, c=PRETO): return PIN.format(x=x, y=y, yc=y + 62, c=c)
def avatar(x, y, r, c=PRETO):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{c}" stroke-width="10"/>'
            f'<circle cx="{x}" cy="{y - r * .22}" r="{r * .3}" fill="{c}"/>'
            f'<path d="M{x - r * .55} {y + r * .62} q{r * .55} {-r * .75} {r * 1.1} 0" fill="{c}"/>')
def balao(x, y, w, h, c=PRETO, dir=1):
    cauda = f'M{x + w * (.25 if dir > 0 else .75)} {y + h} l{-22 * dir} 34 l{40 * dir} -34z'
    pts = ''.join(f'<circle cx="{x + w * k}" cy="{y + h / 2}" r="11" fill="#F2EDE2"/>' for k in (.3, .5, .7))
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="{c}"/><path d="{cauda}" fill="{c}"/>{pts}'
TROFEU = ('<path d="M{x} {y} h120 v40 c0 50 -30 80 -60 84 c-30 -4 -60 -34 -60 -84z" fill="{c}"/>'
          '<path d="M{x} {y1} h-26 c0 34 16 50 34 52 M{x2} {y1} h26 c0 34 -16 50 -34 52" stroke="{c}" stroke-width="10" fill="none"/>'
          '<rect x="{x3}" y="{y2}" width="20" height="34" fill="{c}"/><rect x="{x4}" y="{y3}" width="80" height="18" fill="{c}"/>')
def trofeu(x, y, c=PRETO): return TROFEU.format(x=x, y=y, y1=y + 14, x2=x + 120, x3=x + 50, y2=y + 122, x4=x + 20, y3=y + 154, c=c)

# ------------------------------------------------------------------ textos
def T(texto, fs, cor=PRETO, fam='AB', peso='', extra='', w=1000, alin='center'):
    return (f'<div class="e" style="position:relative;width:{w}px;white-space:normal;text-align:{alin};font-family:{fam};{peso}'
            f'font-size:{fs}px;line-height:.98;color:{cor};letter-spacing:-1px;text-transform:uppercase;{extra}">{texto}</div>')

def caixa(w, h, html, pad=(0, 0)):
    """camada de texto centrada num canvas CWxCH, para imprimir numa folha de w×h centrada"""
    x0, y0 = (CW - w) / 2 + pad[0], (CH - h) / 2 + pad[1]
    return html_camada(f'<div style="position:absolute;left:{x0}px;top:{y0}px;width:{w}px;height:{h}px;display:flex;align-items:center;justify-content:center">'
                       f'<div style="position:relative;width:{w}px;min-height:{h if "<svg" in html else 0}px">{html}</div></div>', CW, CH)

# ------------------------------------------------------------------ física de colagem (do motor_story, sem alterações de método)
def cl(x): return min(1.0, max(0.0, x))
def ease_in(u): return u ** 3
def ease_io(u): return u * u * (3 - 2 * u)
def mola(t): return np.exp(-7 * t) * np.cos(16 * t) if t > 0 else 1.0
class Peca:
    def __init__(s, P, cx, cy, t0, dur=.42, de=(0, -1500), rot0=10, z0=1.3, esc=1.0, ang=0.0, modo='bate', som='papel'):
        s.rgb, s.al, off = P; s.h, s.w = s.al.shape
        s.cx, s.cy = cx + off[0], cy + off[1]
        s.t0, s.dur, s.de, s.rot0, s.z0, s.esc, s.ang, s.modo, s.som = t0, dur, de, rot0, z0, esc, ang, modo, som
        s.assenta = t0 + dur + .8
    def estado(s, t):
        u = (t - s.t0) / s.dur
        if u < 0: return None
        if s.modo == 'fixa':
            return dict(cx=s.cx, cy=s.cy, esc=s.esc, ang=s.ang, alt=0, dobra=0, rev=1)
        if s.modo == 'carimbo':                                 # texto carimbado no cartaz preto
            k = ease_io(cl(u))
            return dict(cx=s.cx, cy=s.cy, esc=s.esc * (1.10 - .10 * k), ang=s.ang, alt=0, dobra=0, rev=1, op=k)
        if s.modo == 'pop':                                     # adesivo: cresce do ponto com mola
            k = ease_io(cl(u)); m = mola(max(0, t - s.t0 - s.dur)) if u >= 1 else 0
            return dict(cx=s.cx, cy=s.cy, esc=s.esc * (.2 + .8 * k) * (1 + .08 * m), ang=s.ang + 12 * (1 - k), alt=0, dobra=0, rev=1, op=cl(u * 3))
        if t >= s.assenta:
            return dict(cx=s.cx, cy=s.cy, esc=s.esc, ang=s.ang, alt=0, dobra=0, rev=1)
        if u < 1:
            e = ease_in(u); alt = 1 - e
            return dict(cx=s.cx + s.de[0] * alt, cy=s.cy + s.de[1] * alt, esc=s.esc * (1 + (s.z0 - 1) * alt),
                        ang=s.ang + s.rot0 * alt, alt=alt, dobra=.10 * alt + .03, rev=1)
        d = t - (s.t0 + s.dur); m = mola(d)
        return dict(cx=s.cx, cy=s.cy, esc=s.esc * (1 - .03 * m), ang=s.ang - .9 * m, alt=0, dobra=max(0, .03 * np.exp(-9 * d)), rev=1)
    def impacto(s): return s.t0 + (s.dur if s.modo == 'bate' else 0)

def mat_peca(p, st):
    w, h = p.w, p.h; e = st['esc']; r = np.deg2rad(st['ang']); b = st['dobra']
    src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    loc = np.float32([[-w / 2 + b * w / 2, -h / 2 + b * h * .25], [w / 2 - b * w / 2, -h / 2 + b * h * .25], [w / 2, h / 2], [-w / 2, h / 2]]) * e
    R = np.array([[np.cos(r), -np.sin(r)], [np.sin(r), np.cos(r)]])
    dst = ((loc @ R.T) + [st['cx'], st['cy']]).astype(np.float32)
    return cv2.getPerspectiveTransform(src, dst)

def _roi(Mx, w, h, WH):
    """retângulo do quadro onde a peça (w×h) cai depois da transformação, com 2 px de folga; None se fica fora"""
    q = cv2.perspectiveTransform(np.float32([[[0, 0]], [[w, 0]], [[w, h]], [[0, h]]]), np.asarray(Mx, np.float64))[:, 0]
    if not np.isfinite(q).all(): return 0, 0, WH[0], WH[1]
    x0, y0 = max(0, int(np.floor(q[:, 0].min())) - 2), max(0, int(np.floor(q[:, 1].min())) - 2)
    x1, y1 = min(WH[0], int(np.ceil(q[:, 0].max())) + 2), min(WH[1], int(np.ceil(q[:, 1].max())) + 2)
    return None if x1 <= x0 or y1 <= y0 else (x0, y0, x1, y1)

def blend(out, rgb, al, Mx, op=1.0, WH=(CW, CH), inplace=False):
    """compõe a peça só na região que ela ocupa (27/11/2026; antes: o quadro inteiro por peça, 42 % do render).
    Fora dessa região o resultado antigo era out·(1−0) = out, por isso a imagem não muda (regressão em kit_video/LEIA-ME.md).
    inplace=True escreve em `out` (float32 próprio do render); por defeito devolve uma cópia, como antes."""
    # o mesmo tipo numérico que o cálculo antigo daria (op em np.float64 promove o quadro a float64): imagem igual bit a bit
    dt = np.result_type(out.dtype, (np.zeros(1, al.dtype) * op).dtype, np.float32 if rgb is None else rgb.dtype)
    if dt != out.dtype or not inplace: out = out.astype(dt)
    r = _roi(Mx, al.shape[1], al.shape[0], WH)
    if r is None: return out
    x0, y0, x1, y1 = r
    Mr = np.array([[1, 0, -x0], [0, 1, -y0], [0, 0, 1]], np.float64) @ np.asarray(Mx, np.float64)
    al2 = cv2.warpPerspective(al, Mr, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR)[..., None] * op
    reg = out[y0:y1, x0:x1]
    if rgb is None:
        reg *= (1 - al2)
    else:
        reg[...] = reg * (1 - al2) + cv2.warpPerspective(rgb, Mr, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR) * al2
    return out

def desenha(out, p, st, inplace=False):
    Mx = mat_peca(p, st)
    if st['alt'] > 0:
        off = np.array([[1, 0, 18 + 70 * st['alt']], [0, 1, 30 + 110 * st['alt']], [0, 0, 1]])
        out = blend(out, None, cv2.GaussianBlur(p.al, (0, 0), 4 + 20 * st['alt']), off @ Mx, .45 * (1 - .5 * st['alt']), inplace=inplace)
        inplace = True                                          # a partir daqui `out` já é uma cópia própria
    return blend(out, p.rgb, p.al, Mx, st.get('op', 1.0), inplace=inplace)

# ------------------------------------------------------------------ muro (o mesmo método do motor_story: restos dos modelos aprovados)
def muro(seed=3, W=CW, H=CH):
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

# ------------------------------------------------------------------ logos
def logo_binder():
    """lockup oficial (símbolo + «BINDER Vision») tirado do fecho oficial, quadro de 3,0 s, sem redesenho"""
    f = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', '3.0', '-i', FECHO, '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'],
                       capture_output=True, check=True).stdout
    f = np.frombuffer(f, np.uint8).reshape(1920, 1080, 3)
    return f[686:1114, 236:844].copy()
def logo_play():
    m = cv2.imread(PLAY, cv2.IMREAD_UNCHANGED); return m[..., :3], m[..., 3]
def logo_magic():
    m = cv2.imread(MAGIC, cv2.IMREAD_UNCHANGED); return m[..., :3], m[..., 3]

# ------------------------------------------------------------------ render
CADEIA = 'lowpass=f=11000,acompressor=threshold=0.03:ratio=6:attack=3:release=120:makeup=6,alimiter=limit=0.4:level=false:attack=2:release=40,aresample=48000'
def _pico_real(video):
    r = subprocess.run(['ffmpeg', '-nostats', '-i', video, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float([l for l in r.splitlines() if l.strip().startswith('Peak:')][-1].split()[1])
def render(L, dur, saida, fecho=True, audio=False, extras=(), abertura=(540, 990), zoom0=.34, folha=(), fps=30):
    """L: lista de Peca por ordem de t0. extras: funções f(out, t) -> out desenhadas por cima (ex.: traços a marcador).
    abertura: ponto focado no quadro 0 (zoom0 = aproximação inicial; 0 desliga). folha: tempos (s) para quadros-chave JPG."""
    L = sorted(L, key=lambda p: p.t0)
    W, H = CW, CH; NF = int(round(dur * fps)); base = muro(); baked = 0
    bat = sorted(p.impacto() for p in L if p.modo == 'bate')
    tmp = saida + '.v.mp4'
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(fps), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', tmp], stdin=subprocess.PIPE)
    chaves = {min(NF - 1, int(x * fps)) for x in folha}
    for i in range(NF):
        t = i / fps
        while baked < len(L) and t >= L[baked].assenta and all(t >= q.assenta for q in L[:baked]):
            p = L[baked]; base = desenha(base, p, p.estado(p.assenta), inplace=True); baked += 1
        out = base.copy()
        for p in L[baked:]:
            st = p.estado(t)
            if st is not None: out = desenha(out, p, st, inplace=True)
        for f in extras: out = f(out, t)
        s = 1.025 + .03 * ((t % 2.6) / 2.6)
        z = zoom0 * (1 - ease_io(cl((t - .08) / .55))) if zoom0 else 0
        s += z; fx = W / 2 + (abertura[0] - W / 2) * (z / zoom0 if zoom0 else 0); fy = H / 2 + (abertura[1] - H / 2) * (z / zoom0 if zoom0 else 0)
        sx = sy = 0
        for b in bat:
            d = t - b
            if 0 <= d < .2: k = np.exp(-18 * d); sx += 3 * k * np.sin(90 * d); sy += 5 * k * np.cos(80 * d)
        Mc = np.float32([[s, 0, W / 2 - s * fx + sx], [0, s, H / 2 - s * fy + sy]])
        fr = cv2.warpAffine(np.clip(out, 0, 255).astype(np.uint8), Mc, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        ff.stdin.write(fr.tobytes())
        if i in chaves: cv2.imwrite(saida.replace('.mp4', f'_f{i:04d}.jpg'), fr, [cv2.IMWRITE_JPEG_QUALITY, 88])
    ff.stdin.close(); ff.wait()
    if fecho:
        cat = saida + '.c.mp4'
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-i', FECHO, '-filter_complex',
                        '[0:v]setsar=1[a];[1:v]scale=1080:1920,setsar=1,fps=30[b];[a][b]concat=n=2:v=1:a=0[v]', '-map', '[v]',
                        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', cat], check=True)
        os.remove(tmp); tmp = cat
    if audio:
        wav = saida + '.wav'
        total = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', tmp], capture_output=True, text=True).stdout)
        sfx(L, total, wav)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                        '-af', CADEIA, '-c:a', 'aac', '-b:a', '192k', '-shortest', saida], check=True)
        tp = _pico_real(saida)
        if tp > -6.3:                                   # garante o pico ≤ −6 dBFS da bíblia (true peak, depois do AAC)
            ajuste = -6.6 - tp
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                            '-af', CADEIA + f',volume={ajuste:.2f}dB', '-c:a', 'aac', '-b:a', '192k', '-shortest', saida + '.a.mp4'], check=True)
            os.replace(saida + '.a.mp4', saida)
        os.remove(tmp); os.remove(wav)
    else:
        os.replace(tmp, saida)
    return saida

def folha_contacto(video, saida, tempos, larg=270):
    ims = []
    for t in tempos:
        r = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', str(t), '-i', video, '-frames:v', '1', '-vf', f'scale={larg}:-2', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], capture_output=True).stdout
        im = np.frombuffer(r, np.uint8).reshape(-1, larg, 3).copy(); cv2.putText(im, f'{t:.1f}s', (8, im.shape[0] - 10), 0, .7, (255, 255, 255), 2); ims.append(im)
    n = (len(ims) + 1) // 2
    while len(ims) < 2 * n: ims.append(np.zeros_like(ims[0]))
    cv2.imwrite(saida, np.vstack([np.hstack(ims[:n]), np.hstack(ims[n:])]), [cv2.IMWRITE_JPEG_QUALITY, 88])

# ------------------------------------------------------------------ som próprio (sintetizado): papel a bater, cola, adesivo
def sfx(L, total, wav, sr=48000):
    n = int(total * sr); a = np.zeros(n, np.float32); rng = np.random.default_rng(1)
    def env(d, att, dec): x = np.arange(int(d * sr)) / sr; return np.minimum(x / att, 1) * np.exp(-x / dec)
    def ruido(d, lo, hi):
        x = rng.normal(0, 1, int(d * sr)).astype(np.float32); X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / sr)
        X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x)).astype(np.float32)
    def soma(t, s):
        i = int(t * sr)
        if i >= n: return
        s = s[:n - i]; a[i:i + len(s)] += s
    for p in L:
        if p.modo == 'fixa' or p.som == 'nada': continue
        ti = p.impacto()
        if p.som == 'pop':
            s = ruido(.09, 1500, 7000) * env(.09, .002, .02) * .35
            x = np.arange(len(s)) / sr; s += (np.sin(2 * np.pi * (520 + 900 * x) * x) * env(.09, .001, .03) * .25).astype(np.float32)
            soma(ti, s); continue
        g = 1.0 if p.som == 'grande' else .7
        soma(ti - p.dur * .8, ruido(p.dur * .8, 300, 3000) * np.linspace(0, 1, int(p.dur * .8 * sr)) ** 2 * .08 * g)   # ar
        tap = ruido(.18, 80, 2500) * env(.18, .001, .035) * .9 * g
        x = np.arange(int(.2 * sr)) / sr; th = np.sin(2 * np.pi * 70 * x) * env(.2, .001, .05) * .6 * g
        soma(ti, tap); soma(ti, th.astype(np.float32))
        soma(ti + .05, ruido(.25, 2000, 9000) * env(.25, .01, .08) * .05)            # cola/papel a assentar
    leito = ruido(total, 120, 1800) * .012                                                 # ar do muro (leito contínuo, muito baixo)
    a[:len(leito)] += leito[:n]
    a = np.tanh(a * 3.5) / np.tanh(3.5)                                                      # compressão suave: sobe o volume médio
    a *= 10 ** (-6.5 / 20) / max(1e-6, np.abs(a).max())                                   # pico −6,5 dBFS (margem para o −6 da bíblia)
    st = np.stack([a, a], 1)
    with wave.open(wav, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((st * 32767).astype(np.int16).tobytes())

