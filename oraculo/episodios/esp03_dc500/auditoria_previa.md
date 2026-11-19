# MC-ESP03 · auditoria da prévia técnica v1 e correções da v2 (19/11/2026, 15:50–16:30)

## Inventário
- Commit `7227e2c` na `main` remota (conferido com `git ls-remote`). `esp03_render.py`, ficha, roteiro, storyboard, `dados/` e rascunhos presentes. Sem alterações por integrar.
- Prévia v1 `ESP03_PREVIA_TECNICA.mp4` e capa v1 gerados pelo motor desse commit, no ambiente da sessão (não versionados). A capa foi gerada de novo depois de suavizar a máscara do TUBO (mesmo commit).
- Recursos: `oraculo/assets/tubo_mestra_916.png` (intacta), `oraculo/musica/tubo_tema.mp3`, sons sintetizados como no `esp01_audio.py` (tum de CRT, modem, clique, pop), `comum/outro/outro_binder_916.mp4` (sem faixa de áudio; o motor junta silêncio com a duração dele, sem cortar nem reconstruir o fecho). Referências: `oraculo/esp01/esp01_render.py` (`hook()`), `oraculo/episodios/ep08b_render.py`.
- Dados: continuam inacessíveis (19/11, 15:50). As páginas do portal e do Farpas Builder abrem só com os rótulos («WR%», «HOT»), sem números.

## Diagnóstico da v1 (folha de contacto a cada 0,5–1 s)

| # | Tempo | Problema | Gravidade | Correção na v2 |
|---|---|---|---|---|
| 1 | 16–20 s | «Com essa amostra, a diferença aguenta» + faixas de Wilson de cada comandante: intervalos individuais **não** provam a diferença. Nos dados de teste, a regra antiga dizia «resiste» onde o intervalo de Newcombe da diferença inclui zero | P0 (cálculo errado / conclusão sem prova) | `calcular.py` passa a usar Newcombe (método 10) para B − A, validado no exemplo publicado (Newcombe 1998: 0,0524 a 0,3339); a frase depende do veredito; pressupostos no ecrã |
| 2 | 0,0 s | Quadro 0 com só 2 das 4 peças (entrada escalonada) | P1 | as quatro peças estão no quadro 0 e só assentam (escala 1,05 → 1) |
| 3 | 4–12 s | Um painel misturava popularidade e desempenho («POPULARIDADE × WIN RATE»), com 6 linhas técnicas de ~20 px | P1 | três painéis com título, unidade e escala próprios: POPULARIDADE (listas), DESEMPENHO (0–100 % com linha de 50 %), A DIFERENÇA (pontos, zero marcado) |
| 4 | 12–16 s e 20–26,5 s | TUBO em 4 planos quase iguais (~10,5 s, 40 % do vídeo); 20,0–26,5 s sem nenhuma mudança | P1 (repetição; intervalo > 3 s) | TUBO só 2 vezes: leitura (13,5–16,5 s, a expressão depende do veredito) e fecho (24,5–27,5 s); a pergunta final passa para as cartas A × B |
| 5 | 1,5–3 s | A pergunta tapava as cartas a meio da grelha | P1 | a pergunta passa para cima da grelha |
| 6 | todo | Pergunta, títulos, legendas e fontes fora da zona segura do QC (topo 220, base 380, direita 140 px) | P1 | layout dentro de x 80–940 e y 220–1540 (HUD e marca de água da prévia ficam fora, como nos episódios anteriores) |
| 7 | 3,6 s | O zoom revelava «[nA]» sem contexto | P1 (na final) | o ecrã do TUBO mostra número + «LISTAS»; na final é o número real |
| 8 | 20–23 s | Pergunta genérica («Qual comandante só parece forte?») | P1 | pergunta ligada à descoberta (campo `pergunta`, ex.: trocar A por B), a escrever com os dados |
| 9 | todo | Textos de leitura com 28–34 px de corpo | P1 | leitura ≥ 38–44 px (MONO negrito), fontes 34–36 px (altura de maiúscula ≈ 25 px), legenda 44 px |
| 10 | capa | «POPULAR ≠ FORTE» afirmava a tese antes dos dados | P1 | frase pela tese que o cálculo devolver; sem dados, «MAIS JOGADO, MAIS FORTE?», TUBO desconfiado |
| 11 | 0–27 s | Placeholders «[A]», «CARTA A»… | P0 numa final · aceite só na prévia, com a marca «PRÉVIA TÉCNICA · SEM DADOS» | depende do Gate A |

Som (v1 e v2): trilha oficial; corte seco de 0,6 s alinhado à revelação da diferença (16,5 s); um som curto em cada revelação; −14,3 LUFS; pico −4,9 dBTP; sem cliques nem saturação ouvidos na medição.

## QC da candidata v2 (`ESP03_PREVIA_TECNICA_v2.mp4`, executado)
- `qc_video.py --frente tubo`: 1080×1920 · 30 fps · 31,37 s (27,5 s + fecho) · −14,3 LUFS · pico −4,9 dBTP · fecho presente a partir de 27,5 s · «sem problemas mensuráveis».
- Corte lateral (cropdetect): 1080:1920 em 724 de 791 amostras; as restantes são cenas de terminal com bordas escuras, sem conteúdo cortado.
- Maior intervalo sem mudança relevante: 2,6 s (21,9–24,5 s), medido como >0,6 % dos píxeis a mudar >40 níveis entre quadros (10 fps).
- Conferido a olho na folha de contacto: quadro 0 completo; pergunta aos 2–3 s; nada tapa cartas ou fontes; TUBO no modelo.

## Pendentes
- P0 da final: dados, cartas Scryfall, pergunta, frase de leitura e capa — todos dependem do Gate A.
- P1 na final: confirmar que nenhum nome de comandante passa de 860 px a 40 px (o motor encolhe, mínimo 20; a rever com os nomes reais).
- P2: a trilha entra cheia aos ~12,6 s do tema e não coincide com nenhum bloco (o mergulho acontece aos 3,4 s); o fecho do TUBO aos 24,5–27,5 s varia só na expressão.
