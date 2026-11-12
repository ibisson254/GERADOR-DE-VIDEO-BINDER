# VV-EP01 v2 · ficha técnica de produção

| Item | Valor |
|---|---|
| Formato | 1080×1920, 9:16, 30 fps, H.264 + AAC 48 kHz |
| Duração | 40,9 s de episódio + 3,87 s de fecho = 44,77 s |
| Loudness | −14,3 LUFS integrado, pico verdadeiro −1,3 dBTP (loudnorm I=−14, TP=−1,5) |
| Kit visual | `vince/kit/v1/` da branch `vince/kit-v1` (PR #23, **ainda fora da `main`**): `cenario_916.png`, poses `aponta`, `pitch`, `pega_telefone`, `ao_telefone`, `testa`, `bracos`, `confidencia`, `prop_telefone_fora.png`. Nenhum desenho novo. |
| Derivado do kit | `assets/cenario_sem_telefone.png`: o telefone da mesa retirado do `cenario_916.png` para os planos em que está na mão do Vince |
| Carta | `assets/spock535.png`, imagem oficial do Scryfall (`cards/trk/535`), inteira, sem nada por cima |
| Movimento | empurrão de 2 % no 1.º quadro de cada pose nova; contador do painel uma vez (0–0,8 s). Sem respiração, deriva de câmara, sincronia labial, flashes nem efeitos. Piscar: as poses do kit não têm olhos fechados e não se usou |
| Ritmo | 11 planos de 3,0–4,5 s (bíblia §3: 3–6 s) |
| Voz | a da v1 (ElevenLabs `nDJxgaKfMo1DDJJqNg0f`, eleven_v3, flow `1OZhISAeTjWGjnkig55F`, geração `I1pCHshxN0tr5PkoKjHb`), reaproveitada: 11 das 19 frases, reposicionadas. **Zero créditos gastos na v2.** Não versionada |
| Fonte e telefone | `vince/audio/fonte.py` (local): `telefone_toque` (0,62 s), `fonte_ma_noticia`, `telefone_pousa` |
| Música | a faixa da v1, escolhida e enviada pelo fundador (`sweat_on_the_walls.mp3`), preservada; trecho 59,22–104,0 s, com a paragem da bateria no toque do telefone; −20 LUFS sob a voz, ducking durante a chamada, sobe no fecho. Não versionada. **Licença para o Instagram por confirmar** |
| Legenda queimada | uma frase de cada vez, maiúsculas, dentro da zona segura; na carta fica por cima da carta, nunca sobre ela |
| Scripts | `render.py` (planos e painel) · `mistura.py` (voz, Fonte, música, fecho) |
| Recriar | `python3 mistura.py voz --assets <pasta com voz.mp3 e cenario_sem_telefone.png e spock535.png> --fonte vince/audio/saida` → `python3 render.py --kit <vince/kit/v1> --assets <pasta> --saida mudo.mp4` → `python3 mistura.py final … --musica sweat_on_the_walls.mp3 --video mudo.mp4 --fecho comum/outro/outro_binder_916.mp4 --saida final.mp4` |
