#!/usr/bin/env python3
"""Testes 1–10 do evento `episode.completed` (missão de engenharia de 28/11/2026).

Só mocks e cópias temporárias: nenhuma rede, nenhum crédito, nenhum vídeo real.

  python3 -I comum/ferramentas/test_eventos.py
"""
import csv
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
sys.path.insert(0, str(AQUI))
import eventos as ev  # noqa: E402
import memoria as m  # noqa: E402

EP = 'MB-EP21'
PASTA_EP = 'manaburn/episodios/ep21_capacete_obediencia'
APROVACAO = '\n- Aprovação final: Ibisson · 27/11/2026 (teste)\n- tipo_abertura: objeto\n'
FORMATO_OK = {'w': 1080, 'h': 1920, 'fps': 30.0, 'dur': 54.37}


def repo_teste(dest, estado='EM PRODUÇÃO', aprovacao=APROVACAO):
    """Cópia mínima do repositório com o MB-EP21 de volta a EM PRODUÇÃO e (opcional) aprovação na ficha."""
    for rel in ('comum/REGISTRO_EDITORIAL.md', 'comum/historico.md', 'comum/insights/registo_posts.csv',
                'comum/reconciliacao/2026-11-28_publicados.csv'):
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(RAIZ / rel, dest / rel)
    (dest / PASTA_EP).mkdir(parents=True)
    for f in (RAIZ / PASTA_EP).iterdir():
        if f.is_file() and f.suffix in ('.md', '.txt', '.json'):
            shutil.copy(f, dest / PASTA_EP / f.name)
    reg = dest / 'comum/REGISTRO_EDITORIAL.md'
    linhas = reg.read_text(encoding='utf-8').split('\n')
    for i, l in enumerate(linhas):
        if l.startswith(f'| {EP} |'):
            cel = [c.strip() for c in l.strip().strip('|').split('|')]
            cel[m.COLUNAS.index('Estado')] = estado
            linhas[i] = '| ' + ' | '.join(cel) + ' |'
    reg.write_text('\n'.join(linhas), encoding='utf-8')
    if aprovacao:
        with open(dest / PASTA_EP / 'ficha.md', 'a', encoding='utf-8') as fh:
            fh.write(aprovacao)


def qc(dest, problemas=(), formato=FORMATO_OK):
    p = dest / 'qc.json'
    p.write_text(json.dumps({'formato': formato, 'problemas': list(problemas)}), encoding='utf-8')
    return p


def estado(raiz, ep=EP):
    return next(e['Estado'] for e in m.ler_registo(raiz)[0] if e['ID'] == ep)


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)


class T01_ConclusaoNormal(Base):
    def test_evento_completo_e_registo_concluido(self):
        repo_teste(self.tmp)
        cod, msgs, e = ev.concluir(self.tmp, EP, qc(self.tmp), branch='main')
        self.assertEqual(cod, 0, msgs)
        self.assertEqual(set(ev.CAMPOS) - set(e), set())
        self.assertEqual(e['event_id'], ev.event_id(EP))
        self.assertEqual((e['resolution'], e['fps'], e['duration_s'], e['format']), ('1080x1920', 30.0, 54.37, '9:16'))
        self.assertEqual((e['approval_status'], e['approved_by'], e['completed_at']), ('aprovado', 'Ibisson', '2026-11-27'))
        self.assertEqual(e['creative_attributes'], {'tipo_abertura': 'objeto'})
        self.assertTrue(e['video_path'].endswith('.mp4'))
        self.assertIsNone(e['created_at'])  # fora do git não se inventa a data
        self.assertEqual(estado(self.tmp), 'PUBLICADO')
        self.assertEqual(ev.estado_sync(self.tmp), {e['event_id']: 'pendente'})
        self.assertEqual(ev.validar(self.tmp), [])


class T01b_RegraDasVozes(Base):
    def test_vozes_autorizadas_publica(self):
        repo_teste(self.tmp, aprovacao='')
        cod, msgs = ev.vozes_autorizadas(self.tmp, EP, '28/11/2026', 'fundador, 28/11 08:05: «pode gerar as vozes» (teste)')
        self.assertEqual(cod, 0, msgs)
        e = next(x for x in m.ler_registo(self.tmp)[0] if x['ID'] == EP)
        self.assertEqual(e['Estado'], 'PUBLICADO')
        self.assertIn('fundador autorizou as vozes', e['Fonte do estado'])
        e2, _ = m.validar_registo(self.tmp, m.ler_registo(self.tmp)[0])
        self.assertFalse([x for x in e2 if EP in x])

    def test_sem_fonte_recusa(self):
        repo_teste(self.tmp, aprovacao='')
        self.assertEqual(ev.vozes_autorizadas(self.tmp, EP, '28/11/2026', ' ')[0], 2)
        self.assertEqual(estado(self.tmp), 'EM PRODUÇÃO')

    def test_concluido_passa_a_publicado(self):
        repo_teste(self.tmp, estado='CONCLUÍDO')
        cod, _, e = ev.concluir(self.tmp, EP, qc(self.tmp), branch='main')
        self.assertEqual((cod, estado(self.tmp), e['production_status']), (0, 'PUBLICADO', 'PUBLICADO'))

    def test_rejeitado_nao_muda(self):
        repo_teste(self.tmp, estado='REJEITADO', aprovacao='')
        ev.vozes_autorizadas(self.tmp, EP, '28/11/2026', 'teste')
        self.assertEqual(estado(self.tmp), 'REJEITADO')


class T02_EventoDuplicado(Base):
    def test_segunda_conclusao_nao_duplica(self):
        repo_teste(self.tmp)
        ev.concluir(self.tmp, EP, qc(self.tmp), branch='main')
        cod, msgs, e = ev.concluir(self.tmp, EP, qc(self.tmp), branch='outra')
        self.assertEqual(cod, 0)
        self.assertIsNone(e)
        self.assertIn('já existe', msgs[0])
        self.assertEqual(len(ev.ler_jsonl(self.tmp / ev.OUTBOX)), 1)

    def test_id_deterministico(self):
        self.assertEqual(ev.event_id(EP), ev.event_id(EP))
        self.assertNotEqual(ev.event_id(EP), ev.event_id('MB-EP20'))
        self.assertNotEqual(ev.event_id(EP), ev.event_id(EP, versao=2))


class T03_FalhaDeSync(Base):
    def test_falha_fica_pendente_e_recupera(self):
        repo_teste(self.tmp)
        _, _, e = ev.concluir(self.tmp, EP, qc(self.tmp), branch='main')

        def cai(_):
            raise ConnectionError('Data Binder indisponível (mock)')
        ok, falhas = ev.sincronizar(self.tmp, cai, agora='T1')
        self.assertEqual((ok, falhas), ([], [e['event_id']]))
        self.assertEqual(ev.estado_sync(self.tmp)[e['event_id']], 'pendente')
        self.assertEqual(len(ev.ler_jsonl(self.tmp / ev.OUTBOX)), 1)  # nada se perdeu
        destino = self.tmp / 'binder-dados'
        destino.mkdir()
        ok, falhas = ev.sincronizar(self.tmp, ev.entregar_em_pasta(destino), agora='T2')
        self.assertEqual((ok, falhas), ([e['event_id']], []))
        self.assertEqual(ev.estado_sync(self.tmp)[e['event_id']], 'sincronizado')
        tent = ev.ler_jsonl(self.tmp / ev.SYNC)
        self.assertEqual([t['estado'] for t in tent], ['falhou', 'sincronizado'])

    def test_destino_inexistente_conta_como_falha(self):
        repo_teste(self.tmp)
        ev.concluir(self.tmp, EP, qc(self.tmp), branch='main')
        ok, falhas = ev.sincronizar(self.tmp, ev.entregar_em_pasta(self.tmp / 'nao-existe'))
        self.assertEqual(len(falhas), 1)


class T04_SemAprovacaoHumana(Base):
    def test_sem_linha_recusa(self):
        repo_teste(self.tmp, aprovacao='')
        cod, msgs, e = ev.concluir(self.tmp, EP, qc(self.tmp), branch='main')
        self.assertEqual(cod, 2)
        self.assertIn('aprovação final humana', msgs[0])
        self.assertFalse((self.tmp / ev.OUTBOX).exists())
        self.assertEqual(estado(self.tmp), 'EM PRODUÇÃO')

    def test_modelo_nao_aprova(self):
        repo_teste(self.tmp, aprovacao='\n- Aprovação final: Claude · 2026-11-27\n')
        cod, _, _ = ev.concluir(self.tmp, EP, qc(self.tmp), branch='main')
        self.assertEqual(cod, 2)


class T05_QCFalhado(Base):
    def test_p0_recusa(self):
        repo_teste(self.tmp)
        cod, msgs, _ = ev.concluir(self.tmp, EP, qc(self.tmp, [['P0', 'fecho do scanner não encontrado']]), branch='m')
        self.assertEqual(cod, 2)
        self.assertIn('P0', msgs[0])
        self.assertFalse((self.tmp / ev.OUTBOX).exists())
        self.assertEqual(estado(self.tmp), 'EM PRODUÇÃO')

    def test_sem_qc_recusa(self):
        repo_teste(self.tmp)
        cod, _, _ = ev.concluir(self.tmp, EP, self.tmp / 'nao-ha.json', branch='m')
        self.assertEqual(cod, 2)

    def test_p1_nao_bloqueia(self):
        repo_teste(self.tmp)
        cod, _, _ = ev.concluir(self.tmp, EP, qc(self.tmp, [['P1', 'loudness -16 LUFS']]), branch='m')
        self.assertEqual(cod, 0)


class T06_ReconciliacaoHistorica(Base):
    def test_csv_bate_com_o_registo(self):
        reg = {e['ID']: e for e in m.ler_registo(RAIZ)[0]}
        with open(RAIZ / 'comum/reconciliacao/2026-11-28_publicados.csv', encoding='utf-8', newline='') as fh:
            linhas = list(csv.DictReader(fh))
        self.assertGreater(len(linhas), 0)
        for r in linhas:
            self.assertIn(r['id'], reg, 'ID histórico desapareceu ou mudou')
            self.assertEqual(reg[r['id']]['Estado'], r['estado_depois'])
            self.assertNotEqual(r['estado_antes'], r['estado_depois'])

    def test_publicado_nunca_recua(self):
        repo_teste(self.tmp, estado='PUBLICADO')
        cod, msgs, _ = ev.concluir(self.tmp, EP, qc(self.tmp), branch='main')
        self.assertEqual(cod, 0)
        self.assertEqual(estado(self.tmp), 'PUBLICADO')
        self.assertIn('mantido', msgs[-1])

    def test_so_a_linha_do_episodio_muda(self):
        repo_teste(self.tmp)
        antes = (self.tmp / 'comum/REGISTRO_EDITORIAL.md').read_text(encoding='utf-8').split('\n')
        ev.concluir(self.tmp, EP, qc(self.tmp), branch='main')
        depois = (self.tmp / 'comum/REGISTRO_EDITORIAL.md').read_text(encoding='utf-8').split('\n')
        dif = [i for i, (a, b) in enumerate(zip(antes, depois)) if a != b]
        self.assertEqual(len(antes), len(depois))
        self.assertEqual(len(dif), 1)
        self.assertTrue(depois[dif[0]].startswith(f'| {EP} |'))


class T07_MetricaAusente(Base):
    def test_celula_vazia_e_none(self):
        leituras = ev.metricas(RAIZ, 'MB-EP13')
        self.assertGreater(len(leituras), 0)
        for r in leituras:
            self.assertIsNone(r['valores']['impressoes'])  # vazia no CSV: não vira 0
        self.assertEqual(ev._num(''), None)
        self.assertEqual(ev._num('—'), None)
        self.assertEqual(ev._num('0'), 0)

    def test_evento_sem_formato_fica_null(self):
        repo_teste(self.tmp)
        _, _, e = ev.concluir(self.tmp, EP, qc(self.tmp, formato={}), branch='main')
        self.assertEqual((e['duration_s'], e['fps'], e['resolution'], e['format']), (None, None, None, None))


class T08_ConsultaPreservaContexto(Base):
    def test_origem_periodo_definicao_id(self):
        r = ev.metricas(RAIZ, 'MB-EP13')[0]
        self.assertEqual(r['id_editorial'], 'MB-EP13')
        self.assertTrue(r['fonte'] and r['periodo'] and r['semana_fim'])
        self.assertEqual(r['valores']['visualizacoes'], 19688)
        self.assertIn('Instagram', r['definicoes']['visualizacoes'])
        self.assertEqual(set(r['valores']), set(r['definicoes']))

    def test_episodio_sem_numeros_devolve_lista_vazia(self):
        self.assertEqual(ev.metricas(RAIZ, 'MB-EP21'), [])


class T09_ValidacoesCruzadas(unittest.TestCase):
    def test_outbox_real_valido(self):
        self.assertEqual(ev.validar(RAIZ), [])

    def test_campos_da_missao(self):
        pedidos = {'episode_id', 'series_id', 'production_status', 'approval_status', 'qc_status', 'created_at',
                   'completed_at', 'video_path', 'duration_s', 'format', 'resolution', 'fps',
                   'creative_attributes', 'source_branch', 'event_version'}
        self.assertLessEqual(pedidos, set(ev.CAMPOS))

    def test_csv_de_insights_compativel(self):
        with open(RAIZ / 'comum/insights/registo_posts.csv', encoding='utf-8', newline='') as fh:
            cab = next(csv.reader(fh))
        self.assertLessEqual(set(m.CSV_COLUNAS), set(cab))
        self.assertIn('id_editorial', cab)
        for c in m.NUMERICAS:
            self.assertIn(c, ev.DEFINICOES, f'métrica {c} sem definição')

    def test_evento_alterado_a_mao_e_detetado(self):
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            repo_teste(t)
            ev.concluir(t, EP, qc(t), branch='main')
            f = t / ev.OUTBOX
            f.write_text(f.read_text(encoding='utf-8').replace(EP, 'MB-EP20'), encoding='utf-8')
            self.assertTrue(any('event_id' in x for x in ev.validar(t)))


class T10_ReexecucaoSemDuplicar(Base):
    def test_tudo_duas_vezes(self):
        repo_teste(self.tmp)
        destino = self.tmp / 'binder-dados'
        destino.mkdir()
        for _ in range(2):
            ev.concluir(self.tmp, EP, qc(self.tmp), branch='main')
            ev.sincronizar(self.tmp, ev.entregar_em_pasta(destino))
        self.assertEqual(len(ev.ler_jsonl(self.tmp / ev.OUTBOX)), 1)
        self.assertEqual(len(ev.ler_jsonl(destino / ev.DESTINO_FICHEIRO)), 1)
        self.assertEqual([t['estado'] for t in ev.ler_jsonl(self.tmp / ev.SYNC)], ['sincronizado'])
        self.assertEqual(ev.validar(self.tmp), [])

    def test_entrega_repetida_no_destino_nao_duplica(self):
        destino = self.tmp
        e = {'event_id': 'evt_x'}
        ev.entregar_em_pasta(destino)(e)
        ev.entregar_em_pasta(destino)(e)
        self.assertEqual(len(ev.ler_jsonl(destino / ev.DESTINO_FICHEIRO)), 1)


if __name__ == '__main__':
    unittest.main(verbosity=1)
