"""Conde Ep. 005 · capa do Reel (1080x1920), com o layout e os recursos do montador.
Arte original inteira (sem texto por cima), título no papel, abaixo da arte, dentro do recorte 4:5 da grelha.
Uso (pasta conde/): python3 capa_ep005.py [saida.jpg]
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import montar_ep005 as m
from PIL import ImageDraw

F_T1 = m.font("lora", 64, "Bold")
F_T2 = m.font("lorai", 46, "SemiBold Italic")

def capa():
    f = m.BG.copy()
    m.scene_art(f, "f")
    m.paste_center(f, m.INSETS["desconfiado"], *m.INSET_XY)
    d = ImageDraw.Draw(f)
    m.credit(d)
    d.text((m.W / 2, 1376), "O réu errou de mitologia.", font=F_T1, fill=m.BORDO, anchor="mm")
    d.text((m.W / 2, 1452), "lemur ≠ lemure", font=F_T2, fill=m.INK, anchor="mm")
    d.text((m.W // 2, 1530), "@binderthetrade", font=m.F_CRED, fill=m.GREY, anchor="mm")
    return f

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else f"{m.BASE}/saida/EP005_CONDE_LEMURE_capa.jpg"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    capa().convert("RGB").save(out, quality=92)
    print(out)
