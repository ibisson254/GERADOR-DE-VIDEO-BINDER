"""LL-ART20 · Caio Monteiro: o ilustrador do Rio por trás de Shark Typhoon. 7 slides 1080x1350.
Uso: python3 -I carrossel.py <pasta_cartas> <foto> <foto_mask.png|-> <pasta_saida> [--sem-foto] [--previa]
Cartas (Scryfall, não versionadas): <set>_<n>_png.png e <set>_<n>_art_crop.jpg para iko_67, frc_44, stx_37, znr_112, fdn_79.
Foto: só a enviada pelo fundador (não versionada). Máscara '-' = recorte retangular com papel rasgado.
--sem-foto: versão B (plano alternativo). --previa: marca «PRÉVIA · AGUARDA AUTORIZAÇÃO» no muro, fora das cartas."""
import sys, os, cv2, numpy as np
args = [a for a in sys.argv[1:] if not a.startswith('--')]
SEM_FOTO, PREVIA = '--sem-foto' in sys.argv, '--previa' in sys.argv
G, FOTO_P, MASK_P, OUT = args[0], args[1], args[2], args[3]
G, OUT = os.path.abspath(G), os.path.abspath(OUT)
FOTO_P = os.path.abspath(FOTO_P) if FOTO_P != '-' else None
MASK_P = os.path.abspath(MASK_P) if MASK_P != '-' else None
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../kit_carrossel')))
from motor_padrao import *
os.makedirs(OUT, exist_ok=True)

# Dados verificados a 16/11/2026 (fontes.md): Scryfall, ranking EDHREC devolvido pela API do Scryfall.
N = {'iko_67': ('Shark Typhoon', 'IKO 67'), 'frc_44': ('Shark Typhoon', 'FRC 44'), 'stx_37': ('Archmage Emeritus', 'STX 37'),
     'znr_112': ('Marauding Blight-Priest', 'ZNR 112'), 'fdn_79': ('Boltwave', 'FDN 79')}
png = lambda n: f'{G}/{n}_png.png'
art = lambda n: f'{G}/{n}_art_crop.jpg'
def cr(*ns): return ' · '.join(f'{N[n][0]} ({N[n][1]})' for n in ns) + ' · Caio Monteiro · © Wizards of the Coast'
TOPO = ((-1.0, -1.04, -45), (1.0, -1.04, 45))   # fita só nos dois cantos de cima

def titulo(txt, top=236, fs=70, w=620, left=96):
    return (f'<div class="e" data-w="{w}" style="left:{left}px;top:{top}px;font-family:AB;font-size:{fs}px;line-height:1;color:#111;'
            f'transform:rotate(-1.5deg);transform-origin:left;letter-spacing:-1px">{txt}</div>')
def bloco(x, y, w, html, fs=33, ang=2):
    return (f'<div class="e" style="left:{x}px;top:{y}px;width:{w}px;white-space:normal;transform:rotate({ang}deg);transform-origin:left;'
            f'font-family:RB;font-weight:800;font-size:{fs}px;line-height:1.16;color:#111">{html}</div>')
def previa():
    if not PREVIA: return ''
    return ('<div style="position:absolute;left:1040px;top:640px;transform:translateX(-50%) rotate(90deg);background:#111;color:#FFD84A;'
            'font-family:AB;font-size:20px;padding:5px 14px;letter-spacing:2px;white-space:nowrap">PRÉVIA · AGUARDA AUTORIZAÇÃO</div>')

def ranking(seed, n, pos, linha, frase):
    """um slide por carta: carta inteira à esquerda, dado do ranking EDHREC à direita"""
    b = fundo(seed); b = selo(b)
    b = papel(b, 64, 205, 760, 150, -1.5, 1, seed)
    b = carta(b, png(n), 300, 720, 430, -2.5, fitas=TOPO, fl=78)
    b = papel(b, 580, 470, 440, 520, 2, 0, seed + 3)
    b = rodape(b, 1228)
    t = (titulo('NO COMMANDER', 238, 70, 660) + traco(104, 314, 560, -1.5, 9)
         + f'<div class="e" style="left:800px;top:500px;transform:translateX(-50%) rotate(2deg);text-align:center;font-family:AB;font-size:118px;line-height:1;color:#E61E6E">#{pos}</div>'
         + '<div class="e" style="left:800px;top:630px;transform:translateX(-50%) rotate(2deg);text-align:center;font-family:BC;font-size:34px;line-height:1.05;color:#111">NO RANKING DE CARTAS<br>DO EDHREC</div>'
         + traco(640, 712, 320, 2, 7)
         + f'<div class="e" data-w="400" style="left:800px;top:770px;transform:translateX(-50%) rotate(2deg);text-align:center;font-family:AB;font-size:38px;line-height:1.04;color:#111">{N[n][0].upper()}</div>'
         + f'<div class="e" style="left:800px;top:{770+92}px;transform:translateX(-50%) rotate(2deg);text-align:center;font-family:PF;font-style:italic;font-weight:700;font-size:26px;line-height:1.2;color:#2b2b2b">{linha}</div>'
         + '<div class="e" style="left:792px;top:948px;transform:translateX(-50%) rotate(2deg);text-align:center;font-family:Geist;font-weight:700;font-size:15px;color:#3a3a3a">Fonte: EDHREC via Scryfall · 16/11/2026</div>')
    return b, t + previa(), rodape_txt(1228, frase, cr(n), 44)

S = {}
# 01 · CAPA
b = fundo(0); b = selo(b)
b = papel(b, 64, 205, 950, 235, -1.5, 1)
b = carta(b, png('iko_67'), 320, 800, 450, -2.5, fitas=TOPO, fl=78)
b = papel(b, 600, 520, 420, 290, 2, 0, 3)
b = papel(b, 596, 846, 430, 150, -2, 2, 4)
b = rodape(b, 1230)
t = (titulo('O ILUSTRADOR DO RIO', 228, 86, 880)
     + '<div class="e" data-w="880" style="left:96px;top:322px;font-family:AB;font-size:56px;line-height:1;color:#111;transform:rotate(-1.5deg);transform-origin:left">POR TRÁS DE <b>SHARK TYPHOON</b></div>'
     + traco(100, 388, 820, -1.5, 10)
     + '<div class="e" style="left:810px;top:556px;transform:translateX(-50%) rotate(2deg);text-align:center;font-family:BC;font-size:34px;color:#111">QUEM PINTOU?</div>'
     + '<div class="e" data-w="370" style="left:810px;top:606px;transform:translateX(-50%) rotate(2deg);text-align:center;font-family:AB;font-size:78px;line-height:.98;color:#111">CAIO<br>MONTEIRO</div>'
     + traco(650, 772, 330, 2, 8)
     + '<div class="e" style="left:810px;top:874px;transform:translateX(-50%) rotate(-2deg);text-align:center;font-family:BC;font-size:30px;line-height:1.05;color:#111">NA CAPA<br><span style="font-family:AB;font-size:34px">SHARK TYPHOON</span><br><b>IKORIA · Nº 67</b></div>')
c = ('<div style="position:absolute;left:740px;top:462px;transform:rotate(-4deg);background:#10893E;color:#fff;font-family:AB;font-size:26px;padding:6px 16px;letter-spacing:1px">DO BRASIL</div>'
     + rodape_txt(1230, 'Série <y>Artistas de Magic</y>', cr('iko_67'), 46) + previa())
S['01_capa'] = (b, t, c)

# 02 · QUEM É (A: com foto · B: sem foto)
b = fundo(5); b = selo(b)
TXT = ('<b>Ilustrador freelancer</b> baseado no <b>Rio de Janeiro</b>.<br><br>'
       'Assina cartas de <b>Magic</b> e também de outros jogos, como <b>KeyForge</b>.')
if not SEM_FOTO:
    b = papel(b, 64, 205, 560, 250, -2, 1, 30)
    b = recorte(b, cv2.imread(FOTO_P), cv2.imread(MASK_P, 0), cx=820, topo=60, alt=440, ang=1.5)
    b = carta(b, png('fdn_79'), 290, 860, 380, -2.5, fitas=TOPO, fl=72)
    b = papel(b, 560, 620, 460, 450, 2, 0, 32)
    b = rodape(b, 1250)
    t = (titulo('QUEM É<br>CAIO MONTEIRO?', 240, 62, 520) + traco(104, 384, 470, -2, 9)
         + bloco(596, 660, 390, TXT, 32)
         + '<div class="e" style="left:596px;top:985px;transform:rotate(2deg);transform-origin:left;font-family:BC;font-size:28px;line-height:1.08;color:#111">NA PAREDE<br>'
           '<span style="font-family:PF;font-style:italic;font-weight:700;font-size:27px;color:#2b2b2b">Boltwave · Foundations nº 79</span></div>')
    frase_cy = 1250
else:
    b = papel(b, 64, 205, 950, 200, -1.5, 1, 30)
    b = carta(b, png('fdn_79'), 300, 770, 440, -2.5, fitas=TOPO, fl=78)
    b = papel(b, 570, 470, 450, 600, 2, 0, 32)
    b = rodape(b, 1235)
    t = (titulo('QUEM É CAIO MONTEIRO?', 240, 66, 880) + traco(104, 318, 800, -1.5, 9)
         + '<div class="e" data-w="400" style="left:796px;top:510px;transform:translateX(-50%) rotate(2deg);text-align:center;font-family:AB;font-size:64px;line-height:.98;color:#111">CAIO<br>MONTEIRO</div>'
         + traco(640, 650, 320, 2, 7)
         + bloco(606, 690, 390, TXT, 31)
         + '<div class="e" style="left:606px;top:1000px;transform:rotate(2deg);transform-origin:left;font-family:BC;font-size:28px;line-height:1.08;color:#111">NA PAREDE<br>'
           '<span style="font-family:PF;font-style:italic;font-weight:700;font-size:27px;color:#2b2b2b">Boltwave · Foundations nº 79</span></div>')
    frase_cy = 1235
S['02_quem_e'] = (b, t + previa(), rodape_txt(frase_cy, 'Do Rio para as <y>cartas de Magic</y>.', cr('fdn_79'), 44))

# 03 · O PORTFÓLIO
b = fundo(2); b = selo(b)
b = papel(b, 64, 205, 820, 150, -1.5, 1, 50)
b = papel(b, 90, 420, 560, 560, -1.5, 0, 51)
b, ah = impressa(b, cv2.imread(art('stx_37')), 830, 470, 300, 3, fitas=((0, -1, -8),), seed=52)
b, ah2 = impressa(b, cv2.imread(art('znr_112')), 830, 760, 300, -2.5, fitas=((0, -1, 7),), seed=53)
b = rodape(b, 1228)
t = (titulo('QUANTAS ARTES ELE JÁ ASSINOU?', 238, 60, 800) + traco(104, 310, 700, -1.5, 9)
     + '<div class="e" style="left:370px;top:470px;transform:translateX(-50%) rotate(-1.5deg);text-align:center;font-family:AB;font-size:230px;line-height:1;color:#E61E6E">88</div>'
     + '<div class="e" style="left:370px;top:700px;padding-top:26px;transform:translateX(-50%) rotate(-1.2deg);text-align:center;font-family:AB;font-size:43px;line-height:1.04;color:#111">ILUSTRAÇÕES<br>EM CARTAS DE PAPEL</div>'
     + '<div class="e" style="left:370px;top:840px;transform:translateX(-50%) rotate(-1.5deg);text-align:center;font-family:PF;font-style:italic;font-weight:700;font-size:30px;color:#2b2b2b">de 2019 a 2026</div>'
     + '<div class="e" style="left:370px;top:910px;transform:translateX(-50%) rotate(-1.5deg);text-align:center;font-family:Geist;font-weight:700;font-size:16px;line-height:1.35;color:#3a3a3a">Scryfall · artista «Caio Monteiro» · uma por ilustração<br>só papel (inclui tokens) · consulta de 16/11/2026</div>')
S['03_portfolio'] = (b, t + previa(), rodape_txt(1228, 'Do <y>Core Set 2020</y> a<br><y>Lorwyn Eclipsed</y>.', 'Arte: ' + cr('stx_37', 'znr_112'), 42))

# 04–06 · AS CARTAS NO COMMANDER (ranking EDHREC por n.º de decks)
S['04_archmage_emeritus'] = ranking(1, 'stx_37', 252, 'Strixhaven · nº 37 · 2021', 'A arte dele mais presente<br>nos decks de <y>Commander</y>.')
S['05_marauding_blight_priest'] = ranking(3, 'znr_112', '1.092', 'Zendikar Rising · nº 112 · 2020', 'Você ganhou vida?<br><y>Cada oponente perde 1.</y>')
S['06_shark_typhoon'] = ranking(4, 'frc_44', '1.231', 'Arte de Ikoria (2020),<br>reimpressa em FRC, out. 2026',
                                'A mesma arte de 2020<br>voltou em <y>outubro de 2026</y>.')

# 07 · PARTICIPAÇÃO
b = fundo(6); b = selo(b)
b, a1 = impressa(b, cv2.imread(art('stx_37')), 230, 300, 300, -3, fitas=((0, -1, -8),), seed=71)
b, a2 = impressa(b, cv2.imread(art('znr_112')), 540, 340, 300, 2, fitas=((0, -1, 6),), seed=72)
b, a3 = impressa(b, cv2.imread(art('iko_67')), 850, 300, 300, -2, fitas=((0, -1, -7),), seed=73)
b = papel(b, 70, 730, 940, 300, -1, 0, 40)
b = rodape(b, 1235)
t = ('<div class="e" style="left:230px;top:540px;transform:translateX(-50%) rotate(-3deg);text-align:center;font-family:BC;font-size:27px;line-height:1.1;color:#111"><span style="font-family:AB;font-size:40px;color:#E61E6E">1</span><br>ARCHMAGE EMERITUS<br>STX 37</div>'
     '<div class="e" style="left:540px;top:580px;transform:translateX(-50%) rotate(2deg);text-align:center;font-family:BC;font-size:27px;line-height:1.1;color:#111"><span style="font-family:AB;font-size:40px;color:#E61E6E">2</span><br>MARAUDING BLIGHT-PRIEST<br>ZNR 112</div>'
     '<div class="e" style="left:850px;top:540px;transform:translateX(-50%) rotate(-2deg);text-align:center;font-family:BC;font-size:27px;line-height:1.1;color:#111"><span style="font-family:AB;font-size:40px;color:#E61E6E">3</span><br>SHARK TYPHOON<br>IKO 67</div>'
     '<div class="e" data-w="860" style="left:106px;top:772px;transform:rotate(-1deg);transform-origin:left;font-family:AB;font-size:58px;line-height:1.04;color:#111">QUAL DESSAS ARTES<br>É A SUA <b>FAVORITA?</b></div>'
     '<div class="e" data-w="860" style="left:110px;top:934px;transform:rotate(-1deg);transform-origin:left;font-family:PF;font-style:italic;font-weight:700;font-size:32px;color:#2b2b2b">Responda nos comentários com o nome da carta.</div>')
S['07_participacao'] = (b, t + previa(), rodape_txt(1235, 'Artistas de Magic · <y>BINDER</y>', 'Artes acima: Caio Monteiro · © Wizards of the Coast', 50))

for nome, (b, t, c) in S.items():
    render(b, t, c, os.path.join(OUT, f'{nome}.png')); print(nome)
