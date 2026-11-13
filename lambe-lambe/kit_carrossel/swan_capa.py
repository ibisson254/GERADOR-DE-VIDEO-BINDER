import asyncio, cv2, sys
sys.path.insert(0,'.')
from compor import *
base = cv2.imread('modelo_capa.png')
base = pintura(base,'mask_pintura_1.png','swan_ugin.jpg',foco=(0.5,0.35))
tinta = '''
<div class="e ab" style="left:160px;top:200px;font-size:92px;transform:scaleX(.9) rotate(-1.5deg);transform-origin:left;color:#111">QUEM PINTOU O</div>
<div class="e ab" style="left:250px;top:282px;font-size:160px;transform:scaleX(.95) rotate(-1.5deg);transform-origin:left;color:#111">UGIN<span style="color:#C2186E;font-size:170px;margin-left:10px">?</span></div>
<svg class="e" style="left:250px;top:418px" width="600" height="40"><path d="M10 30 C 200 14, 400 18, 590 8" stroke="#C2186E" stroke-width="11" fill="none" stroke-linecap="round"/></svg>
<div class="e bc" data-w="790" style="left:540px;transform:translateX(-50%);top:1112px;font-size:54px;color:#111;text-align:center">MAIS DE 200 ARTES PARA MAGIC<br>8 ANOS NA SÉRIE ODDWORLD</div>
<div class="e bc" style="left:568px;transform:translateX(-50%);top:1232px;font-size:52px;color:#111;text-transform:none">Desde 2007</div>
'''
claro = '''
<div class="e ab" data-w="840" style="left:540px;transform:translateX(-50%) rotate(-.8deg);top:968px;font-size:108px;color:#F2E6CC;text-transform:none">RAYMOND SWANLAND</div>
<div style="position:absolute;right:80px;top:912px;font-family:Geist;font-size:13px;color:#fff;text-shadow:0 1px 3px #000;opacity:.9">Arte: Ugin, the Spirit Dragon (Fate Reforged, 2015) · Raymond Swanland · © Wizards of the Coast</div>
'''
asyncio.run(camada(tinta,'_tinta.png')); asyncio.run(camada(claro,'_claro.png'))
out = aplicar(base,'_tinta.png','_claro.png')
cv2.imwrite('swan_1.png',out)
