# LL-ART20 · Story «o cartaz está sendo colado no muro» — edição e QC

Missão do fundador de 16/11/2026 (18:51). Zero créditos: sem IA, sem ElevenLabs, sem instalações. Só Python, OpenCV e FFmpeg locais.

## Como se faz
`python3 -I story.py <cartas> <01_capa.png da versão A> <foto|-> <saida.mp4> [--previa]`
- Cartas: as mesmas do carrossel (Scryfall, ver `../fontes.md`). Capa: `01_capa.png` renderizado pelo `../carrossel.py` (versão A, sem faixa de prévia).
- Peças isoladas sem segmentação generativa: a capa é recortada pela máscara exata da folha rasgada (`rasgo_alpha(1000,1290,16,9)`, −0,4°) mais o selo azul, por isso não há muro dentro do muro. As outras peças (papel kraft, impressões, carta, fita, faixa preta, recorte P&B da foto) são desenhadas pelo `motor_padrao.py` sobre fundo preto e branco e separadas por matting. O motor não foi alterado.
- O muro é reconstruído a partir da cor e das bordas dos modelos aprovados (restos de cartazes antigos nas laterais), com grão de tinta.
- Textos finais com as fontes do kit (`compor.camada`).

## Timeline (30 fps, 270 frames, 9,0 s)
| Tempo | Ação | Movimento |
|---|---|---|
| 0,0–1,15 | Muro vazio | câmara 1,14× a derivar; a partir de 0,55 s, uma sombra grande anuncia o cartaz |
| 1,15–1,77 | A capa chega do alto | aceleração cúbica, escala 1,25→1, rotação −9°→−1,2°, curvatura em perspetiva, sombra projetada que encolhe; no impacto: tremor de 0,2 s e overshoot amortecido |
| 2,30 / 2,78 | Fitas nos dois cantos de cima | entram a rodar (25°) e a encolher (1,5→1), com pequeno ressalto; ondulação de luz do papel a desaparecer |
| 3,30 / 3,72 / 4,20 | Kraft, impressão de Marauding Blight-Priest, kraft | cada uma de uma direção, com rotação, sombra e assentamento |
| 3,0–5,5 | Câmara | desce o foco para a parte de baixo do muro |
| 5,55 | A: retrato P&B (foto do fundador) · B: carta Archmage Emeritus | bate sobre o kraft da direita |
| 6,35 | Detalhe de Boltwave | desenrola de cima para baixo |
| 7,2–8,4 | Revelação | câmara recua para 1,0× (o muro tem parallax de 0,6) |
| 7,25 | Faixa preta | sobe com ressalto: «CAIO MONTEIRO · Artistas de Magic · BINDER» e créditos |
| 8,4–9,0 | Plano fixo para leitura | — |

## Exportações (não versionadas)
- `LL_ART20_story_previa_com_foto.mp4`: com foto e faixa vertical «PRÉVIA · AGUARDA AUTORIZAÇÃO» na lateral direita. Só para envio privado ao Caio.
- `LL_ART20_story_sem_foto.mp4`: versão B, para publicar enquanto a foto não estiver autorizada.
- H.264, yuv420p, CRF 18, preset veryfast, 1080×1920, 30 fps, 9,0 s. **Sem áudio**: não há efeitos sonoros locais adequados; acrescentar som no próprio Instagram.

## QC (16/11/2026)
- ffprobe: as duas versões em h264, 1080×1920, 30/1, 270 frames, 9,000 s: OK.
- Folha de contacto com 8 frames-chave por versão (0,5 / 1,5 / 2 / 3 / 4,6 / 6 / 7 / 8,9 s), entregue ao fundador.
- Cartas sem deformação (escala uniforme; perspetiva só durante o voo); fitas só nos cantos de cima; nenhum texto sobre as artes: OK.
- Zona segura: capa entre ~270 e ~1250 px; nome final em ~1640–1760 px (acima da barra de resposta dos Stories). Sem corte lateral: OK.
- Créditos no plano final: cartas com set e número · Caio Monteiro · © Wizards of the Coast. Sem alegação de parceria: OK.
- B sem vestígios da foto: OK. A identificada como prévia: OK.
- Limitações: os créditos (15 px) são de rodapé e leem-se mal num telemóvel, como no carrossel. A versão com foto não se publica sem autorização expressa.
