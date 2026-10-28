import numpy as np, soundfile as sf, subprocess, json
SR=48000; TEMPO=1.05; LEAD=0.25
def load(p):
    raw=subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','2','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).reshape(-1,2).copy()
# voz: atempo 1.05, normalizar ~ -16 LUFS
subprocess.run(['ffmpeg','-y','-v','error','-i','vozA.mp3','-af',f'atempo={TEMPO},highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,loudnorm=I=-16:TP=-1.5:LRA=7','-ar',str(SR),'-ac','2','voz_proc.wav'],check=True)
voz=load('voz_proc.wav')
vend=LEAD+len(voz)/SR
OUT_START=round(vend+0.55,3); OUT_LEN=3.87; TOTAL=OUT_START+OUT_LEN
N=int(TOTAL*SR)
V=np.zeros((N,2),np.float32); a=int(LEAD*SR); V[a:a+len(voz)]=voz[:N-a]
# música: tema original, a partir de 0
M=load('/root/kit/oraculo/musica/tubo_tema_original.mp3')[:N]
M=np.pad(M,((0,N-len(M)),(0,0)))
t=np.arange(N)/SR
# envelope da voz (sidechain manual, suave) -> ducking
env=np.abs(V).mean(1); w=int(0.05*SR)
env=np.convolve(env,np.ones(w)/w,'same')
speak=(env>0.01).astype(float)
# manter fala "colada" entre palavras: dilatar 0.35 s e suavizar 0.25 s
d=int(0.35*SR); speak=np.convolve(speak,np.ones(d),'same')>0
s=int(0.25*SR); speak=np.convolve(speak.astype(float),np.ones(s)/s,'same')
g_db=-6 + speak*(-10)           # sem voz: -6 dB ; com voz: -19 dB
g=10**(g_db/20)
# corte seco da revelação
w=json.load(open('words.json')); 
def vt(x): return x/TEMPO+LEAD
REV0=vt(17.017)-0.18; REV1=vt(18.16)-0.02
cut=np.ones(N); i0,i1=int(REV0*SR),int(REV1*SR); f=int(0.03*SR)
cut[i0:i1]=0; cut[i0-f:i0]=np.linspace(1,0,f); cut[i1:i1+f]=np.linspace(0,1,f)
# fecho: sobe no outro e fade final
g=np.where(t>=OUT_START-0.3, 10**(-3/20), g)
fade=np.clip((TOTAL-t)/1.2,0,1)
M=M*(g*cut*fade)[:,None]
# SFX sintetizados
def thump(dur=0.7,f0=58):
    tt=np.arange(int(dur*SR))/SR
    x=np.sin(2*np.pi*f0*tt*(1-0.25*tt))*np.exp(-tt*6)*0.9
    x+=np.sin(2*np.pi*50*tt)*np.exp(-tt*3)*0.12*np.sign(np.sin(2*np.pi*100*tt))
    cl=np.random.default_rng(1).normal(0,1,len(tt))*np.exp(-tt*120)*0.35
    return (x+cl).astype(np.float32)
def modem(dur=0.55):
    tt=np.arange(int(dur*SR))/SR; rng=np.random.default_rng(2)
    fr=900+1400*((tt*9)%1); x=np.sin(2*np.pi*np.cumsum(fr)/SR)*0.18
    x+=rng.normal(0,1,len(tt))*0.08*(0.5+0.5*np.sin(2*np.pi*23*tt))
    env=np.minimum(1,tt/0.03)*np.minimum(1,(dur-tt)/0.12)
    return (x*env).astype(np.float32)
S=np.zeros_like(V)
def put(x,at,gain):
    i=int(at*SR); n=min(len(x),N-i); S[i:i+n]+=x[:n,None]*gain
put(thump(),0.0,0.8)
DIVE=vt(5.76)-0.55
put(modem(),DIVE,0.55)
EXIT=vt(30.587)-0.45
put(thump(0.4,70),EXIT+0.25,0.35)
mix=V+M+S
peak=np.abs(mix).max(); 
if peak>0.97: mix*=0.97/peak
sf.write('mix_raw.wav',mix,SR)
sf.write('musica_mix.wav',M,SR); sf.write('voz_final.wav',V,SR)
json.dump(dict(TEMPO=TEMPO,LEAD=LEAD,OUT_START=OUT_START,TOTAL=TOTAL,DIVE=DIVE,EXIT=EXIT,REV0=REV0,REV1=REV1),open('tl.json','w'),indent=1)
# envelope por frame para o LED
fps=30; nf=int(round(TOTAL*fps)); hop=SR//fps
e=np.array([np.sqrt((V[i*hop:(i+1)*hop]**2).mean()) if i*hop<N else 0 for i in range(nf)])
np.save('led_env.npy',e/ (np.percentile(e[e>0.005],95) if (e>0.005).any() else 1))
print(json.load(open('tl.json')))
