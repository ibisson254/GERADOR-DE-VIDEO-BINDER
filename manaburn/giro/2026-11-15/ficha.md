# Ficha · Mana & Burn · Giro de domingo nº 3 · semana 09–15/11/2026

Código: `MB-GIRO03`. Pasta: `manaburn/giro/2026-11-15/`. **Produzido, não publicado** (15/11/2026). Pedido do fundador (01:58): «Faça o episódio de giro da semana e inclua Burger King e outros temas da semana»; às 02:07: «Faltou falar dos episódios da semana que tivemos».

## Classificação
- Série: Mana & Burn · formato derivado Giro de domingo (`manaburn/PERFIL.md`)
- Classe: notícia + retrospectiva da casa + chamada
- Complexidade: alta (3 notícias, 6 conteúdos na retrospectiva, previsão do TUBO)
- Estratégia: verificação rápida com data (fonte primária + uma independente); retrospectiva só com publicações confirmadas pelo fundador (15/11, 02:10)
- Originalidade: `memoria.py pauta` livre para Burger King, Chandra/PLANESWALKER e Numot. Star Trek nas lojas ficou de fora (pauta bloqueada: MB-ESP03, MC-EP05, LL-PRETRK).

## Editorial
- Objetivo: fechar a semana com duas notícias que o jogador casual comenta (lanche de Magic, série na Netflix), mostrar o que o BINDER publicou e levar ao Meta em Curto de segunda sem antecipar o Top 8.
- Público: jogador casual e de Commander no Brasil.
- Hipótese a testar: notícia de cultura pop fora da mesa (fast food, streaming) gera mais respostas «1/2/3» por 1.000 views do que o Giro nº 2.
- Gancho (0–3 s): Burn, «Giro de domingo, mano! Magic no Burger King, na Netflix e a semana no BINDER.»

## Roteiro definitivo (24 falas, `episode.json`)
| Bloco | Falas | Canal da TV SAL | Conteúdo |
|---|---|---|---|
| Abertura | 1 | ABERTURA | Giro de domingo, 15/11 |
| 1 · Lanche | 2–6 | 1 · LANCHE | Burger King Itália: €19,90, deck box + 100 sleeves, só na Itália até 30/11; Rosewater: «pode expandir, nada decidido» |
| 2 · Streaming | 7–11 | 2 · STREAMING → 2 · LÊ A CARTA | PLANESWALKER (Netflix, 2027, Chandra); «Lê a carta» do −3 da Chandra (uma criatura só); «Isso devia ser banido!» |
| A semana no BINDER | 12–20 | MANA & BURN · CONDE · META EM CURTO · EXPEDIÇÃO | Numot (Lê a carta: paga {2}{R}, até dois terrenos); Conde EP005 (obra notável, errou de mitologia); TUBO: EP07 + ESP01 + ESP02 (66% para quem começa); Expedição Nauctis (um Lotus no fundo) |
| 3 · Mundial | 21–22 | 3 · MUNDIAL | Mundial 32 termina hoje; TUBO cravou Jund Sacrifice; presta contas amanhã, sem spoiler |
| Fecho | 23–24 | — | «Comenta 1, 2 ou 3» → «Comenta aí.» → TV desliga → fecho do scanner |

Cortes feitos para caber no orçamento de créditos (fundador, 02:22, «Corta para caber em 1.700»): saíram a carne seca de Magic (Mythical Meats), o Terry Matalas na fala (fica na tela) e o «Top 8 saiu ontem».

## Fontes e evidências
Ver `fontes.md`.

## Produção
- Motor: kit v2 de `manaburn/` (sala v3, luz no cenário), sem alterar código. Motor de canais (`EP.canais`), 9 canais. Planos `tv`, `tv2`, `tvtext`, `wide`, `cuM`; sem `push` nem `cuB`.
- Telas tipográficas: `telas_giro.py`. Cartas reais: Chandra, Torch of Defiance (KLD 110) e Numot, the Devastator (CMD 215), PNG do Scryfall; destaques medidos nas linhas do texto. Retrospectiva do Conde: recorte da capa real do EP005.
- Vozes: ElevenLabs eleven_v4, flow `xiCL5Tg0uv0l1swiXKMd`. Burn: Talis (`E9a8LlXPNWtyvvSoZzrb`), 852 créditos. Mana: Erik (`nfiLpQ54jEQninp3nNqL`), 845 créditos. 1 geração cada; total 1.697 de 1.700 autorizados (fundador, 02:03 e 02:22).
- Música: midnight_throttle (`manaburn/musica.mp3`). Fecho: `comum/outro/outro_binder_916.mp4` por `juntar_fecho.py`.
- Revisão interna: no 1.º render a fala do Lotus estava em `cuM` e a tela da Expedição quase não aparecia; passou para `tv2` e foi re-renderizado.
- Capa: `MB_GIRO03_CAPA.png` no modelo fixo (carta da Chandra; frase «MAGIC NO BURGER KING», foco «E NA NETFLIX», selo «€19,90 · SÓ NA ITÁLIA», faixa «MANA & BURN · GIRO DE DOMINGO · 15/11»). O foco tem 3 palavras (o perfil pede 1): a pedir confirmação ao fundador.
- Easter egg: nenhum.

## Riscos e limitações
- Pronúncia não ouvida (sem transcrição Scribe nesta sessão). Ouvir: «Burger King», «BK», «Rosewater», «PLANESWALKER», «Chandra», «BINDER», «Numot», «Preconauta», «Nauctis», «Lotus», «Jund Sacrifice», «Top 8».
- «Spoiler da edição nova» = Expedição BINDER #01 (EX-01, Nauctis), pela resposta do fundador «O spoiler da nova edição»; o STATUS dava EX-01 como por publicar a 16/11. Confirmar.
- Publicações da semana confirmadas pelo fundador a 15/11 (02:10) sem data exata: MC-EP07, CM-EP005, MC-ESP01, MC-ESP02, EX-01. O registo editorial ainda as dava como não publicadas; atualizado nesta sessão (menos a EX-01, que fica como estava até confirmação).
- Revenda do kit do BK no eBay (a partir de ~US$ 70, MTG Rocks) não entrou no vídeo.
- Licença comercial das vozes: depende do plano ElevenLabs ativo (não verificável por esta ligação).

## Entregáveis
- [x] Vídeo · [x] Capa · [x] Legenda · [x] Comentário fixado · [x] Texto alternativo · [x] Fontes

## Ficheiros finais
- Vídeo: `ManaBurn_Giro_2026-11-15_916.mp4` (enviado ao fundador na conversa de 15/11/2026; não versionado). Recriar: `LEIA-ME.md`.
- Capa: `manaburn/giro/2026-11-15/MB_GIRO03_CAPA.png` (+ `_grelha.png`).

## Depois de publicar
- Métrica principal: respostas «1/2/3» por 1.000 views. Secundária: partilhas.
- Publicação: (data, hora) · Resultado observado: —

## Controlo de qualidade (ficheiro final `ManaBurn_Giro_2026-11-15_916.mp4`)
| Critério | Alvo | Medido | OK |
|---|---|---|---|
| Formato | 1080×1920, 30 fps, H.264 + AAC 48 kHz | 1080×1920, 30 fps | sim |
| Duração | pela história | 74,07 s (70,2 s + fecho de 3,87 s) | sim |
| Loudness / pico | −14 LUFS, < −1 dBTP | −14,5 LUFS, −1,1 dBTP | sim |
| `qc_video.py --frente manaburn` | sem problemas | «Sem problemas mensuráveis»; fecho a partir de 70,2 s | sim |
| cropdetect 24:2:0 | 1080:1920:0:0 | 2220/2220 quadros | sim |
| `bordas.py` | OK | 1182 quadros de TV, laterais 10–1068 px, topo ≥ 300 px | sim |
| Textos da TV SAL | legíveis, sem corte | 2.º render cortava «TERRENOS POR PANCADA» e «QUEM COMEÇA VENCE»; títulos encurtados e re-renderizado (3.º render); conferido a 6, 31, 41, 47, 52, 57 e 61 s | sim |
| Carta inteira e destaque | Chandra (−3), Numot (pagar {2}{R}, até dois terrenos) | cartas inteiras; destaques sobre as linhas certas (31 s e 41 s) | sim |
| Legenda queimada | zona segura, sem tapar a carta | folha de contacto conferida | sim |
| Sincronia das falas | fronteiras certas | 12 falas do Burn e 12 do Mana cortadas pelo `process.py`, conferidas contra o texto | sim |
| Bordões | intactos | «Lê a carta» (×2), «Isso devia ser banido!», «Comenta aí» | sim |
| Fim | TV desliga → ponto verde → scanner → logo | pancada 69,88 s; fecho 70,2 s | sim |
| Retenção | quadro 0 com Magic; mudança visual ≤ 3 s; som em cada revelação | quadro 0 = tela «Giro de domingo» da TV SAL com 1-2-3 (sem carta: P2); 23 cortes em 70 s (maior intervalo 5,5 s entre 21,6 e 27,0 s, com troca de tela na TV a meio); som de troca de canal em cada canal e de destaque nas 2 leituras | sim (P2 no quadro 0) |
| Pronúncia | ouvida | **não ouvida** | P1 a confirmar pelo fundador |
| Afirmações | todas com fonte | `fontes.md` | sim |
