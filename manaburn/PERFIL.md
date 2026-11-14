# Perfil operacional · Mana & Burn

Herda `nucleo/CONSTITUICAO_EDITORIAL_BINDER_ORIGINALS.md`. Identidade (personagens, cenário, estética, gíria, TV SAL, vozes, trilha): documento da série no Google Drive "BINDER Marketing · Série Mana & Burn" e skill `binder-mana-burn-episodio` (autoridade). Pipeline técnico: `manaburn/LEIA-ME.md`.

- **Território:** cultura e caos de Magic. Cartas polémicas, Salt Score, hype de sets e spoilers, preço noticiado, eventos sazonais, reação da comunidade, notícias da Wizards.
- **Fora do território:** análise tática de jogada ou de metagame → Meta em Curto. Crítica de ilustração → Conde. Um torneio pode entrar como *acontecimento* (reação, polémica), nunca como análise de decisão.
- **Público e necessidade:** jogador casual e de Commander no Brasil que quer rir da mesa e perceber a carta do momento.

## Classes e estratégia por defeito

| Classe | Estratégia | Prova mínima |
|---|---|---|
| Carta polémica / Salt Score | Verificação rápida | Oracle (texto da carta) + EDHREC com data |
| Notícia / anúncio | Verificação rápida com data | Wizards ou Magic.gg; secundária atribuída |
| Tendência / reação da comunidade | Investigação aprofundada | 2 fontes (ex.: EDHREC/Wargamer/MTG Rocks + Reddit), data da semana; opinião da comunidade atribuída |
| Mercado / preço | Análise de dados | Preço com fonte e data, "estimativa"; nada de dados de preço do Scryfall |
| Sazonal | Verificação rápida | Data do evento na fonte oficial |

## Regras próprias de rigor

- Opinião é do Burn e do Mana; facto tem fonte. O "Lê a carta" do Mana é sempre regra real, conferida no Oracle.
- Putômetro = Salt Score do EDHREC ÷ 4, conta e fonte no ecrã; sem dado real, sai o putômetro.
- Manchetes da TV SAL: piada sobre o meta, sem pessoas reais; facto citado numa manchete tem de ser verdadeiro.
- Tema que muda depressa: dizer o "quando" (data da fonte) na legenda ou no comentário.

## Gancho e fecho

Gancho: opinião quente do Burn. Fecho: pergunta do Burn (a mesma do comentário fixado) → "Comenta aí." do Mana → TV desliga e vira o ponto verde da logo → fecho do scanner.

## Luz e cenário

Luz padrão em todos os episódios novos (decisão de 07/11/2026): sala antiga com luz quente, reflexo frio da TV, primeiro plano mais escuro. Desde 08/11/2026 vem do cenário (`index.html`, sala v3), com a mesa de noite de Commander; `luz.py` só para vídeos de outro motor.

## Formato

Duração livre (constituição §6): a necessária para reter sem perder o ritmo. Referência histórica: 35–53 s nos episódios, 65 s no Giro de domingo. Bate-volta (14 falas no formato base), -14 LUFS.

Formato derivado **Giro de domingo**: três notícias da semana na TV SAL, reação da dupla a cada uma, pergunta "Comenta 1, 2 ou 3" (primeiro publicado a 01/11/2026).

## Capa (modelo fixo desde 14/11/2026)

Todas as capas do Mana & Burn, de episódios novos ou pedidas para episódios antigos, seguem este modelo (fundador, 14/11/2026 02:57; referência: capa do MB-EP11, Numot). Gerador: `manaburn/capas/capa_mb.py`. A capa deixa de ser um quadro tirado do vídeo (`render.py` continua a gerá-lo, mas não é a capa a publicar).

- **Carta principal do episódio** (a da TV) na largura toda, imagem «png» do Scryfall (maior resolução). A arte fica livre em cima; nada tapa a criatura nem o nome da carta. Sem personagens.
- **Frase** (2–5 palavras, branco, Bangers) e **foco** (1 palavra ou número, amarelo #FFD84A, gigante, com brilho), por cima do texto de regras escurecido. A frase repete a ideia do gancho; o foco é a palavra que a pessoa tem de ler na miniatura.
- **Selo vermelho** (opcional, 1 só) com o dado-chave do episódio (ex.: «−2 POR PANCADA»), no canto da arte, sem tapar a criatura.
- **Faixa fixa** em baixo: «MANA & BURN · EP. NN» a amarelo; à direita, o formato ou a collab a branco (ex.: «COMMANDER»).
- Tudo dentro do recorte 3:4 da grelha (y 240–1680); conferir o `*_grelha.png` em tamanho pequeno antes de entregar.
- Crédito da carta da capa na legenda (já é o crédito da carta da TV).
- Episódio sem carta principal (notícia, Giro): usar a carta mais representativa; se não houver, perguntar ao fundador.

Exemplo: `python3 capas/capa_mb.py --scryfall cmd/215 --frase "O dragão que come" --foco "terreno" --selo "−2 por pancada" --ep 11 --tag Commander --saida MB_EP11_CAPA.png`

## Ponte para o BINDER

Ligada à carta do episódio, entre as funções confirmadas (ex.: escanear e ver o valor de referência). CTA da legenda não repete o do post anterior.

## Métrica principal

Respostas à pergunta do comentário fixado (o histórico de 26/10 mostra comentários quase a zero: testar pergunta A/B ou de número). Secundária: partilhas.

## Critérios de aceitação próprios

- [ ] Gíria: máx. 2 por fala, entendida no Brasil inteiro, sem palavrão; bordões intactos.
- [ ] Carta inteira na TV, também nos zooms; destaques alinhados ao texto.
- [ ] TV SAL sem cortes nos zooms; putômetro com conta e fonte.
- [ ] "Comenta aí" na parada seca da música.
- [ ] Vozes geradas no plano com licença comercial.

## Lacunas conhecidas

- Kit v2 no repositório desde 02/11/2026 (`manaburn/LEIA-ME.md`); a skill ainda aponta para o projeto claude.ai. O motor do Giro de domingo foi feito noutro chat e não está no repositório.
- O fecho com logo próprio da série + fecho do scanner: confirmar no próximo episódio que os dois não se sobrepõem.
