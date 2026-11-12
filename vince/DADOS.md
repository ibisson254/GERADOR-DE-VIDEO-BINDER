# Multiverse Capital — de onde vêm os números

Decisão do fundador a 12/11/2026: a série sai **todos os sábados** e o Vince comenta rubricas de dados — carta mais procurada, a que mais valorizou, a que mais desvalorizou. Este documento diz o que é possível hoje, o que não é, e o que se liga quando a instrumentação do BINDER existir.

---

## 1. O que o Scryfall deixa e não deixa fazer

Verificado na documentação da própria API (12/11/2026):

- **"You may not simply repackage, republish, or proxy Scryfall data. Your software must create additional value for end-users."** A regra é contra o reempacotamento simples. Um episódio que explica a causa de um movimento acrescenta valor; uma placa com uma lista de preços copiada não acrescenta nada.
- **Os preços atualizam uma vez por dia** e a própria Scryfall avisa: *"Prices are not updated frequently enough to power a storefront or sales system. You consume price information at your own risk."*
- O Data Intelligence Master v1.2 (§2) e a constituição do estúdio (§4) já tinham fechado a leitura conservadora: **não republicar dados de preço do Scryfall**.

**Posição da série:** mantemos a leitura conservadora, e não por medo — por qualidade. Um preço com até 24 h de atraso, apresentado como "a carta que mais subiu esta semana", é um número que pode estar errado no dia em que o episódio sai. Citar a praça diretamente custa o mesmo e é melhor jornalismo.

**O Scryfall continua a servir para:** texto da carta, oracle_id, coleção, artista, imagem. É aí que ele é insubstituível.

## 2. Hoje: as três rubricas com fontes externas

Cada rubrica leva **nome da fonte, data e hora da recolha** no ecrã, e a nota **"estimativa, não oferta de compra"**.

| Rubrica | Como se apura hoje | Cuidado |
|---|---|---|
| **Mais valorizou / mais desvalorizou** | Variação entre duas datas na mesma praça: Cardmarket (tendência de preço), TCGplayer ou praça brasileira. Sempre a mesma praça nas duas pontas — comparar Cardmarket com LigaMagic dá um número inventado. | Cartas de baixo valor dão percentagens enormes sem significado. Piso mínimo de valor absoluto, senão o "+400 %" é de uma carta de 40 cêntimos. |
| **Mais procurada** | Proxy honesto, com o nome do proxy dito em voz alta: inclusões em baralhos no EDHREC na semana, ou presença em listas de topo. Não é procura de compra; é interesse de construção. | Nunca chamar "mais procurada do mercado" a um proxy. Diz-se o que é: "a mais adicionada a baralhos". |
| **Movimento da semana** | Causa verificada: anúncio da Wizards, banimento, resultado de torneio, reimpressão anunciada ou que não veio. | Uma causa por episódio. Sem causa citável, muda-se de carta. |

**Por verificar antes do primeiro episódio** (não afirmo que existam nem que permitam uso): se o MTGStocks, o MTGGoldfish ou outro agregador publicam listas de maiores subidas e descidas e em que condições as deixam citar. Quem produzir o episódio confirma na própria página de termos e regista no relatório. Até lá, apura-se a variação a partir das praças.

## 3. Amanhã: a rubrica que ninguém pode copiar

O Data Intelligence Master diz a coisa mais importante para esta série, e não é sobre preço:

> O valor do BINDER não está em mostrar o preço do Scryfall — isso é uma comodidade gratuita que qualquer app replica. Está em cruzar essa referência com dados que só o BINDER tem.

Quando a instrumentação existir, a série ganha uma rubrica que mais nenhum canal de Magic no mundo consegue dizer: **"a carta mais procurada no BINDER esta semana"** — desejos, pesquisas e pesquisas *sem resultado*, que é o sinal mais valioso de todos. É a rubrica que justifica a série existir, e é também o melhor anúncio que o app pode ter, porque a resposta só existe dentro dele.

**Mas ainda não existe, e usá-la agora seria inventar.** A 02/10/2026 a base tinha **445 itens, 5 donos de coleção e 11 desejos**. "A carta mais procurada" apurada em 5 pessoas não é um dado: é ruído com ar de número, e é exatamente o tipo de coisa que destrói a credibilidade de um canal que se propõe a falar de mercado.

**Condições para a rubrica entrar no ar** (todas, não algumas):
1. A F0 (instrumentação) no ar, com `oracle_id` nas tabelas e captura de pesquisas com `result_count`.
2. A declaração de Segurança dos dados na Play atualizada para "Análise", a política de privacidade revista e a opção de recusa a funcionar — **antes** da primeira recolha. Isto está escrito no §7 do Data Intelligence e não é negociável.
3. Amostra que sustente o número. O próprio documento impõe k ≥ 5 na apresentação; para uma rubrica pública semanal, o piso tem de ser muito mais alto — proposta: **≥ 300 utilizadores ativos no mês e ≥ 100 eventos na semana**, alinhado com o gatilho da F1. Abaixo disso, a rubrica não vai ao ar.
4. Nunca nomes, nunca localização, nunca uma carta que identifique um utilizador. Agregado ou nada.

**Proposta de faseamento:** até lá, o Vince diz a verdade com graça — "o meu terminal ainda está a aquecer" — e usa as fontes externas. No dia em que a rubrica entrar, é um episódio especial: a estreia do dado próprio.

## 4. Estrutura do sábado (45–60 s)

O boletim semanal já estava proposto na bíblia antiga (07/11) e mantém-se, agora com as rubricas:

1. **0–3 s:** o número da semana — a maior variação, com praça e data.
2. **3–15 s:** **Subiu.** Carta, quanto, e a causa verificada.
3. **15–25 s:** **Caiu.** Carta, quanto, e a causa.
4. **25–35 s:** **Procurada.** O proxy, dito pelo nome que tem.
5. **35–45 s:** o telefonema à Fonte a confirmar um dos três; se algum número não tiver fonte fechada, é esse que "não atende".
6. **Fecho:** scanner.

Uma carta por rubrica. Três cartas por episódio, não mais — o objetivo é que o espectador consiga repetir uma delas a um amigo no dia seguinte.

## 5. Fronteira com o Giro de Domingo

O Giro do Mana & Burn sai ao domingo e dá notícia da semana. O Vince sai ao **sábado** e dá mercado. Ficam a um dia de distância, por isso a regra é dura:

- **Notícia de mercado** (uma polémica de preço, um hype) é do Giro.
- **Variação de preço com causa e números** é do Vince.
- O que o Vince deu no sábado **não se repete** no Giro no domingo; se for grande de mais para ignorar, o Giro refere em uma linha e manda ver o episódio do Vince.
- A pesquisa de sábado à tarde do Giro passa a ler primeiro o episódio do Vince desse dia.
