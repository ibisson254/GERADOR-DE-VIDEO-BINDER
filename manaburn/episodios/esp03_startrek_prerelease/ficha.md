# Ficha · Mana & Burn · Especial pré-release Star Trek · "BURN FOI ASSIMILADO!"

Subtítulo: O pré-release de Star Trek chegou. E ninguém está preparado.

## Classificação
- Série: Mana & Burn · especial (tarja "ESPECIAL PRÉ-RELEASE STAR TREK · <ato>")
- Tipo de produção: especial (constituição §14), pedido do fundador de 06/11/2026 ("Prompt de engenharia avançada · Especial Mana & Burn: Star Trek pré-release")
- Router: carta/set do momento + reação da comunidade = território Mana & Burn. Tem leitura de Limited, mas sem lista de deck nem análise de partida (isso seria Meta em Curto); a informação de Sealed entra como regra de carta e recomendação oficial
- Classe: hype de set + leitura de carta
- Complexidade: alta (set novo, 6 cartas, 3 previsões, sem dados de jogo)
- Estratégia: investigação aprofundada; Oracle e notas de lançamento para toda regra; previsões com evidência, risco e certeza; nenhuma percentagem de vitória

## Editorial
- Objetivo: respostas A/B no comentário fixado no fim de semana do pré-release; partilhas entre quem vai jogar.
- Proposta de valor: abrir a rara não é montar o deck. Seis cartas reais mostram porquê, em seis atos.
- Público: jogador casual brasileiro que vai ao pré-release de Star Trek (e quem só gosta de Star Trek).
- Hipótese a testar: um especial de pré-release publicado no próprio dia gera mais guardados por 1.000 views do que o Ep. 9 (informação útil para levar à loja). Secundária: A/B com dois arquétipos concretos.
- Gancho (0–3 s): "Mana! Abri um Cubo Borg no pré-release! Eu fui assimilado!" com o Borg Cube na TV.
- Surpresa central (ato 5): Resistance Is Futile, a frase dos Borg, só destrói criatura **não artefato**; todo Borg do set é artefato. A carta dos Borg não mata Borg.
- Fecho: veredito com três apostas do Mana → o Burn discorda ("Cubo, cinco cores e três naves") → pergunta A/B → "Comenta aí." → TV desliga → fecho do scanner.

## Estrutura (6 atos = 6 canais da TV SAL)
| Ato | Falas | Canal (carta) | Pergunta de retenção | O que o público leva |
|---|---|---|---|---|
| 1 A assimilação | 1–4 | Borg Cube | O que o Burn abriu? | A rara precisa de 39 cartas e de 12 marcadores |
| 2 A primeira descoberta | 5–8 | The Traveler (+ insert Orion) | Cinco cores funciona? | Conta-se nome, não terreno; os 10 planetas comuns entram virados |
| 3 Os Borg não perdoam | 9–12 | Locutus (+ insert Vexing Drone), CH 47 | Quem ganha a corrida? | Borg de 2 manas com +1/+1 punem a turnê lenta |
| 4 A armadilha das naves | 13–16 | U.S.S. Voyager | A nave salva? | Station vira o tripulante, que não bloqueia; 2–3 naves, não uma frota |
| 5 O segredo do dilema | 17–21 | Resistance Is Futile | A remoção dos Borg resolve? | Não mata artefato; escolher modo é dilema |
| 6 O veredito | 22–28 | Perils of the Past | Quem tem razão? | Três apostas + remoção de artefato |

## Duração
95,3 s com o fecho (91,4 s antes do fecho do scanner; 3,87 s de fecho). Escolhida depois do roteiro: seis atos com uma carta cada, mais o veredito. Cortado de ~105 s estimados para ~91 s (constituição §5: cada fala avança a ideia). Referências: Especial de Halloween 97,6 s; Picard 69,9 s.

## Produção
- Kit v2 de `manaburn/` sem alterações de código. Usado o motor de canais (`EP.canais`, zapping de 25/10) para trocar de carta, medidor e placar a cada ato; o som de troca de canal marca cada ato.
- Planos: só `tv`, `tv2`, `tvtext`, `tvtext2`, `wide` e `cuM`. Sem `push` nem `cuB`, porque cortam a TV ao fundo (preferência do fundador: nenhum zoom que corte a TV). Conferido na prévia.
- Cartas: 8 PNGs reais do Scryfall (744×1040). Destaques medidos nas linhas de pixels escuros e conferidos nos quadros.
- TV SAL: medidores só com dados das cartas (Oracle) e do guia oficial; o "Putômetro" não existe porque cartas novas não têm Salt Score. Placar por canal. 8 manchetes, todas verdadeiras ou piada sem pessoas reais.
- Vozes: ElevenLabs eleven_v4, flow "Mana & Burn — Especial pré-release Star Trek (Burn foi assimilado)" (uynVVRurU7AQlC3bwwc5). Burn: Talis (E9a8LlXPNWtyvvSoZzrb), 1.027 créditos. Mana: Erik (nfiLpQ54jEQninp3nNqL), 1.144 créditos. 1 geração cada, descarregadas pela sessão. Ritmo ×1,06 / ×1,12, respiro 0,14 s. Grafias: Bórg, pré-rilís, Locútus, Tráveler, Vóiajer, Resistênce is Fiútail, Spóc.
- Autorização de créditos: o pedido do fundador de 06/11 manda executar a produção completa sem parar no roteiro (constituição §1: pedido explícito do fundador prevalece). Uma geração por voz, sem repetição.
- Música: midnight_throttle (`manaburn/musica.mp3`), trecho 35,2–131,1 s; parada seca no "Comenta aí", pancada desliga a TV.
- Fecho: `comum/outro/outro_binder_916.mp4` colado por `juntar_fecho.py` do Ep. 9 (corte em T_SLAM + 0,52 s; tira os 7 quadros de ligar a TV).
- Easter egg: "CH 47" no ecrã de troca de canal do ato 3 (Borg), ~28,2–28,6 s. 47 é a piada interna dos argumentistas de Star Trek.
- Sensibilidade: o Locutus é o Picard assimilado, e a morte de Sir Patrick Stewart é recente (especial Picard de 29/10, Giro de 01/11). A carta aparece só pelo efeito de jogo; nenhuma piada é sobre o personagem.

## Riscos e limitações
- Pronúncia não conferida por transcrição nem por ouvido nesta sessão: ouvir "Bórg", "Locútus", "Tráveler", "Vóiajer", "Resistance Is Futile", "Spock" antes de publicar.
- Licença comercial das vozes: depende do plano ElevenLabs ativo às 10:30 de 06/11/2026 (não verificável por esta ligação).
- Nenhum resultado de pré-release existe ainda; as três previsões são apostas e dizem-no.
- Insert do Vexing Drone e do Orion passa por cima da TV pequena nos planos de conjunto (comportamento do kit, igual ao Ep. 9); nos planos da TV a carta principal fica inteira.
- Legenda com 934 caracteres (créditos de 6 cartas).

## QC medido no ficheiro final (`ManaBurn_Especial_StarTrek_Prerelease_916.mp4`, 06/11/2026)
| Critério | Alvo | Medido | OK |
|---|---|---|---|
| Resolução / fps / codecs | 1080×1920, 30, H.264 + AAC 48 kHz | 1080×1920, 30/1, h264 + aac 48000 Hz | sim |
| Duração | pela história (§14) | 95,30 s (91,43 s + fecho) | sim |
| Loudness / pico | −14 LUFS, < −1 dBTP | −14,0 LUFS, −1,5 dBTP (o 1.º passe deu +0,5 dBTP depois da colagem do fecho; corrigido com loudnorm de 2 passes, vídeo copiado sem reencode) | sim |
| `qc_video.py` | sem problemas | "Sem problemas mensuráveis"; fecho presente a partir de 91,43 s | sim |
| cropdetect 24:2:0 | 1080:1920:0:0 | 2857/2857 quadros reportados = 1080:1920:0:0 | sim |
| `bordas.py` (tela da TV) | OK | 1263 quadros de TV, laterais 10–1068 px, topo ≥ 300 px: OK | sim |
| TV ao fundo nos planos do sofá | inteira | sem push/cuB; conferida nos quadros 36, 50, 78, 86, 90 s | sim |
| Carta inteira, destaques alinhados | 6 cartas | quadros 9,6 / 16,2 / 30 / 42 / 58 / 63 / 71 s; destaques sobre as linhas certas | sim |
| Medidor com conta e fonte | todos os canais | visível em todos os planos de TV conferidos | sim |
| Legenda queimada | zona segura | conferida nos 20 quadros e na folha de contacto | sim |
| Bordões | intactos | "Lê a carta" (×3), "Isso devia ser banido", "Comenta aí" | sim |
| Fim | TV desliga → ponto verde → scanner real → logo | 91,6 / 93,5 / 95,1 s | sim |
| Easter egg | visível e discreto | "CH 47" a 28,25–28,4 s | sim |
| Pronúncia | ouvida | **não conferida** nesta sessão (sem audição nem transcrição) | P1 a confirmar pelo fundador |

## Entregáveis
- [x] Vídeo · [x] Capa · [x] Legenda · [x] Comentário fixado · [x] Texto alternativo · [x] Legendas .srt · [x] Fontes e previsões

## Depois de publicar
- Métrica principal: respostas A/B por 1.000 views. Secundária: guardados e partilhas.
- Rever as três previsões depois de 12/11 com dados reais.
- Resultado observado: —
