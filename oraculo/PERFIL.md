# Perfil operacional · Meta em Curto (TUBO)

Herda `nucleo/CONSTITUICAO_EDITORIAL_BINDER_ORIGINALS.md`. Identidade, visual, trilha, estrutura do Reel e tipos de episódio: `oraculo/CONTEXTO.md` (autoridade). Pasta e scripts mantêm o nome antigo `oraculo/`; o nome público da série é **Meta em Curto**.

- **Território:** competição. Torneios mais recentes e mais falados da comunidade mundial; decks, metagame, matchups, mulligan, sideboard, sequenciamento, decisões de jogo.
- **Fora do território:** curiosidades, hype de sets, preço, Salt Score, cultura → Mana & Burn. Arte → Conde. Temas genéricos ou sem torneio por trás não entram.
- **Público e necessidade:** jogador competitivo e de Commander que quer perceber *porquê* um deck ou uma jogada funcionou, em 40 s.

## Classes e estratégia por defeito

| Classe (`CONTEXTO.md` §6) | Estratégia | Prova mínima |
|---|---|---|
| Leitura de Carta | Verificação rápida | Oracle + formatos legais |
| A Jogada que Não Viste | Reconstrução esquemática | VOD com minuto exato; estado da mesa (vida, mão conhecida, campo, mana) confirmado no VOD; alternativas avaliadas com o texto Oracle |
| Relatório do Meta | Análise de dados | Fonte, data, evento e tamanho da amostra no ecrã; distinguir **representação** (quantos jogaram), **desempenho** (conversão / win rate) e **confronto direto** |
| Previsão | Opinião registada | Marcada como opinião no ecrã; registada em `comum/historico.md`; revista depois do evento |

## Regras próprias de rigor

- "Dentro do tubo" só entram dados verificados; "fora do tubo" é personalidade e opinião.
- Comparar a jogada feita com 1–2 alternativas plausíveis, com o custo de cada uma; não afirmar que a alternativa "ganhava" sem o demonstrar.
- Uma partida não gera conclusão universal; uma amostra pequena é dita como pequena.
- Win rate só de fonte que o publica; nunca calculado sobre dados incompletos sem o dizer.
- Jogadores reais: nome e resultado sim; deboche não (`CONTEXTO.md` §7.2.3). "O TUBO julga o teu deck" só com autorização do autor.
- Contador `ERROS HUMANOS` = contagem real de episódios.

## Gancho e fecho

Gancho: frase seca com o dado ou a decisão surpreendente (fora do tubo, desconfiado). Fecho: pergunta competitiva + «Probabilidade calculada. Humanos, imprevisíveis.» + fecho do scanner.

## Formato

35–45 s **sem contar o fecho** do scanner (o EP01 teve 43,4 s + 3,9 s de fecho). Áudio alvo da trilha -16 LUFS (`CONTEXTO.md` §7.1); mix final -14 LUFS. Corte seco da trilha alinhado à revelação (não a um segundo fixo).

## Ponte para o BINDER

O "scan" da carta a entrar no tubo ecoa o scanner real do fecho. Nenhuma outra função.

## Métrica principal

Guardados + partilhas (conteúdo de referência). Secundária: respostas à pergunta competitiva. Hipótese inicial, a rever com 4+ episódios.

## Critérios de aceitação próprios

- [ ] Torneio, formato, data, jogadores e listas confirmados na fonte.
- [ ] Cada número no ecrã tem fonte e data visíveis.
- [ ] Representação, desempenho e confronto não estão misturados.
- [ ] Previsão marcada e registada (se houver).
- [ ] Nenhuma imagem de transmissão.
- [ ] Ficha e `*_fontes.txt` em `oraculo/episodios/`.

## Lacunas conhecidas

Ver `CONTEXTO.md` §12. Episódios: EP01 (AC13, Relatório do Meta) — `episodios/ep01_ac13_ficha.md`; EP02 (Spotlight Fracture, Leitura da Final) — `episodios/ep02_hartford_ficha.md`.

Evidência visual obrigatória (lista, carta, ficha de jogador sem foto): `CONTEXTO.md` §6.4.
