"""Carrossel v2 "Pare de digitar" · paleta clara (papel + tinta + esmeralda + ouro) · 6 slides 1080x1350.
Uso: python3 build_v2.py -> ../png_v2/
Telas reais: scan.png (gravação 24/10), top3.png (Perfil, 11/11), sem rostos nem nomes de outros usuários."""
import pathlib, asyncio
from playwright.async_api import async_playwright

HERE = pathlib.Path(__file__).parent
OUT = HERE.parent / "png_v2"

CSS = """
@font-face{font-family:G;src:url(Geist-Medium.woff2);font-weight:500}
@font-face{font-family:G;src:url(Geist-Bold.woff2);font-weight:700}
*{margin:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#F2EEE6;font-family:G,sans-serif;color:#0A0F14;overflow:hidden;position:relative}
body.ink{background:#0A0F14;color:#F2EEE6}
.grain{position:absolute;inset:0;opacity:.35;background-image:radial-gradient(rgba(10,15,20,.08) 1px,transparent 1px);background-size:6px 6px}
.ink .grain{background-image:radial-gradient(rgba(242,238,230,.05) 1px,transparent 1px)}
.top{position:absolute;top:60px;left:80px;right:80px;display:flex;justify-content:space-between;align-items:center;font-size:24px;font-weight:700;letter-spacing:.06em}
.top .n{color:#8A8478;font-weight:500}
.dot{display:inline-block;width:14px;height:14px;border-radius:50%;background:#0E9F6E;margin-right:12px}
.pad{position:absolute;left:80px;right:80px}
h1{font-size:104px;line-height:.98;font-weight:700;letter-spacing:-.045em}
h2{font-size:80px;line-height:1;font-weight:700;letter-spacing:-.04em}
.e{color:#0E9F6E}.o{color:#E0A526}
.hl{background:#E0A526;color:#0A0F14;padding:0 14px;border-radius:10px}
.sub{font-size:36px;line-height:1.3;color:#4A4E55;font-weight:500;margin-top:32px}
.ink .sub{color:#A9A59C}
.foot{position:absolute;bottom:54px;left:80px;right:80px;font-size:20px;line-height:1.4;color:#8A8478}
.shot{position:absolute;border-radius:36px;overflow:hidden;box-shadow:0 30px 80px rgba(10,15,20,.28);border:10px solid #0A0F14;background:#0A0F14}
.shot img{display:block;width:100%}
.tag{display:inline-block;font-size:24px;font-weight:700;letter-spacing:.1em;color:#0E9F6E;border:2px solid #0E9F6E;border-radius:999px;padding:8px 22px;margin-bottom:34px}
.list{font-family:ui-monospace,Menlo,monospace;font-size:34px;line-height:1.7;background:#0A0F14;color:#E7E3DA;border-radius:28px;padding:40px 48px}
.opt{display:flex;align-items:center;gap:28px;background:#fff;border-radius:26px;padding:34px 40px;margin-bottom:24px;box-shadow:0 10px 30px rgba(10,15,20,.08)}
.opt .k{font-size:28px;font-weight:700;color:#F2EEE6;background:#0E9F6E;border-radius:16px;padding:14px 20px;min-width:110px;text-align:center}
.opt .t{font-size:38px;font-weight:700;letter-spacing:-.02em}
.opt .d{font-size:26px;color:#6B6F76;margin-top:6px;font-weight:500}
.arrow{position:absolute;bottom:58px;right:80px;font-size:28px;font-weight:700;color:#0E9F6E}
.btn{display:inline-block;background:#0E9F6E;color:#F2EEE6;font-weight:700;font-size:40px;padding:30px 60px;border-radius:999px}
"""

def page(n, body, cls="", total=6):
    return f"""<html><head><style>{CSS}</style></head><body class="{cls}"><div class=grain></div>
<div class=top><span><span class=dot></span>BINDER Vision</span><span class=n>{n}/{total}</span></div>{body}</body></html>"""

CARD_CRED = "Cartas © Wizards of the Coast; Star Trek © CBS; Marvel ©. Telas reais do app."

SLIDES = {
"01_hook": page(1, """
<div class=pad style="top:360px">
<h1>Seu fichário<br>tem 300 cartas.</h1>
<h1 style="margin-top:44px;line-height:1.12">Vai digitar<br><span class=hl>uma por uma?</span></h1>
</div><div class=arrow>arraste →</div>"""),

"02_dor": page(2, """
<div class=pad style="top:270px">
<h2>A parte chata<br>de ter coleção:</h2>
<div class=list style="margin-top:56px">
1 Sol Ring<br>1 Arcane Signet<br>1 Command Tower<br>1 Swords to Plowshares<br><span style="color:#6B6F76">... faltam 296</span><span style="color:#E0A526">▌</span>
</div>
<p class=sub>Nome em inglês. Edição certa. Foil ou não.</p>
</div><div class=arrow>→</div>"""),

"03_scanner": page(3, f"""
<div class=pad style="top:300px;right:560px">
<span class=tag>SCANNER</span>
<h2>Aponte<br>a câmera.</h2>
<p class=sub>O BINDER Vision lê a carta e ajuda a identificar a edição.</p>
</div>
<div class=shot style="left:560px;top:170px;width:440px;transform:rotate(2deg)"><img src=scan.png></div>
<div class=foot style="right:560px">Iron Man Armor (Marvel Super Heroes), arte de Javier Charro. © Wizards of the Coast; Marvel ©. Tela real do app.</div>"""),

"04_valor": page(4, f"""
<div class=pad style="top:180px">
<span class=tag>SEU BINDER</span>
<h2>Cada carta<br>com <span class=e>valor em reais.</span></h2>
</div>
<div class=shot style="left:60px;right:60px;top:520px"><img src=top3.png></div>
<div class=foot>Valor de referência do app, em 11/11/2026. Estimativa, não oferta de compra. {CARD_CRED}</div>"""),

"05_liga": page(5, """
<div class=pad style="top:180px">
<span class=tag>EXPORTAR</span>
<h2>Leve tudo pra<br><span class=e>LigaMagic.</span></h2>
<p class=sub>Sem digitar nada. Escolha o formato e cole lá:</p>
<div style="margin-top:48px">
<div class=opt><span class=k>LISTA</span><div><div class=t>Texto rápido</div><div class=d>vai direto no Cadastro por Lista</div></div></div>
<div class=opt><span class=k>CSV</span><div><div class=t>Planilha</div><div class=d>vai na Importar Coleção</div></div></div>
</div>
<p class=sub style="font-size:32px">Cadastrou? Confira o preço da Liga e anuncie lá.</p>
</div>
<div class=foot>Exportação no formato aceito pela LigaMagic. O BINDER não tem parceria com a LigaMagic.</div>"""),

"06_cta": page(6, """
<div class=pad style="top:300px;text-align:center">
<h1>Escaneie aqui.<br><span class=e>Venda</span> <span class=o>lá.</span></h1>
<p class=sub style="margin-top:48px">BINDER Vision · beta para Android</p>
<div style="margin-top:70px"><span class=btn>Baixe no Google Play · link na bio</span></div>
</div>
<div class=foot style="text-align:center">Só Android. Valores de referência são estimativas.</div>""", cls="ink"),
}

async def main():
    OUT.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for name, html in SLIDES.items():
            f = HERE / f"v2_{name}.html"; f.write_text(html, encoding="utf-8")
            await pg.goto(f.as_uri()); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(OUT / f"{name}.png"))
        await b.close()

asyncio.run(main())
