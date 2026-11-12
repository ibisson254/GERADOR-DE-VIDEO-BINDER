#!/usr/bin/env python3
"""EP05 · engenharia de probabilidades. Fórmulas exatas (hipergeométrica, multivariada) + Monte Carlo de confirmação.
Baralho de 40 cartas, sem mão suavizada (pré-release é papel; o Bo1 do Arena suaviza a mão, por isso os números não valem lá).
Cartas vistas até o fim da compra do turno t: JOGANDO 7+(t-1), COMPRANDO 7+t. Mão inicial = 7.
Mulligans calculados à parte, nunca misturados com os cenários sem mulligan. Saída: resultados/prob.json + resultados/prob.md"""
from math import comb
from fractions import Fraction as Fr
import itertools, json, os, sys
import numpy as np
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N = 40
def vistas(t, comeca=True): return 7 + (t - 1 if comeca else t)
def hg_ge(N_, K, n, k=1):
    """P(X>=k), X~Hipergeométrica(N_ cartas, K sucessos, n vistas)."""
    tot = comb(N_, n)
    return Fr(sum(comb(K, i) * comb(N_ - K, n - i) for i in range(k, min(K, n) + 1)), tot)
def mv_ge(N_, grupos, n):
    """P(todas as exigências) numa multivariada: grupos=[(K_i, k_i)...]; o resto do baralho é indiferente."""
    resto = N_ - sum(K for K, _ in grupos); tot = 0
    faixas = [range(k, min(K, n) + 1) for K, k in grupos]
    for xs in itertools.product(*faixas):
        s = sum(xs)
        if s > n: continue
        v = comb(resto, n - s)
        for (K, _), x in zip(grupos, xs): v *= comb(K, x)
        tot += v
    return Fr(tot, comb(N_, n))
def pct(x, c=2): return round(float(x) * 100, c)
R = {}
# --- A. Abertura de boosters: colação oficial (Wizards, Collecting Star Trek)
# Taxas publicadas por booster, só carta do set principal; variantes "<1%" ficam de fora: os valores são pisos.
RM = dict(rara=.801, mitica=.124); WILD = dict(rara=.167, mitica=.026); FOIL = dict(rara=.063, mitica=.010)
NR, NM = 80, 25
def p_esp(tipo, boosters=6, nsel=None):
    n = nsel or (NR if tipo == 'rara' else NM)
    falha = (1 - RM[tipo] / n) * (1 - WILD[tipo] / n) * (1 - FOIL[tipo] / n)
    return 1 - falha ** boosters
def p_any(tipo, boosters=6):
    falha = (1 - RM[tipo]) * (1 - WILD[tipo]) * (1 - FOIL[tipo])
    return 1 - falha ** boosters
pb1 = 1 - (1 - .167 - .026) * (1 - .063 - .010)                        # 2.ª rara/mítica num booster (coringa ou foil), piso
A = {'rara_especifica_booster': pct(p_esp('rara', 1), 3), 'rara_especifica_6': pct(p_esp('rara')),
     'mitica_especifica_booster': pct(p_esp('mitica', 1), 3), 'mitica_especifica_6': pct(p_esp('mitica')),
     'qualquer_mitica_booster_piso': pct(p_any('mitica', 1)), 'qualquer_mitica_6_piso': pct(p_any('mitica')),
     'qualquer_rara_ou_mitica_6': 100.0, 'booster_com_2+_raras_piso': pct(pb1)}
# nº esperado de raras+míticas em 6 boosters: 6 da vaga garantida + coringa + foil (piso)
A['raras_miticas_esperadas_6_piso'] = round(6 * (1 + .193 + .073), 3)
from math import comb as C
A['6boosters_0_extras_piso'] = pct((1 - pb1) ** 6)
A['6boosters_2+_extras_piso'] = pct(1 - (1 - pb1) ** 6 - 6 * pb1 * (1 - pb1) ** 5)
A['stardates_6_boosters'] = pct(1 - (24 / 25) ** 6)
A['vaga_rara_mitica_mitica_oficial'] = 12.4
A['dual_especifico_6'] = pct(1 - (1 - .05) ** 6)
R['abertura'] = A
# --- B. Consistência: k cópias em 40, por turno, começando e comprando
TT = [('mao', 7), *[(f'T{t}', None) for t in range(2, 7)]]
B = {'jogando': {}, 'comprando': {}}
for k in range(1, 9):
    for lado, cm in (('jogando', True), ('comprando', False)):
        l = {'mao': pct(hg_ge(N, k, 7))}
        for t in range(2, 9): l[f'T{t}'] = pct(hg_ge(N, k, vistas(t, cm)))
        B[lado][k] = l
R['copias'] = B
# --- C. Terrenos e curva
Cv = {}
for L in (16, 17, 18):
    x = {}
    for lado, cm in (('jogando', True), ('comprando', False)):
        x[lado] = {f'>={k}T_T{k}': pct(hg_ge(N, L, vistas(k, cm), k)) for k in (2, 3, 4, 5, 6)}
        x[lado]['mao_2a5'] = pct(sum(Fr(comb(L, i) * comb(N - L, 7 - i), comb(N, 7)) for i in range(2, 6)))
    Cv[L] = x
R['terrenos'] = Cv
# carta de custo 2 no T2: >=2 terrenos e >=1 carta de custo 2 entre as vistas
Cd = {}
for L in (16, 17, 18):
    for d2 in (3, 5, 7, 8, 9):
        Cd[f'{L}T_{d2}c2'] = {lado: pct(mv_ge(N, [(L, 2), (d2, 1)], vistas(2, cm))) for lado, cm in (('jogando', True), ('comprando', False))}
R['dois_drop_T2'] = Cd
# curva 2-3: custo 2 no T2 e custo 3 no T3 (>=3 terrenos até T3, >=1 c2, >=1 c3, com pelo menos 2 terrenos até T2) -> Monte Carlo em baixo
# cores: 2 cores, fontes A/B
Co = {}
for a, b, dual in ((9, 8, 0), (8, 8, 1), (8, 7, 2), (7, 7, 3), (10, 7, 0)):
    for lado, cm in (('jogando', True), ('comprando', False)):
        for t in (2, 3, 4, 5):
            n = vistas(t, cm)
            # P(>=1 fonte de A e >=1 fonte de B); dual conta para as duas
            so_a, so_b = a, b
            tot = 0
            resto = N - so_a - so_b - dual
            for x in range(0, min(so_a, n) + 1):
                for y in range(0, min(so_b, n - x) + 1):
                    for z in range(0, min(dual, n - x - y) + 1):
                        if (x + z >= 1) and (y + z >= 1):
                            tot += comb(so_a, x) * comb(so_b, y) * comb(dual, z) * comb(resto, n - x - y - z)
            Co[f'{a}+{b}+{dual}d_{lado}_T{t}'] = pct(Fr(tot, comb(N, n)))
R['duas_cores'] = Co
# custo duplo CC no T4 com 9 ou 8 fontes; splash com 2,3,4 fontes até T6/T8
Du = {}
for s in (7, 8, 9, 10):
    Du[f'CC_{s}fontes_T4'] = {lado: pct(hg_ge(N, s, vistas(4, cm), 2)) for lado, cm in (('jogando', True), ('comprando', False))}
for s in (2, 3, 4):
    Du[f'splash_{s}fontes'] = {f'T{t}': {lado: pct(hg_ge(N, s, vistas(t, cm))) for lado, cm in (('jogando', True), ('comprando', False))} for t in (6, 8)}
R['fontes'] = Du
# --- D. Sinergias
Sy = {}
for t in (4, 5, 6, 8):
    for lado, cm in (('jogando', True), ('comprando', False)):
        n = vistas(t, cm); s = {}
        s['bomba_1_copia'] = pct(hg_ge(N, 1, n))
        s['combo_2pecas_1_1'] = pct(mv_ge(N, [(1, 1), (1, 1)], n))              # A+B, uma cópia de cada
        s['2_de_3_pecas_unicas'] = pct(hg_ge(N, 3, n, 2))                        # duas quaisquer de 3 cartas diferentes, que se ligam entre si
        s['2_de_4_pecas_unicas'] = pct(hg_ge(N, 4, n, 2))
        s['2_de_5'] = pct(hg_ge(N, 5, n, 2)); s['2_de_7'] = pct(hg_ge(N, 7, n, 2)); s['2_de_9'] = pct(hg_ge(N, 9, n, 2))
        s['unico_payoff_8_peças'] = pct(mv_ge(N, [(1, 1), (8, 2)], n))           # 1 payoff exato + 2 peças
        s['3_payoffs_8_peças'] = pct(mv_ge(N, [(3, 1), (8, 2)], n))
        s['4_payoffs_8_peças'] = pct(mv_ge(N, [(4, 1), (8, 2)], n))
        s['5_payoffs_8_peças'] = pct(mv_ge(N, [(5, 1), (8, 2)], n))
        s['>=1_de_7'] = pct(hg_ge(N, 7, n)); s['>=1_de_9'] = pct(hg_ge(N, 9, n))
        Sy[f'T{t}_{lado}'] = s
R['sinergia'] = Sy
# --- E. Monte Carlo de confirmação e mulligan (London): mantém 7 com 2 a 5 terrenos; 6 com 2 a 4; 5 sempre.
rng = np.random.default_rng(1701)
M = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
def sim_sem_mull(L=17, d2=7, d3=6, chave=1, n_t=8):
    # baralho: L terrenos, d2 custo 2, d3 custo 3, chave, resto
    baralho = np.zeros(N, dtype=np.int8)
    baralho[:L] = 1; baralho[L:L + d2] = 2; baralho[L + d2:L + d2 + d3] = 3; baralho[L + d2 + d3:L + d2 + d3 + chave] = 4
    ordem = np.argsort(rng.random((M, N)), axis=1)[:, :15]
    c = baralho[ordem]
    out = {}
    for lado, cm in (('jogando', True), ('comprando', False)):
        v = lambda t: vistas(t, cm)
        chk = lambda val, t: (c[:, :v(t)] == val).sum(1)
        out[f'T5_chave_{lado}'] = pct((chk(4, 5) >= 1).mean())
        ok2 = (chk(1, 2) >= 2) & (chk(2, 2) >= 1)
        ok3 = ok2 & (chk(1, 3) >= 3) & (chk(3, 3) >= 1)
        out[f'c2_T2_{lado}'] = pct(ok2.mean()); out[f'curva_2_3_{lado}'] = pct(ok3.mean())
        ok4 = (chk(1, 4) >= 4)
        out[f'4T_T4_{lado}'] = pct(ok4.mean())
    return out
R['mc_confirmacao'] = sim_sem_mull()
def sim_mulligan(L=17, K=7):
    """London: compra 7, decide; ao mulligan compra 7 de novo e põe 1 no fundo por mulligan. Regra de manutenção fixa (premissa, não conselho)."""
    res = {}
    for lado, cm in (('jogando', True), ('comprando', False)):
        ids = np.arange(N); terreno = ids < L; chave = (ids >= L) & (ids < L + K)
        o1 = np.argsort(rng.random((M, N)), axis=1)
        t7 = terreno[o1[:, :7]].sum(1); keep7 = (t7 >= 2) & (t7 <= 5)
        o2 = np.argsort(rng.random((M, N)), axis=1)
        t6 = terreno[o2[:, :7]].sum(1)                              # 7 cartas, 1 vai ao fundo; escolhe-se o melhor terreno/feitiço
        keep6 = (t6 >= 2) & (t6 <= 5)
        o3 = np.argsort(rng.random((M, N)), axis=1)
        final = np.where(keep7[:, None], o1, np.where(keep6[:, None], o2, o3))
        mao = np.where(keep7, 7, np.where(keep6, 6, 5))
        # botões: ao ficar com menos, põe no fundo a carta mais supérflua: terreno se >=4 terrenos (ou 5+), senão feitiço. Aproximação: não mexe em cartas-chave.
        t5_vistas = vistas(5, cm)
        vista = final[:, :t5_vistas + 7 - mao.min()]
        # conta chave entre as 7 iniciais (com mulligan guardam-se as chaves) + compras
        ch7 = chave[final[:, :7]].sum(1); ch_c = chave[final[:, 7:7 + (t5_vistas - 7)]].sum(1)
        res[f'{lado}'] = {'mantem_7': pct(keep7.mean()), 'vai_a_6': pct((~keep7 & keep6).mean()), 'vai_a_5': pct((~keep7 & ~keep6).mean()),
                          'chave_ate_T5_com_mull': pct(((ch7 + ch_c) >= 1).mean()), 'chave_ate_T5_sem_mull_mesma_regra': pct(hg_ge(N, K, t5_vistas))}
    return res
R['mulligan_17T_7chaves'] = sim_mulligan()
R['mulligan_17T_1chave'] = sim_mulligan(K=1)
# --- F. Testes de sanidade (casos extremos)
assert hg_ge(40, 0, 7) == 0 and hg_ge(40, 40, 7) == 1
assert hg_ge(40, 1, 40) == 1
assert hg_ge(40, 1, 11) == Fr(11, 40)
assert mv_ge(40, [(40, 7)], 7) == 1
assert abs(float(mv_ge(40, [(17, 2), (7, 1)], 8)) - R['mc_confirmacao']['c2_T2_jogando'] / 100) < 0.003
json.dump(R, open(f'{D}/resultados/prob.json', 'w'), ensure_ascii=False, indent=1)
# pilot EP00 (60 cartas, 24 terrenos): recálculo
ep00 = {'2o_terreno_T2': pct(Fr(23, 53)), '3T_T3_duas_compras': pct(Fr(23, 53) * Fr(22, 52)), 'mao_1_terreno': pct(Fr(comb(24, 1) * comb(36, 6), comb(60, 7)))}
print(json.dumps({'abertura': A, 'ep00': ep00, 'mc': R['mc_confirmacao'], 'mull': R['mulligan_17T_7chaves'], 'mull1': R['mulligan_17T_1chave']}, indent=1, ensure_ascii=False))
print('bomba/T5:', Sy['T5_jogando']); print('T5 comprando', Sy['T5_comprando']); print('T6 jog', Sy['T6_jogando'])
print('terrenos 17 jogando', Cv[17]['jogando'], 'comprando', Cv[17]['comprando']); print('16', Cv[16]['jogando']); print('18', Cv[18]['jogando'])
print('d2', Cd)
print({k: v for k, v in Co.items() if 'T3' in k or 'T4' in k})
print(Du)
print(B['jogando'][1], B['jogando'][7], B['comprando'][7])
