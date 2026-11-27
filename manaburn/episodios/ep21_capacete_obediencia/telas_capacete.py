"""MB-EP21 (27/11/2026) · telas da TV SAL e painéis do plano de prova. CSS e fontes do MB-EP19 (Bangers + Geist), sem alterações.
Só cartas reais (PNG do Scryfall em cards/src/: helm = all/121, Alliances 1996, arte Brian Snõddy; rip = big/4, arte Grady Frederick)
e a capa real do MB-EP19 (episódio da casa). Números de mesa marcados «EXEMPLO». Oracle e ruling citados do Scryfall (27/11/2026).
Uso, na pasta do kit:  CHROME=/usr/bin/google-chrome python3 telas_capacete.py   → cards/t*.png (744x1040)"""
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
.giant{position:absolute;left:0;right:0;text-align:center;font:400 190px/0.9 Bangers;color:#FFD84A;text-shadow:0 0 30px rgba(255,216,74,.45)}
.fonte{position:absolute;left:28px;right:28px;bottom:22px;font:500 24px/1.25 Geist;color:#C9C3B2;z-index:3}
.card{position:absolute;border-radius:12px;box-shadow:0 12px 0 rgba(0,0,0,.45)}
.stamp{position:absolute;font:400 64px/1 Bangers;color:#FF5A4E;border:6px solid #FF5A4E;border-radius:10px;padding:4px 16px;background:rgba(15,23,42,.86);letter-spacing:2px;white-space:nowrap;z-index:4}
.opt{position:absolute;left:40px;right:40px;height:250px;border:6px solid #F4F1E8;border-radius:18px;background:#16213A}
.opt .l{position:absolute;left:24px;top:22px;font:400 200px/1 Bangers;color:#FFD84A}
.opt .t{position:absolute;left:175px;right:20px;top:50%;transform:translateY(-50%);font:400 66px/0.95 Bangers;color:#F4F1E8}
.lv1{position:absolute;left:30px;right:30px;text-align:center;font:400 96px/0.95 Bangers;color:#FFD84A;letter-spacing:1px;text-shadow:0 0 24px rgba(255,216,74,.35)}
.lv2{position:absolute;left:40px;right:40px;text-align:center;font:700 34px/1.22 Geist;color:#F4F1E8}
.lv2 em{font-style:normal;color:#FFD84A}
.ex{position:absolute;right:30px;top:30px;z-index:3;background:#F4F1E8;color:#0F172A;font:700 24px/1 Geist;letter-spacing:2px;padding:8px 14px;border-radius:6px}
.pile{position:absolute;width:190px;height:250px;border-radius:14px;border:6px solid #F4F1E8;background:#16213A;text-align:center;font:700 26px/1.1 Geist;padding-top:26px;color:#F4F1E8}
.pile b{display:block;font:400 104px/1 Bangers;color:#FFD84A;margin-top:12px}
.pile.ko{border-color:#FF5A4E}.pile.ko b{color:#FF5A4E}
.pile.ex2{border-color:#6FE39A}.pile.ex2 b{color:#6FE39A}
.arr{position:absolute;font:400 80px/1 Bangers;color:#FFD84A}
.seat{position:absolute;width:190px;height:190px;border-radius:50%;border:6px solid #F4F1E8;background:#16213A;text-align:center;font:700 24px/1.1 Geist;padding-top:34px;color:#F4F1E8}
.seat b{display:block;font:400 64px/1 Bangers;color:#FFD84A;margin-top:8px}
.seat.ko{border-color:#FF5A4E}.seat.ko b{color:#FF5A4E}
.quote{position:absolute;left:50px;right:50px;font:700 30px/1.25 Geist;color:#C9C3B2;text-align:left}
"""
def card(n, x, y, w, rot=0, extra=''): return f'<img class="card" src="{u(n)}" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);{extra}">'
CR = '© Wizards of the Coast. Conteúdo de fã não oficial.'
HELM = 'Helm of Obedience (ALL 121, arte Brian Snõddy)'
RIP = 'Rest in Peace (BIG 4, arte Grady Frederick)'
def grimorio(n, cls, t1, t2, rip=True):
    return f"""<div class="f"><span class="ex">EXEMPLO</span>
   {card('helm.png', 40, 90, 250)}{card('rip.png', 40, 450, 250) if rip else ''}
   <div class="pile {cls}" style="left:330px;top:120px">GRIMÓRIO<b>{n}</b></div>
   <div class="arr" style="left:540px;top:190px">→</div>
   <div class="lv2" style="top:150px;left:590px;right:30px;font-size:28px;text-align:left">{'EXÍLIO' if rip else 'CEMITÉRIO'}</div>
   <div class="lv1" style="top:470px;left:320px;right:30px;font-size:88px">{t1}</div>
   <div class="lv2" style="top:680px;left:320px;right:30px;font-size:30px">{t2}</div>
   <div class="fonte">{HELM} · {RIP}. Grimório de exemplo. {CR}</div></div>"""
def mesa(v1, v2, v3, t1, t2):
    def s(n, v):
        ko = ' ko' if v == '0' else ''
        return f'<div class="seat{ko}" style="left:{36 + (n - 1) * 222}px;top:90px">OPON. {n}<b>{v}</b></div>'
    return f"""<div class="f"><span class="ex">EXEMPLO · MESA DE 4</span>
   {s(1, v1)}{s(2, v2)}{s(3, v3)}
   <div class="lv2" style="top:300px;font-size:26px;color:#C9C3B2">cartas no grimório</div>
   {card('helm.png', 60, 370, 230)}
   <div class="lv1" style="top:400px;left:310px;right:20px;font-size:{86 if len(t1) < 16 else 70}px">{t1}</div>
   <div class="lv2" style="top:610px;left:310px;right:20px;font-size:30px">{t2}</div>
   <div class="fonte">{HELM}. «Target opponent» e custo de virar: um oponente por ativação. {CR}</div></div>"""
TELAS = {
 # fala 1 (TV, depois da abertura): uma mana, grimório inteiro
 't00_capacete': f"""<div class="f">
   {card('helm.png', 30, 130, 300)}
   <div class="lv2" style="top:130px;left:345px;right:15px;font-size:40px">PAGA</div>
   <div class="lv1" style="top:180px;left:345px;right:15px;font-size:110px">1 MANA</div>
   <div class="lv2" style="top:300px;left:345px;right:15px;font-size:36px">e some o</div>
   <div class="lv1" style="top:350px;left:345px;right:15px;font-size:72px">GRIMÓRIO<br>INTEIRO</div>
   <div class="giant" style="top:560px;left:345px;right:15px;font-size:180px">?!</div>
   <div class="fonte">Helm of Obedience (Alliances, 1996, nº 121). Arte: Brian Snõddy. {CR}</div></div>""",
 # fala 2 (prova, a meio): Oracle atual do Helm (a carta de 1996 tem texto antigo)
 't02_oracle': f"""<div class="f"><span class="badge">ORACLE ATUAL</span>
   {card('helm.png', 470, 40, 240)}
   <div class="lv1" style="top:350px;font-size:80px">PARA QUANDO<br>X CARTAS CHEGAM</div>
   <div class="quote" style="top:560px">“Target opponent mills a card, then repeats this process until a creature card or <span style="color:#FFD84A">X cards have been put into their graveyard</span> this way, whichever comes first.”</div>
   <div class="fonte">Oracle no Scryfall, consultado a 27/11/2026. {HELM}. {CR}</div></div>""",
 # fala 7 (TV): callback ao MB-EP19, a mesma Rest in Peace
 't07_ep19': f"""<div class="f"><span class="badge">NO EP. 19</span>
   <img src="{u('ep19_capa.png')}" style="position:absolute;left:30px;top:100px;width:340px;border-radius:12px;box-shadow:0 12px 0 rgba(0,0,0,.45)">
   {card('rip.png', 400, 140, 290)}
   <div class="lv1" style="top:730px;font-size:72px">PAROU O ROBÔ</div>
   <div class="lv2" style="top:820px;font-size:30px">agora é <em>arma</em></div>
   <div class="fonte">Capa do MB-EP19 «O Robô Que Não Morre» (BINDER). {RIP}. {CR}</div></div>""",
 # fala 8 (prova): a ruling oficial
 't08_ruling': f"""<div class="f"><span class="badge">RULING</span>
   {card('helm.png', 470, 40, 240)}
   <div class="lv1" style="top:340px;font-size:86px">NUNCA PARA</div>
   <div class="quote" style="top:450px">“If an effect like that of Leyline of the Void prevents cards from being put into your opponent’s graveyard, the process […] will never stop. <span style="color:#FFD84A">Your opponent’s entire library will be exiled, even if X is 1.</span>”</div>
   <div class="lv2" style="top:770px">grimório <em>inteiro</em>, mesmo com <em>X = 1</em></div>
   <div class="fonte">Ruling de 01/10/2008 (Scryfall, consultada a 27/11/2026). {HELM}. {CR}</div></div>""",
 't08a': grimorio('60', '', 'MÓI 1…', 'vai pro <em>exílio</em>, não chega ao cemitério:<br><em>continua</em>'),
 't08b': grimorio('0', 'ko', 'MÓI TUDO', 'nenhuma chegou ao cemitério:<br>o capacete <em>nunca parou</em>'),
 # fala 10 (prova): grimório vazio não é derrota imediata
 't10_regra': f"""<div class="f"><span class="badge">REGRA 704.5b</span>
   <div class="pile ko" style="left:60px;top:120px">GRIMÓRIO<b>0</b></div>
   <div class="lv1" style="top:150px;left:290px;right:30px;font-size:78px">AINDA<br>NÃO PERDEU</div>
   <div class="lv2" style="top:420px;font-size:36px">perde quando <em>tentar comprar</em><br>com o grimório vazio</div>
   <div class="quote" style="top:580px">“If a player attempted to draw a card from a library with no cards in it since the last time state-based actions were checked, that player loses the game.”</div>
   <div class="fonte">Regras Completas, 704.5b. Na maioria das mesas, na próxima etapa de compra dele. {CR}</div></div>""",
 # fala 12 (prova): um oponente por vez + resposta da mesa
 't12_mesa': mesa('0', '60', '60', 'UM POR<br>VEZ', 'o capacete <em>vira</em> pra ativar:<br>uma ativação por volta,<br><em>três voltas</em> na mesa de 4'),
 't12_resp': f"""<div class="f"><span class="ex">EM RESPOSTA</span>
   {card('rip.png', 40, 110, 300, 0, 'filter:grayscale(.85) brightness(.7)')}{card('helm.png', 404, 110, 300)}
   <div class="stamp" style="left:60px;top:220px;transform:rotate(-10deg)">DESTRUÍDA</div>
   <div class="lv1" style="top:580px;font-size:96px">MÓI 1 E PARA</div>
   <div class="lv2" style="top:700px">sem <em>Rest in Peace</em>, a primeira carta<br>chega ao cemitério: X = 1 cumprido</div>
   <div class="fonte">{RIP} · {HELM}. {CR}</div></div>""",
 # fala 13 (TV): pergunta A/B de conta
 't13_ab': f"""<div class="f"><span class="badge">SEM REST IN PEACE</span>
   <div class="lv2" style="top:118px;font-size:32px">X = 3. A <em>primeira</em> carta moída<br>é uma <em>criatura</em>. Quantas ele mói?</div>
   <div class="opt" style="top:250px"><span class="l">A</span><span class="t">UMA</span></div>
   <div class="opt" style="top:560px"><span class="l">B</span><span class="t">TRÊS</span></div>
   <div class="fonte">{HELM}. {CR}</div></div>""",
}
TELAS['t12_mesa_b'] = mesa('0', '0', '0', 'MESA SEM<br>GRIMÓRIO', 'cada um perde<br>na <em>próxima compra</em>')
TELAS['t13_ab_b'] = TELAS['t13_ab'].replace('<div class="fonte">',
    '<div class="lv1" style="top:860px;font-size:64px">COMENTA AÍ</div><div class="fonte" style="display:none">')
def main():
    kw = {'executable_path': os.environ['CHROME']} if os.environ.get('CHROME') else {}
    for n in ('helm.png', 'rip.png'):
        shutil.copy(SRC / n, ROOT / 'cards' / n)
    with sync_playwright() as p:
        b = p.chromium.launch(**kw); pg = b.new_page(viewport={'width': 744, 'height': 1040})
        for nome, html in TELAS.items():
            tmp = ROOT / '_tela.html'
            tmp.write_text(f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{html}</body></html>', encoding='utf-8')
            pg.goto(tmp.as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
            pg.screenshot(path=str(ROOT / 'cards' / f'{nome}.png')); print('ok', nome)
        b.close(); (ROOT / '_tela.html').unlink(missing_ok=True)
if __name__ == '__main__': main()
