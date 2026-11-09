"""Conde Ep. 005 · encurta a narração bruta (ElevenLabs) com pausas-alvo e tempo, sem cortar frases.
Copiado de encurtar_narracao_ep004.py (+ fusão de palavras: números e "Ice Age"). Take de 86,0 s, 1 geração.
pausas-alvo em tempo FINAL, pausa pode ser maior do que a original (preenche com silêncio), tempos por palavra
encostados aos silêncios reais (o alinhamento do Scribe acolchoa o fim das frases).
Uso (na pasta conde/ep005/audio): python3 ../../encurtar_narracao_ep005.py
Entradas: narracao_raw.mp3, words_raw.json  ·  Saídas: narracao.wav, words_novo.json
"""
import json, re, subprocess
import numpy as np

SRC, SR, TEMPO = "narracao_raw.mp3", 48000, 1.15

CORTES = []    # nenhuma frase cortada
# pausa (tempo final, s) antes da palavra indicada; o resto usa PAUSA_BASE
PAUSA_BASE = 0.20
PAUSA_ANTES = {"O@3.6": 0.36, "Observem": 0.42, "As@18.7": 0.30, "Raialópterus:": 0.26, "Nisso,": 0.26,
               "Agora,": 0.45, "Pelagem": 0.28, "Máscara": 0.28, "Garras": 0.28, "Senhores...": 0.55,
               "Em@41.7": 0.45, "Lêmiur,": 0.32, "Em@50.4": 0.45, "A@58.8": 0.36, "O@62.3": 0.45, "Até": 0.30,
               "Na": 0.42, "a@71.7": 0.58, "Parecer:": 0.45, "obra@76": 0.24, "A@77.4": 0.28, "O@78.9": 0.24,
               "A@80.3": 0.40, "Qual": 0.45}
# grafia real nas legendas (o TTS recebeu grafia fonética)
GRAFIA = {"Raialópterus": "Hyalopterous", "Raialópterus:": "Hyalopterous:", "Lêmiur.": "Lemure.", "Lêmiur,": "Lemure,",
          "Lêmiurs": "Lemures", "lí-mur,": "lemur,", '"é",': '"e",', "Rôuzuóter,": "Rosewater,", "Uízards,": "Wizards,"}
# várias palavras faladas = uma palavra na legenda
FUSOES = [(["mil", "novecentos", "e", "noventa", "e", "cinco."], "1995."),
          (["dois", "mil", "e", "três,"], "2003,"),
          (["Ais", "Eidj"], "Ice Age")]

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
    fus = next(((p, r) for p, r in FUSOES if [w[0] for w in W[i:i + len(p)]] == p), None)
    if fus:
        p, r = fus
        novo.append([r, remap(a), remap(W[i + len(p) - 1][2])]); i += len(p)
        continue
    if novo and novo[-1][0][-1] in ".?!" and not novo[-1][0].endswith("...") and t != "e":
        t = t[0].upper() + t[1:]
    novo.append([GRAFIA.get(t, t), remap(a), remap(b)]); i += 1
json.dump([[w, round(a, 3), round(b, 3)] for w, a, b in novo], open("words_novo.json", "w"), ensure_ascii=False)
print("duração nova:", round(len(y) / SR / TEMPO, 2), "palavras:", len(novo))
