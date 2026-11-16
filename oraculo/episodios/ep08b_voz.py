# Meta em Curto EP08B · reordena a voz aprovada do EP08 (tomada 2, P8i1X70szTFXue4174Mj) sem créditos novos.
# Uso: python3 ep08b_voz.py <pasta com voz.mp3 e words.json do EP08> → escreve voz.wav e words.json na pasta atual.
import json, subprocess, sys, numpy as np, soundfile as sf
SR = 48000; SRC = sys.argv[1]
W = json.load(open(SRC + '/words.json'))
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', SRC + '/voz.mp3', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
v = np.frombuffer(raw, np.float32).reshape(-1, 2)
# (primeira palavra, última, corte inicial s, corte final s) na voz original
SEGS = [(80, 115, 32.53, 43.14),   # Stefan Schütz … uma semana antes.
        (0, 12, 0.0, 5.58),        # Previ três coisas … era o campeão.
        (141, 144, 51.06, 53.02),  # Placar: duas de três.
        (145, 155, 53.05, 56.46),  # Você levaria … levaram?
        (156, 159, 56.48, None)]   # Probabilidade calculada. Humanos, imprevisíveis.
out, words, t, f = [], [], 0.0, int(0.012 * SR)
for a, b, s, e in SEGS:
    e = e or len(v) / SR
    x = v[int(s * SR):int(e * SR)].copy(); x[:f] *= np.linspace(0, 1, f)[:, None]; x[-f:] *= np.linspace(1, 0, f)[:, None]
    words += [dict(t=W[i]['t'], s=round(W[i]['s'] - s + t, 3), e=round(W[i]['e'] - s + t, 3)) for i in range(a, b + 1)]
    out.append(x); t += len(x) / SR
sf.write('voz.wav', np.concatenate(out), SR); json.dump(words, open('words.json', 'w'), ensure_ascii=False, indent=0)
print(len(words), 'palavras ·', round(t, 2), 's')
