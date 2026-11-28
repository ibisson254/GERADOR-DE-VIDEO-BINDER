#!/usr/bin/env python3
"""Evento `episode.completed`: a ponte entre o BINDER Originals e o Data Binder.

Só biblioteca padrão, 0 créditos, sem rede. Correr a partir da raiz do repositório (ou passar --raiz).

  python3 comum/ferramentas/eventos.py vozes MB-EP22 --data 2026-11-29 --fonte "fundador, 29/11 10:02, conversa X: «pode gerar as vozes»"
  python3 comum/ferramentas/eventos.py concluir MB-EP22 --qc /caminho/qc_video/qc.json
  python3 comum/ferramentas/eventos.py sincronizar --destino ../-Binder-Dados/entradas
  python3 comum/ferramentas/eventos.py pendentes
  python3 comum/ferramentas/eventos.py metricas MB-EP13
  python3 comum/ferramentas/eventos.py validar

Ordem que o `concluir` impõe: render → QC sem P0 (qc.json do `comum/qc/qc_video.py`) →
**aprovação final humana escrita na ficha** → pacote completo (memoria.py encerramento) →
evento no outbox + registo em PUBLICADO → sincronização com o Data Binder.

Regra do fundador (28/11/2026, 08:05): assim que ele autoriza as vozes, o episódio conta como publicado.
O `vozes` regista esse momento; o `concluir` garante PUBLICADO para quem ainda não estiver.

O modelo nunca aprova: sem a linha «Aprovação final: <nome> · <data>» na ficha, escrita pelo
fundador ou copiada das palavras dele com a fonte, o comando recusa.

Ficheiros (append-only, nunca se apagam linhas):
  comum/eventos/episodios.jsonl  um evento por linha; event_id determinístico (repetir não duplica)
  comum/eventos/sync.jsonl       tentativas de sincronização; um evento sem «sincronizado» continua pendente

Códigos de saída: 0 = ok · 1 = erros de validação · 2 = recusado (falta QC, aprovação ou pacote) ·
3 = houve falhas de sincronização (os eventos ficam pendentes para a próxima vez).
"""
import argparse
import csv
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import memoria as m  # noqa: E402

TIPO = 'episode.completed'
VERSAO = 1
CAMPOS = ['event_id', 'event_type', 'episode_id', 'series_id', 'production_status', 'approval_status',
          'qc_status', 'created_at', 'completed_at', 'video_path', 'duration_s', 'format', 'resolution',
          'fps', 'creative_attributes', 'source_branch', 'event_version']
OUTBOX = Path('comum/eventos/episodios.jsonl')
SYNC = Path('comum/eventos/sync.jsonl')
DESTINO_FICHEIRO = 'originals_episodios.jsonl'
NAO_HUMANOS = {'claude', 'modelo', 'agente', 'ia', 'ai', 'bot', 'assistente', 'automatico', 'automático'}
RE_APROVACAO = re.compile(r'(?im)^[-*\s]*aprova[çc][ãa]o final\s*:\s*(?P<nome>[^·|\n]+?)\s*·\s*'
                          r'(?P<data>\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})')
RE_VIDEO = re.compile(r'(?im)^[-*\s]*v[íi]deo\s*:\s*`?([^`\s]+\.(?:mp4|mov|webm))`?')
RE_ATRIBUTO = re.compile(r'(?im)^[-*\s]*(tipo_abertura|tipo_narrativa)\s*:\s*`?([a-z-]+)`?')
# O que cada métrica significa (o Data Binder recebe sempre a definição junto com o número).
DEFINICOES = {
    'visualizacoes': 'reproduções do Reel/post no período (Instagram Insights)',
    'alcance': 'contas únicas que viram pelo menos uma vez',
    'impressoes': 'vezes que o conteúdo apareceu no ecrã',
    'curtidas': 'gostos', 'comentarios': 'comentários', 'guardados': 'guardados', 'partilhas': 'partilhas',
    'visitas_perfil': 'visitas ao perfil a partir do conteúdo', 'novos_seguidores': 'seguidores ganhos a partir do conteúdo',
    'cliques_link': 'cliques no link (bio/sticker) atribuídos', 'alcance_pago': 'alcance da parte impulsionada',
    'duracao_s': 'duração do vídeo em segundos', 'tempo_medio_s': 'tempo médio de visualização em segundos',
    'pct_assistida': '% média assistida segundo o Instagram', 'taxa_saltos': '% que saiu nos primeiros 3 s',
}
METRICAS = [c for c in DEFINICOES]


def event_id(episode_id, tipo=TIPO, versao=VERSAO):
    """Determinístico: o mesmo episódio e versão do evento dão sempre o mesmo id."""
    return 'evt_' + hashlib.sha256(f'{episode_id}|{tipo}|{versao}'.encode()).hexdigest()[:24]


def _data_iso(txt):
    if re.fullmatch(r'\d{2}/\d{2}/\d{4}', txt):
        d, mth, a = txt.split('/')
        return f'{a}-{mth}-{d}'
    return txt


def ler_jsonl(caminho):
    if not caminho.exists():
        return []
    return [json.loads(l) for l in caminho.read_text(encoding='utf-8').splitlines() if l.strip()]


def _append(caminho, obj):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, 'a', encoding='utf-8') as fh:
        fh.write(json.dumps(obj, ensure_ascii=False, sort_keys=False) + '\n')


def ler_qc(caminho):
    """Lê o qc.json do qc_video.py. Devolve (estado, formato, problemas_p0)."""
    rel = json.loads(Path(caminho).read_text(encoding='utf-8'))
    p0 = [t for g, t in rel.get('problemas', []) if g == 'P0']
    return ('aprovado' if not p0 else 'reprovado'), rel.get('formato', {}), p0


def aprovacao_humana(txt_ficha):
    """Devolve (nome, data_iso) da aprovação final escrita na ficha, ou None."""
    mt = RE_APROVACAO.search(txt_ficha)
    if not mt:
        return None
    nome = mt.group('nome').strip()
    if m.norm(nome).strip() in NAO_HUMANOS or not nome:
        return None
    return nome, _data_iso(mt.group('data'))


def _git(raiz, *args):
    try:
        r = subprocess.run(['git', '-C', str(raiz), *args], capture_output=True, text=True, timeout=10)
        return (r.stdout.strip() or None) if r.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


def criado_em(raiz, ficha_rel):
    """Data do commit que criou a ficha (None fora do git: não se inventa)."""
    out = _git(raiz, 'log', '--diff-filter=A', '--format=%cs', '--', ficha_rel)
    return out.splitlines()[-1] if out else None


def _ficheiro_ficha(raiz, entrada):
    p = m.caminho_ficha(raiz, entrada['Ficha'])
    if p is None or not p.exists():
        return None
    pasta = p if p.is_dir() else p.parent
    return next((f for pd in m.PECAS['ficha'] for f in sorted(pasta.glob(pd))), None)


def montar_evento(raiz, entrada, ficha_txt, ficha_rel, aprov, qc_estado, formato, video=None, branch=None):
    w, h, fps, dur = (formato.get(k) for k in ('w', 'h', 'fps', 'dur'))
    v = video or (RE_VIDEO.search(ficha_txt).group(1) if RE_VIDEO.search(ficha_txt) else None)
    return {
        'event_id': event_id(entrada['ID']),
        'event_type': TIPO,
        'episode_id': entrada['ID'],
        'series_id': entrada['ID'].split('-')[0],
        'production_status': 'PUBLICADO',
        'approval_status': 'aprovado',
        'approved_by': aprov[0],
        'qc_status': qc_estado,
        'created_at': criado_em(raiz, ficha_rel),
        'completed_at': aprov[1],
        'video_path': v,
        'duration_s': round(dur, 2) if isinstance(dur, (int, float)) else None,
        'format': ('9:16' if w and h and abs(w / h - 9 / 16) < 0.01 else (f'{w}:{h}' if w and h else None)),
        'resolution': f'{w}x{h}' if w and h else None,
        'fps': fps if isinstance(fps, (int, float)) else None,
        'creative_attributes': {k: val for k, val in RE_ATRIBUTO.findall(ficha_txt)},
        'source_branch': branch if branch is not None else _git(raiz, 'rev-parse', '--abbrev-ref', 'HEAD'),
        'event_version': VERSAO,
    }


REGRA_VOZES = 'regra do fundador de 28/11/2026 08:05: vozes autorizadas = publicado'
ANTES_DE_PUBLICADO = ('APROVADO', 'EM PRODUÇÃO', 'CONCLUÍDO')


def marcar_publicado(raiz, entrada, fonte, data):
    """Passa a linha do registo a PUBLICADO (regra de 28/11: vozes autorizadas = publicado).
    Só a partir de APROVADO/EM PRODUÇÃO/CONCLUÍDO; só muda Estado, Publicação (se vazia) e acrescenta à Fonte."""
    if entrada['Estado'] not in ANTES_DE_PUBLICADO:
        return False
    caminho = raiz / 'comum' / 'REGISTRO_EDITORIAL.md'
    linhas = caminho.read_text(encoding='utf-8').split('\n')
    i = entrada['_linha'] - 1
    cel = [c.strip() for c in linhas[i].strip().strip('|').split('|')]
    assert cel[0] == entrada['ID'], 'linha do registo mudou desde a leitura'
    cel[m.COLUNAS.index('Estado')] = 'PUBLICADO'
    k = m.COLUNAS.index('Publicação')
    if cel[k] in m.VAZIOS | {'A CONFIRMAR', 'não publicada'} or cel[k].startswith(('agendad', 'não publicad')):
        cel[k] = f'vozes autorizadas a {data} ({REGRA_VOZES}; data exata do post por confirmar)'
    k = m.COLUNAS.index('Fonte do estado')
    cel[k] = f'{cel[k]} · PUBLICADO: {fonte}'
    linhas[i] = '| ' + ' | '.join(cel) + ' |'
    caminho.write_text('\n'.join(linhas), encoding='utf-8')
    return True


def vozes_autorizadas(raiz, episodio, data, fonte):
    """Registo do momento em que o fundador autoriza as vozes: o episódio passa a PUBLICADO."""
    if not fonte or not fonte.strip():
        return 2, ['RECUSADO: falta a fonte (as palavras do fundador, com data e onde)']
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}', data or ''):
        return 2, ['RECUSADO: data em AAAA-MM-DD ou DD/MM/AAAA']
    entradas, _ = m.ler_registo(raiz)
    e = next((x for x in entradas if x['ID'] == episodio), None)
    if not e:
        return 2, [f'{episodio} não está no registo']
    if marcar_publicado(raiz, e, f'fundador autorizou as vozes ({fonte.strip()})', data):
        return 0, [f'{episodio}: {e["Estado"]} → PUBLICADO ({REGRA_VOZES})']
    return 0, [f'{episodio}: estado {e["Estado"]} mantido']


def concluir(raiz, episodio, qc_json, video=None, branch=None):
    """Devolve (código, mensagens, evento|None)."""
    entradas, erros = m.ler_registo(raiz)
    e = next((x for x in entradas if x['ID'] == episodio), None)
    if not e:
        return 2, [f'{episodio} não está no registo'], None
    ficha = _ficheiro_ficha(raiz, e)
    if ficha is None:
        return 2, [f'ficha de {episodio} não encontrada ({e["Ficha"]})'], None
    txt = ficha.read_text(encoding='utf-8')
    if not qc_json or not Path(qc_json).exists():
        return 2, ['RECUSADO: falta o qc.json do comum/qc/qc_video.py (o QC vem antes da aprovação)'], None
    qc_estado, formato, p0 = ler_qc(qc_json)
    if qc_estado != 'aprovado':
        return 2, ['RECUSADO: QC com P0 — ' + '; '.join(p0)], None
    aprov = aprovacao_humana(txt)
    if not aprov:
        return 2, ['RECUSADO: sem aprovação final humana na ficha '
                   '(linha «Aprovação final: <nome> · <data>», escrita pelo fundador)'], None
    faltas = [f for f in m.verificar_encerramento(raiz, e) if not f.startswith('estado no registo')]
    if faltas:
        return 2, ['RECUSADO: pacote incompleto — ' + '; '.join(faltas)], None
    eid = event_id(episodio)
    outbox = raiz / OUTBOX
    if any(ev.get('event_id') == eid for ev in ler_jsonl(outbox)):
        return 0, [f'{episodio}: evento {eid} já existe, nada a fazer (idempotente)'], None
    ev = montar_evento(raiz, e, txt, str(ficha.relative_to(raiz)), aprov, qc_estado, formato, video, branch)
    _append(outbox, ev)
    msgs = [f'evento {eid} gravado em {OUTBOX} (sincronização pendente)']
    if marcar_publicado(raiz, e, f'`eventos.py concluir` ({eid}; {REGRA_VOZES})', aprov[1]):
        msgs.append(f'{episodio}: registo passou a PUBLICADO')
    else:
        msgs.append(f'{episodio}: estado {e["Estado"]} mantido')
    return 0, msgs, ev


def estado_sync(raiz):
    """{event_id: 'sincronizado' | 'pendente'} a partir do outbox e das tentativas."""
    feitos = {s['event_id'] for s in ler_jsonl(raiz / SYNC) if s.get('estado') == 'sincronizado'}
    return {ev['event_id']: ('sincronizado' if ev['event_id'] in feitos else 'pendente')
            for ev in ler_jsonl(raiz / OUTBOX)}


def entregar_em_pasta(destino):
    """Destino por defeito: um JSONL na pasta do Data Binder (clone local). Idempotente por event_id."""
    def entregar(ev):
        pasta = Path(destino)
        if not pasta.is_dir():
            raise FileNotFoundError(f'destino não existe: {pasta}')
        f = pasta / DESTINO_FICHEIRO
        if any(x.get('event_id') == ev['event_id'] for x in ler_jsonl(f)):
            return
        _append(f, ev)
    return entregar


def sincronizar(raiz, entregar, agora=None):
    """Tenta entregar cada evento pendente. Falha = fica pendente e regista a tentativa. Devolve (ok, falhas)."""
    agora = agora or dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    estados = estado_sync(raiz)
    ok, falhas = [], []
    for ev in ler_jsonl(raiz / OUTBOX):
        if estados.get(ev['event_id']) != 'pendente':
            continue
        try:
            entregar(ev)
        except Exception as x:  # noqa: BLE001 — qualquer falha deixa o evento pendente
            _append(raiz / SYNC, {'event_id': ev['event_id'], 'estado': 'falhou', 'em': agora,
                                  'erro': f'{type(x).__name__}: {x}'[:200]})
            falhas.append(ev['event_id'])
            continue
        _append(raiz / SYNC, {'event_id': ev['event_id'], 'estado': 'sincronizado', 'em': agora})
        ok.append(ev['event_id'])
    return ok, falhas


def _num(v):
    v = (v or '').strip()
    if v in m.VAZIOS:
        return None
    try:
        return float(v.replace(',', '.')) if re.search(r'[.,]', v) else int(v)
    except ValueError:
        return None


def metricas(raiz, episodio):
    """Leituras do registo_posts.csv para um episódio: origem, período, definição e id preservados.
    Célula vazia = None (nunca 0, nunca estimado)."""
    f = raiz / 'comum' / 'insights' / 'registo_posts.csv'
    if not f.exists():
        return []
    out = []
    with open(f, encoding='utf-8', newline='') as fh:
        for r in csv.DictReader(fh):
            if r.get('id_editorial') != episodio:
                continue
            out.append({
                'id_editorial': r['id_editorial'], 'post_ref': r.get('post_ref') or None,
                'semana_fim': r.get('semana_fim') or None, 'periodo': r.get('periodo') or None,
                'fonte': r.get('fonte') or None,
                'valores': {k: _num(r.get(k)) for k in METRICAS if k in r},
                'definicoes': {k: DEFINICOES[k] for k in METRICAS if k in r},
            })
    return out


def validar(raiz):
    erros = []
    ids = {e['ID'] for e in m.ler_registo(raiz)[0]}
    vistos = set()
    try:
        evs = ler_jsonl(raiz / OUTBOX)
        tent = ler_jsonl(raiz / SYNC)
    except json.JSONDecodeError as x:
        return [f'JSON inválido em comum/eventos/: {x}']
    for n, ev in enumerate(evs, 1):
        falta = [c for c in CAMPOS if c not in ev]
        if falta:
            erros.append(f'evento {n}: faltam campos {falta}')
            continue
        if ev['event_id'] != event_id(ev['episode_id'], ev['event_type'], ev['event_version']):
            erros.append(f'evento {n}: event_id não bate com o episódio (alterado à mão?)')
        if ev['event_id'] in vistos:
            erros.append(f'evento {n}: duplicado ({ev["event_id"]})')
        vistos.add(ev['event_id'])
        if ev['episode_id'] not in ids:
            erros.append(f'evento {n}: {ev["episode_id"]} não está no registo')
        if ev['approval_status'] != 'aprovado' or ev['qc_status'] != 'aprovado':
            erros.append(f'evento {n}: sem aprovação humana ou QC aprovado')
    for n, s in enumerate(tent, 1):
        if s.get('event_id') not in vistos:
            erros.append(f'sync {n}: event_id desconhecido')
    return erros


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--raiz', default=None)
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('concluir', help='QC + aprovação humana + pacote → evento e registo CONCLUÍDO')
    p.add_argument('id')
    p.add_argument('--qc', required=True, help='qc.json gerado por comum/qc/qc_video.py')
    p.add_argument('--video', default=None, help='caminho do vídeo final (por defeito: linha «Vídeo:» da ficha)')
    p = sub.add_parser('sincronizar', help='entrega os eventos pendentes ao Data Binder')
    p.add_argument('--destino', required=True, help='pasta do clone do Data Binder (ex.: ../-Binder-Dados/entradas)')
    p = sub.add_parser('vozes', help='o fundador autorizou as vozes: o episódio passa a PUBLICADO (regra de 28/11)')
    p.add_argument('id')
    p.add_argument('--data', required=True)
    p.add_argument('--fonte', required=True, help='palavras do fundador, com data e onde')
    sub.add_parser('pendentes', help='lista eventos por sincronizar')
    p = sub.add_parser('metricas', help='leituras de um episódio com origem, período e definição')
    p.add_argument('id')
    sub.add_parser('validar', help='valida o outbox e as tentativas de sincronização')
    a = ap.parse_args(argv)
    raiz = Path(a.raiz) if a.raiz else AQUI.parents[1]

    if a.cmd == 'concluir':
        cod, msgs, _ = concluir(raiz, a.id, a.qc, a.video)
        print('\n'.join(msgs))
        return cod
    if a.cmd == 'vozes':
        cod, msgs = vozes_autorizadas(raiz, a.id, a.data, a.fonte)
        print('\n'.join(msgs))
        return cod
    if a.cmd == 'sincronizar':
        ok, falhas = sincronizar(raiz, entregar_em_pasta(a.destino))
        print(f'{len(ok)} sincronizado(s) · {len(falhas)} falha(s) (ficam pendentes)')
        return 3 if falhas else 0
    if a.cmd == 'pendentes':
        pend = [k for k, v in estado_sync(raiz).items() if v == 'pendente']
        print('\n'.join(pend) if pend else 'nenhum evento pendente')
        return 0
    if a.cmd == 'metricas':
        print(json.dumps(metricas(raiz, a.id), ensure_ascii=False, indent=2))
        return 0
    erros = validar(raiz)
    for x in erros:
        print('ERRO', x)
    print(f'{len(ler_jsonl(raiz / OUTBOX))} evento(s) · ' + ('OK' if not erros else f'{len(erros)} erro(s)'))
    return 1 if erros else 0


if __name__ == '__main__':
    sys.exit(main())
