"""Carrossel v3 "300 cartas. Zero digitação." · 6 slides 1080x1350.
Paleta: papel #F2EEE6, tinta #0A0F14, painel do app #0A0E19, esmeralda #0E9F6E/#10B981, ouro #E0A526.
Imagens: cartas inteiras do Scryfall (sem corte nem filtro, rodapé visível) e telas reais do app
(scan.png 24/10; khan_tile.png e patrimonio.png do Binder em 11/11, sem a linha Investido/Lucro).
Uso: python3 build_v3.py -> ../png_v3/"""
import pathlib, asyncio, json
from playwright.async_api import async_playwright

HERE = pathlib.Path(__file__).parent
OUT = HERE.parent / "png_v3"
CRED = json.load(open(HERE.parent / "cartas" / "creditos.json", encoding="utf-8"))

def cred(*slugs):
    parts = [f'{CRED[s]["name"]} ({CRED[s]["set"]}, {CRED[s]["year"]}), nº {CRED[s]["num"]}, arte de {CRED[s]["artist"]}' for s in slugs]
    return "Na imagem: " + "; ".join(parts) + ". © Wizards of the Coast."

LOGO = '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><path fill="#FBBC04" d="M22.018 13.298l-3.919 2.218-3.515-3.493 3.543-3.521 3.891 2.202a1.49 1.49 0 0 1 0 2.594z"/><path fill="#4285F4" d="M1.337.924a1.486 1.486 0 0 0-.112.568v21.017c0 .217.045.419.124.6l11.155-11.087L1.337.924z"/><path fill="#34A853" d="M13.544 10.989l3.258-3.238L3.45.195a1.466 1.466 0 0 0-.946-.179l11.04 10.973z"/><path fill="#EA4335" d="M13.544 13.056l-11 10.933c.298.036.612-.016.906-.183l13.324-7.54-3.23-3.21z"/></svg>'
def badge(k=1.0):
    return (f'<div style="display:inline-flex;align-items:center;gap:{22*k:.0f}px;background:#000;border:{max(2,3*k):.0f}px solid #A6A6A6;'
            f'border-radius:{22*k:.0f}px;padding:0 {38*k:.0f}px 0 {30*k:.0f}px;height:{130*k:.0f}px;color:#fff;text-align:left">{LOGO.format(s=int(70*k))}'
            f'<div><div style="font-size:{22*k:.0f}px;font-weight:500;letter-spacing:.06em">DISPONÍVEL NO</div>'
            f'<div style="font-size:{52*k:.0f}px;font-weight:500;line-height:1">Google Play</div></div></div>')

CSS = """
@font-face{font-family:G;src:url(Geist-Medium.woff2);font-weight:500}
@font-face{font-family:G;src:url(Geist-Bold.woff2);font-weight:700}
*{margin:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#F2EEE6;font-family:G,sans-serif;color:#0A0F14;overflow:hidden;position:relative}
body.ink{background:#0A0F14;color:#F2EEE6}
.top{position:absolute;top:56px;left:80px;right:80px;display:flex;justify-content:space-between;align-items:center;font-size:24px;font-weight:700;letter-spacing:.06em;z-index:5}
.top .n{color:#8A8478;font-weight:500}
.dot{display:inline-block;width:14px;height:14px;border-radius:50%;background:#10B981;margin-right:12px}
h1{font-size:112px;line-height:.96;font-weight:700;letter-spacing:-.05em}
h2{font-size:84px;line-height:.98;font-weight:700;letter-spacing:-.045em}
.e{color:#0E9F6E}.ink .e,.panel .e{color:#10B981}.o{color:#E0A526}
.hl{display:inline-block;margin-top:14px;line-height:1.02;background:#E0A526;color:#0A0F14;padding:0 16px;border-radius:12px;-webkit-box-decoration-break:clone}
.sub{font-size:36px;line-height:1.3;color:#4A4E55;font-weight:500}
.ink .sub,.panel .sub{color:#A9A59C}
.foot{position:absolute;bottom:40px;left:80px;right:80px;font-size:18px;line-height:1.4;color:#8A8478;z-index:5}
.card{position:absolute;border-radius:4.75%/3.5%;box-shadow:0 24px 50px rgba(10,15,20,.32)}
.panel{position:absolute;background:#0A0E19;color:#F2EEE6;border-radius:44px;overflow:hidden}
.shot{position:absolute;border-radius:34px;overflow:hidden;border:9px solid #000;box-shadow:0 30px 70px rgba(0,0,0,.5)}
.shot img,.tile img{display:block;width:100%}
.tile{position:absolute;border-radius:30px;overflow:hidden;background:#000;box-shadow:0 34px 80px rgba(10,15,20,.35)}
.tag{display:inline-block;font-size:24px;font-weight:700;letter-spacing:.12em;color:#0E9F6E;border:2px solid currentColor;border-radius:999px;padding:8px 22px;margin-bottom:30px}
.panel .tag{color:#10B981}
.opt{display:flex;align-items:center;gap:26px;padding:26px 0;border-top:2px solid #DDD7CB}
.opt .k{font-size:26px;font-weight:700;color:#F2EEE6;background:#0A0F14;border-radius:14px;padding:12px 18px;min-width:96px;text-align:center}
.opt .t{font-size:36px;font-weight:700;letter-spacing:-.02em}
.opt .d{font-size:26px;color:#6B6F76;margin-top:4px;font-weight:500}
.arrow{position:absolute;bottom:96px;right:80px;font-size:28px;font-weight:700;color:#0E9F6E;z-index:5}
"""

def page(n, body, cls="", total=6):
    return (f'<html><head><style>{CSS}</style></head><body class="{cls}">'
            f'<div class=top><span><span class=dot></span>BINDER Vision</span><span class=n>{n}/{total}</span></div>{body}</body></html>')

def card(slug, x, y, w, rot=0, z=1):
    return f'<img class=card src="{slug}.png" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);z-index:{z}">'

SLIDES = {}

# 01 · capa: três staples reconhecíveis + promessa
SLIDES["01_capa"] = page(1, f"""
{card("sol_ring", 70, 160, 320, -7)}{card("the_one_ring", 380, 132, 320, 0, 2)}{card("rhystic_study", 690, 160, 320, 7)}
<div style="position:absolute;left:80px;right:80px;top:720px">
<h1>300 cartas.<br><span class=hl>Zero digitação.</span></h1>
<p class=sub style="margin-top:34px">Escaneie a coleção com a câmera<br>e leve tudo pra LigaMagic.</p>
</div>
<div style="position:absolute;left:80px;bottom:150px">{badge(.62)}</div>
<div class=arrow style="bottom:180px">arraste →</div>
<div class=foot>{cred("sol_ring","the_one_ring","rhystic_study")}</div>""")

# 02 · dor (segunda chance do feed)
grid = ["arcane_signet", "command_tower", "cultivate", "cyclonic_rift", "smothering_tithe", "swords_to_plowshares"]
cells = "".join(card(s, 150 + (i % 3) * 270, 500 + (i // 3) * 345, 236) for i, s in enumerate(grid))
SLIDES["02_dor"] = page(2, f"""
<div style="position:absolute;left:80px;right:80px;top:150px">
<h2>Cadastrar coleção é<br>a pior parte de <span class=e>colecionar.</span></h2>
<p class=sub style="margin-top:26px;display:flex;align-items:center;gap:22px">Nome em inglês. Edição. Foil. <span style="background:#0A0F14;color:#F2EEE6;font-weight:700;font-size:32px;padding:10px 22px;border-radius:16px">6 de 300<span class=o>…</span></span></p>
</div>
{cells}

<div class=foot>{cred(*grid)}</div>""")

# 03 · scanner, painel escuro (liga à identidade do app)
SLIDES["03_scanner"] = page(3, f"""
<div class=panel style="left:48px;right:48px;top:130px;bottom:130px">
<div style="position:absolute;left:56px;top:150px;width:400px">
<span class=tag>SCANNER</span>
<h2>Aponte.<br><span class=e>Pronto.</span></h2>
<p class=sub style="margin-top:30px">A câmera lê a carta e o BINDER Vision ajuda a identificar a edição.</p>
</div>
<div class=shot style="left:500px;top:58px;width:420px;transform:rotate(3deg)"><img src=scan.png></div>
</div>
<div class=foot>Tela real do app (24/10/2026). Na imagem: Iron Man Armor (Marvel Super Heroes), nº 248, arte de Javier Charro. © Wizards of the Coast. Marvel ©.</div>""")

# 04 · valor: o número é o herói
SLIDES["04_valor"] = page(4, f"""
<div style="position:absolute;left:80px;top:170px;width:470px">
<span class=tag>SEU BINDER</span>
<h2>Cada carta<br>com valor<br>em reais.</h2>
<div style="margin-top:70px;font-size:150px;line-height:.9;font-weight:700;letter-spacing:-.05em" class=e>R$&nbsp;396</div>
<p class=sub style="margin-top:22px;font-size:30px">Sheoldred, the Apocalypse,<br>na coleção do fundador.</p>
</div>
<div class=tile style="left:585px;top:200px;width:430px;transform:rotate(3deg)"><img src=khan_tile.png></div>
<div class=foot>Tela real do Binder (11/11/2026). Valor de referência do app: estimativa, não oferta de compra. Na imagem: Khan, Engineered Evil / Sheoldred, the Apocalypse, arte de Nicky Barkla. © Wizards of the Coast. Star Trek © CBS.</div>""")

# 05 · LigaMagic com a tela real do botão Exportar
SLIDES["05_liga"] = page(5, f"""
<div style="position:absolute;left:80px;right:80px;top:150px">
<span class=tag>EXPORTAR</span>
<h2>Um toque.<br>Coleção na <span class=e>LigaMagic.</span></h2>
</div>
<div class=tile style="left:56px;right:56px;top:500px;border-radius:36px;background:#0A0E19">
<img src=patrimonio.png>
<div style="position:absolute;left:632px;top:114px;width:288px;height:114px;border:5px solid #E0A526;border-radius:999px"></div>
</div>
<div style="position:absolute;left:80px;right:80px;top:800px">
<div class=opt><span class=k>LISTA</span><div><div class=t>Texto rápido</div><div class=d>cole no Cadastro por Lista</div></div></div>
<div class=opt><span class=k>CSV</span><div><div class=t>Planilha</div><div class=d>suba no Importar Coleção</div></div></div>
<p class=sub style="margin-top:26px;font-size:32px">Cadastrou? <b style="color:#0A0F14">Confira o preço da Liga e anuncie lá.</b></p>
</div>
<div class=foot>Tela real do Binder (11/11/2026); patrimônio = soma dos valores de referência. Exportação no formato aceito pela LigaMagic; o BINDER não tem parceria com a LigaMagic.</div>""")

# 06 · conversão
SLIDES["06_cta"] = page(6, f"""
{card("sol_ring", 250, 140, 190, -8)}{card("the_one_ring", 445, 122, 190, 0, 2)}{card("rhystic_study", 640, 140, 190, 8)}
<div style="position:absolute;left:60px;right:60px;top:470px;text-align:center">
<h1>Escaneie aqui.<br><span class=e>Venda</span> <span class=o>lá.</span></h1>
<p class=sub style="margin-top:44px;color:#F2EEE6;font-size:44px;font-weight:700">Baixe o BINDER Vision agora</p>
<p class=sub style="margin-top:10px">e escaneie sua primeira carta hoje.</p>
<div style="margin-top:50px">{badge(1)}</div>
<p class=sub style="margin-top:30px;color:#10B981;font-weight:700">Link na bio ↑</p>
</div>
<div class=foot style="text-align:center">Beta para Android. Valores de referência são estimativas. {cred("sol_ring","the_one_ring","rhystic_study")} Google Play e o logótipo do Google Play são marcas da Google LLC.</div>""", cls="ink")

async def main():
    OUT.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for name, html in SLIDES.items():
            f = HERE / f"v3_{name}.html"; f.write_text(html, encoding="utf-8")
            await pg.goto(f.as_uri()); await pg.wait_for_timeout(400)
            await pg.screenshot(path=str(OUT / f"{name}.png"))
        await b.close()

asyncio.run(main())
