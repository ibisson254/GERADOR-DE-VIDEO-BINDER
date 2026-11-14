# Ficha · Mana & Burn · EP10 · A febre do autógrafo (cartas especiais de Star Trek)

Estado (07/11/2026, 12h): **vídeo final renderizado e conferido; aguarda aprovação e publicação pelo fundador. Não publicado.** Vozes geradas com autorização do fundador ("Ok prossiga", 07/11, 11:52).

## Classificação
- Série: Mana & Burn · tarja "PLANTÃO DO PACOTE"
- Router: carta do set de Star Trek → Órbita *ou* série pelo ângulo (SHOWRUNNER §2.2). Ângulo = hype, coleção e reação da comunidade → território do Mana & Burn ("hype de sets", "reação da comunidade"). Pauta pedida pelo fundador na missão de 07/11.
- Classe: tendência / reação da comunidade + notícia (produto)
- Complexidade: média
- Estratégia (constituição §3): investigação aprofundada (2 fontes independentes por conclusão; opinião atribuída) + verificação rápida dos factos de produto na Wizards + Scryfall para a carta.

## Editorial
- Objetivo: respostas A/B no comentário fixado; levar quem vai ao pré-release a conhecer o BINDER Vision pelo fecho do scanner.
- Proposta de valor: o autógrafo que você sonha abrir no pré-release nem vem naquele pacote, e na mesa ele faz o mesmo que o Kirk comum.
- Público: jogador casual e de Commander no Brasil que vai ao pré-release desta semana (6–12/11).
- Tese: entrar no pré-release para jogar e sair a sonhar com a peça de coleção é humano; o humor é a febre, não o colecionador. Encantamento (assinatura real, menos de 250), surpresa (não sai em Play Booster; é a mesma carta do nº 142), humor (moldura comprada antes de abrir o pacote).
- Gancho (0–3 s): "Mano, hoje eu abro um Kirk assinado no pré-release. Tô sentindo!" com o Kirk assinado na TV.
- Pergunta (fala 13 = comentário fixado): "Autógrafo dentro do booster: A, genial. B, loteria."
- Hipótese a testar: pergunta A/B de opinião sobre o produto (não sobre a carta) gera mais respostas por 1.000 views que a do Ep. 9. Secundária: guardados (comentário com o que sai em cada booster).
- Território: sem preço (pré-venda instável), sem probabilidade inventada, sem nomes de atores, sem o Picard.

## Fontes
Ver `ficha_fontes.md`.

## Roteiro final (14 falas, bate-volta, Burn começa)
1. B [shouting] Mano, hoje eu abro um *Kirk assinado* no pré-release. Tô sentindo! · plano tv (carta 1701)
2. M [bored] Assinado à mão pelo ator. Sete cartas. Umas *250* de cada. · cuM
3. B [excited] *250* no planeta e uma vai brotar no *meu* pacote! · wide
4. M [deadpan] Lê a carta: *não tem texto*. Só o espaço da assinatura. · tvtext (destaque no painel prateado)
5. B [outraged] Então ela faz o quê na mesa?! · cuB
6. M [deadpan] O mesmo que o Kirk *nº 142*. Camisa autografada não faz gol. · wide + insert Kirk nº 142
7. B [shouting] Mas fica linda na parede! Já comprei até a *moldura*! · push
8. M [tired] Pré-release é *Play Booster*. Assinada só vem no *Collector*. · push
9. B [outraged] Seis pacotes de esperança e *zero* autógrafo?! · cuB
10. M [bored] Zero. Mas *Stardate* e *LCARS* saem no Play. Ilusão liberada. · cuM
11. B [shouting] E a internet rachou: uns acham *genial*, outros dizem que virou *loteria*! · tv2
12. M [deadpan] Na mesa, todo Kirk faz *igual*. Só um faz a mão *tremer*. · wide (veredito)
13. B Autógrafo dentro do booster: *A*, genial. *B*, loteria. · cuB (point_cam)
14. M [bored] Comenta aí. · cuM (remote; TV desliga)

Fórmula da bíblia: gancho (1) → o que a carta é + comparação do dia a dia ("camisa autografada não faz gol", 6) → "Lê a carta" com regra real (4: sem caixa de texto; 6: mesmo oracle do nº 142) → ferroada e pergunta (11–13). Os 8 blocos do brief cabem nas 14 falas sem forçar: gancho 1 · o que são 2 · Headliners 2–4 · comunidade 11 · colecionar × jogar 5–6, 12 · situação engraçada 3, 7, 9 · veredito 12 · pergunta 13.

Gíria: máx. 2 por fala (mano; brotar; rachou). Sem palavrão. Bordões "Lê a carta." e "Comenta aí." intactos. Fala que repetiria piada do Ep. 4 do Drive ("álbum da Copa", "central de atendimento") evitada.

## Produção
- Kit v2 de `manaburn/` sem alterações (cópia de trabalho fora do repositório). Episódio: `episode.json` (esquema 2) + `episode.js`.
- Cartas (PNG oficial, Scryfall, 744×1040): `cards/main.png` = Kirk nº 1701 (Chris Rallis); `cards/kirk142.png` = Kirk nº 142 (Jason Pastrana). Para renderizar, copiar para `manaburn/cards/`.
- Destaque (fala 4): painel prateado medido no PNG, [0,070; 0,661; 0,845; 0,152], zoom 1,5. Conferido na prévia (14,5 s).
- TV SAL: sem Salt Score (carta nova) → **Assinômetro 0%** ("no Play Booster · Wizards · 20/10/2026"): facto, não probabilidade. Placar "Assinadas no mundo < 1.750" (7 × menos de 250). 8 manchetes (factos citados: 2/2, 1 em 25 Play Boosters, mesma carta, atraso do Collector na Europa, 13/11). "Plantão do Pacote: atrasou, mas chegou" cumpre a promessa aberta do Zapping nº 1 (TV SAL, 25/10: "Ter 3/11, 21h: Plantão do Pacote").
- Easter egg: relógio da TV SAL em **17:01** = nº 1701 da carta (e NCC-1701). Implementado no `episode.js`, visível em todos os planos da TV na prévia. Regista-se em `comum/easter_eggs.md` quando o vídeo final for renderizado.
- Pôster: `mago` (nenhum pôster do kit é capitão).
- Vozes: ElevenLabs eleven_v4, flow "Mana & Burn — Ep. 10 (A febre do autógrafo)" (LIlbUJTIgrnM05abwheX). Burn: Talis (E9a8LlXPNWtyvvSoZzrb), 520 créditos; Mana: Erik (nfiLpQ54jEQninp3nNqL), 531 créditos; 1 geração cada (gerações G46TdgHaY91SCQJ6lM5J e j4XqZPtxSL8ssp9Y5ykj). Texto em `vozes_elevenlabs.txt`. Ritmo Burn ×1,06, Mana ×1,12, respiro 0,14 s. Sem transcrição Scribe (não pedida para gastar mais créditos): a pronúncia confere-se a ouvir. Grafias: pré-relíse, Plêi Búster, Colétor, Stardêite, Él-cars, búster, "Á, genial. Bê, loteria", números por extenso no feminino ("duzentas e cinquenta").
- Fecho: `juntar_fecho.py` (cópia do Ep. 9 + limitador de pico depois do fade) + `comum/outro/outro_binder_916.mp4`.

## QC da prévia sem vozes (07/11/2026, ficheiro `PREVIA_Ep10_com_fecho.mp4`, não publicável)
Vozes substituídas por faixas de marcação com a duração estimada de cada fala; o áudio da prévia é só a trilha. Serve para conferir imagem, ritmo dos planos e bordas, não a mistura final.

| Critério | Alvo | Medido | OK |
|---|---|---|---|
| Resolução / fps | 1080×1920, 30 | 1080×1920, 30 | sim |
| Duração | livre | 51,0 s + fecho 3,87 s = 54,9 s (estimada; muda com as vozes) | — |
| Bordas da TV (`bordas.py`) | laterais 0–1080, topo ≥ 295 | 366 quadros de TV, laterais 10–1068 px, topo 300 px · OK | sim |
| cropdetect (0–50 s) | 1080:1920:0:0 | 1503/1503 quadros | sim |
| Fecho do scanner | presente | presente a partir de 51,0 s (dif. 0,07) | sim |
| Loudness / pico (só trilha) | −14 LUFS, < −1 dBTP | −14,3 LUFS, −1,6 dBTP (depois do limitador; antes −0,2 → corrigido) | sim (prévia) |
| Carta inteira, rodapé visível, nada por cima | — | conferido a 2,0 / 14,5 / 39,5 s e na folha de contacto | sim |
| Destaque alinhado | painel da assinatura | 14,5 s: retângulo amarelo sobre o painel | sim |
| Insert Kirk 142 | PNG real + crédito | 21 s: carta inteira, crédito "Na tela:" no topo | sim |
| Medidor com conta e fonte | todas as tomadas da TV | 2 / 14,5 / 39,5 s | sim (corrigida a 1.ª linha da conta, que saía da TV) |
| Legenda na zona segura | fora do vermelho | folha de contacto | sim |
| P2 | plano parado > 5 s | fala 2 (cuM, ~4,9 s na estimativa) | aceitável; rever com as vozes |

Não testado (depende das vozes): sincronização das falas, mistura a −14 LUFS com voz, "Comenta aí" na parada seca, duração real.

## QC do ficheiro final (07/11/2026, `ManaBurn_Ep10_CartasEspeciais_916.mp4`)
| Critério | Alvo | Medido | OK |
|---|---|---|---|
| Resolução / fps | 1080×1920, 30 | 1080×1920, 30 | sim |
| Duração | livre | 47,67 s + fecho 3,87 s = 51,53 s | sim |
| Cortes do `process.py` | 14 falas | 14 trechos com durações coerentes com o texto (Burn 0,03–27,37 s; Mana 0,10–33,58 s) | sim |
| Loudness / pico | −14 LUFS, < −1 dBTP | −14,5 LUFS, −1,7 dBTP | sim |
| cropdetect (0–47 s) | 1080:1920:0:0 | 1413/1413 quadros | sim |
| Bordas da TV (`bordas.py`) | laterais 0–1080, topo ≥ 295 | 337 quadros, 10–1068 px, topo 300 px · OK | sim |
| Fecho do scanner | presente, inteiro | a partir de 47,67 s (dif. 0,07), 3,87 s | sim |
| "Comenta aí" → pancada | parada seca | "Comenta aí" 46,10 s; TV desliga 47,35 s (tempos do kit) | sim |
| Carta inteira, destaque, insert, medidor, tarja, legenda na zona segura | — | quadros 2,0 / 13,6 / 19,5 / 36,0 / 46,4 / 47,5 / 49,0 s + folha de contacto | sim |
| `qc_video.py` | sem P0/P1 | "Sem problemas mensuráveis" | sim |

## Entregáveis
- [x] Roteiro · [x] episode.json/js · [x] Cartas · [x] Legenda (671 caracteres) · [x] Comentário fixado (967) · [x] Texto alternativo · [x] Fontes · [x] Prévia e capa provisória (fora do repositório)
- [x] Vozes · [x] Vídeo final (fora do repositório) · [x] Capa (2,5 s, fala 1) · [x] QC do ficheiro final

## Capa no modelo fixo (14/11/2026)
`MB_EP10_CAPA.png` (+ `_grelha.png`), gerada com `manaburn/capas/capa_mb.py --carta cards/main.png --frase "Kirk assinado no pré-release?" --foco ZERO --selo "Só no Collector" --ep 10 --tag "Star Trek"`. Substitui a capa de quadro do vídeo (PERFIL, secção «Capa»). Foco = fala 9 (zero autógrafo no Play Booster); selo = fala 8. Crédito da carta (Chris Rallis) já na legenda.

## Depende do fundador
1. Ouvir a pronúncia ("pré-release", "Play Booster", "Collector", "Stardate", "LCARS") e aprovar o vídeo; publicar.
2. Confirmar que o Ep. 4 do Drive ("Autógrafos de Star Trek", Kirk 1701) não foi publicado; o tema toca no mesmo produto (ângulo novo, piadas diferentes).
3. Aprovar o uso da tarja "PLANTÃO DO PACOTE" para cumprir a promessa do Zapping nº 1.

## Depois de publicar
- Métrica principal: respostas A/B por 1.000 views. Secundária: guardados.
- Resultado observado: —
- Aprendizagem: —
