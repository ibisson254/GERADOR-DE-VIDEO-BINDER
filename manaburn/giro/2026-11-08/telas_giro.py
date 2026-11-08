"""Giro de domingo 08/11/2026 · telas tipográficas da TV SAL (744x1040, o formato das cartas no kit).
Uso, na pasta do kit (precisa de node_modules/ para as fontes Bangers e Geist):
  python3 telas_giro.py            -> cards/giro_abre.png, cards/giro_filme.png, cards/giro_prerelease.png
Só texto com fonte verificada (ficha_fontes.md). As telas da retrospectiva são quadros reais dos episódios (ver ficha.md).
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
    <div class="k">DOMINGO · 08/11/2026</div>
    <div class="t">GIRO DE<br><em>DOMINGO</em></div>
    <div class="num"><div>1</div><div>2</div><div>3</div></div>
    <ul style="margin-top:56px"><li>a semana no BINDER</li><li>recado do TUBO</li></ul>
    <div class="fonte">notícias de 02 a 08/11/2026</div></div>""",
  'giro_filme': """<div class="f"><span class="badge">1 · CINEMA</span>
    <div class="k">FILME DE MAGIC · LIVE-ACTION</div>
    <div class="t">MAYA HAWKE<br><em>NO ELENCO</em></div>
    <ul><li>primeira atriz anunciada</li><li>papel ainda em segredo</li><li>direção: Matt Johnson</li></ul>
    <div class="fonte">Fontes: Deadline e TheWrap (04/11/2026). Legendary e Hasbro.</div></div>""",
  'giro_prerelease': """<div class="f"><span class="badge">3 · PRA JOGAR</span>
    <div class="k">MAGIC: THE GATHERING | STAR TREK</div>
    <div class="t">PRÉ-RELEASE<br><em>ATÉ 12/11</em></div>
    <ul><li>Sealed: 6 boosters</li><li>MTG Arena: 10/11</li><li>nas lojas: 13/11</li></ul>
    <div class="fonte">Fontes: Wizards of the Coast, guia do pré-release e anúncios do MTG Arena (02/11/2026).</div></div>""",
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
