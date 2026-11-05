#!/usr/bin/env python3
"""EP05 · robustez do ranking de pares às notas: perturba cada nota com ruído N(0, 0,5) por réplica (a crítica é pré-lançamento) e refaz o deck-modelo.
Saída: resultados/robustez.json"""
import json, os, sys, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = [sys.argv[0], '1']
import pools as PL
rng = np.random.default_rng(1701)
REPL, N = 30, 2500
base = PL.nota.copy(); cont = {p: [] for p in PL.PARES}
for rep in range(REPL):
    nt = base + rng.normal(0, .5, len(base)); PL.rng = np.random.default_rng(rep); mel = collections.Counter()
    for _ in range(N):
        pl = PL.pool(); cnt = np.bincount(np.array(pl), minlength=len(PL.CARTAS)); sc = {}
        for par in PL.PARES:
            ids = np.repeat(np.arange(len(PL.CARTAS)), cnt * PL.mask[par])
            if len(ids) == 0: continue
            n = nt[ids]; o = ids[np.argsort(-n, kind='stable')]
            cps = [i for i in o if PL.corpo[i]][:13]; r = list(o)
            for i in cps: r.remove(i)
            d = np.array(cps + r[:23 - len(cps)]); sc[par] = nt[d].mean()
        mel[max(sc, key=sc.get)] += 1
    for p in PL.PARES: cont[p].append(mel[p] / N * 100)
out = {p: dict(media=round(float(np.mean(v)), 2), p5=round(float(np.percentile(v, 5)), 2), p95=round(float(np.percentile(v, 95)), 2)) for p, v in cont.items()}
json.dump(out, open(f'{PL.D}/resultados/robustez.json', 'w'), indent=1)
print(sorted(out.items(), key=lambda kv: -kv[1]['media']))
