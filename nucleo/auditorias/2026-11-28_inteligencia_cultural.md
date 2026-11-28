# BINDER Cultural Intelligence · Fase 1 (diagnóstico), com desenho e prioridades

28/11/2026 · pedido do fundador «Missão: BINDER Cultural Intelligence» · branch local `inteligencia-cultural-binder` (sem push, sem merge) · 0 créditos gastos.

As secções 1–7 são as fases 1 a 3 (entregues antes de implementar). O fundador escolheu «Sim, conjunto mínimo + piloto» no cartão (28/11, 00:57 UTC); as fases 4 e 5 e o relatório final no formato A–I estão no §8.

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

## 8. Fases 4 e 5 · relatório final (A–I)

### A. Diagnóstico
§1–§4. Em resumo: 70 % da camada já existia; faltavam descoberta fora dos combos (radar), uma avaliação com fontes, longevidade, custo, identidade e «agora ou esperar», e dados de retenção (1 de 52 publicados com tempo médio). O gargalo é publicar e medir (39 conteúdos à espera), não descobrir.

### B. Arquitetura
§5, implementada só na parte mínima: radar v2 → ficha de oportunidade (10 critérios + portões) → escolha do fundador → Showrunner e ficha como hoje → registo com retenção e atributos → `padroes` só com amostra.

### C. O que foi implementado

| Ficheiro | Novo/alterado | Porquê |
|---|---|---|
| `comum/inteligencia/LEIA-ME.md` | novo | regras, fluxo de 30 min, critérios, portões, limites |
| `comum/inteligencia/oportunidades/OP-2026-W48-01.yaml` | novo | caso-piloto real (10 evidências, 5 verificações pendentes) |
| `comum/inteligencia/oportunidades/OP-2026-W48-02.yaml` | novo | exemplo real sem fontes lidas: o portão manda **esperar** |
| `comum/inteligencia/pilotos/OP-2026-W48-01_proposta.md` | novo | proposta audiovisual completa (14 pontos) e plano de medição |
| `comum/ferramentas/inteligencia.py` | novo (~300 linhas, só PyYAML) | `validar`, `oportunidades [--detalhe]`, `padroes` |
| `comum/ferramentas/test_inteligencia.py` | novo | 18 testes |
| `comum/ferramentas/memoria.py`, `test_memoria.py` | alterado | aceita e valida as 7 colunas novas (números com ponto, % ≤ 100, data) + 1 teste |
| `comum/insights/registo_posts.csv` | alterado | 7 colunas vazias no fim; conferido por script que **todas as linhas antigas ficaram iguais** antes da vírgula nova |
| `comum/insights/LEIA-ME.md`, `comum/radar/LEIA-ME.md`, `comum/radar/2026-W48.md` | alterado | colunas novas documentadas; radar v2 com varrimento; linhas 13–15 no formato v2 |
| `nucleo/SHOWRUNNER.md` | +1 passo (§2.4 passo 10) | aponta para a tabela; a rubrica de 7 critérios não muda |
| `nucleo/DECISOES.md`, `comum/historico.md`, `STATUS.md` | alterado | registo da decisão e do estado |

Não mexido: motores, QC, episódios, identidade visual, workflow do GitHub (a branch da auditoria também o altera; acrescentar o passo dos testes novos depois do merge dela evita conflito).

### D. Testes (resultados reais, 28/11)
- `test_inteligencia.py`: 18 testes OK (nota sem porquê recusada, critério em falta, evidência sem URL, ausência sem URL aceite, portões identidade/fontes/janela/saturado, ordenação, padrões com e sem amostra, vazio ≠ zero, % calculada identificada, registo real).
- `test_memoria.py`: 18 OK (17 antigos + retenção inválida). `test_ciclo.py`: OK. `memoria.py validar`: OK. `ciclo.py validar`: OK. `validar_repo.py`: 1 problema não grave, **já existente** (`vince/kit/v1/`).
- `inteligencia.py oportunidades`: 0,06 s. `padroes` no registo real: «amostra insuficiente» (nenhum conteúdo tem `tempo_medio_s` nas colunas novas). É o resultado correto, não uma falha: o M4 está à espera de dados.
- Não testado: Windows/PowerShell (só Python + PyYAML, sem caminhos fixos; deve correr, mas não foi visto); o workflow `validar` no GitHub (sem push).

### E. Economia operacional (estimativas, ditas como tal)
- **Evitado construir:** crawler, base de dados, dashboard, agentes por módulo, MCP novo (§4). Tudo o que existe são ~44 KB de texto e código num formato que o fundador lê sem ferramentas.
- **Custo de execução:** 0 créditos e 0 assinaturas; a pesquisa do piloto usou pesquisa web, um agente de leitura de páginas (6 páginas) e a API gratuita do Scryfall.
- **Tempo:** a avaliação fica escrita uma vez e reaproveita-se; hoje as reservas de cada ficha perdem-se e a escuta refaz-se por episódio. Estimativa (não medida): 15–30 min poupados por pauta nova quando a oportunidade já está avaliada. Medir nas próximas 3 pautas: tempo da escolha do tema na ficha.
- **Risco evitado:** o `memoria.py pauta` apanhou durante o piloto que The One Ring é objeto bloqueado (LL-R02, LL-CUR07): entrou só como contexto.

### F. Demonstração (caso-piloto)
- **Assunto:** a versão LCARS de «There's Coffee in that Nebula» (Star Trek, 13/11/2026) passou a creditar também Rutger van de Steeg; a nebulosa é uma pintura dele para Star Trek: Prodigy.
- **Fontes e evidências:** Scryfall (#369, #503, #40; hoc #44), ICv2 (13/11), três comunicados oficiais da Wizards (2021, 2023, 2025), EpicFlix (05/2026); um blog promocional marcado como fonte fraca; ausência de dados de interesse e de fontes BR/PT registada.
- **Avaliação:** 40/50, veredito AVALIAR, confiança média, janela até 08/12; notas 5·3·4·4·4·4·3·4·5·4 com as frases em `--detalhe`. A OP-02 (artistas convidados) fica em ESPERAR porque só há um título de pesquisa.
- **Abordagem:** Reel documental do Lambe-lambe, sem voz, 35–40 s, «1 carta · 2 artistas», linha do tempo de casos, sem acusar pessoas nem mostrar a pintura original.
- **Medição pós-publicação:** taxa de saltos, tempo médio, % assistida, guardados, partilhas, comentários, UTM; atributos `objeto-contraste` e `documental-linha-do-tempo`.
- **Bloqueante antes de produzir:** ler o comunicado da Wizards de 12/11/2026.

### G. Riscos
- O radar v2 só funciona se for feito: sem varrimento semanal, as oportunidades voltam a nascer dos combos.
- Notas 1–5 continuam a ser juízo; a frase obrigatória torna o juízo revisível, não objetivo.
- `padroes` com amostras pequenas pode tentar a ler causas: o texto diz «hipótese» e «não é causa», mas a leitura humana tem de respeitar isso.
- Fontes que só abrem por navegador (Reddit, Instagram, magic.wizards.com) dependem da sessão; a ausência fica registada.
- Temas de autoria envolvem pessoas reais: o piloto tem de passar pela verificação jurídica de redação (§13 da proposta).
- `STATUS.md` continua acima de 6 KB (já estava; não reduzido aqui para não colidir com outras conversas).

### H. Decisões do fundador
1. Integrar a branch `inteligencia-cultural-binder` (push + merge), e depois a da auditoria de 27/11; a seguir, acrescentar `test_inteligencia.py` ao workflow `validar`.
2. Escolher, mandar esperar ou descartar a OP-2026-W48-01 (e a frente: Lambe-lambe ou Conde).
3. Ligar a @binder_vision no vidIQ e dizer se autoriza créditos para ler os Insights por API (custo por confirmar); ou enviar os prints de domingo com tempo médio e taxa de saltos.
4. Autorizar preencher as colunas novas das linhas antigas a partir dos prints/exports originais (só onde existirem).
5. Publicar a fila (39 conteúdos) antes de abrir pautas novas: é o que dá dados ao M4.

### I. Próxima missão
**Primeira semana real do ciclo:** com a @binder_vision ligada no vidIQ, fazer o radar v2 de 2026-W49 (segunda, 30 min), avaliar 3 oportunidades, e registar a retenção dos Reels publicados nessa semana nas colunas novas. É o que transforma o desenho em aprendizagem; nada mais deve ser construído antes disso.

## Handoff

Branch local `inteligencia-cultural-binder` (2 commits: diagnóstico; fases 4–5). Sem push nem merge, por pedido do fundador; bundle em `/mnt/project-files/inteligencia-cultural-2026-11-28/`. Próximo passo: decisões do §8 H.
