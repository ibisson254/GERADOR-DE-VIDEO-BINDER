#!/usr/bin/env python3
"""EP05 · simulações específicas de mecânicas de Star Trek. Goldfish = sem oponente: são TETOS, não previsões de jogo.
Saída: resultados/sim.json"""
import json, os, sys, re, collections, statistics
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cartas import CARTAS
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rng = np.random.default_rng(2266)
M = int(sys.argv[1]) if len(sys.argv) > 1 else 300000
R = {}
def vistas(t, cm): return 7 + (t - 1 if cm else t)
# ---- A. Strange New Worlds: nomes diferentes de terreno em jogo no turno t (assume jogar todo terreno que comprar)
def snw(lands, t, cm=True, fontes=None):
    """lands: lista de (nome, cópias). Devolve E[X], P(X>=3), P(>=4) e, se fontes=(A,B), P(ambas as cores até T3)."""
    deck = []
    for i, (n, k) in enumerate(lands): deck += [i] * k
    deck += [-1] * (40 - len(deck)); deck = np.array(deck)
    o = np.argsort(rng.random((M, 40)), axis=1)[:, :vistas(t, cm)]
    c = deck[o]; X = np.zeros(M); nt = (c >= 0).sum(1)
    # em jogo: até t terrenos (1 por turno); ordem de jogo prioriza nomes novos (melhor caso)
    dist = np.zeros(M)
    for i in range(len(lands)): dist += (c == i).any(1)
    X = np.minimum(dist, np.minimum(nt, t))
    return dict(media=round(float(X.mean()), 3), p3=round(float((X >= 3).mean() * 100), 2), p4=round(float((X >= 4).mean() * 100), 2))
def cores(lands, a, b, t=3, cm=True):
    deck = []
    for i, (n, k) in enumerate(lands): deck += [i] * k
    deck += [-1] * (40 - len(deck)); deck = np.array(deck)
    o = np.argsort(rng.random((M, 40)), axis=1)[:, :vistas(t, cm)]; c = deck[o]
    return round(float((np.isin(c, a).any(1) & np.isin(c, b).any(1)).mean() * 100), 2)
base = [('Forest', 9), ('Island', 8)]
pool = [('Forest', 7), ('Island', 6), ('Planeta GU', 1), ('Planeta 2', 1), ('Anomalia', 1), ('Unexplored', 1)]
boxes = [('Forest', 6), ('Island', 5), ('Plains', 1), ('Mountain', 1), ('Swamp', 1), ('Planeta GU', 1), ('Planeta 2', 1), ('Anomalia', 1)]
R['snw'] = {'9F+8I': {f'T{t}': snw(base, t) for t in (4, 6, 8)}, 'pool_4_nomes': {f'T{t}': snw(pool, t) for t in (4, 6, 8)}, 'pool_mais_basicos': {f'T{t}': snw(boxes, t) for t in (4, 6, 8)}}
R['snw']['cores_T3'] = {'9F+8I': cores(base, [0], [1]), 'pool_4_nomes': cores(pool, [0, 2], [1, 2]), 'pool_mais_basicos': cores(boxes, [0, 5], [1, 5])}
# ---- B. Federation: tipos distintos entre criaturas não-Borg
tp = []
for c in CARTAS:
    if 'Creature' in c['t'] and '—' in c['t'] and c['r'] in 'CU' and 'Borg' not in c['t']:
        tp.append(set(c['t'].split('—')[1].split()))
F = {}
for k in (1, 2, 3, 4, 5):
    amos = [len(set().union(*[tp[i] for i in rng.choice(len(tp), k, replace=False)])) for _ in range(40000)]
    F[k] = round(float(np.mean(amos)), 3)
R['federation'] = dict(tipos_media_por_n_criaturas=F, media_tipos_por_criatura=round(statistics.mean(len(t) for t in tp), 3), n=len(tp),
                       comuns=collections.Counter(x for t in tp for x in t).most_common(8))
# ---- C. Poder total 8: goldfish com a curva real de corpos W/R de comum+incomum (poder médio por custo, do Oracle)
wr = [c for c in CARTAS if c['r'] in 'CU' and 'Creature' in c['t'] and c['cores_set'] <= {'W', 'R'} and c['p'] not in (None, '*') and not c['terreno']]
pmc = {}
for c in wr:
    k = min(int(c['cmc']), 6); pmc.setdefault(k, []).append(float(c['p']))
mp = {k: round(statistics.mean(v), 3) for k, v in sorted(pmc.items())}
R['poder8_poder_medio_por_custo'] = mp; R['poder8_n_corpos'] = {k: len(v) for k, v in sorted(pmc.items())}
def goldfish(curva, L=17, alvo=8, cm=True, n=100000, maxt=8):
    """curva = {custo: cópias}. Cada turno: joga terreno, depois lança o maior custo possível repetidamente. Conta poder em mesa antes do ataque."""
    deck = [('L', 0)] * L
    for c, k in curva.items(): deck += [('C', c)] * k
    deck += [('X', 0)] * (40 - len(deck))
    arr_t = np.array([0 if d[0] == 'L' else (1 if d[0] == 'C' else 2) for d in deck]); arr_c = np.array([d[1] for d in deck])
    hits = np.zeros(maxt + 1)
    for _ in range(n):
        o = rng.permutation(40); mao = list(o[:7]); pos = 7; terra = 0; poder = 0.0; ok = False
        for t in range(1, maxt + 1):
            if t > 1 or not cm: mao.append(o[pos]); pos += 1
            ts = [i for i in mao if arr_t[i] == 0]
            if ts: mao.remove(ts[0]); terra += 1
            mana = terra
            cs = sorted([i for i in mao if arr_t[i] == 1], key=lambda i: -arr_c[i])
            for i in cs:
                if arr_c[i] <= mana:
                    mana -= arr_c[i]; mao.remove(i); poder += mp.get(min(int(arr_c[i]), 6), 3.0)
            if poder >= alvo: ok = True
            if ok: hits[t] += 1
    return {f'T{t}': round(hits[t] / n * 100, 2) for t in range(3, maxt + 1)}
R['poder8_goldfish_jogando'] = goldfish({2: 6, 3: 5, 4: 3, 5: 2})
R['poder8_goldfish_comprando'] = goldfish({2: 6, 3: 5, 4: 3, 5: 2}, cm=False)
R['poder8_goldfish_lento'] = goldfish({2: 3, 3: 5, 4: 4, 5: 3})
# ---- D. Station: tabela real das naves
nv = []
for c in CARTAS:
    if 'Spacecraft' in c['t']:
        o = c['o']; lim = re.findall(r'(\d+)\+ \|', o); etb = bool(re.search(r'enters', re.sub(r'\([^)]*\)', '', o)))
        nv.append(dict(n=c['n'], r=c['r'], cmc=c['cmc'], lim=[int(x) for x in lim], etb=etb, nota=c['nota']))
R['naves'] = nv
for r_ in ('CU', 'RM'):
    L = [n for n in nv if n['r'] in r_]
    print(r_, len(L), 'etb', sum(n['etb'] for n in L), 'lim', statistics.mean(max(n['lim']) for n in L if n['lim']))
# ---- E. Remoção que acerta nave por estacionar
rm = [c for c in CARTAS if c['r'] in 'CU' and 'remocao' in c['f']]
hit = [c['n'] for c in rm if 'anti_artefato' in c['f']]
R['remocao_cu'] = dict(total=len(rm), acerta_nave_parada=hit)
R['anti_art_cu'] = [c['n'] for c in CARTAS if c['r'] in 'CU' and 'anti_artefato' in c['f']]
json.dump(R, open(f'{D}/resultados/sim.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in R.items() if k != 'naves'}, ensure_ascii=False, indent=0))
