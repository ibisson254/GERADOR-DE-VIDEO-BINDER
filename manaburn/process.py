"""Monta a dublagem: corta as duas faixas (Burn e Mana) nas pausas, encaixa as 18 falas em
bate-volta, alinha a parada seca da música com o "Comenta aí", gera data.js e a trilha final.
uso: python3 process.py burn.mp3 mana.mp3
"""
import sys, json, subprocess, wave
import numpy as np

SR = 44100
EPI = json.load(open('episode.json', encoding='utf-8'))
TEXT = {'B': EPI['B'], 'M': EPI['M']}
# folga antes de cada fala (negativo = atropela a anterior, como numa discussão)
GAP = EPI['gap']
MUSIC_BREAK, MUSIC_SLAM = 125.05, 126.30   # parada seca e pancada no trecho escolhido da música

def load(path):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '_t.wav'], check=True)
    w = wave.open('_t.wav'); x = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float32) / 32768
    return x

def split(x, texts):
    """Corta a faixa nas pausas certas: entre todas as pausas, escolhe as n-1 que deixam cada
    trecho com a duração mais parecida com o tamanho do texto (e prefere as pausas mais longas)."""
    n = len(texts); hop = int(0.01 * SR)
    fr = np.sqrt(np.convolve(x ** 2, np.ones(hop) / hop, 'same'))[::hop]
    thr = max(0.012, np.percentile(fr, 95) * 0.06); v = fr > thr
    idx = np.where(v)[0]; first, last = idx[0], idx[-1] + 1
    sil = []; i = first
    while i < last:
        if not v[i]:
            j = i
            while j < last and not v[j]: j += 1
            if (j - i) * 0.01 >= 0.25: sil.append((i, j))
            i = j
        else: i += 1
    chars = np.array([len(t.replace('*', '')) for t in texts], float)
    voiced = v[first:last].sum() * 0.01; rate = voiced / chars.sum()
    exp = chars * rate + 0.25
    m = len(sil); INF = 1e9
    starts = [first] + [b for a, b in sil]; ends = [a for a, b in sil] + [last]
    # dp[k][j]: melhor custo usando k cortes, com o último corte na pausa j
    from functools import lru_cache
    def segcost(a, b, k):  # trecho do fim da pausa a ao começo da pausa b, é a fala k
        d = (b - a) * 0.01; return ((d - exp[k]) / exp[k]) ** 2
    @lru_cache(None)
    def best(k, j):  # k = fala atual (0..n-1), j = índice de início (0 = começo, 1..m = depois da pausa j-1)
        a = starts[j]
        if k == n - 1: return (segcost(a, last, k), ())
        res = (INF, ())
        for q in range(j, m):
            b, e = sil[q]
            if b <= a: continue
            c = segcost(a, b, k) - 0.6 * (e - b) * 0.01
            sub = best(k + 1, q + 1)
            if c + sub[0] < res[0]: res = (c + sub[0], (q,) + sub[1])
        return res
    cuts = best(0, 0)[1]
    if len(cuts) != n - 1: raise SystemExit('não consegui separar as falas')
    bounds = [(first, sil[cuts[0]][0])] + [(sil[cuts[k]][1], sil[cuts[k + 1]][0]) for k in range(n - 2)] + [(sil[cuts[-1]][1], last)]
    pad = int(0.05 * SR)
    for k, (a, b) in enumerate(bounds): print(f'   {texts[k][:30]:30s} {a*0.01:6.2f}-{b*0.01:6.2f}s')
    return [x[max(0, a * hop - pad): b * hop + pad] for a, b in bounds]

burn = split(load(sys.argv[1]), TEXT['B'])
if len(sys.argv) > 3:   # fala do "Bane ou não bane?" regravada com a pronúncia certa
    xb = load(sys.argv[3]); hop = int(0.01*SR); fr = np.sqrt(np.convolve(xb**2, np.ones(hop)/hop, 'same'))[::hop]
    idx = np.where(fr > max(0.012, np.percentile(fr, 95)*0.06))[0]
    burn[-1] = xb[max(0, idx[0]*hop - int(0.05*SR)): idx[-1]*hop + int(0.08*SR)]
    print('   fala 17 trocada pela versão regravada')
mana = split(load(sys.argv[2]), TEXT['M'])
# nivela cada fala: o Mana fala baixo e calmo, então sobe até ficar no mesmo volume do Burn
def level(seg, target=0.11):
    hop = int(0.02 * SR); fr = np.sqrt(np.convolve(seg ** 2, np.ones(hop) / hop, 'same'))
    act = fr > max(0.01, fr.max() * 0.12)
    rms = np.sqrt((seg[act] ** 2).mean()) if act.any() else 1e-3
    y = seg * np.clip(target / rms, 0.4, 8.0)
    return np.tanh(y * 1.6) / 1.6          # segura os picos sem achatar a voz
burn = [level(x) for x in burn]; mana = [level(x) for x in mana]
order = []
for k in range(len(TEXT['B'])):
    order.append(('B', burn[k], TEXT['B'][k])); order.append(('M', mana[k], TEXT['M'][k]))

t = 0.35; lines = []
for i, (who, seg, txt) in enumerate(order):
    if i: t = lines[-1]['start'] + lines[-1]['dur'] + GAP[i]
    dur = len(seg) / SR
    hop = SR // 12; e = np.array([np.sqrt((seg[j:j + hop] ** 2).mean()) for j in range(0, len(seg) - hop // 2, hop)])
    e = np.clip(e / (np.percentile(e, 90) + 1e-6), 0, 1)
    lines.append(dict(who=who, text=txt, start=round(t, 3), dur=round(dur, 3), env=[round(float(v), 2) for v in e]))
    print(f'{i+1:2d} {who} {t:6.2f}s +{dur:4.2f}s  {txt}')

last = lines[-1]
music_start = MUSIC_BREAK - last['start']
T_SLAM = MUSIC_SLAM - music_start
assert last['start'] + last['dur'] < T_SLAM - 0.05, 'o "Comenta aí" passou da pancada'
T_END = round(T_SLAM + 2.0, 2)
open('data.js', 'w').write('const DATA=' + json.dumps(dict(lines=lines, T_SLAM=round(T_SLAM, 3), T_END=T_END), ensure_ascii=False) + ';')

# ---------- mixagem ----------
n = int(T_END * SR)
voice = np.zeros(n, np.float32)
for l, (_, seg, _) in zip(lines, order):
    a = int(l['start'] * SR); voice[a:a + len(seg)] += seg[:max(0, n - a)]
voice /= np.max(np.abs(voice)) + 1e-9; voice *= 0.85
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{music_start:.3f}', '-t', f'{T_END:.3f}', '-i', 'musica.mp3',
                '-ac', '2', '-ar', str(SR), '_m.wav'], check=True)
w = wave.open('_m.wav'); m = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float32).reshape(-1, 2) / 32768
m = np.pad(m, ((0, max(0, n - len(m))), (0, 0)))[:n]
tt = np.arange(n) / SR
# música de fundo: 4 dB mais baixa que antes nas falas, abaixa mais quando alguém fala, sobe na abertura e no fecho
env = np.convolve(np.abs(voice), np.ones(int(0.12 * SR)) / int(0.12 * SR), 'same')
duck = 1 - 0.40 * np.clip(env / (np.percentile(env, 95) + 1e-9), 0, 1)
g = 0.125 * duck
op = np.clip((lines[0]['start'] - tt) / 0.25, 0, 1); g = g * (1 - op) + 0.42 * op
up = np.clip((tt - T_SLAM) / 0.2, 0, 1); g = g * (1 - up) + 0.62 * up
g *= np.clip(tt / 0.15, 0, 1) * np.clip((T_END - tt) / 0.45, 0, 1)
import sfx
import os
INS = [tuple(x) for x in EPI.get('ins', [])] if os.path.exists('cards/island.png') else []
import re
shots = re.findall(r"'(wide|tv|tvtext|tvtext2|tv2|cuM|cuB|push)'\]", open('episode.js', encoding='utf-8').read())
TVS = ('tv', 'tvtext', 'tvtext2', 'tv2')
cuts = [lines[k]['start'] for k in range(len(lines)) if shots[k] in TVS and (k == 0 or shots[k - 1] not in TVS)]
cuts = [c for c in cuts if c > 0.2]
sh = next((l['start'] + l['dur'] * 0.6 for l in lines if 'embaralh' in l['text']), None)
fxt = sfx.track(n, SR, lines, T_SLAM, [lines[k]['start'] + lines[k]['dur'] * a for k, a in INS], cuts, sh)
mix = m * g[:, None] + voice[:, None] + fxt
mix /= np.max(np.abs(mix)) * 1.05
with wave.open('_mix.wav', 'wb') as o:
    o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR); o.writeframes((mix * 32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', '_mix.wav', '-af', 'loudnorm=I=-14:TP=-1:LRA=11', '-ar', str(SR), 'trilha_final.wav'], check=True)
print(f'música de {music_start:.2f}s a {music_start + T_END:.2f}s · pancada (TV desliga) em {T_SLAM:.2f}s · fim {T_END}s')
