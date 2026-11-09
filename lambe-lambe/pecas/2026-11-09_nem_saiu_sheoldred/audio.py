"""Trilha sintetizada própria (efeitos + batida) para o Lambe-lambe "Nem saiu e já tem preço". Uso: python3 -I audio.py out.wav DUR"""
import sys, wave
import numpy as np
SR = 48000
DUR = float(sys.argv[2])
N = int(SR * DUR)
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(1)

def add(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR); j = min(N, i + len(sig))
    if i >= N: return
    L[i:j] += sig[:j - i] * gain * (1 - max(0, pan)); R[i:j] += sig[:j - i] * gain * (1 + min(0, pan))

def env(n, a=0.002, d=0.08):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / d)

def lp(x, k):  # passa-baixo simples
    y = np.zeros_like(x); acc = 0
    for i, v in enumerate(x): acc += k * (v - acc); y[i] = acc
    return y

def kick(n=int(0.35 * SR)):
    t = np.arange(n) / SR
    f = 50 + 110 * np.exp(-t / 0.03)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.12)

def hat(n=int(0.05 * SR)):
    x = rng.normal(0, 1, n); x = x - lp(x, 0.3)
    return x * env(n, 0.0005, 0.015) * 0.5

def slap():
    n = int(0.18 * SR); t = np.arange(n) / SR
    body = lp(rng.normal(0, 1, n), 0.25) * env(n, 0.001, 0.035) * 2.2
    thump = np.sin(2 * np.pi * 95 * t) * np.exp(-t / 0.04)
    return body + thump * 0.9

def tapefx():
    n = int(0.09 * SR); x = rng.normal(0, 1, n); x = x - lp(x, 0.2)
    return x * env(n, 0.002, 0.03) * 0.6

def rip():
    n = int(0.45 * SR); t = np.arange(n) / SR
    x = rng.normal(0, 1, n); x = x - lp(x, 0.08)
    crack = (rng.random(n) < 0.02).astype(float) * rng.normal(0, 3, n)
    return (x * 0.6 + crack) * np.minimum(1, t / 0.02) * np.exp(-t / 0.18)

def whoosh(d=0.95):
    n = int(d * SR); t = np.arange(n) / SR
    x = rng.normal(0, 1, n)
    out = np.zeros(n); acc = 0
    k = 0.02 + 0.5 * (t / d) ** 2
    for i in range(n): acc += k[i] * (x[i] - acc); out[i] = acc
    rise = np.sin(2 * np.pi * np.cumsum(200 + 900 * (t / d) ** 2) / SR) * 0.25
    e = (t / d) ** 1.5 * np.exp(-np.maximum(0, t - d * 0.9) / 0.03)
    return (out * 2.5 + rise) * e

def click():
    n = int(0.03 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * 2400 * t) * np.exp(-t / 0.006) * 0.5

def chime():
    n = int(0.5 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1318 * t) + 0.6 * np.sin(2 * np.pi * 1975 * t)) * np.exp(-t / 0.15) * 0.25

def bass(f, d):
    n = int(d * SR); t = np.arange(n) / SR
    x = np.sign(np.sin(2 * np.pi * f * t)) * 0.5 + np.sin(2 * np.pi * f * t)
    return lp(x, 0.06) * env(n, 0.005, d * 0.6)

BPM = 128; B = 60 / BPM
T2, T3, T4, T5, TEND = 2.55, 4.55, 5.45, 8.45, 10.55
# batida (pausa durante o redemoinho, volta forte no cartaz preto)
t = 0.0; notes = [55, 55, 65.4, 49]
k = 0
while t < TEND:
    if not (T3 + 0.05 < t < T4 - 0.02):
        add(kick(), t, 0.9)
        add(bass(notes[(k // 4) % 4], B * 0.9), t, 0.32)
    add(hat(), t + B / 2, 0.35, 0.3)
    if k % 2: add(hat(), t + B * 0.75, 0.2, -0.3)
    t += B; k += 1
# no fecho: batida aberta e fade
t = TEND
while t < DUR - 0.3:
    add(kick(), t, 0.75); add(bass(55, B * 1.8), t, 0.28); add(hat(), t + B / 2, 0.3, 0.2)
    t += B * 2
# efeitos
for i in range(8): add(slap(), 0.05 + i * 0.22, 0.55, (-0.4, 0.4)[i % 2]); add(tapefx(), 0.09 + i * 0.22, 0.4)
add(slap(), 0.0, 0.4); add(slap(), T2, 0.7); add(slap(), T2 + 0.5, 0.35)
add(rip(), T2 + 1.62, 0.8)
add(whoosh(), T3 - 0.05, 0.6)
add(slap(), T4, 0.85); add(tapefx(), T4 + 0.05, 0.5); add(slap(), T4 + 0.25, 0.35)
add(click(), 7.02, 0.8); add(chime(), 7.17, 0.6)
add(slap(), T5, 0.85); add(slap(), T5 + 0.15, 0.4); add(slap(), T5 + 0.55, 0.5)
# fade final
fade = np.ones(N); fl = int(0.6 * SR); fade[-fl:] = np.linspace(1, 0, fl)
st = np.stack([L * fade, R * fade], 1)
st /= np.max(np.abs(st)); st *= 10 ** (-6 / 20)
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes())
print("ok")
