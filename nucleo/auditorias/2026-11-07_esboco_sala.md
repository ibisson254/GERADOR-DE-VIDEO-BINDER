# Esboço da sala do Mana & Burn · 07/11/2026 · APROVADO (08/11/2026) E APLICADO NO MOTOR

Feito numa cópia do kit (`manaburn/index.html` intocado), com os dados do Ep. 2. Carta na TV é marcador (o PNG do Stasis não está no repositório). Imagens e patch: `esboco_sala/`.

## O que o esboço mostra
1. **Mesa de noite de Commander:** os 4 retângulos castanhos dão lugar a 4 decks com sleeves (vermelho, azul, preto, verde), cartas em jogo genéricas (sem cartas reais), d20, dois dados e deckboxes. Copo e lata mantidos.
2. **Mesa sobe 96 px** (e +4% de escala): no plano geral a legenda tapava a mesa inteira; agora fica entre os pés da dupla e a legenda, e nos closes do Mana aparece inteira.
3. **Luz dentro do cenário (fase 2):** lâmpada quente, reflexo frio da TV na parede e na dupla (com máscara na tela), primeiro plano mais escuro. Substituiria o `luz.py` em renders novos (o `luz.py` fica para vídeos de outro motor).
4. **Piso de taco** numa faixa entre o rodapé e a borda do carpete.

## O que já existia no kit (não duplicado)
Ventilador de pé, antena com palha de aço, paninho de crochê, manta de crochê no sofá, benjamim na tomada.

## Refinamentos do agente
- O taco quase não aparece (o sofá e as caixas tapam-no) e a bíblia fala em carpete: proposta é **não** o adotar, ou deixá-lo só como detalhe discreto.
- Achado, sem alteração (personagem): no plano da TV o Burn aparece só como cabeça careca, sem boné nem ombros, atrás da TV. Mexer no modelo exige decisão do fundador.

## Decisão pedida
Aprovar 1, 2 e 3 (e 4 sim/não). Com aprovação: aplicar no `manaburn/index.html`, testar com `bordas.py` e com um episódio, registar em `nucleo/DECISOES.md`.
