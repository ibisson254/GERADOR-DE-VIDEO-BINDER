#!/usr/bin/env python3
"""Testes de comum/ferramentas/inteligencia.py (só biblioteca padrão + PyYAML)."""
import copy
import datetime as dt
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import inteligencia as i  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
HOJE = dt.date(2026, 11, 28)


def op_base():
    ops = dict((p.stem, o) for p, o in i.ler_oportunidades(RAIZ))
    return copy.deepcopy(ops['OP-2026-W48-01'])


class A_Repositorio(unittest.TestCase):
    def test_fichas_do_repo_validas(self):
        for p, op in i.ler_oportunidades(RAIZ):
            self.assertEqual(i.validar_oportunidade(op, p.name), [], p.name)
            self.assertEqual(p.stem, op['id'])

    def test_cli_validar(self):
        self.assertEqual(i.main(['validar']), 0)


class B_Validacao(unittest.TestCase):
    def test_nota_sem_porque(self):
        op = op_base()
        op['criterios']['fontes']['porque'] = ''
        self.assertTrue(any('sem «porque»' in e for e in i.validar_oportunidade(op)))

    def test_nota_fora_de_escala(self):
        op = op_base()
        op['criterios']['originalidade']['nota'] = 7
        self.assertTrue(any('1–5' in e for e in i.validar_oportunidade(op)))

    def test_criterio_em_falta(self):
        op = op_base()
        del op['criterios']['longevidade']
        self.assertTrue(any('longevidade' in e for e in i.validar_oportunidade(op)))

    def test_evidencia_sem_url(self):
        op = op_base()
        op['evidencias'][0]['url'] = ''
        self.assertTrue(any('sem «url»' in e for e in i.validar_oportunidade(op)))

    def test_ausencia_nao_pede_url(self):
        op = op_base()
        op['evidencias'] = [{'tipo': 'ausência', 'evidencia': 'nada encontrado'}]
        self.assertEqual(i.validar_oportunidade(op), [])


class C_Portoes(unittest.TestCase):
    def test_identidade_baixa_fica_fora_mesmo_com_soma_alta(self):
        op = op_base()
        for k, _ in i.CRITERIOS:
            op['criterios'][k]['nota'] = 5
        op['criterios']['identidade_binder']['nota'] = 2
        self.assertEqual(i.portoes(op, HOJE)[0], 'FORA')

    def test_fontes_fracas_mandam_esperar(self):
        op = op_base()
        op['criterios']['fontes']['nota'] = 2
        self.assertEqual(i.portoes(op, HOJE)[0], 'ESPERAR')

    def test_janela_vencida(self):
        op = op_base()
        op['janela']['ate'] = dt.date(2026, 11, 1)
        v, motivos = i.portoes(op, HOJE)
        self.assertEqual(v, 'FORA')
        self.assertTrue(any('vencida' in m for m in motivos))

    def test_saturado(self):
        op = op_base()
        op['categoria'] = 'D'
        self.assertEqual(i.portoes(op, HOJE)[0], 'FORA')

    def test_tabela_poe_esperar_depois_de_avaliar(self):
        a, b = op_base(), op_base()
        b['id'] = 'OP-2026-W48-99'
        b['criterios']['fontes']['nota'] = 1
        for k in ('relevancia_cultural', 'potencial_visual'):
            b['criterios'][k]['nota'] = 5
        t = i.tabela_oportunidades([(None, b), (None, a)], HOJE)
        self.assertLess(t.index('OP-2026-W48-01'), t.index('OP-2026-W48-99'))


def linha(id_, sem, abertura, tempo, dur='45'):
    return {'id_editorial': id_, 'semana_fim': sem, 'tipo_abertura': abertura, 'tempo_medio_s': tempo,
            'duracao_s': dur, 'frente': 'Mana & Burn', 'formato': 'Reel 9:16', 'tipo_narrativa': ''}


class D_Padroes(unittest.TestCase):
    def test_amostra_insuficiente(self):
        r = i.ler_padroes([linha('MB-EP13', '2026-11-21', 'objeto', '31')], 'tipo_abertura', 'tempo_medio_s')
        self.assertIn('Amostra insuficiente', r)
        self.assertNotIn('Hipótese', r)

    def test_hipotese_com_amostra_minima_e_sem_causa(self):
        ls = [linha(f'MB-EP{n}', '2026-11-21', 'objeto', str(30 + n)) for n in range(1, 4)]
        ls += [linha(f'MB-EP{n}', '2026-11-21', 'personagem', str(10 + n)) for n in range(4, 7)]
        r = i.ler_padroes(ls, 'tipo_abertura', 'tempo_medio_s')
        self.assertIn('Hipótese (não comprovada)', r)
        self.assertIn('não é causa', r)

    def test_usa_so_o_snapshot_mais_recente(self):
        ls = [linha('MB-EP13', '2026-11-14', 'objeto', '10'), linha('MB-EP13', '2026-11-21', 'objeto', '31')]
        r = i.ler_padroes(ls, 'tipo_abertura', 'tempo_medio_s')
        self.assertIn('n=1 · mediana 31', r)

    def test_vazio_nao_e_zero(self):
        r = i.ler_padroes([linha('MB-EP13', '2026-11-21', 'objeto', '')], 'tipo_abertura', 'tempo_medio_s')
        self.assertIn('nunca zero', r)
        self.assertNotIn('mediana 0', r)

    def test_percentagem_calculada_identificada(self):
        r = i.ler_padroes([linha('MB-EP13', '2026-11-21', 'objeto', '31.5')], 'tipo_abertura',
                          'pct_assistida_calc')
        self.assertIn('calculada', r)
        self.assertIn('mediana 70', r)

    def test_registo_real_nao_falha(self):
        self.assertEqual(i.main(['padroes', '--por', 'tipo_abertura', '--metrica', 'tempo_medio_s']), 0)


if __name__ == '__main__':
    unittest.main()
