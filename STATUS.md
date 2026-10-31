# STATUS · Estúdio BINDER

Branch principal: `main` (consolidação integrada a 31/10/2026, PR #1, aprovado pelo fundador). A branch `consolidacao-estudio` fica como histórico.
Missão em curso: "Consolidação estrutural do BINDER Originals" (31/10/2026, 10:46), que sucede à "Operação de Consolidação" da mesma data.

## Estado editorial

Frentes ativas: Mana & Burn, Conde de Manaforte, Meta em Curto (séries); Órbita (temática); Lambe-lambe (espontânea); especiais. Tudo o que está no repositório está aprovado e lançado; Halloween 2026 e Star Trek publicados. Detalhe: `nucleo/CATALOGO_EDITORIAL.md`.

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

## Depende do fundador

Nada bloqueia a produção. Opcional: colar `nucleo/prompts/CHATGPT.md` nas instruções do projeto ou GPT do ChatGPT.

## Pendências técnicas (não bloqueiam a governação)

- Motor v2 do Mana & Burn está só no projeto claude.ai (`claude/gerador-manaburn/`); o `process.py` do Ep. 09 importa módulos que faltam no repositório.
- Gerador do Órbita já no repositório (`orbita/gerador/`); para renderizar faltam os PNGs das cartas (`BINDER_gerador_orbita.zip`) e as fontes em `node_modules/`.
- `oraculo/episodios/ep01_render_v2.py` importa `render`, que não existe; `conde/montar_ep002.py` tem caminho absoluto. Não se mexe em scripts de episódios publicados sem necessidade.
- Skills `binder-*` ainda mandam ler primeiro o Drive e dizem que o Scryfall não abre; alinhar com o repositório quando o fundador quiser.

## Próximo passo concreto

Produzir normalmente a partir da `main`: palavra de arranque → `AGENTS.md` → `nucleo/SHOWRUNNER.md`. Pendência técnica com mais impacto: subir o motor v2 do Mana & Burn (`claude/gerador-manaburn/` no projeto claude.ai) para `manaburn/`.

## Handoff

```
HANDOFF · 31/10/2026 · Claude
Repositório: ibisson254/GERADOR-DE-VIDEO-BINDER · branch main (PR #1 integrado)
Objetivo atual: consolidação concluída; estúdio pronto a produzir a partir da main.
Decisões: Órbita e Lambe-lambe ativos; nome Meta em Curto; Órbita sem fecho; conteúdos do repositório aprovados e lançados; fecho do scanner cortado do Ep. 6 (nucleo/DECISOES.md, 31/10).
Documentos consultados: AGENTS.md, STATUS.md, comum/outro/LEIA-ME.md, ManaBurn_Ep6_GodPack_916.mp4 (enviado pelo fundador).
Alterações: comum/outro/outro_binder_916.mp4 e gerar_fecho.py; comum/outro/LEIA-ME.md; series.yaml; nucleo/DECISOES.md; nucleo/prompts/CHATGPT.md (links para main); STATUS.md.
Pendentes: ver "Pendências técnicas".
Próximo passo: produzir; ou subir o motor v2 do Mana & Burn para manaburn/.
```
