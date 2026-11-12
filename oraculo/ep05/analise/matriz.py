#!/usr/bin/env python3
"""EP05 · matriz dos dez planos. Notas 1–5 por min-máx entre os 10 pares (pesos iguais). NÃO é win rate: ainda não há jogos de TRK.
Disponibilidade: % de pools com 23+ jogáveis e % com 2+ payoffs. Potência: média do top 23 e % de pools com bomba (nota ≥ 4).
Consistência: motor ligado até T5 (deck-modelo) e corpos de custo ≤ 2 no deck. Flexibilidade: cartas boas sem ser payoff e % de pools com 5+ remoções.
Boros e Simic: o motor multiplica P(payoff até T5) pelo teto da condição (poder 8 até T5 em goldfish; 3+ nomes de terreno até T6)."""
import json, os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = json.load(open(f'{D}/resultados/pools.json'))['pares']; S = json.load(open(f'{D}/resultados/sim.json')); Rb = json.load(open(f'{D}/resultados/robustez.json'))
aj = {}
for k, o in P.items(): aj[k] = o['motor_T5']
aj['RW'] = round(P['RW']['payoff_T5'] * S['poder8_goldfish_jogando']['T5'] / 100, 1)
aj['GU'] = round(P['GU']['payoff_T5'] * S['snw']['pool_4_nomes']['T6']['p3'] / 100, 1)
def esc(d):
    a, b = min(d.values()), max(d.values()); return {k: 1 + 4 * (v - a) / (b - a) for k, v in d.items()}
def media(*ds): return {k: sum(d[k] for d in ds) / len(ds) for k in ds[0]}
get = lambda f: {k: o[f] for k, o in P.items()}
Dp = media(esc(get('p23')), esc(get('p_P2'))); Po = media(esc(get('media_top23')), esc(get('p_bomba')))
Co = media(esc(aj), esc(get('deck_2'))); Fl = media(esc(get('indep')), esc(get('p5rem')))
T = {k: (Dp[k] + Po[k] + Co[k] + Fl[k]) / 4 for k in P}
ord_ = sorted(P, key=lambda k: -T[k]); M = []
for k in ord_:
    o = P[k]; M.append(dict(par=k, nome=o['nome'], plano=o['plano'], disponibilidade=round(Dp[k], 1), potencia=round(Po[k], 1), consistencia=round(Co[k], 1), flexibilidade=round(Fl[k], 1), total=round(T[k], 2),
                            motor_T5=aj[k], remocao_pool=o['remocao'], p5rem=o['p5rem'], payoffs_pool=o['P'], melhor_modelo=Rb[k]['media'], banda=[Rb[k]['p5'], Rb[k]['p95']], confianca='média-baixa' if Rb[k]['p5'] > 10 else 'baixa'))
json.dump(M, open(f'{D}/resultados/matriz.json', 'w'), ensure_ascii=False, indent=1)
for m in M: print(m)
