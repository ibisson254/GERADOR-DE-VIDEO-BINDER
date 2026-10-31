# Fecho de marca BINDER Vision (obrigatório)

Todo vídeo das séries e do Lambe-lambe termina com este fecho (o Órbita não; ver constituição §6).
Ele mostra o scanner real do app a funcionar e a assinatura da marca. É a única parte de cada vídeo que vende o produto, por isso nunca sai.

## Ficheiros

| Ficheiro | O que é | Uso |
| --- | --- | --- |
| `outro_binder_916.mp4` | 3,87 s (116 quadros), 1080x1920, 30 fps, H.264, **sem áudio**, sem o nome de nenhuma série | Padrão para qualquer frente com fecho. O áudio vem da trilha do episódio |
| `gerar_fecho.py` | Script que gerou o `outro_binder_916.mp4` a partir do fim de um Reel do Mana & Burn | Refazer o fecho a partir de outro Reel (ex.: com uma gravação nova do scanner) |
| `scan/000.jpg` … `scan/044.jpg` | 45 quadros (1,5 s) só do scanner | Para o gerador do Mana & Burn (`outro/scan/`) ou para montar um fecho próprio |

Origem (31/10/2026): fim do `ManaBurn_Ep6_GodPack_916.mp4` publicado, enviado pelo Ibisson, a partir de 49,0 s (quadro escuro antes do scanner) até ao fim (52,87 s). O rótulo "MANA & BURN" que aparece por cima da logo foi tapado com a cor do fundo liso (#050A10) em cada quadro da fase da logo; scanner, ponto verde, logo e textos não foram mexidos. Comando: `python3 -I gerar_fecho.py ManaBurn_Ep6_GodPack_916.mp4 49.0 pasta_trabalho outro_binder_916.mp4`. Conferido: 1080x1920, 116 quadros, sem áudio, cropdetect 1080:1920:0:0, nenhum resto do rótulo.

A gravação é real: o Ibisson a escanear uma Iron Man Armor, a 24/10/2026 (a mesma do fecho do Ep. 5). O nome e o valor de mercado (R$ 15,00) na tela são o que o app leu de verdade.

O `outro_manaburn_com_audio_916.mp4` citado em versões anteriores deste ficheiro nunca chegou ao repositório; para o fecho com rótulo e áudio do Mana & Burn, cortar o fim de um Reel publicado da série.

## Sequência do fecho

Medida no ficheiro (31/10/2026):

1. 0,0–1,5 s: scanner real (câmara, moldura verde, tela de resultado com Confirmar).
2. 1,5–1,75 s: ponto branco que fica verde.
3. 1,75–3,6 s: o logótipo nasce do ponto a girar, e aparecem "BINDER Vision", "Escaneie suas cartas e organize seus decks." e "Disponível no Google Play · Link na bio".
4. 3,6–3,87 s: fade para preto.

## Regras

- Sempre no fim, depois da última fala ou do carimbo. Nunca no meio do vídeo.
- Corte seco ou transição de 0,2 s. O fecho não é encurtado nem acelerado.
- Na trilha, a música sobe no fecho (sem narração por cima) e termina com o fade.
- Nunca redesenhar a tela do app, nem trocar a carta ou o valor dentro dela.
- Para mostrar a carta do episódio no scanner, gravar o app a ler essa carta de verdade e substituir os quadros de `scan/`.
- Conferir o enquadramento antes de entregar: o fecho é 9:16 nativo e não pode ter corte lateral.

## Como juntar ao vídeo (ffmpeg)

```
ffmpeg -i episodio.mp4 -i comum/outro/outro_binder_916.mp4 \
  -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0[v]" -map "[v]" -map 0:a ...
```

O áudio do episódio tem de cobrir também os 3,87 s do fecho (música sem voz).
