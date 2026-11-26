"""MB-EP18 (26/11/2026) · telas da TV SAL e painéis do plano de prova. CSS e fontes do MB-EP16 v2 (Bangers + Geist).
Só cartas e fichas reais (PNG do Scryfall em cards/src/: broodscale = mh3/145, rosie = ltr/27, corpse_knight = moc/321,
spawn = tmh3/2, food = tltr/10, swords = trc/429). Números de mesa marcados «EXEMPLO».
Uso, na pasta do kit:  CHROME=/usr/bin/google-chrome python3 telas_lagarto.py   → cards/t*.png (744x1040)"""
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
CSS += """
.cnt{position:absolute;z-index:5;background:#1E7A3C;color:#F4F1E8;border:5px solid #050A10;border-radius:50%;width:104px;height:104px;text-align:center;font:400 50px/94px Bangers;letter-spacing:1px;box-shadow:0 6px 0 rgba(0,0,0,.45)}
.arr{position:absolute;font:700 26px/1.1 Geist;color:#FFD84A;text-align:center}
.life{position:absolute;width:190px;height:190px;border-radius:50%;border:6px solid #F4F1E8;background:#16213A;text-align:center;font:700 24px/1.1 Geist;padding-top:34px;color:#F4F1E8}
.life b{display:block;font:400 84px/1 Bangers;color:#FFD84A;margin-top:6px}
.life.ko{border-color:#FF5A4E}.life.ko b{color:#FF5A4E}
"""
SP = lambda x, y, w=110: card('spawn.png', x, y, w)
def ciclo(n, t1, t2, inf=False):
    sp = ''.join(SP(40 + i * 62, 520 + (i % 2) * 12) for i in range(n))
    return f"""<div class="f"><span class="ex">O CICLO</span>
   {card('broodscale.png', 36, 80, 270)}{card('rosie.png', 438, 80, 270)}
   <div class="cnt" style="left:200px;top:120px">{'∞' if inf else '+' + str(n)}</div>
   <svg class="full" viewBox="0 0 744 1040"><g fill="none" stroke="#FFD84A" stroke-width="9">
     <path d="M428 210 C 400 190, 350 190, 322 210"/><path d="M420 600 C 520 640, 600 560, 590 470"/></g>
     <path d="M330 196 l-24 24 l34 4 z" fill="#FFD84A"/><path d="M574 482 l18 -26 l16 30 z" fill="#FFD84A"/></svg>
   <div class="arr" style="left:300px;top:230px;width:144px">MARCADOR<br>+1/+1</div>
   <div class="arr" style="left:440px;top:640px;width:280px;font-size:24px">FICHA CRIADA:<br>ROSIE DE NOVO</div>
   {sp}
   <div class="lv1" style="top:745px;font-size:70px">{t1}</div>
   <div class="lv2" style="top:830px">{t2}</div>
   <div class="fonte">Rosie Cotton of South Lane (LTR 27) · Basking Broodscale (MH3 145) · ficha Eldrazi Spawn (MH3). {CR}</div></div>"""
def vida(v, ko=False):
    c = ' ko' if ko else ''
    return f"""<div class="f"><span class="ex">EXEMPLO · MESA DE 4</span>
   <div class="life{c}" style="left:40px;top:90px">OPON. 1<b>{v}</b></div>
   <div class="life{c}" style="left:277px;top:90px">OPON. 2<b>{v}</b></div>
   <div class="life{c}" style="left:514px;top:90px">OPON. 3<b>{v}</b></div>
   {card('corpse_knight.png', 60, 330, 230)}
   <div class="lv1" style="top:360px;left:300px;right:20px;font-size:92px">{'MESA<br>DERROTADA' if ko else '40 SPAWNS'}</div>
   <div class="lv2" style="top:560px;left:300px;right:20px;font-size:30px">{'40 entradas = 40 de vida<br>de <em>cada</em> oponente' if ko else 'cada um entra:<br><em>cada oponente −1</em>'}</div>
   <div class="lv2" style="top:720px;font-size:30px;color:#C9C3B2">Commander começa com 40 de vida (regra 903.7).<br>Sem resposta da mesa.</div>
   <div class="fonte">Corpse Knight (MOC 321, arte Karl Kopinski). Exemplo com 3 oponentes a 40. {CR}</div></div>"""
TELAS = {
 # fala 1 (TV, depois da abertura): o lagarto de duas manas e a promessa
 't00_lagarto': f"""<div class="f">
   {card('broodscale.png', 40, 120, 330)}
   <div class="lv2" style="top:150px;left:390px;right:20px;font-size:40px">CUSTA</div>
   <div class="lv1" style="top:200px;left:390px;right:20px;font-size:120px">2 MANAS</div>
   <div class="giant" style="top:430px;left:390px;right:20px;font-size:260px">∞</div>
   <div class="lv2" style="top:690px;left:390px;right:20px">fichas <em>com</em><br>outra carta</div>
   <div class="fonte">Basking Broodscale (Modern Horizons 3, 2024), nº 145. Arte: Caio Monteiro. {CR}</div></div>""",
 't05a': ciclo(1, '1 MARCADOR = 1 SPAWN', 'o lagarto <em>pode</em> criar a ficha'),
 't05b': ciclo(2, 'SPAWN É FICHA', 'a Rosie dispara <em>de novo</em>'),
 't05c': ciclo(5, 'E DE NOVO…', 'até <em>você</em> decidir parar', True),
 't10_vida': vida(40),
 't10_vida_b': vida(0, True),
 # fala 12 (prova): remoção em resposta corta o ciclo
 't11_resposta': f"""<div class="f"><span class="ex">EXEMPLO</span>
   {card('swords.png', 40, 110, 300)}{card('broodscale.png', 404, 110, 300, 0, 'filter:grayscale(.85) brightness(.7)')}
   <div class="stamp" style="left:420px;top:200px;transform:rotate(-10deg)">EXILADO</div>
   <div class="lv1" style="top:580px;font-size:110px">CICLO PARA</div>
   <div class="lv2" style="top:720px">remoção no lagarto <em>em resposta</em>:<br>a Rosie não tem mais onde pôr marcador</div>
   <div class="fonte">Exemplo de remoção: Swords to Plowshares (TRC 429, arte Pablo Mendoza). Basking Broodscale (MH3 145). {CR}</div></div>""",
 # fala 13 (TV): pergunta A/B
 't12_ab': f"""<div class="f"><span class="badge">E VOCÊ?</span>
   <div class="opt" style="top:250px"><span class="l">A</span><span class="t">MATA O LAGARTO</span></div>
   <div class="opt" style="top:560px"><span class="l">B</span><span class="t">MATA O CAVALEIRO</span></div>
   <div class="fonte">Basking Broodscale (MH3 145) · Corpse Knight (MOC 321). {CR}</div></div>""",
}
TELAS['t12_ab_b'] = TELAS['t12_ab'].replace('<div class="fonte">',
    '<div class="lv1" style="top:860px;font-size:64px">COMENTA AÍ</div><div class="fonte" style="display:none">')
def main():
    kw = {'executable_path': os.environ['CHROME']} if os.environ.get('CHROME') else {}
    for n in ('broodscale.png', 'rosie.png', 'corpse_knight.png', 'spawn.png', 'food.png', 'swords.png'):
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
