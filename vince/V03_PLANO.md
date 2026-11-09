# Vince V03 · auditoria e plano de execução

Brief do fundador: "Operação Vince V03 — Character Refinement & Performance Engineering" (09/11/2026). Regra central: evoluir, não reinventar. Critério de sucesso: reconhecer o Vince pela caminhada, antes de ele falar.

Fonte de verdade visual para a V03, por decisão do brief: os dois renders da V02 (corpo/busto e folha de nove expressões). Consequências: a malha da V02 fica como base (não se gera outra), o Vince da V03 não usa óculos e o lenço é escuro. Isto diverge da bíblia §2 e da ficha (óculos de assinatura, lenço vermelho); registar em `nucleo/DECISOES.md` quando o fundador aprovar a V03.

## 1. Ferramentas reais (o que existe e o que não existe)

| Função | Ferramenta | Nota |
|---|---|---|
| Decidir, programar, conferir renders | Claude (Fable 5.2) | Não gera malhas nem texturas. Escreve Python para o Blender, lê os renders e corrige |
| Gerar geometria e textura | TRELLIS.2 local (ComfyUI) | Só imagem→3D. Malha sem loops, triangulada, cortada nas costuras de UV |
| Modelar, rig, shape keys, animar, renderizar | Blender 5.2.3 por MCP | Cada chamada tem de responder em menos de 60 s |
| Vídeo | Blender (saída FFMPEG) | Por confirmar no PC do fundador |

Limites que condicionam o plano:
- Não há escultura à mão nem pintura de textura com pincel. Tudo é procedimental: campos de deslocamento, operações de malha, edição de píxeis por regra.
- A malha da IA não tem loops de olhos e boca. Deformações faciais suaves fazem-se com shape keys por campo de deslocamento (como as sobrancelhas da V02). Abrir a boca de verdade exige cortar a malha e modelar o interior.
- A animação é escrita em código (curvas e chaves). Não há captura de movimento nem ajuste à mão no viewport. A qualidade confere-se em vídeo, ciclo a ciclo.

## 2. Auditoria da V02

### Crítico (impede animação de produção)
| # | Problema | Evidência |
|---|---|---|
| C1 | Pernas e braços só em FK, sem IK nem controlo de pés. Não dá para garantir pés sem deslizar | Rig de 20 ossos, sem restrições |
| C2 | Dedos sem ossos; a tentativa com dois ossos por mão amassou a malha | `_conf/p_maoE.jpg` |
| C3 | Boca é uma tira sobreposta, sem lábios, interior nem língua | Folha de expressões |
| C4 | Pesos nunca testados em passada completa (anca, joelho, tornozelo, ombro com balanço) | Só poses estáticas testadas |
| C5 | Lip sync nunca testado com áudio | — |

### Importante
| # | Problema | Evidência |
|---|---|---|
| I1 | Rebordo irregular entre queixo e colarinho | `render_v02_busto.png` |
| I2 | 8 a 9 botões em vez de 6 | idem |
| I3 | Pálpebras são elipsoides soltos; aparecem com as sobrancelhas levantadas. Sem pálpebra inferior | chocado, desesperado, eufórico |
| I4 | Expressões feitas quase só de boca e sobrancelha; bochechas não participam | Folha de expressões |
| I5 | Cabeça pequena e ombros largos face à base aprovada (`03_base_falar_916.jpg`) | Comparação lado a lado |
| I6 | Mãos muito grandes e planas; dedos compridos | `render_v02_corpo.png` |
| I7 | Sem anel na mão direita | idem |
| I8 | Material único vindo do glTF: pele, tecido, metal e couro com a mesma resposta à luz | Nós do material |

### Cosmético
| # | Problema |
|---|---|
| K1 | Riscas do fato pintadas e irregulares |
| K2 | Relógio é um bloco sem mostrador |
| K3 | Cabelo sem brilho anisotrópico |
| K4 | Sem chão nem sombra de contacto nos renders |

## 3. Plano por etapas

Cada etapa grava um ficheiro novo (`vince_modelo_v03a.blend`, `v03b`, …) e só fecha com evidência em render ou vídeo.

### Etapa B · Modelo (ordem de execução)
1. I5: escalar a cabeça (cerca de +12%) e estreitar os ombros por campo de deslocamento, a comparar com a base para falar. Reajustar ossos e rosto.
2. I6: reduzir as mãos (cerca de −12%) em torno do pulso.
3. I1: faixa de colarinho limpa por cima do rebordo, presa ao osso `neck`.
4. I2: achatar os botões a mais e repintar a zona na textura com a cor do fato.
5. I7 e K2: anel e mostrador do relógio em geometria.
6. I8: separar o material em pele (subsurface leve), tecido (mais rugoso), metal e couro, por máscara de cor da textura.

### Etapa C · Rig e expressões
1. C1: IK nas pernas (alvo no pé, polo no joelho), rolamento do pé, IK opcional nos braços, osso de raiz para deslocação.
2. C2: um osso por dedo (3 falanges, polegar 2), com articulações medidas por dedo na malha fechada; pesos por dedo. Se a malha voltar a amassar, retopologia só das mãos.
3. C3: cortar a boca na malha, modelar lábios, cavidade, dentes de cima e de baixo e língua; substituir as tiras por shape keys de lábios e osso de mandíbula. Alternativa se o corte não der malha limpa: manter a tira, com lábios em relevo.
4. I3 e I4: pálpebras superior e inferior que seguem a curva do olho; shape keys de bochechas; rever as nove expressões para olhos, pálpebras, sobrancelhas, bochechas e boca trabalharem em conjunto.
5. C5: teste de lip sync com áudio real (precisa de autorização para o ElevenLabs ou de um `.wav` existente).

### Etapa D · Animação
1. Vince Swagger Walk: ciclo de 42 frames a 30 fps (1,4 s), em loop, no lugar e com deslocação. Chaves: contacto, descida, passagem, subida. Anca com balanço lateral e rotação, ombros em contratempo com acento, braços assimétricos (o direito mais solto), queixo erguido, cabeça com atraso. Pés presos por IK.
2. Conferência: vídeo de frente, de lado e a três quartos; medir o deslizamento dos pés em números (posição do pé de apoio entre frames).
3. Depois: idle, stop, turn, look around, confident pose, laugh, talking, gesture, reaction, todas derivadas da mesma postura de base.

### Etapa E · Render e validação
Renders de frente, lado e costas, corpo inteiro, close-up, folha de nove expressões, vídeos da caminhada e das animações, exportação `.glb` com animações, relatório e lista de limitações.

## 4. Riscos assumidos
- C3 (boca cortada) e C2 (dedos) são os pontos onde a malha da IA pode não aguentar. Há alternativa definida para cada um.
- Animação escrita em código não chega sozinha ao nível de um animador sénior. O que se garante é: loop sem salto, pés sem deslizar, transferência de peso e uma postura reconhecível. O polimento final depende de o fundador ver os vídeos e pedir ajustes.
- Riscas do fato (K1) e brilho do cabelo (K3) só melhoram a sério com texturas novas; ficam para o fim.

## 5. Estado
- 09/11/2026: auditoria e plano feitos. Nada da V03 executado ainda. Base: `Documentos\Vince\vince_modelo_v02.blend`.
- Próximo passo: Etapa C1 e D1 em primeiro lugar (a caminhada é o critério de sucesso), depois B e o resto de C.
