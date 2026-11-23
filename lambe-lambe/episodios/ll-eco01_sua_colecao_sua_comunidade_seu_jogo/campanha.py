"""LL-ECO01 · «Sua coleção. Sua comunidade. Seu jogo.» — campanha de posicionamento do BINDER Vision no Lambe-lambe.
Base visual: animação aprovada do Story («o cartaz está sendo colado no muro», lambe-lambe/kit_story/motor_story.py, 16/11/2026)
e peças do carrossel aprovado (kit_carrossel/motor_padrao.py, 13–14/11/2026). Nenhum dos dois motores é alterado: este script
importa as peças do motor_padrao e reaproveita a física de colagem do motor_story (voo, impacto, mola, tremor, fitas).

Uso:
  python3 -I campanha.py video  <config.json> <saida.mp4> [--reel] [--audio] [--sem-fecho]
  python3 -I campanha.py carrossel <config.json> <pasta_saida>
config.json: {"cartas": pasta com sld_<n>_png.png / sld_<n>_art_crop.jpg (Scryfall), "ligamagic": jpg do ícone}
Story: 15,4 s + fecho 3,87 s. Reel (--reel): tempos ×1,15 (17,7 s + fecho). --audio: efeitos sintetizados próprios (pico −6 dBFS).
Zero créditos externos: OpenCV, numpy, Playwright (texto) e FFmpeg locais."""
import sys, os, json, asyncio, subprocess, wave
import cv2, numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, '../../..'))
KIT = os.path.join(RAIZ, 'lambe-lambe/kit_carrossel')
sys.path.insert(0, KIT)
_cwd = os.getcwd()
import motor_padrao as M          # muda o cwd para o kit (fontes relativas)
os.chdir(_cwd)
from compor import colar, rasgo_alpha, aplicar, CSS
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
            b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
            pg = await b.new_page(viewport={"width": 1080, "height": 1920})
            for i, (html, w, h) in enumerate(_FILA):
                if i in _TX: continue
                f = os.path.join(KIT, f'_eco_{os.getpid()}_{i}.html'); o = os.path.join(KIT, f'_eco_{os.getpid()}_{i}.png')
                css = CSS.replace('#s{width:1080px;height:1350px', f'#s{{width:{w}px;height:{h}px')
                open(f, 'w').write(f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{css}"
                                   ".e y{color:#FFD84A;font-style:italic;font-weight:900}.g{color:#10B981}.k{color:#E61E6E}</style></head>"
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

# ------------------------------------------------------------------ textos da campanha
def T(texto, fs, cor=PRETO, fam='AB', peso='', extra='', w=1000, alin='center'):
    return (f'<div class="e" style="position:relative;width:{w}px;white-space:normal;text-align:{alin};font-family:{fam};{peso}'
            f'font-size:{fs}px;line-height:.98;color:{cor};letter-spacing:-1px;text-transform:uppercase;{extra}">{texto}</div>')

def caixa(w, h, html, pad=(0, 0)):
    """camada de texto centrada num canvas CWxCH, para imprimir numa folha de w×h centrada"""
    x0, y0 = (CW - w) / 2 + pad[0], (CH - h) / 2 + pad[1]
    return html_camada(f'<div style="position:absolute;left:{x0}px;top:{y0}px;width:{w}px;height:{h}px;display:flex;align-items:center;justify-content:center">'
                       f'<div style="position:relative;width:{w}px;min-height:{h if "<svg" in html else 0}px">{html}</div></div>', CW, CH)

def pecas(cfg):
    C = cfg['cartas']; c = lambda n, k='png': os.path.join(C, f'sld_{n}_{k}.png' if k == 'png' else f'sld_{n}_art_crop.jpg')
    t = {}
    # --- camadas de texto
    t['s1a'] = caixa(860, 240, T('Magic é muito<br>mais do que', 92, w=860))
    t['s1b'] = caixa(880, 150, T('cartas.', 120, '#fff', w=880))
    t['s2a'] = caixa(860, 170, T('Organize sua<br><span class="k">coleção.</span>', 78, w=860))
    t['s2b'] = caixa(820, 120, T('Identifique suas cartas.', 52, '#fff', 'RB', 'font-weight:900;font-style:italic;', w=820))
    t['s2c'] = caixa(520, 170, T('Exporte para<br>a LigaMagic.', 60, w=520, alin='left'))
    t['s3a'] = caixa(880, 200, T('Encontre jogadores<br><span class="k">perto de você.</span>', 72, w=880))
    t['s3b'] = caixa(860, 120, T('Converse. <span class="g">Conecte-se.</span>', 54, '#fff', w=840))
    t['s4a'] = caixa(860, 150, T('Crie <span class="k">campeonatos.</span>', 74, w=860))
    t['s4b'] = caixa(860, 150, T('Reúna a comunidade.<br><span class="g">Jogue.</span>', 58, '#fff', w=860))
    t['s5a'] = caixa(900, 90, T('Não é só um aplicativo.', 56, PRETO, 'RB', 'font-weight:900;font-style:italic;', w=900))
    t['s5b'] = caixa(940, 250, T('É um <span style="background:#050A10;color:#fff;padding:2px 18px 6px;-webkit-box-decoration-break:clone">ecossistema</span><br>para quem vive', 82, PRETO, w=940, extra='line-height:1.12;'))
    t['s5c'] = caixa(860, 90, '<div style="font-family:Geist;font-weight:500;font-size:19px;line-height:1.35;color:#06281D;text-align:center">'
                     'BINDER Vision é um app independente. Magic: The Gathering é marca da Wizards of the Coast.<br>'
                     'LigaMagic é marca dos seus titulares. Google Play e o logotipo do Google Play são marcas da Google LLC. Sem afiliação, parceria ou patrocínio.</div>')
    t['s5d'] = caixa(330, 70, '<div style="font-family:RB;font-weight:800;font-size:26px;color:#050A10;text-align:left;line-height:1.1">exporte a coleção<br>para a LigaMagic</div>')
    t['s6a'] = caixa(760, 120, T('Tudo isso,', 92, w=760))
    t['s6b'] = caixa(800, 130, T('gratuitamente.', 76, PRETO, w=800))
    t['s6c'] = caixa(880, 170, '<div style="text-align:center"><div style="font-family:AB;font-size:52px;line-height:1;color:#fff;letter-spacing:-1px;text-transform:uppercase;white-space:nowrap">'
                     'Conheça o <span class="g">BINDER Vision.</span></div><div style="margin-top:18px;font-family:RB;font-weight:800;font-size:34px;color:#FFD84A">'
                     'Beta para Android · Link na bio</div></div>')
    # ícones (tinta preta/verde em papel creme)
    t['ic_pin'] = caixa(160, 200, svg(160, 200, pin(80, 10, VERDE)))
    t['ic_bal'] = caixa(240, 130, svg(240, 130, balao(10, 10, 220, 84)))
    t['ic_bal2'] = caixa(240, 130, svg(240, 130, balao(10, 10, 220, 84, VERDE, -1)))
    t['ic_av'] = caixa(150, 150, svg(150, 150, avatar(75, 75, 60)))
    t['ic_av2'] = caixa(150, 150, svg(150, 150, avatar(75, 75, 60, VERDE)))
    t['ic_tro'] = caixa(180, 190, svg(180, 190, trofeu(30, 8)))
    t['ic_seta'] = caixa(200, 110, svg(200, 110, f'<path d="M10 70 C 60 20, 120 20, 170 52" stroke="{ROSA}" stroke-width="12" fill="none" stroke-linecap="round"/>'
                                     f'<path d="M150 22 L186 58 L138 74" stroke="{ROSA}" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'))
    return t, c

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

def blend(out, rgb, al, Mx, op=1.0, WH=(CW, CH)):
    al2 = cv2.warpPerspective(al, Mx, WH, flags=cv2.INTER_LINEAR)[..., None] * op
    if rgb is None: return out * (1 - al2)
    c = cv2.warpPerspective(rgb, Mx, WH, flags=cv2.INTER_LINEAR)
    return out * (1 - al2) + c * al2

def desenha(out, p, st):
    Mx = mat_peca(p, st)
    if st['alt'] > 0:
        off = np.array([[1, 0, 18 + 70 * st['alt']], [0, 1, 30 + 110 * st['alt']], [0, 0, 1]])
        out = blend(out, None, cv2.GaussianBlur(p.al, (0, 0), 4 + 20 * st['alt']), off @ Mx, .45 * (1 - .5 * st['alt']))
    return blend(out, p.rgb, p.al, Mx, st.get('op', 1.0))

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

# ------------------------------------------------------------------ guião (tempos da versão Story; Reel = ×1,15)
def cena(cfg, S=1.0):
    t, c = pecas(cfg); render_textos()
    lig = cv2.imread(cfg['ligamagic'])
    L = []; ap = L.append
    # 1 · O UNIVERSO — quadro 0: a carta inteira já colada (abertura de objeto)
    ap(Peca(peca_carta(c(901), 460, -1.5), 540, 990, 0, modo='fixa'))
    ap(Peca(peca_folha(900, 270, 'creme', 1, -1.2, t['s1a'], fitas=((-.94, -1, -40), (.94, -1, 40))), 540, 520, .30, .40, de=(-80, -1500), rot0=-8))
    ap(Peca(peca_folha(900, 170, 'preto', 2, 1.0, t['s1b'], claro=True), 540, 1420, .95, .36, de=(0, 1400), rot0=6))
    ap(Peca(peca_folha(170, 210, 'creme', 3, -6, t['ic_pin']), 175, 860, 1.45, .22, modo='pop', esc=1, ang=-6, som='pop'))
    ap(Peca(peca_folha(250, 140, 'creme', 4, 5, t['ic_bal']), 900, 820, 1.60, .22, modo='pop', ang=5, som='pop'))
    ap(Peca(peca_folha(190, 200, 'creme', 5, 4, t['ic_tro']), 912, 1150, 1.75, .22, modo='pop', ang=4, som='pop'))
    # 2 · A COLEÇÃO
    ap(Peca(peca_folha(1010, 1560, 'creme', 6, -.6), 540, 945, 2.40, .40, de=(0, -1900), rot0=-4, z0=1.15, som='grande'))
    ap(Peca(peca_folha(900, 210, 'kraft', 7, 1.2, t['s2a'], fitas=((-.94, -1, -40), (.94, -1, 40))), 540, 410, 2.62, .36, de=(900, -200), rot0=12))
    ap(Peca(peca_carta(c(7104), 380, -3), 300, 820, 2.95, .36, de=(-800, -300), rot0=14))
    ap(Peca(peca_carta(c(334), 380, 3), 780, 830, 3.20, .36, de=(800, -300), rot0=-14))
    ap(Peca(peca_folha(860, 130, 'preto', 8, -1, t['s2b'], claro=True), 540, 1188, 3.55, .34, de=(-900, 0), rot0=-6))
    ap(Peca(peca_img(lig, 210, ang=-4, margem=14, seed=9), 250, 1392, 4.05, .30, de=(-700, 300), rot0=-10))
    ap(Peca(peca_folha(560, 200, 'kraft', 10, 1.5, t['s2c'], fitas=((-.96, -1, -40), (.96, -1, 40))), 680, 1392, 4.25, .30, de=(800, 200), rot0=8))
    # 3 · A COMUNIDADE
    ap(Peca(peca_folha(1010, 1560, 'kraft', 11, .7), 540, 950, 5.30, .40, de=(0, -1900), rot0=5, z0=1.15, som='grande'))
    ap(Peca(peca_folha(940, 240, 'creme', 12, -1, t['s3a'], fitas=((-.94, -1, -40), (.94, -1, 40))), 540, 400, 5.50, .36, de=(-900, -200), rot0=-10))
    ap(Peca(peca_carta(c(7029), 420, 1.5), 540, 905, 5.82, .38, de=(0, -1500), rot0=8))
    ap(Peca(peca_folha(170, 210, 'creme', 13, -5, t['ic_pin']), 165, 690, 6.20, .2, modo='pop', ang=-5, som='pop'))
    ap(Peca(peca_folha(160, 160, 'creme', 14, 4, t['ic_av']), 170, 930, 6.32, .2, modo='pop', ang=4, som='pop'))
    ap(Peca(peca_folha(160, 160, 'creme', 15, -3, t['ic_av2']), 915, 700, 6.44, .2, modo='pop', ang=-3, som='pop'))
    ap(Peca(peca_folha(250, 140, 'creme', 16, 4, t['ic_bal']), 900, 940, 6.56, .2, modo='pop', ang=4, som='pop'))
    ap(Peca(peca_folha(250, 140, 'creme', 17, -4, t['ic_bal2']), 185, 1150, 6.68, .2, modo='pop', ang=-4, som='pop'))
    ap(Peca(peca_folha(880, 140, 'preto', 18, 1, t['s3b'], claro=True), 540, 1355, 6.90, .34, de=(900, 0), rot0=6))
    # 4 · O JOGO
    ap(Peca(peca_folha(1010, 1560, 'creme', 19, -.5), 540, 945, 7.90, .40, de=(0, -1900), rot0=-5, z0=1.15, som='grande'))
    ap(Peca(peca_folha(900, 180, 'kraft', 20, -1.2, t['s4a'], fitas=((-.94, -1, -40), (.94, -1, 40))), 540, 400, 8.10, .34, de=(900, -300), rot0=10))
    ap(Peca(peca_folha(560, 620, 'kraft', 21, .8), 370, 900, 8.38, .32, de=(-800, 100), rot0=-8))          # quadro do torneio
    ap(Peca(peca_carta(c(83), 330, 3), 800, 900, 8.62, .34, de=(800, -200), rot0=-12))
    ap(Peca(peca_folha(190, 200, 'creme', 22, -4, t['ic_tro']), 815, 1235, 9.35, .2, modo='pop', ang=-4, som='pop'))
    ap(Peca(peca_folha(900, 190, 'preto', 23, .8, t['s4b'], claro=True), 540, 1390, 9.15, .32, de=(-900, 0), rot0=-6))
    # 5 · REVELAÇÃO DA MARCA — cartaz verde-esmeralda (pedido do fundador 23/11: fundo que não seja preto); logos em etiquetas pretas
    ap(Peca(peca_folha(1040, 1640, 'verde', 24, .4), 540, 955, 10.20, .40, de=(0, -1900), rot0=4, z0=1.15, som='grande'))
    ap(Peca(peca_folha(860, 110, 'verde', 25, -1, t['s5a'], claro=True), 540, 350, 10.45, .18, modo='carimbo', som='pop'))
    ap(Peca(peca_folha(960, 270, 'verde', 26, 0, t['s5b'], claro=True), 540, 555, 11.0, .18, modo='carimbo', som='pop'))
    mg, ma = logo_magic()
    ap(Peca(peca_img(mg, 430, ma, ang=-1.5, margem=26, fundo=(16, 10, 5), seed=34, fitas=((-1, -1, -40), (1, -1, 40))), 540, 785, 11.55, .3, modo='pop', som='pop'))
    lb = logo_binder()
    ap(Peca(peca_img(lb, 430, ang=1, margem=22, fundo=(16, 10, 5), seed=35, fitas=((-1, -1, -40), (1, -1, 40))), 540, 1100, 12.00, .30, modo='pop', som='pop'))
    ap(Peca(peca_img(lig, 110, ang=-3, margem=8, seed=31), 360, 1395, 12.25, .25, modo='pop', som='pop'))
    ap(Peca(peca_folha(380, 100, 'verde', 32, 0, t['s5d'], claro=True), 610, 1397, 12.3, .25, modo='carimbo'))
    ap(Peca(peca_folha(900, 110, 'verde', 27, 0, t['s5c'], claro=True), 540, 1515, 12.3, .25, modo='carimbo'))
    # 6 · GRATUIDADE E CTA
    ap(Peca(peca_folha(1010, 1560, 'creme', 33, .6), 540, 950, 13.20, .40, de=(0, -1900), rot0=-5, z0=1.15, som='grande'))
    ap(Peca(peca_folha(840, 150, 'kraft', 28, -2, t['s6a'], fitas=((-.94, -1, -40), (.94, -1, 40))), 540, 370, 13.42, .32, de=(-900, -200), rot0=-10))
    ap(Peca(peca_folha(840, 150, 'amarelo', 29, 1.5, t['s6b']), 548, 520, 13.70, .30, de=(900, -100), rot0=10))
    ap(Peca(peca_carta(c(369), 300, -2), 540, 885, 13.95, .34, de=(0, 1500), rot0=-8))
    ap(Peca(peca_folha(940, 200, 'preto', 30, -.8, t['s6c'], claro=True), 540, 1215, 14.30, .32, de=(0, 1400), rot0=4))
    pb, pa = logo_play()      # selo oficial do Google Play: sem rotação, sem fita, sem textura por cima
    ap(Peca(matte(lambda b: colar(b, pb, pa, CW / 2, CH / 2, 0, sombra=False)), 540, 1385, 14.65, .25, modo='carimbo', esc=.42, som='pop'))
    for p in L:
        p.t0 *= S; p.dur *= S if p.modo not in ('pop', 'carimbo') else 1; p.assenta = p.t0 + p.dur + .8
    DUR = 16.0 * S
    ANIM = dict(radar=(6.20 * S, 7.90 * S, (165, 650)), chave=(8.70 * S, 9.40 * S), lig=(4.45 * S, 5.30 * S), S=S)
    return L, DUR, ANIM

# ------------------------------------------------------------------ animações desenhadas (radar e chaveamento do torneio)
def radar(out, t, a):
    t0, t1, (x, y) = a
    if not (t0 <= t < t1): return out
    for k in range(3):
        u = ((t - t0) * .9 + k / 3) % 1
        ov = np.zeros(out.shape[:2], np.float32)
        cv2.circle(ov, (x, y), int(30 + 135 * u), 1.0, 6, cv2.LINE_AA)
        a2 = (ov * (1 - u) * .8)[..., None]
        out = out * (1 - a2) + np.array((129, 185, 16), np.float32) * a2
    return out

CHAVE = [((185, 700), (290, 700), (290, 775)), ((185, 850), (290, 850), (290, 775)), ((290, 775), (420, 775), (420, 925)),
         ((185, 1000), (290, 1000), (290, 1075)), ((185, 1150), (290, 1150), (290, 1075)), ((290, 1075), (420, 1075), (420, 925)),
         ((420, 925), (550, 925))]
SLOTS = ((185, 700), (185, 850), (185, 1000), (185, 1150))

# ------------------------------------------------------------------ render do vídeo
def video(cfg, saida, reel=False, audio=False, fecho=True):
    S = 1.15 if reel else 1.0
    L, DUR, A = cena(cfg, S)
    W, H, FPS = CW, CH, 30; NF = int(round(DUR * FPS))
    MURO = muro()
    bat = sorted(p.impacto() for p in L if p.modo == 'bate')
    base = MURO.copy(); baked = 0
    tmp = saida + '.v.mp4'
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', tmp], stdin=subprocess.PIPE)
    chaves = {int(x * FPS * S) for x in (0.0, 1.2, 2.3, 4.0, 5.2, 7.0, 7.8, 9.8, 11.0, 12.8, 14.2, 15.9)}
    chaves = {min(k, NF - 1) for k in chaves}
    for i in range(NF):
        t = i / FPS
        # coze as peças já assentes, por ordem (o que fica por baixo nunca volta a mexer)
        while baked < len(L) and t >= L[baked].assenta and all(t >= q.assenta for q in L[:baked]):
            p = L[baked]; base = desenha(base, p, p.estado(p.assenta)); baked += 1
        out = base.copy()
        for p in L[baked:]:
            st = p.estado(t)
            if st is None: continue
            out = desenha(out, p, st)
        out = radar(out, t, A['radar'])
        if A['chave'][0] <= t < 10.2 * S + .2:   # quadro do torneio desenhado a marcador (por baixo do cartaz da cena 5)
            out = chave_sobre(out, base, t, A, L)
        # câmara: aproximação lenta por cena + tremor curto em cada impacto (motor_story)
        s = 1.025 + .03 * ((t % (2.6 * S)) / (2.6 * S))
        sx = sy = 0
        for b in bat:
            d = t - b
            if 0 <= d < .2: k = np.exp(-18 * d); sx += 3 * k * np.sin(90 * d); sy += 5 * k * np.cos(80 * d)
        z = .34 * (1 - ease_io(cl((t - .08) / (.55 * S))))      # abertura de objeto: a carta em tela cheia no quadro 0, depois recua
        s += z; fy = H / 2 + 30 * z / .34
        Mc = np.float32([[s, 0, W / 2 - s * W / 2 + sx], [0, s, H / 2 - s * fy + sy]])
        fr = cv2.warpAffine(np.clip(out, 0, 255).astype(np.uint8), Mc, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        ff.stdin.write(fr.tobytes())
        if i in chaves: cv2.imwrite(saida.replace('.mp4', f'_f{i:03d}.jpg'), fr, [cv2.IMWRITE_JPEG_QUALITY, 88])
    ff.stdin.close(); ff.wait()
    partes = [tmp]
    if fecho:
        cat = saida + '.c.mp4'
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-i', FECHO, '-filter_complex',
                        '[0:v]setsar=1[a];[1:v]scale=1080:1920,setsar=1,fps=30[b];[a][b]concat=n=2:v=1:a=0[v]', '-map', '[v]',
                        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', cat], check=True)
        os.remove(tmp); tmp = cat
    if audio:
        wav = saida + '.wav'; total = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', tmp], capture_output=True, text=True).stdout)
        sfx(L, total, wav)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', saida], check=True)
        os.remove(tmp); os.remove(wav)
    else:
        os.replace(tmp, saida)
    print('ok', saida)

def chave_sobre(out, base, t, A, L):
    """traços do chaveamento a marcador preto sobre o quadro kraft; somem quando o cartaz preto da cena 5 cobre"""
    S = A['S']; t0, t1 = A['chave']
    if t < t0: return out
    capa5 = [p for p in L if p.t0 >= 10.2 * S - 1e-6][0]
    if t >= capa5.t0 + capa5.dur: return out
    u = cl((t - t0) / (t1 - t0))
    ov = np.zeros(out.shape[:2], np.float32)
    for x, y in SLOTS:
        cv2.rectangle(ov, (x - 70, y - 32), (x, y + 32), 1.0, 6, cv2.LINE_AA)
    if u >= 1: cv2.circle(ov, (575, 925), 20, 1.0, -1, cv2.LINE_AA)
    k = u * len(CHAVE)
    for i, seg in enumerate(CHAVE):
        f = cl(k - i)
        if f <= 0: break
        pts = np.array(seg, np.float32); Ls = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))]; d = f * Ls[-1]
        for j in range(len(pts) - 1):
            if d <= Ls[j]: break
            e = pts[j] + (pts[j + 1] - pts[j]) * min(1, (d - Ls[j]) / (Ls[j + 1] - Ls[j]))
            cv2.line(ov, tuple(int(v) for v in pts[j]), tuple(int(v) for v in e), 1.0, 9, cv2.LINE_AA)
    a2 = (cv2.GaussianBlur(ov, (0, 0), .8) * .9)[..., None]
    # só onde o quadro kraft está visível por cima (as peças em voo da cena 5 tapam os traços)
    vis = np.ones(out.shape[:2], np.float32)
    if t >= capa5.t0:
        st = capa5.estado(t)
        vis = 1 - cv2.warpPerspective(capa5.al, mat_peca(capa5, st), (CW, CH))
    a2 = a2 * vis[..., None]
    return out * (1 - a2) + np.array((22, 18, 14), np.float32) * a2

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
        if p.modo == 'fixa': continue
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
    a = np.tanh(a * 1.2)
    a *= 10 ** (-6 / 20) / max(1e-6, np.abs(a).max())                                     # pico −6 dBFS
    st = np.stack([a, a], 1)
    with wave.open(wav, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((st * 32767).astype(np.int16).tobytes())

# ------------------------------------------------------------------ entrada
if __name__ == '__main__':
    arg = [a for a in sys.argv[1:] if not a.startswith('--')]
    modo, cfgp, saida = arg[0], os.path.abspath(arg[1]), os.path.abspath(arg[2])
    cfg = json.load(open(cfgp)); d = os.path.dirname(cfgp)
    for k in ('cartas', 'ligamagic'):
        if not os.path.isabs(cfg[k]): cfg[k] = os.path.normpath(os.path.join(d, cfg[k]))
    if modo == 'video':
        os.makedirs(os.path.dirname(saida), exist_ok=True)
        video(cfg, saida, '--reel' in sys.argv, '--audio' in sys.argv, '--sem-fecho' not in sys.argv)
    elif modo == 'carrossel':
        sys.path.insert(0, AQUI); import carrossel; carrossel.gerar(cfg, saida)
    elif modo == 'capa':
        sys.path.insert(0, AQUI); import carrossel; carrossel.capas(cfg, saida)
