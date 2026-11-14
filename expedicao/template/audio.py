# Expedição BINDER · áudio v3 (voz + música rearranjada na grelha + sonoplastia desenhada), por versão de final.
# Uso:  python3 -I audio.py <pasta_do_episodio> <pasta_de_trabalho> [A|B]
#   episódio: episode.json, audio/words.json (Scribe, sem tags). trabalho: voz.mp3.
#   Saídas no trabalho (sufixo _A/_B): voz_edit, musica_arranjo, tl.json (palavras, grelha, energia por quadro,
#   eventos presos à grelha, blocos de fim), mix_final.wav (-14 LUFS, pico < -1 dBTP).
# Música (BIBLIA §3): arranjo automático em batidas inteiras: pré-drop + os n compassos anteriores repetidos até o drop
#   cair na palavra musica.drop_w (a pausa musica.ajuste_pausa_w absorve o resto) + pós-drop + m repetições + cauda,
#   para a cauda natural da faixa acabar com o vídeo (sem trecho final mudo).
# Sonoplastia (BIBLIA §5): três sons de kit/sfx + um fundo de água sintetizado só no gancho e no Abismo.
import json, subprocess, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linha_tempo import construir

EP, WK = sys.argv[1].rstrip('/'), sys.argv[2].rstrip('/')
VER = sys.argv[3] if len(sys.argv) > 3 else 'A'
SR = 48000; FPS = 30
CFG = json.load(open(f'{EP}/episode.json'))
VCFG = CFG['versoes'][VER]
WORDS = json.load(open(f'{EP}/{CFG["voz"]["words"]}'))
V = CFG['voz']; MU = CFG['musica']; TEMPO, LEAD = V['tempo'], V['lead']

def load(p, sr=SR):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '2', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
def save(p, x):
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', p], input=x.astype(np.float32).tobytes(), check=True)

P, OFF = MU['periodo'], MU['offset']
def bt(b): return OFF + b * P

# ---------- 1. voz ----------
raw = load(f'{WK}/voz.mp3')
mono = np.abs(raw).mean(1); win = int(0.01 * SR); env = np.convolve(mono, np.ones(win) / win, 'same')
def quiet(t, span=0.09):
    a, b = int(max(0, t - span) * SR), int(min(len(env) / SR, t + span) * SR)
    return (a + int(np.argmin(env[a:b]))) / SR if b > a else t
cortes = sorted(V['cortes'] + VCFG.get('cortes_extra', []))
cuts = []
for i0, i1 in cortes:
    a = quiet((WORDS[i0 - 1]['e'] + WORDS[i0]['s']) / 2) if i0 > 0 else 0.0
    b = quiet((WORDS[i1]['e'] + WORDS[i1 + 1]['s']) / 2) if i1 + 1 < len(WORDS) else len(raw) / SR
    cuts.append((a, b))
removed = set()
for i0, i1 in cortes: removed |= set(range(i0, i1 + 1))
pausas = {i: d for i, d in V['pausas'] if i not in removed}
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
t_alvo = vt_of(edit_t, WORDS[MU['drop_w']]['s'])

# ---------- 2. música: arranjo automático ----------
pre_len = sum(bt(b1) - (0 if b0 == 0 else bt(b0)) for b0, b1 in MU['pre_drop'])
r0, r1 = MU['repetir_pre']; rep = bt(r1) - bt(r0)   # um compasso; n compassos = repetir os n compassos anteriores ao drop, seguidos
drop_in_pos = bt(MU['drop_beat']) - bt(MU['pos_drop'][0])
n = 0
while pre_len + n * rep + drop_in_pos < t_alvo + 0.12: n += 1
drop_t = pre_len + n * rep + drop_in_pos
pausas[MU['ajuste_pausa_w']] = round(pausas.get(MU['ajuste_pausa_w'], 0) + (drop_t - t_alvo) * TEMPO, 4)
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
save(f'{WK}/voz_edit_raw_{VER}.wav', np.concatenate(out))
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f'{WK}/voz_edit_raw_{VER}.wav', '-af',
                f'rubberband=tempo={TEMPO}:pitch=1:transients=crisp:formant=preserved,highpass=f=70,'
                'acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,loudnorm=I=-16:TP=-1.5:LRA=7',
                '-ar', str(SR), '-ac', '2', f'{WK}/voz_edit_{VER}.wav'], check=True)
voz = load(f'{WK}/voz_edit_{VER}.wav')
e2 = np.abs(voz).mean(1); idx = np.where(e2 > 0.003)[0]; voz = voz[:idx[-1] + int(0.08 * SR)]   # sem silêncio final
tw = [dict(w=w['w'], s=round(vt_of(edit_t, w['s']), 3), e=round(vt_of(edit_t, w['e']), 3), i=i, cortada=i in removed) for i, w in enumerate(WORDS)]
VEND = LEAD + len(voz) / SR
# blocos de fim (scanner, cartão) a começar num tempo forte depois da voz
fim = []; t = VEND + VCFG['apos_voz']
k = int(np.ceil((t - OFF) / (4 * P))); t = OFF + k * 4 * P
for f in VCFG['fim']:
    d = round(f['dur'] / P) * P
    fim.append(dict(f, t=round(t, 4), t1=round(t + d, 4))); t += d
TOTAL = round(t, 3)
post_len = bt(MU['pos_drop'][1]) - bt(MU['drop_beat']); c0 = MU['cauda'][0]
M0 = load(f'{EP}/{MU["arquivo"]}')
cauda_len = len(M0) / SR - bt(c0)
q0, q1 = MU['repetir_pos']; qrep = bt(q1) - bt(q0); m = 0
while drop_t + post_len + m * qrep + cauda_len < TOTAL + 0.2: m += 1
bar = r1 - r0
arranjo = list(MU['pre_drop']) + ([[r1 - n * bar, r1]] if n else []) + [MU['pos_drop']] + ([[q1 - m * (q1 - q0), q1]] if m else []) + [MU['cauda']]
pieces = []
for j, (b0, b1) in enumerate(arranjo):
    a = 0.0 if (j == 0 and b0 == 0) else bt(b0); b = len(M0) / SR if b1 is None else bt(b1)
    seg = M0[int(a * SR):int(b * SR)].copy(); f = int(0.012 * SR)
    if j > 0: seg[:f] *= np.linspace(0, 1, f)[:, None]
    if b1 is not None: seg[-f:] *= np.linspace(1, 0, f)[:, None]
    pieces.append(seg)
MUS = np.concatenate(pieces)
N = int(TOTAL * SR)
BEATS = [round(OFF + j * P, 4) for j in range(int((TOTAL - OFF) / P) + 1)]
if len(MUS) < N: MUS = np.concatenate([MUS, np.zeros((N - len(MUS), 2), np.float32)])
MUS = MUS[:N]
e = np.sqrt(np.convolve((MUS ** 2).mean(1), np.ones(int(0.12 * SR)) / int(0.12 * SR), 'same'))
fr = e[np.minimum((np.arange(int(TOTAL * FPS)) * SR / FPS).astype(int), N - 1)]
lo, hi = np.percentile(fr[fr > 0], 5), np.percentile(fr, 98)
ENV = [round(float(x), 3) for x in np.clip((fr - lo) / (hi - lo + 1e-9), 0, 1)]
TL = dict(versao=VER, words=tw, VEND=round(VEND, 3), TOTAL=TOTAL, TEMPO=TEMPO, LEAD=LEAD, P=P, OFF=OFF, BEATS=BEATS,
          DROP=round(drop_t, 4), ENV=ENV, pausas=pausas, arranjo=arranjo, fim=fim)
TL['eventos'] = construir(CFG, tw, TOTAL, VER, BEATS, drop_t, fim)
json.dump(TL, open(f'{WK}/tl_{VER}.json', 'w'), ensure_ascii=False, indent=0)
VOX = np.zeros((N, 2), np.float32); a = int(LEAD * SR); VOX[a:a + len(voz)] = voz[:N - a]

# ---------- 3. sonoplastia ----------
KIT = os.path.abspath(f'{EP}/../kit/sfx')
lib = {k: load(f'{KIT}/{k}.mp3') for k in ('descida', 'glitch', 'swell')}
gain = {'descida': 0.55, 'glitch': 0.2, 'swell': 0.35}
SFX = np.zeros((N, 2), np.float32); usados = {}
for ev in TL['eventos']:
    s = ev.get('som')
    if not s: continue
    x = lib[s] * gain[s]; t0 = ev['t'] - (len(x) / SR if s == 'swell' else 0)
    i = int(max(0, t0) * SR)
    if i < N: SFX[i:i + len(x)] += x[:N - i]
    usados[s] = usados.get(s, 0) + 1
# fundo de água discreto (ruído castanho filtrado) só no gancho e no Abismo até ao drop
rng = np.random.default_rng(5); nz = np.cumsum(rng.normal(0, 1, (N, 2)), 0).astype(np.float32)
for c in range(2): nz[:, c] -= np.convolve(nz[:, c], np.ones(4800) / 4800, 'same')
kk = 400; cs = np.cumsum(nz, 0); nz2 = np.zeros_like(nz); nz2[kk:] = (cs[kk:] - cs[:-kk]) / kk
nz2 /= (np.abs(nz2).max() + 1e-9)
tt = np.arange(N) / SR
abis = [ev['t'] for ev in TL['eventos'] if ev['tipo'] == 'respiro' and CFG['blocos'][ev['bloco']]['camada'] == 'abismo']
first = min(ev['t'] for ev in TL['eventos'] if ev['tipo'] == 'carta')
amb = np.clip((first - tt) / 0.3, 0, 1)
if abis: amb = np.maximum(amb, np.clip((tt - abis[0]) / 0.6, 0, 1) * np.clip((drop_t - tt) / 0.25, 0, 1))
amb = amb * (0.75 + 0.25 * np.sin(tt * 0.9))
AMB = nz2 * (amb * 0.06)[:, None]

# ---------- 4. música: musica.lufs (−26), ducking musica.duck_db sob a voz (≥ 15 dB abaixo da voz, para a tradução
#      automática do Instagram separar a fala), sobe musica.fim_db depois da voz ----------
import pyloudnorm as pyln
meter = pyln.Meter(SR)
MUS = MUS * 10 ** ((MU['lufs'] - meter.integrated_loudness(MUS[:int(VEND * SR)])) / 20)
ev = np.abs(VOX).mean(1); w = int(0.05 * SR); ev = np.convolve(ev, np.ones(w) / w, 'same')
speak = np.convolve((ev > 0.01).astype(float), np.ones(int(0.3 * SR)), 'same') > 0
speak = np.convolve(speak.astype(float), np.ones(int(0.2 * SR)) / int(0.2 * SR), 'same')
g_db = speak * MU['duck_db'] + MU.get('drop_db', 3) * np.exp(-((tt - drop_t - 0.6) / 1.0) ** 2)
fim_db = MU.get('fim_db', 2.0); g_db = np.where(tt >= VEND + 0.2, fim_db, g_db)
g_db = np.where((tt > VEND - 0.3) & (tt < VEND + 0.2), np.interp(tt, [VEND - 0.3, VEND + 0.2], [MU['duck_db'], fim_db]), g_db)
MUS = MUS * (10 ** (g_db / 20) * np.clip((TOTAL - tt) / 0.6, 0, 1))[:, None]
save(f'{WK}/musica_arranjo_{VER}.wav', MUS)
save(f'{WK}/mix_pre_{VER}.wav', VOX + MUS + SFX + AMB)
st = subprocess.run(['ffmpeg', '-v', 'info', '-i', f'{WK}/mix_pre_{VER}.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'],
                    capture_output=True, text=True).stderr
j = json.loads(st[st.rfind('{'):st.rfind('}') + 1])
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f'{WK}/mix_pre_{VER}.wav', '-af',
                f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true",
                '-ar', str(SR), f'{WK}/mix_final_{VER}.wav'], check=True)
print(f'[{VER}] voz até {VEND:.2f} s · total {TOTAL:.2f} s · drop {drop_t:.3f} s (n={n}, m={m}) · pausa de ajuste {pausas[MU["ajuste_pausa_w"]]:.2f} s · sons {usados}')
