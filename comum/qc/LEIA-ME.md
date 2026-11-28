# Controlo de qualidade automático

`qc_video.py` mede o ficheiro final antes da entrega (checklist, bloco C). Não altera o vídeo.

```
python3 -I comum/qc/qc_video.py VIDEO.mp4 --frente manaburn   # tubo | conde | orbita | lambe
python3 -I comum/qc/qc_video.py VIDEO.mp4 --sem-fecho          # especial com exceção registada
```

Mede: resolução e fps da frente; codec (h264/yuv420p) e áudio (AAC); duração com e sem o fecho (TUBO: 25–35 s, regra de 16/11); loudness integrado e pico verdadeiro **com o alvo da frente**; presença de `comum/outro/outro_binder_916.mp4` no fim (diferença média < 12 em 0–255); quadros pretos no corpo (≥ 0,3 s; o preto que entra no fecho é transição e não conta); silêncios no corpo (≥ 1,5 s abaixo de −50 dB, P2 nas frentes com voz/trilha); diferença de duração entre áudio e vídeo (> 0,25 s); cortes com timecode; tamanho do ficheiro. Gera `qc_<video>/qc.json` e `folha_contacto.png` (1 quadro por segundo, zona segura do Instagram a vermelho).

**Alvos de áudio por frente (27/11/2026):** Mana & Burn, TUBO e Conde −14 ± 1 LUFS e pico < −1 dBTP. Lambe-lambe: pico < −6 dBFS (efeitos próprios) e loudness só informativo, porque a música entra no Instagram (`lambe-lambe/CONTEXTO.md`, «Som nos Reels»); a versão muda é aceite. Órbita: sem áudio é o normal. Antes desta data o QC dava um P1 de loudness em todos os vídeos do Lambe-lambe, que era sempre aceite à mão.

Classifica P0 (impede publicação), P1, P2. Código de saída 1 quando há P0.

A zona segura (220 px em cima, 380 px em baixo, 140 px à direita) é uma aproximação de trabalho, não especificação do Instagram: em casos limite, conferir no telemóvel.

O que a máquina não vê e tem de ser conferido a olho na folha de contacto: carta inteira (também nos planos em que a TV está ao fundo), texto a tapar fontes, personagens inteiros e no modelo, corte lateral. **O QC automático nunca substitui a aprovação do fundador nem a revisão editorial** (factos, gancho, ritmo).

## Regressão de imagem (qualquer motor)

Antes de integrar uma alteração a um motor que não deva mudar a imagem: renderizar antes e depois e comparar.

```
python3 -I comum/qc/comparar_videos.py ANTES.mp4 DEPOIS.mp4 [--tol 0] [--audio] [--json r.json]
```

Diz quantos quadros são iguais byte a byte, o pior quadro (píxeis, diferença máxima, PSNR). Sai com 1 se algum quadro passar da tolerância. Atenção: o H.264 espalha uma diferença de 1 nível num píxel por um bloco de ~16×16 nos quadros seguintes; quando falhar por pouco, conferir os quadros compostos antes da codificação (exemplo em `nucleo/auditorias/2026-11-27_motor_producao.md` §C). O TUBO tem o seu próprio `oraculo/motor/mc_render_regressao.py`, que também renderiza.

## Testes

`python3 -I comum/qc/test_qc.py`: 5 testes com vídeos sintéticos (fecho, alvos por frente, pretos, falta de fecho, comparação). Correm no workflow `validar` (~45 s; saltam se não houver ffmpeg).

Dependências: ffmpeg, numpy, Pillow. Testado a 02/11/2026 no Giro de 01/11 e a 27/11/2026 em MC-EP10, MB-EP21 (final e prévia) e LL-ART21 V4.
