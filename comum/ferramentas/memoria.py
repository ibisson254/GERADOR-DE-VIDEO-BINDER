#!/usr/bin/env python3
"""Memória editorial do Estúdio BINDER: registo, originalidade, encerramento e insights.

Só biblioteca padrão. Correr a partir da raiz do repositório (ou passar --raiz).

  python3 comum/ferramentas/memoria.py validar
  python3 comum/ferramentas/memoria.py pauta --objeto "Stasis" --tema "carta mais odiada"
  python3 comum/ferramentas/memoria.py encerramento MB-EP10
  python3 comum/ferramentas/memoria.py semana 2026-11-08
  python3 comum/ferramentas/memoria.py segredos

Códigos de saída: 0 = ok · 1 = erros de validação · 2 = pauta bloqueada / encerramento incompleto.
"""
import argparse
import csv
import datetime as dt
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ESTADOS = {
    'IDEIA', 'EM ANÁLISE', 'APROVADO', 'EM PRODUÇÃO', 'CONCLUÍDO', 'PUBLICADO',
    'REJEITADO', 'PAUSADO', 'NÃO PUBLICÁVEL', 'POR AUDITAR',
}
NAO_BLOQUEIAM = {'REJEITADO'}
COLUNAS = ['ID', 'Tema central', 'Objeto', 'Tese · ângulo', 'Gancho', 'Estado', 'Fonte do estado',
           'Aprovação', 'Publicação', 'Ficha', 'Relações', 'Originalidade']
PREFIXOS = {'MB': 'Mana & Burn', 'MC': 'Meta em Curto', 'CM': 'Conde de Manaforte', 'ESP': 'Especiais',
            'ORB': 'Órbita', 'LL': 'Lambe-lambe', 'PM': 'Pequeno Mestre', 'VV': 'Vince Vault'}
RE_ID = re.compile(r'^(MB|MC|CM|ESP|ORB|LL|PM|VV)-[A-Z0-9-]+$')
PROMOCAO = {'SIM', 'NÃO', 'PARCIAL', 'A CONFIRMAR'}
CSV_COLUNAS = ['semana_fim', 'periodo', 'id_editorial', 'frente', 'post_ref', 'formato', 'idade',
               'visualizacoes', 'alcance', 'impressoes', 'curtidas', 'comentarios', 'guardados',
               'partilhas', 'visitas_perfil', 'novos_seguidores', 'cliques_link', 'outras_acoes',
               'impulsionado', 'investimento', 'moeda', 'campanha_periodo', 'objetivo_anuncio',
               'alcance_pago', 'fonte', 'notas']
NUMERICAS = ['visualizacoes', 'alcance', 'impressoes', 'curtidas', 'comentarios', 'guardados',
             'partilhas', 'visitas_perfil', 'novos_seguidores', 'cliques_link', 'alcance_pago']
VAZIOS = {'', '—', '-', 'LACUNA'}
# Palavras que não distinguem objetos (evitam falsos positivos na comparação).
GENERICAS = {'the', 'of', 'and', 'de', 'da', 'do', 'das', 'dos', 'e', 'a', 'o', 'carta', 'cartas', 'magic',
             'n', 'no', 'na', 'em', 'com', 'um', 'uma', 'para', 'mais', 'commander', 'lacuna'}
SEGREDOS = [
    re.compile(r'sk-[A-Za-z0-9_-]{20,}'),                 # chaves estilo OpenAI/Anthropic
    re.compile(r'gh[pousr]_[A-Za-z0-9]{30,}'),            # tokens GitHub
    re.compile(r'github_pat_[A-Za-z0-9_]{30,}'),
    re.compile(r'AKIA[0-9A-Z]{16}'),                      # AWS
    re.compile(r'xox[baprs]-[A-Za-z0-9-]{10,}'),          # Slack
    re.compile(r'eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}'),  # JWT
    re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----'),
    re.compile(r'(?i)(api[_-]?key|secret|password|senha|token)\s*[:=]\s*["\'][^"\'\s]{12,}["\']'),
]


def norm(txt):
    txt = unicodedata.normalize('NFKD', txt).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', ' ', txt).strip()


def tokens(txt):
    return {t for t in norm(txt).split() if len(t) > 2 and t not in GENERICAS and not t.isdigit()}


# ---------------------------------------------------------------- registo

def ler_registo(raiz):
    """Lê as tabelas do registo. Devolve (entradas, erros)."""
    caminho = raiz / 'comum' / 'REGISTRO_EDITORIAL.md'
    entradas, erros = [], []
    if not caminho.exists():
        return [], [f'{caminho} não existe']
    for n, linha in enumerate(caminho.read_text(encoding='utf-8').splitlines(), 1):
        if not linha.startswith('| ') or linha.startswith('|---'):
            continue
        celulas = [c.strip() for c in linha.strip().strip('|').split('|')]
        if celulas[0] in ('ID', 'Estado') or not RE_ID.match(celulas[0]):
            continue
        if len(celulas) != len(COLUNAS):
            erros.append(f'linha {n}: {celulas[0]} tem {len(celulas)} colunas (esperado {len(COLUNAS)}); '
                         'evitar "|" dentro das células')
            continue
        e = dict(zip(COLUNAS, celulas))
        e['_linha'] = n
        e['Frente'] = PREFIXOS[celulas[0].split('-')[0]]
        entradas.append(e)
    return entradas, erros


def caminho_ficha(raiz, ficha):
    """Devolve o Path local da ficha, ou None se a ficha vive noutra branch/projeto ou é lacuna."""
    if ficha in VAZIOS or ficha.startswith(('branch:', 'projeto:')):
        return None
    return raiz / ficha


def validar_registo(raiz, entradas):
    erros, avisos = [], []
    ids = {}
    for e in entradas:
        i = e['ID']
        if i in ids:
            erros.append(f'{i}: ID repetido (linhas {ids[i]} e {e["_linha"]})')
        ids[i] = e['_linha']
        if e['Estado'] not in ESTADOS:
            erros.append(f'{i}: estado inválido "{e["Estado"]}"')
        for campo in COLUNAS:
            if not e[campo]:
                erros.append(f'{i}: campo "{campo}" vazio (usar — ou LACUNA)')
        if e['Estado'] == 'PUBLICADO' and e['Publicação'] in VAZIOS | {'A CONFIRMAR'}:
            erros.append(f'{i}: PUBLICADO sem confirmação de publicação')
        if e['Estado'] == 'PUBLICADO' and e['Fonte do estado'] in VAZIOS:
            erros.append(f'{i}: PUBLICADO sem fonte do estado')
        if e['Estado'] in ('CONCLUÍDO', 'EM PRODUÇÃO', 'APROVADO', 'PUBLICADO', 'NÃO PUBLICÁVEL'):
            p = caminho_ficha(raiz, e['Ficha'])
            if p is not None and not p.exists():
                erros.append(f'{i}: ficha não existe no repositório: {e["Ficha"]}')
        if e['Estado'] == 'POR AUDITAR':
            avisos.append(i)
    for e in entradas:
        for rel in re.findall(r'\b(?:MB|MC|CM|ESP|ORB|LL|PM)-[A-Z0-9]+(?:-[A-Z0-9]+)*', e['Relações']):
            if rel not in ids:
                erros.append(f'{e["ID"]}: relação para ID inexistente {rel}')
    return erros, avisos


# ---------------------------------------------------------------- pauta

def comparar_pauta(entradas, objeto, tema='', gancho=''):
    """Compara uma pauta com o registo. Devolve lista de (entrada, motivo, bloqueia)."""
    objs = [o.strip() for o in objeto.split(';') if o.strip()]
    conflitos = []
    for e in entradas:
        motivos = []
        objs_reg = [o.strip() for o in e['Objeto'].split(';') if o.strip() not in VAZIOS]
        for o in objs:
            no = norm(o)
            to = tokens(o)
            for r in objs_reg:
                nr = norm(r)
                tr = tokens(r)
                if no and nr and (no == nr or (len(no) >= 4 and no in nr) or (len(nr) >= 4 and nr in no)):
                    motivos.append(f'mesmo objeto ("{o}" ~ "{r}")')
                elif to and tr and len(to & tr) >= max(2, (min(len(to), len(tr)) + 1) // 2):
                    motivos.append(f'objeto parecido ("{o}" ~ "{r}": {", ".join(sorted(to & tr))})')
        for nome, valor, campo in (('tema', tema, 'Tema central'), ('gancho', gancho, 'Gancho')):
            if not valor:
                continue
            tv, te = tokens(valor), tokens(e[campo] + ' ' + e['Tese · ângulo'])
            comuns = tv & te
            if tv and len(comuns) >= max(2, (len(tv) + 1) // 2):
                motivos.append(f'{nome} parecido ({", ".join(sorted(comuns))})')
        if motivos:
            conflitos.append((e, '; '.join(dict.fromkeys(motivos)), e['Estado'] not in NAO_BLOQUEIAM))
    return conflitos


# ---------------------------------------------------------------- encerramento

PECAS = {
    'ficha': ['ficha*.md', '*_ficha.md'],
    'roteiro': ['roteiro*', 'guiao*', 'episode.json', '*roteiro*.json'],
    'legenda': ['legenda*.txt', '*_legenda.txt'],
    'comentário fixado': ['comentario_fixado*.txt'],
    'texto alternativo': ['texto_alternativo*.txt', 'alt_text*.txt'],
    'fontes': ['*fontes*', 'ficha_de_fatos*.md'],
}


def verificar_encerramento(raiz, entrada):
    """Confere o pacote de um episódio na pasta da ficha. Devolve lista de faltas."""
    faltas = []
    p = caminho_ficha(raiz, entrada['Ficha'])
    if p is None:
        return [f'ficha fora da main ou em falta ({entrada["Ficha"]})']
    if not p.exists():
        return [f'ficha não existe: {entrada["Ficha"]}']
    pasta = p if p.is_dir() else p.parent
    # A ficha indicada no registo tem prioridade (ficha_fontes.md também casa com 'ficha*.md').
    ficha = p if p.is_file() else next((f for pd in PECAS['ficha'] for f in sorted(pasta.glob(pd))), None)
    txt = ficha.read_text(encoding='utf-8') if ficha else ''
    # Estrutura antiga (Conde, Meta em Curto): legendas em <frente>/legendas/<epNN>_*.txt,
    # com o comentário fixado dentro do mesmo ficheiro.
    prefixo = (p.stem if p.is_file() else p.name).split('_')[0]
    antigas = sorted((pasta.parent / 'legendas').glob(f'{prefixo}_*.txt')) if prefixo else []
    txt_antigas = ' '.join(f.read_text(encoding='utf-8') for f in antigas)
    for peca, padroes in PECAS.items():
        if any(any(pasta.glob(pd)) for pd in padroes):
            continue
        if peca == 'legenda' and antigas:
            continue
        if peca == 'comentário fixado' and 'COMENTÁRIO FIXADO' in txt_antigas.upper():
            continue
        if peca == 'roteiro' and re.search(r'(?im)^#+ *(roteiro definitivo|narração final|guião)', txt):
            continue
        faltas.append(peca)
    if ficha:
        for marca, nome in (('Controlo de qualidade', 'controlo de qualidade na ficha'),
                            ('Ficheiros finais', 'localização do vídeo e da capa na ficha')):
            if marca.lower() not in txt.lower():
                faltas.append(nome)
        if entrada['ID'] not in txt:
            faltas.append('ID editorial na ficha')
    if entrada['Estado'] not in ('CONCLUÍDO', 'PUBLICADO'):
        faltas.append(f'estado no registo é {entrada["Estado"]} (esperado CONCLUÍDO ou PUBLICADO)')
    hist = raiz / 'comum' / 'historico.md'
    if not hist.exists() or entrada['ID'] not in hist.read_text(encoding='utf-8'):
        faltas.append('linha em comum/historico.md com o ID')
    return faltas


# ---------------------------------------------------------------- insights

def validar_insights(raiz, ids):
    erros = []
    base = raiz / 'comum' / 'insights'
    csv_p = base / 'registo_posts.csv'
    if not csv_p.exists():
        return [f'{csv_p} não existe']
    with csv_p.open(encoding='utf-8', newline='') as f:
        leitor = csv.DictReader(f)
        if leitor.fieldnames != CSV_COLUNAS:
            erros.append(f'registo_posts.csv: cabeçalho diferente do esperado ({CSV_COLUNAS})')
            return erros
        chaves = set()
        for n, r in enumerate(leitor, 2):
            k = (r['semana_fim'], r['periodo'], r['post_ref'])
            if k in chaves:
                erros.append(f'registo_posts.csv:{n}: linha repetida {k}')
            chaves.add(k)
            try:
                dt.date.fromisoformat(r['semana_fim'])
            except ValueError:
                erros.append(f'registo_posts.csv:{n}: semana_fim inválida "{r["semana_fim"]}"')
            if r['impulsionado'] not in PROMOCAO:
                erros.append(f'registo_posts.csv:{n}: impulsionado "{r["impulsionado"]}" '
                             f'(usar {", ".join(sorted(PROMOCAO))}; sem confirmação = A CONFIRMAR)')
            if r['impulsionado'] == 'NÃO' and r['investimento'] not in ('', '0'):
                erros.append(f'registo_posts.csv:{n}: NÃO impulsionado com investimento')
            if r['investimento'] and not r['moeda']:
                erros.append(f'registo_posts.csv:{n}: investimento sem moeda')
            if r['id_editorial'] not in ('', 'SEM-ID') and r['id_editorial'] not in ids:
                erros.append(f'registo_posts.csv:{n}: ID editorial desconhecido {r["id_editorial"]}')
            for c in NUMERICAS:
                if r[c] and not re.fullmatch(r'\d+', r[c]):
                    erros.append(f'registo_posts.csv:{n}: {c}="{r[c]}" não é inteiro (vazio se não visível)')
            sem = base / 'semanas' / f'{r["semana_fim"]}.md'
            if not sem.exists():
                erros.append(f'registo_posts.csv:{n}: falta o relatório semanas/{r["semana_fim"]}.md')
    return erros


CONTA_COLUNAS = ['periodo_inicio', 'periodo_fim', 'dias', 'seguidores', 'visualizacoes_reels', 'visualizadores',
                 'visualizacoes_total', 'contas_alcancadas', 'interacoes', 'curtidas', 'comentarios', 'reposts',
                 'partilhas', 'guardados', 'visitas_perfil', 'toques_link', 'reels_no_periodo', 'fonte', 'notas']


def validar_conta(raiz):
    erros = []
    p = raiz / 'comum' / 'insights' / 'registo_conta.csv'
    if not p.exists():
        return erros
    with p.open(encoding='utf-8', newline='') as f:
        leitor = csv.DictReader(f)
        if leitor.fieldnames != CONTA_COLUNAS:
            return [f'registo_conta.csv: cabeçalho diferente do esperado ({CONTA_COLUNAS})']
        vistos = set()
        for n, r in enumerate(leitor, 2):
            k = (r['periodo_inicio'], r['periodo_fim'])
            if k in vistos:
                erros.append(f'registo_conta.csv:{n}: período repetido {k}')
            vistos.add(k)
            for c in ('periodo_inicio', 'periodo_fim'):
                try:
                    dt.date.fromisoformat(r[c])
                except ValueError:
                    erros.append(f'registo_conta.csv:{n}: {c} inválido "{r[c]}"')
            for c in CONTA_COLUNAS[2:17]:
                if r[c] and not re.fullmatch(r'\d+', r[c]):
                    erros.append(f'registo_conta.csv:{n}: {c}="{r[c]}" não é inteiro')
            if not (raiz / 'comum' / 'insights' / 'semanas' / f'{r["periodo_fim"]}.md').exists():
                erros.append(f'registo_conta.csv:{n}: falta o relatório semanas/{r["periodo_fim"]}.md')
    return erros


def nova_semana(raiz, data):
    dt.date.fromisoformat(data)
    base = raiz / 'comum' / 'insights'
    destino = base / 'semanas' / f'{data}.md'
    if destino.exists():
        raise FileExistsError(f'{destino} já existe: cada domingo cria um snapshot novo, nunca se reescreve')
    modelo = (base / 'MODELO_SEMANAL.md').read_text(encoding='utf-8')
    corpo = modelo.split('<!-- INÍCIO -->', 1)[-1].lstrip('\n')
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(corpo.replace('AAAA-MM-DD', data), encoding='utf-8')
    return destino


# ---------------------------------------------------------------- segredos

def procurar_segredos(raiz, ficheiros=None):
    if ficheiros is None:
        try:
            saida = subprocess.run(['git', '-C', str(raiz), 'ls-files'], capture_output=True, text=True, check=True)
            ficheiros = [raiz / f for f in saida.stdout.splitlines()]
        except (subprocess.CalledProcessError, FileNotFoundError):
            ficheiros = [p for p in raiz.rglob('*') if p.is_file() and '.git' not in p.parts]
    achados = []
    for p in ficheiros:
        if p.suffix.lower() in {'.png', '.jpg', '.jpeg', '.mp3', '.mp4', '.woff2', '.ttf', '.otf', '.mpeg', '.gif', '.zip'}:
            continue
        try:
            txt = p.read_text(encoding='utf-8', errors='ignore')
        except (OSError, IsADirectoryError):
            continue
        for padrao in SEGREDOS:
            for m in padrao.finditer(txt):
                achados.append(f'{p.relative_to(raiz)}: {m.group(0)[:12]}…')
    return achados


# ---------------------------------------------------------------- CLI

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--raiz', default=None, help='raiz do repositório (por defeito: deduzida)')
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('validar', help='valida o registo, o CSV de insights e procura segredos')
    p = sub.add_parser('pauta', help='auditoria de originalidade de uma pauta')
    p.add_argument('--objeto', required=True, help='carta, pessoa, deck ou evento (vários separados por ;)')
    p.add_argument('--tema', default='')
    p.add_argument('--gancho', default='')
    p = sub.add_parser('encerramento', help='confere o pacote de um episódio')
    p.add_argument('id')
    p = sub.add_parser('semana', help='cria comum/insights/semanas/AAAA-MM-DD.md a partir do modelo')
    p.add_argument('data')
    sub.add_parser('segredos', help='procura credenciais nos ficheiros versionados')
    a = ap.parse_args(argv)
    raiz = Path(a.raiz) if a.raiz else Path(__file__).resolve().parents[2]

    entradas, erros = ler_registo(raiz)
    if a.cmd == 'validar':
        e2, avisos = validar_registo(raiz, entradas)
        erros += e2 + validar_insights(raiz, {e['ID'] for e in entradas}) + validar_conta(raiz)
        seg = procurar_segredos(raiz)
        erros += [f'possível segredo: {s}' for s in seg]
        for x in erros:
            print('ERRO', x)
        print(f'{len(entradas)} conteúdos no registo · {len(avisos)} POR AUDITAR'
              + (' · inventário INCOMPLETO' if avisos else ' · sem lacunas retroativas'))
        print('OK' if not erros else f'{len(erros)} erro(s)')
        return 1 if erros else 0
    if a.cmd == 'pauta':
        conflitos = comparar_pauta(entradas, a.objeto, a.tema, a.gancho)
        bloqueia = any(b for _, _, b in conflitos)
        for e, motivo, b in conflitos:
            print(f'{"BLOQUEIA" if b else "AVISO   "} {e["ID"]} [{e["Estado"]}] {e["Frente"]}: {motivo}')
        if bloqueia:
            print('PAUTA BLOQUEADA: decisão do fundador registada em nucleo/DECISOES.md antes de avançar.')
            return 2
        print('PAUTA LIVRE' + (' (com avisos)' if conflitos else '') + ': sem conflito no registo.')
        return 0
    if a.cmd == 'encerramento':
        e = next((x for x in entradas if x['ID'] == a.id), None)
        if not e:
            print(f'{a.id} não está no registo')
            return 2
        faltas = verificar_encerramento(raiz, e)
        for f in faltas:
            print('FALTA', f)
        print('ENCERRAMENTO OK' if not faltas else f'ENCERRAMENTO INCOMPLETO ({len(faltas)} falta(s))')
        return 0 if not faltas else 2
    if a.cmd == 'semana':
        try:
            print(nova_semana(raiz, a.data))
        except FileExistsError as x:
            print('ERRO', x)
            return 1
        return 0
    if a.cmd == 'segredos':
        seg = procurar_segredos(raiz)
        for s in seg:
            print('SEGREDO?', s)
        print('OK' if not seg else f'{len(seg)} possível(eis) segredo(s)')
        return 1 if seg else 0


if __name__ == '__main__':
    sys.exit(main())
