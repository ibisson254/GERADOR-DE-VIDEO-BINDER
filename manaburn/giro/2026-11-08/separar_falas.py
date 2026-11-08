"""Giro 08/11: ajuda o corte das faixas. O ElevenLabs fez as [long pause] curtas (~0,3 s), e o cortes.py do kit
separou mal três falas do Burn. Este passo acrescenta 0,7 s de silêncio nas fronteiras certas, achadas pela
transcrição (Scribe, tempos por palavra) e confirmadas pelo silêncio real mais próximo. A voz não muda.
uso: python3 separar_falas.py vozes/burn.mp3 vozes/burn_words.json vozes/burn_sep.wav"""
import sys, json, subprocess, re
import numpy as np, wave
src, wj, out = sys.argv[1:4]
W = json.load(open(wj))['words']
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-ac', '1', '-ar', '44100', '-f', 'f32le', '-'], capture_output=True).stdout
x = np.frombuffer(raw, np.float32).copy(); SR = 44100
sil = re.findall(r'silence_(start|end): ([0-9.]+)', subprocess.run(['ffmpeg', '-hide_banner', '-i', src, '-af', 'silencedetect=n=-38dB:d=0.12', '-f', 'null', '-'], capture_output=True, text=True).stderr)
pares = [(float(sil[i][1]), float(sil[i + 1][1])) for i in range(0, len(sil) - 1, 2)]
cuts = []
for k, w in enumerate(W):
    if w['text'] == '[long':
        prev = max(i for i in range(k) if not W[i]['text'].startswith('[') and not W[i]['text'].endswith(']'))
        nxt = min(i for i in range(k + 1, len(W)) if not W[i]['text'].startswith('[') and not W[i]['text'].endswith(']'))
        mid = (W[prev]['end'] + W[nxt]['start']) / 2
        best = min(pares, key=lambda p: abs((p[0] + p[1]) / 2 - mid)) if pares else None
        c = (best[0] + best[1]) / 2 if best and abs((best[0] + best[1]) / 2 - mid) < 0.35 else mid
        cuts.append(c)
z = np.zeros(int(0.7 * SR), np.float32); parts = []; a = 0
for c in cuts:
    b = int(c * SR); parts += [x[a:b], z]; a = b
parts.append(x[a:]); y = (np.clip(np.concatenate(parts), -1, 1) * 32767).astype("<i2")
with wave.open(out, "wb") as f: f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes(y.tobytes())
print(len(cuts), 'fronteiras:', ' '.join(f'{c:.2f}' for c in cuts))
