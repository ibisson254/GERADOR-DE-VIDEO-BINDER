"""MB-EP19 (26/11/2026) · telas da TV SAL e painéis do plano de prova. CSS e fontes do MB-EP18 (Bangers + Geist), sem alterações.
Só cartas reais (PNG do Scryfall em cards/src/: mikaeus = cmm/173, triskelion = moc/387 redimensionada a 744x1040, rip = big/4).
Números de mesa marcados «EXEMPLO». Ruling citada do Scryfall (07/12/2018).
Uso, na pasta do kit:  CHROME=/usr/bin/google-chrome python3 telas_robo.py   → cards/t*.png (744x1040)"""
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
TRI = 'Triskelion (MOC 387, arte Christopher Moeller)'
MIK = 'Mikaeus, the Unhallowed (CMM 173, arte Chris Rahn)'
def loop(cnt, t1, t2, alvo='', dead=False):
    flt = 'filter:grayscale(.85) brightness(.7)' if dead else ''
    return f"""<div class="f"><span class="ex">O LOOP</span>
   {card('triskelion.png', 40, 90, 330, 0, flt)}
   <div class="cnt" style="left:300px;top:110px;{'background:#C8352B' if dead else ''}">{cnt}</div>
   {card('mikaeus.png', 470, 120, 230)}
   <div class="arr" style="left:450px;top:440px;width:270px">MIKAEUS: +1/+1<br>E UNDYING</div>
   {alvo}
   <div class="lv1" style="top:620px;font-size:76px">{t1}</div>
   <div class="lv2" style="top:720px">{t2}</div>
   <div class="fonte">{TRI} · {MIK}. Bolinha = marcadores +1/+1. {CR}</div></div>"""
def vida(v, ko=False):
    c = ' ko' if ko else ''
    return f"""<div class="f"><span class="ex">EXEMPLO · MESA DE 4</span>
   <div class="life{c}" style="left:40px;top:90px">OPON. 1<b>{v}</b></div>
   <div class="life{c}" style="left:277px;top:90px">OPON. 2<b>{v}</b></div>
   <div class="life{c}" style="left:514px;top:90px">OPON. 3<b>{v}</b></div>
   {card('triskelion.png', 60, 330, 230)}
   <div class="lv1" style="top:360px;left:300px;right:20px;font-size:{88 if ko else 96}px">{'MESA<br>ZERADA' if ko else '2 POR<br>VOLTA'}</div>
   <div class="lv2" style="top:570px;left:300px;right:20px;font-size:30px">{'120 de dano<br><em>≈ 60 voltas</em>' if ko else 'sem gastar<br><em>nenhuma mana</em>'}</div>
   <div class="lv2" style="top:720px;font-size:30px;color:#C9C3B2">Commander começa com 40 de vida (regra 903.7).<br>Sem resposta da mesa.</div>
   <div class="fonte">{TRI}. Exemplo com 3 oponentes a 40. {CR}</div></div>"""
TELAS = {
 # fala 1 (TV, depois da abertura): o robô que atira em si mesmo
 't00_robo': f"""<div class="f">
   {card('triskelion.png', 40, 120, 330)}
   <div class="lv2" style="top:150px;left:390px;right:20px;font-size:40px">ATIRA</div>
   <div class="lv1" style="top:200px;left:390px;right:20px;font-size:116px">2 VEZES<br>NELE</div>
   <div class="giant" style="top:470px;left:390px;right:20px;font-size:240px">∞</div>
   <div class="lv2" style="top:720px;left:390px;right:20px">volta <em>com</em><br>o Mikaeus</div>
   <div class="fonte">{TRI.replace('MOC 387', 'March of the Machine Commander, 2023, nº 387')}. {CR}</div></div>""",
 # fala 6 (prova): a ruling do Mikaeus
 't05_ruling': f"""<div class="f"><span class="badge">RULING</span>
   {card('mikaeus.png', 470, 40, 240)}
   <div class="lv1" style="top:330px;font-size:84px">BÔNUS ≠<br>MARCADOR</div>
   <div class="lv2" style="top:530px;font-size:30px;text-align:left;left:50px;right:50px;color:#C9C3B2">“The +1/+1 bonus that Mikaeus gives to other non-Human creatures you control isn’t a counter. It won’t prevent undying from triggering.”</div>
   <div class="lv2" style="top:740px">o +1/+1 do Mikaeus<br><em>não</em> impede o undying</div>
   <div class="fonte">Ruling de 07/12/2018 (Scryfall, consultada a 26/11/2026). {MIK}. {CR}</div></div>""",
 't09a': loop(4, 'VOLTA COM 4', '3 da carta <em>+ 1</em> do undying'),
 't09c': loop(0, '2 TIROS NELE', 'morre <em>sem</em> marcador: <em>undying</em> → volta com 4',
              '<div class="stamp" style="left:470px;top:515px;font-size:50px;transform:rotate(-6deg)">MORREU</div>', True),
 't10_vida': vida(40),
 't10_vida_b': vida(0, True),
 # fala 12 (prova): Rest in Peace corta o loop
 't11_rip': f"""<div class="f"><span class="ex">EXEMPLO</span>
   {card('rip.png', 40, 110, 300)}{card('triskelion.png', 404, 110, 300, 0, 'filter:grayscale(.85) brightness(.7)')}
   <div class="stamp" style="left:420px;top:200px;transform:rotate(-10deg)">EXILADO</div>
   <div class="lv1" style="top:580px;font-size:104px">NEM MORRE</div>
   <div class="lv2" style="top:700px">com <em>Rest in Peace</em>, não vai pro cemitério:<br>vai pro exílio, <em>sem undying</em></div>
   <div class="fonte">Rest in Peace (BIG 4, arte Grady Frederick). {TRI}. {CR}</div></div>""",
 # fala 13 (TV): pergunta A/B
 't12_ab': f"""<div class="f"><span class="badge">PRIMEIRA VOLTA</span>
   <div class="lv2" style="top:118px;font-size:34px">Triskelion <em>recém-jogado</em>, com 3 marcadores:<br>quanto de dano <em>na mesa</em>?</div>
   <div class="opt" style="top:250px"><span class="l">A</span><span class="t">1 DE DANO</span></div>
   <div class="opt" style="top:560px"><span class="l">B</span><span class="t">2 DE DANO</span></div>
   <div class="fonte">{TRI} · {MIK}. {CR}</div></div>""",
}
TELAS['t12_ab_b'] = TELAS['t12_ab'].replace('<div class="fonte">',
    '<div class="lv1" style="top:860px;font-size:64px">COMENTA AÍ</div><div class="fonte" style="display:none">')
def main():
    kw = {'executable_path': os.environ['CHROME']} if os.environ.get('CHROME') else {}
    for n in ('mikaeus.png', 'triskelion.png', 'rip.png'):
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
