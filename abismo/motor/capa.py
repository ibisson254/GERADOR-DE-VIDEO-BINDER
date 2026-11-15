# ABISMO · capa de Reel (1080×1920; o essencial fica no recorte 3:4 da grelha, y 240–1680).
# Uso (raiz do repositório): python3 -I abismo/motor/capa.py abismo/publicacoes/<ID>
# Lê "capa" do post.json (linhas do gancho, sub) ou usa o gancho do Reel. Reaproveita fundo, carta e marca do motor.
import os, sys
sys.argv = [sys.argv[0], sys.argv[1], 'capa']
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import abismo as A
from PIL import ImageDraw

cfg = A.CFG; c = cfg['carta']; cap = cfg.get('capa', {})
linhas = cap.get('texto', cfg.get('gancho', [])); sub = cap.get('sub', '')
im = A.fundo(3.0, lotus=1.0)
d = ImageDraw.Draw(im, 'RGBA')
A.tracked(d, A.ID['etiqueta'], 300, 'bold', 24, A.EM + (235,), track=0.2)
A.logo_small(im, 270)
for j, ln in enumerate(linhas):
    A.text_center(d, ln, 410 + j * 108, 'black', 104, A.YEL if j == len(linhas) - 1 else A.WHITE, stroke=7)
cw = A.W * 0.56; ch = cw * 1040 / 745; x = (A.W - cw) / 2; y = 410 + len(linhas) * 108 + 10
A.glow(im, x, y, cw, ch, 0.75); A.paste_card(im, A.card(c, cw), x, y)
d = ImageDraw.Draw(im, 'RGBA')
if sub:
    f = A.fit(d, sub, 'black', 44, A.W - 220); tw = d.textlength(sub, font=f); yy = y + ch + 62
    d.rounded_rectangle(((A.W - tw) / 2 - 30, yy - 38, (A.W + tw) / 2 + 30, yy + 38), radius=38, fill=A.INK + (225,))
    d.text((A.W / 2, yy), sub, font=f, fill=A.WHITE, anchor='mm')
A.credit(im, c, A.H - 150)
out = f'{A.OUT}/{cfg["id"]}_capa.png'; im.convert('RGB').save(out); print(out)
