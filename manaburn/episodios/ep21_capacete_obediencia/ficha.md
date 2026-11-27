# Ficha · Mana & Burn · EP21 · «O Capacete Que Nunca Para» (Helm of Obedience + Rest in Peace)

## Identificação
- ID editorial: MB-EP21
- Estado no registo: CONCLUÍDO (ver «Controlo de qualidade»); à espera de publicação pelo fundador
- Pedido do fundador: «faça um episódio inspirado nesse» com o Reel https://www.instagram.com/reel/DRF269kE1bZ/ (27/11/2026, 18:00, na conversa do MB-EP18; encaminhado pelo coordenador do projeto claude.ai).
- Inspirado = formato e ideia, não o conteúdo: o Reel de referência explica em 44 s um combo de duas cartas (Helm of Obedience + Rest in Peace) com a estrutura «o que precisa → como funciona» e memes de terceiros. Aqui fica o combo e a promessa («duas cartas que acabam com o grimório»); roteiro, correções, telas, piadas e personagens são do Mana & Burn, sem memes nem imagens do Reel.
- O Instagram não abre por automação: o Reel foi visto pelo vidIQ (`vidiq_watch_shortform_content`, 10 créditos, 27/11/2026), porque sem isso não havia pauta (SHOWRUNNER §2.4 passo 8).

## Classificação
- Frente: Mana & Burn (série) · formato base 14 falas, Commander · padrão «Episódio de combo» (`manaburn/PERFIL.md`, 26/11/2026)
- Porquê esta frente: combo curioso de duas cartas com regras que a mesa erra = território «cultura e caos» do Mana & Burn; não é torneio nem metagame (TUBO), e não se sobrepõe ao episódio do TUBO em produção noutra conversa.
- Classe: leitura de carta / combo (Oracle + rulings + Commander Spellbook/EDHREC com data + Regras Completas)
- Complexidade: média (efeito de substituição, «até que», ação baseada em estado na compra)

## Originalidade
- `python3 comum/ferramentas/memoria.py pauta --objeto "Helm of Obedience; Rest in Peace" --tema "combo de duas cartas que exila o grimório inteiro de um oponente (efeito de substituição faz o Helm nunca parar)"` → **PAUTA BLOQUEADA** (27/11/2026): `BLOQUEIA MB-EP19 [CONCLUÍDO] Mana & Burn: mesmo objeto ("Rest in Peace" ~ "Rest in Peace (exemplo de resposta)")`.
- Comparação manual: no MB-EP19 a Rest in Peace aparece numa fala como **resposta** ao combo do robô (exílio em vez de morte). Aqui é **peça do combo**; objeto principal (Helm), tese (o processo nunca para), mecânica (efeito de substituição + moer), cor (branco + incolor) e vitória (grimório vazio) são diferentes. Nenhuma linha do registo com Helm of Obedience.
- **Liberada pelo fundador** no cartão de decisão: «Avançar com Helm + RiP» (27/11/2026, 18:10); registada em `nucleo/DECISOES.md` (27/11/2026, 18:10).
- Relações: MB-EP19 (a mesma Rest in Peace, agora do outro lado: fala 7 faz a ponte), MB-EP13 (deck que esvazia o próprio grimório; aqui é o do oponente), MB-EP18/EP20 (mesmo padrão de combo, outra mecânica).

## Análise comparativa (método de 21/11)
- Referências: MB-EP13 (publicado 20/11, orgânico; 19.688 views, 361 guardados, 282 partilhas, 43 comentários em 2 d 9 h, `comum/insights/registo_posts.csv`) e MB-EP15 (publicado, 1.911 views no print de 21/11, orgânico). MB-EP18, EP19 e EP20 ainda sem dados (não publicados).
- Facto observado: o melhor orgânico da conta é um combo explicado passo a passo (MB-EP13).
- Interpretação: guarda-se e partilha-se a explicação de algo que parece impossível; não há retenção por segundo.
- **Hipótese (MB-EP21):** um combo de duas cartas cuja graça é uma **regra contraintuitiva** («X = 1 e mesmo assim tudo») e que já circula como Reel viral noutra conta mantém guardados e partilhas no nível do MB-EP13. Medir às 48 h e aos 7 dias contra MB-EP13 e MB-EP19, sem impulso.

## Pesquisa de pauta (§2.4)
O tema veio do fundador (o Reel): comparam-se 2 ângulos do mesmo objeto.

| Ângulo | Tese | Correções do Mana | Visual | Escolha |
|---|---|---|---|---|
| **A · «X = 1 e some tudo»** (VENCEDOR) | O Helm para quando a carta *chega* ao cemitério; com a Rest in Peace nenhuma chega, e a ruling confirma: grimório inteiro mesmo com X = 1 | (1) o Helm para pela chegada ao cemitério, não pelo número moído; (2) grimório vazio não perde na hora (704.5b); (3) um oponente por ativação e o Helm vira; (4) a mesa responde tirando a RiP | carta de 1996 + Oracle atual + ruling + grimório 60 → 0 | escolhido: paga o gancho com a ruling oficial e dá 3+ correções reais |
| B · «Qual peça de exílio usar» (Rest in Peace × Leyline of the Void × Dauthi Voidwalker) | Três cartas fazem o mesmo combo, com custos e riscos diferentes | menos regras, mais comparação de cartas | três cartas lado a lado | reserva: vira lista, perde o «isso funciona?!»; Leyline e Dauthi ficam para o comentário se o fundador quiser |

Escuta: o radar `comum/radar/2026-W48.md` (válido até 03–06/12) não tinha linha deste combo; acrescentada a linha 12 (EUA/global, EDHREC + Commander Spellbook). Brasil e Europa continuam sem dado sobre o combo nesta sessão (LigaMagic/MYP com anti-robô); a prova de interesse é o próprio Reel enviado pelo fundador (contagens não visíveis pelo vidIQ).

## Gancho visual (7 campos)
| # | Campo | MB-EP21 |
|---|---|---|
| 1 | Quadro 0 | Helm of Obedience (Alliances 1996) inteiro em tela cheia, linha «X, {T}: Put the top card of target opponent's library…» destacada, selo «1 MANA → TUDO» no céu amarelo da arte |
| 2 | Objeto | o capacete da arte (carta real, PNG do Scryfall) |
| 3 | Ação | entrada com escala 1,06 → 1 e tremor; voa para a TV SAL |
| 4 | Som | pancada + pop; zap de canal na saída |
| 5 | Descoberta até 3 s | «Paga UMA mana… e o oponente perde o grimório INTEIRO!» |
| 6 | Promessa | perceber como uma mana apaga um grimório inteiro, e se isso ganha o jogo |
| 7 | Pagamento | fala 8 (~24–30 s na prévia): ruling «entire library… even if X is 1» e grimório 60 → 0 |

## Roteiro (v1, 27/11/2026)
| # | Quem | Fala | Tela |
|---|---|---|---|
| 1 | Burn | Paga UMA mana… e o oponente perde o grimório INTEIRO! | abertura → TV: Helm + «1 MANA» |
| 2 | Mana | É o Helm of Obedience. Paga X e vira: o oponente mói até X cartas chegarem ao cemitério. | prova: Helm, linha da ativação → linha do «até» |
| 3 | Burn | Então com X igual a um, mói uma e acabou! Que capacete fraco! | rosto |
| 4 | Mana | Lê a carta. Ele para quando a carta chega ao cemitério. E se nenhuma chegar? | prova: Helm + painel «ORACLE ATUAL» |
| 5 | Burn | Como assim nenhuma? Moeu, caiu no cemitério, gênio! | rosto |
| 6 | Mana | Não com Rest in Peace. Tudo que iria pro cemitério vai pro exílio. | prova: Rest in Peace, linha do exílio |
| 7 | Burn | A mesma Rest in Peace que parou o robô?! | TV: capa do MB-EP19 + RiP |
| 8 | Mana | Ela mesma. Nenhuma carta chega, e o capacete nunca para. Tá na ruling: grimório inteiro, mesmo com X igual a um. | prova: ruling → grimório 60 → 0 |
| 9 | Burn | Grimório zerado! Ganhei, mano! | rosto |
| 10 | Mana | Ainda não. Ele só perde quando tiver que comprar e não tiver carta. | prova: regra 704.5b |
| 11 | Burn | Tá, então faço na mesa inteira, de uma vez! | rosto |
| 12 | Mana | Um oponente por vez, e o capacete vira: numa mesa de quatro, três voltas. E a mesa responde tirando a Rest in Peace. | prova: mesa de 4 (EXEMPLO) → «mói 1 e para» |
| 13 | Burn | Pergunta: sem Rest in Peace, X igual a três, e a primeira carta é uma criatura. Ele mói A, uma, ou B, três? | TV: A/B |
| 14 | Mana | Comenta aí. | — |

Pergunta final: de **conta** (o MB-EP20 foi de ação). Resposta no comentário fixado: A (a criatura para o processo e é roubada).

## Revisão narrativa (§4.2)
| Critério | MB-EP21 |
|---|---|
| Tese | «Com a Rest in Peace, X = 1 basta: nenhuma carta chega ao cemitério e o Helm exila o grimório inteiro, mas isso ainda não é vitória.» |
| Originalidade | bloqueio por palavra liberado pelo fundador (27/11/2026, 18:10) |
| Clareza | carta + número no quadro 0; «grimório inteiro» dito até ~3 s |
| Progressão | peça 1 → engano do Burn → regra do «até» → peça 2 → ponte EP19 → ruling (pagamento) → engano «ganhei» → 704.5b → engano «mesa inteira» → um por vez + resposta → pergunta |
| Evidência | cada fala de prova com carta, Oracle, ruling ou regra citada no ecrã |
| Ritmo | a medir na prévia (folha de contacto) |
| Recompensa | fala 8 |
| CTA | pergunta A/B; app: exportar coleção para a LigaMagic (ANUNCIÁVEL, CTA diferente do MB-EP20) |

## Auditoria técnica do combo (27/11/2026)
- Oracle do Helm: «{X}, {T}: Target opponent mills a card, then repeats this process until a creature card or X cards have been put into their graveyard this way, whichever comes first. If one or more creature cards were put into that graveyard this way, sacrifice this artifact and put one of them onto the battlefield under your control. X can't be 0.»
- Ruling (01/10/2008): efeito como o da Leyline of the Void → o processo nunca para; grimório inteiro exilado mesmo com X = 1.
- Rest in Peace: substituição «exile it instead» para qualquer cemitério (também o do controlador).
- 704.5b: perde quem tentou comprar de grimório vazio. Não é vitória imediata.
- Um alvo por ativação e custo {T}: uma ativação por desvirar. «Três voltas» para 3 oponentes sem desviradores (marcado EXEMPLO).
- Interrupção: tirar a RiP em resposta (o Helm mói 1 e para com X = 1); destruir o Helm em resposta não impede a habilidade na pilha (113.7a). Não é «impossível de parar».
- Commander Spellbook 3002-5065: «Exile target opponent's library» (o próprio Spellbook não chama vitória). Popularidade 4.387 listas.
- Salt do Helm 0,60 → putômetro 15 % (EDHREC, 27/11/2026).

## Produção
- Kit Mana & Burn v3 com abertura de carta, plano de prova, quadro do Conde e TV acesa no quadro 0; cópia de trabalho fora do repositório.
- Telas: `telas_capacete.py` (12 telas, CSS do MB-EP19). Capa: `capas/capa_mb.py --carta helm.png --frase "Uma mana e some o grimório" --foco INTEIRO --selo "SÓ X = 1" --selo-y 420 --ep 21 --tag Commander`.
- Prévia sem voz: `python3 previa_sem_voz.py` → `render.py` → `juntar_fecho.py` com `comum/outro/outro_binder_916.mp4`. 0 créditos.
- Vozes: autorizadas pelo fundador (cartão da prévia + «Prossiga», 27/11/2026 18:16). ElevenLabs eleven_v4, flow «Mana & Burn — MB-EP21 (O Capacete Que Nunca Para)» (`7irp5GgIqRugB1Fjgq1p`). Burn: Talis (`E9a8LlXPNWtyvvSoZzrb`), 547 créditos, 28,9 s. Mana: Erik (`nfiLpQ54jEQninp3nNqL`), 687 créditos, 37,4 s. **Total 1.234 créditos**, uma geração cada, sem repetição; IDs confirmados no `creative_list_voices`. Texto das faixas: `faixas_elevenlabs.txt`. Corte pelo `tts` (`processar_vozes.py`).

## Controlo de qualidade (ficheiro final, 27/11/2026)
- `qc_video.py --frente manaburn`: 1080x1920, 30 fps, **54,37 s** (50,5 s + fecho do scanner a partir de 50,5 s, dif. 0,07), **−14,9 LUFS**, pico −1,4 dBTP, **sem problemas mensuráveis**. `bordas.py` OK (1.136 quadros de TV, laterais 58–804 px). `check_quadro.py` OK (trocas do Conde em cortes).
- Retenção: quadro 0 com a carta inteira e o selo (sim); mudança visual ≤ 3 s (cortes, aproximações, flips e trocas a meio; o maior intervalo sem corte de plano, 24,1–29,6 s, tem 3 telas: ruling → «MÓI 1…» → «MÓI TUDO»); som em cada revelação (pancada, flips, destaques, zaps).
- Abertura: sai a 1,02 s (fração 0,36 da 1.ª fala), depois de «Paga UMA mana».
- Pagamento do gancho: **24,1–29,5 s** (ruling + grimório 60 → 0), como previsto no campo 7.
- Rubrica medida (folha de contacto sem som): relevância 5 · impacto 4 · clareza 4 · curiosidade 4 · pagamento 5 · identidade 5. Sem P0/P1.

## Ficheiros finais
- Vídeo: `/mnt/project-files/manaburn/ep21/ManaBurn_Ep21_CapaceteInfinito_916.mp4` (não versionado). Prévia sem voz e faixas MP3 na mesma pasta.
- Capa: `MB_EP21_CAPA.png` (+ `_grelha`) nesta pasta e na pasta do projeto. Folha de contacto: `folha_contacto_final.png`.

## Pacote de publicação
`legenda.txt`, `comentario_fixado.txt`, `texto_alternativo.txt`, `fontes.md`. UTM: `utm_campaign=MB-EP21`. Não publicar no mesmo dia do MB-EP19 (mesma Rest in Peace) nem do MB-EP20.

## Encerramento
- [x] Briefing e roteiro na ficha · [x] legenda, comentário fixado, texto alternativo · [x] fontes · [x] QC · [x] ficheiros finais
- [x] `comum/REGISTRO_EDITORIAL.md` (CONCLUÍDO) · [x] `comum/historico.md` · [x] radar W48 (linha 12) · [x] `nucleo/DECISOES.md` (pauta liberada) · [x] `STATUS.md`
- [x] `memoria.py encerramento MB-EP21`, `validar`, `validar_repo.py` · [x] commit na `main` conferido (hash no handoff)

## Handoff
Ver o fim do `STATUS.md` e a mensagem da sessão; resumo: MB-EP21 CONCLUÍDO a 27/11/2026 (~18h45 UTC), 1.234 créditos de voz, vídeo na pasta do projeto, à espera de publicação. Episódio inspirado num Reel visto pelo vidIQ (10 créditos). Pendente do fundador: escuta e publicação.
