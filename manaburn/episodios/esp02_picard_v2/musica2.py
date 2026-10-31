"""Trilha original do especial Picard v2 (sintetizada aqui; sem amostras, sem tema de Star Trek).
Ré maior, 96 BPM: cordas em colcheias, metais suaves (serra filtrada), piano brilhante e um motivo próprio
em graus conjuntos (Ré-Mi-Fá#-Lá / Si-Lá-Fá#), sem os saltos de oitava das fanfarras da franquia.
Marcas vindas da montagem: pausa seca no banimento, crescendo nas "sete temporadas", calma no Sir Patrick,
acorde final no "Engage".
"""
import numpy as np
from scipy.signal import lfilter

def hz(n): return 440.0 * 2 ** ((n - 69) / 12)
def lp(x, sr, fc):
    a = np.exp(-2 * np.pi * fc / sr); return lfilter([1 - a], [1, -a], x, axis=0)

def nota_piano(f, dur, sr, v):
    t = np.arange(int(dur * sr)) / sr
    s = (np.sin(2*np.pi*f*t) + .5*np.sin(4*np.pi*f*t)*np.exp(-t*3) + .2*np.sin(6.02*np.pi*f*t)*np.exp(-t*5))
    return s * np.exp(-t * (1.2 + f / 1200)) * np.clip(t / .004, 0, 1) * v

def serra(f, t, n=8):
    ph = 2 * np.pi * f * t
    return sum(np.sin(h * ph) / h for h in range(1, n + 1))

def metais(fs, dur, sr, v):   # metais suaves: serra com filtro que abre no ataque
    t = np.arange(int(dur * sr)) / sr
    s = sum(serra(f * (1 + d), t) for f in fs for d in (-.003, .003)) / (2 * len(fs))
    env = np.clip(t / .18, 0, 1) * np.clip((dur - t) / .35, 0, 1)
    return lp(s, sr, 2200) * env * v

def cordas_colcheias(fs, dur, sr, v, bpm):   # ostinato de cordas em colcheias
    t = np.arange(int(dur * sr)) / sr; step = 60 / bpm / 2
    out = np.zeros_like(t); k = 0; t0 = 0
    while t0 < dur:
        f = fs[k % len(fs)]; i0 = int(t0 * sr); i1 = min(len(t), i0 + int(step * sr))
        tt = t[: i1 - i0]; out[i0:i1] += serra(f, tt, 6) * np.clip(tt / .01, 0, 1) * np.exp(-tt * 4)
        t0 += step; k += 1
    return lp(out, sr, 3200) * v

def tambor(sr, v, f0=70):     # tímpano suave
    t = np.arange(int(1.2 * sr)) / sr
    return np.sin(2*np.pi*np.cumsum(f0*(1+.6*np.exp(-t*12)))/sr) * np.exp(-t*3.2) * v

PROG = [  # (baixo, acorde) por compasso
    (38, [62, 66, 69]), (35, [59, 62, 66]), (43, [59, 62, 67]), (45, [61, 64, 69]),
    (38, [62, 66, 69]), (42, [61, 66, 69]), (43, [59, 62, 67]), (45, [61, 64, 69]),
]
MOTIVO = [(0, 74), (.5, 76), (1, 78), (1.5, 81), (2.5, 83), (3, 81), (3.5, 78)]   # em tempos (semínimas)

def trilha(T, marcas, sr=44100, bpm=96, seed=3):
    """marcas: dict com t_ban, t_ban_fim, t_swell, t_calma, t_calma_fim, t_engage"""
    rng = np.random.default_rng(seed); n = int(T * sr); out = np.zeros((n, 2)); tt = np.arange(n) / sr
    beat = 60 / bpm; bar = 4 * beat
    m = marcas
    inten = np.interp(tt, [0, 2, m['t_ban'] - .5, m['t_ban'], m['t_ban_fim'], m['t_swell'], m['t_swell'] + 3, m['t_calma'], m['t_calma_fim'], m['t_engage'], T],
                          [.55, .8, .8, .15, .15, .9, 1.0, .5, .5, .6, 1.0])
    k = 0; t0 = 0.0
    while t0 < m['t_engage'] - .2:
        b, ac = PROG[k % len(PROG)]; dur = min(bar, m['t_engage'] - t0)
        i0 = int(t0 * sr); i1 = min(n, i0 + int((dur + .4) * sr)); L = i1 - i0
        if L <= 0: break
        cz = cordas_colcheias([hz(x) for x in (ac[0], ac[2], ac[1] + 12, ac[2])], L / sr, sr, .16, bpm)[:L]
        mt = metais([hz(x - 12) for x in ac], L / sr, sr, .12)[:L]
        bx = nota_piano(hz(b), L / sr, sr, .22)[:L]
        g = inten[i0:i1]
        out[i0:i1, 0] += (cz * .7 + mt * .5 + bx * .5) * g
        out[i0:i1, 1] += (cz * .5 + mt * .5 + bx * .5) * g
        if k % 2 == 0:   # motivo no piano a cada dois compassos
            for bt, nn in MOTIVO:
                ts = t0 + bt * beat
                if ts > m['t_engage'] - .3 or m['t_ban'] - .3 < ts < m['t_ban_fim']: continue
                p = nota_piano(hz(nn), 1.6, sr, .13); a = int(ts * sr); e = min(n, a + len(p))
                pan = .45 + .1 * rng.random(); out[a:e, 0] += p[:e-a] * (1 - pan) * inten[a:e]; out[a:e, 1] += p[:e-a] * pan * inten[a:e]
        t0 += bar; k += 1
    # tímpanos: entrada do crescendo e o "Engage"
    for ts, v in ((m['t_swell'], .35), (m['t_engage'], .55)):
        d = tambor(sr, v); a = int(ts * sr); e = min(n, a + len(d)); out[a:e] += d[:e-a, None]
    # acorde final em Ré, aberto e brilhante, sobre o "Engage"
    a = int(m['t_engage'] * sr); d = T - m['t_engage']
    if d > .5:
        fin = metais([hz(x) for x in (50, 57, 62, 66, 69, 74)], d, sr, .22) + cordas_colcheias([hz(x) for x in (74, 78, 81, 86)], d, sr, .10, bpm * 2)
        for j, nn in enumerate((74, 78, 81, 86)):
            p = nota_piano(hz(nn), min(d, 3), sr, .14); i0 = a + int(j * .09 * sr); e = min(n, i0 + len(p)); fin[i0-a:e-a] += p[:e-i0]
        out[a:a + len(fin)] += fin[: n - a, None] * np.clip((T - tt[a:a+len(fin)]) / 1.2, 0, 1)[:, None]
    out = lp(out, sr, 7000)
    out *= (np.clip(tt / .3, 0, 1) * np.clip((T - tt) / .6, 0, 1))[:, None]
    return out / (np.max(np.abs(out)) + 1e-9) * .9
