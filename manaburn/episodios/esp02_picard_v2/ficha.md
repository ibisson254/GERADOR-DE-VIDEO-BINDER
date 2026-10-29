# Ficha · Mana & Burn · Especial Capitão Picard v2 · "Isso NÃO devia ser banido"

## Classificação
- Série: Mana & Burn · especial (tarja "ESPECIAL · CAPITÃO PICARD")
- Classe: tendência cultural + leitura de carta
- Complexidade: alta (homenagem num tema sensível, notícia da semana)
- Estratégia: investigação aprofundada (fontes da v1 revistas + factos do personagem com 2 fontes) + Oracle para a regra
- Regra aplicada: constituição §14 (especiais e homenagens), v1.1

## Editorial
- Proposta de valor: Picard é o capitão que até o Burn se recusa a banir.
- Objetivo: celebração partilhável; comentários com o momento favorito de cada fã.
- Público: comunidade de Magic e de Star Trek, colecionadores.
- Gancho (0–4 s): o Burn aponta a TV: "Mano, olha quem tá chegando no Magic: o capitão Jean-Luc Picard!"
- Pivô: fala 13, carimbo "NUNCA" na lista de banimento do Burn.
- Fecho: pergunta do Burn → "Comenta aí." → "Engage." → arrancada do ponto verde → BINDER Originals + "Obrigado, capitão."
- Métrica: comentários com memórias por 1.000 views; partilhas. Sem previsões.
- Conceito, guião e comparação: `conceito_e_comparacao.md`, `guiao_definitivo.md`. Fontes: `ficha_fontes.md`.

## Produção
- Vozes: ElevenLabs eleven_v4, flow "Mana & Burn — Especial Picard v2 (celebração)"; Burn (Talis) 711 créditos, Mana (Erik) 729 créditos, 1 geração cada; descarregadas pela sessão.
- `processar2.py`: corte nas pausas reais, respiros (0,22 s; 0,75 s na fala 13; 0,38 s na 16), +0,5 s de suspense depois do "Isso", ritmo ×1,04/×1,06, ducking, carimbo, arrancada, −14 LUFS.
- `musica2.py`: trilha original sintetizada (Ré maior, 96 BPM, cordas em colcheias, metais suaves, piano com motivo próprio em graus conjuntos, tímpanos); marcas da montagem: pausa no banimento, crescendo no legado, calma no Sir Patrick, acorde no "Engage". Sem tema, amostra ou fanfarra de Star Trek.
- `especial.html` = desenhos do `manaburn/index.html` sem alteração + `cena_v2.js` (luz de fim de tarde, poses e planos por fala, zoom no texto da carta com destaque medido no PNG, lista de banimento, textos de ecrã, arrancada final).
- `quadros.py` (2 processos) → ffmpeg. `previa.py`, `capa2.py`.
- Easter egg: nenhum. A lista de banimento do Burn (cartas dos Ep. 1, 2, 8 e 9) é uma referência aberta, não um detalhe escondido; por isso o comentário fixado também não traz o "Diga o segundo".

## Riscos e limitações
- Pronúncia (Jean-Luc Picard, Luminary, Make it so, Earl Grey, Sir Patrick Stewart, Engage) não conferida por transcrição: o envio ao Scribe é bloqueado pela rede desta sessão. Ouvir antes de publicar.
- Licença comercial das vozes: depende do plano ElevenLabs ativo às 23:07 de 29/10/2026; não verificável por esta ligação.
- "Essa semana" na fala 16 só vale até sábado, 31/10.
- Sem fecho do scanner nem CTA do app: exceção do brief original mantida (ver DECISOES).

## QC medido no ficheiro final (`ManaBurn_Especial_Picard_v2_916.mp4`, 29/10/2026)
| Critério | Alvo | Medido | OK |
|---|---|---|---|
| Resolução / fps | 1080×1920, 30 | 1080×1920, 30/1, 2097 quadros | sim |
| Codecs | H.264 + AAC 48 kHz | h264 + aac 48000 Hz | sim |
| Duração | pela história (§14) | 69,89 s | sim |
| Loudness integrado | −14 ±0,5 LUFS | −14,1 LUFS | sim |
| True peak | < −1 dBFS | −2,7 dBFS (loudnorm + limitador) | sim |
| cropdetect 24:2:0 | 1080:1920:0:0 | 2089/2097 = 1080:1920:0:0; os 8 restantes são a TV a ligar (0–0,2 s) e a encolher no "Engage" (67,0–67,4 s), preto por desenho | sim |
| Tela da TV inteira | laterais dentro do quadro | trava do kit em tv, tv2 e tvtext; conferido em 24 quadros do ficheiro final | sim |
| Carta inteira, nada por cima | — | 2 / 31 / 34,5 s (destaque translúcido só sobre as linhas do Seek out) | sim |
| Destaque alinhado ao texto | linhas do Seek out | 3 linhas, medidas no PNG, "Spacecraft." inteiro | sim |
| Lista e carimbo | legíveis | nomes 27 px, "NUNCA" 40 px na tela da TV (capa) | sim |
| Legenda queimada | zona segura | bottom 440 px, 19 blocos | sim |
| Bordões | intactos | "Lê a carta", "Comenta aí"; "Isso devia ser banido" virado do avesso de propósito | sim |
| Tom (§14) | celebração | luz de fim de tarde, música em Ré maior a 96 BPM, 4 momentos de humor, nenhum sobre a morte | sim |
| Publicidade | nenhuma | sem CTA, sem preço, sem app, sem scanner | sim |
| Fecho | forte | "Engage" → TV encolhe → ponto verde em arrancada → BINDER Originals + "Obrigado, capitão." (67,3 / 68,2 / 69,5 s) | sim |
| Pronúncia dos nomes | ouvida | NÃO conferida (ver Riscos) | pendente |

## Entregáveis
- [x] Vídeo · [x] Capa · [x] Legenda · [x] Comentário fixado · [x] SRT · [x] Guião definitivo · [x] Conceito e comparação · [x] Fontes
