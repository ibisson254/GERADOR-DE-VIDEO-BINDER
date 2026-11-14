# Motor do Pregão Magic (formato sem personagem)

Composição 100% por código: canvas 1080×1920 desenhado quadro a quadro no Chromium (Playwright), som sintetizado em Python, montagem e mistura em FFmpeg. Zero créditos de serviços externos; nenhuma imagem gerada. Criado para o VV-PG01 (14/11/2026) e pensado para os próximos pregões: muda-se `dados.js` (cartas, números, fontes, marcas musicais) e o desenho das cenas em `pregao.js`.

## Ficheiros

| Ficheiro | O que faz |
|---|---|
| `pregao.html` | página do canvas; fontes Inter Display locais |
| `dados.js` | **dados do episódio**: cotações, fontes, câmbio, marcas musicais, cartas da parede e do leque |
| `pregao.js` | componentes (`carta`, `molduraCarta`, `etiqueta`, `preco`, `pctGrande`, `linhaFonte`, `rotulo`, `tremor`, `flash`, painel de fecho) e as cenas por tempo (`CENAS`); `render(t)` desenha o quadro t; `render(-1)` desenha a capa |
| `render.py` | `quadros t1 t2…` (PNG de inspeção) ou `video saida.mp4 [t_fim]` (sem áudio) |
| `som.py` | stems (música, efeitos, voz) e `mix.wav` a −14 LUFS / −1,5 dBTP; ducking automático se houver `voz.wav` |
| `montar.py` | junta o episódio ao fecho oficial e à mistura |
| `analise_musica.py` | BPM, batidas, energia por meio segundo e onsets mais fortes (base do `MUSIC_MAP.md`) |
| `cartas.py` | descarrega do Scryfall as imagens oficiais das cartas (só imagem e dados) |

## Refazer o VV-PG01

```
cd vince/pregao/motor
python3 -I cartas.py ../cartas                      # imagens (pasta não versionada)
python3 render.py video ../saida/ep01_sem_audio.mp4 # ~6 min
python3 som.py "Auction_of_Power.mp3" ../saida [voz.wav]
python3 montar.py ../saida/ep01_sem_audio.mp4 ../saida/mix.wav ../../../comum/outro/outro_binder_916.mp4 ../saida/PregaoMagic_EP01_916.mp4
python3 -I ../../../comum/qc/qc_video.py ../saida/PregaoMagic_EP01_916.mp4 --frente manaburn
```

`dados.js` espera as cartas em `../cartas/` (relativo ao HTML). A faixa "Auction of Power" é do fundador (ElevenLabs Music) e não está no repositório.

Dependências: Python 3, `playwright` (Chromium), `numpy`, `scipy`, `librosa` (só para a análise), FFmpeg, fontes Inter Display instaladas.

## Regras do motor

- Cartas sempre inteiras e sem recolor (`carta()` desenha a imagem completa; o motion blur é por amostras sobrepostas da mesma imagem).
- Todo o plano com número chama `linhaFonte()` (28 px, dentro da zona segura).
- Escalas de gráfico com zero na base; pontos calculados vêm marcados "(calculado)".
- Nenhum número provisório no ecrã: na tensão antes de um drop usa-se "+ ? ? %", nunca dígitos aleatórios.
- Texto dentro de x 70–930 e y 220–1540 (zona segura de `comum/qc/qc_video.py`).
