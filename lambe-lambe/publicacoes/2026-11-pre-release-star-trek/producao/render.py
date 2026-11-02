#!/usr/bin/env python3
"""Lambe-lambe · Pré-release Invasion. Renderiza os 484 quadros originais (sem o fecho).
Uso: render.py --frames 0,40,... (provas PNG) | render.py --master saida.mkv"""
import sys, json, math, random, subprocess, argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0,'/home/claude/prod')
from lib import *
WW,WH=1500,2640
K=dict(kirk='142',spock='74',data='69',khan='119',jane='187',q='165',ent='43',worf='180')

def base_wall():
    rng=np.random.default_rng(7)
    n=fbm(WW,WH,rng,(300,90,30,8),(.5,.28,.15,.07))
    rgb=np.ones((WH,WW,3),dtype=np.float32)*np.array(PINK,dtype=np.float32)
    rgb*= (1+(n-.5)[...,None]*.16)
    # rejunte de placas
    im=Image.fromarray(rgb.astype('uint8')); d=ImageDraw.Draw(im)
    for y in range(0,WH,340):
        d.line([(0,y),(WW,y+rng.integers(-6,6))],fill=GROUT,width=5)
        for x in range((y//340%2)*260,WW,520): d.line([(x,y),(x,y+340)],fill=GROUT,width=5)
    # restos de cartazes antigos
    r=random.Random(3)
    cols=list(POP.values())+[CREAM,PAPER]
    for i in range(34):
        c=r.choice(cols); w,h=r.randint(180,560),r.randint(120,520)
        def pr(m,M,c=c,i=i):
            if i%2==0: halftone(m,tuple(int(v*.84) for v in c),i,22)
        s=paper(w,h,c,100+i,margin=8,tornamp=40,print_fn=pr).rotate(r.uniform(-14,14),expand=True,resample=Image.BILINEAR)
        s.putalpha(s.getchannel('A').point(lambda v:int(v*.8)))
        im.paste(s,(r.randint(-120,WW-120),r.randint(-120,WH-140)),s)
    # tinta lascada, cola, tags sem texto
    a=np.asarray(im,dtype=np.float32).copy()
    chips=fbm(WW,WH,rng,(36,12,4),(.5,.3,.2))
    m=np.clip((chips-.70)*22,0,1)[...,None]
    a=a*(1-m*.55)+np.array(GROUT,dtype=np.float32)*m*.55
    glue=np.clip(fbm(WW,WH,rng,(420,120,30),(.6,.3,.1))-.52,0,1)*1.1
    a=a+glue[...,None]*38
    a*=(1+(rng.random((WH,WW,1))-.5)*.05)
    im=Image.fromarray(np.clip(a,0,255).astype('uint8')); d=ImageDraw.Draw(im)
    for i in range(12):
        x,y=r.randint(0,WW),r.randint(0,WH); pts=[(x+r.randint(-130,130),y+r.randint(-70,70)) for _ in range(5)]
        d.line(pts,fill=r.choice([INK,POP['navy'],POP['red']]),width=r.randint(5,9),joint='curve')
    # calçada
    y0=WH-300
    for y in range(y0,WH,62):
        for x in range(-(y%2)*30,WW,92):
            v=r.randint(150,190); d.rounded_rectangle([x,y,x+86,y+56],9,fill=(v,v-4,v-10))
    return im.filter(ImageFilter.GaussianBlur(.5))

BASE=None; WALLS={}
def wall(col,seed):
    k=(col,seed)
    if k in WALLS: return WALLS[k]
    im=BASE.copy()
    if col:
        c=POP[col]; r=random.Random(seed)
        w,h=r.randint(1060,1200),r.randint(1500,1760)
        dark=tuple(int(v*.82) for v in c)
        s=paper(w,h,c,500+seed,margin=10,tornamp=56,print_fn=lambda m,M:halftone(m,dark,seed,30)).rotate(r.uniform(-5,5),expand=True,resample=Image.BICUBIC)
        s=with_shadow(s,(14,18),16)
        im.paste(s,((WW-s.size[0])//2+r.randint(-170,170),(WH-s.size[1])//2+r.randint(-140,100)),s)
    WALLS[k]=im; return im

def item_card(key,w,ang,cx,cy,t=0,fx='slam',seed=None,drift=(0,0),pc=PAPER,tear=14):
    n=K[key]; sp,co=card_poster(n,w,ang,seed or (hash(key+str(w))%9000+int(cx)),pc,tear)
    mx=sum(p[0] for p in co)/4; my=sum(p[1] for p in co)/4
    return dict(kind='card',sp=sp,x=round(cx-mx),y=round(cy-my),t=t,fx=fx,corners=co,n=n,drift=drift,w=w,ang=ang)
def item_text(sp,cx,cy,t=0,fx='slam',drift=(0,0),label=''):
    return dict(kind='text',sp=sp,x=round(cx-sp.size[0]/2),y=round(cy-sp.size[1]/2),t=t,fx=fx,drift=drift,label=label)
def item_scrap(col,w,h,x,y,t,seed,ang=0,from_=(0,0),dur=7,drift=(0,0)):
    s=paper(w,h,POP.get(col,col),seed,margin=6,tornamp=26,print_fn=lambda m,M:halftone(m,tuple(int(v*.85) for v in POP.get(col,col)),seed,20))
    s=with_shadow(s,(8,10),9)
    if ang: s=s.rotate(ang,expand=True,resample=Image.BILINEAR)
    return dict(kind='scrap',sp=s,x=x,y=y,t=t,fx='slide',frm=from_,dur=dur,drift=drift)
def item_burst(col,size,cx,cy,t,life,seed,edge=INK):
    return dict(kind='burst',sp=burst(size,POP[col],seed,edge=edge),x=cx-size//2,y=cy-size//2,t=t,life=life,fx='pop',drift=(0,0))
def item_fall(col,w,h,x,y,t,seed):
    i=item_scrap(col,w,h,x,y,t,seed,ang=-8); i['fx']='fall'; return i

def build():
    S=[]
    def shot(s,e,col,seed,items,cam,tr='tear',dirn=0):
        S.append(dict(s=s,e=e,col=col,seed=seed,items=items,cam=cam,tr=tr,dirn=dirn))
    # BLOCO A · impacto
    ta=text_poster([('ATENÇÃO,','Bangers.ttf',230),('TRIPULAÇÃO!','Bangers.ttf',230)],POP['yellow'],11,900,-2,accent=POP['rose'])
    shot(0,24,None,1,[item_fall('sky',420,300,620,240,3,21),item_fall('orange',300,420,30,1380,7,22),
        item_burst('rose',1050,470,860,0,24,5),item_text(ta,470,860,0,'slam',(0,0),'ATENÇÃO, TRIPULAÇÃO!'),
        item_scrap('red',700,120,160,1300,10,23,3,(0,380),6)],(1.02,1.10,0,0,0,-30,.5))
    # BLOCO B · invasão (cortes sincopados)
    b=[('kirk',700,-2,470,800,'red',28,'yellow'),('spock',640,3,500,770,'blue',16,None),('data',640,-3,440,850,'sky',16,None),
       ('khan',700,2,470,790,'purple',28,'orange'),('ent',700,-2,470,800,'navy',24,'sky'),('jane',620,3,440,750,'yellow',16,None),
       ('q',620,-3,500,860,'rose',16,None),('worf',680,2,470,800,'orange',20,'red')]
    f=24
    for i,(k,w,a,cx,cy,col,d,bc) in enumerate(b):
        it=[item_scrap(['yellow','sky','rose','orange'][i%4],520,170,-60 if i%2 else 620,250+i*90,2,40+i,(-1)**i*6,(-500 if i%2 else 500,0),6),
            item_scrap(['blue','red','purple','yellow'][i%4],460,160,640 if i%2 else -40,1440-i*40,5,60+i,(-1)**i*-5,(420 if i%2 else -420,0),6)]
        if bc: it.append(item_burst(bc,1180,cx,cy,0,d,70+i))
        it.append(item_card(k,w,a,cx,cy,0,'slam' if d>=20 else 'nudge',800+i,(0,0)))
        zs=(1.06,1.16) if i%2==0 else (1.2,1.1)
        shot(f,f+d,col,10+i,it,(zs[0],zs[1],(-1)**i*30,(-1)**i*-20,(-1)**i*-30,(-1)**i*30,(-1)**i*.9),'tear' if i%3!=2 else 'cut',i%2); f+=d
    # dupla final do bloco B
    shot(f,f+16,'red',30,[item_burst('yellow',720,250,500,0,16,90),item_card('kirk',380,-3,250,500,0,'slam',830),
        item_burst('sky',720,690,1160,2,14,91),item_card('spock',380,3,690,1160,2,'slam',831)],(1.12,1.2,0,0,20,20,-.6),'cut'); f+=16
    assert f==204,f
    # BLOCO C · identidade
    t1=text_poster([('STAR TREK','Bangers.ttf',222),('× MAGIC','Bangers.ttf',222)],POP['red'],12,900,1.5,ink=PAPER,accent=INK)
    top=[('khan',170),('ent',470),('jane',770)]; bot=[('data',170),('q',470),('worf',770)]
    its=[item_scrap('sky',380,160,-30,600,8,120,4,(-400,0),6),item_scrap('yellow',360,150,720,1100,12,121,-4,(400,0),6)]
    for j,(k,x) in enumerate(top): its.append(item_card(k,232,(-1)**j*2,x,400,6+j*6,'pop',840+j))
    for j,(k,x) in enumerate(bot): its.append(item_card(k,232,(-1)**(j+1)*2,x,1368,24+j*6,'pop',850+j))
    its.insert(2,item_text(t1,470,885,0,'slam',(0,0),'STAR TREK × MAGIC'))
    shot(204,252,None,2,its,(1.04,1.12,-20,10,20,-20,.7),'tear',1)
    its=[item_scrap('orange',380,160,700,580,4,122,-4,(400,0),6)]
    for j,(k,x) in enumerate([('kirk',170),('spock',470),('q',770)]): its.append(item_card(k,232,(-1)**(j+1)*2,x,400,0+j*5,'pop',860+j))
    for j,(k,x) in enumerate([('ent',170),('khan',470),('jane',770)]): its.append(item_card(k,232,(-1)**j*2,x,1368,14+j*5,'pop',870+j))
    its.insert(1,item_text(t1,470,885,0,'none',(0,0),'STAR TREK × MAGIC'))
    shot(252,300,'blue',31,its,(1.12,1.02,20,-20,-20,10,-.7),'cut')
    # BLOCO D · convocação (2×2 acelerado)
    g=[('worf','kirk','ent','jane'),('spock','khan','q','data'),('jane','worf','kirk','ent'),('data','q','khan','spock'),('ent','jane','worf','kirk'),('q','spock','data','khan')]
    cols=['yellow','rose','sky','orange','purple','red']; f=300
    for i,ks in enumerate(g):
        d=[12,9,9,9,8,7][i]; ps=[(262,525),(678,525),(262,1110),(678,1110)]
        it=[item_card(k,376,(-1)**(q)*1.5*(-1)**i,x,y,0,'none',900+i*4+q,tear=8) for q,(k,(x,y)) in enumerate(zip(ks,ps))]
        shot(f,f+d,cols[i],40+i,it,(1.05+.03*i,1.12+.03*i,(-1)**i*30,0,(-1)**i*-30,20,(-1)**i*.8),'cut'); f+=d
    assert f==354,f
    t2=text_poster([('A PRÓXIMA','Bangers.ttf',150),('MISSÃO','Bangers.ttf',185),('É NA MESA.','Bangers.ttf',150)],POP['yellow'],13,880,-1.5,accent=POP['rose'])
    its=[]
    for j,k in enumerate(['kirk','khan','ent','q']): its.append(item_card(k,180,(-1)**j*2,145+j*222,368,2+j*2,'pop',880+j,tear=7))
    for j,k in enumerate(['spock','jane','worf','data']): its.append(item_card(k,180,(-1)**(j+1)*2,145+j*222,1400,10+j*2,'pop',890+j,tear=7))
    its.insert(0,item_text(t2,470,890,0,'slam',(0,0),'A PRÓXIMA MISSÃO É NA MESA.'))
    shot(354,390,None,3,its,(1.04,1.14,0,-20,0,20,.5),'tear',0)
    # BLOCO E · chamada final (mais lento, para ler)
    t3=text_poster([('PRÉ-RELEASE','Bangers.ttf',240)],(5,10,16) if False else POP['rose'],14,900,-1.5,accent=PAPER)
    t4=text_poster([('6 A 12 DE NOVEMBRO','Bangers.ttf',118),('DE 2026','Bangers.ttf',150)],POP['yellow'],15,860,1,accent=None)
    t5=text_poster([('ENCONTRE UM EVENTO','Bangers.ttf',92),('NA SUA LOJA.','Bangers.ttf',104)],PAPER,16,800,-1)
    t6=text_poster([('Conteúdo de fã não oficial. Não aprovado pela Wizards.','Geist-Medium.ttf',30),('© Wizards of the Coast · Star Trek © CBS','Geist-Medium.ttf',30)],CREAM,17,860,0,pad=(30,30))
    its=[item_scrap('blue',500,170,-60,1000,14,130,5,(-500,0),7),item_scrap('orange',430,170,660,240,22,131,-6,(460,0),7),
         item_text(t3,470,420,0,'slam',(0,0),'PRÉ-RELEASE'),item_text(t4,470,760,16,'slam',(0,0),'6 A 12 DE NOVEMBRO DE 2026'),
         item_text(t5,470,1095,36,'slam',(0,0),'ENCONTRE UM EVENTO NA SUA LOJA.'),item_text(t6,470,1400,50,'none',(0,0),'aviso')]
    shot(390,484,None,4,its,(1.02,1.09,0,10,0,-10,.3),'tear',1)
    assert S[-1]['e']==484
    return S

def ease(x): return 1-(1-x)**3
def draw_items(fr,sh,f,rec):
    for it in sh['items']:
        a=f-sh['s']-it['t']
        if a<0: continue
        if it['kind']=='burst' and a>=it['life']: continue
        sp=it['sp']; x,y=it['x'],it['y']; settled=True
        fx=it['fx']
        if fx in('slam','pop'):
            sc={'slam':[1.13,1.07,1.02],'pop':[1.1,1.03]}[fx]
            if a<len(sc):
                s=sc[a]; w,h=sp.size; n=sp.resize((round(w*s),round(h*s)),Image.BILINEAR)
                x-=(n.size[0]-w)//2; y-=(n.size[1]-h)//2; sp=n; settled=False
        elif fx=='nudge':
            if a<3: x+=[-46,-18,-5][a]*(1 if sh['s']%2 else -1); settled=False
        elif fx=='slide':
            p=min(1,(a+1)/it['dur']); e=ease(p)
            x+=round(it['frm'][0]*(1-e)); y+=round(it['frm'][1]*(1-e))
        elif fx=='fall':
            x+=round(a*a*1.4*.25); y+=round(a*a*2.1)
            if a%2==0: sp=sp.rotate(-a*1.3,expand=True,resample=Image.BILINEAR)
        elif fx=='pop' : pass
        if it['kind']=='burst':
            if a>=it['life']-2: sp=sp.resize((sp.size[0]*11//10,sp.size[1]*11//10)); 
        x+=round(it['drift'][0]*a); y+=round(it['drift'][1]*a)
        fr.paste(sp,(x,y),sp)
        if it['kind']=='card' and rec is not None:
            rec.append(dict(n=it['n'],settled=settled,w=it['w'],ang=it['ang'],corners=[(round(px+x,1),round(py+y,1)) for px,py in it['corners']]))
        if it['kind']=='text' and rec is not None:
            rec.append(dict(text=it['label'],box=[x,y,x+sp.size[0],y+sp.size[1]]))

def cam_frame(sh,f):
    z0,z1,px0,py0,px1,py1,rot=sh['cam']; t=(f-sh['s'])/max(1,sh['e']-sh['s']-1)
    z=z0+(z1-z0)*t; px=px0+(px1-px0)*t; py=py0+(py1-py0)*t
    k=f-sh['s']; imp=math.exp(-k/2.6)
    r=random.Random(f*7+1); sx=(r.uniform(-1,1))*22*imp; sy=(r.uniform(-1,1))*22*imp
    A=math.radians(rot*(t-.5)*2+r.uniform(-1,1)*.5*imp); c,s=math.cos(A)/z,math.sin(A)/z
    cx,cy=WW/2+px+sx,WH/2+py+sy
    # saída (x,y) -> origem
    a,b,d,e=c,s,-s,c
    tx=cx-a*W/2-b*H/2; ty=cy-d*W/2-e*H/2
    return wall(sh['col'],sh['seed']).transform((W,H),Image.AFFINE,(a,b,tx,d,e,ty),Image.BILINEAR)

def render_shot(sh,f,rec=None):
    fr=cam_frame(sh,f); draw_items(fr,sh,f,rec); return fr

def tear_mix(prev,cur,p,dirn,seed):
    a=np.asarray(prev).copy(); b=np.asarray(cur)
    rng=np.random.default_rng(seed); L=H if dirn==0 else W; O=W if dirn==0 else H
    n=np.asarray(Image.fromarray((rng.random((1,O//24+2))*255).astype('uint8')).resize((O,1),Image.BICUBIC),dtype=np.float32)[0]/255-.5
    n=n*150+(rng.random(O)-.5)*22
    edge=p*(L+320)-160+n
    if dirn==0:
        yy=np.arange(H,dtype=np.float32)[:,None]; d=edge[None,:]-yy
    else:
        xx=np.arange(W,dtype=np.float32)[None,:]; d=edge[:,None]-xx
    m=d>0; fib=(d>-16)&(d<=0)
    a[m]=b[m]; a[fib]=(np.array(PAPER)*(.93+.07*rng.random((fib.sum(),1)))).astype('uint8')
    return a

S=None; SH=None
def frame(f,rec=None):
    i=[k for k,s in enumerate(S) if s['s']<=f<s['e']][0]; sh=S[i]
    k=f-sh['s']
    if sh['tr']=='tear' and i>0 and k<3:
        prev=S[i-1]; p=(k+1)/4
        return Image.fromarray(tear_mix(render_shot(prev,prev['e']-1),render_shot(sh,f),p,sh['dirn'],f)),i
    return render_shot(sh,f,rec),i

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--frames'); ap.add_argument('--master'); a=ap.parse_args()
    BASE=base_wall(); S=build()
    if a.frames:
        for f in map(int,a.frames.split(',')):
            r=[]; im,_=frame(f,r); im.save(f'/home/claude/prod/render/p{f:03d}.jpg',quality=88)
    if a.master:
        p=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','30','-i','-','-c:v','ffv1','-level','3','-threads','2',a.master],stdin=subprocess.PIPE)
        man=[]
        for f in range(484):
            r=[]; im,i=frame(f,r); p.stdin.write(im.tobytes()); man.append(dict(f=f,shot=i,items=r))
            if f%60==0: print(f,flush=True)
        p.stdin.close(); p.wait()
        json.dump(dict(man=man,cuts=[dict(s=s['s'],e=s['e'],tr=s['tr'],col=s['col']) for s in S]),open('/home/claude/prod/render/manifest.json','w'))
