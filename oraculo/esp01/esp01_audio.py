# Meta em Curto ESP01 · Precon em dupla · áudio (voz + trilha + SFX), derivado de ep07_audio.py
# Uso: numa pasta de trabalho com voz.mp3 (ElevenLabs) e words.json (tempos por palavra, Scribe, texto canónico):
#   python3 esp01_audio.py /caminho/do/kit
# Pausas inseridas na voz: 0,6 s depois de «três mil.» (ler o comentário), 0,4 s depois de «carta.» (conta),
# 1,0 s depois de «agradece.» (saída do tubo) e 1,2 s depois de «mesa.» (corte seco da trilha = assinatura da série).
import numpy as np, soundfile as sf, subprocess, json, sys
K = sys.argv[1] if len(sys.argv) > 1 else '../..'
SR = 48000; TEMPO = 1.10; LEAD = 0.15
W = json.load(open('words.json'))
PAUSES = [((W[45]['e'] + W[46]['s']) / 2, 0.60), ((W[90]['e'] + W[91]['s']) / 2, 0.40), ((W[106]['e'] + W[107]['s']) / 2, 1.00), ((W[115]['e'] + W[116]['s']) / 2, 1.20)]   # (tempo da voz original, s)
def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
def vt(x): return x / TEMPO + LEAD + sum(d for a, d in PAUSES if x >= a)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'voz.mp3', '-af',
                f'atempo={TEMPO},highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,loudnorm=I=-16:TP=-1.5:LRA=7',
                '-ar', str(SR), '-ac', '2', 'voz_proc.wav'], check=True)
voz = load('voz_proc.wav'); parts = []; prev = 0
for a, d in PAUSES:
    c = int(a / TEMPO * SR); parts += [voz[prev:c], np.zeros((int(d * SR), 2), np.float32)]; prev = c
parts.append(voz[prev:]); voz = np.concatenate(parts)
vend = LEAD + len(voz) / SR
OUT_START = round(vend + 0.25, 3); OUT_LEN = 3.87; TOTAL = OUT_START + OUT_LEN
N = int(TOTAL * SR)
V = np.zeros((N, 2), np.float32); a = int(LEAD * SR); V[a:a + len(voz)] = voz[:N - a]
# --- trilha: tema original até ao corte seco; silêncio; retoma no ponto que faz o tema acabar por baixo do fecho
REV0 = vt(W[115]['e']) + 0.02         # fim de «mesa.»
REV1 = REV0 + 1.20
T = load(K + '/oraculo/musica/tubo_tema_original.mp3'); TL_ = len(T) / SR
resume = max(0.0, TL_ - (TOTAL - REV1) - 0.3)
M = np.zeros((N, 2), np.float32)
i0 = int(REV0 * SR); n0 = min(i0, len(T)); M[:n0] = T[:n0]
seg = T[int(resume * SR):]; i1 = int(REV1 * SR); n = min(len(seg), N - i1); M[i1:i1 + n] = seg[:n]
t = np.arange(N) / SR
env = np.abs(V).mean(1); w = int(0.05 * SR); env = np.convolve(env, np.ones(w) / w, 'same')
speak = (env > 0.01).astype(float)
d = int(0.35 * SR); speak = np.convolve(speak, np.ones(d), 'same') > 0
s = int(0.25 * SR); speak = np.convolve(speak.astype(float), np.ones(s) / s, 'same')
g = 10 ** ((-6 + speak * (-12)) / 20)          # ducking ~12 dB sob a voz
c = np.ones(N); f = int(0.03 * SR); j0, j1 = int(REV0 * SR), int(REV1 * SR)
c[j0:j1] = 0; c[j0 - f:j0] = np.linspace(1, 0, f); c[j1:j1 + f] = np.linspace(0, 1, f)
g = np.where(t >= OUT_START - 0.3, 10 ** (-3 / 20), g)
fade = np.clip((TOTAL - t) / 1.2, 0, 1)
M = M * (g * c * fade)[:, None]
def thump(dur=0.7, f0=58):
    tt = np.arange(int(dur * SR)) / SR
    x = np.sin(2 * np.pi * f0 * tt * (1 - 0.25 * tt)) * np.exp(-tt * 6) * 0.9
    x += np.sin(2 * np.pi * 50 * tt) * np.exp(-tt * 3) * 0.12 * np.sign(np.sin(2 * np.pi * 100 * tt))
    cl = np.random.default_rng(1).normal(0, 1, len(tt)) * np.exp(-tt * 120) * 0.35
    return (x + cl).astype(np.float32)
def modem(dur=0.55):
    tt = np.arange(int(dur * SR)) / SR; rng = np.random.default_rng(2)
    fr = 900 + 1400 * ((tt * 9) % 1); x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * 0.18
    x += rng.normal(0, 1, len(tt)) * 0.08 * (0.5 + 0.5 * np.sin(2 * np.pi * 23 * tt))
    e = np.minimum(1, tt / 0.03) * np.minimum(1, (dur - tt) / 0.12)
    return (x * e).astype(np.float32)
def stamp_click(dur=0.18):
    tt = np.arange(int(dur * SR)) / SR
    return (np.sin(2 * np.pi * 120 * tt) * np.exp(-tt * 30) * 0.7 + np.random.default_rng(4).normal(0, 1, len(tt)) * np.exp(-tt * 80) * 0.25).astype(np.float32)
def pop(dur=0.13, f0=650, f1=1300):
    tt = np.arange(int(dur * SR)) / SR; fr = f0 + (f1 - f0) * tt / dur
    return (np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt * 18) * 0.45).astype(np.float32)
def swish(dur=0.35):
    tt = np.arange(int(dur * SR)) / SR; n = np.random.default_rng(5).normal(0, 1, len(tt))
    n = np.convolve(n, np.ones(12) / 12, 'same'); e = np.sin(np.pi * tt / dur) ** 2
    return (n * e * 0.5).astype(np.float32)
S = np.zeros_like(V)
def put(x, at, gain):
    i = int(at * SR); n = min(len(x), N - i); S[i:i + n] += x[:n, None] * gain
DIVE = vt(W[14]['e']) + 0.02           # depois de «Em dupla, com cinquenta.»
EXIT = vt(W[107]['s']) - 0.85          # sai do tubo na pausa depois de «O suíço agradece.»
PREV = vt(W[116]['s'])                 # clique do medidor GRAU DE CERTEZA
put(thump(), 0.0, 0.8)
put(modem(), DIVE, 0.55)
put(thump(0.4, 70), EXIT + 0.25, 0.35)
put(stamp_click(), PREV, 0.5)
# Micro-recompensas (retenção): um som curto em cada revelação visual.
def wsa(i): return vt(W[i]['s'])
for k in range(4): put(stamp_click(), 0.06 * k, 0.45)            # 4 cartas batem na mesa
put(pop(), wsa(6) - .05, 0.5)                                     # 25%
put(swish(), wsa(11) - .05, 0.5)                                  # cartas viram duplas
put(pop(f0=800, f1=1600), wsa(14) - .05, 0.5)                     # 50%
for i in (29, 39, 63, 87, 104): put(stamp_click(), wsa(i) - .05, 0.4)   # carimbos e cartões
for i in (72, 82): put(pop(), wsa(i) - .05, 0.4)                   # 25% / 50% na conta
for i in (111,): put(pop(f0=500, f1=1000), wsa(i) - .05, 0.35)    # «A dupla iguala a mesa»
for i in (133, 137, 141): put(pop(0.09, 900, 1400), wsa(i) - .05, 0.3)   # chips A/B/C
mix = V + M + S
sf.write('mix_raw.wav', mix, SR)
m = subprocess.run(['ffmpeg', '-v', 'info', '-i', 'mix_raw.wav', '-af', 'loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
js = json.loads(m[m.rfind('{'):m.rfind('}') + 1])
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'mix_raw.wav', '-af',
                f"loudnorm=I=-14:TP=-2.2:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true",
                '-ar', str(SR), 'mix_final.wav'], check=True)
json.dump(dict(TEMPO=TEMPO, LEAD=LEAD, PAUSES=PAUSES, OUT_START=OUT_START, TOTAL=TOTAL,
               DIVE=DIVE, EXIT=EXIT, PREV=PREV, REV0=REV0, REV1=REV1), open('tl.json', 'w'), indent=1)
fps = 30; nf = int(round(TOTAL * fps)); hop = SR // fps
e = np.array([np.sqrt((V[i * hop:(i + 1) * hop] ** 2).mean()) if i * hop < N else 0 for i in range(nf)])
np.save('led_env.npy', e / (np.percentile(e[e > 0.005], 95) if (e > 0.005).any() else 1))
print(json.load(open('tl.json')))
