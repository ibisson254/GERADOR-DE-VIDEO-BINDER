# Ficha · Mana & Burn · EP18 · «O Lagarto Infinito» (Basking Broodscale + Rosie Cotton + Corpse Knight)

## Identificação
- ID editorial: MB-EP18
- Estado no registo: CONCLUÍDO (ver «Controlo de qualidade»)
- Aprovação do fundador: missão «PROMPT DE ENGENHARIA AVANÇADA — MB-EP18 · O LAGARTO INFINITO · PRODUÇÃO COMPLETA ATÉ AO VÍDEO FINAL» (projeto claude.ai, 26/11/2026 17:08), com comandantes, combo e finalizador já decididos pelo fundador; orçamento do deck **R$ 300** e **vozes autorizadas** no cartão de decisão (26/11/2026 17:18); «prossiga» (17:22).

## Classificação
- Frente: Mana & Burn (série) · formato base 14 falas, Commander
- Classe: leitura de carta / combo (verificação rápida: Oracle + rulings + Commander Spellbook/EDHREC com data)
- Complexidade: média (combo com gatilhos e alvo)
- Estratégia: «isso funciona mesmo?!» com recompensa visível (referência de retenção: MB-EP13, «97 terrenos»)

## Originalidade
- Objeto: Basking Broodscale + Rosie Cotton of South Lane (+ Corpse Knight); comandantes Frodo, Adventurous Hobbit e Sam, Loyal Attendant
- `python3 comum/ferramentas/memoria.py pauta --objeto "Basking Broodscale + Rosie Cotton of South Lane" --tema "Commander: combo de fichas infinitas com Corpse Knight (Frodo e Sam)"` → **PAUTA LIVRE** (26/11/2026, uma vez, regra E3)
- Relações: MB-EP13 (referência de construção narrativa: absurdo → explicação simples → recompensa visível; outro objeto e outra mecânica); MB-EP15 (40 de vida do Commander reaproveitado como conta, não como tese); MB-EP16 (plano de prova)

## Pesquisa de pauta (§2.4)
- Tema e cartas definidos pelo fundador (decisões «não reabrir»). Ângulos comparados (≥ 2, tema dado):

| Ângulo | Gancho | Orig. | Compr. | Visual | Partilha | Recomp. | Adequação | Total |
|---|---|---|---|---|---|---|---|---|
| A · **«lagarto de duas manas cria infinito e acaba com a mesa»** (combo + finalizador, correções de regra) — VENCEDOR | 5 | 4 | 4 | 5 | 4 | 5 | 5 | 32 |
| B · «o deck dos hobbits que come a mesa» (Frodo e Sam, Comida) | 3 | 4 | 4 | 3 | 3 | 3 | 4 | 24 |
| C · «combo de R$ 6 que é bracket 4» (preço e nível de poder) | 4 | 4 | 3 | 3 | 4 | 3 | 3 | 24 |

- A vence: o número do gancho (duas manas → infinito) é visível na carta, o ciclo é desenhável passo a passo e dá quatro leituras reais ao Mana. C fica de reserva, mas exige preço brasileiro verificado (não conseguido nesta sessão).
- Radar: `comum/radar/2026-W48.md` criado nesta sessão (linhas 1–3; Brasil e Europa sem dado, limitação registada).
- Limitações: LigaMagic e MYP Cards bloqueiam acesso automático (Cloudflare); Reddit não aberto. Nada disso entra no vídeo.

## Editorial
- Objetivo: respostas A/B no comentário fixado; secundária: guardados e partilhas.
- Proposta de valor: perceber, sem saber o combo, porque duas cartas baratas criam infinito e qual a terceira que transforma isso em vitória.
- Hipótese: a estrutura do MB-EP13 (absurdo com número → explicação simples → recompensa que se vê) repete o desempenho orgânico com um objeto novo. Comparar às 48 h e aos 7 dias com o MB-EP15/MB-EP16 (sem impulso).
- Tese: duas cartas fazem o infinito; a terceira faz a vitória; e o ciclo para se alguém responder.

## Auditoria técnica do combo (Oracle, 26/11/2026)
1. Basking Broodscale ({1}{G}, 2/2): «Whenever one or more +1/+1 counters are put on this creature, **you may** create a 0/1 colorless Eldrazi Spawn creature token with "Sacrifice this token: Add {C}."»
2. Rosie Cotton of South Lane ({2}{W}, 1/1): ao entrar cria Comida; «Whenever you **create a token**, put a +1/+1 counter on **target** creature you control other than Rosie Cotton.»
3. Corpse Knight ({W}{B}, 2/2): «Whenever another creature you control enters, each opponent loses 1 life.»
4. Mirkwood Bats ({3}{B}): «Whenever you create or sacrifice a token, each opponent loses 1 life.» Fica como **alternativa no comentário**, não no vídeo: não há razão técnica para trocar (Corpse Knight custa 2 e é procurado pelo Recruiter of the Guard e pelo Corpse Harvester; os Bats custam 4).

**Correções à explicação proposta (aplicadas no roteiro):**
- Passo 6 da missão («a entrada da ficha desencadeia a Rosie»): a Rosie dispara ao **criar** a ficha, não à entrada. (Para o Corpse Knight, sim, conta a entrada.)
- O lagarto **pode** criar (opcional): o ciclo é arbitrariamente grande, não obrigatório; o jogador escolhe o número (por isso «Acaba quando você quiser»).
- A Rosie **tem alvo**: cada gatilho escolhe o lagarto. Com o lagarto removido em resposta, o gatilho perde o alvo e o ciclo acaba; removida a Rosie, o gatilho que já está na pilha resolve, mas não nasce o seguinte; removido o Corpse Knight, as fichas continuam e a mesa deixa de perder vida.
- Cada gatilho usa a pilha (os oponentes têm prioridade entre eles): o combo **não é** invulnerável.
- A vida perde-se 1 a 1 por Spawn: 40 Spawns zeram 3 oponentes a 40 (sem ganho de vida da mesa; marcado «EXEMPLO»).
- Combo de duas cartas = fichas, marcadores e mana incolor infinitos (Commander Spellbook 2433-5641, pré-requisito: lagarto em campo, Rosie na mão, {2}{W}). A vitória precisa da terceira carta.
- Gancho proposto («Esse lagarto de duas manas pode criar criaturas infinitas… e acabar com a mesa!») mantido: o custo é {1}{G} (2), o «pode» cobre a dependência da Rosie, e o vídeo paga com o Corpse Knight.

## Deck de 100 cartas
`DECK.md` (lista, plano de jogo, curva, simulação, faixa de poder, preços), `lista_ligamagic.txt`, `MB-EP18_deck_precos.csv`. Legalidade e identidade conferidas carta a carta no Scryfall. Estimativa **R$ 290,15** (99 cartas, Sam sem preço fiável), **R$ 259,10 sem básicos**, combo de 3 cartas R$ 5,92 — referência internacional convertida (Cards Realm), **não verificada em loja brasileira**. O vídeo não fala de preço.

## Gancho visual (7 campos)
1. Quadro 0: Basking Broodscale em tela cheia, linha dos marcadores destacada, selo «2 MANAS → ∞» na arte.
2. Objeto: carta oficial (PNG do Scryfall, MH3 145).
3. Ação: entra com impacto 0,18 s; voa para a TV quando o Burn diz «infinitas» (`ate` 0,55 ≈ 2,7 s do vídeo).
4. Som: pancada + pop; zap na saída.
5. Descoberta: um lagarto de duas manas promete infinito.
6. Promessa: como, e como isso ganha da mesa.
7. Pagamento: ciclo (19,8–23,9 s) e mesa a 0 (36,5–38,9 s).

## Roteiro definitivo
`episode.json` (14 falas). Texto falado em `faixas_elevenlabs.txt`.

## Alterações ao roteiro de origem (§4.3)
O roteiro preliminar do fundador não está no repositório; da missão vieram a estrutura, o gancho e a ordem da revelação. Alterações:

| Rascunho (missão) | Final | Porquê |
|---|---|---|
| «a entrada da ficha desencadeia novamente Rosie» | «Spawn é ficha: Rosie de novo» | a Rosie conta criação, não entrada (Oracle) |
| ciclo sem fim | «O lagarto diz pode criar. Acaba quando você quiser.» | «you may» (Oracle) |
| vitória sem condição | «Se ninguém responder. Removeu o lagarto no meio, o ciclo para.» | a missão pede não dizer que é invulnerável |
| «cada ficha que entra faz cada adversário perder vida» | «Quarenta Spawns… e a mesa inteira cai!» + painel 40 → 0 | número concreto, visual e verdadeiro (regra 903.7) |
| fecho do Burn com humor | A/B «mata o lagarto / mata o cavaleiro» | padrão da série: penúltima fala = 1.ª linha do comentário fixado |

## Produção
- Recursos reutilizados: kit v2 + v3 (sala, dupla, TV SAL, Conde), abertura de carta, plano de prova (MB-EP16 v2), `processar_vozes.py` (corte pelo `tts`), `previa_sem_voz.py`, `juntar_fecho.py` (MB-EP16), `capas/capa_mb.py`. Telas novas: `telas_lagarto.py` (9 painéis, só cartas e fichas reais).
- Vozes: ElevenLabs eleven_v4, flow «Mana & Burn — MB-EP18 (O Lagarto Infinito)» (`dKtmlDCnOjU1Otwxi15R`). Burn: Talis (`E9a8LlXPNWtyvvSoZzrb`), 485 créditos, 24,0 s. Mana: Erik (`nfiLpQ54jEQninp3nNqL`), 658 créditos, 42,5 s. **Total 1.143 créditos**, uma geração cada, sem repetição. IDs confirmados no `creative_list_voices` e iguais aos episódios anteriores.
- Easter egg: relógio da TV SAL em «01:45» = nº de coleção do Basking Broodscale (MH3 145).
- Putômetro: Salt EDHREC do lagarto 0,53 ÷ 4 = 13 %.
- Quadro do Conde: uma expressão por fala; `check_quadro.py` OK (todas as trocas num corte).
- Ambiente: liberados no ambiente cloud (com aprovação do fundador) api.scryfall.com, cards.scryfall.io, edhrec.com, json.edhrec.com, mtg.cardsrealm.com, elevenlabsusercontent.com; LigaMagic e MYP continuam bloqueadas por anti-robô.
- Riscos: factuais (mitigados pela leitura do Oracle e pelas correções acima); direitos (cartas e artes © Wizards of the Coast, com crédito na tela e na legenda; conteúdo de fã).
- Limitações conhecidas: preços do deck não verificados em loja brasileira (ver `DECK.md`); o vídeo não usa preço.

## Fontes e evidências
Ver `fontes.md` (Oracle e rulings no Scryfall, Commander Spellbook, EDHREC Salt, Cards Realm, Regras Completas 903.7; consultas a 26/11/2026).

Limitações: LigaMagic e MYP Cards sem acesso automático (Cloudflare); Sam, Loyal Attendant com uma única oferta de R$ 237,56 (fora do total, NÃO VERIFICADO).
Capturas ou exportações: `MB-EP18_deck_precos.csv`, `DECK.md`.
Créditos e autorizações de terceiros: não se aplica (só cartas oficiais com crédito).

## Controlo de qualidade
Medido no ficheiro final `ManaBurn_Ep18_LagartoInfinito_916.mp4` com `python3 -I comum/qc/qc_video.py … --frente manaburn` (26/11/2026, 17:45).

| Critério | Alvo | Medido | OK |
|---|---|---|---|
| Resolução / fps | 1080×1920, 30 fps | 1080×1920, 30 fps | ✓ |
| Duração | ~42–46 s + fecho | 51,17 s (47,30 s + fecho de 3,87 s) | ✓ (14 falas; +1 s face ao EP15 por causa da 3.ª carta) |
| Corte lateral (cropdetect) | nenhum | 1080:1920:0:0 em todos os quadros | ✓ |
| Loudness / pico | −14 LUFS / < −1 dBFS | −14,7 LUFS / −1,3 dBTP | ✓ |
| Fecho do scanner | presente | presente a partir de 47,3 s (dif. 0,07) | ✓ |
| Factos = ficha | sim | sim (Oracle de 26/11) | ✓ |
| Quadro 0 | carta + selo, legível sem som | Basking Broodscale inteira, linha dos marcadores destacada, selo «2 MANAS → ∞» | ✓ |
| Descoberta | ≤ 3,0 s | carta voa para a TV de 2,73 a 3,0 s, quando o Burn diz «infinitas» | ✓ (o `ate` 0,55 passa 0,2 s do máximo de 2,5 s da skill: escolhido para a saída cair na palavra do selo «∞») |
| Pagamento do gancho | campo 7 | ciclo 19,7–23,9 s; mesa a 0 em 36,5–38,9 s | ✓ |
| Maior intervalo sem mudança visual | ≤ 3 s | 3,13 s (fala 8, Burn no sofá: há movimento das personagens, sem troca de plano) e 3,23 s na fala 12 (troca `meio` discreta «COMENTA AÍ» aos 43,7 s) | aceite (P2) |
| Retenção | quadro 0 com Magic · mudança ≤ 3 s · som em cada revelação | sim · ver linha anterior · pancada, flips e destaques com som | ✓ |
| P0 / P1 abertos | 0 / 0 | 0 / 0 | ✓ |

Outros controlos: `check_quadro.py` OK; `bordas.py` OK (1.121 quadros da TV); folha de contacto conferida a olho (`folha_contacto_final.png`): cartas inteiras, sem nada sobre o texto, destaques alinhados, legendas na zona segura.

## Ficheiros finais
- Vídeo final: `ManaBurn_Ep18_LagartoInfinito_916.mp4` · 51,17 s · entregue ao fundador na conversa de 26/11/2026 (projeto claude.ai, ficheiros do projeto); não versionado.
- Capa: `MB_EP18_CAPA.png` (nesta pasta; frase «O LAGARTO» + foco «INFINITO», selo «COMBO DE 2 CARTAS», faixa «MANA & BURN · EP.18», tag COMMANDER; o glifo ∞ não existe na fonte Bangers, por isso não entra na capa). Grelha 3:4: `MB_EP18_CAPA_grelha.png`.

## Pacote de publicação
- [x] `legenda.txt`
- [x] `comentario_fixado.txt`
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
- [x] `memoria.py encerramento MB-EP18`
- [x] Commit enviado e conferido no GitHub (hash no handoff do `STATUS.md`)
- [x] Handoff entregue

## Reproduzir
Kit numa cópia de trabalho (manaburn/ sem episodios/), `episode.js`/`episode.json` na raiz, `cards/src/` com os PNG do Scryfall (mh3/145, ltr/27, moc/321 redimensionada a 744×1040, tmh3/2, tltr/10, trc/429), `CHROME=/usr/bin/google-chrome python3 telas_lagarto.py`, `python3 processar_vozes.py burn18.mp3 mana18.mp3`, `python3 bordas.py`, `python3 render.py …_kit.mp4`, `python3 juntar_fecho.py …_kit.mp4 comum/outro/outro_binder_916.mp4 …_916.mp4 0`.

## Depois de publicar
- Data e hora de publicação (confirmada por): 
- Métrica principal: respostas A/B; guardados e partilhas às 48 h e aos 7 dias contra MB-EP15/MB-EP16
- Resultado observado: 
- Aprendizagem: 
