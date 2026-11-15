# ABISMO · camada de vida: medusas bioluminescentes + luz ondulante (cáusticas), sincronizadas com a música.
# "O abismo respira": cada medusa contrai-se no 1.º tempo do compasso, no mesmo instante em que a carta pulsa.
# Procedural (numpy + PIL), custo zero, sem imagens de terceiros. Valores em identidade.json -> "vida".
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def ease(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)

def contracao(t, ciclo, fase):
    """0 = relaxada, 1 = contraída. Aperto rápido (25% do ciclo) e relaxamento lento, como uma medusa real."""
    u = (t / ciclo + fase) % 1
    return ease(u / 0.25) if u < 0.25 else math.exp(-(u - 0.25) * 6)

class Vida:
    def __init__(self, W, H, cfg, periodo):
        self.W, self.H, self.cfg = W, H, cfg
        self.ciclo = cfg['pulso_batidas'] * periodo
        self.h = 2   # desenho a meia resolução, depois amplia
        self.cores = {k: np.array(v, np.float32) for k, v in cfg['cores'].items()}
        self.calma = np.ones((H, W), np.float32)
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        for z in cfg.get('_zonas', []):   # (x0, y0, x1, y1, fator, margem_px)
            x0, y0, x1, y1, f, mg = z
            dx = np.maximum(np.maximum(x0 - xx, xx - x1), 0); dy = np.maximum(np.maximum(y0 - yy, yy - y1), 0)
            k = np.clip(np.hypot(dx, dy) / mg, 0, 1); k = k * k * (3 - 2 * k)
            self.calma = np.minimum(self.calma, f + (1 - f) * k)
        w8, h8 = W // 8, H // 8
        self.X, self.Y = np.meshgrid(np.linspace(0, 1, w8), np.linspace(0, H / W, h8))

    def _medusa(self, d, m, t, s):
        W, H = self.W / self.h, self.H / self.h
        c = contracao(t, self.ciclo, m['fase'])
        r = m['r'] * W; bw = r * (1 - 0.14 * c); bh = r * 0.72 * (1 + 0.12 * c)
        # deslocação real: deriva constante + impulso no fim de cada contração (como uma medusa a nadar)
        u = t / self.ciclo + m['fase']; imp = math.floor(u) + (ease((u % 1) / 0.25) if (u % 1) < 0.25 else 1)
        dist = m['vel'] * t + m['impulso'] * imp
        ang = math.radians(m['rumo'] + 9 * math.sin(t * 0.4 + 5 * m['fase']))   # direção do corpo (0 = para cima)
        mx = m['x'] + math.sin(ang) * dist + 0.02 * math.sin(t * 0.3 + 7 * m['fase'])
        my = m['y'] - math.cos(ang) * dist * W / H
        mx = (mx + 0.2) % 1.4 - 0.2; my = (my + 0.25) % 1.5 - 0.25   # sai por um lado, volta a entrar pelo outro
        cx, cy = mx * W, my * H
        ca, sa = math.cos(ang), math.sin(ang)
        def R(x, y): x -= cx; y -= cy; return (cx + x * ca - y * sa, cy + x * sa + y * ca)
        a = s * (0.9 + 0.1 * c)   # sem flash: a única pulsação forte do quadro é a da carta
        # tentáculos: onda que viaja para baixo, amplitude cresce com a distância à campânula
        L = bh * 3.4 * (1 + 0.12 * (1 - c)); n = 9
        for i in range(n):
            x0 = cx + bw * (-0.85 + 1.7 * i / (n - 1)) * (1 - 0.1 * c); ph = i * 1.7 + m['fase'] * 9
            pts = [R(x0 + bw * 0.28 * k * math.sin(5.5 * k - 2 * math.pi * t / (self.ciclo * 1.3) + ph), cy + 0.06 * bh + k * L) for k in np.linspace(0, 1, 26)]
            for j in range(len(pts) - 1):
                d.line((pts[j], pts[j + 1]), fill=int(170 * a * (1 - j / 25) ** 1.3), width=2)
        # braços orais: mais grossos, curtos e ondulantes
        for i in range(4):
            x0 = cx + bw * (-0.3 + 0.2 * i); ph = i * 2.3 + m['fase'] * 5
            pts = [R(x0 + bw * 0.22 * k * math.sin(4 * k - 2 * math.pi * t / (self.ciclo * 1.6) + ph), cy + k * bh * 1.9) for k in np.linspace(0, 1, 18)]
            for j in range(len(pts) - 1):
                d.line((pts[j], pts[j + 1]), fill=int(120 * a * (1 - j / 17)), width=5)
        # campânula: cúpula translúcida, bordo festonado e brilhante, nervuras internas
        th = np.linspace(math.pi, 2 * math.pi, 40)
        top = [R(cx + bw * math.cos(q), cy + bh * math.sin(q)) for q in th]
        rim = [R(cx + bw * (1 - 2 * k), cy + 0.07 * bh * math.sin(k * 8 * math.pi + t * 3)) for k in np.linspace(0, 1, 30)]
        d.polygon(top + rim, fill=int(55 * a))
        d.line(top, fill=int(235 * a), width=3); d.line(rim, fill=int(150 * a), width=2)
        for k in (0.35, 0.62):
            d.line([R(cx + bw * k * math.cos(q), cy + bh * k * math.sin(q) - 0.05 * bh) for q in th], fill=int(90 * a), width=2)
        for q in np.linspace(math.pi * 1.15, math.pi * 1.85, 6):
            d.line((R(cx, cy - 0.1 * bh), R(cx + bw * 0.95 * math.cos(q), cy + bh * 0.95 * math.sin(q))), fill=int(55 * a), width=1)

    def aplicar(self, im, t, forca=1.0):
        if not self.cfg.get('ativo', True) or forca <= 0: return im
        A = np.array(im, np.float32)
        w2, h2 = self.W // self.h, self.H // self.h
        for m in self.cfg['medusas']:
            L = Image.new('L', (w2, h2), 0); self._medusa(ImageDraw.Draw(L), m, t, forca * m.get('intensidade', 1.0))
            pr = m['profundidade']   # 0 = perto, 1 = longe: mais longe = mais desfocada e mais fraca
            nit = np.array(L.filter(ImageFilter.GaussianBlur(1 + 3 * pr)).resize((self.W, self.H), Image.BILINEAR), np.float32) / 255
            gl = np.array(L.filter(ImageFilter.GaussianBlur(8 + 10 * pr)).resize((self.W, self.H), Image.BILINEAR), np.float32) / 255
            A[..., :3] += self.cores[m['cor']] * ((nit * 0.5 + gl * 1.1) * self.cfg['forca'] * self.calma)[..., None]
        # luz ondulante: rede fina de cáusticas a fluir, mais visível em cima
        X, Y, T = self.X, self.Y, t
        a = np.sin(X * 9 + 1.6 * np.sin(Y * 6 + T * 0.55)); b = np.sin(Y * 11 + 1.6 * np.sin(X * 7 - T * 0.45))
        k = ((1 - np.abs(a)) ** 10 + (1 - np.abs(b)) ** 10) * (1 - 0.65 * Y / Y.max())
        k = np.array(Image.fromarray((k * 255).clip(0, 255).astype(np.uint8)).resize((self.W, self.H), Image.BICUBIC), np.float32) / 255
        A[..., :3] += self.cores['ciano'] * (k * self.cfg['caustica'] * forca * self.calma)[..., None]
        return Image.fromarray(A.clip(0, 255).astype(np.uint8), im.mode)
