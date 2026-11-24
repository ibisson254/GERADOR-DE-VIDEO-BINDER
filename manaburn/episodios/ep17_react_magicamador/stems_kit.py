"""MB-EP17: corre o process.py (corte pelo tts, como processar_vozes.py) e guarda as faixas separadas
(voz+sfx e música com ducking) para a montagem React pôr a música contínua por baixo do vídeo do parceiro."""
import pathlib
src = pathlib.Path('process.py').read_text(encoding='utf-8')
alvo = "burn = split(load(sys.argv[1]), TEXT['B'])\nmana = split(load(sys.argv[2]), TEXT['M'])"
novo = """_TTS = {q: [(f.get('tts') or f['legenda']) for f in EPI['falas'] if f['quem'] == q] for q in 'BM'}
burn = split(load(sys.argv[1]), _TTS['B'])
mana = split(load(sys.argv[2]), _TTS['M'])"""
alvo2 = "mix = m * g[:, None] + voice[:, None] + fxt"
novo2 = alvo2 + "\nnp.save('_stem_vf.npy', (voice[:, None] + fxt).astype(np.float32)); np.save('_stem_g.npy', g.astype(np.float32)); np.save('_stem_k.npy', np.array([np.max(np.abs(m * g[:, None] + voice[:, None] + fxt)) * 1.05]))"
assert alvo in src and alvo2 in src, 'o process.py mudou'
exec(compile(src.replace(alvo, novo).replace(alvo2, novo2), 'process.py (stems)', 'exec'))
