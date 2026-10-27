# ORÁCULO DE TUBO — CONTEXTO (v4, 27/10/2026)

Fonte de verdade da série. Ler inteiro antes de qualquer produção.

Série BINDER Originals do @binderthetrade. Análise competitiva de Magic: metagame, matchups, mulligan, sideboard, sequenciamento e decisões de torneio. Reels 9:16 (1080×1920, 30 fps), 35–45 s, PT-BR.

Território distinto: Mana & Burn = cultura/caos · Conde de Manaforte = estética · Oráculo de Tubo = competição e decisão.

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
- Voz: masculina, médio-grave, articulada, leve nasalidade (a escolher no ElevenLabs).

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
- Montagem: baixar a trilha ~12 dB enquanto o TUBO fala (ducking) e subir nas pausas. Alinhar a revelação ao corte dos 29 s.

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

## 11. Pendente

1. Camadas animadas: olhos (4 expressões), chuva de código, LED, recorte do monitor no pivô.
2. Escolher a voz no ElevenLabs.
3. Teste de 5 s com LED sincronizado à primeira narração.
4. Terminal "dentro do tubo" (template HTML 9:16) e transição de mergulho.
5. Piloto: "A Jogada que Não Viste", com jogada real verificada.
