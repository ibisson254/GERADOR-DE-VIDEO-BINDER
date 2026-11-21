"""Ep. 10 (11/11/2026): cola o fecho do scanner depois de a imagem apagar até ao ponto verde (EP.desliga).
Corta o vídeo do kit em T_OFF + 0,52 s, cola comum/outro/outro_binder_916.mp4 (3,87 s) e põe por baixo do fecho
a pancada final da musica.mp3 (a partir de 126,30 s, −8 dB, fade de 0,55 s). Áudio com limitador antes do AAC
(o ruído das trocas de canal passa de 0 dBTP no AAC sem ele).
uso: python3 kit/v3/juntar_fecho_v3.py kit.mp4 trilha_master.wav saida.mp4"""
import sys, json, subprocess
kit, wav, out = sys.argv[1:4]
d = json.loads(open('data.js').read().strip()[11:-1]); L = d['lines'][-1]
ep = json.load(open('episode.json')); T_OFF = L['start'] + L['dur'] + ep['loop']['desliga']
cut = round(T_OFF + 0.52, 3)
fc = (f"[0:v]trim=0:{cut},setpts=PTS-STARTPTS,fps=30,format=yuv420p,setsar=1[a];[1:v]fps=30,format=yuv420p,setsar=1[b];[a][b]concat=n=2:v=1:a=0[v];"
      f"[2:a]atrim=0:{cut},asetpts=PTS-STARTPTS[x];[3:a]aresample=48000,volume=-8dB,afade=t=in:d=0.05,afade=t=out:st=3.32:d=0.55[m];"
      f"[x][m]concat=n=2:v=0:a=1,lowpass=f=15500,alimiter=limit=0.75:attack=1:release=50:level=false[au]")
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',kit,'-i','../comum/outro/outro_binder_916.mp4','-i',wav,'-ss','126.30','-t','3.87','-i','musica.mp3',
  '-filter_complex',fc,'-map','[v]','-map','[au]','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-r','30',
  '-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',out],check=True)
print(f'kit até {cut}s + fecho 3,87 s ->', out)
