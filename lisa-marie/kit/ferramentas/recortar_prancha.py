"""Recorta a prancha «10 inspirações» (19/11/2026) nos 10 looks individuais.
Uso: python3 -I lisa-marie/kit/ferramentas/recortar_prancha.py <prancha.png> <pasta_saida>
Coordenadas medidas na prancha de 1312x1199 px; outra resolução exige medir de novo.
"""
import sys
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
nomes = ["01_reporter_do_multiverso","02_otaku_casual","03_dj_de_vinil","04_exploradora_do_multiverso","05_artista_de_rua",
         "06_colecionadora_de_mundos","07_fashionista_do_multiverso","08_nerd_de_cultura_pop","09_investigadora_de_historias","10_vibe_90s"]
xs = [0, 262, 524, 787, 1049, 1312]
rows = [(112, 625), (630, 1160)]
for r,(y0,y1) in enumerate(rows):
    for c in range(5):
        n = nomes[r*5+c]
        im.crop((xs[c], y0, xs[c+1], y1)).save(f"{out}/{n}.png", optimize=True)
