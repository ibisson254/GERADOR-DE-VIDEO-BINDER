import sys, json, math, subprocess
sys.path.insert(0,'/root/ep01')
import render as R
from PIL import Image, ImageDraw
R.rain_cols=[]   # sem chuva animada: o ecrã fica com o código estático da mestra
W,H,FPS=R.W,R.H,R.FPS; F=R.F; vt=R.vt; eio=R.eio; ease=R.ease
TL=R.TL; OUT=TL['OUT_START']; TOTAL=TL['TOTAL']
PH,EM,WHITE,GREY,BG=R.PH,R.EM,R.WHITE,R.GREY,R.BG
LAND=(0,255,65); LIFE=(236,241,245); DIMC=(38,52,62)
def term(t, egg=False):
    im=R.TERM_BG.copy(); d=ImageDraw.Draw(im,'RGBA')
    d.text((80,220),'AC13 · STANDARD · 24–25 OUT 2026',font=F(R.MONOB,34),fill=EM)
    d.line((80,276,1000,276),fill=(16,185,129,90),width=2)
    if egg: d.text((1000,1330),'GG·FEVOLD',font=F(R.MONO,22),fill=(0,255,65,60),anchor='ra')
    return im,d
def fin(im,t,d):
    R.hud(d,t); return R.term_finish(im,t)
# --- B: campo (waffle 16x11 = 176) ---
def scene_campo(t):
    im,d=term(t, egg=vt(9.0)<=t<vt(10.0))
    k0=eio((t-vt(6.64))/0.4)
    d.text((80,320),'176 JOGADORES',font=F(R.INTB,96),fill=WHITE+(int(255*k0),))
    S=56; X0=(W-16*S)/2+6; Y0=470
    for i in range(176):
        r,c=divmod(i,16); x=X0+c*S; y=Y0+r*S
        col=DIMC
        if i<29 and t>=vt(8.56)+i*0.012: col=LAND
        elif 29<=i<50 and t>=vt(10.12)+(i-29)*0.012: col=LIFE
        d.rounded_rectangle((x,y,x+44,y+44),8,fill=col)
    y=Y0+11*S+30
    if t>=vt(8.56): d.text((80,y),'■ MONO-GREEN LANDFALL  29',font=F(R.MONOB,42),fill=LAND)
    if t>=vt(10.12): d.text((80,y+64),'■ ORZHOV LIFEGAIN  21',font=F(R.MONOB,42),fill=LIFE)
    if t>=vt(11.76): d.text((80,y+140),typed('CAMPEÃO: GAGE FEVOLD (LIFEGAIN)',vt(11.76),t),font=F(R.MONOB,36),fill=EM)
    d.text((80,1330),'fonte: magic.gg',font=F(R.MONO,24),fill=GREY)
    return fin(im,t,d)
def typed(s,t0,t,cps=45): return s[:int(max(0,t-t0)*cps)]
# --- C: funil ---
def scene_funil(t):
    im,d=term(t)
    d.text((80,320),'DO CAMPO AO TOP 8',font=F(R.INTB,80),fill=WHITE)
    cols=[('CAMPO',None),('TOP 16',vt(15.44)),('TOP 8',None)]
    xs=[380,640,880]; rows=[('LANDFALL',LAND,[29,4,1],[None,vt(17.76),None]),('LIFEGAIN',LIFE,[21,3,3],[None,vt(18.92),None])]
    hi16= t>=vt(15.44)
    if hi16: d.rounded_rectangle((xs[1]-110,470,xs[1]+110,930),18,outline=EM,width=4,fill=(16,185,129,28))
    for j,(name,tt) in enumerate(cols):
        a=255 if (j!=1 or hi16) else 0
        d.text((xs[j],500),name,font=F(R.MONOB,34),fill=(150,170,175,a),anchor='ma')
    for i,(nm,col,vals,tv) in enumerate(rows):
        y=620+i*170
        d.text((80,y),nm,font=F(R.MONOB,40),fill=col,anchor='lm')
        for j,v in enumerate(vals):
            if j==1 and not hi16: continue
            show = (j!=1) or (tv[1] is not None and t>=tv[1])
            s=str(v) if show else '?'
            d.text((xs[j],y),s,font=F(R.INTB,104),fill=(col if show else (80,100,110)),anchor='mm')
        if t>=vt(21.36):
            p=['13,8%','14,3%'][i]; k=eio((t-vt(21.36))/0.4)
            d.text((xs[1],y+66),p,font=F(R.MONOB,40),fill=EM+(int(255*k),),anchor='mm')
    if t>=vt(24.12):
        d.text((W/2,1040),'TOP 16:  13,8%  ≈  14,3%',font=F(R.MONOB,54),fill=PH,anchor='mm')
        d.text((W/2,1110),'conversão praticamente igual',font=F(R.MONO,34),fill=GREY,anchor='mm')
    d.text((80,1330),'fontes: magic.gg · mtggoldfish (melee.gg)',font=F(R.MONO,24),fill=GREY)
    return fin(im,t,d)
# --- D: oitavas ---
def scene_oitavas(t):
    im,d=term(t)
    d.text((80,320),'OITAVAS (1 RODADA)',font=F(R.INTB,80),fill=WHITE)
    if t<vt(27.16)-0.05:
        if int(t*4)%2==0: d.rectangle((80,520,106,566),fill=PH)
        return fin(im,t,d)
    def row(y,nm,col,n,ok,t0):
        d.text((80,y),nm,font=F(R.MONOB,44),fill=col)
        for k in range(n):
            x=80+k*150; on=k<ok; vis=t>=t0+k*0.12
            if not vis: continue
            d.rounded_rectangle((x,y+80,x+120,y+200),16,fill=(col if on else None),outline=col,width=5)
            d.text((x+60,y+140),'✓' if on else '✕',font=F(R.MONOB,64),fill=(BG if on else col),anchor='mm')
        if t>=t0+0.5: d.text((1000,y+140),f'{ok}/{n}',font=F(R.INTB,110),fill=col,anchor='rm')
    row(500,'LIFEGAIN → TOP 8',LIFE,3,3,vt(27.16))
    if t>=vt(29.2): row(820,'LANDFALL → TOP 8',LAND,4,1,vt(29.2))
    d.text((80,1330),'fonte: mtggoldfish (classificação final, melee.gg)',font=F(R.MONO,24),fill=GREY)
    return fin(im,t,d)
# --- FORA ---
def card(im,lines,y=200):
    d=ImageDraw.Draw(im,'RGBA')
    for s,f,c in lines:
        d.text((W/2,y),s,font=f,fill=c,anchor='ma'); y+=f.size*1.18
    return im
def frame(t):
    if t>=OUT: return R.outro(t-OUT)
    if t>=OUT-0.4:
        a=(t-(OUT-0.4))/0.4; return Image.blend(frame_main(OUT-0.41),R.outro(0),a)
    return frame_main(t)
DIVE=TL['DIVE']; DIVE_END=DIVE+0.45; EXIT=TL['EXIT']; EXIT_END=vt(30.78)
def frame_main(t):
    if t<DIVE_END:
        zbase=1.45
        if t<DIVE:
            im=R.tubo_frame(t,'desconfiado' if t<vt(4.4) else 'confiante',zoom=1.16+0.03*eio(t/5),cx=W/2+(R.SCX-W/2)*0.5,cy=860)
            d=ImageDraw.Draw(im,'RGBA')
            for x0,lab,tl,num,tn,col in [(285,'MAIS JOGADO',vt(0.48),'1',vt(2.84),WHITE),(795,'3º MAIS JOGADO',vt(4.48),'3',vt(5.92),PH)]:
                if t>=tl: d.text((x0,120),lab,font=F(R.INTSB,44),fill=GREY,anchor='ma')
                if t>=tn:
                    d.text((x0,170),num,font=F(R.INTB,150),fill=col,anchor='ma')
                    d.text((x0,340),'no TOP 8',font=F(R.INTB,52),fill=col,anchor='ma')
            if t>=vt(4.48): d.line((W/2,130,W/2,400),fill=(120,140,150,120),width=2)
            return R.subs(im,t,1600)
        k=eio((t-DIVE)/(DIVE_END-DIVE)); z=1.5+k*3.7
        im=R.tubo_frame(t,'analitico',zoom=z,cx=R.SCX,cy=R.SCY+60*(1-k))
        if k>0.6: im=Image.blend(im,scene_campo(t),(k-0.6)/0.4)
        return im
    if t<vt(13.42): return R.subs(scene_campo(t),t,1500)
    if t<vt(25.0): return R.subs(scene_funil(t),t,1500)
    if t<EXIT: return R.subs(scene_oitavas(t),t,1500)
    if t<EXIT_END:
        k=eio((t-EXIT)/(EXIT_END-EXIT)); z=5.2-4.2*k
        im=R.tubo_frame(t,'analitico',zoom=z,cx=W/2+(R.SCX-W/2)*(1-k),cy=H/2+(R.SCY-H/2)*(1-k))
        if k<0.35: im=Image.blend(scene_oitavas(t),im,k/0.35)
        return im
    Q=vt(38.114); CL=vt(43.584)
    if t<Q:
        expr='desconfiado' if t>=vt(36.6) else 'analitico'
        im=R.tubo_frame(t,expr,zoom=1.0)
        L=[('1 rodada ≠ 1 deck',F(R.INTB,84),WHITE)]
        if t>=vt(34.64):
            L.append(('',F(R.MONO,20),GREY))
            im=card(im,L,200); d=ImageDraw.Draw(im,'RGBA')
            d.text((W/2,330),'GRAU DE CERTEZA',font=F(R.MONOB,36),fill=GREY,anchor='ma')
            for i in range(5):
                x=W/2-250+i*102; on=i<1
                d.rounded_rectangle((x,385,x+90,425),8,fill=(EM if on else None),outline=EM,width=3)
            if t>=vt(35.52): d.text((W/2,440),'BAIXO',font=F(R.MONOB,40),fill=EM,anchor='ma')
            return R.subs(im,t,1600)
        return R.subs(card(im,L,200),t,1600)
    if t<CL:
        im=R.tubo_frame(t,'analitico',zoom=1.0); d=ImageDraw.Draw(im,'RGBA')
        im=card(im,[('Nas oitavas,',F(R.INTB,70),WHITE),('o que pesou mais?',F(R.INTB,70),PH)],170)
        d=ImageDraw.Draw(im,'RGBA')
        chips=[('MATCHUP',vt(40.0)),('CHAVEAMENTO',vt(40.6)),('PILOTAGEM',vt(41.6))]
        f=F(R.MONOB,34); y=1450
        ws=[d.textlength(s,font=f)+48 for s,_ in chips]; x=(W-sum(ws)-2*20)/2
        for (s,tt),w in zip(chips,ws):
            on=t>=tt
            d.rounded_rectangle((x,y,x+w,y+70),35,fill=(EM if on else (15,23,42,230)),outline=EM,width=3)
            d.text((x+w/2,y+35),s,font=f,fill=(BG if on else EM),anchor='mm'); x+=w+20
        return R.subs(im,t,1640)
    kz=eio((t-CL)/1.2)
    im=R.tubo_frame(t,'confiante',zoom=1.0+0.22*kz,cx=W/2,cy=H/2+(R.SCY+260-H/2)*kz)
    k=ease((t-CL)/0.4)
    im=R.top_card(im,[('META EM CURTO',F(R.INTB,96),WHITE),('com TUBO · BINDER Originals',F(R.MONO,34),EM)],k)
    return R.subs(im,t,1600)
if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='stills':
        for tt in map(float,sys.argv[2:]): frame(tt).save(f'still_{tt:05.2f}.png')
        sys.exit()
    nf=int(round(TOTAL*FPS))
    p=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i','mix_final.wav',
        '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','-shortest','EP01_META_EM_CURTO_FINAL_v2.mp4'],stdin=subprocess.PIPE)
    for i in range(nf): p.stdin.write(frame(i/FPS).tobytes())
    p.stdin.close(); p.wait(); print('done',nf)
