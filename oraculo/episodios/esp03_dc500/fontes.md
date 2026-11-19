# MC-ESP03 · fontes, tentativas de acesso e limitações

Fonte primária única: portal Duel Commander 500 do Farpas de Mana — https://duelcommander500.com.br/ (referência institucional: https://farpasdemana.com.br/duel-commander-500). Proibido: MTGDC500 / Lotus Games, ou qualquer outro site como substituto (`comum/parcerias.md`, decisão de 19/11/2026).

## O que está verificado (19/11/2026, 15:00–15:10 Lisboa)

| # | Afirmação | Tipo | Fonte (URL exato) | Data | Uso no episódio |
|---|---|---|---|---|---|
| V1 | O portal tem uma página «Matriz de Matchups» com a análise de performance entre os 20 comandantes com mais matchups registadas | facto (texto da página) | https://duelcommander500.com.br/matchups | 19/11/2026 | define o universo possível do indicador de vitórias |
| V2 | A legenda da matriz usa «Vitória», «Derrota», «Win Rate» e «Popularidade» | facto (rótulos da página) | https://duelcommander500.com.br/matchups | 19/11/2026 | o portal publica um indicador chamado win rate; definição e denominador ainda por ler |
| V3 | A galeria ordena por «Mais Populares», «Maior Conversão» e «Mais Recentes», com filtros de identidade de cor e arquétipo | facto (rótulos da página) | https://duelcommander500.com.br/galeria | 19/11/2026 | existem os dois eixos do episódio: popularidade e conversão |
| V4 | O portal tem mapa de lojas e torneios de DC500 no Brasil | facto | https://duelcommander500.com.br/stores | 19/11/2026 | universo de eventos (teste de robustez 4) |
| V5 | O Farpas tem um deckbuilder oficial do formato (Farpas Builder) | facto | https://builder.duelcommander500.com.br/ | 19/11/2026 | não entra no vídeo; confirma que o domínio é do Farpas |

Nenhum número de comandante foi lido: os valores são carregados por JavaScript e a leitura feita daqui só devolveu «Carregando Matchups...» e os rótulos.

## Tentativas de acesso (Gate A)

| Hora (Lisboa) | Via | Resultado |
|---|---|---|
| 15:03 | `curl` (shell) a `duelcommander500.com.br`, `www.` e `farpasdemana.com.br/duel-commander-500` | sem ligação (rede do ambiente só permite registos de pacotes) |
| 15:03 | leitura web direta das duas URLs do briefing | recusada (URL fora da lista permitida da sessão) |
| 15:04–15:06 | pesquisa web; leitura de `/matchups` e `/galeria` encontradas na pesquisa | páginas abertas, só esqueleto (V1–V3); números por JavaScript |
| 15:06 | Claude in Chrome (para ler a página renderizada e os pedidos de rede do próprio portal) | extensão não ligada (pedido feito do telemóvel) |

Não foram procurados nem usados endpoints de terceiros. A pesquisa devolveu páginas do MTGDC500 e artigos da LigaMagic com números de DC500: **não foram usados**, nem copiados para este repositório.

## Metodologia (19/11, corrigida às 16h)
- Popularidade: listas publicadas pelo portal; quota = listas do comandante / total de listas na extração (cálculo do BINDER). Lista ≠ jogador ≠ partida.
- Desempenho: win rate tal como o portal o publica, com o denominador (partidas) publicado. Top 4, se usado, é indicador separado e nunca se chama vitória.
- Diferença B − A: intervalo de Newcombe a 95 % (método 10), `dados/calcular.py`, verificado no exemplo de Newcombe (1998). Intervalos individuais de Wilson não são usados como prova de diferença (era o erro da prévia v1).
- Robustez: alertas por amostra (≥ 20 listas, ≥ 50 partidas), ≥ 3 torneios, ≤ 50 % das listas num só torneio; repetir a extração noutro período e comparar o código do veredito.

## Limitações já conhecidas (antes dos números)

- «Win Rate» do portal: falta a definição (partidas ou jogos? empates? só os 20 com mais matchups?) e o denominador por comandante.
- «Conversão» da galeria: falta saber se é Top 4, Top 8 ou título, e o denominador (listas ou aparições).
- O win rate só existe para os 20 comandantes com mais matchups: um comandante raro com resultado alto pode nem aparecer na matriz. A comparação «mais jogado × melhor» tem de ficar dentro do mesmo universo (os 20) ou usar a conversão da galeria — nunca misturar.
- Período e data de atualização: por confirmar no print.
- Independência: no win rate da matriz, um jogo A×B entra no registo de A e no de B; jogos do mesmo piloto repetem-se. O intervalo da diferença é aproximado; se o portal mostrar a célula A×B, retiram-se esses jogos e recalcula-se.

## Tabela final (preencher depois das capturas)

| Afirmação no vídeo | Indicador (definição do portal) | Valor | Denominador | Período | Filtros | URL | Extraído em | Captura | Limitação |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |
