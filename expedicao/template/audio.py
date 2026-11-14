# Expedição BINDER · áudio v2 (voz + música rearranjada na grelha + sonoplastia desenhada).
# Uso:  python3 -I audio.py <pasta_do_episodio> <pasta_de_trabalho>
#   episódio: episode.json, audio/words.json (Scribe, sem tags). trabalho: voz.mp3.
#   Saídas no trabalho: voz_edit.wav, musica_arranjo.wav, tl.json (palavras, grelha de batidas, energia por quadro,
#   eventos já presos à grelha), mix_final.wav (-14 LUFS, pico < -1 dBTP).
# Música (BIBLIA §3): rearranjada em batidas inteiras (episode.json -> musica.arranjo) para o drop cair na palavra
#   musica.drop_w; a pausa musica.ajuste_pausa_w absorve a diferença. A grelha do vídeo é a da música.
# Sonoplastia (BIBLIA §5): três sons de kit/sfx (descida, glitch, swell), só nos eventos marcados pela linha do tempo.
import json, subprocess, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linha_tempo import construir

EP, WK = sys.argv[1].rstrip('/'), sys.argv[2].rstrip('/')
SR = 48000; FPS = 30
CFG = json.load(open(f'{EP}/episode.json'))
WORDS = json.load(open(f'{EP}/{CFG["voz"]["words"]}'))
V = CFG['voz']; MU = CFG['musica']; TEMPO, LEAD = V['tempo'], V['lead']

def load(p, sr=SR):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '2', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
def save(p, x):
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', p], input=x.astype(np.float32).tobytes(), check=True)

# ---------- 1. música: arranjo em batidas inteiras ----------
P, OFF = MU['periodo'], MU['offset']
M0 = load(f'{EP}/{MU["arquivo"]}')
def bt(b): return OFF + b * P
pieces, vpos, drop_t = [], 0.0, None
for k, (b0, b1) in enumerate(MU['arranjo']):
    a = 0.0 if (k == 0 and b0 == 0) else bt(b0); b = len(M0) / SR if b1 is None else bt(b1)
    seg = M0[int(a * SR):int(b * SR)].copy(); f = int(0.012 * SR)
    if k > 0: seg[:f] *= np.linspace(0, 1, f)[:, None]
    if b1 is not None: seg[-f:] *= np.linspace(1, 0, f)[:, None]
    if b0 <= MU['drop_beat'] and (b1 is None or MU['drop_beat'] < b1): drop_t = vpos + (bt(MU['drop_beat']) - a)
    pieces.append(seg); vpos += len(seg) / SR
MUS = np.concatenate(pieces)

# ---------- 2. voz: cortes por palavra, pausas, tempo; a pausa de ajuste leva o drop à palavra-alvo ----------
raw = load(f'{WK}/voz.mp3')
mono = np.abs(raw).mean(1); win = int(0.01 * SR); env = np.convolve(mono, np.ones(win) / win, 'same')
def quiet(t, span=0.09):
    a, b = int(max(0, t - span) * SR), int(min(len(env) / SR, t + span) * SR)
    return (a + int(np.argmin(env[a:b]))) / SR if b > a else t
cuts = []
for i0, i1 in V['cortes']:
    a = quiet((WORDS[i0 - 1]['e'] + WORDS[i0]['s']) / 2) if i0 > 0 else 0.0
    cuts.append((a, quiet((WORDS[i1]['e'] + WORDS[i1 + 1]['s']) / 2)))
pausas = {i: d for i, d in V['pausas']}
def build(pausas):
    pauses = [(quiet((WORDS[i - 1]['e'] + WORDS[i]['s']) / 2), d) for i, d in sorted(pausas.items())]
    def edit_t(x):
        y = x
        for a, b in cuts:
            if x >= b: y -= (b - a)
            elif x > a: y -= (x - a)
        for p, d in pauses:
            if x >= p: y += d
        return y
    return pauses, edit_t
def vt_of(edit_t, x): return edit_t(x) / TEMPO + LEAD
pauses, edit_t = build(pausas)
alvo = WORDS[MU['drop_w']]['s']
delta = drop_t - vt_of(edit_t, alvo)
pausas[MU['ajuste_pausa_w']] = round(pausas.get(MU['ajuste_pausa_w'], 0) + delta * TEMPO, 4)
assert pausas[MU['ajuste_pausa_w']] >= 0.15, f'pausa de ajuste negativa ({pausas[MU["ajuste_pausa_w"]]:.2f}): mudar o arranjo'
pauses, edit_t = build(pausas)
marks = sorted([(a, 'cut', b) for a, b in cuts] + [(p, 'pause', d) for p, d in pauses])
out, pos = [], 0.0
for t, kind, v in marks:
    out.append(raw[int(pos * SR):int(t * SR)])
    if kind == 'cut': pos = v
    else: out.append(np.zeros((int(v * SR), 2), np.float32)); pos = t
out.append(raw[int(pos * SR):])
fade = int(0.006 * SR)
for s in out:
    if len(s) > 2 * fade: s[:fade] *= np.linspace(0, 1, fade)[:, None]; s[-fade:] *= np.linspace(1, 0, fade)[:, None]
save(f'{WK}/voz_edit_raw.wav', np.concatenate(out))
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f'{WK}/voz_edit_raw.wav', '-af',
                f'rubberband=tempo={TEMPO}:pitch=1:transients=crisp:formant=preserved,highpass=f=70,'
                'acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,loudnorm=I=-16:TP=-1.5:LRA=7',
                '-ar', str(SR), '-ac', '2', f'{WK}/voz_edit.wav'], check=True)
voz = load(f'{WK}/voz_edit.wav')
removed = set()
for i0, i1 in V['cortes']: removed |= set(range(i0, i1 + 1))
tw = [dict(w=w['w'], s=round(vt_of(edit_t, w['s']), 3), e=round(vt_of(edit_t, w['e']), 3), i=i, cortada=i in removed) for i, w in enumerate(WORDS)]
VEND = LEAD + len(voz) / SR
OUT_START = round(VEND + 0.35, 3); OUT_LEN = 3.867; TOTAL = round(OUT_START + OUT_LEN, 3)
N = int(TOTAL * SR)
nb = int((TOTAL - OFF) / P) + 1
BEATS = [round(OFF + j * P, 4) for j in range(nb)]
if len(MUS) < N: MUS = np.concatenate([MUS, np.zeros((N - len(MUS), 2), np.float32)])
MUS = MUS[:N]
# energia da música por quadro (0..1) para o fundo respirar
e = np.sqrt(np.convolve((MUS ** 2).mean(1), np.ones(int(0.12 * SR)) / int(0.12 * SR), 'same'))
fr = e[(np.arange(int(TOTAL * FPS)) * SR / FPS).astype(int)]
lo, hi = np.percentile(fr[fr > 0], 5), np.percentile(fr, 98)
ENV = [round(float(x), 3) for x in np.clip((fr - lo) / (hi - lo + 1e-9), 0, 1)]
TL = dict(words=tw, OUT_START=OUT_START, TOTAL=TOTAL, TEMPO=TEMPO, LEAD=LEAD, P=P, OFF=OFF, BEATS=BEATS, DROP=round(drop_t, 4),
          ENV=ENV, pausas=pausas)
TL['eventos'] = construir(CFG, tw, TOTAL, OUT_START, BEATS, drop_t)
json.dump(TL, open(f'{WK}/tl.json', 'w'), ensure_ascii=False, indent=0)
VOX = np.zeros((N, 2), np.float32); a = int(LEAD * SR); VOX[a:a + len(voz)] = voz[:N - a]

# ---------- 3. sonoplastia: três sons do kit, presos à grelha ----------
KIT = os.path.abspath(f'{EP}/../kit/sfx')
lib = {k: load(f'{KIT}/{k}.mp3') for k in ('descida', 'glitch', 'swell')}
gain = {'descida': 0.55, 'glitch': 0.22, 'swell': 0.35}
SFX = np.zeros((N, 2), np.float32); usados = {}
for ev in TL['eventos']:
    s = ev.get('som')
    if not s: continue
    x = lib[s] * gain[s]; t0 = ev['t'] - (len(x) / SR if s == 'swell' else 0)   # o swell acaba no instante do evento
    i = int(max(0, t0) * SR)
    if i < N: SFX[i:i + len(x)] += x[:N - i]
    usados[s] = usados.get(s, 0) + 1

# ---------- 4. música: -21 LUFS, ducking sob a voz, abre no drop e no fecho ----------
import pyloudnorm as pyln
meter = pyln.Meter(SR)
MUS = MUS * 10 ** ((MU['lufs'] - meter.integrated_loudness(MUS[:int(VEND * SR)])) / 20)
ev = np.abs(VOX).mean(1); w = int(0.05 * SR); ev = np.convolve(ev, np.ones(w) / w, 'same')
speak = np.convolve((ev > 0.01).astype(float), np.ones(int(0.3 * SR)), 'same') > 0
speak = np.convolve(speak.astype(float), np.ones(int(0.2 * SR)) / int(0.2 * SR), 'same')
t = np.arange(N) / SR
g_db = speak * MU['duck_db'] + 3 * np.exp(-((t - drop_t - 0.6) / 1.0) ** 2)
g_db = np.where(t >= OUT_START - 0.1, 2.0, g_db)
MUS = MUS * (10 ** (g_db / 20) * np.clip((TOTAL - t) / 0.8, 0, 1))[:, None]
save(f'{WK}/musica_arranjo.wav', MUS)
save(f'{WK}/mix_pre.wav', VOX + MUS + SFX)
st = subprocess.run(['ffmpeg', '-v', 'info', '-i', f'{WK}/mix_pre.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'],
                    capture_output=True, text=True).stderr
j = json.loads(st[st.rfind('{'):st.rfind('}') + 1])
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f'{WK}/mix_pre.wav', '-af',
                f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true",
                '-ar', str(SR), f'{WK}/mix_final.wav'], check=True)
print(f'voz {VEND:.2f} s · fecho a {OUT_START:.2f} s · total {TOTAL:.2f} s · drop {drop_t:.3f} s · pausa de ajuste {pausas[MU["ajuste_pausa_w"]]:.2f} s · sons {usados}')
