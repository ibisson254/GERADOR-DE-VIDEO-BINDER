# Ficha · Mana & Burn · EP22 · «A Fada Infinita» (Splinter Twin + Pestermite)

## Identificação
- ID editorial: MB-EP22
- Estado no registo: PUBLICADO (regra de 28/11/2026: vozes autorizadas = publicado; `eventos.py vozes`, 28/11/2026 09:24); data real do post por confirmar
- Pedido do fundador (28/11/2026, 08:55–08:57): análise de desempenho com a fórmula «uma carta, um combo, um número no hook» e a ideia «Combo de duas cartas que fecha no turno 4» (sugestão: Kiki-Jiki + Pestermite); «Produza o próximo episódio».

## Classificação
- Frente: Mana & Burn · formato base 14 falas · padrão «Episódio de combo» (`manaburn/PERFIL.md`, 26/11/2026)
- Classe: leitura de carta / combo + notícia (banimento e liberação no Modern, com data)
- Complexidade: média (cópia de criatura, gatilho de entrada, ímpeto, pilha)

## Originalidade
- `python3 comum/ferramentas/memoria.py pauta --objeto "Kiki-Jiki, Mirror Breaker + Pestermite" --tema "combo de duas cartas, criaturas infinitas com pressa no turno 4"` → **PAUTA LIVRE** (28/11/2026). Nenhuma linha do registo com Splinter Twin, Pestermite ou Kiki-Jiki.
- Comparação manual com os combos já feitos: MB-EP13 (limite de mão + descarte), EP18 (fichas + drenagem por entrada; aqui as fichas ganham no **ataque**, com ímpeto, e o motor é **cópia + desvirar**), EP19 (undying), EP20 (mana incolor + cópia de habilidade), EP21 (moer + substituição). Cores novas no padrão de combo (azul + vermelho).

## Análise comparativa (método de 21/11)
- Dados trazidos pelo fundador (análise externa, 28/11/2026; mediana dos últimos 12 Reels 1,45 mil plays): «97 terrenos / turno 5» (MB-EP13) 25,2 mil = 17,4× a mediana; «mata com matemática» 13,3 mil = 9,2×; react Vingadora (MB-EP17) 4,8 mil = 3,3×; parceria e torneio abaixo da mediana (0,47× e 0,62×). Fonte: mensagem do fundador; não conferido nos Insights nesta sessão (vidIQ sem a conta ligada).
- Facto observado: os dois maiores têm número absurdo + condição de vitória no texto do gancho.
- Interpretação: o número do turno («turno 5») funciona como promessa de velocidade e de vitória.
- **Hipótese (MB-EP22):** «DUAS cartas… no turno QUATRO… fadas INFINITAS» (número + turno + vitória no quadro 0) repete o molde do MB-EP13; medir plays, guardados e partilhas às 48 h e aos 7 dias contra MB-EP13 e MB-EP21, sem impulso.

## Pesquisa de pauta (§2.4)
Tema do fundador: comparam-se 2 ângulos do mesmo objeto (combo de duas cartas com Pestermite que ganha no turno 4).

| Ângulo | Tese | Turno 4? | Correções do Mana | Escolha |
|---|---|---|---|---|
| **A · Splinter Twin + Pestermite** (VENCEDOR) | Pestermite no turno 3 (3 manas), Twin no turno 4 (4 manas): fadas infinitas com ímpeto; a carta que a mesa queria banir **foi** banida (Modern, 2016) e liberada (16/12/2024) | **sim, sem acelerar mana** | (1) qualquer permanente; (2) a ficha tem ímpeto; (3) a ficha não copia a Aura (ruling); (4) já foi banida e voltou; (5) para em resposta (ruling: sai uma ficha só) | escolhido: o «turno 4» é verdadeiro sem asteriscos e o «isso devia ser banido» do Burn tem resposta real com data |
| B · Kiki-Jiki + Pestermite (ideia original) | O Kiki copia a Pestermite, que desvira o Kiki | só com aceleração (Kiki custa {2}{R}{R}{R}) | (1)–(3) parecidas; sem a história do banimento | reserva: fica como variante no comentário fixado e numa manchete |

Escuta: radar `comum/radar/2026-W48.md` sem linha deste combo; acrescentada a linha 16 (EUA/global). Brasil e Europa sem dado nesta sessão.

## Gancho visual (7 campos)
| # | Campo | MB-EP22 |
|---|---|---|
| 1 | Quadro 0 | Splinter Twin inteira em tela cheia, linha «Enchanted creature has "{T}: Put a token that's a copy…"» destacada, selo «2 CARTAS · TURNO 4» no fundo da arte (acima das cabeças) |
| 2 | Objeto | a carta (PNG do Scryfall) |
| 3 | Ação | escala 1,06 → 1 com tremor; voa para a TV SAL, que mostra Pestermite + Twin com «2 CARTAS / TURNO 4» |
| 4 | Som | pancada + pop; zap de canal na saída |
| 5 | Descoberta até 3 s | «DUAS cartas… e no turno QUATRO você tem fadas INFINITAS!» |
| 6 | Promessa | perceber como duas cartas fazem fadas infinitas, e se isso ganha |
| 7 | Pagamento | falas 6–9 (~18–33 s na prévia): loop em 3 passos, ruling, conta 1, 2, 3…, mesa 40 → 0 |

## Roteiro (v2, 28/11/2026, 09h30)
v1 tinha ~48 s de falas (52 s com o fecho). O fundador pediu (09:16) melhor hierarquia visual e duração ideal: v2 corta palavras em todas as falas, mantém as 14 falas e as 5 correções, e mira ~39 s de falas (~43 s com o fecho), abaixo do MB-EP13 (45,8 s), o melhor orgânico. Telas refeitas com 3 níveis (título gigante, uma linha de apoio, fonte curta), o crédito completo só na tarja do topo, e plano de prova a 690 px (padrão 620) para ler melhor no telemóvel.

| # | Quem | Fala | Tela |
|---|---|---|---|
| 1 | Burn | DUAS cartas… e no turno QUATRO você tem fadas INFINITAS! | abertura (Twin) → TV: as duas cartas |
| 2 | Mana | Pestermite: três manas. Quando entra, vira ou desvira uma permanente. | prova: Pestermite, linha do gatilho |
| 3 | Burn | Desvirar terreno? Grande coisa! | rosto |
| 4 | Mana | Lê a carta: qualquer permanente. No turno quatro, Splinter Twin nela. | prova: «target permanent» → painel T3 / T4 «SEM RAMP» |
| 5 | Burn | A cópia nasce enjoada, mano! | rosto |
| 6 | Mana | Tem ímpeto. E entra como Pestermite: desvira a original. | prova: Twin, linha do ímpeto → loop em 3 passos |
| 7 | Burn | Então a cópia também tem a Twin! | rosto |
| 8 | Mana | Não. A ruling diz: não copia a Aura. A original vira e desvira: uma fada por volta. | prova: «NÃO COPIA A AURA» → «1, 2, 3…» |
| 9 | Burn | Fada infinita com ímpeto! Isso devia ser BANIDO! | TV: mesa de 4 (EXEMPLO) 40 → 0, 60 fadas |
| 10 | Mana | Já foi, no Modern, em 2016. E liberaram em 2024. | prova: banida/liberada → «AGORA ESTÁ LIVRE» |
| 11 | Burn | E ninguém para isso! | rosto |
| 12 | Mana | Para: mata a Pestermite em resposta e o loop acaba. | prova: Pestermite destruída, «1 FICHA E PARA» |
| 13 | Burn | Pergunta: A, bane de novo. B, deixa solta. | TV: A/B no Modern |
| 14 | Mana | Comenta aí. | — |

Pergunta final: de **ação/opinião** (o MB-EP21 foi de conta). Resposta e passo a passo no comentário fixado.

## Revisão narrativa (§4.2)
| Critério | MB-EP22 |
|---|---|
| Tese | «Twin + Pestermite fecha no turno 4 sem acelerar mana: a cópia com ímpeto desvira a original, uma fada por volta; a mesa só para em resposta.» |
| Originalidade | pauta livre (28/11/2026) |
| Clareza | as duas cartas + «turno 4» no quadro 0 e na 1.ª tela da TV |
| Progressão | peça 1 → engano (só terreno) → turno 4 + peça 2 → engano (enjoo) → loop → engano (quadrado) → ruling (pagamento) → vitória → «devia ser banido» → já foi → engano (ninguém para) → resposta → pergunta |
| Evidência | carta, Oracle, ruling ou anúncio da Wizards em cada fala de prova |
| Recompensa | falas 8–10 |
| CTA | Radar do app («jogadores perto de você», ANUNCIÁVEL desde 23/11), diferente do MB-EP21 (LigaMagic) |

## Auditoria técnica do combo (28/11/2026)
- Oracle da Twin: «Enchant creature / Enchanted creature has "{T}: Create a token that's a copy of this creature, except it has haste. Exile that token at the beginning of the next end step."» Custo {2}{R}{R}.
- Oracle da Pestermite: «Flash / Flying / When this creature enters, you may tap or untap target permanent.» {2}{U}, 2/1. O «may» torna o loop opcional; o jogador escolhe quantas vezes repete.
- Ruling da Twin (15/06/2010): a ficha não copia Auras nem a habilidade dada pela Twin; se a criatura encantada sai antes de a habilidade resolver, a ficha é criada na mesma.
- Turno 4: a Pestermite entra no turno 3 (ou com lampejo no fim do turno do oponente) e está sob controlo desde o início do turno 4, por isso pode usar {T}. Sem aceleração de mana.
- Vitória (EXEMPLO): fichas 2/1 com voar e ímpeto; 3 oponentes × 40 = 120 = 60 fadas, sem bloqueadores voadores. As fichas são exiladas na próxima etapa final.
- Interrupção: matar a Pestermite com a habilidade na pilha; anular ou destruir a Twin. Não é «impossível de parar».
- Legalidade: Commander e Modern (Scryfall). Banida no Modern em 2016 e liberada a 16/12/2024 (anúncio da Wizards).
- Salt da Twin 0,47 → putômetro 12 % (EDHREC, 28/11/2026).

## Produção
- Kit Mana & Burn v3 (abertura de carta, plano de prova, quadro do Conde, TV acesa no quadro 0); cópia de trabalho fora do repositório.
- Telas: `telas_fada.py` (13 telas, CSS do MB-EP21). Capa: `capas/capa_mb.py --carta twin.png --frase "Duas cartas, turno 4" --foco INFINITAS --selo LIBERADA --selo-y 440 --ep 22 --tag Commander`.
- Prévia sem voz: `python3 previa_sem_voz.py` → `bordas.py` → `render.py` → `juntar_fecho.py` com `comum/outro/outro_binder_916.mp4`. 0 créditos.
- Prévia v1 (52 s) → pedido do fundador (09:16) de melhor hierarquia visual e duração → prévia v2 (43 s), ver «Roteiro (v2)» e `nucleo/DECISOES.md` (28/11/2026, 09:30).
- Vozes: autorizadas pelo fundador («Pode / E gerar as vezes», 28/11/2026 09:24, sobre a prévia v2). ElevenLabs eleven_v4, flow «Mana & Burn — MB-EP22 (A Fada Infinita)» (`kRV3pzyFilWsSXPdZZme`). Burn: Talis (`E9a8LlXPNWtyvvSoZzrb`), 419 créditos, 22,7 s. Mana: Erik (`nfiLpQ54jEQninp3nNqL`), 575 créditos, 33,5 s. **Total 994 créditos**, uma geração cada, sem repetição; IDs confirmados no `creative_list_voices`. Texto: `faixas_elevenlabs.txt`. Corte pelo `tts` (`processar_vozes.py`): 7 + 7 cortes conferidos.
- Easter egg: relógio da TV SAL em «20:16» = ano do banimento da Splinter Twin no Modern.

## Controlo de qualidade (ficheiro final, 28/11/2026)
- `qc_video.py --frente manaburn`: 1080x1920, 30 fps, **42,63 s** (38,77 s + fecho do scanner, dif. 0,07), **−14,9 LUFS**, pico −1,4 dBTP, **sem problemas mensuráveis**. `bordas.py` OK.
- Retenção: quadro 0 com a carta inteira e o selo; mudança visual ≤ 3 s exceto 4–7,9 s (Pestermite inteira → aproximação com destaque e faixa, um só plano de prova; a aproximação conta como renovação); som em cada revelação.
- Abertura: sai a ~2,0 s (fração 0,6 da 1.ª fala), depois de «turno QUATRO».
- Pagamento do gancho: 15,3–26,8 s (loop em 3 passos → ruling → «1, 2, 3…» → mesa 40 → 0).
- Folha de contacto: `folha_contacto_final.png`. Sem P0/P1.

## Ficheiros finais
- Vídeo: `/mnt/project-files/manaburn/ep22/ManaBurn_Ep22_FadaInfinita_916.mp4` (não versionado). Prévia sem voz e faixas MP3 na mesma pasta.
- Capa: `MB_EP22_CAPA.png` (+ `_grelha`) nesta pasta e na pasta do projeto.

## Pacote de publicação
`legenda.txt`, `comentario_fixado.txt`, `texto_alternativo.txt`, `fontes.md`. UTM: `utm_campaign=MB-EP22`.

## Encerramento
- [x] Briefing, pesquisa e roteiro na ficha · [x] legenda, comentário fixado, texto alternativo · [x] fontes · [x] QC · [x] ficheiros finais
- [x] `comum/REGISTRO_EDITORIAL.md` (PUBLICADO por `eventos.py vozes`) · [x] `comum/historico.md` · [x] radar W48 (linha 16) · [x] easter egg · [x] `nucleo/DECISOES.md` (telas v2 e 690 px) · [x] `STATUS.md`
- [ ] Aprovação final do fundador (linha «Aprovação final: <nome> · <data>») para o `eventos.py concluir MB-EP22` gravar o evento do Data Binder

## Handoff
MB-EP22 feito a 28/11/2026 (~09h45 Lisboa), 994 créditos de voz; vídeo na pasta do projeto. Pendente do fundador: publicar, escrever a aprovação final na ficha (depois `eventos.py concluir MB-EP22 --qc <qc.json>`) e as métricas às 48 h e 7 dias contra MB-EP13.
