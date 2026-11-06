# Especial pré-release Star Trek · "BURN FOI ASSIMILADO!" · como recriar

O vídeo não está no repositório (regra §7). Para o recriar com o kit v2 de `manaburn/`:

1. Copiar para uma pasta de trabalho o kit (`manaburn/`: index.html, process.py, cortes.py, trilha.py, sfx.py, roteiro.py, foneticos.json, render.py, preview.py, bordas.py, musica.mp3, tv_asset.png, logo/, node_modules/, cards/) e, desta pasta, `episode.json`, `episode.js` e `../ep09_dack/juntar_fecho.py`.
2. Cartas (Scryfall, set TRK, PNG 744×1040) em `cards/`: borgcube (227), traveler (254), locutus (245), voyager (222), resistance (125), perils (161), orion (288), vexing (45).
3. Vozes: flow ElevenLabs "Mana & Burn — Especial pré-release Star Trek (Burn foi assimilado)" (uynVVRurU7AQlC3bwwc5) → `burn.mp3` (Talis) e `mana.mp3` (Erik). Não gerar de novo: descarregar as tomadas existentes.
4. `python3 process.py burn.mp3 mana.mp3` → `data.js` (igual ao guardado aqui) e `trilha_final.wav`.
5. `python3 render.py kit_render.mp4 2.0` (Chromium; nesta sessão usou-se `executable_path='/usr/bin/google-chrome'`).
6. `python3 juntar_fecho.py kit_render.mp4 ../../../comum/outro/outro_binder_916.mp4 ManaBurn_Especial_StarTrek_Prerelease_916.mp4`
7. Loudnorm de 2 passes no áudio (I −14, TP −2, vídeo copiado) e `python3 -I comum/qc/qc_video.py … --frente manaburn` + `bordas.py`.
