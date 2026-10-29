"""(29/10) Começa no quadro 7: sem a animação de ligar a TV.
Junta o episódio do kit ao fecho do scanner sem repetir a logo:
corta o vídeo do kit logo depois de o ponto ficar verde (T_SLAM + 0,52 s, antes de a logo do kit crescer),
cola o fecho do scanner (3,87 s, sem encurtar) e põe por baixo a trilha do episódio (a música cobre o fecho),
com fade de 0,45 s no fim. Saída: H.264 + AAC 48 kHz, 1080x1920, 30 fps.
uso: python3 juntar_fecho.py kit.mp4 fecho.mp4 saida.mp4
"""
import sys, json, subprocess
kit, fecho, out = sys.argv[1:4]
d = json.loads(open('data.js').read()[11:-1])
cut = round(d['T_SLAM'] + 0.52, 3)
T0 = 7 / 30   # tira o 'liga a TV' (quadros 0-6 achatados sobre preto, que o cropdetect lê como corte)
dur_f = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', fecho]))
total = cut - T0 + dur_f
fc = (f"[0:v]trim={T0}:{cut},setpts=PTS-STARTPTS,fps=30,format=yuv420p[a];"
      f"[1:v]fps=30,format=yuv420p,setsar=1[b];[a][b]concat=n=2:v=1:a=0[v];"
      f"[2:a]atrim={T0}:{T0 + total:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.05,afade=t=out:st={total - 0.45:.3f}:d=0.45,aresample=48000[au]")
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', kit, '-i', fecho, '-i', 'trilha_final.wav', '-filter_complex', fc,
                '-map', '[v]', '-map', '[au]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', '30',
                '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', out], check=True)
print(f'corte do kit em {cut}s + fecho {dur_f:.2f}s = {total:.2f}s ->', out)
