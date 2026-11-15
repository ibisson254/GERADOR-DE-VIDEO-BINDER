# Giro de domingo nº 3 · 15/11/2026 · como recriar o vídeo

O vídeo final não está no repositório (regra do estúdio). Para o recriar, numa cópia de `manaburn/` (kit v2, sala v3):

1. (v2) Pôr as fotos oficiais em `cards/src/foto_bk.jpg` e `cards/src/foto_netflix.jpg` e correr `python3 telas_visuais.py` (com `node_modules/`), que gera `cards/v*.png` e `cards/ins_*.png`.
1. Copiar `episode.js`, `episode.json` e `cards/giro_*.png`, `cards/v*.png` e `cards/ins_*.png` desta pasta para a raiz da cópia do kit (as telas tipográficas recriam-se com `python3 telas_giro.py`, com `node_modules/` ao lado; `giro_chandra.png` e `giro_numot.png` são os PNG do Scryfall em 744×1040; `giro_conde.png` é o recorte 3:4 de `conde/capas/referencia/CM_EP005_CAPA.png`).
2. Vozes: flow ElevenLabs "Mana & Burn — Giro de domingo 15/11/2026" (`xiCL5Tg0uv0l1swiXKMd`). Burn: geração `wxbszwOzdcQ5d8RrnL6t` (Talis, 852 créditos, 44,1 s). Mana: geração `jaLKUccGQ5bREgk8l6AU` (Erik, 845 créditos, 50,5 s). Descarregar como `vozes/burn.mp3` e `vozes/mana.mp3`. Não gerar de novo. (O nó `kFcfDLufYeZxoERFwnq8` do mesmo flow é uma estimativa da versão longa: nunca correu nem custou créditos.)
3. `python3 process.py vozes/burn.mp3 vozes/mana.mp3` → `data.js`, `trilha_final.wav` (24 falas, pancada 69,88 s). Os cortes saíram certos sem `separar_falas.py`.
4. `python3 bordas.py` (OK) e `python3 render.py ManaBurn_Giro_2026-11-15_kit.mp4 1.5`.
5. `python3 juntar_fecho.py ManaBurn_Giro_2026-11-15_kit.mp4 ../comum/outro/outro_binder_916.mp4 ManaBurn_Giro_2026-11-15_916.mp4`.
6. `python3 -I ../comum/qc/qc_video.py ManaBurn_Giro_2026-11-15_916.mp4 --frente manaburn`.

Capa: `MB_GIRO03_CAPA.png` (gerada com `python3 capas/capa_mb.py --scryfall kld/110 --frase "MAGIC NO BURGER KING" --foco "E NA NETFLIX" --selo "€19,90 · SÓ NA ITÁLIA" --ep "GIRO DE DOMINGO" --tag "15/11" --saida …`).
