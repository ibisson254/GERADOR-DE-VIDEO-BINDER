# Ficha · Meta em Curto · ESP01 · A comunidade falou: Precon em dupla

ID editorial: **MC-ESP01**. Render de 13/11/2026: 59,2 s com o fecho, 55,3 s sem o fecho. Pacote nesta pasta: `esp01_audio.py`, `esp01_render.py`, `roteiro.json`, `words.json`, `fontes.txt`, `legenda.txt`, `comentario_fixado.txt`, `texto_alternativo.txt`.

## Classificação
- Série: Meta em Curto (TUBO) · **especial**, fora do ciclo segunda/quinta (não substitui o MC-EP06).
- Classe: leitura de formato de torneio (competição) a partir de um comentário da comunidade. Estratégia: regra oficial + cálculo nosso (modelo sem habilidade) + leitura do TUBO marcada como opinião.
- Autorização: fundador, 13/11/2026 02:13 («Pode fazer o episódio eu assumo a responsabilidade…»); `../autorizacoes/2026-11-13_esp01_diarioplaninauta.md`; `nucleo/DECISOES.md` (13/11). O autor do comentário não foi consultado antes da produção.

## Editorial
- Proposta de valor: precon iguala os decks; a dupla iguala a mesa (25% de base numa mesa de 4 × 50% em dupla).
- Público: jogador de Commander/Precon PT-BR que joga ou organiza torneio em loja.
- Antecedente: especial «Precon em jogo» do Mana & Burn (`especiais/precon_em_jogo/`). Ângulo novo: matemática do formato.
- Hipótese a testar: comentário de criador conhecido no ecrã + menção na legenda gera mais visitas ao perfil por 1.000 views do que os episódios do ciclo (EP07 como comparação).
- Sem previsão registada (nada a conferir).

## Narração final
Mesa de quatro: você começa com vinte e cinco por cento. Em dupla, com cinquenta. Quem trouxe a tese foi o Diário Planinauta, aqui nos comentários. Para torneio grande, Precon em dupla é o ideal. Ele conta que a Montcard já fez torneio valendo três mil. Na versão oficial da Wizards, cada jogador usa o próprio deck de cem cartas. A dupla divide sessenta pontos de vida. Mesa de quatro, um vencedor: vinte e cinco por cento por jogador. Dois contra dois: cinquenta por cento por dupla. Antes da primeira carta. E o resultado fica binário. Vitória ou derrota, como no um contra um. O suíço agradece. Precon iguala os decks. A dupla iguala a mesa. Grau de certeza: três de cinco. Ninguém publica win rate de dupla. Ainda. Torneio grande de Precon: A, mesa de quatro. B, dois contra dois. C, depende do prêmio. Responda com a letra. Probabilidade calculada. Humanos, imprevisíveis.

Voz: ElevenLabs «Antonio de Jesus» (`MK5tXPmT83J5SUlpUo4K`), eleven_v4, tomada 2 de 2 (flow `FEmOouBmKp7Tk9u4qLWo`, geração `YRmcCMRMnvw502bI6YlB`), atempo 1,10. Tempos por palavra: Scribe v1 (153 palavras = 153 do roteiro).

## Estrutura (render)
| Tempo | Onde | Conteúdo |
|---|---|---|
| 0–5,0 s | Fora (desconfiado → confiante) | Gancho: MESA DE 4 25% · EM DUPLA 50% |
| 5,0–15,2 s | Mergulho → dentro | Arquivo: comentário de @diarioplaninauta (silhueta, sem foto), carimbo 2x2 = IDEAL; cartão @montcardshop «3k · relato do comentário · não verificado» |
| 15,2–21,7 s | Dentro | Regras: 1 deck de 100 por jogador; 60 de vida por dupla; Commander comum 40; egg «30» |
| 21,7–29,8 s | Dentro | Modelo sem habilidade: mesa de 4 (25%) × dois contra dois (50%); carimbo ANTES DA PRIMEIRA CARTA |
| 29,8–34,9 s | Dentro | Resultado da mesa: 1.º–4.º × vitória/derrota; carimbo SUÍÇO (leitura do TUBO) |
| 34,9–40,0 s | Sai do tubo → fora | Revelação: «Precon iguala os decks. A dupla iguala a mesa.»; corte seco da trilha 38,8–40,0 s |
| 40,0–44,9 s | Fora | GRAU DE CERTEZA 3 de 5; «nenhum win rate publicado na nossa pesquisa (13/11)» |
| 44,9–51,7 s | Fora | Pergunta com chips A / B / C |
| 51,7–55,3 s | Fora | Cartão de assinatura + frase de fecho |
| 55,3–59,2 s | Fecho | `comum/outro/outro_binder_916.mp4` |

## Controlo de qualidade (ficheiro final, 13/11/2026)
| Critério | Resultado |
|---|---|
| `qc_video.py --frente tubo` | Sem problemas mensuráveis |
| 1080×1920, 30 fps | OK |
| Corte lateral | cropdetect 1080:1920:0:0 em todos os quadros medidos |
| Loudness | −14,0 LUFS, pico −2,1 dBTP |
| Fecho | Presente a partir de 55,3 s |
| Folha de contacto | Vista do início ao fim; corrigidas sobreposições do gancho, da revelação e da pergunta com o monitor; ecrã vazio nas regras (15–17 s) corrigido |
| Facto × opinião | 25%/50% marcado como cálculo nosso (não é win rate); «suíço» e revelação marcados como leitura do TUBO; 3k marcado como não verificado |
| Pessoas | Sem foto de perfil; nome e @ com autorização do fundador |
| Egg | «30» na chuva de código (vida do Gigante de Duas Cabeças clássico), `comum/easter_eggs.md` |

## Ficheiros finais
- Vídeo: `ESP01_META_EM_CURTO.mp4` (md5 a9ba08dbbe6bddc9e23ab705fc06a973), entregue ao fundador na conversa de 13/11/2026; não versionado.
- Capa: `ESP01_CAPA.png` (md5 95b9a6d8a5b7fb9cdb915408f59ae5e6), entregue na mesma conversa; não versionada.
- Refazer: na pasta de trabalho com `voz.mp3` (tomada acima) e `words.json` desta pasta: `python3 esp01_audio.py <kit>` → `python3 esp01_render.py <kit>` → `python3 esp01_render.py <kit> capa`.

## Limitações
- Não ouvi o áudio: confirmar a pronúncia de «Planinauta», «Montcard», «Wizards» e «win rate».
- O torneio de 3k da Montcard não foi verificado; regulamento desconhecido (pode não seguir os 60 de vida da versão WPN).
- «Ninguém publica win rate de dupla» é uma afirmação de ausência; o ecrã limita-a à nossa pesquisa.
- O autor do comentário não foi avisado: recomendado avisar e convidar para Collab antes de publicar.

## Depois de publicar
- Métrica principal: guardados + partilhas · secundária: respostas A/B/C e visitas ao perfil por 1.000 views.
