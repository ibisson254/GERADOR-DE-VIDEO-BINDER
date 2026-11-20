# ABISMO · capa de Reel (1080×1920; o essencial fica no recorte 3:4 da grelha, y 240–1680).
# Uso (raiz do repositório): python3 -I abismo/motor/capa.py abismo/publicacoes/<ID>
# Lê "capa" do post.json (linhas do gancho, sub) ou usa o gancho do Reel. Reaproveita fundo, carta e marca do motor.
import os, sys
sys.argv = [sys.argv[0], sys.argv[1], 'capa']
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import abismo as A
from PIL import ImageDraw

cfg = A.CFG; cap = cfg.get('capa', {})
if cfg.get('modo') == 'decks':   # AB-04: grelha 2×2 dos decks; carta real onde existe, espaço «?» onde ainda não há
    im = A.fundo(3.0, lotus=1.0); d = ImageDraw.Draw(im, 'RGBA')
    A.tracked(d, A.ID['etiqueta'], 300, 'bold', 24, A.EM + (235,), track=0.2); A.logo_small(im, 270)
    for j, ln in enumerate(cap['texto']): A.text_center(d, ln, 384 + j * 104, 'black', 100, A.YEL if j == len(cap['texto']) - 1 else A.WHITE, stroke=7)
    cw = 300; ch = cw * 1040 / 745; gx = 70; x0 = (A.W - 2 * cw - gx) / 2; y0 = 660; credito = None
    for i, dk in enumerate(cfg['decks']):
        x = x0 + (i % 2) * (cw + gx); y = y0 + (i // 2) * (ch + 96)
        if dk.get('embalagem'):   # v2: embalagem oficial à altura do espaço da carta
            c = A.embalagem(dk['embalagem'], ch); xe = x + (cw - c.width) / 2; A.glow(im, xe, y, c.width, ch, 0.4); A.sombra(im, c, xe, y); credito = 'emb'
        elif dk.get('carta'): A.glow(im, x, y, cw, ch, 0.6); A.paste_card(im, A.card(dk['carta'], cw), x, y); credito = dk['carta']
        else: A.paste_card(im, A.slot(dk, cw), x, y)
        d = ImageDraw.Draw(im, 'RGBA'); nome = f'{i + 1} · {dk["nome"].upper()}'
        d.text((x + cw / 2, y + ch + 34), nome, font=A.fit(d, nome, 'black', 30, cw + 60), fill=A.WHITE, anchor='mm', stroke_width=4, stroke_fill=A.INK)
    if cap.get('sub'):
        f = A.fit(d, cap['sub'], 'black', 38, A.W - 220); tw = d.textlength(cap['sub'], font=f); yy = 586
        d.rounded_rectangle(((A.W - tw) / 2 - 28, yy - 30, (A.W + tw) / 2 + 28, yy + 30), radius=30, fill=A.INK + (225,))
        d.text((A.W / 2, yy), cap['sub'], font=f, fill=A.WHITE, anchor='mm')
    if credito == 'emb':
        s_ = cap.get('credito', 'Embalagens oficiais · © Wizards of the Coast'); d = ImageDraw.Draw(im, 'RGBA')
        d.text((A.W / 2, A.H - 150), s_, font=A.fit(d, s_, 'med', 21, A.W - 160), fill=(225, 238, 240, 215), anchor='mm')
    elif credito: A.credit(im, credito, A.H - 150)
    out = f'{A.OUT}/{cfg["id"]}_capa.png'; im.convert('RGB').save(out); print(out); sys.exit(0)
c = cfg['carta']
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
