# MC-EP08 · «Acertei duas. Nenhuma era o campeão.» (proposta, 16/11/2026)

Estado: **PUBLICADO** (confirmado pelo fundador a 16/11 com o print dos Insights: 250 visualizações, 176 contas, tempo médio 7 s, 4 curtidas, 2 comentários, 1 repost, 3 guardados, 1 seguidor ~6 h depois). Direção aprovada pelo fundador a 16/11, 01:12: «a conclusão do episódio do mundial prossiga e só pare quando o episódio estiver pronto» (inclui a voz). Pedido do fundador (16/11, 00:53): episódio do TUBO sobre o Mundial 32 — decks do Top 8, campeão, conferência das previsões, foto do campeão no episódio e na capa.

Tipo: segunda · prestação de contas (CICLO_SEMANAL §3) + Leitura da Final. Proposta: substitui o MC-EP06 «placar zero» (decide o fundador).

## Ideia refinada

Uma só mensagem: **o TUBO acertou o que mediu e falhou o que não mediu.** Previu os decks; o título foi para um jogador num deck que quase ninguém levou.

- Placar: 2 de 3 (a pública confirmada).
- Campeão: Stefan Schütz (Áustria), Izzet Mission — 2 jogadores em 128 (1,6%).
- Autocorreção honesta: no EP07 o TUBO disse «o deck chega, não quem pilota». No domingo, quem pilotou chegou. Não é previsão registada (não muda placar); é a tese revista em voz alta.

## Conferências (escritas em `oraculo/previsoes/registo.yaml`, 16/11)

| ID | Texto original | Dado (magic.gg) | Estado |
|---|---|---|---|
| PR-WC32-01 (pública) | Jund Sacrifice no Top 8 | Abe Schnake, Jund Sacrifice, no Top 8 | CONFIRMADA |
| PR-WC32-02 | Jund Sacrifice no top 3 dos mais jogados | 7.º, 7/128 (5,5%) | REFUTADA |
| PR-WC32-03 | Izzet Spellementals abaixo de 5% | 0 jogadores | CONFIRMADA |

## Estrutura (~50 s + fecho)

| Tempo | Bloco | No ecrã |
|---|---|---|
| 0–3 s | Gancho, fora do tubo: «Previ três coisas sobre o Mundial. Acertei duas. Nenhuma era o campeão.» | TUBO desconfiado |
| 3–7 s | `ARQUIVO: WC32 · Standard · 15/11 · PRESTAÇÃO DE CONTAS` | mergulho |
| 7–20 s | As 3 previsões, cada uma com «TEXTO ORIGINAL · NÃO EDITADO» e carimbo | 01 ✔ com a lista do Schnake · 03 ✔ «0 de 128» · 02 ✘ «7.º, 5,5%» (carimbo vermelho; o «Erro de sistema» fica para previsões públicas) |
| 20–30 s | Top 8: 8 jogadores, 8 arquétipos diferentes | grelha 2×4 com nome, país e deck; listas em leque rápido |
| 30–40 s | Revelação após o corte seco curto: o campeão | **foto do campeão** + lista Izzet Mission + «2 em 128 · 1,6%» |
| 40–47 s | Tese revista + placar `2/3` + contador `ERROS HUMANOS` +1 | TUBO analítico |
| 47–52 s | «Você levaria ao Mundial um deck que só dois jogadores levaram?» + «Probabilidade calculada. Humanos, imprevisíveis.» | fora do tubo |
| fim | `comum/outro/outro_binder_916.mp4` | — |

## Capa (modelo §7.3)

«O campeão do mundo jogava um deck de» → **1,6%** gigante → TUBO a reagir + foto recortada do campeão → faixa fixa da série.

## Roteiro definitivo

Texto da legenda no ecrã (a fala fonética está em `oraculo/episodios/ep08_roteiro.json`):

- **gancho** (fora): Previ três coisas sobre o Mundial. Acertei duas. Nenhuma delas era o campeão.
- **arquivo** (dentro): Prestação de contas. Mundial trinta e dois, Standard, Top 8 de domingo.
- **prev01** (dentro): Previsão pública: Jund Sacrifice no Top 8. Um Jund chegou lá. Confirmada.
- **prev03** (dentro): Izzet Spellementals abaixo de cinco por cento. Zero jogadores em cento e vinte e oito. Confirmada.
- **prev02** (dentro): Jund entre os três mais jogados? Sétimo lugar, cinco vírgula cinco por cento. Refutada.
- **top8** (dentro): No Top 8, oito jogadores e oito decks diferentes.
- **campeao** (dentro): E o campeão é Stefan Schütz, da Áustria, com Izzet Mission. Dois jogadores em cento e vinte e oito levaram esse deck. A carta que dá nome a ele é de Star Trek e entrou no formato uma semana antes.
- **tese** (fora): No último episódio eu disse: os dados escolhem o deck, não quem pilota. No domingo, quem pilota escolheu um deck que os dados não viam. Placar: duas de três.
- **pergunta** (fora): Você levaria ao Mundial um deck que só dois jogadores levaram?
- **fecho** (fora): Probabilidade calculada. Humanos, imprevisíveis.

## Produção (16/11/2026)

- Roteiro definitivo: `ep08_roteiro.json` (160 palavras; texto = legenda, fala = grafia fonética). Diferenças face à proposta: o gancho diz «Nenhuma delas era o campeão»; o contador ERROS HUMANOS ficou de fora (sem valor registado, `comum/continuidade/tubo.md`); a REFUTADA da PR-WC32-02 sai com carimbo vermelho sem «Erro de sistema» (reservado a previsões públicas).
- Voz: ElevenLabs «Antonio de Jesus», eleven_v4, tomada 2 de 2 (flow `uOmbd2z44s77ysEx7pu6`, geração `P8i1X70szTFXue4174Mj`; 1.868 créditos nas duas). Scribe 160 = 160. Atempo 1,10.
- Pausas: 0,5/0,4/0,6 s depois dos carimbos, 0,3 s depois do Top 8, 0,6 s depois de «com Izzet Mission.» (corte seco de 0,8 s com aproximação lenta à foto), 1,0 s antes de sair do tubo, 0,3 s depois do placar.
- Cenas: arquivo (3 IDs) → PR-WC32-01 (cartas do Jund do Schnake, CONFIRMADA) → PR-WC32-03 («0», CONFIRMADA) → PR-WC32-02 (barras do metagame, Jund em 7.º, REFUTADA) → Top 8 (8 cartões) → campeão (foto, «2 / 128», lista de 60, Anthropological Mission) → fora: tese do EP07 riscada, placar 2/3, pergunta SIM/NÃO, assinatura e fecho do scanner.
- Easter egg: «MOCS» na chuva de código (~35–38 s).
- Capa (§7.3): «DECK DO CAMPEÃO» → **1,6%** → TUBO confiante + foto do campeão com selo «SÓ 2 EM 128 JOGARAM» → faixa «META EM CURTO · EP. 08 | PLACAR 2/3». Fundo: Ral, Anthropological Mission e Into the Flood Maw desfocadas.

## Controlo de qualidade (ficheiro final)

`comum/qc/qc_video.py --frente tubo`: 1080×1920, 30 fps, 62,73 s (58,87 s sem fecho), −14,0 LUFS, pico −1,8 dBTP, fecho presente a partir de 58,87 s, «sem problemas mensuráveis». Folha de contacto conferida a olho: sem texto cortado nas laterais, legendas legíveis, fontes ≥ 24 px.
Retenção: **quadro 0 sem carta (falha)**: abria com o TUBO e «3 PREVISÕES», contra a regra «quadro 0 com Magic» (constituição, 13/11); a revelação do campeão só entrava aos ~31 s. Resultado nas primeiras 6 h: 250 visualizações, tempo médio 7 s. Corrigido no MC-EP08B. Mudança visual ≤ 3 s e som em cada revelação cumpridos.

## Ficheiros finais

- Vídeo e capa: fora do Git (enviados ao fundador na conversa de 16/11). Recriar: pasta de trabalho com `voz.mp3` (tomada acima) e `ep08_words.json` como `words.json` → `python3 ep08_audio.py <kit>` → `python3 ep08_render.py <kit>` → `… capa`.
- Legenda, comentário fixado e texto alternativo: `legenda.txt`, `comentario_fixado.txt`, `texto_alternativo.txt` (nesta pasta).
- Fontes: `fontes.txt` (nesta pasta). Scripts e roteiro: `oraculo/episodios/ep08_*`.

## Antes de publicar

1. Ouvir a pronúncia de «Schütz» («Chúts»), «Izzet Mission» e «Spellementals».
2. Decidir o MC-EP06 («placar zero»), que continua aberto: com o EP08, a premissa dele (zero jogos no Sealed) caducou.

## Antes de produzir (proposta de 16/11, 00:53 · resolvido)

1. **Foto:** confirmar que é do Stefan Schütz e de onde veio (crédito). A magic.gg dá Schütz como campeão; o mtg.wiki diz Charis Kikidis (contradição; vale a fonte oficial). Os dois são da Team Handshake, por isso o casaco não basta para confirmar.
2. Artigo oficial da final (adversário e resultado) para a fala «vitória sem perder jogo», se for usada.
3. Listas: Schütz (Izzet Mission) e Schnake (Jund Sacrifice) via magic.gg/mtgtop8.
4. Autorização da voz (ElevenLabs, 2 tomadas).

## Fontes

- magic.gg/events/magic-world-championship-32 (campeão: «Mission Accomplished for World Champion Stefan Schütz»)
- magic.gg/news/magic-world-championship-32-top-8-players-and-decks
- magic.gg/news/magic-world-championship-32-standard-metagame-breakdown
- mtgtop8.com/event?e=93781&f=ST (listas do Top 8)

## Handoff

```
HANDOFF · 16/11/2026 ~01:50 Lisboa · Claude
Repositório: ibisson254/GERADOR-DE-VIDEO-BINDER · branch main · último commit: ver git log (conferido no remoto no fim da sessão)
Objetivo atual: MC-EP08 produzido e entregue ao fundador.
Conteúdos tocados: MC-EP08 · (novo) → CONCLUÍDO
Encerramento: MC-EP08 · memoria.py encerramento: OK · vídeo e capa: enviados ao fundador na conversa (não versionados)
Decisões: avançar apesar da pauta bloqueada (pedido explícito do fundador) e campeão pela fonte oficial (nucleo/DECISOES.md, 16/11: sim)
Documentos consultados: AGENTS.md, STATUS.md, oraculo/CICLO_SEMANAL.md, oraculo/CONTEXTO.md, oraculo/episodios/ep07_*, oraculo/esp02/*
Alterações: oraculo/previsoes/registo.yaml (conferências de 16/11 das PR-WC32-01..03 e PR-TRK-01..03), oraculo/ep08/*, oraculo/episodios/ep08_*, oraculo/autorizacoes/2026-11-16_ep08_foto_campeao.md, comum/REGISTRO_EDITORIAL.md, comum/historico.md, comum/easter_eggs.md, comum/continuidade/tubo.md, nucleo/DECISOES.md, STATUS.md
Tarefas pendentes: ouvir a pronúncia e publicar (fundador); decidir o MC-EP06 (fundador)
Próximo passo concreto: quinta 19/11 → `python3 -I oraculo/previsoes/ciclo.py quinta`
```
