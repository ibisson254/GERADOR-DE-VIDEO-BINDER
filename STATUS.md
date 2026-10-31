# STATUS · Estúdio BINDER

Branch de trabalho: `consolidacao-estudio` (a `main` não é tocada até o fundador aprovar o merge).
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
| Merge para `main` | Preparado: pull request aberto, sem conflitos (a `main` está contida na branch) | GitHub, PR `consolidacao-estudio` → `main` |

## Depende do fundador

1. Aprovar o pull request `consolidacao-estudio` → `main` (botão "Merge" no GitHub, ou pedir ao agente).
2. Enviar `comum/outro/outro_binder_916.mp4` (a regra do fecho aponta para um ficheiro que não está no repositório). Origem: corte do fim do `ManaBurn_Ep5_Knacksaw_916.mp4` (a partir de 43,2 s), sem rótulo de série, entregue num chat do claude.ai por volta de 24–25/10; não está no Drive nem no projeto claude.ai. Alternativa sem custo: gerar a reconstrução que os episódios publicados já usam (`manaburn/episodios/ep09_dack/fecho_scanner.py`, 3,87 s, quadros reais do scanner). Não bloqueia o merge.

## Pendências técnicas (não bloqueiam a governação)

- Motor v2 do Mana & Burn está só no projeto claude.ai (`claude/gerador-manaburn/`); o `process.py` do Ep. 09 importa módulos que faltam no repositório.
- Gerador do Órbita já no repositório (`orbita/gerador/`); para renderizar faltam os PNGs das cartas (`BINDER_gerador_orbita.zip`) e as fontes em `node_modules/`.
- `oraculo/episodios/ep01_render_v2.py` importa `render`, que não existe; `conde/montar_ep002.py` tem caminho absoluto. Não se mexe em scripts de episódios publicados sem necessidade.
- Skills `binder-*` ainda mandam ler primeiro o Drive e dizem que o Scryfall não abre; alinhar com o repositório quando o fundador quiser.
- `nucleo/prompts/CHATGPT.md`: depois do merge, trocar `consolidacao-estudio` por `main` nos links.

## Próximo passo concreto

Fundador: aprovar o merge de `consolidacao-estudio` para `main`. Agente: fazer o merge e trocar `consolidacao-estudio` por `main` nos links de `nucleo/prompts/CHATGPT.md`.

## Handoff

```
HANDOFF · 31/10/2026 · Claude
Repositório: ibisson254/GERADOR-DE-VIDEO-BINDER · branch consolidacao-estudio
Objetivo atual: merge da consolidação para main.
Decisões: Órbita e Lambe-lambe ativos; conteúdos do repositório aprovados e lançados; pastas das séries mantidas (nucleo/DECISOES.md, 31/10).
Documentos consultados: missão de 31/10, perfis das 3 séries, índices do Drive do Órbita e do Lambe-lambe, claude/serie-star-trek-bauhaus.md, claude/reel-lambe-lambe-pop.md.
Alterações: nucleo/CATALOGO_EDITORIAL.md, nucleo/SHOWRUNNER.md, nucleo/modelos/HANDOFF.md, nucleo/prompts/, constituição v1.3, checklist, series.yaml, AGENTS.md, nucleo/README.md, comum/historico.md, INVENTARIO.md (nota de histórico).
Alterações (15:18): orbita/ (bíblia + gerador), lambe-lambe/ (bíblia), constituição v1.4, catálogo, series.yaml, AGENTS.md, SHOWRUNNER.md.
Pendentes: ver "Depende do fundador" e "Pendências técnicas".
Próximo passo: merge para main com aprovação do fundador.
```
