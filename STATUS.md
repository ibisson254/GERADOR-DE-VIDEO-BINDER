# STATUS · Estúdio BINDER

Branch de trabalho: `consolidacao-estudio` (a `main` não é tocada até o fundador aprovar o merge).
Missão em curso: "Consolidação estrutural do BINDER Originals" (31/10/2026, 10:46), que sucede à "Operação de Consolidação" da mesma data.

## Estado editorial

Frentes ativas: Mana & Burn, Conde de Manaforte, Meta em Curto · Oráculo de Tubo (séries); Órbita (temática); Lambe-lambe (espontânea); especiais. Tudo o que está no repositório está aprovado e lançado; Halloween 2026 e Star Trek publicados. Detalhe: `nucleo/CATALOGO_EDITORIAL.md`.

## Consolidação

| Bloco | Estado | Onde |
|---|---|---|
| Inventário | Concluído | `INVENTARIO.md` (histórico) |
| Integração de `especial/sir-patrick` | Concluído, sem conflitos | commit 4e6af96 |
| Núcleo e fonte de verdade | Concluído | `nucleo/`, constituição v1.3 |
| Catálogo editorial (Órbita e Lambe-lambe ativos) | Concluído | `nucleo/CATALOGO_EDITORIAL.md` |
| Hierarquia documental | Concluído | constituição §1, `nucleo/README.md` |
| Showrunner + handoff | Concluído | `nucleo/SHOWRUNNER.md`, `nucleo/modelos/HANDOFF.md` |
| Prompts Claude Project e ChatGPT | Texto pronto | `nucleo/prompts/` |
| Instruções do projeto claude.ai | **Por aplicar pelo fundador** (o conector não altera esse campo) | texto em `nucleo/prompts/CLAUDE_PROJECT.md` |
| Merge para `main` | Aguarda aprovação do fundador | — |

## Depende do fundador

1. Colar `nucleo/prompts/CLAUDE_PROJECT.md` no campo Instruções do projeto "Binder Marketing" (hoje tem o rascunho de um comentário do TUBO).
2. Responder Q1–Q3 (`nucleo/DECISOES.md`, 31/10): nome público do TUBO; fecho do scanner nos Reels 4:5 do Órbita; trazer as bíblias do Órbita e do Lambe-lambe para o repositório.
3. Aprovar o merge de `consolidacao-estudio` para `main`.
4. Enviar `comum/outro/outro_binder_916.mp4` (a regra do fecho aponta para um ficheiro que não está no repositório).

## Pendências técnicas (não bloqueiam a governação)

- Motor v2 do Mana & Burn está só no projeto claude.ai (`claude/gerador-manaburn/`); o `process.py` do Ep. 09 importa módulos que faltam no repositório.
- Gerador do Órbita só no projeto claude.ai (`claude/gerador/`).
- `oraculo/episodios/ep01_render_v2.py` importa `render`, que não existe; `conde/montar_ep002.py` tem caminho absoluto. Não se mexe em scripts de episódios publicados sem necessidade.
- Skills `binder-*` ainda mandam ler primeiro o Drive e dizem que o Scryfall não abre; alinhar com o repositório quando o fundador quiser.
- `nucleo/prompts/CHATGPT.md`: depois do merge, trocar `consolidacao-estudio` por `main` nos links.

## Próximo passo concreto

Fundador: colar as instruções do projeto (ponto 1) e responder Q1–Q3. Agente, na sessão seguinte: aplicar as respostas e preparar o merge para `main`.

## Handoff

```
HANDOFF · 31/10/2026 · Claude
Repositório: ibisson254/GERADOR-DE-VIDEO-BINDER · branch consolidacao-estudio
Objetivo atual: fechar a consolidação estrutural e fazer merge para main.
Decisões: Órbita e Lambe-lambe ativos; conteúdos do repositório aprovados e lançados; pastas das séries mantidas (nucleo/DECISOES.md, 31/10).
Documentos consultados: missão de 31/10, perfis das 3 séries, índices do Drive do Órbita e do Lambe-lambe, claude/serie-star-trek-bauhaus.md, claude/reel-lambe-lambe-pop.md.
Alterações: nucleo/CATALOGO_EDITORIAL.md, nucleo/SHOWRUNNER.md, nucleo/modelos/HANDOFF.md, nucleo/prompts/, constituição v1.3, checklist, series.yaml, AGENTS.md, nucleo/README.md, comum/historico.md, INVENTARIO.md (nota de histórico).
Pendentes: ver "Depende do fundador" e "Pendências técnicas".
Próximo passo: aplicar Q1–Q3 e preparar o merge para main.
```
