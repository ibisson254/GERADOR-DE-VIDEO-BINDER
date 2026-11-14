# Expedição BINDER · motor (template reutilizável)

Bíblia do formato: `../BIBLIA.md`. Este motor não reescreve o gerador das séries: usa o mesmo padrão dos episódios do TUBO (PIL + numpy + ffmpeg, voz ElevenLabs, tempos por palavra do Scribe, fecho real do scanner).

## Ficheiros
| Ficheiro | Faz |
|---|---|
| `audio.py` | Cortes por palavra (fronteira no ponto de menor energia), pausas, tempo com `rubberband`, tema a −22 LUFS com ducking, assinatura sonora sintetizada (ping, bolhas, whoosh), mistura final −14 LUFS / pico < −1 dBTP. Gera `tl.json` (tempos finais de cada palavra e de cada evento) |
| `linha_tempo.py` | Converte os blocos do `episode.json` (presos a índices de palavra) em eventos com tempo |
| `render.py` | Cena «oceano» (fundo por camada, raios, partículas, medidor, ficha, legenda palavra a palavra, logótipo) e os oito movimentos; abertura, pagamento e fecho; junta o fecho de marca; capas A e B; prévias em quadros parados |
| `baixar_cartas.py` | Descarrega os PNG do Scryfall listados em `cards/creditos.json` |

## Episódio novo (um set novo)
1. Copiar `01-nauctis/` para `NN-<set>/` e limpar `audio/`, `cards/`, `products/`, `broll/`.
2. Verificar factos (BIBLIA §6) e escrever o roteiro; gerar a voz (uma tomada) e o Scribe (alinhamento ao texto, 0 créditos) → `audio/words.json` sem as tags `[...]`.
3. Preencher `episode.json`: `voz.cortes`/`voz.pausas` (índices de palavra), `legenda.amarelo`/`trocas`, `camadas`, `caixas` (imagem oficial + `ret_subtitulo` em px da imagem), `blocos` (cada `w` é o índice da palavra que dispara o corte; retângulos de punch-in em px do PNG 745×1040 do Scryfall).
4. `python3 -I template/baixar_cartas.py NN-<set>` (depois de escrever `cards/creditos.json`).
5. Numa pasta de trabalho com `voz.mp3`:
   ```
   python3 -I template/audio.py  NN-<set> <trabalho>
   python3 -I template/render.py NN-<set> <trabalho> stills 0 3 10 20   # prévias
   python3 -I template/render.py NN-<set> <trabalho>                     # vídeo (PARTES=n para paralelizar)
   python3 -I template/render.py NN-<set> <trabalho> capas
   python3 -I ../comum/qc/qc_video.py --frente lambe <trabalho>/<ficheiro>.mp4
   ```
   (correr a partir de `expedicao/`; `-I` isola os imports, por isso `audio.py` acrescenta a própria pasta ao caminho.)

## Limites conhecidos
- Sem as caixas oficiais em `products/`, o render mostra cartões «PRÉVIA · NÃO PUBLICAR» e a abertura/o fecho usam cartas em vez da fila de caixas. O episódio não é publicável assim.
- B-roll: suportado na bíblia, ainda não implementado no motor (o EX-01 saiu sem B-roll porque os bancos não abrem nesta rede).
- Requisitos: Python 3, Pillow, numpy, pyloudnorm, ffmpeg com `rubberband`, fontes Inter em `/usr/share/fonts/opentype/inter/`.
