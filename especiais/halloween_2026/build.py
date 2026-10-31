"""Junta kit.mp4 (render.py) + fecho do scanner (fecho.mp4) + trilha.wav (mix.py) no vídeo final.
uso: python3 build.py [nome.mp4]
"""
import json, sys, subprocess
TL = json.load(open('tl.json'))
out = sys.argv[1] if len(sys.argv) > 1 else ('BINDER_Especial_Halloween_InnistradXDuskmourn' + ('_PREVIA' if TL['previa'] else '') + '_916.mp4')
fc = ("[0:v]fps=30,format=yuv420p,setsar=1[a];[1:v]fps=30,format=yuv420p,setsar=1[b];[a][b]concat=n=2:v=1:a=0[v];"
      f"[2:a]atrim=0:{TL['TOTAL']:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={TL['TOTAL'] - 0.45:.3f}:d=0.45,aresample=48000[au]")
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'kit.mp4', '-i', 'fecho.mp4', '-i', 'trilha.wav', '-filter_complex', fc,
                '-map', '[v]', '-map', '[au]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', '30',
                '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', out], check=True)
print('ok', out)
