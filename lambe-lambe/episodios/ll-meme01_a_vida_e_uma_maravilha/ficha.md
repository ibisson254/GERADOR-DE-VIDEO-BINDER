# Ficha · Lambe-lambe · LL-MEME01 · «O que é a vida? A vida é uma maravilha»

## Identificação
- ID editorial: LL-MEME01
- Estado no registo: CONCLUÍDO (não publicado; a publicação é do fundador)
- Origem: pedido do fundador, 23/11/2026 (14:48): «Quero fazer um vídeo simples com o áudio "o que é a vida, a vida é uma maravilha", um áudio muito usado em memes brasileiros». Às 14:50: «Escolha o caminho que mais o público ia se identificar» → vídeo mudo com o áudio pela biblioteca do Instagram (precedente AB-02, `nucleo/DECISOES.md` 15/11) e a piada do booster.

## Classificação
- Frente: **Lambe-lambe** (espontânea, meme de cultura TCG). Pilar C.
- Formato: Reel 9:16, 1080×1920, 30 fps, 7,0 s + fecho do scanner = 10,87 s, **sem áudio**.
- Motor: `meme_vida.py` (PIL + numpy, muro procedural, fitas só nos cantos de cima). Zero créditos.

## Originalidade (`memoria.py pauta`, 23/11/2026)
- Sheoldred, the Apocalypse: **BLOQUEADA** por LL-SHEOL (Lambe-lambe publicado) → trocada pela Liliana of the Veil.
- Liliana of the Veil, Bog Badger, Academy Wall, Goblin Picker, Tidepool Turtle, Argivian Phalanx: LIVRE.
- Palavra genérica «booster»: a ferramenta acusa MB-EP06 (god packs do Collector Booster) e MB-GIRO01 (Collector Booster de Star Trek) por coincidência de nome. Objeto e ângulo diferentes (aqui: meme de abrir comuns; lá: preço e god packs). **Sinalizado ao fundador** para confirmar.

## Gancho visual (SHOWRUNNER §4.1)
1. Quadro 0: a primeira comum (Bog Badger) já está a bater no muro, com «O QUE É A VIDA?» no topo
2. Objeto: cartas reais de Dominaria United
3. Ação: cinco comuns coladas a cada 0,45 s, contador «COMUM ×1…×5»
4. Som: o áudio do meme, escolhido no Instagram
5. Descoberta até 3 s: corte em 2,5 s com clarão para a Liliana of the Veil
6. Promessa: a virada do pacote ruim
7. Pagamento: «A VIDA É UMA MARAVILHA» + etiqueta «A ÚLTIMA CARTA DO BOOSTER»

## Roteiro definitivo
| Tempo | Imagem | Texto |
|---|---|---|
| 0–2,5 s | 5 comuns DMU coladas uma a uma, tremor curto a cada batida | «O QUE É A VIDA?» · «COMUM ×n» · faixa de créditos |
| 2,5 s | clarão de 2 quadros | — |
| 2,5–7,0 s | Liliana of the Veil cai sobre a pilha escurecida, zoom lento | «A VIDA É UMA / MARAVILHA» · «A ÚLTIMA CARTA DO BOOSTER» · crédito |
| 7,0–10,87 s | fecho do scanner (`comum/outro/outro_binder_916.mp4`) | — |

## Áudio (publicação)
No Instagram: Adicionar áudio → buscar «o que é a vida a vida é uma maravilha» → escolher o trecho para que «a vida é uma maravilha» comece no corte de 2,5 s. Não há ficheiro de áudio no pacote nem nenhum descarregado.

## Imagens e direitos
Cartas reais do Scryfall (PNG, não versionadas), inteiras, sem filtro; fitas só nos cantos de cima; nada sobre o rodapé com artista e ©. Créditos no vídeo e na legenda. Nenhuma afirmação de preço, raridade estatística ou função do app no vídeo (a única parte de produto é o fecho real do scanner).

## Produção
1. Descarregar do Scryfall `dmu/156`, `41`, `128`, `69`, `5`, `97` como `dmu_<n>.png` numa pasta `cartas/`.
2. `python3 -I meme_vida.py cartas frames` (~70 s)
3. `ffmpeg -framerate 30 -i frames/%04d.jpg -c:v libx264 -crf 18 -pix_fmt yuv420p meme.mp4` e concat com o fecho.

## Controlo de qualidade (23/11/2026)
- `qc_video.py --frente lambe`: 1080×1920, 30 fps, 10,87 s (7,0 + fecho), fecho presente a partir de 7,0 s; único aviso «sem faixa de áudio» (esperado).
- Folha de contacto conferida: textos legíveis, sem corte lateral; a etiqueta amarela foi afastada do rodapé da Liliana (1.ª versão tapava o crédito).
- Limitação: o tempo do corte (2,5 s) é estimado; a sincronia final faz-se ao escolher o trecho do áudio no Instagram.

## Métrica
Partilhas e guardados por alcance; visitas ao perfil. UTM do link: `utm_campaign=LL-MEME01`.

## Ficheiros finais
- Vídeo: `LL-MEME01_a_vida_e_uma_maravilha_916.mp4` e capa `capa.jpg` (quadro 0), entregues ao fundador na conversa de 23/11/2026; não versionados (regra do estúdio).
