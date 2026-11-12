# Vince Vault · Bíblia do personagem

Estado: **personagem em desenvolvimento** (07/11/2026). Ainda não é uma frente: falta o fundador decidir o formato (série própria, convidado do Mana & Burn ou outro). Até lá não entra em `nucleo/CATALOGO_EDITORIAL.md` nem em `series.yaml`.

## 1. Quem é

- Nome: **Vince Vault**. Casa fictícia: **Multiverse Capital**. Bordão: **"Buy the dip!"**. Apelido: "Vaultinho".
- Corretor da bolsa dos anos 80/90: narcisista, hiperativo, informado.
- Regra do estúdio: quando fala de preços, os números vêm de dados reais (Scryfall/Cardmarket, com data). Nunca inventar preços, valorizações nem previsões apresentadas como facto.

## 2. Visual oficial

Referência canónica: `referencias/01_turnaround_OFICIAL.jpg` (versão A da folha original). Em qualquer geração nova, anexar o turnaround como **referência 1**.

Características visuais detalhadas (proporções, rosto, roupa, acessórios, paleta, expressões, regras do fantoche e lista de conferência): `FICHA_VISUAL.md`.

Bloco fixo para prompts (copiar sem alterar):

```
CHARACTER LOCK — "Vince Vault". Match the attached reference images exactly; they are the ground truth for face, hair, outfit and proportions.
Stylized 3D animated-feature character, premium cartoon render, soft cinematic lighting, clean subsurface skin shading.
Adult man, early 40s, warm tan skin. Exaggerated heroic proportions: broad shoulders, V-shaped torso, very large square jaw with prominent chin, thick dark arched eyebrows, confident smirk with bright white teeth.
Hair: tall glossy jet-black pompadour quiff, swept back, perfectly styled, identical silhouette in every image.
Signature eyewear: gold-framed aviator sunglasses (only ONE pair, on the face or pushed up on the hair).
Outfit: navy-charcoal pinstripe double-breasted suit with gold buttons, crisp white dress shirt, red silk tie with subtle paisley pattern, red pocket square, polished black dress shoes.
Accessories: chunky gold wristwatch on LEFT wrist, gold signet ring on RIGHT hand.
Consistency rules: same face shape, same hairstyle, same tie color, same suit pattern in every output. Anatomically correct hands with five fingers.
Output rules: NO text, NO letters, NO logos, NO watermark, NO captions, NO labels anywhere in the image.
```

Cenários: pregão da bolsa à noite, como na folha original. Tons roxo e índigo, brilho violeta dos monitores, candeeiros âmbar e dourados, madeira escura com latão. Os monitores de fundo mostram só gráficos abstratos, **sem números nem texto**. O monitor ou telemóvel "de leitura" sai em ecrã verde (#00B140), para compor dados e ecrãs reais do app.

## 3. Voz

| Campo | Valor |
|---|---|
| Fornecedor | ElevenLabs (voice design, `eleven_ttv_v3`) |
| Nome na biblioteca | Vince Vault |
| voice_id | `L93SDe6kGQj79D6svMgA` |
| Língua | pt-BR |
| Descrição usada | Brazilian Portuguese male voice, early 40s, fast-talking 1980s Wall Street broker. Loud, cocky and theatrical, slightly raspy, a big smile in the voice, salesman cadence with dramatic pauses, charismatic and over-confident. Clean studio quality. |
| Critério de escolha | Das 3 amostras (mesma frase), a de leitura mais rápida (12,6 s contra 13,1 e 13,4 s), coerente com "hiperativo". Escolha feita por Claude a pedido do fundador, sem audição; o fundador valida ao ouvir. |

## 4. Assets (`referencias/`)

| Ficheiro | Estado | Notas |
|---|---|---|
| `00_folha_original.png` | Referência | Folha de conceito inicial (5 versões, 5 expressões, 5 poses). |
| `01_turnaround_OFICIAL.jpg` | ✅ Oficial | Frente, 3/4, perfil e costas. 1408×768. |
| `02_expressoes_A.png` / `_C.png` | ✅ Aprovadas para uso | Grelha 3×3: neutro, confiante, a rir, furioso, chocado, desesperado, sarcástico, pensativo, eufórico. 1376×768: cada célula tem ~450 px, serve para inserções, não para ecrã inteiro. A versão A tem o rosto vermelho no "furioso". |
| `03_base_falar_PROVISORIA_16x9.png` | Substituída | Trocada pela versão 9:16 a 08/11. Mantida até o fundador autorizar apagar. |
| `03_base_falar_916.jpg` | ✅ Base do lip sync | 768×1376 (9:16), app Gemini, 08/11. Frontal, olhar na lente, boca fechada, óculos no topete, fundo do pregão. Enquadramento até às coxas (pedido: cintura) e folga acima do topete ~15%: sobra margem para recortar. Anel nas duas mãos (desvio menor, aceite). |
| `04_pose_andar.jpg`, `04_pose_piscadela.jpg` | ✅ | Corpo inteiro, fundo cinza. O anel está na mão do relógio (desvio menor, aceite). |
| `04_pose_confiante_pregao.jpg` | ✅ Extra (não estava na lista) | 9:16, 08/11. Corpo inteiro no corredor do pregão, sorriso de lado, óculos no topete. Serve de plano de apresentação. Anel na mão do relógio (mesmo desvio aceite). |
| `05_cenario_pregao_corredor.jpg` | ✅ Cenário principal | 9:16. |
| `05_cenario_pregao_mesas.jpg` | ✅ Segundo fundo | 9:16. |
| `06_mesa_ecra_verde.jpg` | ✅ Plano de inserção | 9:16, 08/11, sem personagem. Ecrã verde liso: média RGB (4, 178, 73), desvio < 1, perto de #00B140. O monitor ocupa o centro da mesa, por isso **não dá para pôr o Vince atrás**: usa-se como plano de inserção (dados e telas reais no ecrã), com o Vince noutro plano. A taça toca ~5 px na borda de baixo do verde (o recorte resolve). |

Os ficheiros de 08/11 ficaram em `.jpg`, o formato que o Gemini entrega (converter para PNG não ganha qualidade).

Rejeitados, não versionados: expressões da primeira ronda (sem fato e com outro rosto), folha de bocas (outro rosto; desnecessária, o lip sync dispensa-a), primeira base para falar (dois pares de óculos), mesa na estética verde antiga, palco roxo desfocado (refaz-se em código), expressões B (grelha 5×3 não pedida).

Flow no ElevenLabs com as referências e gerações: `https://elevenlabs.io/app/flows/wUUIl1MCrzeChYd1Lejx`

## 5. Em falta

1. ~~Base para falar em 9:16~~ e ~~mesa com ecrã verde~~: feitas a 08/11.
2. Poses restantes: a apontar para a câmara, a comemorar, a reclamar, a pensar, ao telefone dourado, com o telemóvel em ecrã verde e com uma carta em ecrã verde. Nenhuma é necessária para o Reel de teste.
3. Fundador ouvir e validar a voz.
4. Decisão do fundador sobre o formato e a frente: proposta em `PROPOSTA_FORMATO.md`.
5. Primeiro teste de lip sync (gancho de 3–5 s), com o custo estimado antes; depende da renovação do saldo.

## 6. Estratégia de créditos (decidida a 07/11/2026)

Custos medidos no ElevenLabs a 07/11/2026, por imagem: Nano Banana Pro (`gemini-3-pro-image`) ~1.830 créditos; Nano Banana 2.1 ~407; Gemini 3.1 Flash ~812.

1. **Imagens fixas no app Gemini/Nano Banana**, fora do ElevenLabs. O ElevenLabs fica só para voz e lip sync.
2. Antes de qualquer geração paga: estimar com `estimate_only` e dizer o custo ao fundador.
3. Uma variação por pedido. Rascunho no modelo barato; o modelo Pro só para a versão final aprovada.
4. Definir o formato (9:16) explicitamente: o prompt sozinho não chega, o ElevenLabs gerou 16:9.
5. Por episódio: guião fechado → todo o áudio de uma vez → só os visuais que o guião pede. Lip sync **só no gancho** (3–5 s); o resto é o Vince em fantoche (expressões e poses existentes, animadas em código, custo zero).
6. Nunca versionar vídeos renderizados.

Lição de 07/11: pedir 4 variações em Nano Banana Pro sem estimativa esgotou o saldo do plano (~5.900 créditos gastos em 4 imagens).
