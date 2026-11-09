# Vince Vault · personagem 3D

Fonte de verdade da criação do Vince em 3D. Qualquer sessão nova que trabalhe no Vince 3D começa aqui. Atualizado a 09/11/2026.

## ▶ Retomar aqui

**Estado:** o pipeline está montado e testado. Falta gerar o modelo final e pôr-lhe o rig.

**Decisão do fundador (09/11):** a geometria do Vince é gerada por IA local (TRELLIS.2, licença MIT, uso comercial livre). O modelo feito à mão (v01) fica só como fonte do rig, do rosto e do lip sync. O fundador escolheu a "opção A": imagem→3D em vez de modelar à mão, que considerou amador.

**Próximo passo concreto:**
1. O fundador gera no Gemini a vista de frente com o prompt da secção "Prompt da folha de modelação" (sem óculos, boca fechada, pose em A) e guarda-a em `E:\ComfyUI\input\`.
2. Correr o workflow no ComfyUI (secção "Gerar no ComfyUI") e obter `E:\ComfyUI\output\3d\Vince_000NN.glb`.
3. No Blender: importar, reduzir a malha (hoje tem ~395 mil vértices; alvo de 30 a 60 mil), orientar (frente −Y, 1,85 m), encaixar `VINCE_rig` com pesos automáticos, pôr os óculos (`OCULOS_ctrl`) e o rosto (`VINCE_rosto`: bocas projetadas sobre a cabeça nova, sobrancelhas, pálpebras), e conferir as 9 expressões e o lip sync.
4. Render de conferência contra o turnaround e a ficha §11.

**Por decidir (fundador):** usar o 3D em produção. A ficha §10 limita o lip sync ao gancho (3–5 s); com o rig deixa de haver limite técnico. Se aprovado, registar em `nucleo/DECISOES.md` e atualizar a ficha.

## Onde está cada coisa

| O quê | Onde |
|---|---|
| Ficha visual e referências | `vince/FICHA_VISUAL.md`, `vince/referencias/01_turnaround_OFICIAL.jpg` |
| Blender do fundador | Blender 5.2.3 LTS portátil em `E:\blender.exe`; add-on oficial do Blender Lab "MCP" (porta 9876; ligar o servidor sempre que abrir o Blender) |
| Ficheiro de trabalho | `Documentos\Vince\vince_modelo_v01.blend` (no PC; não vai para o repositório). Cena `Scene` = modelo v01 com rig; cena `Teste_TRELLIS` = primeiro modelo gerado |
| Renders de conferência | `Documentos\Vince\render_teste_v01.png`, `Documentos\Vince\expressoes\_folha_expressoes.png` |
| ComfyUI + TRELLIS.2 | `E:\ComfyUI` (atalho "ComfyUI (TRELLIS 3D)" no ambiente de trabalho) |
| Modelos 3D gerados | `E:\ComfyUI\output\3d\` (teste 1: `Vince_00001.glb`, 49 MB) |
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
4. Para um agente lançar a geração sem cliques: abrir a página no navegador integrado e correr `app.loadGraphData(workflow)` → `app.graphToPrompt()` → `POST /prompt`. Acompanhar com `GET /history/<id>`.

Pormenores técnicos: ComfyUI 0.44.0 com suporte nativo ao TRELLIS.2 (sem extensões compiladas), Python 3.12, PyTorch 2.14 cu126, driver NVIDIA 560.94. Modelos em `E:\ComfyUI\models`. O Pixal3D não foi descarregado; o ficheiro com esse nome é uma ligação física ao TRELLIS.2, só para o workflow passar a validação. Interruptor do workflow em TRELLIS.2.

Testes:
- Teste 1 (09/11), frente do turnaround oficial → `Vince_00001.glb`, ~395 mil vértices. Muito acima do v01: topete, mandíbula, sorriso, fato com riscas, botões, relógio e sapatos fiéis. Traz óculos e sorriso gravados na textura e os braços colados ao corpo (esperado, por causa da imagem de entrada).

## Licenças das ferramentas 3D (verificado a 09/11/2026)

| Ferramenta | Publicar no Instagram |
|---|---|
| TRELLIS.2 (Microsoft) | Sim, licença MIT. **É a que usamos** |
| TripoSR | Sim, MIT (qualidade de rascunho) |
| Meshy gratuito | Sim, com atribuição (CC BY 4.0) |
| Tripo gratuito | Não (só uso não comercial; o Pro é pago) |
| Hunyuan3D | Não: a licença exclui a UE |

## Rig e rosto (feitos no v01, a transferir para o modelo gerado)

| Parte | Como funciona |
|---|---|
| Rig | `VINCE_rig`: 20 ossos (root, hips, spine, chest, neck, head, shoulder/upper_arm/forearm/hand `.L/.R`, thigh/shin/foot `.L/.R`). Peças rígidas presas por empties `PIV_<osso>` com mundo = identidade em repouso, para os drivers continuarem absolutos |
| Óculos | Um par; `OCULOS_ctrl["no_topete"]` 0 = cara, 1 = topete (drivers de posição e rotação) |
| Rosto | `VINCE_rosto`: `boca_A…boca_H` (Rhubarb), `boca_sorriso/riso/furia/triste/choque/sarcasmo/pensativo`, `sobr_E/D_sobe`, `sobr_E/D_zanga`, `palpebra_E/D`, `olhar_x/z` |
| Boca | Três tiras (`boca`, `dentes_sup`, `dentes_inf`) com shape keys e Shrinkwrap projetado em Y sobre a cabeça; transferem para qualquer cabeça nova trocando o alvo |
| Expressões | As 9 da ficha §8 em `vince_ferramentas.py` → `aplicar_expressao(nome, frame)` |
| Cena | Câmara 9:16 1080×1920, 30 fps (como o resto do estúdio), luz de pregão, EEVEE |

Convenção de lados: frente = −Y; esquerda dele = +X (ossos `.L`). Nunca espelhar (ficha §10).

Notas de trabalho com o Blender por MCP:
- A interface está em português: procurar nós de shader pelo tipo (`bl_idname`), não pelo nome.
- Os drivers só reavaliam depois de `obj.update_tag()` + `view_layer.update()` + `frame_set`.
- Processos longos (instalações, downloads) correm com `subprocess.Popen` em segundo plano e com registo em ficheiro.
- O Hugging Face corta ligações: usar `curl -C -` em ciclo.

## Fluxo de lip sync

1. Gerar a fala no ElevenLabs (voz do Vince) e exportar `.wav`.
2. `rhubarb -f tsv -o fala.tsv fala.wav`
3. No Blender, separador Scripting:
   ```python
   V = bpy.data.texts["vince_ferramentas.py"].as_module()
   V.oculos(no_topete=True, frame=1)
   V.aplicar_expressao("confiante", frame=1, manter_boca=True)
   V.importar_rhubarb(r"C:\...\fala.tsv", frame_inicio=1)
   ```
4. Render em PNG com fundo transparente ou com o cenário, e montar no pipeline do estúdio.

## Histórico

- 08/11: blocking e modelo v01 procedimental no Blender (corpo, rosto, óculos, fato, mãos), rig, 9 expressões, importador do Rhubarb. O fundador avaliou-o como amador; diagnóstico: as formas geradas por código têm um teto baixo.
- 09/11: escolhida a geração por IA. TRELLIS.2 instalado localmente (gratuito, MIT) em vez de serviços pagos. Teste 1 aprovado como direção.
