# Vince Vault · Proposta de formato e Reel de teste

Estado: **proposta, por aprovar pelo fundador** (08/11/2026). Nada aqui entra no catálogo nem em `series.yaml` antes do "ok".

## 1. Formato recomendado: série própria, curta, sobre o valor da coleção

**Nome de trabalho:** "Pregão do Vince".
**Território:** quanto vale a carta que o colecionador tem, e porque duas cópias da "mesma" carta valem coisas diferentes (impressão, edição, acabamento). Classe de conteúdo: mercado/preço.
**Porquê série própria:** nenhuma frente fala de valor de coleção; e é o território que liga direto a duas funções confirmadas do app (constituição §9): o scanner que ajuda a identificar a carta e a impressão, e o Binder com valor de referência. O Vince passa a ser a porta de entrada do pilar "problemas dos colecionadores".
**Fronteira com o Mana & Burn:** preço *noticiado* (polémica, hype, picos) continua no Mana & Burn. O Vince não comenta notícias: compara impressões com dados do dia.

Alternativas avaliadas:

| Opção | Contra |
|---|---|
| Convidado do Mana & Burn (intervalo da TV SAL) | Mistura identidades entre frentes (Showrunner §3); seria especial, não formato. |
| Peças avulsas no Lambe-lambe | Gasta o personagem sem fórmula nem continuidade; o Lambe-lambe tem estética própria (muro rosa). |

**Regras propostas para a série** (entram no `PERFIL.md` se aprovada):
- Preços só do Cardmarket (tendência de preço), com data no ecrã (linha de fonte ≥ 24 px) e "estimativa, não oferta de compra". Nunca do Scryfall (termos de uso, constituição §4).
- Sem previsões nem conselho de compra. O bordão "Buy the dip!" é piada sobre a ganância do Vince e fica sempre cortado ou desmentido em cena.
- Lip sync só no gancho (3–5 s); o resto é fantoche em código com os assets aprovados.
- Termina com `comum/outro/outro_binder_916.mp4`.

## 2. Reel de teste · Ep. 0 "Qual deles?"

| Campo | Valor |
|---|---|
| Objetivo | Testar se o Vince segura os 3 primeiros segundos e leva a visitas ao perfil. |
| Público | Jogador de Commander no Brasil que tem cartas comuns em várias edições. |
| Proposta de valor | A mesma carta pode valer muito ou quase nada, e a diferença está na impressão. |
| Carta candidata | Sol Ring (impressa em dezenas de produtos; quase todo jogador de Commander tem um). Confirmar no dia que a diferença entre duas impressões é grande; se não for, trocar de carta. |
| Duração | ~21 s + fecho do scanner. |
| Hipótese | Personagem com rosto e voz + pergunta direta ao espectador retém mais do que a abertura das outras séries. |
| Métrica principal | Visitas ao perfil por 1.000 alcançados; secundária: retenção aos 3 s. |

### Guião (PT-BR)

`[A]`, `[B]` = tendência de preço do Cardmarket recolhida no dia; `[EDIÇÃO A]`, `[EDIÇÃO B]` = as duas impressões escolhidas; `[DATA]` = dia da recolha.

| Tempo | Plano (asset) | Fala do Vince | Texto no ecrã |
|---|---|---|---|
| 0–4 s | **Lip sync** · `03_base_falar_916.jpg`, recorte da cintura para cima | "Você tem um Sol Ring? Ótimo. Mas qual deles?" | QUAL DELES? |
| 4–10 s | Inserção · `06_mesa_ecra_verde.jpg`, no ecrã as duas cartas reais (imagem oficial) lado a lado; zoom lento | (off) "Mesma carta, mesmo texto. Essa aqui sai por [A] euros." | [EDIÇÃO A] · €[A] |
| 10–14 s | Mesmo plano, destaque na segunda carta; corte para a expressão "chocado" (`02_expressoes_C.png`) | (off) "E essa, por [B]." | [EDIÇÃO B] · €[B] · Fonte: Cardmarket, tendência, [DATA]. Estimativa, não oferta de compra. |
| 14–18 s | `04_pose_confiante_pregao.jpg`, entrada lateral com mola, piscar de olhos | "A diferença está na impressão. E impressão, meu amigo, é dinheiro." | A DIFERENÇA ESTÁ NA IMPRESSÃO |
| 18–21 s | `04_pose_piscadela.jpg` sobre `05_cenario_pregao_mesas.jpg` | "Escaneie a sua no BINDER Vision e descubra qual você tem. Buy the… não. Primeiro descubra." | Scanner do BINDER Vision: ajuda a identificar a impressão |
| 21 s → | Fecho do scanner (`comum/outro/outro_binder_916.mp4`) | — | — |

Animação do fantoche (custo zero, em código): respiração lenta, mola de entrada, troca de expressão no corte, brilho dos monitores. A voz das falas em off sai de uma só geração de TTS com o guião inteiro.

### Pacote de publicação (rascunho)

**Legenda**
> Você tem um Sol Ring. Mas qual deles?
> A mesma carta, com o mesmo texto, muda de preço conforme a impressão. Os valores do vídeo estão no comentário fixado.
> Na tela: Sol Ring ([EDIÇÃO A]) e Sol Ring ([EDIÇÃO B]). Arte: [ARTISTAS]. © Wizards of the Coast. Conteúdo de fã não oficial.
> Vince Vault e a Multiverse Capital são personagens fictícios.
> #magicthegathering #commander #mtgbrasil #colecionador #binderthetrade
> Baixe o BINDER Vision.

**Comentário fixado**
> Quantos Sol Ring você tem na coleção?
> Valores do vídeo: [EDIÇÃO A] €[A] · [EDIÇÃO B] €[B] (Cardmarket, tendência de preço, [DATA]). Estimativa, não oferta de compra. O que costuma mudar o preço entre impressões: edição, idade, acabamento (foil ou não) e estado da carta.

**Texto alternativo**
> Personagem animado Vince Vault, corretor de terno risca de giz e topete, num pregão dos anos 80 com monitores roxos. Num monitor aparecem duas cópias da carta Sol Ring com preços diferentes. Texto no ecrã: "Qual deles?", os dois preços com fonte Cardmarket e data, "A diferença está na impressão". Termina com o scanner do BINDER Vision.

## 3. Materiais e custos antes de produzir

| Item | Estado |
|---|---|
| Assets de imagem | Todos aprovados (`referencias/`). Nenhuma pose nova é necessária. |
| Voz | Fundador tem de ouvir e validar `L93SDe6kGQj79D6svMgA` antes. |
| Preços `[A]`/`[B]` e data | Recolher no Cardmarket no dia da produção (o Cardmarket não abre a partir deste ambiente: o fundador envia a captura ou o link). |
| Imagens das cartas e artistas | Scryfall (imagem e créditos; preços não). |
| TTS (~250 caracteres, 1 geração) | `estimate_only` quando houver saldo; esperar "ok". |
| Lip sync do gancho (4 s) | `estimate_only` quando houver saldo; esperar "ok". |
| Fecho do scanner | No repositório. |
