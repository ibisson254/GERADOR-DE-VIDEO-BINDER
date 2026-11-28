#!/usr/bin/env python3
"""Inteligência cultural do Estúdio BINDER: avaliar oportunidades e ler padrões de audiência.

Não escolhe pautas nem chama serviços externos: lê ficheiros do repositório e mostra o raciocínio.
Precisa só de PyYAML (o mesmo do ciclo do TUBO). Correr a partir da raiz do repositório.

  python3 comum/ferramentas/inteligencia.py oportunidades            # tabela da semana, com os porquês
  python3 comum/ferramentas/inteligencia.py oportunidades --detalhe OP-2026-W48-01
  python3 comum/ferramentas/inteligencia.py padroes --por tipo_abertura --metrica tempo_medio_s
  python3 comum/ferramentas/inteligencia.py referencias             # referências culturais e princípios recorrentes
  python3 comum/ferramentas/inteligencia.py validar

Regras em comum/inteligencia/LEIA-ME.md. Códigos de saída: 0 = ok · 1 = erros de validação.
"""
import argparse
import csv
import datetime as dt
import re
import statistics
import sys
from pathlib import Path

import yaml

# Os 10 critérios do fundador (missão de 28/11/2026). Todos 1–5; 5 é sempre o melhor para o BINDER
# (em «custo_esforco», 5 = barato de produzir).
CRITERIOS = [
    ('relevancia_cultural', 'Relevância cultural'),
    ('interesse_audiencia', 'Interesse da audiência'),
    ('originalidade', 'Originalidade da abordagem'),
    ('profundidade', 'Profundidade narrativa'),
    ('potencial_visual', 'Potencial visual'),
    ('fontes', 'Fontes confiáveis disponíveis'),
    ('compartilhamento', 'Potencial de compartilhamento'),
    ('longevidade', 'Longevidade'),
    ('identidade_binder', 'Relação com a identidade BINDER'),
    ('custo_esforco', 'Custo e esforço (5 = barato)'),
]
CATEGORIAS = {
    'A': 'Tendência emergente', 'B': 'Tendência consolidada', 'C': 'Oportunidade editorial',
    'D': 'Assunto saturado', 'E': 'Evento com janela temporal', 'F': 'Movimento cultural',
}
ESTADOS = {'aberta', 'esperar', 'escolhida', 'descartada', 'virou-pauta'}
CONFIANCA = {'alta', 'média', 'baixa'}
TIPOS_EVIDENCIA = {'facto', 'cálculo', 'opinião', 'inferência', 'ausência'}
OBRIGATORIOS = ['id', 'titulo', 'criada', 'estado', 'categoria', 'confianca', 'frente_sugerida',
                'pergunta_central', 'angulo', 'diferenca', 'porque_agora', 'publico', 'evidencias',
                'verificar', 'criterios', 'marca']
RE_ID = re.compile(r'^OP-\d{4}-W\d{2}-\d{2}$')

# Colunas do registo de insights que o subcomando «padroes» sabe ler (comum/insights/LEIA-ME.md).
METRICAS = ['visualizacoes', 'alcance', 'guardados', 'partilhas', 'comentarios', 'novos_seguidores',
            'tempo_medio_s', 'pct_assistida', 'taxa_saltos', 'duracao_s']
ATRIBUTOS = ['frente', 'formato', 'tipo_abertura', 'tipo_narrativa']
MIN_POR_GRUPO = 3   # abaixo disto um grupo não entra na leitura
MIN_GRUPOS = 2      # sem dois grupos comparáveis não há padrão a ler

# Referências culturais (fundador, 28/11/2026): exemplos de estética, design e comportamento que a
# cultura BINDER deve ter. Uma referência inspira um princípio; nunca se copia a peça.
DIMENSOES = {'estetica', 'design', 'comportamento', 'ritmo', 'som', 'narrativa', 'tom'}
ESTADOS_REF = {'recebida', 'vista', 'principio-proposto', 'virou-regra', 'descartada'}
REF_OBRIGATORIOS = ['id', 'url', 'recebida', 'enviada_por', 'palavras_do_fundador', 'estado', 'nao_copiar']
RE_REF = re.compile(r'^REF-\d{4}-\d{2}-\d{2}-\d{2}$')
RE_ETIQUETA = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
MIN_RECORRENCIA = 3  # um princípio só se propõe como regra quando aparece em 3 referências


def raiz_repo():
    return Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------- oportunidades

def ler_oportunidades(raiz):
    pasta = raiz / 'comum' / 'inteligencia' / 'oportunidades'
    ops = []
    for p in sorted(pasta.glob('OP-*.yaml')):
        with p.open(encoding='utf-8') as f:
            ops.append((p, yaml.safe_load(f) or {}))
    return ops


def validar_oportunidade(op, nome='?'):
    erros = []
    for c in OBRIGATORIOS:
        if c not in op or op[c] in (None, '', []):
            erros.append(f'{nome}: falta «{c}»')
    if erros:
        return erros
    if not RE_ID.match(str(op['id'])):
        erros.append(f'{nome}: id «{op["id"]}» fora do formato OP-AAAA-Wss-nn')
    if op['estado'] not in ESTADOS:
        erros.append(f'{nome}: estado «{op["estado"]}» (usar {", ".join(sorted(ESTADOS))})')
    if op['categoria'] not in CATEGORIAS:
        erros.append(f'{nome}: categoria «{op["categoria"]}» (usar A–F)')
    conf = op['confianca']
    if not isinstance(conf, dict) or conf.get('nivel') not in CONFIANCA or not conf.get('porque'):
        erros.append(f'{nome}: confianca precisa de nivel (alta/média/baixa) e porque')
    for i, ev in enumerate(op['evidencias'], 1):
        if ev.get('tipo') not in TIPOS_EVIDENCIA:
            erros.append(f'{nome}: evidência {i} sem tipo válido ({", ".join(sorted(TIPOS_EVIDENCIA))})')
        if ev.get('tipo') != 'ausência':
            for c in ('fonte', 'url', 'data_coleta', 'evidencia'):
                if not ev.get(c):
                    erros.append(f'{nome}: evidência {i} sem «{c}»')
    crit = op['criterios']
    for chave, rotulo in CRITERIOS:
        c = crit.get(chave)
        if not isinstance(c, dict):
            erros.append(f'{nome}: falta o critério «{chave}» ({rotulo})')
            continue
        if c.get('nota') not in (1, 2, 3, 4, 5):
            erros.append(f'{nome}: {chave}.nota tem de ser 1–5')
        if not str(c.get('porque', '')).strip():
            erros.append(f'{nome}: {chave} sem «porque» (nota sem justificação não conta)')
    extra = set(crit) - {k for k, _ in CRITERIOS}
    if extra:
        erros.append(f'{nome}: critérios desconhecidos {sorted(extra)}')
    jan = op.get('janela') or {}
    if jan.get('ate') and not isinstance(jan['ate'], dt.date):
        erros.append(f'{nome}: janela.ate tem de ser data AAAA-MM-DD')
    return erros


def ler_referencias(raiz):
    pasta = raiz / 'comum' / 'inteligencia' / 'referencias'
    refs = []
    for p in sorted(pasta.glob('REF-*.yaml')):
        with p.open(encoding='utf-8') as f:
            refs.append((p, yaml.safe_load(f) or {}))
    return refs


def validar_referencia(ref, nome='?'):
    """Regras: só se tiram princípios do que foi visto (nada inventado sobre uma peça que não se viu);
    cada princípio diz onde se aplica e como se testa; regra só com decisão do fundador."""
    erros = [f'{nome}: falta «{c}»' for c in REF_OBRIGATORIOS if ref.get(c) in (None, '', [])]
    if erros:
        return erros
    if not RE_REF.match(str(ref['id'])):
        erros.append(f'{nome}: id «{ref["id"]}» fora do formato REF-AAAA-MM-DD-nn')
    if ref['estado'] not in ESTADOS_REF:
        erros.append(f'{nome}: estado «{ref["estado"]}» (usar {", ".join(sorted(ESTADOS_REF))})')
    if not isinstance(ref['recebida'], dt.date):
        erros.append(f'{nome}: recebida tem de ser data AAAA-MM-DD')
    dims = ref.get('dimensoes') or []
    if set(dims) - DIMENSOES:
        erros.append(f'{nome}: dimensões desconhecidas {sorted(set(dims) - DIMENSOES)}')
    vista = ref.get('vista') or {}
    princ = ref.get('principios') or []
    if ref['estado'] != 'recebida' and ref['estado'] != 'descartada':
        if not vista.get('como') or not vista.get('em'):
            erros.append(f'{nome}: estado {ref["estado"]} pede «vista» (como e em que data a peça foi vista)')
        if not ref.get('observado'):
            erros.append(f'{nome}: estado {ref["estado"]} pede «observado» (o que se viu, em factos)')
    if princ and not (vista.get('como') and vista.get('em')):
        erros.append(f'{nome}: princípios sem a peça ter sido vista (não se tiram conclusões do que não se viu)')
    for i, pr in enumerate(princ, 1):
        for c in ('etiqueta', 'dimensao', 'principio', 'aplicar_em', 'teste'):
            if not pr.get(c):
                erros.append(f'{nome}: princípio {i} sem «{c}»')
        if pr.get('dimensao') and pr['dimensao'] not in DIMENSOES:
            erros.append(f'{nome}: princípio {i} com dimensão «{pr["dimensao"]}»')
        if pr.get('etiqueta') and not RE_ETIQUETA.match(str(pr['etiqueta'])):
            erros.append(f'{nome}: princípio {i}: etiqueta em minúsculas-com-hífens')
    if ref['estado'] == 'virou-regra' and not (ref.get('decisao') or {}).get('fundador'):
        erros.append(f'{nome}: virou-regra sem decisão do fundador registada (decisao.fundador)')
    return erros


def tabela_referencias(refs):
    linhas = ['Referências culturais (comum/inteligencia/referencias/)', '']
    if not refs:
        return '\n'.join(linhas + ['nenhuma referência registada'])
    for _, r in refs:
        dims = ', '.join(r.get('dimensoes') or []) or '—'
        linhas.append(f"{r['id']} · {r['estado']} · {dims} · {r['url']}")
    contagem = {}
    for _, r in refs:
        if r['estado'] == 'descartada':
            continue
        for pr in r.get('principios') or []:
            contagem.setdefault((pr['dimensao'], pr['etiqueta']), []).append(r['id'])
    linhas += ['', f'Princípios (recorrente = em {MIN_RECORRENCIA}+ referências → propor ao fundador como regra):']
    if not contagem:
        linhas.append('  ainda nenhum (só se tiram princípios de referências vistas)')
    for (dim, et), ids in sorted(contagem.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        marca = 'RECORRENTE' if len(ids) >= MIN_RECORRENCIA else f'{len(ids)}/{MIN_RECORRENCIA}'
        linhas.append(f'  [{marca}] {dim} · {et} · {", ".join(ids)}')
    return '\n'.join(linhas)


def portoes(op, hoje):
    """Regras que nenhuma soma compensa. Devolve (veredito, motivos)."""
    crit = op['criterios']
    motivos = []
    veredito = 'AVALIAR'
    if crit['identidade_binder']['nota'] <= 2:
        veredito = 'FORA'
        motivos.append('identidade BINDER ≤ 2')
    if op['categoria'] == 'D':
        veredito = 'FORA'
        motivos.append('assunto saturado (categoria D)')
    ate = (op.get('janela') or {}).get('ate')
    if ate and ate < hoje:
        veredito = 'FORA'
        motivos.append(f'janela vencida a {ate:%d/%m/%Y}')
    if veredito != 'FORA' and crit['fontes']['nota'] <= 2:
        veredito = 'ESPERAR'
        motivos.append('fontes confiáveis ≤ 2: verificar antes de pôr na mesa')
    return veredito, motivos


def soma(op):
    return sum(op['criterios'][k]['nota'] for k, _ in CRITERIOS)


def tabela_oportunidades(ops, hoje, todas=False):
    linhas = []
    for _, op in ops:
        if not todas and op['estado'] in {'descartada', 'virou-pauta'}:
            continue
        v, motivos = portoes(op, hoje)
        linhas.append((v, op, motivos))
    ordem = {'AVALIAR': 0, 'ESPERAR': 1, 'FORA': 2}
    linhas.sort(key=lambda t: (ordem[t[0]], -soma(t[1]), t[1]['id']))
    out = [f'Oportunidades a {hoje:%d/%m/%Y} (o script ordena; quem escolhe é o fundador)', '']
    out.append('| # | ID | Veredito | Soma /50 | Notas (rel·int·ori·pro·vis·fon·par·lon·ide·cus) | Cat. | Confiança | Janela | Título |')
    out.append('|---|---|---|---|---|---|---|---|---|')
    for i, (v, op, motivos) in enumerate(linhas, 1):
        notas = '·'.join(str(op['criterios'][k]['nota']) for k, _ in CRITERIOS)
        ate = (op.get('janela') or {}).get('ate')
        jan = f'até {ate:%d/%m}' if ate else 'sem prazo'
        vtxt = v + (f' ({"; ".join(motivos)})' if motivos else '')
        out.append(f'| {i} | {op["id"]} | {vtxt} | {soma(op)} | {notas} | {op["categoria"]} | '
                   f'{op["confianca"]["nivel"]} | {jan} | {op["titulo"]} |')
    if not linhas:
        out.append('| — | — | — | — | — | — | — | — | nenhuma oportunidade aberta |')
    out += ['', 'A soma só ordena dentro do mesmo veredito; ler sempre as notas e os porquês (--detalhe ID).']
    return '\n'.join(out)


def detalhe(op, hoje):
    v, motivos = portoes(op, hoje)
    jan = op.get('janela') or {}
    out = [f'{op["id"]} · {op["titulo"]}',
           f'Veredito: {v}' + (f' ({"; ".join(motivos)})' if motivos else ''),
           f'Categoria: {op["categoria"]} {CATEGORIAS[op["categoria"]]} · confiança {op["confianca"]["nivel"]}: '
           f'{op["confianca"]["porque"]}',
           f'Frente sugerida: {op["frente_sugerida"]}',
           f'Janela: {jan.get("ate") or "sem prazo"} · {jan.get("motivo", "")}', '',
           f'Pergunta central: {op["pergunta_central"]}',
           f'Ângulo: {op["angulo"]}',
           f'O que a torna diferente: {op["diferenca"]}',
           f'Porquê agora (ou esperar): {op["porque_agora"]}',
           f'Público: {op["publico"]}', '', 'Critérios:']
    for k, rot in CRITERIOS:
        c = op['criterios'][k]
        out.append(f'  {c["nota"]} · {rot}: {c["porque"]}')
    out.append(f'  Soma: {soma(op)}/50')
    out += ['', 'Evidências:']
    for ev in op['evidencias']:
        if ev['tipo'] == 'ausência':
            out.append(f'  [ausência] {ev.get("evidencia", "")}')
        else:
            out.append(f'  [{ev["tipo"]}] {ev["evidencia"]} — {ev["fonte"]}, '
                       f'publicada {ev.get("data_publicacao", "sem data")}, lida {ev["data_coleta"]} · {ev["url"]}')
    out += ['', 'Falta verificar:'] + [f'  - {x}' for x in op['verificar']]
    m = op['marca']
    out += ['', f'Marca: {m.get("valor", "")}', f'Direitos: {m.get("direitos", "")}']
    return '\n'.join(out)


# ---------------------------------------------------------------- padrões de audiência

def num(txt):
    txt = (txt or '').strip().replace(',', '.')
    try:
        return float(txt) if txt else None
    except ValueError:
        return None


def ultimas_leituras(linhas):
    """Uma linha por conteúdo: a do snapshot mais recente (semana_fim maior)."""
    por_id = {}
    for r in linhas:
        i = r.get('id_editorial', '')
        if i in ('', 'SEM-ID'):
            continue
        if i not in por_id or r['semana_fim'] >= por_id[i]['semana_fim']:
            por_id[i] = r
    return list(por_id.values())


def ler_padroes(linhas, por, metrica):
    """Devolve o texto da leitura. Nunca conclui causalidade; abaixo da amostra diz que não há leitura."""
    if por not in ATRIBUTOS:
        raise ValueError(f'--por tem de ser um de {ATRIBUTOS}')
    if metrica not in METRICAS + ['pct_assistida_calc']:
        raise ValueError(f'--metrica tem de ser uma de {METRICAS + ["pct_assistida_calc"]}')
    obs = ultimas_leituras(linhas)
    grupos, sem_valor, sem_atributo = {}, [], []
    for r in obs:
        if metrica == 'pct_assistida_calc':
            t, d = num(r.get('tempo_medio_s')), num(r.get('duracao_s'))
            v = round(100 * t / d, 1) if t and d else None
        else:
            v = num(r.get(metrica))
        a = (r.get(por) or '').strip()
        if v is None:
            sem_valor.append(r['id_editorial'])
        elif not a:
            sem_atributo.append(r['id_editorial'])
        else:
            grupos.setdefault(a, []).append((r['id_editorial'], v))
    tipo = 'calculada (tempo médio ÷ duração, ambos observados)' if metrica == 'pct_assistida_calc' else 'observada'
    out = [f'Padrões · {metrica} ({tipo}) por {por}', f'Conteúdos com leitura: {len(obs)} · com valor e atributo: '
           f'{sum(len(g) for g in grupos.values())}', '']
    out.append('FACTOS OBSERVADOS')
    if not grupos:
        out.append('  (nenhum conteúdo tem esta métrica e este atributo preenchidos)')
    for a, g in sorted(grupos.items()):
        vals = [v for _, v in g]
        out.append(f'  {a}: n={len(g)} · mediana {statistics.median(vals):g} · '
                   f'mín {min(vals):g} · máx {max(vals):g} · {", ".join(i for i, _ in g)}')
    validos = {a: g for a, g in grupos.items() if len(g) >= MIN_POR_GRUPO}
    out += ['', 'LEITURA']
    if len(validos) < MIN_GRUPOS:
        out.append(f'  Amostra insuficiente: é preciso pelo menos {MIN_GRUPOS} grupos com n ≥ {MIN_POR_GRUPO}. '
                   'Nenhuma conclusão; continuar a registar.')
    else:
        med = sorted(((statistics.median([v for _, v in g]), a, len(g)) for a, g in validos.items()), reverse=True)
        topo, resto = med[0], med[1:]
        out.append(f'  Hipótese (não comprovada): nesta amostra, «{topo[1]}» tem a mediana mais alta '
                   f'({topo[0]:g}, n={topo[2]}) face a ' +
                   ', '.join(f'«{a}» ({m:g}, n={n})' for m, a, n in resto) + '.')
        out.append('  Amostra pequena e sem controlo de tema, idade do post nem impulso: não é causa. '
                   'Recomendação: testar a mesma variável em 3 episódios comparáveis antes de virar regra '
                   '(constituição §12).')
    if sem_valor:
        out += ['', f'Sem {metrica}: {len(sem_valor)} conteúdo(s) ({", ".join(sorted(sem_valor)[:8])}'
                f'{"…" if len(sem_valor) > 8 else ""}). Vazio = não visível no print, nunca zero.']
    if sem_atributo:
        out.append(f'Sem {por}: {", ".join(sorted(sem_atributo))}.')
    return '\n'.join(out)


# ---------------------------------------------------------------- CLI

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--raiz', type=Path, default=None)
    ap.add_argument('--hoje', type=dt.date.fromisoformat, default=dt.date.today(), help=argparse.SUPPRESS)
    sub = ap.add_subparsers(dest='cmd', required=True)
    o = sub.add_parser('oportunidades', help='tabela das oportunidades abertas, com portões e notas')
    o.add_argument('--detalhe', metavar='ID')
    o.add_argument('--todas', action='store_true', help='inclui descartadas e as que viraram pauta')
    p = sub.add_parser('padroes', help='padrões entre um atributo do vídeo e uma métrica do Insights')
    p.add_argument('--por', default='tipo_abertura', choices=ATRIBUTOS)
    p.add_argument('--metrica', default='tempo_medio_s', choices=METRICAS + ['pct_assistida_calc'])
    sub.add_parser('referencias', help='referências culturais e princípios recorrentes')
    sub.add_parser('validar', help='valida as fichas de oportunidade e de referência')
    a = ap.parse_args(argv)
    raiz = a.raiz or raiz_repo()

    if a.cmd == 'padroes':
        with (raiz / 'comum' / 'insights' / 'registo_posts.csv').open(encoding='utf-8', newline='') as f:
            print(ler_padroes(list(csv.DictReader(f)), a.por, a.metrica))
        return 0

    ops = ler_oportunidades(raiz)
    erros = []
    ids = set()
    for p_, op in ops:
        e = validar_oportunidade(op, p_.name)
        if not e and p_.stem != op['id']:
            e.append(f'{p_.name}: o nome do ficheiro tem de ser o id ({op["id"]}.yaml)')
        if op.get('id') in ids:
            e.append(f'{p_.name}: id repetido')
        ids.add(op.get('id'))
        erros += e
    refs = ler_referencias(raiz)
    rids = set()
    for p_, ref in refs:
        e = validar_referencia(ref, p_.name)
        if not e and p_.stem != ref['id']:
            e.append(f'{p_.name}: o nome do ficheiro tem de ser o id ({ref["id"]}.yaml)')
        if ref.get('id') in rids:
            e.append(f'{p_.name}: id repetido')
        rids.add(ref.get('id'))
        erros += e
    if erros:
        print('\n'.join(erros))
        return 1
    if a.cmd == 'validar':
        print(f'OK · {len(ops)} oportunidade(s) · {len(refs)} referência(s)')
        return 0
    if a.cmd == 'referencias':
        print(tabela_referencias(refs))
        return 0
    if a.detalhe:
        alvo = [op for _, op in ops if op['id'] == a.detalhe]
        if not alvo:
            print(f'{a.detalhe} não existe')
            return 1
        print(detalhe(alvo[0], a.hoje))
        return 0
    print(tabela_oportunidades(ops, a.hoje, a.todas))
    return 0


if __name__ == '__main__':
    sys.exit(main())
