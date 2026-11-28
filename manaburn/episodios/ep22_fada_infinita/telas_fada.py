"""MB-EP22 (28/11/2026) · telas da TV SAL e painéis do plano de prova. CSS e fontes do MB-EP21 (Bangers + Geist), sem alterações.
Só cartas reais (PNG do Scryfall em cards/src/: twin = mm2/129, Modern Masters 2015, arte Goran Josic; pestermite = j25/343,
Foundations Jumpstart 2024, arte Christopher Moeller). Números de mesa marcados «EXEMPLO». Oracle, ruling e anúncio da Wizards
citados com data (28/11/2026).
Uso, na pasta do kit:  python3 telas_fada.py   → cards/t*.png (744x1040)  [CHROME=<caminho> opcional]"""
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
CSS += """
.step{position:absolute;left:40px;right:40px;height:150px;border:6px solid #F4F1E8;border-radius:18px;background:#16213A}
.step .n{position:absolute;left:22px;top:12px;font:400 120px/1 Bangers;color:#FFD84A}
.step .t{position:absolute;left:120px;right:20px;top:50%;transform:translateY(-50%);font:700 32px/1.2 Geist;color:#F4F1E8}
.step .t em{font-style:normal;color:#FFD84A}
.tok{position:absolute;width:96px;border-radius:8px;box-shadow:0 6px 0 rgba(0,0,0,.45)}
"""
def card(n, x, y, w, rot=0, extra=''): return f'<img class="card" src="{u(n)}" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);{extra}">'
CR = '© Wizards of the Coast. Conteúdo de fã não oficial.'
TWIN = 'Splinter Twin (MM2 129, arte Goran Josic)'
PEST = 'Pestermite (J25 343, arte Christopher Moeller)'
def enxame(n, x0, y0, cols, dx, dy):
    return ''.join(f'<img class="tok" src="{u("pestermite.png")}" style="left:{x0 + (i % cols) * dx}px;top:{y0 + (i // cols) * dy}px;transform:rotate({(i * 7) % 11 - 5}deg)">' for i in range(n))
def mesa(v, t1, t2):
    def s(n, x):
        ko = ' ko' if x == '0' else ''
        return f'<div class="seat{ko}" style="left:{36 + (n - 1) * 222}px;top:90px">OPON. {n}<b>{x}</b></div>'
    return f"""<div class="f"><span class="ex">EXEMPLO · MESA DE 4</span>
   {s(1, v)}{s(2, v)}{s(3, v)}
   <div class="lv2" style="top:300px;font-size:26px;color:#C9C3B2">vida no Commander</div>
   {enxame(12, 60, 330, 6, 104, 145)}
   <div class="lv1" style="top:635px;font-size:90px">{t1}</div>
   <div class="lv2" style="top:735px;font-size:30px">{t2}</div>
   <div class="fonte">Fichas 2/1 com voar e ímpeto; mesa sem bloqueadores voadores. {CR}</div></div>"""
# v2 (28/11/2026, pedido do fundador: «melhorar a hierarquia visual»): 3 níveis no máximo (título Bangers gigante,
# uma linha de apoio, fonte curta); menos texto; cartas e números maiores; o crédito completo fica só na tarja do topo.
FT = lambda t: f'<div class="fonte" style="font-size:22px;color:#8F8A7C">{t}</div>'
def big(t, top, size=150, color='#FFD84A'): return f'<div class="lv1" style="top:{top}px;font-size:{size}px;color:{color}">{t}</div>'
def sub(t, top, size=40): return f'<div class="lv2" style="top:{top}px;font-size:{size}px">{t}</div>'
def toks(n, x0, y0, cols, dx, dy, w=150):
    return ''.join(f'<img class="tok" src="{u("pestermite.png")}" style="width:{w}px;left:{x0 + (i % cols) * dx}px;top:{y0 + (i // cols) * dy}px;transform:rotate({(i * 7) % 11 - 5}deg)">' for i in range(n))
def mesa(v, t1, t2):
    def s(n, x):
        ko = ' ko' if x == '0' else ''
        return f'<div class="seat{ko}" style="left:{30 + (n - 1) * 226}px;top:80px;width:206px;height:206px;padding-top:30px">OPON. {n}<b style="font-size:84px">{x}</b></div>'
    return f"""<div class="f"><span class="ex">EXEMPLO</span>
   {s(1, v)}{s(2, v)}{s(3, v)}
   {toks(5, 40, 330, 5, 132, 0, 124) if v != '0' else ''}
   {big(t1, 540 if v != '0' else 420, 120 if len(t1) < 12 else 96, '#FFD84A' if v != '0' else '#FF5A4E')}
   {sub(t2, 700 if v != '0' else 600, 42)}
   {FT('Mesa de 4 no Commander, sem voadores para bloquear.')}</div>"""
TELAS = {
 't00_combo': f"""<div class="f">
   {card('pestermite.png', 30, 70, 320, -3)}{card('twin.png', 370, 70, 320, 3)}
   {big('2 CARTAS', 580, 160)}
   {big('TURNO 4', 740, 150, '#FF5A4E')}</div>""",
 't04_turnos': f"""<div class="f">
   {card('pestermite.png', 40, 60, 310)}{card('twin.png', 390, 60, 310)}
   <div class="lv1" style="top:520px;left:20px;right:370px;font-size:110px">T3</div>
   <div class="lv1" style="top:520px;left:370px;right:20px;font-size:110px">T4</div>
   <div class="lv2" style="top:640px;left:20px;right:370px;font-size:44px">3 manas</div>
   <div class="lv2" style="top:640px;left:370px;right:20px;font-size:44px">4 manas</div>
   {big('SEM RAMP', 770, 110, '#6FE39A')}
   {FT('Custos no Oracle (Scryfall, 28/11/2026).')}</div>""",
 't06_loop': f"""<div class="f"><span class="badge">O LOOP</span>
   <div class="step" style="top:120px;height:180px"><span class="n" style="top:22px">1</span><span class="t" style="font:400 66px/1 Bangers">VIRA → FICHA</span></div>
   <div class="step" style="top:330px;height:180px"><span class="n" style="top:22px">2</span><span class="t" style="font:400 66px/1 Bangers">A FICHA ENTRA</span></div>
   <div class="step" style="top:540px;height:180px"><span class="n" style="top:22px">3</span><span class="t" style="font:400 66px/1 Bangers;color:#FFD84A">DESVIRA A ORIGINAL</span></div>
   {big('REPETE', 770, 130, '#FF5A4E')}
   {FT('Commander Spellbook, combo 2905-4702 (28/11/2026).')}</div>""",
 't08_ruling': f"""<div class="f"><span class="badge">RULING</span>
   {big('NÃO COPIA<br>A AURA', 170, 150)}
   <div class="quote" style="top:540px;font-size:40px;line-height:1.25;color:#F4F1E8">“It doesn’t copy the ability granted to the enchanted creature by <span style="color:#FFD84A">Splinter Twin</span>.”</div>
   {FT('Ruling de 15/06/2010 (Scryfall).')}</div>""",
 't08_conta': f"""<div class="f"><span class="ex">EXEMPLO</span>
   {card('pestermite.png', 232, 60, 280)}
   {big('1, 2, 3…', 470, 150)}
   {toks(5, 40, 660, 5, 132, 0, 128)}
   {sub('uma fada <em>por volta</em>', 880, 44)}</div>""",
 't09_mesa': mesa('40', '60 FADAS', '× 2 de dano = <em>120</em> = 3 × 40'),
 't10_ban': f"""<div class="f"><span class="badge">MODERN</span>
   {card('twin.png', 30, 90, 320, 0, 'filter:grayscale(.85) brightness(.7)')}
   <div class="stamp" style="left:40px;top:300px;transform:rotate(-10deg);font-size:58px">BANIDA 2016</div>
   {card('twin.png', 394, 90, 320)}
   <div class="stamp" style="left:420px;top:300px;transform:rotate(8deg);color:#6FE39A;border-color:#6FE39A;font-size:58px">LIBERADA</div>
   {big('16/12/2024', 590, 130)}
   {sub('anúncio oficial da Wizards', 735, 40)}
   {FT('Banned and Restricted Announcement, 16/12/2024.')}</div>""",
 't10_quote': f"""<div class="f"><span class="badge">WIZARDS</span>
   {big('«AGORA ESTÁ<br>LIVRE»', 170, 118)}
   <div class="quote" style="top:520px;font-size:40px;line-height:1.25;color:#F4F1E8">“…an era of Modern that people look back on fondly, <span style="color:#FFD84A">and it is now free.</span>”</div>
   {FT('Banned and Restricted Announcement, 16/12/2024.')}</div>""",
 't12_resp': f"""<div class="f"><span class="ex">EM RESPOSTA</span>
   {card('pestermite.png', 172, 60, 400, 0, 'filter:grayscale(.85) brightness(.7)')}
   <div class="stamp" style="left:170px;top:250px;transform:rotate(-10deg);font-size:78px">DESTRUÍDA</div>
   {big('1 FICHA E PARA', 640, 110)}
   {sub('sem a original, nada <em>desvira</em>', 770, 40)}
   {FT('Ruling de 15/06/2010 (Scryfall).')}</div>""",
 't13_ab': f"""<div class="f"><span class="badge">NO MODERN</span>
   <div class="opt" style="top:150px;height:300px"><span class="l" style="top:40px">A</span><span class="t" style="font-size:86px">BANE DE NOVO</span></div>
   <div class="opt" style="top:500px;height:300px"><span class="l" style="top:40px">B</span><span class="t" style="font-size:86px">DEIXA SOLTA</span></div></div>""",
}
TELAS['t09_mesa_b'] = mesa('0', 'MESA A ZERO', 'num ataque só, <em>no turno 4</em>')
TELAS['t13_ab_b'] = TELAS['t13_ab'][:-6] + big('COMENTA AÍ', 850, 90) + '</div>'
def main():
    kw = {'executable_path': os.environ['CHROME']} if os.environ.get('CHROME') else {}
    for n in ('twin.png', 'pestermite.png'):
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
