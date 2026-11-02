# Controlo de qualidade automático

`qc_video.py` mede o ficheiro final antes da entrega (checklist, bloco C). Não altera o vídeo.

```
python3 -I comum/qc/qc_video.py VIDEO.mp4 --frente manaburn   # tubo | conde | orbita | lambe
python3 -I comum/qc/qc_video.py VIDEO.mp4 --sem-fecho          # especial com exceção registada
```

Mede: resolução e fps da frente; duração com e sem o fecho; loudness integrado e pico verdadeiro (alvo −14 LUFS ± 1, pico < −1 dBTP); presença de `comum/outro/outro_binder_916.mp4` no fim (diferença média < 12 em 0–255); cortes com timecode. Gera `qc_<video>/qc.json` e `folha_contacto.png` (1 quadro por segundo, zona segura do Instagram a vermelho).

Classifica P0 (impede publicação), P1, P2. Código de saída 1 quando há P0.

A zona segura (220 px em cima, 380 px em baixo, 140 px à direita) é uma aproximação de trabalho, não especificação do Instagram: em casos limite, conferir no telemóvel.

O que a máquina não vê e tem de ser conferido a olho na folha de contacto: carta inteira (também nos planos em que a TV está ao fundo), texto a tapar fontes, personagens inteiros e no modelo, corte lateral.

Dependências: ffmpeg, numpy, Pillow. Testado a 02/11/2026 no Giro de domingo de 01/11 (ver `nucleo/auditorias/2026-11-02_evolucao_visual.md`).
