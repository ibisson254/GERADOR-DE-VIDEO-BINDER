# MC-ESP03 · storyboard v2 (implementado em `esp03_render.py`, `BEAT`)

1080×1920, 30 fps, 27,5 s + fecho. Zona segura: x 80–940, y 220–1540 (HUD da série e marca de água da prévia ficam fora, como nos episódios anteriores). Leitura ≥ 38 px de corpo; fontes 34–36 px; legenda 44 px a y 1490. Cartas sempre inteiras. Cada grandeza tem o seu painel, a sua unidade e a sua escala. Timecodes da prévia; na final ajustam-se às palavras da voz, sem mudar a ordem.

| # | In–out | Plano / imagem | Carta | Número e unidade | Texto no ecrã | Voz | TUBO | Movimento | Som | Fonte | Objetivo |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0,00–0,30 | Grelha 2×2 completa sobre o TUBO escurecido | A (cima esq.), B (baixo dir.) | rótulos «MAIS JOGADO · LISTAS» e «MAIOR WIN RATE» | «DUEL COMMANDER 500 · [per]»; linha de fonte | — | escurecido | peças assentam 1,05 → 1 | tum de CRT + 4 cliques | portal | conflito no quadro 0, sem som |
| 2 | 0,30–1,00 | Scan verde sobre a carta A; contorno acende | A | — | — | — | — | scan 0,5 s | modem | — | aponta o mais jogado |
| 3 | 1,00–1,60 | Números entram nas peças | — | «[nA] LISTAS · [qA] do meta» / «[iB] WIN RATE · em [dB] partidas» | — | — | — | entrada | pop | galeria + matchups | unidades claras |
| 4 | 1,60–2,00 | Destaque salta para B; lado A escurece | B | — | — | — | — | contorno troca | pop agudo | — | o rival |
| 5 | 2,00–3,00 | Pergunta por cima da grelha | A, B | — | «O MAIS JOGADO É / O QUE MAIS VENCE?» | — | — | escreve a 60 cps | clique | — | descoberta até 3 s |
| 6 | 3,00–4,00 | Peças sobem; ecrã do TUBO mostra o número; mergulho | — | «[nA] LISTAS» | legenda | «[A]: [nA] listas.» | ecrã | subida 0,4 s + zoom 0,6 s | modem | galeria | entra na investigação |
| 7 | 4,00–8,50 | Painel POPULARIDADE: 5 barras de listas (escala de 0); A a verde aos 5,6 s, B a âmbar aos 7,2 s (B acrescentada abaixo de «…» se não estiver no top 5) | A aos 5,6 s, B aos 7,2 s | listas por comandante | «> POPULARIDADE · listas registadas no portal · [per]»; «lista ≠ jogador ≠ partida» | «O mais jogado do portal, [qA] do meta. [B]: só [nB] listas.» | — | barras crescem 0,6 s, desfasadas | clique, pop, pop | galeria | quem escolhe |
| 8 | 8,50–13,50 | Painel DESEMPENHO: duas colunas 0–100 %, linha de 50 % | A sobre a coluna A, B sobre a B | «[iA]», «[iB]»; aos 12,0 s «em [dA]/[dB] partidas» a âmbar | «> DESEMPENHO · win rate · só os 20 com mais partidas» | «No win rate, [A] faz [iA]. [B], [iB]. Em [dA] e [dB] partidas.» | — | colunas crescem; denominadores com pulso | clique, pop, clique | matchups | quem ganha, com a amostra à vista |
| 9 | 13,50–16,50 | TUBO sai do terminal; aos 15,0 s «ESCOLHE ≠ GANHA» no ecrã dele | — | — | legenda | «Popularidade mede quem escolhe. Win rate mede quem ganha.» | Analítico → Confiante ou Desconfiado (veredito) | zoom-out 0,6 s | tum curto, clique | opinião | a regra que o espectador leva |
| 10 | 16,50–21,50 | Painel A DIFERENÇA: eixo simétrico em pontos, zero marcado; ponto aos 17,2 s, margem aos 18,0 s, veredito aos 19,0 s, nota aos 20,2 s | — | «[dif]» e a margem de 95 % | «> A DIFERENÇA É REAL?»; «ponto = diferença · faixa = margem de 95 %»; veredito; «aproximado: jogos entre os dois contam nos dois lados da conta» | por cenário | — | corte seco 0,6 s; margem desenha-se 0,8 s | silêncio → pop, pop agudo, clique | cálculo do BINDER (Newcombe) | pagamento do gancho |
| 11 | 21,50–24,50 | Cartas A × B lado a lado | A, B | «[iA] · [nA] listas» / «[iB] · [nB] listas» | pergunta do cenário | pergunta | — | cartas entram dos lados | clique | portal | pergunta ligada à descoberta |
| 12 | 24,50–27,50 | TUBO; aos 26,0 s muda de expressão | — | — | legenda | «Probabilidade calculada. Humanos, imprevisíveis.» | Analítico → Confiante/Desconfiado | push-in lento | tum curto | — | assinatura |
| 13 | 27,50–fim | Fecho oficial do scanner, inteiro | — | — | — | — | — | corte | (sem áudio no ficheiro do fecho) | — | ponte para o app |

Maior intervalo sem mudança relevante na prévia: 2,6 s (21,9–24,5 s).

## Capa (`CONTEXTO.md` §7.3)
Frase pela tese do cálculo: «POPULAR ≠ FORTE» (`B_fora_margem`), «AMOSTRA CURTA» (`dentro_margem`), «O HYPE ACERTOU» (`A_melhor`); sem dados, «MAIS JOGADO, MAIS FORTE?». Foco a verde: [iB] (ou [iA] em `A_melhor`). TUBO Confiante ou Desconfiado pelo cenário. Faixa «META EM CURTO · ESP. 03», sem collab. Fundo: cartas A e B desfocadas. Recorte 3:4 (`ESP03_CAPA_grelha.png`) e miniatura conferidos.
