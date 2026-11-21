"""MB-EP15 · Felidar Sovereign · telas da TV SAL e inserts (feedback visual em cada fala, decisão de 15/11/2026).
Estilo e CSS iguais a episodios/ep14_everything/telas_everything.py. Só cartas reais (PNG do Scryfall em cards/src/:
felidar.png = j25/198, oloro.png = c13/203, 21/11/2026) e o texto oficial da ruling do Felidar (Wizards, 25/08/2015, via Scryfall).
Uso, na pasta do kit (com cards/src/ copiado):  CHROME=/usr/bin/google-chrome python3 telas_felidar.py
Saída: cards/<nome>.png (744x1040). As posições das linhas destacadas (EP.canais[].hl) são frações destas telas."""
import os, pathlib, shutil
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
.row{position:absolute;left:44px;right:44px;height:66px;border-radius:10px;background:#16213A;border:3px solid #F4F1E8;font:700 30px/60px Geist;padding-left:18px;color:#F4F1E8;white-space:nowrap}
.row b{color:#FFD84A}
.fonte{position:absolute;left:28px;right:28px;bottom:22px;font:500 24px/1.25 Geist;color:#C9C3B2;z-index:3}
.card{position:absolute;border-radius:12px;box-shadow:0 12px 0 rgba(0,0,0,.45)}
.lbl{position:absolute;text-align:center;font:400 34px/1 Bangers;letter-spacing:1px;color:#F4F1E8}
.stamp{position:absolute;font:400 64px/1 Bangers;color:#FF5A4E;border:6px solid #FF5A4E;border-radius:10px;padding:4px 16px;background:rgba(15,23,42,.86);letter-spacing:2px;white-space:nowrap;z-index:4}
.hlbox{position:absolute;background:rgba(255,216,74,.38);border:3px solid #FFD84A;border-radius:6px;mix-blend-mode:normal}
.seat{position:absolute;width:150px;height:150px;border-radius:50%;border:6px solid #F4F1E8;background:#16213A;text-align:center;font:400 40px/1 Bangers;padding-top:30px}
.seat b{display:block;font-size:56px;color:#FFD84A}
.opt{position:absolute;left:40px;right:40px;height:250px;border:6px solid #F4F1E8;border-radius:18px;background:#16213A}
.opt .l{position:absolute;left:24px;top:22px;font:400 200px/1 Bangers;color:#FFD84A}
.opt .t{position:absolute;left:175px;right:20px;top:50%;transform:translateY(-50%);font:400 66px/0.95 Bangers;color:#F4F1E8}
.full{position:absolute;left:0;top:0;width:744px;height:1040px}
"""
def card(n, x, y, w, rot=0): return f'<img class="card" src="{u(n)}" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg)">'
CR = '© Wizards of the Coast. Conteúdo de fã não oficial.'
FEL = 'Felidar Sovereign (Foundations Jumpstart, 2024, nº 198, arte Zoltan Boros & Gabor Szikszai).'
RUL = 'Ruling oficial da Wizards, 25/08/2015 (via Scryfall).'
# frações das linhas de texto medidas no PNG j25/198 (744x1040) a 21/11/2026
SEATS = """<div class="seat" style="left:279px;top:150px">OPON.<b>1</b></div>
   <div class="seat" style="left:60px;top:330px">OPON.<b>2</b></div>
   <div class="seat" style="left:498px;top:330px">OPON.<b>3</b></div>
   <div class="seat" style="left:279px;top:510px;border-color:#FFD84A">VOCÊ<b>40</b></div>"""
TELAS = {
 # fala 1 · B «Esse gato ganha com 40 de vida. E no Commander a gente COMEÇA com 40!» — quadro 0
 's01_quarenta': f"""<div class="f"><span class="badge">O GATO DOS 40</span>
   {card('felidar.png', 26, 100, 372, -2)}
   <div class="lbl" style="left:410px;width:290px;top:170px;font-size:56px">VIDA</div>
   <div class="giant" style="left:400px;right:0;top:230px;font-size:240px">40</div>
   <div class="sub" style="left:410px;right:20px;top:470px;font-size:30px;text-align:center">= vitória na<br>sua manutenção</div>
   <div class="row" style="top:640px;font-size:26px">…if you have <b>40 or more life</b>, you win the game.</div>
   <div class="fonte">{FEL} {CR}</div></div>""",
 # fala 4 · M «Se a vez voltar com 40 ou mais. A mesa inteira joga antes.»
 's04_mesa': f"""<div class="f"><span class="badge">UMA VOLTA</span>
   <svg class="full" viewBox="0 0 744 1040"><circle cx="354" cy="420" r="230" fill="none" stroke="#FFD84A" stroke-width="8" stroke-dasharray="26 18"/>
   <path d="M600 470 l22 -40 l22 40 z" fill="#FFD84A" transform="rotate(180 622 450)"/></svg>
   {SEATS}
   <div class="big" style="top:720px;font-size:72px">A MESA <em>INTEIRA</em><br>JOGA ANTES</div>
   <div class="fonte">Exemplo de mesa de 4 jogadores. Vida inicial 40: Regras Completas, 903.7. {CR}</div></div>""",
 # fala 6 · M «Não. Ele confere quando a manutenção começa. Com 38, nem dispara.» — linhas destacadas (tvtext)
 's06_ruling': f"""<div class="f"><span class="badge">LÊ A RULING</span>
   {card('felidar.png', 520, 30, 170, 4)}
   <div class="sub" style="top:150px;left:30px;right:230px;text-align:left;font-size:30px">Felidar Sovereign<br><em>ruling oficial · 25/08/2015</em></div>
   <div class="row" style="top:440px;font-size:25px">…checks to see if you have 40 or more life</div>
   <div class="row" style="top:518px"><b>as your upkeep begins.</b></div>
   <div class="row" style="top:596px;font-size:26px"><b>If you don't, the ability won't trigger at all.</b></div>
   <div class="sub" style="top:700px;font-size:32px">Confere quando a manutenção <em>começa</em>.<br>Sem 40, <em>nem dispara</em>.</div>
   <div class="fonte">{RUL} {CR}</div></div>""",
 # fala 7 · B «Tá. Mas disparou? Já era.»
 's07_gatilho': f"""<div class="f"><span class="badge">GATILHO NA PILHA</span>
   {card('felidar.png', 172, 110, 400, 0)}
   <div class="stamp" style="left:120px;top:690px;font-size:58px;color:#6FE39A;border-color:#6FE39A;transform:rotate(-3deg)">VIDA 40 · DISPAROU</div>
   <div class="fonte">{FEL} {CR}</div></div>""",
 # fala 8 · M «Confere de novo ao resolver. Cravado em 40? Um ponto em resposta e acabou.» — linhas destacadas (tvtext)
 's08_ruling2': f"""<div class="f"><span class="badge">LÊ A RULING</span>
   {card('felidar.png', 520, 30, 170, 4)}
   <div class="sub" style="top:150px;left:30px;right:230px;text-align:left;font-size:30px">Felidar Sovereign<br><em>ruling oficial · 25/08/2015</em></div>
   <div class="row" style="top:440px"><b>If you do, the ability will check again</b></div>
   <div class="row" style="top:518px"><b>as it tries to resolve.</b></div>
   <div class="row" style="top:596px;font-size:26px">If you don't have 40 or more life at that time,</div>
   <div class="row" style="top:674px">the ability won't do anything.</div>
   <div class="sub" style="top:770px;font-size:32px">Confere <em>de novo</em> ao resolver.</div>
   <div class="fonte">{RUL} {CR}</div></div>""",
 # fala 12 · M «Ou some com o gato. Se não: manutenção, 40… vitória.» — pagamento do gancho
 's12_vitoria': f"""<div class="f"><span class="badge">SUA MANUTENÇÃO</span>
   {card('felidar.png', 222, 100, 300, 0)}
   <div class="big" style="top:530px;font-size:76px">VIDA <em>40</em></div>
   <div class="sub" style="top:650px;font-size:40px">ninguém te bateu.<br>gatilho resolve com <em>40</em>…</div>
   <div class="fonte">Se ninguém tirar o Felidar nem baixar sua vida. {CR}</div></div>""",
 # ---- inserts nos grandes planos do Burn (cuB) ----
 # fala 3 · B «Baixo no turno seis, ganho no sete!»
 'i03_turno': f"""<div class="f"><span class="badge">O PLANO DO BURN</span>
   {card('felidar.png', 232, 110, 280, -3)}
   <div class="giant" style="top:530px;font-size:170px">T6 → T7</div>
   <div class="sub" style="top:720px">6 manas no turno 6,<br>vitória no turno 7?</div>
   <div class="fonte">Um terreno por turno, sem aceleração. {FEL} {CR}</div></div>""",
 # fala 5 · B «Meu comandante, Oloro, me dá 2 na manutenção: 38 vira 40 e ganho na hora!»
 'i05_oloro': f"""<div class="f"><span class="badge">O PLANO DO BURN</span>
   {card('oloro.png', 172, 90, 400, 0)}
   <div class="hlbox" style="left:186px;top:441px;width:372px;height:40px"></div>
   <div class="giant" style="top:640px;font-size:170px">38 → 40</div>
   <div class="fonte">Oloro, Ageless Ascetic (Commander 2013, nº 203, arte Eric Deschamps). {CR}</div></div>""",
 # fala 9 · B «UM PONTO?! Esse gato é inútil!»
 'i09_um': f"""<div class="f"><span class="badge">EM RESPOSTA</span>
   <div class="giant" style="top:90px;font-size:420px">1</div>
   <div class="big" style="top:480px">PONTO DE<br><em>DANO</em></div>
   <div class="sub" style="top:690px">cravado em 40 → 39<br>o gatilho não faz nada</div>
   <div class="fonte">{RUL} {CR}</div></div>""",
 # fala 11 · B «A mesa inteira tem que me bater… ou perde pra um gato?!»
 'i11_mesa': f"""<div class="f"><span class="badge">TV SAL · PLACAR</span>
   <svg class="full" viewBox="0 0 744 1040"><g stroke="#FF5A4E" stroke-width="10" fill="#FF5A4E">
   <line x1="354" y1="300" x2="354" y2="490"/><path d="M332 480 l22 34 l22 -34 z"/>
   <line x1="200" y1="430" x2="300" y2="540"/><path d="M282 548 l36 12 l-6 -38 z"/>
   <line x1="510" y1="430" x2="410" y2="540"/><path d="M428 548 l-36 12 l6 -38 z"/></g></svg>
   {SEATS}
   <div class="big" style="top:700px;font-size:70px">JOGADORES PUTOS<br><em>3 DE 3</em></div>
   <div class="fonte">Para parar o Felidar: baixar sua vida, tirar o gato da mesa ou 1 ponto em resposta (cravado em 40). {CR}</div></div>""",
 # fala 13 · B pergunta A/B
 's13_ab': f"""<div class="f"><span class="badge">E VOCÊ?</span>
   {card('felidar.png', 540, 30, 140, 5)}
   <div class="opt" style="top:330px"><span class="l">A</span><span class="t">BATO NO DONO DO GATO</span></div>
   <div class="opt" style="top:620px"><span class="l">B</span><span class="t">TIRO O GATO DA MESA</span></div>
   <div class="fonte">{FEL} {CR}</div></div>""",
}
# variantes «a meio da fala» (EP.canais[].meio): a mesma tela com um elemento novo, sem tapar as linhas destacadas
def _var(base, velho, novo):
    assert velho in TELAS[base], base
    return TELAS[base].replace(velho, novo)
TELAS['s01_quarenta_b'] = _var('s01_quarenta', '<div class="row" style="top:640px;font-size:26px">',
    '<div class="row" style="top:560px;border-color:#FFD84A">REGRA 903.7 · <b>todos começam com 40</b></div>'
    '<div class="stamp" style="left:250px;top:740px;transform:rotate(-4deg)">= VITÓRIA?</div><div class="row" style="top:640px;font-size:26px">')
TELAS['s12_vitoria_b'] = _var('s12_vitoria', '<div class="sub" style="top:650px;font-size:40px">ninguém te bateu.<br>gatilho resolve com <em>40</em>…</div>',
    '<div class="giant" style="top:615px;font-size:130px">VOCÊ<br>VENCEU</div>')
TELAS['s04_mesa_b'] = _var('s04_mesa', '<div class="big" style="top:720px',
    '<div class="stamp" style="left:400px;top:40px;font-size:52px;transform:rotate(6deg)">40 OU MAIS?</div><div class="big" style="top:720px')
TELAS['s06_ruling_b'] = _var('s06_ruling', '<div class="sub" style="top:700px',
    '<div class="stamp" style="left:60px;top:300px;transform:rotate(-3deg)">38 = NEM DISPARA</div><div class="sub" style="top:700px')
TELAS['s08_ruling2_b'] = _var('s08_ruling2', '<div class="sub" style="top:770px',
    '<div class="stamp" style="left:60px;top:300px;transform:rotate(-3deg)">40 → 39 · ACABOU</div><div class="sub" style="top:770px')
TELAS['i05_oloro_b'] = _var('i05_oloro', '<div class="giant" style="top:640px;font-size:170px">38 → 40</div>',
    '<div class="giant" style="top:640px;font-size:170px">38 → 40</div><div class="stamp" style="left:420px;top:20px;font-size:54px;transform:rotate(6deg)">GANHEI?!</div>')
# a carta inteira, com marcas fora do texto de regras (custo no fala 2; vida ganha no fala 10)
TELAS['c02_custo'] = f"""<img class="full" src="{u('felidar.png')}">
   <div style="position:absolute;left:562px;top:52px;width:138px;height:58px;border:6px solid #FFD84A;border-radius:30px"></div>
   <div class="stamp" style="left:520px;top:130px;font-size:54px;color:#FFD84A;border-color:#FFD84A;transform:rotate(6deg)">= 6</div>"""
TELAS['c10_vida'] = f"""<img class="full" src="{u('felidar.png')}">
   <div class="stamp" style="left:470px;top:470px;font-size:54px;color:#6FE39A;border-color:#6FE39A;transform:rotate(-4deg)">40 → 44</div>"""

def main():
    kw = {'executable_path': os.environ['CHROME']} if os.environ.get('CHROME') else {}
    shutil.copy(SRC / 'felidar.png', ROOT / 'cards' / 'felidar.png'); shutil.copy(SRC / 'oloro.png', ROOT / 'cards' / 'oloro.png')
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
