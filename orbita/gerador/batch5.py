"""Lote 5 (24/10/2026): Reel 22 Test of Courage (Star Trek) + Problema de colecionador Ep. 1 (Lifegift).

Antes de rodar, preencha CONFIG com o número e o artista que estão no rodapé de cada PNG
e coloque as cartas normalizadas em cards/ (976x1360, cantos arredondados), como nos outros lotes.
Uso: python3 batch5.py [22-test-of-courage] [pc01-lifegift] [--preview]
"""
import sys
import build2, build4, batch2, batch3, batch4  # noqa: F401  (cada lote estende o anterior)
from build3 import VIVID

CONFIG = {
    "toc_num": "",       # número do Test of Courage no rodapé (ex.: "123")
    "toc_artist": "",    # artista do Test of Courage no rodapé
    "life_artist": "",   # artista do Lifegift no rodapé (Betrayers of Kamigawa, nº 132)
}

CR = build2.CR                         # "© Wizards of the Coast. Star Trek © CBS."
CRW = "© Wizards of the Coast."        # cartas fora de Star Trek

NEW = [
 dict(file="22-test-of-courage", card=f"testofcourage_{CONFIG['toc_num'].zfill(4)}", seed=2222,
      tag="Uma mana verde", title="Custa 1 mana",
      sub=f"Test of Courage | Star Trek, 2026 · nº {CONFIG['toc_num']}",
      body="Para a MTG Rocks, está entre as melhores cartas do set, sobretudo no Modern.",
      credit=f"Na imagem: Test of Courage (Star Trek, 2026), nº {CONFIG['toc_num']}. Arte: {CONFIG['toc_artist']}. {CR}"),
 dict(file="pc01-lifegift", card="lifegift_0132", seed=2323, label="Problema de colecionador",
      tag="Era bulk", title="De bulk a US$ 23",
      sub="Lifegift | Betrayers of Kamigawa, 2005 · nº 132",
      body="Valia menos de 1 dólar. Em outubro, chegou a US$ 23,45, segundo a Wargamer.",
      credit=f"Na imagem: Lifegift (Betrayers of Kamigawa, 2005), nº 132. Arte: {CONFIG['life_artist']}. {CRW}"),
]
VIVID.update({"22-test-of-courage": ["sage", "vermilion", "prussian", "mustard", "sky"],
              "pc01-lifegift": ["olive", "ochre", "teal", "pink", "navy"]})

_prev = build2.page
def page(p):
    h = _prev(p)
    if p.get("label"):  # série fora de Star Trek: troca a etiqueta preta
        h = h.replace("<b>Star Trek × Magic</b>", f"<b>{p['label']}</b>")
    return h
build2.page = page
build2.POSTS.extend(NEW)


def _missing(name):
    need = {"22-test-of-courage": ["toc_num", "toc_artist"], "pc01-lifegift": ["life_artist"]}.get(name, [])
    return [k for k in need if not CONFIG[k].strip()]


if __name__ == "__main__":
    a = sys.argv[1:]; prev = "--preview" in a
    for n in [x for x in a if not x.startswith("--")] or [p["file"] for p in NEW]:
        falta = _missing(n)
        if falta:
            sys.exit(f"{n}: preencha {', '.join(falta)} em CONFIG (dados do rodapé do PNG) antes de renderizar.")
        build4.run(n, prev)
