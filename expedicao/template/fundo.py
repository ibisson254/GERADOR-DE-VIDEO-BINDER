# Expedição BINDER · fundo «Prisma Abissal» (v2). Pintura digital gerada em código, a partir das características
# das referências do designer (brief_v2.md): arrasto vertical, aguarela pastel, coluna espectral com reflexo,
# fenda prismática, linhas de sinal vermelhas, grão. Calculado a 540x960 e ampliado (é tudo difuso por natureza).
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy.ndimage import gaussian_filter

BW, BH = 540, 960
W, H = 1080, 1920
RED = np.array([255, 42, 42], np.float32)

def _up(a, w, h, res=Image.BICUBIC):
    return np.asarray(Image.fromarray(a.astype(np.float32), 'F').resize((w, h), res), np.float32)

def _noise(rng, gw, gh, w=BW, h=BH):
    return _up(rng.random((gh, gw)), w, h)

def _streaks(rng, h=BH, rows=10, w=BW, smooth=1.2):
    """campo de arrasto vertical (pixel-sort): poucas linhas aleatórias esticadas na vertical, periódico em y."""
    a = rng.random((rows, w)).astype(np.float32)
    a = np.concatenate([a, a[:2]], 0)
    up = _up(a, w, int(h * (rows + 2) / rows))[:h]
    up = gaussian_filter(up, (0, smooth), mode='wrap')
    return (up - up.min()) / (up.max() - up.min() + 1e-6)

def _hsmear(a, k):
    """arrasto horizontal (reflexo na água / riscos da aguarela)."""
    if a.ndim == 2: a = a[:, :, None]
    cs = np.cumsum(np.pad(a, ((0, 0), (k, k), (0, 0)), mode='edge'), 1)
    out = (cs[:, 2 * k:] - cs[:, :-2 * k]) / (2 * k)
    return out[:, :a.shape[1]] if out.shape[1] >= a.shape[1] else np.pad(out, ((0, 0), (0, a.shape[1] - out.shape[1]), (0, 0)), mode='edge')

def spectral(u):
    """u 0..1 -> cor espectral da ref. 3 (verde-lima, amarelo, laranja, magenta, violeta)."""
    stops = np.array([[120, 255, 140], [255, 240, 110], [255, 160, 70], [255, 70, 170], [150, 90, 255]], np.float32)
    x = np.clip(u, 0, 1) * (len(stops) - 1); i = np.minimum(x.astype(int), len(stops) - 2); f = (x - i)[..., None]
    return stops[i] * (1 - f) + stops[i + 1] * f

class Fundo:
    def __init__(self, seed=11):
        rng = np.random.default_rng(seed)
        yy = np.linspace(0, 1, BH)[:, None]; xx = np.linspace(0, 1, BW)[None, :]
        self.st1 = _streaks(rng, rows=12); self.st2 = _streaks(rng, rows=7, smooth=2.5); self.st3 = _streaks(rng, rows=16, smooth=0.6)
        # ---------- Rasos: aguarela pastel (ref. 5) com riscos horizontais, escurecida para as cartas respirarem
        pal = np.array([[88, 205, 214], [244, 150, 196], [170, 150, 236], [244, 222, 140], [118, 170, 244], [250, 120, 110]], np.float32)
        ws = [np.clip(_noise(rng, 3, 5) * 0.75 + _noise(rng, 9, 15) * 0.25, 0, 1) ** 4 for _ in pal]
        S = sum(ws) + 1e-6; past = sum(w[..., None] * c for w, c in zip(ws, pal)) / S[..., None]
        past = gaussian_filter(past, (22, 22, 0)) * 0.7 + _hsmear(past, 40) * 0.3
        sat = past.mean(-1, keepdims=True); past = sat + (past - sat) * 1.1; past = past * 0.85 + 255 * 0.12
        lum = 0.72 + 0.28 * _noise(rng, 5, 8)
        spk = (rng.random((BH, BW)) > 0.99993).astype(np.float32); spk = gaussian_filter(spk, 0.8) * 9
        past = past * lum[..., None] * 0.68 + spk[..., None] * np.array([255, 240, 250], np.float32) * 0.5
        self.rasos = np.concatenate([past, past[:, ::-1]], 1)  # largo para deslizar em x
        # ---------- Grande Marinho: arrasto vertical azul-violeta com núcleo rosa-pêssego (ref. 2)
        base = (np.array([14, 18, 52], np.float32) * (1 - yy[..., None]) + np.array([46, 62, 128], np.float32) * yy[..., None]) * np.ones((1, BW, 1))
        viol = np.array([120, 110, 200], np.float32)
        vary = 0.45 + 0.55 * _noise(rng, 5, 3)
        g = base + (self.st1[..., None] ** 1.6 * 0.8 + 0.1) * viol * 0.6 * vary[..., None]
        core = np.exp(-((xx - 0.47) / 0.09) ** 2) * (0.35 + 0.65 * yy) * (0.55 + 0.45 * self.st3)
        core = core * (0.4 + 0.6 * np.clip((yy - 0.15) / 0.6, 0, 1))
        g = g + core[..., None] * np.array([240, 120, 170], np.float32) * 1.15 + (core ** 3)[..., None] * np.array([255, 225, 190], np.float32) * 0.9
        cy = (self.st2 > 0.78) * np.exp(-((xx - 0.78) / 0.08) ** 2) * np.exp(-((yy - 0.45) / 0.2) ** 2)
        g = g + cy[..., None] * np.array([40, 200, 255], np.float32) * 1.4
        dark = np.clip((0.40 - xx) * 2.6 + (yy - 0.5) * 1.8, 0, 1) ** 0.7 * (0.55 + 0.45 * self.st1)   # massa escura a escorrer (canto inf. esq.)
        self.grande = g * (1 - 0.85 * dark[..., None])
        # ---------- Abismo: quase negro, uma coluna espectral e reflexo (ref. 3)
        self.hz = 0.64
        mist = np.exp(-((xx - 0.85) / 0.25) ** 2) * np.exp(-((yy - 0.35) / 0.3) ** 2) * (0.5 + 0.5 * self.st2)
        ab = np.array([7, 7, 12], np.float32) + mist[..., None] * np.array([60, 66, 92], np.float32)
        ab = ab * np.clip(0.35 + xx * 1.1, 0, 1)[..., None]
        self.abismo = ab
        cx = 0.5; dx = (xx - cx) / 0.055
        prof = np.exp(-dx ** 2 * 0.9)
        up = np.clip(yy / self.hz, 0, 1) ** 1.6
        col = prof * (0.25 + 0.75 * up) * (yy < self.hz)
        self.halo = np.exp(-((xx - cx) / 0.2) ** 2) * (0.2 + 0.8 * up) * (yy < self.hz + 0.02) * 0.5
        self.col_rgb = spectral(np.clip(0.5 + dx * 0.32, 0, 1) * np.ones((BH, 1)))
        self.col = col
        refl = np.flipud(np.where(yy[::-1] >= 0, 1, 1) * 0)  # placeholder para forma
        ry = np.clip((yy - self.hz) / (1 - self.hz), 0, 1)
        mirror_row = np.clip((self.hz - (yy - self.hz) * 1.1) * BH, 0, BH - 1).astype(int)[:, 0]
        r = (col * (0.45 + 0.55 * self.st3))[mirror_row]
        lines = 0.55 + 0.45 * np.sin(np.linspace(0, 260, BH))[:, None] ** 2
        r = _hsmear(r[..., None], 18)[..., 0] * (yy >= self.hz) * (1 - ry) ** 1.4 * lines * 0.65
        self.refl = r
        self.horizon = np.exp(-((yy - self.hz) / 0.006) ** 2) * np.exp(-((xx - cx) / 0.2) ** 2)
        # ---------- fenda prismática (ref. 1) para o Lotus: pedra em blocos + fissura de luz
        stone = (0.5 + 0.5 * _noise(rng, 30, 50)) * (0.6 + 0.4 * _noise(rng, 6, 10))
        img = Image.new('F', (BW, BH), 0); d = ImageDraw.Draw(img)
        for _ in range(26):
            x0 = rng.integers(0, BW); y0 = rng.integers(0, BH); w0 = rng.integers(40, 150); h0 = rng.integers(30, 110)
            d.rectangle((x0, y0, x0 + w0, y0 + h0), outline=1.0)
        self.stone = stone * 0.10 - np.asarray(img, np.float32) * 0.04
        pts = []; x = -10; y = 0.44 * BH
        while x < BW + 20:
            pts.append((x, y)); x += rng.integers(14, 38); y += rng.normal(0, 7) + 1.2
        crack = Image.new('F', (BW, BH), 0); ImageDraw.Draw(crack).line(pts, fill=1.0, width=5)
        for k in range(8):   # raízes da fissura
            p = pts[rng.integers(3, len(pts) - 3)]; q = (p[0] + rng.normal(0, 40), p[1] + rng.normal(30, 30))
            ImageDraw.Draw(crack).line([p, q], fill=0.8, width=2)
        c = np.asarray(crack, np.float32)
        self.crack_core = gaussian_filter(c, 2)
        self.crack_mid = gaussian_filter(c, 14) * 9
        self.crack_out = gaussian_filter(c, 60) * 60
        self.crack_x = xx * np.ones((BH, 1))
        self.grain = [np.random.default_rng(100 + i).normal(0, 6, (H // 2, W // 2)).astype(np.float32) for i in range(6)]

    # ------------------------------------------------------------------------------------------------
    def layer(self, name, t, energy=0.5, pulse=0.0, lotus=0.0):
        if name == 'rasos':
            sh = int(t * 9) % BW
            a = self.rasos[:, sh:sh + BW]
            st = np.roll(self.st2, int(t * 14), 0)
            a = a * (0.9 + 0.12 * st[..., None]) * (0.92 + 0.12 * energy)
        elif name == 'grande':
            st = np.roll(self.st1, int(t * 22), 0)[..., None]
            a = self.grande * (0.82 + 0.3 * st) * (0.9 + 0.18 * energy)
        else:
            col = self.col * (0.45 + 0.55 * np.roll(self.st3, int(t * 30), 0))
            k = (0.7 + 0.5 * energy) * (1 - 0.65 * lotus)
            a = self.abismo + (col * k)[..., None] * self.col_rgb * 1.1 + (self.refl * k)[..., None] * self.col_rgb * 0.9 \
                + (self.halo * k)[..., None] * np.array([110, 70, 200], np.float32) \
                + (self.horizon * k)[..., None] * np.array([255, 220, 200], np.float32) * 0.8
            if lotus > 0:
                a = a + self.stone[..., None] * 255 * lotus
                hue = spectral(np.clip(self.crack_x * 0.9 + 0.05, 0, 1))
                outer = spectral(np.clip(1 - self.crack_x * 1.0, 0, 1)) * 0.35 + np.array([40, 130, 255], np.float32) * 0.65
                m = np.clip(self.crack_mid, 0, 1.4)[..., None]
                a = a + (np.clip(self.crack_out, 0, 1)[..., None] * outer * 0.55 + m * np.array([255, 70, 150], np.float32) * 0.55
                         + m ** 3 * np.array([255, 160, 60], np.float32) * 0.5
                         + np.clip(self.crack_core * 2.2, 0, 1)[..., None] * np.array([255, 240, 210], np.float32) * 1.0) * lotus
        return a * (1 + 0.06 * pulse)

    def frame(self, t, cur, prev=None, mix=1.0, energy=0.5, pulse=0.0, lotus=0.0, glitch=0.0, sinal=0.0, seed=0):
        a = self.layer(cur, t, energy, pulse, lotus)
        if prev is not None and mix < 1:
            b = self.layer(prev, t, energy, pulse, 0)
            # transição «arrasto»: a camada nova escorre de cima para baixo com bordo irregular
            front = mix * 1.25 * BH - (1 - self.st3[0][None, :]) * 0.25 * BH
            m = np.clip((front - np.arange(BH)[:, None]) / 60, 0, 1)[..., None]
            a = a * m + b * (1 - m)
        if glitch > 0:    # deslocamento de faixas horizontais no corte (2-3 quadros)
            r = np.random.default_rng(seed)
            for _ in range(5):
                y0 = int(r.integers(0, BH - 40)); hh = int(r.integers(6, 40)); dx = int(r.normal(0, 26 * glitch))
                a[y0:y0 + hh] = np.roll(a[y0:y0 + hh], dx, 1)
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
        g = self.grain[int(t * 24) % len(self.grain)]
        arr = np.asarray(im, np.float32) + np.asarray(Image.fromarray(g, 'F').resize((W, H), Image.NEAREST))[..., None]
        if sinal > 0: arr = self.sinal(arr, sinal, seed)
        return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert('RGBA')

    def sinal(self, arr, k, seed):
        """linhas de sinal vermelhas (ref. 4): horizontais finas a partir de um ponto, com um traço vertical."""
        r = np.random.default_rng(seed); cx = int(W * 0.66); cy = int(H * 0.5)
        for i in range(5):
            y = cy + (0 if i == 0 else int(r.normal(0, 40))); x0 = int(cx - (W if i == 0 else r.uniform(150, 600)) * k); x1 = int(cx + (W * 0.4 if i == 0 else r.uniform(60, 260)) * k)
            th = 4 if i == 0 else 2; a = (1.0 if i == 0 else 0.7) * k
            arr[y:y + th, max(0, x0):min(W, x1)] = arr[y:y + th, max(0, x0):min(W, x1)] * (1 - a) + RED * a
        for i in range(3):
            x = cx + int(r.normal(0, 22)); y0 = int(cy - r.uniform(300, 900) * k)
            arr[max(0, y0):cy + 60, x:x + 3] = arr[max(0, y0):cy + 60, x:x + 3] * (1 - 0.85 * k) + RED * 0.85 * k
        return arr
