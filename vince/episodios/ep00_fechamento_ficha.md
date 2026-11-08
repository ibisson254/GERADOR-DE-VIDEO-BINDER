# Ficha · Vince Vault · EP00 (piloto) · Fechamento da semana

Estado: **animatic para aprovação** (08/11/2026). Sem voz nem lip sync: as falas estão em legenda no ecrã. Não publicar.

## Classificação
- Frente: Vince Vault (por aprovar, `vince/PROPOSTA_FORMATO.md`)
- Classe de conteúdo: mercado/preço
- Complexidade: média
- Estratégia: análise de dados, com fonte, data e mercado no ecrã

## Editorial
- Objetivo: testar o Vince como "boletim da bolsa" semanal de cartas acessíveis, com fecho no scanner.
- Proposta de valor: em 30 s, o que subiu, o que caiu e o que está no radar na semana, com cartas que o espectador pode ter.
- Público: jogador de Commander no Brasil.
- Hipótese: um personagem que fala como corretor e se apoia em dados segura a atenção e leva a visitas ao perfil.
- Gancho: "Fechamento da semana no pregão do Magic!"

## Fontes e evidências
| Afirmação | Tipo | Fonte | Data |
|---|---|---|---|
| Gandalf, White Rider a US$ 8,48, +38% na semana; procura puxada por Commander | Facto (atribuído) | MTGStocks, Weekly Winners 2026-45 (Arjen), preço TCGplayer: https://www.mtgstocks.com/news/25844-weekly-winners-2026---45 | 06/11/2026 |
| Plaza of Heroes (Commander da Marvel) a US$ 4,52, "moving down" | Facto (atribuído) | idem | 06/11/2026 |
| Elminster (CLB) a US$ 1,81, "atingiu o fundo e começa tendência de alta" | Facto atribuído ao MTGStocks (indicador Penny Stocks deles) | idem | 06/11/2026 |
| "Buy the dip!" | Bordão do personagem, desmentido em cena | — | — |
| Scanner identifica a carta; Binder mostra valor de referência (estimativa) | Função confirmada | Constituição §9 | 19/10/2026 |

As impressões no ecrã são as base de cada coleção (o MTGStocks liga o preço à impressão base): Gandalf LTR 290 (Ekaterina Burmak), Plaza of Heroes MSC 255 (Taurin Clarke), Elminster CLB 274 (Viktor Titov). Imagens do Scryfall; nenhum preço do Scryfall.

**Porque não a plataforma BINDER:** a 08/11/2026 a base do BINDER não guarda histórico de preços (`analytics.card_price_daily` é a fase F1 do Data Intelligence Master v1.2, ainda por construir), e o valor de referência da app vem do Scryfall, cujos termos proíbem republicar preços. A variação semanal tem de vir de uma fonte que a publique: usou-se o MTGStocks (não o Cardmarket, a pedido do fundador). A app entra como chamada para ação: o espectador vê o valor de referência das suas cartas no BINDER Vision.

## Produção
- Recursos: `03_base_falar_916.jpg` (gancho), expressões C (eufórico, chocado, pensativo, sarcástico), `04_pose_piscadela.jpg`, cenários do pregão, fecho do scanner.
- Motor: `episodios/ep00/render.py` (fantoche em código, trilha sintetizada) + `recortes.py` (tira o fundo cinza das expressões e poses).
- Comando: `cd vince/episodios/ep00 && python3 recortes.py ../../referencias rec && python3 render.py ../../referencias saida.mp4 [narracao.wav]`
- QC (`comum/qc/qc_video.py`): 1080×1920, 30 fps, 34,5 s (30,6 + fecho), −14,6 LUFS, pico −1,2 dBTP, fecho presente, sem problemas mensuráveis. Folha de contacto vista: sem corte lateral, carta inteira e sem nada por cima.
- Easter egg: nenhum.

## Pendente para a versão final
1. Ok do fundador ao guião.
2. Narração: voz "Vince Vault" (`L93SDe6kGQj79D6svMgA`), `eleven_v3`, 1 geração, **670 créditos** (estimativa de 08/11). Saldo esgotado até à renovação.
3. Lip sync do gancho (4,6 s): estimar quando houver saldo.
4. Com a narração, a legenda das falas sai e os tempos das cenas ajustam-se ao áudio.

## Pacote de publicação (rascunho)

**Legenda**
> Fechamento da semana no pregão do Magic.
> Gandalf subiu 38%, Plaza of Heroes está em queda e Elminster entrou no radar. Fonte e datas no comentário fixado.
> Na tela: Gandalf, White Rider (The Lord of the Rings: Tales of Middle-earth, 2023), nº 290, arte: Ekaterina Burmak · Plaza of Heroes (Marvel Super Heroes Commander, 2026), nº 255, arte: Taurin Clarke · Elminster (Commander Legends: Battle for Baldur's Gate, 2022), nº 274, arte: Viktor Titov. © Wizards of the Coast. Conteúdo de fã não oficial. Vince Vault e a Multiverse Capital são personagens fictícios. Não é recomendação de compra.
> #magicthegathering #commander #mtgbrasil #colecionador #binderthetrade
> Baixe o BINDER Vision.

**Comentário fixado**
> Qual dessas três está no seu fichário?
> Dados: MTGStocks, Weekly Winners 2026-45 (06/11/2026), preços do TCGplayer em dólares. Gandalf, White Rider US$ 8,48 (+38% na semana); Plaza of Heroes US$ 4,52 (em queda); Elminster US$ 1,81 (segundo o MTGStocks, no fundo e a começar a subir). Valores mudam todos os dias; são estimativas, não ofertas de compra.

**Texto alternativo**
> Animação com o personagem Vince Vault, corretor de terno risca de giz e topete, num pregão dos anos 80. Aparecem três cartas de Magic com cotações: Gandalf, White Rider, "Alta da semana, +38%, US$ 8,48, 7 dias"; Plaza of Heroes, "No vermelho, em queda, US$ 4,52"; Elminster, "No radar, US$ 1,81, testou o fundo e virou pra cima". Depois: "Buy the dip!", "Não é recomendação. É leitura de gráfico." e "Quanto vale a sua carteira? Escaneie no BINDER Vision e veja o valor de referência." Termina com o scanner do BINDER Vision.
