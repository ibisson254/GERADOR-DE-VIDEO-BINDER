"""Trilha original do especial (sintetizada aqui, sem amostras nem melodia existente).
Ré maior, 64 BPM: piano com poucas notas, cordas suaves e uma textura de ar quase inaudível.
Cresce até o meio (o "Picard não liderava...") e resolve em Ré no fim.
uso: import musica; musica.trilha(T_END, pico_ini, pico_fim, T_FIM_VOZ, SR) -> np.array (n, 2)
"""
import numpy as np

A4 = 440.0
def hz(n):  # n = número MIDI
    return A4 * 2 ** ((n - 69) / 12)

# acordes (MIDI): D, Bm, G, A, G, D/F#, Em7, Asus4->A, ... e resolução em D
PROG = [
    ('D',    [50, 57, 62, 66, 69]),
    ('Bm',   [47, 54, 62, 66, 71]),
    ('G',    [43, 55, 59, 62, 67]),
    ('A',    [45, 52, 61, 64, 69]),
    ('G',    [43, 55, 59, 62, 71]),
    ('D/F#', [42, 54, 62, 66, 69]),
    ('Em7',  [40, 55, 59, 62, 67]),
    ('Asus', [45, 52, 62, 64, 69]),
]
FIM = ('D', [38, 50, 57, 62, 66, 69])

def piano(f, dur, sr, vel):
    t = np.arange(int(dur * sr)) / sr
    dec = np.exp(-t * (1.6 + f / 900))
    s = (np.sin(2 * np.pi * f * t) + 0.42 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 2.5)
         + 0.18 * np.sin(2 * np.pi * 3.01 * f * t) * np.exp(-t * 4) + 0.06 * np.sin(2 * np.pi * 4.02 * f * t) * np.exp(-t * 6))
    att = np.clip(t / 0.006, 0, 1)
    return s * dec * att * vel

def cordas(fs, dur, sr, amp, rng):
    t = np.arange(int(dur * sr)) / sr
    out = np.zeros((len(t), 2))
    for k, f in enumerate(fs):
        for d, pan in ((-0.004, 0.3), (0.004, 0.7)):     # dois naipes levemente desafinados
            ff = f * (1 + d)
            vib = 1 + 0.0025 * np.sin(2 * np.pi * (4.6 + 0.3 * k) * t + rng.uniform(0, 6))
            ph = 2 * np.cumsum(np.pi * ff * vib / sr)
            w = sum(np.sin(h * ph) / h ** 1.6 for h in range(1, 7))   # serra suavizada
            out[:, 0] += w * (1 - pan); out[:, 1] += w * pan
    env = np.clip(t / 1.4, 0, 1) * np.clip((dur - t) / 1.2, 0, 1)
    return out * env[:, None] * amp / len(fs)

def lowpass(x, sr, fc):
    from scipy.signal import lfilter
    a = np.exp(-2 * np.pi * fc / sr)
    return lfilter([1 - a], [1, -a], x, axis=0)

def trilha(T, pico_a, pico_b, t_res, sr=44100, seed=7):
    rng = np.random.default_rng(seed)
    n = int(T * sr); out = np.zeros((n, 2))
    bar = 60 / 64 * 4                                    # 3,75 s por compasso
    tt = np.arange(n) / sr
    # curva de intensidade: entra baixo, cresce até o pico, volta a serena
    inten = np.interp(tt, [0, 3, pico_a, (pico_a + pico_b) / 2, pico_b, t_res, T], [0.35, 0.5, 0.7, 1.0, 0.8, 0.55, 0.5])
    k = 0; t0 = 0.0
    while t0 < t_res - 0.5:
        nome, ns = PROG[k % len(PROG)]
        dur = min(bar, t_res - t0)
        a, b = int(t0 * sr), int(t0 * sr) + int((dur + 1.2) * sr)
        b = min(b, n)
        cs = cordas([hz(x) for x in ns[1:4]], (b - a) / sr, sr, 0.22, rng)
        out[a:b] += cs[: b - a] * inten[a:b, None]
        # piano: arpejo esparso (3 ou 4 notas por compasso), notas do próprio acorde
        pat = [ns[2], ns[3], ns[4], ns[3]] if k % 2 == 0 else [ns[2], ns[4], ns[3]]
        for j, m in enumerate(pat):
            ts = max(0.0, t0 + j * bar / len(pat) + rng.uniform(-0.02, 0.02))
            if ts > t_res - 0.3: break
            p = piano(hz(m + 12), 3.2, sr, 0.16 * (0.9 + 0.2 * rng.random()))
            i0 = int(ts * sr); i1 = min(n, i0 + len(p)); pan = 0.4 + 0.2 * rng.random()
            out[i0:i1, 0] += p[: i1 - i0] * (1 - pan) * inten[i0:i1]; out[i0:i1, 1] += p[: i1 - i0] * pan * inten[i0:i1]
        bp = piano(hz(ns[0]), 3.8, sr, 0.10)           # baixo do piano
        i1 = min(n, a + len(bp)); out[a:i1] += (bp[: i1 - a] * inten[a:i1])[:, None] * 0.5
        t0 += bar; k += 1
    # resolução em Ré: acorde aberto longo
    a = int(t_res * sr); d = T - t_res
    if d > 0.5:
        cs = cordas([hz(x) for x in FIM[1][1:5]], d, sr, 0.24, rng); out[a:a + len(cs)] += cs[: n - a]
        for j, m in enumerate([FIM[1][0], FIM[1][2] + 12, FIM[1][4] + 12, FIM[1][3] + 24]):
            p = piano(hz(m), min(5.0, d), sr, 0.15 if j else 0.12); i0 = a + int(j * 0.32 * sr); i1 = min(n, i0 + len(p))
            out[i0:i1] += (p[: i1 - i0])[:, None] * 0.5
    # textura de ar (ruído filtrado), quase inaudível
    ar = lowpass(rng.standard_normal((n, 2)) * 0.02, sr, 900) * (0.5 + 0.5 * np.sin(2 * np.pi * tt / 9))[:, None]
    out += ar
    out = lowpass(out, sr, 5200)
    out *= (np.clip(tt / 1.5, 0, 1) * np.clip((T - tt) / 1.8, 0, 1))[:, None]
    return out / (np.max(np.abs(out)) + 1e-9) * 0.9
