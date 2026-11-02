set -e
cd /home/claude/prod; python3 render.py --master render/master.mkv >/dev/null
FX="-c:v libx264 -profile:v high -level 4.0 -pix_fmt yuv420p -preset slow -crf 17 -bf 2 -g 60 -video_track_timescale 15360 -an -movflags +faststart"
ffmpeg -y -v error -i render/master.mkv $FX render/orig_limpo.mp4
ffmpeg -y -v error -i render/master.mkv -i render/carimbo.png -filter_complex "[0:v][1:v]overlay=(W-w)/2-40:18" $FX render/orig_prev.mp4
for v in limpo prev; do ffmpeg -y -v error -f concat -safe 0 -i render/l_$v.txt -i render/fx.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -t 20 -movflags +faststart -metadata comment="PREVIA - DIREITOS A CONFIRMAR" render/f_$v.mp4; done
cp render/f_prev.mp4 entrega/LAMBE_LAMBE_PRERELEASE_STAR_TREK_2026_FINAL.mp4
cp render/f_limpo.mp4 entrega/LAMBE_LAMBE_PRERELEASE_STAR_TREK_2026_MASTER_SEM_CARIMBO.mp4
rm render/master.mkv.keep 2>/dev/null || true
