"""Conde Ep. 004 · encurta a narração bruta (ElevenLabs) com pausas-alvo e tempo, sem cortar frases.
Copiado de encurtar_narracao_ep003.py. Take de 66,5 s, 1 geração.
pausas-alvo em tempo FINAL, pausa pode ser maior do que a original (preenche com silêncio), tempos por palavra
encostados aos silêncios reais (o alinhamento do Scribe acolchoa o fim das frases).
Uso (na pasta conde/ep004/audio): python3 ../../encurtar_narracao_ep004.py
Entradas: narracao_raw.mp3, words_raw.json  ·  Saídas: narracao.wav, words_novo.json
"""
import json, re, subprocess
import numpy as np

SRC, SR, TEMPO = "narracao_raw.mp3", 48000, 1.15

CORTES = []    # nenhuma frase cortada
# pausa (tempo final, s) antes da palavra indicada; o resto usa PAUSA_BASE
PAUSA_BASE = 0.20
PAUSA_ANTES = {"Jóven.@4.6": 0.34, "Observem": 0.40, "Os@7.9": 0.24, "A@11.1": 0.30, "A@17.7": 0.45, "E@23.9": 0.45,
               "Afinal,": 0.30, "Os@30.1": 0.40, "Três": 0.42, "e@36.8": 0.45, "No": 0.42, "Mas": 0.32,
               "Uma@49.8": 0.55, "Parecer:": 0.42, "Um@57": 0.30, "Qual": 0.45}
# grafia real nas legendas (o TTS recebeu grafia fonética)
GRAFIA = {"Jóven.": "Joven.", "Jóven": "Joven", "Tchândler": "Chandler", "Éron": "Eron"}

log = subprocess.run(["ffmpeg", "-hide_banner", "-i", SRC, "-af", "silencedetect=noise=-40dB:d=0.12", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
sil = list(zip([float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)],
               [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]))
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", SRC, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
x = np.frombuffer(raw, np.float32)
dur = len(x) / SR

ilhas, c = [], 0.0
for a, b in sil:
    ilhas.append((c, a)); c = b
ilhas.append((c, dur))
ilhas = [(a, b) for a, b in ilhas if b - a > 0.01 and not any(a >= p - 0.03 and b <= q + 0.03 for p, q in CORTES)]

# palavras (sem tags), encostadas aos silêncios
W = []
for w in json.load(open("words_raw.json"))["words"]:
    t = w["text"]
    if w.get("type") != "word" or t.startswith("[") or t.endswith("]") or w["end"] < 0.08:
        continue
    a, b = w["start"], w["end"]
    for s0, s1 in sil:
        if s0 < a < s1: a = s1
        if s0 < b < s1 or (a < s0 < b): b = min(b, s0)
    W.append([t, a, max(b, a + 0.05)])
W = [w for w in W if any(i0 - 0.05 <= w[1] < i1 for i0, i1 in ilhas)]
# a primeira palavra de cada ilha começa onde o som começa (o alinhador atrasa-a até ~0,25 s)
for i0, i1 in ilhas:
    dentro = [w for w in W if i0 - 0.05 <= w[1] < i1]
    if dentro and dentro[0][1] - i0 < 0.4:
        dentro[0][1] = i0

def pausa_antes(w):
    for k, v in PAUSA_ANTES.items():
        nome, _, quando = k.partition("@")
        if w[0] == nome and (not quando or abs(w[1] - float(quando)) < 1.2):
            return v
    return PAUSA_BASE

# montar: ilha + pausa (em tempo bruto = alvo final × TEMPO)
out, mapa, cur = [], [], 0.0
for i, (a, b) in enumerate(ilhas):
    if i:
        primeira = next((w for w in W if a - 0.05 <= w[1] < b), None)
        p = (pausa_antes(primeira) if primeira else PAUSA_BASE) * TEMPO
        out.append(np.zeros(int(p * SR), np.float32)); cur += p
    seg = x[int(a * SR):int(b * SR)].copy()
    f = min(len(seg) // 4, int(0.008 * SR))
    if f:
        seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    out.append(seg); mapa.append((a, b, cur)); cur += b - a

def remap(t):
    for a, b, o in mapa:
        if a - 0.06 <= t <= b + 0.06:
            return (o + min(max(t - a, 0), b - a)) / TEMPO
    raise ValueError(t)

y = np.concatenate(out)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                "-af", f"atempo={TEMPO},loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), "narracao.wav"],
               input=y.tobytes(), check=True)

# legendas: grafia real
novo, i = [], 0
while i < len(W):
    t, a, b = W[i]
    if novo and novo[-1][0][-1] in ".?!" and not novo[-1][0].endswith("...") and t != "e":
        t = t[0].upper() + t[1:]
    novo.append([GRAFIA.get(t, t), remap(a), remap(b)]); i += 1
json.dump([[w, round(a, 3), round(b, 3)] for w, a, b in novo], open("words_novo.json", "w"), ensure_ascii=False)
print("duração nova:", round(len(y) / SR / TEMPO, 2), "palavras:", len(novo))
