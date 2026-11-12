# Dossiê · Meta em Curto EP05 · Star Trek: engenharia de um deck vencedor

Data: 05/11/2026. Tabelas completas (geradas dos dados, sem transcrição à mão): `oraculo/ep05/resultados/tabelas.md`. Código: `oraculo/ep05/analise/`. Fontes: `ep05_star_trek_fontes.txt`.

Reproduzir, a partir da raiz: `python3 -I oraculo/ep05/analise/X.py`, com X = probabilidades, pools, simulacoes, grafo, robustez, matriz, relatorio, auditoria.

Legenda de evidência: **facto** (fonte primária) · **cálculo** (fórmula e premissa documentadas) · **modelo** (simulação com premissas) · **crítica** (opinião publicada, pré-lançamento) · **previsão**.

## 1. Estado da evidência

- Star Trek não tem resultados. **Nenhum torneio de Sealed, nenhuma lista de troféu, nenhum win rate** existem em 05/11/2026: o pré-release começa a 06/11, o Arena a 10/11 e as lojas a 13/11. MTGMeta confirma "no recorded games". Nada aqui é desempenho de Star Trek.
- O primeiro torneio relevante é o **Worlds 32 (13–15/11), Booster Draft**. Não é Sealed.

## 2. Auditoria do roteiro

**A proposta anterior não foi localizada.** Procurei em todas as branches do repositório (`oraculo/`), nos docs do projeto, no Drive e no histórico de conversas. A única conta anterior é o piloto EP00 (`claude/oraculo/episodios/ep00_piloto_um_terreno.md`, nunca produzido). A auditoria incide sobre as premissas do briefing e sobre esse piloto.

| Ponto | Problema | Decisão |
|---|---|---|
| Números do episódio anterior | EP00 é de 60 cartas e 24 terrenos. As contas estão certas (43,4%, 18,4%, 12,1%), mas não servem para 40 cartas | Refeito tudo do zero |
| Território do TUBO | O perfil exclui temas sem torneio. O fundador pediu este episódio | Pedido explícito prevalece (constituição §1). Âncora: Worlds 32 e pré-release |
| "Federation" como plano | Não é um dos 10 arquétipos oficiais: 6 cartas, 2 comuns/incomuns | Tratado como mecanismo isolado |
| Listas vencedoras de Star Trek | Não existem | Sets anteriores só como método |
| Grafo por coocorrência de cartas em listas | Exige listas completas do mesmo set. Só há 2, de sets diferentes | Grafo real sobre o Oracle completo + camada rasa de 69 listas |
| "Maior bomba" sem número | Tese vaga | Quantificada: 1 jogo em 96 |
| Promo do pré-release | "Rara ou mítica", sem distribuição publicada | Fora das contas e dito no ecrã |
| Rascunho do roteiro: «noventa e um por cento» | 91,63% arredonda para 92 | Encontrado no QC; frase regravada |
| Rascunho do roteiro: 322 palavras | ~2 min | Cortado para 274; 93 s |

## 3. Investigação: o que é facto

- **Colação (facto):** 14 cartas por booster: 7 comuns (6 quando sai Stardates, 1 em 25), 3 incomuns, coringa, rara/mítica, foil, terreno. Pool de 84 cartas + promo. Principal: 91 C (10 são Planetas da vaga de terreno), 110 U, 80 R, 25 M.
- **Dez planos oficiais (facto, guia Wizards):** WU Spacecraft e artífices · UB Dilemma · BR Klingons e morte · RG Away Team Landfall · GW Médicos e marcadores · WB Borg · UR Cientistas e não-criaturas · BG Arqueologia e cemitério · RW Comando, poder total 8+ · GU Strange New Worlds.
- **Receita Wizards (facto):** 17 terrenos; 7–8 de custo 2; 5–6 de custo 3; 2–3 ameaças; pelo menos 5 remoções; artefato: "extra Perils of the Past".
- **Crítica pré-lançamento:** Draftsim espera formato lento. MTG Arena Zone sugere jogos mais rápidos para tappers e muitos tokens 1/1. As duas leituras não coincidem: velocidade do formato fica por decidir.
- **Draft × Sealed (facto, outro set):** Reality Fracture: Azorius 1.º nos dois; Gruul 3.º → 9.º; Simic 10.º → 4.º–6.º. Spearman 0,50 (n = 10, p = 0,14). Sealed com 2.226–5.660 jogos por par, IC95% de ±1,3 a ±2,1 pontos: boa parte da ordem do meio é ruído.
- **Spacecraft (cálculo, Oracle):** naves C/U de TRK custam 3,5 e ligam em 6,9 em média; EOE, 4,7 e 7,3. Draftsim diz que as de EOE foram "simply not good" e que nada mudou; a crítica não é evidência de jogo.

## 4. Listas vencedoras

**Tamanho real:** 69 listas de troféu de Sealed do Arena, 9 sets, **rasas** (cores, recorde, terrenos). Só **2 listas completas** com carta a carta. A meta de 20 listas comparáveis completas **não foi cumprida**. Curva, remoções, bombas, plano alternativo e dependência por lista não foram extraídos: inventá-los estava fora de questão.

- 58 de 2 cores, 11 de 3. 60 com 17 terrenos, 9 com 16, nenhuma com 18.
- 7–0: 9 · 7–1: 18 · 7–2: 42.
- Até 1 derrota: 26 de 58 com 2 cores (lift 1,15); **1 de 11 com 3 cores** (lift 0,23). Fisher p = 0,04.

**Vieses.** Só vencedores: mostra o que existe entre troféus, não o que causa troféus. Só as primeiras 7–8 linhas de cada página, de milhares (EOE: 8 de 3.014), ordem desconhecida. Arena Bo1, com mão suavizada. Um dos sets com só 650 partidas (SOS, Early Access). Sets com fixação diferente. Testes múltiplos: p = 0,04 sobrevive mal. **Sem grupo mediano**: nada separa o que distingue vencedores do que é comum a todos. Contraexemplo real: Allen Wu fez 9-0 em GP Cleveland 2019 com base de guildas em 4 cores.

## 5. Grafo

Imagem: `oraculo/ep05/resultados/grafo.png`. Nós: cartas C/U, mecanismos, funções. Ligações: peça, payoff, função; projeção mecanismo–mecanismo por cartas jogáveis (nota ≥ 2,0) partilhadas. Lista de nós por tipo pedida no briefing: **cores, curvas e condições de vitória não foram nós do grafo calculado** (cor e curva entram como atributos da carta).

- **Três famílias (modularidade):** VALOR (Borg, Dilemma, Cemitério) · CORPOS (Klingon, Poder 8, Beam me up) · MESA (Marcadores, Landfall, Spacecraft). Os nomes são meus. Densidade da projeção 0,72.
- **Isolados:** Federation e Strange New Worlds, 0 ligações. Não-criaturas fica fora: 108 cartas, ligaria tudo.
- **Ligação mais forte:** Dilemma–Cemitério, 10 cartas (Jaccard 0,25). Quem abre preto fica com UB e BG abertos.
- **Pontes (intermediação):** Poder 8 0,46; Marcadores 0,32; Borg 0,18.
- **Cartas-ponte:** L'Rell, Stray from History, Sarcophagus, Rogue Artificial Intelligence, Resistance Is Futile.
- **Estruturas resilientes (modelo):** Rakdos: payoffs baratos e qualquer corpo serve. Golgari: 4,3 payoffs por pool.
- **Excessivamente dependentes:** Dimir (motor 15%, 10% dos pools sem payoff); Orzhov/Borg: 2,5 payoffs para 8,6 peças; Simic paga o motor com a própria mana.
- **Limitações:** etiquetas minhas sobre Oracle; notas de um crítico; coocorrência é de texto, não de decks; correlação não é causa. Suporte, confiança e lift estão em `tabelas.md` para etiquetas do set e para as listas de troféu, não para cartas em decks.

## 6. Probabilidades

Tudo em `tabelas.md` (A–G): abertura, k = 1 a 8 cópias por turno e por lado, terrenos, custo 2, duas cores, custo duplo, splash, sinergias e mulligan à parte. Fórmulas em `analise/probabilidades.py`. Auditoria em `analise/auditoria.py`: 17 de 17 conferem.

| Pergunta | Quem começa | Quem compra |
|---|---|---|
| 1 carta única até T5 | 27,5% | 30,0% |
| 7 cartas da mesma função até T5 | 91,6% | 93,7% |
| Combo A+B, 1 cópia de cada, até T5 | 7,1% | 8,5% |
| 2 de 4 peças únicas até T5 | 30,0% | 34,6% |
| 1 payoff + 2 de 8 peças até T5 | 18,6% | 22,1% |
| 4 payoffs + 2 de 8 peças até T5 | 51,6% | 58,7% |
| Custo 2 no T2, 17 terrenos, 8 cartas | 80,4% | 86,4% |
| Custo 2 no T2, 17 terrenos, 3 cartas | 45,6% | 52,0% |
| Duas cores até T3, 9+8 | 82,7% | 87,3% |
| Duas cores até T3, 7+7+3 duais | 89,8% | 93,1% |

Abrir uma carta não é jogá-la: mítica específica 3,77% × ver até T5 27,5% = 1,04%, 1 jogo em 96, e isso supondo que entra no deck. Mulligan (London) quase não muda a chance de ver a carta: 26,7% contra 27,5%, porque se veem 7 cartas de novo; o custo é uma carta a menos. Planeta específico nos 6 boosters: 26,5%.

## 7. Dez planos

**Não é win rate.** Modelo de 40.000 pools + notas pré-lançamento de um crítico + etiquetas minhas. Ranking robusto a ruído nas notas, não a erro sistemático da crítica. Em Reality Fracture, Rakdos foi último no Sealed: o prior tem de ser largo.

| # | Plano | Disp. | Pot. | Cons. | Flex. | Total | Motor T5 | Remoção por pool | Confiança |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | Rakdos · Klingon/sacrifício | 4,8 | 4,8 | 3,9 | 3,8 | 4,32 | 64,6% | 5,75 | média-baixa |
| 2 | Golgari · Cemitério | 4,4 | 4,7 | 3,1 | 2,3 | 3,62 | 46,6% | 3,44 | baixa |
| 3 | Gruul · Landfall | 3,7 | 4,3 | 2,4 | 4,0 | 3,60 | 49,3% | 4,01 | baixa |
| 4 | Orzhov · Borg | 1,5 | 3,1 | 3,4 | 3,9 | 2,97 | 24,6% | 5,27 | baixa |
| 5 | Boros · Poder 8 | 1,2 | 2,8 | 2,6 | 4,9 | 2,88 | 24,2%* | 5,59 | baixa |
| 6 | Izzet · Não-criaturas | 3,4 | 2,6 | 2,3 | 3,0 | 2,82 | 35,6% | 4,58 | baixa |
| 7 | Selesnya · Marcadores | 1,4 | 3,2 | 3,3 | 2,3 | 2,56 | 39,2% | 3,28 | baixa |
| 8 | Dimir · Dilemma | 3,0 | 2,9 | 1,7 | 2,2 | 2,45 | 14,9% | 4,01 | baixa |
| 9 | Simic · Strange New Worlds | 3,4 | 2,6 | 2,0 | 1,7 | 2,40 | 25,1%* | 2,26 | baixa |
| 10 | Azorius · Spacecraft | 2,2 | 1,0 | 3,8 | 1,9 | 2,20 | 41,5% | 3,85 | baixa |

\* Teto: P(payoff até T5) × condição sem oponente. Melhor par por nota, com ruído de ±0,5: Rakdos 17,6% (banda 10,7–30,5), Golgari 13,9, Gruul 13,3, Orzhov 10,1, Selesnya 9,8, Izzet 8,1, Dimir 8,0, Boros 7,9, Simic 5,9, Azorius 5,4. Sorteio puro daria 10%: **só Rakdos sai da faixa**.

Requisito do motor: 1+ payoff e Borg 2+ criaturas artefato; Spacecraft 1+ nave e 2+ corpos; Klingon 2+ corpos; Izzet 2+ não-criaturas; Dilemma 2+ modais; Marcadores 1+ colocador; Cemitério 1+ surveil/mill; Landfall a própria queda de terreno.

Nota sobre o par "melhor deck × melhor carta": em 18% dos pools a carta de maior nota nem cabe no melhor par (modelo; empates contam a favor). Não é o número do gancho porque depende das notas.

### As dez perguntas, par a par

**WU Spacecraft.** Motor: nave estacionada por corpos. Densidade: 3+ naves e 14+ corpos; o pool dá 2,7 naves. Suporte: Hemmer, Rutherford, Brad Boimler, Zefram Cochrane. Sem sinergia: Constable Odo, Malfunctioning Holodeck, U.S.S. Excelsior, Marooned. Fracas fora: Warp Core, Class-F Shuttlecraft, Emergency Holographic Crew. Curva: 5+ corpos baratos, nave no T3–T4. Vulnerável: cada estacionamento é um ataque a menos (nave 6+ com poder 3 = 2 taps, 6 de dano não dados). Alternativa: voadores e tempo. Bomba: pior par, 43% de pools com nota ≥ 4. Evidência: guia + crítica; precedente fraco em EOE.

**UB Dilemma.** Motor: modais + "face a dilemma". Densidade: 6,7 peças, 2,2 payoffs. Suporte: Seven of Nine, Lorca, Tell Me What You See, Jett Reno. Sem sinergia: He's Dead Jim, Hoshi Sato, Marooned, Eject the Warp Core. Fracas fora: Obsidian Order Operative, Melkotian Adjudicator. Curva: reativa, topo 5–6. Vulnerável: 10% dos pools sem payoff. Alternativa: controlo com remoção preta. Bomba: média. Evidência: MTG Arena Zone avisa para não forçar cartas fracas por Seven of Nine.

**BR Klingons e sacrifício.** Motor: corpos baratos + saída de sacrifício. Densidade: 3–4 payoffs, 13+ corpos; o pool dá 5,0 payoffs. Suporte: L'Rell, Dahar Master, Automated Warfare System, In the Pale Moonlight. Sem sinergia: He's Dead Jim, Transporter Malfunction, The Duras Sisters, Plasma Cascade, Khaaaaaaaaaaaannn!. Fracas fora: Battle-Scarred Survivalist, A Good Day to Die, Targ Wrangler. Curva: baixa. Vulnerável: tokens 2/1 contra mesa de 1/1 e varredura; sacrificar sem pressão é desvantagem. Alternativa: remoção + valor. Bomba: 69%. Evidência: modelo + crítica. Contraponto: último em FRA Sealed.

**RG Landfall.** Motor: payoff + terreno. Densidade: 3,0 payoffs; terrenos fazem o resto. Suporte: Syndicate Liquidators, Dal R'El, Cleveland Booker, Burnham. Sem sinergia: Transporter Malfunction, Plasma Cascade, Support Mission, Horta. Fracas fora: Planetary Patrol, Exploratory Mission, Jake Sisko. Curva: payoff no T3, terreno depois. Vulnerável: payoff tardio perde quedas de terreno. Alternativa: corpos grandes + queimadura. Bomba: 71%. Evidência: guia + modelo.

**GW Marcadores.** Motor: colocar marcador e cobrar. Densidade: 7,8 peças, 2,5 payoffs. Suporte: Phlox, Support Mission, The Doctor, Federation Field Medic. Sem sinergia: Malfunctioning Holodeck, Excelsior, Sylvia Tilly, Syndicate Liquidators. Fracas fora: Dr. McCoy Surly Surgeon, Dominion Supervisor. Curva: 2-drops que recebem marcador. Vulnerável: 3,3 remoções. Alternativa: corpos e voadores. Bomba: 66%. Evidência: crítica ("excellent support").

**WB Borg.** Motor: criaturas artefato + senhores. Densidade: 8,6 peças, 2,5 payoffs. Suporte: Locutus, Hive Mind Coprocessor, Organic Avulsion Unit, Command Subadjunct. Sem sinergia: He's Dead Jim, Holodeck, Excelsior, D'Ghor Bloodletter. Fracas fora: Conquest Mission, Collective Drone, Assault Drone. Curva: a mais barata (7,2 corpos ≤ 2). Vulnerável: Wizards recomenda remoção de artefato; Perils of the Past é comum. Alternativa: 5,3 remoções. Bomba: 59%. Evidência: crítica entusiasmada; Sealed limita a densidade que o Draft permitiria.

**UR Não-criaturas.** Motor: mágicas baratas + gatilhos; naves contam. Densidade: 15,4 peças, 2,5 payoffs. Suporte: Academy Instructor, Gray and Adira, Tal Shiar Analyst. Sem sinergia: Transporter Malfunction, Spock, Hoshi Sato, Marooned, Plasma Cascade. Fracas fora: Cetacean Ops, Anthropological Mission. Curva: mágicas ≤ 3. Vulnerável: só 14 corpos. Alternativa: remoção + voadores. Bomba: 55%. Evidência: guia + crítica.

**BG Cemitério.** Motor: surveil, recursão e "deixa o cemitério". Densidade: 5,3 peças, 4,3 payoffs. Suporte: Vash, Sylvia Tilly, Stray from History, Hologram Stalker, Daniels. Sem sinergia: He's Dead Jim, Eject, Syndicate Liquidators, Support Mission. Fracas fora: Test of Loyalty, Relentless Drednok, Storied Veteran. Curva: corpos de valor. Vulnerável: 3,4 remoções; exílio de cemitério em comum (Dominion Assault Force). Alternativa: 2-por-1. Bomba: 72%, a mais alta. Evidência: modelo + crítica ("respectable").

**RW Poder 8.** Motor: 8 de poder em mesa. Densidade: goldfish 59,6% no T5, 77,2% no T6, sem oponente. Suporte: Kirk Commanding Officer, Cantankerous Captain, Hologram Janeway, La'An. Sem sinergia: Transporter Malfunction, Holodeck, Excelsior, Plasma Cascade. Fracas fora: Tactical Officer, Una Chin-Riley, Worf. Curva: agressiva. Vulnerável: troca de criaturas desliga o limiar. Alternativa: 5,6 remoções. Bomba: 58%. Evidência: guia; crítica morna nos payoffs.

**GU Strange New Worlds.** Motor: nomes diferentes de terreno. Densidade: 5,3 não básicos por pool, qualquer cor; 4 nomes extra dão 3+ até T6 em 71%. Custo: duas cores até T3 cai de 82,7% para 76,8%; com 3 básicos fora de cor, 69,2%. No Sealed os básicos são livres. Suporte: The Traveler, Species 8472, Suus Mahna. Sem sinergia: Hoshi Sato, Marooned, Support Mission, D'Vana Tendi. Fracas fora: Cloak and Phaser, Pavel Chekov, Warp Speed. Curva: rampa. Vulnerável: a menor remoção (2,3) e mana pior. Alternativa: corpos grandes. Bomba: 59%. Evidência: crítica ("irresponsible mana bases").

### Mecânicas pedidas

- **Borg/artefato:** 35 peças, 14 payoffs no set. **Scientists:** 108 não-criaturas, 8 payoffs. **Klingons:** 15 peças, 17 payoffs de morte/sacrifício. **Spacecraft:** 17 naves, 8 C/U. **Federation:** 6 cartas; 1,94 tipos por criatura, 5,3 tipos com 3 criaturas: X alto com pouca carta, mas 2 cartas C/U. **Dilemma:** 39 modais, 9 payoffs. **Landfall:** 9 payoffs, todos C/U. **Marcadores:** 36 peças, 9 payoffs. **Recursão:** 13 cartas com retorno do cemitério, 11 delas no mecanismo de cemitério (lift 6,4). **Interação com artefatos:** só 5 de 27 remoções C/U acertam nave parada (70,000 Light-Years from Home, Malfunctioning Holodeck, Guidance Failure, Marooned, Rules of Acquisition); 9 cartas C/U no total lidam com artefato. Resistance Is Futile não acerta criatura artefato.

## 8. Hipóteses e previsões

Auditar em `comum/historico.md`, com dados de Sealed do 17Lands.

| Hipótese | Tipo | Confiança | Prazo |
|---|---|---|---|
| Rakdos no top 3 de win rate do Sealed de TRK | previsão pública do TUBO | baixa (~35%) | 01/12/2026 |
| Azorius na metade de baixo do Sealed | previsão de registo | baixa | 01/12/2026 |
| Decks de 3+ cores abaixo dos de 2 cores no Sealed | hipótese | média-baixa | 01/12/2026 |
| O ranking de Draft de TRK não prevê bem o de Sealed (Spearman < 0,7) | hipótese | média-baixa | 01/12/2026 |

## 9. Bloqueios

1. **17Lands:** sem acesso, logo sem listas completas, sem grupo mediano e sem win rate por curva, criaturas ou remoção em Sealed. Desbloqueia: o fundador acrescentar `17lands-public.s3.amazonaws.com` e `www.17lands.com` em Capabilities, ou ligar o computador.
2. **Áudio não ouvido.** Tenho medições, não audição. A transcrição Scribe repete a grafia fonética do prompt, por isso não prova a pronúncia. Conferir: "Síld", "pêiof", "Uízards", "Strêinj Niú Uôrlds", "Rácdos" e o corte em ~36–40 s (frase regravada).
3. **Distribuição da promo:** a Wizards não publica.

## 10. Auditorias (ficheiro final)

| Pergunta | Resposta |
|---|---|
| Cada percentagem tem fonte ou fórmula? | Sim: ficha, tabela de evidências |
| Denominadores identificados? | Sim, no ecrã: 6 boosters, 40 cartas, 69 listas, 11 e 58, 40.000 pools |
| Sealed ou Draft? | Identificado em cada dado; Reality Fracture mostra os dois |
| Listas de alto desempenho? | Sim, troféus (7 vitórias), Arena; não são amostra aleatória |
| Inferência separada de facto? | Sim: «padrão, não causa», «modelo, não jogo», «leitura do TUBO» |
| Previsão apresentada como certeza? | Não: «previsão registrada», «certeza baixa» |
| Resultados de Star Trek inexistentes? | Nenhum citado; o vídeo diz que são zero |
| Matemática recalculada? | Sim, por caminho independente: 17 de 17 |
| Casos extremos? | K = 0, K = N, n = N, 11/40 |
| Teoria × simulação? | Diferenças ≤ 0,06 pontos nos números do vídeo; a tolerância é de 0,15 |
| Arredondamentos? | Um erro achado e corrigido (91 → 92) |
| Gráfico = dados? | O render lê os JSON e falha se as famílias ou os 96 divergirem |
