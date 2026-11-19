# Prova de estilo · Lisa de recorte (19/11/2026)

Teste de **custo zero** pedido pelo fundador depois de duas tentativas de personagem caras e com qualidade fraca. A pergunta a responder é se o estilo «motion comic» (recorte 2D + boca automática) serve para a Lisa **antes** de encomendar arte definitiva.

**Não é personagem-mestre nem episódio.** Usa o look 1 da prancha (conceito, 262×513 px ampliado), bocas e pálpebras desenhadas por código e uma voz sintética provisória. Não tem ID nem pauta e não se publica.

## Linha proposta (por decidir pelo fundador)

1. Arte desenhada **uma vez** por uma ilustradora: PSD em camadas, com corpo, 2–3 braços, olhos a piscar e as 6 bocas A–F do Rhubarb. Ideia: a ilustradora é a primeira convidada de `Elas no Multiverso`.
2. Boca automática a partir da voz com o **Rhubarb Lip Sync** (MIT, local), com reconhecedor `phonetic`, que funciona em português.
3. Montagem neste motor: piscar, respiração, balanço com a voz, cortes VJ ≤ 3 s, tarja e bug do kit.
4. Custo por episódio: só a voz.

Limite assumido: o movimento é de recorte, não de anime fluido.

## Reproduzir

Ferramentas locais, nenhuma versionada:
- Rhubarb Lip Sync 1.14.0 (Linux): release no GitHub `DanielSWolf/rhubarb-lip-sync`.
- `pip install "rembg[cpu]" opencv-contrib-python-headless piper-tts`. O modelo `isnet-anime.onnx` vem da release `v0.0.0` de `danielgatis/rembg`, em `~/.u2net/`.
- Voz provisória: Piper `voice-pt-br-edresson-low` (release `v0.0.2` de `rhasspy/piper`), voz masculina com o tom subido. Só serve para o teste. **Não é a voz da Lisa.**

```bash
python3 recortar.py                                   # look1_recorte_4x.png
python3 -m piper -m pt-br-edresson-low.onnx -f fala_raw.wav < fala.txt
ffmpeg -i fala_raw.wav -af "aresample=44100,rubberband=pitch=1.42:pitchq=quality,highpass=f=140,loudnorm=I=-16:TP=-1.5" fala.wav
rhubarb -r phonetic -f json --dialogFile fala.txt -o boca.json fala.wav
python3 camadas.py                                    # lisa_base.png, bocas/, palpebra_*.png
rsvg-convert -w 1080 -h 1920 fundo.svg -o fundo.png   # estudio_base.svg sem as 2 linhas de texto
rsvg-convert -w 1080 tarja.svg -o tarja.png           # tarja_vj.svg com «LISA MARIE / VJ DO MULTIVERSO»
rsvg-convert -w 360 ../identidade/bug_programa.svg -o bug.png
python3 motor_recorte.py                              # prova_lisa_recorte.mp4 (não versionar)
```

Resultado de 19/11: 5,8 s, 1080×1920, 30 fps, −15,6 LUFS. Vídeo entregue na conversa, não versionado.

## Defeitos conhecidos (são da prova, não do método)

- A arte ampliada 4× a partir de 262 px fica mole no grande plano. A arte definitiva tem de vir em alta resolução.
- As bocas e as pálpebras são vetoriais e não seguem o traço da ilustração. O olho fechado é uma elipse preta.
- Recorte com serrilhado e algum papel da prancha limpo à mão (`camadas.py`, passo 1).
- O fundo vetorial do kit e a personagem ilustrada não combinam no estilo.
