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
import csv, math, sys
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


def escolher(rows, chave):
    """A = mais listas. B = melhor indicador entre os sem alertas. Robustez = IC de B acima do valor de A."""
    a = max(rows, key=lambda r: r['listas'] or 0)
    cand = [r for r in rows if r is not a and r[chave] is not None and not r['alertas']]
    if a[chave] is None or not cand:
        return a, None, 'sem indicador comparável publicado para A ou sem candidato B sem alertas'
    b = max(cand, key=lambda r: r[chave])
    ic = b[chave + '_ic']
    if b[chave] <= a[chave]:
        veredito = 'o mais jogado também tem o melhor indicador entre os comparáveis'
    elif ic and ic[0] > a[chave]:
        veredito = 'B supera A e a diferença resiste ao intervalo de 95 % (cálculo do BINDER)'
    else:
        veredito = 'B tem valor maior, mas o intervalo de 95 % inclui o valor de A: diferença não distinguível da amostra'
    return a, b, veredito


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
        a, b, v = escolher(rows, chave)
        L += ['', f'## Comparação por {nome}', f'- A (mais listas): {a["comandante"]} · {pct(a[chave])}',
              f'- B: {b["comandante"] + " · " + pct(b[chave]) if b else "—"}', f'- Veredito: {v}']
    L += ['', 'Notas: win rate e Top 4 só existem se o portal os publicar; a conversão é top4/listas (cálculo do BINDER',
          'quando o portal só publica contagens). Nunca comparar win rate de um com conversão de outro.']
    return '\n'.join(L) + '\n'


def main():
    if '--teste' in sys.argv:
        import tempfile
        cab = 'comandante,listas,partidas,vitorias,derrotas,empates,top4,torneios,max_listas_num_torneio,periodo_inicio,periodo_fim,filtros,url,extraido_em,captura\n'
        lin = ['SINTETICO A,100,400,210,190,,30,20,15,x,y,z,,,', 'SINTETICO B,40,160,104,56,,18,12,8,x,y,z,,,',
               'SINTETICO C,6,20,15,5,,4,2,5,x,y,z,,,']
        f = Path(tempfile.mkdtemp()) / 't.csv'; f.write_text(cab + '\n'.join(lin) + '\n', encoding='utf-8')
        rows, per = ler(f); tot = indicadores(rows)
        a, b, v = escolher(rows, 'wr')
        assert a['comandante'] == 'SINTETICO A' and b['comandante'] == 'SINTETICO B', (a, b)
        assert 'amostra pequena (listas)' in rows[2]['alertas']
        print(relatorio(rows, per, tot)); print('TESTE OK (dados sintéticos, não publicar)'); return
    src = Path(sys.argv[1] if len(sys.argv) > 1 else 'extracao.csv')
    rows, per = ler(src); tot = indicadores(rows)
    (src.parent / 'resultado.md').write_text(relatorio(rows, per, tot), encoding='utf-8')
    print(f'resultado.md escrito ({len(rows)} comandantes)')


if __name__ == '__main__':
    main()
