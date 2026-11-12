# Missão Master · Relatório final (12/11/2026)

Branch de trabalho: `consolidacao/2026-11-12-missao-master` (a partir de `main`, commit `3fee799`). Nada foi merged para `main`. Matriz de integração completa: `2026-11-12_matriz_integracao.md` (mesma pasta).

## A. Diagnóstico

| # | Gravidade | Problema | Evidência |
|---|---|---|---|
| 1 | P0 (governação) | `STATUS.md` desatualizado: dizia que o motor do Giro "não está disponível" — **está na branch `giro/2026-11-01`** — e não refletia os 11 PRs abertos nem as 36 branches | `git show origin/giro/2026-11-01:manaburn/giro/2026-11-01/processar.py`; API do GitHub |
| 2 | P0 (continuidade) | O comando de continuação do TUBO (`ciclo.py continuacao`) era um alias de `segunda`: só mostrava previsões com prazo vencido ou conferência na janela semanal. Previsões abertas de prazo longo desapareciam do briefing em dias arbitrários — exatamente o risco que a missão proíbe | `ciclo.py` na branch `meta-em-curto/ep06-ciclo-semanal`, linha `elif cmd in ("continuacao", "abertas")` |
| 3 | P1 | O sistema de previsões (registo canónico, ciclo, calendário) vivia só em branches abertas (PR #16 e `ep07-wc32`), fora da `main`: uma sessão nova clonando a `main` não via o que o TUBO prometeu ao público | matriz §2.2 |
| 4 | P1 | ~20 branches alteram os mesmos ficheiros de registo (`STATUS.md`, `comum/historico.md`, `comum/continuidade/*`, `nucleo/DECISOES.md`): merge em bloco geraria conflitos e perda de registo | matriz §4 |
| 5 | P1 | Quatro branches candidatas ao Ep. 10 do Mana & Burn (`ep10-97-terrenos`, `ep10-numot`, `ep10-olag`, `ep10-cartas-especiais`), mutuamente exclusivas; `ep10-97-terrenos` ainda reestrutura o kit (`manaburn/kit/v3/`, raiz movida) | matriz §2.1 e §5 |
| 6 | P1 | PR #3 (memória editorial) escrito antes da evolução visual: sobrepõe-se a `comum/continuidade/` (já na `main`) e altera constituição/AGENTS/SHOWRUNNER; 20 commits atrás | matriz §4 |
| 7 | P1 | PR #7 com base numa branch já merged (`especial/precon-em-jogo`): desatualizado | API GitHub |
| 8 | P2 | `ciclo.py` rebentava (KeyError) ao listar um registo malformado; `validar` não verificava datas de conferência nem coerência estado × conferências | código original |
| 9 | P2 | Imports locais em falta: `oraculo/episodios/ep01_render_v2.py` (`render`), `manaburn/episodios/ep09_dack/process.py` (`trilha`, `roteiro`, `cortes`) — motores ficaram no projeto claude.ai; e caminho absoluto em `conde/montar_ep002.py`. Episódios publicados: **não se tocam**, ficam documentados como aceites | varrimento AST; `STATUS.md` já os registava em parte |
| 10 | P2 | Duplicação binária: `manaburn/musica.mp3` ≡ `manaburn/musica/musica.mp3` (4,2 MB cada). Scripts publicados referem a raiz (`processar.py` do Giro usa `../../musica.mp3`) — não remover sem autorização | `du` + `git ls-files` |
| 11 | OK | Segurança: nenhum segredo, token ou chave versionado; único vídeo versionado é a exceção documentada do fecho | `validar_repo.py` secção F |

## B. Melhorias implementadas (nesta branch)

| Ficheiro | Alteração | Justificação |
|---|---|---|
| `nucleo/auditorias/2026-11-12_matriz_integracao.md` | Novo: matriz de integração (6 categorias da missão) | 1ª frente |
| `oraculo/previsoes/` + `oraculo/CICLO_SEMANAL.md` | Integrados de `meta-em-curto/ep07-wc32` (PR #16), origem identificada | 3ª frente: o registo canónico tem de estar acessível; metodologia preservada sem alterações |
| `oraculo/previsoes/ciclo.py` | `continuacao` verdadeiro: todas as abertas em qualquer dia, agrupadas (vencidas / conferência ≤ 7 dias / restantes), promessas públicas destacadas, última e próxima conferência, fechadas como histórico; `linha()` tolerante a registo malformado; `validar` reforçado (datas de conferência ≥ registo, coerência estado × última conferência que muda estado) | Exigência explícita da missão (§6); nenhuma previsão desaparece |
| `oraculo/previsoes/test_ciclo.py` | Novo: 15 testes (registo real + registos sintéticos em pasta temporária) | "Testa os comandos e cria testes automatizados" |
| `comum/ferramentas/validar_repo.py` | Novo: integridade do repositório (series.yaml, sintaxe, imports, vídeos, links internos, segredos), com lista de aceites documentados | 6ª e 8ª frentes |
| `manaburn/giro/2026-11-01/` | Integrado de `giro/2026-11-01`: motor + pacote do Giro nº 1 (publicado 01/11); só ficheiros novos, conteúdo publicado intocado | Resolve a pendência "motor do Giro"; arquivo, não reabertura |
| `STATUS.md` | Secção da missão; correção do motor do Giro; estado real dos PRs; decisões pendentes do fundador | 9ª frente: documentação reflete a realidade |

Não alterado (deliberadamente): conteúdos publicados/aprovados, scripts de episódios publicados (mesmo com imports quebrados — documentados como aceites), bíblias, perfis, identidades, `series.yaml`, constituição, vozes, músicas, `comum/qc/qc_video.py` (auditado: base sólida; melhorias propostas na secção D).

## C. Testes

| Comando | Resultado |
|---|---|
| `python3 -I oraculo/previsoes/ciclo.py validar` | OK · 7 previsões válidas |
| `python3 -I oraculo/previsoes/test_ciclo.py` | 15/15 OK (continuação em qualquer dia lista as 7 abertas; promessas públicas destacadas; `segunda`/`quinta` intactos; registo malformado acusado sem crash; fechadas visíveis como histórico) |
| `python3 -I comum/ferramentas/validar_repo.py` | 0 problemas, 3 aceites documentados |
| Varrimento AST de todos os `.py` da `main` | 0 erros de sintaxe |
| **Não executado**: renders de vídeo (Playwright/ffmpeg sobre kits), QC de vídeos publicados | Gastaria recursos sem necessidade e a regra proíbe testar sobre vídeos publicados; os motores não foram alterados |

## D. Melhorias adicionais descobertas (fora da missão ou deixadas pendentes)

1. **Motor do Giro encontrado** na branch `giro/2026-11-01` — a maior surpresa da auditoria; o STATUS dava-o como perdido noutro chat.
2. **QC (`comum/qc/qc_video.py`)**: base sólida (formato, loudness, pico, fecho, cortes, folha de contacto). Propostas P2, não implementadas por tocarem em critérios: (a) QC próprio para imagens estáticas e carrosséis 4:5 (hoje não existe — Lambe-lambe posts e carrosséis saem sem verificação automática); (b) a zona segura é aproximada — confirmar com reclamações reais antes de apertar; (c) o perfil `lambe` no QC assume 9:16, mas o formato principal do Lambe-lambe é post 4:5 (sem vídeo não há QC — reforça a proposta (a)).
3. **PR #3**: o conceito de registo editorial universal (IDs MB-/MC-/CM-, estados, anti-duplicação via `memoria.py`) continua a ser a melhor resposta à 7ª frente (insights/métricas) e à anti-duplicação; precisa de rebase e de remover o que a `main` entretanto resolveu. Recomendação técnica: reconciliar, não descartar.
4. **Duplicação `manaburn/musica.mp3`**: consolidar num único caminho exigiria tocar em scripts de episódios publicados → fica como está, documentado (A.10).
5. **Skills `binder-*`** ainda mandam ler primeiro o Drive (pendência já registada no STATUS; alinhamento depende do fundador).

## E. Estado das branches e PRs

- **Analisado**: as 36 branches e os 17 PRs (matriz §0–§6).
- **Integrado só nesta branch de trabalho**: sistema de previsões do TUBO (de `ep07-wc32`), motor/pacote do Giro nº 1 (de `giro/2026-11-01`).
- **Aguarda aprovação**: todos os pacotes de conteúdo (EP03–EP07, Giro nº 2/PR #15, Conde EP005, especiais #10, lambes #8, campanha), PR #3, PR #9, frentes novas (#2, #11, #17), este próprio merge.
- **Não tocado**: branches merged (histórico), as 4 branches ep10, `tv-analogica-binder` (#7), `manaburn/esboco-sala`, todas as branches de frentes novas.

## F. Decisões do fundador

1. **Merge desta branch (`consolidacao/2026-11-12-missao-master`) para `main`.** Recomendação: aprovar — traz o registo de previsões, os testes, o validador e o motor do Giro para a fonte de verdade; não muda identidade nem conteúdo publicado. Impacto de adiar: sessões novas continuam sem ver as 7 previsões abertas do TUBO.
2. **Qual é o Ep. 10 do Mana & Burn** (4 candidatos; matriz §5.1). Recomendação técnica: nenhuma — é editorial; mas decidir também o destino de `manaburn/kit/v3/` (em `ep10-97-terrenos`), que muda a estrutura do kit.
3. **Ordem de integração dos pacotes de conteúdo** (recomendação: cronológica — EP03 → EP04 → EP05+carrossel → EP06/EP07 → Giro nº 2 → Conde EP005 → especiais/lambes — um de cada vez, pela sobreposição nos ficheiros de registo).
4. **PR #3**: mandar reconciliar (recomendado) ou fechar.
5. **PR #9** (protocolo pré-release do TUBO): integrar a seguir ao sistema de previsões (recomendado — o `CICLO_SEMANAL.md` já o referencia).
6. **Frentes novas** (Pequeno Mestre #2, Vince Vault #11, Vinci #17): aprovar, manter em desenvolvimento ou arquivar. Nota: Vince Vault tem duas branches divergentes (`vince-vault` com pasta `vince/`, `proposta/vince-vault` com pasta `vince-vault/`) — escolher uma.
7. **PR #7**: autorizar o rebase para `main` (a base atual já foi merged).

## G. Próximo passo

Fundador decide F.1 (merge da consolidação). Com o merge feito, a próxima sessão de produção do TUBO começa por `python3 -I oraculo/previsoes/ciclo.py continuacao` — as PR-WC32-01..03 têm prazo 16/11, as PR-TRK-01..03 têm conferência marcada a 16/11, e o Mundial 32 acaba a 15/11: **a segunda-feira 16/11 é uma prestação de contas obrigatória.**

## H. Handoff

```
HANDOFF · 12/11/2026, ~02h Lisboa · Claude
Repositório: ibisson254/GERADOR-DE-VIDEO-BINDER · branch main (PRs #18, #19 e reconciliação do #3 integrados) · último commit: ver git log

Objetivo atual: Missão Master concluída — consolidação, previsões do TUBO, protocolo pré-release, memória editorial e validador na main.

Decisões tomadas nesta sessão:
- Merges dos PRs #18, #19 e do PR #3 reconciliado; PR #7 rebaseado para main (registado em nucleo/DECISOES.md, 12/11: sim — autorização «Escolha as melhores opções e pode prosseguir»)

Documentos consultados: AGENTS, STATUS, constituição, catálogo, SHOWRUNNER, DECISOES, historico, continuidade, series.yaml, qc_video.py, as 36 branches e 17 PRs.

Alterações realizadas: ver secções B e o adendo acima; tudo na main via PRs #18 e #19 e o merge da reconciliação do #3.

Tarefas pendentes:
- Ep. 10 do Mana & Burn (4 candidatos) · fundador
- Frentes novas: Pequeno Mestre (#2), Vince Vault (#11, duas branches divergentes), Vinci (#17) · fundador
- Merge dos pacotes de conteúdo, por ordem cronológica, um de cada vez (EP03 → EP04 → EP05+carrossel → EP06/EP07 → Giro nº 2 → Conde EP005 → especiais/lambes) · fundador aprova, agente executa
- Atualizar comum/REGISTRO_EDITORIAL.md com os conteúdos pós-01/11 · agente, na próxima sessão
- 30 linhas POR AUDITAR do registo + quais dois vídeos levaram os R$ 11 · fundador

Próximo passo concreto: segunda 16/11, prestação de contas do TUBO:
python3 -I oraculo/previsoes/ciclo.py segunda
(prazo das PR-WC32-01..03 e conferência das PR-TRK-01..03; Mundial 32 acaba a 15/11)
```


---

## Adendo · 2ª fase (12/11/2026, 01:32): «Escolha as melhores opções e pode prosseguir»

Com a autorização do fundador sobre a secção F, foram executadas as recomendações:

| Decisão | Execução |
|---|---|
| F.1 Merge da consolidação | **Feito** — PR #18 merged na `main` |
| F.5 PR #9 (protocolo pré-release) | **Feito** — PR #19 (reconciliado: registo canónico em `oraculo/previsoes/registo.yaml`, histórico só com remissão, decisões de 06/11, 09/11 e 10/11 em `DECISOES.md`); PR #9 fechado como integrado |
| F.4 PR #3 (memória editorial) | **Feito** — reconciliado e integrado (branch `reconciliacao/pr3-memoria-editorial`): constituição **v1.6** (§10 registo editorial + encerramento, §12 insights, §13), `comum/REGISTRO_EDITORIAL.md`, `memoria.py` (17 testes OK), `comum/insights/`, SHOWRUNNER §2.3 e §6, AGENTS atualizado (inclui as linhas `tubo segunda`/`tubo quinta` das decisões de 09–10/11). Pendência nova: o registo editorial está desatualizado desde 01/11 (conteúdos das branches por registar) |
| F.7 PR #7 | Base mudada para `main` |
| F.2 Ep. 10 (4 candidatos) · F.6 frentes novas · F.3 merges de conteúdo | **Não executado — continuam com o fundador** (editorial/identitário; a autorização genérica não substitui estas escolhas) |

Testes da 2ª fase: `memoria.py validar` OK (72 conteúdos, 30 POR AUDITAR) · `test_memoria.py` 17/17 · `test_ciclo.py` 15/15 · `validar_repo.py` 0 problemas.
