"""Passo 1 da prova: amplia o look 1 da prancha (4x, Lanczos) e recorta o fundo com o rembg
(modelo isnet-anime, local, sem custo). Saída: look1_recorte_4x.png na pasta atual."""
import os
from PIL import Image
from rembg import remove, new_session

AQUI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(AQUI, '..', '..', 'referencias', 'inspiracoes_2026-11-19', '01_reporter_do_multiverso.png')
im = Image.open(SRC).convert('RGB')
big = im.resize((im.width * 4, im.height * 4), Image.LANCZOS)
remove(big, session=new_session('isnet-anime'), post_process_mask=True).save('look1_recorte_4x.png')
print('ok')
