"""v2: 10 posts de uma imagem, fundo pintado (paint.js). 1080×1350 JPG."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
from build import FONTS

ROOT = Path(__file__).parent
OUT = ROOT / "out2"; OUT.mkdir(exist_ok=True)
HT = ROOT / "html2"; HT.mkdir(exist_ok=True)
CR = "© Wizards of the Coast. Star Trek © CBS."

P = dict(mustard="#E2A72E", red="#C9412B", vermilion="#E05A2E", blue="#2F5E8C", prussian="#22436A", teal="#3C7F86",
         sage="#8EA48A", pink="#E3A6A0", navy="#1E2A42", sky="#8FC0CC", olive="#9AA33A", ochre="#C98A2B")
pal = lambda *k: [P[x] for x in k]

POSTS = [
 dict(file="01-kirk-autografo", card="kirk_1701", seed=101, pal=pal("red","mustard","navy","sky","blue"),
      tag="Carta de autógrafo", title="Assinada à mão", sub="Captain James T. Kirk | Star Trek, 2026 · nº 1701",
      body="William Shatner assina no painel prateado. São 7 cartas autografadas, cerca de 250 cópias de cada.",
      credit=f"Na imagem: Captain James T. Kirk (Star Trek, 2026), nº 1701. Arte: Chris Rallis. {CR}"),
 dict(file="02-khan", card="khan_0011", seed=202, pal=pal("prussian","red","navy","sky","mustard"),
      tag="Stardates", title="O Khan é um Sheoldred", sub="Khan, Engineered Evil | Star Trek Stardates, 2026 · nº 11",
      body="É o Sheoldred, the Apocalypse, com as mesmas habilidades e a arte do Khan da linha Kelvin.",
      credit=f"Na imagem: Khan, Engineered Evil (Star Trek Stardates, 2026), nº 11. Arte: Nicky Barkla. {CR}"),
 dict(file="03-crusher-lcars", card="crusher_0366", seed=303, pal=pal("mustard","teal","navy","pink","vermilion"),
      tag="Moldura LCARS", title="Tela da Frota", sub="Dr. Beverly Crusher | Star Trek, 2026 · nº 366",
      body="A moldura LCARS imita a interface dos computadores da Frota Estelar em The Next Generation.",
      credit=f"Na imagem: Dr. Beverly Crusher (Star Trek, 2026), nº 366. Arte: Anna Czeszejko. {CR}"),
 dict(file="04-enterprise-d", card="enterprise_0273", seed=404, pal=pal("vermilion","prussian","navy","mustard","sky"),
      tag="Nave · Spacecraft", title="NCC-1701-D", sub="U.S.S. Enterprise-D, Galaxy-Class | Star Trek, 2026 · nº 273",
      body="Cada turno em que a nave recebe marcadores vale uma carta a mais para jogar.",
      credit=f"Na imagem: U.S.S. Enterprise-D, Galaxy-Class (Star Trek, 2026), nº 273. Arte: Pablo Mendoza. {CR}"),
 dict(file="05-kirk-classic", card="kirk_0418", seed=505, pal=pal("blue","mustard","red","sage","prussian"),
      tag="Moldura Classic Enterprise", title="Cartaz de cinema", sub="Captain James T. Kirk | Star Trek, 2026 · nº 418",
      body="A moldura Classic Enterprise imita os cartazes pintados dos filmes antigos de Star Trek.",
      credit=f"Na imagem: Captain James T. Kirk (Star Trek, 2026), nº 418. Arte: Josh Newton. {CR}"),
 dict(file="06-crystalline-entity", card="crystalline_0478", seed=606, pal=pal("sky","prussian","teal","mustard","red"),
      tag="Arte estendida", title="Não sobra ninguém", sub="Crystalline Entity | Star Trek, 2026 · nº 478",
      body="Quando é conjurada, destrói todas as criaturas que não são artefatos. Ela, que é artefato, fica.",
      credit=f"Na imagem: Crystalline Entity (Star Trek, 2026), nº 478. Arte: David Alvarez. {CR}"),
 dict(file="07-crusher-comandante", card="crusher_0013", seed=707, pal=pal("sky","mustard","prussian","pink","red"),
      tag="Moldura normal", title="A comandante", sub="Dr. Beverly Crusher | Star Trek, 2026 · nº 13",
      body="Cresce a cada ganho de vida, e o EDHREC a pôs acima das outras comandantes do tema.",
      credit=f"Na imagem: Dr. Beverly Crusher (Star Trek, 2026), nº 13. Arte: Mattia Rangoni. {CR}"),
 dict(file="08-kirk-surge-foil", card="kirk_0542", seed=808, pal=pal("pink","olive","red","sky","navy"),
      tag="Surge foil", title="A mesma, em foil", sub="Captain James T. Kirk | Star Trek, 2026 · nº 542",
      body="A arte da Classic Enterprise em surge foil, que só sai nos Collector Boosters.",
      credit=f"Na imagem: Captain James T. Kirk (Star Trek, 2026), nº 542. Arte: Josh Newton. {CR}"),
 dict(file="09-crusher-surge-foil", card="crusher_0500", seed=909, pal=pal("ochre","teal","navy","pink","olive"),
      tag="LCARS em surge foil", title="LCARS brilhante", sub="Dr. Beverly Crusher | Star Trek, 2026 · nº 500",
      body="A versão LCARS da Crusher em surge foil só sai nos Collector Boosters.",
      credit=f"Na imagem: Dr. Beverly Crusher (Star Trek, 2026), nº 500. Arte: Anna Czeszejko. {CR}"),
 dict(file="10-kirk-normal", card="kirk_0142", seed=1010, pal=pal("vermilion","ochre","navy","sage","red"),
      tag="Moldura normal", title="O Kirk de todo dia", sub="Captain James T. Kirk | Star Trek, 2026 · nº 142",
      body="Ao entrar ou atacar: troca uma carta da mão, cria um oficial ou dá +1/+0 ao time.",
      credit=f"Na imagem: Captain James T. Kirk (Star Trek, 2026), nº 142. Arte: Jason Pastrana. {CR}"),
]

CSS = FONTS + """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden;background:#EFE4CB}
canvas{position:absolute;left:0;top:0;width:1080px;height:1350px}
.card{position:absolute;left:325px;top:160px;width:430px;
 filter:drop-shadow(0 1px 1px rgba(20,12,4,.55)) drop-shadow(0 10px 12px rgba(45,28,10,.42)) drop-shadow(0 34px 44px rgba(45,28,10,.32))}
.card img{width:100%;display:block}
.txt{position:absolute;left:60px;right:60px;top:906px;color:#1B1A17}
.tag{display:inline-flex;align-items:center;gap:12px;font:600 21px Jost;letter-spacing:.22em;text-transform:uppercase;margin-bottom:12px}
.tag b{display:inline-block;background:#1B1A17;color:#F6EEDC;padding:7px 12px;font-weight:600}
.title{font:700 62px/1.02 Jost;letter-spacing:.035em;text-transform:uppercase}
.sub{font:italic 500 34px/1.15 Corm;margin-top:6px}
.body{font:500 35px/1.28 Jost;margin-top:12px}
.credit{position:absolute;left:62px;bottom:44px;font:500 19px/1.35 Geist;color:#3b382f;max-width:680px}
.binder{position:absolute;right:58px;bottom:42px;background:#050A10;color:#fff;font:700 26px Geist;padding:13px 22px 13px 18px;border-radius:999px;
 display:flex;align-items:center;gap:12px;box-shadow:0 8px 18px rgba(30,18,6,.35)}
.binder i{width:14px;height:14px;border-radius:50%;background:#10B981;display:block}
"""


def page(p):
    js = (ROOT / "paint.js").read_text()
    return f"""<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>
<canvas id="c"></canvas>
<div class="card"><img src="file://{ROOT}/cards/{p['card']}.png"></div>
<div class="txt"><div class="tag"><b>Star Trek × Magic</b>{p['tag']}</div><div class="title">{p['title']}</div>
<div class="sub">{p['sub']}</div><div class="body">{p['body']}</div></div>
<div class="credit">{p['credit']}</div><div class="binder"><i></i>BINDER Vision</div>
<script>{js}
paint(document.getElementById('c'),{p['seed']},{p['pal']},{{cx:540,cy:458,px:48,py:48,pw:984,ph:820}});const bd=document.querySelector('.body');document.title=bd.offsetHeight>95?'done-OVER':'done';</script></body></html>"""


def render(posts):
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
        for p in posts:
            h = HT / f"{p['file']}.html"; h.write_text(page(p), encoding="utf-8")
            pg.goto(f"file://{h}"); pg.wait_for_function("document.title.startsWith('done')"); pg.wait_for_timeout(300)
            png = HT / f"{p['file']}.png"; pg.screenshot(path=str(png))
            Image.open(png).convert("RGB").resize((1080, 1350), Image.LANCZOS).save(OUT / f"{p['file']}.jpg", quality=95)
            print("ok", p["file"], pg.title())
        b.close()


if __name__ == "__main__":
    only = sys.argv[1:]
    render([p for p in POSTS if not only or any(p["file"].startswith(o) for o in only)])
