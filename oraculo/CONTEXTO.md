# META EM CURTO (TUBO, ex-Oráculo de Tubo) — CONTEXTO (v6, 29/10/2026)

Fonte de verdade da série. Ler inteiro antes de qualquer produção.

Série BINDER Originals do @binderthetrade. Análise competitiva de Magic: metagame, matchups, mulligan, sideboard, sequenciamento e decisões de torneio. Reels 9:16 (1080×1920, 30 fps), 35–45 s, PT-BR.

Território distinto: Mana & Burn = cultura/caos · Conde de Manaforte = estética · Meta em Curto = competição e decisão.

---

## 1. Personagem: TUBO (T.U.B.O.)

- **Nome:** TUBO. Sigla irónica: **Terminal Unificado de Balanço e Otimização**.
- Nasce do título da série; duas sílabas, fácil de falar e de citar nos comentários ("O Tubo ia surtar vendo o meu deck").
- **Corpo:** monitor CRT bege dos anos 90 sobre pescoço mecânico curto (placa com rebites, cabo solto), em cima de uma CPU bege com 2 botões e frisos. Sem braços, pernas, boné ou boca.
- **Personalidade:** analítico, confiante, ligeiramente arrogante, curioso, humor seco. Acredita que tudo pode ser calculado e irrita-se com a imprevisibilidade humana. Nunca inventa dados; quando os dados não chegam, admite-o de forma pouco graciosa.
- **Crença:** «Tudo pode ser calculado.»
- **Frase de fecho (todo episódio):** «Probabilidade calculada. Humanos, imprevisíveis.»
- **Assinatura rara:** «Analisa o presente. Prevê o futuro. Mas é só um CRT.»

## 2. Visual definitivo

Imagem-mestra: `assets/tubo_mestra_916.png` (1080×1920). Feita por edição da ilustração original — **não se regenera o personagem**.

- Fundo #0F172A; corpo bege levemente dessaturado; contraluz verde #10B981 na silhueta.
- Ecrã #050A10 com chuva de código fósforo (#00FF41) e scanlines; código escurecido atrás dos olhos.
- Olhos quadrados #10B981 com pupila escura.
- Placa frontal: "BINDER" pequeno + LED verde ao lado.

## 3. Fala

A voz é o LED ao lado de BINDER: o brilho segue a amplitude do áudio (ElevenLabs), com halo ~40 px na placa.
- Silêncio: verde muito escuro.
- Erro de sistema: LED vermelho, 2–3 piscadelas secas.
- Voz: ElevenLabs "Antonio de Jesus" (voice_id `MK5tXPmT83J5SUlpUo4K`), modelo eleven_v4, acelerada com atempo 1,10 (escolhida e usada no EP01).

## 4. Expressões (camadas na montagem, sem gerar imagens novas)

O monitor é recortado e rodado no pivô do pescoço.
- **Analítico** (principal): pupilas ao centro, pálpebra reta a meio, código lento.
- **Confiante:** pálpebra diagonal num olho, push-in da câmara, código rápido.
- **Desconfiado:** um olho semicerrado, pupilas de lado, monitor inclinado ~15°, código congela.
- **Erro de sistema:** olhos duplicados (separação verde/vermelho), glitch, tremor, LED vermelho.

---

## 5. Ambientação: FORA DO TUBO / DENTRO DO TUBO

Regra central da série.

- **Fora do tubo:** TUBO inteiro, como na imagem-mestra. Personalidade, gancho, opinião, revelação e pergunta. Expressões e LED visíveis.
- **Dentro do tubo:** a câmara mergulha no ecrã CRT (push-in até o vidro preencher o quadro) e a análise acontece em tela cheia 9:16 num terminal verde fósforo com scanlines. **Aqui só entram dados verificados.**
- Dentro do tubo, o LED vira HUD: `● BINDER` no rodapé, pulsando com a voz.
- O terminal é desenhado nativamente em 9:16 → nunca há corte lateral.
- Código visual que o público aprende: entrou no tubo = dado com fonte.

## 6. Tipos de episódio (conforme o material)

### 6.1 Leitura de Carta
Para carta nova, spoiler ou candidata a ban.
- Imagem oficial puxada automaticamente do Scryfall (`manaburn/` já tem a lógica).
- A carta entra no ecrã como "scan" linha a linha.
- TUBO analisa custo, formatos onde entra e o que ameaça.

### 6.2 A Jogada que Não Viste
Para uma partida de torneio.
- **Não usar imagens da transmissão** (direitos).
- Reconstruir o estado da mesa com imagens das cartas (Scryfall) num tabuleiro esquemático: vida, mão conhecida, campo, mana disponível.
- Link do VOD com o minuto exato vai no comentário fixado (é a prova).

### 6.3 Relatório do Meta
Para dados de metagame (MTGGoldfish, MTGTop8, Melee).
- Percentagens em barras de terminal.
- Fonte e data sempre visíveis no ecrã.

### 6.4 Evidência visual (regra de todos os tipos, desde o EP02)
Tudo o que o TUBO cita aparece no ecrã.
- **Deck citado** → «impressão» da lista principal completa no terminal: agrupada por tipo, quantidade + nome, 2 colunas, letra com ≥ 28 px de corpo, parada ≥ 2,5 s, cartas-chave a verde #10B981 e o resto em fósforo esmaecido. A mesma lista vai em texto no comentário fixado e no carrossel derivado, sempre com a linha de fonte.
- **Carta citada** → imagem oficial do Scryfall (impressão usada no torneio quando se sabe), entrada «scan» linha a linha, ≥ 60 % da largura quando é o assunto, arte nunca alterada nem recortada. Crédito no ecrã: carta · coleção nº · artista + «Cartas © Wizards of the Coast · imagens via Scryfall». Só entram cartas efetivamente citadas.
- **Jogador citado** → «FICHA DE JOGADOR» no terminal: nome, deck, seed, campanha, títulos verificados; avatar = silhueta pixelizada em fósforo, nunca um rosto.
  - Não se descarregam nem usam fotos de jogadores (cobertura SCG/WotC, redes sociais, pesquisa de imagens): têm direitos de terceiros e direito de imagem da pessoa.
  - Foto real só se o Ibisson a fornecer com autorização registada em `oraculo/autorizacoes/`.
  - O @ oficial do jogador vai no comentário fixado só se confirmado num perfil verificável; senão, omite-se.
- Imagens de transmissão continuam proibidas (6.2).

## 7. Estrutura do Reel (~40 s)

| Tempo | Bloco | Onde | Expressão |
|---|---|---|---|
| 0–3 s | Gancho: frase seca | Fora | Desconfiado |
| 3–8 s | Cabeçalho `ARQUIVO: torneio · formato · data` | Entra no tubo | — |
| 8–28 s | Análise (carta / mesa / gráfico) | Dentro | HUD `● BINDER` |
| 28–35 s | Revelação | Sai do tubo | Confiante ou Erro de sistema |
| 35–40 s | Pergunta competitiva + frase de fecho | Fora | Analítico |
| fim | `comum/outro/outro_binder_916.mp4` | — | — |

- Easter egg (máx. 1) escondido na chuva de código; registar em `comum/easter_eggs.md`.

## 7.1 Trilha: jazz de precisão

Tema oficial: `musica/tubo_tema.mp3` (40,6 s). Composição própria do Ibisson ("Paper Thin Alibi"); original completo em `musica/tubo_tema_original.mp3` (62 s).
- Conceito: big band tensa à la Whiplash — o TUBO é o maestro implacável; qualquer desvio é erro humano. Tom menor (Fá menor).
- Edição (`editar_tema.py`): dois cortes nas batidas mais parecidas (12,6→26,7 s e 49,1→54,3 s do original), EQ a puxar bombo e caixa (+3,5 dB 70 Hz, +2,5 dB 3,5 kHz, −2 dB 800 Hz), −16 LUFS.
- Mapa no vídeo:
  - 0–6 s: abertura quase em silêncio com batidas soltas → gancho.
  - ~12,6 s: banda entra cheia → mergulho no tubo / análise.
  - **29,0–30,2 s: corte seco (silêncio) → revelação.** Assinatura sonora da série: o silêncio anuncia a jogada.
  - 30,2 s: banda volta → pergunta e frase de fecho; termina em 40,6 s e passa ao outro.
- Montagem: baixar a trilha ~12 dB enquanto o TUBO fala (ducking) e subir nas pausas. Alinhar o corte seco à revelação: o silêncio segue a revelação, não um segundo fixo (no EP01 ficou entre 23,0 e 24,9 s).

## 7.2 Identidade extra (aprovada 27/10/2026)

**Personagem**
1. **Som de arranque:** "tum" de desmagnetização de CRT ao ligar + chiado curto de modem no mergulho para dentro do tubo. A série reconhece-se em 1 s pelo som.
2. **Contador de erros humanos:** número no canto do terminal (`ERROS HUMANOS: 007`) que sobe a cada episódio com jogada imprevisível. Contagem real de episódios, nunca inventada.
3. **Limite do humor:** a arrogância visa decisões e probabilidades, nunca jogadores reais pelo nome em tom de deboche.

**Episódios**
4. **Previsões registadas:** antes de um torneio grande, o TUBO faz uma previsão marcada como opinião. Depois do evento, volta a ela e mostra acerto ou erro (erro = "Erro de sistema"). Registar cada previsão em `comum/historico.md`.
5. **"O TUBO julga o teu deck":** seguidores deixam a lista nos comentários; uma é analisada por semana. Pedir autorização ao autor e citar o @.
6. **Crossovers:** TUBO vs Conde ("carta feia, mas presença real no meta", com número verificado) ou o TUBO a aparecer na TV do sofá de Mana & Burn. Um universo BINDER partilhado.

**Produção e conversão**
7. **Legendas em estilo terminal:** fonte mono verde, palavra a palavra (a maioria vê sem som).
8. **Ponte honesta para o app:** o "scan" da carta a entrar no tubo ecoa o scanner real do outro. Nunca mostrar ou inventar outras funcionalidades.
9. **Carrossel derivado:** cada "Relatório do Meta" também sai como carrossel com os mesmos dados e fontes.

## 8. Pilares

1. A Jogada que Não Viste.
2. Manual de Sobrevivência ao Meta.
3. O Meta Não Mente.
4. Erro de Sistema.

## 9. Rigor

- Confirmar torneio, formato, data, jogadores, decks e estado da partida.
- Distinguir facto de interpretação.
- Nunca inventar win rates, partidas, jogadas ou citações.
- Nada de conclusões universais a partir de uma única partida.

## 10. Entrega

- Legenda limpa terminando com "baixe o BINDER Vision".
- Comentário fixado: pergunta fácil + complemento (fonte/VOD/detalhe técnico) + "Tem um detalhe escondido. Diga o segundo."
- Conferir enquadramento 9:16 sem corte lateral antes de entregar.
- Commit: roteiro, legenda e histórico. Nunca vídeos renderizados.

## 11. Elementos fixados no EP01 (29/10/2026)

Usados no EP01 e mantidos como identidade da série:
- **Medidor "GRAU DE CERTEZA"** (5 segmentos) fora do tubo, sempre que a amostra é pequena ou a conclusão é incerta. É a forma visual de separar dado de opinião.
- **Pergunta com 3 opções em chips** (ex.: matchup · chaveamento · pilotagem), respondida com uma letra no comentário fixado.
- **Cartão de assinatura** antes do fecho: "META EM CURTO · com TUBO · BINDER Originals".
- **Rodapé do terminal:** `● BINDER` à esquerda e `META EM CURTO · EPnn` à direita; linha de fontes por cima.
- **Fecho:** quadros reais de `comum/outro/scan/` + logótipo, entrada com transição de 0,4 s.

Ficha completa e controlo de qualidade: `episodios/ep01_ac13_ficha.md`.

## 11.1 Estreado no EP02 (29/10/2026)

- **Erro de sistema**: olhos duplicados (separação verde/vermelho), fatias deslocadas no ecrã, tremor, LED vermelho a piscar e caixa «MODELO TUBO» com o erro a vermelho. Usado quando o modelo do TUBO falha (ex.: «vencedor provável = mesa maior → Ott»).
- **Fichas de jogador** e **impressão da lista** (6.4).
- **Leitura da Final** (Modo B): quando não há VOD analisável, explica a final só com o relato do organizador + texto Oracle, sem reconstruir jogadas. Fica entre o 6.2 e o 6.3.
- Linha de fontes com corpo 34 (≥ 24 px de altura de letra), acima das legendas; mix a −14,0 LUFS.

Ficha: `episodios/ep02_hartford_ficha.md`.

## 12. Pendente

1. Primeiro episódio «A Jogada que Não Viste» com jogada real verificada no VOD. EP01 e EP02 caíram por VODs de 8–11 h sem legendas. Pedir à cobertura (ou ao Ibisson) o minuto da final, ou escolher eventos com VOD da final em vídeo próprio.
2. Contador `ERROS HUMANOS` ainda não estreado.
3. Fecho `comum/outro/outro_binder_916.mp4` continua fora do repositório (fecho reconstruído com os quadros do scanner).
4. Melee.gg inacessível nas sessões de produção: resultados jogo a jogo e listas só pela SCG/magic.gg.
