# BINDER Cultural Intelligence · Fase 1 (diagnóstico), com desenho e prioridades

28/11/2026 · pedido do fundador «Missão: BINDER Cultural Intelligence» · branch local `inteligencia-cultural-binder` (sem push, sem merge) · 0 créditos gastos.

Este documento cobre as fases 1 a 3 do pedido (diagnóstico, arquitetura, priorização). **Nada foi implementado**: o pedido manda entregar o diagnóstico antes de implementar, e três das mudanças propostas alteram regras (radar, rubrica do Showrunner, colunas do registo de insights), que só mudam com decisão do fundador (`AGENTS.md` §2, constituição §1).

## 1. Estado verificado do repositório (28/11/2026, 00h50 UTC)

| Verificação | Resultado |
|---|---|
| `main` | `9380fda` (MB-EP21), árvore limpa |
| `auditoria/motor-producao-2026-11-27` | no GitHub (`e9dc3d4`) = `main` + 1 commit; **não integrada**. Toca motores, QC, ambiente e `cartas.py`; não toca radar, insights, registo nem Showrunner: não há conflito com esta missão, por isso a branch nova parte da `main` |
| `inteligencia-cultural-binder` | não existia no GitHub; criada localmente a partir da `main` |
| Arranque obrigatório | `AGENTS` + `STATUS` + constituição + catálogo + `SHOWRUNNER` = 88 KB (~22 mil tokens) |

## 2. O que já existe e responde às cinco perguntas

A camada pedida **já existe em 70 %**, espalhada por peças que funcionam. Não se reconstrói nenhuma.

| Pergunta do fundador | Peça existente | Estado |
|---|---|---|
| 1. O que está a acontecer? | Radar semanal `comum/radar/` (regra de 26/11; `2026-W48.md`, 12 linhas) · calendário de eventos com fonte `oraculo/previsoes/calendario.yaml` | funciona, mas estreito (ver L1) |
| 2. Que histórias merecem ser contadas? | `SHOWRUNNER.md` §2.4: ≥ 3 candidatos, ficha de 9 campos, rubrica 1–5 com 7 critérios, reservas · `memoria.py pauta` (saturação interna) · router §2.2 | funciona por episódio; não compara entre semanas (L2) |
| 3. Por que interessa à audiência? | §2.4 passo 2a (correlação Brasil/Europa/EUA) · ficha de 9 campos | regra existe; na prática Brasil e Europa ficam vazios (L1) |
| 4. Qual formato? | router §2.2 · catálogo · gancho em 7 campos §4.1 · abertura de objeto §4.1.1 · `FICHA_EPISODIO.md` (premissa, estrutura, fontes, riscos, QC) | completo: o Módulo 3 pedido já é a ficha + bíblia da frente |
| 5. Como aprender com o publicado? | `comum/insights/` (rotina de domingo, testes de uma variável, leitura a 48 h e 7 dias, constituição §12) · `registo_app.csv` · prestação de contas das previsões `oraculo/previsoes/registo.yaml` | método bom, **sem dados** (L3) |

## 3. Lacunas reais (com a evidência)

- **L1 · O radar é evidência de pautas já escolhidas, não descoberta.** As 12 linhas de W48: 9 de EDHREC/Commander Spellbook (EUA/global), 3 de cEDH em Portugal; **0 do Brasil**, 0 de arte, artistas, estética, colecionismo ou cultura geek; todas com a coluna «Usado em» preenchida por um episódio de Mana & Burn ou TUBO. Não há categoria (emergente, saturado, janela, movimento), nem grau de confiança. As três limitações registadas repetem «Brasil e Europa sem linha».
- **L2 · A rubrica do Showrunner não mede o que o fundador pede.** Os 7 critérios de §2.4 cobrem gancho, originalidade, compreensão, visual, partilha, recompensa e adequação. Faltam: **disponibilidade de fontes, longevidade, custo/esforço, relevância cultural, identidade BINDER** (além da personagem) e **«porquê agora ou esperar»**. E vive em prosa dentro de cada ficha: oportunidades preteridas perdem-se e não se comparam de uma semana para a outra.
- **L3 · A aprendizagem não tem dados.** O registo tem **52 conteúdos `PUBLICADO`**; `registo_posts.csv` tem números de **11**, e só **1** (MB-EP13) tem tempo médio de visualização. Retenção aos 3 s: 0. Atributos do vídeo (duração, tipo de gancho, narrativa): 0 colunas (auditoria de 27/11, B11). Último snapshot: 21/11. **Hoje nenhuma análise de padrões é possível**, nem com cautela. Bloqueio: a @binder_vision não está ligada no vidIQ (pendente desde 16/11) e os prints de domingo não chegam.
- **L4 · O gargalo não é descobrir histórias.** Há **26 `CONCLUÍDO` + 13 `APROVADO` = 39 conteúdos prontos ou aprovados por publicar**, contra 52 publicados. Um sistema que gere mais pautas aumenta a fila; o valor está em escolher melhor entre menos e em medir o que sai.
- **L5 · A memória de originalidade tem buracos.** 30 linhas `POR AUDITAR` no registo: `memoria.py pauta` não as conhece bem.
- **L6 · Acesso às fontes (testado na cloud a 28/11).** Pela shell abrem só Scryfall, `json.edhrec.com` e Cards Realm. Reddit (JSON e RSS), RSS do YouTube, magic.wizards.com, magic.gg, MTGGoldfish, ArtStation e Instagram: sem ligação; LigaMagic: 403. Pela pesquisa web e pelo agente web-fetch abrem caso a caso. No PC do fundador provavelmente abrem (não testado: o repositório não está clonado lá).

## 4. O que não vale a pena construir

| Ideia | Porquê não |
|---|---|
| Crawler multiplataforma, base de dados, dashboard | 30 min/dia de operação; sem dados de audiência para alimentar; manutenção maior que o ganho |
| «Trend score» automático de popularidade | não há métricas fiáveis de popularidade nas fontes abertas; seria número inventado |
| Recolha do Instagram ou de perfis de terceiros | termos de uso; só os Insights da própria conta (vidIQ ou prints) |
| Agentes por módulo, MCP novo, skills novas | a constituição §3 e a auditoria de 27/11 já concluíram: um agente em sequência; cada subagente relê ~22 mil tokens de arranque |
| Novo módulo de desenvolvimento criativo | já é `FICHA_EPISODIO.md` + §4.1–4.3 + bíblia da frente |
| Módulo comercial de marca | o pedido diz que a marca conquista o direito de vender pela cultura; basta um critério na avaliação (abaixo) |

## 5. Arquitetura proposta (Fase 2): três extensões e um script

Nada de sistema novo. Três peças existentes ganham o que lhes falta e um script só com a biblioteca padrão liga-as.

```
 segunda (≤ 30 min)                quando há vaga                 depois de publicar
 ┌──────────────┐  linhas   ┌─────────────────────┐ escolha ┌───────────────┐   ┌─────────────────┐
 │ M1 Radar v2  │─────────▶ │ M2 Oportunidades     │───────▶ │ Showrunner    │──▶│ M4 Insights v2  │
 │ comum/radar/ │           │ comum/inteligencia/  │ fundador│ ficha (M3)    │   │ registo_posts + │
 │ +categoria   │           │ oportunidades/*.yaml │         │ memoria.py    │   │ atributos do    │
 │ +confiança   │           │ oportunidades.py     │         │ pauta, motor  │   │ vídeo; padrões  │
 │ +janela      │           │ (10 critérios, porquês)│       │ da frente     │   │ só com amostra  │
 └──────────────┘           └─────────────────────┘         └───────────────┘   └────────┬────────┘
        ▲                                                                                │
        └──────────────── aprendizagem (facto · hipótese · teste) volta à avaliação ◀────┘
```

| Módulo | Entrada | Saída | Onde vive | Intervenção humana | Se falhar |
|---|---|---|---|---|---|
| **M1 Trend** (radar v2) | fontes abertas lidas na sessão (pesquisa web, web-fetch, Scryfall, EDHREC) e, se se confirmar, o PC do fundador | linhas com **categoria A–F**, **confiança** (alta/média/baixa + porquê), **janela** e evidência | `comum/radar/AAAA-Www.md` (mesmo ficheiro, 3 colunas novas) + uma lista fixa de varrimento por região **e por território cultural** (arte e artistas, colecionismo, cultura geek) | nenhuma para recolher | fonte fechada = limitação escrita, nunca linha |
| **M2 Editorial** (oportunidades) | linhas do radar, ideias do fundador, reservas das fichas | uma ficha por oportunidade, 10 critérios 1–5 **cada um com a frase que o justifica**, pergunta central, ângulo, evidências, o que falta verificar, «agora ou esperar»; tabela semanal ordenada | `comum/inteligencia/oportunidades/<id>.yaml` + `comum/ferramentas/oportunidades.py` (valida e imprime a tabela) | **o fundador escolhe**; o script nunca escolhe | sem script, o YAML lê-se à mão |
| **M3 Criativo** | oportunidade escolhida | ficha de episódio | `FICHA_EPISODIO.md` + §4.1–4.3 (sem mudanças) | aprovação de roteiro e créditos, como hoje | — |
| **M4 Audiência** | Insights (vidIQ como dono, ou prints), Play Console por UTM, `registo_app.csv` | colunas observadas (tempo médio, % assistida, taxa de saltos, partilhas, guardados…) separadas das calculadas e dos atributos do vídeo (duração, tipo de abertura, tipo de narrativa); relatório de padrões que diz «amostra insuficiente» abaixo do limiar | `comum/insights/registo_posts.csv` (colunas novas no fim) + subcomando `memoria.py padroes` | o fundador liga o vidIQ ou envia os prints | sem dados: o relatório diz o que falta, não estima |
| **M5 Marca** | — | critério «valor de marca» na avaliação (artista, estética, comunidade, relação futura) e nota de direitos | dentro do M2 | colaborações só pelo fundador (`nucleo/auditorias/2026-11-16_parcerias.md`) | — |

**Regras de avaliação do M2** (transparentes, sem média mágica): os 10 critérios do pedido, cada um 1–5 com uma frase; mostra-se a soma **e** as notas todas; portões que nenhuma soma compensa: identidade BINDER ≤ 2 → fora; fontes confiáveis ≤ 2 → «esperar»; janela vencida → fora. A rubrica de 7 critérios do §2.4 continua para escolher entre candidatos do mesmo episódio; o M2 decide **se e quando** a história merece um episódio.

**Fluxo completo (exemplo):** segunda, radar (30 min) → `oportunidades.py` mostra as 3–5 melhores com os porquês → o fundador escolhe uma → `memoria.py pauta` → ficha e produção como hoje → publicação com `utm_campaign=<ID>` → domingo, números + atributos no registo → quando houver amostra, `padroes` propõe um teste («repetir em 3 episódios») → a lição entra como hipótese na avaliação seguinte.

## 6. Prioridades (Fase 3)

| # | Melhoria | P | Esforço | Custo | Benefício |
|---|---|---|---|---|---|
| 1 | Ligar a @binder_vision no vidIQ (OAuth) e confirmar o custo em créditos de `vidiq_instagram_owner_insights` antes de a usar | **P0** | 5 min do fundador | a confirmar (pode gastar créditos) | sem isto o M4 não existe |
| 2 | M2: esquema YAML + `oportunidades.py` + testes + caso-piloto real | P1 | ~1 sessão | 0 créditos | decisão de pauta explicada e comparável entre semanas |
| 3 | M1: 3 colunas no radar + lista de varrimento cultural e Brasil | P1 | ~1 h de documentação | 0 | descoberta fora dos combos de Commander |
| 4 | M4: colunas de retenção e atributos no `registo_posts.csv` (já proposto pela auditoria, B11) | P1 | ~1 h | 0 | a aprendizagem passa a ter onde viver |
| 5 | Publicar a fila de 39 antes de abrir pautas novas | P1 | do fundador | 0 | dados reais para o M4 |
| 6 | `memoria.py padroes` (só com ≥ 10 Reels com retenção na mesma frente) | P2 | ~2 h | 0 | padrões com aviso de amostra |
| 7 | Fechar as 30 linhas `POR AUDITAR` | P2 | fundador + 1 h | 0 | originalidade fiável |
| 8 | Recolha automática no PC do fundador (RSS do Reddit e do YouTube, sem chaves) | P3 | ~3 h + teste no Windows | 0 | só se o radar manual provar valor durante 3–4 semanas |
| 9 | API do YouTube, Trend Lab, registo de relações com artistas | P3 | — | chave/quota | experimento futuro |

**Conjunto mínimo para a Fase 4:** itens 2, 3 e 4, mais o caso-piloto (um assunto real de Magic, com fontes, avaliação, proposta de roteiro e o plano de medição). Nenhum toca motores, episódios publicados ou identidade visual. Custo: 0 créditos.

## 7. Decisões do fundador

1. Avançar para a Fase 4 com o conjunto mínimo (itens 2–4 + piloto).
2. Autorizar as mudanças de regra que isso implica, registadas em `DECISOES.md`: 3 colunas no radar; avaliação de oportunidades com 10 critérios; colunas novas no `registo_posts.csv`.
3. Ligar a @binder_vision no vidIQ; autorizar (ou não) créditos para ler os Insights por API.
4. Independente desta missão: integrar a branch da auditoria de 27/11.

## Handoff

Branch local `inteligencia-cultural-binder` (1 commit: este documento). Sem push. Próximo passo: com o «sim» do fundador, Fase 4 pelo conjunto mínimo do §6.
