# Ficha · Vince Vault (Multiverse Capital) · VV-EP01 · O Pregão de Véspera

Versão **v2** (12/11/2026, 18h Lisboa): auditoria factual e reconstrução editorial da v1 (16h–17h), por missão do fundador de 12/11, 17:22. A v1 não foi publicada e fica substituída; os scripts dela estão no histórico do Git (commit b2f6624).

## Classificação
- Série: Vince Vault · Multiverse Capital (frente aprovada a 12/11; direção 2D)
- Classe de conteúdo: mercado
- Complexidade: média
- Estratégia: ensinar a ler um número. Sem causa comprovada para o preço, o episódio trata da limitação de mercado que os dados provam: o preço de mercado do #535 assenta em vendas insuficientes e está muito acima do anúncio mais barato

## Editorial
- Objetivo: estreia da série; levar o espectador de «que preço!» a «agora entendi o que esse preço significa»
- Proposta de valor numa frase: US$ 299,98 é a última venda de uma carta com vendas insuficientes para medir volatilidade, e o anúncio mais barato está bem abaixo; em pré-venda, isso ainda não é um preço formado
- Público: jogador brasileiro adulto que abriu ou pensa abrir Collector Booster de Star Trek
- Hipótese a testar: um episódio que desmonta um número (em vez de o celebrar) gera guardados por 1.000 views acima da média do perfil
- Gancho (0–3 s): «Trezentos dólares!», falado; no painel, o contador chega a US$ 299,98 ≈ R$ 1.673,89, com «preço de mercado · TCGplayer (EUA)», data e hora
- Causa do preço: **nenhuma comprovada**; não se atribui causa
- Easter egg: nenhum
- Fecho: `comum/outro/outro_binder_916.mp4` (demonstração real do scanner com Iron Man Armor; não existe gravação real do scanner com o Mr. Spock, por isso a carta da demonstração não foi trocada)

## Auditoria de originalidade
`memoria.py pauta --objeto "Mr. Spock, Science Officer #535 Borderless Surge Foil"` → BLOQUEIA por ORB-17. Comparação:

| | ORB-17 | ORB-18 | VV-EP01 |
|---|---|---|---|
| Objeto | Spock autografado, n.º 1702 (Headliner) | Commander Spock, n.º 2 (deck Commander) | Mr. Spock, Science Officer, n.º 535 (Showcase Surge Foil) |
| Frente | Órbita (estética) | Órbita (estética) | Vince Vault (mercado) |
| Ângulo | «Mais um autógrafo» | «Fascinante» | o que um preço de pré-venda significa |

Impressões diferentes, frentes diferentes, ângulos sem sobreposição: sem conflito editorial. O alerta vem do nome comum da carta. Decisão do fundador registada em `nucleo/DECISOES.md` (12/11, 16:34).

## Auditoria factual (12/11/2026, 17h30 Lisboa)

| # | Ponto | Resultado | Fonte |
|---|---|---|---|
| 1 | Impressão | Star Trek (TRK) #535, mítica, arte de Grant Griffin | Scryfall API `cards/trk/535` |
| 2 | Acabamento | Showcase (moldura Classic Enterprise), borda preta, só surge foil. O TCGplayer cataloga como «(Borderless) (Surge Foil)»; os dados de preço são do produto 725123, que é o #535 | Scryfall; Face to Face Games («[535] [Showcase] [Classic Enterprise] [Surge Foil]»); TCGplayer |
| 3 | Preço de mercado | US$ 299,98, igual à venda mais recente | TCGplayer, produto 725123 |
| 4 | Menor anúncio | US$ 154,99 (MyTCGValue, conferido pelo fundador a 12/11; a página não abre deste ambiente); o TCGplayer mostrava US$ 159,98 noutro momento. Anúncios mudam a toda a hora; o vídeo mostra os dois com a fonte | MyTCGValue; TCGplayer |
| 5 | Quantidade de vendas | **Não há prova direta do número.** Prova direta do limite: o TCGplayer diz que o produto não teve vendas suficientes para calcular a volatilidade; venda mais baixa = mais alta = mais recente = US$ 299,98. A v1 dizia «uma venda»: **retirado** | TCGplayer |
| 6 | Ranking | O TCGIndex ordena as cartas do set por preço de mercado do TCGplayer e põe o #535 em 1.º; outro rastreador (The Hobby Bin) põe o #353 foil acima. O ranking depende do rastreador: **retirado do episódio** (não sustenta a tese) | TCGIndex; The Hobby Bin |
| 7 | Data e hora | consulta de 12/11/2026, 17h30 (Lisboa) | — |
| 8 | Moeda | dólar (praça dos EUA). Sem preço brasileiro do #535 encontrado. Conversão documentada: dólar comercial de fecho de 10/11/2026, R$ 5,58 (último fecho encontrado) | Metrópoles |
| 9 | Mercado × anúncios | mercado US$ 299,98; mediana dos anúncios US$ 193,98; 21 cópias de 14 vendedores; menor anúncio ~US$ 155–160 | TCGplayer |
| 10 | Calendário | pré-lançamento 6–12/11 (lojas WPN podem vender todos os produtos nessa semana); lançamento global 13/11. A v1 dizia «só chega nas lojas dia 13»: **retirado** | WPN, «Star Trek Dates and Details» |

## Roteiro definitivo (voz existente da v1, sem nova geração)

| Tempo | Plano (função) | Voz do Vince | Painel / ecrã |
|---|---|---|---|
| 0,0–3,4 | Painel · impacto | Trezentos dólares! | US$ 299,98 (contador, única vez) ≈ R$ 1.673,89 · preço de mercado · TCGplayer (EUA) · 12/11/2026, 17h30 · conversão: dólar de 10/11, R$ 5,58 |
| 3,4–7,3 | Carta · identificação | Trezentos dólares, meu amigo. | Carta oficial inteira; créditos por baixo: #535 · Showcase · Surge Foil · Grant Griffin · Scryfall · © WotC · © CBS |
| 7,3–10,3 | Conjunto · discurso (pitch) | É o pregão do século! … Buy the d— | — (o toque corta o bordão: desmentido em cena) |
| 10,3–14,0 | Telefone · conflito (pega no auscultador) | Fala. … Quantas vendas? | toque; a bateria da faixa pára |
| 14,0–17,6 | Próximo · a resposta (ao telefone) | — | Fonte: `fonte_ma_noticia`; `telefone_pousa` |
| 17,6–21,0 | Próximo · reação (palma na testa) | — | quem ouve reage |
| 21,0–25,5 | Painel · o dado | O preço de mercado é essa venda. | PREÇO DE MERCADO US$ 299,98 = ÚLTIMA VENDA · TCGplayer: vendas insuficientes para medir a volatilidade |
| 25,5–29,0 | Conjunto · objeção (braços cruzados) | E o anúncio mais barato hoje? | — |
| 29,0–32,8 | Painel · o dado | — | MENOR ANÚNCIO US$ 154,99 ≈ R$ 864,84 · MyTCGValue · anúncio é pedido, não venda · TCGplayer: US$ 159,98 |
| 32,8–36,5 | Conjunto · conclusão (confidência) | Pré-venda não é mercado. | TEM A CARTA? US$ 299,98 é a última venda, não uma oferta. NÃO TEM? O preço ainda não se formou. |
| 36,5–40,9 | Conjunto · ponte (aponta) | Quer saber quanto vale a sua pasta? Escaneia no BINDER Vision. | QUANTO VALE A SUA PASTA? |
| 40,9–44,8 | Fecho oficial | — | scanner real do BINDER Vision |

Frases da v1 retiradas por falta de sustentação: «nem saiu da caixa», «primeiro lugar do ranking», «só chega nas lojas dia treze», «Uma?», «Uma venda. Uma.», «Cento e sessenta», «O preço de verdade nasce quando a carta chega».

A Fonte: um telefonema; não aparece, não fala palavras, não é legendada. A resposta é o som aprovado `fonte_ma_noticia` e a reação do Vince.

## Fontes e evidências
Tabela acima; ligações em `fontes.md`.

## Produção
Ficha técnica: `producao.md`. Controlo de qualidade: `qc.md`, `qc.json`, `folha_contacto.jpg`.

## Controlo de qualidade
`python3 -I comum/qc/qc_video.py … --frente vince`: 1080×1920 · 30 fps · 44,77 s (40,9 s + fecho) · −14,3 LUFS · pico −1,3 dBTP · fecho presente · sem problemas mensuráveis · sem corte lateral (`cropdetect` 1080:1920:0:0). Folha de contacto conferida a olho. Detalhe e correções em `qc.md`.

## Ficheiros finais
- Vídeo: `MultiverseCapital_Ep01_PregaoDeVespera_v2_916.mp4`, entregue ao fundador na conversa de 12/11/2026 (claude.ai, projeto Binder Marketing). Fora do Git.
- Capa: `capa.jpg` (nesta pasta).

## Entregáveis
- [x] Vídeo · [x] Capa · [x] Legenda (`legenda.txt`) · [x] Comentário fixado (`comentario_fixado.txt`) · [x] Texto alternativo (`texto_alternativo.txt`) · [x] Fontes (`fontes.md`) · [x] Ficha técnica (`producao.md`) · [x] Relatório de QC (`qc.md`) · [x] Folha de contacto (`folha_contacto.jpg`)

## Depois de publicar
- Métrica principal: guardados por 1.000 views; secundária: retenção aos 3 s.
- Resultado observado: —
- Aprendizagem: —
