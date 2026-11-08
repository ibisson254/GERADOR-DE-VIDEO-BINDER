# Giro de domingo nº 2 · 08/11/2026 · como recriar o vídeo

O vídeo final não está no repositório (regra do estúdio). Para o recriar, numa cópia de `manaburn/` (kit v2, sala v3):

1. Copiar `episode.js`, `episode.json` e `cards/giro_*.png` desta pasta para a raiz da cópia do kit (as telas tipográficas recriam-se com `python3 telas_giro.py`).
2. Vozes: flow ElevenLabs "Mana & Burn — Giro de domingo 08/11/2026" (`gBn9kgrx6Gf3cgGdSSws`). Burn: geração `1RV7lgN2vEh3QPkNMZpK` (Talis, 1.017 créditos). Mana: geração `69TTbm0Bj6poPoVwgzUU` (Erik, 1.183 créditos). Descarregar como `vozes/burn.mp3` e `vozes/mana.mp3`; transcrições Scribe do mesmo flow como `vozes/burn_words.json` e `vozes/mana_words.json`. Não gerar de novo.
3. `python3 separar_falas.py vozes/burn.mp3 vozes/burn_words.json vozes/burn_sep.wav` (e o mesmo para o Mana).
4. `python3 process.py vozes/burn_sep.wav vozes/mana_sep.wav` → `data.js`, `trilha_final.wav` (24 falas, fim 103,6 s).
5. `python3 bordas.py` (OK) e `python3 render.py ManaBurn_Giro_2026-11-08_kit.mp4 1.5` (capa no 1,5 s).
6. `python3 juntar_fecho.py ManaBurn_Giro_2026-11-08_kit.mp4 ../comum/outro/outro_binder_916.mp4 ManaBurn_Giro_2026-11-08_916.mp4`.
7. Áudio final: `volume=+0,2 dB` + `alimiter=limit=0.66` sobre a trilha do ficheiro do passo 6 (o loudnorm de 2 passes deixou o pico acima de −1 dBTP depois do AAC); vídeo copiado sem reencode.
8. `python3 -I ../comum/qc/qc_video.py ManaBurn_Giro_2026-11-08_916.mp4 --frente manaburn`.

Telas da retrospectiva (`giro_conde.png`, `giro_burn.png`, `giro_tubo.png`, `giro_previsao.png`): quadros reais renderizados pelos motores dos próprios episódios (ver `ficha.md`), recortados para 744×1040.
