#!/usr/bin/env python3
"""Testes de aceitação da memória editorial (A–F). Correr na raiz:

  python3 -m unittest comum/ferramentas/test_memoria.py -v
"""
import csv
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
sys.path.insert(0, str(AQUI))
import memoria as m  # noqa: E402


def repo_minimo(dest):
    """Cópia mínima do repositório para testes que escrevem ficheiros."""
    for rel in ('comum/REGISTRO_EDITORIAL.md', 'comum/historico.md', 'comum/insights/MODELO_SEMANAL.md',
                'comum/insights/registo_posts.csv'):
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(RAIZ / rel, dest / rel)
    shutil.copytree(RAIZ / 'comum/insights/semanas', dest / 'comum/insights/semanas')


class A_Duplicidade(unittest.TestCase):
    def setUp(self):
        self.reg, erros = m.ler_registo(RAIZ)
        self.assertEqual(erros, [])

    def test_pauta_publicada_bloqueada(self):
        c = m.comparar_pauta(self.reg, 'Stasis', 'carta mais odiada do Commander')
        self.assertTrue(any(e['ID'] == 'MB-EP02' and b for e, _, b in c))

    def test_mudar_frente_e_titulo_nao_liberta(self):
        # Mesmo objeto (Knacksaw Clique) proposto noutra frente e com outro título.
        c = m.comparar_pauta(self.reg, 'Knacksaw Clique', 'curiosidade sobre fadas de Shadowmoor')
        self.assertTrue(any(e['ID'] == 'MB-EP05' and b for e, _, b in c))

    def test_objeto_dentro_de_lista(self):
        c = m.comparar_pauta(self.reg, 'Leyline of Anticipation')
        ids = {e['ID'] for e, _, b in c if b}
        self.assertTrue({'MB-EP07', 'MB-GIRO01'} <= ids)

    def test_pauta_nova_livre(self):
        self.assertEqual(m.comparar_pauta(self.reg, 'Grist, the Hunger Tide', 'planeswalker inseto'), [])

    def test_rejeitado_so_avisa(self):
        reg = [dict(self.reg[0], ID='MB-EP99', Estado='REJEITADO', Objeto='Carta Inventada Teste')]
        c = m.comparar_pauta(reg, 'Carta Inventada Teste')
        self.assertTrue(c and not any(b for _, _, b in c))


class B_Continuidade(unittest.TestCase):
    def test_registo_valido_e_todas_as_frentes(self):
        reg, erros = m.ler_registo(RAIZ)
        e2, _ = m.validar_registo(RAIZ, reg)
        self.assertEqual(erros + e2, [])
        prefixos = {e['ID'].split('-')[0] for e in reg}
        self.assertTrue({'MB', 'MC', 'CM', 'ESP', 'ORB', 'LL'} <= prefixos)

    def test_todas_as_fichas_do_repositorio_estao_no_registo(self):
        reg, _ = m.ler_registo(RAIZ)
        fichas_reg = ' '.join(e['Ficha'] for e in reg)
        fichas = [p for p in RAIZ.glob('*/episodios/**/*ficha*.md')] + list(RAIZ.glob('especiais/*/LEIA-ME.md'))
        self.assertTrue(fichas)
        for p in fichas:
            rel = p.relative_to(RAIZ).as_posix()
            pasta = p.parent.relative_to(RAIZ).as_posix()
            self.assertTrue(rel in fichas_reg or pasta + '/' in fichas_reg, f'{rel} não está no registo')

    def test_episodios_por_frente_identificaveis(self):
        reg, _ = m.ler_registo(RAIZ)
        mb = [e['ID'] for e in reg if e['Frente'] == 'Mana & Burn']
        self.assertIn('MB-EP09', mb)
        self.assertIn('MB-EP01', mb)


class C_Encerramento(unittest.TestCase):
    def _episodio(self, raiz, completo=True):
        pasta = raiz / 'manaburn/episodios/ep99_teste'
        pasta.mkdir(parents=True)
        (pasta / 'ficha.md').write_text('# Ficha MB-EP99\n## Roteiro definitivo\nx\n## Controlo de qualidade\nok\n'
                                        '## Ficheiros finais\nvídeo com o fundador\n', encoding='utf-8')
        for f in ('legenda.txt', 'comentario_fixado.txt', 'fontes.md') + (('texto_alternativo.txt',) if completo else ()):
            (pasta / f).write_text('x', encoding='utf-8')
        with (raiz / 'comum/historico.md').open('a', encoding='utf-8') as h:
            h.write('\n- 01/11/2026 · MB-EP99 · teste · CONCLUÍDO\n')
        return {'ID': 'MB-EP99', 'Estado': 'CONCLUÍDO', 'Ficha': 'manaburn/episodios/ep99_teste/ficha.md'}

    def test_pacote_completo(self):
        with tempfile.TemporaryDirectory() as d:
            raiz = Path(d)
            repo_minimo(raiz)
            self.assertEqual(m.verificar_encerramento(raiz, self._episodio(raiz)), [])

    def test_pacote_incompleto_nao_arquiva(self):
        with tempfile.TemporaryDirectory() as d:
            raiz = Path(d)
            repo_minimo(raiz)
            faltas = m.verificar_encerramento(raiz, self._episodio(raiz, completo=False))
            self.assertIn('texto alternativo', faltas)

    def test_estado_em_producao_nao_arquiva(self):
        with tempfile.TemporaryDirectory() as d:
            raiz = Path(d)
            repo_minimo(raiz)
            e = self._episodio(raiz)
            e['Estado'] = 'EM PRODUÇÃO'
            self.assertTrue(any('estado no registo' in f for f in m.verificar_encerramento(raiz, e)))


class D_Insights(unittest.TestCase):
    def test_snapshot_novo_preserva_anteriores(self):
        with tempfile.TemporaryDirectory() as d:
            raiz = Path(d)
            repo_minimo(raiz)
            antes = {p.name: p.read_text(encoding='utf-8') for p in (raiz / 'comum/insights/semanas').glob('*.md')}
            novo = m.nova_semana(raiz, '2026-11-08')
            self.assertTrue(novo.exists())
            self.assertIn('2026-11-08', novo.read_text(encoding='utf-8'))
            for nome, txt in antes.items():
                self.assertEqual((raiz / 'comum/insights/semanas' / nome).read_text(encoding='utf-8'), txt)
            with self.assertRaises(FileExistsError):
                m.nova_semana(raiz, '2026-11-08')
            with self.assertRaises(FileExistsError):
                m.nova_semana(raiz, '2026-10-26')

    def test_linha_repetida_rejeitada(self):
        with tempfile.TemporaryDirectory() as d:
            raiz = Path(d)
            repo_minimo(raiz)
            p = raiz / 'comum/insights/registo_posts.csv'
            linhas = p.read_text(encoding='utf-8').splitlines()
            p.write_text('\n'.join(linhas + [linhas[-1]]) + '\n', encoding='utf-8')
            ids = {e['ID'] for e in m.ler_registo(raiz)[0]}
            self.assertTrue(any('repetida' in e for e in m.validar_insights(raiz, ids)))


class E_Impulsionamento(unittest.TestCase):
    def test_sem_confirmacao_fica_a_confirmar(self):
        with (RAIZ / 'comum/insights/registo_posts.csv').open(encoding='utf-8', newline='') as f:
            linhas = list(csv.DictReader(f))
        self.assertTrue(linhas)
        for r in linhas:
            if not r['notas'].lower().count('confirmado pelo fundador'):
                self.assertEqual(r['impulsionado'], 'A CONFIRMAR', r['post_ref'])

    def test_vazio_e_rejeitado(self):
        with tempfile.TemporaryDirectory() as d:
            raiz = Path(d)
            repo_minimo(raiz)
            p = raiz / 'comum/insights/registo_posts.csv'
            with p.open(encoding='utf-8', newline='') as f:
                linhas = list(csv.DictReader(f))
            linhas[0]['impulsionado'] = ''
            with p.open('w', encoding='utf-8', newline='') as f:
                w = csv.DictWriter(f, m.CSV_COLUNAS)
                w.writeheader()
                w.writerows(linhas)
            ids = {e['ID'] for e in m.ler_registo(raiz)[0]}
            self.assertTrue(any('A CONFIRMAR' in e for e in m.validar_insights(raiz, ids)))


class F_Seguranca(unittest.TestCase):
    def test_repositorio_sem_segredos(self):
        self.assertEqual(m.procurar_segredos(RAIZ), [])

    def test_detecta_token(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'x.md'
            p.write_text('token = "ghp_' + 'a1B2' * 9 + '"\n', encoding='utf-8')
            self.assertTrue(m.procurar_segredos(Path(d), [p]))


if __name__ == '__main__':
    unittest.main()
