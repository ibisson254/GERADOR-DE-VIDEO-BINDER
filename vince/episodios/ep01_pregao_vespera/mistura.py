#!/usr/bin/env python3
"""VV-EP01 — áudio: monta a voz no relógio do vídeo, a Fonte, efeitos e a faixa; normaliza a −14 LUFS.

Uso:
  python3 mistura.py voz   --assets <pasta> --fonte <vince/audio/saida>          -> voz_video.wav + env_voz.npy
  python3 mistura.py final --assets <pasta> --fonte <...> --musica <mp3> --video <mudo.mp4> --fecho <outro.mp4> --saida <final.mp4>
"""
import argparse, subprocess, sys
from pathlib import Path
import numpy as np
import soundfile as sf
import librosa

sys.path.insert(0, str(Path(__file__).parent))
from render import FRASES, DUR, TOQUE  # noqa: E402

SR = 48000
JANELA_MUSICA = 59.221        # início do trecho: a bateria pára (69,52 s da faixa) quando o telefone toca
PARA_BATERIA = 10.30          # o telefone toca; a bateria pára
VOLTA_BATERIA = 12.233
FIM_CHAMADA = 17.60
FECHO = 116 / 30           # outro_binder_916.mp4 não tem áudio: a trilha sobe por baixo dele
TOTAL = DUR + FECHO

def carrega(p, sr=SR):
    y, _ = librosa.load(str(p), sr=sr, mono=True)
    return y

def poe(trilha, y, t, ganho=1.0):
    i = int(t * SR)
    j = min(len(trilha), i + len(y))
    trilha[i:j] += y[: j - i] * ganho

def faixa_voz(assets):
    voz = carrega(Path(assets) / "voz.mp3")
    tr = np.zeros(int(DUR * SR))
    for a, b, t0, _ in FRASES:
        seg = voz[int((a - 0.03) * SR): int((b + 0.06) * SR)].copy()
        f = int(0.008 * SR); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
        poe(tr, seg, t0 - 0.03)
    # "Buy the d—" é cortado pelo toque
    i = int((TOQUE - 0.03) * SR); r = int(0.03 * SR)
    tr[i:i + r] *= np.linspace(1, 0, r); tr[i + r: int((TOQUE + 0.9) * SR)] = 0
    return tr

def efeitos(fonte):
    """Só o telefone e a Fonte (sons aprovados de vince/audio/fonte.py). Sem efeitos decorativos."""
    fonte = Path(fonte); tr = np.zeros(int(DUR * SR))
    toque = carrega(fonte / "telefone_toque.wav")[: int(0.62 * SR)].copy()
    toque[-int(0.05 * SR):] *= np.linspace(1, 0, int(0.05 * SR))
    poe(tr, toque, TOQUE, 0.9)
    poe(tr, carrega(fonte / "fonte_ma_noticia.wav"), 14.25, 0.9)
    poe(tr, carrega(fonte / "telefone_pousa.wav"), 17.30, 1.0)
    return tr

def musica(mp3):
    y = carrega(mp3)
    m = y[int(JANELA_MUSICA * SR): int((JANELA_MUSICA + TOTAL) * SR)].copy()
    m = np.pad(m, (0, max(0, int(TOTAL * SR) - len(m))))
    f = int(1.6 * SR); m[-f:] *= np.linspace(1, 0, f) ** 2
    return m

def lufs(y):
    import pyloudnorm as pyln
    return pyln.Meter(SR).integrated_loudness(y)

def ganho_para(y, alvo):
    return 10 ** ((alvo - lufs(y)) / 20)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("modo"); ap.add_argument("--assets", required=True); ap.add_argument("--fonte", required=True)
    ap.add_argument("--musica"); ap.add_argument("--video"); ap.add_argument("--fecho"); ap.add_argument("--saida")
    a = ap.parse_args()
    voz = faixa_voz(a.assets)
    if a.modo == "voz":
        sf.write(Path(a.assets) / "voz_video.wav", voz, SR)
        hop = SR // 100
        rms = np.array([np.sqrt(np.mean(voz[i:i + hop] ** 2)) for i in range(0, len(voz), hop)])
        rms = np.convolve(rms, np.ones(3) / 3, "same"); rms /= np.percentile(rms[rms > 0], 95)
        np.save(Path(a.assets) / "env_voz.npy", np.clip(rms, 0, 1.5))
        print("voz ok", round(lufs(voz), 1), "LUFS")
        return
    v = voz * ganho_para(voz, -16.0)
    m = musica(a.musica)
    m *= ganho_para(m, -20.0)
    # ducking extra durante o telefonema (bateria parada + conversa)
    duck = np.ones_like(m)
    i0, i1 = int(PARA_BATERIA * SR), int(FIM_CHAMADA * SR)
    duck[i0:i1] = 0.35
    r = int(0.15 * SR); duck[i1:i1 + r] = np.linspace(0.35, 1, r)
    # no fecho a música sobe (sem narração por cima)
    sobe = np.ones_like(m); i = int((DUR - 0.3) * SR); r = int(0.3 * SR)
    sobe[i:i + r] = np.linspace(1, 1.8, r); sobe[i + r:] = 1.8
    fx = efeitos(a.fonte)
    pad = lambda x: np.pad(x, (0, len(m) - len(x)))
    mix = pad(v) + m * duck * sobe + pad(fx) * ganho_para(v, -16.0) * 0.9
    mix *= ganho_para(mix, -14.0)
    pico = np.max(np.abs(mix))
    if pico > 0.97:
        mix = np.tanh(mix / pico * 1.4) / np.tanh(1.4) * 0.97
        mix *= ganho_para(mix, -14.0)
        mix = np.clip(mix, -0.99, 0.99)
    corpo = Path(a.saida).with_suffix(".corpo.wav")
    sf.write(corpo, mix, SR)
    print("mistura", round(lufs(mix), 2), "LUFS, pico", round(float(np.max(np.abs(mix))), 3))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", a.video, "-i", a.fecho, "-i", str(corpo), "-filter_complex",
                    "[0:v]fps=30,format=yuv420p,setsar=1[v0];[1:v]fps=30,scale=1080:1920,format=yuv420p,setsar=1[v1];"
                    "[v0][v1]concat=n=2:v=1:a=0[v]",
                    "-map", "[v]", "-map", "2:a", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-shortest", a.saida], check=True)
    print("final", a.saida)

if __name__ == "__main__":
    main()
