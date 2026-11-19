"""MC-ESP03 · cálculos reproduzíveis sobre a extração do portal Duel Commander 500 (Farpas de Mana).

Entrada: dados/extracao.csv (preenchido a partir das capturas em ../capturas/, uma linha por comandante,
mesmo período e mesmos filtros). Saída: dados/resultado.md. Tudo o que este script calcula é «cálculo do
BINDER» na ficha; os números do portal entram tal como publicados.

Uso:
  python3 -I calcular.py extracao.csv            -> resultado.md
  python3 -I calcular.py --teste                 -> corre com dados SINTÉTICOS (nunca usar no episódio)

Colunas de extracao.csv (vazio = o portal não publica; nunca 0):
  comandante, listas, partidas, vitorias, derrotas, empates, top4, torneios, max_listas_num_torneio,
  periodo_inicio, periodo_fim, filtros, url, extraido_em, captura
"""
import csv, json, math, sys
from pathlib import Path

MIN_LISTAS = 20          # abaixo disto, «amostra pequena» no ecrã
MIN_PARTIDAS = 50
MAX_CONCENTRACAO = 0.5   # mais de metade das listas num só torneio = resultado concentrado


def num(x):
    x = (x or '').strip().replace(',', '.')
    return float(x) if x else None


def wilson(k, n, z=1.96):
    """Intervalo de Wilson a 95 % para uma proporção k/n (contagens completas e publicadas)."""
    if not n:
        return None
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def newcombe(k1, n1, k2, n2):
    """Intervalo a 95 % da diferença p2 − p1 entre duas proporções INDEPENDENTES (Newcombe 1998, método 10,
    híbrido de Wilson). Só vale se cada n for o denominador publicado e as observações forem independentes."""
    l1, u1 = wilson(k1, n1); l2, u2 = wilson(k2, n2); p1, p2 = k1 / n1, k2 / n2
    d = p2 - p1
    return d - math.sqrt((p2 - l2) ** 2 + (u1 - p1) ** 2), d + math.sqrt((u2 - p2) ** 2 + (p1 - l1) ** 2)


def ler(caminho):
    rows = list(csv.DictReader(open(caminho, encoding='utf-8')))
    periodos = {(r['periodo_inicio'], r['periodo_fim'], r['filtros']) for r in rows}
    if len(periodos) != 1:
        sys.exit(f'ERRO: período/filtros diferentes entre linhas ({len(periodos)}). A comparação não é válida.')
    out = []
    for r in rows:
        d = {k: num(r.get(k)) for k in ('listas', 'partidas', 'vitorias', 'derrotas', 'empates', 'top4', 'torneios', 'max_listas_num_torneio')}
        d['comandante'] = r['comandante'].strip()
        d['url'] = r.get('url', '')
        out.append(d)
    return out, periodos.pop()


def indicadores(rows):
    total = sum(r['listas'] or 0 for r in rows)
    for r in rows:
        r['quota'] = (r['listas'] / total) if (total and r['listas'] is not None) else None
        r['wr'] = (r['vitorias'] / r['partidas']) if (r['vitorias'] is not None and r['partidas']) else None
        r['wr_ic'] = wilson(r['vitorias'], r['partidas']) if r['wr'] is not None else None
        r['conv'] = (r['top4'] / r['listas']) if (r['top4'] is not None and r['listas']) else None
        r['conv_ic'] = wilson(r['top4'], r['listas']) if r['conv'] is not None else None
        r['conc'] = (r['max_listas_num_torneio'] / r['listas']) if (r['max_listas_num_torneio'] is not None and r['listas']) else None
        alertas = []
        if (r['listas'] or 0) < MIN_LISTAS: alertas.append('amostra pequena (listas)')
        if r['partidas'] is not None and r['partidas'] < MIN_PARTIDAS: alertas.append('amostra pequena (partidas)')
        if r['conc'] is not None and r['conc'] > MAX_CONCENTRACAO: alertas.append('concentrado num torneio')
        if r['torneios'] is not None and r['torneios'] < 3: alertas.append('menos de 3 torneios')
        r['alertas'] = alertas
    return total


NUM = {'wr': ('vitorias', 'partidas'), 'conv': ('top4', 'listas')}


def escolher(rows, chave):
    """A = mais listas. B = melhor indicador entre os sem alertas (regra fixada na ficha antes dos dados).
    A diferença B − A é avaliada com o intervalo de Newcombe (não com os intervalos individuais, que não
    provam diferença). Devolve (A, B, código, texto, intervalo da diferença)."""
    a = max(rows, key=lambda r: r['listas'] or 0)
    cand = [r for r in rows if r is not a and r[chave] is not None and not r['alertas']]
    if a[chave] is None or not cand:
        return a, None, 'sem_dados', 'sem indicador comparável publicado para A ou sem candidato B sem alertas', None
    b = max(cand, key=lambda r: r[chave])
    kk, nn = NUM[chave]
    dif = newcombe(a[kk], a[nn], b[kk], b[nn])
    if b[chave] <= a[chave]:
        if dif[1] < 0:
            return a, b, 'A_melhor', 'o mais jogado lidera e a vantagem sobre o 2.º fica fora da margem de erro', dif
        return a, b, 'A_melhor_margem', 'o mais jogado lidera, mas a vantagem sobre o 2.º cabe na margem de erro', dif
    if dif[0] > 0:
        return a, b, 'B_fora_margem', 'B fica à frente mesmo com a margem de erro da diferença (Newcombe 95 %, cálculo do BINDER)', dif
    return a, b, 'dentro_margem', 'B tem valor maior, mas a margem de erro da diferença inclui zero: não distinguível com esta amostra', dif


def pct(x): return '—' if x is None else f'{100 * x:.1f}%'.replace('.', ',')


def relatorio(rows, periodo, total):
    L = ['# MC-ESP03 · resultado dos cálculos (gerado por calcular.py)', '',
         f'Período: {periodo[0]} a {periodo[1]} · filtros: {periodo[2]} · total de listas na extração: {int(total)}', '',
         '| Comandante | Listas | Quota | Partidas | Win rate (portal) | IC 95 % | Top 4 | Conversão Top 4 | IC 95 % | Concentração | Alertas |',
         '|---|---|---|---|---|---|---|---|---|---|---|']
    for r in sorted(rows, key=lambda r: -(r['listas'] or 0)):
        ic = lambda t: '—' if not t else f'{pct(t[0])}–{pct(t[1])}'
        L.append(f"| {r['comandante']} | {int(r['listas'] or 0)} | {pct(r['quota'])} | {'' if r['partidas'] is None else int(r['partidas'])} | "
                 f"{pct(r['wr'])} | {ic(r['wr_ic'])} | {'' if r['top4'] is None else int(r['top4'])} | {pct(r['conv'])} | {ic(r['conv_ic'])} | "
                 f"{pct(r['conc'])} | {'; '.join(r['alertas']) or '—'} |")
    for chave, nome in (('wr', 'win rate'), ('conv', 'conversão para Top 4')):
        a, b, cod, v, dif = escolher(rows, chave)
        L += ['', f'## Comparação por {nome}', f'- A (mais listas): {a["comandante"]} · {pct(a[chave])}',
              f'- B: {b["comandante"] + " · " + pct(b[chave]) if b else "—"}',
              f'- Diferença B − A: {"—" if not dif else pct(b[chave] - a[chave]) + " (95 %: " + pct(dif[0]) + " a " + pct(dif[1]) + ")"}',
              f'- Veredito ({cod}): {v}']
    L += ['', 'Pressupostos que NÃO são verificáveis só com os totais (dizer no ecrã/ficha se ficarem por confirmar):',
          '1. Independência: os jogos A×B contam no registo de A e no de B; jogos do mesmo piloto não são independentes.',
          '   O intervalo é aproximado; com partidas A×B conhecidas, retirá-las e recalcular.',
          '2. Unidade: win rate por partida (match) ≠ por jogo (game). Usar só a definição publicada pelo portal.',
          '3. Empates: ficam fora do numerador e dentro do denominador, salvo definição diferente do portal.',
          '4. Universo: a matriz cobre só os 20 comandantes com mais matchups; B tem de sair desse mesmo universo.',
          'Win rate e conversão Top 4 nunca na mesma escala nem trocados entre si.']
    return '\n'.join(L) + '\n'


def para_video(rows, periodo, chave='wr'):
    """Rascunho de episodio.json para o render. confirmado=False até o fundador aprovar a tese (Gate B)."""
    a, b, cod, v, dif = escolher(rows, chave)
    if not b: return None
    ind, den = ('WIN RATE', 'partidas') if chave == 'wr' else ('CONVERSÃO TOP 4', 'listas')
    kk, nn = NUM[chave]
    num = lambda x: f'{int(x):,}'.replace(',', '.')
    txt = {'B_fora_margem': ('À FRENTE MESMO COM A MARGEM', 'verde'), 'dentro_margem': ('DENTRO DA MARGEM DE ERRO', 'ambar'),
           'A_melhor': ('O MAIS JOGADO TAMBÉM VENCE MAIS', 'verde'), 'A_melhor_margem': ('LIDERA, MAS DENTRO DA MARGEM', 'ambar')}[cod]
    top = sorted(rows, key=lambda r: -(r['listas'] or 0))[:5]
    return dict(confirmado=False, cenario=cod, indicador=ind, denominador=den, per=f'{periodo[0]} a {periodo[1]}', filtros=periodo[2],
                A=a['comandante'], B=b['comandante'], nA=num(a['listas']), nB=num(b['listas']), qA=pct(a['quota']), qB=pct(b['quota']),
                iA=pct(a[chave]), iB=pct(b[chave]), iA_v=a[chave], iB_v=b[chave], dA=num(a[nn]), dB=num(b[nn]),
                dif=pct(b[chave] - a[chave]), dif_v=b[chave] - a[chave], dif_lo=dif[0], dif_hi=dif[1],
                veredito=txt[0], veredito_cor=txt[1], pop_top=[[r['comandante'], int(r['listas'])] for r in top],
                carta_A='', carta_B='', extraido='', pergunta='', capa_frase='', capa_foco='')


def main():
    if '--teste' in sys.argv:
        import tempfile
        cab = 'comandante,listas,partidas,vitorias,derrotas,empates,top4,torneios,max_listas_num_torneio,periodo_inicio,periodo_fim,filtros,url,extraido_em,captura\n'
        lin = ['SINTETICO A,100,400,210,190,,30,20,15,x,y,z,,,', 'SINTETICO B,40,160,104,56,,18,12,8,x,y,z,,,',
               'SINTETICO C,6,20,15,5,,4,2,5,x,y,z,,,']
        f = Path(tempfile.mkdtemp()) / 't.csv'; f.write_text(cab + '\n'.join(lin) + '\n', encoding='utf-8')
        rows, per = ler(f); tot = indicadores(rows)
        a, b, cod, v, dif = escolher(rows, 'wr')
        assert a['comandante'] == 'SINTETICO A' and b['comandante'] == 'SINTETICO B', (a, b)
        # referência: Newcombe (1998), exemplo 56/70 vs 48/80 → diferença 0,2000, IC 0,0524 a 0,3339
        lo, hi = newcombe(48, 80, 56, 70); assert abs(lo - 0.0524) < 5e-4 and abs(hi - 0.3339) < 5e-4, (lo, hi)
        assert 'amostra pequena (listas)' in rows[2]['alertas']
        assert para_video(rows, per)['cenario'] == 'B_fora_margem'
        print(relatorio(rows, per, tot)); print('TESTE OK (dados sintéticos, não publicar)'); return
    src = Path(sys.argv[1] if len(sys.argv) > 1 else 'extracao.csv')
    rows, per = ler(src); tot = indicadores(rows)
    (src.parent / 'resultado.md').write_text(relatorio(rows, per, tot), encoding='utf-8')
    ep = para_video(rows, per, 'wr' if any(r['wr'] is not None for r in rows) else 'conv')
    if ep: (src.parent / 'episodio_rascunho.json').write_text(json.dumps(ep, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'resultado.md escrito ({len(rows)} comandantes)')


if __name__ == '__main__':
    main()
