"""Efeitos sonoros sintetizados (sem amostras de terceiros): estática de TV, cartas embaralhando,
clique do controle remoto, TV de tubo desligando e troca de canal (zapping)."""
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

def marker(sr, dur=0.26):
    """Marca-texto passando no papel: atrito filtrado com a ressonância subindo (on_oracle_highlight)."""
    n = int(dur * sr); t = np.arange(n) / sr
    x = rng.standard_normal(n) * (0.7 + 0.3 * np.sin(2 * np.pi * 38 * t))          # o atrito da ponta
    lo = _f(x, 'band', [1700, 2600], sr, 3); hi = _f(x, 'band', [2600, 3800], sr, 3)
    mix = lo * (1 - t / dur) + hi * (t / dur)                                       # o tom sobe com o traço
    env = np.minimum(1, t / 0.02) * np.minimum(1, (dur - t) / 0.05)
    return mix * env * 0.42

def flick(sr):
    """Estalo de carta de Magic (on_secondary_card_pop): o peteleco, o corpo do papel e o ar."""
    n = int(0.12 * sr); t = np.arange(n) / sr; out = np.zeros(n)
    m = int(0.002 * sr); out[:m] += _f(rng.standard_normal(m), 'high', 3000, sr) * 0.55
    out += _f(rng.standard_normal(n), 'band', [1400, 6500], sr) * np.exp(-t / 0.012) * 0.8
    out += _f(rng.standard_normal(n), 'low', 900, sr) * np.exp(-((t - 0.03) / 0.025) ** 2) * 0.25
    return out * 0.42

def thump(sr):
    """Impacto curto e grave para a indignação do Burn (on_rage_arms_up)."""
    n = int(0.22 * sr); t = np.arange(n) / sr
    f = 46 + 40 * np.exp(-t / 0.03)
    body = np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t / 0.08)
    knock = _f(rng.standard_normal(n), 'band', [200, 1600], sr) * np.exp(-t / 0.01) * 0.6
    return np.tanh((body + knock) * 1.4) * 0.3

def zap(sr, dur=0.30, forte=True):
    """Troca de canal numa TV de tubo: o clique do controle, o \"tum\" do relé e um chiado curto que some."""
    n = int(dur * sr); t = np.arange(n) / sr
    hiss = _f(rng.standard_normal(n), 'band', [700, 9000], sr) * np.where(t < dur * 0.75, 1, np.exp(-(t - dur * 0.75) / 0.02)) * 0.30
    hum = np.sin(2 * np.pi * 15734 / 4 * t) * 0.025 * (t < dur * 0.6)                 # o zumbido agudo do tubo
    relay = np.sin(2 * np.pi * 120 * t) * np.exp(-t / 0.025) * 0.35
    out = hiss + hum + relay
    c = click(sr); out[:len(c)] += c * 0.9
    return out * (1.0 if forte else 0.45)

def track(n, sr, lines, t_slam, inserts=(), tv_cuts=(), shuffle_at=None, destaques=(), raiva=(), carta='pop', tv=True,
          zaps=(), zaps_leves=()):
    """Camada de efeitos. Os eventos chegam com os horários do process.py (os mesmos que vão para o data.js)."""
    out = np.zeros((n, 2), np.float32)
    def put(t, x, pan=0.0):
        a = int(t * sr); b = min(n, a + len(x))
        if 0 <= a < n: out[a:b, 0] += x[:b - a] * (1 - pan); out[a:b, 1] += x[:b - a] * (1 + pan)
    if tv:
        for k, t in enumerate(tv_cuts):                              # on_tv_cut: estática no corte para a TV
            put(max(0, t - 0.12), static(sr) * (1 if k == 0 else 0.6))
    for t in zaps: put(max(0, t - 0.02), zap(sr), -0.1)              # troca de canal
    for t in zaps_leves: put(max(0, t - 0.01), zap(sr, 0.11, False), -0.1)   # zapping rápido da abertura
    if shuffle_at is not None: put(shuffle_at, shuffle(sr), 0.2)     # cartas embaralhando
    put(t_slam - 0.16, click(sr), -0.3)                              # controle remoto
    put(t_slam, crt_off(sr))                                         # TV de tubo desligando
    for t in inserts: put(t, flick(sr) if carta == 'flick' else pop(sr), 0.25)   # on_secondary_card_pop
    for t in destaques: put(t, marker(sr), 0.1)                      # on_oracle_highlight
    for t in raiva: put(t, thump(sr), 0.15)                          # on_rage_arms_up
    return out
