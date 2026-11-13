"""Compõe um slide a partir de um modelo limpo do kit: python3 -I compor.py (usa specs em código)"""
import numpy as np, cv2, os, sys, json, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import transferir_textura
from playwright.async_api import async_playwright
CSS = '''@font-face{font-family:AB;src:url(fontes/archivo-black-latin-400-normal.woff2)}
@font-face{font-family:BC;src:url(fontes/barlow-condensed-latin-800-normal.woff2)}
@font-face{font-family:RB;src:url(fontes/rubik-latin-800-normal.woff2);font-weight:800}
@font-face{font-family:RB;src:url(fontes/rubik-latin-900-italic.woff2);font-weight:900;font-style:italic}
@font-face{font-family:CB;src:url(fontes/caveat-brush-latin-400-normal.woff2)}
@font-face{font-family:Geist;src:url(fontes/Geist-Medium.woff2);font-weight:500}
@font-face{font-family:Geist;src:url(fontes/Geist-Bold.woff2);font-weight:700}
*{margin:0;padding:0}html,body{background:transparent}
#s{width:1080px;height:1350px;position:relative}
.e{position:absolute;white-space:nowrap;-webkit-mask-image:url(fontes/desgaste.png);-webkit-mask-size:520px}
.ab{font-family:AB;text-transform:uppercase;letter-spacing:-1px;line-height:.9;-webkit-text-stroke:3px currentColor}
.bc{font-family:BC;text-transform:uppercase;line-height:1.02}
.rb{font-family:RB;font-weight:800;line-height:1.08}
.rb y{font-weight:900;font-style:italic;color:#F4B21A}
'''
async def camada(html, saida):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg = await b.new_page(viewport={"width":1080,"height":1350})
        f = os.path.abspath("_camada.html"); open(f,"w").write(f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body><div id='s'>{html}</div><script>window.fit=()=>document.querySelectorAll('[data-w]').forEach(e=>{{let s=parseFloat(e.style.fontSize);const r=()=>{{const g=document.createRange();g.selectNodeContents(e);return g.getBoundingClientRect().width}};while(r()>+e.dataset.w&&s>20){{s-=2;e.style.fontSize=s+'px'}}}});</script></body></html>")
        await pg.goto("file://"+f); await pg.evaluate("document.fonts.ready"); await pg.evaluate("fit()"); await pg.wait_for_timeout(300)
        await pg.locator("#s").screenshot(path=saida, omit_background=True); await b.close()
def aplicar(base, tinta_png, claro_png=None):
    """tinta escura em multiplicação (pega a textura do papel); tinta clara em normal com grão"""
    out = base.astype(np.float32)
    t = cv2.imread(tinta_png, cv2.IMREAD_UNCHANGED).astype(np.float32)
    a = cv2.GaussianBlur(t[...,3]/255.0,(0,0),0.6)[...,None]; c = t[...,:3]/255.0
    out = out*(1-a) + out*c*a*1.08
    if claro_png:
        t = cv2.imread(claro_png, cv2.IMREAD_UNCHANGED).astype(np.float32)
        a = cv2.GaussianBlur(t[...,3]/255.0,(0,0),0.6)[...,None]; c = t[...,:3]
        lum = cv2.GaussianBlur(base.astype(np.float32).mean(2),(0,0),1)
        tex = 0.88 + 0.5*((lum - cv2.GaussianBlur(lum,(0,0),4))/255.0)[...,None]
        out = out*(1-a) + np.clip(c*tex,0,255)*a
    return np.clip(out,0,255).astype(np.uint8)
def pintura(base, mask_png, arte, foco=(0.5,0.5), k=0.9, sat=1.12):
    m = cv2.imread(mask_png,0); ys,xs = np.where(m>0); x0,x1,y0,y1 = xs.min(),xs.max()+1,ys.min(),ys.max()+1
    a = cv2.imread(arte); ah,aw = a.shape[:2]; W,H = x1-x0,y1-y0; s = max(W/aw,H/ah)
    a = cv2.resize(a,(int(aw*s)+1,int(ah*s)+1),interpolation=cv2.INTER_LANCZOS4)
    ox = int((a.shape[1]-W)*foco[0]); oy = int((a.shape[0]-H)*foco[1]); a = a[oy:oy+H,ox:ox+W]
    hsv = cv2.cvtColor(a,cv2.COLOR_BGR2HSV).astype(np.float32); hsv[...,1] = np.clip(hsv[...,1]*sat,0,255); a = cv2.cvtColor(hsv.astype(np.uint8),cv2.COLOR_HSV2BGR)
    a = np.clip((a.astype(np.float32)-128)*1.12+128,0,255).astype(np.uint8)
    velha = base[y0:y1,x0:x1]
    nova = transferir_textura(a, velha, None, k)
    mm = (cv2.GaussianBlur(m[y0:y1,x0:x1],(0,0),0.8)/255.0)[...,None]
    out = base.copy(); out[y0:y1,x0:x1] = (velha*(1-mm) + nova*mm).astype(np.uint8)
    return out

def rasgo_alpha(w, h, amp=10, seed=3):
    """máscara de papel rasgado (passeio aleatório nas 4 bordas)"""
    rng = np.random.default_rng(seed); m = np.zeros((h,w),np.uint8); pts=[]; v=amp/2
    def d():
        nonlocal v; v=float(np.clip(v+rng.normal(0,amp*.3),amp*.1,amp)); return v+rng.normal(0,amp*.12)
    for x in range(0,w,3): pts.append((x,d()))
    for y in range(0,h,3): pts.append((w-d(),y))
    for x in range(w,0,-3): pts.append((x,h-d()))
    for y in range(h,0,-3): pts.append((d(),y))
    cv2.fillPoly(m,[np.array(pts,np.int32)],255); return m
def colar(base, img, alpha, cx, cy, ang=0, sombra=True):
    """cola img (BGR) com alpha (0-255) centrada em (cx,cy), rodada ang graus, com sombra"""
    h,w = img.shape[:2]; D=int(np.hypot(w,h))+40
    can = np.zeros((D,D,3),np.uint8); al=np.zeros((D,D),np.uint8)
    ox,oy=(D-w)//2,(D-h)//2; can[oy:oy+h,ox:ox+w]=img; al[oy:oy+h,ox:ox+w]=alpha
    R=cv2.getRotationMatrix2D((D/2,D/2),-ang,1)
    can=cv2.warpAffine(can,R,(D,D),flags=cv2.INTER_LANCZOS4); al=cv2.warpAffine(al,R,(D,D),flags=cv2.INTER_LINEAR)
    x0,y0=int(cx-D/2),int(cy-D/2); out=base.astype(np.float32)
    def blend(src,a,dx=0,dy=0,op=1.0,cor=None):
        X0,Y0=x0+dx,y0+dy; xs,ys=max(0,X0),max(0,Y0); xe,ye=min(out.shape[1],X0+D),min(out.shape[0],Y0+D)
        A=(a[ys-Y0:ye-Y0,xs-X0:xe-X0]/255.0*op)[...,None]
        S=np.full_like(out[ys:ye,xs:xe],cor) if cor is not None else src[ys-Y0:ye-Y0,xs-X0:xe-X0].astype(np.float32)
        out[ys:ye,xs:xe]=out[ys:ye,xs:xe]*(1-A)+S*A
    if sombra:
        sh=cv2.GaussianBlur(al,(0,0),9); blend(None,sh,6,12,0.55,(20,0,10))
    blend(can,al)
    return np.clip(out,0,255).astype(np.uint8)
def fita(base, cx, cy, ang, larg=150):
    t=cv2.imread('kit_fita.png'); hsv=cv2.cvtColor(t,cv2.COLOR_BGR2HSV)
    rosa=(hsv[...,1]>85)&((hsv[...,0]>135)|(hsv[...,0]<10))
    a=np.where(~rosa&(hsv[...,2]>120),255,0).astype(np.uint8); a=cv2.morphologyEx(a,cv2.MORPH_CLOSE,np.ones((7,7),np.uint8)); a=cv2.morphologyEx(a,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
    n,lab,st,_=cv2.connectedComponentsWithStats(a); k=1+np.argmax(st[1:,4]); a=np.where(lab==k,255,0).astype(np.uint8)
    a=cv2.GaussianBlur(a,(0,0),1)
    hs=cv2.cvtColor(t,cv2.COLOR_BGR2HSV); hs[...,1]=(hs[...,1]*0.35).astype(np.uint8); t=cv2.cvtColor(hs,cv2.COLOR_HSV2BGR)
    s=larg/t.shape[1]; t=cv2.resize(t,None,fx=s,fy=s); a=cv2.resize(a,None,fx=s,fy=s)
    return colar(base,t,a,cx,cy,ang,sombra=False)
