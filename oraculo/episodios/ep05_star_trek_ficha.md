# Ficha · Meta em Curto · EP05 · Star Trek: engenharia de um deck vencedor

Scripts: `ep05_audio.py`, `ep05_render.py`. Dados: `ep05_roteiro.json`, `ep05_words.json`, `../ep05/`. Dossiê: `ep05_star_trek_dossie.md`. Fontes: `ep05_star_trek_fontes.txt`. Pacote: `../legendas/ep05_star_trek_legenda.txt`.

## Classificação
- Série: Meta em Curto (TUBO) · Episódio regular · Classe: Previsão + Relatório do Meta, sem torneio concluído
- Complexidade: alta · Estratégia: análise de dados + Oracle
- Exceção de território: o perfil pede torneio recente; este episódio é pedido direto do fundador (05/11/2026; constituição §1). Âncoras: pré-release (06–12/11) e Worlds 32 (Star Trek Draft, 13–15/11). Não muda a regra.
- Autorização de créditos: dada na missão de 05/11/2026 («A autorização para executar esta operação já foi dada»).

## Editorial
- Objetivo: dar a jogadores experientes uma conta de construção antes do pré-release.
- Proposta de valor: no Sealed, a estrutura aparece nos jogos e a bomba quase nunca.
- Público: jogador competitivo de Limited. Sem explicação de regras básicas.
- Hipótese a testar: gráfico próprio aumenta guardados; pergunta A/B/C sobre decisão real gera respostas.
- Tese (leitura do TUBO): o deck que ganha não é o da maior bomba; é o que executa o próprio plano.
- Gancho: «A Enterprise-A que você quer: 3,8% de abrir.»
- Duração: 93,1 s sem o fecho. Oito blocos obrigatórios; o rascunho tinha ~2 min e perdeu 48 palavras. A referência da série é 45–60 s: é o episódio mais longo; ver retenção.

## Alterações ao roteiro
A proposta anterior não foi localizada (dossiê §2). O roteiro foi escrito depois da pesquisa. Cortes: arquivo do set, 17 terrenos (só no ecrã), Klingon no grafo, Golgari nos pools. Correção: 91% → 92%.

## Fontes e evidências
| Afirmação | Tipo | Fonte | Data |
|---|---|---|---|
| 14 cartas, taxas por vaga, promo | facto | Wizards, Collecting Star Trek | 05/11/2026 |
| 3,8% (3,77%) de abrir mítica específica | cálculo, piso; premissa: taxa igual entre 25 míticas | colação + `probabilidades.py` | 05/11/2026 |
| 27,5% até T5 | cálculo: 11/40, começando | hipergeométrica | 05/11/2026 |
| 1 jogo em 96 | cálculo: 1,04% | produto | 05/11/2026 |
| 0 partidas de TRK | facto em 05/11 | MTGMeta; calendário Wizards | 05/11/2026 |
| 69 listas, 58 com 2 cores, 60 com 17 terrenos | facto, amostra rasa | Untapped.gg | 05/11/2026 |
| 1 de 11 com 3 cores e até 1 derrota | facto, amostra enviesada | Untapped.gg | 05/11/2026 |
| Mundial é Draft | facto | magic.gg | 05/11/2026 |
| Gruul 3.º → 9.º em Reality Fracture | facto atribuído | note.com (Portent Lab/17Lands, MTGMeta) | 18/10/2026 |
| 92% (91,63%), 19%, 52% | cálculo | hipergeométrica + Monte Carlo | 05/11/2026 |
| 3 famílias, 10 cartas partilhadas, 2 isolados | cálculo; etiquetas nossas; nota MTGAZone | Oracle + `grafo.py` | 05/11/2026 |
| Motor 65 / 25 / 15 | modelo | `pools.py` | 05/11/2026 |
| Wizards pede 5 remoções | facto | guia de pré-release | 30/10/2026 |
| Rakdos quase 6, Simic nem 3 | modelo; remoção marcada à mão | `pools.py` | 05/11/2026 |
| Tese | opinião do TUBO, marcada no ecrã | — | — |
| Rakdos top 3 | previsão, marcada no ecrã | `comum/historico.md` | até 01/12/2026 |

## Produção
- Voz: ElevenLabs "Antonio de Jesus", eleven_v4, tomada 1 de 2 (1.503 créditos cada, 3.006) + correção da frase das 7 cartas (2 × 76, take 2), atempo 1,10. Flow: `on9fdsdEWluJv0rGTgtn`. Total 3.158 créditos.
- Trilha: "Paper Thin Alibi" (`tubo_tema_original.mp3`) prolongada com repetição de um troço: salto 49,78 → 19,02 s (batidas parecidas, cromas + MFCC). Corte seco de 1,2 s depois de «É modelo, não é jogo.».
- Efeitos: arranque, modem, ticks, zumbido em «zero partidas».
- Gráficos: 100% determinísticos, a ler `oraculo/ep05/resultados/*.json`. Nenhuma imagem gerada.
- Carta: U.S.S. Enterprise-A, Free Spirit, TRK 43, arte de Evan Shipard, imagem Scryfall.
- Personagem: imagem-mestra, sem regenerar. Sem foto de jogador: nenhum jogador citado.
- Contador ERROS HUMANOS: não mostrado (sem valor registado).
- Grau de certeza: previsão BAIXO.
- Easter egg: «1701-A» na vertical na chuva de código, à direita da Enterprise-A (~4,5–7,5 s): o registo da nave.
- Direitos: arte de Star Trek em conteúdo de fã, com crédito. Mesma exposição do Órbita já publicado; impulsionar é decisão do fundador.

## Controlo de qualidade (ficheiro final, 05/11/2026)
| Critério | Resultado |
|---|---|
| Formato | 1080×1920, 30 fps; 96,9 s (93,1 s sem o fecho) |
| Corte lateral | Quadros conferidos, carta inteira; cropdetect só acusa fundo escuro |
| Loudness | −14,0 LUFS, pico −1,9 dBTP |
| Fecho | `outro_binder_916.mp4` real, sem encurtar, música até ao fade |
| Sincronia | Até 45 ms entre legenda e ataque da voz em 10 pontos |
| Fontes no ecrã | Corpo 34, até x = 940 |
| qc_video.py | Sem problemas mensuráveis |
| Revisão visual | Quadros a 2 qps do penúltimo render e 1 qps do final, todos vistos |
| Áudio | **Medido, não ouvido.** Scribe repete a grafia do prompt: não prova a pronúncia |
| Auditoria matemática | `auditoria.py`: 17 de 17 |
| Defeitos bloqueadores | Nenhum encontrado |

## Carrossel derivado (06/11/2026)
Guia de bolso do pré-release, 9 slides 1080×1350: `ep05_carrossel.py` (lê os mesmos resultados do vídeo; os números de controlo são verificados por `assert`). Pacote: `../legendas/ep05_carrossel_legenda.txt`. Previsão no formato do Protocolo de Pré-Release (PR-TRK-01, grau 2 de 5, sem o «~35%»). Sem easter egg. Métrica: guardados. Slides conferidos um a um (fontes com corpo 28, carta inteira, personagem inteiro).

## Depende do fundador
- Ouvir o áudio: pronúncias e o corte da frase em ~36–40 s.
- Aceitar ou não os 93 s.
- Publicar.

## Depois de publicar
- Métrica: guardados + partilhas; secundária respostas A/B/C.
- Auditar a previsão a 01/12/2026.
