# Perfil operacional · Vince Vault (proposta)

Versão 0.1 · 07/11/2026 · **proposta, não ativa**. Herda `nucleo/CONSTITUICAO_EDITORIAL_BINDER_ORIGINALS.md`. Identidade criativa: `vince-vault/CONTEXTO.md`. Marcas [CONFIRMADO]/[PROPOSTA]/[HIPÓTESE]/[PENDENTE]: ver `PROPOSTA.md`.

- **Identidade (autoridade, depois da ativação):** `vince-vault/CONTEXTO.md`
- **Território [CONFIRMADO]:** acompanhamento sistemático do mercado de cartas de Magic: cartas que mais valorizaram e desvalorizaram, mais procuradas, caras, procura e liquidez, tendências, movimentações, análise de oportunidades, previsões marcadas como opinião.
- **Fora do território:** pico de preço isolado como notícia, hype e reação da comunidade → Mana & Burn. Decisões de jogo, listas e metagame → Meta em Curto (o Vince cita um torneio só como causa, com fonte). Arte → Conde. Regras de fronteira: `PROPOSTA.md` §4.
- **Público e necessidade [PROPOSTA]:** colecionador e jogador de Commander no Brasil que compra e vende cartas e quer saber, uma vez por semana, o que mexeu de verdade no mercado sem cair em preço anunciado nem em hype.
- **Frequência [CONFIRMADO]:** 1 episódio por semana. Não aumenta sem decisão do fundador.

## Classes e estratégia por defeito

| Classe | Estratégia (constituição §3) | Prova mínima |
|---|---|---|
| Maior alta / maior queda da semana | Análise de dados | 2 mercados (TCGplayer + Cardmarket) na mesma janela; preço vendido, não anunciado; nº de vendas se a fonte publica |
| Cartas caras ("Baleias") | Análise de dados | Vendas concluídas com data; amostra dita no ecrã |
| Procura e liquidez | Análise de dados | Indicador nomeado (vendas na janela, ofertas disponíveis, spread de buylist) com fonte |
| Causa de um movimento | Verificação rápida com data | Fonte primária (Wizards para reimpressão/proibição, resultado oficial de torneio) |
| Previsão / oportunidade | Opinião registada | Carimbo "PALPITE DO VINCE · opinião, não recomendação"; registo em `comum/historico.md`; revisão no Placar |

## Metodologia de investigação de mercado

### Princípios
1. **Não inventar dados.** Sem fonte, a afirmação sai (constituição §11.3).
2. **Toda afirmação de mercado leva: fonte, data de consulta, janela (período) e amostra.** No ecrã (linha de fontes ≥ 24 px) e na ficha.
3. **Previsão nunca vira certeza nem recomendação.** Bordão obrigatório: "Opinião minha. Dinheiro seu. Decisão sua."
4. **Uma impressão de cada vez.** Coleção, número, idioma, acabamento (normal/foil/etched) e condição (NM por defeito) sempre ditos. Nunca misturar impressões nem somar mercados diferentes.

### Os sete conceitos que nunca se confundem

| Conceito | O que é | Onde se vê |
|---|---|---|
| **Preço anunciado** | O que um vendedor pede agora | TCGplayer "Low" e "Listed Median"; Cardmarket "From"; lojas brasileiras na LigaMagic |
| **Preço vendido** | O que alguém pagou | TCGplayer "Market Price" (média de vendas recentes); Cardmarket "AVG1/AVG7/AVG30" e "Price Trend" |
| **Variação percentual** | (fim − início) ÷ início, na mesma métrica, mesma impressão, mesma janela | Calculada pelo estúdio ou lida em MTGGoldfish "Movers & Shakers" (com a métrica dita) |
| **Volume** | Quantas transações houve na janela | Só quando a fonte publica (ex.: vendas recentes listadas no TCGplayer); senão diz-se "volume não publicado" |
| **Procura** | Quanta gente quer a carta | Indicadores indiretos e nomeados: número de decks no EDHREC, presença em listas de torneio, descida de ofertas disponíveis no Cardmarket |
| **Liquidez** | Facilidade de vender sem perder valor | Vendas na janela, distância entre menor anúncio e preço vendido, **spread de buylist** (diferença entre o preço de venda e o de recompra de uma loja; quanto menor, mais líquida) |
| **Edição, idioma, condição** | O mesmo nome de carta pode valer 10× mais noutra impressão | Sempre explícitos na boleta |

### Fontes (pesquisa de 07/11/2026; termos de uso a reconfirmar antes do piloto)

| Fonte | Uso | Notas verificadas |
|---|---|---|
| **TCGplayer** (EUA, USD) | Preço vendido de referência nos EUA | O "Market Price" é calculado a partir de vendas concluídas recentes no site; "Listed Median" é sobre anúncios e pode ficar muito acima das vendas quando há poucos vendedores ([ajuda TCGplayer](https://help.tcgplayer.com/hc/en-us/articles/222376867-What-do-the-different-price-points-on-TCGplayer-com-mean)). A API não está a ser dada a novos programadores com facilidade ([FAQ TCGCSV](https://tcgcsv.com/faq)). |
| **Cardmarket** (Europa, EUR) | Segundo mercado para confirmar movimentos | Guia de preços com médias de venda de 1, 7 e 30 dias e "Price Trend"; a API de guia de preços está restrita a certos tipos de aplicação ([documentação](https://api.cardmarket.com/ws/documentation/API_2.0:PriceGuide)); o guia de preços e o catálogo passaram a estar disponíveis para descarga a todos os utilizadores no site ([notícia Cardmarket](https://news.cardmarket.com/en/FoW/adding-non-singles-and-accessories-to-the-price-guide)). |
| **MTGGoldfish** | Radar: maiores altas e quedas diárias e semanais por formato | Os preços em papel por defeito passaram a ser o TCGplayer Market Price ([MTGGoldfish](https://www.mtggoldfish.com/articles/website-update-more-accurate-paper-prices)). As listas "Movers & Shakers" incluem valores extremos de mercados finos (cartas de cêntimos com +9.000%), por isso servem de radar, nunca de prova ([exemplo](https://www.mtggoldfish.com/movers/paper/all)). |
| **MTGJSON** | Automatização do radar (dados em ficheiro) | Projeto aberto com preços de Card Kingdom, Cardmarket, Cardsphere e TCGplayer ([modelo de preços](https://mtgjson.com/data-models/price/price-formats)); histórico limitado. Licença dos dados: confirmar antes de publicar números derivados. |
| **TCGCSV** | Histórico diário do TCGplayer (terceiro) | Arquivo diário desde 08/02/2024, atualizado uma vez por dia ([FAQ](https://tcgcsv.com/faq)). Fonte secundária: atribuir sempre. |
| **LigaMagic** (Brasil, BRL) | Preço anunciado nas lojas brasileiras | Plataforma brasileira de preços e mercado de cartas. **A confirmar:** se publica preço vendido e quais os termos de reutilização. Até lá, só "preço anunciado em lojas brasileiras, segundo a LigaMagic", com data. |
| **EDHREC** | Procura em Commander (número de decks) | Não é fonte de preço. |
| **Scryfall** | Identificação da carta, imagem, texto Oracle | **Preços do Scryfall não se usam** (regra do estúdio, constituição §4). |
| Wizards / Magic.gg | Causas: reimpressões, proibições, resultados oficiais | Fonte primária para o "porquê". |

**[PENDENTE]** Outras fontes brasileiras (ex.: outros marketplaces nacionais) a avaliar pelo fundador, que conhece o mercado local.

### Filtros contra falsos movimentos [PROPOSTA]
1. Preço mínimo de entrada no ranking: US$ 2 / € 2 (abaixo disso as percentagens são ruído). Ajustável na ficha.
2. Movimento só é "da semana" se aparecer no TCGplayer **e** no Cardmarket na mesma direção. Se só aparecer num, diz-se "só nos EUA" ou "só na Europa".
3. Subida com poucas vendas é dita com o número de vendas ("Liquidez, meu amigo.").
4. Excluir da lista da semana impressões de tiragem mínima ou promocionais muito raras, salvo se forem o tema.
5. Procurar a causa antes de gravar: reimpressão anunciada, proibição, spoiler, resultado de torneio. Sem causa encontrada: "causa não identificada", nunca uma causa inventada.

### Moeda
**[PROPOSTA]** Mostrar a moeda original (USD/EUR) e, ao lado, o valor aproximado em reais com a cotação PTAX do Banco Central e a data ("≈ R$ … · PTAX dd/mm"). Arredondar para unidades. Valores são "estimativa, não oferta de compra" (constituição §4).

### Registo
Cada episódio tem ficha (`nucleo/modelos/FICHA_EPISODIO.md`) e `epNN_fontes.txt` em `vince-vault/episodios/` com URL, data e hora de consulta, janela e amostra de cada número. Capturas de ecrã das páginas de preço ficam fora do repositório (podem conter dados de terceiros); a ficha guarda o valor e o link.

## Gancho e fecho

Gancho: o número mais forte da semana numa frase de Vince ao telefone (0–3 s). Fecho: pergunta ▲/▼ → "Opinião minha. Dinheiro seu. Decisão sua." (quando houve previsão) → "Fecha o pregão!" → fecho do scanner (`comum/outro/outro_binder_916.mp4`).

## Formato

Reel 9:16, 1080×1920, 30 fps, -14 LUFS, pico < -1 dBFS. Duração livre (constituição §6); referência inicial 45–60 s, a ajustar com a retenção do piloto. Máximo 3 cartas por episódio e 4 números por ecrã. Carta inteira, nada por cima, rodapé visível.

## Ponte para o BINDER

Binder com valor de referência (estimativa), função confirmada (constituição §9): "Quer saber quanto vale a sua? Escaneie no BINDER Vision e veja o valor de referência no seu Binder." Nunca afirmar que o app mostra o mesmo valor do vídeo nem chamar-lhe "cotação".

## Métrica principal [PROPOSTA]

Guardados e partilhas por 1.000 visualizações (conteúdo de dados é guardado). Secundárias: respostas ▲/▼ por 1.000 visualizações; menções espontâneas a "Vaultinho"; retenção média. Marcos de decisão: `PRODUCAO.md` §8.

## Critérios de aceitação próprios

- [ ] Cada número tem fonte, data, janela e amostra no ecrã e na ficha.
- [ ] Anunciado e vendido nunca confundidos; métrica nomeada.
- [ ] Impressão, idioma, acabamento e condição ditos.
- [ ] Movimento "da semana" confirmado em 2 mercados, ou limitação dita.
- [ ] Previsão com carimbo de opinião e bordão de responsabilidade; registada no histórico.
- [ ] Nenhum "compre/venda/invista/garantido".
- [ ] Monitores âmbar, sem verde de terminal; verde BINDER só no fecho.
- [ ] Vaultinho: no máximo 1 reação forte; contagem de episódios sem a piada respeitada.
- [ ] Personagem a partir do pacote aprovado; nada regenerado.

## Lacunas conhecidas

Nome e empresa finais, vozes, trilha, dia de publicação, termos de uso da LigaMagic e da MTGJSON, ferramenta de imagem. Ver `PROPOSTA.md` §8.
