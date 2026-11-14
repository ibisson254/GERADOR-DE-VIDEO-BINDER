"""Junta o episódio renderizado ao fecho oficial e à mistura final.
Uso: python3 montar.py episodio_sem_audio.mp4 mix.wav OUTRO.mp4 saida.mp4
O fecho não é encurtado nem acelerado; corte seco no último acento (41,2 s).
"""
import subprocess, sys

ep, mix, outro, saida = sys.argv[1:5]
subprocess.run([
    "ffmpeg", "-y", "-loglevel", "error", "-i", ep, "-i", outro, "-i", mix,
    "-filter_complex", "[0:v]setsar=1,fps=30[a];[1:v]setsar=1,fps=30[b];[a][b]concat=n=2:v=1:a=0[v]",
    "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
    "-r", "30", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", "-shortest", saida,
], check=True)
print("ok", saida)
