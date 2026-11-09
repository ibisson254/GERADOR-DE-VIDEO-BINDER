# Vince Vault · personagem 3D

Fonte de verdade da criação do Vince em 3D. Qualquer sessão nova que trabalhe no Vince 3D começa aqui. Atualizado a 09/11/2026 (noite).

## ▶ Retomar aqui

**Estado (09/11, noite):** o modelo v02 existe, com rig de corpo, olhos, pálpebras, boca, queixo e sobrancelhas a funcionar; sem óculos. Ficheiro: `Documentos\Vince\vince_modelo_v02.blend` (o v01 ficou intacto). Renders de conferência: `Documentos\Vince\render_v02_corpo.png` e `render_v02_busto.png`.

**Decisão do fundador (09/11):** a geometria do Vince é gerada por IA local (TRELLIS.2, licença MIT, uso comercial livre). O modelo feito à mão (v01) fica só como fonte do rig, do rosto e do lip sync.

**O que está feito no v02:**
- Malha `VINCE_corpo` (83 mil vértices, 90 mil triângulos), gerada de `E:\ComfyUI\input\vince_frente_B.png` → `Vince_00002.glb`. Original de 396 mil vértices guardado na cena `Vince_v02` (`VINCE_hi`).
- `VINCE_rig` (20 ossos) reajustado às proporções novas (pose A). Pesos automáticos calculados num proxy fechado (`VINCE_proxy_pesos`, remesh por voxels) e transferidos para a malha; cabeça 100% no osso `head`.
- **Óculos escondidos** por ordem do fundador (09/11, "não está bem, tira"). Os objetos `oculos_*` e o `OCULOS_ctrl` continuam no ficheiro, ajustados à cabeça nova; basta reativar a visibilidade. Atenção: a bíblia §2 e a ficha tratam os óculos como elemento de assinatura; falta o fundador dizer se saem de vez ou se quer um par novo.
- Olhos: escleras e íris do v01 recolocadas sobre os olhos pintados (centro em x ±0,037, z 1,603), com `olhar_x/z`. Pálpebras novas (`palpebra_obj_E/D`, material `V2_pele` com a cor tirada da textura) ligadas a `palpebra_E/D`.
- Boca: tiras `boca` e `dentes_sup` do v01, 2,4 cm mais acima, projetadas sobre `VINCE_corpo`; ficam invisíveis quando todas as `boca_*` estão a zero (vê-se a boca esculpida). `dentes_inf` escondido.
- Queixo: shape key `queixo` em `VINCE_corpo`, ligada às formas abertas (B–H, riso, choque).
- Sobrancelhas: shape keys `sobr_E/D_sobe` e `sobr_E/D_zanga` em `VINCE_corpo`, com os mesmos controlos em `VINCE_rosto`.
- Ferramentas novas em `vince_ferramentas.py`: `pose(nome)` (A, neutra, braco_ao_lado, bracos_abertos, aceno), `repouso()`, `piscar(frame)`, `olhar(x, z)`.
- Folha das 9 expressões conferida em render (`Documentos\Vince\_conf\x9_*.jpg`).
- As peças do v01 (corpo, cabeça, cabelo, roupa) ficam escondidas na cena `Scene`, não apagadas.

**Defeitos conhecidos do v02 (por resolver):**
1. O casaco saiu com 8 a 9 botões; a ficha pede 6. Corrigir na textura ou gerar de novo.
2. Rebordo irregular entre o queixo e o colarinho (malha fundida pela IA).
3. Sem anel na mão direita: a geração perdeu-o. O `anel_D` do v01 está escondido, por reposicionar num dedo.
4. Dedos sem ossos: as mãos ficam abertas. Uma tentativa de fechar os quatro dedos com dois ossos por mão amassou a malha e foi desfeita; é preciso um osso por dedo, com as articulações marcadas à mão.
5. A boca continua a ser uma tira sobre o rosto (com queixo a acompanhar); não há interior de boca nem língua.
6. Com as sobrancelhas levantadas (chocado, desesperado, eufórico) vê-se o rebordo das pálpebras.
7. Ombros mais largos e cabeça mais pequena do que no turnaround e na base para falar (`03_base_falar_916.jpg`).
8. Lip sync ainda não testado com áudio real.

**Próximo passo concreto:**
1. O fundador vê `render_v02_corpo.png`, `render_v02_busto.png` e a folha de expressões, e decide: seguir com este modelo ou gerar outra imagem no Gemini (cabeça maior, ombros mais estreitos, 6 botões, anel na mão direita).
2. Teste de lip sync com uma fala real (precisa de um `.wav`; gerar no ElevenLabs gasta créditos e exige autorização).
3. Dedos (um osso por dedo), anel, botões e colarinho.

**Por decidir (fundador):** usar o 3D em produção. A ficha §10 limita o lip sync ao gancho (3–5 s); com o rig deixa de haver limite técnico. Se aprovado, registar em `nucleo/DECISOES.md` e atualizar a ficha.

## Onde está cada coisa

| O quê | Onde |
|---|---|
| Ficha visual e referências | `vince/FICHA_VISUAL.md`, `vince/referencias/01_turnaround_OFICIAL.jpg` |
| Blender do fundador | Blender 5.2.3 LTS portátil em `E:\blender.exe`; add-on oficial do Blender Lab "MCP" (porta 9876; ligar o servidor sempre que abrir o Blender) |
| Ficheiro de trabalho | `Documentos\Vince\vince_modelo_v02.blend` (no PC; não vai para o repositório). Cena `Scene` = modelo v02 com rig; cena `Vince_v02` = malha original; cena `Teste_TRELLIS` = primeiro modelo gerado. `vince_modelo_v01.blend` = modelo procedimental, intacto |
| Renders de conferência | `Documentos\Vince\render_v02_corpo.png`, `render_v02_busto.png`; vistas de trabalho em `Documentos\Vince\_conf\` |
| ComfyUI + TRELLIS.2 | `E:\ComfyUI` (atalho "ComfyUI (TRELLIS 3D)" no ambiente de trabalho) |
| Modelos 3D gerados | `E:\ComfyUI\output\3d\` (teste 1: `Vince_00001.glb`; modelo v02: `Vince_00002.glb`, 50 MB) |
| Workflow do ComfyUI | `vince/3d/comfyui/Vince_TRELLIS2_imagem_para_3D.json` (cópia em `E:\ComfyUI\user\default\workflows\`) |
| Instalador reproduzível | `vince/3d/comfyui/instalar_comfyui_trellis2.bat` |
| Ferramentas do rig (expressões, óculos, Rhubarb) | `vince/blender/vince_ferramentas.py` (também dentro do .blend, texto `vince_ferramentas.py`) |
| Construção procedimental v01 (histórico) | `vince/blender/vince_blocking_v01.py` |

## Prompt da folha de modelação (Gemini)

Anexar sempre `01_turnaround_OFICIAL.jpg` como referência 1. Colar o bloco CHARACTER LOCK da bíblia (§2) sem alterar e, a seguir:

```
TASK — 3D MODELING REFERENCE (for 3D reconstruction, not for publishing).
This task overrides the eyewear and expression rules above.
Orthographic FRONT view, full body, head to shoes fully visible, centered, square 1:1 image.
Plain flat light-gray background, flat even studio lighting, no rim light, no colored light, no cast shadow, no perspective distortion.
Pose: neutral A-pose, standing straight, arms straight and angled about 40 degrees away from the body, hands open and relaxed with five separated fingers, palms facing the thighs, feet shoulder-width apart, looking straight ahead.
Face: neutral relaxed expression, mouth CLOSED, eyes open looking straight forward.
NO sunglasses anywhere: remove the aviators completely (not on the face, not on the hair).
Keep everything else identical to the reference: pompadour, square jaw, pinstripe double-breasted suit with 6 gold buttons, white shirt, red paisley tie, red pocket square, gold watch on LEFT wrist, gold signet ring on RIGHT hand, black shoes.
```

Porquê: o rig traz óculos, boca e sobrancelhas próprios, por isso a cabeça tem de vir sem óculos e de boca fechada (senão ficam em duplicado na textura). A pose em A evita braços fundidos ao tronco.

## Gerar no ComfyUI

1. Abrir o atalho "ComfyUI (TRELLIS 3D)"; o navegador abre em `http://127.0.0.1:8188`.
2. Carregar o workflow `Vince_TRELLIS2_imagem_para_3D`; no nó **Load Image** escolher a imagem; **Run**.
3. Na RTX 3060 de 12 GB: cerca de 10 minutos (a primeira geração inclui o carregamento dos modelos). Saída em `E:\ComfyUI\output\3d\`.
4. Para um agente lançar a geração sem cliques nem navegador: o workflow em formato API está em `E:\ComfyUI\user\default\workflows\Vince_TRELLIS2_API.json`. Trocar `["122"]["inputs"]["image"]` pelo nome da imagem em `input\` e fazer `POST /prompt`; acompanhar com `GET /history/<id>`. Se o ComfyUI estiver fechado, arrancá-lo com `venv\Scripts\python.exe main.py` em `E:\ComfyUI` (demora cerca de 1 minuto a responder).
5. O Gemini descarrega em `.jfif`; converter para PNG na raiz de `input\` antes de usar.

Pormenores técnicos: ComfyUI 0.44.0 com suporte nativo ao TRELLIS.2 (sem extensões compiladas), Python 3.12, PyTorch 2.14 cu126, driver NVIDIA 560.94. Modelos em `E:\ComfyUI\models`. O Pixal3D não foi descarregado; o ficheiro com esse nome é uma ligação física ao TRELLIS.2, só para o workflow passar a validação. Interruptor do workflow em TRELLIS.2.

Testes:
- Teste 2 (09/11), vista de frente em pose A, sem óculos e de boca fechada (`vince_frente_B.png`) → `Vince_00002.glb`, 396 mil vértices, 15 minutos na RTX 3060. Braços livres, dedos separados, sobrancelhas e orelhas esculpidas. É a base do v02. A primeira tentativa no Gemini saiu com proporções realistas (cabeça pequena, ombros estreitos) e foi rejeitada; a correção pediu cabeça = 1/4 da altura, ombros largos e pernas curtas.
- Teste 1 (09/11), frente do turnaround oficial → `Vince_00001.glb`, ~395 mil vértices. Muito acima do v01: topete, mandíbula, sorriso, fato com riscas, botões, relógio e sapatos fiéis. Traz óculos e sorriso gravados na textura e os braços colados ao corpo (esperado, por causa da imagem de entrada).

## Licenças das ferramentas 3D (verificado a 09/11/2026)

| Ferramenta | Publicar no Instagram |
|---|---|
| TRELLIS.2 (Microsoft) | Sim, licença MIT. **É a que usamos** |
| TripoSR | Sim, MIT (qualidade de rascunho) |
| Meshy gratuito | Sim, com atribuição (CC BY 4.0) |
| Tripo gratuito | Não (só uso não comercial; o Pro é pago) |
| Hunyuan3D | Não: a licença exclui a UE |

## Rig e rosto do v02

| Parte | Como funciona |
|---|---|
| Rig | `VINCE_rig`: 20 ossos (root, hips, spine, chest, neck, head, shoulder/upper_arm/forearm/hand `.L/.R`, thigh/shin/foot `.L/.R`). `VINCE_corpo` deforma com o modificador Armature; as peças rígidas do rosto estão presas ao empty `PIV_head` (mundo = identidade em repouso) |
| Controlo do rosto | `VINCE_rosto`: `boca_A…boca_H` (Rhubarb), `boca_sorriso/riso/furia/triste/choque/sarcasmo/pensativo`, `sobr_E/D_sobe`, `sobr_E/D_zanga`, `palpebra_E/D`, `olhar_x/z` |
| Boca | Tiras `boca` e `dentes_sup` com shape keys e Shrinkwrap projetado em Y sobre `VINCE_corpo`; shape key `queixo` na malha |
| Olhos | `esclera_E/D`, `iris_E/D`, `palpebra_obj_E/D`, com drivers |
| Expressões | As 9 da ficha §8 em `vince_ferramentas.py` → `aplicar_expressao(nome, frame)` |
| Corpo | `pose(nome)`, `repouso()`; aplicar sempre depois da expressão |
| Cena | Câmaras `VINCE_cam` (corpo) e `VINCE_cam_busto`, 9:16 1080×1920, 30 fps, luz de pregão, EEVEE, fundo índigo |

Convenção de lados: frente = −Y; esquerda dele = +X (ossos `.L`). Nunca espelhar (ficha §10).

Notas de trabalho com o Blender por MCP:
- A interface está em português: procurar nós de shader pelo tipo (`bl_idname`), não pelo nome.
- Os drivers só reavaliam depois de `obj.update_tag()` + `view_layer.update()` + `frame_set`.
- Processos longos (instalações, downloads) correm com `subprocess.Popen` em segundo plano e com registo em ficheiro.
- O Hugging Face corta ligações: usar `curl -C -` em ciclo.
- Cada chamada ao Blender tem de responder em menos de 60 s; esperas longas fazem-se fora do Blender.
- Pesos automáticos falham em malhas de IA (abertas, cortadas nas costuras de UV): calcular num proxy com remesh por voxels e passar com o modificador Data Transfer.
- `V.aplicar_expressao()` faz `frame_set`: aplicar a expressão antes de posar os ossos.
- O texto `claude_util.py` dentro do .blend tem `conff()`, que grava vistas ortográficas de conferência em `_conf\`.
- Rotação dos braços em eixos do mundo: `upper_arm.L` com Y positivo baixa o braço; no `.R` é o sinal contrário.

## Fluxo de lip sync

1. Gerar a fala no ElevenLabs (voz do Vince) e exportar `.wav`.
2. `rhubarb -f tsv -o fala.tsv fala.wav`
3. No Blender, separador Scripting:
   ```python
   V = bpy.data.texts["vince_ferramentas.py"].as_module()
   V.aplicar_expressao("confiante", frame=1, manter_boca=True)
   V.pose("neutra", frame=1)
   V.importar_rhubarb(r"C:\...\fala.tsv", frame_inicio=1)
   ```
4. Render em PNG com fundo transparente ou com o cenário, e montar no pipeline do estúdio.

## Histórico

- 08/11: blocking e modelo v01 procedimental no Blender (corpo, rosto, óculos, fato, mãos), rig, 9 expressões, importador do Rhubarb. O fundador avaliou-o como amador; diagnóstico: as formas geradas por código têm um teto baixo.
- 09/11: escolhida a geração por IA. TRELLIS.2 instalado localmente (gratuito, MIT) em vez de serviços pagos. Teste 1 aprovado como direção.
- 09/11 (noite): folha de modelação gerada pelo fundador no Gemini (segunda tentativa), modelo v02 gerado e com rig. A pedido do fundador, óculos retirados e rosto refinado: olhos e pálpebras de geometria, boca invisível em repouso, queixo, poses de corpo.
