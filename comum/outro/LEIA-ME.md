# Fecho de marca BINDER Vision (obrigatório)

Todo vídeo do @binderthetrade termina com este fecho: Mana & Burn, Conde de Manaforte e qualquer Reel novo.
Ele mostra o scanner real do app a funcionar e a assinatura da marca. É a única parte de cada vídeo que vende o produto, por isso nunca sai.

## Ficheiros

| Ficheiro | O que é | Uso |
| --- | --- | --- |
| `outro_binder_916.mp4` | 3,87 s, 1080x1920, 30 fps, **sem áudio**, sem o nome de nenhuma série | Padrão para qualquer série. O áudio vem da trilha do episódio |
| `outro_manaburn_com_audio_916.mp4` | O mesmo trecho com o rótulo "MANA & BURN" e o áudio original do Ep. 5 | Só para o Mana & Burn, quando quiser o fecho exatamente como publicado |
| `scan/000.jpg` … `scan/044.jpg` | 45 quadros (1,5 s) só do scanner | Para o gerador do Mana & Burn (`outro/scan/`) ou para montar um fecho próprio |

Origem: fim do `ManaBurn_Ep5_Knacksaw_916.mp4` (a partir de 43,2 s). Gravação real do Ibisson a escanear uma Iron Man Armor, a 24/10/2026. O nome e o valor de mercado (R$ 15,00) na tela são o que o app leu de verdade.

## Sequência do fecho

1. 0,0–1,3 s: scanner real (câmara, moldura verde, tela de resultado com Confirmar).
2. 1,3–3,4 s: o logótipo cresce, e aparecem "BINDER Vision", "Escaneie suas cartas e organize seus decks." e "Disponível no Google Play · Link na bio".
3. 3,4–3,87 s: fade para preto.

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
