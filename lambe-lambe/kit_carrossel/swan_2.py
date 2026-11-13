import asyncio, cv2, sys, numpy as np
sys.path.insert(0,'.')
from compor import *
base=cv2.imread('modelo_editorial.png')
base=pintura(base,'mask_pintura_2.png','swan_vengevine.jpg',foco=(0.35,0.4),sat=1.35)
hsvb=None
# papel de fundo da carta (lugar do retrato da referência)
p=cv2.resize(cv2.imread('kit_papel.png'),(400,560)); base=colar(base,p,rasgo_alpha(400,560,14,5),830,345,3)
c=cv2.imread('/home/claude/ll/v3/cartas/swan_vengevine.png'); c=cv2.resize(c,(320,int(320*c.shape[0]/c.shape[1])),interpolation=cv2.INTER_AREA)
ca=np.zeros(c.shape[:2],np.uint8); cv2.rectangle(ca,(0,0),(c.shape[1],c.shape[0]),255,-1)
ca=cv2.GaussianBlur(ca,(0,0),.6)
base=colar(base,c,ca,832,345,3)
base[1225:1260,160:240]=base[1225:1260,250:330]
base=fita(base,690,118,-35,150); base=fita(base,975,140,38,150)
tinta='''
<div class="e ab" data-w="470" style="left:140px;top:215px;font-size:130px;transform:rotate(-1deg);color:#111;line-height:.95">RAYMOND</div>
<div class="e ab" data-w="470" style="left:140px;top:345px;font-size:130px;transform:rotate(-1deg);color:#111;line-height:.95">SWANLAND</div>
<svg class="e" style="left:150px;top:490px" width="460" height="36"><path d="M8 28 C 150 14, 300 18, 450 6" stroke="#C2186E" stroke-width="10" fill="none" stroke-linecap="round"/></svg>
<div class="e" style="left:700px;top:700px;width:290px;font-family:BC;font-size:44px;line-height:1.02;color:#111;text-align:center;transform:rotate(-2deg);white-space:normal">Desde 2007, Swanland já fez mais de<br><span style="font-family:AB;font-size:100px;color:#C2186E;line-height:1.05">200</span><br>artes para Magic.</div>
<svg class="e" style="left:700px;top:1000px" width="270" height="30"><path d="M6 22 C 90 12, 180 16, 262 6" stroke="#C2186E" stroke-width="9" fill="none" stroke-linecap="round"/></svg>
'''
claro='''
<div class="e" style="left:150px;top:600px;font-family:CB;font-size:70px;line-height:.98;color:#F4EAD2;transform:rotate(-5deg);text-shadow:0 2px 8px rgba(0,0,0,.75)">Dragões e criaturas<br>em movimento</div>
<div class="e rb" data-w="800" style="left:540px;transform:translateX(-50%) rotate(-1deg);top:1112px;font-size:58px;color:#F2E6CC;text-align:center">Estreou em <y>Future Sight</y> e<br>pintou o <y>Ugin</y> de Fate Reforged.</div>
<div style="position:absolute;left:96px;top:1050px;font-family:Geist;font-size:13px;color:#fff;text-shadow:0 1px 3px #000;opacity:.9">Arte e carta: Vengevine (Rise of the Eldrazi, 2010), nº 212 · Raymond Swanland · © Wizards of the Coast</div>
'''
asyncio.run(camada(tinta,'_tinta.png')); asyncio.run(camada(claro,'_claro.png'))
cv2.imwrite('swan_2.png',aplicar(base,'_tinta.png','_claro.png'))
