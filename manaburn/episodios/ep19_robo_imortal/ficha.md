# Ficha · Mana & Burn · EP19 · «O Robô Que Não Morre» (Mikaeus, the Unhallowed + Triskelion)

## Identificação
- ID editorial: MB-EP19
- Estado no registo: CONCLUÍDO (ver «Controlo de qualidade»)
- Aprovação do fundador: missão «PROMPT DE ENGENHARIA AVANÇADA — MANA & BURN · CONSOLIDAR A FÓRMULA DOS COMBOS + PRODUZIR DOIS REELS EM PARALELO» (projeto claude.ai, 26/11/2026 21:02), que pede um segundo episódio de combo escolhido pela sessão; **vozes autorizadas** no cartão de decisão da mesma sessão (≈ 21:05: «Sim, autorizo»), uma geração por personagem.
- Primeira aplicação do padrão «Episódio de combo» (`manaburn/PERFIL.md`, decisão de 26/11/2026 21h em `nucleo/DECISOES.md`).

## Classificação
- Frente: Mana & Burn (série) · formato base 14 falas, Commander
- Classe: leitura de carta / combo (Oracle + rulings + Commander Spellbook/EDHREC com data)
- Complexidade: média (gatilho de morte, marcadores como custo, ação baseada em estado)
- Estratégia: «isso funciona mesmo?!» com recompensa visível; o Mana desfaz três enganos reais da mesa

## Originalidade
- Objeto: Mikaeus, the Unhallowed + Triskelion (+ Rest in Peace como exemplo de resposta)
- `python3 comum/ferramentas/memoria.py pauta --objeto "Mikaeus, the Unhallowed + Triskelion" --tema "Commander: combo de dano infinito com persistir/undying"` → **PAUTA LIVRE** (26/11/2026, uma vez, regra E3). Comparação manual com o registo: nenhuma linha com Mikaeus, Triskelion, undying ou Rest in Peace.
- Relações: MB-EP18 (mesmo padrão de combo; mecânica, cores, número de peças e condição de vitória diferentes); MB-EP13 (referência de desempenho).

## Análise comparativa (método de 21/11, `manaburn/PERFIL.md`)
| | MB-EP13 «97 terrenos» | MB-EP18 «Lagarto Infinito» |
|---|---|---|
| Estado | publicado 20/11 09:00, orgânico | CONCLUÍDO, não publicado |
| Números | 19.688 views, 361 guardados, 282 partilhas, 43 comentários, 64 seguidores, tempo médio 31,5 s em 45 s (2 d 9 h; `comum/insights/registo_posts.csv`) | sem dados |
| Objeto | 3 cartas, limite de mão de 7 | 3 cartas, fichas infinitas + drenagem |
| Gancho | absurdo com número («97 terrenos… turno 5») | número + infinito («2 manas → ∞») |
| Recompensa | 85 de dano em cada oponente | mesa de 40 a 0 |

- Facto observado: o MB-EP13 é o melhor orgânico confirmado da conta; guardados (~18/1.000) e partilhas (~14/1.000) acima de outubro.
- Interpretação: o que se guarda e partilha é a explicação passo a passo de algo que parece impossível; não há dado de retenção por segundo.
- Hipótese (MB-EP19): um combo de **duas** cartas, com uma regra que a mesa costuma errar (undying e marcador vs bónus), mantém guardados e partilhas no nível do MB-EP13 com menos peças a explicar. Comparar às 48 h e aos 7 dias com MB-EP13 e MB-EP18, se nenhum for impulsionado.
- Não se infere causalidade das visualizações.

## Pesquisa de pauta (§2.4)
Reação-alvo: «Peraí… isso funciona mesmo?!». Radar `comum/radar/2026-W48.md` (válido): linhas 1–3 são do MB-EP18; acrescentadas as linhas 4–5 nesta sessão.

| # | Cartas | Custo e condições | Sequência | Resultado / vitória | Interrupção | Commander | Visual | Compreensão | Diferença | Fontes (26/11/2026) |
|---|---|---|---|---|---|---|---|---|---|---|
| A · **Mike e Trike** (VENCEDOR) | Mikaeus, the Unhallowed + Triskelion | 6 + 6 manas; ambos em campo, Triskelion com ≥ 2 marcadores | tira marcadores: 2 na mesa, 2 nele → morre sem marcador → undying → volta com 4 | dano infinito a qualquer alvo; vence a mesa inteira sem mana extra | exílio/remoção em resposta; Rest in Peace; anular o gatilho do undying | legal; 2 cartas = bracket 3+ | robô que «morre e volta»; contador 4 → 0 → 4 | alta: 2 cartas, 3 regras | morte e retorno, não fichas; preto + incolor; 2 peças | Scryfall (Oracle + ruling 07/12/2018); EDHREC/Spellbook 628-1495 (8,69 mil decks, rank 650) |
| B · Thassa's Oracle + Demonic Consultation | 2 cartas | {U}{U} + {B}; Consultation nomeia carta fora do deck | exila o grimório inteiro → Oracle entra com 0 cartas | vitória imediata | anular, Stifle no gatilho | legal; Oracle é «Game Changer» | grimório a desaparecer | média: devoção e «perder com deck vazio» | parecido com o MB-EP13 («o deck inteiro some»); cEDH, longe do público casual | EDHREC 742-1295 (136 mil decks, o combo mais jogado); Scryfall |
| C · Bloodchief Ascension + Mindcrank | 2 cartas | Ascension com 3 marcadores de missão (3 turnos) | perde 2 → moe 2 → cada carta → perde 2… | mata **um** oponente por vez (ou esvazia o grimório) | remover a encantamento; preparação lenta | legal | vida e grimório a cair | média: preparação de 3 turnos | perda de vida + moagem | Scryfall (Oracle) |

| Rubrica (1–5) | Gancho | Orig. | Compr. | Visual | Partilha | Recomp. | Adequação | Total |
|---|---|---|---|---|---|---|---|---|
| A · Mike e Trike | 5 | 4 | 4 | 5 | 4 | 5 | 5 | 32 |
| B · Oracle + Consultation | 5 | 2 | 3 | 4 | 4 | 4 | 3 | 25 |
| C · Ascension + Mindcrank | 3 | 4 | 3 | 3 | 3 | 3 | 3 | 22 |

- A vence: duas cartas, uma imagem que se percebe sem regras («o robô atira em si mesmo e volta»), três correções reais do Mana (undying só sem marcador; bónus não é marcador; tirar marcadores não mata) e uma pergunta de conta para o comentário. B é o combo mais conhecido do formato (pouca surpresa para quem já joga) e repete a ideia do MB-EP13; C só mata um oponente e depende de três turnos de preparação.
- Reserva: B e C (sem linha no registo).
- Escuta regional: EUA/global com dados (EDHREC, Spellbook, TappedOut). Brasil e Europa **sem fonte nesta sessão** (LigaMagic e MYP bloqueiam acesso automático; Reddit não aberto); limitação registada no radar. Nada disso entra no vídeo.
- Sem Salt Score verificado (o EDHREC não mostrou o número na página e o `json.edhrec.com` está bloqueado nesta sessão): sai o putômetro; o medidor da TV mostra o **bracket mínimo** do combo (3+, EDHREC), com fonte.

## Editorial
- Objetivo: respostas à pergunta de conta no comentário fixado; secundária: guardados e partilhas.
- Proposta de valor: perceber, com duas cartas, porque um robô que se mata ganha o jogo, e qual a regra que a mesa costuma errar.
- Tese: o undying só volta sem marcador, o bónus do Mikaeus não é marcador, e por isso os dois últimos tiros do Triskelion vão nele mesmo.
- Pergunta final: quiz A/B («na primeira volta, 1 ou 2 de dano?»). Resposta (A) no comentário fixado. Diferente do A/B de ação do MB-EP18.

## Gancho visual (7 campos)
1. Quadro 0: Triskelion em tela cheia, linha «Remove a +1/+1 counter… 1 damage» destacada, selo «2 TIROS → ∞» na arte.
2. Objeto: carta oficial (PNG do Scryfall, MOC 387).
3. Ação: entra com impacto 0,18 s; voa para a TV quando o Burn acaba «duas vezes nele» (`ate` 0,42).
4. Som: pancada + pop; zap na saída.
5. Descoberta: um robô que atira em si mesmo e volta.
6. Promessa: como volta e como isso ganha da mesa.
7. Pagamento: painéis do loop (29,8–33,3 s) e mesa a 0 (≈ 34,8–39 s).

Medido no final: saída da abertura aos 2,2 s (≤ 2,5 s).

## Roteiro definitivo
`episode.json` (14 falas, roteiro original desta sessão). Texto falado em `faixas_elevenlabs.txt`.

| Fala | Quem | Texto |
|---|---|---|
| 1 | Burn | Esse robô atira duas vezes nele mesmo… morre… e volta pra sempre! |
| 2 | Mana | É o Mike e Trike. O Mikaeus dá undying pras outras criaturas não humanas. |
| 3 | Burn | Undying?! Então tudo volta toda vez! Bane! |
| 4 | Mana | Lê a carta. Só volta se morreu sem marcador +1/+1. |
| 5 | Burn | Mas o Mikaeus dá +1/+1! Pronto, tem marcador! |
| 6 | Mana | Bônus não é marcador. Tá na ruling. O undying funciona. |
| 7 | Burn | E esse robô? Seis manas num 1/1?! |
| 8 | Mana | Entra com três marcadores. Tira um: 1 de dano em qualquer alvo. |
| 9 | Burn | Tirou todos, ficou sem marcador… e não morreu, gênio! |
| 10 | Mana | Porque os dois últimos tiros vão nele. Morre sem marcador… e volta com quatro. |
| 11 | Burn | Quatro?! Dois na mesa, dois nele… e repete?! |
| 12 | Mana | Sem gastar mana, até a mesa zerar. Com Rest in Peace na mesa, ele nem morre: vai pro exílio. |
| 13 | Burn | Pergunta: na primeira volta, a mesa toma A, um de dano, ou B, dois? |
| 14 | Mana | Comenta aí. |

Revisão narrativa (§4.2): cada fala do Mana corrige ou acrescenta uma regra (undying condicional; bónus ≠ marcador; marcador como custo; auto-alvo; resposta da mesa); o Burn faz as três objeções que a mesa faz; a pergunta final testa a regra ensinada (primeira volta com 3 marcadores, não 4).

## Auditoria técnica do combo (Oracle, 26/11/2026)
1. Mikaeus, the Unhallowed ({3}{B}{B}{B}, 5/5, Zombie Cleric): «Other non-Human creatures you control get +1/+1 and have undying.» Lembrete: volta só se morreu **sem** marcador +1/+1, com um marcador.
2. Ruling (07/12/2018): o +1/+1 do Mikaeus não é marcador e não impede o undying.
3. Triskelion ({6}, 1/1, Construct): entra com três marcadores; «Remove a +1/+1 counter: It deals 1 damage to any target.» O marcador é custo; o dano usa a pilha.
4. Com o Mikaeus: 5/5 ao entrar (3 marcadores); 2/2 sem marcadores. Dois tiros nele = 2 de dano num 2/2 → morre (ação baseada em estado). Volta com 3 + 1 = 4 marcadores (Spellbook, passo 6). Por volta: 2 na mesa, 2 nele. Primeira volta (recém-jogado, 3 marcadores): 1 na mesa.
5. Rest in Peace: a criatura iria para o cemitério e é exilada; não «morre» (regra 700.4), o undying não dispara.
6. Não é invulnerável: exilar o Triskelion ou o Mikaeus com uma ativação ou o gatilho na pilha corta o loop.
7. Não há afirmação de preço, orçamento nem lista de 100 cartas (fora do âmbito deste episódio).

## Fontes e evidências
`fontes.md`. Limitações: Salt Score não verificado (sem putômetro); Brasil e Europa sem fonte (ver acima).

## Produção
- Recursos reutilizados, sem motor novo: kit v2 + v3 (sala, dupla, TV SAL, Conde), abertura de carta, plano de prova, `processar_vozes.py` (corte pelo `tts`), `juntar_fecho.py` e `previa_sem_voz.py` (cópias do MB-EP18), CSS das telas do MB-EP18, `capas/capa_mb.py`. Novo só `telas_robo.py` (8 telas, só cartas reais).
- Vozes: ElevenLabs eleven_v4, flow «Mana & Burn — MB-EP19 (O Robô Que Não Morre)» (`ptFbnfiLh2Xoe3yQBfbU`). Burn: Talis (`E9a8LlXPNWtyvvSoZzrb`), 530 créditos, 29,8 s. Mana: Erik (`nfiLpQ54jEQninp3nNqL`), 582 créditos, 32,6 s. **Total 1.112 créditos**, uma geração cada, sem repetição. IDs confirmados no `creative_list_voices`.
- Easter egg: relógio da TV SAL em «06:03» = o Triskelion custa 6 e entra com 3 marcadores.
- Medidor da TV: «BRACKET 3+» (fill 3/5), conta e fonte no ecrã (EDHREC, 26/11).
- Quadro do Conde: uma expressão por fala; `check_quadro.py` OK.
- Riscos: factuais (mitigados pelo Oracle, pela ruling e pelo Spellbook); direitos (cartas e artes © Wizards of the Coast, com crédito na tela e na legenda; conteúdo de fã).

## Controlo de qualidade
Medido no ficheiro final `ManaBurn_Ep19_RoboQueNaoMorre_916.mp4` (v2, revisão de 26/11/2026 22h45) com `python3 -I comum/qc/qc_video.py … --frente manaburn`; valores iguais aos da v1.

| Critério | Alvo | Medido | OK |
|---|---|---|---|
| Resolução / fps | 1080×1920, 30 fps | 1080×1920, 30 fps | ✓ |
| Duração | ~42–47 s + fecho | 50,90 s (47,03 s + fecho de 3,87 s) | ✓ |
| Corte lateral | nenhum | `bordas.py` OK (1.078 quadros de TV, laterais 58–804 px) | ✓ |
| Loudness / pico | −14 LUFS / < −1 dBTP | −14,7 LUFS / −1,6 dBTP | ✓ |
| Fecho do scanner | presente | a partir de 47,03 s (dif. 0,07) | ✓ |
| Factos = ficha | sim | sim (Oracle e ruling de 26/11) | ✓ |
| Carta mostrada = carta falada | sim | Mikaeus nas falas 2 e 4, ruling na 6, Triskelion nas 7–8, loop na 10, Rest in Peace na 12 | ✓ |
| Sequência do combo | ordem da fala | fala 10: «2 TIROS NELE / MORREU» → «VOLTA COM 4» | ✓ (painel reordenado depois da 1.ª prévia) |
| Condição de vitória | demonstrada | mesa 40 → 0 (exemplo, 120 de dano ≈ 60 voltas) | ✓ |
| Quadro 0 | carta + selo | Triskelion inteiro, linha do dano destacada, selo «2 TIROS → ∞» no céu, canto superior direito da arte (v2) | ✓ |
| Saída da abertura | ≤ 2,5 s | 2,2 s | ✓ |
| Maior intervalo sem troca forte | ≤ 3 s | 4,1 s na fala 13 (pergunta na TV; troca `meio` discreta «COMENTA AÍ» a meio e câmara em movimento) e 3,3 s na fala 9 (Burn no sofá, personagens em movimento) | aceite (P2, mesmo caso do MB-EP18) |
| P0 / P1 abertos | 0 / 0 | 0 / 0 | ✓ |

Outros controlos: folha de contacto conferida a olho (`folha_contacto_final.png`): cartas inteiras, destaques alinhados nas linhas citadas, nada sobre o texto das cartas, legendas na zona segura. Na aproximação ao texto do Mikaeus (fala 4) as margens da carta ficam fora da janela, como em todos os zooms do plano de prova.

## Revisão (26/11/2026, 22h45, pedido do fundador «Revise o episódio do robô»)
Revisão de factos, roteiro, telas e quadros do ficheiro final. Factos, roteiro e áudio sem erros: não se mexeu nas vozes (0 créditos). Três correções visuais, novo render (v2):

| Problema na v1 | Correção na v2 | Gravidade |
|---|---|---|
| Medidor da TV com «cEDH» em baixo e «CASUAL» em cima, ao contrário da barra (verde em baixo, vermelho em cima): o «3+» parecia perto do cEDH | `levels` invertidos: cEDH no topo, CASUAL em baixo | P1 (leitura errada de um dado) |
| Conta do medidor cortada pela moldura da TV («combo de 2 carta:») | conta encurtada: «2 cartas: / fora do 1 e 2 / EDHREC · 26/11» | P2 |
| Selo da abertura sobre a cauda do robô (canto superior esquerdo da arte) | selo menor no céu, canto superior direito, fora da criatura e do nome | P2 |
| Pergunta «primeira volta» com duas leituras possíveis (recém-jogado com 3 marcadores ou depois do 1.º undying com 4) | tela da pergunta diz «Triskelion recém-jogado, com 3 marcadores: quanto de dano na mesa?» (a fala do Burn não muda) | P1 (resposta do comentário fixado tem de ser inequívoca) |

Mantidos (P2, sem mudança): 4,1 s na fala 13 com a pergunta na TV (troca «COMENTA AÍ» a meio) e 3,3 s do Burn no sofá na fala 9. A manchete «Plantão anterior: lagarto de duas manas cria infinito» pressupõe o MB-EP18 publicado antes: publicar o EP18 primeiro.

## Ficheiros finais
- Vídeo final: `ManaBurn_Ep19_RoboQueNaoMorre_916.mp4` **v2** (revisão de 22h45) · 50,90 s · entregue ao fundador na conversa de 26/11/2026 (projeto claude.ai); a v1 não se publica; não versionado.
- Capa: `MB_EP19_CAPA.png` (frase «O ROBÔ QUE NÃO» + foco «MORRE», selo «2 TIROS NELE», faixa «MANA & BURN · EP. 19», tag COMMANDER). Grelha 3:4: `MB_EP19_CAPA_grelha.png`.
- Telas: `cards/t*.png` (geradas por `telas_robo.py`).

## Pacote de publicação
- [x] `legenda.txt` (CTA: escanear e ver o valor de referência; diferente do MB-EP18)
- [x] `comentario_fixado.txt` (pergunta na 1.ª linha, resposta, passo a passo, Oracle, ruling, fontes, convite ao easter egg)
- [x] `texto_alternativo.txt`
- [x] `fontes.md`

## Encerramento
- [x] Briefing e roteiro definitivo nesta ficha
- [x] Legenda, comentário fixado e texto alternativo na pasta
- [x] Fontes e evidências
- [x] Controlo de qualidade preenchido
- [x] Localização do vídeo e da capa
- [x] `comum/REGISTRO_EDITORIAL.md` (CONCLUÍDO)
- [x] `comum/historico.md`
- [x] Easter egg em `comum/easter_eggs.md`
- [x] `STATUS.md`
- [x] `memoria.py encerramento MB-EP19`
- [x] Commit enviado e conferido no GitHub (hash no handoff do `STATUS.md`)
- [x] Handoff entregue

## Reproduzir
Kit numa cópia de trabalho (manaburn/ sem episodios/), `episode.js`/`episode.json` na raiz, `cards/src/` com os PNG do Scryfall (cmm/173, moc/387 redimensionada a 744×1040, big/4) e cópias `mikaeus.png`, `triskelion.png`, `rip.png`; `CHROME=/usr/bin/google-chrome python3 telas_robo.py`, `python3 processar_vozes.py burn19.mp3 mana19.mp3`, `python3 bordas.py`, `python3 render.py …_kit.mp4` (Chrome do sistema), `python3 juntar_fecho.py …_kit.mp4 comum/outro/outro_binder_916.mp4 …_916.mp4 0`. Capa: `python3 capas/capa_mb.py --carta cards/src/triskelion.png --frase "O robô que não" --foco "morre" --selo "2 tiros nele" --selo-y 400 --ep 19 --tag Commander --saida MB_EP19_CAPA.png` (precisa de `brotli`).

## Depois de publicar
- Data e hora de publicação (confirmada por): 
- Métrica principal: respostas à pergunta do comentário fixado; guardados e partilhas às 48 h e aos 7 dias contra MB-EP13 e MB-EP18
- Resultado observado: 
- Aprendizagem: 

## Handoff

```
HANDOFF · 26/11/2026, 21h50 (Lisboa) · Claude
Repositório: ibisson254/GERADOR-DE-VIDEO-BINDER · branch main · commit do episódio 2fc9422 (conferido no remoto: sim)

Objetivo atual: fórmula dos combos consolidada; MB-EP18 e MB-EP19 prontos para o fundador publicar.

Conteúdos tocados (comum/REGISTRO_EDITORIAL.md):
- MB-EP19 · (novo) → CONCLUÍDO
- MB-EP18 · CONCLUÍDO → CONCLUÍDO (verificado; sem alterações; re-render das vozes já pagas, 0 créditos)

Encerramento:
- MB-EP19 · memoria.py encerramento: OK · memoria.py validar: OK · validar_repo: 0 graves (P2 antigo: vince/kit/v1/)
- Vídeos e capas: entregues na conversa do projeto claude.ai de 26/11/2026 (21h); capas também nas pastas dos episódios. Vídeos não versionados.

Decisões tomadas nesta sessão:
- «Episódio de combo» passa a padrão recorrente, não exclusivo (nucleo/DECISOES.md, 26/11/2026 21:45; manaburn/PERFIL.md) · sim
- Vozes do MB-EP19 autorizadas pelo fundador no cartão da sessão (1.112 créditos, uma geração cada) · na ficha
- Sem Salt verificado: o medidor da TV mostra o bracket mínimo do combo (EDHREC) em vez do putômetro · na ficha

Documentos consultados:
- AGENTS.md, STATUS.md, manaburn/PERFIL.md, manaburn/LEIA-ME.md, skill binder-mana-burn-episodio, nucleo/DECISOES.md, comum/REGISTRO_EDITORIAL.md, comum/easter_eggs.md, comum/radar/2026-W48.md, comum/insights/semanas/2026-11-21.md, fichas MB-EP13 e MB-EP18, nucleo/modelos/FICHA_EPISODIO.md e HANDOFF.md

Alterações realizadas:
- manaburn/episodios/ep19_robo_imortal/ · episódio completo · 2fc9422
- manaburn/PERFIL.md, nucleo/DECISOES.md · padrão «Episódio de combo» · 2fc9422
- comum/REGISTRO_EDITORIAL.md, comum/historico.md, comum/easter_eggs.md, comum/radar/2026-W48.md, STATUS.md, comum/status_arquivo.md · 2fc9422

Insights (domingo): não se aplica (quinta-feira)

Tarefas pendentes:
- Escutar e publicar o MB-EP19 (e o MB-EP18), em dias diferentes · fundador
- Confirmar os preços do deck do MB-EP18 na LigaMagic antes de citar valores · fundador
- Medir às 48 h e aos 7 dias contra o MB-EP13 (guardados, partilhas, respostas) · agente, com prints do fundador
- Escuta Brasil/Europa do radar W48 continua em falta (LigaMagic/MYP/Reddit) · agente noutra sessão

Próximo passo concreto: publicar o MB-EP19 com legenda.txt e comentario_fixado.txt desta pasta (utm_campaign=MB-EP19).
```
