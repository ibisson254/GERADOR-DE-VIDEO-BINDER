# Ficha · Meta em Curto · EP07 · Mundial 32: seis brasileiros e a primeira previsão

Render v2 de 10/11/2026: 64,1 s com o fecho, 60,3 s sem o fecho (v1: 57,4 s, sem listas). Scripts: `ep07_audio.py`, `ep07_render.py`. Dados: `ep07_roteiro.json`, `ep07_words.json`. Fontes: `ep07_mundial_fontes.txt`. Legenda: `../legendas/ep07_mundial_legenda.txt`.

## Classificação
- Série: Meta em Curto (TUBO) · episódio de previsão do ciclo semanal (`../CICLO_SEMANAL.md` §4), produzido numa terça por pedido do fundador (texto da legenda enviado por ele a 10/11).
- Classe: Previsão (opinião registada) + Relatório do Meta. Estratégia: análise de dados atribuída (Karsten, magic.gg) + cálculo nosso.

## Editorial
- Proposta de valor: o Mundial tem 6 brasileiros entre 134 convidados; os dados dizem que deck chega (Jund Sacrifice), não quem pilota.
- Público: jogador competitivo PT/BR que vai acompanhar o WC32.
- Hipótese a testar: pergunta com nome de jogador real ("comente o nome") gera mais comentários por 1.000 views do que A/B/C.
- Previsões: PR-WC32-01 (pública, 3/5), PR-WC32-02 e 03 (registo). Conferência: segunda 16/11 (episódio de prestação de contas).

## Narração final
Seis brasileiros. Cento e trinta e quatro convidados. Oito vagas no Top 8. Mundial trinta e dois. Atlanta, de treze a quinze de novembro. Draft de Star Trek, coleção que chega às lojas no primeiro dia, e Standard. Na lista oficial, seis brasileiros. Cinco vieram dos Regional Championships. Um, do Arena Championship. Se o Top 8 fosse sorteio, a chance de pelo menos um brasileiro entrar seria de trinta e um por cento. Mas Mundial não é sorteio. Mil oitocentas e dez listas de três torneios. O deck mais jogado é Mono-Green Landfall: doze vírgula sete por cento. O que mais vence é Jund Sacrifice: cinquenta e sete vírgula seis por cento das partidas. E os dois títulos do Spotlight. Analisei os dois aqui. Previsão registrada: Jund Sacrifice no Top 8. Certeza três de cinco. Segunda eu confiro. Os dados escolhem o deck. Não escolhem quem pilota. Qual brasileiro chega ao Top 8? Comente o nome. Probabilidade calculada. Humanos, imprevisíveis.

## Estrutura (render)
| Tempo | Onde | Conteúdo |
|---|---|---|
| 0–5,3 s | Fora (desconfiado → confiante) | Gancho: 6 BRASILEIROS · 134 CONVIDADOS · 8 VAGAS NO TOP 8 |
| 5,3–13,9 s | Mergulho → dentro | Arquivo WC32: 134, 8, formatos (Star Trek "lança 13/11"; Standard, Top 8 em Standard) |
| 13,9–19,5 s | Dentro | 6 fichas de jogador com silhueta e origem do convite (5 RC, 1 Arena Championship 11); egg "2002" |
| 19,5–26,6 s | Dentro | Modelo sem habilidade: 134 pontos, 6 verdes, 8 vagas → 31%; carimbo MUNDIAL NÃO É SORTEIO |
| 26,6–30,6 s | Dentro | Relatório do Meta: representação (Landfall 12,7% em destaque) |
| 30,6–35,0 s | Dentro | Lista agregada do Mono-Green Landfall (60), "26 TERRENOS" (pausa de voz 1,6 s) |
| 35,0–39,9 s | Dentro | Desempenho separado da representação; Jund 57,6% com linha de 50% |
| 39,9–44,1 s | Dentro | Os dois títulos: não-terrenos de von Stange (Hartford) e Que Mo (Pequim), 7 iguais a verde; remissão EP02/EP04 (pausa 1,8 s) |
| 41,5–47,8 s | Fora | Cartão PREVISÃO REGISTRADA · PR-WC32-01, GRAU DE CERTEZA 3 de 5, conferência 16/11 |
| 47,8–51,0 s | Fora | "Os dados escolhem o deck. Não quem pilota." (leitura do TUBO); corte seco da trilha 50,7–51,9 s |
| 51,0–53,6 s | Fora | Pergunta + 6 nomes em chips |
| 53,6–57,4 s | Fora | Cartão de assinatura + frase de fecho |
| 57,4–61,2 s | Fecho | `comum/outro/outro_binder_916.mp4` |

## Controlo de qualidade (ficheiro final, 10/11/2026)
| Critério | Resultado |
|---|---|
| `qc_video.py --frente tubo` | Sem problemas mensuráveis |
| 1080×1920, 30 fps | OK |
| Corte lateral | cropdetect 1080:1920:0:0 em todos os quadros medidos (v2: 1922) |
| Loudness | −14,0 LUFS, pico −1,6 dBTP (v2) |
| Fecho | Presente a partir de 57,37 s |
| Folha de contacto | Vista do início ao fim; textos fora das linhas de fonte; legendas na faixa habitual da série |
| Fotos de pessoas | Autorizadas pelo fundador a 10/11 (ver `oraculo/autorizacoes/`); 5 fotos recortadas da captura enviada pelo fundador (17:24); João Jorge Sales Junior com silhueta (miniatura sem rosto) |
| Representação × desempenho | Em blocos separados, com a definição de win rate na linha de fonte |
| Previsão | Marcada no ecrã, registada antes da voz, `ciclo.py validar` OK |
| P2 (v1) | Relatório do Meta parado 15 s → resolvido na v2 com as listas |

## Limitações
- Não ouvi o áudio: confirmar a pronúncia de "Regional Championships", "Arena Championship", "Spotlight" e "Mono-Green Landfall".
- Lista de convidados sujeita a alterações; se um brasileiro desistir, a pergunta e o egg continuam válidos, o "6" não.
- Não usa listas do próprio Mundial (publicadas na ronda 4, 13/11).

## Depois de publicar
- Segunda 16/11: `python3 -I oraculo/previsoes/ciclo.py segunda` → conferir PR-WC32-01..03 com o Top 8 e a análise do metagame do magic.gg.
- Métrica principal: guardados + partilhas · secundária: comentários com nome por 1.000 views.
