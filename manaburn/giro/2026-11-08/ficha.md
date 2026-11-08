# Ficha · Mana & Burn · Giro de domingo nº 2 · semana 02–08/11/2026

Código: `MB-GIRO-2026-11-08`. Pasta: `manaburn/giro/2026-11-08/`. **Produzido, por aprovar, não publicado** (08/11/2026).

## Classificação
- Série: Mana & Burn · formato derivado Giro de domingo (`manaburn/PERFIL.md`)
- Classe: notícia + retrospectiva da casa + chamada
- Complexidade: alta (3 notícias, 3 frentes na retrospectiva, previsão do TUBO)
- Estratégia: verificação rápida com data para as notícias (fonte primária + uma independente); retrospectiva só com publicações confirmadas pelo fundador

## Editorial
- Objetivo: fechar a semana do BINDER Originals e levar o público ao Meta em Curto de segunda (09/11) sem antecipar o resultado.
- Proposta de valor: em pouco mais de um minuto e meio, as três notícias da semana, o que o BINDER publicou e o recado do TUBO.
- Público: jogador casual e de Commander no Brasil.
- Hipótese a testar: a pergunta numérica do Giro ("Comenta 1, 2 ou 3") com as três opções escritas no comentário fixado gera mais respostas por 1.000 views do que o Giro de 01/11 (1 comentário em 838 views).
- Gancho (0–3 s): Burn, "TV SAL, giro de domingo, mano! Três notícias, a semana no BINDER e um recado do TUBO."

## Estrutura (24 falas, 8 canais da TV SAL)
| Bloco | Falas | Canal | Conteúdo |
|---|---|---|---|
| Abertura | 1 | ABERTURA | Giro de domingo, 08/11 |
| A · Plantão | 2–4 | 1 · CINEMA | Maya Hawke no filme de Magic |
| A | 5–9 | 2 · SECRET LAIR | Rise of the Polygons (Extra Life 2026) + "Lê a carta" do Young Pyromancer |
| A | 10 | 3 · PRA JOGAR | Pré-release até 12/11, Arena 10/11, lojas 13/11 |
| B · A semana no BINDER | 11–13 | A SEMANA · CONDE | Conde Ep. 004, Joven: "obra notável" |
| B | 14–16 | A SEMANA · BURN FOI ASSIMILADO | a carta dos Borg não mata Borg ("Isso devia ser banido!") |
| B | 17–18 | A SEMANA · META EM CURTO | EP05: Enterprise-A 3,8%; recorde com impulsionamento pago |
| C · O TUBO volta segunda | 19–22 | RECADO DO TUBO | previsão do EP05, palavra por palavra; prestação de contas a 09/11 |
| D · Veredito e fecho | 23–24 | (mesmo) | "Comenta 1, 2 ou 3" → "Comenta aí." → TV desliga → fecho do scanner |

## Retrospectiva: o que entrou e porquê
| Frente | Episódio | Publicação | Material na TV |
|---|---|---|---|
| Conde de Manaforte | Ep. 004 Joven (`conde/episodios/ep004_joven_ficha.md`) | confirmada pelo fundador a 08/11 (data exata por confirmar) | quadro real a 46,2 s, renderizado por `conde/montar_ep004.py --preview` (sem áudio) |
| Mana & Burn | Especial "Burn foi assimilado!" (branch `especial-startrek-prerelease`) | confirmada pelo fundador a 08/11 (data exata por confirmar) | quadro real a 63,5 s, renderizado pelo kit da branch com o `episode.js`/`data.js` do especial |
| Meta em Curto | EP05 Star Trek (branch `meta-em-curto-ep05`) | quinta, 05/11 (fundador); 5.334 visualizações com impulsionamento pago | quadros reais a 2,6 s e 81,6 s, renderizados por `ep05_render.py`; linha do tempo refeita a partir de `ep05_words.json` (desvio ≤ 0,14 s; o LED não pisca porque o envelope do áudio não está no repositório) |

Fora da retrospectiva por não haver publicação confirmada: Especial "Precon em jogo", Meta em Curto EP03 e EP04, Mana & Burn Ep. 10, carrosséis de 06/11.

## Fontes e evidências
Ver `ficha_fontes.md`.

## Produção
- Motor: kit v2 de `manaburn/` em `main` (sala v3 e luz no cenário, decisões de 07 e 08/11), sem alterar código. Motor de canais (`EP.canais`). O motor do Giro de 01/11 (branch `giro/2026-11-01`, cena v1) não foi usado porque é anterior à sala v3 e à luz aprovada.
- Planos: `tv`, `tv2`, `tvtext`, `wide`, `cuM`; sem `push` nem `cuB`.
- Telas tipográficas: `telas_giro.py` (TV SAL: abertura, cinema, pré-release). Carta real: Young Pyromancer (Magic 2014, nº 163), PNG do Scryfall; destaque medido nas linhas do texto.
- Vozes: ElevenLabs eleven_v4, flow "Mana & Burn — Giro de domingo 08/11/2026" (`gBn9kgrx6Gf3cgGdSSws`). Burn: Talis (`E9a8LlXPNWtyvvSoZzrb`), 1.017 créditos. Mana: Erik (`nfiLpQ54jEQninp3nNqL`), 1.183 créditos. 1 geração cada; total 2.200 de 2.500 autorizados (fundador, 08/11, 00:10). Transcrição Scribe das duas faixas: 0 créditos.
- Corte: as `[long pause]` saíram curtas (~0,3 s) e o `cortes.py` trocou as fronteiras de três falas do Burn. `separar_falas.py` acrescenta 0,7 s de silêncio nas fronteiras certas (transcrição + silêncio real) antes do `process.py`; a voz não muda.
- Música: midnight_throttle (`manaburn/musica.mp3`). Fecho: `comum/outro/outro_binder_916.mp4` por `juntar_fecho.py` (cópia do Ep. 10).
- Easter egg: nenhum.

## Riscos e limitações
- Pronúncia: Scribe repete a grafia do prompt, por isso não prova a pronúncia. Ouvir: "Maya Hawke", "Stranger Things", "Matt Johnson", "BlackBerry", "Secret Lair", "Rise of the Polygons", "Young Pyromancer", "Joven", "Borg", "Enterprise-A", "Rakdos", "Sealed", "BINDER".
- Chamada do Bloco C: o critério da previsão é o 17Lands até 01/12; o Star Trek só chega ao MTG Arena a 10/11, por isso na segunda (09/11) ainda não há dados de Sealed do 17Lands. A fala diz só que o TUBO "volta pra prestar contas"; o formato do episódio de segunda é decisão do fundador.
- "Mais visto do canal": confirmado pelo fundador (5.334 visualizações); o vídeo diz que houve impulsionamento pago. Valor investido e divisão orgânico/pago: por confirmar.
- Licença comercial das vozes: depende do plano ElevenLabs ativo a 08/11 (não verificável por esta ligação).

## Entregáveis
- [x] Vídeo · [x] Capa · [x] Legenda · [x] Comentário fixado · [x] Texto alternativo · [x] Fontes

## Depois de publicar
- Métrica principal: respostas "1/2/3" por 1.000 views. Secundária: partilhas.
- Publicação: (data, hora) · Resultado observado: —

## Controlo de qualidade (ficheiro final `ManaBurn_Giro_2026-11-08_916.mp4`, 08/11/2026)
| Critério | Alvo | Medido | OK |
|---|---|---|---|
| Formato | 1080×1920, 30 fps, H.264 + AAC 48 kHz | 1080×1920, 30/1, h264 + aac 48000 Hz | sim |
| Duração | pela história | 103,0 s (99,13 s + fecho de 3,87 s) | sim |
| Loudness / pico | −14 LUFS, < −1 dBTP | −14,3 LUFS, −2,6 dBTP (1.º render deu −0,8 dBTP; corrigido com limitador) | sim |
| `qc_video.py --frente manaburn` | sem problemas | "Sem problemas mensuráveis"; fecho a partir de 99,13 s | sim |
| cropdetect 24:2:0 | 1080:1920:0:0 | 3085/3085 quadros | sim |
| `bordas.py` | OK | 1607 quadros de TV, laterais 10–1068 px, topo ≥ 300 px | sim |
| Textos da TV SAL | legíveis, sem corte | 1.º render cortava a conta do medidor e "OBRA NOTÁVEL"; textos encurtados e re-renderizado; conferido nos quadros 22, 31, 50, 58, 70,5 e 82 s | sim |
| Carta inteira e destaque | Young Pyromancer | carta inteira; destaques sobre as 3 linhas do texto (31 s) | sim |
| Legenda queimada | zona segura, sem tapar a carta | conferida na folha de contacto; na fala 20 (4 linhas) o plano passou de `tv2` para `tv` para não tapar o medidor | sim |
| Sincronia das falas | fronteiras certas | cortes conferidos contra a transcrição Scribe (24 falas) | sim |
| Bordões | intactos | "Lê a carta", "Isso devia ser banido!", "Comenta aí" | sim |
| Fim | TV desliga → ponto verde → scanner → logo | 98,6 / 99,1 / 101,5 s | sim |
| Pronúncia | ouvida | **não ouvida** (Scribe repete a grafia do prompt) | P1 a confirmar pelo fundador |
| Afirmações | todas com fonte | `ficha_fontes.md`; previsão do TUBO citada palavra por palavra | sim |
