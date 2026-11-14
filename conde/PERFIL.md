# Perfil operacional · Conde de Manaforte (O Tribunal Estético)

Herda `nucleo/CONSTITUICAO_EDITORIAL_BINDER_ORIGINALS.md`. Identidade, personalidade, fórmula, voz, música, visual e pipeline: `conde/CONTEXTO.md` (autoridade). Este perfil não altera nenhuma decisão criativa de lá.

Nome oficial: **Conde de Manaforte**. ("Conde de Terra Forte" apareceu num pedido de 28/10/2026; o repositório e todos os episódios usam Manaforte. Ver `nucleo/DECISOES.md`.)

- **Território:** ilustração de cartas de Magic: composição, luz, anatomia, perspectiva, simbolismo, técnica, bastidores de arte, artistas.
- **Fora do território:** jogadas e meta → Meta em Curto. Hype, preço, Salt Score → Mana & Burn. Memes e cultura pop brasileira na fala (rejeitado a 26/10/2026).
- **Público e necessidade:** colecionador e fã de arte que gosta de humor erudito sobre cartas que conhece.

## Classes e estratégia por defeito

| Classe | Estratégia | Prova mínima |
|---|---|---|
| Comentário sobre uma obra | Análise estética | Arte inteira (Scryfall); dados da carta no Scryfall |
| Bastidor da arte | Investigação | Fonte nomeada; fonte única fica atribuída na fala e no ecrã |
| Perfil de artista / contexto histórico | Investigação aprofundada | Fonte primária ou 2 independentes |

## Regras próprias de rigor (três camadas, sempre separadas)

1. **Observação:** o que está visível na arte (pode ser apontado com elipse/seta). Tem de ser verificável por quem pausa.
2. **Interpretação crítica:** a leitura do Conde; é opinião da personagem, dita como tal.
3. **Facto histórico ou de bastidor:** só com fonte; vai no comentário fixado com o link.

O alvo do humor é a arrogância do Conde, nunca o artista. Elogio e crítica sempre com razão.

## Gancho e fecho

Abertura "Meus caros apreciadores do duvidoso…" e veredito/carimbo conforme `CONTEXTO.md` §3; depois o fecho do scanner.

## Formato

Duração livre (constituição §6); referência histórica ~42–48 s. -14 LUFS, layout e paleta de `CONTEXTO.md` §6 (a paleta da série é própria; o verde BINDER só no fecho).

## Capa (modelo fixo desde 14/11/2026)

Todas as capas do Tribunal Estético, de episódios novos ou pedidas para episódios antigos, seguem este modelo (fundador, 14/11/2026 09:59; referência: capa do CM-EP005, Lêmure). Gerador: `conde/capas/capa_cm.py`. É a estratégia das capas do Mana & Burn e do Meta em Curto (um ponto focal, a personagem a reagir, faixa fixa, recorte 3:4) na linguagem do Conde.

- **Fundo:** papel marfim com grão (o do vídeo). Sem cartas desfocadas: o papel é a assinatura da série.
- **A obra (o réu):** `art_crop` do Scryfall, inteira, sem nada por cima, numa moldura dupla a tinta, como num museu. Arte de 2 faces: a face julgada.
- **Frase** (3–7 palavras, Lora SemiBold Italic, tinta): a acusação. Pode deixar a frase em suspenso para o foco a completar («Pediram um espírito. Veio um…»).
- **Foco:** o veredito numa palavra, gigante, em Lora Bold bordô dentro do carimbo gasto e inclinado (o carimbo do vídeo). É a palavra que a pessoa tem de ler na miniatura.
- **O Conde** no medalhão, à esquerda do carimbo, de perfil a olhar para o veredito, na expressão do episódio (desconfiado, indignado, admirado; neutro só se nada encaixar).
- **Faixa fixa** em baixo: «O TRIBUNAL ESTÉTICO · Nº 00X» a marfim; à direita, «réu de ANO» em itálico rosado.
- Máximo de 3 blocos de texto (frase, foco, faixa). Crédito da arte e «Conteúdo de fã não oficial» vão na legenda.
- Tudo dentro do recorte 3:4 da grelha (y 240–1680); conferir o `*_grelha.png` em tamanho pequeno antes de entregar. Capas já publicadas não se refazem (só se o fundador pedir).

Exemplo: `python3 conde/capas/capa_cm.py --scryfall ice/133 --frase "Pediram um espírito. Veio um…" --foco lêmure --expressao desconfiado --processo 5 --saida CM_EP005_CAPA.png`

## Ponte para o BINDER

Ligada à carta julgada (ex.: escanear a carta e guardá-la no Binder), só funções confirmadas.

## Métrica principal

Respostas à pergunta do comentário fixado (ex.: o próximo réu) + guardados.

## Critérios de aceitação próprios

- [ ] Arte inteira, nunca cortada nas laterais; crédito "Conteúdo de fã não oficial…" sob o palco.
- [ ] Observação, interpretação e facto distinguíveis.
- [ ] Bastidor com fonte atribuída.
- [ ] Sem memes nem cultura pop.
- [ ] Carta não repetida (lista "Não usar" em `CONTEXTO.md` §10).

## Divergências com a regra comum

`CONTEXTO.md` §8 manda terminar a legenda com "→ Baixe a beta para Android. Link na bio." e o comentário com "Pausou o vídeo? Repare em…". Prevalece a regra comum (constituição §10): legenda termina com "baixe o BINDER Vision"; comentário termina com "Tem um detalhe escondido. Diga o segundo." O resto de §8 mantém-se.
