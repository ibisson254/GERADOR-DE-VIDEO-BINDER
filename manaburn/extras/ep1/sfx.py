"""Efeitos sonoros sintetizados (sem amostras de terceiros): estática de TV, cartas embaralhando,
clique do controle remoto e TV de tubo desligando."""
import numpy as np
from scipy.signal import butter, sosfilt
rng = np.random.default_rng(42)

def _f(x, kind, f, sr, order=2):
    return sosfilt(butter(order, f, kind, fs=sr, output='sos'), x)

def static(sr, dur=0.38):
    n = int(dur * sr); t = np.arange(n) / sr
    x = _f(rng.standard_normal(n), 'band', [900, 9000], sr)
    crack = (rng.random(n) > 0.9965) * rng.standard_normal(n) * 6
    env = np.minimum(1, t / 0.008) * np.exp(-t / 0.16)
    return (x * 0.5 + _f(crack, 'high', 1500, sr)) * env * 0.42

def shuffle(sr, dur=0.8):
    n = int(dur * sr); out = np.zeros(n)
    k = 46; ts = np.cumsum(np.r_[0, 0.006 + 0.016 * np.sin(np.linspace(0.3, 2.8, k - 1)) ** 2])
    ts = ts / ts[-1] * (dur * 0.72)
    for t0 in ts:                                   # cada carta batendo na outra
        m = int(0.006 * sr); a = int(t0 * sr)
        b = _f(rng.standard_normal(m), 'band', [1800, 7500], sr) * np.exp(-np.arange(m) / (0.0012 * sr))
        out[a:a + m] += b * (0.5 + 0.5 * rng.random())
    w = _f(rng.standard_normal(n), 'low', 1400, sr) * np.exp(-((np.arange(n) / sr - dur * 0.35) / 0.22) ** 2) * 0.25
    for t0 in (dur * 0.84, dur * 0.9):               # o maço batendo na mesa
        m = int(0.03 * sr); a = int(t0 * sr)
        out[a:a + m] += _f(rng.standard_normal(m), 'band', [300, 2500], sr) * np.exp(-np.arange(m) / (0.004 * sr)) * 1.2
    return (out + w) * 0.5

def click(sr):
    n = int(0.06 * sr); out = np.zeros(n)
    for t0, v in ((0, 1), (0.018, .6)):
        m = int(0.004 * sr); a = int(t0 * sr)
        out[a:a + m] += _f(rng.standard_normal(m), 'band', [2000, 6000], sr) * np.exp(-np.arange(m) / (0.0008 * sr)) * v
    return out * 0.7

def crt_off(sr, dur=0.9):
    n = int(dur * sr); t = np.arange(n) / sr
    zap_f = 1400 * np.exp(-t / 0.07) + 70
    zap = np.sin(2 * np.pi * np.cumsum(zap_f) / sr) * np.exp(-t / 0.12) * 0.5
    thump = np.sin(2 * np.pi * 55 * t) * np.exp(-t / 0.09) * 0.8
    whine = np.sin(2 * np.pi * (7800 - 1500 * t) * t) * np.exp(-t / 0.35) * 0.06
    hiss = _f(rng.standard_normal(n), 'band', [1200, 8000], sr) * np.exp(-t / 0.05) * 0.35
    return np.tanh((zap + thump + whine + hiss) * 1.3) * 0.75

def pop(sr):
    n = int(0.16 * sr); t = np.arange(n) / sr
    f = 280 + 900 * t / 0.16
    return np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t / 0.05) * 0.28

def track(n, sr, lines, t_slam, inserts=()):
    out = np.zeros((n, 2), np.float32)
    def put(t, x, pan=0.0):
        a = int(t * sr); b = min(n, a + len(x))
        if a < n: out[a:b, 0] += x[:b - a] * (1 - pan); out[a:b, 1] += x[:b - a] * (1 + pan)
    put(lines[2]['start'] - 0.12, static(sr))                     # corte para a TV
    put(lines[4]['start'] - 0.08, static(sr, 0.22) * 0.6)
    put(lines[5]['start'] + lines[5]['dur'] * 0.55, shuffle(sr), 0.2)   # "embaralha"
    put(t_slam - 0.16, click(sr), -0.3)                             # controle remoto
    put(t_slam, crt_off(sr))                                        # TV de tubo desligando
    for t in inserts: put(t, pop(sr), 0.25)
    return out
