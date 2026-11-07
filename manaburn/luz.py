"""Luz e profundidade padrão do Mana & Burn (decisão de 07/11/2026; origem: V2 do especial "Precon em jogo").

Aplica sobre o MP4 já renderizado, quadro a quadro, sem tocar no áudio (-c:a copy):
luz ambiente quente com sombras abertas · reflexo frio azul-esverdeado à volta da TV (segue o logo da
TV SAL e apaga com a tela) · parede com menos contraste · primeiro plano mais escuro, com desfoque leve
abaixo da zona das legendas · vinheta leve. Ficam com os pixels originais: tela da TV, legendas, tarja e,
com --ate, tudo a partir desse segundo (fecho do scanner).

Uso:
  python3 -I luz.py ENTRADA.mp4 SAIDA.mp4            # vídeo do render.py (sem fecho): tudo
  python3 -I luz.py ENTRADA.mp4 SAIDA.mp4 --ate 75.47 # vídeo que já tem o fecho: para no início dele
  luz.quadro(rgb_uint8)                               # um quadro solto (ex.: capa)
render.py chama isto por defeito; `python3 render.py SAIDA.mp4 [capa] --sem-luz` desliga.
"""
import subprocess, sys
import numpy as np, cv2
from scipy import ndimage as nd

W, H, FPS = 1080, 1920, 30
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
def ramp(v, a, b): return np.clip((v - a) / (b - a), 0, 1)

# máscaras fixas (geometria do quadro, iguais em todos os planos)
fundo   = 1 - ramp(yy, 480, 760)                                   # parede: contraste um pouco menor
frente  = ramp(yy, 1500, 1920) ** 1.3                              # chão/mesa em primeiro plano: mais escuro
cantos  = np.clip(((xx - 540) / 540) ** 2 * 0.6 + ((yy - 900) / 1100) ** 2 * 0.5 - 0.25, 0, 1)  # vinheta leve
tarja   = (1 - ramp(xx, 620, 760)) * (1 - ramp(yy, 290, 400))      # MANA & BURN + crédito: intocáveis (borda suave)
desfoq  = ramp(yy, 1620, 1780)                                      # desfoque suave só abaixo da zona das legendas
TEAL    = np.array([0.30, 0.86, 0.80], np.float32)                  # reflexo frio da TV (RGB)

def acha_tv(a, ult):
    """Logo verde da TV SAL → centro e escala da TV (geometria do kit: logo no canto sup. direito)."""
    r, g, b = (a[..., i].astype(np.int16) for i in range(3))
    m = (g > 130) & (g - r > 70) & (b - r > 30) & (g - b > 15)
    lab, n = nd.label(m)
    best = None
    for i, o in enumerate(nd.find_objects(lab)):
        h, w = o[0].stop - o[0].start, o[1].stop - o[1].start
        if h < 12 or not 0.3 <= w / h <= 1.3: continue
        s = (lab[o] == i + 1).sum()
        if s < 40 or s / (w * h) < 0.25: continue
        if best is None or s > best[0]: best = (s, o)
    if best is None: return ult
    o = best[1]
    # junta os pedaços vizinhos do logo (nos planos de sala ele aparece partido em 2)
    ys, xs = np.nonzero(m[max(0, o[0].start - 30):o[0].stop + 30, max(0, o[1].start - 30):o[1].stop + 30])
    y0, x0 = max(0, o[0].start - 30) + ys.min(), max(0, o[1].start - 30) + xs.min()
    y1, x1 = max(0, o[0].start - 30) + ys.max(), max(0, o[1].start - 30) + xs.max()
    s = (y1 - y0 + 1) / 30.0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    return (cx, cy, s)

def grade(f, tv):
    a = f.astype(np.float32) / 255
    proteg = np.zeros((H, W), np.float32)
    mn = a.min(2); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    proteg = np.maximum(proteg, ramp(mn, 0.80, 0.86))                         # texto branco das legendas / cartão
    proteg = np.maximum(proteg, ((r > 0.88) & (g > 0.72) & (b < 0.50)).astype(np.float32))  # amarelo #FFD84A
    proteg = cv2.dilate(proteg, np.ones((3, 3), np.uint8))
    glow = np.zeros((H, W), np.float32)
    if tv:
        cx, cy, s = tv
        x0, x1, y0, y1 = cx - 369 * s, cx + 43 * s, cy - 63 * s, cy + 213 * s     # corpo da TV
        caixa = (ramp(xx, x0 - 28, x0 + 2) * (1 - ramp(xx, x1 - 2, x1 + 28)) *
                 ramp(yy, y0 - 28, y0 + 2) * (1 - ramp(yy, y1 - 2, y1 + 28)))    # TV inteira intocada, borda suave
        proteg = np.maximum(proteg, caixa)
        sx, sy = (x0 + x1) / 2 - 40 * s, (y0 + y1) / 2                       # centro da tela
        sig = 0.62 * (x1 - x0)
        ilum = a[int(max(0, y0 + 40 * s)):int(min(H, y1 - 40 * s)), int(max(0, x0 + 30 * s)):int(min(W, x1 - 120 * s))]
        k = float(np.clip(ilum.mean() / 0.30, 0, 1)) if ilum.size else 0     # TV apagada = sem reflexo
        glow = k * np.exp(-(((xx - sx) ** 2 + (yy - sy) ** 2) / (2 * sig * sig))) * (1 - caixa)
    livre = (1 - proteg) * (1 - tarja)
    o = a.copy()
    # A. luz ambiente quente e sombras abertas (sem mexer na saturação)
    o = o + 0.05 * (1 - o) ** 3
    o = o * np.array([1.025, 1.006, 0.965], np.float32)
    # B. parede com menos contraste, primeiro plano mais escuro, vinheta leve
    o = o + (fundo * 0.08)[..., None] * (0.47 - o)
    o = o * (1 - (0.24 * frente + 0.10 * cantos))[..., None]
    bl = cv2.GaussianBlur(o, (0, 0), 1.8)
    o = o + desfoq[..., None] * (bl - o)
    # A. reflexo frio azul-esverdeado da TV na região próxima (tela tipo "screen")
    gl = (0.13 * glow)[..., None] * TEAL
    o = 1 - (1 - o) * (1 - gl)
    o = a + livre[..., None] * (np.clip(o, 0, 1) - a)
    return (o * 255 + 0.5).astype(np.uint8)

def quadro(f):
    """Um quadro solto (RGB uint8, 1080×1920)."""
    return grade(f, acha_tv(f, None))

def aplicar(src, dst, ate=None):
    n_max = int(ate * FPS) if ate else 10 ** 9
    dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-i', src, '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17',
                            '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'copy', '-movflags', '+faststart', dst], stdin=subprocess.PIPE)
    i, tv = 0, None
    while True:
        buf = dec.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        f = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        if i < n_max:
            novo = acha_tv(f, None)
            if novo and tv and abs(novo[2] - tv[2]) < 0.15 * tv[2]:      # suaviza só dentro do mesmo plano
                tv = tuple(0.5 * p + 0.5 * q for p, q in zip(tv, novo))
            else:
                tv = novo or tv
            f = grade(f, tv)
        enc.stdin.write(f.tobytes()); i += 1
        if i % 300 == 0: print('luz: quadro', i, flush=True)
    enc.stdin.close(); enc.wait(); dec.wait()
    if enc.returncode: raise SystemExit('luz: ffmpeg falhou')
    print('luz:', i, 'quadros ->', dst)

if __name__ == '__main__':
    a = sys.argv[1:]
    ate = float(a[a.index('--ate') + 1]) if '--ate' in a else None
    aplicar(a[0], a[1], ate)
