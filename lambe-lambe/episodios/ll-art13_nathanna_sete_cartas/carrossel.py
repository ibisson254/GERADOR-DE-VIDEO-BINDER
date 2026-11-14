"""LL-ART13 · Nathanna Érica: sete cartas em Special Guests (Lorwyn Eclipsed). 7 slides 1080x1350.
Uso: python3 -I carrossel.py <pasta_cartas_scryfall> <foto.png> <foto_mask.png> <pasta_saida>
Cartas: <n>_png.png e <n>_art_crop.jpg do Scryfall (set spg). Foto: só a enviada pelo fundador (não versionada)."""
import sys, os, cv2
G, FOTO_P, MASK_P, OUT = [os.path.abspath(a) for a in sys.argv[1:5]]
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../kit_carrossel')))
from motor_padrao import *
os.makedirs(OUT, exist_ok=True)

C = {'130': 'Kinsbaile Cavalier', '132': 'Wanderwine Prophets', '134': 'Faerie Macabre', '135': 'Goblin Chieftain',
     '139': 'Helix Pinnacle', '141': 'Regal Force', '143': 'Risen Reef'}
T = {'130': 'Criatura — Kithkin Cavaleiro', '132': 'Criatura — Tritão Mago', '134': 'Criatura — Fada Ladina',
     '135': 'Criatura — Goblin', '139': 'Encantamento', '141': 'Criatura — Elemental', '143': 'Criatura — Elemental'}
png = lambda n: f'{G}/{n}_png.png'
art = lambda n: f'{G}/{n}_art_crop.jpg'
def cr(*ns): return ' · '.join(f'{C[n]} (SPG {n})' for n in ns) + ' · Nathanna Erica · © Wizards of the Coast'
TOPO = ((-1.0, -1.04, -45), (1.0, -1.04, 45))           # fita só nos dois cantos de cima

def titulo(txt, top=236, fs=70, w=620):
    return (f'<div class="e" data-w="{w}" style="left:96px;top:{top}px;font-family:AB;font-size:{fs}px;line-height:1;color:#111;'
            f'transform:rotate(-1.5deg);transform-origin:left;letter-spacing:-1px">{txt}</div>')
def etiqueta(n, cx, top, ang):
    return (f'<div class="e" style="left:{cx}px;top:{top}px;transform:translateX(-50%) rotate({ang}deg);text-align:center;'
            f'font-family:AB;font-size:30px;line-height:1.08;color:#111" data-w="430">{C[n].upper()}<br><b>Nº {n}</b> '
            f'<span style="font-family:PF;font-style:italic;font-weight:700;text-transform:none;font-size:25px;color:#2b2b2b">· {T[n]}</span></div>')
def dupla(seed, tit, a, b, frase):
    bs = fundo(seed); bs = selo(bs)
    bs = papel(bs, 64, 205, 720, 140, -1.5, 1, seed)
    bs = carta(bs, png(a), 290, 690, 390, -3, fitas=TOPO, fl=78)
    bs = carta(bs, png(b), 790, 700, 390, 3, fitas=TOPO, fl=78)
    bs = papel(bs, 66, 980, 470, 112, -2.5, 2, seed + 1); bs = papel(bs, 548, 990, 470, 112, 2.5, 2, seed + 2)
    bs = rodape(bs, 1228)
    t = (titulo(tit, 238, 66, 660) + traco(104, 312, 560, -1.5, 9)
         + etiqueta(a, 300, 1000, -2.5) + etiqueta(b, 783, 1010, 2.5))
    return bs, t, rodape_txt(1228, frase, cr(a, b), 44)

S = {}
# 01 · CAPA
b = fundo(0); b = selo(b)
b = papel(b, 64, 205, 950, 235, -1.5, 1)
b = carta(b, png('130'), 330, 790, 455, -2.5, fitas=TOPO, fl=78)
b = papel(b, 600, 500, 420, 300, 2, 0, 3)
b = papel(b, 596, 836, 430, 160, -2, 2, 4)
b = rodape(b, 1230)
t = (titulo('7 CARTAS.', 228, 104, 880)
     + '<div class="e" data-w="880" style="left:96px;top:330px;font-family:AB;font-size:62px;line-height:1;color:#111;transform:rotate(-1.5deg);transform-origin:left">UMA ARTISTA <b>BRASILEIRA.</b></div>'
     + traco(100, 395, 820, -1.5, 10)
     + '<div class="e" data-w="360" style="left:810px;top:540px;transform:translateX(-50%) rotate(2deg);text-align:center;font-family:AB;font-size:74px;line-height:.98;color:#111">NATHANNA<br>ÉRICA</div>'
     + traco(650, 700, 330, 2, 8)
     + '<div class="e" style="left:810px;top:866px;transform:translateX(-50%) rotate(-2deg);text-align:center;font-family:BC;font-size:30px;line-height:1.05;color:#111">NA CAPA<br><span style="font-family:AB;font-size:34px">KINSBAILE CAVALIER</span><br><b>Nº 130</b></div>')
c = ('<div style="position:absolute;left:840px;top:752px;transform:rotate(-4deg);background:#10893E;color:#fff;font-family:AB;font-size:26px;padding:6px 16px;letter-spacing:1px">DO BRASIL</div>'
     + rodape_txt(1230, 'SPECIAL GUESTS · <y>LORWYN ECLIPSED</y>', cr('130'), 46))
S['01_capa'] = (b, t, c)

S['02_fadas_e_merfolks'] = dupla(1, 'FADAS E MERFOLKS', '134', '132', 'Uma fada <y>preta</y> e um tritão <y>azul</y>,<br>no mesmo traço de papel recortado.')
S['03_goblins_e_elementais'] = dupla(2, 'GOBLINS E ELEMENTAIS', '135', '141', 'Do <y>vermelho</y> ao <y>verde</y>:<br>um goblin e um elemental.')
S['04_elemental_e_encantamento'] = dupla(3, 'ELEMENTAL E ENCANTAMENTO', '143', '139', 'Helix Pinnacle é o único<br><y>encantamento</y> entre as sete.')

# 05 · AS SETE CARTAS (lista para guardar)
b = fundo(4); b = selo(b)
b = papel(b, 64, 205, 760, 150, -1.5, 1, 20)
b = papel(b, 70, 380, 945, 760, .8, 0, 21)
b = rodape(b, 1235)
lin = ''.join(f'<div style="display:flex;align-items:baseline;gap:22px;margin-bottom:12px"><span style="font-family:AB;font-size:46px;color:#E61E6E;width:110px">{n}</span>'
              f'<span><span style="font-family:AB;font-size:40px;color:#111">{C[n].upper()}</span><br>'
              f'<span style="font-family:PF;font-style:italic;font-weight:700;font-size:25px;color:#2b2b2b">{T[n]}</span></span></div>' for n in C)
t = (titulo('AS SETE CARTAS', 238, 72, 660) + traco(104, 314, 560, -1.5, 9)
     + f'<div class="e" style="left:130px;top:420px;transform:rotate(.8deg);transform-origin:left;white-space:normal;width:840px">{lin}</div>')
S['05_as_sete_cartas'] = (b, t, rodape_txt(1235, '<y>7 dos 20</y> Special Guests de<br>Lorwyn Eclipsed. Salve para consultar.', 'Special Guests (SPG) 130–143 · Nathanna Erica · © Wizards of the Coast', 44))

# 06 · A ARTISTA
b = fundo(5); b = selo(b)
b = papel(b, 64, 205, 600, 250, -2, 1, 30)
b = recorte(b, cv2.imread(FOTO_P), cv2.imread(MASK_P, 0), cx=830, topo=40, alt=470, ang=1.5)
b, ah = impressa(b, cv2.imread(art('135')), 330, 545, 500, -2.5, fitas=((0, -1, -6),), seed=31)
b = papel(b, 600, 590, 425, 470, 2, 0, 32)
b = rodape(b, 1228)
t = (titulo('QUEM É<br>NATHANNA ÉRICA?', 240, 64, 560) + traco(104, 384, 500, -2, 9)
     + '<div class="e" style="left:636px;top:628px;width:360px;white-space:normal;transform:rotate(2deg);transform-origin:left;font-family:RB;font-weight:800;font-size:33px;line-height:1.16;color:#111">'
       '<b>Ilustradora</b> e <b>artista de papel</b> (paper art).<br><br>Também trabalha com <b>visual development</b>.<br><br>Vive em <b>São Paulo</b>.</div>'
     + f'<div class="e" style="left:92px;top:{545+ah+40}px;transform:rotate(-2.5deg);transform-origin:left;font-family:BC;font-size:28px;line-height:1.08;color:#111">NO DETALHE<br>'
       '<span style="font-family:PF;font-style:italic;font-weight:700;text-transform:none;font-size:27px;color:#2b2b2b">Goblin Chieftain · SPG 135</span></div>')
S['06_a_artista'] = (b, t, rodape_txt(1228, 'Ilustração, <y>paper art</y> e<br><y>visual development</y>.', 'Arte: ' + cr('135'), 44))

# 07 · ENCERRAMENTO
b = fundo(6); b = selo(b)
b, ah = impressa(b, cv2.imread(art('134')), 540, 210, 900, -.5, fitas=((-.5, -1, -9), (.5, -1, 9)), seed=72)
b = papel(b, 70, 900, 940, 230, -1, 0, 40)
b = rodape(b, 1245)
t = ('<div class="e" data-w="860" style="left:106px;top:925px;transform:rotate(-1deg);transform-origin:left;font-family:AB;font-size:52px;line-height:1.04;color:#111">QUAL DESSAS SETE ILUSTRAÇÕES<br>MAIS CHAMOU SUA <b>ATENÇÃO?</b></div>'
     + '<div class="e" data-w="860" style="left:110px;top:1058px;transform:rotate(-1deg);transform-origin:left;font-family:PF;font-style:italic;font-weight:700;font-size:30px;color:#2b2b2b">Responda nos comentários com o número da carta.</div>')
S['07_encerramento'] = (b, t, rodape_txt(1245, 'Artistas de Magic · <y>BINDER</y>', 'Arte: ' + cr('134'), 50))

for i, (nome, (b, t, c)) in enumerate(S.items(), 1):
    render(b, t, c, os.path.join(OUT, f'{nome}.png')); print(nome)
