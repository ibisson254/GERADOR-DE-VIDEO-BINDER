# Ficha · Meta em Curto · ESP02 · A Taça respondeu

ID editorial: **MC-ESP02**. Render de 14/11/2026: 59,4 s com o fecho, 55,6 s sem o fecho. Pacote nesta pasta: `comentarios/` (prints dos comentários), `cartas/` (4 imagens Scryfall + `creditos.json`), `dados/` (instantâneo da Taça), `esp02_audio.py`, `esp02_render.py`, `roteiro.json`, `words.json`, `fontes.txt`, `legenda.txt`, `comentario_fixado.txt`, `texto_alternativo.txt`.

## Classificação
- Série: Meta em Curto (TUBO) · **especial**, continuação do MC-ESP01; fora do ciclo segunda/quinta.
- Classe: dados reais de torneio (2x2 de Precon) que corrigem a conta teórica do ESP01. Collab com @preconautamtg.
- Autorizações: fundador, 14/11/2026 01:07 («Análise o site e faça a continuação do vídeo e para fazermos o colab com eles também»), que inclui a voz na ElevenLabs; Preconauta (dados e collab): `../autorizacoes/2026-11-13_preconauta_dados_2x2.md`.

## Editorial
- Proposta de valor: a dupla iguala a mesa; a ordem de turno desempata (quem começa o jogo 1 vence 66%).
- Público: jogador de Precon/Commander PT-BR, em especial quem joga ou acompanha ligas 2x2.
- Pagamento de ciclo aberto: o «Ainda.» do ESP01 vira «Agora publicam».
- Sem nomes de jogadores ou duplas da Taça (dados públicos no site, mas sem autorização individual). Os comentaristas aparecem no print real (regra de 14/11).
- Hipótese a testar: a collab (post no perfil do Preconauta) traz mais visitas ao perfil por 1.000 views do que o ESP01.

## Plano de retenção (constituição, «Retenção e recompensa»)
- Quadro 0: quatro comandantes reais dos precons mais jogados da Taça a cair na mesa.
- Gancho visual que encena a tese: «50% — a conta do TUBO» riscado a vermelho → as cartas viram «começa × em 2º» → «66%» no ecrã do TUBO.
- Revelações com som curto: 50%, risco, duplas, 66%, «agora publicam», 101/230/97, barras 66/59, «52 de 101», barras dos decks, carimbo do Jeskai, «Errei a conta», «A ordem de turno desempata», chips A/B/C.
- Participação: pergunta A/B/C e egg «29».

## Narração final
Eu disse cinquenta por cento. A Taça Preconauta respondeu: sessenta e seis. Lembra do ainda? Eles publicam tudo. Primeira edição: cento e um matches, duzentos e trinta jogos, noventa e sete precons diferentes. No jogo um, quem começa é sorteado. Quem começa vence sessenta e seis por cento. Em todos os jogos, cinquenta e nove. E mais da metade dos matches foi para o terceiro jogo. O Ahoy Mateys vence setenta e dois por cento começando. Em segundo, trinta e sete. Só o Jeskai Striker segura jogando em segundo: cinquenta e seis. Errei a conta. A dupla iguala a mesa. A ordem de turno desempata. Grau de certeza: quatro de cinco. Setenta jogos sorteados. A Taça ainda está rolando. Qual precon você leva pra Taça? A, Ahoy Mateys. B, Jeskai Striker. C, Multiverse Reforged. Responda com a letra. Probabilidade calculada. Humanos, imprevisíveis.

Voz: ElevenLabs «Antonio de Jesus» (`MK5tXPmT83J5SUlpUo4K`), eleven_v4, tomada 2 de 2 (flow `TpVm0lubJKw9SGFwt9tB`, geração `zspT1elD1FRFJQYfYMsI`; 1.702 créditos nas duas tomadas), atempo 1,10. Tempos por palavra: Scribe v1 (142 = 142).

## Estrutura (render)
| Tempo | Onde | Conteúdo |
|---|---|---|
| 0–4,9 s | Fora | Gancho: 4 comandantes na mesa · «50%» riscado · duplas «começa × em 2º» · «66%» no ecrã do TUBO |
| 4,9–14,0 s | Mergulho → dentro | «A comunidade respondeu»: citação do ESP01 riscada + AGORA PUBLICAM; prints reais de @jorel.oliveira e @preconautamtg (scan); 101 · 230 · 97 |
| 14,0–24,0 s | Dentro | Ordem de turno: jogo 1 66% (linha da previsão 50%), todos 59%; «52 de 101» ao 3.º jogo |
| 24,0–32,6 s | Dentro | Ahoy Mateys 72/37 · Jeskai Striker 71/56 · carimbo «único dos 6 acima de 50% em 2º» |
| 32,6–38,5 s | Fora | «Errei a conta. A dupla iguala a mesa. A ordem de turno desempata.»; corte seco 37,3–38,5 s |
| 38,5–43,6 s | Fora | GRAU DE CERTEZA 4 de 5; «70 jogos sorteados · a Taça ainda está rolando» |
| 43,6–51,4 s | Fora | Pergunta A/B/C |
| 51,4–55,6 s | Fora | Assinatura + frase de fecho |
| 55,6–59,4 s | Fecho | `comum/outro/outro_binder_916.mp4` |

## Controlo de qualidade (ficheiro final, 14/11/2026)
| Critério | Resultado |
|---|---|
| `qc_video.py --frente tubo` | Sem problemas mensuráveis |
| 1080×1920, 30 fps; corte lateral | OK; sem corte |
| Loudness | −14,0 LUFS, pico −1,8 dBTP |
| Fecho | Presente a partir de 55,6 s |
| Folha de contacto | Vista do início ao fim |
| Retenção | Quadro 0 com cartas de Magic; mudança visual ≤ 3 s; som em cada revelação |
| Facto × opinião | Números do site com fonte no ecrã; margem 55–77% marcada como cálculo nosso; revelação marcada como leitura do TUBO |
| Pessoas | Prints reais com foto de @jorel.oliveira e @preconautamtg (regra «Comentários da comunidade no vídeo», 14/11 02:15); sem nomes de jogadores/duplas da Taça |
| Egg | «29» na chuva de código (duplas da 1.ª edição), `comum/easter_eggs.md` |

## Ficheiros finais
- Vídeo: `ESP02_META_EM_CURTO.mp4` (md5 f0589e6c0b976733fffee6808af26a58; v2 com os prints dos comentários, 14/11 02:20), entregue ao fundador na conversa de 14/11/2026; não versionado.
- Capa: `ESP02_CAPA.png` (md5 7926d90070f852fbedad30ff8d02f2fc), mesma conversa; não versionada.
- Refazer: pasta de trabalho com `voz.mp3` (tomada acima) e `words.json` desta pasta → `python3 esp02_audio.py <kit>` → `python3 esp02_render.py <kit>` → `… capa`.

## Limitações
- Dados de uma Taça em andamento (instantâneo de 14/11, ~01:10). Regra de vida do 2x2 da Taça não confirmada (o vídeo não fala de vida).
- Não ouvi o áudio: confirmar «Ahoy Mateys», «Jeskai Striker», «Multiverse Reforged», «matches».
- Ligas 2x2/mesão (árvore de links) não lidas: preconauta.com.br não respondeu (502); fica para um próximo episódio.
- Roteiro prometido ao Preconauta antes de publicar.

## Depois de publicar
- Convite de Collab para @preconautamtg. Métrica principal: visitas ao perfil por 1.000 views · secundária: respostas A/B/C.
