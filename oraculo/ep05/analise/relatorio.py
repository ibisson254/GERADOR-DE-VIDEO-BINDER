#!/usr/bin/env python3
"""EP05 · gera as tabelas do dossiê a partir de resultados/*.json (nada escrito à mão). Saída: resultados/tabelas.md"""
import json, os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda n: json.load(open(f'{D}/resultados/{n}.json'))
P, Q, G, S, M, R = J('prob'), J('pools'), J('grafo'), J('sim'), J('matriz'), J('robustez')
o = []
def tab(cab, linhas):
    o.append('| ' + ' | '.join(cab) + ' |'); o.append('|' + '---|' * len(cab))
    for l in linhas: o.append('| ' + ' | '.join(str(x) for x in l) + ' |')
    o.append('')
o.append('### A. Abertura (6 Play Boosters, sem a promo; pisos: variantes com taxa "<1%" ficam de fora)\n')
A = P['abertura']
tab(['Evento', 'Probabilidade'], [['Rara específica, por booster', f"{A['rara_especifica_booster']}%"], ['Rara específica, 6 boosters', f"{A['rara_especifica_6']}%"], ['Mítica específica, por booster', f"{A['mitica_especifica_booster']}%"], ['Mítica específica, 6 boosters', f"{A['mitica_especifica_6']}%"],
     ['Alguma mítica, por booster', f"{A['qualquer_mitica_booster_piso']}%"], ['Alguma mítica, 6 boosters', f"{A['qualquer_mitica_6_piso']}%"], ['Pelo menos uma rara ou mítica', 'garantida (1 vaga por booster)'], ['Booster com 2+ raras/míticas', f"{A['booster_com_2+_raras_piso']}%"],
     ['Raras/míticas esperadas em 6 boosters', A['raras_miticas_esperadas_6_piso']], ['6 boosters sem nenhuma extra', f"{A['6boosters_0_extras_piso']}%"], ['6 boosters com 2+ extras', f"{A['6boosters_2+_extras_piso']}%"], ['Stardates em pelo menos 1 de 6 boosters', f"{A['stardates_6_boosters']}%"], ['Dual específico (vaga de terreno)', f"{A['dual_especifico_6']}%"]])
o.append('### B. Consistência: k cartas em 40 (%, sem mulligan)\n')
for lado in ('jogando', 'comprando'):
    o.append(f'**{lado.capitalize()} primeiro**\n'.replace('Comprando primeiro', 'Comprando (no empate: quem não começa)').replace('Jogando primeiro', 'Quem começa'))
    b = P['copias'][lado]
    tab(['k', 'mão', 'T2', 'T3', 'T4', 'T5', 'T6', 'T8'], [[k, v['mao'], v['T2'], v['T3'], v['T4'], v['T5'], v['T6'], v['T8']] for k, v in b.items()])
o.append('### C. Terrenos\n')
for L, x in P['terrenos'].items():
    o.append(f"**{L} terrenos** · mão com 2 a 5 terrenos: {x['jogando']['mao_2a5']}%\n")
    tab(['Lado', '2 no T2', '3 no T3', '4 no T4', '5 no T5', '6 no T6'], [[l, x[l]['>=2T_T2'], x[l]['>=3T_T3'], x[l]['>=4T_T4'], x[l]['>=5T_T5'], x[l]['>=6T_T6']] for l in ('jogando', 'comprando')])
o.append('### D. Carta de custo 2 no T2 (2+ terrenos e 1+ carta de custo 2)\n')
tab(['Terrenos', 'Cartas de custo 2', 'Jogando', 'Comprando'], [[k.split('_')[0][:-1], k.split('_')[1][:-2], v['jogando'], v['comprando']] for k, v in P['dois_drop_T2'].items()])
mc = P['mc_confirmacao']
o.append(f"Curva 2+3 (17 terrenos, 7 de custo 2, 6 de custo 3, Monte Carlo): {mc['curva_2_3_jogando']}% jogando, {mc['curva_2_3_comprando']}% comprando.\n")
o.append('### E. Duas cores, jogando / comprando\n')
C = P['duas_cores']; lin = []
for mb in ('9+8+0d', '8+8+1d', '8+7+2d', '7+7+3d', '10+7+0d'):
    lin.append([mb.replace('d', ' duais')] + [f"{C[f'{mb}_jogando_T{t}']} / {C[f'{mb}_comprando_T{t}']}" for t in (2, 3, 4, 5)])
tab(['Base', 'T2', 'T3', 'T4', 'T5'], lin)
F = P['fontes']
tab(['Custo duplo CC no T4', 'Jogando', 'Comprando'], [[k.replace('CC_', '').replace('fontes_T4', ' fontes'), v['jogando'], v['comprando']] for k, v in F.items() if k.startswith('CC')])
tab(['Splash', 'T6 jog/comp', 'T8 jog/comp'], [[k.replace('splash_', '').replace('fontes', ' fontes'), f"{v['T6']['jogando']} / {v['T6']['comprando']}", f"{v['T8']['jogando']} / {v['T8']['comprando']}"] for k, v in F.items() if k.startswith('splash')])
o.append('### F. Sinergias até T5 (e T6), jogando / comprando\n')
Y = P['sinergia']; nomes = [('bomba_1_copia', '1 carta única'), ('combo_2pecas_1_1', 'combo A+B, 1 cópia de cada'), ('2_de_3_pecas_unicas', '2 de 3 peças'), ('2_de_4_pecas_unicas', '2 de 4 peças'), ('2_de_5', '2 de 5'), ('2_de_7', '2 de 7'), ('2_de_9', '2 de 9'),
                                ('unico_payoff_8_peças', '1 payoff + 2 de 8 peças'), ('3_payoffs_8_peças', '3 payoffs + 2 de 8'), ('4_payoffs_8_peças', '4 payoffs + 2 de 8'), ('5_payoffs_8_peças', '5 payoffs + 2 de 8')]
tab(['Estrutura', 'T5', 'T6', 'T8'], [[n] + [f"{Y[f'T{t}_jogando'][k]} / {Y[f'T{t}_comprando'][k]}" for t in (5, 6, 8)] for k, n in nomes])
o.append('### G. Mulligan (London; mantém 7 com 2 a 5 terrenos, 6 com 2 a 5 antes do fundo, 5 sempre). Separado dos cenários acima\n')
m7, m1 = P['mulligan_17T_7chaves'], P['mulligan_17T_1chave']
tab(['Lado', 'Mantém 7', 'Vai a 6', 'Vai a 5', '1 carta até T5', 'sem mull', '7 cartas até T5', 'sem mull'], [[l, m7[l]['mantem_7'], m7[l]['vai_a_6'], m7[l]['vai_a_5'], m1[l]['chave_ate_T5_com_mull'], m1[l]['chave_ate_T5_sem_mull_mesma_regra'], m7[l]['chave_ate_T5_com_mull'], m7[l]['chave_ate_T5_sem_mull_mesma_regra']] for l in ('jogando', 'comprando')])
o.append('### H. Pools simulados por par (40.000 pools)\n')
ge = Q['geral']
o.append(f"Pool médio: {ge['mit']} míticas · {ge['rar']} raras+míticas · {ge['planetas']} Planetas · {ge['terrenos_nomes']} terrenos não básicos de nomes diferentes. Melhor par (por nota) com 23+ jogáveis: {ge['p_best_23jog']}%; com 5+ remoções: {ge['p_best_5rem']}%. Carta de maior nota fora do melhor par: {ge['p_bomba_fora']}%.\n")
tab(['Par', 'Plano', 'Jogáveis (nota ≥ 2)', '%23+', 'Média top 23', '%bomba', 'Remoção', '%5+', 'Dura', 'Peças', 'Payoffs', '%0 payoff', '%2+ payoffs', 'Corpos ≤ 2'],
    [[k, o_['plano'], o_['jogaveis'], o_['p23'], o_['media_top23'], o_['p_bomba'], o_['remocao'], o_['p5rem'], o_['remocao_dura'], o_['E'], o_['P'], o_['p_P0'], o_['p_P2'], o_['corpos_2']] for k, o_ in Q['pares'].items()])
o.append('### I. Matriz dos dez planos (notas 1 a 5, pesos iguais; não é win rate)\n')
tab(['#', 'Par', 'Plano', 'Disponib.', 'Potência', 'Consist.', 'Flex.', 'Total', 'Motor T5', 'Melhor no modelo (banda 5–95%)', 'Confiança'],
    [[i + 1, f"{m['nome']} ({m['par']})", m['plano'], m['disponibilidade'], m['potencia'], m['consistencia'], m['flexibilidade'], m['total'], f"{m['motor_T5']}%", f"{m['melhor_modelo']}% ({m['banda'][0]}–{m['banda'][1]})", m['confianca']] for i, m in enumerate(M)])
o.append('### J. Grafo: mecanismos\n')
tab(['Mecanismo', 'Peças C/U', 'Payoffs C/U', 'Peças (todas)', 'Payoffs (todas)', 'Grau ponderado', 'Intermediação'], [[v['rotulo'], v['pecas_cu'], v['payoffs_cu'], v['pecas_todas'], v['payoffs_todas'], v['grau_ponderado'], v['intermediacao']] for v in G['mecanismos'].values()])
tab(['Ligação', 'Cartas partilhadas', 'Jaccard'], [[f"{l['a']} — {l['b']}", l['cartas'], l['jaccard']] for l in G['ligacoes'][:12]])
o.append(f"Densidade da projeção: {G['densidade']}. Comunidades (modularidade gulosa): " + ' · '.join(' + '.join(c) for c in G['clusters']) + '.\n')
tab(['Carta-ponte', 'Rar.', 'Nota', 'Mecanismos'], [[c['n'], c['r'], c['nota'], ', '.join(c['mecanismos'])] for c in G['cartas_ponte'][:14]])
tab(['Regra (etiquetas no set)', 'n', 'Suporte', 'Confiança', 'Lift'], [[f"{r['a']} → {r['b']}", r['n'], r['suporte'], r['confianca'], r['lift']] for r in G['regras_top'] if 'remocao_' not in r['a'] + r['b'] and {r['a'], r['b']} != {'remocao', 'anti_artefato'}][:8])
o.append('### K. Listas de troféu (Camada B)\n')
T = G['trofeus']
tab(['Medida', 'Valor'], [['Listas', T['n']], ['Coleções', T['sets']], ['2 cores / 3 cores', f"{T['duas_cores']} / {T['tres_cores']}"], ['17 / 16 terrenos', f"{T['t17']} / {T['t16']}"], ['7–0 / 7–1 / 7–2', f"{T['r70']} / {T['r71']} / {T['r72']}"],
                          ['Até 1 derrota com 2 cores', f"{T['duas_top']} de {T['duas_cores']} (lift {T['lift_top_2cores']})"], ['Até 1 derrota com 3 cores', f"{T['tres_top']} de {T['tres_cores']} (lift {T['lift_top_3cores']})"], ['Teste exato de Fisher', T['fisher_p']], ['Até 1 derrota com 16 terrenos', f"{T['t16_top']} de {T['t16']}"], ['Até 1 derrota com 17 terrenos', f"{T['t17_top']} de {T['t17']}"], ['Pares nas listas de 2 cores', ', '.join(f'{a} {b}' for a, b in T['pares'])]])
o.append('### L. Simulações de mecânica (goldfish: tetos, sem oponente)\n')
g = S['poder8_goldfish_jogando']; s = S['snw']
tab(['Medida', 'T5', 'T6', 'T7'], [['Poder total 8 em mesa, jogando', g['T5'], g['T6'], g['T7']], ['idem, comprando', S['poder8_goldfish_comprando']['T5'], S['poder8_goldfish_comprando']['T6'], S['poder8_goldfish_comprando']['T7']], ['idem, curva lenta, jogando', S['poder8_goldfish_lento']['T5'], S['poder8_goldfish_lento']['T6'], S['poder8_goldfish_lento']['T7']]])
tab(['Base GU (17 terrenos)', 'Nomes em T6 (média)', '3+ nomes em T6', 'Duas cores até T3'], [[k, s[k]['T6']['media'], f"{s[k]['T6']['p3']}%", f"{s['cores_T3'][k]}%"] for k in ('9F+8I', 'pool_4_nomes', 'pool_mais_basicos')])
o.append(f"Federation: {S['federation']['media_tipos_por_criatura']} tipos por criatura não-Borg de C/U (n={S['federation']['n']}); tipos distintos com 1 a 5 criaturas: {S['federation']['tipos_media_por_n_criaturas']}.\n")
open(f'{D}/resultados/tabelas.md', 'w').write('\n'.join(o))
print(len('\n'.join(o)))
