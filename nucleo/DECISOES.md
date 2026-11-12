# Registo de decisões · BINDER Originals

Uma entrada por alteração de regra: data · o quê · porquê · impacto. Mais recente no topo.

## 12/11/2026 (12:27) · Carrosséis de artistas v4: gerados por IA no estilo das referências (teste John Avon)

**O quê:** «Não quero perto quero igual». O fundador autorizou gastar créditos ElevenLabs só para testar o carrossel do John Avon (5 slides). Gerados com gpt-image-2 usando a capa dele como referência de estilo; texto conferido; slide 5 com o cartaz BINDER real colado por código. Custo: 6.490 créditos. As pinturas são ilustrações de IA, não obras do artista: a legenda e uma etiqueta discreta nos slides dizem-no.
**Impacto:** os outros 5 artistas só avançam com a aprovação do teste. Prompts e nós em `lambe-lambe/carrosseis_artistas/ia/PROMPTS_AVON.md`.

## 12/11/2026 (12:18) · Carrosséis de artistas v3: identidade igual às referências

**O quê:** v2 reprovada («Refine mais tem que fica identidade igual a do ficheiro que enviei»). v3: arte de ponta a ponta no cartaz principal, relevo de tinta e papel amassado, letras gastas, fitas, Rubik itálico amarelo nas faixas. Mantêm-se: sem retrato, sem símbolo de Magic, arte real com a carta inteira no carrossel.
**Impacto:** `gerador/` passa à v3; v2 em `v2_reprovada/`.

## 12/11/2026 (12:04) · Carrosséis de artistas refeitos no layout das referências

**O quê:** a v1 (ilustração vetorial plana) foi reprovada: «Tem que ser todos nesse padrão do ficheiro que lhe enviei refaça». A v2 segue o layout das duas referências. Imagem grande = detalhe ampliado da arte real da carta (opção escolhida pelo fundador, entre arte real, geração no ElevenLabs ou geração no ChatGPT). Mantém-se sem retrato do artista e sem o símbolo de Magic no selo.
**Impacto:** `lambe-lambe/carrosseis_artistas/gerador/` passa à v2; a v1 fica em `v1_reprovada/`.

## 12/11/2026 (11:43) · Padrão visual oficial dos carrosséis do Lambe-lambe

**O quê:** o fundador aprovou como padrão permanente dos carrosséis do Lambe-lambe a estética das duas referências que enviou (muro rosa, cartazes rasgados, tipografia grande, unidade entre slides). Regras em `lambe-lambe/CONTEXTO.md` §2 («Padrão oficial de carrossel»). Pedido: «Terminei esses carrocel e faça mais uns 5 com artistas mais conhecidos do Magic».
**Porquê:** reconhecimento imediato da série no feed.
**Impacto:** carrosséis LL-ART13 (John Avon) a LL-ART18 produzidos em `lambe-lambe/carrosseis_artistas/`. As referências não se publicam como estão: tinham factos errados e um rosto gerado do artista; o padrão exclui fotos e rostos gerados de pessoas reais e usa ilustração original + cartas reais.

## 12/11/2026 (05:54) · Todos os episódios fechados, menos o TUBO de segunda; Vince Vault aprovada

**O quê:** (1) Entram na `main`, fechados (CONCLUÍDO; PUBLICADO onde o índice de 08/11 já o confirmava): MC-EP03, MC-EP04, MC-EP05 (+carrossel), MC-EP07, MB-ESP03, MB-EP10 («A febre do autógrafo», branch `ep10-cartas-especiais`, conforme o índice semanal confirmado pelo fundador a 08/11 — as branches `ep10-97-terrenos`, `ep10-numot` e `ep10-olag` ficam como rascunhos não integrados), MB-GIRO02, CM-EP004 (registo), CM-EP005, LL-PRETRK, LL-SHEOL, LL-DIVCAR e LL-CAMPBR. (2) **MC-EP06 («Prestação de contas: placar zero», o episódio de segunda) fica ABERTO**: escrito, não produzido; a prestação de contas é segunda, 16/11. (3) **Vince Vault aprovada como frente** (pasta `vince/`, branch `vince-vault`/PR #11; a `proposta/vince-vault` de 07/11 fica como proposta substituída); secção no catálogo. Pequeno Mestre (PR #2) e Vinci (PR #17) continuam em desenvolvimento, sem aprovação.
**Porquê:** fundador, 12/11/2026 (05:54): «Todos episódios dê como fechados menos o tubo de segunda. Vince vault».
**Impacto:** registo editorial atualizado (86 conteúdos); nenhum conteúdo publicado reaberto; `PUBLICADO` só onde havia confirmação (índice de 08/11); o resto fica `CONCLUÍDO` com publicação por confirmar.

## 12/11/2026 · Missão Master: merge da consolidação e integração do protocolo de pré-release
**O quê:** (1) A branch `consolidacao/2026-11-12-missao-master` entra na `main` (PR #18): matriz de integração, sistema de previsões do TUBO (de `meta-em-curto/ep07-wc32`, PR #16) com `ciclo.py continuacao` corrigido (mostra TODAS as previsões abertas em qualquer dia, não só a janela semanal) e 15 testes, `comum/ferramentas/validar_repo.py`, motor do Giro nº 1 arquivado de `giro/2026-11-01`, STATUS ao estado real. (2) A branch `protocolo-pre-release-tubo` (PR #9, decisão de 06/11 abaixo) entra reconciliada: a secção de previsões de `comum/historico.md` passa a remissão para `oraculo/previsoes/registo.yaml` (fonte canónica única, decisão de 09/11 abaixo); as entradas de 06/11, 09/11 e 10/11 entram neste registo de decisões. (3) A branch `feature/memoria-editorial-insights` (PR #3, decisão de 01/11 abaixo) entra reconciliada: constituição v1.6, registo editorial, encerramento obrigatório (`SHOWRUNNER.md` §6) e `comum/insights/`; o registo editorial fica marcado como desatualizado desde 01/11. (4) PR #7 passa a ter base `main` (a base anterior já foi integrada).
**Porquê:** fundador, 12/11/2026 (01:32): «Escolha as melhores opções e pode prosseguir», em resposta à secção F de `nucleo/auditorias/2026-11-12_missao_master.md`.
**Fica de fora (decisão própria do fundador):** qual das 4 branches é o Ep. 10 do Mana & Burn; frentes novas (Pequeno Mestre, Vince Vault, Vinci); merge dos pacotes de conteúdo (EP03–EP07, Giro nº 2, Conde EP005, especiais, lambes).

## 10/11/2026 · Meta em Curto EP07: fotos dos brasileiros e listas no ecrã
**O quê:** o fundador autorizou fotos reais dos 6 brasileiros convidados ao WC32 nas fichas do EP07 e assumiu a responsabilidade pelos direitos (registo em `oraculo/autorizacoes/2026-11-10_ep07_fotos_brasileiros.md`). Exceção só deste episódio; a regra geral do CONTEXTO §6.4 mantém-se (foto do campeão por defeito; restantes jogadores com silhueta). Pediu também as listas dos decks citados: entram a lista agregada de Mono-Green Landfall (Karsten, magic.gg) e as duas listas campeãs de Jund Sacrifice (Hartford e Pequim), com pausas de voz novas em vez de voz regenerada.
**Porquê:** pedido do fundador (10/11, 17:06): «Coloque as fotos dos jogadores brasileiros, eu assumo a responsabilidade e coloque algumas listas de cartas que você citou no episódio». Os ficheiros das fotos têm de vir do fundador: os agentes não descarregam fotos de pessoas da web.

## 10/11/2026 · Toda previsão do TUBO conta no registo, em qualquer dia

**O quê:** (1) `oraculo/CICLO_SEMANAL.md` §0: qualquer previsão do TUBO, em qualquer peça e dia, entra em `oraculo/previsoes/registo.yaml` antes da voz; qualquer produção do TUBO começa por ler o registo. (2) `ciclo.py continuacao` (igual a `segunda`, para qualquer dia). (3) Linha no `AGENTS.md` §2. (4) Recorte das PR-TRK-01 e 03 no 17Lands fixado antes de haver dados (linhas de guilda sem splash; «Two-color» contra três ou mais cores).
**Porquê:** pedido do fundador (10/11/2026, 09:54), ao enviar o EP05: «sempre que der uma previsão tem que contar nos históricos de previsão do personagem no Github para quando o personagem for fazer episódio já saber qual é que ele tem que produzir sem eu ter que falar toda vez».
**Impacto:** só vale em sessões novas depois de a branch `meta-em-curto/ep06-ciclo-semanal` entrar na `main` (as sessões clonam a `main`). Identidade do TUBO sem alterações.

## 09/11/2026 · Ciclo semanal do TUBO: quinta prevê, segunda presta contas

**O quê:** (1) Novo `oraculo/CICLO_SEMANAL.md`: o episódio de quinta fecha previsões sobre o fim de semana; o de segunda volta a elas com dado. (2) Registo único e legível por máquina em `oraculo/previsoes/registo.yaml` (texto original, critério, prazo, conferências, estado) e calendário em `oraculo/previsoes/calendario.yaml`. (3) `oraculo/previsoes/ciclo.py` gera o briefing (`segunda`, `quinta`) e valida o registo (`validar`). (4) Palavras `tubo segunda` / `tubo quinta` no `AGENTS.md`. (5) `comum/historico.md` deixa de repetir a tabela de previsões e aponta para o registo. (6) PR-TRK-01..04 do EP05 transcritas para o registo, com a conversão prevista a 06/11 (grau 2; sem o «~35%»).
**Porquê:** pedido do fundador (09/11/2026, 01:20): «tem que se tornar padrão salvar as previsões para assim que eu pedir o episódio de segunda tem que ser automático. Ele tem que buscar as previsões feita na quinta, e quando eu pedir episódio da quinta ele já tem que saber o que pesquisar.»
**Decisões técnicas:** o registo fica em YAML porque a segunda tem de o ler sem interpretação; o histórico humano remete para ele, para não haver duas tabelas. A shell não chega ao 17Lands, magic.gg nem MTGMeta: o script não pesquisa, diz o quê e onde; o agente usa as ferramentas web. Previsões de prazo longo levam conferências marcadas às segundas (placar parcial, nunca auditoria).
**Impacto:** identidade, voz, trilha e estrutura do TUBO não mudam. A `main` ainda não tem o `PROTOCOLO_PRE_RELEASE.md` (branch `protocolo-pre-release-tubo`) nem o EP05 (branch `meta-em-curto-ep05`); o ciclo remete para eles e funciona sem eles, mas a integração dessas branches fica por aprovar.

## 08/11/2026 · Vince Vault: boletim semanal e fonte de preços

**O quê:** o formato proposto para o Vince passa a ser um boletim semanal (altas, baixas e oportunidades em cartas acessíveis, com vocabulário da bolsa). Preços sem Cardmarket. Fonte preferida: a plataforma BINDER; como a base ainda não guarda histórico de preços (F1 do Data Intelligence Master v1.2) e o valor de referência da app vem do Scryfall (termos proíbem republicar preços), a variação semanal vem de uma fonte que a publica, atribuída e datada no ecrã (piloto: MTGStocks, preços do TCGplayer). O BINDER Vision entra como chamada para ação (scanner + valor de referência).
**Porquê:** pedido do fundador (08/11/2026).
**Impacto:** quando a F1 existir, o boletim passa a usar os dados do BINDER. Sem previsões nem recomendação de compra; "Buy the dip!" é sempre desmentido em cena.

## 08/11/2026 (02:06) · Calendário da parede configurável (Mana & Burn)
**O quê:** o ano do calendário velho da sala passa a vir de `EP.calendario` (por defeito "2019"). O Giro de 08/11 usa "1996".
**Porquê:** fundador, 08/11/2026: "mude o calendário na parede para 1996".
**Impacto:** só o Giro de 08/11 muda; os outros episódios e a sala v3 ficam iguais. Se o fundador quiser 1996 em todos, basta mudar o valor por defeito no `index.html`.

## 12/11/2026 · Frente nova em desenvolvimento: Vinci (o mercado das cartas)

**O quê:** pasta `vinci/` (palavras de arranque `vinci`, `mercado`, `preco`): série sobre preço de cartas, com causa, fonte e data. Inclui `CONTEXTO.md` (bíblia), `PERFIL.md` e `audio/` com o sintetizador da voz da Fonte. Entradas novas no catálogo, em `series.yaml` e no `AGENTS.md`.
**Porquê:** pedido do fundador (11–12/11/2026). O plano original era uma personagem 3D, descartada por custo: em 3D o custo não baixa com o tempo, e nesta série o que muda a cada episódio é o número, a carta e a causa — texto e uma imagem do Scryfall. Decidiu-se character design 2D desenhado uma vez e composto em camadas, com o método de planos parados cortados a cada 3–6 s.
**Impacto:** nenhuma série existente muda; preço continua a poder ser remate cómico em Mana & Burn e notícia no Giro. Três regras novas próprias desta frente: nunca prever preço nem recomendar compra ou venda; todo o número com fonte e data no ecrã; a Fonte (personagem do telefone) nunca aparece, nunca fala palavras e nunca é legendada, e quando não há fonte verificada não atende. O som da Fonte é sintetizado localmente, sem créditos de serviços externos.

*Reconciliação (12/11/2026, mesma madrugada):* o PR #17 declara que esta é a mesma frente do Vince Vault («por engano foi criada uma segunda frente»; frente única Multiverse Capital, apresentada pelo Vince Vault). Reconciliado: pasta única `vince/` (bíblia 2D `vince/CONTEXTO.md` substitui `BIBLIA_PERSONAGEM.md`, que fica como arquivo com o resto do material 3D), voz antiga mantida (`L93SDe6kGQj79D6svMgA`). O kit 2D, `recortar.py`, `EDICAO.md` e `PROMPT_EPISODIO.md` descritos no corpo do PR #17 **não chegaram à branch** — ausência registada, nada foi inventado. Fontes de preço seguem a decisão de 08/11 (sem Cardmarket; piloto MTGStocks/TCGplayer): o corpo do PR #17 mencionava Cardmarket — **a confirmar pelo fundador qual das duas vale**.

## 08/11/2026 (00:05) · Burn no plano da TV

**O quê:** correção de um defeito de render, não de modelo: no plano da TV os padrões SVG (cabelo raspado do Burn, xadrez da camisa, papel de parede) saíam transparentes porque os ids repetidos apontavam para o mundo escondido. O plano da TV passa a ter defs próprios (sufixo `_2`). O Burn sobe 40 px atrás da TV e mostra pescoço e ombros com a mesma camisa do plano geral, ligando-se ao braço que aponta.
**Porquê:** fundador, 08/11/2026: "Pode corrigir de forma eficaz e eficiente que faça sentido para o projeto."
**Impacto:** nos episódios novos, o Burn do plano da TV fica igual ao do plano geral, e a parede desse plano volta a ter o papel listrado. `bordas.py` OK.

## 08/11/2026 (00:03) · Sala v3 do Mana & Burn no motor

**O quê:** entra no `manaburn/index.html` o esboço de 07/11 (`nucleo/auditorias/2026-11-07_esboco_sala.md`): mesa de noite de Commander (decks com sleeves, cartas genéricas, d20, dados, deckboxes), mesa 96 px acima para sair da faixa das legendas no plano geral, piso de taco discreto entre rodapé e carpete, e a luz dentro do cenário (lâmpada quente, reflexo frio da TV que apaga com ela, primeiro plano mais escuro). Com a luz no cenário, o `luz.py` deixa de correr por defeito no `render.py` (`--luz-pos` liga); continua a servir vídeos de outro motor.
**Porquê:** fundador, 08/11/2026: "Sim finalizei tudo", em resposta ao pedido de aprovação dos pontos 1 a 4 do esboço.
**Fica de fora:** modelo do Burn no plano da TV (só cabeça, sem boné nem ombros): precisa de decisão própria.

## 07/11/2026 · Vince Vault: personagem em desenvolvimento e estratégia de créditos

**O quê:** novo personagem Vince Vault (Multiverse Capital, "Buy the dip!"), com bíblia em `vince/BIBLIA_PERSONAGEM.md` e referências em `vince/referencias/`. Turnaround oficial fixado; voz desenhada no ElevenLabs (`L93SDe6kGQj79D6svMgA`). Estratégia de créditos: imagens fixas no app Gemini, ElevenLabs só para voz e lip sync, estimativa antes de cada geração, uma variação por pedido, lip sync só no gancho.
**Porquê:** pedido do fundador (07/11/2026); a primeira ronda no ElevenLabs esgotou o saldo do plano.
**Impacto:** ainda não é uma frente. Formato e catálogo dependem de decisão do fundador. Os preços ditos pelo Vince seguem a regra de não inventar factos.

## 07/11/2026 (17:54) · Merge da luz padrão e do especial "Precon em jogo" para `main`

**O quê:** as branches `manaburn/luz-padrao` e `especial/precon-em-jogo-v2` (que inclui `especial/precon-em-jogo`) entram na `main`.
**Porquê:** "Prossiga" do fundador (07/11/2026, 17:54), em resposta ao pedido de decisão sobre o merge e a V2.
**Impacto:** `main` passa a renderizar o Mana & Burn com a luz padrão. Continuam por aprovar, com esboço próprio: fase 2 (luz no `index.html`), objetos novos e planos fixos.

## 07/11/2026 (17:36) · Luz e profundidade padrão em todos os episódios do Mana & Burn

**O quê:** as melhorias de cenário da V2 do especial "Precon em jogo" passam a padrão da série: luz ambiente quente com sombras abertas, reflexo frio azul-esverdeado à volta da TV (apaga com a tela), parede com menos contraste, primeiro plano mais escuro com desfoque leve abaixo das legendas, vinheta leve. Ficam intocados: tela da TV e carta, legendas, tarja, fecho e áudio. Implementação (fase 1): `manaburn/luz.py`, chamado por defeito no `render.py` (`--sem-luz` desliga); serve também para vídeos de outro motor (`--ate` = início do fecho).
**Porquê:** fundador, 07/11/2026: "Todos episódios de mana burn deve manter as melhorias que foram feitas nesse episódio", e "Pode avançar" à proposta refinada.
**Âmbito:** episódios novos e especiais do Mana & Burn. Publicados não se reabrem. Não vale para Conde, Meta em Curto nem Órbita.
**Fica de fora (precisa de aprovação própria):** fase 2 (luz dentro do `index.html`, como camadas do cenário); objetos novos (manta de crochê, benjamim, piso de taco); planos fixos da auditoria §5.

## 06/11/2026 · Protocolo de Pré-Release do TUBO (Meta em Curto)

**O quê:** (1) Novo `oraculo/PROTOCOLO_PRE_RELEASE.md`, canónico: quatro fases (investigação, previsões, acompanhamento, auditoria), integridade estatística, escala do grau de certeza e estados (PENDENTE, CONFIRMADA, PARCIALMENTE CONFIRMADA, REFUTADA, INCONCLUSIVA). (2) Novo modelo `nucleo/modelos/PREVISOES_PRE_RELEASE.md`; fichas por coleção em `oraculo/pre-release/`. (3) Ativação em `oraculo/PERFIL.md` e linha no router (`SHOWRUNNER.md` §2.2): previsões de pré-release passam a ser território do TUBO; hype e reação a spoilers continuam no Mana & Burn. (4) `comum/historico.md` ganha a secção «Previsões registadas do TUBO» (ID, estado, revisões, lições), que continua a ser o único histórico. (5) Remissões em `oraculo/CONTEXTO.md` §7.2 item 4, catálogo e `nucleo/README.md`; referência partida «§10» corrigida para «§7.2» em `comum/continuidade/`.
**Porquê:** decisão editorial aprovada pelo fundador (prompt «Implementação do Protocolo de Pré-Release do TUBO», 06/11/2026): tornar as previsões de pré-release do EP05 uma metodologia permanente e verificável, independente de cada coleção.
**Decisões técnicas:** um só documento de método e só remissões nos outros (sem duplicar regras); grau de certeza em 5 níveis, ligado ao medidor de 5 segmentos que já existe (`oraculo/CONTEXTO.md` §11), nunca em percentagem, com teto 3 antes do pré-release (não há dados de Sealed da coleção); o texto original da previsão não se edita e a auditoria compara sempre o original; previsão retrospectiva nunca entra como previsão.
**Impacto:** identidade, voz, trilha, cenários, estrutura, fecho e episódios publicados não mudam. Resolve a «exceção de território» que o EP05 tinha de declarar. O EP05 (branch `meta-em-curto-ep05`, por publicar) não foi tocado: ao integrá-lo, a sua tabela de previsões tem conflito com esta secção e as 4 linhas convertem-se para `PR-TRK-01` a `04`; a coluna «Confiança» passa à escala 1–5 (arredondando para baixo: «baixa» → 2, «média-baixa» → 2) e o «~35%» da linha pública sai ou ganha fonte e método, por decisão do fundador.

## 02/11/2026 · Especial "Precon em jogo": seguidor na tela e quadro do Conde

**O quê:** o fundador autorizou (02/11, 18:16) usar a foto de @diegoalencard e os seus comentários no especial `especiais/precon_em_jogo/`. Retrato do Conde na sala como detalhe visual silencioso, só neste especial. Trecho original do TUBO na TV. Autorizou a produção imediata às 18:28.
**Porquê:** missão de produção do especial (reconhecer a contribuição da comunidade).
**Impacto:** só este episódio; a identidade da sala não muda. Opções do kit ficam em `especiais/precon_em_jogo/patch.py`, fora de `manaburn/`.

## 02/11/2026 (01:27) · Merge da evolução visual para `main`

**O quê:** a branch `evolucao-visual-2026-11` (auditoria, QC automático, checklist P0/P1/P2, memória de continuidade, duração livre, kit v2 do Mana & Burn) entra na `main` por PR.
**Porquê:** "Aprovado" do fundador (02/11/2026, 01:27), em resposta ao pedido de aprovação do merge.
**Impacto:** `main` volta a ser a branch de trabalho. Continuam por aprovar, com esboço próprio, as expressões novas do Mana e do Burn (auditoria §4).

## 02/11/2026 (01:08) · Duração livre nos episódios de série (constituição v1.5) e Giro publicado

**O quê:** (1) Os episódios de série não têm duração mínima nem máxima: duram o necessário para reter o público sem destruir o entretenimento. Constituição §6, perfis do Mana & Burn, Meta em Curto e Conde, catálogo, `oraculo/CONTEXTO.md` (linha de formato) e `comum/qc/qc_video.py` (duração só informativa). As durações anteriores ficam como referência histórica. O Órbita mantém o loop de 12 s. (2) O formato Giro de domingo entra no perfil do Mana & Burn. (3) O Giro de domingo de 01/11 está publicado. (4) Seguir com as melhorias mesmo sem o motor do Giro, que foi feito noutro chat e não está disponível.
**Porquê:** mensagem do fundador de 02/11/2026, 01:08: "A duração dos episódios tem que ser livre o quanto for necessário para melhorar retenção do público sem destruir o entretenimento. Siga com as atualizações mesmo sem o motor."
**Impacto:** resolve a divergência 35–45 s (perfil) × 35–53 s (doc 05 do Drive). A regra §5 ("repetição = corte") passa a ser o limite real da duração. Em execução de (4): o núcleo do kit v2 do Mana & Burn passa para `manaburn/` (v1 em `manaburn/extras/v1/`) com as correções técnicas da auditoria e os elementos de cenário que a bíblia já previa (ventilador, antena com palha de aço, paninho de crochê); as expressões novas das personagens ficam por aprovar.

## 02/11/2026 · Gravidade P0/P1/P2, controlo de qualidade automático e memória de continuidade

**O quê:** (1) `CHECKLIST_QUALIDADE.md`: classificação P0 (bloqueia) / P1 (corrige ou o fundador aceita por escrito) / P2 (opcional), novo bloco E (personagens, cena, montagem, TV SAL) e passo automático. (2) Novo `comum/qc/qc_video.py` (formato, duração, loudness, pico, fecho, cortes, folha de contacto com zona segura). (3) Nova pasta `comum/continuidade/`: uma memória por série/personagem + índice comum; previsões do TUBO continuam em `comum/historico.md`. (4) Auditoria do Giro de domingo de 01/11 e propostas de evolução visual em `nucleo/auditorias/2026-11-02_evolucao_visual.md` (nada identitário aplicado).
**Porquê:** missão do fundador "Visual Evolution & Character Excellence" (02/11/2026), §9 (memória), §10 (checklist P0/P1/P2) e §8 (correções técnicas seguras).
**Impacto:** nenhum episódio publicado, asset mestre, voz, música ou script de episódio mudou. A TV ao fundo cortada nos planos de conjunto fica como P1 a confirmar pelo fundador (a bíblia só exige a carta inteira nos planos de TV e nos zooms; episódios aprovados já tinham a TV ao fundo cortada). Propostas de personagens, cenário-mestre e formato "Giro de domingo" aguardam aprovação. Bíblia do Mana & Burn no Drive lida a 02/11 e atualizada só com uma nota de fonte de verdade e uma secção de estado (sem mudar a identidade); notas iguais no "05 · como produzir um episódio" e no "06 · Mapa do Drive".

## 01/11/2026 · Memória editorial universal, encerramento obrigatório e insights (constituição v1.5)

**O quê:**
1. Novo `comum/REGISTRO_EDITORIAL.md`: um ID e uma linha por conteúdo de todas as frentes, com tema, objeto, tese, gancho, estado, fonte do estado, datas, ficha, relações e auditoria de originalidade. Estados `IDEIA → EM ANÁLISE → APROVADO → EM PRODUÇÃO → CONCLUÍDO → PUBLICADO`, mais `REJEITADO`, `PAUSADO`, `NÃO PUBLICÁVEL` e `POR AUDITAR` (este só para a migração retroativa).
2. Originalidade: antes de propor uma pauta, comparar tema, objeto, tese, gancho e ângulo com o registo inteiro; mudar título, personagem, frente ou formato não elimina a duplicidade; na dúvida, bloquear até decisão do fundador (`SHOWRUNNER.md` §2.3, constituição §10).
3. Encerramento obrigatório em 12 passos (`SHOWRUNNER.md` §6): pacote completo na pasta do episódio (roteiro, legenda, comentário fixado, texto alternativo, fontes, QC, localização do vídeo e da capa), registo, histórico, STATUS, handoff e commit conferido no GitHub. Nenhum episódio se declara arquivado antes disso. Ficha, handoff e checklist atualizados.
4. Novo `comum/insights/` (LEIA-ME, MODELO_SEMANAL, `registo_posts.csv`, `semanas/`): um snapshot por domingo, nunca reescrito; impulsionamento SIM/NÃO/PARCIAL/A CONFIRMAR, nunca inferido pelas views; relatório separa facto, interpretação, hipótese e recomendação. Os números deixam de ir para `comum/historico.md`, que passa a ser só a cronologia.
5. Ferramenta `comum/ferramentas/memoria.py` (validar, pauta, encerramento, semana, segredos) e testes A–F em `comum/ferramentas/test_memoria.py`.

**Porquê:** missão de engenharia do fundador de 01/11/2026 ("Memória Editorial Universal e Inteligência de Audiência"): trocar de agente, plataforma ou sessão sem perder a memória, repetir episódios ou perder o histórico de audiência.

**Impacto:**
- Nenhum conteúdo publicado ou aprovado foi reaberto; nenhum script de episódio mudou.
- Migração retroativa: 72 conteúdos (main, branches `giro/2026-11-01` e `pequeno-mestre/ep01`, projeto claude.ai). 30 ficam `POR AUDITAR` por falta de fonte: o inventário **não** está completo (lacunas no fim do registo).
- Critério de estado aplicado sem inventar: `PUBLICADO` só com Insights, captura do perfil ou confirmação do fundador. A confirmação global de 31/10 (10:46, "tudo o que está no repositório foi aprovado e lançado") vale como publicação sem data, exceto MB-EP09 e CM-EP003, que estavam agendados para depois dessa hora: ficam `APROVADO` com publicação A CONFIRMAR.
- Correção na migração dos insights de 26/10: o histórico marcava "não" no impulso de seis posts sem confirmação; passam a `A CONFIRMAR` (o fundador só disse "R$ 11 em dois vídeos").
- Alerta de originalidade (não decidido, para o fundador): MB-GIRO01 (branch `giro/2026-11-01`, publicação prevista 01/11, 21h) repete no bloco 3 o evento, a carta e a regra do MB-EP07 (All Leylines' Eve).
- O registo de 26/10 sobre o Q (MB-EP01 × ORB-11), Kirk e Picard mostra objetos repetidos entre frentes antes desta regra; ficam como precedentes, não se reabrem.

*Reconciliação (12/11/2026):* a entrada acima previa a constituição v1.5; entre 01/11 e a integração a v1.5 passou a ser a duração livre (02/11), por isso estas alterações entram como **v1.6**. Os números já registados em `comum/historico.md` ficam como histórico; os novos vão para `comum/insights/`. O registo editorial está desatualizado desde 01/11 (conteúdos das branches por registar).

## 31/10/2026 · Fecho do scanner no repositório e merge da consolidação para `main`

**O quê:** `comum/outro/outro_binder_916.mp4` passa a existir no repositório, cortado do fim do `ManaBurn_Ep6_GodPack_916.mp4` publicado (49,0 s → fim), com o rótulo "MANA & BURN" tapado na fase da logo; script em `comum/outro/gerar_fecho.py`. Resolve o bloqueador 8 da entrada de 28/10. O fundador aprovou o merge de `consolidacao-estudio` para `main` (PR #1).
**Porquê:** pedido do fundador (31/10/2026, 15:50): "Tire do final do vídeo que te enviei. Aprovado o merge."
**Impacto:** quem clona o repositório já cumpre a regra do fecho sem reconstruir. Os episódios publicados com o fecho reconstruído não mudam. Depois do merge, `main` é a branch de trabalho e o prompt do ChatGPT aponta para ela.

## 31/10/2026 (15:18) · Respostas do fundador a Q1–Q3 (constituição v1.4)

**O quê:**
1. Q1 · O nome público da série do TUBO é **Meta em Curto**. A pasta `oraculo/` mantém-se (scripts). Catálogo, `series.yaml`, `AGENTS.md`, `SHOWRUNNER.md` e a linha de território de `oraculo/CONTEXTO.md` usam o nome novo.
2. Q2 · **O Órbita não termina com o fecho do scanner nem com propaganda do BINDER no fim do vídeo.** Constituição §6, checklist C, `orbita/CONTEXTO.md` §4 e `series.yaml` (`fecho: false`). O selo "BINDER Vision" da composição e o CTA da legenda mantêm-se, porque o fundador falou do fim do vídeo e fazem parte da identidade aprovada.
3. Q3 · Órbita e Lambe-lambe passam a ter pasta no repositório: `orbita/CONTEXTO.md` (bíblia), `orbita/gerador/` (10 ficheiros copiados sem alterações de `claude/gerador/` do projeto claude.ai, com `LEIA-ME.md`) e `lambe-lambe/CONTEXTO.md` (bíblia). As bíblias foram compostas só a partir das fontes indicadas no topo de cada uma; os documentos de origem ficam como histórico.
**Porquê:** mensagem do fundador de 31/10/2026, 15:18.
**Impacto:** a exceção "bíblias do Órbita e do Lambe-lambe fora do repositório" sai da constituição §1. Para renderizar o Órbita faltam os PNGs das cartas e as fontes em `node_modules/` (ver `orbita/gerador/LEIA-ME.md`). `captions2–5.py` (legendas publicadas do Órbita) ficam no projeto claude.ai como histórico.

## 31/10/2026 · Missão "Consolidação estrutural do BINDER Originals": frentes, hierarquia e Showrunner (constituição v1.3)

**Decisões do fundador (missão de 31/10/2026, 10:46):**
1. Órbita (universo temático de Star Trek) e Lambe-lambe (formato espontâneo, permanente) estão **ativos**. Revoga a classificação "arquivada" da entrada abaixo.
2. O especial de Halloween 2026 e a sequência de Star Trek estão publicados. Tudo o que está no repositório foi testado, aprovado e lançado. Vozes e músicas foram criadas pelo fundador e estão aprovadas: não se reabrem aprovação, qualidade, licenciamento nem produção desses materiais, nem aparecem como pendências.
3. Pastas das séries mantêm-se (`manaburn/`, `oraculo/`, `conde/`, `especiais/`, `comum/`); núcleo em `nucleo/`, sem duplicação.

**O quê (execução):**
- Novo `nucleo/CATALOGO_EDITORIAL.md`, canónico para classificação, estado, objetivo, identidade e território de cada frente; `series.yaml` passa a ter só configuração técnica (sem estado nem classificação).
- Constituição v1.3: §1 hierarquia documental (AGENTS → constituição → catálogo → bíblias → decisões → técnica → histórico, com o pedido explícito do fundador acima de tudo); §2 remete para o catálogo em vez de repetir a tabela; §6 formato por frente (séries 9:16, Órbita 4:5, Lambe-lambe 4:5 ou 9:16), sem corte lateral em qualquer formato; §10 e checklist: "Tem um detalhe escondido. Diga o segundo." só quando há easter egg (a regra anterior pedia a frase mesmo com 0 eggs).
- Novo `nucleo/SHOWRUNNER.md` (quatro tipos de produção, router entre frentes, o que decide e o que pede, briefing, manutenção do estado), `nucleo/modelos/HANDOFF.md`, `nucleo/prompts/CLAUDE_PROJECT.md` e `nucleo/prompts/CHATGPT.md`.
- Palavras de arranque novas, operacionais: `especial`, `orbita`, `lambe`/`post`, `oraculo` (acrescenta a `tubo`/`meta`).

**Perguntas ao fundador (não decididas, para não inventar):**
- Q1 · Nome público da série do TUBO: "Meta em Curto" (repositório desde 28/10) ou "Oráculo de Tubo" (missão de 31/10)? Até lá, os documentos usam "Meta em Curto · Oráculo de Tubo".
- Q2 · Fecho do scanner nos Reels 4:5 do Órbita: o fecho existe só em 9:16. Fazer uma versão 4:5, aceitar sem fecho, ou outra regra?
- Q3 · Bíblias do Órbita e do Lambe-lambe: trazer para o repositório os documentos do projeto claude.ai e do Drive (e o gerador `claude/gerador/` do Órbita)?

**Impacto:** nenhum conteúdo publicado, voz, música ou script mudou. A missão substitui o plano por fases do prompt anterior; o que dele faltava de técnico (motor v2 do Mana & Burn no repositório, episódios de referência) passa a pendência técnica, não bloqueia a governação.

## 31/10/2026 · Consolidação do estúdio, Fase 1: núcleo, registo e fonte de verdade (constituição v1.2)

**O quê:** (1) `comum/originals/` passa a `nucleo/` (mesmos nomes de ficheiro; nenhum script dependia da pasta). (2) Constituição §1: o repositório é a fonte de verdade; as instruções do projeto claude.ai, o Drive e as skills apontam para ele; o pedido explícito do Ibisson continua no topo. (3) §2: entram `especiais/`, `nucleo/` e o registo `series.yaml`. (4) §10 e checklist C: o texto alternativo passa a ser entregável (já era a peça 4 da skill `binder-posts-instagram`). (5) `AGENTS.md` passa a ser o ponto de entrada neutro; `CLAUDE.md` só remete para ele. (6) Merge da branch `especial/sir-patrick` (constituição v1.1 §14, especial Picard v2) para `consolidacao-estudio`.
**Porquê:** prompt "Operação de Consolidação — Estúdio BINDER" (31/10/2026), §3 e §7, e `INVENTARIO.md` (divergências D1, D3, D4). Opções do inventário aplicadas por defeito depois de "Prossiga" sem resposta às perguntas P1–P4: pastas das séries ficam no lugar (Opção B); Órbita e Lambe-lambe registadas como arquivadas; TUBO mantém silhueta em vez de foto de jogador (entrada de 29/10 abaixo; a bíblia prevalece sobre o prompt); `especial/sir-patrick` integrada.
**Impacto:** nenhum episódio publicado muda. As pastas `manaburn/`, `oraculo/`, `conde/` e `comum/outro/` não mudaram de sítio, por isso nenhum script parte. As skills e as instruções do projeto claude.ai ainda dizem que o Drive manda; ficam alinhadas na Fase 3. Tudo isto vive só na branch `consolidacao-estudio` até o Ibisson aprovar o merge para `main`.

## 29/10/2026 · Especial Capitão Picard refeito (v2) pela secção 14

**O quê:** nova versão do especial em `manaburn/episodios/esp02_picard_v2/` (celebração, conversa de Mana e Burn, 69,9 s). A v1 (`esp01_sir_patrick/`, commit caf6e97) fica guardada e marcada como não publicável.
**Porquê:** ordem do Ibisson de 29/10/2026 (23:04) para refazer o especial segundo a §14.
**Impacto:** mantêm-se as exceções de entrega do brief original (sem fecho do scanner, sem CTA do app, sem "Diga o segundo"), porque a ordem nova não as revoga e o episódio continua ligado a uma morte. A duração deixa de ser exceção (§14).

## 29/10/2026 · Especiais e homenagens (constituição v1.1, secção 14)

**O quê:** nova secção 14 na constituição e um item no checklist (A). Especiais, homenagens e acontecimentos extraordinários podem existir em qualquer série, sem limite rígido de duração; homenagens priorizam celebração, admiração, legado, inspiração, personalidade e reconhecimento, com humor subtil quando adequado; velocidade editorial nunca à custa de rigor, identidade da marca ou qualidade narrativa.
**Porquê:** regra enviada pelo Ibisson a 29/10/2026, depois do especial de Sir Patrick Stewart.
**Impacto:** a exceção de duração registada para o especial de Sir Patrick (entrada abaixo, ponto 4) passa a estar coberta pela regra geral. O especial entregue a 29/10 tem tom contido e melancólico (noite, piano lento, sem humor), pedido no brief original; não segue a nova orientação de celebração até ser refeito.

## 29/10/2026 · Mana & Burn · especial de homenagem (Sir Patrick Stewart): exceções pontuais

**O quê:** o especial `manaburn/episodios/esp01_sir_patrick/` não segue quatro regras da série e da constituição: (1) sem fecho do scanner (`outro_binder_916.mp4`); o vídeo termina no ponto verde e na assinatura "BINDER Originals", sem "Disponível no Google Play"; (2) legenda sem "baixe o BINDER Vision" nem CTA do app; (3) comentário fixado sem "Tem um detalhe escondido. Diga o segundo." e sem easter egg; (4) formato fora do perfil: 54,8 s, locução contínua do Mana + uma fala do Burn, em vez de 14 falas em bate-volta e 35–45 s.
**Porquê:** pedido explícito do Ibisson no brief do especial (nível 1 da hierarquia, §1): homenagem sem promoção do app, sem humor e sem parecer exploração comercial do luto.
**Impacto:** só este episódio. As regras voltam a valer no episódio seguinte. Cena própria (`homenagem.html`) feita com os desenhos do `manaburn/index.html` sem alterá-lo; trilha original sintetizada (`musica.py`) em vez da trilha rock da série.

## 02/11/2026 · Meta em Curto: foto real do campeão passa a padrão

**O quê:** `oraculo/CONTEXTO.md` §6.4: o campeão aparece com foto real na ficha, em vez da silhueta. Altera a regra de 29/10, que exigia autorização registada em `oraculo/autorizacoes/`. Outros jogadores mantêm a silhueta.
**Porquê:** pedido do fundador (02/11/2026, EP04).
**Impacto:** risco aceite pelo fundador: a foto tem direitos do autor ou do organizador e o direito de imagem do jogador; pode haver denúncia de direitos. Mitigação: só foto oficial, com crédito.

## 29/10/2026 · Meta em Curto EP02 e regra de evidência visual

**O quê:** `oraculo/CONTEXTO.md` passa a v6 com a secção 6.4: deck citado → lista completa no ecrã; carta citada → imagem oficial do Scryfall; jogador citado → ficha de jogador com silhueta, sem fotos. Novo modo «Leitura da Final» para quando não há VOD analisável. Estreia do Erro de sistema.
**Porquê:** pedido do Ibisson (29/10/2026): quem vê deve poder conferir a lista, a carta e quem é o jogador. Fotos de jogadores ficam de fora por direitos de imagem e de autor (cobertura SCG/WotC); só entram com autorização registada em `oraculo/autorizacoes/`.
**Impacto:** episódios do TUBO ficam mais longos de produzir (listas e cartas), mas reutilizam `ep02_render.py`. A lista também sai no comentário fixado e no carrossel.

## 29/10/2026 · Análise do Meta em Curto EP01 (render final)

**O quê:** ficha com controlo de qualidade (`oraculo/episodios/ep01_ac13_ficha.md`); `oraculo/CONTEXTO.md` passa a v5 (voz definida, silêncio alinhado à revelação, elementos fixados no EP01, pendentes atualizados); duração do perfil conta sem o fecho.
**Porquê:** o EP01 resolveu decisões que o `CONTEXTO.md` ainda dava como pendentes.
**Impacto:** a divergência 6 (voz do TUBO) da entrada de 28/10 fica resolvida: "Antonio de Jesus". Sem defeitos bloqueadores no EP01; 2 melhorias para o EP02 (tamanho das fontes no ecrã, −14 LUFS).

## 28/10/2026 · v1.0 do sistema BINDER Originals

**O quê:** constituição comum, checklist, modelos de ficha e de perfil, `PERFIL.md` por série, `CLAUDE.md` + `AGENTS.md` na raiz.
**Porquê:** as regras estavam espalhadas entre instruções do projeto, skills, documentos do Drive e conversas; cada série repetia regras comuns de forma diferente.
**Impacto:** todo agente começa pelo `CLAUDE.md`. Os `CONTEXTO.md` não foram alterados.

Divergências encontradas na auditoria e como ficaram:

1. **Nome do Conde.** Pedido de 28/10 diz "Conde de Terra Forte"; repositório, episódios e instruções do projeto dizem "Conde de Manaforte". Mantido **Manaforte** até o Ibisson confirmar outra coisa.
2. **Nome da série do TUBO.** Pasta `oraculo/` e `CONTEXTO.md` dizem "Oráculo de Tubo"; nome atual é "Meta em Curto". Pasta mantida (scripts dependem dela); perfil e `CLAUDE.md` usam o nome novo.
3. **Fecho da legenda e do comentário do Conde.** `conde/CONTEXTO.md` §8 tem frases anteriores ao sistema de easter eggs. Prevalece a regra comum ("baixe o BINDER Vision" / "Tem um detalhe escondido. Diga o segundo.").
4. **Território Mana & Burn × Meta em Curto.** O doc do Mana & Burn previa "episódio de campeonato". Regra: decisão e meta → Meta em Curto; reação/polémica de um torneio → Mana & Burn.
5. **Kit do Mana & Burn.** GitHub tem a v1; a skill usa a v2 do projeto claude.ai. Pendente subir a v2.
6. **Voz do TUBO.** `comum/historico.md` regista "Antonio de Jesus"; `oraculo/CONTEXTO.md` §3 diz "a escolher". Pendente confirmar.
7. **Arranque.** As instruções do projeto só conhecem `manaburn` e `conde`; o `CLAUDE.md` acrescenta `tubo`.
8. **Fecho do scanner ausente do repositório (bloqueador).** `.gitignore` ignora `*.mp4`, por isso `comum/outro/outro_binder_916.mp4` nunca subiu; só os 45 quadros de `comum/outro/scan/` estão no GitHub. Adicionada a exceção `!comum/outro/*.mp4` ao `.gitignore`. Falta o Ibisson enviar o ficheiro para ele ser commitado. Até lá, quem clona o kit não consegue cumprir a regra do fecho.
9. **"Dois prompts operacionais anteriores"** (auditoria / produção autónoma) não estão no repositório nem nos documentos do projeto; as regras deles que já estavam nas instruções foram absorvidas aqui.

Testes de coerência (28/10/2026), sem produzir vídeos:
- A · TUBO analisa jogada real → `oraculo/PERFIL.md` (reconstrução, VOD com minuto, Oracle, alternativas) + bloqueador "imagem de transmissão". OK.
- B · Mana & Burn sobre tendência recente → perfil (investigação aprofundada, 2 fontes, data da semana) + constituição §4 (datas). OK.
- C · Conde comenta uma obra → `conde/PERFIL.md` (observação / interpretação / facto separados). OK.
- D · Série nova → `modelos/PERFIL_SERIE.md` + linha na tabela §2; constituição intacta. OK.
- E · Fonte, ferramenta ou autorização indisponível → constituição §11. OK; o próprio teste revelou o bloqueador 8.
