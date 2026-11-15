"""Giro de domingo 15/11/2026 · uma tela da TV SAL por fala (padrão «feedback visual em cada fala», fundador 15/11/2026 03:08).
Cada tela mostra a coisa de que a personagem está a falar: foto do produto, carta real, capa real do episódio, print real.
Uso, na pasta do kit (precisa de node_modules/ para Bangers e Geist):  python3 telas_visuais.py
Imagens de origem em cards/src/ (cartas do Scryfall, capas e prints reais do repositório).
Fotos que a sessão não consegue descarregar (rede fechada aos sites de notícias) entram por ficheiro, se existirem:
  cards/src/foto_bk.jpg       -> foto oficial da deck box + sleeves do Burger King Itália (crédito: Burger King Itália)
  cards/src/foto_netflix.jpg  -> imagem oficial do primeiro olhar de PLANESWALKER (crédito: Netflix)
Sem elas, a tela sai com a moldura «FOTO EM FALTA» e NÃO é para publicar.
Saída: cards/v01_abre.png … cards/v23_comenta.png (744x1040) e inserts cards/ins_*.png.
"""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent.resolve()
SRC = ROOT / 'cards' / 'src'
def u(nome):
    p = SRC / nome
    return p.as_uri() if p.exists() else None

CSS = """
@font-face{font-family:Bangers;src:url(node_modules/@fontsource/bangers/files/bangers-latin-400-normal.woff2)}
@font-face{font-family:Geist;font-weight:700;src:url(node_modules/geist/dist/fonts/geist-sans/Geist-Bold.woff2)}
@font-face{font-family:Geist;font-weight:500;src:url(node_modules/geist/dist/fonts/geist-sans/Geist-Medium.woff2)}
*{margin:0;padding:0;box-sizing:border-box}
body{width:744px;height:1040px;background:#0F172A;color:#F4F1E8;font-family:Geist;overflow:hidden;position:relative}
.f{position:absolute;inset:18px;border:6px solid #FFD84A;border-radius:18px;overflow:hidden}
.badge{position:absolute;left:30px;top:26px;z-index:3;background:#C8352B;color:#FFD84A;font:400 44px Bangers;letter-spacing:3px;padding:2px 18px;border-radius:6px}
.big{font:400 96px/0.95 Bangers;color:#F4F1E8;letter-spacing:1px}
.big em{font-style:normal;color:#FFD84A}
.giant{font:400 230px/0.9 Bangers;color:#FFD84A;text-shadow:0 0 30px rgba(255,216,74,.45)}
.sub{font:700 34px/1.2 Geist;color:#F4F1E8}
.y{color:#FFD84A}
.fonte{position:absolute;left:28px;right:28px;bottom:20px;font:500 22px/1.25 Geist;color:#C9C3B2;z-index:3}
.foto{position:absolute;left:0;right:0;background:#000 center/cover no-repeat}
.falta{position:absolute;left:30px;right:30px;border:6px dashed #FF5A4E;border-radius:14px;display:flex;align-items:center;justify-content:center;
       text-align:center;font:400 54px/1.05 Bangers;color:#FF5A4E;background:repeating-linear-gradient(45deg,#1b2338 0 22px,#141b2c 22px 44px)}
.card{position:absolute;border-radius:16px;box-shadow:0 14px 0 rgba(0,0,0,.45)}
.stamp{position:absolute;border:8px solid #C8352B;color:#C8352B;background:rgba(244,241,232,.92);font:400 78px/1 Bangers;padding:6px 22px;border-radius:10px;transform:rotate(-9deg)}
.n{position:absolute;width:78px;height:78px;border-radius:50%;background:#FFD84A;color:#0F172A;font:400 64px/78px Bangers;text-align:center;box-shadow:0 6px 0 rgba(0,0,0,.4)}
.thumb{position:absolute;border:5px solid #FFD84A;border-radius:12px;background:#000 center/cover no-repeat}
"""

def foto(nome, top, h, legenda_falta):
    s = u(nome)
    if s:
        return f'<div class="foto" style="top:{top}px;height:{h}px;background-image:url({s})"></div>'
    return f'<div class="falta" style="top:{top+20}px;height:{h-40}px">FOTO EM FALTA<br>{legenda_falta}</div>'

def thumb(nome, x, y, w, h, alt=None):
    s = u(nome) or (u(alt) if alt else None)
    if s:
        return f'<div class="thumb" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background-image:url({s})"></div>'
    return f'<div class="falta" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;right:auto;font-size:34px">FOTO<br>EM FALTA</div>'

def card(nome, x, y, w, rot=0):
    return f'<img class="card" src="{u(nome)}" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg)">'

TELAS = {
  # 1 · B «Giro de domingo… Burger King, Netflix e a semana no BINDER» — quadro 0 com cartas de Magic à vista
  'v01_abre': f"""<div class="f"><span class="badge">TV SAL · GIRO DE DOMINGO</span>
     {card('giro_chandra.png', 40, 170, 300, -6)}{card('giro_numot.png', 380, 150, 300, 5)}
     <div style="position:absolute;left:30px;right:30px;top:600px;font-size:80px" class="big">MAGIC NO<br><em>BURGER KING</em>,<br>NA <em>NETFLIX</em> E NO BINDER</div>
     <div class="fonte">domingo, 15/11/2026 · notícias de 09 a 15/11</div></div>""",
  # 2 · M «O Burger King da Itália lançou lanche de Magic com deck box e cem sleeves»
  'v02_bk': f"""<div class="f"><span class="badge">1 · LANCHE</span>{foto('foto_bk.jpg', 0, 640, 'deck box + sleeves<br>do Burger King Itália')}
     <div style="position:absolute;left:30px;right:30px;top:668px" class="big">DECK BOX<br><em>+ 100 SLEEVES</em></div>
     <div style="position:absolute;left:30px;top:880px" class="sub">no lanche do <span class="y">Burger King Itália</span></div>
     <div class="fonte">Imagem: Burger King Itália. Fontes: Dexerto, ICv2 (10/11/2026).</div></div>""",
  # 4 · M «Dezenove e noventa euros. Só na Itália, até dia 30»
  'v04_preco': f"""<div class="f"><span class="badge">1 · LANCHE</span>{foto('foto_bk.jpg', 0, 430, 'deck box do BK')}
     <div style="position:absolute;left:24px;top:420px" class="giant">€19,90</div>
     <div style="position:absolute;left:30px;top:640px" class="sub">lanche + deck box + 100 sleeves</div>
     <div style="position:absolute;left:30px;right:30px;top:710px" class="big">SÓ NA ITÁLIA<br><em>ATÉ 30/11</em></div>
     <div class="fonte">Fontes: Burger King Itália, via Dexerto e MTG Rocks (10/11/2026).</div></div>""",
  # 6 · M «O Rosewater disse: se der certo, pode expandir. Nada decidido»
  'v06_rosewater': f"""<div class="f"><span class="badge">1 · E O BRASIL?</span>{thumb('foto_bk.jpg', 30, 130, 330, 240)}
     <div style="position:absolute;left:390px;top:150px;width:300px" class="sub">Mark Rosewater,<br>designer-chefe de Magic, no blog dele (Blogatog)</div>
     <div style="position:absolute;left:30px;right:30px;top:440px" class="big">SE DER CERTO,<br><em>PODE EXPANDIR</em></div>
     <div class="stamp" style="left:120px;top:720px">NADA DECIDIDO</div>
     <div class="fonte">Paráfrase. Fonte: Blogatog, via MTG Rocks (11/11/2026).</div></div>""",
  # 7 · B «Dois! Série de Magic na Netflix: PLANESWALKER, em 2027»
  'v07_netflix': f"""<div class="f"><span class="badge">2 · STREAMING</span>{foto('foto_netflix.jpg', 0, 600, 'primeiro olhar<br>de PLANESWALKER (Netflix)')}
     <div style="position:absolute;left:30px;right:30px;top:625px" class="big">PLANES-<br><em>WALKER</em></div>
     <div style="position:absolute;left:30px;top:830px" class="sub">série animada · Netflix · <span class="y">2027</span></div>
     <div class="fonte">Imagem: Netflix. Fontes: Netflix Tudum, Deadline (13/11/2026).</div></div>""",
  # 12 · M «A semana no BINDER. O Burn sofreu com o Numot» — capa real do EP11
  'v12_numot_ep': f"""<div class="f"><span class="badge">A SEMANA NO BINDER</span>
     <img src="{u('mb_ep11_capa_34.jpg')}" style="position:absolute;left:84px;top:110px;width:564px">
     <div style="position:absolute;left:30px;right:30px;top:870px" class="sub">no perfil: <span class="y">Mana &amp; Burn EP11</span></div>
     <div class="fonte">Capa do episódio. Numot, the Devastator (Commander 2011). Arte: Dan Dos Santos. © Wizards of the Coast.</div></div>""",
  # 16 · M «Parecer: obra notável. Só errou de mitologia» — carta real do réu + carimbo
  'v16_lemure': f"""<div class="f"><span class="badge">A SEMANA · CONDE</span>
     {card('lemure.png', 132, 110, 480, 0)}
     <div class="stamp" style="left:150px;top:640px">OBRA NOTÁVEL</div>
     <div class="fonte">Hyalopterous Lemure (Ice Age, 1995), nº 133. Arte: Richard Thomas. © Wizards of the Coast.</div></div>""",
  # 17 · B «O TUBO fez o Mundial e dois especiais de Precon»
  'v17_tubo': f"""<div class="f"><span class="badge">A SEMANA · TUBO</span>
     <img src="{u('tubo.jpg')}" style="position:absolute;left:-20px;top:100px;width:420px">
     <div style="position:absolute;left:380px;top:170px;width:320px" class="big"><span style="font-size:150px">3</span><br><em style="font-size:66px">EPISÓDIOS</em></div>
     <div style="position:absolute;left:30px;right:30px;top:690px" class="sub">· Mundial: seis brasileiros<br>· Especial: Precon em dupla<br>· Especial: <span class="y">A Taça respondeu</span></div>
     <div class="fonte">Meta em Curto, com o TUBO (BINDER Originals).</div></div>""",
  # 18 · M «Na Taça Preconauta, quem começou o jogo um venceu 66%» — print real do comentário
  'v18_taca': f"""<div class="f"><span class="badge">A SEMANA · TUBO</span>
     <img src="{u('preconautamtg_taca.png')}" style="position:absolute;left:30px;top:120px;width:670px;border-radius:14px">
     <div style="position:absolute;left:40px;top:330px" class="giant">66%</div>
     <div style="position:absolute;left:30px;right:30px;top:560px" class="big">QUEM COMEÇA<br><em>O JOGO 1 VENCE</em></div>
     <div class="fonte">Dados da Taça Preconauta 2x2 (@preconautamtg), no Meta em Curto ESP02.</div></div>""",
  # 19 · B «E teve spoiler de Nauctis!»
  'v19_nauctis': f"""<div class="f"><span class="badge">A SEMANA · EXPEDIÇÃO</span>
     {card('mentor.png', 60, 120, 330, -5)}{card('lotus.png', 360, 170, 330, 6)}
     <div style="position:absolute;left:30px;right:30px;top:650px" class="big">NAUCTIS:<br><em>THE SUNKEN REALM</em></div>
     <div class="fonte">Calmwater Mentor (NAU 5, arte Danny Schwartz) e Abyssal Lotus (NAU 234, arte Sarah Finnigan). © Wizards of the Coast.</div></div>""",
  # 20 · M «No fundo daquele oceano tem um Lotus»
  'v20_lotus': f"""<div class="f"><span class="badge">A SEMANA · EXPEDIÇÃO</span>
     {card('lotus.png', 102, 100, 540, 0)}
     <div class="fonte">Abyssal Lotus (Nauctis: The Sunken Realm), nº 234. Arte: Sarah Finnigan. © Wizards of the Coast.</div></div>""",
  # 21 · B «Três! O Mundial termina hoje. O TUBO cravou Jund Sacrifice no Top 8!»
  'v21_jund': f"""<div class="f"><span class="badge">3 · MUNDIAL 32</span>
     {card('biotech_specialist.png', 40, 120, 320, -5)}{card('the_sackvillebagginses.png', 380, 140, 320, 5)}
     <div style="position:absolute;left:30px;right:30px;top:600px" class="big">PREVISÃO DO TUBO:<br><em>JUND SACRIFICE</em><br>NO TOP 8</div>
     <div class="fonte">Biotech Specialist (Edge of Eternities 214, arte Alexandre Honoré); The Sackville-Bagginses (The Hobbit 83, arte Denman Rooke). © Wizards of the Coast.</div></div>""",
  # 22 · M «Sem spoiler. Amanhã ele presta contas»
  'v22_contas': f"""<div class="f"><span class="badge">3 · MUNDIAL 32</span>
     <img src="{u('tubo.jpg')}" style="position:absolute;left:150px;top:90px;width:440px">
     <div style="position:absolute;left:30px;right:30px;top:640px" class="big">SEGUNDA, <em>16/11</em><br>PRESTAÇÃO<br>DE CONTAS</div>
     <div class="fonte">Meta em Curto · previsão registrada no EP07 (certeza 3 de 5).</div></div>""",
  # 23 · B «Comenta 1, 2 ou 3: qual a notícia da semana?»
  'v23_comenta': f"""<div class="f"><span class="badge">COMENTA 1, 2 OU 3</span>
     {thumb('foto_bk.jpg', 40, 120, 300, 260)}<div class="n" style="left:20px;top:100px">1</div>
     {thumb('foto_netflix.jpg', 404, 120, 300, 260, 'giro_chandra.png')}<div class="n" style="left:384px;top:100px">2</div>
     {card('biotech_specialist.png', 230, 430, 280, 0)}<div class="n" style="left:200px;top:410px">3</div>
     <div style="position:absolute;left:30px;top:850px" class="sub">1 lanche · 2 série · 3 Mundial</div></div>""",
  # inserts (aparecem ao lado das personagens nos grandes planos)
  'ins_bk': f"""<div class="f" style="inset:0;border-radius:0">{foto('foto_bk.jpg', 0, 1040, 'deck box BK')}</div>""",
  'ins_brasil': """<div class="f" style="inset:0;border-radius:0;padding:60px 40px">
     <div class="big" style="font-size:150px">ITÁLIA<br><em>SIM</em></div>
     <div class="big" style="font-size:150px;margin-top:60px;color:#FF5A4E">BRASIL<br>NÃO</div>
     <div class="sub" style="margin-top:40px">(por enquanto)</div></div>""",
}

def main():
    out = ROOT / 'cards'; out.mkdir(exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 744, 'height': 1040})
        for nome, corpo in TELAS.items():
            html = ROOT / f'_{nome}.html'
            html.write_text(f'<!doctype html><meta charset="utf-8"><style>{CSS}</style><body>{corpo}</body>', encoding='utf-8')
            pg.goto(html.as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400)
            pg.screenshot(path=str(out / f'{nome}.png')); html.unlink()
            print('ok', nome)
        b.close()

if __name__ == '__main__':
    main()
