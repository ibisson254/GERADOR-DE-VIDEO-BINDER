# MC-ESP03 · storyboard e direção de montagem (cenário 1; os outros mudam só o texto)

1080×1920, 30 fps. Timecodes provisórios: ajustam-se às palavras da voz (`words.json`) mantendo a ordem e a regra de ≤ 3 s sem mudança. Dentro do tubo = só dados verificados com linha de fonte; fora = TUBO e opinião. Textos de leitura ≥ 28 px; linha de fonte ≥ 24 px; cartas inteiras (arte e rodapé), nunca recortadas; nenhum print de transmissão; barras sempre a partir de 0 e no mesmo eixo.

| # | In–out | Imagem e composição | Material | Texto no ecrã | Movimento / transição | TUBO | Voz | Som | Fonte do dado |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0,00–0,30 | Grelha dupla 2×2 em ecrã inteiro sobre o TUBO escurecido (opacidade ~20 %) | carta A, carta B (Scryfall) | cabeçalho «DUEL COMMANDER 500 · [per]» (mono 34 px) | as quatro peças entram com um passo de 6 px e escala 0,96→1 | escurecido ao fundo | — | «tum» CRT | — |
| 2 | 0,30–1,00 | scan verde atravessa a carta A; contorno verde acende; quadro do número A conta até [nA] | carta A | «[nA] LISTAS» (Inter Black 120 px) + «[qA] do meta» (40 px) | scan vertical 0,5 s; contagem | — | «O comandante mais jogado…» | chiado de modem + bip | galeria, [per] |
| 3 | 1,00–3,00 | destaque salta para B; A escurece a 40 %; número B: «[iB]» e «em [dB] partidas»; pergunta por cima | carta B | «O MAIS JOGADO É O QUE MAIS VENCE?» (Inter Black 64 px, 2 linhas) · linha de fonte (26 px) | contorno passa de A para B; pergunta escreve-se a 40 cps | — | «…não é o que mais vence.» | bip duplo | matchups, [per] |
| 4 | 3,00–4,20 | quadros sobem para uma fila por cima do TUBO; o ecrã do TUBO mostra «[nA]»; mergulho | as 4 peças | — | subida 0,4 s + zoom no ecrã 0,8 s | ecrã acende | «[A]: [nA] listas.» | chiado de modem | — |
| 5 | 4,20–8,00 | terminal: barra horizontal de A (listas) e, por baixo, «WIN RATE [iA]»; carta A em insert à esquerda | carta A | «[A] · [nA] listas · [qA] do meta · win rate [iA] em [dA] partidas» (mono 32 px) · fonte | barra cresce 0,6 s; insert entra a 5,5 s | — | «…[qA] do meta. Win rate: [iA].» | tique por número | galeria + matchups |
| 6 | 8,00–12,00 | barra de B no mesmo eixo de A (0–100 %); carta B em insert à direita | carta B | «[B] · [nB] listas · win rate [iB] em [dB] partidas» · fonte | barra cresce; a 10 s destaque verde em [iB] | — | «[B] aparece bem menos. Mas vence [iB]… em [dB] partidas.» | bip | matchups |
| 7 | 12,00–14,20 | sai do tubo: TUBO em plano médio | TUBO mestra | legenda terminal palavra a palavra | zoom-out 0,6 s | Analítico | «Popularidade mede quem escolhe.» | modem invertido | opinião |
| 8 | 14,20–16,00 | TUBO, ecrã mostra «ESCOLHE ≠ GANHA» | TUBO | legenda terminal | corte com glitch curto | Desconfiado | «Win rate mede quem ganha.» | glitch | opinião |
| 9 | 16,00–20,00 | **pagamento:** volta ao terminal; as duas barras com faixa de 95 % (traço claro) no mesmo eixo; veredito | — | «DIFERENÇA ACIMA DO ACASO» (verde) · «cálculo do BINDER · intervalo de 95 %» (26 px) | corte seco da trilha (~0,6 s) com aproximação lenta; faixas desenham-se 0,8 s | — | «E não é sorte: com essa amostra, a diferença aguenta.» | silêncio → bip | cálculo do BINDER sobre o portal |
| 10 | 20,00–23,00 | TUBO, pergunta em mono no ecrã dele | TUBO | «QUAL COMANDANTE SÓ PARECE FORTE?» (48 px) | push-in lento | Confiante | «Então, qual comandante você acha que só parece forte?» | banda volta | — |
| 11 | 23,00–26,50 | TUBO; frase de fecho | TUBO | legenda terminal | — | Analítico | «Probabilidade calculada. Humanos, imprevisíveis.» | final da trilha | — |
| 12 | 26,50–fim | fecho oficial do scanner | `comum/outro/outro_binder_916.mp4` | — | corte | — | — | do fecho | — |

Maior intervalo sem mudança: 3,0 s (plano 6, com o destaque a 10 s a partir-lo). Easter egg: no máx. 1, na chuva de código do plano 5–6, decidido com os números.

## Mudanças por cenário
- Cenário 2: plano 9 com veredito âmbar «DIFERENÇA DENTRO DO ACASO» e a sobreposição das faixas destacada.
- Cenário 3: plano 3 destaca A e não salta para B; plano 9 «O HYPE ACERTOU».
- Conversão em vez de win rate: todos os rótulos «WIN RATE» passam a «CONVERSÃO TOP 4» e «partidas» a «listas».

## Capa (`CONTEXTO.md` §7.3) — layout fechado, conteúdo pendente
Frase: cenário 1 «POPULAR ≠ FORTE» · cenário 2 «AMOSTRA CURTA» · cenário 3 «O HYPE ACERTOU». Foco (verde fósforo ~400 px): o número de B ([iB]) no cenário 1 e 2; [iA] no 3. TUBO: Desconfiado (1, 2) ou Confiante (3). Faixa: «META EM CURTO · ESP. 03», sem collab à direita. Fundo: cartas A e B desfocadas e escurecidas. Gerar também `ESP03_CAPA_grelha.png` (recorte y 240–1680) e conferir em miniatura.
