# STATUS · Estúdio BINDER

**Só o estado ativo** (decisão de 26/11/2026, `nucleo/DECISOES.md`): o que está em curso, o que depende do fundador e o próximo passo. Quando um item fecha (publicado, rejeitado, integrado), a secção sai daqui e vai **para o topo** de `comum/status_arquivo.md`; o detalhe de cada conteúdo está na ficha e em `comum/REGISTRO_EDITORIAL.md`. Alvo: ≤ 6 KB.

Branch principal: `main`. Git direto para a `main` com validação verde (`AGENTS.md` §3). Histórico até 26/11/2026: `comum/status_arquivo.md`.

## Última sessão

**MB-EP21 «O Capacete Que Nunca Para» (27/11/2026, 18h45)**: CONCLUÍDO, à espera de publicação. Helm of Obedience + Rest in Peace, inspirado num Reel enviado pelo fundador (visto pelo vidIQ, 10 créditos; o Instagram não abre por automação); pauta bloqueada por palavra com o MB-EP19 e liberada pelo fundador (`nucleo/DECISOES.md` 18:10); vozes 1.234 créditos; 54,37 s, QC sem problemas. Ficha: `manaburn/episodios/ep21_capacete_obediencia/ficha.md`.

**MC-EP10 «Larsen: de 1-3 a Jogador do Ano» (27/11/2026, ~18h30 UTC)**: CONCLUÍDO, à espera de publicação (voz 463 créditos; 34,87 s; QC sem problemas). Pedido «ache um que viralize»; tema escolhido pelo fundador no cartão. Mundial 32 (MagicCon Atlanta): Larsen começou 1-3, quase abandonou, ganhou 8 das 10 seguintes (9-5, 20.º) e ficou Jogador do Ano porque o Sajgalik perdeu a final por 3-0. Entregas em `/mnt/project-files/tubo/mc-ep10/`. Ficha: `oraculo/episodios/ep10_larsen_jogador_ano/ficha.md`.

**MC-EP09 «cEDH na Mercadia Games» v3 (27/11/2026, 16h10)**: CONCLUÍDO, à espera de publicação (publicar a **v4** com a capa da bandeira: logótipo da Mercadia, TUBO aos 2,4 s, nome do campeão e lista em destaque). v2: campeão primeiro (voz reordenada, 0 créditos), mosaico dos 39, mapa de Lisboa e cartão da Mercadia, efeitos novos; cenas `mosaico`/`evento` + deixas `sfx` no motor. Primeiro cEDH do TUBO: Official P9Q Side Quest na Mercadia Games (Lisboa, 22/11, 39 jogadores, TopDeck); o campeão foi o único Thrasios + Tymna; 13 combos na lista (Commander Spellbook), Devoted Druid + Swift Reconfiguration. Cenas novas `decklist` e `combo` no motor TUBO (regressão sem diferenças); voz 411 créditos; 30,60 s, QC sem problemas. Falta o logótipo da loja (re-render sem voz). Ficha: `oraculo/episodios/ep09_mercadia_cedh/ficha.md`.

**MB-EP20 «O Monólito Infinito» (27/11/2026, 09h30)**: CONCLUÍDO, à espera de publicação. Basalt Monolith + Rings of Brighthearth (mana incolor infinita por cópia de habilidade, pilha desenhada passo a passo) e Walking Ballista de finalizador; roteiro do fundador produzido pela SHOWRUNNER §4.3; vozes 1.423 créditos; 62,20 s, QC sem problemas. Novo **módulo de pesquisa «deck Commander»** (`nucleo/SHOWRUNNER.md` §2.4 passo 9; `nucleo/DECISOES.md` 27/11). Ficha: `manaburn/episodios/ep20_monolito_infinito/ficha.md`.

**Falta o fundador colar** `nucleo/prompts/CLAUDE_PROJECT.md` (claude.ai) e `nucleo/prompts/CHATGPT.md` (ChatGPT).

## Ciclo de vida (desde 28/11/2026: `python3 comum/ferramentas/memoria.py painel`)

Reconciliação de 28/11 (fundador, 02:13: «os episódios que já foram criados e finalizados também já foram publicados»): os 26 `CONCLUÍDO` e 12 Órbita `APROVADO` («sequência publicada») passaram a `PUBLICADO`, com a data exata por confirmar; antes/depois em `comum/reconciliacao/2026-11-28_publicados.csv`. **Já não há fila de publicação.** O que exige ação agora é a **métrica**: 80 dos 90 publicados não têm números no registo. Versão publicada por confirmar em 8 (MB-EP17, MC-ESP03, MB-ESP05, LL-ART21, AB-04, MC-EP09, MC-EP10, LL-ECO01; coluna `confirmar` do CSV). Em produção: MB-GIRO01, EX-01, PM-EP01, LM-EP00; ORB-21 continua `APROVADO` (estava «agendado 06/11», sem confirmação).

Para fechar um episódio novo: QC → o fundador escreve «Aprovação final: <nome> · <data>» na ficha → `python3 comum/ferramentas/eventos.py concluir <ID> --qc <qc.json>` (grava o evento para o Data Binder e muda o registo; `comum/eventos/LEIA-ME.md`).

## Em desenvolvimento

- **Lisa Marie no Ar:** veredito do fundador sobre o recorte 2D e as prévias LM-EP00/LM-EP01; faltam personagem-mestre, voz e trilha oficiais (autorização de custo) e as decisões de 19/11 (paleta, estética de papel, símbolos). Próxima tarefa: `lisa-marie/PROMPT_CLAUDE.md` → ficha de modelo + preview estático.
- **Vince Vault:** kit 2D em falta (refazer ou recuperar do PR #17); decidir a fonte de preços (Cardmarket sim/não).
- **Meta em Curto · ciclo:** conferência de PR-PAU02-01 a 30/11 (anúncio de banidos) → MC-PAU03; a prestação de contas do Pauper de 01/12 passa a «#4». Começar sempre por `python3 -I oraculo/previsoes/ciclo.py continuacao`.

## Depende do fundador (decisões e dados)

- Missão estrutural: decisões de `nucleo/auditorias/2026-11-19_missao_estrutural.md` §8 (integrar MB-EP11 e os insights de 13–14/11).
- Insights: ecrã Conteúdo, visitas ao perfil, toques no link, impulso de 8–14/11; datas de publicação dos conteúdos fechados a 16/11; R$ 11 de impulso de 26/10 (quais vídeos).
- Registo: confirmar as 30 linhas `POR AUDITAR` de `comum/REGISTRO_EDITORIAL.md`.
- BINDER Vision: prints de visitas e toques no link, Play Console, bio e destaque «Comece aqui», gravações de `binder-vision/ESTRATEGIA.md` §8, pautas da Camada 2.
- Infraestrutura: ligar a @binder_vision no vidIQ; RLS em `public.spatial_ref_sys` (Supabase); atualizar as skills `binder-*` (ainda mandam ler o Drive primeiro).
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

Último: 27/11/2026 (18h45), MB-EP21, no fim de `manaburn/episodios/ep21_capacete_obediencia/ficha.md`. Anterior: 27/11/2026 (~18h30 UTC), MC-EP10, no fim de `oraculo/episodios/ep10_larsen_jogador_ano/ficha.md`. Anterior: 27/11/2026 (16h10), MC-EP09 v3, no fim de `oraculo/episodios/ep09_mercadia_cedh/ficha.md`. Anterior: 27/11/2026 (09h30), MB-EP20, no fim de `manaburn/episodios/ep20_monolito_infinito/ficha.md`. Anterior: 27/11/2026 (00h45), MB-ESP05, no fim de `manaburn/episodios/esp05_taverna_avalon/ficha.md`. Anterior: 26/11/2026 (21h45), MB-EP19, no fim de `manaburn/episodios/ep19_robo_imortal/ficha.md`. Anterior: LL-ART21 (`lambe-lambe/episodios/ll-art21_will_murai_alem_das_cartas/ficha.md`). Anteriores: `comum/status_arquivo.md` («Handoff»).
