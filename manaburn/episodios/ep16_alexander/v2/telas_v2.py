"""MB-EP16 v2 (22/11/2026) · painéis do plano de prova e da TV SAL. Mesmo CSS e fontes da v1 (Bangers + Geist).
Hierarquia de 3 níveis por painel: informação principal (Bangers), explicação (Geist), fonte (Geist pequeno).
Só cartas reais (PNG do Scryfall em cards/src/: alexander = trc/81, swords = trc/429). Números de mesa marcados «exemplo».
Uso, na pasta do kit:  CHROME=/usr/bin/google-chrome python3 telas_v2.py   → cards/t*.png (744x1040)"""
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
CSS += """
.lv1{position:absolute;left:30px;right:30px;text-align:center;font:400 96px/0.95 Bangers;color:#FFD84A;letter-spacing:1px;text-shadow:0 0 24px rgba(255,216,74,.35)}
.lv2{position:absolute;left:40px;right:40px;text-align:center;font:700 34px/1.22 Geist;color:#F4F1E8}
.lv2 em{font-style:normal;color:#FFD84A}
.ex{position:absolute;right:30px;top:30px;z-index:3;background:#F4F1E8;color:#0F172A;font:700 24px/1 Geist;letter-spacing:2px;padding:8px 14px;border-radius:6px}
.st{position:absolute;width:156px;height:156px;border-radius:50%;border:6px solid #F4F1E8;background:#16213A;text-align:center;font:700 24px/1.1 Geist;padding-top:34px;color:#F4F1E8}
.st b{display:block;font:400 40px/1 Bangers;color:#6FE39A;margin-top:6px;letter-spacing:1px}
.st.dono{border-color:#FFD84A}.st.alvo{border-color:#FF5A4E;border-style:dashed}
"""
def card(n, x, y, w, rot=0, extra=''): return f'<img class="card" src="{u(n)}" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);{extra}">'
CR = '© Wizards of the Coast. Conteúdo de fã não oficial.'
POS = {'top': (294, 90), 'esq': (70, 270), 'dir': (518, 270), 'dono': (294, 450)}
def st(k, nome, val, cls=''):
    x, y = POS[k]; return f'<div class="st {cls}" style="left:{x}px;top:{y}px">{nome}<b>{val}</b></div>'
TELAS = {
 # fala 1 (TV, depois da abertura): os quatro participantes do exemplo; um oponente aleatório leva o dano
 't01_mesa': f"""<div class="f"><span class="ex">EXEMPLO · MESA DE 4</span>
   {st('top','OPON.','+1')}{st('esq','OPON.','+1')}{st('dir','OPON.','+1')}{st('dono','DONO','+1','dono')}
   <div class="lv1" style="top:650px">4 COMPRAM</div>
   <div class="lv2" style="top:750px">e <em>1 oponente aleatório</em><br>leva o dano</div>
   <div class="fonte">Alexander, Ship's Fool (TRC 81). Cada jogador compra 1 carta. {CR}</div></div>""",
 # fala 4 (prova, 2.ª metade): X = maior valor de mana revelado → um oponente sorteado
 't04_dano': f"""<div class="f"><span class="ex">EXEMPLO</span>
   {st('top','OPON.','VALOR 2')}{st('esq','OPON.','VALOR 1')}{st('dir','OPON.','VALOR 3')}{st('dono','DONO','VALOR 5','dono')}
   
   <div class="lv1" style="top:650px">5 DE DANO</div>
   <div class="lv2" style="top:750px">num <em>oponente aleatório</em>,<br>não escolhido</div>
   <div class="fonte">Exemplo de mesa de 4. X = maior valor de mana entre as cartas reveladas (Oracle TRC 81). {CR}</div></div>""",
 # fala 6 (prova): a ruling oficial, com a ressalva destacada
 't06_ruling': f"""<div class="f">
   <div class="lv2" style="top:60px;font-size:30px;color:#C9C3B2">RULING OFICIAL · 07/10/2026</div>
   <div class="row" style="top:150px;font-size:31px;border-color:#FFD84A;background:#2A2410"><b>Except in some very unusual cases,</b></div>
   <div class="row" style="top:228px;font-size:31px">the card each player reveals</div>
   <div class="row" style="top:306px;font-size:31px">is the one they'll draw.</div>
   <div class="lv1" style="top:455px;font-size:108px">REVELADA<br>= COMPRADA</div>
   <div class="lv2" style="top:690px">exceto em <em>casos muito raros</em>,<br>a carta revelada é a que<br>cada jogador compra</div>
   <div class="fonte">Ruling de Alexander, Ship's Fool, Wizards, 07/10/2026 (via Scryfall). {CR}</div></div>""",
 # fala 6 (prova, 2.ª metade): a mesa inteira vê a carta revelada (Swords to Plowshares como exemplo)
 't06_mesa': f"""<div class="f"><span class="ex">EXEMPLO</span>
   <svg class="full" viewBox="0 0 744 1040"><g stroke="#FFD84A" stroke-width="7" stroke-dasharray="16 12" fill="none">
   <line x1="372" y1="250" x2="372" y2="290"/><line x1="230" y1="380" x2="280" y2="400"/><line x1="514" y1="380" x2="464" y2="400"/></g></svg>
   {st('top','OPON.','VIU')}{st('esq','OPON.','VIU')}{st('dir','DONO','VIU','dono')}
   {card('swords.png', 287, 280, 170)}
   <div class="lv1" style="top:640px;font-size:88px">A MESA<br>INTEIRA VÊ</div>
   <div class="lv2" style="top:830px">a remoção que <em>você</em> comprou</div>
   <div class="fonte">Exemplo de carta revelada: Swords to Plowshares (TRC 429, arte Pablo Mendoza). {CR}</div></div>""",
 # fala 10 (prova, 2.ª metade): desvirar → ativar de novo (a carta real, virada e desvirada)
 't10_desvira': f"""<div class="f">
   <div class="lv2" style="top:56px;font-size:30px;color:#C9C3B2">CUSTO DA HABILIDADE: VIRAR</div>
   {card('alexander.png', 80, 190, 230, 90, 'transform-origin:50% 50%;opacity:.55')}
   <svg class="full" viewBox="0 0 744 1040"><path d="M405 330 C 430 300, 460 300, 485 330" stroke="#6FE39A" stroke-width="10" fill="none"/>
   <path d="M473 312 l30 22 l-34 12 z" fill="#6FE39A"/></svg>
   {card('alexander.png', 505, 170, 200, 0)}
   <div class="lv2" style="top:500px;font-size:28px;left:40px;right:400px;color:#C9C3B2">VIRADO</div>
   <div class="lv2" style="top:480px;font-size:28px;left:480px;right:20px;color:#6FE39A">DESVIRADO</div>
   <div class="lv1" style="top:590px;font-size:92px">ATIVA<br>DE NOVO</div>
   <div class="lv2" style="top:790px">a habilidade <em>não é mágica</em>:<br>Rule of Law não a limita</div>
   <div class="fonte">Alexander, Ship's Fool (TRC 81). Exemplo de efeito de desvirar: Thousand-Year Elixir (C21 271). {CR}</div></div>""",
 # fala 11 (TV): pergunta A/B
 't11_ab': f"""<div class="f"><span class="badge">E VOCÊ?</span>
   <div class="opt" style="top:250px"><span class="l">A</span><span class="t">ENCARO A MESA</span></div>
   <div class="opt" style="top:560px"><span class="l">B</span><span class="t">TROCO DE DECK</span></div>
   <div class="fonte">Alexander, Ship's Fool (TRC 81, arte Javier Charro). {CR}</div></div>""",
}
TELAS['t11_ab_b'] = TELAS['t11_ab'].replace('<div class="fonte">',
    '<div class="lv1" style="top:860px;font-size:64px">COMENTA AÍ</div><div class="fonte" style="display:none">').replace('class="opt"','class="opt" style="border-color:#FFD84A"',0)
def main():
    kw = {'executable_path': os.environ['CHROME']} if os.environ.get('CHROME') else {}
    for n in ('alexander.png', 'rule_of_law.png', 'elixir.png', 'swords.png'):
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
