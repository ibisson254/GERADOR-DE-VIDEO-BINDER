# Vince Vault · modelo 3D no Blender (v01)

Modelo 3D do Vince feito no Blender 5.2 a partir da `FICHA_VISUAL.md` e do turnaround oficial. Alternativa ao fantoche de imagens do Gemini: qualquer pose, ângulo e lip sync no vídeo inteiro, sem gerar imagens novas. Ainda **não substitui** o fantoche: é preciso decisão do fundador (ver "Por decidir"). Atualizado a 08/11/2026.

## Onde está

- Ficheiro: no PC do fundador, `Documentos\Vince\vince_modelo_v01.blend` (não vai para o repositório, como os vídeos).
- Render de teste 9:16 e folha das 9 expressões: `Documentos\Vince\render_teste_v01.png` e `Documentos\Vince\expressoes\`.
- Ferramentas do rig: `vince/blender/vince_ferramentas.py` (cópia do texto que vem dentro do .blend).

## O que tem

| Parte | Estado |
|---|---|
| Silhueta e proporções | Conferidas com o turnaround de frente e perfil (1,85 m, ~3,6 cabeças) |
| Cabeça | Mandíbula quadrada, queixo saliente, nariz largo, costeletas, sorriso com dentes |
| Topete | Peça única com a onda frontal, brilho e textura de fios |
| Óculos aviador | Um par, armação dourada; `OCULOS_ctrl → no_topete` (0 cara, 1 topete) |
| Fato | Risca de giz (material), lapela de bico, 6 botões dourados, bolsos, lenço à esquerda dele |
| Mãos | 5 dedos; relógio no pulso esquerdo, anel na mão direita |
| Rig | `VINCE_rig`: 20 ossos (cabeça, pescoço, coluna, braços, mãos, pernas, pés), pesos automáticos no corpo |
| Rosto | Controlo `VINCE_rosto`: bocas, sobrancelhas, pálpebras, olhar |
| Expressões | As 9 da ficha §8, em `vince_ferramentas.py` → `aplicar_expressao(nome, frame)` |
| Lip sync | Bocas A–H/X no formato do Rhubarb Lip Sync → `importar_rhubarb(tsv, frame_inicio)` |
| Cena | Câmara 9:16 1080×1920, 30 fps, luz de pregão (âmbar, roxo, violeta), EEVEE |

Convenção de lados: frente = −Y; esquerda dele = +X (ossos `.L`). Nunca espelhar (ficha §10).

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

## Por fazer

- Gravata: falta o padrão paisley (hoje lisa, vermelho-escuro).
- Fato: com a luz de teste sai mais claro que `#1E1F2A`; afinar no cenário final.
- Topete: passagem de escultura para marcar madeixas.
- Cenário do pregão em 3D (monitores CRT, candeeiros) ou composição sobre `05_cenario_*`.
- Poses-chave da ficha (`pose_andar`, `pose_piscadela`, `pose_confiante_pregao`) como poses do rig.

## Por decidir (fundador)

- Usar o 3D em produção. A ficha §10 limita o lip sync ao gancho (3–5 s) e o resto ao fantoche; com o rig isso deixa de ser limitação técnica. Se aprovado, registar em `nucleo/DECISOES.md` e atualizar a ficha.
