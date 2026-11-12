# Meta em Curto EP05 · áudio (voz + trilha + SFX), derivado de ep04_audio.py
# Uso: numa pasta de trabalho com t1.mp3 (tomada 1), p2.mp3 (correção, take 2) e words.json (= oraculo/episodios/ep05_words.json):
#   python3 ep05_audio.py /caminho/do/kit
# Correção: a tomada 1 dizia «noventa e um por cento», mas 91,63% arredonda para 92. A frase das sete cartas (39,44–43,92 s da tomada 1)
# é trocada pela frase regravada, acelerada para caber na mesma janela: nenhuma outra palavra muda de tempo.
# Trilha: "Paper Thin Alibi" original (62 s). O episódio dura mais do que o tema, por isso um troço repete-se:
# salto de 49,78 s para 19,02 s, o par de batidas mais parecido que a análise de cromas+MFCC encontrou (mesmo método de editar_tema.py).
# Corte seco de 1,2 s logo depois de «É modelo, não é jogo.»; a primeira frase da revelação cai no silêncio.
# Pausas: a fala bruta corre seguida; aqui abrem-se silêncios curtos entre blocos para a leitura dos gráficos.
import numpy as np, soundfile as sf, subprocess, json, sys
K = sys.argv[1] if len(sys.argv) > 1 else '../..'
SR = 48000; TEMPO = 1.10; LEAD = 0.15
D = json.load(open('words.json')); W = D['falada']
# (índice da palavra que abre o bloco, segundos de pausa antes dela)
PAUSAS = [(46, .18), (65, .22), (97, .2), (118, .28), (151, .3), (175, .3), (216, .85), (236, .4), (254, .4), (270, .3)]
def corte(i): return (W[i - 1]['e'] + W[i]['s']) / 2 / TEMPO      # ponto de corte, no tempo da voz já acelerada
def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
def vt(x):                                                         # tempo bruto da fala → tempo do vídeo
    y = x / TEMPO + LEAD
    for i, g in PAUSAS:
        if x / TEMPO >= corte(i): y += g
    return y
A, B = 39.44, 43.92; P0, P1 = 0.02, 5.32
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 't1.mp3', '-i', 'p2.mp3', '-filter_complex',
                f'[0:a]atrim=0:{A},asetpts=N/SR/TB,aresample=44100[a];[1:a]atrim={P0}:{P1},asetpts=N/SR/TB,atempo={(P1 - P0) / (B - A):.5f},volume=1.09,aresample=44100[p];'
                f'[0:a]atrim=start={B},asetpts=N/SR/TB,aresample=44100[c];[a][p][c]concat=n=3:v=0:a=1[o]', '-map', '[o]', '-c:a', 'libmp3lame', '-q:a', '2', 'voz.mp3'], check=True)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'voz.mp3', '-af',
                f'atempo={TEMPO},highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,loudnorm=I=-16:TP=-1.5:LRA=7',
                '-ar', str(SR), '-ac', '2', 'voz_proc.wav'], check=True)
voz0 = load('voz_proc.wav')
peda = []; ini = 0
for i, g in PAUSAS:
    c = int(corte(i) * SR); peda += [voz0[ini:c], np.zeros((int(g * SR), 2), np.float32)]; ini = c
peda.append(voz0[ini:]); voz = np.concatenate(peda)
vend = LEAD + len(voz) / SR
OUT_START = round(vend + 0.25, 3); OUT_LEN = 3.87; TOTAL = OUT_START + OUT_LEN
N = int(TOTAL * SR)
V = np.zeros((N, 2), np.float32); a = int(LEAD * SR); V[a:a + len(voz)] = voz[:N - a]
# --- trilha prolongada
T0 = load(K + '/oraculo/musica/tubo_tema_original.mp3')
A1, B0 = 49.78, 19.02; xf = int(.03 * SR)
p1 = T0[:int(A1 * SR) + xf]; p2 = T0[int(B0 * SR):]
r = np.linspace(1, 0, xf)[:, None]
T = np.concatenate([p1[:-xf], p1[-xf:] * r + p2[:xf] * (1 - r), p2[xf:]])
TL_ = len(T) / SR
REV0 = vt(W[215]['e']) + 0.02          # fim de «jogo.»
REV1 = REV0 + 1.20                     # silêncio de 1,2 s (assinatura da série)
resume = max(0.0, TL_ - 2.4 - (TOTAL - REV1))   # o tema tem 2,4 s de silêncio na cauda: a música acaba com o fade do fecho
M = np.zeros((N, 2), np.float32)
i0 = int(REV0 * SR); n0 = min(i0, len(T)); M[:n0] = T[:n0]
seg = T[int(resume * SR):]; i1 = int(REV1 * SR); n = min(len(seg), N - i1); M[i1:i1 + n] = seg[:n]
t = np.arange(N) / SR
env = np.abs(V).mean(1); w = int(0.05 * SR); env = np.convolve(env, np.ones(w) / w, 'same')
speak = (env > 0.01).astype(float)
d = int(0.35 * SR); speak = np.convolve(speak, np.ones(d), 'same') > 0
s = int(0.25 * SR); speak = np.convolve(speak.astype(float), np.ones(s) / s, 'same')
g = 10 ** ((-6 + speak * (-12)) / 20)          # ducking ~12 dB sob a voz
c = np.ones(N); f = int(0.03 * SR)
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
def tick(dur=0.06):
    tt = np.arange(int(dur * SR)) / SR
    return (np.sin(2 * np.pi * 1800 * tt) * np.exp(-tt * 70) * 0.35).astype(np.float32)
def buzz(dur=0.35):                    # «SEM DADOS»
    tt = np.arange(int(dur * SR)) / SR
    x = np.sign(np.sin(2 * np.pi * 140 * tt)) * 0.08 * (np.floor(tt * 24) % 2)
    return (x * np.minimum(1, (dur - tt) / 0.05)).astype(np.float32)
S = np.zeros_like(V)
def put(x, at, gain):
    i = int(at * SR); n = min(len(x), N - i); S[i:i + n] += x[:n, None] * gain
DIVE = vt(W[12]['e']) - 0.05           # mergulho depois de «abrir.»
EXIT = vt(W[215]['e']) - 0.10          # sai do tubo logo depois de «jogo.»
put(thump(), 0.0, 0.8)
put(modem(), DIVE, 0.55)
for k in (15, 34, 65, 75, 81, 105, 121, 136, 146, 151, 159, 161, 168, 175, 189, 193, 197, 199, 208): put(tick(), vt(W[k]['s']), 0.5)
put(buzz(0.3), vt(W[51]['s']), 0.3)    # «zero partidas»
put(thump(0.4, 70), EXIT + 0.25, 0.35)
mix = V + M + S
sf.write('mix_raw.wav', mix, SR)
m = subprocess.run(['ffmpeg', '-v', 'info', '-i', 'mix_raw.wav', '-af', 'loudnorm=I=-14:TP=-2.0:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
js = json.loads(m[m.rfind('{'):m.rfind('}') + 1])
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', 'mix_raw.wav', '-af',
                f"loudnorm=I=-14:TP=-2.0:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true",
                '-ar', str(SR), 'mix_final.wav'], check=True)
json.dump(dict(TEMPO=TEMPO, LEAD=LEAD, OUT_START=OUT_START, TOTAL=TOTAL, DIVE=DIVE, EXIT=EXIT, REV0=REV0, REV1=REV1, RESUME=resume,
               PAUSAS=PAUSAS, CORTES=[corte(i) for i, _ in PAUSAS], tema_s=TL_), open('tl.json', 'w'), indent=1)
fps = 30; nf = int(round(TOTAL * fps)); hop = SR // fps
e = np.array([np.sqrt((V[i * hop:(i + 1) * hop] ** 2).mean()) if i * hop < N else 0 for i in range(nf)])
np.save('led_env.npy', e / (np.percentile(e[e > 0.005], 95) if (e > 0.005).any() else 1))
print(json.load(open('tl.json')))
