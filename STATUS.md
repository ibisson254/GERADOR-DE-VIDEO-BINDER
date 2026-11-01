# STATUS · Estúdio BINDER

Branch principal: `main` (consolidação integrada a 31/10/2026, PR #1, aprovado pelo fundador). A branch `consolidacao-estudio` fica como histórico.
Missão em curso: "Consolidação estrutural do BINDER Originals" (31/10/2026, 10:46), que sucede à "Operação de Consolidação" da mesma data.

## Memória editorial e insights (01/11/2026, branch `feature/memoria-editorial-insights`, PR #3 para `main` à espera de aprovação)

| Bloco | Estado | Onde |
|---|---|---|
| Registo editorial universal | Criado; 72 conteúdos migrados; **inventário incompleto** (30 `POR AUDITAR`) | `comum/REGISTRO_EDITORIAL.md` |
| Auditoria de originalidade | Ativa (script + regra) | `SHOWRUNNER.md` §2.3, `comum/ferramentas/memoria.py pauta` |
| Encerramento obrigatório | Ativo | `SHOWRUNNER.md` §6, `modelos/FICHA_EPISODIO.md`, `memoria.py encerramento` |
| Insights semanais | Ativo; snapshots de 21/10 e 26/10 migrados | `comum/insights/` |
| Testes A–F | 17 testes OK | `python3 -m unittest comum/ferramentas/test_memoria.py` |

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

Nada bloqueia a produção. Para fechar a memória editorial:
1. Aprovar o merge do PR #3 (`feature/memoria-editorial-insights` → `main`).
2. **Hoje, antes das 21h:** o Giro de Domingo nº 1 (MB-GIRO01, branch `giro/2026-11-01`) repete no bloco 3 o evento, a carta e a regra do Ep. 07 (All Leylines' Eve). Publicar assim ou trocar o bloco?
3. Confirmar as lacunas do fim de `comum/REGISTRO_EDITORIAL.md` (Ep. 03/04 do Mana & Burn, datas de publicação, quais Reels do Órbita e posts do Lambe-lambe saíram).
4. Dizer quais dois vídeos levaram os R$ 11 de impulsionamento de 26/10 (e se o valor é total ou por vídeo).
5. Domingo: enviar os prints de Visão geral **e** Conteúdo (e Anúncios, se houver impulso).
Opcional: colar `nucleo/prompts/CHATGPT.md` nas instruções do projeto ou GPT do ChatGPT.

## Pendências técnicas (não bloqueiam a governação)

- Motor v2 do Mana & Burn está só no projeto claude.ai (`claude/gerador-manaburn/`); o `process.py` do Ep. 09 importa módulos que faltam no repositório.
- Gerador do Órbita já no repositório (`orbita/gerador/`); para renderizar faltam os PNGs das cartas (`BINDER_gerador_orbita.zip`) e as fontes em `node_modules/`.
- `oraculo/episodios/ep01_render_v2.py` importa `render`, que não existe; `conde/montar_ep002.py` tem caminho absoluto. Não se mexe em scripts de episódios publicados sem necessidade.
- Skills `binder-*` ainda mandam ler primeiro o Drive e dizem que o Scryfall não abre; alinhar com o repositório quando o fundador quiser.

## Próximo passo concreto

Depois do merge: produzir a partir da `main` com a auditoria de originalidade (`memoria.py pauta`) e o encerramento obrigatório; no domingo seguinte, `memoria.py semana AAAA-MM-DD` com os prints. Antes do merge: decidir o alerta do Giro (item 2 acima). Pendência técnica com mais impacto: subir o motor v2 do Mana & Burn (`claude/gerador-manaburn/` no projeto claude.ai) para `manaburn/`.

## Handoff

```
HANDOFF · 01/11/2026, ~18h Lisboa · Claude
Repositório: ibisson254/GERADOR-DE-VIDEO-BINDER · branch feature/memoria-editorial-insights · PR #3 · commit anterior a este a5a6935 (conferido no remoto: sim)

Objetivo atual: memória editorial universal, encerramento obrigatório e insights semanais, à espera do merge.

Conteúdos tocados (comum/REGISTRO_EDITORIAL.md): migração retroativa de 72 IDs; nenhum estado aprovado ou publicado foi reaberto.

Decisões tomadas nesta sessão:
- Registo, originalidade, encerramento e insights (nucleo/DECISOES.md 01/11/2026: sim)

Documentos consultados: AGENTS.md, STATUS.md, constituição, catálogo, SHOWRUNNER, DECISOES, historico, modelos; fichas e legendas de todas as frentes; branches giro/2026-11-01 e pequeno-mestre/ep01; projeto claude.ai (contexto Instagram, lambe-lambe, legendas e planos do Mana & Burn, piloto do TUBO, auditoria de 30/10).

Alterações realizadas: ver PR #3 (comum/REGISTRO_EDITORIAL.md, comum/insights/, comum/ferramentas/, AGENTS.md, nucleo/SHOWRUNNER.md, modelos, constituição v1.5, checklist, DECISOES, historico, STATUS).

Insights (domingo): snapshots 2026-10-21 e 2026-10-26 migrados · impulso A CONFIRMAR: MB-EP01, MB-EP05, ORB-18, MB-SN01, CM-EP001, MB-EP07, MB-ZAP01, LL-SN01

Tarefas pendentes:
- Merge do PR #3 · fundador
- Alerta MB-GIRO01 × MB-EP07 antes das 21h de hoje · fundador
- Lacunas do registo (30 POR AUDITAR) e quais posts levaram os R$ 11 · fundador
- Episódios antigos sem texto_alternativo.txt nem "Ficheiros finais" (não se reabrem; só se completam se o fundador quiser) · agente

Próximo passo concreto: depois do merge, próxima pauta com `python3 comum/ferramentas/memoria.py pauta --objeto "…"`; no domingo, `python3 comum/ferramentas/memoria.py semana AAAA-MM-DD`.
```
