#!/bin/sh
# Instala as fontes livres (OFL) do kit em kit_carrossel/fontes/. Uso: sh preparar_fontes.sh
set -e
D="$(cd "$(dirname "$0")" && pwd)"; T="$(mktemp -d)"; mkdir -p "$D/fontes"
cd "$T" && npm i --silent @fontsource/archivo-black @fontsource/barlow-condensed @fontsource/rubik @fontsource/caveat-brush @fontsource/playfair-display geist >/dev/null
F=node_modules/@fontsource
cp $F/archivo-black/files/archivo-black-latin-400-normal.woff2 $F/barlow-condensed/files/barlow-condensed-latin-800-normal.woff2 \
   $F/rubik/files/rubik-latin-800-normal.woff2 $F/rubik/files/rubik-latin-900-italic.woff2 \
   $F/caveat-brush/files/caveat-brush-latin-400-normal.woff2 $F/playfair-display/files/playfair-display-latin-700-italic.woff2 \
   node_modules/geist/dist/fonts/geist-sans/Geist-Medium.woff2 node_modules/geist/dist/fonts/geist-sans/Geist-Bold.woff2 "$D/fontes/"
python3 -I "$D/desgaste.py" "$D/fontes/desgaste.png"
echo "fontes prontas em $D/fontes"
