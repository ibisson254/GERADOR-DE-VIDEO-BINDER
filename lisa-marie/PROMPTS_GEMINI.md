# Lisa Marie · Prompts para o app Gemini (Nano Banana)

Gera, sem créditos da ElevenLabs, todas as imagens de que o motor de recorte (`kit/prova_recorte/`) e uma futura douga precisam. Os prompts estão em inglês porque o modelo os segue melhor. Segue o método do `vince/PROMPTS_GEMINI.md`, com uma mudança: **a mestra é feita primeiro, sozinha, e todo o resto deriva dela em conversas paralelas.**

Pedido do fundador (20/11/2026, 00:02). Estas imagens **não são personagem-mestre aprovada** enquanto o fundador não aprovar a imagem M1 (`IDENTIDADE_VISUAL.md`, CONTEXTO §13).

## Porque é que a ordem importa

Cada conversa nova do Gemini «redesenha» a personagem um pouco. Se as 40 imagens forem pedidas em paralelo do zero, saem 40 Lisas diferentes, e foi assim que as tentativas anteriores perderam qualidade. Por isso:

1. **Fase 1 (sequencial, 1 conversa):** gerar e aprovar **uma** imagem-mestra (M1).
2. **Fase 2 (paralela, 5 conversas abertas ao mesmo tempo):** cada conversa recebe a M1 aprovada e **edita** a partir dela, sem desenhar de raiz.
3. **Fase 3 (Claude):** alinho as imagens à M1 por registo de imagem, recorto só a região que muda (boca, olhos, braço) e monto as camadas. O Gemini não precisa de acertar o píxel, só o desenho.

## Preparação

- Modelo: o modelo de imagem mais alto do app (Nano Banana Pro / «Thinking»), proporção **9:16**, resolução máxima disponível.
- Anexos da Fase 1: `referencias/inspiracoes_2026-11-19/01_reporter_do_multiverso.png` (look-base), `referencias/inspiracoes_2026-11-19/00_prancha_10_inspiracoes.png` (estilo e constantes) e `referencias/referencia_oculos_fundador.jpg` (armação).
- Fundo de **todas** as imagens da personagem: verde chroma liso `#00B140`. A Lisa não tem verde, por isso o recorte fica limpo.
- Descarregar cada imagem em tamanho completo com o nome da tabela e enviar ao Claude, ou pô-las numa pasta do PC ligada à sessão. Destino no repositório: `lisa-marie/kit/personagem/gemini/`. As imagens só ficam versionadas depois de aprovadas.

---

## Bloco de identidade (colar no início de TODAS as conversas)

```
CHARACTER LOCK — "Lisa Marie". Treat every rule below as a hard constraint for every image in this conversation.

IDENTITY (never changes):
1. Anthropomorphic adult female cat, tuxedo coat: black head/back/arms, white muzzle, white chest, white blaze between the eyes. NOT a human with cat ears.
2. Large amber-gold eyes with dark pupils and a small white highlight, expressive anime eyes.
3. Thick black acetate glasses exactly like the attached glasses photo: medium-thick frame, outer top corners slightly lifted, rounded-rectangle / subtle cat-eye shape, CLEAR lenses (never tinted, never pink).
4. Messy black fringe/tufts on top of the head, tall pointed ears with pink inner ear and white tufts, long white whiskers, small pink nose.
5. Same head shape, muzzle length, eye spacing and ear size in every image; same body proportions (slim adult, not chibi, not a child).

BASE OUTFIT (unless a request explicitly changes it):
6. Oversized charcoal bomber jacket, plain white graphic tee with an abstract black ink splash (no text, no logo, no symbols), dark wide jeans, black fingerless paw gloves, black studio headphones resting around the neck.

STYLE (match the attached reference sheet exactly):
7. Hand-inked anime illustration: confident dark ink outlines of varying weight, soft cel shading, warm desaturated palette (charcoal, ivory, pink accents #EF4F91, teal accents #53BFC0). Same line weight and rendering in every image.

OUTPUT CONTRACT:
8. Vertical 9:16, highest resolution available, ONE image per request.
9. Background: perfectly flat, uniform chroma green #00B140, no gradient, no shadow, no texture, no paper, no props unless requested. Character fully separated from the background, no green spill on the fur.
10. Absolutely NO text, letters, numbers, logos, brand marks, crowns, Magic: The Gathering symbols or card backs, MTV references, watermarks.
11. Never sexualized, never infantilized.

Do not generate anything yet. Reply only "LOCKED" and wait for my request.
```

---

## Fase 1 · Conversa A · Mestra (sequencial)

Anexar as 3 referências, colar o bloco de identidade e, depois de «LOCKED», enviar:

**M1 · `M1_mestra_frente_916.png`, a imagem de que tudo depende**

```
Request M1. MEDIUM SHOT from the waist up, character centered, body and face turned straight to the camera, eyes looking directly into the lens. Mouth gently CLOSED in a relaxed neutral cat mouth (small "ω" shape). Both arms relaxed and low, hands near the bottom edge, NOTHING crossing in front of the face, neck, chest or headphones. Ears fully inside the frame with 8% headroom above the ear tips. Even, flat front lighting (no strong cast shadows on the face) so parts can be swapped later. Flat chroma green #00B140 background.
```

Gerar até 3 variações. O fundador escolhe **uma** e só depois se passa à Fase 2. Se nenhuma servir, corrigir uma vez por texto («keep everything identical, only fix …»). Se o rosto mudar, abrir uma conversa nova.

**M2 · `M2_ficha_modelo.png`** (na mesma conversa, depois de aprovar a M1)

```
Request M2. Using the approved image as the exact identity, create a character model sheet on a flat chroma green #00B140 background, vertical 9:16, four full-body views of the SAME character in the SAME outfit standing side by side at equal scale: front, three-quarter, side profile, back. Neutral standing pose, arms slightly away from the body. No text, no labels.
```

---

## Fase 2 · Conversas paralelas (abrir as 5 ao mesmo tempo)

Em cada uma: anexar **só a M1 aprovada** (e, na E, a foto dos óculos), colar o bloco de identidade e depois a frase de edição abaixo. Todos os pedidos são **edições da M1**.

Frase de edição (colar logo a seguir ao «LOCKED»):

```
The attached image is the APPROVED MASTER. Every request in this conversation is an EDIT of this exact image: keep the same framing, camera, scale, pose, position in frame, lighting, line weight, colors and background pixel-for-pixel, and change ONLY the part named in each request. If you cannot keep the rest identical, keep it as close as possible rather than redrawing.
```

### Conversa B · Bocas (lip sync, formas do Rhubarb)

Um pedido por mensagem: «Request [ID]. Change ONLY the mouth: [FORMA]. Everything else identical to the master.»

| ID | Ficheiro | `[FORMA]` | Sons |
|---|---|---|---|
| X | `B_boca_X.png` | relaxed closed cat mouth, small soft "ω" (same as master) | repouso |
| A | `B_boca_A.png` | lips pressed firmly closed, slightly tighter and flatter than rest | M, B, P |
| B | `B_boca_B.png` | slightly open, wide, upper and lower teeth visible and nearly touching | K, S, T, EE |
| C | `B_boca_C.png` | open medium, small cat fangs visible, tip of the tongue visible | EH, AE |
| D | `B_boca_D.png` | wide open, tongue visible, small fangs, happy talking energy | AA |
| E | `B_boca_E.png` | open in a medium vertical rounded oval | AO, ER |
| F | `B_boca_F.png` | small tight round pucker | UW, OO, W |
| G | `B_boca_G.png` | upper teeth resting on the lower lip | F, V |
| H | `B_boca_H.png` | open medium with the tongue tip raised to touch behind the upper teeth | L |

### Conversa C · Olhos e sobrancelhas

| ID | Ficheiro | Pedido («Change ONLY the eyes: …») |
|---|---|---|
| C1 | `C_olhos_meio.png` | both eyelids half closed, relaxed blink in progress |
| C2 | `C_olhos_fechados.png` | both eyes fully closed in a soft downward curve, as in a calm blink |
| C3 | `C_olhos_lado.png` | pupils looking to her left (screen right), as if reading a monitor |
| C4 | `C_olhos_cima.png` | pupils looking up and to the side, thinking |
| C5 | `C_piscadela.png` | right eye closed in a playful wink, left eye open |

### Conversa D · Expressões (cabeça e boca podem mudar; o corpo não)

Pedido: «Request [ID]. Change ONLY the facial expression (eyes, brows, ears, mouth) to: [EXPRESSÃO]. Body, outfit, framing and background identical.»

| ID | Ficheiro | `[EXPRESSÃO]` |
|---|---|---|
| D1 | `D_curiosa.png` | curious: head tilted 10°, one ear rotated forward, slight smile |
| D2 | `D_surpresa.png` | surprised: eyes wide, ears straight up, small open "o" mouth |
| D3 | `D_cetica.png` | skeptical: one brow raised, eyes half-lidded, mouth pulled to one side |
| D4 | `D_concentrada.png` | focused: brows lowered, eyes narrowed at the camera, mouth closed |
| D5 | `D_divertida.png` | amused: closed-eye laugh, open smile with small fangs |
| D6 | `D_empatica.png` | empathetic: soft eyes, ears slightly lowered, gentle closed smile |

### Conversa E · Gestos de VJ (poses-chave para recorte e douga)

Aqui o braço muda e a cabeça e o tronco **não**. Cada gesto tem **chave inicial e chave final**, com a mesma câmara. São estas duas chaves que alimentam a douga (ToonCrafter).

Pedido: «Request [ID]. Change ONLY the arms and paws to: [GESTO]. Head, face, glasses, torso, outfit, framing and background identical to the master.»

| ID | Ficheiro | `[GESTO]` |
|---|---|---|
| E1a | `E_acenar_a.png` | right paw raised beside the head, palm facing camera, starting a wave (paw tilted left) |
| E1b | `E_acenar_b.png` | same raised right paw, wave at the other extreme (paw tilted right) |
| E2a | `E_apontar_camara_a.png` | right arm bent, paw at chest height about to point |
| E2b | `E_apontar_camara_b.png` | right arm extended toward the camera, index claw pointing at the viewer |
| E3a | `E_apresentar_ecra_a.png` | left arm relaxed at the side |
| E3b | `E_apresentar_ecra_b.png` | left arm open to her left (screen right), palm up, presenting something off-frame |
| E4a | `E_microfone_a.png` | holding a plain black handheld microphone (no logo) low at the waist |
| E4b | `E_microfone_b.png` | same microphone raised to just below the chin, ready to speak |
| E5a | `E_pensar_a.png` | right paw lowered |
| E5b | `E_pensar_b.png` | right paw on her chin, thinking |

### Conversa F · Estúdio sem personagem (no estilo da ilustração)

Anexar só a M1 e a prancha. **Não colar o bloco de identidade** (aqui não há personagem). Isto resolve o choque entre o fundo vetorial e a personagem ilustrada que se via na prova.

```
Match the line work, cel shading and warm desaturated palette of the attached illustrations exactly, but draw NO characters and NO animals.

Vertical 9:16, highest resolution. A small, lived-in bedroom music-TV studio at night, seen straight on at chest height, as a background plate: a compact desk at the bottom of the frame with a desk microphone and a small mixer; a retro CRT monitor on the right whose screen is flat, evenly lit pure chroma green #00B140 (no content, no reflections); a short shelf of vinyl records and books on the left; a turntable on the desk edge; soft pink key light from the left and teal rim light from the right; the CENTER of the frame (from 15% to 80% height) left empty for a waist-up character to be composited later.

NO people, NO animals, NO text, NO letters, NO numbers, NO logos, NO posters with writing, NO crowns, NO Magic: The Gathering symbols, NO pink paper wall, NO taped posters.
```

Pedir também `F_estudio_vazio_2.png`: «Same studio, camera slightly closer, for a close-up.»

---

## Controlo de qualidade (cada imagem, antes de enviar)

- [ ] 9:16 vertical e fundo verde liso, sem sombra nem papel
- [ ] Rosto, olhos âmbar e manchas do pelo iguais à M1
- [ ] Óculos pretos com lentes **transparentes** e a mesma armação
- [ ] Só mudou o que o pedido mandou (comparar lado a lado com a M1)
- [ ] Mãos/patas com dedos coerentes, sem deformações
- [ ] Nenhum texto, logótipo, coroa ou símbolo de Magic
- [ ] Nem sexualizada nem infantilizada

Uma imagem que falhe o controlo pede-se de novo **uma vez**. Se falhar outra vez, avança-se sem ela e eu resolvo na montagem ou peço outro caminho. Não se gasta a conversa a insistir.

## Quantidades

Fase 1: 1–3 + 1. Fase 2: 9 bocas + 5 olhos + 6 expressões + 10 gestos + 2 estúdios = **32 imagens**, em 5 conversas paralelas.
