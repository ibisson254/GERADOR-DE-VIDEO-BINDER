# STATUS · Estúdio BINDER

**Só o estado ativo** (decisão de 26/11/2026, `nucleo/DECISOES.md`): o que está em curso, o que depende do fundador e o próximo passo. Quando um item fecha (publicado, rejeitado, integrado), a secção sai daqui e vai **para o topo** de `comum/status_arquivo.md`; o detalhe de cada conteúdo está na ficha e em `comum/REGISTRO_EDITORIAL.md`. Alvo: ≤ 6 KB.

Branch principal: `main`. Git direto para a `main` com validação verde (`AGENTS.md` §3). Histórico até 26/11/2026: `comum/status_arquivo.md`.

## Última sessão

**LL-ART21 V2 «Will Murai — o artista por trás das cartas» (26/11/2026, 23h)**: reconstrução autorizada pelo fundador. As 54 ilustrações de Willian Murai no Scryfall, foto do artista só na versão privada; 94,17 s, sem voz, 0 créditos, QC sem problemas. Publicável: `ll-art21_v2_semfoto.mp4`; V1 preservada. Ficha, secção «V2».

**Fórmula dos combos + MB-EP19 «O Robô Que Não Morre» (26/11/2026, 21h45)**: CONCLUÍDO, à espera de publicação. «Episódio de combo» passa a padrão recorrente (não exclusivo) do Mana & Burn (`manaburn/PERFIL.md`; `nucleo/DECISOES.md` 21:45). MB-EP19: Mikaeus, the Unhallowed + Triskelion, escolhido entre 3 candidatos; vozes 1.112 créditos; 50,90 s, QC sem P0/P1. MB-EP18 verificado sem alterações; re-render das vozes já pagas (0 créditos).

**Falta o fundador colar** `nucleo/prompts/CLAUDE_PROJECT.md` (claude.ai) e `nucleo/prompts/CHATGPT.md` (ChatGPT).

## Prontos, à espera do fundador (publicação ou envio)

| ID | O que falta | Onde |
|---|---|---|
| MB-EP19 O Robô Que Não Morre | escuta e publicação (`utm_campaign=MB-EP19`); não publicar no mesmo dia do MB-EP18 | `manaburn/episodios/ep19_robo_imortal/` |
| LL-ART21 Will Murai (Reel **V2**) | ver a V2 e escolher V1 ou V2; publicar a versão **sem foto** (`utm_campaign=LL-ART21`); música no Instagram; versão com foto só com autorização da imagem | `lambe-lambe/episodios/ll-art21_will_murai_alem_das_cartas/` |
| MB-EP18 O Lagarto Infinito | escuta e publicação; confirmar preços na LigaMagic antes de citar valores | `manaburn/episodios/ep18_lagarto_infinito/` |
| MB-EP17 React @magicamador | ouvir o corte aos 43,6 s; pedir ao parceiro o OK do âmbito + collab; resposta em `manaburn/autorizacoes/2026-11-24_magicamador_react.md` (se recusar: arquivar) | `manaburn/episodios/ep17_react_magicamador/` |
| MC-PAU02 «Vai ser banida?» | escutar a pronúncia; enviar as duas mensagens (resposta até 28/11); publicar a 29/11 com `utm_campaign=MC-PAU02` | `oraculo/episodios/pau02_tenda_snacker/` |
| MC-PAU08 «O mais jogado não ganhou» | publicar (collab Tiago Fuguete + Tenda da Liliana) | `oraculo/episodios/pau08_fuguete_tenda/` |
| MC-PAU01 «86 dólares» | publicar | `oraculo/pau01/` |
| MB-EP14 Everything | escuta e publicação **antes de 30/11, 14h de Brasília** (venda do Secret Lair) | `manaburn/episodios/ep14_everything/` |
| MB-EP16 Alexander (v2) | escuta e publicação; decidir como registar o «EP. 12» do Olag já publicado | `manaburn/episodios/ep16_alexander/` |
| MB-EP12 Money Burn | escuta e publicação | `manaburn/episodios/ep12_money_burn/` |
| LL-ECO01 ecossistema | confirmar se qualquer utilizador cria campeonatos; publicar carrossel + Reel + Story com `utm_campaign=LL-ECO01` | ficha do LL-ECO01 |
| LL-MEME01 «a vida é uma maravilha» | confirmar que «booster» não conflita com MB-EP06/MB-GIRO01; publicar | ficha do LL-MEME01 |
| LL-LISA01 teaser Lisa Marie | publicar a v2 | `lambe-lambe/episodios/ll-lisa01_estreia_lisa_marie/` |
| MC-ESP03 Farpas de Mana | enviar a prévia (`oraculo/episodios/esp03_dc500/mensagem_farpas.txt`); plano B: publicar com crédito, sem collab | `oraculo/episodios/esp03_dc500/` |
| AB-03 a AB-10 (ABISMO) | escolher v1 ou v2 do AB-04; aprovar e publicar | `abismo/publicacoes/CAMPANHA_NAUCTIS_EMBALAGENS.md` |
| EX-01 Nauctis | escolher A ou B; licença da «Auction of Power» | registo |
| Especial «Precon em jogo» V2 | aprovar a V2 (branch `especial/precon-em-jogo-v2`) | `comum/status_arquivo.md` |

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

1. Antes de 30/11: publicar MB-EP14 e MC-PAU02 (fundador).
2. 30/11: conferência PR-PAU02-01 → MC-PAU03 (`tubo segunda`).
3. Primeiro episódio de cada semana: criar ou atualizar `comum/radar/<AAAA-Www>.md` pelo modelo de `comum/radar/LEIA-ME.md`.

## Handoff

Último: 26/11/2026 (21h45), MB-EP19 + fórmula dos combos, no fim de `manaburn/episodios/ep19_robo_imortal/ficha.md`. Anterior: LL-ART21 (`lambe-lambe/episodios/ll-art21_will_murai_alem_das_cartas/ficha.md`). Anteriores: `comum/status_arquivo.md` («Handoff»).
