"""LL-LISA01 v2 · teaser de estreia da Lisa Marie com os 10 looks da prancha de 19/11 (pedido do fundador, 19:29).
Linguagem do Lambe-lambe (muro rosa, papel, kraft, fitas, faixa preta), peças do motor-padrão do carrossel; zero créditos.
Uso: python3 -I teaser_v2.py <pasta_saida>   (correr antes capa.py <pasta_saida>, que gera 01_capa.png)
Saída: <pasta_saida>/LL-LISA01_teaser_v2.mp4 (1080x1920, 30 fps, sem áudio) + fecho do scanner; frames-chave *_fNNN.jpg.
Estrutura: 0–2,4 s cartaz de estreia (já a entrar no quadro 0) · 2,4–12,4 s os 10 looks colados um a um, cada um com
nome e tema pop · 12,6–16 s a parede completa (grelha 5×2) com título e faixa «estreia em breve» · fecho."""
import sys, os, asyncio, subprocess, cv2, numpy as np
OUT = os.path.abspath(sys.argv[1]); os.makedirs(OUT, exist_ok=True)
AQUI = os.path.dirname(os.path.abspath(__file__))
LOOKS = os.path.normpath(os.path.join(AQUI, '../../../lisa-marie/referencias/inspiracoes_2026-11-19'))
FECHO = os.path.normpath(os.path.join(AQUI, '../../../comum/outro/outro_binder_916.mp4'))
sys.path.insert(0, os.path.normpath(os.path.join(AQUI, '../../kit_carrossel')))
import motor_padrao as M
from compor import camada, colar, rasgo_alpha
W, H, FPS, DUR = 1080, 1920, 30, 16.0

LISTA = [('01_reporter_do_multiverso', 'REPÓRTER DO MULTIVERSO', 'a apresentadora'),
         ('02_otaku_casual', 'OTAKU CASUAL', 'anime e mangá'),
         ('03_dj_de_vinil', 'DJ DE VINIL', 'música e vinil'),
         ('04_exploradora_do_multiverso', 'EXPLORADORA DO MULTIVERSO', 'os planos de Magic'),
         ('05_artista_de_rua', 'ARTISTA DE RUA', 'arte urbana'),
         ('06_colecionadora_de_mundos', 'COLECIONADORA DE MUNDOS', 'cartas e coleção'),
         ('07_fashionista_do_multiverso', 'FASHIONISTA DO MULTIVERSO', 'moda'),
         ('08_nerd_de_cultura_pop', 'NERD DE CULTURA POP', 'anime, K-pop e Magic'),
         ('09_investigadora_de_historias', 'INVESTIGADORA DE HISTÓRIAS', 'quem faz a comunidade'),
         ('10_vibe_90s', "VIBE 90'S", 'a era dos VJs')]

def look(n):
    im = cv2.imread(f'{LOOKS}/{n}.png'); im = im[14:im.shape[0] - 78]           # sem a faixa rosa e sem a etiqueta da prancha
    im = cv2.resize(im, None, fx=2, fy=2, interpolation=cv2.INTER_LANCZOS4)       # ampliação + nitidez leve (recortes de ~262 px)
    return np.clip(im * 1.35 - cv2.GaussianBlur(im, (0, 0), 2.2) * .35, 0, 255).astype(np.uint8)

# ---------- peças RGBA (mesmo método do motor do Story: desenhar sobre preto e sobre branco) ----------
def matte(draw):
    k = np.zeros((1350, 1080, 3), np.uint8); w = np.full_like(k, 255)
    kb = draw(k).astype(np.float32); wb = draw(w).astype(np.float32)
    al = np.clip(1 - (wb - kb).mean(2) / 255, 0, 1)
    rgb = np.where(al[..., None] > .02, kb / np.maximum(al[..., None], 1e-3), 0)
    ys, xs = np.where(al > .02); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    return np.clip(rgb[y0:y1, x0:x1], 0, 255).astype(np.float32), al[y0:y1, x0:x1].astype(np.float32)

def texto(html, nome='_tx.png'):
    cwd = os.getcwd(); os.chdir(M.KIT); asyncio.run(camada(html, nome)); t = cv2.imread(nome, cv2.IMREAD_UNCHANGED); os.remove(nome)
    for f in ('_camada.html',):
        if os.path.exists(f): os.remove(f)
    os.chdir(cwd); t = t.astype(np.float32); ys, xs = np.where(t[..., 3] > 3)
    t = t[ys.min():ys.max() + 1, xs.min():xs.max() + 1]; return t[..., :3], t[..., 3] / 255

def sobre(a, b, dx, dy):
    """junta a peça b (texto) por cima de a, com o centro de b deslocado (dx, dy) do centro de a"""
    (ra, aa), (rb, ab) = a, b
    h, w = max(aa.shape[0], ab.shape[0] + abs(2 * dy)), max(aa.shape[1], ab.shape[1] + abs(2 * dx))
    R = np.zeros((h, w, 3), np.float32); A = np.zeros((h, w), np.float32)
    def put(r, al, cx, cy):
        y0, x0 = int(cy - al.shape[0] / 2), int(cx - al.shape[1] / 2)
        sl = (slice(y0, y0 + al.shape[0]), slice(x0, x0 + al.shape[1]))
        R[sl] = R[sl] * (1 - al[..., None]) + r * al[..., None]; A[sl] = A[sl] + al * (1 - A[sl])
    put(ra, aa, w / 2, h / 2); put(rb, ab, w / 2 + dx, h / 2 + dy); return R, A

print('peças…')
P = {}
cap = cv2.imread(f'{OUT}/01_capa.png').astype(np.float32)
z = np.zeros((1350, 1080, 3), np.uint8)
fol = colar(z, np.full((1290, 1000, 3), 255, np.uint8), rasgo_alpha(1000, 1290, 16, 9), 540, 677, -0.4, sombra=False)[..., 0]
al = cv2.GaussianBlur(fol, (0, 0), .8).astype(np.float32) / 255; ys, xs = np.where(al > .02)
P['capa'] = cap[ys.min():ys.max() + 1, xs.min():xs.max() + 1], al[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
P['fita'] = matte(lambda b: M.fita(b, 540, 675, 0, 120))
P['faixa'] = matte(lambda b: M.rodape(b, 675, 0))
for i, (n, nome, tema) in enumerate(LISTA):
    img = look(n)
    P[n] = matte(lambda b: M.impressa(b, img, 540, 60, 470, 0, fitas=((-.75, -1, -12), (.75, -1, 12)), seed=50 + i)[0])
    k = matte(lambda b: M.papel(b, 280, 600, 520, 132, 0, i % 3, 60 + i))
    t = texto(f'<div class="e" data-w="440" style="left:540px;top:30px;transform:translateX(-50%);text-align:center;font-family:AB;font-size:38px;line-height:1.05;color:#111">'
              f'<span style="color:#E61E6E">{i + 1:02d}</span> {nome}</div>'
              f'<div style="position:absolute;left:540px;top:84px;transform:translateX(-50%);white-space:nowrap;font-family:PF;font-style:italic;font-weight:700;font-size:28px;color:#2b2b2b">{tema}</div>')
    P['et' + n] = sobre(k, t, 0, -2)
P['mini_tit'] = texto('<div class="e" style="left:540px;top:20px;transform:translateX(-50%);text-align:center;white-space:nowrap">'
                      '<div style="font-family:AB;font-size:40px;color:#111">10 JEITOS DE ESTAR</div>'
                      '<div style="font-family:AB;font-size:118px;line-height:1;color:#E61E6E;letter-spacing:-2px">NO AR</div></div>')
P['tit_papel'] = matte(lambda b: M.papel(b, 120, 400, 840, 260, 0, 1, 77))
P['titulo'] = sobre(P['tit_papel'], P['mini_tit'], 0, 0)
P['faixa_txt'] = texto('<div style="position:absolute;left:540px;top:20px;transform:translateX(-50%);text-align:center;white-space:nowrap">'
                       '<div class="e" style="position:relative;font-family:AB;font-size:64px;line-height:1;color:#fff;letter-spacing:-1px">LISA MARIE NO AR</div>'
                       '<div class="e" style="position:relative;margin-top:10px;font-family:RB;font-weight:800;font-size:32px;color:#fff">Estreia em breve · <span style="color:#FFD84A;font-style:italic;font-weight:900">BINDER</span> Originals</div>'
                       '<div style="margin-top:12px;font-family:Geist;font-weight:500;font-size:15px;line-height:1.3;color:#D9D2C4">Lisa Marie · personagem original BINDER Originals · imagens conceituais<br>Símbolo e verso de carta de Magic © Wizards of the Coast</div></div>')
P['tag'] = texto('<div style="position:absolute;left:20px;top:20px;background:#111;color:#FFD84A;font-family:AB;font-size:46px;padding:10px 26px;letter-spacing:3px;white-space:nowrap">CONHEÇA OS 10 LOOKS</div>')

# ---------- muro (igual ao motor do Story) ----------
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
MURO = muro()

# ---------- animação ----------
cl = lambda x: min(1.0, max(0.0, x))
ease_in = lambda u: u ** 3
ease_io = lambda u: u * u * (3 - 2 * u)
def mola(t): return np.exp(-7 * t) * np.cos(16 * t) if t > 0 else 1.0

class Peca:
    """papel que voa e bate no muro (esc = escala final, de = deslocamento inicial, rot0 = rotação inicial)"""
    def __init__(s, nome, cx, cy, esc, ang, t0, dur=.42, de=(0, -1500), rot0=10, z0=1.3, t1=99):
        s.rgb, s.al = P[nome]; s.cx, s.cy, s.esc, s.ang, s.t0, s.dur, s.de, s.rot0, s.z0, s.t1 = cx, cy, esc, ang, t0, dur, de, rot0, z0, t1
    def estado(s, t):
        u = (t - s.t0) / s.dur
        if u < 0 or t >= s.t1: return None
        if u < 1:
            a = 1 - ease_in(u)
            return s.cx + s.de[0] * a, s.cy + s.de[1] * a, s.esc * (1 + (s.z0 - 1) * a), s.ang + s.rot0 * a, a
        m = mola(t - s.t0 - s.dur); return s.cx, s.cy, s.esc * (1 - .03 * m), s.ang - .9 * m, 0
    def bate(s): return s.t0 + s.dur

def blend(out, rgb, al, Mx, op=1.0):
    a2 = cv2.warpAffine(al, Mx, (W, H), flags=cv2.INTER_LINEAR)[..., None] * op
    if rgb is None: return out * (1 - a2)
    return out * (1 - a2) + cv2.warpAffine(rgb, Mx, (W, H), flags=cv2.INTER_LINEAR) * a2

def mat(p, cx, cy, esc, ang, C):
    h, w = p.al.shape
    R = cv2.getRotationMatrix2D((w / 2, h / 2), -ang, esc); R[:, 2] += [cx - w / 2, cy - h / 2]
    return (C @ np.vstack([R, [0, 0, 1]]))[:2]

# fase 1 · cartaz de estreia (entra já no quadro 0)
F1 = 2.4
capa = Peca('capa', 540, 860, .86, -1.2, -0.12, .42, de=(-40, -1300), rot0=-8, z0=1.2, t1=F1)
tag = Peca('tag', 540, 1640, 1.0, -3, 1.2, .3, de=(0, 500), rot0=6, z0=1.4, t1=F1)
fase1 = [capa, tag]
fitas1 = [(250, 330, -45, .55), (830, 330, 45, .78)]
# fase 2 · os 10 looks, um por segundo, empilhados como cartazes colados por cima
F2, PASSO, F3 = 2.4, 1.0, 12.6
fase2 = []
for i, (n, _, _) in enumerate(LISTA):
    t0 = F2 + i * PASSO; lado = -1 if i % 2 == 0 else 1
    dx, ang = [(-30, -3), (40, 2.5), (-50, 1.5), (35, -2), (0, 3), (-40, -1.5), (45, 2), (-20, -3), (30, 1), (0, -1.5)][i]
    fase2.append(Peca(n, 540 + dx, 800, 1.22, ang, t0, .36, de=(lado * 900, -500), rot0=-lado * 14, z0=1.3, t1=F3))
    fase2.append(Peca('et' + n, 540 + dx * .4, 1440, 1.15, -ang * .6, t0 + .28, .22, de=(-lado * 700, 300), rot0=lado * 10, z0=1.25,
                      t1=(t0 + PASSO + .28) if i < 9 else F3))   # a etiqueta sai quando chega a do look seguinte
# fase 3 · parede completa (grelha 5×2) + título + faixa
fase3 = [Peca('titulo', 540, 380, .95, -1.5, F3, .32, de=(0, -900), rot0=-6, z0=1.3)]
for i, (n, _, _) in enumerate(LISTA):
    c, r = i % 5, i // 5
    fase3.append(Peca(n, 136 + c * 202, 830 + r * 450 + (18 if c % 2 else -12), .45, [-3, 2, -1.5, 3, -2][c] * (1 if r == 0 else -1),
                      F3 + .35 + i * .09, .22, de=(0, -700), rot0=8, z0=1.4))
BATIDAS = [p.bate() for p in fase1 + fase2 + fase3] + [f[3] + .1 for f in fitas1]

def camera(t):
    if t < F2: s = 1.0
    elif t < F3: s = 1.0 + .06 * ((t - F2) / (F3 - F2))
    else: s = 1.0
    sx = sy = 0
    for b in BATIDAS:
        d = t - b
        if 0 <= d < .18: k = np.exp(-18 * d); sx += 3 * k * np.sin(90 * d); sy += 5 * k * np.cos(80 * d)
    return np.array([[s, 0, W / 2 - s * 540 + sx], [0, s, H / 2 - s * 960 + sy], [0, 0, 1]], np.float64)

def desenha(out, p, t, C):
    st = p.estado(t)
    if st is None: return out
    cx, cy, esc, ang, alt = st
    Mx = mat(p, cx, cy, esc, ang, C)
    sh = Mx.copy(); sh[:, 2] += [14 + 60 * alt, 24 + 90 * alt]
    out = blend(out, None, cv2.GaussianBlur(p.al, (0, 0), 6 + 18 * alt), sh, .4)
    return blend(out, p.rgb, p.al, Mx)

def frame(t):
    C = camera(t); out = cv2.warpAffine(MURO, C[:2], (W, H), borderMode=cv2.BORDER_REFLECT)
    if t < F1:
        out = desenha(out, capa, t, C)
        for x, y, ang, tf in fitas1:
            u = (t - tf) / .2
            if u < 0: continue
            k = ease_io(cl(u)); fr, fa = P['fita']
            Mx = mat(type('p', (), {'al': fa})(), x, y, .85 * (1.5 - .5 * k), ang + 25 * (1 - k), C)
            out = blend(out, fr, fa, Mx, cl(u * 2))
        out = desenha(out, tag, t, C)
    elif t < F3:
        for p in fase2: out = desenha(out, p, t, C)
    else:
        for p in fase3: out = desenha(out, p, t, C)
        u = (t - (F3 + 1.5)) / .45
        if u > 0:
            k = ease_io(cl(u)); m = mola(max(0, t - F3 - 1.95)); cy = 1735 + 260 * (1 - k)
            for nm, op in (('faixa', 1), ('faixa_txt', cl((t - F3 - 1.7) / .25))):
                r, a = P[nm]; h, w = a.shape
                R = cv2.getRotationMatrix2D((w / 2, h / 2), .8 + 2 * (1 - k) - .6 * m, 1.0); R[:, 2] += [540 - w / 2, cy - h / 2 - (4 if nm != 'faixa' else 0)]
                out = blend(out, r, a, R, op)
    if F3 - .12 < t < F3 + .05:                                 # corte seco com flash de papel
        out = out * .4 + 255 * .6
    return np.clip(out, 0, 255).astype(np.uint8)

if __name__ == '__main__':
    mp4 = f'{OUT}/LL-LISA01_teaser_v2.mp4'
    print('render…')
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', mp4], stdin=subprocess.PIPE)
    chaves = {int(x * FPS) for x in (0.0, 0.5, 1.8, 2.9, 4.9, 7.9, 11.9, 13.4, 15.9)}
    for i in range(int(FPS * DUR)):
        f = frame(i / FPS); ff.stdin.write(f.tobytes())
        if i in chaves: cv2.imwrite(mp4.replace('.mp4', f'_f{i:03d}.jpg'), f, [cv2.IMWRITE_JPEG_QUALITY, 85])
    ff.stdin.close(); ff.wait()
    tmp = mp4 + '.tmp.mp4'                                     # fecho do scanner (regra de todos os vídeos)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp4, '-i', FECHO, '-filter_complex',
                    '[0:v]setsar=1[a];[1:v]scale=1080:1920,setsar=1,fps=30[b];[a][b]concat=n=2:v=1:a=0[v]', '-map', '[v]',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', tmp], check=True)
    os.replace(tmp, mp4); print('ok', mp4)
