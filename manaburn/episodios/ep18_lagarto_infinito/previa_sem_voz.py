"""MB-EP12 · prévia SEM VOZ (créditos do ElevenLabs não autorizados).
Corre o process.py do kit sem alterar nada nele, trocando só a origem das falas: em vez das faixas do ElevenLabs,
cada fala é um silêncio com a duração prevista pelo tamanho do texto (calibrada no MB-EP11: Burn 0,0403 s/caractere
+ 0,73 s; Mana 0,0466 s/caractere + 0,68 s, já com o ritmo do episódio). A boca mexe com um envelope sintético
só para se ver quem fala. Quando houver vozes: python3 process.py burn.mp3 mana.mp3 (os tempos passam a ser os reais).
Uso, na pasta do kit com o episode.json/episode.js do episódio:  python3 previa_sem_voz.py
"""
import re, json, pathlib, numpy as np
src = pathlib.Path('process.py').read_text(encoding='utf-8')
fake = '''
def _dur(who, txt):
    c = len(txt.replace('*', ''))
    return (0.0403 * c + 0.73) if who == 'B' else (0.0466 * c + 0.68)
burn = [np.zeros(int(_dur('B', t) * SR), np.float32) for t in TEXT['B']]
mana = [np.zeros(int(_dur('M', t) * SR), np.float32) for t in TEXT['M']]
'''
src = src.replace("burn = split(load(sys.argv[1]), TEXT['B'])\nmana = split(load(sys.argv[2]), TEXT['M'])", fake)
src = src.replace("RESP = EPI.get('respiro_max')", "RESP = None")
src = src.replace("TEMPO = EPI.get('tempo', {})", "TEMPO = {}")
assert 'def _dur' in src and 'RESP = None' in src and 'TEMPO = {}' in src
exec(compile(src, 'process.py (prévia sem voz)', 'exec'))
# envelope sintético da boca (12 valores/s, como o process.py), só para a prévia
d = json.loads(pathlib.Path('data.js').read_text()[11:-1]); rng = np.random.default_rng(12)
for l in d['lines']:
    k = max(2, int(l['dur'] * 12)); e = np.clip(0.55 + 0.45 * np.sin(np.arange(k) * 1.9) * rng.uniform(0.5, 1, k), 0, 1)
    e[-1] = 0.05; l['env'] = [round(float(v), 2) for v in e]
pathlib.Path('data.js').write_text('const DATA=' + json.dumps(d, ensure_ascii=False) + ';')
print('prévia sem voz: envelope sintético aplicado em', len(d['lines']), 'falas')
