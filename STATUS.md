# STATUS · Estúdio BINDER

**Só o estado ativo** (26/11/2026): em curso, depende do fundador, próximo passo. O que fecha vai **para o topo** de `comum/status_arquivo.md`. Alvo: ≤ 6 KB.

Branch principal: `main`. Git direto para a `main` com validação verde (`AGENTS.md` §3). Histórico até 26/11/2026: `comum/status_arquivo.md`.

## Última sessão

**Integração Data Binder + Originals (28/11/2026, 02h–08h)**: auditoria do motor, inteligência cultural e reconciliação juntas na `main` com autorização do fundador (07:53). (1) Fase zero: o Data Binder é o repo `-Binder-Dados` (consultas e relatórios do funil do app); os números dos Originals ficam em `comum/insights/registo_posts.csv`. (2) Evento `episode.completed`: `comum/eventos/LEIA-ME.md`. (3) Revisão pré-merge e divergências por confirmar: `nucleo/auditorias/2026-11-28_integracao_data_binder.md`. Sessões que renderizam começam por `sh comum/ferramentas/preparar_ambiente.sh`.

**Falta o fundador colar** `nucleo/prompts/CLAUDE_PROJECT.md` (claude.ai) e `nucleo/prompts/CHATGPT.md` (ChatGPT).

## Ciclo de vida (desde 28/11/2026: `python3 comum/ferramentas/memoria.py painel`)

Reconciliação de 28/11 (fundador, 02:13: «os episódios que já foram criados e finalizados também já foram publicados»): os 26 `CONCLUÍDO` e 12 Órbita `APROVADO` («sequência publicada») passaram a `PUBLICADO`, com a data exata por confirmar; antes/depois em `comum/reconciliacao/2026-11-28_publicados.csv`. **Já não há fila de publicação.** O que exige ação agora é a **métrica**: 80 dos 90 publicados não têm números no registo. Os 8 com versão por confirmar foram confirmados como publicados (08:05). **Vozes autorizadas = publicado** (regra de 28/11, `eventos.py vozes`). Por confirmar: se ORB-21, MB-GIRO01 e EX-01 já saíram (ou tiveram vozes autorizadas); AB-01 (PUBLICADO mas «não publicada»).

Para fechar um episódio novo: vozes autorizadas → `eventos.py vozes` → QC → o fundador escreve «Aprovação final: <nome> · <data>» na ficha → `python3 comum/ferramentas/eventos.py concluir <ID> --qc <qc.json>` (grava o evento para o Data Binder e garante PUBLICADO; `comum/eventos/LEIA-ME.md`).

## Em desenvolvimento

- **Lisa Marie no Ar:** veredito do fundador sobre o recorte 2D e as prévias LM-EP00/LM-EP01; faltam personagem-mestre, voz e trilha oficiais (autorização de custo) e as decisões de 19/11 (paleta, estética de papel, símbolos). Próxima tarefa: `lisa-marie/PROMPT_CLAUDE.md` → ficha de modelo + preview estático.
- **Vince Vault:** kit 2D em falta (refazer ou recuperar do PR #17); decidir a fonte de preços (Cardmarket sim/não).
- **Meta em Curto · ciclo:** conferência de PR-PAU02-01 a 30/11 (anúncio de banidos) → MC-PAU03; a prestação de contas do Pauper de 01/12 passa a «#4». Começar sempre por `python3 -I oraculo/previsoes/ciclo.py continuacao`.

## Depende do fundador (decisões e dados)

- Missão estrutural: decisões de `nucleo/auditorias/2026-11-19_missao_estrutural.md` §8 (integrar MB-EP11 e os insights de 13–14/11).
- Insights: ecrã Conteúdo, visitas ao perfil, toques no link, impulso de 8–14/11; datas de publicação dos conteúdos fechados a 16/11; R$ 11 de impulso de 26/10 (quais vídeos).
- Registo: confirmar as 30 linhas `POR AUDITAR` de `comum/REGISTRO_EDITORIAL.md`.
- BINDER Vision: prints de visitas e toques no link, Play Console, bio e destaque «Comece aqui», gravações de `binder-vision/ESTRATEGIA.md` §8, pautas da Camada 2.
- Inteligência cultural: escolher (ou não) a oportunidade OP-2026-W48-01 (`python3 comum/ferramentas/inteligencia.py oportunidades`).
- Infraestrutura: ligar a @binder_vision no vidIQ (0 créditos por leitura; desbloqueia métricas e `inteligencia.py padroes`); RLS em `public.spatial_ref_sys` (Supabase); atualizar as skills `binder-*` (ainda mandam ler o Drive primeiro).
- Mana & Burn: esboço das expressões novas do Mana e do Burn; PR #2 (Pequeno Mestre) e PR #7 (TV analógica).
- Parcerias: LL-ART20 Caio Monteiro (prazo de 21/11 passado; registar a resposta) → MC-ESP04 Preconauta.

## Pendências técnicas (não bloqueiam)

- Mana & Burn: `montar.py`, `scryfall.py`, `lote.py`, `testes.py`, `formatos.*` e episódios 1, 5–7 continuam só no projeto claude.ai.
- Órbita: faltam os PNG das cartas e as fontes em `node_modules/` para renderizar.
- `oraculo/episodios/ep01_render_v2.py` importa `render` inexistente; `conde/montar_ep002.py` tem caminho absoluto (publicados: não se mexe sem necessidade).
- Captura paralela do Mana & Burn: medir num PC com mais núcleos se os renders passarem a correr lá (`--workers=1` para comparar).

## Próximo passo concreto

1. Métricas dos publicados (fundador ou Binder Dados): prints/export do Insights por Reel → `comum/insights/` (rotina de domingo 29/11).
2. 30/11: conferência PR-PAU02-01 → MC-PAU03 (`tubo segunda`).
3. Primeiro episódio de cada semana: criar ou atualizar `comum/radar/<AAAA-Www>.md` pelo modelo de `comum/radar/LEIA-ME.md`.

## Handoff

Último: 28/11/2026 (07h55), integração Data Binder, em `nucleo/auditorias/2026-11-28_integracao_data_binder.md`. Anteriores: `comum/status_arquivo.md` («Handoff»).
