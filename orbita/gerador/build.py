"""Gera os slides 'Bauhaus Cósmico' da série Star Trek × Magic (1080×1350, JPG)."""
import json, math, random, os, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = Path(__file__).parent
NM = ROOT / "node_modules"
OUT = ROOT / "out"; OUT.mkdir(exist_ok=True)

C = dict(paper="#EEE4CD", ink="#1B1A17", mustard="#E0A431", petrol="#2D5A6C", red="#C3452E",
         sage="#93A589", navy="#1F2C44", sky="#9DC4C8", cream="#F6EEDC", orange="#D9782D")

FONTS = f"""
@font-face{{font-family:Jost;font-weight:500;src:url(file://{NM}/@fontsource/jost/files/jost-latin-500-normal.woff2)}}
@font-face{{font-family:Jost;font-weight:600;src:url(file://{NM}/@fontsource/jost/files/jost-latin-600-normal.woff2)}}
@font-face{{font-family:Jost;font-weight:700;src:url(file://{NM}/@fontsource/jost/files/jost-latin-700-normal.woff2)}}
@font-face{{font-family:Corm;font-style:italic;font-weight:500;src:url(file://{NM}/@fontsource/cormorant-garamond/files/cormorant-garamond-latin-500-italic.woff2)}}
@font-face{{font-family:Corm;font-style:italic;font-weight:600;src:url(file://{NM}/@fontsource/cormorant-garamond/files/cormorant-garamond-latin-600-italic.woff2)}}
@font-face{{font-family:Geist;font-weight:500;src:url(file://{NM}/geist/dist/fonts/geist-sans/Geist-Medium.woff2)}}
@font-face{{font-family:Geist;font-weight:700;src:url(file://{NM}/geist/dist/fonts/geist-sans/Geist-Bold.woff2)}}
"""

CSS = FONTS + f"""
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px;overflow:hidden}}
body{{background:{C['paper']};position:relative;font-family:Jost;color:{C['ink']}}}
.abs{{position:absolute}}
.grain{{position:absolute;inset:0;pointer-events:none;mix-blend-mode:multiply;opacity:.55}}
.card{{position:absolute;filter:drop-shadow(0 12px 16px rgba(40,30,15,.38))}}
.card img{{width:100%;display:block}}
.kicker{{position:absolute;left:52px;top:46px;padding:8px;background:{C['paper']};font:600 22px Jost;letter-spacing:.28em;text-transform:uppercase}}
.stardate{{position:absolute;right:52px;top:36px;padding:2px 8px;background:{C['paper']};font:italic 500 32px Corm}}
.title{{position:absolute;left:60px;right:60px;font:700 68px/1.02 Jost;letter-spacing:.035em;text-transform:uppercase}}
.sub{{position:absolute;left:62px;right:60px;font:italic 500 38px/1.1 Corm}}
.body{{position:absolute;left:62px;right:60px;font:500 35px/1.3 Jost}}
.tag{{position:absolute;font:600 22px Jost;letter-spacing:.2em;text-transform:uppercase;padding:9px 16px;color:{C['cream']}}}
.credit{{position:absolute;left:62px;bottom:46px;font:500 19px/1.35 Geist;color:#3b382f;max-width:690px}}
.binder{{position:absolute;right:58px;bottom:44px;background:#050A10;color:#fff;font:700 26px Geist;
  padding:13px 22px 13px 18px;border-radius:999px;display:flex;align-items:center;gap:12px}}
.binder i{{width:14px;height:14px;border-radius:50%;background:#10B981;display:block}}
.swipe{{position:absolute;right:60px;font:italic 600 34px Corm}}
"""

GRAIN = """<svg class="grain" width="1080" height="1350"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="3" seed="%d"/>
<feColorMatrix values="0 0 0 0 .42  0 0 0 0 .36  0 0 0 0 .26  0 0 0 .55 0"/></filter>
<filter id="b"><feTurbulence type="fractalNoise" baseFrequency=".006" numOctaves="2" seed="%d"/>
<feColorMatrix values="0 0 0 0 .55  0 0 0 0 .42  0 0 0 0 .22  0 0 0 1.1 -.45"/></filter>
<rect width="1080" height="1350" filter="url(#b)" opacity=".5"/><rect width="1080" height="1350" filter="url(#n)"/></svg>"""


def shapes_svg(items):
    """items: lista de tuplas de formas geométricas."""
    s = ['<svg class="abs" style="left:0;top:0" width="1080" height="1350" viewBox="0 0 1080 1350">']
    for it in items:
        k = it[0]
        if k == "circle":
            _, x, y, r, col, *op = it
            s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{C.get(col,col)}" opacity="{op[0] if op else 1}"/>')
        elif k == "ring":
            _, x, y, r, col, w = it
            s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{C.get(col,col)}" stroke-width="{w}"/>')
        elif k == "half":  # meia-lua: semicírculo
            _, x, y, r, col, rot = it
            s.append(f'<path d="M{x-r},{y} A{r},{r} 0 0 1 {x+r},{y} Z" fill="{C[col]}" transform="rotate({rot} {x} {y})"/>')
        elif k == "rect":
            _, x, y, w, h, col, *op = it
            s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{C.get(col,col)}" opacity="{op[0] if op else 1}"/>')
        elif k == "line":
            _, x1, y1, x2, y2, w = it
            s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{C["ink"]}" stroke-width="{w}"/>')
        elif k == "stripes":  # hachuras finas verticais
            _, x, y, w, h, n = it
            for i in range(n):
                xx = x + i * w / n
                s.append(f'<line x1="{xx:.1f}" y1="{y}" x2="{xx:.1f}" y2="{y+h}" stroke="{C["ink"]}" stroke-width="1.6"/>')
        elif k == "dot":
            _, x, y, r, col = it
            s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{C[col]}"/>')
        elif k == "stem":  # haste com bolinha, como nas referências
            _, x, y1, y2, r, col = it
            s.append(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{C["ink"]}" stroke-width="2"/><circle cx="{x}" cy="{y1}" r="{r}" fill="{C[col]}"/>')
    s.append("</svg>")
    return "".join(s)


def card(name, x, y, w, rot=0):
    return f'<div class="card" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg)"><img src="file://{ROOT}/cards/{name}.png"></div>'


def page(slide):
    seed = slide.get("seed", 3)
    html = [f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>"]
    html.append(shapes_svg(slide["shapes"]))
    html.append(GRAIN % (seed, seed + 7))
    html.append(slide.get("extra_under", ""))
    for c in slide.get("cards", []):
        html.append(card(*c))
    html.append(f'<div class="kicker">Star Trek × Magic</div><div class="stardate">Stardate 2026 · {slide["n"]}</div>')
    html.append(slide.get("text", ""))
    if slide.get("credit"):
        html.append(f'<div class="credit">{slide["credit"]}</div>')
    if slide.get("binder", True):
        html.append('<div class="binder"><i></i>BINDER Vision</div>')
    html.append("</body></html>")
    return "".join(html)


def render(slides):
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
        for s in slides:
            h = ROOT / "html" / f"{s['file']}.html"; h.parent.mkdir(exist_ok=True)
            h.write_text(page(s), encoding="utf-8")
            pg.goto(f"file://{h}"); pg.wait_for_timeout(250)
            png = ROOT / "html" / f"{s['file']}.png"
            pg.screenshot(path=str(png))
            Image.open(png).convert("RGB").resize((1080, 1350), Image.LANCZOS).save(OUT / f"{s['file']}.jpg", quality=95)
            print("ok", s["file"])
        b.close()


if __name__ == "__main__":
    from slides import SLIDES
    only = sys.argv[1:]
    render([s for s in SLIDES if not only or any(s["file"].startswith(o) for o in only)])
