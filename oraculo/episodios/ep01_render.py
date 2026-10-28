import json, math, subprocess, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
W,H,FPS=1080,1920,30
TL=json.load(open('tl.json')); WORDS=json.load(open('words.json'))
TEMPO,LEAD=TL['TEMPO'],TL['LEAD']; TOTAL=TL['TOTAL']; OUT=TL['OUT_START']
def vt(x): return x/TEMPO+LEAD
for w in WORDS: w['vs']=vt(w['s']); w['ve']=vt(w['e'])
ENV=np.load('led_env.npy')
K='/root/kit/'
MASTER=Image.open(K+'oraculo/assets/tubo_mestra_916.png').convert('RGB')
LOGO=Image.open(K+'manaburn/logo/logo_mark.png').convert('RGBA')
SCAN=[Image.open(K+f'comum/outro/scan/{i:03d}.jpg').convert('RGB') for i in range(45)]
F=lambda p,s: ImageFont.truetype(p,s)
MONO='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'; MONOB='/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
INTB='/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'; INTSB='/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf'; INTM='/usr/share/fonts/opentype/inter/Inter-Medium.otf'
BG=(5,10,16); SLATE=(15,23,42); EM=(16,185,129); PH=(0,255,65); WHITE=(236,241,245); DIM=(52,92,72); GREY=(120,140,150)
# geometria da mestra
SCR=(492,566,740,792); SCX,SCY=(SCR[0]+SCR[2])/2,(SCR[1]+SCR[3])/2
EYES=[(518,615,596,702),(634,615,709,702)]; LED=(592,828)
rng=np.random.default_rng(13)
GLY='0123456789ABCDEF#*+=<>/:'
def ease(x): x=min(1,max(0,x)); return x*x*(3-2*x)
def eio(x): x=min(1,max(0,x)); return 1-(1-x)**3
def T(d,xy,s,font,fill,anchor='la',sp=0):
    d.text(xy,s,font=font,fill=fill,anchor=anchor)
def fit(d,s,path,size,maxw):
    while size>20:
        f=F(path,size)
        if d.textlength(s,font=f)<=maxw: return f
        size-=2
    return F(path,size)
# ---------- FORA: TUBO ----------
rain_cols=[dict(x=x,y=rng.uniform(0,300),v=rng.uniform(40,90)) for x in range(500,736,14)]
def tubo_frame(t, expr='analitico', zoom=1.0, cx=None, cy=None, egg=None):
    im=MASTER.copy(); d=ImageDraw.Draw(im,'RGBA')
    # chuva de código animada no ecrã (fora dos olhos)
    fs=F(MONO,13)
    for c in rain_cols:
        y=SCR[1]+((c['y']+t*c['v'])%(SCR[3]-SCR[1]+40))-20
        for k in range(5):
            yy=y-k*15
            if SCR[1]+8<yy<SCR[3]-14 and not any(e[0]-6<c['x']<e[2]+6 and e[1]-8<yy<e[3]+4 for e in EYES):
                a=int(150*(1-k/5)*(0.6 if expr!='desconfiado' else 0.2))
                d.text((c['x'],yy),GLY[int(t*8+k+c['x'])%len(GLY)],font=fs,fill=(0,255,65,a))
    # varrimento CRT
    sy=SCR[1]+((t*120)%(SCR[3]-SCR[1]))
    d.rectangle((SCR[0]+14,sy,SCR[2]-14,sy+5),fill=(16,185,129,22))
    # pálpebras
    lid=0.0
    bt=t%4.3
    if bt<0.14: lid=math.sin(bt/0.14*math.pi)
    if expr=='desconfiado': lid=max(lid,0.45)
    if expr=='confiante': lid=max(lid,0.22)
    if lid>0.01:
        for i,e in enumerate(EYES):
            h=(e[3]-e[1]+4)*lid
            if expr=='confiante' and lid<0.5 and i==1: h*=0.4   # pálpebra diagonal: um olho só
            d.rectangle((e[0]-3,e[1]-3,e[2]+3,e[1]-3+h),fill=BG+(255,))
            d.line((e[0]-3,e[1]-3+h,e[2]+3,e[1]-3+h),fill=(16,185,129,160),width=3)
    # LED = voz
    fi=int(round(t*FPS)); a=float(ENV[fi]) if fi<len(ENV) else 0
    a=min(1,a)
    d.ellipse((LED[0]-7,LED[1]-7,LED[0]+7,LED[1]+7),fill=(8,40,26,255))
    if a>0.03:
        glow=Image.new('RGBA',(120,120),(0,0,0,0)); gd=ImageDraw.Draw(glow)
        gd.ellipse((40,40,80,80),fill=(16,185,129,int(200*a)))
        glow=glow.filter(ImageFilter.GaussianBlur(14))
        im.paste(glow,(LED[0]-60,LED[1]-60),glow)
        d.ellipse((LED[0]-6,LED[1]-6,LED[0]+6,LED[1]+6),fill=(120,255,190,int(80+175*a)))
    # respiração subtil + câmara
    z=max(1.0,zoom)*(1+0.008*(1+math.sin(t*1.3))/2)
    if cx is None: cx,cy=W/2,H/2
    if abs(z-1)>1e-4:
        cw,ch=W/z,H/z; x0=min(max(cx-cw/2,0),W-cw); y0=min(max(cy-ch/2,0),H-ch)
        im=im.resize((W,H),Image.LANCZOS,box=(x0,y0,x0+cw,y0+ch))
    return im
# ---------- DENTRO: terminal ----------
TERM_BG=Image.new('RGB',(W,H),BG)
_sl=Image.new('RGBA',(W,H),(0,0,0,0)); _d=ImageDraw.Draw(_sl)
for y in range(0,H,4): _d.line((0,y,W,y),fill=(0,0,0,60))
vig=Image.new('L',(W,H),0); vd=ImageDraw.Draw(vig); vd.ellipse((-300,-200,W+300,H+200),fill=255); vig=vig.filter(ImageFilter.GaussianBlur(220))
SCANL=_sl
tcols=[dict(x=x,y=rng.uniform(0,H),v=rng.uniform(60,160)) for x in range(30,W,46)]
def term_base(t, egg=False):
    im=TERM_BG.copy(); d=ImageDraw.Draw(im,'RGBA'); fs=F(MONO,24)
    for i,c in enumerate(tcols):
        y=(c['y']+t*c['v'])%(H+200)-100
        for k in range(9):
            ch=GLY[int(t*6+k*3+c['x'])%len(GLY)]
            d.text((c['x'],y-k*30),ch,font=fs,fill=(0,255,65,int(36*(1-k/9))))
    if egg:  # easter egg: "GG FEVOLD" na chuva, coluna 3
        s='GG·FEVOLD'
        for k,ch in enumerate(s): d.text((tcols[17]['x'],700+k*30),ch,font=fs,fill=(0,255,65,70))
    return im,d
def term_finish(im,t):
    im=Image.composite(im,Image.new('RGB',(W,H),(0,0,0)),vig)
    im.paste(SCANL,(0,0),SCANL)
    return im
def hud(d,t):
    fi=int(round(t*FPS)); a=min(1,float(ENV[fi]) if fi<len(ENV) else 0)
    d.ellipse((80,1576,100,1596),fill=(16,185,129,int(70+185*a)))
    d.text((114,1586),'BINDER',font=F(MONOB,26),fill=(16,185,129,200),anchor='lm')
    d.text((W-80,1586),'META EM CURTO · EP01',font=F(MONO,22),fill=(120,140,150,200),anchor='rm')
def typed(s,t0,t,cps=38): n=int(max(0,(t-t0))*cps); return s[:n]
def header(d,t,t0):
    f=F(MONOB,30); f2=F(MONO,26)
    d.text((80,250),typed('> ARQUIVO: ARENA CHAMPIONSHIP 13',t0,t),font=f,fill=PH)
    d.text((80,296),typed('  STANDARD · 24–25 OUT 2026 · MTG ARENA',t0+0.5,t),font=f2,fill=EM)
    d.line((80,350,1000,350),fill=(16,185,129,90),width=2)
META=[('MONO-GREEN LANDFALL',29,16.5),('DIMIR ULDAROS',25,14.2),('ORZHOV LIFE GAIN',21,11.9),('DIMIR MIDRANGE',14,8.0),('JUND SACRIFICE',14,8.0)]
def scene_meta(t,t0):
    im,d=term_base(t, egg=(vt(9.2)<=t<vt(10.2)))
    header(d,t,t0)
    fl=F(MONOB,28); fn=F(MONOB,34); fsrc=F(MONO,22)
    d.text((80,395),typed('ARQUÉTIPOS MAIS JOGADOS (176 JOGADORES)',t0+1.0,t),font=F(MONO,24),fill=GREY)
    X0,X1=80,1000; scale=(X1-X0-170)/20.0
    for i,(n,c,p) in enumerate(META):
        ts=t0+1.4+i*0.22; y=470+i*150
        if t<ts: continue
        k=eio((t-ts)/0.6); hi=(i==0)
        col=PH if hi else (16,120,90)
        d.text((X0,y),n,font=fl,fill=(WHITE if hi else (170,190,195)))
        bw=p*scale*k
        d.rectangle((X0,y+44,X0+bw,y+90),fill=col+(255 if hi else 200,))
        d.text((X0+bw+16,y+67),f'{p:.1f}%'.replace('.',',')+f'  ({c})',font=(fn if hi else F(MONO,28)),fill=(PH if hi else (150,170,175)),anchor='lm')
    # eixo honesto 0–20%
    d.line((X0,1225,X0+20*scale,1225),fill=(16,185,129,80),width=2)
    for v in (0,10,20): d.text((X0+v*scale,1240),f'{v}%',font=fsrc,fill=GREY,anchor='ma')
    d.text((80,1300),'FONTE: magic.gg · Metagame Breakdown AC13',font=fsrc,fill=GREY)
    if t>vt(1.44)-0 and t<vt(5.6): pass
    hud(d,t); return term_finish(im,t)
def scene_final(t,t0):
    im,d=term_base(t); header(d,t,-9)
    d.text((80,430),typed('> FINAL',t0,t),font=F(MONOB,30),fill=GREY)
    if t>t0+0.25:
        k=eio((t-t0-0.25)/0.4)
        d.text((80,520+(1-k)*30),'JEFF LIN',font=F(INTB,120),fill=WHITE+(int(255*k),))
        d.text((84,680),typed('MONO-GREEN LANDFALL',t0+0.6,t,50),font=F(MONOB,44),fill=PH)
        d.rectangle((84,760,84+typed('████████████',t0+1.2,t,30).__len__()*20,772),fill=EM)
        d.text((84,800),typed('STATUS: FINALISTA',t0+1.3,t,40),font=F(MONO,34),fill=EM)
    hud(d,t); return term_finish(im,t)
def scene_reveal(t,t0,tblank):
    im,d=term_base(t); header(d,t,-9)
    if t<tblank:   # corte seco: cursor
        if int(t*4)%2==0: d.rectangle((80,560,104,600),fill=PH)
        d.text((80,430),'> CAMPEÃO',font=F(MONOB,30),fill=GREY)
        hud(d,t); return term_finish(im,t)
    d.text((80,430),'> CAMPEÃO',font=F(MONOB,30),fill=GREY)
    k=eio((t-tblank)/0.35)
    d.text((80,520),'GAGE',font=F(INTB,150),fill=EM)
    d.text((80,680),'FEVOLD',font=F(INTB,150),fill=EM)
    if t>vt(19.32):
        d.text((84,870),typed('ORZHOV LIFEGAIN',vt(19.32),t,45),font=F(MONOB,48),fill=WHITE)
    if t>vt(19.9):
        d.text((84,960),typed('3º arquétipo mais jogado · 21 jogadores',vt(19.9),t,60),font=F(MONO,28),fill=GREY)
    hud(d,t); return term_finish(im,t)
def scene_tese(t,t0):
    im,d=term_base(t); header(d,t,-9)
    d.text((80,430),typed('> ANÁLISE',t0,t),font=F(MONOB,30),fill=GREY)
    f=F(INTB,84)
    if t>vt(21.8):
        d.text((80,520),'RESULTADO',font=f,fill=WHITE); 
    if t>vt(22.3): d.text((80,620),'≠ PROVA',font=f,fill=PH)
    if t>vt(23.76):
        d.text((80,760),typed('1 final ≠ demonstração',vt(23.76),t,40),font=F(MONO,34),fill=GREY)
    items=[('POPULARIDADE',vt(26.2)),('DESEMPENHO',vt(27.04)),('MATCHUP',vt(27.84))]
    y=880
    for i,(s,ts) in enumerate(items):
        if t<ts: continue
        k=eio((t-ts)/0.3)
        lab=s+(' ≠' if i<2 and t>items[i+1][1]-0.05 else '')
        d.text((80-(1-k)*40,y+i*130),lab,font=F(MONOB,64),fill=(PH if i==0 else WHITE)+(int(255*k),))
    if t>vt(27.84): d.text((84,y+2*130+80),'(confronto direto)',font=F(MONO,28),fill=GREY)
    hud(d,t); return term_finish(im,t)
# ---------- legendas palavra a palavra ----------
def chunks():
    out=[];cur=[]
    for w in WORDS:
        cur.append(w)
        if w['t'][-1] in '.,:?!' or len(cur)>=4: out.append(cur);cur=[]
    if cur: out.append(cur)
    return out
CH=chunks()
def subs(im,t,y=1440,dark=False):
    d=ImageDraw.Draw(im,'RGBA')
    for c in CH:
        if c[0]['vs']-0.05<=t<=c[-1]['ve']+0.12:
            f=F(MONOB,50); txt=[w['t'].upper() for w in c]
            sp=d.textlength(' ',font=f); tot=sum(d.textlength(s,font=f) for s in txt)+sp*(len(txt)-1)
            if tot>W-160:
                f=fit(d,' '.join(txt),MONOB,50,W-160); sp=d.textlength(' ',font=f); tot=sum(d.textlength(s,font=f) for s in txt)+sp*(len(txt)-1)
            x=(W-tot)/2
            d.rounded_rectangle((x-24,y-50,x+tot+24,y+28),12,fill=(5,10,16,200))
            for w,s in zip(c,txt):
                on=t>=w['vs']-0.03
                d.text((x,y),s,font=f,fill=(PH if on else (60,90,75)),anchor='ls')
                x+=d.textlength(s,font=f)+sp
            break
    return im
def top_card(im,lines,k=1.0):
    d=ImageDraw.Draw(im,'RGBA'); y=210
    for s,font,col in lines:
        d.text((W/2,y),s,font=font,fill=col+(int(255*k),),anchor='ma'); y+=font.size*1.15
    return im
# ---------- OUTRO (reconstruído com quadros reais do scanner) ----------
def outro(t):
    if t<1.5: return SCAN[min(44,int(t*30))].copy()
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im,'RGBA')
    v=eio((t-1.5)/0.6); size=int(60+260*v)
    lg=LOGO.resize((size,size),Image.LANCZOS).rotate(-140*(1-v),resample=Image.BICUBIC)
    im.paste(lg,(int(W/2-lg.width/2),int(760-lg.height/2)),lg)
    q=ease((t-1.9)/0.3); r=ease((t-2.1)/0.3)
    d.text((W/2,1000+(1-q)*20),'BINDER Vision',font=F(INTB,92),fill=WHITE+(int(255*q),),anchor='ma')
    d.text((W/2,1130),'Escaneie suas cartas e organize seus decks.',font=F(INTM,38),fill=(190,200,210,int(255*q)),anchor='ma')
    d.text((W/2,1250),'Disponível no Google Play · Link na bio',font=F(INTSB,40),fill=EM+(int(255*r),),anchor='ma')
    if t>3.4: im=Image.blend(im,Image.new('RGB',(W,H),(0,0,0)),min(1,(t-3.4)/0.47))
    return im
# ---------- timeline ----------
DIVE=TL['DIVE']; DIVE_END=vt(5.76); EXIT=TL['EXIT']; EXIT_END=vt(30.64)
FIN0=vt(13.48); REV_T=vt(17.017)-0.18; REV_B=vt(18.16)-0.02; TESE=vt(20.857)
fb=F(INTB,112); fm=F(INTSB,52); fs=F(MONOB,40)
def frame(t):
    if t>=OUT: return outro(t-OUT)
    # FORA inicial
    if t<DIVE_END:
        if t<DIVE:
            expr='desconfiado' if t<vt(3.3) else 'analitico'
            im=tubo_frame(t,expr,zoom=1.0+0.04*eio(t/2.0))
        else:
            k=eio((t-DIVE)/(DIVE_END-DIVE)); z=1+k*4.2
            im=tubo_frame(t,'analitico',zoom=z,cx=W/2+(SCX-W/2)*min(1,k*1.5),cy=H/2+(SCY-H/2)*min(1,k*1.5))
            if k>0.65:
                tm=scene_meta(t,DIVE_END); im=Image.blend(im,tm,(k-0.65)/0.35)
            return im
        k=1 if t<4.6 else 1-(t-4.6)/0.6
        lines=[('29 JOGADORES',fb,PH)]
        if t>vt(2.0): lines.append(('escolheram Mono-Green Landfall',fm,WHITE))
        if t>vt(3.36): lines.append(('O campeão: outro deck.',fm,EM))
        im=top_card(im,lines,max(0,k) if t>4.6 else 1)
        return subs(im,t,1560)
    if t<FIN0: return subs(scene_meta(t,DIVE_END),t)
    if t<REV_T: return subs(scene_final(t,FIN0),t)
    if t<TESE: return subs(scene_reveal(t,REV_T,REV_B),t)
    if t<EXIT: return subs(scene_tese(t,TESE),t)
    if t<EXIT_END:   # saída do tubo
        k=eio((t-EXIT)/(EXIT_END-EXIT)); z=5.2-4.2*k
        im=tubo_frame(t,'analitico',zoom=z,cx=W/2+(SCX-W/2)*(1-k),cy=H/2+(SCY-H/2)*(1-k))
        if k<0.35: im=Image.blend(scene_tese(t,TESE),im,k/0.35)
        return im
    # FORA final
    H1=vt(34.878); Q=vt(37.589); CL=vt(41.431)
    if t<Q:
        if t<H1-0.4: expr,z,cy='analitico',1.0,H/2
        else:
            kk=eio((t-H1+0.4)/0.8); expr='desconfiado'; z=1+0.35*kk; cy=H/2+(SCY-H/2)*kk
        im=tubo_frame(t,expr,zoom=z,cx=W/2+(SCX-W/2)*(z-1),cy=cy)
        lines=[('O resultado diz',fm,WHITE),('QUEM venceu.',fb if False else F(INTB,90),WHITE)]
        if t>vt(32.56): lines=[('Diz QUEM venceu.',F(INTB,74),WHITE),('Não explica por quê.',F(INTB,74),PH)]
        if t>=H1-0.4: lines=[('HUMANOS.',F(INTB,140),PH)]
        im=top_card(im,lines)
        return subs(im,t,1560)
    if t<CL:
        im=tubo_frame(t,'analitico',zoom=1.0)
        im=top_card(im,[('Qual decisão da final',F(INTB,74),WHITE),('merece ser investigada?',F(INTB,74),PH),('↓ responda nos comentários',F(MONO,36),GREY)])
        return subs(im,t,1560)
    im=tubo_frame(t,'confiante',zoom=1.0+0.03*eio((t-CL)/2))
    k=ease((t-CL)/0.4)
    im=top_card(im,[('META EM CURTO',F(INTB,96),WHITE),('com TUBO · BINDER Originals',F(MONO,34),EM)],k)
    return subs(im,t,1560)
if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='stills':
        for tt in map(float,sys.argv[2:]): frame(tt).save(f'still_{tt:05.2f}.png')
        sys.exit()
    nf=int(round(TOTAL*FPS))
    p=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i','mix_raw.wav',
        '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','-shortest','EP01_META_EM_CURTO_FINAL.mp4'],stdin=subprocess.PIPE)
    for i in range(nf):
        p.stdin.write(frame(i/FPS).tobytes())
    p.stdin.close(); p.wait(); print('done',nf)
