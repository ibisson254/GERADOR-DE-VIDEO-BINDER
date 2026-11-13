"""Capa com espaço para a foto do artista.
python3 -I foto_slot.py <capa_base.png> <saida.png> [foto_do_artista.jpg]
Sem foto: deixa o espaço marcado. Com foto (enviada/autorizada): cola-a com a textura de pintura do kit."""
import sys, cv2, numpy as np, asyncio
sys.path.insert(0, '.')
from compor import colar, rasgo_alpha, fita, camada, aplicar
from kit import transferir_textura
base = cv2.imread(sys.argv[1]); W, H, CX, CY, ANG = 360, 450, 820, 690, 3
papel = cv2.resize(cv2.imread('kit_papel.png'), (W+40, H+40))
base = colar(base, papel, rasgo_alpha(W+40, H+40, 12, 21), CX, CY, ANG)
if len(sys.argv) > 3:
    f = cv2.imread(sys.argv[3]); fh, fw = f.shape[:2]; s = max(W/fw, H/fh)
    f = cv2.resize(f, (int(fw*s)+1, int(fh*s)+1), interpolation=cv2.INTER_LANCZOS4)
    oy = int((f.shape[0]-H)*0.25); ox = (f.shape[1]-W)//2; f = f[oy:oy+H, ox:ox+W]
    velha = cv2.resize(cv2.imread('modelo_capa.png')[520:880, 300:700], (W, H))
    f = transferir_textura(f, velha, None, 0.8)
else:
    f = np.full((H, W, 3), (70, 62, 58), np.uint8)
base = colar(base, f, rasgo_alpha(W, H, 7, 22), CX, CY, ANG)
base = fita(base, CX-W/2+20, CY-H/2-8, -35, 140); base = fita(base, CX+W/2-20, CY-H/2-8, 38, 140)
if len(sys.argv) <= 3:
    asyncio.run(camada(f'<div class="e bc" style="left:{CX}px;top:{CY-60}px;transform:translateX(-50%) rotate({ANG}deg);font-size:46px;color:#EDE3CC;text-align:center">FOTO DO<br>ARTISTA<br><span style="font-size:26px">(enviar autorizada)</span></div>', '_c.png'))
    asyncio.run(camada('', '_t.png')); base = aplicar(base, '_t.png', '_c.png')
cv2.imwrite(sys.argv[2], base)
