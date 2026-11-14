# Expedição BINDER · bíblia do formato

Versão 3 · 14/11/2026 (v1 02:24; v2 15:33 «Prisma Abissal», `01-nauctis/brief_v2.md`; v3 16:19 «Operação Abyssal», estrutura de retenção e finais A/B). Formato de lançamento do BINDER Originals: **um episódio por set novo, no «primeiro olhar»**, até 72 h depois da revelação oficial.

## 1. O que é
Reel 9:16 de 60–75 s (sem o fecho) que apresenta as primeiras cartas reveladas de um set **como espécies de um documentário de natureza**, numa descida pelas camadas oficiais do mundo do set. Pergunta aberta no início, paga no fim; espécies numeradas; pedido de comentário com resposta de um número.

- Público: jogadores de Magic do Brasil (sobretudo Commander) que ainda não leram nada sobre o set.
- Proposta de valor: em ~70 s a pessoa conhece o plano, as cartas, os decks de Commander e a data, e lembra-se delas porque foram apresentadas como bichos.
- **Não é Mana & Burn.** Nenhum personagem do BINDER aparece (sem Burn, Mana, sofá, TV SAL, Conde, TUBO, Vince). Sem vozes nem música das séries.

## 1b. Estrutura de retenção (v3)
1. **Gancho (0–2,5 s):** a promessa escrita no quadro 0 sobre a silhueta da carta-pagamento (mesmo enquadramento da revelação), um clarão curto que a deixa entrever, a câmara a descer. Etiqueta da série pequena; nada de título institucional.
2. **Descobertas numeradas (1/6 … n/6)**, cada uma com uma entrada própria (aproximação à arte, varredura de scanner, panorâmica, giro, faixa de luz) e depois o **modo habilidade**: a carta sobe e uma chamada curta em PT-BR diz a habilidade (fichas verdes = vantagem, vermelhas = condição, brancas = informação). Nunca depender do texto inglês impresso.
3. **Camadas** com fundo que muda de luz e contraste; no Abismo, um indício da carta-pagamento lá em baixo.
4. **Revelação no drop** (herói maior, brilho, swell), depois habilidade, comparação verificada e escassez só se confirmada.
5. **Data** («5 FEV 2027») e **decks** em placas gráficas neutras (nunca imitar embalagem; caixa oficial só com imagem oficial).
6. **Final A (engajamento):** grelha 3×2 numerada com nomes, ≥ 4 s, pergunta «QUAL ESPÉCIE VOCÊ LEVA? / COMENTE DE 1 A N»; assinatura curta do BINDER Vision. **Final B (instalação):** sem a pergunta; scanner real em destaque e botão «BAIXE O BINDER VISION». Nunca duas chamadas com o mesmo peso.
7. **Fecho do BINDER Vision:** gravação real do scanner (`comum/outro/scan`) + cartão final de alto contraste (logótipo grande; «Escaneie suas cartas e organize seus decks.» / «Disponível no Google Play.» / «Link na bio.»). Substitui o `outro_binder_916.mp4` neste formato (decisão de 14/11/2026).

## 2. Voz
- ElevenLabs **«Rafael Valente – Brazilian Professional Narrator»**, `voice_id dX7gRq1dIvLTgUaWpEFn`, modelo `eleven_v4`. Escolhida a 14/11/2026 entre duas prévias (a outra: «Bia – Versátil & Expressiva», `0ozreaQ0xnggCu2x9oFC`): é a mais rápida e curiosa das duas, com registo jovem de documentário. Não é voz de nenhuma série.
- Direção no prompt: `[curious, warm, amazed nature-documentary narrator, fast pace]`, `[short pause]` entre frases, `[long pause]` entre camadas. **Uma geração** (1 tomada).
- Pós: cortes por palavra + pausas + `rubberband` (tempo ~1,2) em `template/audio.py`. A voz sai lenta (~2,2 palavras/s): escrever ~170 palavras para caber em 75 s sem acelerar tanto.
- Pronúncia: nomes de cartas e decks em inglês. O nome do set escreve-se com acento no prompt quando ajuda (EX-01: «Náuctis»).

## 3. Música
- **EX-01: «Auction of Power»** (`kit/auction_of_power.mp3`, 45 s, 140 BPM, batida 0,42865 s), escolhida e fornecida pelo fundador a 14/11/2026. **Licença a registar antes de publicar.**
- A música manda no ritmo: `audio.py` rearranja-a sozinho em batidas inteiras (repete os compassos antes do drop até o **drop** cair na palavra da revelação, `drop_w`, e repete compassos depois do drop até a **cauda natural da faixa acabar com o vídeo**); a pausa `ajuste_pausa_w` absorve a diferença. A grelha de batidas do vídeo é a da música.
- −26 LUFS sob a voz com ducking −7 dB: durante a fala a voz fica **≥ 15 dB acima da música** (integrado), para a tradução automática do Instagram separar a fala. Sobe +1 dB no drop e +8 dB depois da voz; acaba com a cauda natural da faixa.
- Tema próprio da v1 (`kit/tema_expedicao.mp3`, ElevenLabs Music) fica como reserva quando o fundador não escolher faixa.

## 4. Os oito movimentos de edição (só estes)
Todos implementados em `template/render.py` e configurados por `episode.json`.
1. **Plano de carta**: carta a 80% da largura, sombra suave, flutuação ±6 px em 3 s.
2. **Troca de variante**: corte seco da versão normal para a alternativa (uma por espécie).
3. **Punch-in em texto**: zoom até 1,6 em 7 quadros na linha que a narração diz (retângulo medido no PNG de 745×1040). Máximo dois por carta.
4. **Slide-in de comparação**: carta a 62%, inclinada 10°, entra do canto inferior esquerdo, sai pelo mesmo canto.
5. **Pop-in de caixa**: 0,85 → 1,05 → 1,0, inclinada 6°; punch-in brutal (×2,3) no subtítulo, letras cortadas.
6. **B-roll de piada visual**: 1–1,5 s de vídeo real com licença confirmada (Pexels/Pixabay), máximo dois. Sem licença confirmada → sem B-roll. Nunca imagem gerada que pareça foto.
7. **Respiração**: 0,5–1 s de fundo vazio com o nome da camada, o índice e a linha de sinal vermelha, num tempo forte.
8. **Fila de caixas**: as caixas lado a lado na abertura e no fecho.

Ritmo: troca ou punch-in a cada 2–4 s; nada estático > 4 s; cortes secos; nada de transições de software. **Todos os cortes, trocas, punch-ins e slide-ins caem numa batida** (janela −0,25/+0,15 s em torno da palavra-chave); as camadas entram num tempo forte do compasso; a revelação final cai no drop.

## 5. Assinatura visual e sonora («Prisma Abissal», v2)
Conceito: a descida é luz a decompor-se. Quanto mais fundo, menos luz e mais pura a cor que resta. Referências do designer lidas em `01-nauctis/brief_v2.md` (características, nunca as imagens).
- **Fundo gerado em código** (`template/fundo.py`): Rasos = aguarela pastel difusa com grão; Grande Marinho = tinta arrastada na vertical, azul-violeta, núcleo rosa-pêssego, massa escura a escorrer; Abismo = quase negro com uma coluna espectral (lima → amarelo → laranja → magenta → violeta) e reflexo arrastado; revelação = fenda prismática numa pedra em blocos, que abre no drop e fica até ao fim.
- O fundo respira com a energia da música e pulsa em cada batida (mais forte no tempo forte); 2–3 quadros de deslocamento de faixas («glitch») em cada corte; transição entre camadas por arrasto de cima para baixo.
- **Linha de sinal vermelha** (#FF2A2A): o acento gráfico do formato. Entra em cada camada e, no Abismo, pisca nos tempos fortes. Só no fundo, nunca sobre cartas ou texto.
- Camada: nome em Inter Display Black com tracking largo e índice «01 / 03» a vermelho.
- **Medidor de descida** à esquerda, **sem números de profundidade**; **ficha de espécie** «Nº n · NOME · tipo · camada» (esmeralda do BINDER no número); legenda palavra a palavra com palavras-chave a amarelo; logótipo do BINDER no canto superior direito, 62 px, 60%.
- Abertura: gancho escrito desde o quadro 0; silhueta da carta-pagamento quase invisível. Pagamento: a mesma carta acende **no mesmo enquadramento**, no drop.
- **Sonoplastia desenhada, três sons e só três** (`kit/sfx/`, ElevenLabs SFX v2, 14/11/2026): *descida* (queda de pressão sub-grave) nas três camadas; *glitch* (rajada digital de 0,3 s) nos punch-ins brutais das caixas e nas três condições da carta-pagamento; *swell* prismático invertido que acaba no drop. Proibido: ping de sonar, bolhas, whoosh de água e qualquer som «de biblioteca» por defeito. Um som que não melhore o plano sai.
- Termina com o scanner real e o cartão final (§1b.7); a música acaba com a cauda natural, sem trecho mudo.

## 6. Regras de facto e de direitos
- Texto Oracle de cada carta lido no Scryfall (ou no artigo da Wizards) antes da voz; nunca regra de memória.
- **Nenhuma frase sugere que uma carta é comandante ou vem num deck** enquanto os comandantes não forem revelados. Os decks entram pelo nome (o que o nome diz é observação; o tema só com a caixa oficial).
- Cores dos decks só pelo que se vê nas caixas oficiais. Sem preços. Camadas com o nome oficial em PT-BR se a Wizards o tiver; senão tradução nossa, marcada na ficha.
- Palavras-chave com a tradução oficial PT-BR (Ameaça, Toque Mortífero, Atropelar…).
- Imagens: cartas do Scryfall; caixas e arte-chave **só imagens oficiais da Wizards**. Sem caixa oficial, o render usa um cartão «PRÉVIA · NÃO PUBLICAR» e o episódio não sai.
- Política de conteúdo de fãs: crédito por carta no rodapé («carta · set · Arte: artista · © Wizards of the Coast»); logótipo do Magic só onde já está nas imagens oficiais.
- Proibido: material de Reels de referência (imagens, música, grafismos, piadas); pessoas reais; imagem gerada que pareça foto.

## 7. O que muda a cada set
`episode.json` (blocos, camadas, gancho, pergunta, data, música e arranjo), `audio/words.json` (Scribe da voz nova), `cards/creditos.json`, `products/` (caixas oficiais e retângulos dos subtítulos), roteiro e pacote de publicação. O motor (`template/`) não muda; se mudar, regista-se aqui.

## 8. Pacote de publicação
Vídeo + capa A (silhueta + gancho) e B (caixas + «SET: N ESPÉCIES») · legenda (gancho; data; lista numerada; decks; créditos; CTA em rotação a terminar em «baixe o BINDER Vision»; ≤ 5 hashtags; sem emojis) · comentário fixado (pergunta 1–N + texto de cada carta em PT-BR, tradução nossa assinalada) · texto alternativo · ficha de factos.

Métrica principal: comentários com número por 1.000 views · secundária: visitas ao perfil por 1.000 views.
