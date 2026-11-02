"""Corte das faixas do ElevenLabs nas pausas (usado pelo process.py e pelo escolher_tomadas.py)."""
import subprocess, wave
import numpy as np

SR = 44100

def load(path):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '_t.wav'], check=True)
    w = wave.open('_t.wav'); x = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float32) / 32768
    return x

def split(x, texts, quiet=False):
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
    for k, (a, b) in enumerate(bounds):
        if not quiet: print(f'   {texts[k][:30]:30s} {a*0.01:6.2f}-{b*0.01:6.2f}s')
    return [x[max(0, a * hop - pad): b * hop + pad] for a, b in bounds]
