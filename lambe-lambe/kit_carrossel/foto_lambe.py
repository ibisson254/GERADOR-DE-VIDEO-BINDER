"""Foto do artista impressa como cartaz de lambe-lambe na capa (foto enviada pelo fundador).
python3 -I foto_lambe.py <capa.png> <foto.jpg> <saida.png>"""
import sys, cv2, numpy as np
sys.path.insert(0, '.')
from compor import colar, rasgo_alpha, fita
base = cv2.imread(sys.argv[1]); orig = base.copy()
W, H, CX, CY, ANG = 390, 520, 812, 690, 2.5
# 1) recorte e cor de impressão
f = cv2.imread(sys.argv[2]); fh, fw = f.shape[:2]; s = max(W/fw, H/fh)
f = cv2.resize(f, (int(fw*s)+1, int(fh*s)+1), interpolation=cv2.INTER_CUBIC)
oy = int((f.shape[0]-H)*0.1); ox = (f.shape[1]-W)//2; f = f[oy:oy+H, ox:ox+W].astype(np.float32)
g = f.mean(2, keepdims=True); f = g + (f-g)*0.6
f = np.clip((f-120)*1.3+132, 0, 255)
# 2) retícula leve de gráfica
yy, xx = np.mgrid[0:H, 0:W]
dots = ((np.sin(xx*0.95)*np.sin(yy*0.95))+1)/2
lum = f.mean(2)/255
f = f * (0.9 + 0.1*(dots[..., None] < lum[..., None]+0.35))
# 3) impressa no papel creme: multiplicação + pincelada/rugas do cartaz original
papel = cv2.resize(cv2.imread('kit_papel.png'), (W, H)).astype(np.float32)
f = papel*(f/255.0)*1.1
rel = cv2.resize(orig[520:880, 260:700], (W, H)).astype(np.float32).mean(2)
hp = np.clip(rel-cv2.GaussianBlur(rel, (0, 0), 1.6), -16, 16)[..., None]
f = np.clip(f+hp*0.9, 0, 255)
# 4) desgaste: falhas de tinta nas bordas e manchas
rng = np.random.default_rng(7)
n = cv2.GaussianBlur(rng.random((H, W)).astype(np.float32), (0, 0), 7); n = (n-n.min())/(n.max()-n.min())
edge = np.minimum.reduce([xx, yy, W-1-xx, H-1-yy]).astype(np.float32)
falha = ((n > 0.62) & (edge < 45)) | (n > 0.9)
falha = cv2.GaussianBlur(falha.astype(np.float32), (0, 0), 1.5)[..., None]
f = (f*(1-falha*0.8)+papel*falha*0.8).astype(np.uint8)
# 5) colar com borda rasgada, sem moldura
base = colar(base, f, rasgo_alpha(W, H, 16, 31), CX, CY, ANG)
# 6) a faixa preta do nome volta a ficar por cima (cartaz colado depois)
hsv = cv2.cvtColor(orig, cv2.COLOR_BGR2HSV); dark = hsv[..., 2] < 80
m = np.zeros(orig.shape[:2], np.uint8)
for x in range(60, 1030):
    col = np.where(dark[905:1010, x])[0]
    if len(col): m[905+col[0]:1100, x] = 255
m = cv2.GaussianBlur(m, (0, 0), 1.2)[..., None]/255.0
base = (base*(1-m)+orig*m).astype(np.uint8)
# 7) uma fita torta no topo
base = fita(base, CX-110, CY-H/2+6, -24, 150)
cv2.imwrite(sys.argv[3], base)
