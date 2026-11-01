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

## Produção recente

- 01/11/2026 · Meta em Curto EP03 «Arquivo Competitivo» produzido (render conferido, pacote de publicação pronto): `oraculo/episodios/ep03_arquivo_ficha.md`. Falta o fundador publicar. Na branch `meta-em-curto-ep03` (PR para `main`).

## Próximo passo concreto

Produzir normalmente a partir da `main`: palavra de arranque → `AGENTS.md` → `nucleo/SHOWRUNNER.md`. Pendência técnica com mais impacto: subir o motor v2 do Mana & Burn (`claude/gerador-manaburn/` no projeto claude.ai) para `manaburn/`.

## Handoff

```
HANDOFF · 01/11/2026 19:45 · Claude
Repositório: ibisson254/GERADOR-DE-VIDEO-BINDER · branch meta-em-curto-ep03 (PR para main)

Objetivo atual: Meta em Curto EP03 «Arquivo Competitivo» entregue (vídeo, capa, legenda, comentário fixado, texto alternativo, fontes).

Decisões tomadas nesta sessão:
- Roteiro do fundador refinado por rigor: cortado o 1.º lugar do Spotlight (sem fonte), Taipei sem formato («sem fonte»), São Paulo sem «torneios paralelos», «amanhã» trocado por pergunta A/B/C. Na ficha; nenhuma regra mudou (DECISOES.md: não).
- Boletim de fim de semana tratado como formato pontual do TUBO, sem alterar a bíblia.

Documentos consultados:
- AGENTS.md, STATUS.md, nucleo/ (constituição, catálogo, showrunner, decisões, modelos), oraculo/PERFIL.md, oraculo/CONTEXTO.md, ficha e scripts do EP02, comum/outro/LEIA-ME.md, comum/historico.md, comum/easter_eggs.md

Alterações realizadas:
- oraculo/episodios/ep03_* (ficha, fontes, roteiro, words, ep03_audio.py, ep03_render.py) · novos
- oraculo/legendas/ep03_arquivo_legenda.txt · novo
- oraculo/PERFIL.md (lista de episódios), comum/historico.md, comum/easter_eggs.md, STATUS.md

Tarefas pendentes:
- Publicar o EP03 · fundador
- Rever o PR e integrar em main · fundador
- EP04: análise do evento escolhido nas respostas A/B/C (resultados, Top 8, listas) · agente, quando houver respostas
- Pendências técnicas anteriores mantêm-se

Próximo passo concreto: publicar o EP03 com oraculo/legendas/ep03_arquivo_legenda.txt; depois ler as respostas A/B/C e produzir o EP04.
```
