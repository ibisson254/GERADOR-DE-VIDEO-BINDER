# QC · Mana & Burn Ep. 10 · Numot (11/11/2026)

Ficheiro: `ManaBurn_Ep10_Numot_916.mp4` (não versionado; recria-se com os passos abaixo).

- Formato: 1080x1920, 30 fps, 54,70 s (50,83 s + fecho do scanner de 3,87 s).
- Áudio: −14,5 LUFS, pico −1,8 dBTP (1.ª montagem a −0,8 dBTP → limitador `alimiter=limit=0.8` só no áudio, vídeo copiado).
- `comum/qc/qc_video.py`: sem problemas mensuráveis; fecho presente a 50,83 s.
- `bordas.py`: OK (423 quadros de TV, laterais 12–1068 px, topo 300 px).
- Folha de contacto (olho): carta inteira nos planos de TV, destaques alinhados às linhas do Oracle, inserts com crédito, legendas na zona segura, TV desliga → ponto verde → fecho.
- P0: nenhum. P1: nenhum aberto (pico corrigido; texto do medidor encurtado para não cortar no zoom).
- P2 (aceites): plano geral ~5 s nas falas 5–6 (o insert do Wildfire cobre a mudança); capa tirada do gancho a 3,2 s.
- A conferir pelo fundador na escuta: pronúncia de "Numot", "Devastator" e "Wildfire" (grafia fonética no `tts`).

Recriar: copiar `episode.json`, `episode.js` e `data.js` desta pasta para `manaburn/`; vozes do ElevenLabs (flows `wRCBNMr8s9tt3eNXKooL` Burn/Talis e `nMFrSrtT2mkzQgPn9DM8` Mana/Erik, eleven_v4) como `burn.mp3`/`mana.mp3`; `python3 render.py ManaBurn_Ep10_Numot_916.mp4` (com `trilha_final.wav` de `process.py burn.mp3 mana.mp3`) → `python3 -I episodios/ep09_dack/juntar_fecho.py ManaBurn_Ep10_Numot_916.mp4 ../comum/outro/outro_binder_916.mp4 final.mp4` → limitador de áudio acima.
