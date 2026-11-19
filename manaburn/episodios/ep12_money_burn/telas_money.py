"""MB-EP12 · MONEY BURN · telas da TV SAL e inserts (feedback visual em cada fala, decisão de 15/11/2026).
Estilo e CSS iguais a manaburn/giro/2026-11-15/telas_visuais.py. Só cartas reais (PNG do Scryfall em cards/src/).
Uso, na pasta do kit:  python3 telas_money.py   (CHROME=/caminho/do/chrome opcional)
Saída: cards/s03_grife.png, cards/i09_upgrades.png, cards/i11_vinte.png, cards/s13_ab.png (744x1040)."""
import os, pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path('.').resolve(); SRC = ROOT / 'cards' / 'src'
u = lambda n: (SRC / n).as_uri()
CSS = """
@font-face{font-family:Bangers;src:url(node_modules/@fontsource/bangers/files/bangers-latin-400-normal.woff2)}
@font-face{font-family:Geist;font-weight:700;src:url(node_modules/geist/dist/fonts/geist-sans/Geist-Bold.woff2)}
@font-face{font-family:Geist;font-weight:500;src:url(node_modules/geist/dist/fonts/geist-sans/Geist-Medium.woff2)}
*{margin:0;padding:0;box-sizing:border-box}
body{width:744px;height:1040px;background:#0F172A;color:#F4F1E8;font-family:Geist;overflow:hidden;position:relative}
.f{position:absolute;inset:18px;border:6px solid #FFD84A;border-radius:18px;overflow:hidden}
.badge{position:absolute;left:30px;top:26px;z-index:3;background:#C8352B;color:#FFD84A;font:400 44px Bangers;letter-spacing:3px;padding:2px 18px;border-radius:6px}
.big{position:absolute;left:0;right:0;text-align:center;font:400 92px/0.95 Bangers;color:#F4F1E8;letter-spacing:1px}
.big em{font-style:normal;color:#FFD84A}
.giant{position:absolute;left:0;right:0;text-align:center;font:400 400px/0.9 Bangers;color:#FFD84A;text-shadow:0 0 34px rgba(255,216,74,.5)}
.sub{position:absolute;left:30px;right:30px;text-align:center;font:700 36px/1.2 Geist;color:#F4F1E8}
.fonte{position:absolute;left:28px;right:28px;bottom:22px;font:500 24px/1.25 Geist;color:#C9C3B2;z-index:3}
.card{position:absolute;border-radius:14px;box-shadow:0 14px 0 rgba(0,0,0,.45)}
.n{position:absolute;width:96px;height:96px;border-radius:50%;background:#FFD84A;color:#0F172A;font:400 78px/96px Bangers;text-align:center;box-shadow:0 6px 0 rgba(0,0,0,.4)}
.arrow{position:absolute;font:400 120px Bangers;color:#FFD84A}
.opt{position:absolute;left:40px;right:40px;height:240px;border:6px solid #F4F1E8;border-radius:18px;background:#16213A}
.opt .l{position:absolute;left:24px;top:22px;font:400 200px/1 Bangers;color:#FFD84A}
.opt .t{position:absolute;left:190px;right:20px;top:50%;transform:translateY(-50%);font:400 74px/0.95 Bangers;color:#F4F1E8}
"""
def card(n, x, y, w, rot=0): return f'<img class="card" src="{u(n)}" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg)">'
TELAS = {
 # fala 3 · B «Troquei DEZ terrenos básicos por terreno de grife»
 's03_grife': f"""<div class="f"><span class="badge">UPGRADE DO BURN</span>
   {card('mountain.png', 50, 200, 250, -5)}<div class="n" style="left:40px;top:150px">10×</div>
   <div class="arrow" style="left:318px;top:300px">→</div>
   {card('volcanic.png', 432, 190, 250, 5)}
   <div class="big" style="top:640px">BÁSICO <em>→</em> GRIFE</div>
   <div class="sub" style="top:750px">Montanha → Volcanic Island<br>(terreno não básico)</div>
   <div class="fonte">Mountain (Foundations 279, Rebecca Guay) · Volcanic Island (Vintage Masters 324, Noah Bradley). © Wizards of the Coast.</div></div>""",
 # fala 9 · B «Agora meu deck é intocável» — insert: as compras do Burn
 'i09_upgrades': f"""<div class="f"><span class="badge">O DECK «PRONTO»</span>
   {card('volcanic.png', 52, 175, 200, -5)}{card('opportunity.png', 272, 150, 200, 0)}{card('greed.png', 492, 175, 200, 5)}
   <div class="big" style="top:560px">INTOCÁVEL<em>?</em></div>
   <div class="sub" style="top:680px">10 terrenos de grife<br>+ Opportunity + Greed</div>
   <div class="fonte">Volcanic Island (VMA 324, Noah Bradley) · Opportunity (J25 338, Allen Williams) · Greed (MH2 274, Izzy). © Wizards of the Coast.</div></div>""",
 # fala 11 · B «VINTE?!» — número gigante com a conta
 'i11_vinte': f"""<div class="f"><span class="badge">PRICE OF PROGRESS</span>
   <div class="giant" style="top:150px">20</div>
   <div class="big" style="top:520px">DE <em>DANO</em></div>
   <div class="sub" style="top:650px">2 de dano × 10 terrenos<br>não básicos = <span style="color:#FFD84A">20</span></div>
   <div class="fonte">Conta com o texto Oracle de Price of Progress (Scryfall, 19/11/2026) e os 10 terrenos do Burn (fala 3).</div></div>""",
 # fala 13 · B pergunta A/B
 's13_ab': f"""<div class="f"><span class="badge">SEU DECK</span>
   {card('unfinished.png', 478, 50, 200, 4)}
   <div class="opt" style="top:370px"><span class="l">A</span><span class="t">TÁ PRONTO</span></div>
   <div class="opt" style="top:640px"><span class="l">B</span><span class="t">FALTA SÓ<br>UMA CARTA</span></div>
   <div class="fonte">Na TV: Unfinished Business (Wilds of Eldraine Commander 44, Mark Zug). © Wizards of the Coast.</div></div>""",
}
def main():
    kw = {'executable_path': os.environ['CHROME']} if os.environ.get('CHROME') else {}
    with sync_playwright() as p:
        b = p.chromium.launch(**kw); pg = b.new_page(viewport={'width': 744, 'height': 1040})
        for nome, html in TELAS.items():
            tmp = ROOT / '_tela.html'
            tmp.write_text(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{html}</body></html>', encoding='utf-8')
            pg.goto(tmp.as_uri())
            pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
            pg.screenshot(path=str(ROOT / 'cards' / f'{nome}.png')); print('ok', nome)
        b.close(); (ROOT / '_tela.html').unlink(missing_ok=True)
if __name__ == '__main__': main()
