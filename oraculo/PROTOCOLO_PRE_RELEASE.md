# Protocolo de Pré-Release · Meta em Curto (TUBO)

v1 · 06/11/2026 · decisão do fundador registada em `../nucleo/DECISOES.md` (06/11/2026).

Documento canónico da metodologia. Não é série, identidade nem estética novas: é a forma como o TUBO investiga, prevê, acompanha e audita uma coleção nova de Magic com pré-release. Hierarquia: constituição (§3 estratégia, §4 rigor, §11 bloqueios) → `CONTEXTO.md` (identidade, autoridade criativa) → `PERFIL.md` (quando ativar) → este protocolo (como executar). Se algo aqui chocar com uma regra superior, vale a regra superior e regista-se o conflito em `../nucleo/DECISOES.md`.

Ficheiros:
- Modelo: `../nucleo/modelos/PREVISOES_PRE_RELEASE.md` → cópia por coleção em `pre-release/<CÓDIGO>_previsoes.md` (código Scryfall da coleção, em maiúsculas).
- Registo e estados: `../comum/historico.md`, secção «Previsões registadas do TUBO». Não há outro histórico.

## 0. Ativação

Regra de ativação e exclusões: `PERFIL.md`, «Protocolo de Pré-Release». Em resumo: pedido de previsões ou de preparação para o pré-release/Sealed de uma coleção nova ativa as quatro fases; episódios comuns de Meta em Curto não o ativam.

## 1. Fase A · Investigação

Antes de qualquer previsão, cobrir e registar na ficha (secção A), com fonte e data:

1. Lista completa de cartas da coleção.
2. Texto Oracle e interações relevantes (incluindo as notas de regras oficiais da coleção, quando publicadas).
3. Mecânicas novas e antigas.
4. Cores e pares de cores (os arquétipos sinalizados pela coleção).
5. Curva de mana e distribuição de custos.
6. Remoções, evasão, criaturas e fixing (contagens por raridade).
7. Sinergias entre comuns e incomuns.
8. Potencial de raras e míticas, com a probabilidade de as abrir só a partir da colação oficial publicada (senão, não se diz).
9. Arquétipos possíveis para Limited.
10. Discussões relevantes nas comunidades.
11. Análises de jogadores experientes em Limited (atribuídas pelo nome da fonte).
12. Resultados de eventos e dados disponíveis, quando existirem (antes do pré-release, normalmente não existem: dizê-lo).

Prioridade de fontes: oficial (Wizards/magic.gg: anúncio, artigo de colação, guia de pré-release, notas de regras) e Oracle/Scryfall → bases de dados com amostra conhecida (ex.: 17Lands, Untapped.gg), sempre com o formato filtrado → análises de Limited publicadas → discussão comunitária.

Não confundir: hype com desempenho · opinião com evidência · popularidade com eficiência · raridade com poder competitivo · dados de outro formato com resultados de Sealed.

Fonte inacessível na sessão (aconteceu com o 17Lands no EP05): constituição §11. Regista-se o bloqueio na ficha e o que o desbloqueia; nada se estima no lugar dela.

## 2. Fase B · Previsões

Cada previsão é uma linha completa na ficha (secção B) e uma linha no histórico, com:

| Campo | Regra |
|---|---|
| ID | `PR-<CÓDIGO>-NN`, sequencial por coleção, nunca reutilizado |
| Coleção · data de elaboração | data em que a previsão é fechada |
| Hipótese | uma frase verificável |
| Evidências · fontes | só da Fase A, com o tipo (facto, cálculo, modelo, opinião atribuída) |
| Grau de certeza | escala da secção 5; nunca em percentagem |
| Riscos | o que a pode invalidar (amostra, viés da fonte, diferença de formato) |
| Condições de validade | formato, população e período a que se aplica |
| Critério de avaliação | o que conta como confirmação, confirmação parcial e refutação; fonte, recorte e prazo da auditoria. Definido **antes**, nunca depois |
| Publicação | pública (dita no vídeo) ou só registo |

Investigar em especial:
- **Arquétipos:** pares de cores fortes; estratégias agressivas, midrange e de controlo; sinergias que podem definir o formato.
- **Cartas:** comuns acima da raridade; incomuns que sustentam arquétipos; raras que decidem partidas; cartas aparentemente fortes que podem decepcionar.
- **Mecânicas:** maior impacto; dependência de outras cartas; consistência de execução; armadilhas.
- **Construção:** curva, número de criaturas, remoções, fixing, distribuição de cores, equilíbrio entre sinergia e qualidade individual.

Uma previsão sem critério de avaliação não é previsão: é opinião, e não entra no histórico.

## 3. Fase C · Acompanhamento

Durante o pré-release, cada evidência nova entra na ficha (secção C) com data, fonte e um destes tipos:

| Tipo | O que é | Pode mudar o estado? |
|---|---|---|
| R · Relato individual | um jogador, uma mesa, um post | Não |
| O · Opinião comunitária | consenso de fórum ou de criadores | Não |
| D · Resultado documentado | resultado publicado de um evento identificado | Só se o critério o previr |
| E · Estatística com amostra | dados com fonte, n, formato e período | Sim, nos termos do critério |

- O texto original da previsão (secção B) **nunca se edita** depois da data de elaboração.
- Revisão = linha nova na tabela de revisões (ficha e histórico): data, ID, o que muda, motivo, nova evidência. A auditoria compara sempre a previsão original; a revista avalia-se à parte e marcada como revisão.
- Relatos isolados não viram estatística.

## 4. Fase D · Auditoria

No prazo do critério (ou quando os dados chegarem):

1. Recuperar a previsão original (ficha, secção B).
2. Comparar com os dados disponíveis do formato certo.
3. Atribuir o estado (secção 6) e atualizar a linha no histórico; nunca apagar a linha.
4. Avaliar a qualidade das evidências usadas na Fase A.
5. Identificar vieses (hype, raridade, dados de Draft lidos como Sealed, fonte única).
6. Registar 1–3 lições na ficha (secção D) e a principal na lista de lições do histórico.

Sem dados suficientes: INCONCLUSIVA, com o motivo. Nunca inventar resultados.

Previsão pública refutada = «Erro de sistema» num episódio seguinte (`CONTEXTO.md` §7.2, item 4). O contador `ERROS HUMANOS` continua a ser contagem real de episódios (§7.2, item 2): o protocolo não lhe atribui valor.

## 5. Integridade estatística

- Percentagens, win rates, probabilidades de vitória, taxas de sucesso de arquétipos, taxas de utilização e rankings estatísticos só com dados e metodologia que os sustentem. Cada número leva **fonte, tamanho da amostra, formato, período e limitações** (na ficha; no ecrã, a linha de fontes da constituição §3).
- Cálculo próprio (hipergeométrica, simulação) é «cálculo» ou «modelo», com premissas escritas; nunca é apresentado como resultado de jogo.
- Draft, Sealed, Construído e outros formatos não se misturam sem justificar a comparação na ficha.
- Sem dados suficientes: avaliação qualitativa.
- **Grau de certeza** (medidor «GRAU DE CERTEZA» de 5 segmentos, `CONTEXTO.md` §11) é juízo editorial, nunca probabilidade estatística, e não leva percentagem:

| Seg. | Grau | Quando |
|---|---|---|
| 1 | Muito baixo | só leitura de cartas ou uma opinião |
| 2 | Baixo | Oracle + uma análise externa, ou modelo próprio com premissas fortes |
| 3 | Médio | duas ou mais fontes independentes convergem (análises, contagens, modelo) |
| 4 | Alto | dados de jogo do mesmo formato com amostra conhecida, ainda curta |
| 5 | Muito alto | dados do mesmo formato com amostra grande e estável |

Antes do pré-release não há dados de Sealed da coleção: o teto é 3. «Probabilidade calculada. Humanos, imprevisíveis.» é o bordão de fecho da série, não uma estatística.

## 6. Estados

| Estado | Quando |
|---|---|
| PENDENTE | prazo por chegar ou dados ainda não publicados |
| CONFIRMADA | critério de confirmação cumprido |
| PARCIALMENTE CONFIRMADA | cumprida só a parte prevista como parcial no critério |
| REFUTADA | critério de refutação cumprido |
| INCONCLUSIVA | prazo vencido sem dados suficientes, fonte indisponível ou critério não mensurável |

## 7. No vídeo (identidade intacta)

Quando uma previsão vira episódio, segue a estrutura, a voz, a trilha, o visual e o fecho de `CONTEXTO.md` sem alterações:
- **Fora do tubo:** a hipótese, marcada como previsão, com o medidor GRAU DE CERTEZA.
- **Dentro do tubo:** só evidência verificada da Fase A (Oracle, contagens, fontes atribuídas, cálculos com premissa).
- Evidência visual (`CONTEXTO.md` §6.4): carta citada = imagem oficial.
- O ID pode ir no comentário fixado, para o público acompanhar a auditoria.
