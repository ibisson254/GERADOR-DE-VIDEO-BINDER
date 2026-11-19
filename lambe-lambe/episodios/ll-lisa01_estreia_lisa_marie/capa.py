"""LL-LISA01 · Teaser de estreia da Lisa Marie no Ar (formato Lambe-lambe). Capa 1080x1350 com o motor-padrão.
Uso: python3 -I capa.py <pasta_saida>
Imagens: recortes da prancha de 19/11 (lisa-marie/referencias/inspiracoes_2026-11-19/), versionados. Zero créditos."""
import sys, os, cv2
OUT = os.path.abspath(sys.argv[1]); os.makedirs(OUT, exist_ok=True)
AQUI = os.path.dirname(os.path.abspath(__file__))
LOOKS = os.path.normpath(os.path.join(AQUI, '../../../lisa-marie/referencias/inspiracoes_2026-11-19'))
sys.path.insert(0, os.path.normpath(os.path.join(AQUI, '../../kit_carrossel')))
from motor_padrao import *
def look(n):
    im = cv2.imread(f'{LOOKS}/{n}.png'); im = im[14:im.shape[0] - 78]   # tira a faixa rosa do topo e a etiqueta numerada da prancha
    cv2.imwrite(f'{OUT}/{n}.png', im); return im                       # recortes limpos também servem ao story.json
for n in ('03_dj_de_vinil', '08_nerd_de_cultura_pop', '02_otaku_casual'): look(n)

b = fundo(7)                                  # sem o selo azul: ele diz «Artistas de Magic»
b = papel(b, 64, 205, 950, 225, -1.5, 1)
b, ah = impressa(b, look('01_reporter_do_multiverso'), 300, 470, 360, -2.5, fitas=((-.7, -1, -10), (.7, -1, 10)), seed=41)
b = papel(b, 560, 500, 455, 300, 2, 0, 3)
b = papel(b, 556, 840, 460, 220, -2, 2, 4)
b = rodape(b, 1230)
t = ('<div class="e" data-w="880" style="left:96px;top:226px;font-family:AB;font-size:44px;line-height:1;color:#111;transform:rotate(-1.5deg);transform-origin:left">ESTREIA NO <b>BINDER ORIGINALS</b></div>'
     + '<div class="e" data-w="900" style="left:96px;top:284px;font-family:AB;font-size:100px;line-height:1;color:#111;transform:rotate(-1.5deg);transform-origin:left;letter-spacing:-2px">LISA MARIE</div>'
     + traco(100, 392, 820, -1.5, 10)
     + '<div class="e" data-w="400" style="left:788px;top:540px;transform:translateX(-50%) rotate(2deg);text-align:center;font-family:AB;font-size:96px;line-height:.95;color:#111">NO<br><b>AR</b></div>'
     + '<div class="e" data-w="400" style="left:788px;top:745px;transform:translateX(-50%) rotate(2deg);text-align:center;font-family:BC;font-size:30px;color:#111">A VJ CULTURAL DO MULTIVERSO</div>'
     + '<div class="e" data-w="410" style="left:786px;top:872px;transform:translateX(-50%) rotate(-2deg);text-align:center;font-family:AB;font-size:36px;line-height:1.12;color:#111">ANIME · K-POP<br>VINIL · <b>MAGIC</b></div>')
c = ('<div style="position:absolute;left:96px;top:96px;transform:rotate(-3deg);background:#111;color:#FFD84A;font-family:AB;font-size:34px;padding:8px 22px;letter-spacing:3px">NOVA SÉRIE</div>'
     + '<div style="position:absolute;left:820px;top:1000px;transform:rotate(-4deg);background:#E61E6E;color:#fff;font-family:AB;font-size:28px;padding:6px 18px;letter-spacing:2px">EM BREVE</div>'
     + rodape_txt(1230, 'Quadro de estreia: <y>Elas no Multiverso</y>', 'Lisa Marie · personagem original BINDER Originals · imagem conceitual', 46))
render(b, t, c, f'{OUT}/01_capa.png'); print('ok', OUT)
