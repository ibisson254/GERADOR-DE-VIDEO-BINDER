#!/usr/bin/env python3
"""PREGÃO MAGIC — trilha (música fornecida, editada na grelha) + sound design sintetizado localmente.

Uso: python3 audio.py MUSICA.mp3 SAIDA.wav [--voz VOZ.wav]
Sem créditos externos: todos os efeitos são gerados aqui com numpy/scipy.
"""
import subprocess, sys, json
import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000
B = 60 / 184.5703
M0 = 140.085            # início do drop da música
TOTAL = 46.87           # 43,0 s + fecho 3,87 s
rng = np.random.default_rng(7)

def carregar(p):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", p, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()

def seg(x, a, b):
    return x[int(a * SR):int(b * SR)].copy()

def xfade_concat(partes, ms=30):
    n = int(SR * ms / 1000); out = partes[0]
    for p in partes[1:]:
        r = np.linspace(0, 1, n)[:, None]
        out = np.concatenate([out[:-n], out[-n:] * (1 - r) + p[:n] * r, p[n:]])
    return out

def lp(x, fc):
    return sosfilt(butter(4, fc, "low", fs=SR, output="sos"), x, axis=0)

def hp(x, fc):
    return sosfilt(butter(2, fc, "high", fs=SR, output="sos"), x, axis=0)

def env(n, a=0.002, d=0.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / d)

def st(m, pan=0.0):
    return np.stack([m * (1 - max(0, pan)), m * (1 + min(0, pan))], 1)

# ----- efeitos -----
def impact(dur=0.9, f0=110, f1=38, ruido=0.6):
    n = int(dur * SR); t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t * 18)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.32)
    nz = lp(rng.standard_normal(n), 2500) * env(n, 0.0005, 0.05) * ruido
    return st(np.tanh(1.6 * (s + nz)))

def snap(dur=0.25):
    n = int(dur * SR)
    nz = hp(rng.standard_normal(n), 1500) * env(n, 0.0005, 0.025)
    k = np.sin(2 * np.pi * 180 * np.arange(n) / SR) * env(n, 0.001, 0.04)
    return st(0.7 * nz + 0.6 * k)

def whoosh(dur=0.45, sobe=True, pan=0.0):
    n = int(dur * SR); t = np.linspace(0, 1, n)
    nz = rng.standard_normal(n)
    out = np.zeros(n); blocos = 24
    for i in range(blocos):
        a, b = i * n // blocos, (i + 1) * n // blocos
        x = (i + 0.5) / blocos
        fc = 300 + 6000 * (x if sobe else 1 - x)
        out[a:b] = lp(nz[max(0, a - 2000):b], fc)[-(b - a):]
    out *= np.sin(np.pi * t) ** 1.5
    return st(out * 1.4, pan)

def riser(dur=1.3):
    n = int(dur * SR); t = np.linspace(0, 1, n)
    nz = hp(rng.standard_normal(n), 800) * t ** 2
    tone = np.sin(2 * np.pi * np.cumsum(200 + 900 * t ** 2) / SR) * t ** 2 * 0.3
    return st(0.6 * nz + tone)

def alerta(sobe=True):
    notas = [880, 1320] if sobe else [1320, 660]
    partes = []
    for f in notas:
        n = int(0.11 * SR); t = np.arange(n) / SR
        partes.append(np.sign(np.sin(2 * np.pi * f * t)) * 0.25 * env(n, 0.002, 0.09) + np.sin(2 * np.pi * f * t) * 0.3 * env(n, 0.002, 0.1))
    return st(np.concatenate(partes))

def ding(f=1568):
    n = int(0.9 * SR); t = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t * (3 + 4 * m)) for a, m in [(1, 1), (0.5, 2.01), (0.3, 3.03), (0.2, 4.2)])
    return st(0.5 * s * np.minimum(1, t / 0.002))

def tick():
    n = int(0.03 * SR)
    return st(hp(rng.standard_normal(n), 3000) * env(n, 0.0003, 0.006) * 0.6)

def ticks(dur, passo=0.045):
    n = int(dur * SR); out = np.zeros((n, 2))
    for i in range(int(dur / passo)):
        tk = tick(); a = int(i * passo * SR); out[a:a + len(tk)] += tk[:max(0, n - a)]
    return out

def ping():
    n = int(0.6 * SR); t = np.arange(n) / SR
    return st(np.sin(2 * np.pi * 1200 * t) * np.exp(-t * 7) * 0.4 + np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 12) * 0.1)

def glitch_s(dur=0.4):
    n = int(dur * SR); out = rng.standard_normal(n)
    sq = np.sign(np.sin(2 * np.pi * 60 * np.arange(n) / SR))
    out = (out * (sq > 0) * 0.5 + np.sign(np.sin(2 * np.pi * 220 * np.arange(n) / SR)) * 0.2) * env(n, 0.001, 0.15)
    return st(lp(out, 5000))

def bass(f=48, dur=0.7):
    n = int(dur * SR); t = np.arange(n) / SR
    return st(np.tanh(2 * np.sin(2 * np.pi * f * t)) * env(n, 0.003, 0.3) * 0.8)

def eventos():
    E = []
    def a(t, x, g): E.append((t, x, g))
    # Bloco A
    a(0.0, impact(1.0, 140, 35, 1.0), 0.9); a(0.0, bass(42), 0.7)
    a(B, snap(), 0.7)
    a(2 * B, impact(0.8, 90, 30), 0.75); a(2 * B, alerta(False), 0.35)
    a(3 * B, whoosh(0.5, False, -0.3), 0.35)
    a(6 * B, ticks(0.4), 0.4)
    a(8 * B - 0.05, whoosh(0.35, True, 0.5), 0.6)
    a(9 * B, alerta(True), 0.35); a(9 * B, ding(), 0.4)
    a(12 * B, impact(0.9, 120, 40), 0.7)
    a(14 * B, riser(2 * B), 0.35)
    # Bloco B
    a(16 * B, whoosh(0.5, True), 0.55); a(16 * B, bass(55), 0.6)
    a(18 * B - 0.2, whoosh(0.3, True), 0.5); a(18 * B, snap(), 0.5)
    a(22 * B, ticks(0.6), 0.45); a(22 * B, alerta(True), 0.3); a(22 * B + 0.6, ding(1760), 0.45)
    a(26 * B, ping(), 0.3)
    a(34 * B, snap(), 0.7); a(34 * B, bass(62, 0.4), 0.4)
    a(38 * B, ticks(0.6), 0.45); a(38 * B + 0.6, ding(1760), 0.45)
    a(42 * B, whoosh(0.35, True, 0.6), 0.4); a(42 * B + 0.3, ping(), 0.3)
    a(48 * B, riser(2 * B), 0.3)
    # Bloco C
    a(50 * B, impact(1.2, 160, 28, 1.0), 0.95); a(50 * B, glitch_s(0.45), 0.4)
    a(52 * B, whoosh(0.32, False), 0.5); a(52 * B + 0.3, impact(0.8, 80, 30), 0.8)
    a(56 * B, ticks(0.6), 0.45); a(56 * B, alerta(False), 0.35); a(56 * B + 0.6, bass(40), 0.6)
    a(60 * B, ping(), 0.25)
    a(68 * B, snap(), 0.7); a(72 * B, alerta(False), 0.35); a(72 * B, ticks(0.6), 0.4); a(72 * B + 0.6, bass(40), 0.5)
    a(78 * B, impact(0.7, 70, 30, 0.3), 0.6)
    # Bloco D
    a(86 * B - 0.2, whoosh(0.3, False), 0.4)
    k = 86 * B
    while k < 102 * B - 0.3:
        a(k, ping(), 0.35); k += 2 * np.pi / 3.2
    a(90 * B, ding(1318), 0.25); a(92 * B, ding(1318), 0.25)
    a(94 * B, bass(50, 0.5), 0.5); a(98 * B, bass(50, 0.5), 0.5)
    # Bloco E
    a(102 * B, whoosh(0.4, True), 0.45); a(102 * B + 0.4, alerta(True), 0.25)
    a(106 * B, ding(2093), 0.4)
    a(118 * B, snap(), 0.4)
    a(43.0, impact(1.0, 120, 40, 0.4), 0.6)
    return E

def lufs(x):
    import pyloudnorm as pyln
    return pyln.Meter(SR).integrated_loudness(x)

def main():
    mus, saida = sys.argv[1], sys.argv[2]
    voz = sys.argv[sys.argv.index("--voz") + 1] if "--voz" in sys.argv else None
    m = carregar(mus)
    c1, c2 = M0 + 64 * B, M0 + 32 * B
    trilha = xfade_concat([seg(m, M0, c1), seg(m, c2, c1), seg(m, c1, c1 + 16.5)])
    n = int(TOTAL * SR); trilha = trilha[:n]
    if len(trilha) < n: trilha = np.concatenate([trilha, np.zeros((n - len(trilha), 2))])
    # mudança de atmosfera nas quedas: filtro passa-baixo do impacto até a carta cair
    a0, a1 = int(50 * B * SR), int(52 * B * SR)
    trilha[a0:a1] = lp(trilha[a0:a1], 500) * 1.4
    # cauda: desvanecer nos últimos 2,5 s
    f = int(2.5 * SR); trilha[-f:] *= np.linspace(1, 0, f)[:, None] ** 1.5
    sfx = np.zeros((n, 2))
    for t, x, g in eventos():
        i = int(t * SR); j = min(n, i + len(x))
        if i < n: sfx[i:j] += x[:j - i] * g
    mix_m = trilha * 0.55
    if voz:
        v = carregar(voz)[:n]
        v = np.concatenate([v, np.zeros((n - len(v), 2))]) if len(v) < n else v
        # ducking da música sob a voz (envolvente RMS suavizada)
        e = np.sqrt(np.convolve((v[:, 0] ** 2), np.ones(2400) / 2400, "same"))
        g = 1 - 0.55 * np.clip(e / (e.max() * 0.15 + 1e-9), 0, 1)
        g = np.convolve(g, np.ones(4800) / 4800, "same")
        mix = mix_m * g[:, None] + sfx * 0.8 + v * 1.0
    else:
        mix = mix_m + sfx * 0.8
    # normalização -14 LUFS e limitação de pico
    L = lufs(mix); mix = mix * 10 ** ((-14.0 - L) / 20)
    for _ in range(3):
        pk = np.abs(mix).max()
        if pk > 0.84:  # ~ -1,5 dBFS
            mix = np.tanh(mix / 0.84 * 1.0) * 0.84
        L = lufs(mix); mix = mix * 10 ** ((-14.0 - L) / 20)
    mix = np.clip(mix, -0.86, 0.86)
    print(json.dumps({"lufs": round(lufs(mix), 2), "pico_dbfs": round(20 * np.log10(np.abs(mix).max()), 2)}))
    import soundfile as sf
    sf.write(saida, mix.astype(np.float32), SR, subtype="PCM_24")

if __name__ == "__main__":
    main()
