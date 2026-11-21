# Ficha · Mana & Burn · EP15 · «O gato que já nasce ganhando» (Felidar Sovereign)

Pré-produção (01:51) e produção completa (02:13–02:50). Créditos: só as vozes (ElevenLabs, 1.037 créditos). Capa gerada localmente com o gerador oficial (`manaburn/capas/capa_mb.py`, sem custo).
Marcação: **C** = confirmada (com fonte) · **I** = interpretação · **P** = piada.

## 1. Identificação e classificação*
- ID editorial*: `MB-EP15` (próximo livre: o último no registo é o MB-EP14).
- Estado no registo*: **CONCLUÍDO** (vídeo final com voz, 21/11/2026). Publicação: com o fundador.
- Pedido: «MISSÃO AUTÓNOMA — PRÓXIMO MANA & BURN» (fundador, 21/11/2026, 01:51). Aprovação e produção: «Refine oque achar interessante e coloque o quadro do conde igual o episódio citado […] Comece a criar o vídeo e só pare quando terminar» (fundador, 21/11/2026, 02:13).
- Frente*: Mana & Burn (território «cultura e caos»: carta que provoca reação forte na mesa; não é análise de metagame → não é TUBO).
- Classe*: leitura de carta (carta polémica / regra do Commander). Estratégia: verificação rápida (Oracle + rulings oficiais + regra 903.7).
- Complexidade: baixa. Formato: episódio base (padrão MB-EP11: 14 falas, Burn abre, ≥3 leituras do Mana, pergunta A/B).

## 2. Tese e objetivo*
- **Tese:** o Felidar Sovereign foi impresso para partidas de 20 de vida e ganha o jogo com 40; no Commander todo mundo **começa** com 40, por isso basta ele sobreviver uma volta da mesa sem que você desça dos 40 — e a mesa inteira passa a ser obrigada a te bater.
- **Objetivo:** provocar o «Peraí… isso funciona mesmo?!» e ensinar duas regras que valem guardar (o «se» confere quando a manutenção começa e confere de novo ao resolver).
- **Proposta de valor numa frase:** em ~45 s, com a carta e as rulings oficiais na tela, por que um gato de 2009 ganha sozinho no Commander e o único ponto de dano que o para.
- **Público:** jogador casual e de Commander no Brasil.
- **Relação com o EP13 (o que se reaproveita, sem repetir):** mesma promessa estrutural (estratégia real + demonstração clara + recompensa surpreendente), outra mecânica (vitória alternativa + cláusula «se»), outro objeto, nenhuma construção de deck extrema, nenhum limite de mão, nenhum combo.

## 3. Auditoria de originalidade*
- Leituras feitas (21/11/2026): `AGENTS.md`, `STATUS.md`, constituição, catálogo, `nucleo/SHOWRUNNER.md`, `manaburn/PERFIL.md`, `manaburn/LEIA-ME.md`, `nucleo/DECISOES.md` (15/11, 13/11, 19/11), `comum/REGISTRO_EDITORIAL.md`, `comum/easter_eggs.md`, fichas do MB-EP13 e MB-EP14, `comum/insights/LEIA-ME.md`.
- `python3 comum/ferramentas/memoria.py pauta --objeto "Felidar Sovereign" --tema "condição de vitória alternativa no Commander"` → **PAUTA LIVRE** (21/11/2026). Os dois candidatos preteridos também deram LIVRE.
- Comparação manual: nenhuma linha do registo cita Felidar, Oloro, vitória alternativa ou vida inicial do Commander. MB-EP02 (Stasis) e MB-EP08 (Tabernacle) são cartas odiadas por tranca/imposto; MB-EP11 (Numot, branch) é destruição de terreno; MB-EP13 é construção de 97 terrenos + limite de mão; MB-EP14 é notícia de preço. **Sem conflito.**
- Fora da lista proibida da missão: sem Sanar, Treasure Hunt, Magmakin Artillerist, 97 terrenos, mesmo combo, tese ou sequência narrativa.
- Easter egg novo (não repete `comum/easter_eggs.md`).

## 4. Investigação: três candidatos

### Candidato A · Felidar Sovereign («começa com 40») — **VENCEDOR**
1. **Comandante e cartas:** Felidar Sovereign (não é lendário: vai nas 99). Comandante de apoio do roteiro: Oloro, Ageless Ascetic (ganha 2 de vida na sua manutenção, também da zona de comando). Comandantes que o EDHREC associa: Oloro, Rin and Seri, Arahbo, Brimaz, Mirri, Aunt May, Haliya.
2. **Tese:** carta feita para 20 de vida cuja condição de vitória coincide com a vida inicial do Commander.
3. **Passo a passo:** (1) começa com 40 (CR 903.7); (2) conjura o Felidar (6 manas; turno 6 com um terreno por turno, sem aceleração); (3) a mesa joga; (4) no início da sua manutenção seguinte, se tiver 40 ou mais, o gatilho dispara; (5) ao resolver confere de novo; com 40 ou mais, você vence.
4. **Condições:** Felidar em jogo no início da sua manutenção; vida ≥ 40 nesse instante **e** quando o gatilho resolve.
5. **Como falha:** qualquer dano/perda de vida abaixo de 40 antes da manutenção (o gatilho nem dispara); um ponto em resposta ao gatilho quando você está cravado em 40; remover o Felidar antes da manutenção; ganhar vida **durante** a manutenção não ajuda nessa manutenção (o Oloro engana).
6. **Fontes:** Oracle e rulings do Felidar (Scryfall, j25/198, ruling de 25/08/2015); CR 903.7 (40 de vida); Oracle e rulings do Oloro (Scryfall c13/203); EDHREC (≈2,1 % dos decks elegíveis; ver §5).
7. **Potencial visual:** contador de vida «40» desde o quadro 0, a linha «40 or more life, you win the game» destacada, 38 → 40 com carimbo «NEM DISPARA», −1 em resposta, ecrã de vitória.
8. **Potencial de entretenimento:** o Burn nunca ataca ninguém e descobre que vai perder para um gato; a mesa inteira tem de bater em quem não fez nada. Leva a discussão para o grupo («manda pro amigo do lifegain»).
9. **Diferença face ao EP13:** não é deck absurdo nem combo; é uma regra do formato a transformar uma carta comum em vitória.

### Candidato B · Thassa's Oracle + Demonic Consultation («ganha sem deck»)
1. **Cartas:** Thassa's Oracle {U}{U}; Demonic Consultation {B}. Comandantes Dimir/cEDH (Thrasios + Tymna, Kinnan, Raffine…).
2. **Tese:** grimório vazio costuma perder; aqui é a condição de vitória.
3. **Passo a passo:** conjura o Oracle; com o gatilho na pilha, conjura a Consultation nomeando uma carta que não está no grimório → exila tudo; o gatilho resolve com X (devoção a azul) ≥ 0 cartas → vence.
4. **Condições:** 3 manas (U, U, B), as duas cartas na mão.
5. **Como falha:** anular qualquer das duas; remover o Oracle não para o gatilho; se a Consultation resolver sem o Oracle, você só perde quando comprar (ruling).
6. **Fontes:** Oracle/rulings (Scryfall thb/73, me2/85); Commander Spellbook combo 833; EDHREC: 136.032 decks com o combo (6,51 % de 2.088.541).
7. **Visual:** contador do grimório 99 → 0, muito forte.
8. **Entretenimento:** alto, mas com sal de cEDH.
9. **Diferença face ao EP13:** outra mecânica, mas **é o combo mais conhecido do formato** (EDHREC, artigo de 22/07/2026 sobre os 10 combos mais populares) e exige explicar devoção.

### Candidato C · Biovisionary + Rite of Replication («quatro cópias num formato de uma»)
1. **Cartas:** Biovisionary {1}{G}{U}; Rite of Replication {2}{U}{U}, kicker {5}. Comandantes Simic (Adrix and Nev, Esix, Riku, Volrath…).
2. **Tese:** num formato singleton, a carta pede quatro cópias dela própria — e uma mágica dá cinco.
3. **Passo a passo:** Biovisionary em jogo; Rite com kicker (9 manas) cria 5 fichas cópia → 6 Biovisionary; no início da etapa final, o gatilho confere ≥ 4 → vence.
4. **Condições:** 12 manas no total (ou Biovisionary já em jogo e 9 manas).
5. **Como falha:** anular o Rite; limpar a mesa em resposta ao gatilho (confere de novo ao resolver).
6. **Fontes:** Oracle/rulings (Scryfall gtc/146, soc/202; «fichas cópia contam»); Commander Spellbook 1744-2743; EDHREC: 8.972 decks com o combo (0,45 % de 2.011.832).
7. **Visual:** uma carta a multiplicar-se em seis, excelente.
8. **Entretenimento:** bom; menos dor de mesa.
9. **Diferença face ao EP13:** outra mecânica, mas custa 12 manas e ensina menos regra «para guardar».

### Rubrica de seleção (1–5, interna)

| Critério | A · Felidar | B · Thoracle | C · Biovisionary |
|---|---|---|---|
| Impacto do gancho | 5 | 5 | 4 |
| Originalidade | 4 | 2 | 4 |
| Facilidade de compreensão | 5 | 3 | 4 |
| Potencial visual | 4 | 5 | 5 |
| Potencial de compartilhamento | 5 | 4 | 4 |
| Recompensa narrativa | 4 | 5 | 4 |
| Adequação ao Mana & Burn | 5 | 4 | 4 |
| **Total** | **32** | 28 | 29 |

**Porque A vence:** é o único cujo gancho é verdadeiro numa frase para quem nunca jogou («ganha com 40; no Commander você começa com 40»); a surpresa vem de uma regra exclusiva do formato; tem três correções reais do Mana (custo/manutenção, «se» no início da manutenção, «se» de novo ao resolver), que é o padrão do MB-EP11; e a recompensa é social («a mesa toda tem de te bater»), o tipo de coisa que se manda para alguém do grupo. B fica atrás em originalidade e clareza; C fica como **reserva forte** para um episódio futuro (mesma rubrica, pauta livre).

## 5. Fontes e evidências*

| Afirmação | Tipo | Fonte | Data da consulta |
|---|---|---|---|
| Texto do Felidar Sovereign {4}{W}{W}, 4/6, vigilância, vínculo com a vida, «At the beginning of your upkeep, if you have 40 or more life, you win the game.» Impressão na TV: Foundations Jumpstart (2024), nº 198, arte Zoltan Boros & Gabor Szikszai | facto | https://scryfall.com/card/j25/198 (API `cards/j25/198`) | 21/11/2026 |
| Ruling: confere a vida quando a manutenção começa; se não tiver 40, nem dispara; se disparar, confere de novo ao resolver; sem 40 nesse momento, não faz nada | facto | ruling Wizards de 25/08/2015, via Scryfall (`rulings` do Felidar) | 21/11/2026 |
| Ruling: no Two-Headed Giant a vida é a da dupla | facto | idem | 21/11/2026 |
| Primeira impressão: Zendikar (2009-10-02), mítica | facto | Scryfall, impressões do Felidar | 21/11/2026 |
| Legal no Commander | facto | Scryfall (`legalities.commander = legal`) | 21/11/2026 |
| Vida inicial 40 no Commander | facto | CR 903.7 (citada no blog de regras dos juízes); magic.wizards.com/Commander («Each player starts with 40 life») | 21/11/2026 |
| Oloro: «At the beginning of your upkeep, you gain 2 life»; da zona de comando também ganha 2 na manutenção; dispara já na 1.ª manutenção se for o comandante | facto | https://scryfall.com/card/c13/203 + rulings de 17/10/2013 | 21/11/2026 |
| Oloro a 38 não liga o Felidar na mesma manutenção | inferência (aplicação direta da ruling do Felidar) | rulings acima | 21/11/2026 |
| Turno 6 / vitória no turno 7 | cálculo (um terreno por turno, sem aceleração, sem perder vida) | aritmética | 21/11/2026 |
| ≈2,1 % dos decks elegíveis no EDHREC | facto, com limitação | página do EDHREC lida por resultados de pesquisa (2,08–2,09 %; contagens 76,4 mil–86,3 mil conforme a cópia em cache) | 21/11/2026 |
| Candidatos B e C (contagens de combo) | facto | edhrec.com/combos/thassas-oracle; edhrec.com/combos/biovisionary; commanderspellbook.com/combo/833 e /1744-2743 | 21/11/2026 |

**Limitações:** EDHREC, Commander Spellbook e o PDF das Regras Completas não abrem desta sessão (bloqueio de rede); os números do EDHREC vêm dos excertos da pesquisa e divergem entre cópias → **o vídeo não mostra contagem de decks**. Salt Score do Felidar não verificado → **sem putômetro** (regra do perfil). Nada de preços. Nenhum resultado de partida, estatística de vitória ou frequência é afirmado.

## 6. Lista de cartas e imagens necessárias (todas reais, nenhuma paga)
| Uso | Imagem | Origem |
|---|---|---|
| TV, quadro 0, falas 1, 2, 7, 10, 12; capa | Felidar Sovereign j25/198 (PNG) | Scryfall |
| Insert fala 5 | Oloro, Ageless Ascetic c13/203 (Commander 2013, arte Eric Deschamps) | Scryfall |
| Tela fala 1 (meio) | «REGRA 903.7 · VIDA INICIAL 40» com a fonte | `telas_visuais.py` (texto real) |
| Telas falas 6 e 8 | texto oficial da ruling (25/08/2015) com a linha destacada e «Wizards, via Scryfall» | `telas_visuais.py` |
| Telas falas 3, 4, 11, 13 | contador de turno, mesa com setas, placar, tela A/B | `telas_visuais.py` |
| Fecho | `comum/outro/outro_binder_916.mp4` | repositório |

## 7. Gancho visual* (7 campos, antes do roteiro)
1. **Quadro 0:** TV SAL já acesa (`tv_ligada`) com o Felidar Sovereign inteiro e um contador de vida gigante «40» a amarelo ao lado; a última linha do texto da carta já destacada.
2. **Objeto:** a carta real (j25/198) + o número 40.
3. **Ação no 1.º segundo:** o «40» entra com «pop» e o Burn aponta para a TV; a ~2,6 s (em «COMEÇA») troca de canal para «REGRA 903.7 · VIDA INICIAL 40» e um carimbo «= VITÓRIA?».
4. **Som:** «pop» no 40, `static` na troca de canal, `zap` de raiva do Burn (biblioteca `manaburn/sfx.py`).
5. **Descoberta até 3 s:** «ganha com 40» + «começa com 40» legível sem som (carta + contador + carimbo).
6. **Promessa:** descobrir se isso funciona mesmo e o que o para.
7. **Pagamento:** ~37,5 s (fala 12): tela «MANUTENÇÃO · VIDA 40 · VOCÊ VENCEU» com o Felidar a brilhar (`thump` + `pop`); o que o para (um ponto em resposta) sai na fala 8 (~26,7 s).

| Rubrica (1–5) | Prevista | Medida no final |
|---|---|---|
| Relevância visual | 5 | — |
| Impacto inicial | 4 | — |
| Clareza | 5 | — |
| Curiosidade | 5 | — |
| Pagamento | 5 | — |
| Identidade | 5 | — |

Teste de genericidade: trocar a carta e o número quebra o gancho (só o Felidar tem «40» e só o Commander começa em 40). OK.

## 8. Roteiro definitivo proposto* (14 falas, 143 palavras; Burn abre; *asteriscos* = amarelo na legenda)
1. **B** [shouting] — Esse gato ganha com *40 de vida*. E no Commander a gente *COMEÇA* com 40!
2. **M** [bored] — *Lê a carta.* Na *sua manutenção*. E custa *seis*.
3. **B** [shouting] — Baixo no turno seis, ganho no *sete*!
4. **M** [deadpan] — Se a vez voltar com *40 ou mais*. A mesa *inteira* joga antes.
5. **B** [outraged] — Meu comandante, *Oloro*, me dá *2 na manutenção*: 38 vira 40 e *ganho na hora*!
6. **M** [tired] — Não. Ele confere quando a manutenção *começa*. Com 38, *nem dispara*.
7. **B** — Tá. Mas disparou? *Já era*.
8. **M** [deadpan] — Confere *de novo* ao resolver. Cravado em 40? *Um* ponto em resposta e *acabou*.
9. **B** [shouting] — *UM PONTO?!* Esse gato é *inútil*!
10. **M** [bored] — *Vigilância* e *vínculo*: bate, *ganha vida* e fica de guarda.
11. **B** [outraged] — A mesa *inteira* tem que me bater… ou *perde pra um gato*?!
12. **M** [deadpan] — Ou some com o gato. Se não: manutenção, *40*… *vitória*.
13. **B** — *A*: bato no dono. *B*: tiro o gato da mesa.
14. **M** [bored] — Comenta aí.

Pronúncia (campo `tts` em `episode.json` na montagem): Oloro → «Olôro»; Commander → «Comânder»; números por extenso («quarenta», «trinta e oito»). «Vínculo» = vínculo com a vida (lifelink); a tela mostra a palavra inteira. Ouvir antes de publicar.

**Revisão narrativa (§4.2):** tese numa frase ✔ · pauta livre ✔ · clareza aos 3 s ✔ (carta + 40 + regra) · progressão: promessa → custo/timing → condição → engano do Oloro → segundo «se» → valor do gato → consequência social → pagamento → pergunta ✔ · evidência real em cada fala ✔ (§9) · ritmo ≤ 3 s (troca a meio das falas 1, 4, 5, 6, 8, 10, 11) ✔ · recompensa no segundo previsto ✔ · relevância: regra que vale guardar ✔ · CTA único (A/B) ✔.
**Rigor das falas:** 3 (turno 7) é a fala do Burn e só é verdadeira com um terreno por turno, sem aceleração e sem perder vida; o Mana corrige para a condição real (4). 11 é exagero do Burn (**P/I**); 12 corrige-o (também se para tirando o gato). 8 diz «cravado em 40» porque, acima de 40, um ponto não chega. 10: vigilância = atacar não vira a criatura, fica para bloquear (**C**).

## 9. Storyboard com timecodes (estimativa a 3,3 palavras/s, ritmo medido no MB-EP14; reajustar com `process.py` depois das vozes)

| # | Tempo | Plano | TV SAL / insert | Troca a meio | Destaque / animação | Som |
|---|---|---|---|---|---|---|
| 0 | 0,0–0,3 | TV (zoom 1.5), já acesa | Felidar inteiro + contador «40» | — | linha «…40 or more life, you win the game» já destacada | trilha |
| 1 | 0,3–4,8 | TV | Felidar + «40» | 2,6 s → «REGRA 903.7 · VIDA INICIAL 40» + carimbo «= VITÓRIA?» | «40» em pop | pop · static · zap |
| 2 | 4,9–7,6 | TV | Felidar | 6,3 s → zoom no custo {4}{W}{W} «= 6» | destaque «At the beginning of your upkeep» | static · marker |
| 3 | 7,7–9,8 | cuB (tremor leve) | insert «TURNO 6 → 7» | — | número em pop | pop |
| 4 | 9,8–13,8 | TV | mesa de 4 lugares, seta a girar | 11,8 s → «40 OU MAIS?» | seta passa pelos 3 oponentes | static · click |
| 5 | 13,8–19,0 | cuB | insert Oloro (c13/203) | 16,4 s → contador 38 → 40 | linha «you gain 2 life» destacada | flick · pop · zap |
| 6 | 19,0–23,0 | TV | ruling oficial (25/08/2015) | 21,0 s → carimbo «38 = NEM DISPARA» | «as your upkeep begins… won't trigger at all» | static · marker · thump |
| 7 | 23,0–24,5 | conjunto | Felidar + ícone «GATILHO NA PILHA» | — | — | click |
| 8 | 24,6–28,8 | TV | ruling (2.ª frase) | 26,7 s → contador 40 → 39 «−1» | «check again as it tries to resolve» | static · marker · pop |
| 9 | 28,9–30,7 | cuB com tremor, caixa alta | insert «1» gigante | — | — | zap |
| 10 | 30,7–33,8 | TV | Felidar | 32,3 s → destaque passa de «Vigilance» para «Lifelink»; contador 40 → 44 | — | static · marker · pop |
| 11 | 33,8–37,5 | cuB → conjunto | setas dos 3 oponentes para o Burn | 35,6 s → placar «Jogadores putos: 3 de 3» | — | static · zap |
| 12 | 37,5–40,5 | TV | «MANUTENÇÃO · VIDA 40 · VOCÊ VENCEU» com o Felidar | — | brilho + carimbo (**pagamento**) | thump · pop |
| 13 | 40,6–43,6 | conjunto | tela A/B: A (alvo no jogador) · B (gato fora da mesa) | — | A e B em pop | static · pop |
| 14 | 43,7–44,3 | conjunto | — | — | «Comenta aí» na parada seca | — |
| — | 44,3–45,2 | TV desliga → ponto verde | — | — | — | crt_off |
| — | 45,2–~49,1 | fecho do scanner | `outro_binder_916.mp4` | — | — | fecho |

Maior intervalo sem mudança visual previsto: 2,6 s. Duração prevista ≈ 49 s com o fecho (EP13: 45,83 s); as réplicas por cima do Burn devem tirar 1–2 s. Se passar de 50 s, corta-se primeiro a fala 7 (fundindo «Já era» na 5) — decisão a registar.

## 10. Direção de voz e sonoplastia
- Vozes aprovadas da série (sem mudar): Burn = Talis (eleven_v4), Mana = Erik. Um nó por personagem, falas na ordem, separadas por `[long pause]`; tags como no roteiro. **Não gerar sem autorização** (estimativa pelo histórico: ~950–1.050 créditos, como EP12/EP14).
- Burn: sobe a cada fala até ao pico da 9 («UM PONTO?!», caixa alta com tremor) e da 11; réplicas entram por cima do Mana.
- Mana: seco, sem pressa, nunca grita; a 12 é dita devagar, com micro-pausa antes de «vitória».
- Trilha da série desde o quadro 0; parada seca em «Comenta aí»; a pancada desliga a TV. −14 LUFS, pico < −1 dBTP.
- Sons só da biblioteca (`manaburn/sfx.py`): `static` em cada troca de canal, `marker` em cada destaque de linha, `pop` em números, `flick` na entrada do Oloro, `zap`/`thump` nas reações, `crt_off` no fim.

## 11. Instruções para a TV SAL (`EP.tv`)
- **Putômetro: fora** (Salt Score do Felidar não verificado nesta sessão).
- **Placar da mesa:** «Jogadores putos: 3 de 3» só na fala 11 (a lógica sustenta: são eles que têm de atacar).
- **Relógio (easter egg):** «20:40» no canto inferior direito, em todos os planos da TV.
- **Manchetes de plantão (8):**
  1. PLANTÃO: gato de 2009 descobre que o Commander começa com 40 (**C**: Zendikar, 02/10/2009)
  2. Mesa pacifista convocada para reunião de emergência (**P**)
  3. Pinger de 1 de dano é promovido a herói da mesa (**P**)
  4. O «se» confere duas vezes, igual mãe na porta (**P** sobre regra **C**)
  5. Vigilância: o gato bate e continua de guarda (**C**)
  6. Two-Headed Giant: a vida é da dupla, diz a ruling (**C**)
  7. Último plantão: 97 terrenos e vitória no turno 5 (chamada do MB-EP13)
  8. Próximo plantão: [teaser a definir pelo fundador; se não houver, sai a manchete]
- Crédito no rodapé da TV: «Na TV: Felidar Sovereign (Foundations Jumpstart, 2024), nº 198. Arte: Zoltan Boros & Gabor Szikszai. © Wizards of the Coast.»

## 12. Capa (modelo oficial de 14/11)
`MB_EP15_CAPA.png` e `MB_EP15_CAPA_grelha.png` nesta pasta (gerados a 21/11/2026, sem custo):
`python3 capas/capa_mb.py --scryfall j25/198 --frase "No Commander, começa com" --foco "40" --selo "40 = vitória?" --ep 15 --tag COMMANDER --saida episodios/ep15_felidar/MB_EP15_CAPA.png`
Conferido no recorte 3:4: nome da carta e criatura livres; selo sobre a rocha, não sobre o gato. O número «EP. 15» é provisório até à aprovação.

## 13. Legenda, comentário fixado e texto alternativo
Ficheiros `legenda.txt`, `comentario_fixado.txt`, `texto_alternativo.txt` nesta pasta (rascunhos para aprovação; o alt descreve o vídeo planeado e revê-se no render final).

## 14. Easter egg
Relógio da TV SAL em «20:40» = os 20 de vida do formato para que o Felidar foi feito e os 40 com que o Commander começa.

## 15. Métrica principal e hipótese
- **Métrica principal (desta missão):** guardados + compartilhamentos por 1.000 visualizações. Referência MB-EP13: 353 / 11.000 ≈ 32,1 por mil. Secundárias: % média assistida (EP13: 30,44 s de 45,83 s ≈ 66,4 %) e respostas A/B no comentário fixado (métrica por defeito do perfil).
- **Hipótese:** um episódio de interação de regras com pagamento demonstrável (vitória na manutenção) obtém guardados + compartilhamentos por mil comparáveis aos do EP13, sem depender de um deck extremo.
- **Variável em teste:** tipo de surpresa — regra/interação (EP15) × construção de deck (EP13). Comparação só se os dois tiverem o mesmo estado de impulso (EP13: impulso **A CONFIRMAR**), idade parecida no print e leitura a 48 h e 7 dias (`comum/insights/LEIA-ME.md`). Nenhuma causalidade se tira de um par.

## 16. Controlo de qualidade (pré-produção)
| Critério | Resultado |
|---|---|
| Oracle | Felidar, Oloro conferidos no Scryfall (21/11) |
| Sequência das interações | gatilhos de manutenção com «se»: ruling oficial; Oloro depois do início da manutenção |
| Regras de Commander | 40 de vida (903.7); Felidar legal; nas 99 (não lendário) |
| Cálculos | turno 6/7 só sem aceleração e sem perder vida (dito como fala do Burn, corrigida) |
| Fontes e datas | §5; limitações declaradas |
| Fala ↔ imagem | §9: imagem real em cada fala |
| Clareza casual | gancho percebe-se sem saber o que é «manutenção» (a fala 2 explica) |
| Originalidade | pauta livre + comparação manual |
| Retenção e recompensa | mudança ≤ 3 s prevista; pagamento a ~37,5 s |
| P0 abertos | nenhum. **P1 a resolver no render:** medir o quadro 0 e o maior intervalo no ficheiro final |

## 17. Depende do fundador
1. Aprovar pauta e roteiro (ou pedir ajustes) — só depois disto a voz.
2. Autorizar ~1.000 créditos ElevenLabs (estimativa) para Talis + Erik.
3. Teaser da manchete 8 (ou retirar).
4. Confirmar o estado de impulso e a data de publicação do MB-EP13 (as métricas da missão indicam que já saiu; o registo ainda diz CONCLUÍDO, não publicado).
5. Par de publicação (carrossel do app no dia seguinte) precisa de capturas reais do scanner/coleção.

## 18. Produção e controlo de qualidade final (21/11/2026)

**Refinamentos face à proposta das 01:51:** roteiro encurtado de 166 para 143 palavras (EP13 ≈ 110, EP14 ≈ 142) para não alongar; «Vigilância e vínculo com a vida» → «Vigilância e vínculo» na fala (a tela mostra a palavra inteira); fala 12 com revelação em dois tempos na TV (aos 62 % da fala entra «VOCÊ VENCEU», em «vitória») para pagar o gancho com som e imagem e manter a troca ≤ 3 s; destaques reais sobre o texto do Felidar (manutenção nas falas 2; vigilância e vínculo na fala 10) e sobre a ruling (falas 6 e 8); Oloro com a linha «you gain 2 life» marcada no insert; contador da TV SAL «SUA VIDA» (exemplo de partida: 40 · 38 · 39 · 44) com a conta «início: 40 · regra 903.7».
**Quadro do Conde de Manaforte na parede** como no MB-EP13 (kit v3 integrado na `main` a 21/11; padrão da série desde esta data, `nucleo/DECISOES.md`). Expressões: 1–2 neutro · 3–4 desconfiado · 5 indignado · 6 desconfiado · 7–8 admirado · 9 indignado · 10 admirado · 11 indignado · 12 admirado · 13–14 neutro (só mudam no início de cada plano).
**Mensagem subliminar pedida pelo fundador: não aplicada** (proibida em Portugal e abusiva no Brasil; ver `nucleo/DECISOES.md`, 21/11). O easter egg visível (relógio 20:40) e a linha «Tem um detalhe escondido na TV» no comentário fixado ficam como alternativa honesta.

**Vozes:** ElevenLabs eleven_v4, flow «Mana & Burn — MB-EP15 (Felidar)» (1IYxWFcByrxAhJZACiLR). Burn: Talis (E9a8LlXPNWtyvvSoZzrb), 500 créditos, 28,32 s. Mana: Erik (nfiLpQ54jEQninp3nNqL), 537 créditos, 31,52 s. Uma geração cada, sem repetição. Faixas: `faixas_elevenlabs.txt`. Corte pelo `tts` (`episodios/ep14_everything/processar_vozes.py`), ritmo Burn ×1,1, Mana ×1,15, silêncios internos ≤ 0,10 s.

**Montagem:** kit da `main` + `kit/v3` (quadro do Conde); telas `telas_felidar.py` → `cards/`; `processar_vozes.py burn.mp3 mana.mp3` → `render.py` → `episodios/ep14_everything/juntar_fecho.py kit.mp4 comum/outro/outro_binder_916.mp4 final.mp4 0`. Playwright com o Chrome do sistema.

**Tempos reais (process.py):** 1 B 0,35 · 2 M 4,39 · 3 B 7,52 · 4 M 9,53 · 5 B 12,94 · 6 M 17,36 · 7 B 20,85 · 8 M 22,37 · 9 B 26,13 · 10 M 28,20 · 11 B 31,45 · 12 M 34,28 (VOCÊ VENCEU a 36,46) · 13 B 37,79 · 14 M 40,56 · pancada 41,81 · fecho 42,33.

| Critério | Alvo | Medido | OK |
|---|---|---|---|
| Resolução / fps | 1080×1920, 30 | 1080×1920, 30 | ✔ |
| Duração | livre; ref. EP13 45,83 s | **46,20 s** (42,33 s + fecho 3,87 s) | ✔ |
| Loudness / pico | −14 LUFS / < −1 dBTP | −14,7 LUFS / −1,3 dBTP | ✔ (EP13: −14,5) |
| Fecho do scanner | presente | presente a 42,33 s | ✔ |
| Bordas da TV (`bordas.py`) | OK | 748 quadros, laterais 12–1068 px | ✔ |
| Quadro 0 | carta + 40 legíveis sem som | Felidar + «VIDA 40» + linha da carta na TV SAL acesa | ✔ |
| Mudança visual ≤ 3 s | ≤ 3 s | maior intervalo ≈ 2,8 s (31,43→34,27) | ✔ |
| Som em cada revelação | sim | troca de canal, destaque, cartas, raiva (process.py: 4 destaques, 5 cartas, 7 zaps) | ✔ |
| Pagamento do gancho | ~37,5 s | «VOCÊ VENCEU» a 36,46 s | ✔ |
| Destaques alinhados | sim | conferidos a 6,5 s (manutenção) e 19,5 s (ruling) | ✔ |
| Factos = ficha | sim | sim | ✔ |

Nota: o medidor «SUA VIDA» do quadro 0 ainda está a subir (mostra 0 nos primeiros 0,35 s e chega a 40 com a animação padrão do kit); a tela ao lado já mostra «40» gigante.

| Rubrica (medida na folha de contacto, sem som) | Medida |
|---|---|
| Relevância visual | 5 |
| Impacto inicial | 4 |
| Clareza | 5 |
| Curiosidade | 5 |
| Pagamento | 5 |
| Identidade | 5 |

### Ficheiros finais
- Vídeo `ManaBurn_Ep15_Felidar_916.mp4` (46,20 s) e capa `MB_EP15_CAPA.png`: entregues na conversa de 21/11/2026 (vídeo não versionado). Folha de contacto: `folha_contacto.png`.
