import sys, numpy as np, librosa, soundfile as sf
src,out=sys.argv[1],sys.argv[2]
ys,sr=librosa.load(src,sr=44100,mono=False)          # estéreo
y=librosa.to_mono(ys)
oenv=librosa.onset.onset_strength(y=y,sr=sr)
_,bf=librosa.beat.beat_track(onset_envelope=oenv,sr=sr,start_bpm=224,tightness=200)
bt=librosa.frames_to_time(bf,sr=sr)
C=librosa.feature.chroma_cqt(y=y,sr=sr); M=librosa.feature.mfcc(y=y,sr=sr,n_mfcc=13)
F=np.vstack([librosa.util.normalize(C,axis=0),M/np.abs(M).max()*2])
Fs=librosa.util.sync(F,bf,aggregate=np.mean)          # 1 coluna por batida
def score(i,j,w=4):
    if i-w<0 or j+w>=Fs.shape[1] or i+w>=Fs.shape[1]: return 9e9
    return np.linalg.norm(Fs[:,i:i+w]-Fs[:,j:j+w])+np.linalg.norm(Fs[:,i-w:i]-Fs[:,j-w:j])
def best(a0,a1,b0,b1,dmin,dmax):
    c=[]
    for i,ti in enumerate(bt):
        if not a0<=ti<=a1: continue
        for j,tj in enumerate(bt):
            if b0<=tj<=b1 and dmin<=tj-ti<=dmax: c.append((score(i,j),ti,tj))
    c.sort(); return c[0]
s1=best(12.5,16,26.5,30.5,12.5,16)      # encurta a análise → corte seco cai ~29 s
s2=best(46,54,49,58,3.6,5.4)            # encurta o fecho → ~41 s
print("salto1 %.2f→%.2f (score %.2f)"%(s1[1],s1[2],s1[0]))
print("salto2 %.2f→%.2f (score %.2f)"%(s2[1],s2[2],s2[0]))
def snap(t):  # cola ao ataque mais próximo (±40 ms)
    on=librosa.onset.onset_detect(y=y,sr=sr,units='time',backtrack=True)
    k=on[np.argmin(abs(on-t))]; return k if abs(k-t)<0.04 else t
segs=[(0,snap(s1[1])),(snap(s1[2]),snap(s2[1])),(snap(s2[2]),59.9)]
xf=int(0.025*sr); parts=[]
for a,b in segs: parts.append(ys[:,int(a*sr):int(b*sr)+xf])
o=parts[0]
for p in parts[1:]:
    r=np.linspace(1,0,xf); o=np.concatenate([o[:,:-xf],o[:,-xf:]*r+p[:,:xf]*(1-r),p[:,xf:]],axis=1)
fade=int(0.6*sr); o[:,-fade:]*=np.linspace(1,0,fade)
sf.write(out,o.T,sr)
dur=o.shape[1]/sr; brk=43.0-segs[1][0]+segs[0][1]
print("duracao %.1fs | corte seco em %.1fs | banda volta em %.1fs"%(dur,brk,brk+1.37))
