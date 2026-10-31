"""Gera comum/outro/outro_binder_916.mp4 a partir do fim de um Reel do Mana & Burn:
corta a partir do quadro escuro antes do scanner e tapa o rótulo "MANA & BURN" na fase da logo
com a cor do fundo do próprio quadro (fundo liso #050A10). Scanner, logo e textos ficam intactos.
uso: python3 -I fecho_neutro.py entrada.mp4 inicio_s pasta_trabalho saida.mp4
"""
import sys, glob, os, subprocess, numpy as np
from PIL import Image
src, ini, wd, out = sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4]
os.makedirs(f'{wd}/in', exist_ok=True); os.makedirs(f'{wd}/out', exist_ok=True)
subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',str(ini),'-i',src,'-an','-vf','fps=30',f'{wd}/in/%04d.png'],check=True)
Y0,Y1,X0,X1 = 548,650,380,700          # rótulo (y 564–607, x 396–683) + descida de 20 px na animação de entrada + margem
RING = 20
tapados = 0
for f in sorted(glob.glob(f'{wd}/in/*.png')):
    x = np.asarray(Image.open(f).convert('RGB')).copy()
    # fase da logo = sem o telemóvel do scanner: coluna à esquerda do telemóvel e zona do ecrã escuras
    scanner = x[300:1500, 260:820].astype(float).mean() > 30 and x[700:900, 184:188].astype(float).mean() > 38
    reg = x[Y0:Y1, X0:X1].astype(float)
    ring = np.concatenate([x[Y0-RING:Y0, X0:X1].reshape(-1,3), x[Y1:Y1+RING, X0:X1].reshape(-1,3),
                           x[Y0:Y1, X0-RING:X0].reshape(-1,3), x[Y0:Y1, X1:X1+RING].reshape(-1,3)]).astype(float)
    bg = np.median(ring, 0)
    tem_rotulo = (np.abs(reg - bg).sum(2) > 18).mean() > 0.003
    if not scanner and np.abs(ring - bg).max() < 12:   # só se o fundo à volta for liso
        x[Y0:Y1, X0:X1] = bg.round().astype(np.uint8); tapados += 1
    Image.fromarray(x).save(f.replace('/in/', '/out/'))
subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','30','-i',f'{wd}/out/%04d.png','-c:v','libx264','-preset','medium',
                '-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',out],check=True)
print(f'quadros: {len(glob.glob(wd+"/out/*.png"))} · rótulo tapado em {tapados}')
