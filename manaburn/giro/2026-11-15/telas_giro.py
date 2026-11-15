"""Giro de domingo 15/11/2026 · telas tipográficas da TV SAL (744x1040, o formato das cartas no kit).
Uso, na pasta do kit (precisa de node_modules/ para as fontes Bangers e Geist):
  python3 telas_giro.py            -> cards/giro_abre.png, giro_bk.png, giro_carne.png, giro_netflix.png, giro_mundial.png
Só texto com fonte verificada (fontes.md). A carta da Chandra é o PNG do Scryfall (cards/giro_chandra.png).
"""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent.resolve()
CSS = """
@font-face{font-family:Bangers;src:url(node_modules/@fontsource/bangers/files/bangers-latin-400-normal.woff2)}
@font-face{font-family:Geist;font-weight:700;src:url(node_modules/geist/dist/fonts/geist-sans/Geist-Bold.woff2)}
@font-face{font-family:Geist;font-weight:500;src:url(node_modules/geist/dist/fonts/geist-sans/Geist-Medium.woff2)}
*{margin:0;padding:0;box-sizing:border-box}
body{width:744px;height:1040px;background:#0F172A;color:#F4F1E8;font-family:Geist;overflow:hidden}
.f{position:absolute;inset:22px;border:6px solid #FFD84A;border-radius:18px;padding:46px 44px}
.badge{display:inline-block;background:#C8352B;color:#FFD84A;font:400 50px Bangers;letter-spacing:4px;padding:4px 22px;border-radius:6px}
.k{margin-top:46px;font:700 34px Geist;letter-spacing:2px;color:#FFD84A}
.t{margin-top:18px;font:400 104px/0.98 Bangers;letter-spacing:1px;color:#F4F1E8}
.t em{font-style:normal;color:#FFD84A}
ul{margin-top:40px;list-style:none}
li{font:700 38px/1.25 Geist;margin-bottom:18px;padding-left:34px;position:relative}
li:before{content:'';position:absolute;left:0;top:16px;width:16px;height:16px;background:#10B981;border-radius:50%}
.fonte{position:absolute;left:44px;right:44px;bottom:40px;font:500 26px/1.3 Geist;color:#C9C3B2}
.num{display:flex;gap:28px;margin-top:56px}
.num div{width:170px;height:170px;border:6px solid #FFD84A;border-radius:14px;font:400 130px/170px Bangers;text-align:center;color:#FFD84A}
"""
TELAS = {
  'giro_abre': """<div class="f"><span class="badge">TV SAL</span>
    <div class="k">DOMINGO · 15/11/2026</div>
    <div class="t">GIRO DE<br><em>DOMINGO</em></div>
    <div class="num"><div>1</div><div>2</div><div>3</div></div>
    <ul style="margin-top:56px"><li>lanche · série · Mundial</li><li>a semana no BINDER</li></ul>
    <div class="fonte">notícias de 09 a 15/11/2026</div></div>""",
  'giro_bk': """<div class="f"><span class="badge">1 · LANCHE</span>
    <div class="k">BURGER KING ITÁLIA × MAGIC</div>
    <div class="t">LANCHE COM<br><em>DECK BOX</em></div>
    <ul><li>€19,90: lanche + deck box + 100 sleeves</li><li>só na Itália, até 30/11</li><li>torneio em 9 restaurantes</li><li>final: 27/11, em Milão</li></ul>
    <div class="fonte">Fontes: Burger King Itália, via Dexerto, ICv2 e MTG Rocks (10–11/11/2026).</div></div>""",
  'giro_netflix': """<div class="f"><span class="badge">2 · STREAMING</span>
    <div class="k">NETFLIX · SÉRIE ANIMADA</div>
    <div class="t">PLANES-<br><em>WALKER</em></div>
    <ul><li>estreia em 2027, sem data</li><li>protagonista: Chandra</li><li>showrunner: Terry Matalas, de <em style="font-style:normal;color:#FFD84A">Star Trek: Picard</em></li></ul>
    <div class="fonte">Fontes: Netflix Tudum e Deadline (13/11/2026).</div></div>""",
  'giro_mundial': """<div class="f"><span class="badge">3 · MUNDIAL</span>
    <div class="k">MAGIC WORLD CHAMPIONSHIP 32</div>
    <div class="t">DECISÃO<br><em>HOJE</em></div>
    <ul><li>Atlanta, 13 a 15/11</li><li>Draft de Star Trek + Standard</li><li>previsão do TUBO: Jund Sacrifice no Top 8</li><li>prestação de contas: segunda, 16/11</li></ul>
    <div class="fonte">Fontes: magic.gg (ficha do Mundial 32); Meta em Curto EP07.</div></div>""",
  'giro_tubo': """<div class="f"><span class="badge">A SEMANA · TUBO</span>
    <div class="k">META EM CURTO · 3 EPISÓDIOS</div>
    <div class="t">O TUBO EM<br><em>DOBRO</em></div>
    <ul><li>EP07: seis brasileiros no Mundial</li><li>ESP01: Precon em dupla</li><li>ESP02: quem começa o jogo 1 vence <em style="font-style:normal;color:#FFD84A">66%</em></li></ul>
    <div class="fonte">Dados do ESP02: Taça Preconauta (@preconautamtg).</div></div>""",
  'giro_nauctis': """<div class="f"><span class="badge">A SEMANA · EXPEDIÇÃO</span>
    <div class="k">EXPEDIÇÃO BINDER #01</div>
    <div class="t">NAUCTIS<br><em>MERGULHO 1</em></div>
    <ul><li>Nauctis: The Sunken Realm</li><li>3 camadas, 6 espécies</li><li>no fundo do mar, um <em style="font-style:normal;color:#FFD84A">Lotus</em></li></ul>
    <div class="fonte">BINDER Originals · Expedição BINDER.</div></div>""",
}

def main():
    out = ROOT / 'cards'; out.mkdir(exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 744, 'height': 1040})
        for nome, corpo in TELAS.items():
            html = ROOT / f'_{nome}.html'
            html.write_text(f'<!doctype html><meta charset="utf-8"><style>{CSS}</style><body>{corpo}</body>', encoding='utf-8')
            pg.goto(html.as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
            pg.screenshot(path=str(out / f'{nome}.png')); html.unlink()
            print('ok', nome)
        b.close()

if __name__ == '__main__':
    main()
