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

## v2 · refinos de retenção (11/11/2026, 14:46, pedido do fundador)

Mesmas vozes (sem créditos novos); só ritmo, planos e destaques.
- Ritmo: Burn ×1,10, Mana ×1,15, silêncios internos ≤ 0,10 s, réplicas do Burn a entrar por cima → 47,8 s + fecho = 51,65 s (era 54,7 s).
- Picos de reação: "DOIS" (fala 1) e "CRIME" (fala 11) em caixa alta → tremor e som de raiva; falas 7 e 11 em close do Burn de braços para cima (5 tremores, eram 3).
- Recompensa visual: fala 8 corta para a carta com destaque no "6/6" (prova do "sai do incêndio sorrindo"); fala 2 passa a `tv2`. 3 cortes para a TV (eram 2), 11 cortes no total.
- Áudio: −14,1 LUFS, pico −2,0 dBTP (limitador + loudnorm TP −1,5). QC automático sem problemas; `bordas.py` OK (482 quadros de TV, laterais 10–1068 px).
- Capa: quadro do gancho a 3,2 s ("somem DOIS!").
