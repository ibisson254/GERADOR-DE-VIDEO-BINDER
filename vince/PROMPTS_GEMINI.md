# Vince Vault · Prompts para o app Gemini (Nano Banana)

Gera os assets em falta (bíblia §5) sem gastar créditos do ElevenLabs. Prompts em inglês, porque o modelo os segue melhor.

## Método

1. **Uma conversa do Gemini para o personagem** (base para falar + poses) e **outra só para a mesa**, para o personagem não aparecer no cenário.
2. Na primeira mensagem, anexar as referências e colar o bloco de abertura. A partir daí, cada pedido é curto: o Gemini mantém o contexto na conversa.
3. Escolher o modelo de imagem mais alto que o app oferecer (Nano Banana Pro / "Thinking") e pedir sempre 9:16.
4. Verificar cada imagem com o controlo de qualidade abaixo. Um defeito pequeno pode corrigir-se uma vez por texto ("keep everything identical, only fix …"). Se o rosto ou o cabelo mudarem, abrir uma conversa nova com as mesmas referências.
5. Descarregar em tamanho completo, com o nome da tabela, e enviar ao Claude para guardar em `referencias/`.

## Conversa 1 · Personagem

Anexar: `01_turnaround_OFICIAL.jpg`, `04_pose_piscadela.jpg`, `05_cenario_pregao_mesas.jpg`.

**Mensagem de abertura:**

```
You are producing official reference art for an animated character called "Vince Vault". I attached 3 reference images:
[1] character turnaround — the absolute ground truth for face, jaw, hair, skin tone, proportions and outfit;
[2] a full-body pose — the exact render style to match;
[3] the background world — a 1980s trading floor at night.

Rules for EVERY image in this conversation:
- Stylized 3D animated-feature render, identical to [2]: soft cinematic lighting, clean subsurface skin shading.
- Adult man, early 40s, warm tan skin, broad shoulders, V-shaped torso, very large square jaw, prominent chin, thick dark arched eyebrows, bright white teeth.
- Tall glossy jet-black pompadour, identical silhouette every time.
- Exactly ONE pair of gold-framed aviator sunglasses (on the face or pushed up on the hair, as each request says).
- Navy-charcoal pinstripe double-breasted suit with gold buttons, crisp white shirt, red silk tie with subtle paisley pattern, red pocket square, polished black shoes.
- Chunky gold watch on his LEFT wrist, gold signet ring on his RIGHT hand.
- Anatomically correct hands with five fingers.
- Vertical 9:16 aspect ratio, highest resolution available.
- NO text, NO letters, NO numbers, NO logos, NO watermark anywhere.

Do not generate anything yet. Reply only "OK" and wait for my first request.
```

**Pedido 1 · `03_base_falar_916.png` (o mais importante: alimenta o lip sync)**

```
Request 1. Vertical 9:16 MEDIUM SHOT framed from the WAIST UP — not full body. Vince centered, facing the camera straight on, eyes looking directly into the lens. Sunglasses pushed up resting on top of the pompadour; eyes fully visible. Mouth gently CLOSED and relaxed, neutral-confident expression, shoulders square, both hands low near the bottom edge of the frame, nothing covering the face or neck. Leave clear headroom above the hair (about 8% of the frame).
Background: the trading floor from [3], softly out of focus with bokeh — deep purple and indigo tones, electric violet monitor glow, warm amber lamps; monitors show only abstract glowing charts, no numbers or text. Warm gold key light on his face, violet rim light on his shoulders. Sharp focus on the face.
```

**Pedido 2 · `03_base_falar_916_oculos.png`** (variante, opcional)

```
Request 2. Identical to Request 1 in every detail, except the sunglasses are ON his face covering the eyes. Same framing, same lighting, same background.
```

**Pedidos 3 a 9 · poses de corpo inteiro** (um por mensagem; trocar `[POSE]`)

```
Request [N]. Vertical 9:16 FULL-BODY shot, entire figure visible from the top of the pompadour to the shoes with margin on all sides. Pose: [POSE]. Clear, readable silhouette. Flat solid medium-gray background (#808080) with only a soft contact shadow under the feet. Sunglasses on his face unless the pose says otherwise.
```

| N | Ficheiro | `[POSE]` |
|---|---|---|
| 3 | `04_pose_apontar.png` | pointing straight at the camera with his right index finger, confident grin, leaning slightly forward |
| 4 | `04_pose_comemorar.png` | celebrating with both fists raised above his head, mouth open in a triumphant shout |
| 5 | `04_pose_reclamar.png` | complaining: both palms open and raised, shoulders up, annoyed frown |
| 6 | `04_pose_pensar.png` | thinking: left arm across his chest, right hand on his chin, sunglasses pushed up, eyes looking up and to the side |
| 7 | `04_pose_telefone.png` | talking on a vintage gold corded telephone handset held to his left ear with his left hand, right hand gesturing, cocky smile |
| 8 | `04_pose_telemovel_verde.png` | holding a modern smartphone in his right hand toward the camera at chest height, the screen fully visible and flat, evenly lit pure chroma green (#00B140) with no content and no reflections, looking at the camera with a grin |
| 9 | `04_pose_carta_verde.png` | holding up a single blank trading card between thumb and index finger of his right hand toward the camera at face height, the card face fully visible and flat pure chroma green (#00B140) with no content, raised eyebrow |

## Conversa 2 · Mesa (sem personagem)

Anexar só `05_cenario_pregao_mesas.jpg`.

**`06_mesa_ecra_verde.png`**

```
Match the world, lighting, palette and stylized 3D animated-feature render style of the attached image exactly: a 1980s trading floor at night, deep purple and indigo shadows, electric violet monitor glow, warm amber and gold lamps, polished dark wood with brass rails.

Vertical 9:16, highest resolution available. Front view of an executive trading desk at chest height, polished dark wood with brass trim. On the desk: a vintage gold telephone, a crystal champagne flute, a leather notebook. Behind the desk, ONE large central monitor whose screen is flat, evenly lit pure chroma green (#00B140), no content, no reflections, no glare. It is flanked by smaller retro CRT monitors showing abstract glowing candlestick and line charts. Empty space behind the desk where a character will later be composited, framed waist-up. Background trading floor softly out of focus with bokeh.

NO people, NO characters, NO numbers, NO tickers, NO text, NO letters, NO logos, NO watermark.
```

## Controlo de qualidade (cada imagem)

- [ ] Formato 9:16 vertical
- [ ] Rosto, queixo e topete iguais ao turnaround
- [ ] Um único par de óculos
- [ ] Relógio no pulso **esquerdo**, anel na mão **direita**
- [ ] Gravata vermelha com padrão discreto; fato risca de giz com botões dourados
- [ ] Cinco dedos em cada mão, sem deformações
- [ ] Nenhum texto, número ou logótipo
- [ ] Ecrãs verdes lisos e uniformes, sem reflexos (pedidos 8, 9 e mesa)
