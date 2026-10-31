"""Prepara as falas do especial: corta cada fala da faixa da personagem, encurta silêncios internos (respiro)
e acelera sem mudar o timbre (atempo), como no kit do Mana & Burn / TUBO / Conde.
- B e M: cortes em roteiro.json ('fonte').
- K e T: se existir vozes/conde_raw.mp3 / vozes/tubo_raw.mp3, corta pelos N-1 maiores silêncios (N = falas da personagem).
  Sem a faixa, a fala fica como PRÉVIA, com duração estimada pelo nº de palavras.
Saída: linhas/<id>.wav (48 kHz mono) e linhas.json {id: {dur, previa, env}}.
uso: python3 vozes.py
"""
import json, subprocess, pathlib, re, numpy as np
R = json.load(open('roteiro.json'))
SR = 48000
TEMPO = {'B': 1.10, 'M': 1.15, 'K': 1.08, 'T': 1.10}     # kit: B 1.06, M 1.12-1.15, Conde 1.08, TUBO 1.10
RESPIRO = {'B': 0.14, 'M': 0.14, 'K': 0.30, 'T': 0.20}  # silêncio interno máximo (o Conde precisa das pausas cómicas)
RAW = {'B': 'vozes/burn_raw.mp3', 'M': 'vozes/mana_raw.mp3', 'K': 'vozes/conde_raw.mp3', 'T': 'vozes/tubo_raw.mp3'}
RATE = {'K': 2.9, 'T': 3.3}                            # palavras/s depois do atempo (estimativa para a PRÉVIA)
out = pathlib.Path('linhas'); out.mkdir(exist_ok=True)

def load(p):
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(pcm, np.int16).astype(np.float32) / 32768

def silences(x, thr_db=-38, min_d=0.22):
    win = int(0.01 * SR); n = len(x) // win
    rms = np.sqrt((x[:n * win].reshape(n, win) ** 2).mean(1) + 1e-12); db = 20 * np.log10(rms)
    q = db < thr_db; res = []; i = 0
    while i < n:
        if q[i]:
            j = i
            while j < n and q[j]: j += 1
            if (j - i) * 0.01 >= min_d: res.append((i * 0.01, j * 0.01))
            i = j
        else: i += 1
    return res

def respiro(x, mx):
    keep = []; last = 0
    for a, b in silences(x, -38, mx + 0.02):
        if a < 0.05 or b > len(x) / SR - 0.05: continue
        keep.append(x[int(last * SR):int((a + mx / 2) * SR)]); last = b - mx / 2
    keep.append(x[int(last * SR):]); return np.concatenate(keep)

def trim(x, thr=-45):
    win = int(0.005 * SR); n = len(x) // win
    db = 20 * np.log10(np.sqrt((x[:n * win].reshape(n, win) ** 2).mean(1) + 1e-12))
    idx = np.where(db > thr)[0]
    if not len(idx): return x
    a = max(0, idx[0] * win - int(0.03 * SR)); b = min(len(x), (idx[-1] + 1) * win + int(0.06 * SR)); return x[a:b]

def atempo(x, f, path):
    tmp = path.with_suffix('.raw.wav'); write(tmp, x)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(tmp), '-af', f'atempo={f}', '-ar', str(SR), '-ac', '1', str(path)], check=True)
    tmp.unlink()

def write(p, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes()
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 's16le', '-ar', str(SR), '-ac', '1', '-i', '-', str(p)], input=pcm, check=True)

def env12(p):   # envelope a 12 Hz (boca do Mana & Burn) e a 30 fps (LED do TUBO)
    x = load(str(p)); e = {}
    for k, hz in (('env', 12), ('env30', 30)):
        w = SR // hz; n = len(x) // w
        r = np.sqrt((x[:n * w].reshape(n, w) ** 2).mean(1)); r = r / (np.percentile(r, 95) + 1e-9)
        e[k] = [round(float(min(1, v)), 2) for v in r]
    return e

info = {}
cache = {}
for q in 'BMKT':
    falas = [f for f in R['falas'] if f['quem'] == q and not f.get('so_ecra')]
    raw = pathlib.Path(RAW[q])
    if raw.exists(): cache[q] = load(str(raw))
    if q in 'KT' and q in cache:     # corta pelos N-1 maiores silêncios
        x = cache[q]; s = sorted(silences(x, -38, 0.25), key=lambda p: p[1] - p[0], reverse=True)[:len(falas) - 1]
        cuts = sorted(s); bounds = [0.0] + [c for p in cuts for c in p] + [len(x) / SR]
        for k, f in enumerate(falas): f['fonte'] = [bounds[2 * k], bounds[2 * k + 1]]
    for f in falas:
        p = out / f"{f['id']}.wav"
        if 'fonte' in f and q in cache:
            a, b = f['fonte']; x = trim(cache[q][int(a * SR):int(b * SR)])
            x = respiro(x, RESPIRO[q]); atempo(x, TEMPO[q], p)
            d = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)]))
            info[f['id']] = dict(dur=round(d, 3), previa=False, **env12(p))
        else:
            txt = re.sub(r'[*]', '', f['legenda']); words = len(txt.split())
            d = round(words / RATE[q] + 0.2 * txt.count('.') + 0.15, 2)
            info[f['id']] = dict(dur=d, previa=True, env=[], env30=[])
            if p.exists(): p.unlink()
for f in R['falas']:
    if f.get('so_ecra'): info[f['id']] = dict(dur=1.0, previa=False, env=[], env30=[], so_ecra=True)
json.dump(info, open('linhas.json', 'w'))
for f in R['falas']:
    i = info[f['id']]; print(f"{f['id']:4} {f['quem']} {i['dur']:5.2f}s {'PRÉVIA' if i['previa'] else 'voz'}  {f['legenda'][:60]}")
print('fala total:', round(sum(i['dur'] for i in info.values()), 2), 's')
