# Perfil operacional · Meta em Curto (TUBO)

Herda `nucleo/CONSTITUICAO_EDITORIAL_BINDER_ORIGINALS.md`. Identidade, visual, trilha, estrutura do Reel e tipos de episódio: `oraculo/CONTEXTO.md` (autoridade). Pasta e scripts mantêm o nome antigo `oraculo/`; o nome público da série é **Meta em Curto**.

- **Território:** competição. Torneios mais recentes e mais falados da comunidade mundial; decks, metagame, matchups, mulligan, sideboard, sequenciamento, decisões de jogo.
- **Previsões de pré-release** de uma coleção nova (Limited/Sealed) entram no território pelo Protocolo de Pré-Release (secção abaixo; fundador, 06/11/2026).
- **Fora do território:** curiosidades, hype de sets, preço, Salt Score, cultura → Mana & Burn. Arte → Conde. Temas genéricos ou sem torneio por trás não entram.
- **Público e necessidade:** jogador competitivo e de Commander que quer perceber *porquê* um deck ou uma jogada funcionou, em 40 s.

## Classes e estratégia por defeito

| Classe (`CONTEXTO.md` §6) | Estratégia | Prova mínima |
|---|---|---|
| Leitura de Carta | Verificação rápida | Oracle + formatos legais |
| A Jogada que Não Viste | Reconstrução esquemática | VOD com minuto exato; estado da mesa (vida, mão conhecida, campo, mana) confirmado no VOD; alternativas avaliadas com o texto Oracle |
| Relatório do Meta | Análise de dados | Fonte, data, evento e tamanho da amostra no ecrã; distinguir **representação** (quantos jogaram), **desempenho** (conversão / win rate) e **confronto direto** |
| Previsão | Opinião registada | Marcada como opinião no ecrã; registada em `previsoes/registo.yaml` antes da voz (`CICLO_SEMANAL.md` §0); revista depois do evento |
| Previsão de pré-release | Protocolo de Pré-Release | Fases A–D de `PROTOCOLO_PRE_RELEASE.md`; ficha em `pre-release/`; ID e estado em `previsoes/registo.yaml` |

## Regras próprias de rigor

- "Dentro do tubo" só entram dados verificados; "fora do tubo" é personalidade e opinião.
- Comparar a jogada feita com 1–2 alternativas plausíveis, com o custo de cada uma; não afirmar que a alternativa "ganhava" sem o demonstrar.
- Uma partida não gera conclusão universal; uma amostra pequena é dita como pequena.
- Win rate só de fonte que o publica; nunca calculado sobre dados incompletos sem o dizer.
- Jogadores reais: nome e resultado sim; deboche não (`CONTEXTO.md` §7.2.3). "O TUBO julga o teu deck" só com autorização do autor.
- Contador `ERROS HUMANOS` = contagem real de episódios.

## Protocolo de Pré-Release (ativação)
Método completo: `PROTOCOLO_PRE_RELEASE.md`. Não muda nada da identidade (`CONTEXTO.md`).
- **Ativa** quando o pedido envolve: previsões de pré-release; análise de uma coleção antes do pré-release; preparação competitiva para Sealed; expectativas sobre arquétipos de uma coleção nova. Ativa as quatro fases, não só a previsão.
- **Coleção já lançada:** identificar primeiro o que se pede. Análise de resultados com previsões registadas → Fase D. Sem previsões registadas → Relatório do Meta normal. Previsão retrospectiva («o que se devia ter previsto») → marcada como retrospectiva e nunca registada como previsão (não é auditável).
- **Não ativa** em episódios comuns (torneio, jogada, leitura de carta, meta de Construído), nem para hype ou reação a spoilers (Mana & Burn).
## Ciclo semanal (09/11/2026)
Quinta prevê, segunda presta contas: `CICLO_SEMANAL.md`. Toda previsão vai para `previsoes/registo.yaml` antes de gravar a voz; o briefing sai de `python3 -I oraculo/previsoes/ciclo.py segunda|quinta`.


## Gancho e fecho

Gancho: abertura padrão de `CONTEXTO.md` §7 (desde 16/11/2026): grelha 2×2 do MC-ESP01 com cartas ou deck reais no quadro 0, revelação até 3 s, mergulho no terminal, dados e fonte legíveis, sonoplastia do TUBO, mudança visual ≤ 3 s e pagamento antes do fecho; os 7 campos vão para a ficha (`nucleo/SHOWRUNNER.md` §4.1). A frase seca «fora do tubo, desconfiado» passou para depois da revelação. Fecho: pergunta competitiva + «Probabilidade calculada. Humanos, imprevisíveis.» + fecho do scanner.

## Formato

Duração: 25–35 s sem o fecho, pela regra de 16/11/2026 (`CONTEXTO.md` §7), que prevalece sobre a duração livre da constituição §6 nesta série. Referência histórica: EP01 43,4 s, EP02 45,0 s. Áudio alvo da trilha -16 LUFS (`CONTEXTO.md` §7.1); mix final -14 LUFS. Corte seco da trilha alinhado à revelação (não a um segundo fixo).

## Ponte para o BINDER

O "scan" da carta a entrar no tubo ecoa o scanner real do fecho. Nenhuma outra função.

## Métrica principal

Guardados + partilhas (conteúdo de referência). Secundária: respostas à pergunta competitiva. Hipótese inicial, a rever com 4+ episódios.

## Critérios de aceitação próprios

- [ ] Torneio, formato, data, jogadores e listas confirmados na fonte.
- [ ] Cada número no ecrã tem fonte e data visíveis.
- [ ] Representação, desempenho e confronto não estão misturados.
- [ ] Previsão marcada e registada em `previsoes/registo.yaml` (se houver).
- [ ] Pré-release: ficha `pre-release/<CÓDIGO>_previsoes.md` com critério de avaliação em cada ID; linhas no histórico; nenhuma percentagem sem fonte, amostra, formato e período; grau de certeza sem %.
- [ ] Nenhuma imagem de transmissão.
- [ ] Ficha e `*_fontes.txt` em `oraculo/episodios/`.

## Lacunas conhecidas

Ver `CONTEXTO.md` §12. Episódios: EP01 (AC13, Relatório do Meta) — `episodios/ep01_ac13_ficha.md`; EP02 (Spotlight Fracture, Leitura da Final) — `episodios/ep02_hartford_ficha.md`; EP03 (Arquivo Competitivo, boletim do fim de semana) — `episodios/ep03_arquivo_ficha.md`.

Evidência visual obrigatória (lista, carta, ficha de jogador sem foto): `CONTEXTO.md` §6.4.

## Lições do MC-ESP03 (19/11/2026) — obrigatórias antes de produzir

O MC-ESP03 custou 460 créditos de voz, três prévias técnicas e um refazer completo da montagem. Para não repetir:

1. **Dados antes de tudo.** Abrir a fonte no início da sessão (se o site carrega por JavaScript, usar o navegador integrado do Claude no PC do fundador). Sem números verificados não se renderiza nada: nada de prévias técnicas com marcadores.
2. **Método estatístico certo à primeira.** Diferença entre dois comandantes = intervalo de Newcombe da diferença (`oraculo/episodios/esp03_dc500/dados/calcular.py`), nunca dois intervalos individuais. Confirmar a definição do indicador do site com os números publicados antes de escrever.
3. **A fonte entra na voz e no ecrã desde o 0 s.** Primeira fala = de onde vêm os dados («No portal X, do Y:»); selo de fonte em todos os planos com números. Uso de capturas ou logótipo de terceiros decide-se no briefing, não depois do render.
4. **Voz numa só geração, já do tamanho certo.** Antonio de Jesus com atempo 1,10 ≈ 11,8 caracteres por segundo com as pausas: 35 s ≈ 390 caracteres no máximo, abertura incluída. Escrever os números que a voz pode ler mal por extenso. Correr `estimate_only` e mostrar texto final + custo ao fundador numa só pergunta. Nada de frases soltas depois.
5. **Voz a partir do 0 s.** O gancho visual corre por baixo da primeira fala; não deixar o vídeo começar mudo.
6. **Trilha cobre o fecho.** O fecho do scanner não tem áudio: a trilha continua por baixo dele e só desvanece no fim (`esp03_render.py`, `audio_previa`).
7. **Hierarquia visual padrão para episódios de dados** (referência do fundador, 19/11; ordem v4: cartas no quadro 0 → TUBO a falar → carta entra no ecrã do TUBO e mergulho → dados sobre chuva estilo Matrix): legenda grande no topo sincronizada com a voz, carta grande e inteira ao centro, número em caixa por baixo, troca de carta em rotação 3D, prova (captura) quando a voz cita o número. Desde 19/11/2026 é o padrão da série: `oraculo/CONTEXTO.md` §7.4 e o motor `oraculo/motor/` (`mc_render.py`, `mc_voz.py`, `LEIA-ME.md`).
8. **Conferir em fotogramas, renderizar uma vez.** Folha de contacto com 10–15 fotogramas → corrigir → um render final → QC. Cada render completo custa ~1 min; cada prévia descartada custa uma volta de revisão do fundador.
