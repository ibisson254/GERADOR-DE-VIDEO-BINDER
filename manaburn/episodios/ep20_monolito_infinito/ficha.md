# Ficha · Mana & Burn · EP20 · «O Monólito Infinito» (Basalt Monolith + Rings of Brighthearth; finalizador Walking Ballista)

## Identificação
- ID editorial: MB-EP20 (provisório na missão; confirmado livre no registo e no `memoria.py` a 27/11/2026)
- Estado no registo: CONCLUÍDO (ver «Controlo de qualidade»)
- Aprovação do fundador: missão «MISSÃO DE PRODUÇÃO — MANA & BURN · NOVO EPISÓDIO DE COMMANDER · MB-EP20 — O MONÓLITO INFINITO» (projeto claude.ai, 27/11/2026 08:44 UTC), com cartas, finalizador, tese, roteiro de origem e capa definidos pelo fundador; **vozes autorizadas** no cartão de decisão da sessão (27/11/2026 08:57 UTC, «Sim, autorizo as vozes», ~1.430 créditos estimados).
- Roteiro vindo de outro agente: produção pela `nucleo/SHOWRUNNER.md` §4.3 (não se refez ideação nem roteiro).

## Classificação
- Frente: Mana & Burn (série) · formato base 14 falas, Commander · padrão «Episódio de combo» (`manaburn/PERFIL.md`)
- Classe: leitura de carta / combo (Oracle + rulings + Commander Spellbook/EDHREC com data)
- Complexidade: média-alta (pilha, cópia de habilidade ativada, habilidade de mana vs não-mana)
- Estratégia: «Peraí… esse artefato consegue mesmo fazer isso?» com recompensa visível (contador de mana e pilha em cada painel)

## Originalidade
- Objeto: Basalt Monolith + Rings of Brighthearth (+ Walking Ballista como finalizador, à parte do combo)
- `python3 comum/ferramentas/memoria.py pauta --objeto "Rings of Brighthearth + Basalt Monolith" --tema "Commander: mana incolor infinita com cópia de habilidade e finalizador Walking Ballista"` → **PAUTA LIVRE: sem conflito no registo** (27/11/2026, uma vez, regra E3).
- Comparação manual com o registo: nenhuma linha com Basalt Monolith, Rings of Brighthearth ou mana infinita. A Walking Ballista só aparece no `DECK.md` do MB-EP18 (finalizador de reserva, fora do vídeo) e no comentário/fontes do MB-EP19 («não faz o mesmo»): aqui é finalizador de um outro motor, não o objeto. Tese, gancho («não desvira… mana infinita») e ângulo (cópia de habilidade + ordem da pilha) sem paralelo.
- Diferença face aos combos anteriores: MB-EP13 limite de mão + descarte; MB-EP18 fichas + drenagem por entrada; MB-EP19 morte e retorno (undying). MB-EP20: **cópia de habilidade ativada e ciclo de artefatos**, incolor, vitória por um finalizador separado. Pergunta final de ação/escolha (o MB-EP19 fechou com conta).

## Análise comparativa (método de 21/11, `manaburn/PERFIL.md`)
| | MB-EP13 «97 terrenos» | MB-EP18 / MB-EP19 |
|---|---|---|
| Estado | publicado 20/11, orgânico | CONCLUÍDOS, não publicados (sem dados) |
| Números | 19.688 views, 361 guardados, 282 partilhas (`comum/insights/registo_posts.csv`) | — |
- Facto observado: o MB-EP13 é a referência orgânica de guardados e partilhas; EP18 e EP19 ainda não têm dados.
- Hipótese (MB-EP20): um combo **sem criaturas** em que a recompensa é um contador de mana a subir, com a pilha desenhada passo a passo, gera guardados (é uma explicação de regra que se volta a ver) ao nível do MB-EP13. A pergunta de escolha (A/B de ação) deve gerar mais respostas do que a pergunta de conta do MB-EP19. Comparar às 48 h e aos 7 dias com MB-EP13, EP18 e EP19, se nenhum for impulsionado.
- Não se infere causalidade das visualizações.

## Pesquisa de pauta (§2.4) e módulo «deck Commander» (§2.4, passo 9, criado nesta missão)
Reação-alvo: «Peraí… esse artefato consegue mesmo fazer isso?». Radar `comum/radar/2026-W48.md` (válido até 03/12): acrescentadas as linhas 6–8 nesta sessão. Tema dado pelo fundador: compararam-se candidatos de objeto e mecânica diferentes para confirmar que o escolhido supera as alternativas.

### Candidatos (combos)
| # | Cartas | Condições | Sequência | Resultado / vitória | Interrupção | Visual | Diferença | Fontes (27/11/2026) |
|---|---|---|---|---|---|---|---|---|
| A · **Monólito + Rings** (VENCEDOR, tema do fundador) | Basalt Monolith + Rings of Brighthearth | ambos em campo, Monolith desvirado, 2 manas | vira +3 → desvirar −3 → Rings −2 (cópia) → cópia desvira → vira +3 → original desvira | +1 mana incolor por ciclo, infinito; **não ganha sozinho** (Walking Ballista fecha) | destruir/exilar uma peça em resposta; anular o gatilho do Rings | contador de mana + pilha a crescer e a esvaziar | cópia de habilidade e ordem da pilha | Scryfall (Oracle + rulings); Spellbook 4131-4235; EDHREC 54.795 decks |
| B · Monólito + Forsaken Monument | Basalt Monolith + Forsaken Monument | Monument em campo | vira por 4 (3 + 1 do Monument), desvira por 3 | +1 por ciclo, infinito | remover uma peça | só o contador | mesmo objeto, mecânica estática, **sem pilha** para ensinar | EDHREC 68.191 decks (rank 23); Spellbook 4131-4547 |
| C · Karn + Mycosynth Lattice | Karn, the Great Creator + Mycosynth Lattice | ambos em campo | tudo vira artefato; o Karn proíbe ativações de artefatos dos oponentes | **tranca** (terrenos incluídos), não vitória | remover o Karn ou a Lattice | mesa «congelada» | tranca e planeswalker | EDHREC 23.107 decks; Spellbook 3263-5089 |
| D · Nim Deathmantle + Ashnod's Altar | + criatura com persist/undying ou Wurmcoil | 3 peças | sacrifica, volta pela Deathmantle | mana/entradas/mortes infinitas | exílio, cemitério fechado | loop de morte | **perto do MB-EP19** (morte e retorno) | EDHREC 31.076 decks; Spellbook 2034-5003 |

| Rubrica (1–5) | Gancho | Orig. | Compr. | Visual | Partilha | Recomp. | Adequação | Total |
|---|---|---|---|---|---|---|---|---|
| A · Monólito + Rings | 5 | 5 | 4 | 5 | 4 | 4 | 5 | 32 |
| B · Monólito + Monument | 4 | 3 | 5 | 3 | 3 | 3 | 3 | 24 |
| C · Karn + Lattice | 5 | 4 | 3 | 4 | 4 | 3 | 3 | 26 |
| D · Deathmantle + Altar | 3 | 2 | 3 | 3 | 3 | 3 | 3 | 20 |

- A vence: é a única com três correções reais do Mana (3 menos 3 dá zero sem a cópia; a cópia resolve primeiro; mana infinita incolor não ganha jogo) e com uma recompensa que se desenha (pilha + contador). B é mais simples mas sem pilha (uma só correção); C não ganha o jogo; D repete o MB-EP19. Reservas: B e C (sem linha no registo).

### Decks Commander com o combo (8 campos)
| Comandante | Cores | Plano de jogo | Cartas centrais | Vitória | Dependências | Vulnerabilidades | Visual |
|---|---|---|---|---|---|---|---|
| Urza, Lord High Artificer (7.862 decks com o combo no EDHREC) | U (mono-azul) | artefatos de mana; o Urza vira artefatos por {U} | Basalt Monolith, Rings, Sol Ring, Mana Vault, Mystic Forge, Sensei's Divining Top | Walking Ballista (≈ 35 % dos decks com o combo), mana infinita para o Urza | ter as duas peças + 2 manas | remoção de artefatos em massa (Vandalblast aparece nas listas do combo) | alto: artefatos e números |
| Zhulodok, Void Gorger (4.456) | C (incolor) | rampa para Eldrazi; cascata dupla em mágicas incolores de MV ≥ 7 | Basalt, Rings, Forsaken Monument, Karn, the Great Creator | mana infinita → Eldrazi gigantes (opção B da pergunta) | Eldrazi na mão; sem ímpeto | anulação, remoção de artefatos | alto: Eldrazi |
| Kozilek, the Great Distortion (1.082) | C | Eldrazi + compra até 7 | Basalt, Rings | Ballista / Eldrazi | idem | idem | médio |

- Listas públicas usadas (URL e data em `fontes.md`): MTGGoldfish «Urza Artifacts» (5362935: as três cartas; 6301237), arquétipo Urza no MTGGoldfish (deck em destaque de 23/11/2026), Archidekt sandbox 18087785 (Urza, Lord Protector, as três cartas), mtgdecks.net Zhulodok (última atualização 11/05/2026), EDHREC deck médio de Zhulodok (8 decks). **Moxfield sem lista** (não abriu). Nenhuma lista copiada.
- Separação de dados: **contagem** (EDHREC: listas publicadas, não partidas) · **popularidade** (não medida) · **opinião** (voto de bracket «4-5» com 15 votos; Salt 2,0 no Spellbook sem amostra: fora do vídeo) · **resultado competitivo** (nenhum consultado; é território do Meta em Curto).
- Escuta regional: EUA/global com dados. **Brasil e Europa sem fonte nesta sessão** (LigaMagic/MYP com anti-robô; pesquisa em português sem resultados). Nada sobre tendência regional no vídeo.

## Editorial
- Objetivo: respostas à pergunta de escolha no comentário fixado; secundária: guardados e partilhas.
- Proposta de valor: perceber, com dois artefatos, como o «3 menos 3» dá lucro, e porque mana infinita ainda não ganha o jogo.
- Tese: dois artefatos geram mana incolor infinita (a cópia do Rings resolve antes da original e deixa o Monolith ser virado duas vezes por ciclo); a Walking Ballista converte esse recurso em dano. O combo de duas cartas, sozinho, não é vitória.
- Pergunta final: A/B de ação («fecha com a Ballista ou conjura um Eldrazi colossal?»). Resposta do Mana (A) no comentário fixado.

## Gancho visual (7 campos)
1. Quadro 0: Basalt Monolith inteiro em tela cheia, linha «doesn't untap during your untap step» destacada, selo «MANA INFINITA» no céu da arte (canto superior direito, fora do monólito e do nome).
2. Objeto: carta oficial (PNG do Scryfall, 2XM 232).
3. Ação: entra com impacto 0,18 s; voa para a TV quando o Burn acaba «não desvira» (`ate` 0,30).
4. Som: pancada + pop; zap na saída.
5. Descoberta: um artefato que não desvira sozinho… e dá mana infinita.
6. Promessa: como «gera 3, cobra 3» dá lucro e como isso ganha o jogo.
7. Pagamento: saldo «+1 POR CICLO» (≈ 27–31 s) e mesa 40 → 0 com a Ballista (≈ 50–52 s).

## Roteiro definitivo
`episode.json` (14 falas). Texto falado em `faixas_elevenlabs.txt`.

| Fala | Quem | Texto |
|---|---|---|
| 1 | Burn | Esse monólito não desvira na sua etapa de desvirar… mas pode gerar mana infinita! |
| 2 | Mana | Com Rings of Brighthearth, ele transforma o próprio desvirar num ciclo. |
| 3 | Burn | Mas o Basalt Monolith gera três e cobra três pra desvirar. Onde está o lucro? |
| 4 | Mana | Quando você ativa o desvirar, Rings pode copiar essa habilidade se você pagar mais duas manas. |
| 5 | Burn | E a cópia resolve primeiro? |
| 6 | Mana | Isso. Ela desvira o Monolith. Você vira de novo e gera outras três. |
| 7 | Burn | E a habilidade original ainda está na pilha! |
| 8 | Mana | Ela resolve depois e desvira o artefato outra vez. Começando com duas manas disponíveis, cada ciclo completo deixa uma mana incolor a mais. |
| 9 | Burn | Uma por volta? Então dá pra repetir até ter o quanto quiser! |
| 10 | Mana | Exatamente. Mas é mana incolor, e mana infinita sozinha não derrota ninguém. |
| 11 | Burn | Então quem transforma esse infinito em dano? |
| 12 | Mana | Walking Ballista. Ela entra com X marcadores. Você remove um e causa um de dano a qualquer alvo. Com 120 marcadores, que custam 240 manas, são 40 de dano pra cada um dos três oponentes, num exemplo de mesa a 40. |
| 13 | Burn | Você fecha com a Ballista ou usa o infinito pra conjurar um Eldrazi colossal? |
| 14 | Mana | Comenta aí. |

## Alterações ao roteiro de origem (§4.3)
| Fala | Rascunho | Final | Porquê |
|---|---|---|---|
| 10 | «…mana incolor — e mana infinita sozinha…» | «…mana incolor, e mana infinita sozinha…» | só pontuação (legenda e TTS) |
| 12 | «Com 120 marcadores, são 40 de dano pra cada um…» | «Com 120 marcadores, **que custam 240 manas**, são 40 de dano pra cada um…» | a missão pede que o exemplo diga que X = 120 custa 240 manas; o sentido não muda (acrescenta o custo correto) |
| 2, 3, 6, 12, 13 | — | grafia fonética só no campo `tts` («Bráit-rárt», «Basált Mônolit», «Uóquin Balísta», «Eldrázi»; números por extenso) | pronúncia; legendas iguais ao rascunho |

Nenhuma mudança de sentido, gancho ou pergunta: não foi preciso mostrar a tabela ao fundador antes da voz.

Revisão narrativa (§4.2): tese numa frase (acima); cada fala do Mana acrescenta uma regra (cópia de habilidade ativada; pilha: último a entrar resolve primeiro; habilidade de mana fora da pilha; saldo; incolor ≠ vitória; X dobrado); o Burn faz as objeções da mesa («3 menos 3 é zero», «a original ainda está na pilha», «quem fecha?»); evidência real em cada fala (carta, ruling ou painel com fonte); pergunta final de escolha.

## Auditoria técnica do combo (Oracle e Spellbook, 27/11/2026)
1. Os dois artefatos em campo; Monolith desvirado; 2 manas disponíveis (Spellbook «manaNeeded {2}»).
2. Basalt Monolith: «{T}: Add {C}{C}{C}» (habilidade de mana) e «{3}: Untap» (não é de mana: custa mana, não a produz; ruling do Rings de 10/11/2020).
3. Rings: «you may pay {2}. If you do, copy that ability» — opcional a cada ativação; não copia habilidades de mana.
4. Ruling do Rings (10/11/2020): o gatilho e a cópia resolvem antes da habilidade original. Regras 603.3 (gatilho vai para o topo) e 405.5 (resolve o topo).
5. Depois de a cópia desvirar o Monolith, ele pode ser virado com a original ainda na pilha (regra 605.3a: habilidades de mana quando se tem prioridade). A original resolve e desvira de novo.
6. Conta: 2 → 5 (vira) → 2 (desvirar) → 0 (Rings) → 3 (vira) → original desvira: fim com 3 e o Monolith desvirado = +1 por ciclo. O jogador escolhe quantas voltas dá (atalho, regra 722).
7. Mana incolor; mana infinita sozinha não muda a vida de ninguém.
8. Walking Ballista: {X}{X}, entra com X marcadores; tirar 1 = 1 de dano a qualquer alvo. X = 120 custa 240 (ruling de 07/08/2020). 120 = 40 × 3 oponentes a 40 (regra 903.7): marcado «EXEMPLO» no ecrã.
9. Respostas da mesa: a cada desvirar e a cada gatilho do Rings os oponentes recebem prioridade; destruir/exilar uma peça ou anular o gatilho corta o ciclo; a Ballista é mágica de criatura (pode ser anulada) e os tiros usam a pilha. «Impossível de parar» não se usa.
10. Ulamog, the Ceaseless Hunger (opção B): {10}, legal no Commander, sem ímpeto. Emrakul, the Aeons Torn foi descartada porque está **banida** no Commander (Scryfall, 27/11/2026).
11. Sem bracket, Salt nem preço no vídeo (amostras pequenas; sem fonte brasileira de preço).

## Fontes e evidências
`fontes.md` (Oracle, rulings, Regras Completas, Spellbook, EDHREC, listas públicas com URL e data). Limitações: Moxfield sem lista; Brasil/Europa sem fonte; Regras Completas lidas em cópias HTML (o .docx oficial não abriu).

## Produção
- Recursos reutilizados, sem motor novo: kit v2 + v3 (sala, dupla, TV SAL, Conde), abertura de carta, plano de prova, `processar_vozes.py` (corte pelo `tts`), `juntar_fecho.py` e `previa_sem_voz.py` (cópias do MB-EP19), CSS das telas do MB-EP18/EP19, `capas/capa_mb.py`. Novo só `telas_monolito.py` (18 telas; painéis do ciclo com pool de mana e pilha; só cartas reais).
- Prévia sem voz (27/11): ritmo, ordem da pilha, telas, `bordas.py` OK e `check_quadro.py` OK antes de gastar créditos; acrescentado o painel `p7b` («+1 MANA INCOLOR») para não passar de 3 s no saldo.
- Vozes: ElevenLabs eleven_v4, flow «Mana & Burn — MB-EP20 (O Monólito Infinito)» (`DWLhppwFs2GnKpze7FIJ`). Burn: Talis (`E9a8LlXPNWtyvvSoZzrb`), 569 créditos, 26,8 s. Mana: Erik (`nfiLpQ54jEQninp3nNqL`), 854 créditos, 47,4 s. **Total 1.423 créditos**, uma geração cada, sem repetição. IDs confirmados no `creative_list_voices`.
- Easter egg: relógio da TV SAL em «03:32» = o Monolith vira por 3, desvira por 3 e o Rings cobra 2.
- Medidor da TV: «MANA +1» com a conta «+3 −3 −2 +3 = +1 por ciclo · Oracle · 27/11» (dado real do Oracle, não Salt nem bracket).
- Quadro do Conde: uma expressão por fala; `check_quadro.py` OK.
- Riscos: factuais (mitigados pelo Oracle, rulings, Spellbook e Regras); direitos (cartas e artes © Wizards of the Coast, com crédito na tela e na legenda; conteúdo de fã).

## Controlo de qualidade
Medido no ficheiro final `ManaBurn_Ep20_MonolitoInfinito_916.mp4` (v3, 27/11/2026) com `python3 -I comum/qc/qc_video.py … --frente manaburn`, `bordas.py`, `kit/v3/check_quadro.py` e medição de diferença entre quadros (90×160, zona sem legendas, limiar 6).

| Critério | Alvo | Medido | OK |
|---|---|---|---|
| Resolução / fps | 1080×1920, 30 fps | 1080×1920, 30 fps | ✓ |
| Duração | livre (ref. 42–53 s + fecho) | 62,20 s (58,33 s + fecho de 3,87 s); roteiro do fundador com 14 falas e fala 12 longa | ✓ (acima da referência; sem cortar falas aprovadas) |
| Corte lateral / cartas truncadas | nenhum | `bordas.py` OK (1.629 quadros de TV, laterais 58–804 px); cartas inteiras no plano de prova (aproximações ao texto como nos episódios anteriores) | ✓ |
| Loudness / pico | ≈ −14 LUFS / < −1 dBTP | −14,9 LUFS / −1,3 dBTP | ✓ |
| Fecho do scanner | presente | a partir de 58,33 s (dif. 0,07) | ✓ |
| Quadro 0 | carta inteira + gancho legível sem som | Basalt Monolith inteiro, linha «doesn't untap during your untap step» destacada, selo «MANA INFINITA» no céu da arte | ✓ |
| Saída da abertura | ligada à fala, ≤ 2,5 s | começa a 1,70 s (fim de «não desvira»), dentro da TV a 2,02 s | ✓ |
| Maior intervalo sem mudança visual forte | ≤ 3 s | 2,97 s (painéis 6 → 7, 24,6–27,6 s); 2,87 s (TV da fala 1) | ✓ (v1: 3,67 s na pergunta e 3,7 s na fala 10 → corrigidos na v2/v3) |
| Legendas na zona segura, sem tapar carta/arte/rosto | sim | sim (folha de contacto `folha_contacto_final.png`) | ✓ |
| Ordem da pilha | igual à fala e às regras | p1 vira +3 → p2 desvirar −3 → p3 Rings −2 (cópia no topo) → p4 cópia resolve → p5 vira +3 → p5b original na pilha → p6 original resolve → p7 saldo +1 | ✓ |
| Factos = Oracle e fontes | sim | sim (ver «Auditoria técnica» e `fontes.md`) | ✓ |
| Quadro do Conde | trocas em cortes | `check_quadro.py` OK | ✓ |
| P0 / P1 abertos | 0 / 0 | 0 / 0 | ✓ |

Revisões antes da entrega (0 créditos, só render): v2 acrescentou a troca a meio na TV da fala 1 (`t00_monolito_b`) e na fala 10 (`t10_incolor_b`) e reforçou a troca da pergunta A/B (`t13_ab_b` com as opções a amarelo); v3 desceu o carimbo «SOZINHA NÃO GANHA» que tapava a linha «falta o finalizador».

Rubrica do gancho (§4.1), medida na folha de contacto sem som: relevância 5, impacto 4, clareza 4, curiosidade 5, pagamento 5 (saldo aos 27–31 s; mesa 40 → 0 aos 50–52 s), identidade 5.

## Ficheiros finais
- Vídeo final: `ManaBurn_Ep20_MonolitoInfinito_916.mp4` · entregue em `/mnt/project-files/manaburn/ep20/` (projeto claude.ai); não versionado.
- Capa: `MB_EP20_CAPA.png` (frase «O MONÓLITO» + foco «INFINITO», selo «2 ARTEFATOS», faixa «MANA & BURN · EP. 20», tag COMMANDER). Grelha 3:4: `MB_EP20_CAPA_grelha.png`.
- Telas: `cards/t*.png` e `cards/p*.png` (geradas por `telas_monolito.py`).

## Pacote de publicação
- [x] `legenda.txt` (CTA: escanear e escolher a impressão certa; diferente do MB-EP19; termina com «baixe o BINDER Vision»; 5 hashtags; sem emojis)
- [x] `comentario_fixado.txt` (pergunta na 1.ª linha, resposta, passo a passo, Oracle, rulings, como parar, fontes, convite ao easter egg)
- [x] `texto_alternativo.txt`
- [x] `fontes.md`

## Reproduzir
Kit numa cópia de trabalho (manaburn/ sem episodios/), `episode.js`/`episode.json` na raiz, `cards/src/` com os PNG do Scryfall redimensionados a 744×1040 (2xm/232 monolith, cmr/335 rings, 2xm/306 ballista, cmm/5 ulamog); `CHROME=/usr/bin/google-chrome python3 telas_monolito.py`, `python3 processar_vozes.py burn20.mp3 mana20.mp3`, `python3 bordas.py`, `python3 render.py …_kit.mp4` (Chrome do sistema), `python3 juntar_fecho.py …_kit.mp4 comum/outro/outro_binder_916.mp4 …_916.mp4 0`. Capa: `python3 capas/capa_mb.py --carta cards/src/monolith.png --frase "O monólito" --foco "infinito" --selo "2 artefatos" --selo-y 420 --ep 20 --tag Commander --saida MB_EP20_CAPA.png` (precisa de `fonttools` + `brotli`).

## Depois de publicar
- Data e hora de publicação (confirmada por):
- Métrica principal: respostas à pergunta do comentário fixado; guardados e partilhas às 48 h e aos 7 dias contra MB-EP13, MB-EP18 e MB-EP19
- Resultado observado:
- Aprendizagem:

## Encerramento
- [x] Briefing e roteiro definitivo nesta ficha (com a tabela «Alterações ao roteiro de origem»)
- [x] Legenda, comentário fixado e texto alternativo na pasta
- [x] Fontes e evidências (`fontes.md`)
- [x] Controlo de qualidade preenchido
- [x] Localização do vídeo e da capa
- [x] `comum/REGISTRO_EDITORIAL.md` (CONCLUÍDO)
- [x] `comum/historico.md`
- [x] Easter egg em `comum/easter_eggs.md`
- [x] Radar `comum/radar/2026-W48.md` (linhas 6–8)
- [x] `nucleo/SHOWRUNNER.md` §2.4 passo 9 e `nucleo/DECISOES.md` (módulo «deck Commander»)
- [x] `STATUS.md` (e `comum/status_arquivo.md`)
- [x] `memoria.py encerramento MB-EP20`: ENCERRAMENTO OK · `memoria.py validar`: OK · `validar_repo.py`: 0 graves
- [x] Commit enviado e conferido no GitHub (hash no handoff abaixo)
- [x] Handoff entregue
