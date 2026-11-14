"""Sound design do Pregão Magic · Brutal Bass Edition (sintetizado localmente, custo zero).

Gera stems a 48 kHz estéreo:
  stems/musica.wav  (faixa original, só ganho e almofada até ao fim do fecho)
  stems/efeitos.wav (foley de cartas, impactos curtos, transições direcionais, acentos)
  stems/voz.wav     (silêncio até haver narração autorizada; se existir voz.wav, entra com ducking)
  mix.wav           (mistura final, −14 LUFS, pico verdadeiro −1,5 dBTP via ffmpeg)
Uso: python3 som.py MUSICA.mp3 PASTA_SAIDA [voz.wav]
"""
import sys, subprocess, pathlib
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 48000
DUR = 1352 / 30  # 41,2 s de episódio + 3,87 s de fecho
rng = np.random.default_rng(46)


def bp(x, lo, hi, o=4):
    return sosfilt(butter(o, [lo, hi], "band", fs=SR, output="sos"), x)


def lp(x, f, o=4):
    return sosfilt(butter(o, f, "low", fs=SR, output="sos"), x)


def hp(x, f, o=4):
    return sosfilt(butter(o, f, "high", fs=SR, output="sos"), x)


def env(n, a, d, curva=4.0):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-curva * np.maximum(0, t - a) / max(d, 1e-4))
    return e


class Pista:
    def __init__(s):
        s.L = np.zeros(int(DUR * SR) + SR); s.R = np.zeros_like(s.L)

    def add(s, t, sinal, ganho_db=0.0, pan=0.0):
        i = int(t * SR); g = 10 ** (ganho_db / 20)
        if np.ndim(pan) == 0:
            pl, pr = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        else:
            pl, pr = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        n = min(len(sinal), len(s.L) - i)
        s.L[i:i + n] += sinal[:n] * g * (pl[:n] if np.ndim(pl) else pl)
        s.R[i:i + n] += sinal[:n] * g * (pr[:n] if np.ndim(pr) else pr)


# ---------- biblioteca de sons ----------
def carta_flick():  # foley: canto da carta a raspar e estalar
    n = int(0.07 * SR); x = rng.standard_normal(n)
    return bp(x, 1800, 9000) * env(n, 0.002, 0.018, 5) * 0.9


def carta_pousa():  # carta assenta na mesa
    n = int(0.12 * SR); x = rng.standard_normal(n)
    corpo = lp(x, 900) * env(n, 0.001, 0.03, 5)
    estalo = bp(x, 3000, 10000) * env(n, 0.0005, 0.006, 5) * 0.5
    return (corpo + estalo) * 0.9


def baralhar(dur=0.45, densidade=34):
    n = int(dur * SR); out = np.zeros(n)
    for k in range(int(dur * densidade)):
        i = int(rng.uniform(0, dur - 0.07) * SR); f = carta_flick() * rng.uniform(0.3, 0.8)
        out[i:i + len(f)] += f[:n - i]
    return out * np.linspace(0.6, 1, n)


def whoosh(dur=0.5, lo=300, hi=4000, sobe=True):
    n = int(dur * SR); x = rng.standard_normal(n)
    # varrimento de banda por blocos
    out = np.zeros(n); blocos = 24
    for b in range(blocos):
        a, z = b * n // blocos, (b + 1) * n // blocos
        f = lo + (hi - lo) * (b / blocos if sobe else 1 - b / blocos)
        out[a:z] = bp(x, max(60, f * 0.6), min(20000, f * 1.6), 2)[a:z]
    forma = np.sin(np.linspace(0, np.pi, n)) ** 2
    return out * forma * 0.8


def impacto(grave=48, dur=0.45):  # impacto cinematográfico curto: sub + transiente
    n = int(dur * SR); t = np.arange(n) / SR
    f = grave * (1 + 1.5 * np.exp(-t * 30))
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, dur * 0.5, 4)
    tr = bp(rng.standard_normal(n), 900, 7000) * env(n, 0.0005, 0.02, 5) * 0.35
    return np.tanh((sub + tr) * 1.6) * 0.8


def blip(notas, dur=0.09, gap=0.07):  # micro-recompensa: duas notas curtas e limpas
    out = np.zeros(int((len(notas) * gap + dur) * SR))
    for k, hz in enumerate(notas):
        n = int(dur * SR); t = np.arange(n) / SR
        s = (np.sin(2 * np.pi * hz * t) + 0.25 * np.sin(4 * np.pi * hz * t)) * env(n, 0.003, 0.05, 5)
        i = int(k * gap * SR); out[i:i + n] += s
    return out * 0.5


def tique(hz=2400):  # textura mecânica refinada
    n = int(0.03 * SR); t = np.arange(n) / SR
    return (bp(rng.standard_normal(n), hz * 0.7, hz * 1.6) * 0.6 + np.sin(2 * np.pi * hz * 0.5 * t) * 0.3) * env(n, 0.0005, 0.006, 5)


def placa():  # painel de cotações a virar (clack)
    n = int(0.09 * SR); x = rng.standard_normal(n)
    return (lp(x, 2500) * env(n, 0.0007, 0.012, 5) + bp(x, 2500, 8000) * env(n, 0.0004, 0.004, 5) * 0.6) * 0.9


def glide(f0, f1, dur, vol=0.2):
    n = int(dur * SR); f = np.geomspace(f0, f1, n)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.linspace(0, np.pi, n)) ** 1.5 * vol


def textura_grave(dur, f=55):  # cama grave discreta para a tensão
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) * 0.5 + lp(rng.standard_normal(n), 140) * 0.8
    return s * np.linspace(0, 1, n) ** 2 * 0.35


def ping():  # radar: uma nota limpa no silêncio
    n = int(0.9 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * 1318.5 * t) * env(n, 0.002, 0.45, 4) * 0.28


def construir():
    P = Pista()
    # ABERTURA: parede de cartas e a carta que atravessa
    P.add(0.00, baralhar(0.5), -20, 0.0)
    P.add(1.02, whoosh(0.52, 400, 6000), -14, np.linspace(-0.9, 0.2, int(0.52 * SR)))
    P.add(1.52, carta_pousa(), -12, 0.0)
    # match cut: moldura vira gráfico
    for k, t in enumerate([2.09, 2.27, 2.45]):
        P.add(t, tique(2000 + 400 * k), -22, -0.3 + 0.3 * k)
    P.add(2.35, glide(320, 980, 0.78, 0.18), -18, 0.3)
    P.add(3.16, impacto(46), -10); P.add(3.18, blip([1318.5, 1975.5]), -13)
    P.add(4.13, whoosh(0.32, 2000, 300, sobe=False), -17)
    P.add(4.62, carta_pousa(), -13)
    # ALTAS
    P.add(7.00, whoosh(0.35, 600, 2500), -21, np.linspace(0.4, -0.5, int(0.35 * SR)))
    for t in (8.31, 9.11, 9.91):
        P.add(t, tique(3000), -25)
    P.add(11.54, textura_grave(2.06), -14)
    for k in range(4):
        P.add(11.70 + k * 0.534, tique(1800), -24)
    P.add(13.72, impacto(42, 0.55), -11); P.add(13.76, blip([1318.5, 1975.5]), -13)
    P.add(16.25, whoosh(0.3, 800, 3000), -22, -0.4)
    # VIRADA e QUEDAS
    P.add(18.81, whoosh(0.4, 500, 3500), -19, 0.0)
    P.add(19.34, glide(900, 220, 0.96, 0.2), -18)
    P.add(20.30, whoosh(0.33, 3000, 200, sobe=False), -16)
    P.add(20.86, impacto(40, 0.5), -10); P.add(20.88, carta_pousa(), -12); P.add(20.92, blip([987.8, 659.3]), -13)
    P.add(23.10, whoosh(0.3, 800, 3000), -22, 0.4)
    # PAUSA: silêncio intencional, só o ping do radar
    P.add(26.80, ping(), -14)
    # RADAR
    P.add(27.487, impacto(44, 0.5), -11)
    P.add(27.60, blip([987.8, 659.3]), -15, -0.6); P.add(27.72, blip([1318.5, 1975.5]), -15, 0.6)
    P.add(30.07, baralhar(0.4, 28), -19)
    P.add(31.67, tique(2600), -22, -0.3); P.add(31.85, tique(2600), -22, 0.3)
    # FECHAMENTO: uma placa por linha
    for t in (34.348, 34.90, 35.43, 36.055, 36.60):
        P.add(t, placa(), -13, 0.2)
    P.add(37.773, impacto(50, 0.35), -15)
    P.add(39.49, blip([1318.5, 1760.0, 1975.5], 0.12, 0.09), -18)
    return P


def medir_lufs(f):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(f), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    linha = [l for l in r.split("Summary:")[-1].splitlines() if l.strip().startswith("I:")][0]
    return float(linha.split()[1])


def main():
    mus, out = sys.argv[1], pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    st = out / "stems"; st.mkdir(exist_ok=True)
    tmp = out / "_musica48k.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mus, "-ar", str(SR), "-ac", "2", str(tmp)], check=True)
    sr, m = wavfile.read(tmp); m = m.astype(np.float64) / 32768.0
    n = int(DUR * SR)
    M = np.zeros((n, 2)); M[:min(n, len(m))] = m[:n]
    M *= 10 ** (-2.0 / 20)  # a música manda; −2 dB abre espaço aos efeitos sem lhe tirar impacto
    P = construir()
    E = np.stack([P.L[:n], P.R[:n]], 1)
    V = np.zeros_like(M)
    if len(sys.argv) > 3:
        sv, v = wavfile.read(sys.argv[3]); v = v.astype(np.float64) / 32768.0
        if v.ndim == 1: v = np.stack([v, v], 1)
        V[:min(n, len(v))] = v[:n]
        # ducking: música −7 dB onde há voz (envolvente suavizada 120 ms)
        lvl = np.abs(V).max(1); k = int(0.12 * SR)
        envv = np.convolve(lvl > 0.01, np.ones(k) / k, "same")
        M *= (1 - envv * (1 - 10 ** (-7 / 20)))[:, None]
    for nome, x in (("musica", M), ("efeitos", E), ("voz", V)):
        wavfile.write(st / f"{nome}.wav", SR, (np.clip(x, -1, 1) * 32767).astype(np.int16))
    mix = M + E + V
    bruto = out / "_mix_bruto.wav"
    wavfile.write(bruto, SR, np.clip(mix, -1, 1).astype(np.float32))
    ganho = -14.0 - medir_lufs(bruto)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(bruto), "-af",
                    f"volume={ganho:.2f}dB,alimiter=limit=0.84:attack=2:release=60:level=false",
                    "-ar", str(SR), "-c:a", "pcm_s16le", str(out / "mix.wav")], check=True)
    tmp.unlink(); bruto.unlink()
    print("ok", out / "mix.wav")


if __name__ == "__main__":
    main()
