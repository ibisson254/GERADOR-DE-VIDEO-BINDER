"""MB-EP14 · EVERYTHING, MENOS TUDO · telas da TV SAL e inserts (feedback visual em cada fala, decisão de 15/11/2026).
Estilo e CSS iguais a manaburn/episodios/ep12_money_burn/telas_money.py. Só cartas reais (PNG do Scryfall em cards/src/,
Secret Lair Drop 2912–2930, 20/11/2026) e números do anúncio oficial da Wizards (18/11/2026) ou contas feitas com eles.
Uso, na pasta do kit (com cards/src/ copiado):  python3 telas_everything.py   (CHROME=/caminho/do/chrome opcional)
Saída: cards/<nome>.png (744x1040). As posições das linhas destacadas (EP.canais[].hl) são frações destas telas."""
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
.big{position:absolute;left:0;right:0;text-align:center;font:400 88px/0.95 Bangers;color:#F4F1E8;letter-spacing:1px}
.big em{font-style:normal;color:#FFD84A}
.giant{position:absolute;left:0;right:0;text-align:center;font:400 190px/0.9 Bangers;color:#FFD84A;text-shadow:0 0 30px rgba(255,216,74,.45)}
.sub{position:absolute;left:30px;right:30px;text-align:center;font:700 36px/1.2 Geist;color:#F4F1E8}
.sub em{font-style:normal;color:#FFD84A}
.row{position:absolute;left:44px;right:44px;height:66px;border-radius:10px;background:#16213A;border:3px solid #F4F1E8;font:700 34px/60px Geist;padding-left:20px;color:#F4F1E8}
.row b{color:#FFD84A}
.fonte{position:absolute;left:28px;right:28px;bottom:22px;font:500 24px/1.25 Geist;color:#C9C3B2;z-index:3}
.card{position:absolute;border-radius:12px;box-shadow:0 12px 0 rgba(0,0,0,.45)}
.lbl{position:absolute;text-align:center;font:400 34px/1 Bangers;letter-spacing:1px;color:#F4F1E8}
.stamp{position:absolute;font:400 64px/1 Bangers;color:#FF5A4E;border:6px solid #FF5A4E;border-radius:10px;padding:4px 16px;background:rgba(15,23,42,.82);letter-spacing:2px}
.brk{position:absolute;border:6px solid #FFD84A;border-top:none;border-radius:0 0 14px 14px}
.opt{position:absolute;left:40px;right:40px;height:250px;border:6px solid #F4F1E8;border-radius:18px;background:#16213A}
.opt .l{position:absolute;left:24px;top:22px;font:400 200px/1 Bangers;color:#FFD84A}
.opt .t{position:absolute;left:175px;right:20px;top:50%;transform:translateY(-50%);font:400 66px/0.95 Bangers;color:#F4F1E8}
.opt .p{display:block;font:700 34px/1.3 Geist;color:#FFD84A;margin-top:6px}
"""
def card(n, x, y, w, rot=0): return f'<img class="card" src="{u(n)}" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg)">'
FW = 'Anúncio oficial: Wizards of the Coast, 18/11/2026 (preços nos EUA).'
CR = '© Wizards of the Coast. Conteúdo de fã não oficial.'
TELAS = {
 # fala 1 · B «TRÊS drops de Duna. E o pacote EVERYTHING só leva DOIS?!» — quadro 0
 's01_tres': f"""<div class="f"><span class="badge">SECRET LAIR x DUNA</span>
   <div class="big" style="top:96px">3 DROPS</div>
   {card('paul.png', 36, 205, 200, -3)}{card('shaihulud.png', 258, 205, 200, 0)}{card('wateroflife.png', 488, 225, 196, 5)}
   <div class="lbl" style="left:30px;width:230px;top:516px">BALANCE<br>OF POWER</div>
   <div class="lbl" style="left:258px;width:230px;top:516px">DESERTS<br>OF ARRAKIS</div>
   <div class="lbl" style="left:476px;width:230px;top:520px;color:#FF5A4E">SPICE</div>
   <div class="brk" style="left:40px;width:420px;top:590px;height:44px"></div>
   <div class="stamp" style="left:520px;top:568px;transform:rotate(-8deg)">FORA</div>
   <div class="big" style="top:660px;font-size:80px">EVERYTHING<br>LEVA <em>2</em></div>
   <div class="fonte">Paul Atreides, Ducal Heir (SLD 2912, Jodie Muir) · Shai-Hulud (SLD 2920, Grzegorz Rutkowski) · Water of Life (SLD 2926, Svetlin Velinov). {CR}</div></div>""",
 # fala 2 · M «Lê o anúncio: Balance of Power e Deserts of Arrakis. Foil e não foil.» — linhas destacadas (tvtext)
 's02_anuncio': f"""<div class="f"><span class="badge">LÊ O ANÚNCIO</span>
   {card('paul.png', 110, 96, 170, -3)}{card('shaihulud.png', 464, 96, 170, 3)}
   <div class="big" style="top:350px;font-size:62px">DESERT POWER<br><em>EVERYTHING</em> BUNDLE</div>
   <div class="row" style="top:490px">1× Balance of Power · <b>foil</b></div>
   <div class="row" style="top:568px">1× Balance of Power · <b>não foil</b></div>
   <div class="row" style="top:646px">1× Deserts of Arrakis · <b>foil</b></div>
   <div class="row" style="top:724px">1× Deserts of Arrakis · <b>não foil</b></div>
   <div class="sub" style="top:815px;color:#FF5A4E">Spice: não está na lista</div>
   <div class="fonte">Anúncio oficial: Wizards, 18/11/2026. Cartas: SLD 2912 (Jodie Muir), SLD 2920 (Grzegorz Rutkowski). {CR}</div></div>""",
 # fala 3 · B «Quatro caixas! E o Spice vem de brinde, né?»
 's03_brinde': f"""<div class="f"><span class="badge">O BURN JURA</span>
   {card('wateroflife.png', 40, 150, 220, -6)}{card('painbox.png', 262, 120, 220, 0)}{card('revel.png', 484, 150, 220, 6)}
   <div class="big" style="top:500px">SPICE DE<br><em>BRINDE?</em></div>
   <div class="sub" style="top:700px">4 caixas no bundle<br>+ o terceiro drop… grátis?</div>
   <div class="fonte">Water of Life (SLD 2926, Svetlin Velinov) · Pain Box (SLD 2930, Alexander Mokhov) · Revel in Riches (SLD 2927, Raymond Swanland). {CR}</div></div>""",
 # fala 4 · M «Não. Spice é o terceiro drop, só em Halo Foil. Vendido à parte.» — linhas destacadas (tvtext)
 's04_spice': f"""<div class="f"><span class="badge">LÊ O ANÚNCIO</span>
   {card('wateroflife.png', 44, 96, 190, -5)}{card('painbox.png', 277, 86, 190, 0)}{card('harvester.png', 498, 96, 184, 4)}
   <div class="big" style="top:405px;font-size:66px">SPICE · <em>TERCEIRO DROP</em></div>
   <div class="row" style="top:510px;text-align:center;padding:0;font-size:40px">Só em <b>Halo Foil</b></div>
   <div class="row" style="top:600px;text-align:center;padding:0;font-size:40px">Vendido <b>à parte</b></div>
   <div class="sub" style="top:705px;color:#FF5A4E">Fora do Everything Bundle</div>
   <div class="fonte">{FW} Water of Life (SLD 2926) · Pain Box (SLD 2930) · Harkonnen Spice Harvester (SLD 2928, Raphael Lacoste). {CR}</div></div>""",
 # fala 5 · B «Tá, e quanto custa esse tempero?» — insert no grande plano do Burn
 'i05_tempero': f"""<div class="f"><span class="badge">O TEMPERO</span>
   {card('harvester.png', 52, 130, 300, -5)}{card('revel.png', 392, 150, 300, 5)}
   <div class="giant" style="top:600px">$ ?</div>
   <div class="fonte">Harkonnen Spice Harvester (SLD 2928, Raphael Lacoste) · Revel in Riches (SLD 2927, Raymond Swanland). Drop Spice, Halo Foil. {CR}</div></div>""",
 # fala 6 · M «US$ 59,99. Sozinho.»
 's06_spice_preco': f"""<div class="f"><span class="badge">PREÇO DO SPICE</span>
   {card('wateroflife.png', 232, 100, 280, 0)}
   <div class="giant" style="top:520px;font-size:170px">$59,99</div>
   <div class="sub" style="top:700px">Spice · <em>Halo Foil</em><br>sozinho, fora do bundle</div>
   <div class="fonte">{FW} Water of Life (SLD 2926, Svetlin Velinov). {CR}</div></div>""",
 # fala 7 · B «E o EVERYTHING? Deve ter um descontão!»
 's07_descontao': f"""<div class="f"><span class="badge">EVERYTHING BUNDLE</span>
   {card('paul.png', 36, 110, 152, -3)}{card('paul.png', 204, 110, 152, 0)}{card('shaihulud.png', 380, 110, 152, 0)}{card('shaihulud.png', 540, 110, 150, 2)}
   <div class="lbl" style="left:36px;width:320px;top:335px;font-size:28px">FOIL + NÃO FOIL</div>
   <div class="lbl" style="left:380px;width:320px;top:335px;font-size:28px">FOIL + NÃO FOIL</div>
   <div class="big" style="top:420px">DESCONTÃO<em>?</em></div>
   <div class="giant" style="top:540px;font-size:230px">$ ??</div>
   <div class="fonte">Balance of Power (SLD 2912, Jodie Muir) e Deserts of Arrakis (SLD 2920, Grzegorz Rutkowski), foil e não foil. {CR}</div></div>""",
 # fala 8 · M «US$ 174,99. Desconto: US$ 4,97.» — linha do desconto destacada (tvtext)
 's08_bundle_preco': f"""<div class="f"><span class="badge">LÊ O ANÚNCIO</span>
   <div class="giant" style="top:120px;font-size:180px">$174,99</div>
   <div class="sub" style="top:300px">Desert Power <em>Everything</em> Bundle</div>
   <div class="sub" style="top:385px;font-size:30px;color:#C9C3B2">Separado: 39,99 + 49,99<br>+ 39,99 + 49,99 = <span style="color:#F4F1E8">179,96</span></div>
   <div class="row" style="top:508px;height:110px;text-align:center;padding:0;font:400 84px/104px Bangers;letter-spacing:1px">DESCONTO: <b>$4,97</b></div>
   {card('paul.png', 150, 640, 120, -3)}{card('shaihulud.png', 290, 640, 120, 0)}<div class="lbl" style="left:150px;width:260px;top:818px;font-size:28px">NO BUNDLE</div>
   {card('wateroflife.png', 474, 645, 120, 5)}<div class="lbl" style="left:444px;width:180px;top:818px;font-size:28px;color:#FF5A4E">FORA</div>
   <div class="fonte">{FW} Desconto = soma dos 4 preços avulsos − preço do bundle (conta do BINDER). {CR}</div></div>""",
 # fala 9 · B «Cinco dólares de desconto… e ainda falta UM?!» — insert no grande plano do Burn
 'i09_desconto': f"""<div class="f"><span class="badge">O DESCONTÃO</span>
   <div class="giant" style="top:110px;font-size:210px">−$4,97</div>
   <div class="big" style="top:330px">E AINDA<br>FALTA <em>1</em></div>
   {card('wateroflife.png', 262, 540, 220, 6)}
   <div class="fonte">179,96 (4 edições separadas) − 174,99 (bundle) = 4,97. Preços oficiais nos EUA, Wizards, 18/11/2026. {CR}</div></div>""",
 # fala 10 · M «Pra levar os três: US$ 234,98.»
 's10_tres_drops': f"""<div class="f"><span class="badge">OS TRÊS DROPS</span>
   {card('paul.png', 50, 100, 190, -4)}{card('shaihulud.png', 277, 90, 190, 0)}{card('wateroflife.png', 498, 100, 184, 3)}
   <div class="sub" style="top:420px;font-size:40px">Bundle <em>174,99</em> + Spice <em>59,99</em></div>
   <div class="giant" style="top:500px;font-size:200px">$234,98</div>
   <div class="sub" style="top:700px">para ter os 3 drops<br>(preço nos EUA, antes de impostos)</div>
   <div class="fonte">Conta do BINDER com os preços oficiais nos EUA (Wizards, 18/11/2026). {CR}</div></div>""",
 # fala 11 · B «Então o pacote de TUDO deixa coisa de fora!» — insert no grande plano do Burn
 'i11_menos': f"""<div class="f"><span class="badge">EVERYTHING*</span>
   <div class="big" style="top:110px;font-size:110px">EVERY<br>THING<em>*</em></div>
   <div class="sub" style="top:360px;font-size:44px;color:#FFD84A">*menos o Spice</div>
   {card('wateroflife.png', 150, 470, 210, -6)}{card('painbox.png', 384, 470, 210, 6)}
   <div class="fonte">Drop Spice (Halo Foil), fora do Desert Power Everything Bundle. Water of Life (SLD 2926) · Pain Box (SLD 2930). {CR}</div></div>""",
 # fala 12 · M «Venda dia 30 de novembro, 14h de Brasília. No site da Secret Lair.» — linhas destacadas (tvtext)
 's12_data': f"""<div class="f"><span class="badge">QUANDO</span>
   {card('shaihulud.png', 247, 86, 250, 0)}
   <div class="row" style="top:460px;height:96px;text-align:center;padding:0;font:400 76px/92px Bangers;letter-spacing:1px">30 DE <b>NOVEMBRO</b></div>
   <div class="row" style="top:572px;height:76px;text-align:center;padding:0;font-size:40px;line-height:70px"><b>14h</b> Brasília · <b>17h</b> Lisboa</div>
   <div class="sub" style="top:672px;font-size:32px">9h PT · fila virtual 1 h antes<br>site da Secret Lair</div>
   <div class="sub" style="top:780px;font-size:26px;color:#C9C3B2">Não foil dos 2 primeiros drops chega<br>depois às lojas WPN (sem data)</div>
   <div class="fonte">{FW} Shai-Hulud (SLD 2920, Grzegorz Rutkowski). {CR}</div></div>""",
 # fala 13 · B pergunta A/B — insert no grande plano do Burn
 's13_ab': f"""<div class="f"><span class="badge">E VOCÊ?</span>
   {card('wateroflife.png', 520, 40, 150, 6)}
   <div class="opt" style="top:330px"><span class="l">A</span><span class="t">BUNDLE DE QUASE TUDO<span class="p">US$ 174,99</span></span></div>
   <div class="opt" style="top:620px"><span class="l">B</span><span class="t">SÓ O SPICE<span class="p">US$ 59,99</span></span></div>
   <div class="fonte">Preços oficiais nos EUA (Wizards, 18/11/2026). Water of Life (SLD 2926). {CR}</div></div>""",
}
# variantes «a meio da fala» (EP.canais[].meio, MB-EP14): a mesma tela com um carimbo novo, sem tapar cartas nem as linhas destacadas
def _var(base, velho, novo):
    assert velho in TELAS[base], base
    return TELAS[base].replace(velho, novo)
TELAS['s01_tres_b'] = _var('s01_tres', '<div class="big" style="top:96px">3 DROPS</div>',
    '<div class="big" style="top:96px">3 DROPS</div><div class="stamp" style="left:516px;top:104px;font-size:38px;white-space:nowrap;padding:2px 10px;transform:rotate(6deg)">2 DE 3?!</div>')
TELAS['s02_anuncio_b'] = _var('s02_anuncio', '<div class="sub" style="top:815px;color:#FF5A4E">Spice: não está na lista</div>',
    '<div class="stamp" style="left:150px;top:796px;font-size:40px;transform:rotate(-2deg)">SPICE: FORA DA LISTA</div>')
TELAS['s04_spice_b'] = _var('s04_spice', '<div class="sub" style="top:705px;color:#FF5A4E">Fora do Everything Bundle</div>',
    '<div class="stamp" style="left:150px;top:700px;font-size:60px;transform:rotate(-4deg)">NÃO É BRINDE</div>')
TELAS['s08_bundle_preco_b'] = _var('s08_bundle_preco', 'font:400 84px/104px Bangers;letter-spacing:1px">DESCONTO: <b>$4,97</b></div>',
    'font:400 58px/104px Bangers;letter-spacing:0;white-space:nowrap;border-color:#FF5A4E">DESCONTO: <b>$4,97</b> <span style="color:#FF5A4E">(≈2,8%)</span></div>')
TELAS['s10_tres_drops_b'] = _var('s10_tres_drops', '<div class="sub" style="top:700px">para ter os 3 drops<br>(preço nos EUA, antes de impostos)</div>',
    '<div class="sub" style="top:700px">para ter os 3 drops<br>(preço nos EUA, antes de impostos)</div><div class="stamp" style="left:396px;top:26px;font-size:36px;padding:2px 12px;transform:rotate(2deg)">AGORA SIM, TUDO</div>')
TELAS['s12_data_b'] = _var('s12_data', '<div class="sub" style="top:780px;font-size:26px;color:#C9C3B2">',
    '<div class="stamp" style="left:516px;top:150px;font-size:40px;transform:rotate(8deg)">AGENDA!</div><div class="sub" style="top:780px;font-size:26px;color:#C9C3B2">')

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
