# Catálogo editorial · Estúdio BINDER (@binderthetrade)

Documento canónico das frentes editoriais: o que existe, como se classifica, onde está a identidade de cada uma e em que estado está. Configuração técnica (pastas, vozes, trilhas, episódio de referência): `../series.yaml`. Regras comuns: `CONSTITUICAO_EDITORIAL_BINDER_ORIGINALS.md`.

Atualizado a 31/10/2026, com as decisões do fundador nessa data (`DECISOES.md`). **Lacuna** = informação que não está documentada em nenhuma fonte e não deve ser preenchida por suposição.

## Estado de publicação confirmado pelo fundador (31/10/2026)

Tudo o que está no repositório foi testado, aprovado e lançado. O especial de Halloween 2026 e a sequência de Star Trek (Órbita) estão publicados. Vozes e músicas foram criadas pelo fundador e estão aprovadas. Não são tarefas pendentes nem se reabrem.

## Tipos de produção

| Tipo | O que é | Frentes |
|---|---|---|
| Episódio de série | Peça recorrente com personagem, fórmula e identidade fixas | Mana & Burn, Conde de Manaforte, Meta em Curto |
| Especial ou homenagem | Peça pontual ligada a um acontecimento, data ou pessoa; pode cruzar séries | Especiais |
| Publicação temática | Peças de um universo temático com estilo visual próprio | Órbita |
| Publicação espontânea | Peças de oportunidade, experimentais ou avulsas | Lambe-lambe |

## Séries permanentes

### Mana & Burn

| Campo | Valor |
|---|---|
| Classificação | Série permanente · episódio de série |
| Estado | Ativa |
| Objetivo editorial | Rir da mesa e perceber a carta do momento (jogador casual e de Commander no Brasil) |
| Identidade | Burn e Mana no sofá, sala gasta dos anos 90, TV de tubo com a TV SAL, bate-volta de 14 falas, rock cru, bordões "Lê a carta." / "Isso devia ser banido." / "Comenta aí." |
| Documentação | Bíblia: doc "BINDER Marketing — Série Mana & Burn" no Drive + skill `binder-mana-burn-episodio` · Perfil: `manaburn/PERFIL.md` · Técnica: `manaburn/LEIA-ME.md` |
| Regras específicas | Putômetro = Salt Score do EDHREC ÷ 4 com fonte no ecrã; "Lê a carta" sempre conferido no Oracle; manchetes da TV SAL sem pessoas reais |
| Território | Cultura e caos de Magic: cartas polémicas, Salt Score, hype e spoilers, preço noticiado, sazonais, reação da comunidade, notícias da Wizards |
| Conteúdo produzido | Reel 9:16, duração livre (constituição §6); formato derivado Giro de domingo; carrossel e Stories derivados (`formatos.py` do motor v2) |
| Relação com o BINDER Vision | Fecho do scanner; no "Comenta aí" o Mana pode segurar o celular com a marca (`fx.celular`) |

### Conde de Manaforte · O Tribunal Estético

| Campo | Valor |
|---|---|
| Classificação | Série permanente · episódio de série |
| Estado | Ativa |
| Objetivo editorial | Humor erudito sobre ilustrações de cartas que o colecionador conhece |
| Identidade | Crítico de arte aristocrático e vaidoso; abertura "Meus caros apreciadores do duvidoso…", veredito com carimbo; piano de câmara com sátira gótica |
| Documentação | Bíblia: `conde/CONTEXTO.md` · Perfil: `conde/PERFIL.md` |
| Regras específicas | Observação, interpretação e facto sempre separados; o alvo do humor é a arrogância do Conde, nunca o artista; sem memes |
| Território | Ilustração: composição, luz, anatomia, perspectiva, simbolismo, técnica, bastidores, artistas |
| Conteúdo produzido | Reel 9:16, duração livre (constituição §6) |
| Relação com o BINDER Vision | Fecho do scanner; verde BINDER só no fecho |

### Meta em Curto (personagem TUBO)

| Campo | Valor |
|---|---|
| Classificação | Série permanente · episódio de série |
| Estado | Ativa |
| Nome | **Meta em Curto** é o nome público (confirmado pelo fundador a 31/10/2026). "Oráculo de Tubo" é o nome antigo; a pasta `oraculo/` mantém-se porque os scripts dependem dela |
| Objetivo editorial | Explicar em ~40 s porque um deck ou uma jogada funcionou (jogador competitivo e de Commander) |
| Identidade | Monitor CRT dos anos 90 com estética de código verde; voz = LED a acender; "fora do tubo / dentro do tubo"; jazz de precisão com o tema "Paper Thin Alibi" |
| Documentação | Bíblia: `oraculo/CONTEXTO.md` · Perfil: `oraculo/PERFIL.md` |
| Regras específicas | Só campeonatos recentes e falados, mais previsões de pré-release pelo protocolo (`oraculo/PROTOCOLO_PRE_RELEASE.md`, 06/11/2026); evidência visual (lista completa, carta oficial, ficha de jogador com silhueta; foto só com autorização); comparar a jogada com 1–2 alternativas |
| Território | Competição: decks, metagame, matchups, mulligan, sideboard, decisões de jogo |
| Conteúdo produzido | Reel 9:16; carrossel com a lista |
| Relação com o BINDER Vision | Fecho do scanner |

## Universo temático

### Órbita · Star Trek

| Campo | Valor |
|---|---|
| Classificação | Universo temático · publicação temática |
| Estado | Ativa |
| Objetivo editorial | Peças sobre as cartas de Magic: The Gathering \| Star Trek, com o que a comunidade diz de cada carta |
| Identidade | Cartaz creme com quadro pintado em abstração geométrica (Kandinsky/Bauhaus, gerado por código), carta inteira e parada no centro, planetas e anéis em órbita, loop perfeito |
| Documentação | Bíblia: `orbita/CONTEXTO.md` · Gerador: `orbita/gerador/` (ver `LEIA-ME.md`) |
| Regras específicas | Não cita preços; carta e texto parados; sem contador acima da carta; CTA da legenda em rotação sem repetir em posts seguidos; **sem fecho do scanner nem propaganda do BINDER no fim do vídeo** (fundador, 31/10/2026) |
| Formatos | Reel 4:5 (1080×1350), 12 s, 30 fps; formatos Quadro, Constelação, Pergunta e Scanner (os dois últimos sem produção registada) |
| Relação com o BINDER Vision | Selo "BINDER Vision" na composição e CTA de download na legenda; o vídeo não termina com o fecho do scanner |

## Formato espontâneo

### Lambe-lambe

| Campo | Valor |
|---|---|
| Classificação | Formato espontâneo · publicação espontânea |
| Estado | Ativo, permanente |
| Objetivo editorial | Publicações de oportunidade e experimentais: curiosidades, artistas, demonstrações do app |
| Identidade | Muro de lambe-lambe pop (rosa), papel rasgado e fita só nos cantos de cima; cartaz pop = cultura TCG, cartaz preto BINDER = produto; adesivos "Curiosidade de Magic" (amarelo) e "Artistas de Magic" (azul) |
| Documentação | Bíblia: `lambe-lambe/CONTEXTO.md` · skill `binder-posts-instagram` |
| Regras específicas | Carta limpa, sem filtros nem cortes, rodapé visível; produto só com gravação real do app; legenda v3 (gancho, curiosidade, fontes, ponte para uma função real, CTA de download, até 5 hashtags) |
| Formatos | Post 4:5 (1080×1350); Reels 9:16 (scanner, "Pause e descubra", "Na prática") |
| Relação com o BINDER Vision | Direta: pilar de demonstração do produto e ponte para funções reais |

## Produções pontuais

### Especiais e homenagens

| Campo | Valor |
|---|---|
| Classificação | Produção pontual · especial ou homenagem |
| Estado | Ativo (sempre disponível) |
| Regras | Constituição §14: duração pela força da história, tom de celebração e legado, humor subtil quando couber, rigor intacto. Exceções a regras de entrega só com pedido do fundador para esse especial, registadas em `DECISOES.md` |
| Onde ficam | Especial de uma série: `<pasta da série>/episodios/espNN_<nome>/` · crossover: `especiais/<nome>/` |
| Já produzidos | Homenagem a Sir Patrick Stewart (v1 `esp01_sir_patrick/`, não publicável; v2 `esp02_picard_v2/`) · Especial de Halloween 2026 Innistrad × Duskmourn (`especiais/halloween_2026/`, publicado) |
| Relação com o BINDER Vision | Fecho do scanner, salvo exceção registada (ex.: homenagem a Sir Patrick) |

## Vince Vault · Multiverse Capital (o mercado das cartas)

| Campo | Valor |
|---|---|
| Classificação | Série permanente · episódio de série |
| Estado | Frente aprovada pelo fundador (12/11/2026, 05:54: «Vince vault»); em desenvolvimento — direção 2D ativa (decisão de 11–12/11: o 3D foi descartado por custo); kit de recortes por fechar; sem calendário |
| Objetivo editorial | Explicar por que razão o preço de uma carta mudou, com causa única, fonte e data; dizer o que isso significa para quem tem a carta |
| Identidade | Vince Vault, corretor da Multiverse Capital, "Buy the dip!" (sempre cortado ou desmentido em cena); traço 2D em camadas, planos parados cortados a cada 3–6 s; a Fonte (telefone) nunca aparece, nunca diz palavras, nunca é legendada; voz ElevenLabs antiga (`L93SDe6kGQj79D6svMgA`) |
| Documentação | Bíblia: `vince/CONTEXTO.md` · Perfil: `vince/PERFIL.md` · Som da Fonte: `vince/audio/fonte.py` · Arquivo 3D (não ativo): `vince/BIBLIA_PERSONAGEM.md`, `vince/FICHA_VISUAL.md`, `vince/MODELO_3D.md`, `vince/V03_PLANO.md`, `vince/referencias/` |
| Regras específicas | Nunca prever preço nem recomendar compra ou venda; todo o número com fonte e data no ecrã e nota «estimativa, não oferta de compra»; sem Cardmarket e sem preços do Scryfall (decisão de 08/11; constituição §4); sem fonte verificada, a Fonte não atende |
| Território | Preço e o que o move. Humor sobre cartas → Mana & Burn; notícia da semana → Giro; resultado competitivo → Meta em Curto |
| Conteúdo produzido | Nenhum ainda (formato previsto: Reel 9:16, 30–45 s); piloto antigo 3D arquivado em `vince/episodios/` |
| Relação com o BINDER Vision | Direta: o fecho do scanner é continuação do conteúdo, não interrupção |

## Frente nova

Criar a pasta, `PERFIL.md` (modelo em `modelos/PERFIL_SERIE.md`) e a bíblia (`CONTEXTO.md`), acrescentar uma secção aqui e uma entrada em `../series.yaml`, e registar em `DECISOES.md`. A constituição não muda.
