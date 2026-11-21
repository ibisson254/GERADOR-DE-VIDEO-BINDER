# Lisa Marie no Ar · identidade visual

**Versão:** 0.1 · direção para protótipo · 17/11/2026  
**Imagem de referência:** `referencias/estudo_estudio_vj_2026-11-17.png`  
**Referência dos óculos:** `referencias/referencia_oculos_fundador.jpg`

## Princípio visual

Um estúdio pessoal de VJ com energia de televisão musical dos anos 90, reimaginado como editorial digital contemporâneo. A imagem deve parecer feita por um estúdio independente com repertório visual — não uma réplica da MTV nem um cenário genérico de streamer.

## Personagem

- Gata antropomórfica preta e branca.
- Óculos de acetato preto, lentes transparentes; armação com topo ligeiramente ascendente nas laterais e base arredondada.
- Olhos expressivos, focinho e marcações de pelagem consistentes no modelo-mestre.
- Jaqueta bomber carvão, t-shirt gráfica sem marca, calça ampla/cargo e ténis.
- Auscultadores grandes e microfone de apresentadora como acessórios alternáveis.
- A personagem deve conservar proporções, óculos, pelagem, olhos, roupa-base e silhueta entre episódios.

## Cenário-base

- Fundo carvão/plum escuro.
- Um CRT principal com moldura geométrica e conteúdos de apoio.
- Prateleira curta com vinis e livros; não colocar objetos só para preencher espaço.
- Mesa compacta com microfone e pequeno controlador de áudio.
- Painel modular de cartões de pauta e imagens de Magic.
- Luz rosa lateral e luz azul-petróleo secundária.
- Uma zona limpa atrás da apresentadora para títulos e grafismos.

A imagem-conceito já gerada é referência de atmosfera. Ela não deve ser utilizada como se fosse uma camada transparente nem como modelo de animação. O desenho final precisa de uma folha de modelo própria, preferencialmente 2D, com vista frontal, 3/4, perfil, corpo inteiro e expressões.

## Paleta oficial proposta

| Token | Hex | Uso |
|---|---|---|
| Carvão | `#17151B` | Fundo e roupa |
| Marfim | `#F3EBDD` | Texto claro e cartões |
| Rosa elétrico | `#EF4F91` | Acento/identificador |
| Azul-petróleo | `#53BFC0` | Acento secundário |
| Azul-cobalto | `#5267A8` | Gráficos e separadores |
| Amarelo-sinal | `#E4D75A` | Destaques raros |

Regra de proporção: carvão e marfim dominam; rosa e azul-petróleo funcionam como luzes/acento; cobalto e amarelo são detalhes pontuais. Não transformar o programa num layout predominantemente rosa.

## Tipografia

- Títulos: sans-serif condensada, pesada, caixa alta; fallback `Impact, Arial Black, sans-serif`.
- Texto de apoio: sans-serif neutra e altamente legível; fallback `Arial, sans-serif`.
- Máximo de duas famílias por peça.
- Não imitar lettering, logótipo ou tipografia proprietária da MTV.

## Grafismos recorrentes

- Identificador de programa: `LISA MARIE NO AR`.
- Identificador de quadro: `ELAS NO MULTIVERSO`.
- Tarja de apresentadora/convidada: nome + função validada.
- Marcador de emissão original, por exemplo `SINAL 001`, apenas como elemento gráfico; não deve parecer uma funcionalidade real do BINDER.
- Scanlines, ruído analógico, glitch curto e barras de sinal apenas em transições pontuais; nunca sobre texto pequeno ou carta.

## Composição

- Formato mestre: 1080×1920, 9:16, 30 fps.
- Manter rosto, óculos, textos e elementos essenciais dentro da zona segura central.
- O quadro 0 deve mostrar Magic/TCG ou o objeto real da pauta; a vinheta não pode atrasar a identificação do assunto.
- A apresentadora ocupa, em regra, 35–55% da altura quando em plano médio; variar com o material real.
- A carta citada surge inteira e legível; não pôr texto por cima da arte nem cortar o rodapé.
- Para 4:5, criar composição própria; não cortar o Reel automaticamente.

## Filmagem urbana (desde 21/11/2026)

Decisão do fundador: a Lisa ilustrada em primeiro plano sobre filmagem real de cidade (`biblioteca_urbana/`). Aplicado pela primeira vez no LM-EP00.

**Hierarquia (do mais ao menos importante):** 1) evidência da história (carta, obra, pessoa, imagem real); 2) Lisa; 3) legendas; 4) grafismos (identificador, tarja, etiqueta); 5) cidade. Nunca todos os grafismos ao mesmo tempo. A tarja entra quando acrescenta informação e sai. O identificador é pequeno.

**Integração da personagem:**
- Fundo com menos exposição (55–78%) e saturação (70–80%), ligeira deriva para carvão, rosa e azul-petróleo, vinheta e desfoque leve (1,5–6 px). A personagem fica nítida.
- Sombra suave deslocada atrás da Lisa, **sem contorno luminoso**.
- Harmonização de cor: a ilustração puxa no máximo ~6% para a cor média do fundo, sem mudar pelagem, olhos ou óculos.
- Base escurecida (gradiente de carvão) onde o recorte termina: a cintura não acaba num corte seco.
- Grão fino comum a filmagem e ilustração, só para os unir.
- O recorte encosta a uma borda do quadro, para a aresta reta do desenho ficar fora do ecrã.
- A cidade nunca compete com os olhos ou a boca: sem luzes fortes atrás do rosto.

**Escala:** plano médio a 35–55% da altura do quadro. O grande plano destaca a expressão **sem ampliar além do que a arte aguenta**: com a arte-conceito atual (262 px de origem) o limite é ≈2× no plano médio e ≈3× no grande plano. A arte definitiva tem de vir em alta resolução (`BRIEFING_ILUSTRADORA.md`: ≥ 4000 px de altura no plano médio).

**Abertura:** o quadro 0 mostra Magic/TCG ou a evidência central, nunca a cidade sozinha nem a apresentação da Lisa.

**Troca de carta:** rotação 3D no eixo Y (~0,34 s, perspetiva e sombra), a mesma técnica do Meta em Curto, reimplementada no motor da Lisa. As cartas aparecem no tamanho nativo do Scryfall (745×1040), sem ampliação.

**Falas sem voz:** caixa com o rótulo «LISA», junto à personagem e sem tapar o rosto (`COMPORTAMENTO.md` §6).

## Personagem colecionável

A silhueta deve ler-se em miniatura (orelhas altas, óculos grossos, auscultadores, bomber). Assinaturas candidatas e regras de direitos: `BRIEFING_ILUSTRADORA.md` §4–5. Nenhum símbolo de terceiros como assinatura permanente.

## Não fazer

- Não transformar a cidade em cyberpunk, colagem de néons ou fundo de videojogo, nem apresentar um clipe como o sítio onde a Lisa vive.
- Não usar o M-ball, logótipo, paleta/identidade exata, vinheta, tipografia ou elementos proprietários da MTV.
- Não usar a identidade de Lambe-lambe: sem muro rosa, papel rasgado e fita nos cantos como cenário principal.
- Não usar cenário de streaming genérico com RGB por todo o lado.
- Não usar roupa de gala, Moulin Rouge, boina parisiense ou estereótipo de personagem feminina.
- Não mudar óculos, formato do rosto, pelagem ou silhueta entre imagens.
- Não gerar uma versão nova da personagem para cada episódio.

## Prancha «10 inspirações» (19/11/2026) — conceito, não master

Enviada pelo fundador a 19/11/2026. Original e recortes em `referencias/inspiracoes_2026-11-19/` (recorte: `kit/ferramentas/recortar_prancha.py`). Confirma o eixo de cultura pop (`CONTEXTO.md` §2.1) e serve de menu de figurinos por tema; não é ficha de modelo.

| Nº | Look | Tema pop que serve |
|---|---|---|
| 1 | Repórter do Multiverso | look-base de apresentadora (bomber, auscultadores, telemóvel) |
| 2 | Otaku Casual | anime e mangá |
| 3 | DJ de Vinil | música e vinil |
| 4 | Exploradora do Multiverso | viagem pelos planos, lore |
| 5 | Artista de Rua | arte urbana, artistas |
| 6 | Colecionadora de Mundos | colecionismo, cartas |
| 7 | Fashionista do Multiverso | moda |
| 8 | Nerd de Cultura Pop | anime + K-pop + Magic (livros na prancha) |
| 9 | Investigadora de Histórias | `Pista de Arquivo`, perfis |
| 10 | Vibe 90's | anos 90, linguagem VJ |

Constantes que a prancha confirma: gata preta e branca, peito e focinho brancos, olhos âmbar, óculos pretos grossos (no 7 com lentes rosa: variação a decidir), cabelo/franja preta desalinhada.

Paleta da prancha (candidata, não substitui a oficial sem decisão): preto, creme, rosa, roxo, azul-ardósia.

Riscos a resolver antes do master:
- Looks 4 e 6 usam o símbolo de planeswalker e o verso da carta de Magic: marcas da Wizards. Não usar como logótipo ou estampa fixa da personagem sem rever a Fan Content Policy.
- Coroas desenhadas (prancha e estudo de 17/11) lembram a coroa associada a Basquiat; não adotar como símbolo do programa.
- Papel creme, fita rosa e título rasgado aproximam-se do Lambe-lambe. A regra deste guia (estúdio, não muro) continua até decisão do fundador (`nucleo/DECISOES.md`, 19/11).

## Ficheiros-base do kit

- `kit/identidade/abertura_serie.svg`
- `kit/identidade/tarja_vj.svg`
- `kit/identidade/bug_programa.svg`
- `kit/identidade/placa_elas_no_multiverso.svg`
- `kit/identidade/estudio_base.svg`
- `referencias/estudo_estudio_vj_2026-11-17.png`
- `referencias/referencia_oculos_fundador.jpg`
- `referencias/inspiracoes_2026-11-19/` (prancha + 10 recortes)
