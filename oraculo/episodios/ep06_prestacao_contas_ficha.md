# Ficha · Meta em Curto · EP06 · Prestação de contas: placar zero

Roteiro e storyboard: `ep06_prestacao_contas_roteiro.md`. Fontes: `ep06_prestacao_contas_fontes.txt`. Pacote: `../legendas/ep06_prestacao_contas_legenda.txt`. Previsões: `../previsoes/registo.yaml`. **Escrito, não produzido** (09/11/2026, 01h): falta autorização para a voz.

## Classificação
- Série: Meta em Curto (TUBO) · Episódio de segunda do ciclo semanal (`../CICLO_SEMANAL.md` §3)
- Classe: Previsão (conferência intermédia, Fase C do protocolo). Sem torneio concluído: o pré-release é casual e o Sealed de TRK só entra no Arena a 10/11.
- Complexidade: baixa · Estratégia: verificação rápida + reutilização dos dados do EP05

## Editorial
- Objetivo: cumprir a promessa pública («volta segunda pra prestar contas») e fixar o ciclo quinta → segunda.
- Proposta de valor: o TUBO mostra a previsão original, admite que ainda não há placar e separa opinião de dado.
- Público: quem viu o EP05 (5.334 visualizações, 13 guardados) e jogador de Limited.
- Hipótese a testar: prestar contas sem placar mantém a retenção se o gancho tiver conflito (Rakdos × cinco cores); pergunta A/B/C com dois lados nomeados gera mais respostas que a do EP05.
- Tese (leitura do TUBO): opinião não mexe no placar.
- Gancho: «Quinta, eu cravei Rakdos. O primeiro relato de quem já jogou diz: cinco cores. Placar oficial: zero jogos.»
- Duração estimada: ~55 s sem o fecho (155 palavras; EP02 = 116 palavras em 45 s).

## Fontes e evidências
| Afirmação | Tipo | Fonte | Data |
|---|---|---|---|
| Texto original de PR-TRK-01 e da fala do EP05 | facto (registo) | `registo.yaml`; `ep05_star_trek_ficha.md` (branch `meta-em-curto-ep05`); Giro de 08/11 | 05/11/2026 |
| Sealed de TRK no Arena desde 10/11 | facto | Wizards, calendário de eventos do Arena (via fontes do EP05) | 05/11/2026 |
| 0 jogos de Sealed TRK no 17Lands | facto em 09/11 (dedução: o set ainda não está no Arena) | idem | 09/11/2026 |
| Strange New Worlds acima do resto; Sealed puxa para cinco cores | opinião (O), Early Access | MTG Rocks, «These Underrated MTG Star Trek Cards Will Win Your Prerelease» | 05/11/2026 |
| The Traveler: {G}{U}, alcance, vigilância, força = terrenos com nomes diferentes | facto | Scryfall API, TRK 254 | 09/11/2026 |
| Simic = Strange New Worlds | facto atribuído (guias de arquétipos) | Ultimate Guard, guia de pré-release | — |
| Motor: Rakdos 65, Simic 25 (teto) | modelo | EP05, `pools.py` | 05/11/2026 |
| PR-TRK-03 (3+ cores abaixo de 2) | previsão de registo | `registo.yaml` | 05/11/2026 |
| «Opinião não mexe no placar» | opinião do TUBO / regra do protocolo (tipos R/O) | `PROTOCOLO_PRE_RELEASE.md` §3 | — |
| Grau de certeza 2/5, igual | juízo editorial | protocolo §5 | 09/11/2026 |

## Produção (quando autorizada)
- Voz: ElevenLabs «Antonio de Jesus» (`MK5tXPmT83J5SUlpUo4K`), eleven_v4, atempo 1,10. **Custo estimado: ~1.000–1.100 créditos por tomada** (EP05: 1.503 créditos para ~250 palavras); 2 tomadas ≈ 2.200. Precisa de autorização explícita (`AGENTS.md` §3).
- Render: `ep05_render.py` como base (mesmos gráficos de barras, mesmo terminal, carta em scan); dados do bloco 7 lidos de `oraculo/ep05/resultados/` (branch `meta-em-curto-ep05`).
- Carta: `../ep06/cartas/the_traveler.png` (Scryfall, 744×1040, inteira).
- Trilha: `tubo_tema.mp3`; corte seco depois de «Opinião não mexe no placar.».
- Contador ERROS HUMANOS: não mostrar (sem valor registado).
- Easter egg: proposta «KOBAYASHI MARU» (roteiro).
- Fecho: `comum/outro/outro_binder_916.mp4`.

## Riscos e limitações
- Se o fundador publicar depois de terça, «zero jogos» deixa de ser verdade: nesse caso, refazer o bloco 4 com o número do dia ou não publicar.
- 17Lands estava inacessível na sessão do EP05 e continua fora da lista de acesso da shell; para as conferências de 16/11 em diante: WebFetch, espelho MTGMeta (mesmo recorte) ou print do fundador.
- Relato único (MTG Rocks) apresentado como «o primeiro relato», não como consenso.

## Entregáveis
- [x] Roteiro e storyboard · [x] Legenda · [x] Comentário fixado · [x] Texto alternativo (do roteiro) · [x] Fontes · [ ] Vídeo · [ ] Capa

## Depois de publicar
- Métrica principal: guardados + partilhas · secundária: respostas A/B/C.
- Próxima conferência: 16/11 (placar parcial de PR-TRK-01..03).

## Atualização de 10/11/2026 (briefing da continuação do EP05)

O fundador enviou o EP05 e pediu a continuação. Estado: EP06 continua escrito e não produzido. O que mudou desde 09/11:

| Novidade | Tipo | Efeito no roteiro |
|---|---|---|
| TRK entra hoje no Arena | facto (Wizards) | Blocos 1, 3 e 4: «zero jogos» deixa de valer. Trocar por «o 17Lands ainda não publicou ranking» (sem número de jogos, que não temos) |
| Draftsim, 09/11: preto-vermelho agressivo funciona; branco-preto destacado; sopa viva pelo fixing, melhor com verde | relato/opinião (uma loja, sem contagem) | Bloco 5: já são dois relatos. Um a favor de PR-TRK-01, dois contra PR-TRK-03. Não muda estado |
| 17Lands sem win rate por par de TRK; datasets públicos ~2 semanas depois | facto de fonte terciária | Bloco 10: o placar parcial de 16/11 pode vir pequeno ou vazio; dizer a amostra |
| Qualifier do Arena em Sealed de TRK: 14/11 (Play-In) e 21–22/11 | facto (Wizards) | Gancho possível para quinta e para a segunda de 23/11 |

Gancho revisto (proposta, por aprovar): «Quinta, eu cravei Rakdos. Dois relatos do pré-release. Um me dá razão. O outro diz: sopa. Ranking oficial: ainda nenhum.»

Não muda: texto original, critério, grau 2/5, pergunta A/B/C, carta The Traveler, custo de voz (~1.000–1.100 créditos por tomada, por autorizar).
