#!/usr/bin/env python3
"""EP05 · auditoria matemática independente: recalcula os números do vídeo por outro caminho (fórmula fechada ou simulação própria) e compara."""
import csv, json, os, sys
from math import comb
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cartas as C
import pools as PL
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rng = np.random.default_rng(42); N = 3_000_000
ok = []
def chk(nome, a, b, tol):
    s = 'OK ' if abs(a - b) <= tol else 'ERRO'; ok.append(s == 'OK '); print(f'{s} {nome}: {a:.3f} vs {b:.3f}')
P = json.load(open(f'{D}/resultados/prob.json')); Q = json.load(open(f'{D}/resultados/pools.json')); M = json.load(open(f'{D}/resultados/matriz.json'))
# 1 mítica específica: simula vagas
R = rng.random((N, 6, 3)); hit = (R[:, :, 0] < .124 / 25) | (R[:, :, 1] < .026 / 25) | (R[:, :, 2] < .010 / 25)
chk('mítica específica em 6 boosters (%)', hit.any(1).any(1).mean() * 100 if False else hit.any(1).mean() * 100, P['abertura']['mitica_especifica_6'], .05)
# 2 uma cópia até T5, jogando: 11/40
chk('1 cópia T5 jogando', 11 / 40 * 100, P['sinergia']['T5_jogando']['bomba_1_copia'], 1e-9)
chk('produto = 1 em 96', 1 / (P['abertura']['mitica_especifica_6'] / 100 * .275), 96.4, .5)
# 3 sete cópias
chk('7 cópias T5', (1 - comb(33, 11) / comb(40, 11)) * 100, P['sinergia']['T5_jogando']['>=1_de_7'], .01)
# 4 motor por simulação direta
def sim(np_, ne, n=11, M_=1500000):
    u = rng.random((M_, 40)).argsort(1)[:, :n]
    pay = (u < np_).sum(1); pc = ((u >= np_) & (u < np_ + ne)).sum(1)
    return ((pay >= 1) & (pc >= 2)).mean() * 100
chk('1 payoff + 8 peças', sim(1, 8), P['sinergia']['T5_jogando']['unico_payoff_8_peças'], .15)
chk('4 payoffs + 8 peças', sim(4, 8), P['sinergia']['T5_jogando']['4_payoffs_8_peças'], .15)
# 5 troféus: recontagem do CSV
L = list(csv.DictReader(open(f'{D}/dados/trofeus_sealed_untapped.csv')))
chk('listas', len(L), 69, 0); chk('2 cores', sum(len(x['cores']) == 2 for x in L), 58, 0); chk('17 terrenos', sum(x['terrenos'] == '17' for x in L), 60, 0)
chk('3 cores com até 1 derrota', sum(len(x['cores']) == 3 and x['recorde'] != '7-2' for x in L), 1, 0)
chk('2 cores com até 1 derrota', sum(len(x['cores']) == 2 and x['recorde'] != '7-2' for x in L), 26, 0)
# 6 remoção esperada por pool, fórmula fechada
ec = 6 * ((7 - 1 / 25) / 81 + PL.P_WILD[0] / 81 + PL.P_FOIL[0] / 81)
eu = 6 * (3 / 110 + PL.P_WILD[1] / 110 + PL.P_FOIL[1] / 110)
er = 6 * (PL.P_RM[0] / 80 + PL.P_WILD[2] / 80 + PL.P_FOIL[2] / 80)
em = 6 * (PL.P_RM[1] / 25 + PL.P_WILD[3] / 25 + PL.P_FOIL[3] / 25)
e = dict(C=ec, U=eu, R=er, M=em)
print('cópias esperadas por carta em 6 boosters', {k: round(v, 4) for k, v in e.items()})
for par in ('BR', 'GU', 'WB'):
    x = sum(e[c['r']] for c in C.CARTAS if C.do_par(c, par) and 'remocao' in c['f'])
    chk(f'remoção {par}', x, Q['pares'][par]['remocao'], .05)
# 7 motor com sobreposição: fórmula x simulação
def sim2(sp, am, sc, req, n=11, M_=1500000):
    u = rng.random((M_, 40)).argsort(1)[:, :n]
    a = (u < sp).sum(1); b = ((u >= sp) & (u < sp + am)).sum(1); c = ((u >= sp + am) & (u < sp + am + sc)).sum(1)
    return (((a >= 1) & (b + c >= req)) | ((a == 0) & (b >= 1) & (b - 1 + c >= req))).mean() * 100
chk('motor exato 2+1+6 req2', sim2(2, 1, 6, 2), PL.motor(2, 1, 6, 2) * 100, .15)
chk('motor exato 4+0+12 req2', sim2(4, 0, 12, 2), PL.motor(4, 0, 12, 2) * 100, .15)
# 8 cartas partilhadas Dilemma ∩ Cemitério
s = [c['n'] for c in C.CARTAS if c['r'] in 'CU' and not c['terreno'] and (c['nota'] or 0) >= 2 and 'dilemma' in c['e'] | c['pay'] and 'cemiterio' in c['e'] | c['pay']]
print(len(s), s); chk('Dilemma ∩ Cemitério', len(s), 10, 0)
print('TUDO OK' if all(ok) else 'HÁ ERROS', sum(ok), 'de', len(ok))
