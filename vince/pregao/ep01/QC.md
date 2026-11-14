# Relatório de controlo de qualidade · VV-PG01 · v1 (14/11/2026)

Ficheiro: `PregaoMagic_VV-PG01_v1_916.mp4` (não versionado). Três renders: v1 → correções → v2 → correção → v3 = entregue como v1 pública.

## Medições automáticas (`comum/qc/qc_video.py`, ffmpeg)

| Item | Resultado |
|---|---|
| Formato | 1080×1920, 30 fps, H.264 yuv420p, AAC 256 kb/s 48 kHz |
| Duração | 45,07 s (41,2 s de episódio + 3,87 s de fecho) |
| Loudness / pico | −14,1 LUFS integrado / −1,5 dBTP |
| Fecho oficial | presente a partir de 41,2 s, diferença média 0,04 (intacto, sem encurtar) |
| Corte lateral | cropdetect 1080:1920:0:0 nos 1350 quadros |
| Problemas P0/P1 mensuráveis | nenhum |

## Imagem (conferido a olho: folha de contacto 1/s + 40 quadros nas transições)

| Critério | Resultado |
|---|---|
| Primeiro quadro com cartas | sim: 16 cartas reais no quadro 0 |
| Integridade das cartas | imagens oficiais inteiras, sem recolor; nos planos de leitura todas as cartas estão inteiras. A parede (0–1,5 s e 37,8–41,2 s) corta cartas nas bordas por desenho (textura, não leitura). |
| Match cuts | carta → moldura → gráfico (1,56–2,40); número → zoom → carta (4,13–4,67); seta → queda (20,30–20,86) |
| Sincronização musical | impactos visuais em 3,16 · 13,72 · 20,63/20,86 · 27,49 · 34,35… 41,20, medidos no `MUSIC_MAP.md` |
| Legibilidade | textos ≥ 28 px; planos de leitura 2,3–3,4 s; tudo dentro da zona segura (x ≤ 930, y 220–1540) |
| Repetição | nenhuma transição repetida em sequência |
| Telas vazias | nenhuma; o quadro escuro antes da queda do Picard (v2) foi corrigido |
| Números provisórios | nenhum: a tensão usa "+ ? ? %" (a v1 interna mostrava dígitos a rodar; removido para que um quadro pausado nunca mostre um número falso) |

## Áudio (medido, não ouvido)

| Critério | Resultado |
|---|---|
| Música | faixa original sem alteração de composição, −2 dB; sem distorção nem clipping (0 amostras ≥ 0 dBFS) |
| Efeitos | 10–15 dB abaixo da música em cada evento; nenhum whoosh por corte (4 no total); nada de caixa registadora, moedas, alarmes |
| Silêncio intencional | break 26,55–27,40 respeitado (só um ping a −14 dB) |
| Telemóvel | correlação L/R 0,78; mono −0,5 dB face ao estéreo (sem cancelamento); impactos têm transiente agudo além do sub; micro-recompensas entre 660 e 1980 Hz |
| Voz | **inexistente** (créditos não autorizados) |

## Conteúdo

| Critério | Resultado |
|---|---|
| Preços verificados | 5 cotações, conferidas com `fontes.md` |
| Fontes e datas visíveis | em todos os planos com número |
| Reais | conversão marcada "≈" com o câmbio e a data no ecrã |
| Afirmações inventadas | nenhuma; causas só as que o MTGStocks dá; queda sem causa atribuída |
| Previsões / recomendação | nenhuma; "Não é recomendação de compra ou venda" no fecho e na legenda |

## Pendente antes de publicar

1. Narração autorizada e integrada (P1: a missão pede voz).
2. Ouvir no telemóvel (P1).
3. Licença comercial da faixa "Auction of Power" confirmada pelo fundador (P0 se não houver licença).
4. Atualizar as cotações se a publicação passar de 16/11 (o vídeo é um retrato de 13/11).
