"""MB-EP20 (27/11/2026) · telas da TV SAL e painéis do plano de prova. CSS e fontes do MB-EP18/EP19 (Bangers + Geist), sem alterações.
Só cartas reais (PNG do Scryfall em cards/src/, redimensionadas a 744x1040): monolith = 2xm/232, rings = cmr/335,
ballista = 2xm/306, ulamog = cmm/5. Painéis do ciclo na ordem exata da pilha (Oracle + ruling do Rings de 10/11/2020 +
passo a passo do Commander Spellbook 4131-4235, consultados a 27/11/2026). Números de mesa marcados «EXEMPLO».
Uso, na pasta do kit:  CHROME=/usr/bin/google-chrome python3 telas_monolito.py   → cards/t*.png e cards/p*.png (744x1040)"""
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
.opt .t{position:absolute;left:175px;right:190px;top:50%;transform:translateY(-50%);font:400 60px/0.95 Bangers;color:#F4F1E8}
.lv1{position:absolute;left:30px;right:30px;text-align:center;font:400 96px/0.95 Bangers;color:#FFD84A;letter-spacing:1px;text-shadow:0 0 24px rgba(255,216,74,.35)}
.lv2{position:absolute;left:40px;right:40px;text-align:center;font:700 34px/1.22 Geist;color:#F4F1E8}
.lv2 em{font-style:normal;color:#FFD84A}
.ex{position:absolute;right:30px;top:30px;z-index:3;background:#F4F1E8;color:#0F172A;font:700 24px/1 Geist;letter-spacing:2px;padding:8px 14px;border-radius:6px}
.life{position:absolute;width:190px;height:190px;border-radius:50%;border:6px solid #F4F1E8;background:#16213A;text-align:center;font:700 24px/1.1 Geist;padding-top:34px;color:#F4F1E8}
.life b{display:block;font:400 84px/1 Bangers;color:#FFD84A;margin-top:6px}
.life.ko{border-color:#FF5A4E}.life.ko b{color:#FF5A4E}
/* MB-EP20: pool de mana e pilha */
.step{position:absolute;left:30px;top:26px;z-index:3;background:#C8352B;color:#FFD84A;font:400 40px Bangers;letter-spacing:2px;padding:2px 16px;border-radius:6px}
.pool{position:absolute;left:400px;top:96px;width:290px;height:300px;border:6px solid #F4F1E8;border-radius:18px;background:#16213A;text-align:center}
.pool .t{font:700 26px/1 Geist;letter-spacing:3px;color:#C9C3B2;margin-top:20px}
.pool .n{font:400 190px/1 Bangers;color:#FFD84A;text-shadow:0 0 26px rgba(255,216,74,.4);margin-top:4px}
.delta{position:absolute;left:470px;top:410px;width:150px;text-align:center;font:400 96px/1 Bangers;letter-spacing:1px}
.delta.up{color:#6FE39A}.delta.dn{color:#FF5A4E}.delta.eq{color:#C9C3B2}
.pilha{position:absolute;left:40px;right:40px;top:550px;height:236px;border:4px dashed #9AA3B2;border-radius:14px}
.pilha .h{position:absolute;left:16px;top:-22px;background:#0F172A;padding:0 10px;font:400 34px Bangers;letter-spacing:2px;color:#9AA3B2}
.it{position:absolute;left:20px;right:20px;height:88px;border-radius:12px;border:4px solid #F4F1E8;background:#16213A;font:400 44px/80px Bangers;letter-spacing:1px;padding-left:20px;color:#F4F1E8;white-space:nowrap}
.it small{font:700 22px Geist;color:#C9C3B2;letter-spacing:0;margin-left:12px}
.it.cp{border-color:#FFD84A;color:#FFD84A}.it.hot{border-color:#FF5A4E;box-shadow:0 0 0 6px rgba(255,90,78,.35)}
.it .tag{position:absolute;right:14px;top:18px;font:700 22px/1 Geist;background:#F4F1E8;color:#0F172A;padding:8px 10px;border-radius:6px;letter-spacing:1px}
.vazia{position:absolute;left:0;right:0;top:92px;text-align:center;font:700 30px Geist;color:#9AA3B2}
.mono{position:absolute;left:62px;top:110px;width:250px;transition:none}
.estado{position:absolute;left:20px;top:466px;width:280px;text-align:center;font:400 46px/1 Bangers;letter-spacing:2px}
.rg{position:absolute;left:300px;top:380px;width:120px;border-radius:8px;box-shadow:0 6px 0 rgba(0,0,0,.45)}
.mb{display:inline-block;width:62px;height:62px;border-radius:50%;background:#C9C3B2;color:#0F172A;font:400 50px/62px Bangers;text-align:center;margin:0 6px;box-shadow:inset 0 -5px 0 rgba(0,0,0,.25)}
"""
CR = '© Wizards of the Coast. Conteúdo de fã não oficial.'
MON = 'Basalt Monolith (2XM 232, arte Yeong-Hao Han)'
RIN = 'Rings of Brighthearth (CMR 335, arte Howard Lyon)'
BAL = 'Walking Ballista (2XM 306, arte Daniel Ljunggren)'
ULA = 'Ulamog, the Ceaseless Hunger (CMM 5, arte Michael Komarck)'
def card(n, x, y, w, rot=0, extra=''): return f'<img class="card" src="{u(n)}" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);{extra}">'

def ciclo(passo, titulo, mana, delta, virado, pilha, nota, rings=False, hot=False):
    """Um painel do ciclo: Monolith (virado = rodado 90°), pool de mana, variação e a pilha (topo primeiro)."""
    rot = 'transform:rotate(90deg);top:150px;' if virado else ''
    est = ('<div class="estado" style="color:#FF5A4E">VIRADO</div>' if virado
           else '<div class="estado" style="color:#6FE39A">DESVIRADO</div>')
    if delta is None: d = '<div class="delta eq">±0</div>'
    else: d = f'<div class="delta {"up" if delta > 0 else "dn"}">{"+" if delta > 0 else "−"}{abs(delta)}</div>'
    its = ''
    for k, (nome, sub, cp) in enumerate(pilha):
        tag = '<span class="tag">TOPO</span>' if k == 0 else ''
        cls = 'it' + (' cp' if cp else '') + (' hot' if hot and k == len(pilha) - 1 else '')
        its += f'<div class="{cls}" style="top:{28 + k * 104}px">{nome}<small>{sub}</small>{tag}</div>'
    if not pilha: its = '<div class="vazia">pilha vazia</div>'
    rg = f'<img class="rg" src="{u("rings.png")}">' if rings else ''
    return f"""<div class="f"><span class="step">{passo} · {titulo}</span>
   <img class="card mono" src="{u('monolith.png')}" style="{rot}">{rg}{est}
   <div class="pool"><div class="t">MANA DISPONÍVEL</div><div class="n">{mana}</div></div>{d}
   <div class="pilha"><span class="h">PILHA</span>{its}</div>
   <div class="lv2" style="top:806px;font-size:30px">{nota}</div>
   <div class="fonte" style="font-size:20px">{MON} · {RIN}. Passo a passo: Commander Spellbook 4131-4235. {CR}</div></div>"""

ORIG = ('ORIGINAL: DESVIRAR', 'pagou 3', False)
COPIA = ('CÓPIA (RINGS)', 'pagou 2', True)
def vida(v, ko=False):
    c = ' ko' if ko else ''
    return f"""<div class="f"><span class="ex">EXEMPLO · MESA DE 4</span>
   <div class="life{c}" style="left:40px;top:90px">OPON. 1<b>{v}</b></div>
   <div class="life{c}" style="left:277px;top:90px">OPON. 2<b>{v}</b></div>
   <div class="life{c}" style="left:514px;top:90px">OPON. 3<b>{v}</b></div>
   {card('ballista.png', 60, 330, 230)}
   <div class="lv1" style="top:350px;left:300px;right:20px;font-size:{88 if ko else 70}px">{'MESA<br>ZERADA' if ko else '120<br>MARCADORES'}</div>
   <div class="lv2" style="top:560px;left:300px;right:20px;font-size:30px">{'120 de dano<br><em>40 + 40 + 40</em>' if ko else 'tira 1 =<br><em>1 de dano</em>'}</div>
   <div class="lv2" style="top:720px;font-size:30px;color:#C9C3B2">Commander começa com 40 de vida (regra 903.7).<br>Sem resposta da mesa.</div>
   <div class="fonte">{BAL}. Exemplo com 3 oponentes a 40. {CR}</div></div>"""

TELAS = {
 # fala 1 (TV, depois da abertura): o monólito e o infinito
 't00_monolito': f"""<div class="f">
   {card('monolith.png', 40, 120, 330)}
   <div class="lv2" style="top:150px;left:390px;right:20px;font-size:40px">NÃO DESVIRA</div>
   <div class="lv1" style="top:200px;left:390px;right:20px;font-size:80px">SOZINHO</div>
   <div class="giant" style="top:340px;left:390px;right:20px;font-size:240px">∞</div>
   <div class="lv2" style="top:590px;left:390px;right:20px">mana<br><em>infinita</em></div>
   <div class="fonte">Basalt Monolith (Double Masters, 2020, nº 232). Arte: Yeong-Hao Han. {CR}</div></div>""",
 # ciclo (ordem exata da pilha)
 'p1': ciclo(1, 'VIRA', 5, +3, True, [], 'Tinha <em>2</em> manas. Vira o Monolith: <em>2 + 3 = 5</em>.'),
 'p2': ciclo(2, 'ATIVA O DESVIRAR', 2, -3, True, [ORIG], 'Paga <em>3</em> pra desvirar: vai pra pilha.'),
 'p3': ciclo(3, 'RINGS COPIA', 0, -2, True, [COPIA, ORIG], 'Paga <em>mais 2</em>: o Rings copia o desvirar.', rings=True),
 'p4': ciclo(4, 'A CÓPIA RESOLVE', 0, None, False, [ORIG], 'O topo resolve <em>primeiro</em>: o Monolith desvira.', rings=True),
 'p5': ciclo(5, 'VIRA DE NOVO', 3, +3, True, [ORIG], 'Vira outra vez: <em>+3</em>. A original <em>ainda espera</em>.', rings=True),
 'p5b': ciclo(5, 'VIRA DE NOVO', 3, +3, True, [ORIG], 'A habilidade <em>original</em> ainda está na pilha!', rings=True, hot=True),
 'p6': ciclo(6, 'A ORIGINAL RESOLVE', 3, None, False, [], 'Desvira <em>de novo</em>. Fim do ciclo.', rings=True),
 # fala 8: o saldo
 'p7': f"""<div class="f"><span class="step">7 · SALDO DO CICLO</span>
   <div class="lv2" style="top:110px;font-size:34px">início: <em>2</em> manas · Monolith desvirado</div>
   <div class="lv2" style="top:170px;font-size:34px">fim: <em>3</em> manas · Monolith desvirado</div>
   <div class="giant" style="top:290px;font-size:250px">+1</div>
   <div class="lv1" style="top:530px;font-size:78px">POR CICLO</div>
   <div class="lv2" style="top:650px;font-size:44px"><span style="color:#6FE39A">+3</span> <span style="color:#FF5A4E">−3 −2</span> <span style="color:#6FE39A">+3</span> = <em>+1</em></div>
   <div class="lv2" style="top:740px;font-size:28px;color:#C9C3B2">Mana incolor. Você escolhe quantas vezes repete.</div>
   <div class="fonte">{MON} · {RIN}. Commander Spellbook 4131-4235 (27/11/2026). {CR}</div></div>""",
 # fala 9 (TV): repetir até quanto quiser
 't09_loop': f"""<div class="f"><span class="badge">REPETE</span>
   {card('monolith.png', 40, 120, 250)}{card('rings.png', 60, 470, 210)}
   <div class="lv1" style="top:150px;left:310px;right:20px;font-size:84px">3 → 4 → 5</div>
   <div class="lv1" style="top:250px;left:310px;right:20px;font-size:84px">→ 6 → …</div>
   <div class="giant" style="top:380px;left:310px;right:20px;font-size:230px">∞</div>
   <div class="lv2" style="top:640px;left:310px;right:20px">você escolhe<br><em>quando parar</em></div>
   <div class="fonte">{MON} · {RIN}. O Rings diz «you may pay»: é opcional a cada volta. {CR}</div></div>""",
 # fala 10 (prova): incolor, e mana não ganha jogo
 't10_incolor': f"""<div class="f"><span class="badge">MANA INCOLOR</span>
   <div style="position:absolute;left:0;right:0;top:130px;text-align:center"><span class="mb">◇</span><span class="mb">◇</span><span class="mb">◇</span><span class="mb">◇</span><span class="mb">◇</span><span class="mb">…</span></div>
   <div class="lv1" style="top:250px;font-size:104px">MANA ≠ VITÓRIA</div>
   <div class="life" style="left:40px;top:420px">OPON. 1<b>40</b></div>
   <div class="life" style="left:277px;top:420px">OPON. 2<b>40</b></div>
   <div class="life" style="left:514px;top:420px">OPON. 3<b>40</b></div>
   <div class="lv2" style="top:680px">infinito no seu pool,<br>mesa <em>intacta</em>: falta o finalizador</div>
   <div class="fonte">Exemplo: mesa de 4 a 40 de vida. Mana do Monolith: {{C}} (incolor). {CR}</div></div>""",
 # fala 5 (prova): a ruling do Rings
 't05_ruling': f"""<div class="f"><span class="badge">RULING</span>
   {card('rings.png', 470, 40, 240)}
   <div class="lv1" style="top:330px;font-size:84px">A CÓPIA<br>RESOLVE ANTES</div>
   <div class="lv2" style="top:530px;font-size:30px;text-align:left;left:50px;right:50px;color:#C9C3B2">“The triggered ability of Rings of Brighthearth and the copy it creates both resolve before the ability that caused it to trigger.”</div>
   <div class="lv2" style="top:750px">pilha: o <em>último</em> a entrar<br>é o <em>primeiro</em> a resolver</div>
   <div class="fonte">Ruling de 10/11/2020 (Scryfall, consultada a 27/11/2026). {RIN}. {CR}</div></div>""",
 # fala 12 (prova): a conta do X
 't12_conta': f"""<div class="f"><span class="badge">CUSTO {{X}}{{X}}</span>
   {card('ballista.png', 40, 100, 260)}
   <div class="lv1" style="top:130px;left:320px;right:20px;font-size:96px">X = 120</div>
   <div class="lv2" style="top:250px;left:320px;right:20px;font-size:40px">você paga</div>
   <div class="giant" style="top:300px;left:320px;right:20px;font-size:180px">240</div>
   <div class="lv2" style="top:470px;left:320px;right:20px;font-size:36px">manas<br><em>(2 × X)</em></div>
   <div class="lv2" style="top:640px;font-size:30px;text-align:left;left:50px;right:50px;color:#C9C3B2">“A casting cost of {{X}}{{X}} means that you pay twice X.”</div>
   <div class="lv2" style="top:770px;font-size:28px">com mana infinita, <em>X é o quanto você quiser</em></div>
   <div class="fonte">Ruling de 07/08/2020 (Scryfall, 27/11/2026). {BAL}. {CR}</div></div>""",
 't12_vida': vida(40),
 't12_vida_b': vida(0, True),
 # fala 13 (TV): pergunta A/B
 't13_ab': f"""<div class="f"><span class="badge">E VOCÊ?</span>
   <div class="lv2" style="top:118px;font-size:34px">Com mana <em>infinita</em> na mão,<br>você fecha como?</div>
   <div class="opt" style="top:250px"><span class="l">A</span><span class="t">FECHA COM A BALLISTA</span>{card('ballista.png', 450, 22, 140)}</div>
   <div class="opt" style="top:560px"><span class="l">B</span><span class="t">CONJURA UM ELDRAZI</span>{card('ulamog.png', 450, 22, 140)}</div>
   <div class="fonte">{BAL} · {ULA}. {CR}</div></div>""",
}
TELAS['p7b'] = TELAS['p7'].replace('<div class="lv2" style="top:740px;font-size:28px;color:#C9C3B2">Mana incolor. Você escolhe quantas vezes repete.</div>',
    '<div class="stamp" style="left:150px;top:735px;font-size:56px;transform:rotate(-4deg)">+1 MANA INCOLOR</div>')
assert TELAS['p7b'] != TELAS['p7']
TELAS['t00_monolito_b'] = TELAS['t00_monolito'].replace('<div class="fonte">',
    '<div class="stamp" style="left:400px;top:690px;font-size:50px;transform:rotate(-5deg)">MANA INFINITA</div><div class="fonte">', 1)
TELAS['t10_incolor_b'] = TELAS['t10_incolor'].replace('<div class="fonte">',
    '<div class="stamp" style="left:130px;top:792px;font-size:46px;transform:rotate(-4deg)">SOZINHA NÃO GANHA</div><div class="fonte">', 1)
assert TELAS['t00_monolito_b'] != TELAS['t00_monolito'] and TELAS['t10_incolor_b'] != TELAS['t10_incolor']
TELAS['t13_ab_b'] = TELAS['t13_ab'].replace('<div class="fonte">',
    '<style>.opt{background:#FFD84A;border-color:#050A10}.opt .l{color:#C8352B}.opt .t{color:#050A10}</style>'
    '<div class="lv1" style="top:860px;font-size:64px">COMENTA AÍ</div><div class="fonte" style="display:none">')
def main():
    kw = {'executable_path': os.environ['CHROME']} if os.environ.get('CHROME') else {}
    for n in ('monolith.png', 'rings.png', 'ballista.png', 'ulamog.png'):
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
