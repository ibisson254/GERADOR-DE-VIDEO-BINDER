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

## Formato

35–45 s, 14 falas em bate-volta, -14 LUFS.

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

- O GitHub tem o kit v1 (`manaburn/`); a skill aponta para o código v2 no projeto claude.ai (`claude/gerador-manaburn/`). Até o v2 subir ao repositório, a versão a usar é a v2 do projeto.
- O fecho com logo próprio da série + fecho do scanner: confirmar no próximo episódio que os dois não se sobrepõem.
