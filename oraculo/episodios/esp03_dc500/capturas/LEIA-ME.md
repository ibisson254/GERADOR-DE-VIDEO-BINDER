# MC-ESP03 · capturas (Gate A resolvido a 19/11/2026, 16:45)

**Estado:** dados lidos diretamente do portal no navegador integrado do Claude, no PC do fundador; capturas `01_galeria_populares_2026-11-19.jpg` e `04_matchups_2026-11-19.jpg` guardadas aqui; números em `../fontes.md`. A lista abaixo fica como referência para episódios futuros.

O portal https://duelcommander500.com.br/ carrega os números por JavaScript. A 19/11/2026 (15:00–15:10, Lisboa) o ambiente do agente não conseguiu abrir o site pela rede (curl sem ligação; leitura web só devolve o esqueleto da página, sem números; extensão do Chrome indisponível). Sem estas capturas, nenhum número entra no episódio.

**Regra para todas as capturas:** ecrã inteiro do browser, com a barra de endereço visível (URL) e o relógio do sistema ou a data no nome do ficheiro. Mesmo período e mesmos filtros em todas. Se o portal tiver botão de exportar (CSV/JSON), a exportação substitui o print e guarda-se aqui tal como sai.

| # | Página | O que tem de aparecer no print | Nome do ficheiro |
|---|---|---|---|
| 1 | `/galeria`, ordenação «Mais Populares», sem filtro de cor nem arquétipo | Os 10–15 primeiros comandantes com o número de listas (ou aparições) de cada um; o texto que diz o período ou a data de atualização, se existir | `01_galeria_populares.png` |
| 2 | `/galeria`, ordenação «Maior Conversão», mesmos filtros | Os 10–15 primeiros com a conversão **e** o denominador (listas ou aparições) de cada um | `02_galeria_conversao.png` |
| 3 | Página de definição ou ajuda (tooltip, «sobre», rodapé) | O que o portal chama «conversão» (Top 4? Top 8? vitória do torneio?) e o que conta como «lista» | `03_definicoes.png` |
| 4 | `/matchups` | A matriz completa dos 20 comandantes, com a legenda (Vitória, Derrota, Win Rate, Popularidade) e o número de partidas por comandante ou por célula | `04_matchups.png` (+ `04b_…` se precisar de rolar) |
| 5 | `/matchups`, passar o rato numa célula e no total de um comandante | O denominador: quantas partidas sustentam o win rate | `05_matchups_tooltip.png` |
| 6 | Página do comandante A (mais jogado) | Listas, win rate/conversão, torneios em que aparece, período | `06_comandante_A.png` |
| 7 | Página do comandante B (candidato) | O mesmo que a 6, mais a lista de torneios (para ver se o resultado está concentrado num só) | `07_comandante_B.png` |
| 8 | Filtro de período (se existir): últimos 30/90 dias e «todo o período» | As mesmas leituras de 1 e 4 noutro período (teste de robustez 1) | `08_periodo_<x>.png` |
| 5b | `/matchups`, célula A×B | Vitórias, derrotas e empates de A contra B (para retirar os jogos comuns da conta da diferença) | `05b_celula_AxB.png` |
| 5c | Ajuda ou rodapé da matriz | Se o win rate conta partidas (match) ou jogos (game) e como trata empates | `05c_definicao_wr.png` |
| 9 | `/stores` ou lista de torneios | Número total de torneios e lojas no período (universo de eventos) | `09_universo.png` |

Depois das capturas: transcrever para `../dados/extracao.csv` (uma linha por comandante, vazio quando o portal não publica, nunca 0) e correr `python3 -I ../dados/calcular.py ../dados/extracao.csv`.

Alternativa mais rápida: o fundador abre este chat no computador com o Chrome e a extensão Claude in Chrome ligada, e o agente lê o portal diretamente (incluindo os pedidos de rede que o próprio portal faz), guardando tudo aqui.
