import numpy as np, json, wave
SR=48000; N=int(SR*20); rng=np.random.default_rng(5); out=np.zeros(N)
def env(n,a,d): t=np.arange(n)/SR; return (1-np.exp(-t/a))*np.exp(-t/d)
def slap(t,g=1):
    n=int(.28*SR); x=np.arange(n)/SR
    low=np.sin(2*np.pi*(95*np.exp(-x*14)+42)*x)*env(n,.001,.07)
    nz=rng.standard_normal(n); nz=np.diff(nz,prepend=0)*env(n,.0005,.018)
    add(t,(low*.9+nz*.32)*g)
def rip(t,dur=.17,g=.6):
    n=int(dur*SR); nz=rng.standard_normal(n); nz=np.diff(nz,prepend=0)
    cr=(rng.random(n)<.016)*rng.standard_normal(n)*3.2
    cr=np.convolve(cr,np.exp(-np.arange(90)/18),'same')
    e=np.sin(np.pi*np.arange(n)/n)**.6*(0.6+.4*np.sin(2*np.pi*31*np.arange(n)/SR))
    add(t,(nz*.34+cr*.5)*e*g)
def add(t,s):
    i=int(t*SR); s=s[:N-i]; out[i:i+len(s)]+=s
m=json.load(open('render/manifest.json'))
for c in m['cuts']:
    t=c['s']/30
    if c['tr']=='tear' and c['s']>0: rip(max(0,t-.02))
    slap(t,1 if c['e']-c['s']>=16 else .6)
slap(16.1333,.9)
out=out/np.abs(out).max()*10**(-6/20)
print('pico dBFS',20*np.log10(np.abs(out).max()))
st=np.stack([out,out*.97],1); pcm=(st*32767).astype('<i2')
w=wave.open('render/fx.wav','wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes());w.close()
