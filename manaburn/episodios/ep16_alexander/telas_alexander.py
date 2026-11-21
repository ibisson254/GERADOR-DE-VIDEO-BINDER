"""MB-EP16 · Alexander, Ship's Fool · telas da TV SAL e inserts (feedback visual em cada fala, decisão de 15/11/2026).
Estilo e CSS iguais a episodios/ep15_felidar/telas_felidar.py. Só cartas reais (PNG do Scryfall em cards/src/, 21/11/2026:
alexander.png = trc/81, rule_of_law.png = m20/35, elixir.png = c21/271, swords.png = trc/429) e o texto oficial da ruling
do Alexander (Wizards, 07/10/2026, via Scryfall). Números de mesa marcados como «exemplo».
Uso, na pasta do kit (com cards/src/ copiado):  CHROME=/usr/bin/google-chrome python3 telas_alexander.py
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
ALX = "Alexander, Ship's Fool (Star Trek Commander, 2026, nº 81, arte Javier Charro)."
RUL = 'Ruling oficial da Wizards, 07/10/2026 (via Scryfall).'
ROL = 'Rule of Law (Core Set 2020, nº 35, arte Scott M. Fischer).'
ELX = 'Thousand-Year Elixir (Commander 2021, nº 271, arte Richard Sardinha).'
STP = 'Swords to Plowshares (Star Trek Commander, 2026, nº 429, arte Pablo Mendoza).'
def seats(vals, nomes=('OPON. 1', 'OPON. 2', 'DONO', 'VOCÊ'), hi=None):
    pos = [(279, 150), (60, 330), (498, 330), (279, 510)]
    out = ''
    for i, ((x, y), n, v) in enumerate(zip(pos, nomes, vals)):
        cor = '#FFD84A' if i == hi else '#F4F1E8'
        out += f'<div class="seat" style="left:{x}px;top:{y}px;border-color:{cor};font-size:30px">{n}<b>{v}</b></div>'
    return out
TELAS = {
 # fala 1 · B «Esse comandante dá carta pra QUATRO. E um oponente apanha no sorteio!» — quadro 0 na TV
 's01_quatro': f"""<div class="f"><span class="badge">TODO MUNDO COMPRA</span>
   {card('alexander.png', 26, 100, 372, -2)}
   <div class="giant" style="left:400px;right:0;top:150px;font-size:300px">4</div>
   <div class="lbl" style="left:400px;width:320px;top:420px;font-size:58px">COMPRAM</div>
   <div class="sub" style="left:410px;right:20px;top:500px;font-size:28px">numa mesa de 4</div>
   <div class="row" style="top:660px;font-size:23px">…each player reveals the top card… <b>then draws.</b></div>
   <div class="fonte">{ALX} {CR}</div></div>""",
 # fala 2 · M — a carta inteira com marca fora do texto (variante «meio»)
 'c02_compra': f"""<img class="full" src="{u('alexander.png')}">
   <div class="stamp" style="left:70px;top:480px;font-size:50px;color:#6FE39A;border-color:#6FE39A;transform:rotate(-4deg)">+1 PRA CADA</div>""",
 # fala 4 · M — maior custo vira dano (variante «meio»)
 'c04_dano': f"""<img class="full" src="{u('alexander.png')}">
   <div class="stamp" style="left:60px;top:470px;font-size:46px;transform:rotate(-3deg)">MAIOR CUSTO = DANO</div>
   <div class="stamp" style="left:440px;top:380px;font-size:42px;color:#FFD84A;border-color:#FFD84A;transform:rotate(5deg)">ALVO? SORTEIO</div>""",
 # fala 6 · M «Lê a ruling. A carta que você revela é a que você compra. A mesa viu tudo.» (tvtext)
 's06_ruling': f"""<div class="f"><span class="badge">LÊ A RULING</span>
   {card('alexander.png', 520, 30, 170, 4)}
   <div class="sub" style="top:150px;left:30px;right:230px;text-align:left;font-size:30px">Alexander, Ship's Fool<br><em>ruling oficial · 07/10/2026</em></div>
   <div class="row" style="top:440px;font-size:26px">Except in some very unusual cases,</div>
   <div class="row" style="top:518px"><b>the card each player reveals</b></div>
   <div class="row" style="top:596px"><b>is the one they'll draw.</b></div>
   <div class="sub" style="top:700px;font-size:32px">A carta revelada é <em>a que você compra</em>.<br>A mesa inteira <em>vê</em>.</div>
   <div class="fonte">{RUL} {CR}</div></div>""",
 # fala 8 · M «E todo mundo sabe. Inclusive o dono do Alexander.»
 's08_mesa': f"""<div class="f"><span class="badge">MÃO ABERTA</span>
   <svg class="full" viewBox="0 0 744 1040"><g stroke="#FFD84A" stroke-width="8" stroke-dasharray="18 12" fill="none">
   <line x1="354" y1="300" x2="354" y2="505"/><line x1="200" y1="430" x2="300" y2="530"/><line x1="510" y1="430" x2="410" y2="530"/></g></svg>
   {seats(['VIU', 'VIU', 'VIU', '!'], hi=3)}
   {card('swords.png', 470, 500, 140, 6)}
   <div class="big" style="top:760px;font-size:66px">TODO MUNDO <em>SABE</em><br>O QUE VOCÊ COMPROU</div>
   <div class="fonte">Exemplo de mesa de 4. {STP} {CR}</div></div>""",
 # fala 10 · M — Rule of Law com marca (variante «meio»)
 'c10_uma': f"""<img class="full" src="{u('rule_of_law.png')}">
   <div class="stamp" style="left:330px;top:510px;font-size:50px;transform:rotate(-3deg)">1 POR TURNO</div>""",
 # fala 12 · M — Elixir com marca (variante «meio»)
 'c12_denovo': f"""<img class="full" src="{u('elixir.png')}">
   <div class="stamp" style="left:330px;top:125px;font-size:40px;color:#FFD84A;border-color:#FFD84A;transform:rotate(3deg)">HABILIDADE ≠ MÁGICA</div>
   <div class="stamp" style="left:300px;top:500px;font-size:40px;transform:rotate(-3deg)">DESVIRA · BATE DE NOVO</div>""",
 # ---- inserts nos grandes planos do Burn (cuB) ----
 # fala 3 · B «Carta de graça pra mesa toda? Isso é deck ou instituição de caridade?!»
 'i03_caridade': f"""<div class="f"><span class="badge">O BURN ACHA</span>
   {card('alexander.png', 232, 90, 280, -3)}
   <div class="giant" style="top:520px;font-size:150px">4 × +1</div>
   <div class="big" style="top:690px;font-size:72px">GROUP <em>HUG</em>?</div>
   <div class="fonte">Cada jogador compra uma carta a cada ativação. {ALX} {CR}</div></div>""",
 # fala 5 · B «Eu ganho carta e posso nem apanhar? Tô dentro!»
 'i05_sorteio': f"""<div class="f"><span class="badge">SORTEIO</span>
   {seats(['?', '?', 'ALEX.', '?'], hi=3)}
   <div class="giant" style="top:690px;font-size:140px">2 EM 3</div>
   <div class="sub" style="top:830px;font-size:30px">vezes, o dano <em>não é em você</em></div>
   <div class="fonte">Exemplo de mesa de 4: dano num dos 3 oponentes, ao acaso. {CR}</div></div>""",
 # fala 7 · B «E daí? Eu comprei uma remoção!»
 'i07_swords': f"""<div class="f"><span class="badge">A COMPRA DO BURN</span>
   {card('swords.png', 172, 90, 400, 0)}
   <div class="stamp" style="left:90px;top:680px;font-size:56px;transform:rotate(-3deg)">REVELADA = COMPRADA</div>
   <div class="fonte">Exemplo. {STP} {CR}</div></div>""",
 # fala 9 · B «Então eu jogo ela agora!»
 'i09_agora': f"""<div class="f"><span class="badge">O PLANO DO BURN</span>
   {card('swords.png', 222, 90, 300, 4)}
   <div class="giant" style="top:560px;font-size:170px">AGORA!</div>
   <div class="fonte">Exemplo. {STP} {CR}</div></div>""",
 # fala 11 · B «UMA?! Ou eu tiro o Alexander, ou faço a minha jogada?!»
 'i11_uma': f"""<div class="f"><span class="badge">1 MÁGICA</span>
   <div class="opt" style="top:150px"><span class="l">1</span><span class="t">TIRO O ALEXANDER</span></div>
   <div class="giant" style="top:440px;font-size:110px">OU</div>
   <div class="opt" style="top:580px"><span class="l">2</span><span class="t">FAÇO A MINHA JOGADA</span></div>
   <div class="fonte">Com Rule of Law na mesa: uma mágica por turno, por jogador. {ROL} {CR}</div></div>""",
 # fala 13 · B pergunta A/B
 's13_ab': f"""<div class="f"><span class="badge">E VOCÊ?</span>
   {card('alexander.png', 540, 30, 140, 5)}
   <div class="opt" style="top:330px"><span class="l">A</span><span class="t">ENCARO A MESA</span></div>
   <div class="opt" style="top:620px"><span class="l">B</span><span class="t">TROCO DE DECK</span></div>
   <div class="fonte">{ALX} {CR}</div></div>""",
}
def _var(base, velho, novo):
    assert velho in TELAS[base], base
    return TELAS[base].replace(velho, novo)
TELAS['s01_quatro_b'] = _var('s01_quatro', '<div class="row" style="top:660px',
    '<div class="stamp" style="left:300px;top:760px;transform:rotate(-4deg)">1 APANHA</div><div class="row" style="top:660px')
TELAS['s06_ruling_b'] = _var('s06_ruling', '<div class="sub" style="top:700px',
    '<div class="stamp" style="left:60px;top:300px;transform:rotate(-3deg)">A MESA VIU</div><div class="sub" style="top:700px')
TELAS['i05_sorteio_b'] = _var('i05_sorteio', '<div class="giant" style="top:690px',
    '<div class="stamp" style="left:400px;top:40px;font-size:52px;transform:rotate(6deg)">TÔ DENTRO!</div><div class="giant" style="top:700px')

def main():
    kw = {'executable_path': os.environ['CHROME']} if os.environ.get('CHROME') else {}
    for n in ('alexander.png', 'rule_of_law.png', 'elixir.png', 'swords.png'):
        shutil.copy(SRC / n, ROOT / 'cards' / n)
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
