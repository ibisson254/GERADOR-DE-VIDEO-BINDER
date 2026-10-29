# Ficha · Meta em Curto · EP02 · Hartford: começou atrás na mesa e ganhou os dois

Render final de 29/10/2026 (48,9 s com o fecho; 45,0 s sem o fecho). Scripts: `ep02_audio.py`, `ep02_render.py`, `ep02_carrossel.py`. Dados: `ep02_roteiro.json`, `ep02_words.json`, `ep02_listas.json`, `../ep02/cartas/`.

## Classificação
- Série: Meta em Curto (TUBO)
- Classe: decisão de torneio, em **Modo B, Leitura da Final**. Não é «A Jogada que Não Viste»: o VOD do Dia 2 tem 10h47, não tem legendas e passa do limite da análise de vídeo (6 h). Sem estado de mesa verificável, nenhuma jogada foi reconstruída.
- Complexidade: média · Estratégia: verificação rápida (Oracle) + atribuição à SCG.

## Editorial
- Objetivo: explicar como Jund Sacrifice ganha mesmo atrás na mesa.
- Proposta de valor: na final de Hartford, Ott teve a mesa nos dois jogos e von Stange ganhou os dois, porque o deck dele conta dano por sacrifício, não tamanho de mesa.
- Público: jogador de Standard e espectador competitivo PT/BR.
- Hipótese a testar: evidência visual completa (lista, cartas, fichas de jogador) aumenta os guardados.
- Tese (marcada como leitura do TUBO): mesa não é vida.
- Gancho: «Na final de Hartford, ele começou atrás na mesa. Nos dois jogos. E ganhou os dois.»
- Nota: o gancho usa «começou atrás na mesa» (relato da SCG) em vez de «perdeu a mesa», que diria mais do que a fonte.

## Narração final
Na final de Hartford, ele começou atrás na mesa. Nos dois jogos. E ganhou os dois. Von Stange, Jund Sacrifice. Contra Ott, Jeskai Artifacts, seed um. Ott tinha a mesa: aceleração, United Battlefront, Constructs enormes. O von Stange não disputava a mesa. Contava dano. Biotech Specialist: artefato sacrificado, dois de dano. Sackville-Bagginses: ficha sacrificada, um de vida. Um Tesouro é as duas coisas: três. E o Lively Dirge busca uma peça e traz até duas de volta. O meu modelo contou a mesa. Ele contou o dano. Mesa não é vida. O que decidiu a final? A: a mesa do Ott chegou tarde. B: o Dirge achou as peças. C: a pilotagem. Probabilidade calculada. Humanos, imprevisíveis.

## Fontes e evidências
| Afirmação | Tipo | Fonte | Data |
|---|---|---|---|
| Von Stange campeão; Ott vice; seeds 3 e 1; QF/SF; 11-0 → R12/R13 derrotas, R14 vitória, R15 ID; RC Chiba 2023 | facto | Star City Games (relato) | 25/10/2026 |
| Ott à frente na mesa nos dois jogos da final; Dirge para achar peças; vitória com Biotech + fichas | facto (relato SCG) | idem | 25/10/2026 |
| Final 2-0 («ganhou os dois») | dedução do relato | idem | — |
| Suíço 12-2-1 | cálculo nosso | idem | — |
| Listas 60 + 15 de ambos os finalistas | facto | idem | 25/10/2026 |
| Textos de Biotech, Sackville, Treasure, Lively Dirge, United Battlefront | facto | Scryfall API | 29/10/2026 |
| Tesouro = 3 (2 + 1); Biotech + Sackville = VM 4 | cálculo nosso | Oracle | — |
| «Mesa não é vida» | opinião / leitura do TUBO | — | — |
Detalhe e falhas de verificação: `ep02_hartford_fontes.txt`.

## Estrutura real (cortes medidos no render)
| Tempo | Onde | Conteúdo |
|---|---|---|
| 0–5,2 s | Fora (desconfiado → confiante) | Gancho; sobreposição «MESA: OTT · TÍTULO: VON STANGE» |
| 5,2–5,7 s | Mergulho | Som de modem |
| 5,7–10,3 s | Dentro | Cabeçalho do arquivo + duas FICHAS DE JOGADOR com silhueta (estreia da regra 6.4) |
| 10,3–15,2 s | Dentro | United Battlefront em scan + «aceleração · United Battlefront · Constructs» |
| 15,2–18,1 s | Dentro | Impressão da lista completa de von Stange (60 cartas, 2 colunas, 3 cartas-chave a verde), 2,9 s parada |
| 18,1–27,0 s | Dentro | Biotech → Sackville → conta do Tesouro (= 3) |
| 27,0–30,8 s | Dentro → sai | Lively Dirge (+{1} cemitério, +{2} até 2 criaturas VM ≤ 4; 2 + 2 = 4) |
| 30,8–33,9 s | Fora | «MODELO TUBO: vencedor provável = mesa maior → Ott»; **Erro de sistema** (estreia) a partir de 32,2 s |
| 33,3–34,8 s | Fora | «MESA ≠ VIDA · leitura do TUBO, não regra do jogo»; corte seco da trilha 34,26–35,51 s |
| 34,8–41,3 s | Fora | Pergunta + GRAU DE CERTEZA (motor ALTO · final BAIXO) + chips A/B/C |
| 41,3–45,0 s | Fora | Cartão de assinatura + frase de fecho |
| 45,0–48,9 s | Fecho | Quadros reais do scanner + logótipo |

## Controlo de qualidade (ficheiro final, 29/10/2026)
| Critério | Resultado |
|---|---|
| 1080×1920, 30 fps, H.264 + AAC 48 kHz | OK |
| Corte lateral (cropdetect em 1466 quadros) | OK: crop=1080:1920:0:0 em todos os 1464 quadros medidos (o cropdetect salta os 2 primeiros) |
| Duração | 45,0 s sem o fecho (limite 45); 48,9 s no total |
| Loudness | −14,0 LUFS integrados, pico real −1,2 dBFS |
| Lista no ecrã = fonte | OK: 22 + 7 + 5 + 4 + 22 = 60 |
| Linha de fontes | Corpo 34 px (antes 22–24 px), acima das legendas |
| Fotos de pessoas | Nenhuma (silhuetas) |
| Cartas | Imagens oficiais do Scryfall, inteiras, com crédito de artista e Wizards |
| Facto / dedução / leitura separados | OK: medidor de certeza e «leitura do TUBO» no ecrã |
| Contacto visual | Folha de contacto do MP4 (1 quadro/s) vista do início ao fim |
| Defeitos bloqueadores | Nenhum |

## Limitações conhecidas
- Modo B por falta de VOD analisável; as listas não foram cruzadas com o Melee, que está bloqueado nesta sessão.
- O alfa do texto não é respeitado pelo Pillow 12 neste pipeline, por isso os textos aparecem de uma vez em vez de em fade. A chuva de código passou a usar cores pré-misturadas.
- O fecho continua reconstruído a partir dos quadros do scanner, porque falta `comum/outro/outro_binder_916.mp4` no repositório.

## Depois de publicar
- Métrica principal: guardados + partilhas · secundária: respostas A/B/C.
- Resultado observado: (aguarda o print do Insights)
