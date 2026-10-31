# Catálogo editorial · Estúdio BINDER (@binderthetrade)

Documento canónico das frentes editoriais: o que existe, como se classifica, onde está a identidade de cada uma e em que estado está. Configuração técnica (pastas, vozes, trilhas, episódio de referência): `../series.yaml`. Regras comuns: `CONSTITUICAO_EDITORIAL_BINDER_ORIGINALS.md`.

Atualizado a 31/10/2026, com as decisões do fundador nessa data (`DECISOES.md`). **Lacuna** = informação que não está documentada em nenhuma fonte e não deve ser preenchida por suposição.

## Estado de publicação confirmado pelo fundador (31/10/2026)

Tudo o que está no repositório foi testado, aprovado e lançado. O especial de Halloween 2026 e a sequência de Star Trek (Órbita) estão publicados. Vozes e músicas foram criadas pelo fundador e estão aprovadas. Não são tarefas pendentes nem se reabrem.

## Tipos de produção

| Tipo | O que é | Frentes |
|---|---|---|
| Episódio de série | Peça recorrente com personagem, fórmula e identidade fixas | Mana & Burn, Conde de Manaforte, Meta em Curto · Oráculo de Tubo |
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
| Conteúdo produzido | Reel 9:16, 35–45 s; carrossel e Stories derivados (`formatos.py` do motor v2) |
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
| Conteúdo produzido | Reel 9:16, ~42–48 s |
| Relação com o BINDER Vision | Fecho do scanner; verde BINDER só no fecho |

### Meta em Curto · Oráculo de Tubo (personagem TUBO)

| Campo | Valor |
|---|---|
| Classificação | Série permanente · episódio de série |
| Estado | Ativa |
| Nome | O repositório usa "Meta em Curto" como nome público (ex-"Oráculo de Tubo"); a missão de 31/10 chama-lhe "Oráculo de Tubo". **Lacuna: confirmar o nome público** (pergunta registada em `DECISOES.md`) |
| Objetivo editorial | Explicar em ~40 s porque um deck ou uma jogada funcionou (jogador competitivo e de Commander) |
| Identidade | Monitor CRT dos anos 90 com estética de código verde; voz = LED a acender; "fora do tubo / dentro do tubo"; jazz de precisão com o tema "Paper Thin Alibi" |
| Documentação | Bíblia: `oraculo/CONTEXTO.md` · Perfil: `oraculo/PERFIL.md` |
| Regras específicas | Só campeonatos recentes e falados; evidência visual (lista completa, carta oficial, ficha de jogador com silhueta; foto só com autorização); comparar a jogada com 1–2 alternativas |
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
| Documentação | Índice no Drive "Órbita · Star Trek · índice" (pasta 02) · `claude/serie-star-trek-bauhaus.md` no projeto claude.ai · documento mestre do Drive §5, 9–11, 13. **Lacuna: não há bíblia nem pasta no repositório** |
| Regras específicas | Não cita preços; carta e texto parados; sem contador acima da carta; CTA em rotação sem repetir em posts seguidos |
| Formatos | Reel 4:5 (1080×1350), 12 s, 30 fps; formatos Quadro, Constelação, Pergunta e Scanner (os dois últimos sem produção registada) |
| Técnica | Gerador `claude/gerador/` no projeto claude.ai (build2–4, paint.js, anim.js, batch, captions). **Lacuna: código fora do repositório** |
| Relação com o BINDER Vision | Legenda termina com CTA de download. **Lacuna: o fecho do scanner existe só em 9:16; não está documentado como os Reels 4:5 cumprem a regra do fecho** |

## Formato espontâneo

### Lambe-lambe

| Campo | Valor |
|---|---|
| Classificação | Formato espontâneo · publicação espontânea |
| Estado | Ativo, permanente |
| Objetivo editorial | Publicações de oportunidade e experimentais: curiosidades, artistas, demonstrações do app |
| Identidade | Muro de lambe-lambe pop (rosa), papel rasgado e fita só nos cantos de cima; cartaz pop = cultura TCG, cartaz preto BINDER = produto; adesivos "Curiosidade de Magic" (amarelo) e "Artistas de Magic" (azul) |
| Documentação | `claude/reel-lambe-lambe-pop.md` e `claude/00-comece-aqui.md` no projeto claude.ai · índice no Drive (pasta 03) · skill `binder-posts-instagram`. **Lacuna: não há bíblia nem pasta no repositório** |
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

## Frente nova

Criar a pasta, `PERFIL.md` (modelo em `modelos/PERFIL_SERIE.md`) e a bíblia (`CONTEXTO.md`), acrescentar uma secção aqui e uma entrada em `../series.yaml`, e registar em `DECISOES.md`. A constituição não muda.
