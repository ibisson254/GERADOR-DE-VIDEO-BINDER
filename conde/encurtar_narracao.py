import json, subprocess, re
SRC="narracao_raw.mp3"; TEMPO=1.08
log=subprocess.run(["ffmpeg","-hide_banner","-i",SRC,"-af","silencedetect=noise=-38dB:d=0.3","-f","null","-"],capture_output=True,text=True).stderr
st=[float(x) for x in re.findall(r"silence_start: ([\d.]+)",log)]
en=[float(x) for x in re.findall(r"silence_end: ([\d.]+)",log)]
dur=float(re.search(r"Duration: (\d+):(\d+):([\d.]+)",log).group(3))+60*int(re.search(r"Duration: (\d+):(\d+)",log).group(2))
sil=list(zip(st,en))
# pausa alvo por silêncio (s); beat cómico antes de "e encontra uma perna" (~28.8)
def alvo(a,b):
    if 28.0<a<28.9: return 0.55
    if 34.5<a<35.8: return 0.40
    if 44.3<a<45.4: return 0.40
    if 49.0<a<49.9: return 0.45
    return 0.24
keep=[]; cur=0.0
for a,b in sil:
    t=alvo(a,b);
    if b-a>t:
        keep.append((cur,a+t/2)); cur=b-t/2
keep.append((cur,dur))
# mapa de tempo antigo->novo
segs=[]; acc=0.0
for a,b in keep: segs.append((a,b,acc)); acc+=b-a
def remap(t):
    for a,b,o in segs:
        if t<=b: return (o+max(0,t-a))/TEMPO
    return acc/TEMPO
filt="".join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[s{i}];" for i,(a,b) in enumerate(keep))
filt+="".join(f"[s{i}]" for i in range(len(keep)))+f"concat=n={len(keep)}:v=0:a=1,atempo={TEMPO},loudnorm=I=-16:TP=-1.5:LRA=11[o]"
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i",SRC,"-filter_complex",filt,"-map","[o]","-ar","48000","narracao.wav"],check=True)
w=json.load(open("words.json"))
json.dump([[x,round(remap(a),3),round(remap(b),3)] for x,a,b in w],open("words_novo.json","w"),ensure_ascii=False)
print("duração nova:", round(acc/TEMPO,2))
