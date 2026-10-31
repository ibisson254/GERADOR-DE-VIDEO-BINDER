"""Lote 3: Mr. Spock (autógrafo), Commander Spock, Worf."""
import sys
import build2, build4, batch2
from build3 import VIVID
CR = build2.CR
NEW = [
 dict(file="17-spock-autografo", card="spock_1702", seed=1717, tag="Carta de autógrafo", title="Mais um autógrafo",
      sub="Mr. Spock, Science Officer | Star Trek, 2026 · nº 1702",
      body="A assinatura vai no painel prateado. É uma das 7 cartas de autógrafo do set.",
      credit=f"Na imagem: Mr. Spock, Science Officer (Star Trek, 2026), nº 1702. Arte: Gal Or. {CR}"),
 dict(file="18-commander-spock", card="cmdspock_0002", seed=1818, tag="Comandante", title="Fascinante",
      sub="Commander Spock | Star Trek Commander, 2026 · nº 2",
      body="Ao entrar ou atacar, pode conjurar a carta do topo de graça, baixar um terreno ou comprar.",
      credit=f"Na imagem: Commander Spock (Star Trek Commander, 2026), nº 2. Arte: Sam Kennedy. {CR}"),
 dict(file="19-worf", card="worf_0004", seed=1919, tag="Comandante", title="Um bom dia para lutar",
      sub="Worf, Defiant Commander | Star Trek Commander, 2026 · nº 4",
      body="Entra com um guerreiro Klingon 2/1 e, a cada ataque, libera cartas extras para jogar.",
      credit=f"Na imagem: Worf, Defiant Commander (Star Trek Commander, 2026), nº 4. Arte: Flavio Greco Paglia. {CR}"),
]
VIVID.update({"17-spock-autografo": ["blue", "mustard", "navy", "sky", "vermilion"],
              "18-commander-spock": ["sage", "pink", "blue", "sky", "mustard"],
              "19-worf": ["red", "ochre", "navy", "pink", "mustard"]})
build2.POSTS.extend(NEW)
if __name__ == "__main__":
    a = sys.argv[1:]; prev = "--preview" in a
    for n in [x for x in a if not x.startswith("--")] or [p["file"] for p in NEW]:
        build4.run(n, prev)
