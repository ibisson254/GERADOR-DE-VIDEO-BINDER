#!/bin/bash
# Recarrega as imagens das cartas do Scryfall (só imagem e dados; nunca preços).
cd "$(dirname "$0")" && mkdir -p cartas
for par in "eoc/7 uthros" "ecl/110 moonshadow" "trk/393 watery_lcars" "trk/398 steam_lcars" "trk/306 watery_trk" "fra/52 dark_matter"; do
  set -- $par; j=$(curl -s "https://api.scryfall.com/cards/$1")
  curl -s -o cartas/$2.png "$(echo "$j" | python3 -c 'import sys,json;print(json.load(sys.stdin)["image_uris"]["png"])')"
  [ "$2" != steam_lcars ] && curl -s -o cartas/${2}_art.jpg "$(echo "$j" | python3 -c 'import sys,json;print(json.load(sys.stdin)["image_uris"]["art_crop"])')"
  sleep 0.2
done
