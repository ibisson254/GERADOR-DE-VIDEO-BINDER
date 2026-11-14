# Expedição BINDER · bíblia do formato

Versão 1 · 14/11/2026 (criado com o episódio #01, pedido do fundador). Formato de lançamento do BINDER Originals: **um episódio por set novo, no «primeiro olhar»**, até 72 h depois da revelação oficial.

## 1. O que é
Reel 9:16 de 60–75 s (sem o fecho) que apresenta as primeiras cartas reveladas de um set **como espécies de um documentário de natureza**, numa descida pelas camadas oficiais do mundo do set. Pergunta aberta no início, paga no fim; espécies numeradas; pedido de comentário com resposta de um número.

- Público: jogadores de Magic do Brasil (sobretudo Commander) que ainda não leram nada sobre o set.
- Proposta de valor: em ~70 s a pessoa conhece o plano, as cartas, os decks de Commander e a data, e lembra-se delas porque foram apresentadas como bichos.
- **Não é Mana & Burn.** Nenhum personagem do BINDER aparece (sem Burn, Mana, sofá, TV SAL, Conde, TUBO, Vince). Sem vozes nem música das séries.

## 2. Voz
- ElevenLabs **«Rafael Valente – Brazilian Professional Narrator»**, `voice_id dX7gRq1dIvLTgUaWpEFn`, modelo `eleven_v4`. Escolhida a 14/11/2026 entre duas prévias (a outra: «Bia – Versátil & Expressiva», `0ozreaQ0xnggCu2x9oFC`): é a mais rápida e curiosa das duas, com registo jovem de documentário. Não é voz de nenhuma série.
- Direção no prompt: `[curious, warm, amazed nature-documentary narrator, fast pace]`, `[short pause]` entre frases, `[long pause]` entre camadas. **Uma geração** (1 tomada).
- Pós: cortes por palavra + pausas + `rubberband` (tempo ~1,2) em `template/audio.py`. A voz sai lenta (~2,2 palavras/s): escrever ~170 palavras para caber em 75 s sem acelerar tanto.
- Pronúncia: nomes de cartas e decks em inglês. O nome do set escreve-se com acento no prompt quando ajuda (EX-01: «Náuctis»).

## 3. Música
Tema próprio do formato: `kit/tema_expedicao.mp3` (ElevenLabs Music v2.5, 14/11/2026, instrumental, 78 s, flow `0XnRy5fnCKLW7pWERfzQ`), três fases que escurecem (rasos → grande → abismo) e sobem na revelação final. −22 LUFS sob a voz com ducking; sobe +4 dB no acender da carta-pagamento e no fecho. Licença: gerada no workspace ElevenLabs do estúdio (a confirmar pelo fundador que o plano ativo inclui uso comercial, como nas outras séries). Reutilizar o mesmo tema em todos os episódios; gerar outro só se o set tiver mais ou menos camadas.

## 4. Os oito movimentos de edição (só estes)
Todos implementados em `template/render.py` e configurados por `episode.json`.
1. **Plano de carta**: carta a 80% da largura, sombra suave, flutuação ±6 px em 3 s.
2. **Troca de variante**: corte seco da versão normal para a alternativa (uma por espécie).
3. **Punch-in em texto**: zoom até 1,6 em 7 quadros na linha que a narração diz (retângulo medido no PNG de 745×1040). Máximo dois por carta.
4. **Slide-in de comparação**: carta a 62%, inclinada 10°, entra do canto inferior esquerdo, sai pelo mesmo canto.
5. **Pop-in de caixa**: 0,85 → 1,05 → 1,0, inclinada 6°; punch-in brutal (×2,3) no subtítulo, letras cortadas.
6. **B-roll de piada visual**: 1–1,5 s de vídeo real com licença confirmada (Pexels/Pixabay), máximo dois. Sem licença confirmada → sem B-roll. Nunca imagem gerada que pareça foto.
7. **Respiração**: 0,5–1 s de fundo vazio com o nome da camada e um anel de sonar.
8. **Fila de caixas**: as caixas lado a lado na abertura e no fecho.

Ritmo: troca ou punch-in a cada 2–4 s; nada estático > 4 s; cortes secos; nada de transições de software.

## 5. Assinatura visual e sonora
- Fundo subaquático que escurece por camada (a cor do fundo é o mapa da descida); partículas; raios de luz nas camadas de cima; partículas bioluminescentes no fundo.
- **Medidor de descida** à esquerda com os nomes das camadas, **sem números de profundidade**.
- **Ficha de espécie** no terço inferior: «Nº n · NOME · tipo · camada», sai antes do primeiro punch-in.
- Legenda palavra a palavra (Inter Display Black), palavras-chave a amarelo.
- Logótipo do BINDER no canto superior direito, 62 px (≤ 6%), 60% de opacidade. Esmeralda #10B981 como cor de destaque.
- Abertura: gancho escrito desde o quadro 0; silhueta da carta-pagamento quase invisível. Pagamento: a mesma carta acende **no mesmo enquadramento**.
- Som: ping de sonar (camadas e revelação), bolhas (caixas), whoosh de água (slide-ins). **Nada mais.**
- Termina com `comum/outro/outro_binder_916.mp4` (corte seco; a música acaba dentro dele).

## 6. Regras de facto e de direitos
- Texto Oracle de cada carta lido no Scryfall (ou no artigo da Wizards) antes da voz; nunca regra de memória.
- **Nenhuma frase sugere que uma carta é comandante ou vem num deck** enquanto os comandantes não forem revelados. Os decks entram pelo nome (o que o nome diz é observação; o tema só com a caixa oficial).
- Cores dos decks só pelo que se vê nas caixas oficiais. Sem preços. Camadas com o nome oficial em PT-BR se a Wizards o tiver; senão tradução nossa, marcada na ficha.
- Palavras-chave com a tradução oficial PT-BR (Ameaça, Toque Mortífero, Atropelar…).
- Imagens: cartas do Scryfall; caixas e arte-chave **só imagens oficiais da Wizards**. Sem caixa oficial, o render usa um cartão «PRÉVIA · NÃO PUBLICAR» e o episódio não sai.
- Política de conteúdo de fãs: crédito por carta no rodapé («carta · set · Arte: artista · © Wizards of the Coast»); logótipo do Magic só onde já está nas imagens oficiais.
- Proibido: material de Reels de referência (imagens, música, grafismos, piadas); pessoas reais; imagem gerada que pareça foto.

## 7. O que muda a cada set
`episode.json` (blocos, camadas e cores, gancho, pergunta, data), `audio/words.json` (Scribe da voz nova), `cards/creditos.json`, `products/` (caixas oficiais e retângulos dos subtítulos), roteiro e pacote de publicação. O motor (`template/`) não muda; se mudar, regista-se aqui.

## 8. Pacote de publicação
Vídeo + capa A (silhueta + gancho) e B (caixas + «SET: N ESPÉCIES») · legenda (gancho; data; lista numerada; decks; créditos; CTA em rotação a terminar em «baixe o BINDER Vision»; ≤ 5 hashtags; sem emojis) · comentário fixado (pergunta 1–N + texto de cada carta em PT-BR, tradução nossa assinalada) · texto alternativo · ficha de factos.

Métrica principal: comentários com número por 1.000 views · secundária: visitas ao perfil por 1.000 views.
