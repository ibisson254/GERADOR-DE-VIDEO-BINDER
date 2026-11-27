# Ficha · Meta em Curto · EP09 · cEDH na Mercadia Games: o motor do deck campeão

## Identificação
- ID editorial: `MC-EP09` (próximo número livre da série; MC-EP08/EP08B são os últimos; PAU e ESP têm numeração própria)
- Estado no registo: CONCLUÍDO (27/11/2026, 15h20)
- Pedido do fundador: «MISSÃO DE PRODUÇÃO — META EM CURTO (TUBO) · Episódio competitivo · Torneio em Portugal» (27/11/2026, 10:31), com a escolha do campeonato delegada ao agente. Voz: estimativa de 411 créditos pedida em cartão; autorizada pelo fundador a 27/11, 15:05 («Pode prosseguir»).

## Classificação
- Frente: Meta em Curto (TUBO). Router (`SHOWRUNNER.md` §2.2): torneio recente, deck e decisão de construção → competição.
- Classe: relatório de torneio / análise de deck (CONTEXTO §6.3 + §6.4). Estratégia: análise de dados + verificação de regras (Oracle, CR). Sem VOD: nada de «A Jogada que Não Viste».
- Complexidade: média.

## Originalidade
- Objeto: Official P9Q Side Quest at Mercadia Games 2.0 (Lisboa, 22/11/2026); Renato Faria; Thrasios + Tymna; Devoted Druid + Swift Reconfiguration.
- `python3 comum/ferramentas/memoria.py pauta --objeto "Official P9Q Side Quest cEDH Mercadia Games Lisboa; Thrasios + Tymna; Renato Faria" --tema "torneio cEDH em Portugal: porque o deck vencedor ganhou"` (27/11/2026): **BLOQUEADA** por MB-EP05 (palavras «cedh, ganhou, porque, torneio»).
- Comparação manual: MB-EP05 é Mana & Burn sobre o preço da Knacksaw Clique num combo de Kinnan; outra frente, outro objeto, outra tese. MB-EP09 (Dack Fayden) e MB-EP20 (Basalt Monolith + Rings, mana infinita) são Mana & Burn, outros combos e sem torneio. No Meta em Curto, nenhum episódio de cEDH. A tese «o mais jogado não ganhou» já existe (MC-PAU08, MC-EP08B): por isso não é a tese deste episódio.
- Decisão: liberada pelo fundador no cartão de decisão «Sim, avançar» (`nucleo/DECISOES.md` 27/11/2026 11:03).
- Relações: MC-PAU08 (mesma estrutura de campo, tese diferente); MB-EP20 (mana infinita: não publicar no mesmo dia).

## Pesquisa de pauta (§2.4)
Reação-alvo: «Então foi por isso que ganhou?»

### Escuta e radar
Radar `comum/radar/2026-W48.md` (< 7 dias) sem linhas de Portugal ou Europa; linhas 9–11 acrescentadas nesta sessão (Portugal e Europa, cEDH, 21–22/11). Brasil: sem linha nova (LigaMagic continua bloqueada à automação).

### Campeonatos candidatos (comparação obrigatória)
| Critério | A · Official P9Q Side Quest @ Mercadia (Lisboa, 22/11/2026) | B · The Power 9 Quest «Timetwister» (Lisboa, 21–22/11/2026) | C · commanderliga.de cEDH November (Dülmen, Alemanha) |
|---|---|---|---|
| Resultados verificáveis | 39 jogadores, 5 rodadas + mesas finais; classificação e V-D-E de todos (cEDH Stats ← TopDeck); campeão em 4 fontes | 104 inscritos, 6 rodadas + Top 16; campeão Ignasi Ibáñez Martí (Kraum + Tymna) | 17 jogadores; campeão Lumra |
| Listas | comandante dos 39; 16 listas públicas; lista do campeão completa (100) | 80 de 104 com comandante; 24 sem nada | 16 de 17 com comandante |
| VOD / partidas | nenhum | nenhum encontrado | nenhum |
| Potencial de análise | alto: campeão sem par no campo + lista com motor claro | alto, mas o campeão é o comandante mais jogado (história esperada) | baixo |
| Interesse cEDH | médio-alto | alto (circuito nacional, prémio Timetwister) | baixo |
| Originalidade | alta (1.º cEDH do TUBO) | alta | — |
| Visual | Thrasios + combo de 2 cartas | Kraum + Tymna | Lumra |
| Contacto com loja | Mercadia (logótipo a enviar pelo fundador) | cEDH PT (organizador) | — |
| Veredito | **escolhido** | reserva (dados incompletos; o «favorito ganhou» rende menos tese) | **descartado: é de 16/11/2025** |

Escolha: A, porque é o único com o campo inteiro conhecido (39 de 39 comandantes) e a lista do campeão completa no mesmo torneio, o que permite separar participação, listas, representação e resultado sem lacunas.

### Ângulos do mesmo evento (rubrica 1–5: gancho · originalidade · compreensão · visual · partilha · recompensa · adequação)
| Ângulo | Notas | Total | Decisão |
|---|---|---|---|
| 1 · «O mais jogado não ganhou» (Kraum + Tymna 8 de 39; 9 V em 43 jogos) | 4 · 1 · 5 · 3 · 3 · 3 · 4 | 23 | sai: repete MC-PAU08 e MC-EP08B |
| 2 · **O motor do deck campeão**: único Thrasios + Tymna; 13 combos, 12 com mana infinita ou quase; Thrasios transforma a mana em cartas | 4 · 5 · 4 · 4 · 4 · 4 · 5 | 30 | **vencedor**: ensina uma regra de construção que o espectador aplica ao próprio deck |
| 3 · «Numa mesa de 4, 25 % é a média: ele venceu 4 de 7» | 3 · 4 · 3 · 2 · 2 · 3 · 4 | 21 | sai: 7 jogos é amostra mínima; risco de conclusão universal |
| 4 · Sábado ganha o favorito (P9Q), domingo ganha o único Thrasios (Mercadia) | 4 · 4 · 3 · 3 · 3 · 3 · 4 | 24 | reserva: mistura dois eventos e o P9Q tem 24 jogadores sem comandante |

## Editorial
- Objetivo: trazer jogadores de Commander competitivo (BR e PT) para a série com uma análise que se aplica ao próprio deck.
- Proposta de valor: em 30 s, perceber porque um comandante «motor» faz de cada combo de mana uma linha de vitória.
- Tese: o único Thrasios + Tymna de 39 venceu com uma lista em que 12 dos 13 combos acabam em mana infinita ou quase, e o comandante é a saída que transforma essa mana em cartas.
- Limite declarado: sem VOD, não se diz como cada mesa terminou (no ecrã e na legenda).
- Variável em teste: nenhuma.

## Gancho visual (§4.1)
1. Quadro 0: Thrasios, Triton Hero grande e acesa com o selo «CAMPEÃO · THRASIOS + TYMNA», pergunta «O QUE O DECK CAMPEÃO TINHA?», selo de fonte TopDeck.
2. Objeto: a carta do comandante campeão.
3. Ação: entrada com escala e flash (0–0,25 s); «1 DE 39» aos 0,45 s; Kraum e Tymna escurecidas aos 0,9 s.
4. Som: «tum» + carimbo no quadro 0, pop no número, cliques nas cartas de apoio (biblioteca do TUBO).
5. Descoberta até 3 s: «1 de 39 · Thrasios + Tymna · 8 levaram Kraum + Tymna».
6. Promessa: mostrar o que esse deck tinha.
7. Pagamento: a lista e os combos (plano da lista a partir da frase 3; carimbo «13 COMBOS» na frase 4; combo e Thrasios nas frases 5–7).

Abertura de objeto: carta inteira no quadro 0, prova = «1 DE 39», saída no fim da frase 1 (a carta voa para o ecrã do TUBO e mergulha).

| Rubrica | Prevista | Medida |
|---|---|---|
| Relevância visual | 5 | 5 |
| Impacto inicial | 4 | 4 |
| Clareza | 4 | 4 |
| Curiosidade | 4 | 4 |
| Pagamento | 5 | 5 |
| Identidade | 5 | 5 |

## Roteiro definitivo (frases = legendas; voz com fonética)
1. No cEDH português, dados do TopDeck:
2. 39 jogadores na Mercadia Games.
3. O campeão foi o único Thrasios e Tymna.
4. Na lista dele, 13 combos.
5. 12 terminam em mana infinita, ou quase.
6. Devoted Druid com Swift Reconfiguration:
7. vira veículo e desvira sem morrer.
8. E o Thrasios troca mana infinita por cartas.
9. Seu comandante transforma mana em quê?
10. Probabilidade calculada. Humanos, imprevisíveis.

Texto enviado ao ElevenLabs (Antonio de Jesus, eleven_v4, 1 geração): «No cê é dê agá português, dados do Tóp Déqui: Trinta e nove jogadores na Mercádia Guêims. O campeão foi o único Trássios e Tímna. Na lista dele, treze combos. Doze terminam em mana infinita, ou quase. Dêvôutid Drúid com Suífit Riconfiguréixon: vira veículo e desvira sem morrer. E o Trássios troca mana infinita por cartas. Seu comandante transforma mana em quê? Probabilidade calculada. Humanos, imprevisíveis.» Gerado: 411 créditos, geração YkwAr3wZs9AcTA1I2Wjd (flow C9N8wFG5EUxZ2AMtdLlQ), 27,28 s em bruto; montada com `mc_voz.py` a atempo 1,0 (a 1,10 ficava abaixo dos 25 s): 26,60 s.

Referência a Portugal: só na frase 1 («No cEDH português») e no rótulo «cEDH · LISBOA». A identidade do criador fica na legenda.

### Revisão narrativa (§4.2)
Tese numa frase ✓ · originalidade com decisão ✓ · clareza aos 3 s (carta + «1 de 39») ✓ · progressão: campo → lista → combo → saída → pergunta ✓ · evidência: cada frase tem imagem real (barras, lista, cartas, Oracle) ✓ · ritmo: medir no final · recompensa na frase 4–8 ✓ · relevância: cEDH em Portugal, semana do P9Q ✓ · CTA: uma pergunta ✓.

## Plano (motor `oraculo/motor/mc_render.py`)
gancho_grade → tubo_abertura → barras (comandantes dos 39, carimbo «1 DE 39 · Renato Faria», canto com o logótipo da loja se chegar) → **decklist** (lista de 100 em 2 colunas a descer como papel, peças de combo a verde, carimbo «13 COMBOS») → **combo** Devoted Druid + Swift Reconfiguration (3 passos) → **combo** Thrasios (Oracle resumido) → previsao (TUBO, ecrã «MANA ∞ → CARTAS», nota «a lista não mostra como cada mesa acabou») → pergunta1 (A · CARTAS / B · DANO) → tubo_fecho (créditos de dados e local) → fecho do scanner.
Cenas novas no motor: `decklist` e `combo` (regressão: ESP03, PAU02 e PAU08 com quadros iguais, 27/11).

## Loja e terceiros
- Mercadia Games só como local do torneio: nome na voz (local do evento), rótulo e créditos. Logótipo: camada `terceiros.loja` (`terceiros/mercadia_logo.png`), círculo pequeno no canto do plano dos comandantes; sem «×», sem selo de parceria. Sem o ficheiro, o plano sai sem logótipo (re-render sem nova voz).
- Nenhuma colaboração afirmada. Convite de collab no Instagram só como convite do fundador.
- Campeão: sem foto (não há foto oficial enviada); a grelha usa as cartas. Nome e resultado públicos.

## Fontes e evidências
`fontes.md` (tabela completa, limitações e créditos). Dados: `dados/campo_39.tsv`, `dados/combos_spellbook.json`, `cartas/creditos.json`.

## Produção
- Recursos reutilizados: imagem-mestra do TUBO, trilha oficial, SFX do motor, fecho do scanner.
- Vozes e créditos: 411 créditos ElevenLabs (Antonio de Jesus, eleven_v4, 1 geração).
- Easter egg: nenhum.
- Ferramentas: Scryfall e Commander Spellbook pela shell; TopDeck, cEDH Stats, MTGTop8, cedhdiff e mtgcontent pelo agente de leitura web; navegador integrado indisponível nesta sessão.
- Prévia sem voz: 39,2 s (36 s estimados + fecho), sem marca «PRÉVIA» (decisão de 23/11); folha de contacto revista (20 quadros).

## Controlo de qualidade (ficheiro final, `qc_final.json`)
| Critério | Alvo | Medido | OK |
|---|---|---|---|
| Resolução / fps | 1080×1920 / 30 | 1080×1920 / 30 | ✓ |
| Duração | 25–35 s sem o fecho | 26,73 s (30,60 s com o fecho) | ✓ |
| Corte lateral | nenhum | cropdetect 1072×1920 (conteúdo de ponta a ponta) | ✓ |
| Loudness / pico | −14 LUFS / < −1 dBTP | −14,0 LUFS / −4,1 dBTP | ✓ |
| Fecho do scanner | presente | a partir de 26,73 s | ✓ |
| Factos = ficha | sim | `fontes.md` | ✓ |
| Quadro 0 | Thrasios + pergunta + selo | sim (folha de contacto) | ✓ |
| Descoberta | ≤ 3 s | «1 DE 39» aos 0,45 s | ✓ |
| Pagamento | lista e combos | carimbo «13 COMBOS» aos 9,96 s; combo 12,6–17,9 s; Thrasios 17,9 s | ✓ |
| Maior intervalo sem mudança visual | ≤ 3 s | fecho do TUBO 23,3–26,7 s com créditos a entrar e LED a pulsar (P2) | ✓ |
| Pronúncia | nomes em inglês por fonética | texto fonético na ficha; escuta final do fundador recomendada | — |
| P0 / P1 | 0 / 0 | 0 / 0 | ✓ |
Desvio registado: a lista de 100 cartas é mostrada inteira a descer durante 4,6 s (em Commander não cabe parada em 2 colunas a ≥ 28 px); a mesma lista vai em texto na resposta ao comentário fixado.

## Ficheiros finais (não versionados)
- Vídeo: `MC_EP09_FINAL.mp4` · 30,60 s · ficheiros do projeto claude.ai `tubo/mc-ep09/`
- Capa: `MC_EP09_CAPA.png` + `MC_EP09_CAPA_grelha.png` · mesma pasta
- Prévia sem voz e folhas de contacto: mesma pasta
- Regenerável com `oraculo/motor/mc_render.py` a partir de `dados/episodio.json` + voz da geração YkwAr3wZs9AcTA1I2Wjd montada com `mc_voz.py` (atempo 1,0). Logótipo da Mercadia: re-render sem nova voz quando chegar (`terceiros/mercadia_logo.png`).

## Pacote de publicação
- [x] `legenda.txt`
- [x] `comentario_fixado.txt` (+ `comentario_lista.txt`, resposta com as 100 cartas: o limite de 2.200 caracteres não deixa pôr tudo num só)
- [x] `texto_alternativo.txt`
- [x] `fontes.md`
- Publicação: `utm_campaign=MC-EP09`; não no mesmo dia do MB-EP20.

## v2 · revisão pedida pelo fundador (27/11/2026, 15:18)
Pedido: «as informações ficaram muito vagas… não diz qual é a loja… aonde… gancho visual inicial… som de efeitos melhor… feedback visual com som… nível profissional… até 45 segundos». Créditos: o fundador perguntou se era preciso gastá-los e pediu o MC-EP08B (campeão do mundo, maior audiência do TUBO) como referência (15:23) → **0 créditos**: a mesma voz (geração YkwAr3wZs9AcTA1I2Wjd) reordenada, campeão primeiro, como no MC-EP08B.

Diagnóstico da v1: loja só na voz e no rodapé, sem cidade, evento nem data; quadro 0 com a carta parada e texto pequeno; SFX sintetizados simples (bipes) e pouco ligados ao movimento; 3,4 s de TUBO parado no fim.

Mudanças:
- Voz: ordem 3 → 1 → 2 → 4…10 («O campeão foi o único Thrasios e Tymna.» abre; depois «No cEDH português, dados do TopDeck: 39 jogadores na Mercadia Games.»). `voz_montada_v2.wav` (não versionado: recria-se cortando `voz_montada.wav` pelos `voz_tempos` da v1).
- Quadro 0: **mosaico** com a arte real dos comandantes dos 39 jogadores (`cartas/arte/`, Scryfall; ordem da classificação com o campeão na posição 15); scanner apaga os quadros (contador 39 → 1); o Thrasios + Tymna salta para ecrã inteiro (1,55 s) e leva o carimbo «CAMPEÃO · 1 DE 39» (2,0 s) com abalo.
- **Ficha do evento** (2,8–8,5 s): mapa Natural Earth com Portugal a verde e alfinete em Lisboa; «LISBOA · PORTUGAL · Commander competitivo (cEDH) · 22·11·2026»; cartão «MERCADIA GAMES · EVENTO PARALELO OFICIAL · POWER 9 QUEST · 39 jogadores · 5 rodadas suíças + mesa final · R. Cláudio Nunes 17A, Lisboa · resultados no TopDeck». Logótipo entra no cartão quando chegar (re-render, 0 créditos).
- Barras e TUBO de abertura saem (o mosaico mostra o campo); lista, combo, Thrasios, previsão, pergunta e fecho mantêm-se.
- Som: deixas de efeitos nos dados (`sfx`, 46 deixas: impacto, scanner, tiques, riser, woosh, carimbo, alfinete, papel de impressora, cartas, brilho de mana, UI, fecho), sintetizadas no motor com cauda de reverberação; abalos de câmara nos impactos e transição rápida entre cenas.
- Motor: cenas `mosaico` e `evento`, deixas `sfx`, `abalos`, `transicoes` (só para episódios que as pedem; regressão ESP03/PAU02/PAU08 sem diferenças, 27/11).

QC v2 (`qc_final_v2.json`): 1080×1920, 30 fps, 31,77 s (27,9 s sem fecho), −14,0 LUFS, pico −3,8 dBTP, fecho presente, «sem problemas mensuráveis». Cropdetect: 1080×1920 em 763 de 808 quadros; 1074 nos quadros de abalo/transição (6 px de margem do abalo, não é corte). Folha de contacto conferida a olho.
Ficheiros: `MC_EP09_FINAL_v2.mp4`, `folha_contacto_v2.png` (projeto claude.ai, `tubo/mc-ep09/`). A capa da v1 mantém-se válida.
Pacote: legenda (evento e morada da loja; créditos do mosaico e do mapa), texto alternativo novo, `comentario_creditos.txt` (segundo comentário: artistas das 28 artes do mosaico).
Por fazer: foto do campeão (com autorização) pode entrar no quadro 0, como no MC-EP08B; logótipo da Mercadia.

## Handoff

```
HANDOFF · 27/11/2026, 15h35 (UTC) · Claude (v2)
Repositório: ibisson254/GERADOR-DE-VIDEO-BINDER · branch main (merge de tubo/mc-ep09) · v1: commit 3256997, merge 1d51eaa; v2: branch tubo/mc-ep09-v2, ver git log (conferido no remoto: ver resposta no fio)

Objetivo atual: MC-EP09 v2 pronto para o fundador publicar (MC_EP09_FINAL_v2.mp4); opcionais: logótipo da Mercadia e foto do campeão.

Conteúdos tocados (comum/REGISTRO_EDITORIAL.md):
- MC-EP09 · (novo) → CONCLUÍDO

Encerramento:
- MC-EP09 · memoria.py encerramento: OK · memoria.py validar: OK · validar_repo: 0 graves (P2 antigo: vince/kit/v1/)
- Vídeo, capa, grelha e folha de contacto finais: /mnt/project-files/tubo/mc-ep09/ (projeto claude.ai, Binder_original). Vídeo não versionado.

Decisões tomadas nesta sessão:
- Campeonato escolhido pelo agente (Mercadia, 39/39 comandantes conhecidos); pauta liberada pelo fundador no cartão (11:03) · nucleo/DECISOES.md 27/11 sim
- Voz autorizada pelo fundador («Pode prosseguir», 15:05; 411 créditos, uma geração) · na ficha
- v2 sem créditos (fundador 15:23: usar o MC-EP08B como referência); voz reordenada, campeão primeiro · na ficha, secção v2
- Tese: motor do deck campeão; descartados «o mais jogado não ganhou» (repete MC-PAU08) e taxa de vitória por mesa (amostra pequena) · na ficha
- Lista de 100 cartas em resposta ao comentário fixado (limite de 2.200 caracteres) · na ficha

Documentos consultados:
- AGENTS.md, STATUS.md, nucleo/SHOWRUNNER.md, oraculo/PERFIL e LEIA-ME do TUBO, nucleo/DECISOES.md (fim), comum/REGISTRO_EDITORIAL.md, comum/radar/2026-W48.md, fichas MC-PAU08 e MC-EP08B, nucleo/modelos/HANDOFF.md

Alterações realizadas:
- oraculo/episodios/ep09_mercadia_cedh/ · episódio completo (dados, cartas, ficha, pacote, qc_final.json)
- oraculo/motor/mc_render.py · cenas `decklist` e `combo` (regressão ESP03/PAU02/PAU08 idêntica)
- comum/REGISTRO_EDITORIAL.md, comum/historico.md, comum/radar/2026-W48.md, nucleo/DECISOES.md, STATUS.md, comum/status_arquivo.md

Insights (domingo): não se aplica (sexta-feira)

Tarefas pendentes:
- Escutar e publicar o MC-EP09 (utm_campaign=MC-EP09), em dia diferente do MB-EP20 · fundador
- Enviar o logótipo da Mercadia, se quiser no canto do gráfico de barras (terceiros/mercadia_logo.png; re-render sem voz) · fundador → agente
- P9 Quest Lisboa (104 jogadores) e contraste entre os dois eventos ficam de reserva para um MC futuro · agente

Próximo passo concreto: publicar o MC-EP09 com legenda.txt, comentario_fixado.txt e comentario_lista.txt desta pasta.
```

