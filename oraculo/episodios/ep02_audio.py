# Meta em Curto EP02 · áudio (voz + trilha + SFX), derivado de ep01_audio.py
# Uso: correr numa pasta de trabalho com voz.mp3 (ElevenLabs) e words.json (tempos por palavra).
#   python3 ep02_audio.py /caminho/do/kit
import numpy as np, soundfile as sf, subprocess, json, sys
K = sys.argv[1] if len(sys.argv) > 1 else '../..'
SR = 48000; TEMPO = 1.10; LEAD = 0.15
PAUSE_AT = 37.62; PAUSE = 0.30        # respiração depois de «Mesa não é vida.» (tempo da voz original)
def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
def vt(x):  # tempo da voz original -> tempo do vídeo
    return x / TEMPO + LEAD + (PAUSE if x >= PAUSE_AT else 0)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'voz.mp3', '-af',
                f'atempo={TEMPO},highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,loudnorm=I=-16:TP=-1.5:LRA=7',
                '-ar', str(SR), '-ac', '2', 'voz_proc.wav'], check=True)
voz = load('voz_proc.wav')
cut = int((PAUSE_AT / TEMPO) * SR)
voz = np.concatenate([voz[:cut], np.zeros((int(PAUSE * SR), 2), np.float32), voz[cut:]])
vend = LEAD + len(voz) / SR
OUT_START = round(vend + 0.25, 3); OUT_LEN = 3.87; TOTAL = OUT_START + OUT_LEN
N = int(TOTAL * SR)
V = np.zeros((N, 2), np.float32); a = int(LEAD * SR); V[a:a + len(voz)] = voz[:N - a]
M = load(K + '/oraculo/musica/tubo_tema_original.mp3')[:N]
M = np.pad(M, ((0, N - len(M)), (0, 0)))
t = np.arange(N) / SR
env = np.abs(V).mean(1); w = int(0.05 * SR); env = np.convolve(env, np.ones(w) / w, 'same')
speak = (env > 0.01).astype(float)
d = int(0.35 * SR); speak = np.convolve(speak, np.ones(d), 'same') > 0
s = int(0.25 * SR); speak = np.convolve(speak.astype(float), np.ones(s) / s, 'same')
g = 10 ** ((-6 + speak * (-12)) / 20)          # ducking ~12 dB sob a voz
W = json.load(open('words.json'))
REV0 = vt(37.52); REV1 = REV0 + 1.25           # corte seco logo a seguir a «Mesa não é vida.»
c = np.ones(N); i0, i1 = int(REV0 * SR), int(REV1 * SR); f = int(0.03 * SR)
c[i0:i1] = 0; c[i0 - f:i0] = np.linspace(1, 0, f); c[i1:i1 + f] = np.linspace(0, 1, f)
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
def glitch(dur=0.5):   # erro de sistema: zumbido digital com cortes
    tt = np.arange(int(dur * SR)) / SR; rng = np.random.default_rng(5)
    x = np.sign(np.sin(2 * np.pi * 180 * tt)) * 0.10 + rng.normal(0, 1, len(tt)) * 0.06
    gate = (np.floor(tt * 28) % 3 != 1).astype(float)
    e = np.minimum(1, tt / 0.01) * np.minimum(1, (dur - tt) / 0.05)
    return (x * gate * e).astype(np.float32)
S = np.zeros_like(V)
def put(x, at, gain):
    i = int(at * SR); n = min(len(x), N - i); S[i:i + n] += x[:n, None] * gain
DIVE = vt(5.56)                    # depois de «E ganhou os dois.»
EXIT = vt(33.40) - 0.45            # sai do tubo antes de «O meu modelo…»
ERR = vt(35.28)                    # «Ele contou o dano» -> erro de sistema
put(thump(), 0.0, 0.8)
put(modem(), DIVE, 0.55)
put(thump(0.4, 70), EXIT + 0.25, 0.35)
put(glitch(), ERR, 0.5)
mix = V + M + S
sf.write('mix_raw.wav', mix, SR)
# mix final a -14 LUFS, pico <= -1 dBFS (loudnorm em duas passagens)
m = subprocess.run(['ffmpeg', '-v', 'info', '-i', 'mix_raw.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
js = json.loads(m[m.rfind('{'):m.rfind('}') + 1])
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'mix_raw.wav', '-af',
                f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true",
                '-ar', str(SR), 'mix_final.wav'], check=True)
json.dump(dict(TEMPO=TEMPO, LEAD=LEAD, PAUSE_AT=PAUSE_AT, PAUSE=PAUSE, OUT_START=OUT_START, TOTAL=TOTAL,
               DIVE=DIVE, EXIT=EXIT, ERR=ERR, REV0=REV0, REV1=REV1), open('tl.json', 'w'), indent=1)
fps = 30; nf = int(round(TOTAL * fps)); hop = SR // fps
e = np.array([np.sqrt((V[i * hop:(i + 1) * hop] ** 2).mean()) if i * hop < N else 0 for i in range(nf)])
np.save('led_env.npy', e / (np.percentile(e[e > 0.005], 95) if (e > 0.005).any() else 1))
print(json.load(open('tl.json')))
