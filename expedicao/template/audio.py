# Expedição BINDER · áudio (voz + tema + assinatura sonora), reutilizável por episódio.
# Uso:  python3 -I audio.py <pasta_do_episodio> <pasta_de_trabalho>
#   episódio: episode.json (voz.cortes / voz.pausas por índice de palavra), audio/words.json (Scribe, sem as tags)
#   trabalho: voz.mp3 (ElevenLabs). Saídas no trabalho: voz_edit.wav, tl.json (tempos finais de cada palavra
#   e dos eventos), mix_final.wav (-14 LUFS, pico < -1 dBTP).
# Assinatura sonora do formato (BIBLIA §5): ping de sonar (camadas e acender do Lotus), bolhas (pop das caixas),
# whoosh de água (slide-ins). Nada mais. Tudo sintetizado aqui, sem bibliotecas externas.
import json, subprocess, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linha_tempo import construir

EP, WK = sys.argv[1].rstrip('/'), sys.argv[2].rstrip('/')
SR = 48000
CFG = json.load(open(f'{EP}/episode.json'))
WORDS = json.load(open(f'{EP}/{CFG["voz"]["words"]}'))
V = CFG['voz']; TEMPO, LEAD = V['tempo'], V['lead']

def load(p, sr=SR):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '2', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()

def save(p, x):
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', p], input=x.astype(np.float32).tobytes(), check=True)

# ---------- 1. voz: cortes por palavra (fronteira no ponto de menor energia), pausas, tempo ----------
raw = load(f'{WK}/voz.mp3')
mono = np.abs(raw).mean(1); win = int(0.01 * SR)
env = np.convolve(mono, np.ones(win) / win, 'same')
def quiet(t, span=0.09):
    a, b = int(max(0, t - span) * SR), int(min(len(env) / SR, t + span) * SR)
    return (a + int(np.argmin(env[a:b]))) / SR if b > a else t
segs, cuts = [], []
for i0, i1 in V['cortes']:
    a = quiet((WORDS[i0 - 1]['e'] + WORDS[i0]['s']) / 2) if i0 > 0 else 0.0
    b = quiet((WORDS[i1]['e'] + WORDS[i1 + 1]['s']) / 2)
    cuts.append((a, b))
pauses = [(quiet((WORDS[i - 1]['e'] + WORDS[i]['s']) / 2), d) for i, d in V['pausas']]
# mapa tempo original -> tempo editado (antes do tempo)
def edit_t(x):
    y = x
    for a, b in cuts:
        if x >= b: y -= (b - a)
        elif x > a: y -= (x - a)
    for p, d in pauses:
        if x >= p: y += d
    return y
marks = sorted([(a, 'cut', b) for a, b in cuts] + [(p, 'pause', d) for p, d in pauses])
out, pos = [], 0.0
for t, kind, v in marks:
    out.append(raw[int(pos * SR):int(t * SR)])
    if kind == 'cut': pos = v
    else: out.append(np.zeros((int(v * SR), 2), np.float32)); pos = t
out.append(raw[int(pos * SR):])
fade = int(0.006 * SR)
for k in range(len(out)):                       # micro-fades nas emendas
    s = out[k]
    if len(s) > 2 * fade:
        s[:fade] *= np.linspace(0, 1, fade)[:, None]; s[-fade:] *= np.linspace(1, 0, fade)[:, None]
save(f'{WK}/voz_edit_raw.wav', np.concatenate(out))
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f'{WK}/voz_edit_raw.wav', '-af',
                f'rubberband=tempo={TEMPO}:pitch=1:transients=crisp:formant=preserved,highpass=f=70,'
                'acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,loudnorm=I=-16:TP=-1.5:LRA=7',
                '-ar', str(SR), '-ac', '2', f'{WK}/voz_edit.wav'], check=True)
voz = load(f'{WK}/voz_edit.wav')
def vt(x): return edit_t(x) / TEMPO + LEAD
removed = set()
for i0, i1 in V['cortes']: removed |= set(range(i0, i1 + 1))
tw = [dict(w=w['w'], s=round(vt(w['s']), 3), e=round(vt(w['e']), 3), i=i, cortada=i in removed) for i, w in enumerate(WORDS)]
VEND = LEAD + len(voz) / SR
OUT_START = round(VEND + 0.35, 3); OUT_LEN = 3.867; TOTAL = round(OUT_START + OUT_LEN, 3)
TL = dict(words=tw, OUT_START=OUT_START, TOTAL=TOTAL, TEMPO=TEMPO, LEAD=LEAD)
TL['eventos'] = construir(CFG, tw, TOTAL, OUT_START)
json.dump(TL, open(f'{WK}/tl.json', 'w'), ensure_ascii=False, indent=0)
N = int(TOTAL * SR)
VOX = np.zeros((N, 2), np.float32); a = int(LEAD * SR); VOX[a:a + len(voz)] = voz[:N - a]

# ---------- 2. assinatura sonora ----------
rng = np.random.default_rng(7)
def ping(dur=1.6):
    t = np.arange(int(dur * SR)) / SR
    x = np.sin(2 * np.pi * 1180 * t) * np.exp(-t * 5.5) * 0.5 + np.sin(2 * np.pi * 2360 * t) * np.exp(-t * 9) * 0.08
    for d, g in ((0.32, 0.35), (0.64, 0.15)):  # eco de sonar
        k = int(d * SR); x[k:] += x[:-k] * g
    return x.astype(np.float32)
def bolhas(dur=0.42):
    y = np.zeros(int(dur * SR), np.float32)
    for k in range(6):
        t0 = rng.uniform(0, dur - 0.08); f0 = rng.uniform(500, 1100); L = int(0.06 * SR)
        t = np.arange(L) / SR; f = f0 * (1 + 2.5 * t / 0.06)
        b = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 55) * rng.uniform(0.15, 0.3)
        i = int(t0 * SR); y[i:i + L] += b[:len(y) - i]
    return y
def whoosh(dur=0.45, up=True):
    n = int(dur * SR); t = np.arange(n) / SR
    x = rng.normal(0, 1, n).astype(np.float32)
    # filtro passa-banda móvel simples: média móvel de largura variável
    k0, k1 = (60, 8) if up else (8, 60)
    y = np.zeros(n, np.float32); cs = np.concatenate([[0], np.cumsum(x)])
    for i in range(n):
        k = int(k0 + (k1 - k0) * i / n); j = max(0, i - k); y[i] = (cs[i + 1] - cs[j]) / (i + 1 - j)
    y -= np.convolve(y, np.ones(400) / 400, 'same')
    env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.5
    return (y * env * 1.4).astype(np.float32)
SFX = np.zeros(N, np.float32)
lib = dict(ping=ping(), bolhas=bolhas(), whoosh=whoosh(), whoosh_out=whoosh(up=False))
gain = dict(ping=0.55, bolhas=0.5, whoosh=0.35, whoosh_out=0.3)
for ev in TL['eventos']:
    s = ev.get('som')
    if not s: continue
    x = lib[s] * gain[s]; i = int(ev['t'] * SR)
    if i < N: SFX[i:i + len(x)] += x[:N - i]

# ---------- 3. tema: -22 LUFS, ducking sob a voz, sobe no Lotus e no fecho ----------
M = load(f'{EP}/{CFG["musica"]["arquivo"]}')
import pyloudnorm as pyln
meter = pyln.Meter(SR)
M *= 10 ** ((CFG['musica']['lufs'] - meter.integrated_loudness(M)) / 20)
if len(M) < N: M = np.concatenate([M, np.zeros((N - len(M), 2), np.float32)])
M = M[:N]
e = np.abs(VOX).mean(1); w = int(0.05 * SR); e = np.convolve(e, np.ones(w) / w, 'same')
speak = np.convolve((e > 0.01).astype(float), np.ones(int(0.3 * SR)), 'same') > 0
speak = np.convolve(speak.astype(float), np.ones(int(0.25 * SR)) / int(0.25 * SR), 'same')
g_db = speak * CFG['musica']['duck_db']
t = np.arange(N) / SR
lit = [ev['t'] for ev in TL['eventos'] if ev.get('tipo') == 'lotus_acende']
for L in lit: g_db += 4 * np.exp(-((t - L - 1.0) / 1.4) ** 2)
g_db = np.where(t >= OUT_START - 0.2, 3.0, g_db)
fade = np.clip((TOTAL - t) / 1.4, 0, 1)
M = M * (10 ** (g_db / 20) * fade)[:, None]
MIX = VOX + M + SFX[:, None]
save(f'{WK}/mix_pre.wav', MIX)
# loudness final em duas passagens
st = subprocess.run(['ffmpeg', '-v', 'info', '-i', f'{WK}/mix_pre.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'],
                    capture_output=True, text=True).stderr
j = json.loads(st[st.rfind('{'):st.rfind('}') + 1])
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f'{WK}/mix_pre.wav', '-af',
                f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true",
                '-ar', str(SR), f'{WK}/mix_final.wav'], check=True)
print(f'voz {VEND:.2f} s · fecho a {OUT_START:.2f} s · total {TOTAL:.2f} s · eventos {len(TL["eventos"])}')
