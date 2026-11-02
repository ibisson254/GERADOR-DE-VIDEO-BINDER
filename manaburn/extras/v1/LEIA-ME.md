# Mana & Burn · kit do gerador (24/10/2026)

Gera os Reels 9:16 (1080x1920, 30 fps) da série Mana & Burn do BINDER Vision. Roteiro, legendas e regras: documento "BINDER Marketing — Série Mana & Burn · 24/10/2026" no Google Drive.

## O que tem aqui
- index.html: a cena inteira (sala, dupla, TV, TV SAL, legendas, fecho com a logo). Lê data.js e episode.js.
- episode.js: o que muda por episódio: carta na TV e crédito, pose e plano de cada fala, destaques no texto da carta, cartas citadas, programação da TV SAL (putômetro, placar da mesa, manchetes).
- episode.json: falas (as palavras entre *asteriscos* ficam amarelas na legenda) e folgas entre falas.
- process.py: corta as faixas do ElevenLabs (uma por personagem, falas separadas por pausas longas), monta o bate-volta, alinha o "Comenta aí" com a parada seca da música e mixa a trilha (-14 LUFS). Gera data.js e trilha_final.wav.
- sfx.py: efeitos sintetizados (estática nos cortes para a TV, clique do controle, TV de tubo desligando, pop das cartas citadas).
- render.py: renderiza quadro a quadro e gera o MP4 e a capa. preview.py: quadros soltos para conferir.
- musica.mp3: faixa "midnight_throttle" feita pelo Ibisson no Gemini. tv_asset.png: foto da TV. logo/: marca BINDER Vision.
- cards/: PNGs das cartas (main.png = carta do episódio atual; Stasis Alpha no Ep. 2).
- burn_ep2.mp3 e mana_ep2.mp3: vozes do Ep. 2 (plano grátis do ElevenLabs: gerar de novo no Starter antes de publicar).
- extras/ep1/: código e vozes do Ep. 1 (versão anterior do modelo).

## Como rodar
Precisa de Python 3 (numpy, Pillow, playwright com Chromium) e ffmpeg.
1. Coloque o PNG da carta em cards/main.png e ajuste episode.js (crédito, poses, destaques medidos no PNG, manchetes).
2. Escreva as falas em episode.json e gere no ElevenLabs uma faixa do Burn e uma do Mana, com [long pause] entre as falas.
3. python3 process.py burn.mp3 mana.mp3
4. python3 preview.py 2.5 10.5 18.0 (confere quadros)
5. python3 render.py ManaBurn_EpN_Nome_916.mp4 (uns 5 minutos)

## Regras que valem para todo episódio
- Carta real, inteira, com o rodapé visível e nada por cima. Crédito: "Na TV: {carta} ({coleção}, {ano}), nº {n}. Arte: {artista}. © Wizards of the Coast."
- Putômetro = Salt Score do EDHREC dividido por 4 (a escala de votação vai de 0 a 4), com a fonte na tela.
- Legenda limpa + comentário fixado (pergunta objetiva na primeira linha + complemento).
