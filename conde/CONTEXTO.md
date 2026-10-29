# Conde de Manaforte — contexto completo da série

Série de Reels do Instagram do BINDER Vision (@binderthetrade).
Atualizado em 26/10/2026. Ler este ficheiro antes de produzir qualquer episódio novo.

---

## 1. O que é

O Conde de Manaforte é um crítico de arte fictício. Julga as ilustrações de cartas de Magic: The Gathering com a solenidade de um aristocrata decadente que se acha a autoridade máxima sobre a arte ocidental.

- **Princípio criativo:** ele leva a arte a sério, leva a própria opinião demasiado a sério e não consegue levar o mundo à sua volta a sério.
- **De onde vem o humor:** a análise artística é verdadeira; a arrogância é que é teatral.
- **Onde vive:** é uma série dentro do @binderthetrade, ao lado do Mana & Burn. Não tem conta própria.
- **Nome da série no ecrã:** O Tribunal Estético ("pareceres do Conde de Manaforte · processo nº 00X").
- **Função no funil:** Pilar C (cultura TCG). Atrai público pela arte e pelo humor; a legenda leva ao BINDER Vision.

---

## 2. Personalidade e regras de comportamento

- É realmente culto: conhece composição, luz, perspectiva, simbolismo, mitologia e técnica. Quando elogia, explica o motivo.
- Tem preconceitos estéticos fictícios: detesta enquadramentos preguiçosos, poses sem propósito e anatomias que "afrontam a geometria".
- É vaidoso, não cruel. O alvo do humor é a arrogância dele, nunca o artista nem o público.
- Fraqueza secreta: é apaixonado por ilustração fantástica. Diante de uma obra extraordinária, perde por instantes a pose de indiferença.

Regras:
1. Nunca começa gritando. A autoridade vem da calma.
2. Nunca diz só "bonita" ou "feia": dá sempre uma razão.
3. Nunca humilha um artista por uma escolha visual.
4. Nunca aceita uma discordância sem transformá-la num debate formal.
5. Quando erra, inventa uma desculpa elegante, mas de vez em quando admite que o público tem razão.

**Decisão do Ibisson (26/10/2026):** sem memes nem referências de cultura pop brasileira na fala. Foi testado e rejeitado. O Conde fica como no Ep. 001.

---

## 3. Fórmula do roteiro

Observação artística verdadeira → interpretação excessivamente séria → conclusão absurda, dita com a mesma calma.

Estrutura fixa de cada episódio:
1. **Abertura:** "Meus caros apreciadores do duvidoso. O Tribunal recebe hoje um réu / uma dama de [ano]."
2. **Nome da carta.**
3. **Análise séria da composição** (o que realmente funciona na arte).
4. **A insolência:** o detalhe que desmonta a arte.
5. **Fato real** (texto da carta ou bastidor com fonte).
6. **A ferroada:** liga o texto da carta ao defeito da arte.
7. **Veredito:** "Parecer: obra notável…" + remate.
8. **Fecho:** "Qual réu o Tribunal julga a seguir?"

Vocabulário de apoio (caixa de ferramentas, não bordões obrigatórios):
- Elogio: "Há aqui uma compreensão da luz que beira o indecente."
- Crítica: "Uma composição ousada. O resultado, infelizmente, também."
- Despedida: "Retirem-se em silêncio. A arte precisa se recuperar."

Regras de conteúdo:
- Fatos sobre a carta e o artista só com fonte verificada (Scryfall para texto e dados; artigos ou fóruns para bastidores).
- Bastidor com fonte única fica atribuído na fala e no ecrã ("segundo o Draftsim").
- Cartas que as pessoas reconhecem e ainda jogam viralizam mais do que cartas obscuras.

---

## 4. Voz

- **Voz no ElevenLabs:** "Conde de Manaforte" — voz desenhada (Voice Design), prévia 2 de 3.
- **voice_id:** `bbnQVGWT7UMdmoK4URLr`
- **Descrição usada no Voice Design:** "Voz masculina adulta, timbre médio-grave, dicção nítida, ritmo controlado e ironia subtil. Crítico de arte aristocrático e vaidoso, calmo e solene, autoridade que vem da calma, nunca grita. Pronúncia brasileira natural, sem sotaque estrangeiro exagerado."
- **Modelo de narração:** `eleven_v4`, generations_count 1.
- **Tags de direção:** `[calm, dry, aristocratic]` no início; `[pause]` entre blocos; `[slow]` antes da preparação da piada; `[deadpan]` na ferroada.
- **Pós-produção da voz** (`encurtar_narracao.py`): pausas comuns 0,24 s; pausa cómica antes da ferroada 0,55–0,6 s; pausas entre blocos finais 0,40–0,45 s; voz acelerada 8% (atempo 1.08). A narração bruta sai com ~52–55 s e fica com ~42–45 s.

---

## 5. Música

- **Tema:** "Verdict in Varnish and Vellum" (ElevenLabs Music, gerado pelo Ibisson a 25/10/2026), 30 s, ~136 BPM. Ficheiro: `musica/tema.mp3`.
- **Briefing:** piano de câmara do fim do século XVIII com sátira gótica vitoriana; piano solo, violoncelo contido, pizzicato e cravo discreto. Sem voz, sem percussão épica.
- **Edição:** tema emendado no compasso (16 batidas de recuo no Ep. 001, 20 no Ep. 002, crossfade 0,25 s); ducking por sidechain (threshold 0.025, ratio 5); no fecho a música sobe e o sting cai no carimbo "Parecer emitido".
- **Volume final:** -14 LUFS, pico abaixo de -1 dBFS.

---

## 6. Identidade visual

**Retrato oficial:** gravura monocromática com medalhão oval, perfil, monóculo com corrente, gola alta e lenço. Quatro expressões. Recortes em `assets/`: `medalhao.png`, `neutro.png`, `desconfiado.png`, `indignado.png`, `admirado.png`.

**Paleta:** preto de tinta `#111111` (contornos e texto) · marfim de papel `#F4F0E6` (fundo) · cinza de gravura `#77736C` (créditos) · bordô de selo `#762F32` (carimbos e palavras-chave).

**Tipografia:** Lora.

**Layout do Reel (1080×1920, 30 fps):** cabeçalho "O TRIBUNAL ESTÉTICO"; palco com a arte em largura total, inteira, nunca cortada nas laterais; crédito sob o palco com "Conteúdo de fã não oficial, sem aprovação ou endosso da Wizards."; legenda palavra a palavra em y≈1372; @binderthetrade em y≈1530.

**Elementos recorrentes:** elipses e setas de tinta, rótulos marfim em itálico, lupa crítica, carimbos bordô ("RÉU · ano", "OBRA NOTÁVEL", "PARECER EMITIDO"), inserto oval do Conde trocando de expressão.

---

## 7. Pipeline de produção

1. Escolher a carta: conhecida ou jogada hoje, com defeito visível e, de preferência, bastidor com fonte.
2. Pesquisar: Scryfall (dados e imagens); Draftsim, Star City Games e MTG Salvation para bastidores.
3. Escrever o roteiro na fórmula (secção 3).
4. Gerar a voz no ElevenLabs e transcrever com `eleven_scribe_v1` para os tempos de cada palavra.
5. `encurtar_narracao.py` → `narracao.wav` e `words_novo.json`.
6. Mapear a arte (coordenadas no `art_crop`) para elipses, setas e lupa.
7. Copiar `montar_ep002.py`, trocar caminhos, KEY, coordenadas, cenas, carimbos e emenda da música. `--preview t1,t2` e depois render (~2 min).
8. Conferir: carta e arte inteiras, legenda na zona segura, -14 LUFS.
9. Entregar: vídeo, capa, legenda, comentário fixado e ficha de fatos.

---

## 8. Legenda e comentário fixado

**Legenda:** gancho; contexto que manda para o comentário; crédito ("Na tela: carta (coleção, ano), nº n. Arte: artista. © Wizards of the Coast. Conteúdo de fã não oficial."); ponte para o BINDER Vision ligada à carta; "→ Baixe a beta para Android. Link na bio."; até 5 hashtags com #TribunalEstetico; sem emojis.

**Comentário fixado:** pergunta fácil na 1ª linha; "O processo nº 00X" com 3 pontos (carta, defeito, bastidor com fonte); fecho "Pausou o vídeo? Repare em…".

---

## 9. Episódios produzidos

- **Ep. 001 · Keldon Warlord** (Alpha, 1993, nº 160, Kev Brockschmidt) — 44,2 s. A perninha abaixo da espada; "obra notável… da cintura para cima".
- **Ep. 002 · Olivia Voldaren** (Innistrad, 2011, nº 215, Eric Deschamps) — 47,5 s. O "joelho órfão"; bastidor do arquivo errado segundo o Draftsim; "salvem sempre duas vezes".
- **Ep. 003 · Voldaren Pariah // Abolisher of Bloodlines** (Secret Lair Drop, 2026, nº 1441, Véronique Meignaud) — 47,3 s. Carta de dupla face com flip; o rosto "inacabado" do verso é a transformação; "está no meio da refeição"; "acusação retirada". Especial Halloween (31/10).

## 10. Próximos réus (candidatos)

Hyalopterous Lemure; Joven (Homelands, 1995, Douglas Shuler, só análise visual); Celestial Prism, Reverse Polarity, Gabriel Angelfire, Mongrel Pack, Sorrow's Path, Urza's Mine, Chains of Mephistopheles. **Não usar:** Stasis (já foi Mana & Burn), Moor Fiend, Olivia Voldaren (Ep. 002) e Voldaren Pariah (Ep. 003).

## 11. Métricas

Sem vidIQ. O Ibisson envia um print semanal do Instagram Insights (Visão geral + Conteúdo) e os números vão para `comum/historico.md`.

## 12. Direitos

Política de Conteúdo de Fãs da Wizards (identificar como não oficial, creditar artista e Wizards). Voz e música do ElevenLabs: publicar só com licença comercial do plano. Nada de imitar vozes reais.

## 13. Fontes

- https://scryfall.com/card/lea/160
- https://scryfall.com/card/isd/215/olivia-voldaren
- https://draftsim.com/worst-mtg-art/
- https://articles.starcitygames.com/articles/vorthos-is-magic-top-10-oddest-art/
- https://company.wizards.com/fancontentpolicy
