"""Lote 2: Q, Khan Vengeful Heart, Picard, Borg Queen, Deep Space 9 + Constelação. Reels Órbita 12 s."""
import sys
import build2, build4
from build3 import VIVID

CR = build2.CR
NEW = [
 dict(file="11-q", card="q_0383", seed=1111, tag="Moldura LCARS", title="O Q é quebrado?",
      sub="Q, Stacking the Deck | Star Trek, 2026 · nº 383",
      body="Cada carta da sua mão pode virar uma cópia da carta que ele exilou.",
      credit=f"Na imagem: Q, Stacking the Deck (Star Trek, 2026), nº 383. Arte: Viktor Fetsch. {CR}"),
 dict(file="12-khan-vengeful", card="khanvh_0416", seed=1212, tag="Moldura Classic Enterprise", title="Mana infinita",
      sub="Khan, Vengeful Heart | Star Trek, 2026 · nº 416",
      body="Com o Food Chain, de 1999, ele volta do exílio sem parar e gera mana infinita.",
      credit=f"Na imagem: Khan, Vengeful Heart (Star Trek, 2026), nº 416. Arte: Grant Griffin. {CR}"),
 dict(file="13-picard", card="picard_0497", seed=1313, tag="LCARS em surge foil", title="Vazou antes da hora",
      sub="Captain Jean-Luc Picard | Star Trek, 2026 · nº 497",
      body="Apareceu antes do anúncio por um descuido numa atualização do MTG Arena.",
      credit=f"Na imagem: Captain Jean-Luc Picard (Star Trek, 2026), nº 497. Arte: Erikas Perl. {CR}"),
 dict(file="14-borg-queen", card="borgqueen_0001", seed=1414, tag="Comandante", title="A resistência é inútil",
      sub="The Borg Queen | Star Trek Commander, 2026 · nº 1",
      body="Assimila a próxima criatura do grimório do adversário e a coloca do seu lado.",
      credit=f"Na imagem: The Borg Queen (Star Trek Commander, 2026), nº 1. Arte: Jodie Muir. {CR}"),
 dict(file="15-deep-space-9", card="ds9_0556", seed=1515, tag="Moldura Schematic", title="Deep Space 9",
      sub="Deep Space 9 | Star Trek, 2026 · nº 556",
      body="Em cada manutenção, exila 4 cartas e coloca em jogo todas as permanentes.",
      credit=f"Na imagem: Deep Space 9 (Star Trek, 2026), nº 556. Arte: Scott Okumura. {CR}"),
 dict(file="16-constelacao-5", card="q_0383", seed=1616, tag="Constelação", title="As 5 mais comentadas",
      sub="Star Trek × Magic | revelações de 20/10/2026",
      body="Q, Khan, Picard, Borg Queen e Deep Space 9. Manda para quem joga Commander com você.",
      credit=("Na imagem: Q, Stacking the Deck (nº 383, Viktor Fetsch); Khan, Vengeful Heart (nº 416, Grant Griffin); "
              "Captain Jean-Luc Picard (nº 497, Erikas Perl); The Borg Queen (Star Trek Commander nº 1, Jodie Muir); "
              f"Deep Space 9 (nº 556, Scott Okumura). {CR}"),
      group=["q_0383", "khanvh_0416", "picard_0497", "borgqueen_0001", "ds9_0556"]),
]
PAL = {"11-q": ["pink", "red", "navy", "sky", "mustard"],
       "12-khan-vengeful": ["ochre", "vermilion", "navy", "sky", "red"],
       "13-picard": ["red", "mustard", "prussian", "sky", "pink"],
       "14-borg-queen": ["teal", "olive", "navy", "sage", "mustard"],
       "15-deep-space-9": ["sky", "teal", "navy", "mustard", "vermilion"],
       "16-constelacao-5": ["mustard", "blue", "red", "pink", "teal"]}

# Constelação: cinco cartas em arco, sem sobrepor rodapés
_orig_page = build2.page
def page(p):
    h = _orig_page(p)
    if "group" in p:
        xs = [80, 268, 452, 636, 824]; ys = [300, 232, 200, 232, 300]; rot = [-9, -4.5, 0, 4.5, 9]; order = [0, 4, 1, 3, 2]
        divs = "".join(
            f'<div class="card" style="left:{xs[i]}px;top:{ys[i]}px;width:176px;transform:rotate({rot[i]}deg);z-index:{2+k}">'
            f'<img src="file://{build2.ROOT}/cards/{p["group"][i]}.png"></div>' for k, i in enumerate(order))
        start = h.index('<div class="card">'); end = h.index("</div>", start) + 6
        h = h[:start] + divs + h[end:]
    return h
build2.page = page

for p in NEW:
    build2.POSTS.append(p)
VIVID.update(PAL)

if __name__ == "__main__":
    args = sys.argv[1:]
    prev = "--preview" in args
    names = [a for a in args if not a.startswith("--")] or [p["file"] for p in NEW]
    for n in names:
        build4.run(n, prev)
