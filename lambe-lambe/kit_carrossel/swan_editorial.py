import asyncio, cv2, sys
sys.path.insert(0,'.')
from compor import *
from recorte_foto import recorte
base=cv2.imread('modelo_editorial.png')
base=pintura(base,'mask_pintura_2.png','swan_etali.jpg',foco=(0.38,0.5),sat=1.05)
base=recorte(base,cv2.imread('foto_2x.png'),cv2.imread('foto_mask.png',0),cx=842,topo=38,alt=610,ang=1.5)
tinta='''
<div class="e ab" data-w="470" style="left:140px;top:215px;font-size:130px;transform:rotate(-1deg);color:#111;line-height:.95">RAYMOND</div>
<div class="e ab" data-w="470" style="left:140px;top:345px;font-size:130px;transform:rotate(-1deg);color:#111;line-height:.95">SWANLAND</div>
<svg class="e" style="left:150px;top:490px" width="460" height="36"><path d="M8 28 C 150 14, 300 18, 450 6" stroke="#C2186E" stroke-width="10" fill="none" stroke-linecap="round"/></svg>
<div class="e" style="left:700px;top:715px;width:290px;font-family:BC;font-size:44px;line-height:1.02;color:#111;text-align:center;transform:rotate(-2deg);white-space:normal">Desde 2007, Swanland já fez mais de<br><span style="font-family:AB;font-size:100px;color:#C2186E;line-height:1.05">200</span><br>artes para Magic.</div>
<svg class="e" style="left:700px;top:1000px" width="270" height="30"><path d="M6 22 C 90 12, 180 16, 262 6" stroke="#C2186E" stroke-width="9" fill="none" stroke-linecap="round"/></svg>
'''
claro='''
<div class="e" style="left:150px;top:610px;font-family:CB;font-size:72px;line-height:.98;color:#F4EAD2;transform:rotate(-5deg);text-shadow:0 2px 8px rgba(0,0,0,.8)">Feras, dragões<br>e tempestades</div>
<div class="e rb" data-w="800" style="left:540px;transform:translateX(-50%) rotate(-1deg);top:1112px;font-size:58px;color:#F2E6CC;text-align:center">Estreou em <y>Future Sight</y> e<br>pintou o <y>Ugin</y> de Fate Reforged.</div>
<div style="position:absolute;left:96px;top:1050px;font-family:Geist;font-size:13px;color:#fff;text-shadow:0 1px 3px #000;opacity:.9">Arte: Etali, Primal Storm (Foundations, 2024), nº 329 · Raymond Swanland · © Wizards of the Coast</div>
'''
asyncio.run(camada(tinta,'_tinta.png')); asyncio.run(camada(claro,'_claro.png'))
out=aplicar(base,'_tinta.png','_claro.png'); out[1228:1262,170:250]=out[1228:1262,260:340]; cv2.imwrite('swan_2b.png',out) #,aplicar(base,'_tinta.png','_claro.png'))
