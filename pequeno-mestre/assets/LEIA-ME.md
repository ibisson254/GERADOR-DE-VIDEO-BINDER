# Assets do Pequeno Mestre · kit v1 (31/10/2026)

Ilustrações geradas pelo fundador numa ferramenta de imagem, a partir da especificação no fim deste ficheiro. Fundo bege liso; os recortes com transparência estão em `recortes/` (gerados por `../recortar.py`).

## Inventário

| ID | Ficheiro | O que é | Recorte | Notas |
|---|---|---|---|---|
| A2 | `personagem/A2_corpo_inteiro_leao.jpg` | Corpo inteiro, de frente, a segurar o leão; mão na bolsinha | sim | Ponta do rabo do leão cortada na borda da imagem |
| A4 | `personagem/A4_alegria.jpg` | Busto: olhos fechados de alegria, mãos a balançar | sim | |
| A5 | `personagem/A5_barulho_fones.jpg` | Busto: fones na cabeça, olhos fechados, calmo | sim | Versão com cabelo preto (a castanha foi descartada) |
| B7 | `personagem/B7_foco_bichos.jpg` | Busto: olha para baixo e alinha os bichos nas mãos | sim | Fundo com textura de papel, mais claro |
| K1 | `personagem/K1_capa_sala.jpg` | Cena completa na sala, com a fila de bichos e o dinossauro | não | Para capa ou cena parada; personagem colado ao fundo |
| B1 | `fala/B1_base_boca_fechada.jpg` | Busto base: boca fechada, olhos abertos | sim | **Composto**: B2 com a boca de B5 (quadros alinhados ao pixel). Se a ferramenta gerar uma B1 própria, substituir |
| B2 | `fala/B2_boca_entreaberta.jpg` | Boca entreaberta | sim | |
| B3 | `fala/B3_boca_A.jpg` | Boca bem aberta ("A") | sim | |
| B4 | `fala/B4_boca_O.jpg` | Boca redonda ("O") | sim | |
| B5 | `fala/B5_piscar.jpg` | Olhos fechados, boca fechada (piscar) | sim | |
| D1 | `bichos/D1_leao_lado.jpg` | Leão de lado, virado à direita | sim | |
| D1b | `bichos/D1b_leao_frente.jpg` | Leão sentado, de frente | sim | |
| D2 | `bichos/D2_trex.jpg` | T-rex verde | sim | |
| D3 | `bichos/D3_girafa.jpg` | Girafa | sim | |
| D4 | `bichos/D4_tigre.jpg` | Tigre | sim | |
| D5 | `bichos/D5_panda.jpg` | Panda sentado | sim | Resto leve de sombra no chão |
| D6 | `bichos/D6_elefante.jpg` | Elefante (versão 2, cores quentes) | sim | A versão 1 (traço fino, cores apagadas) foi descartada |
| E1 | `cenario/E1_sala.jpg` | Sala vazia: cenário fixo | não | 1856×2304 (4:5); para 9:16 cortar ou estender o chão |
| P1 | `cenario/P1_movel_azulejos.jpg` | Móvel de madeira com azulejos | sim | Peça de cenário para compor na sala |
| R1 | `referencias/R1_inspiracao_triciclo.jpg` | Primeira ilustração de referência | — | Só referência (baixa resolução) |
| R2 | `referencias/R2_folha_modelo.jpg` | Folha de personagem (poses e expressões) | — | Referência de consistência |
| R3 | `referencias/R3_folha_fala_v1_substituida.jpg` | Primeiro kit de fala numa folha só | — | Substituído por B1–B5 (sem cordão, não alinhado) |
| R4 | `referencias/R4_leao_e_trex_juntos.jpg` | Leão e T-rex lado a lado | — | Escala relativa dos dois |

**Em falta (não bloqueia o primeiro episódio):** A1 (de pé, parado, braços soltos), A3 (a apontar), A6 (sentado), C1–C5 (corpo sem braços + braços soltos), E2 (tapete visto de cima).

## Recortes

`python3 pequeno-mestre/recortar.py` (a partir da raiz) refaz todos os PNG de `recortes/`. Os quadros B1–B5 saem com a mesma caixa (1381×1957 a partir de x=379, y=31 do original), por isso ficam alinhados para o lip-sync. Para um asset novo: acrescentar uma linha em `ASSETS` no script.

## Especificação para gerar assets novos

Anexar sempre R2 (folha de personagem) e um busto aprovado (B1). Regras que todas as imagens cumprem:

- O mesmo menino: black power redondo **preto**, pele morena quente, olhos castanhos grandes, bochechas redondas; camiseta de listras largas verde e branca, gola verde; fones azuis no pescoço; bolsinha laranja no quadril esquerdo dele, com cordão creme do ombro direito, com pequenos símbolos do infinito em arco-íris; bermuda cáqui, meias brancas, ténis castanhos.
- Ilustração pintada de livro infantil, contorno castanho-escuro, luz quente de cima à esquerda.
- Fundo bege liso, sem sombra no chão nem textura; figura inteira dentro do quadro, com margem; sem texto.
- Variações de um mesmo quadro (bocas, olhos): **editar** a imagem base e mudar só a parte pedida, para continuarem alinhadas.
- Bichos: brinquedos fofos no mesmo estilo de D1–D6, de lado e virados à direita, fundo bege liso.
