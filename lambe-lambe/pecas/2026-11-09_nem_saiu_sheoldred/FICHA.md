# Lambe-lambe · "Nem saiu e já tem preço" (Sheoldred, versão Khan)

Produzido a 09/11/2026 (pedido do fundador: crítica à especulação de cartas, vídeo rápido e enérgico, com a referência de anúncio da Artoto). **Por publicar.** Versão atual: v2 (logo em lambe-lambe). O vídeo não está no repositório: recria-se com os passos abaixo.

## Ficha

| Campo | Valor |
|---|---|
| Frente | Lambe-lambe (espontâneo), Reel 9:16 |
| Classe | Mercado/preço + conteúdo promocional do app |
| Proposta de valor | Antes de comprar no hype, veja quanto vale a sua coleção. |
| Ação única | Baixar a beta para Android (link na bio) |
| Duração | 10,53 s + fecho de 3,87 s = 14,40 s |
| QC | `qc_video.py --frente lambe`: sem problemas mensuráveis (−14,9 LUFS, pico −2,0 dBTP, fecho presente) |
| Easter egg | 0 |

## Ângulo e decisão

Proposta inicial: "mesma carta, outra cara, outro preço". Foi descartada depois da pesquisa, porque a versão Khan (US$ 74,99) é **mais barata** do que a comum (US$ 109,99), e a comparação sairia falsa. Ficou o ângulo verdadeiro: a carta ainda não chegou às lojas (lançamento a 13/11/2026) e já tem um valor de referência de R$ 396,42 no app.

## Estrutura

| Tempo | Cena | Texto na tela |
|---|---|---|
| 0–2,55 s | Muro rosa: 8 cartazes do hype colados a cada 0,22 s ("VAI SUBIR!", "COMPRA ANTES QUE ACABE", "PRÉ-VENDA", "R$ ???", "HYPE", "CONFIA NO PAI", "INVESTIMENTO GARANTIDO *só que não", "↑↑↑") | "Essa Sheoldred nem chegou às lojas…" |
| 2,55–4,55 s | Cartaz amarelo "SHEOLDRED · VERSÃO KHAN": o gráfico a marcador sobe, leva o carimbo "NEM LANÇOU" e rasga o topo | "…e já tem preço: R$ 396,42." · "Lança só dia 13/11." · "valor de referência no BINDER Vision, 09/11/2026" |
| 4,55–5,45 s | Três cartazes pretos BINDER com a logo impressa são colados por cima do hype (0,25 s cada, cola molhada que seca) | — |
| 5,45–8,45 s | Cartaz preto BINDER com a gravação real recortada; selo "TELA REAL DO APP" | "Antes do hype, veja quanto vale a sua coleção." · "Valor de referência no app · 09/11/2026 · estimativa" |
| 8,45–10,53 s | Campanha de lambe-lambe: seis cartazes pretos "BINDER Vision" iguais colados em grelha por cima do muro | "Carta é pra jogar." · "Não pra especular." |
| 10,53–14,40 s | Fecho `comum/outro/outro_binder_916.mp4`, sem cortes | — |

## Material real

- Gravação de tela enviada pelo Ibisson a 09/11/2026 (16,2 s, 1080×2400). Trechos usados, sem acelerar: 9,00–9,38 s (patrimônio R$ 1.544,40, já sem teclado), 9,60–10,75 s (Sheoldred · Stardates, valor de mercado R$ 396,42, Confirmar) e 10,80–11,90 s (patrimônio R$ 1.940,82 com a carta no Binder). Só saíram a digitação da pesquisa e o aviso do gravador. Na tela, recorte vertical de 150 a 1900 px (enquadramento, sem redesenho).
- Logo do BINDER (PNG enviado a 09/11/2026), com as cores originais #3FEA8C e #22A160. Entra sempre impressa em cartaz preto de lambe-lambe (grão, falhas de tinta, leve desacerto de registo, fita nos cantos de cima), nunca solta por cima do vídeo (pedido do fundador, 09/11/2026: a logo a girar parecia não fazer parte do vídeo). O texto da marca usa #10B981.

## Recriar

```
ffmpeg -i GRAVACAO.mp4 -filter_complex "[0:v]trim=9.0:9.38,setpts=PTS-STARTPTS[a];[0:v]trim=9.6:10.75,setpts=PTS-STARTPTS[b];[0:v]trim=10.8:11.9,setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0,fps=30" recorte_app.mp4
mkdir rec_frames && ffmpeg -i recorte_app.mp4 -vf "crop=1080:1750:0:150,scale=648:1050" rec_frames/%03d.png
cp logo_binder.png logo.png
python3 -I build.py .                      # corpo.mp4 (10,53 s)
python3 -I audio.py trilha.wav 14.42
ffmpeg -i trilha.wav -af "volume=18dB,alimiter=limit=0.7:attack=2:release=80:level=disabled" t.wav
ffmpeg -i corpo.mp4 -i ../../../comum/outro/outro_binder_916.mp4 -i t.wav -filter_complex "[0:v]fps=30,format=yuv420p,setsar=1[a];[1:v]fps=30,format=yuv420p,setsar=1[b];[a][b]concat=n=2:v=1:a=0[v]" -map "[v]" -map 2:a -c:v libx264 -crf 18 -c:a aac -b:a 192k -shortest Lambe_NemSaiu_Sheoldred_916.mp4
```

O som é todo sintetizado (batida a 128 BPM, colagens, fita, rasgo e clique), sem música de terceiros.

## Ficha de fatos (consultada a 09/11/2026)

| Facto | Fonte |
|---|---|
| A Sheoldred, the Apocalypse aparece no bonus sheet *Stardates* (SDS #11) como "Khan, Engineered Evil", ilustrada por Nicky Barkla | Scryfall, página SDS #11 (só dados de carta, nenhum preço) |
| O *Stardates* lança a 13/11/2026, com o set *Star Trek* | Wizards ("Collecting Star Trek"), mtg.wiki |
| Sai 1 carta Stardates a cada 25 Play Boosters | Draftsim, TurnZero |
| Não é legal em Standard; é legal em Pioneer, Modern, Legacy, Vintage e Commander, entre outros | Scryfall (legalidades), Draftsim |
| Card Kingdom, NM: versão Khan US$ 74,99; Dominaria United comum US$ 109,99 | cardkingdom.com, 09/11/2026 |
| Valor de referência no app: R$ 396,42 (versão Khan) | Gravação real do BINDER Vision, 09/11/2026, estimativa, não oferta de compra |

## Legenda (fórmula v3)

```
Ninguém abriu um booster de Star Trek ainda, e essa carta já tem preço.

A Sheoldred, the Apocalypse ganhou uma versão "Khan, Engineered Evil" no Stardates, a folha bônus de Magic: The Gathering | Star Trek. O lançamento é só no dia 13/11. Mesmo assim, no dia 09/11 ela já aparecia com valor de referência de R$ 396,42 no BINDER Vision.

O detalhe: a versão Khan não é legal no Standard. Ela joga onde a Sheoldred já jogava (Pioneer, Modern, Commander). E, na Card Kingdom, a versão comum de Dominaria United ainda custa mais: US$ 109,99 contra US$ 74,99 da Khan (09/11/2026).

Carta é pra jogar. Antes de comprar no hype, confira quanto vale o que você já tem.

Fontes: Wizards of the Coast, Card Kingdom e Scryfall (dados de carta), consultados em 09/11/2026. Arte: Nicky Barkla. © Wizards of the Coast. Star Trek e personagens licenciados aos respectivos titulares. Conteúdo de fã não oficial. Gravação real do app; valor de referência é estimativa, não oferta de compra.

No Binder do BINDER Vision, cada carta adicionada entra no valor de referência da sua coleção.

Baixe o BINDER Vision no Android: link na bio.

#mtg #magicthegathering #mtgstartrek #mtgbrasil #binderthetrade
```

## Comentário fixado

```
Você compraria uma carta antes de ela chegar às lojas? Sim ou não?
A versão Khan da Sheoldred sai no dia 13/11 e sai 1 Stardates a cada 25 Play Boosters.
```

## Texto alternativo

Reel em muro rosa de lambe-lambe. Vão sendo colados cartazes pop com "VAI SUBIR!", "COMPRA ANTES QUE ACABE", "PRÉ-VENDA", "HYPE" e "INVESTIMENTO GARANTIDO *só que não". O texto diz: "Essa Sheoldred nem chegou às lojas… e já tem preço: R$ 396,42. Lança só dia 13/11." Um cartaz amarelo mostra um gráfico a subir com o carimbo "NEM LANÇOU" e rasga. Cartazes pretos com a logo verde do BINDER são colados por cima. Num cartaz preto aparece a gravação real do app: a Sheoldred versão Khan com valor de mercado de R$ 396,42, e o patrimônio a subir de R$ 1.544,40 para R$ 1.940,82. Texto: "Antes do hype, veja quanto vale a sua coleção." No fim, seis cartazes pretos "BINDER Vision" colados lado a lado no muro e o texto "Carta é pra jogar. Não pra especular.", seguidos do fecho do scanner do BINDER Vision.

## Pendências antes de publicar

- O fundador ouve e vê o vídeo e decide se publica. A data do valor (09/11) fica na tela e na legenda; se o post sair depois de 13/11, a frase "nem chegou às lojas" deixa de ser verdade e é preciso refazer.
- O fundador confirma se a música fica a batida sintetizada ou se troca por música escolhida no Instagram (a bíblia prevê esta segunda; a batida existe para cumprir os −14 LUFS do QC).
