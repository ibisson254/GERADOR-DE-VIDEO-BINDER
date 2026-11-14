"""Capa v4 do carrossel "300 cartas. Zero digitação." (1080x1350), na paleta escura da marca.
Gancho: pilha de cartas reais (Scryfall) -> celular com a tela real do scanner (scan.png, 24/10/2026).
Uso: python3 build_capa_v4.py <pasta_assets> <saida.png> (assets: PNG das 5 cartas do Scryfall + scan.png + Geist Medium/Bold/Black woff2)"""
import sys, pathlib, asyncio
from playwright.async_api import async_playwright

A = pathlib.Path(sys.argv[1]).resolve(); OUT = pathlib.Path(sys.argv[2]).resolve()

def card(n, x, y, w, r, z):
    return f'<img class=card src="{n}.png" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({r}deg);z-index:{z}">'

PILE = "".join([
    card("cyclonic_rift",    40, 590, 300, -16, 1),
    card("smothering_tithe", 92, 630, 300, -6, 2),
    card("rhystic_study",    30, 720, 300, -11, 3),
    card("the_one_ring",    130, 750, 300,   4, 4),
    card("sol_ring",         70, 820, 300,  -3, 5),
])

HTML = f"""<html><head><meta charset="utf-8"><style>
@font-face{{font-family:G;src:url(Geist-Medium.woff2);font-weight:500}}
@font-face{{font-family:G;src:url(Geist-Bold.woff2);font-weight:700}}
@font-face{{font-family:G;src:url(Geist-Black.woff2);font-weight:900}}
*{{margin:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;background:#050A10;font-family:G,sans-serif;color:#F4F5F2;overflow:hidden;position:relative}}
.glow{{position:absolute;left:420px;top:480px;width:760px;height:900px;background:radial-gradient(closest-side,rgba(16,185,129,.20),rgba(16,185,129,0));}}
.top{{position:absolute;top:58px;left:72px;right:72px;display:flex;justify-content:space-between;font-size:24px;font-weight:700;letter-spacing:.06em}}
.top .r{{color:#6B7686;font-weight:500}}
.dot{{display:inline-block;width:14px;height:14px;border-radius:50%;background:#10B981;margin-right:12px;vertical-align:1px}}
h1{{position:absolute;left:68px;top:140px;font-size:136px;line-height:.93;font-weight:900;letter-spacing:-.055em}}
h1 .e{{color:#10B981}}
.card{{position:absolute;border-radius:4.75%/3.5%;box-shadow:0 26px 48px rgba(0,0,0,.6)}}
.phone{{position:absolute;left:560px;top:420px;width:410px;border-radius:52px;border:12px solid #0B0F14;outline:2px solid #2A323D;
  overflow:hidden;transform:rotate(5deg);z-index:10;box-shadow:0 40px 90px rgba(0,0,0,.7),0 0 0 1px rgba(16,185,129,.15)}}
.phone img{{display:block;width:100%}}
.arrow{{position:absolute;left:400px;top:620px;z-index:11;width:190px}}
.chip{{position:absolute;left:72px;top:432px;font-size:34px;line-height:1.3;color:#A7B0BC;font-weight:500}}
.chip b{{color:#F4F5F2;font-weight:700}}
.swipe{{position:absolute;right:72px;bottom:70px;font-size:28px;font-weight:700;color:#10B981;z-index:12}}
.foot{{position:absolute;left:72px;bottom:24px;right:300px;font-size:15px;line-height:1.35;color:#4E5866;z-index:12}}
</style></head><body>
<div class=glow></div>
<div class=top><span><span class=dot></span>BINDER Vision</span><span class=r>beta · Android</span></div>
<h1>300 cartas.<br><span class=e>Zero digitação.</span></h1>
<p class=chip>Aponte a câmera.<br><b>O app reconhece a carta.</b></p>
{PILE}
<svg class=arrow viewBox="0 0 190 120"><path d="M8 100 C 60 20, 120 10, 170 40" fill="none" stroke="#10B981" stroke-width="7" stroke-linecap="round" stroke-dasharray="2 16"/><path d="M150 22 L176 44 L146 56" fill="none" stroke="#10B981" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>
<div class=phone><img src="scan.png"></div>
<div class=swipe>arraste →</div>
<div class=foot>Tela real do app. Cartas: Sol Ring, The One Ring, Rhystic Study, Smothering Tithe, Cyclonic Rift, Iron Man Armor. © Wizards of the Coast. Marvel ©.</div>
</body></html>"""

async def main():
    f = A / "_capa_v4.html"; f.write_text(HTML, encoding="utf-8")
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width":1080,"height":1350})
        await pg.goto(f.as_uri()); await pg.wait_for_timeout(500)
        await pg.screenshot(path=str(OUT)); await b.close()
asyncio.run(main())
