"""Motor do Story animado do Lambe-lambe: «o cartaz está sendo colado no muro». 1080x1920, 30 fps, 9 s, H.264, sem áudio.
Padrão do fundador (16/11/2026): todo carrossel Lambe-lambe ganha este Story. Referência: LL-ART20.
Uso: python3 -I motor_story.py <config.json> <saida.mp4> [--previa] [--sem-foto] [--sem-fecho]
Termina sempre com o fecho do scanner (comum/outro/outro_binder_916.mp4), salvo --sem-fecho.
config.json (caminhos absolutos ou relativos ao JSON):
  capa      PNG da capa do carrossel (1080x1350, renderizado pelo motor_padrao, sem faixa de prévia)
  esquerda  art_crop (Scryfall) da impressão da esquerda
  direita   {"foto": jpg} e/ou {"carta": png Scryfall}; com --sem-foto (ou sem "foto") usa a carta
  detalhe   art_crop do detalhe que desenrola ao centro
  nome      texto grande da faixa final (ex.: "CAIO MONTEIRO")
  serie     texto da 2.ª linha antes de «· BINDER» (ex.: "Artistas de Magic")
  creditos  {"com_foto": "...", "sem_foto": "..."} em HTML curto (cartas, set nº, artista, © Wizards of the Coast)
Peças isoladas por matting do motor_padrao (não alterado); capa recortada pela máscara exata da folha + selo."""
import sys, os, json, asyncio, subprocess, cv2, numpy as np
_a = [x for x in sys.argv[1:] if not x.startswith('--')]
CFG_P, OUT = os.path.abspath(_a[0]), os.path.abspath(_a[1])
CFG = json.load(open(CFG_P)); _d = os.path.dirname(CFG_P)
_p = lambda x: x if os.path.isabs(x) else os.path.normpath(os.path.join(_d, x))
PREVIA = '--previa' in sys.argv
CAPA = _p(CFG['capa'])
FOTO = _p(CFG['direita']['foto']) if CFG['direita'].get('foto') and '--sem-foto' not in sys.argv else None
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../kit_carrossel')))
import motor_padrao as M
from compor import colar, rasgo_alpha, camada
W, H, FPS, DUR = 1080, 1920, 30, 9.0
NF = int(FPS * DUR)

# ---------- peças (RGBA float) ----------
def matte(draw):
    """desenha a peça sobre preto e sobre branco (1080x1350) e devolve (rgb, alpha) recortados"""
    k = np.zeros((1350, 1080, 3), np.uint8); w = np.full_like(k, 255)
    kb = draw(k).astype(np.float32); wb = draw(w).astype(np.float32)
    al = np.clip(1 - (wb - kb).mean(2) / 255, 0, 1)
    rgb = np.where(al[..., None] > .02, kb / np.maximum(al[..., None], 1e-3), 0)
    ys, xs = np.where(al > .02); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    return np.clip(rgb[y0:y1, x0:x1], 0, 255).astype(np.float32), al[y0:y1, x0:x1].astype(np.float32)

def capa_peca():
    img = cv2.imread(CAPA).astype(np.float32)
    z = np.zeros((1350, 1080, 3), np.uint8)
    fol = colar(z, np.full((1290, 1000, 3), 255, np.uint8), rasgo_alpha(1000, 1290, 16, 9), 540, 677, -0.4, sombra=False)[..., 0]
    sel = (M.selo(z.copy()).astype(np.int16).sum(2) > 60).astype(np.uint8) * 255
    al = cv2.GaussianBlur(np.maximum(fol, sel), (0, 0), .8).astype(np.float32) / 255
    ys, xs = np.where(al > .02)
    return img[ys.min():ys.max() + 1, xs.min():xs.max() + 1], al[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

art = lambda k: cv2.imread(_p(CFG[k]))
P = {}
P['capa'] = capa_peca()
P['kraft1'] = matte(lambda b: M.papel(b, 360, 520, 400, 300, 0, 0, 11))
P['kraft2'] = matte(lambda b: M.papel(b, 380, 480, 330, 400, 0, 2, 12))
P['esq'] = matte(lambda b: M.impressa(b, art('esquerda'), 540, 500, 340, 0, fitas=((0, -1, -8),), seed=21)[0])
P['detalhe'] = matte(lambda b: M.impressa(b, art('detalhe'), 540, 500, 300, 0, fitas=((-.5, -1, -9), (.5, -1, 9)), seed=22)[0])
if FOTO:
    P['retrato'] = matte(lambda b: M.recorte(b, cv2.imread(FOTO), np.full((500, 400), 255, np.uint8), 540, 400, 380, 0))
else:
    P['retrato'] = matte(lambda b: M.carta(b, _p(CFG['direita']['carta']), 540, 675, 300, 0, fitas=((-1.0, -1.04, -45), (1.0, -1.04, 45)), fl=60))
P['fita'] = matte(lambda b: M.fita(b, 540, 675, 0, 120))
P['faixa'] = matte(lambda b: M.rodape(b, 675, 0))

# ---------- textos (mesmas fontes do kit, via compor.camada) ----------
def texto(html, nome):
    cwd = os.getcwd(); os.chdir(M.KIT); asyncio.run(camada(html, nome)); t = cv2.imread(nome, cv2.IMREAD_UNCHANGED); os.remove(nome); os.chdir(cwd)
    t = t.astype(np.float32); ys, xs = np.where(t[..., 3] > 3)
    t = t[ys.min():ys.max() + 1, xs.min():xs.max() + 1]; return t[..., :3], t[..., 3] / 255
NOME, SERIE = CFG['nome'], CFG['serie']
CRED = CFG['creditos']['com_foto' if FOTO else 'sem_foto']
P['titulo'] = texto('<div style="position:absolute;left:540px;top:20px;transform:translateX(-50%);text-align:center;white-space:nowrap">'
                    f'<div class="e" style="position:relative;font-family:AB;font-size:66px;line-height:1;color:#fff;letter-spacing:-1px">{NOME}</div>'
                    f'<div class="e" style="position:relative;margin-top:10px;font-family:RB;font-weight:800;font-size:34px;color:#fff">{SERIE} · <span style="color:#FFD84A;font-style:italic;font-weight:900">BINDER</span></div>'
                    f'<div style="margin-top:14px;font-family:Geist;font-weight:500;font-size:15px;line-height:1.3;color:#D9D2C4">{CRED}</div></div>', '_tit.png')
if PREVIA:
    P['previa'] = texto('<div style="position:absolute;left:20px;top:20px;background:#111;color:#FFD84A;font-family:AB;font-size:22px;padding:6px 16px;letter-spacing:2px;white-space:nowrap">PRÉVIA · AGUARDA AUTORIZAÇÃO</div>', '_prev.png')

# ---------- muro (sem folha; restos dos modelos aprovados nas bordas) ----------
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
    for i, x in enumerate((0, 50, W - 110, W - 60)):   # restos de cartazes antigos, discretos, junto às bordas
        t = tiras[i % 4]; t = np.vstack([t, t[::-1], t])[:H].astype(np.float32)
        m[:, x:x + 60] = m[:, x:x + 60] * .55 + t * .45
    return np.clip(m, 0, 255).astype(np.float32)
MURO = muro()

# ---------- animação ----------
def cl(x): return min(1.0, max(0.0, x))
def ease_in(u): return u ** 3
def ease_io(u): return u * u * (3 - 2 * u)
def mola(t): return np.exp(-7 * t) * np.cos(16 * t) if t > 0 else 1.0

class Peca:
    def __init__(s, nome, cx, cy, esc, ang, t0, dur=.55, de=(0, -1500), rot0=10, z0=1.3, modo='bate', onda=False):
        s.n, s.cx, s.cy, s.esc, s.ang, s.t0, s.dur, s.de, s.rot0, s.z0, s.modo, s.onda = nome, cx, cy, esc, ang, t0, dur, de, rot0, z0, modo, onda
        rgb, al = P[nome]; s.rgb, s.al = rgb, al; s.h, s.w = al.shape
        s.sh = cv2.GaussianBlur(al, (0, 0), 14)
    def estado(s, t):
        u = (t - s.t0) / s.dur
        if u < 0: return None
        if s.modo == 'revela':                                 # desenrola de cima para baixo
            return dict(cx=s.cx, cy=s.cy, esc=s.esc, ang=s.ang, alt=0, dobra=0, rev=ease_io(cl(u)), onda=0)
        if u < 1:                                              # voo: acelera em direção ao muro
            e = ease_in(u); alt = 1 - e
            return dict(cx=s.cx + s.de[0] * alt, cy=s.cy + s.de[1] * alt, esc=s.esc * (1 + (s.z0 - 1) * alt),
                        ang=s.ang + s.rot0 * alt, alt=alt, dobra=.10 * alt + .03, rev=1, onda=0)
        d = t - (s.t0 + s.dur)                                 # impacto: overshoot curto e assentamento
        m = mola(d)
        return dict(cx=s.cx, cy=s.cy, esc=s.esc * (1 - .03 * m), ang=s.ang - .9 * m, alt=0,
                    dobra=max(0, .03 * np.exp(-9 * d)), rev=1, onda=s.onda)
def impacto(p): return p.t0 + p.dur

ROT = 'retrato'
SOMBRA_CAPA = cv2.GaussianBlur(P['capa'][1], (0, 0), 40)
cena = [
    Peca('capa', 540, 770, .76, -1.2, 1.15, .62, de=(-60, -1500), rot0=-9, z0=1.25, onda=True),
    Peca('kraft1', 250, 1405, 1.0, -4, 3.30, .42, de=(-700, 200), rot0=-14),
    Peca('esq', 255, 1390, .95, -3, 3.72, .42, de=(-600, -300), rot0=12),
    Peca('kraft2', 825, 1430, 1.0, 5, 4.20, .42, de=(700, 150), rot0=16),
    Peca(ROT, 825, 1405, .84 if FOTO else .9, 3, 5.55, .5, de=(650, -200), rot0=-12, z0=1.35),
    Peca('detalhe', 545, 1495, .66, -1.5, 6.35, .45, modo='revela'),
]
capa = cena[0]
# fitas da capa: cantos de cima da folha (em coordenadas da peça) → mundo
def canto(p, fx, fy):
    r = np.deg2rad(p.ang); x, y = (fx - .5) * p.w * p.esc, (fy - .5) * p.h * p.esc
    return p.cx + x * np.cos(r) - y * np.sin(r), p.cy + x * np.sin(r) + y * np.cos(r)
fitas = [(*canto(capa, .025, .02), -45, 2.30), (*canto(capa, .975, .02), 45, 2.78)]
BATIDAS = [impacto(p) for p in cena if p.modo == 'bate'] + [f[3] + .12 for f in fitas]

def camera(t):
    if t < 7.2: s = 1.14 - .04 * t / 7.2
    else: s = 1.10 - .10 * ease_io(cl((t - 7.2) / 1.2))
    fy = 820 + 200 * ease_io(cl((t - 3.0) / 2.5))
    fy = fy + (960 - fy) * ease_io(cl((t - 7.2) / 1.2))
    sx = sy = 0
    for b in BATIDAS:                                         # tremor curto no impacto
        d = t - b
        if 0 <= d < .2: k = np.exp(-18 * d); sx += 3 * k * np.sin(90 * d); sy += 5 * k * np.cos(80 * d)
    return s, 540, fy, sx, sy

def mat_cam(s, fx, fy, sx, sy):
    return np.array([[s, 0, W / 2 - s * fx + sx], [0, s, H / 2 - s * fy + sy], [0, 0, 1]], np.float64)

def blend(out, rgb, al, Mx, op=1.0):
    al2 = cv2.warpPerspective(al, Mx, (W, H), flags=cv2.INTER_LINEAR)[..., None] * op
    if rgb is None: return out * (1 - al2)
    c = cv2.warpPerspective(rgb, Mx, (W, H), flags=cv2.INTER_LINEAR)
    return out * (1 - al2) + c * al2

def mat_peca(p, st, C):
    w, h = p.w, p.h; e = st['esc']; r = np.deg2rad(st['ang']); b = st['dobra']
    src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    loc = np.float32([[-w / 2 + b * w / 2, -h / 2 + b * h * .25], [w / 2 - b * w / 2, -h / 2 + b * h * .25], [w / 2, h / 2], [-w / 2, h / 2]]) * e
    R = np.array([[np.cos(r), -np.sin(r)], [np.sin(r), np.cos(r)]])
    dst = (loc @ R.T) + [st['cx'], st['cy']]
    dst = (np.c_[dst, np.ones(4)] @ C.T)[:, :2].astype(np.float32)
    return cv2.getPerspectiveTransform(src, dst)

def frame(t):
    s, fx, fy, sx, sy = camera(t)
    sw = 1 + (s - 1) * .6                                      # parallax: o muro mexe menos
    out = cv2.warpAffine(MURO, mat_cam(sw, 540, 960 + (fy - 960) * .6, sx * .6, sy * .6)[:2], (W, H), borderMode=cv2.BORDER_REFLECT)
    C = mat_cam(s, fx, fy, sx, sy)
    if .55 < t < capa.t0 + capa.dur:                          # sombra a anunciar o cartaz que vem aí
        k = cl((t - .55) / .6)
        Ms = mat_peca(capa, dict(cx=capa.cx + 40, cy=capa.cy + 60, esc=capa.esc * 1.15, ang=capa.ang - 4, dobra=0), C)
        out = blend(out, None, SOMBRA_CAPA, Ms, .28 * k)
    for p in cena:
        st = p.estado(t)
        if st is None: continue
        Mx = mat_peca(p, st, C)
        al = p.al
        if st['rev'] < 1:
            al = al.copy(); al[int(p.h * st['rev']):] = 0
            if st['rev'] <= 0: continue
        if st['alt'] > 0:                                      # sombra projetada enquanto o papel está no ar
            off = np.array([[1, 0, 18 + 70 * st['alt']], [0, 1, 30 + 110 * st['alt']], [0, 0, 1]])
            out = blend(out, None, cv2.GaussianBlur(al, (0, 0), 4 + 20 * st['alt']), off @ Mx, .45 * (1 - .5 * st['alt']))
        rgb = p.rgb
        if st['onda']:                                         # ondulação do papel a assentar
            d = t - impacto(p) - (fitas[1][3] - impacto(p) if p is capa else 0)
            A = .07 * np.exp(-3.5 * max(d, 0)) if d > -1.2 else 0
            if A > .003:
                y = np.arange(p.h, dtype=np.float32)[:, None, None]
                rgb = np.clip(rgb * (1 + A * np.sin(y / p.h * 9 - t * 14)), 0, 255)
        out = blend(out, rgb, al, Mx)
    for x, y, ang, tf in fitas:                                # fitas: entram a rodar e assentam
        u = (t - tf) / .22
        if u < 0: continue
        k = ease_io(cl(u)); m = mola(max(0, t - tf - .22))
        sc = .85 * (1.5 - .5 * k) * (1 + .04 * m); an = ang + 25 * (1 - k) + 4 * m
        fr, fa = P['fita']; h, w = fa.shape
        R = cv2.getRotationMatrix2D((w / 2, h / 2), -an, sc); R[:, 2] += [x - w / 2, y - h / 2]
        Mx = C @ np.vstack([R, [0, 0, 1]])
        out = blend(out, fr, fa, Mx, cl(u * 2))
    u = (t - 7.25) / .5                                       # faixa final com nome e créditos
    if u > 0:
        k = ease_io(cl(u)); m = mola(max(0, t - 7.75))
        fr, fa = P['faixa']; h, w = fa.shape
        cy = 1700 + 260 * (1 - k)
        R = cv2.getRotationMatrix2D((w / 2, h / 2), .8 + 2 * (1 - k) - .6 * m, 1.0); R[:, 2] += [540 - w / 2, cy - h / 2]
        out = blend(out, fr, fa, np.vstack([R, [0, 0, 1]]))
        tr, ta = P['titulo']; h, w = ta.shape
        R = cv2.getRotationMatrix2D((w / 2, h / 2), .8 + 2 * (1 - k) - .6 * m, 1.0); R[:, 2] += [540 - w / 2, cy - h / 2 - 4]
        out = blend(out, tr, ta, np.vstack([R, [0, 0, 1]]), cl((t - 7.5) / .25))
    if PREVIA:
        tr, ta = P['previa']; h, w = ta.shape
        R = cv2.getRotationMatrix2D((w / 2, h / 2), -90, 1.0); R[:, 2] += [1052 - w / 2, 960 - h / 2]
        out = blend(out, tr, ta, np.vstack([R, [0, 0, 1]]))
    return np.clip(out, 0, 255).astype(np.uint8)

FECHO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../comum/outro/outro_binder_916.mp4'))
def fecho(mp4):
    """acrescenta o fecho do scanner (regra de todos os vídeos do BINDER), sem corte lateral: mesmo 1080x1920 a 30 fps"""
    tmp = mp4 + '.tmp.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp4, '-i', FECHO, '-filter_complex',
                    '[0:v]setsar=1[a];[1:v]scale=1080:1920,setsar=1,fps=30[b];[a][b]concat=n=2:v=1:a=0[v]', '-map', '[v]',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', tmp], check=True)
    os.replace(tmp, mp4)

if __name__ == '__main__':
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
    chaves = {int(x * FPS) for x in (0.5, 1.5, 2.0, 3.0, 4.6, 6.0, 7.0, 8.9)}
    for i in range(NF):
        f = frame(i / FPS); ff.stdin.write(f.tobytes())
        if i in chaves: cv2.imwrite(OUT.replace('.mp4', f'_f{i:03d}.jpg'), f, [cv2.IMWRITE_JPEG_QUALITY, 85])
    ff.stdin.close(); ff.wait()
    if '--sem-fecho' not in sys.argv: fecho(OUT)
    print('ok', OUT)
