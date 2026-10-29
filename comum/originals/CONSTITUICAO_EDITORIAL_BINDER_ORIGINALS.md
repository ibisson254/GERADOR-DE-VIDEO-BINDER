# Constituição editorial e operacional · BINDER Originals

Versão 1.0 · 28/10/2026 · alterações registadas em `DECISOES.md` (mesma pasta).

Norma comum de **processo** para todas as séries do @binderthetrade. Não define personagens nem estética: isso vive no `CONTEXTO.md` de cada série. Não define o produto: só funções confirmadas (secção 9).

Princípio: **mesma disciplina, identidades diferentes.** Nenhuma série herda a voz, o humor, a duração, a estrutura de guião ou o visual de outra.

---

## 1. Hierarquia de fontes (quando duas regras chocam)

1. Instruções do projeto Binder Marketing (claude.ai) e pedido explícito do Ibisson na conversa.
2. Esta constituição (processo, rigor, entrega, registo).
3. `PERFIL.md` da série (adaptações operacionais da série).
4. `CONTEXTO.md` da série (identidade, voz, visual, fórmula). **Autoridade criativa**: o perfil e a constituição nunca a reescrevem.
5. Fichas de episódio e histórico.

Se uma regra criativa do `CONTEXTO.md` contradiz uma regra de entrega daqui (ex.: frase final da legenda), vale a regra de entrega e regista-se a divergência em `DECISOES.md`. Lacuna de identidade: assinalar, nunca inventar.

## 2. Séries e onde estão

| Série | Pasta | Identidade | Perfil |
|---|---|---|---|
| Meta em Curto (personagem TUBO; ex-Oráculo de Tubo) | `oraculo/` | `oraculo/CONTEXTO.md` | `oraculo/PERFIL.md` |
| Mana & Burn | `manaburn/` | Doc da série no Google Drive + skill `binder-mana-burn-episodio` + `manaburn/LEIA-ME.md` | `manaburn/PERFIL.md` |
| Conde de Manaforte · O Tribunal Estético | `conde/` | `conde/CONTEXTO.md` | `conde/PERFIL.md` |
| Recursos partilhados | `comum/` | — | — |

Série nova: copiar `modelos/PERFIL_SERIE.md` para `<pasta>/PERFIL.md`, criar `<pasta>/CONTEXTO.md`, acrescentar uma linha nesta tabela e em `DECISOES.md`. Esta constituição não muda.

## 3. Motor de orquestração (antes de cada produção)

**Etapa 1 · Classificar.** Série · classe de conteúdo · objetivo · complexidade (baixa / média / alta).
Classes de referência (lista aberta): leitura de carta, jogada de torneio, relatório de meta, notícia, tendência cultural, mercado/preço, comentário sobre arte, perfil de artista, contexto histórico, opinião, conteúdo promocional do app. Se a classe não pertence ao território da série (ver perfil), muda de série ou recusa a pauta.

**Etapa 2 · Escolher a estratégia** (só o que a peça precisa):

| Situação | Estratégia | Verificação mínima |
|---|---|---|
| Facto simples e bem documentado | Verificação rápida | 1 fonte primária |
| Afirmação controversa, recente ou complexa | Investigação aprofundada | 2 fontes independentes ou fonte primária + atribuição na fala |
| A história depende de uma sequência real (partida) | Reconstrução esquemática | VOD com minuto + texto Oracle de cada carta citada |
| Conclusão depende de números | Análise de dados | Fonte, data e amostra visíveis no ecrã |
| Objeto central é uma obra de arte | Análise estética | Observação separada de interpretação e de facto histórico |
| Recursos do kit já resolvem | Produção por reutilização | Conferir que o recurso é a versão atual |
| Não há material utilizável | Produção visual original | Nunca simular gravação, ecrã do app ou transmissão |

**Etapa 3 · Dividir funções.** Investigação → verificação → guião → arte → montagem → controlo de qualidade. Num só agente, em sequência. Agentes separados só com ganho real (ex.: revisão independente de factos numa peça de risco alto); nunca dois agentes a fazer o mesmo.

**Etapa 4 · Produzir** com o que existe de facto: confirmar ferramentas (ElevenLabs, Scryfall, ffmpeg, Playwright, rede) antes de planear em cima delas. Ver secção 7.

**Etapa 5 · Validar** com `CHECKLIST_QUALIDADE.md` + critérios do perfil, proporcional ao risco.

**Etapa 6 · Entregar** o ficheiro final quando há meios para o produzir; senão, o máximo produzível + o bloqueio concreto. Nunca um plano no lugar de um resultado possível.

As 12 perguntas da orquestração (série, objetivo, interesse, investigação, fontes, formato, recursos, ferramentas, riscos, verificação, indicadores, poupança de esforço) respondem-se na ficha do episódio (`modelos/FICHA_EPISODIO.md`). Peça simples = ficha curta.

## 4. Rigor factual

- Nunca inventar factos, números, citações, jogadas, eventos, fontes ou funções do app.
- Marcar o tipo de cada afirmação central: **facto** (fonte) · **inferência** · **opinião** (da personagem) · **previsão** · **incerteza**.
- Fonte primária quando existe: Oracle/Scryfall (texto e dados da carta), Wizards/Magic.gg (anúncios, resultados oficiais), EDHREC (Salt Score), MTGGoldfish/MTGTop8/Melee (meta). Fonte secundária é atribuída ("segundo o Draftsim").
- Datas: toda pauta que muda depressa leva a data da fonte. Preço só com fonte e data; valores são "estimativa, não oferta de compra". Não republicar dados de preço do Scryfall (termos de uso).
- Regra de carta nunca de memória: conferir no Oracle.
- Se a evidência não sustenta a tese, muda a tese, não a evidência.
- Fontes registadas em `<série>/episodios/` (ficha ou `*_fontes.txt`) com URL.

## 5. Qualidade editorial

- Uma proposta de valor por vídeo, dita numa frase na ficha.
- O gancho promete o que o vídeo entrega.
- Cada bloco avança a ideia; repetição = corte.
- Personalidade não substitui substância.
- Acidez para o meta, o hype, o preço e as escolhas visuais; nunca para pessoas reais.
- Fecho com função clara (pergunta, veredito, previsão) e uma única ação pedida.

## 6. Qualidade audiovisual

- 9:16, 1080×1920, 30 fps, **sem corte lateral** (regra com historial de reclamações: conferir quadros reais do vídeo final, não só a prévia).
- Carta real, inteira, rodapé visível, nada por cima.
- Texto legível no telemóvel; legenda dentro da zona segura.
- Voz, música, efeitos e legendas conferidos no ficheiro final; -14 LUFS (ou o alvo do perfil), pico < -1 dBFS.
- Todo vídeo termina com `comum/outro/outro_binder_916.mp4` (ver `comum/outro/LEIA-ME.md`). Nunca redesenhar a tela do app.
- Reutilizar recursos mestres (retratos, imagem-mestra, temas, fecho); não regenerar personagens.
- Nunca dizer que um vídeo foi inspecionado se não foi.

## 7. Ferramentas, direitos e transparência

- Política de Conteúdo de Fãs da Wizards: identificar como não oficial, creditar artista e Wizards.
- Vozes e músicas ElevenLabs: publicar só o que foi gerado com licença comercial ativa. Nada de imitar vozes reais.
- Nada de imagens de transmissões de torneio; reconstruir com imagens de cartas.
- Reconstrução nunca é apresentada como gravação.
- Nenhum segredo, token ou dado de testadores no repositório. Vídeos renderizados não são commitados (`.gitignore`).
- Ferramenta, fonte ou autorização indisponível: ver secção 11.

## 8. Eficiência

- Resultado final primeiro; perguntas só quando o erro sai caro.
- Reutilizar scripts do episódio anterior da mesma série (copiar e trocar parâmetros).
- Automatizar só o que se repete em vários episódios; nada de infraestrutura para um caso único.
- 1 chat = 1 entrega; avisar quando o chat ficar longo e deixar o resumo para continuar.

## 9. Relação com o BINDER Vision (comum a todas as séries)

- Objetivo do funil: levar colecionadores a experimentar a beta (Android). Views não são instalações.
- Funções que podem ser citadas (confirmadas em 19/10/2026, `claude/00-comece-aqui.md` do projeto): scanner (aponta a câmara, identifica a carta, escolhe a impressão), Binder com valor de referência (estimativa), decks, lista de desejos, Explorar e chat entre colecionadores. Qualquer outra função: confirmar com o Ibisson antes.
- Proibido: "grátis" (pendente de confirmação), "o melhor", "milhares de utilizadores", números de utilizadores.
- A prova do produto no vídeo é só o fecho real do scanner.

## 10. Entrega e registo (comum)

Entregáveis: vídeo · capa · legenda limpa · comentário fixado · ficha de fatos/fontes.

- **Legenda:** gancho; uma frase de facto que manda para o comentário; créditos ("Na tela/TV: carta (coleção, ano), nº n. Arte: artista. © Wizards of the Coast. Conteúdo de fã não oficial."); CTA em rotação; até 5 hashtags; sem emojis; **termina com "baixe o BINDER Vision"**. PT-BR, tratamento por "você".
- **Comentário fixado:** pergunta fácil na 1.ª linha + complemento (passos, texto Oracle, fonte, VOD) + **"Tem um detalhe escondido. Diga o segundo."**
- **Easter egg:** no máximo 1 por episódio, registado em `comum/easter_eggs.md`.
- **Commit no fim:** roteiro/ficha, legenda, fontes, histórico. Nunca vídeos.

## 11. Bloqueios (fonte, ferramenta ou autorização indisponível)

1. Produzir tudo o que não depende do bloqueio.
2. Sem imagem real da carta → só prévia com cartão "PRÉVIA", não publicável.
3. Sem fonte para uma afirmação → cortar a afirmação ou atribuí-la como opinião da personagem.
4. Sem voz licenciada → marcar a versão como não publicável.
5. Sem autorização (jogador, loja, autor de deck) → não usar nome nem material.
6. Dizer ao Ibisson numa linha o que falta e quem o desbloqueia.

## 12. Depois da publicação · aprendizagem

- Números do print semanal do Insights (Visão geral + Conteúdo) → `comum/historico.md`, com série e data.
- Separar **observado** de **leitura**; uma aprendizagem acionável por semana, no máximo.
- Um resultado isolado não muda a estratégia; uma regra nova precisa de padrão em 2+ semanas ou de decisão do Ibisson.
- Sem limiares universais de sucesso: cada perfil diz que métrica olha.
- Mudança na constituição ou num perfil → entrada em `DECISOES.md` (data, o quê, porquê, impacto).

## 13. O que o repositório guarda

Guarda: regras aprovadas, perfis, modelos, fichas e fontes de episódios, legendas, aprendizagens verificadas, scripts reutilizáveis.
Não guarda: transcrições de conversas, prompts temporários, resultados não verificados, mídia renderizada, segredos.
