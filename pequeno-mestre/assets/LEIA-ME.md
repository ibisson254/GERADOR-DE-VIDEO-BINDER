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
| M1 | `audio/M1_aventura_no_gramado.mp3` | Música de fundo da série, composição do fundador (2:59, −11,8 LUFS) | — | Trecho calmo 0:03–0:45; evitar 0:55–1:20, 1:55–2:20, 2:40–2:48 |
| R1 | `referencias/R1_inspiracao_triciclo.jpg` | Primeira ilustração de referência | — | Só referência (baixa resolução) |
| R2 | `referencias/R2_folha_modelo.jpg` | Folha de personagem (poses e expressões) | — | Referência de consistência |
| R3 | `referencias/R3_folha_fala_v1_substituida.jpg` | Primeiro kit de fala numa folha só | — | Substituído por B1–B5 (sem cordão, não alinhado) |
| R4 | `referencias/R4_leao_e_trex_juntos.jpg` | Leão e T-rex lado a lado | — | Escala relativa dos dois |

**Em falta:** P2 (armário antigo, refúgio; o P1 faz de armário até lá). A1 (de pé, parado, braços soltos), A3 (a apontar), A6 (sentado), C1–C5 (corpo sem braços + braços soltos), E2 (tapete visto de cima).

## Recortes

`python3 pequeno-mestre/recortar.py` (a partir da raiz) refaz todos os PNG de `recortes/`. Os quadros B1–B5 saem com a mesma caixa (1381×1957 a partir de x=379, y=31 do original), por isso ficam alinhados para o lip-sync. Para um asset novo: acrescentar uma linha em `ASSETS` no script.

## Especificação para gerar assets novos

Anexar sempre R2 (folha de personagem) e um busto aprovado (B1). Regras que todas as imagens cumprem:

- O mesmo menino: black power redondo **preto**, pele morena quente, olhos castanhos grandes, bochechas redondas; camiseta de listras largas verde e branca, gola verde; fones azuis no pescoço; bolsinha laranja no quadril esquerdo dele, com cordão creme do ombro direito, com pequenos símbolos do infinito em arco-íris; bermuda cáqui, meias brancas, ténis castanhos.
- Ilustração pintada de livro infantil, contorno castanho-escuro, luz quente de cima à esquerda.
- Fundo bege liso, sem sombra no chão nem textura; figura inteira dentro do quadro, com margem; sem texto.
- Variações de um mesmo quadro (bocas, olhos): **editar** a imagem base e mudar só a parte pedida, para continuarem alinhadas.
- Bichos: brinquedos fofos no mesmo estilo de D1–D6, de lado e virados à direita, fundo bege liso.


Fontes: `../fontes/Baloo2-700.ttf` e `Baloo2-800.ttf` (Baloo 2, licença SIL OFL), usadas nas legendas e nas cartas.

## Pedido de asset · P2 armário antigo (01/11/2026)

Gerar na ferramenta de imagem, anexando P1 e E1 como referência de estilo. Guardar como `cenario/P2_armario.jpg` (e `P2b_armario_dentro.jpg`, se gerar a segunda) e acrescentar uma linha em `ASSETS` no `recortar.py`.

P2 (peça de cenário, recortável):
> Children's picture-book illustration, soft painted brush texture, dark brown outlines, warm light from the upper left, same style as the attached references. An old, friendly wooden wardrobe, a bit taller than a small child, rounded top edge, warm honey-brown wood with gentle wear, small decorative painted tiles on the top panel like the attached cabinet. Both doors are wide open toward the viewer. Inside: a warm small lamp glow, a soft cushion and a little rug on the lower shelf, a short row of toy-animal silhouettes on the upper shelf. Cozy and safe, not dark, not scary. Front view, slightly from above, whole wardrobe inside the frame with margin. Plain flat beige background, no floor shadow, no texture, no text, no people.

P2b (opcional, plano da mesa):
> Same style and same wardrobe. Close-up of the open lower shelf seen from the front: a warm-lit wooden shelf with a little round rug, used as a play table. Empty, ready for toys and cards. Plain flat beige background around it, no text, no people.

Regras: portas sempre abertas; ninguém dentro; nada que lembre esconderijo fechado.
