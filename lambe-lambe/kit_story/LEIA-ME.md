# Kit do Story Lambe-lambe · «o cartaz está sendo colado no muro»

Padrão do fundador (16/11/2026): **todo carrossel Lambe-lambe sai com este Story**. Referência: LL-ART20 (`../episodios/ll-art20_caio_monteiro_shark_typhoon/story/`). Zero créditos: Python, OpenCV e FFmpeg locais; nada de IA, ElevenLabs nem instalações.

## Fazer
1. Renderizar o carrossel (kit do carrossel). A capa sem faixa de prévia é o cartaz principal.
2. Copiar `story.json` do LL-ART20 para `<episódio>/story/` e trocar: `capa`, `esquerda` (art_crop), `direita` (`foto` do fundador e/ou `carta` PNG), `detalhe` (art_crop), `nome`, `serie`, `creditos`.
3. `python3 -I lambe-lambe/kit_story/motor_story.py <story.json> <saída.mp4> [--sem-foto] [--previa]` (~50 s por versão).
   - Sem foto de terceiros: uma versão só (`--sem-foto` ou sem `foto` no JSON).
   - Com foto ainda não autorizada: `--previa` (envio privado) **e** `--sem-foto` (publicável). A versão com foto só se publica com autorização registada.
4. QC: `python3 -I comum/qc/qc_video.py <saída.mp4> --frente lambe` (o aviso «sem faixa de áudio» é esperado).
5. O motor grava 8 frames-chave ao lado do MP4 (`*_fNNN.jpg`): montar a folha de contacto e conferir.
6. MP4 e frames não se versionam. No repositório ficam `story.json` e a nota de QC.

## O que o motor faz (9 s + fecho do scanner = 12,87 s, 1080×1920, 30 fps, H.264, sem áudio)
0–1,15 s muro vazio e sombra a anunciar · 1,15–1,77 capa cai e bate (aceleração, curvatura, tremor, overshoot) · 2,3 e 2,8 fitas nos cantos de cima, ondulação do papel · 3,3–4,6 kraft, impressão da esquerda, kraft · 5,55 retrato ou carta bate à direita · 6,35 detalhe desenrola ao centro · 7,2–8,4 câmara recua, faixa preta com `nome`, `serie · BINDER` e créditos · 8,4–9,0 plano parado · 9,0–12,87 fecho do scanner (`comum/outro/outro_binder_916.mp4`, regra de todos os vídeos; `--sem-fecho` só para testes).

## Regras
- Mesma identidade do carrossel; o motor do carrossel não se altera.
- Cartas sem deformação; fitas só nos cantos de cima; nada sobre artes; créditos no plano final.
- Zona segura: capa ~270–1250 px; faixa final ~1640–1760 px. Sem corte lateral.
- Som: escolher no Instagram (não há efeitos locais adequados).
- Nunca escrever parceria no vídeo antes de a collab ser aceite.

## Publicação (refinamento de 16/11)
- Publicar o Story **logo depois do carrossel**, com o sticker de link para o post na zona livre do muro (canto superior direito, abaixo da barra do perfil). Texto do sticker: ver `story_sticker.txt` do episódio.
- O Story é a porta para o carrossel, não um conteúdo à parte: uma só ação (ver o post).
- Leitura: toques no sticker e visitas ao perfil, na rotina de domingo.
