# Matriz de integração · Missão Master (12/11/2026)

Auditoria de todas as branches e PRs do repositório contra a `main` (commit `3fee799`, merge do PR #14). Fonte: `git` + API do GitHub a 12/11/2026. Nada foi merged para `main` nesta missão; a branch de trabalho é `consolidacao/2026-11-12-missao-master`.

## 0. Estado real dos PRs (confere com a missão)

| PR | Branch | Estado | Conteúdo |
|---|---|---|---|
| #1 | `consolidacao-estudio` | **MERGED** | Consolidação (31/10) |
| #2 | `pequeno-mestre/kit-v1` | ABERTO | Frente nova Pequeno Mestre (em desenvolvimento) |
| #3 | `feature/memoria-editorial-insights` | ABERTO | Registo editorial universal + insights + `memoria.py` |
| #4 | `meta-em-curto-ep03` | ABERTO | Meta em Curto EP03 |
| #5 | `evolucao-visual-2026-11` | **MERGED** | Evolução visual (02/11) |
| #6 | `especial/precon-em-jogo` | **MERGED** | Especial Precon em jogo |
| #7 | `tv-analogica-binder` | ABERTO (base: `especial/precon-em-jogo`) | TV analógica BINDER; base já merged — PR desatualizado |
| #8 | `producao/lambe-pre-release-star-trek` | ABERTO | Lambe pré-release Star Trek (PRÉVIA) |
| #9 | `protocolo-pre-release-tubo` | ABERTO | Protocolo de pré-release do TUBO |
| #10 | `especial-startrek-prerelease` | ABERTO | Especial Star Trek do Mana & Burn |
| #11 | `vince-vault` | ABERTO | Vince Vault (frente **não aprovada**) |
| #12–#14 | luz-padrao, sala-v3, burn-plano-tv | **MERGED** | Mana & Burn (07–08/11) |
| #15 | `giro/2026-11-08` | ABERTO | Giro de domingo nº 2 |
| #16 | `meta-em-curto/ep06-ciclo-semanal` | ABERTO | Registo de previsões + ciclo semanal + EP06 |
| #17 | `vinci/kit-v1` | ABERTO | Frente nova Vinci (em desenvolvimento) |

A missão citava #3, #9, #10, #11, #15 e #16 como abertos; **além desses estão abertos #2, #4, #7, #8 e #17**. O `STATUS.md` da `main` não refletia este estado.

## 1. O que já está na `main`

Consolidação (PR #1), evolução visual + QC + continuidade (PR #5), especial Precon em jogo e V2 (PR #6 + #12), luz padrão, sala v3, Burn no plano da TV (PR #12–#14). Branches correspondentes (`consolidacao-estudio`, `evolucao-visual-2026-11`, `especial/precon-em-jogo*`, `especial/sir-patrick`, `manaburn/luz-padrao`, `manaburn/sala-v3`, `manaburn/burn-plano-tv`) estão a 0 commits à frente: são histórico, nada a integrar.

## 2. O que está apenas em branches (não chegou à `main`)

### 2.1 Episódios e conteúdos produzidos (1 branch = 1 pacote de conteúdo)

| Branch | Conteúdo | Observação |
|---|---|---|
| `meta-em-curto-ep03` (PR #4) | EP03 Arquivo Competitivo | 20 commits atrás da main |
| `meta-em-curto-ep04` | EP04 Jund Pequim | sem PR |
| `meta-em-curto-ep05` / `carrossel-ep05` | EP05 Star Trek + carrossel | `carrossel-ep05` contém o EP05 + carrossel |
| `meta-em-curto/ep06-ciclo-semanal` (PR #16) | EP06 + **sistema de previsões** | ver 2.2 |
| `meta-em-curto/ep07-wc32` | EP07 Mundial 32 + fotos autorizadas | superconjunto do EP06 (inclui PR #16) |
| `giro/2026-11-01` | Kit do Giro nº 1 (publicado a 01/11) | o motor do Giro que o STATUS dava como indisponível **está nesta branch** |
| `giro/2026-11-08` (PR #15) | Giro nº 2 + índice semanal | altera `manaburn/index.html` |
| `manaburn/ep10-97-terrenos` · `ep10-numot` · `ep10-olag` · `ep10-cartas-especiais` | **Quatro candidatos a Ep. 10** | qual é o Ep. 10 real é decisão editorial |
| `conde/ep005-lemure` | Conde EP005 | |
| `especial-startrek-prerelease` (PR #10) | Especial "BURN FOI ASSIMILADO!" | |
| `producao/lambe-pre-release-star-trek` (PR #8) | Lambe pré-release (PRÉVIA) | |
| `lambe/nem-saiu-sheoldred` · `lambe/carrossel-divulgacao` · `campanha/aquisicao-br-carrossel` | Peças Lambe-lambe / campanha | |
| `tv-analogica-binder` (PR #7) | TV analógica no especial + kit | base merged; precisa rebase |
| `manaburn/esboco-sala` | Esboço da sala (parte já aplicada via PR #13) | conferir o que resta |

### 2.2 Infraestrutura e governação

| Branch | O que traz | Estado |
|---|---|---|
| `meta-em-curto/ep06-ciclo-semanal` + `ep07-wc32` | `oraculo/previsoes/{registo,calendario}.yaml`, `ciclo.py`, `oraculo/CICLO_SEMANAL.md` | **Integrado nesta branch de consolidação** (3ª frente da missão), com correções e testes; origem identificada nos cabeçalhos |
| `protocolo-pre-release-tubo` (PR #9) | `oraculo/PROTOCOLO_PRE_RELEASE.md` + modelo | Metodologia; altera CONTEXTO/PERFIL/constituição → reconciliação |
| `feature/memoria-editorial-insights` (PR #3) | `comum/REGISTRO_EDITORIAL.md`, `memoria.py`, `comum/insights/` | Sobrepõe-se em parte a `comum/continuidade/` (já na main); altera constituição, AGENTS, SHOWRUNNER → reconciliação + fundador |

### 2.3 Frentes novas (não aprovadas)

`pequeno-mestre/kit-v1` + `ep01` (PR #2), `vince-vault` + `proposta/vince-vault` (PR #11), `vinci/kit-v1` (PR #17). **Ficam separadas** até decisão do fundador (catálogo: frente nova exige decisão registada). Nota: `vince-vault` e `proposta/vince-vault` são duas versões da mesma frente (pasta `vince/` vs `vince-vault/`) — ao aprovar, escolher uma.

## 3. O que pode ser integrado sem conflito (e foi, nesta branch)

- Sistema de previsões do TUBO (ficheiros novos de `meta-em-curto/ep07-wc32`: `oraculo/previsoes/`, `oraculo/CICLO_SEMANAL.md`) — não toca em nada da `main`; corrigido e testado aqui (ver `nucleo/auditorias/2026-11-12_missao_master.md`).
- Ferramenta de validação do repositório (`comum/ferramentas/validar_repo.py`) — nova.
- Esta matriz e o relatório da missão (`nucleo/auditorias/`).
- `STATUS.md` atualizado ao estado real.

## 4. O que necessita de reconciliação (não integrado)

- **PR #3 × `comum/continuidade/`**: o PR foi escrito antes da evolução visual; a main já tem memória por série. O registo editorial universal (IDs, estados, anti-duplicação) continua útil e não existe na main. Reconciliar: manter `comum/continuidade/` como memória narrativa, adotar `REGISTRO_EDITORIAL.md` + `memoria.py` como inventário de estados, remover do PR as alterações à constituição que a main entretanto resolveu de outra forma. 20 commits atrás; rebase obrigatório.
- **PR #9 × PR #16**: o `CICLO_SEMANAL.md` (PR #16) já referencia o protocolo (PR #9); ambos alteram `oraculo/CONTEXTO.md`/`PERFIL.md` e docs do núcleo. Integrar o #9 logo a seguir ao #16, resolvendo os dois `oraculo/PERFIL.md`.
- **PR #7**: base (`especial/precon-em-jogo`) já merged; mudar a base para `main` e rebasear; conferir sobreposição com a sala v3 (ambos tocam `manaburn/index.html`).
- **STATUS.md / historico.md / continuidade / easter_eggs / DECISOES.md**: ~20 branches alteram os mesmos ficheiros de registo. Integração de conteúdos tem de ser **sequencial** (um pacote de cada vez, por ordem cronológica de produção), nunca em bloco.
- **Quatro branches ep10**: além da escolha editorial, as quatro alteram ficheiros comuns (`manaburn/cards/`, raiz do kit); `ep10-97-terrenos` também move a raiz para `episodios/_raiz_antes_ep10/` e cria `manaburn/kit/v3/` — mudança estrutural do kit que precisa de decisão própria.

## 5. O que depende do fundador

1. Qual das quatro branches é o **Ep. 10** do Mana & Burn (e o destino das outras três).
2. Aprovar (ou não) as frentes novas: Pequeno Mestre (PR #2), Vince Vault (PR #11 — a missão confirma: ainda sem frente editorial aprovada), Vinci (PR #17).
3. Merge dos pacotes de conteúdo produzidos (EP03–EP07, Giros, Conde EP005, especiais, lambes) — são conteúdo editorial; o estado de publicação de cada um só o fundador confirma.
4. Merge desta branch de consolidação para `main`.
5. Reconciliação do PR #3 (muda governação) e do PR #9 (muda metodologia do TUBO).
6. `manaburn/kit/v3/` (em `ep10-97-terrenos`): adotar ou não como evolução do kit.

## 6. O que deve permanecer separado

- Frentes novas não aprovadas (secção 2.3).
- Branches já merged (histórico; não apagar sem autorização).
- `giro/2026-11-01`: conteúdo publicado a 01/11 — integrar como **arquivo histórico** sem reabrir o conteúdo (constituição: publicados não se reabrem); o valor é o motor do Giro que lá está.
