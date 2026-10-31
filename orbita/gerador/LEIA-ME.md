# Gerador do Órbita

Código copiado sem alterações do projeto claude.ai (`claude/gerador/`) a 31/10/2026. Cadeia de imports conferida: os 23 posts carregam e as páginas de 1, 4 e 5 cartas montam.

## Ficheiros

| Ficheiro | Função |
|---|---|
| `paint.js` | Pintura generativa do quadro (uma semente por peça) |
| `anim.js` | Camada em movimento: discos em órbita, anéis, arco tracejado, película fixa |
| `build.py` | Fontes (`FONTS`) e o gerador da v1 em slides (só as fontes são usadas pelos seguintes) |
| `build2.py` | Página de cada peça e os posts 1–10 (`POSTS`) |
| `build3.py` | Paletas vivas (`V`, `VIVID`) |
| `build4.py` | Render do Reel 4:5, 12 s, loop (frames + ffmpeg) e capa |
| `batch2.py` … `batch5.py` | Lotes 2 a 5 (Reels 11–22 e "Problema de colecionador"); cada lote importa os anteriores |

## Como rodar

```
cd orbita/gerador
python3 build4.py 01-kirk-autografo --preview   # 4 quadros num mosaico, para conferir
python3 build4.py 01-kirk-autografo             # Reel completo em out4/
python3 batch4.py 21-constelacao-comandantes     # peças de um lote
```

Precisa de Python 3 com `playwright` (Chromium) e `Pillow`, e de `ffmpeg`. Render: cerca de 9 min por vídeo.

## O que falta no repositório para renderizar

- `cards/`: PNGs das cartas, normalizados a 976×1360 com cantos arredondados (`kirk_1701.png`, `q_0383.png`…). Estão no ZIP `BINDER_gerador_orbita.zip` entregue no chat de 22/10, segundo o índice do Drive.
- `node_modules/` com as fontes: `@fontsource/jost` (500, 600, 700), `@fontsource/cormorant-garamond` (500 e 600 itálico) e `geist` (Medium e Bold). Instalar com `npm install @fontsource/jost @fontsource/cormorant-garamond geist` dentro desta pasta.
- `batch5.py`: preencher `CONFIG` (número e artista do rodapé) antes de renderizar.

As pastas de saída (`out*/`, `html*/`, `frames*/`) não são versionadas.
