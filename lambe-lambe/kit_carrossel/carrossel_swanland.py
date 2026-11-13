"""Carrossel «Artistas de Magic» · Raymond Swanland · 7 slides. python3 -I carrossel_swanland.py <pasta_saida>"""
import sys, os, json, cv2
sys.path.insert(0, '/home/claude/kit')
from motor import *
G = '/home/claude/gal/scry/'; OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
CR = json.load(open('/home/claude/gal/creditos.json'))
def cr(k): c = CR[k]; return f"Arte: {c['name']} ({c['set']}, {c['year']}) · Raymond Swanland · Wizards of the Coast"
FOTO = (cv2.imread(KIT + 'foto_2x.png'), cv2.imread(KIT + 'foto_mask.png', 0))
S = {}

# 01 · CAPA
b = fundo(0); b = selo(b)
b = papel(b, 64, 205, 590, 300, -2.5, 1)
b, ah = impressa(b, arte(G + 'ugin_art.jpg', .025), 530, 478, 880, .4, fitas=((-.62, -1, -10), (.55, -1, 8)))
b = recorte(b, *FOTO, cx=848, topo=40, alt=455, ang=1.5)
b = papel(b, 810, 905, 215, 215, 2.5, 2); b = papel(b, 62, 1000, 330, 120, -3, 1)
b = rodape(b, 1212)
t = ('<div class="e" data-w="520" style="left:100px;top:232px;font-family:AB;font-size:100px;line-height:.95;color:#111;transform:rotate(-2.5deg);transform-origin:left;letter-spacing:-2px;-webkit-text-stroke:2px #111">RAYMOND<br>SWANLAND</div>'
     + traco(110, 457, 480, -2.5, 11)
     + '<div class="e" style="left:917px;top:931px;transform:translateX(-50%) rotate(2.5deg);text-align:center;font-family:BC;font-size:29px;line-height:1;color:#111">EM MAGIC DESDE<br><span style="font-family:AB;font-size:70px;color:#E61E6E;line-height:1.08">2007</span><br>FUTURE SIGHT</div>'
     + '<div class="e" style="left:90px;top:1022px;transform:rotate(-3deg);transform-origin:left;font-family:PF;font-style:italic;font-weight:700;font-size:38px;line-height:1.05;color:#2b2b2b">Feras feitas<br>de tempestade</div>'
     + traco(92, 1082, 250, -3, 5))
S['01_CAPA'] = (b, t, rodape_txt(1212, 'Um mestre do <y>movimento</y>, que faz<br>cada criatura parecer <y>viva</y>.', cr('ugin')))

# 02 · BIOGRAFIA
b = fundo(1); b = selo(b)
b = papel(b, 64, 205, 610, 250, -2, 1, 2)
b = recorte(b, *FOTO, cx=835, topo=48, alt=520, ang=1.2, seed=8)
b, ah = impressa(b, arte(G + 'pact_art.jpg'), 300, 560, 470, -2.5, fitas=((0, -1, -6),), seed=22)
b = papel(b, 70, 560 + ah + 30, 470, 115, -2.5, 2, 3)
b = papel(b, 575, 600, 450, 470, 2, 0, 4)
b = rodape(b, 1212)
t = ('<div class="e" data-w="540" style="left:96px;top:240px;font-family:AB;font-size:66px;line-height:1;color:#111;transform:rotate(-2deg);transform-origin:left;letter-spacing:-1px">QUEM ESTÁ POR<br>TRÁS DA ARTE?</div>'
     + traco(104, 398, 470, -2, 10)
     + f'<div class="e" style="left:96px;top:{560+ah+48}px;transform:rotate(-2.5deg);transform-origin:left;font-family:BC;font-size:30px;line-height:1.08;color:#111">A PRIMEIRA CARTA<br><span style="font-family:PF;font-style:italic;font-weight:700;text-transform:none;font-size:30px;color:#2b2b2b">Pact of the Titan · Future Sight, 2007</span></div>'
     + '<div class="e" style="left:612px;top:640px;width:380px;white-space:normal;transform:rotate(2deg);transform-origin:left;font-family:RB;font-weight:800;font-size:33px;line-height:1.16;color:#111">'
       'Antes de Magic, passou <b>8 anos</b> na série de jogos <b>Oddworld</b>.<br><br>'
       'Estreou nas cartas em <b>2007</b>.<br><br>'
       'Hoje são <b>217 artes</b> diferentes em cartas físicas, segundo o Scryfall.</div>')
S['02_BIOGRAFIA'] = (b, t, rodape_txt(1212, 'Do <y>videogame</y> para as<br>cartas de <y>Magic</y>.', cr('pact')))

# 03 · ASSINATURA VISUAL
b = fundo(2); b = selo(b)
b = papel(b, 64, 205, 700, 150, -1.5, 1, 5)
b, ah = impressa(b, arte(G + 'etali_art.jpg'), 540, 395, 930, -.6, fitas=((-.45, -1, -12), (.5, -1, 9)), seed=32)
for i, (x, y, a) in enumerate(((70, 1030, -3), (395, 1042, 2), (720, 1026, -2))):
    b = papel(b, x, y, 290, 95, a, (i + 1) % 3, 6 + i)
b = rodape(b, 1245)
t = ('<div class="e" data-w="620" style="left:96px;top:238px;font-family:AB;font-size:72px;line-height:1;color:#111;transform:rotate(-1.5deg);transform-origin:left">A ASSINATURA VISUAL</div>'
     + traco(104, 312, 560, -1.5, 9)
     + ''.join(f'<div class="e" style="left:{x+145}px;top:{y+20}px;transform:translateX(-50%) rotate({a}deg);text-align:center;font-family:BC;font-size:30px;line-height:1.02;color:#111">{s}</div>'
               for (x, y, a), s in zip(((70, 1030, -3), (395, 1042, 2), (720, 1026, -2)),
                                       ('CRIATURAS EM<br><b>MOVIMENTO</b>', 'RAIOS E LUZ DE<br><b>TEMPESTADE</b>', 'CENAS EM<br><b>DIAGONAL</b>'))))
S['03_ASSINATURA_VISUAL'] = (b, t, rodape_txt(1245, 'Nada fica <y>parado</y>: até a<br>tempestade parece <y>viva</y>.', cr('etali'), 46))

# 04 · OBRA MEMORÁVEL
b = fundo(3); b = selo(b)
b, ah = impressa(b, arte(G + 'mesa_art.jpg'), 540, 215, 940, .5, fitas=((0, -1, -5),), seed=42)
b = carta(b, G + 'mesa_card.png', 225, 935, 270, -5, fitas=((.78, -1, 35),))
b = papel(b, 420, 870, 600, 300, 1.5, 1, 7)
b = rodape(b, 1230)
t = ('<div class="e" data-w="540" style="left:452px;top:890px;transform:rotate(1.5deg);transform-origin:left;font-family:AB;font-size:58px;line-height:1;color:#111">ARID MESA</div>'
     + '<div class="e" style="left:454px;top:952px;transform:rotate(1.5deg);transform-origin:left;font-family:PF;font-style:italic;font-weight:700;font-size:30px;color:#2b2b2b">Zendikar, 2009</div>'
     + '<div class="e" style="left:454px;top:1004px;width:530px;white-space:normal;transform:rotate(1.5deg);transform-origin:left;font-family:RB;font-weight:800;font-size:30px;line-height:1.16;color:#111">A primeira edição desta terra saiu com a paisagem dele: rochas que se erguem do <b>deserto</b> como <b>ruínas</b>.</div>')
S['04_OBRA_MEMORAVEL'] = (b, t, rodape_txt(1230, 'A paisagem como <y>personagem</y>,<br>não só como <y>cenário</y>.', cr('mesa'), 44))

# 05 · OUTRA FACETA
b = fundo(4); b = selo(b)
b = papel(b, 64, 205, 640, 150, -2, 1, 8)
b, ah = impressa(b, arte(G + 'tutor_art.jpg'), 470, 395, 800, -1.2, fitas=((-.3, -1, -8),), seed=52)
b = carta(b, G + 'tutor_card.png', 880, 900, 250, 6, fitas=((.8, -1, 38),))
b = rodape(b, 1225)
t = ('<div class="e" data-w="600" style="left:96px;top:236px;font-family:AB;font-size:70px;line-height:1;color:#111;transform:rotate(-2deg);transform-origin:left">O LADO SOMBRIO</div>'
     + traco(104, 310, 520, -2, 9)
     + '<div class="e" style="left:90px;top:1000px;width:620px;white-space:normal;transform:rotate(-1.2deg);transform-origin:left;font-family:PF;font-style:italic;font-weight:700;font-size:36px;line-height:1.12;color:#2b2b2b">Vampiric Tutor (Eternal Masters, 2016): sombra, silêncio e uma caveira no centro.</div>')
S['05_OUTRA_FACETA'] = (b, t, rodape_txt(1225, 'Do caos da tempestade ao<br><y>silêncio</y> de uma <y>caveira</y>.', cr('tutor'), 46))

# 06 · CURIOSIDADES
b = fundo(5); b = selo(b)
b = papel(b, 64, 205, 760, 230, -1.5, 1, 9)
b = carta(b, G + 'drain_card.png', 300, 760, 380, -4, fitas=((.8, -1, 34),))
b = carta(b, G + 'tutor_card.png', 780, 780, 380, 4, fitas=((.8, -1, 38),))
b = papel(b, 150, 1010, 300, 80, -3, 2, 10); b = papel(b, 630, 1020, 300, 80, 3, 2, 11)
b = rodape(b, 1225)
t = ('<div class="e" data-w="680" style="left:96px;top:238px;font-family:AB;font-size:64px;line-height:1;color:#111;transform:rotate(-1.5deg);transform-origin:left">ELE REPINTOU<br>CLÁSSICOS</div>'
     + traco(104, 384, 600, -1.5, 9)
     + '<div class="e" style="left:300px;top:1030px;transform:translateX(-50%) rotate(-3deg);font-family:AB;font-size:38px;color:#111">1994 <b>→</b> 2017</div>'
     + '<div class="e" style="left:780px;top:1040px;transform:translateX(-50%) rotate(3deg);font-family:AB;font-size:38px;color:#111">1997 <b>→</b> 2016</div>')
S['06_CURIOSIDADES'] = (b, t, rodape_txt(1225, 'Mana Drain e Vampiric Tutor ganharam<br><y>arte nova</y> nas edições <y>Masters</y>.', 'Mana Drain (Iconic Masters, 2017) · Vampiric Tutor (Eternal Masters, 2016) · Raymond Swanland · Wizards of the Coast', 42))

# 07 · ENCERRAMENTO
b = fundo(6); b = selo(b)
b, ah = impressa(b, arte(G + 'grave_art.jpg'), 540, 215, 920, -.5, fitas=((-.5, -1, -9),), seed=72)
b = papel(b, 70, 900, 940, 230, -1, 0, 12)
b = rodape(b, 1240)
t = ('<div class="e" data-w="860" style="left:106px;top:928px;transform:rotate(-1deg);transform-origin:left;font-family:AB;font-size:56px;line-height:1.02;color:#111">QUAL DESTAS OBRAS MERECE<br>UM LUGAR NO SEU <b>BINDER?</b></div>'
     + '<div class="e" data-w="850" style="left:110px;top:1060px;transform:rotate(-1deg);transform-origin:left;font-family:PF;font-style:italic;font-weight:700;font-size:32px;color:#2b2b2b">Ugin, Etali, Arid Mesa, Vampiric Tutor, Mana Drain ou Watery Grave?</div>')
S['07_ENCERRAMENTO'] = (b, t, rodape_txt(1240, 'Raymond Swanland: <y>tempestade</y>,<br>ruína e <y>movimento</y>.', cr('grave'), 46))

for nome, (b, t, c) in S.items():
    render(b, t, c, os.path.join(OUT, nome + '.png')); print(nome)
