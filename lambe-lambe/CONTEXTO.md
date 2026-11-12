# Lambe-lambe · bíblia

Formato espontâneo e permanente do @binderthetrade: publicações de oportunidade, experimentais e avulsas. Ativo. Classificação no `nucleo/CATALOGO_EDITORIAL.md`.

Fontes desta bíblia (31/10/2026): `claude/reel-lambe-lambe-pop.md` e `claude/00-comece-aqui.md` (projeto claude.ai, 18–19/10), "Lambe-lambe, Scanner e Na prática · índice" (Drive, pasta 03) e a skill `binder-posts-instagram`. Este ficheiro passa a ser o canónico; os documentos de origem ficam como histórico, com as legendas e os créditos completos de cada peça. Nada aqui foi acrescentado além do que eles dizem.

## 1. Conceito

O muro de lambe-lambe pop é o caos da coleção; o BINDER Vision é a lente que põe ordem.

## 2. Sistema visual

- Muro rosa de lambe-lambe pop. Papel rasgado com canto descolado, fibras na borda, rugas, grão, tinta lascada, restos de cartazes antigos, cola, tags, fita-cola e calçada.
- **Cartaz pop no muro rosa = cultura TCG. Cartaz preto BINDER no muro rosa = produto.**
- A marca entra sempre em preto #050A10 e verde-esmeralda #10B981, nunca tingida de rosa.
- Adesivos de série: amarelo "Curiosidade de Magic", azul "Artistas de Magic".
- Etiquetas: "Quem pintou?" (nome do artista a marcador), "Do Brasil" (verde) e "De Portugal" (vermelha) para artistas lusófonos, "ARTE" com o nome do artista nas peças em vídeo, selo "TELA REAL DO APP" nas demonstrações.
- Cartazes pop desenhados para ilustrar a curiosidade sem copiar a arte da carta; lupas com detalhes ampliados ao lado da carta, que fica inteira.

### Padrão oficial de carrossel (aprovado pelo fundador a 12/11/2026)

Referências de direção de arte: as duas composições enviadas pelo fundador a 12/11/2026 (cartaz de paisagem e cartaz editorial de John Avon). São referência estética, não modelo: os textos factuais delas tinham erros (nome "Jhon", "desde 1998", "mais de 200 cartas") e não se publicam.

- Formato 4:5, 1080×1350 por slide; todos os slides parecem capítulos da mesma publicação de rua.
- Muro rosa, cartazes rasgados e sobrepostos, colagem física; tipografia editorial grande (Anton, Geist, Permanent Marker).
- Slide 1 com gancho visual forte; slides do meio com informação e narrativa; último slide com pergunta e o cartaz preto BINDER.
- Layout das referências (v2, 12/11 12:04): cartaz creme rasgado, selo azul sem símbolo de Magic, título condensado pesado + palavra-chave com risco rosa, imagem grande, faixa preta com o nome, chip amarelo. A imagem grande é um detalhe ampliado da arte real da carta (a carta inteira aparece no carrossel). Sem fotos nem rostos gerados de pessoas reais.
- Cartas reais inteiras, créditos no slide e na legenda. Factos, datas, números e créditos sempre verificados.
- Implementação de referência: `lambe-lambe/carrosseis_artistas/` (LL-ART13 a LL-ART18).

## 3. Formatos já usados

| Formato | Descrição |
|---|---|
| Carrossel 4:5 (5 × 1080×1350) | Padrão oficial desde 12/11/2026: capa ilustrada, 3 slides de história com cartas reais, pergunta + cartaz BINDER |
| Post avulso 4:5 (1080×1350) | Uma curiosidade ou um artista por post ("Curiosidades de Magic", "Artistas de Magic") |
| Reel do scanner 9:16 | Gravação de tela real; gancho → problema → linha de scan esmeralda → app real → cartaz BINDER → CTA (~23 s) |
| "Pause e descubra" 9:16 | Colagens de 0,2 s no muro, cada carta várias vezes sem repetir num intervalo curto; fecho com cartaz preto BINDER |
| "Na prática" 9:16 | Telemóvel colado no muro, legenda numerada por passo, toques reais marcados, nomes de outros utilizadores desfocados |

Som nos Reels: efeitos sintetizados próprios, pico a −6 dBFS; a música é escolhida no Instagram.

## 4. Regras próprias

- Carta limpa: sem filtros, cortes, distorção nem marca d'água. A fita só toca os cantos de cima; nada tapa o rodapé com o artista e o ©.
- Créditos (artista e © Wizards of the Coast; personagens licenciados aos titulares) no post e na legenda.
- Produto só com gravação ou captura real do app. Nada acelerado: os cortes só tiram esperas. Dizer "Gravação real do app" na legenda.
- Pontes para o produto só com funções confirmadas (constituição §9), com as palavras da página do Google Play: scanner ("ajuda a identificar"), Binder com valor de referência ("estimativa, não oferta de compra"), decks, lista de desejos, Explorar e chat ("o app não intermedia pagamentos").
- Lojas, torneios e trocas ficam fora das pontes até haver lojas e utilizadores suficientes.

## 5. Legenda (fórmula v3)

1. Gancho na 1.ª linha (até ~100 caracteres), com ângulo diferente do título do cartaz.
2. A curiosidade em parágrafos curtos, só com factos verificados.
3. Fontes e créditos.
4. Ponte para UMA função real do app.
5. CTA final de download, sempre com "Android" e "link na bio", em rotação: "Baixe o BINDER Vision no Android: link na bio." · "(beta para Android). Link na bio." · "e comece o seu Binder." · "e escaneie a sua primeira carta hoje." · "Seja um dos primeiros colecionadores no BINDER Vision: baixe a beta para Android pelo link na bio."
6. Até 5 hashtags. Uma ação por legenda.

O pacote completo (legenda, comentário fixado, texto alternativo, ficha de fatos) segue a constituição §10 e a skill `binder-posts-instagram`.

## 6. Banco de ideias (19/10/2026, nada aprovado)

Qual versão é a sua? · Problema de colecionador · Cola na loja (com autorização) · Noite de torneio na Arena (depende do teste no app e da loja) · Fichário da semana (com autorização, maiores de 18) · Magic em português · Feito por um colecionador em Castelo Branco (só com o aval do fundador) · Exporte para a LigaMagic (precisa de confirmação da função e de captura real).

## 7. Onde está o material

Peças, legendas e créditos de cada publicação: páginas no claude.ai listadas no índice do Drive (pasta 03) e `claude/reel-lambe-lambe-pop.md`. Ficheiros de trabalho das legendas: `captions_ig.py` / `captions_ig.json` (fonte única das legendas v3, citados no documento de origem; não estão no repositório).
