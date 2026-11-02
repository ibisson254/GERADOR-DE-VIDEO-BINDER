import numpy as np, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H=1080,1920
F='/home/claude/prod/fontes/'
INK=(21,19,26); PAPER=(255,247,234); CREAM=(255,241,214); PINK=(243,163,203); GROUT=(249,199,225)
POP=dict(yellow=(255,210,63),red=(255,61,46),blue=(44,107,255),sky=(108,201,255),rose=(255,95,168),orange=(255,138,42),purple=(122,92,255),navy=(35,40,107))
def font(n,s): return ImageFont.truetype(F+n,s)
def noise(w,h,cell,rng):
    a=rng.random((max(2,h//cell+2),max(2,w//cell+2)))
    return np.asarray(Image.fromarray((a*255).astype('uint8')).resize((w,h),Image.BICUBIC),dtype=np.float32)/255
def fbm(w,h,rng,cells=(64,24,8,3),amps=(.5,.27,.15,.08)):
    return sum(a*noise(w,h,c,rng) for c,a in zip(cells,amps))
def paper(w,h,color,seed,margin=26,fiber=True,tornamp=26,print_fn=None):
    """Papel rasgado RGBA com fibras, rugas e grão. print_fn(PIL RGB) imprime dentro."""
    rng=np.random.default_rng(seed); M=margin+tornamp
    TW,TH=w+2*M,h+2*M
    yy,xx=np.mgrid[0:TH,0:TW].astype(np.float32)
    d=np.minimum.reduce([xx-M,yy-M,TW-M-xx,TH-M-yy])
    n=fbm(TW,TH,rng,(90,30,10,3),(.5,.3,.14,.06))-.5
    dd=d+n*tornamp*1.6
    a=np.clip(dd+.5,0,1)
    im=Image.new('RGB',(TW,TH),color)
    if print_fn: print_fn(im,M)
    rgb=np.asarray(im,dtype=np.float32).copy()
    wr=np.asarray(Image.fromarray(((fbm(TW,TH,rng,(220,80),(.7,.3)))*255).astype('uint8')).filter(ImageFilter.GaussianBlur(6)),dtype=np.float32)/255-.5
    gx=np.gradient(wr,axis=1)*40
    shade=1+np.clip(wr*.10+gx*.6,-.07,.05)
    grain=1+(rng.random((TH,TW))-.5)*.05
    rgb*=(shade*grain)[...,None]
    if fiber:
        fw=3+fbm(TW,TH,rng,(14,5),(.7,.3))*11
        m=np.clip((fw-dd)/2,0,1)[...,None]
        rgb=rgb*(1-m)+np.array(PAPER,dtype=np.float32)*(.97+.03*rng.random((TH,TW,1)))*m
    out=np.dstack([np.clip(rgb,0,255),a*255]).astype('uint8')
    return Image.fromarray(out,'RGBA')
def with_shadow(sp,off=(10,14),blur=12,alpha=.42):
    e=40; w,h=sp.size
    c=Image.new('RGBA',(w+2*e,h+2*e),(0,0,0,0))
    s=Image.new('L',c.size,0); s.paste(sp.getchannel('A').point(lambda v:int(v*alpha)),(e+off[0],e+off[1]))
    s=s.filter(ImageFilter.GaussianBlur(blur))
    sh=Image.new('RGBA',c.size,(20,8,18,0)); sh.putalpha(s)
    c=Image.alpha_composite(c,sh); c.alpha_composite(sp,(e,e)); return c
def halftone(im,color,seed,step=26,box=None):
    x0,y0,x1,y1=box or (0,0,*im.size); dr=ImageDraw.Draw(im); r=random.Random(seed)
    cx,cy=r.uniform(x0,x1),r.uniform(y0,y1); D=math.hypot(x1-x0,y1-y0)
    for j,y in enumerate(range(y0,y1,step)):
        for x in range(x0+(j%2)*step//2,x1,step):
            q=1-math.hypot(x-cx,y-cy)/D; rad=max(0,(q**1.6)*step*.62)
            if rad>1: dr.ellipse([x-rad,y-rad,x+rad,y+rad],fill=color)
def burst(size,color,seed,points=14,edge=None):
    r=random.Random(seed); S=size*2; c=S/2
    pts=[]
    for i in range(points*2):
        a=i*math.pi/points+r.uniform(-.06,.06); R=(S*.49 if i%2==0 else S*.3)*r.uniform(.86,1)
        pts.append((c+R*math.cos(a),c+R*math.sin(a)))
    im=Image.new('RGBA',(S,S),(0,0,0,0)); d=ImageDraw.Draw(im)
    if edge: d.polygon(pts,fill=edge+(255,)); pts=[(c+(x-c)*.9,c+(y-c)*.9) for x,y in pts]
    d.polygon(pts,fill=color+(255,))
    return im.resize((size,size),Image.LANCZOS)
def tape(w=96,h=34,ang=35,seed=1):
    r=np.random.default_rng(seed)
    a=np.zeros((h,w,4),dtype=np.float32); a[...,:3]=(244,232,190); a[...,3]=150+r.random((h,w))*22
    a[:,:3,3]*=r.random((h,1))>.4; a[:,-3:,3]*=r.random((h,1))>.4
    return Image.fromarray(a.astype('uint8'),'RGBA').rotate(ang,expand=True,resample=Image.BICUBIC)
_c={}
def card_img(n,w):
    k=(n,w)
    if k not in _c:
        im=Image.open(f'/home/claude/prod/cartas/{n}.png').convert('RGBA')
        _c[k]=im.resize((w,round(w*1040/744)),Image.LANCZOS)
    return _c[k]
def card_poster(n,w,ang,seed,paper_color=PAPER,tear=14):
    """Cartaz: papel + carta inteira + fita só nos cantos de cima do papel, fora da carta. Devolve sprite e cantos da carta no sprite."""
    c=card_img(n,w); cw,ch=c.size
    mx,mt,mb=max(30,w//11),max(40,w//8),max(24,w//14)
    sp=paper(cw+2*mx,ch+mt+mb,paper_color,seed,margin=4,tornamp=tear,fiber=True)
    M=4+tear; ox,oy=M+mx,M+mt
    sp.alpha_composite(c,(ox,oy))
    if w>=300:
        sc=min(1,w/560)
        t1=tape(int(96*sc),int(32*sc),32,seed); t2=tape(int(96*sc),int(32*sc),-32,seed+1)
        tw,th=t1.size
        sp.alpha_composite(t1,(M-int(14*sc),M-int(16*sc)))
        sp.alpha_composite(t2,(sp.size[0]-M-tw+int(14*sc),M-int(16*sc)))
    s=with_shadow(sp,(8,12),10)
    e=40; corners=[(ox+e,oy+e),(ox+e+cw,oy+e),(ox+e+cw,oy+e+ch),(ox+e,oy+e+ch)]
    if ang:
        w0,h0=s.size; r=s.rotate(ang,expand=True,resample=Image.BICUBIC); w1,h1=r.size
        A=math.radians(ang); ca,sa=math.cos(A),math.sin(A)
        corners=[(w1/2+(x-w0/2)*ca+(y-h0/2)*sa, h1/2-(x-w0/2)*sa+(y-h0/2)*ca) for x,y in corners]
        s=r
    return s,corners
def text_poster(lines,color,seed,width,ang=0,ink=INK,accent=None,pad=(50,36)):
    """lines: [(texto, fonte, tamanho_max)] ajustado à largura."""
    L=[]; iw=width-2*pad[0]
    for t,fn,sz in lines:
        f=font(fn,sz)
        while f.getlength(t)>iw: sz-=2; f=font(fn,sz)
        b=f.getbbox(t); L.append((t,f,b,sz))
    gap=[int(l[3]*.10) for l in L]
    h=sum(l[2][3]-l[2][1] for l in L)+sum(gap[:-1])+2*pad[1]
    def pr(im,M):
        halftone(im,tuple(int(c*.95) for c in color),seed,24) if color!=PAPER and color!=CREAM else None
        d=ImageDraw.Draw(im); y=M+pad[1]
        for (t,f,b,sz),g in zip(L,gap):
            x=M+(width-(b[2]-b[0]))/2-b[0]
            if accent and sz>=70: d.text((x+max(4,sz//24),y-b[1]+max(4,sz//24)),t,font=f,fill=accent)
            d.text((x,y-b[1]),t,font=f,fill=ink); y+=b[3]-b[1]+g
    sp=with_shadow(paper(width,h,color,seed,margin=10,tornamp=18,print_fn=pr),(10,14),12)
    if ang: sp=sp.rotate(ang,expand=True,resample=Image.BICUBIC)
    return sp
