#!/usr/bin/env python3
"""EP05 · Monte Carlo de pools de Sealed de Star Trek com a colação oficial (Wizards, Collecting Star Trek).
Modelo, não dados de jogo: mostra a DISPONIBILIDADE de cartas em 6 Play Boosters, não win rate.
Premissas (registadas para auditoria):
 - Booster: 7 comuns (6 em 1 de cada 25: Stardates), 3 incomuns, 1 coringa, 1 rara/mítica, 1 foil, 1 terreno = 14 cartas. Sem repetição dentro da vaga de comuns/incomuns.
 - Variantes visuais contam como a carta base. Taxas "<1%" da Wizards: o resíduo de cada vaga vai para rara/mítica na proporção 8:1 (coringa, foil) ou fica na vaga R/M.
 - Cada rara principal e cada mítica principal têm a mesma taxa dentro da sua raridade (a Wizards não publica por carta).
 - Vaga de terreno: 50% dual comum (10 Planetas), 50% básico. Promo do pré-release fica de fora (raridade rara ou mítica; distribuição não publicada).
 - Stardates: não modelada (a Wizards não dá lista por raridade para Limited; 1 em 25 boosters).
Deck-modelo por par: 23 mágicas: as 13 melhores criaturas/naves por nota, depois as melhores restantes. Nota = crítica pré-lançamento, não desempenho."""
import json, os, sys, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cartas import CARTAS, PARES, NOME_PAR, PLANO, MECH_PAR, ROTULO, do_par
from math import comb
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N_POOLS = int(sys.argv[1]) if len(sys.argv) > 1 else 40000
rng = np.random.default_rng(1966)
idx = {c['n']: i for i, c in enumerate(CARTAS)}
PLANETAS = [i for i, c in enumerate(CARTAS) if 'Planet' in c['t']]
COMUNS = [i for i, c in enumerate(CARTAS) if c['r'] == 'C' and i not in PLANETAS]
INC = [i for i, c in enumerate(CARTAS) if c['r'] == 'U']
RAR = [i for i, c in enumerate(CARTAS) if c['r'] == 'R']
MIT = [i for i, c in enumerate(CARTAS) if c['r'] == 'M']
assert len(COMUNS) == 81 and len(INC) == 110 and len(RAR) == 80 and len(MIT) == 25 and len(PLANETAS) == 10
# coringa: C 20.8+~0.4 | U 54.1+1+1.5+1 | R 16.7+resto | M 2.6+resto
def norm(a): a = np.array(a, float); return a / a.sum()
P_WILD = norm([21.2, 57.6, 18.4, 2.8]); P_FOIL = norm([51.6, 38.4, 8.8, 1.2]); P_RM = norm([86.8, 13.2])
def pick(r): 
    L = (COMUNS, INC, RAR, MIT)[r]; return L[rng.integers(len(L))]
def booster():
    n_c = 6 if rng.random() < 1 / 25 else 7
    p = list(rng.choice(COMUNS, n_c, replace=False)) + list(rng.choice(INC, 3, replace=False))
    p.append(pick(rng.choice(4, p=P_WILD)))
    p.append(RAR[rng.integers(80)] if rng.random() < P_RM[0] else MIT[rng.integers(25)])
    p.append(pick(rng.choice(4, p=P_FOIL)))
    if rng.random() < .5: p.append(PLANETAS[rng.integers(10)])
    return p
def pool():
    out = []
    for _ in range(6): out += booster()
    return out
nota = np.array([(c['nota'] if c['nota'] is not None else 2.5) for c in CARTAS])
corpo = np.array([('Creature' in c['t']) or ('Spacecraft' in c['t']) for c in CARTAS])
crit = np.array(['Creature' in c['t'] for c in CARTAS]); cmc = np.array([c['cmc'] for c in CARTAS])
rem = np.array(['remocao' in c['f'] for c in CARTAS]); dura = np.array(['remocao_dura' in c['f'] for c in CARTAS])
anti = np.array(['anti_artefato' in c['f'] for c in CARTAS])
mask = {p: np.array([do_par(c, p) for c in CARTAS]) for p in PARES}
E = {k: np.array([k in c['e'] for c in CARTAS]) for k in ROTULO}; P = {k: np.array([k in c['pay'] for c in CARTAS]) for k in ROTULO}
REQ = dict(borg=2, nave=2, klingon=2, naocriatura=2, dilemma=2, landfall=0, marcadores=1, cemiterio=1, poder8=2, snw=0)
def motor(so_pay, ambos, so_peca, req, vistas=11, N=40):
    """P(>=1 payoff e >=req OUTRAS peças) em `vistas` cartas de 40. `ambos` = cartas que são payoff e peça: uma delas pode ser o payoff, as outras contam como peça."""
    tot = 0; rest = N - so_pay - ambos - so_peca
    for a in range(0, min(so_pay, vistas) + 1):
        for b in range(0, min(ambos, vistas - a) + 1):
            for c in range(0, min(so_peca, vistas - a - b) + 1):
                if a + b == 0: continue
                pecas = b + c if a >= 1 else b - 1 + c
                if pecas < req: continue
                tot += comb(so_pay, a) * comb(ambos, b) * comb(so_peca, c) * comb(rest, vistas - a - b - c)
    return tot / comb(N, vistas)
if __name__ == '__main__':
    res = {p: collections.defaultdict(list) for p in PARES}; melhor = collections.Counter(); pool_stats = collections.defaultdict(list)
    for it in range(N_POOLS):
        pl = pool(); arr = np.array(pl); cnt = np.bincount(arr, minlength=len(CARTAS))
        pool_stats['mit'].append(sum(1 for i in pl if CARTAS[i]['r'] == 'M')); pool_stats['rar'].append(sum(1 for i in pl if CARTAS[i]['r'] in 'RM'))
        pool_stats['planetas'].append(sum(1 for i in pl if i in PLANETAS))
        pool_stats['n'].append(len(pl))
        nb = len({i for i in pl if CARTAS[i]['terreno']})
        pool_stats['terrenos_nomes'].append(nb)
        scores = {}
        for par in PARES:
            m = mask[par]; ids = np.repeat(np.arange(len(CARTAS)), cnt * m)
            if len(ids) == 0: continue
            n = nota[ids]; jog = (n >= 2.0).sum()
            # deck-modelo
            ordem = ids[np.argsort(-n, kind='stable')]
            corpos = [i for i in ordem if corpo[i]][:13]
            resto = list(ordem); 
            for i in corpos: resto.remove(i)
            deck = corpos + resto[:23 - len(corpos)]; deck = np.array(deck)
            media = nota[deck].mean(); scores[par] = media
            k = MECH_PAR[par]
            r = res[par]
            r['jog'].append(jog); r['23jog'].append(jog >= 23)
            r['media'].append(media); r['bomba'].append((nota[ids] >= 4).sum()); 
            r['rem'].append(rem[ids].sum()); r['rem_d'].append(dura[ids].sum()); r['anti'].append(anti[ids].sum())
            r['crit'].append(crit[ids].sum()); r['c2'].append(((cmc[ids] <= 2) & corpo[ids]).sum())
            r['E'].append(E[k][ids].sum()); r['P'].append(P[k][ids].sum())
            # no deck
            # peça certa por plano: sacrifício come qualquer corpo; a nave é o payoff e os corpos é que a estacionam
            pecas = corpo if k in ('klingon', 'nave') else E[k]
            pay_ = E['nave'] if k == 'nave' else P[k]
            so_pay = (pay_[deck] & ~pecas[deck]).sum(); ambos = (pay_[deck] & pecas[deck]).sum(); so_peca = (pecas[deck] & ~pay_[deck]).sum()
            dp = pay_[deck].sum()
            r['dE'].append(E[k][deck].sum()); r['dP'].append(dp)
            r['motor_T5'].append(motor(int(so_pay), int(ambos), int(so_peca), REQ[k]))
            r['payoff_T5'].append(1 - comb(40 - int(dp), 11) / comb(40, 11))
            r['dcrit'].append(corpo[deck].sum()); r['drem'].append(rem[deck].sum()); r['dbomba'].append((nota[deck] >= 4).sum())
            r['d2'].append(((cmc[deck] <= 2) & corpo[deck]).sum()); r['d5'].append((cmc[deck] >= 5).sum())
            r['indep'].append(((nota[deck] >= 2.5) & ~P[k][deck]).sum())
            r['media_sem_bomba'].append(nota[deck][nota[deck] < 4].mean() if (nota[deck] < 4).any() else np.nan)
        b = max(scores, key=scores.get); melhor[b] += 1
        # a melhor carta do pool cabe no melhor par?
        nl = [i for i in set(pl) if not CARTAS[i]['terreno']]; topo = max(nota[i] for i in nl); tops = [i for i in nl if nota[i] == topo]
        dentro = any(mask[b][i] for i in tops)
        pool_stats['topo'].append(topo); pool_stats['bomba_fora'].append(not dentro)
        pares_com_top = [p for p in PARES if any(mask[p][i] for i in tops) and p in scores]
        melhor_com_top = max((scores[p] for p in pares_com_top), default=np.nan)
        pool_stats['delta_top'].append(scores[b] - melhor_com_top)
        pool_stats['rem_best'].append(res[b]['rem'][-1]); pool_stats['jog_best'].append(res[b]['jog'][-1])
        pool_stats['bomba_ge45'].append(topo >= 4.5)
        res[b]['foi_melhor_media'].append(scores[b])
    out = {}
    def q(v, p): return float(np.percentile(v, p))
    for par in PARES:
        r = res[par]; a = {k: np.array(v, float) for k, v in r.items()}
        out[par] = dict(nome=NOME_PAR[par], plano=PLANO[par], jogaveis=round(a['jog'].mean(), 2), p23=round(a['23jog'].mean() * 100, 1), media_top23=round(a['media'].mean(), 3),
                        bomba_pool=round(a['bomba'].mean(), 2), p_bomba=round((a['bomba'] >= 1).mean() * 100, 1), remocao=round(a['rem'].mean(), 2), p5rem=round((a['rem'] >= 5).mean() * 100, 1),
                        remocao_dura=round(a['rem_d'].mean(), 2), anti=round(a['anti'].mean(), 2), criaturas=round(a['crit'].mean(), 2), corpos_2=round(a['c2'].mean(), 2),
                        E=round(a['E'].mean(), 2), P=round(a['P'].mean(), 2), p_P0=round((a['P'] == 0).mean() * 100, 1), p_P1=round((a['P'] >= 1).mean() * 100, 1), p_P2=round((a['P'] >= 2).mean() * 100, 1), p_P3=round((a['P'] >= 3).mean() * 100, 1),
                        deck_E=round(a['dE'].mean(), 2), deck_P=round(a['dP'].mean(), 2), motor_T5=round(a['motor_T5'].mean() * 100, 1), payoff_T5=round(a['payoff_T5'].mean() * 100, 1), deck_corpos=round(a['dcrit'].mean(), 2), deck_rem=round(a['drem'].mean(), 2),
                        deck_bomba=round(a['dbomba'].mean(), 2), deck_2=round(a['d2'].mean(), 2), deck_5=round(a['d5'].mean(), 2), indep=round(a['indep'].mean(), 2),
                        melhor_pct=round(melhor[par] / N_POOLS * 100, 1), media_sem_bomba=round(float(np.nanmean(a['media_sem_bomba'])), 3))
    geral = {k: round(float(np.nanmean(np.array(v, float))), 3) for k, v in pool_stats.items()}
    geral['p_best_5rem'] = round(float((np.array(pool_stats['rem_best']) >= 5).mean() * 100), 2)
    geral['p_best_23jog'] = round(float((np.array(pool_stats['jog_best']) >= 23).mean() * 100), 2)
    _df = np.array(pool_stats['bomba_fora'], float); _tp = np.array(pool_stats['topo'], float)
    geral['p_bomba_fora'] = round(float(_df.mean() * 100), 2); geral['p_bomba_fora_se_nota_ge4'] = round(float(_df[_tp >= 4].mean() * 100), 2); geral['p_topo_ge4'] = round(float((_tp >= 4).mean() * 100), 2)
    geral['p_bomba_fora_se_nota_ge45'] = round(float(_df[_tp >= 4.5].mean() * 100), 2)
    geral['p_mitica>=1'] = round(float((np.array(pool_stats['mit']) >= 1).mean() * 100), 2)
    geral['n_pools'] = N_POOLS
    # melhor par por pool e número de bombas: quantos pools têm o melhor par por média SEM bomba
    json.dump(dict(geral=geral, pares=out), open(f'{D}/resultados/pools.json', 'w'), ensure_ascii=False, indent=1)
    print(geral)
    print({k:geral[k] for k in geral if k.startswith('p_') or k.startswith('delta')})
    hdr = ['par', 'jog', '%23', 'méd', 'bombas', '%bomba', 'rem', '%5r', 'dura', 'anti', 'E', 'P', '%P=0', '%P≥2', 'dE', 'dP', 'motorT5', 'd2', 'indep', 'melhor%']
    print(' '.join(f'{h:>7s}' for h in hdr))
    for par, o in sorted(out.items(), key=lambda kv: -kv[1]['melhor_pct']):
        print(' '.join(f'{str(v):>7s}' for v in [par, o['jogaveis'], o['p23'], o['media_top23'], o['bomba_pool'], o['p_bomba'], o['remocao'], o['p5rem'], o['remocao_dura'], o['anti'], o['E'], o['P'], o['p_P0'], o['p_P2'], o['deck_E'], o['deck_P'], o['payoff_T5'] if False else o['motor_T5'], o['deck_2'], o['indep'], o['melhor_pct']]))
