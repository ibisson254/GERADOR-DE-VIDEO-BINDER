"""Gera os 7 slides 1080x1350 do carrossel "Pare de digitar carta por carta".
Uso: python3 build.py  -> ../png/01_hook.png ... 07_cta.png
Só usa telas reais (quadros da gravação do scanner de 24/10/2026, comum/outro/scan/)."""
import pathlib, asyncio
from playwright.async_api import async_playwright

HERE = pathlib.Path(__file__).parent
OUT = HERE.parent / "png"

CSS = """
@font-face{font-family:G;src:url(Geist-Medium.woff2);font-weight:500}
@font-face{font-family:G;src:url(Geist-Bold.woff2);font-weight:700}
*{margin:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#050A10;font-family:G,sans-serif;color:#F1F5F9;overflow:hidden;position:relative}
.glow{position:absolute;inset:0;background:radial-gradient(ellipse 70% 45% at 50% 110%,rgba(16,185,129,.16),transparent 70%)}
.pad{position:absolute;inset:96px 88px}
.top{position:absolute;top:64px;left:88px;right:88px;display:flex;justify-content:space-between;font-size:24px;color:#64748B;letter-spacing:.08em;font-weight:500}
.top b{color:#10B981;font-weight:700}
h1{font-size:92px;line-height:1.02;font-weight:700;letter-spacing:-.035em}
h2{font-size:72px;line-height:1.05;font-weight:700;letter-spacing:-.03em}
.g{color:#10B981}
.sub{font-size:36px;line-height:1.35;color:#94A3B8;font-weight:500;margin-top:36px}
.foot{position:absolute;bottom:56px;left:88px;right:88px;font-size:20px;line-height:1.4;color:#64748B}
.swipe{position:absolute;bottom:60px;right:88px;font-size:26px;color:#10B981;font-weight:700}
.phone{position:absolute;border-radius:44px;overflow:hidden;box-shadow:0 40px 120px rgba(0,0,0,.6),0 0 0 2px #1E293B}
.phone img{display:block;width:100%}
.mono{font-family:ui-monospace,Menlo,monospace;font-size:30px;line-height:1.75;color:#CBD5E1}
.card{background:#0F172A;border:1px solid #1E293B;border-radius:28px;padding:44px 48px}
.step{display:flex;gap:32px;align-items:baseline;margin-bottom:40px}
.step .n{font-size:30px;color:#10B981;font-weight:700;width:54px}
.step .t{font-size:46px;font-weight:700;letter-spacing:-.02em}
.step .d{font-size:28px;color:#94A3B8;margin-top:8px;font-weight:500}
"""

def page(n, body, total=7):
    return f"""<html><head><style>{CSS}</style></head><body><div class=glow></div>
<div class=top><span><b>BINDER</b> Vision</span><span>{n:02d}/{total:02d}</span></div>{body}</body></html>"""

CRED = "Tela real do app (24/10/2026). Na carta: Iron Man Armor (Marvel Super Heroes, 2026), nº 248. Arte: Javier Charro. © Wizards of the Coast. Marvel ©."

SLIDES = {
"01_hook": page(1, """
<div class=pad style="top:300px">
<h1>Seu fichário tem<br>300 cartas.</h1>
<h1 class=g style="margin-top:28px">Você vai digitar<br>uma por uma?</h1>
</div><div class=swipe>arraste →</div>"""),

"02_identificacao": page(2, """
<div class=pad style="top:190px">
<h2>Todo colecionador<br>já fez isso.</h2>
<div class="card mono" style="margin-top:64px">
1 Sol Ring<br>1 Arcane Signet<br>1 Command Tower<br>1 Swords to Plowshares<br>1 Cultivate<br><span style="color:#475569">... faltam 295</span><span class=g>▌</span>
</div>
<p class=sub>Nome em inglês, edição certa, foil ou não.<br>E repete. E repete.</p>
</div><div class=swipe>→</div>"""),

"03_curiosidade": page(3, """
<div class=pad style="top:380px">
<h1>E se a câmera<br>fizesse a<br><span class=g>parte chata?</span></h1>
</div><div class=swipe>→</div>"""),

"04_descoberta": page(4, f"""
<div class=pad style="right:540px;top:330px">
<h2>Aponte.<br><span class=g>Pronto.</span></h2>
<p class=sub>O BINDER Vision lê a carta pela câmera e ajuda a identificá-la.</p>
</div>
<div class=phone style="left:560px;top:200px;width:460px"><img src=scan.png></div>
<div class=foot style="right:520px">{CRED}</div>"""),

"05_demonstracao": page(5, f"""
<div class=pad style="right:540px;top:330px">
<h2>Confirme.<br><span class=g>Já está no seu Binder.</span></h2>
<p class=sub>Nome, coleção e um valor de referência na mesma tela.</p>
</div>
<div class=phone style="left:560px;top:200px;width:460px"><img src=resultado.png></div>
<div class=foot style="right:520px">Valor exibido pelo app em 24/10/2026: referência do Scryfall convertida para reais. Estimativa, não oferta de compra.<br>{CRED}</div>"""),

"06_diferencial": page(6, """
<div class=pad style="top:180px">
<h2>Coleção escaneada?<br><span class=g>Leve para a LigaMagic.</span></h2>
<div style="margin-top:80px">
<div class=step><span class=n>01</span><div><div class=t>Escaneie</div><div class=d>carta por carta, com a câmera</div></div></div>
<div class=step><span class=n>02</span><div><div class=t>Exporte do seu Binder</div><div class=d>em texto (lista) ou planilha CSV</div></div></div>
<div class=step><span class=n>03</span><div><div class=t>Cole na LigaMagic</div><div class=d>no cadastro por lista ou na importação por CSV</div></div></div>
</div></div>
<div class=foot>Função de exportação do BINDER Vision no formato aceito pela LigaMagic. O BINDER não tem parceria nem vínculo com a LigaMagic; o nome pertence aos seus titulares.</div>"""),

"07_cta": page(7, """
<div class=pad style="top:330px;text-align:center;left:60px;right:60px">
<h1>Escaneie aqui.<br><span class=g>Pare de digitar.</span></h1>
<p class=sub style="margin-top:56px">BINDER Vision · beta para Android</p>
<div style="margin:64px auto 0;display:inline-block;background:#10B981;color:#050A10;font-weight:700;font-size:40px;padding:30px 64px;border-radius:999px">Baixe no Google Play · link na bio</div>
</div>
<div class=foot style="text-align:center">Disponível só para Android. Valores de referência são estimativas.</div>"""),
}

async def main():
    OUT.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for name, html in SLIDES.items():
            f = HERE / f"{name}.html"; f.write_text(html, encoding="utf-8")
            await pg.goto(f.as_uri()); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(OUT / f"{name}.png"))
        await b.close()

asyncio.run(main())
