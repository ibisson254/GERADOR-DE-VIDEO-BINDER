#!/usr/bin/env python3
"""EP05 · grafo de estruturas de Star Trek e métricas das listas de troféu.
Camada A (dados completos): cartas → mecanismos → pares, a partir do Oracle das 306 cartas. Nenhum resultado de jogo.
Camada B (amostra real, rasa): 69 listas de troféu de Sealed do Arena (Untapped.gg), 9 sets. Só cores, recorde e terrenos são fiáveis.
Sem grupo de controlo de decks medianos: os dados brutos do 17Lands não estão acessíveis nesta sessão.
Saída: resultados/grafo.json"""
import csv, json, os, sys, itertools, collections
from math import comb
import networkx as nx
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cartas import CARTAS, PARES, NOME_PAR, PLANO, MECH_PAR, ROTULO
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEC = list(ROTULO)
cu = [c for c in CARTAS if c['r'] in 'CU' and not c['terreno']]
def membros(c): return (c['e'] | c['pay']) - {'naocriatura'}        # "não-criatura" é quase metade do set: conta à parte
G = nx.Graph()
for m in MEC: G.add_node(m, tipo='mecanismo', rotulo=ROTULO[m])
for c in cu:
    G.add_node(c['n'], tipo='carta', r=c['r'], nota=c['nota'], cores=''.join(sorted(c['cores_set'])))
    for m in c['e']: G.add_edge(c['n'], m, papel='peca')
    for m in c['pay']: G.add_edge(c['n'], m, papel='payoff')
    for fn in c['f'] & {'remocao', 'anti_artefato', 'vantagem', 'fixacao', 'recursao'}:
        G.add_node(fn, tipo='funcao'); G.add_edge(c['n'], fn, papel='funcao')
# projeção mecanismo-mecanismo por cartas partilhadas (só cartas jogáveis, nota >= 2.0)
def viz(m): return {c['n'] for c in cu if m in c['e'] | c['pay'] and (c['nota'] or 0) >= 2}
P = nx.Graph(); viz_ = {m: viz(m) for m in MEC if m != 'naocriatura'}
for a, b in itertools.combinations(viz_, 2):
    s = viz_[a] & viz_[b]; u = viz_[a] | viz_[b]
    if s: P.add_edge(a, b, peso=len(s), jaccard=round(len(s) / len(u), 3), cartas=sorted(s))
for u, v, d in P.edges(data=True): d['dist'] = 1 / d['peso']
bet = nx.betweenness_centrality(P, weight='dist'); wdeg = dict(P.degree(weight='peso'))
coms = list(nx.algorithms.community.greedy_modularity_communities(P, weight='peso'))
# métricas de carta: em quantos mecanismos entra
cart = sorted(((len(membros(c)), c['nota'] or 0, c['n'], c['r'], sorted(membros(c))) for c in cu if (c['nota'] or 0) >= 2.5), reverse=True)[:25]
# suporte/confiança/lift entre etiquetas no conjunto real de 306 cartas (estrutura do set, não coocorrência em decks)
T = [(c['e'] | c['pay'] | c['f']) for c in CARTAS if not c['terreno']]
n = len(T); items = sorted({x for t in T for x in t} - {'criatura'})
sup = {i: sum(i in t for t in T) / n for i in items}; regras = []
for a, b in itertools.permutations(items, 2):
    ab = sum(a in t and b in t for t in T) / n
    if ab * n >= 5:
        regras.append(dict(a=a, b=b, suporte=round(ab, 4), confianca=round(ab / sup[a], 3), lift=round(ab / (sup[a] * sup[b]), 3), n=round(ab * n)))
regras.sort(key=lambda r: -r['lift'])
dens = nx.density(P)
# Camada B
L = list(csv.DictReader(open(f'{D}/dados/trofeus_sealed_untapped.csv')))
def fisher(a, b, c, d_):
    def hg(x): return comb(a + b, x) * comb(c + d_, a + c - x) / comb(a + b + c + d_, a + c)
    p0 = hg(a); return sum(hg(x) for x in range(max(0, a - d_), min(a + b, a + c) + 1) if hg(x) <= p0 + 1e-12)
n2 = [x for x in L if len(x['cores']) == 2]; n3 = [x for x in L if len(x['cores']) == 3]
top = lambda g: sum(x['recorde'] in ('7-0', '7-1') for x in g)
tab = dict(n=len(L), sets=len({x['set'] for x in L}), duas_cores=len(n2), tres_cores=len(n3), t17=sum(x['terrenos'] == '17' for x in L), t16=sum(x['terrenos'] == '16' for x in L),
           r70=sum(x['recorde'] == '7-0' for x in L), r71=sum(x['recorde'] == '7-1' for x in L), r72=sum(x['recorde'] == '7-2' for x in L),
           duas_top=top(n2), tres_top=top(n3), fisher_p=round(fisher(top(n2), len(n2) - top(n2), top(n3), len(n3) - top(n3)), 4),
           t16_top=top([x for x in L if x['terrenos'] == '16']), t17_top=top([x for x in L if x['terrenos'] == '17']),
           lift_top_2cores=round((top(n2) / len(n2)) / (top(L) / len(L)), 3), lift_top_3cores=round((top(n3) / len(n3)) / (top(L) / len(L)), 3),
           pares=collections.Counter(x['cores'] for x in n2).most_common())
out = dict(mecanismos={m: dict(rotulo=ROTULO[m], pecas_cu=sum(m in c['e'] for c in cu), payoffs_cu=sum(m in c['pay'] for c in cu),
                               pecas_todas=sum(m in c['e'] for c in CARTAS), payoffs_todas=sum(m in c['pay'] for c in CARTAS),
                               grau_ponderado=wdeg.get(m, 0), intermediacao=round(bet.get(m, 0), 3)) for m in MEC},
           ligacoes=sorted([dict(a=ROTULO[u], b=ROTULO[v], cartas=d['peso'], jaccard=d['jaccard']) for u, v, d in P.edges(data=True)], key=lambda r: -r['cartas']),
           clusters=[sorted(ROTULO[m] for m in c) for c in coms], densidade=round(dens, 3), cartas_ponte=[dict(n=x[2], r=x[3], nota=x[1], mecanismos=x[4]) for x in cart],
           regras_top=regras[:20], trofeus=tab)
json.dump(out, open(f'{D}/resultados/grafo.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ('regras_top',)}, ensure_ascii=False, indent=0)[:6500])
print([ (r['a'],r['b'],r['n'],r['lift']) for r in regras[:14]])
