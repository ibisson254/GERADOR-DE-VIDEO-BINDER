"""Lote 4: Jean-Luc Picard, Luminary + Constelação dos 4 comandantes."""
import sys
import build2, build4, batch2, batch3
from build3 import VIVID
CR = build2.CR
NEW = [
 dict(file="20-picard-luminary", card="picardlum_0003", seed=2020, tag="Comandante", title="Motor de cartas",
      sub="Jean-Luc Picard, Luminary | Star Trek Commander, 2026 · nº 3",
      body="Compra uma carta a cada histórico de custo 3+ e carrega as naves mais rápido.",
      credit=f"Na imagem: Jean-Luc Picard, Luminary (Star Trek Commander, 2026), nº 3. Arte: Jason Pastrana. {CR}"),
 dict(file="21-constelacao-comandantes", card="borgqueen_0001", seed=2121, tag="Constelação", title="Qual deck você leva?",
      sub="Os 4 decks prontos de Star Trek Commander · 13/11/2026",
      body="Borg Queen, Spock, Picard ou Worf. Responda nos comentários.",
      credit=("Na imagem: The Borg Queen (nº 1, Jodie Muir); Commander Spock (nº 2, Sam Kennedy); "
              "Jean-Luc Picard, Luminary (nº 3, Jason Pastrana); Worf, Defiant Commander (nº 4, Flavio Greco Paglia). "
              f"Star Trek Commander, 2026. {CR}"),
      group4=["borgqueen_0001", "cmdspock_0002", "picardlum_0003", "worf_0004"]),
]
VIVID.update({"20-picard-luminary": ["vermilion", "mustard", "navy", "sky", "red"],
              "21-constelacao-comandantes": ["teal", "red", "blue", "mustard", "pink"]})
_prev = build2.page
def page(p):
    if "group4" not in p:
        return _prev(p)
    h = batch2._orig_page(p)
    xs = [104, 328, 552, 776]; ys = [352, 296, 296, 352]; rot = [-7, -2.5, 2.5, 7]
    divs = "".join(f'<div class="card" style="left:{xs[i]}px;top:{ys[i]}px;width:200px;transform:rotate({rot[i]}deg);z-index:{2+i}">'
                   f'<img src="file://{build2.ROOT}/cards/{p["group4"][i]}.png"></div>' for i in range(4))
    s = h.index('<div class="card">'); e = h.index("</div>", s) + 6
    return h[:s] + divs + h[e:]
build2.page = page
build2.POSTS.extend(NEW)
if __name__ == "__main__":
    a = sys.argv[1:]; prev = "--preview" in a
    for n in [x for x in a if not x.startswith("--")] or [p["file"] for p in NEW]:
        build4.run(n, prev)
