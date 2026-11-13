#!/bin/bash
# mux.sh VIDEO_SEM_FECHO.mp4 TRILHA.wav SAIDA.mp4  — loudnorm 2 passagens (-14 LUFS, TP -2) + fecho oficial
set -e
V=$1; A=$2; S=$3; O=${OUTRO:-$(dirname "$0")/../../comum/outro/outro_binder_916.mp4}
J=$(ffmpeg -hide_banner -i "$A" -af loudnorm=I=-14:TP=-2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g(){ echo "$J" | python3 -c "import sys,json;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -y -loglevel error -i "$A" -af "loudnorm=I=-14:TP=-2:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true" -ar 48000 /tmp/_norm.wav
ffmpeg -y -loglevel error -i "$V" -i "$O" -i /tmp/_norm.wav -filter_complex "[0:v]fps=30,format=yuv420p[a];[1:v]scale=1080:1920,fps=30,format=yuv420p,setsar=1[b];[a][b]concat=n=2:v=1:a=0[v]" -map "[v]" -map 2:a -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a aac -b:a 256k -ar 48000 -movflags +faststart -shortest "$S"
