"""Roteiro do episódio (episode.json) nas versões 1 e 2, e o texto que vai para o ElevenLabs.

Versão 1 (Ep. 1 a 4): {"B": [...], "M": [...], "gap": [...], ...}
Versão 2: {"schema": 2, "falas": [{"quem": "B", "tags": "[shouting]", "legenda": "...", "tts": null}, ...], ...}
  - legenda: o que aparece na tela; *palavra*, **palavra** ou <hl>palavra</hl> ficam amarelas.
  - tts: opcional. Sem ele, o TTS lê a legenda limpa, passada pelo sanitizador fonético
    (foneticos.json) e com os números por extenso. Use tts para tags no meio da fala ([laughs]).
  - as falas alternam Burn e Mana, começando pelo Burn (o bate-volta do process.py).

uso: python3 roteiro.py episodios/ep5_knacksaw.json   → imprime as duas faixas para colar no ElevenLabs
"""
import json, re, sys, os

AQUI = os.path.dirname(os.path.abspath(__file__))
FON = {k: v for k, v in json.load(open(os.path.join(AQUI, 'foneticos.json'), encoding='utf-8')).items() if not k.startswith('_')}
PAUSA = ' [long pause] '


def marca(t):
    """Normaliza a marcação de destaque para *palavra* (o formato que o index.html pinta de amarelo)."""
    t = re.sub(r'<hl>(.*?)</hl>', r'*\1*', t)
    return re.sub(r'\*\*(.+?)\*\*', r'*\1*', t)


def limpa(t):
    return marca(t).replace('*', '')


def _num(m):
    from num2words import num2words
    s = m.group(0); pct = s.endswith('%'); n = s.rstrip('%').replace('.', '')
    if ',' in n:
        a, b = n.split(','); w = num2words(int(a), lang='pt_BR') + ' vírgula ' + num2words(int(b), lang='pt_BR')
    else:
        w = num2words(int(n), lang='pt_BR')
    return w + (' por cento' if pct else '')


def fonetico(t):
    """Sanitizador fonético: troca termos de Magic e gírias em inglês pela grafia que o TTS lê certo,
    escreve números por extenso e tira a marcação da legenda. As tags [shouting] etc. passam intactas."""
    t = limpa(t)
    for sim, moeda in (('US\\$', 'dólares'), ('R\\$', 'reais'), ('€', 'euros')):        # US$ 2,80 → 2 dólares e 80
        t = re.sub(sim + r'\s?(\d+),(\d{2})\b', lambda m: f'{m.group(1)} {moeda} e {m.group(2)}', t)
        t = re.sub(sim + r'\s?(\d+)', lambda m: f'{m.group(1)} {moeda}', t)
    partes = re.split(r'(\[[^\]]+\])', t)                      # não mexe dentro das tags
    out = []
    for p in partes:
        if p.startswith('['): out.append(p); continue
        for k in sorted(FON, key=len, reverse=True):
            p = re.sub(r'(?<![\wÀ-ÿ])' + re.escape(k) + r'(?![\wÀ-ÿ])', FON[k], p)
        p = re.sub(r'\d+(?:[.,]\d+)?%?', _num, p)
        out.append(p)
    return ''.join(out)


def carrega(path='episode.json'):
    """Devolve o episódio normalizado: sempre com B e M (legendas) e falas (com tts pronto)."""
    e = json.load(open(path, encoding='utf-8'))
    if e.get('schema', 1) >= 2:
        falas = e['falas']
        for k, f in enumerate(falas):
            if e.get('ordem_livre'): break             # Ep. 10 (11/11/2026): falas na ordem do roteiro, sem bate-volta obrigatório
            esperado = 'B' if k % 2 == 0 else 'M'
            if f['quem'] != esperado:
                raise SystemExit(f'fala {k + 1}: era a vez do {esperado} (as falas alternam Burn e Mana)')
        e['B'] = [marca(f['legenda']) for f in falas if f['quem'] == 'B']
        e['M'] = [marca(f['legenda']) for f in falas if f['quem'] == 'M']
    else:
        e['B'] = [marca(x) for x in e['B']]; e['M'] = [marca(x) for x in e['M']]
        falas = []
        for b, m in zip(e['B'], e['M']):
            falas += [dict(quem='B', legenda=b), dict(quem='M', legenda=m)]
        e['falas'] = falas
    for f in e['falas']:
        f['tts_final'] = ((f.get('tags') or '') + ' ' + fonetico(f.get('tts') or f['legenda'])).strip()
    if len(e['B']) != len(e['M']) and not e.get('ordem_livre'):
        raise SystemExit('o Burn e o Mana precisam do mesmo número de falas')
    if len(e.get('gap', [])) not in (0, len(e['falas'])):
        raise SystemExit(f'gap tem {len(e["gap"])} valores para {len(e["falas"])} falas')
    return e


def faixas(e):
    """Texto das duas faixas do ElevenLabs (uma por personagem), com [long pause] entre as falas."""
    return {q: PAUSA.join(f['tts_final'] for f in e['falas'] if f['quem'] == q) for q in 'BM'}


if __name__ == '__main__':
    e = carrega(sys.argv[1] if len(sys.argv) > 1 else 'episode.json')
    fx = faixas(e)
    print('BURN (Talis):\n' + fx['B'] + f'\n({len(fx["B"])} caracteres)\n')
    print('MANA (Erik):\n' + fx['M'] + f'\n({len(fx["M"])} caracteres)')
