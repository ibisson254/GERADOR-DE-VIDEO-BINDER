# PREGÃO MAGIC · motor de produção (ESP-2026-02)

Reel de mercado sem personagem: a carta é a protagonista. Tudo é gerado localmente (Python + ffmpeg), sem créditos externos.

## Ficheiros

| Ficheiro | Para quê |
|---|---|
| `dados.json` | Preços, versões, períodos, causas, câmbio e fontes. Mudar um número aqui e voltar a renderizar. |
| `render.py` | Quadros 1080×1920 a 30 fps (PIL) em stream para o ffmpeg. Linha do tempo em `T` (grelha da música: B = 0,325 s). |
| `audio.py` | Edita a música fornecida na grelha (drop a 140,085 s; repete 8 compassos) e sintetiza os efeitos (impactos, whooshes, risers, alertas de pregão, contadores, pings, dings). `--voz voz.wav` faz ducking da música sob a narração. |
| `capa.py` | Capa 1080×1920 (zona 3:4 da grelha entre y 240 e 1680). |
| `mux.sh` | Loudnorm em 2 passagens (−14 LUFS, TP −2) + fecho oficial `comum/outro/outro_binder_916.mp4` + AAC. |
| `roteiro.md` | Narração cronometrada, storyboard com timecodes e os match cuts. |

## Recriar

```bash
npm pack geist && mkdir -p /tmp/geist && tar xzf geist-*.tgz -C /tmp/geist   # fontes Geist (OFL), não versionadas
# cartas (Scryfall, só imagem): cartas/<chave>.png e <chave>_art.jpg — ver dados.json → "scryfall"
python3 render.py video.mp4
python3 audio.py musica.mp3 trilha.wav [--voz voz.wav]
OUTRO=../../comum/outro/outro_binder_916.mp4 ./mux.sh video.mp4 trilha.wav PREGAO_MAGIC.mp4
python3 -I ../../comum/qc/qc_video.py PREGAO_MAGIC.mp4 --frente lambe
```

A música (`sweat_on_the_walls.mp3`, enviada pelo fundador a 13/11) e as imagens das cartas não são versionadas; a música está no chat de 13/11 e as cartas recarregam-se do Scryfall (`cartas.sh`).

## Reutilizar noutro pregão

1. Novas cartas e números em `dados.json` e nas chamadas de `bloco_carta(...)` em `render.py`.
2. A função `bloco_carta` já faz a hierarquia: carta → nome → variação → cotação → causa → fonte.
3. Entradas disponíveis: `queda` (cai do topo com tremor), `zoom` (zoom-out) e `match` (mesma posição e escala do plano anterior).
