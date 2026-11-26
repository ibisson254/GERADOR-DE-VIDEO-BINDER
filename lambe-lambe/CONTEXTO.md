# Lambe-lambe · bíblia

Formato espontâneo e permanente do @binder_vision: publicações de oportunidade, experimentais e avulsas. Ativo. Classificação no `nucleo/CATALOGO_EDITORIAL.md`.

Fontes desta bíblia (31/10/2026): `claude/reel-lambe-lambe-pop.md` e `claude/00-comece-aqui.md` (projeto claude.ai, 18–19/10), "Lambe-lambe, Scanner e Na prática · índice" (Drive, pasta 03) e a skill `binder-posts-instagram`. Este ficheiro passa a ser o canónico; os documentos de origem ficam como histórico, com as legendas e os créditos completos de cada peça. Nada aqui foi acrescentado além do que eles dizem.

## 1. Conceito

O muro de lambe-lambe pop é o caos da coleção; o BINDER Vision é a lente que põe ordem.

## 2. Sistema visual

- Muro rosa de lambe-lambe pop. Papel rasgado com canto descolado, fibras na borda, rugas, grão, tinta lascada, restos de cartazes antigos, cola, tags, fita-cola e calçada.
- **Cartaz pop no muro rosa = cultura TCG. Cartaz preto BINDER no muro rosa = produto.**
- A marca entra sempre em preto #050A10 e verde-esmeralda #10B981, nunca tingida de rosa. Desde 23/11/2026 (LL-ECO01, pedido do fundador) o cartaz de produto pode ser verde-esmeralda, com os logótipos em etiquetas pretas; o selo oficial do Google Play entra sem alterações.
- Adesivos de série: amarelo "Curiosidade de Magic", azul "Artistas de Magic".
- Etiquetas: "Quem pintou?" (nome do artista a marcador), "Do Brasil" (verde) e "De Portugal" (vermelha) para artistas lusófonos, "ARTE" com o nome do artista nas peças em vídeo, selo "TELA REAL DO APP" nas demonstrações.
- Cartazes pop desenhados para ilustrar a curiosidade sem copiar a arte da carta; lupas com detalhes ampliados ao lado da carta, que fica inteira.

### Modelo pronto do carrossel (14/11/2026)

Referências canónicas, aprovadas pelo fundador (13/11) e reutilizadas sem gerar imagens: `referencias/carrossel_padrao_01.png` (capa) e `referencias/carrossel_padrao_02.png` (editorial). São os slides do John Avon sem texto. Todas as páginas de um carrossel novo saem destes dois modelos: muro rosa, folha creme rasgada, selo azul «Artistas de Magic», papéis kraft, faixa preta com risco rosa, fitas.

- Motor: `kit_carrossel/motor_padrao.py` (instruções em `kit_carrossel/LEIA-ME.md`). Fontes livres: `sh kit_carrossel/preparar_fontes.sh`.
- Carrossel novo = script curto na pasta do episódio, com cartas reais do Scryfall. Zero créditos ElevenLabs.
- Cartas inteiras, fita só nos cantos de cima, sem texto sobre arte, crédito em cada página. Foto do artista só a enviada pelo fundador, em recorte P&B, sem tapar a arte.
- Exemplo: `episodios/ll-art13_nathanna_sete_cartas/` (7 slides).

### Story animado de cada carrossel (16/11/2026)

Todo carrossel Lambe-lambe sai também com um Story de 9 s (1080×1920) «o cartaz está sendo colado no muro», feito com `kit_story/motor_story.py` a partir dos mesmos materiais (instruções em `kit_story/LEIA-ME.md`; referência LL-ART20). Publica-se logo depois do carrossel, com o sticker de link para o post. Com foto de terceiros por autorizar: versão prévia privada + versão sem foto.

### Entrega no chat

No fim de cada lambe, enviar ao fundador, separados e prontos a copiar: capa, legenda, comentário fixado e texto do sticker do Story.

## 3. Formatos já usados

**Padrão de vídeo (26/11/2026, decisão do fundador):** todos os vídeos 9:16 do Lambe-lambe seguem a linguagem do LL-ECO01 e são feitos com `lambe-lambe/kit_video/motor_video.py` (instruções em `kit_video/LEIA-ME.md`): muro rosa; cada cena abre com um cartaz grande colado por cima do anterior (creme, kraft, preto, amarelo ou verde); faixas de papel com texto, cartas e autocolantes voam e batem no muro com mola e sombra; texto carimbado; câmara com recuo de abertura (objeto em tela cheia no quadro 0) e tremor em cada impacto; efeitos sintetizados próprios; fecho do scanner. Primeiras aplicações: LL-ECO01 e LL-ART21 V3/V4. Cartas grandes, uma de cada vez, coladas por cima da anterior e recortadas à mão (margem branca cortada à tesoura); nada de cartas pequenas lado a lado (fundador, 26/11/2026, 23:27). Os formatos abaixo continuam válidos como conteúdo, mas passam a ser montados neste padrão.

| Formato | Descrição |
|---|---|
| Post avulso 4:5 (1080×1350) | Uma curiosidade ou um artista por post ("Curiosidades de Magic", "Artistas de Magic") |
| Reel do scanner 9:16 | Gravação de tela real; gancho → problema → linha de scan esmeralda → app real → cartaz BINDER → CTA (~23 s) |
| "Pause e descubra" 9:16 | Colagens de 0,2 s no muro, cada carta várias vezes sem repetir num intervalo curto; fecho com cartaz preto BINDER |
| "Na prática" 9:16 | Telemóvel colado no muro, legenda numerada por passo, toques reais marcados, nomes de outros utilizadores desfocados |

Som nos Reels: efeitos sintetizados próprios, pico a −6 dBFS (true peak, garantido pelo motor); a música é escolhida no Instagram, por isso o volume médio fica abaixo de −14 LUFS e o P1 de loudness do QC é aceite nesta frente.

## 4. Regras próprias

- Gancho visual (19/11/2026, `nucleo/SHOWRUNNER.md` §4.1): o objeto (carta, artista, tela real do app) aparece no 1.º slide ou no quadro 0, numa leitura simples e forte; o formato continua pop e espontâneo (ficha curta).
- Carta limpa: sem filtros, cortes, distorção nem marca d'água. A fita só toca os cantos de cima; nada tapa o rodapé com o artista e o ©.
- Créditos (artista e © Wizards of the Coast; personagens licenciados aos titulares) no post e na legenda.
- Produto só com gravação ou captura real do app. Nada acelerado: os cortes só tiram esperas. Dizer "Gravação real do app" na legenda.
- Pontes para o produto só com funções confirmadas (constituição §9), com as palavras da página do Google Play: scanner ("ajuda a identificar"), Binder com valor de referência ("estimativa, não oferta de compra"), decks, lista de desejos, Explorar e chat ("o app não intermedia pagamentos").
- Trocas e funções de loja ficam fora das pontes. Desde 23/11/2026 (confirmação do fundador): jogadores perto, chat, campeonatos, exportação LigaMagic e «gratuito» podem entrar, sem telas inventadas (LL-ECO01).

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
