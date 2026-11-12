# STATUS · Estúdio BINDER

Branch principal: `main` (consolidação integrada a 31/10/2026, PR #1, aprovado pelo fundador). A branch `consolidacao-estudio` fica como histórico.
Missão "Visual Evolution & Character Excellence" (02/11/2026) integrada em `main` por PR (aprovação do fundador, 02/11, 01:27). Anterior: "Consolidação estrutural do BINDER Originals" (31/10/2026), concluída.

## Missão Master (12/11/2026) · branch `consolidacao/2026-11-12-missao-master`

Auditoria integral do repositório, matriz de integração de todas as branches e PRs, sistema de previsões do TUBO corrigido e testado, ferramenta de integridade do repositório. **Nada entrou na `main`: aguarda aprovação do fundador.** Relatório: `nucleo/auditorias/2026-11-12_missao_master.md` · Matriz: `nucleo/auditorias/2026-11-12_matriz_integracao.md`.

- **Estado real dos PRs** (12/11): abertos #2, #3, #4, #7, #8, #9, #10, #11, #15, #16, #17 (a missão citava só 6). 36 branches; ~20 alteram os mesmos ficheiros de registo (STATUS, histórico, continuidade) → integração de conteúdos tem de ser sequencial.
- **Sistema de previsões do TUBO** (`oraculo/previsoes/` + `oraculo/CICLO_SEMANAL.md`, origem: branch `meta-em-curto/ep07-wc32`, PR #16) integrado nesta branch com correções: `ciclo.py continuacao` agora funciona em qualquer dia e mostra **todas** as previsões abertas e as promessas ao público (antes só mostrava a janela semanal); validação reforçada (datas de conferência, coerência de estado); 15 testes automatizados em `oraculo/previsoes/test_ciclo.py`, todos a passar. Registo canónico: `oraculo/previsoes/registo.yaml` (7 previsões, todas PENDENTE).
- **Motor do Giro encontrado**: está na branch `giro/2026-11-01` (`manaburn/giro/2026-11-01/`: `processar.py`, `previa.py`, `quadros.py`, `giro.html`, `cena_giro.js`); integrado nesta branch como arquivo do episódio publicado. A pendência "enviar ou subir o motor que gerou o Giro" (abaixo) fica resolvida quando esta branch entrar na `main`.
- **Integridade**: `python3 -I comum/ferramentas/validar_repo.py` — caminhos do `series.yaml`, sintaxe Python, imports locais, vídeos versionados, links internos e segredos. Resultado a 12/11: 0 problemas (3 limitações conhecidas documentadas e aceites). Nenhum segredo versionado.

## Memória editorial e insights (01/11/2026, branch `feature/memoria-editorial-insights`, PR #3 para `main` à espera de aprovação)

| Bloco | Estado | Onde |
|---|---|---|
| Registo editorial universal | Criado; 72 conteúdos migrados; **inventário incompleto** (30 `POR AUDITAR`) | `comum/REGISTRO_EDITORIAL.md` |
| Auditoria de originalidade | Ativa (script + regra) | `SHOWRUNNER.md` §2.3, `comum/ferramentas/memoria.py pauta` |
| Encerramento obrigatório | Ativo | `SHOWRUNNER.md` §6, `modelos/FICHA_EPISODIO.md`, `memoria.py encerramento` |
| Insights semanais | Ativo; snapshots de 21/10 e 26/10 migrados; outubro (1–31/10) registado a 01/11 | `comum/insights/` |
| Testes A–F | 17 testes OK | `python3 -m unittest comum/ferramentas/test_memoria.py` |

## Estado editorial

Giro de domingo de 01/11 publicado (registado em `comum/historico.md`, 02/11). Frentes ativas: Mana & Burn, Conde de Manaforte, Meta em Curto (séries); Órbita (temática); Lambe-lambe (espontânea); especiais. Tudo o que está no repositório está aprovado e lançado; Halloween 2026 e Star Trek publicados. Detalhe: `nucleo/CATALOGO_EDITORIAL.md`.

## Em produção

Lambe-lambe · chamada do pré-release de Star Trek (branch `producao/lambe-pre-release-star-trek`): vídeo v2 renderizado (68 impressões de cartas), **PRÉVIA — DIREITOS A CONFIRMAR**, não publicado, 5 P1 por decidir. Ver `lambe-lambe/publicacoes/2026-11-pre-release-star-trek/relatorio_qc.md` e `HANDOFF.md`.

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

- Meta em Curto EP04 produzido e conferido (branch `meta-em-curto-ep04`): falta o fundador publicar, com `oraculo/legendas/ep04_jund_pequim_legenda.txt`; merge do PR depois do EP03 (PR #4).

- Aprovar um esboço das expressões novas do Mana e do Burn (auditoria §4) antes de as desenhar no kit.
- ~~Enviar ou subir o motor que gerou o Giro~~ → encontrado na branch `giro/2026-11-01` e integrado na `main` (PR #18, 12/11).
- Decisões que continuam com o fundador (secção F de `nucleo/auditorias/2026-11-12_missao_master.md`): qual das 4 branches é o Ep. 10 do Mana & Burn; frentes novas (Pequeno Mestre, Vince Vault, Vinci); merge dos pacotes de conteúdo (EP03–EP07, Giro nº 2, Conde EP005, especiais, lambes).
- ~~Protocolo de Pré-Release: aprovar o PR e decidir o «~35%»~~ → integrado a 12/11 («Escolha as melhores opções e pode prosseguir»); o «~35%» já tinha saído conforme a decisão de 06/11 (aplicado em `oraculo/previsoes/registo.yaml`).
- Memória editorial (`comum/REGISTRO_EDITORIAL.md`): confirmar as lacunas do fim do registo (30 linhas `POR AUDITAR`) e dizer quais dois vídeos levaram os R$ 11 de impulsionamento de 26/10 (e se o valor é total ou por vídeo).
- Drive atualizado a 02/11 (notas de fonte de verdade na bíblia, no doc 05 e no Mapa do Drive; secção de estado na bíblia).

## Pendências técnicas (não bloqueiam a governação)

- Motor v2 do Mana & Burn: núcleo no repositório desde 02/11 (`manaburn/`, v1 em `manaburn/extras/v1/`); ficaram no projeto claude.ai `montar.py`, `scryfall.py`, `lote.py`, `testes.py`, `formatos.*` e episódios 1, 5–7. O motor do Giro foi feito noutro chat e não está disponível.
- Gerador do Órbita já no repositório (`orbita/gerador/`); para renderizar faltam os PNGs das cartas (`BINDER_gerador_orbita.zip`) e as fontes em `node_modules/`.
- `oraculo/episodios/ep01_render_v2.py` importa `render`, que não existe; `conde/montar_ep002.py` tem caminho absoluto. Não se mexe em scripts de episódios publicados sem necessidade.
- Skills `binder-*` ainda mandam ler primeiro o Drive e dizem que o Scryfall não abre; alinhar com o repositório quando o fundador quiser.

## Especial em espera de publicação

`especiais/precon_em_jogo/`: vídeo final conferido (02/11), publicação prevista a 04/11/2026. Depende do fundador: ouvir, avisar @diegoalencard e publicar.

## Especial "Precon em jogo" · V2 para impulsionamento (03/11/2026)

Branch `especial/precon-em-jogo-v2` (a partir de `especial/precon-em-jogo`). V2 com luz e profundidade em pós-produção (`especiais/precon_em_jogo/polimento_v2.py`), áudio idêntico, QC sem problemas (`qc_v2.md`). Bloqueado: objetos novos e reenquadramento (faltam vozes, `data.js` e quadros do TUBO deste especial no repositório). Aguarda aprovação do fundador.

## Sala v3 do Mana & Burn (08/11/2026)

Aprovada e aplicada no `manaburn/index.html`: mesa de Commander, mesa acima das legendas, taco, luz no cenário (`luz.py` passa a opcional). `bordas.py` OK com o Ep. 2 (laterais 10–1068 px, topo 300 px). Burn no plano da TV corrigido (cabelo, camisa e ombros; 08/11, 00:05). Pendente: primeiro episódio completo com a sala v3.

## Luz padrão do Mana & Burn (07/11/2026)

Aprovada pelo fundador (`nucleo/DECISOES.md`). Fase 1 implementada e integrada na `main` (07/11, "Prossiga" do fundador): `manaburn/luz.py` + `render.py` (por defeito), docs e checklist. Por aprovar: fase 2 (luz no `index.html`); objetos novos e planos fixos. Especial "Precon em jogo" e V2 integrados na `main` no mesmo merge.

## Próximo passo concreto

Conde Ep. 004 (Joven) produzido a 03/11/2026 e por publicar: o fundador ouve a pronúncia de "Joven", "Chandler" e "Eron" e publica o pacote (`conde/legendas/ep004_joven_legenda.txt`, ficha em `conde/episodios/ep004_joven_ficha.md`; o vídeo não está no repositório, recria-se com `python3 conde/montar_ep004.py`, desde que `conde/ep004/audio/narracao.wav` exista: se faltar, ver o flow ElevenLabs em `conde/episodios/ep004_fontes.txt`). **Segunda 16/11 é prestação de contas obrigatória do TUBO** (`python3 -I oraculo/previsoes/ciclo.py segunda`): prazo das PR-WC32-01..03 e conferência das PR-TRK-01..03, com o Mundial 32 a acabar a 15/11.

## Handoff

Ver o handoff de 12/11/2026 no fim de `nucleo/auditorias/2026-11-12_missao_master.md`.
