"""MB-EP13: corre o process.py do kit sem o alterar, mas corta as faixas pelo tamanho do texto FALADO (campo tts).
Porquê: as legendas mostram os preços em algarismos («US$ 174,99») e a voz diz-os por extenso
(«cento e setenta e quatro dólares e noventa e nove»); com o tamanho da legenda o cortes.split desalinhava as falas 8–12 do Mana.
O resto (legendas, tempos, eventos, mistura) é o process.py original.
Uso, na pasta do kit:  python3 processar_vozes.py burn.mp3 mana.mp3
"""
import pathlib
src = pathlib.Path('process.py').read_text(encoding='utf-8')
alvo = "burn = split(load(sys.argv[1]), TEXT['B'])\nmana = split(load(sys.argv[2]), TEXT['M'])"
novo = """_TTS = {q: [(f.get('tts') or f['legenda']) for f in EPI['falas'] if f['quem'] == q] for q in 'BM'}
burn = split(load(sys.argv[1]), _TTS['B'])
mana = split(load(sys.argv[2]), _TTS['M'])"""
assert alvo in src, 'o process.py mudou: rever este script'
exec(compile(src.replace(alvo, novo), 'process.py (corte pelo tts)', 'exec'))
