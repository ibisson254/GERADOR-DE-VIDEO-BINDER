# STATUS · Estúdio BINDER

Branch principal: `main` (consolidação integrada a 31/10/2026, PR #1, aprovado pelo fundador). A branch `consolidacao-estudio` fica como histórico.
Missão "Visual Evolution & Character Excellence" (02/11/2026) integrada em `main` por PR (aprovação do fundador, 02/11, 01:27). Anterior: "Consolidação estrutural do BINDER Originals" (31/10/2026), concluída.

## Missão Master (12/11/2026) — concluída e integrada na `main`

Auditoria integral, matriz de integração, sistema de previsões do TUBO corrigido e testado, validador de integridade, memória editorial e protocolo de pré-release reconciliados — tudo na `main` (PRs #18, #19, #20; autorização de 01:32). Às 05:54 o fundador fechou os episódios («Todos episódios dê como fechados menos o tubo de segunda. Vince vault»): 12 pacotes de conteúdo integrados e CONCLUÍDOS, MC-EP06 aberto, frente Vince Vault aprovada (`nucleo/DECISOES.md`, 12/11). Relatório: `nucleo/auditorias/2026-11-12_missao_master.md` · Matriz: `2026-11-12_matriz_integracao.md`.

- **PRs** (12/11, fim da sessão): abertos só #2 (Pequeno Mestre) e #7 (TV analógica, rebaseado). #3, #9, #17 integrados reconciliados; #4, #8, #10, #11, #15, #16 integrados pelo fecho de 05:54; #18–#22 merged.
- **Sistema de previsões do TUBO** (`oraculo/previsoes/` + `oraculo/CICLO_SEMANAL.md`, origem: branch `meta-em-curto/ep07-wc32`, PR #16) integrado nesta branch com correções: `ciclo.py continuacao` agora funciona em qualquer dia e mostra **todas** as previsões abertas e as promessas ao público (antes só mostrava a janela semanal); validação reforçada (datas de conferência, coerência de estado); 15 testes automatizados em `oraculo/previsoes/test_ciclo.py`, todos a passar. Registo canónico: `oraculo/previsoes/registo.yaml` (7 previsões, todas PENDENTE).
- **Motor do Giro encontrado**: está na branch `giro/2026-11-01` (`manaburn/giro/2026-11-01/`: `processar.py`, `previa.py`, `quadros.py`, `giro.html`, `cena_giro.js`); integrado nesta branch como arquivo do episódio publicado. A pendência "enviar ou subir o motor que gerou o Giro" (abaixo) fica resolvida quando esta branch entrar na `main`.
- **Integridade**: `python3 -I comum/ferramentas/validar_repo.py` — caminhos do `series.yaml`, sintaxe Python, imports locais, vídeos versionados, links internos e segredos. Resultado a 12/11: 0 problemas (3 limitações conhecidas documentadas e aceites). Nenhum segredo versionado.

## Infraestrutura (16/11/2026, 10:48)

- **GitHub Actions** `validar` a cada push/PR (`.github/workflows/validar.yml`): integridade, memória, previsões e testes. Encerramento só conta com o visto verde.
- **Funil do app**: `comum/insights/registo_app.csv` (contas novas e carta em 7 dias, por semana, do Supabase). 37 contas desde 21/09; 6 com carta em 7 dias. Consulta e limites em `comum/insights/LEIA-ME.md`.
- **Tarefa agendada** «Briefing do TUBO» (seg e qui, 09:47 Lisboa), só leitura. Próxima: quinta 19/11.
- **Depende do fundador:** ligar a @binder_vision no vidIQ (hoje está a conta pessoal) para a rotina de domingo ler os Insights por API; decidir RLS em `public.spatial_ref_sys` no Supabase (aviso crítico do advisor; nada alterado); atualizar as skills `binder-*` (proposta feita no chat de 16/11).

## Estado editorial

Frentes ativas: Mana & Burn, Conde de Manaforte, Meta em Curto (séries); **Vince Vault (série, aprovada a 12/11, em desenvolvimento)**; Órbita (temática); Lambe-lambe (espontânea); especiais. Estados por conteúdo: `comum/REGISTRO_EDITORIAL.md` (86 conteúdos). Fecho de 12/11: MC-EP03/04/05/07, MB-ESP03, MB-EP10, MB-GIRO02, CM-EP004/005, LL-PRETRK, LL-SHEOL, LL-DIVCAR, LL-CAMPBR fechados; **MC-EP06 (episódio de segunda) aberto**. Pequeno Mestre (PR #2) em desenvolvimento, sem aprovação; o PR #17 era a direção 2D do próprio Vince Vault (integrado, reconciliado). Detalhe: `nucleo/CATALOGO_EDITORIAL.md`.

## Em produção e publicação (atualizado a 16/11/2026, 11:30)

- **Publicados:** o fundador confirmou a 16/11 (11:23) que «todos os episódios criados já foram lançados». No registo passaram a PUBLICADO: MB-GIRO02, MB-GIRO03, MB-EP10, MB-ESP03-CARR, MC-EP03, MC-EP04, MC-EP08B, ORB-07 a 10, LL-ART13, LL-PRETRK, LL-SHEOL, LL-DIVCAR, LL-CAMPBR, AB-01, e a linha nova MB-ESP04 (especial «Precon em jogo», que faltava). MC-ESP01, MC-ESP02 e MC-EP08 já estavam PUBLICADO. Datas exatas por confirmar no domingo, com os Insights.
- **EX-01 «Nauctis: Primeiro Mergulho»**: continua EM PRODUÇÃO no registo (não estava concluído: faltava escolher A ou B e a licença da «Auction of Power»). Se já saiu, o fundador diz qual versão e passa a PUBLICADO.
- **MC-EP06**: REJEITADO (fundador, 16/11 13:47: perdeu o timing do pré-release; nunca produzido).
- **Parcerias**: plano dos projetos em `comum/parcerias.md` (16/11, 17h): painel, calendário até 13/12 e três projetos — MC-ESP03 (Farpas de Mana, piloto), MC-ESP04 (Preconauta, ligas mesão × 2x2), LL-ART20 (Caio Monteiro). IDs provisórios, pautas LIVRES, nada enviado. Base: `nucleo/auditorias/2026-11-16_parcerias.md`.
- **Vince Vault (Multiverse Capital)**: direção 2D ativa (PR #17, decisões de 11–12/11; 3D arquivado). Bíblia `vince/CONTEXTO.md`, som da Fonte `vince/audio/fonte.py`. **Em falta:** o kit 2D (16 PNG), `recortar.py`, `EDICAO.md` e `PROMPT_EPISODIO.md` descritos no PR #17 não chegaram à branch — pedir à sessão de origem ou refazer com aprovação.

## Consolidação

| Bloco | Estado | Onde |
|---|---|---|
| Inventário | Concluído | `INVENTARIO.md` (histórico) |
| Integração de `especial/sir-patrick` | Concluído, sem conflitos | commit 4e6af96 |
| Núcleo e fonte de verdade | Concluído | `nucleo/`, constituição v1.4 |
| Catálogo editorial (Órbita e Lambe-lambe ativos) | Concluído | `nucleo/CATALOGO_EDITORIAL.md` |
| Hierarquia documental | Concluído | constituição §1, `nucleo/README.md` |
| Showrunner + handoff | Concluído | `nucleo/SHOWRUNNER.md`, `nucleo/modelos/HANDOFF.md` |
| Prompts Claude Project e ChatGPT | Texto pronto | `nucleo/prompts/` |
| Instruções do projeto claude.ai | Aplicadas pelo fundador (31/10) | `nucleo/prompts/CLAUDE_PROJECT.md` |
| Respostas Q1–Q3 aplicadas (nome Meta em Curto, Órbita sem fecho, Órbita e Lambe-lambe no repositório) | Concluído | `orbita/`, `lambe-lambe/`, constituição v1.4 |
| Fecho do scanner no repositório | Concluído (cortado do fim do Ep. 6, rótulo tapado) | `comum/outro/outro_binder_916.mp4`, `comum/outro/gerar_fecho.py` |
| Merge para `main` | Concluído, aprovado pelo fundador | GitHub, PR #1 |
| Prompt do ChatGPT a apontar para `main` | Concluído | `nucleo/prompts/CHATGPT.md` |

## Evolução visual (02/11/2026)

| Bloco | Estado | Onde |
|---|---|---|
| Auditoria do Giro de domingo (01/11) com timecodes, revista com a bíblia do Drive | Concluído: 0 P0, 10 P1, 4 P2, 1 decisão pendente | `nucleo/auditorias/2026-11-02_evolucao_visual.md` |
| Controlo de qualidade automático | Implementado e testado | `comum/qc/` |
| Checklist P0/P1/P2 + bloco E | Implementado | `nucleo/CHECKLIST_QUALIDADE.md` |
| Memória de continuidade por série | Implementado (semente) | `comum/continuidade/` |
| Expressões e poses novas do Mana e do Burn, regra "quem ouve reage" | Proposto | auditoria §4 |
| Cenário-mestre, planos fixos, luz da TV, grelha da TV SAL | Proposto | auditoria §5 |
| Formato "Giro de domingo" no perfil | Proposto | auditoria §7 |
| Correções no motor que gerou o Giro | Bloqueado: motor feito noutro chat | auditoria §6 |
| Kit v2 no repositório + melhorias (legenda na zona segura, fonte do medidor, ventilador, antena, paninho) | Implementado e testado (bordas OK) | `manaburn/LEIA-ME.md` |
| Duração livre nas séries | Implementado (constituição v1.5) | `nucleo/DECISOES.md` |

## Protocolo de Pré-Release do TUBO (06/11/2026)

| Bloco | Estado | Onde |
|---|---|---|
| Método (fases A–D, integridade estatística, estados, grau de certeza) | Implementado | `oraculo/PROTOCOLO_PRE_RELEASE.md` |
| Modelo de ficha por coleção | Implementado | `nucleo/modelos/PREVISOES_PRE_RELEASE.md` → `oraculo/pre-release/` |
| Ativação e router | Implementado | `oraculo/PERFIL.md`, `nucleo/SHOWRUNNER.md` §2.2 |
| Registo canónico (IDs, estados, conferências) | Implementado | `oraculo/previsoes/registo.yaml` (decisão de 09/11: o histórico remete para ele) |
| Migrar as 4 previsões do EP05 para `PR-TRK-01`–`04` | Concluído (09/11, na branch do EP07; no registo desde o PR #18) | `oraculo/previsoes/registo.yaml` |

## Memória editorial universal e insights (01/11/2026, integrado a 12/11)

| Bloco | Estado | Onde |
|---|---|---|
| Registo editorial (ID e estado por conteúdo, todas as frentes) | Implementado; **desatualizado desde 01/11** (falta registar EP04–EP07, Giro nº 2, Conde EP004–005, especiais e lambes das branches) | `comum/REGISTRO_EDITORIAL.md` |
| Auditoria de originalidade antes de cada pauta | Implementado | `python3 comum/ferramentas/memoria.py pauta --objeto "…" --tema "…"` |
| Encerramento obrigatório em 12 passos | Implementado | `nucleo/SHOWRUNNER.md` §6 |
| Insights semanais (snapshots, CSV, impulso SIM/NÃO/A CONFIRMAR) | Implementado | `comum/insights/` |
| Constituição v1.6 (§10, §12, §13) | Aplicada | `nucleo/DECISOES.md` (01/11, integrada a 12/11) |

## Depende do fundador

- Aprovar um esboço das expressões novas do Mana e do Burn (auditoria §4) antes de as desenhar no kit.
- ~~Enviar ou subir o motor que gerou o Giro~~ → encontrado na branch `giro/2026-11-01` e integrado na `main` (PR #18, 12/11).
- ~~Ep. 10, frentes novas e pacotes de conteúdo~~ → resolvido a 12/11 (05:54): MB-EP10 = «A febre do autógrafo»; Vince Vault aprovada; pacotes integrados. Continuam com o fundador: Pequeno Mestre (PR #2); PR #7 (TV analógica, rebaseado para `main`); publicações por confirmar; fontes de preço do Vince (decisão de 08/11 sem Cardmarket × corpo do PR #17 com Cardmarket — qual vale?); kit 2D do Vince em falta (refazer ou recuperar).
- ~~Protocolo de Pré-Release: aprovar o PR e decidir o «~35%»~~ → integrado a 12/11 («Escolha as melhores opções e pode prosseguir»); o «~35%» já tinha saído conforme a decisão de 06/11 (aplicado em `oraculo/previsoes/registo.yaml`).
- Memória editorial (`comum/REGISTRO_EDITORIAL.md`): confirmar as lacunas do fim do registo (30 linhas `POR AUDITAR`) e dizer quais dois vídeos levaram os R$ 11 de impulsionamento de 26/10 (e se o valor é total ou por vídeo).
- Drive atualizado a 02/11 (notas de fonte de verdade na bíblia, no doc 05 e no Mapa do Drive; secção de estado na bíblia).

## Pendências técnicas (não bloqueiam a governação)

- Motor v2 do Mana & Burn: núcleo no repositório desde 02/11 (`manaburn/`, v1 em `manaburn/extras/v1/`); ficaram no projeto claude.ai `montar.py`, `scryfall.py`, `lote.py`, `testes.py`, `formatos.*` e episódios 1, 5–7. O motor do Giro nº 1 está em `manaburn/giro/2026-11-01/` desde o PR #18.
- Gerador do Órbita já no repositório (`orbita/gerador/`); para renderizar faltam os PNGs das cartas (`BINDER_gerador_orbita.zip`) e as fontes em `node_modules/`.
- `oraculo/episodios/ep01_render_v2.py` importa `render`, que não existe; `conde/montar_ep002.py` tem caminho absoluto. Não se mexe em scripts de episódios publicados sem necessidade.
- Skills `binder-*` ainda mandam ler primeiro o Drive e dizem que o Scryfall não abre; alinhar com o repositório quando o fundador quiser.

## Especial «Precon em jogo» (MB-ESP04)

Publicado (fundador, 16/11). Linha criada no registo a 16/11.

## Especial "Precon em jogo" · V2 para impulsionamento (03/11/2026)

Branch `especial/precon-em-jogo-v2` (a partir de `especial/precon-em-jogo`). V2 com luz e profundidade em pós-produção (`especiais/precon_em_jogo/polimento_v2.py`), áudio idêntico, QC sem problemas (`qc_v2.md`). Bloqueado: objetos novos e reenquadramento (faltam vozes, `data.js` e quadros do TUBO deste especial no repositório). Aguarda aprovação do fundador.

## Sala v3 do Mana & Burn (08/11/2026)

Aprovada e aplicada no `manaburn/index.html`: mesa de Commander, mesa acima das legendas, taco, luz no cenário (`luz.py` passa a opcional). `bordas.py` OK com o Ep. 2 (laterais 10–1068 px, topo 300 px). Burn no plano da TV corrigido (cabelo, camisa e ombros; 08/11, 00:05). Pendente: primeiro episódio completo com a sala v3.

## Luz padrão do Mana & Burn (07/11/2026)

Aprovada pelo fundador (`nucleo/DECISOES.md`). Fase 1 implementada e integrada na `main` (07/11, "Prossiga" do fundador): `manaburn/luz.py` + `render.py` (por defeito), docs e checklist. Por aprovar: fase 2 (luz no `index.html`); objetos novos e planos fixos. Especial "Precon em jogo" e V2 integrados na `main` no mesmo merge.

## Meta em Curto · ciclo semanal e EP06 (09/11/2026)

Integrado na `main` a 12/11 (ciclo e registo pelo PR #18; roteiro do EP06 pelo fecho de 05:54). Novo ciclo «quinta prevê, segunda presta contas» (`oraculo/CICLO_SEMANAL.md`, registo `oraculo/previsoes/registo.yaml`, briefing `oraculo/previsoes/ciclo.py`). EP06 «Prestação de contas: placar zero» escrito (roteiro, storyboard, legenda, comentário, alt, fontes); depende do fundador: autorizar a voz (~2.200 créditos, 2 tomadas) e publicar até terça 10/11 (depois disso o «zero jogos» muda). Próximos: quinta 12/11 `tubo quinta` (Worlds 32, 13–15/11); segunda 16/11 placar parcial de PR-TRK-01..03.

Atualização de 10/11/2026: regra geral no `oraculo/CICLO_SEMANAL.md` §0 (toda previsão do TUBO vai ao registo; toda produção começa por `ciclo.py continuacao`). Conferência de 10/11 registada em PR-TRK-01 e 03 (PENDENTE, sem ranking no 17Lands). EP06: «zero jogos» venceu hoje; ajustes na ficha (secção de 10/11). Depende do fundador: aprovar o gancho revisto e autorizar a voz do EP06 — ou deixar que a prestação de contas de segunda 16/11 o substitua.

## Meta em Curto EP07 · Mundial 32 (10/11/2026)

Integrado na `main` e CONCLUÍDO a 12/11 (05:54). Produzido, publicação por confirmar: 57,4 s + fecho, QC sem problemas, −14,0 LUFS, sem corte lateral. Ficha `oraculo/episodios/ep07_mundial_ficha.md`, legenda `oraculo/legendas/ep07_mundial_legenda.txt`. Previsões PR-WC32-01 (pública) a 03 registadas antes da voz; conferência na segunda 16/11 (`ciclo.py segunda`). O vídeo não está no repositório: recria-se com `ep07_audio.py` + `ep07_render.py` a partir de `voz.mp3` (flow ElevenLabs em `ep07_mundial_fontes.txt`). v2 (17h): listas de Landfall e das duas campeãs de Jund no ecrã; 5 fotos dos brasileiros no ecrã (17:30); falta a de João Jorge Sales Junior. Depende do fundador: foto do Sales Junior (opcional), ouvir a pronúncia e publicar (de preferência antes de 13/11, dia 1 do Mundial).

## Próximo passo concreto

1. Fundador: EX-01 (saiu? versão?), ligar a @binder_vision no vidIQ; parcerias pela ordem de `comum/parcerias.md`: fechos Q1–Q4 (roteiro ao Preconauta, agradecimentos, foto da Nathanna no LL-ART13 publicado), depois DM ao Farpas; prints das ligas Preconauta para o MC-ESP04.
2. Domingo 22/11: rotina de insights com as datas de publicação dos conteúdos fechados a 16/11 e as métricas do MC-ESP01/ESP02 (termo de comparação das parcerias).
3. Quinta 19/11: briefing automático do TUBO (tarefa agendada).

## Handoff

Último: 16/11/2026, no fim de `nucleo/auditorias/2026-11-16_parcerias.md` (mais a adenda das 11:30). Anterior: 12/11, em `nucleo/auditorias/2026-11-12_missao_master.md`.
