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

## Padrão de episódio (decisão do fundador, 13/11/2026)

Molde: **MB-EP11 (Numot)**, `manaburn/episodios/ep10_numot/`. Todo episódio novo segue estes cinco pontos; fugir de um deles exige registo em `nucleo/DECISOES.md`.

1. **Carta vilã que a mesa já sofreu.** O objeto é uma carta (ou combo) que o jogador casual reconhece como dor real: destruição de terreno, imposto, tranca, roubo. O gancho do Burn diz a dor em uma frase, com um número ("cada pancada dele, somem DOIS!").
2. **Burn exagera → Mana lê a carta e corrige.** O corpo é uma sequência de enganos comuns da mesa, cada um desfeito com o texto Oracle ("Lê a carta…", "Não destrói. Sacrifica."). Mínimo 3 correções reais por episódio; cada uma ensina uma regra que vale guardar. Cartas de apoio entram como insert com crédito.
3. **Prova visual da correção.** Quando o Mana corrige, a imagem mostra a linha da carta que prova (destaque no Oracle, no "6/6", no "não básico").
4. **Pergunta A/B no fim.** O Burn fecha com uma escolha binária de ação ("A, mata o dragão. B, vira amigo do dono"), a mesma do comentário fixado → "Comenta aí."
5. **Par de publicação.** No dia seguinte ao Reel publica-se um carrossel do app (Lambe-lambe) ligado ao tema do episódio, com o pedido de instalação e o link da bio. O pedido do app vive no carrossel e na legenda; o fecho do scanner continua obrigatório no vídeo.

Impulsionamento (quando houver): só o episódio que já mostra guardados acima do normal nas primeiras horas, só no Instagram (sem Facebook), e o carrossel do dia seguinte não se impulsiona antes de medir os toques no link.

Métricas de controlo do padrão: guardados e comentários por 1.000 views, seguidores orgânicos, e toques no link do carrossel do par. Referência MB-EP11: 71 guardados, ~3,9 comentários por 1.000 (orgânico), ~56 seguidores orgânicos; carrossel do par com 43 toques no link (`comum/insights/semanas/2026-11-13.md`).

## Gancho e fecho

Gancho: opinião quente do Burn. Fecho: pergunta do Burn (a mesma do comentário fixado) → "Comenta aí." do Mana → TV desliga e vira o ponto verde da logo → fecho do scanner.

## Luz e cenário

Luz padrão em todos os episódios novos (decisão de 07/11/2026): sala antiga com luz quente, reflexo frio da TV, primeiro plano mais escuro. Desde 08/11/2026 vem do cenário (`index.html`, sala v3), com a mesa de noite de Commander; `luz.py` só para vídeos de outro motor.

## Formato

Duração livre (constituição §6): a necessária para reter sem perder o ritmo. Referência histórica: 35–53 s nos episódios, 65 s no Giro de domingo. Bate-volta (14 falas no formato base), -14 LUFS.

Formato derivado **Giro de domingo**: três notícias da semana na TV SAL, reação da dupla a cada uma, pergunta "Comenta 1, 2 ou 3" (primeiro publicado a 01/11/2026).

## Ponte para o BINDER

Ligada à carta do episódio, entre as funções confirmadas (ex.: escanear e ver o valor de referência). CTA da legenda não repete o do post anterior.

## Métrica principal

Respostas à pergunta A/B do comentário fixado e guardados por 1.000 views. Secundária: toques no link do carrossel do par (padrão de 13/11/2026).

## Critérios de aceitação próprios

- [ ] Gíria: máx. 2 por fala, entendida no Brasil inteiro, sem palavrão; bordões intactos.
- [ ] Carta inteira na TV, também nos zooms; destaques alinhados ao texto.
- [ ] TV SAL sem cortes nos zooms; putômetro com conta e fonte.
- [ ] "Comenta aí" na parada seca da música.
- [ ] Vozes geradas no plano com licença comercial.

## Lacunas conhecidas

- Kit v2 no repositório desde 02/11/2026 (`manaburn/LEIA-ME.md`); a skill ainda aponta para o projeto claude.ai. O motor do Giro de domingo foi feito noutro chat e não está no repositório.
- O fecho com logo próprio da série + fecho do scanner: confirmar no próximo episódio que os dois não se sobrepõem.
