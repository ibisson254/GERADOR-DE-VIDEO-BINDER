# Auditoria crítica · prova de recorte de 19/11/2026

**Ficheiro auditado:** `prova_lisa_recorte.mp4` (gerado por `kit/prova_recorte/motor_recorte.py`, entregue na conversa a 19/11, não versionado). A identidade foi confirmada pelos metadados e pela imagem: Lisa, look 1, sobre o estúdio vetorial do kit, com a fala «Oi! Eu sou a Lisa Marie…».

| Medida | Valor (ffprobe / ebur128) |
|---|---|
| Vídeo | H.264, 1080×1920, 30 fps, 5,80 s, 3,1 Mb/s |
| Áudio | AAC mono **96 kHz**, 182 kb/s |
| Loudness | −15,6 LUFS integrado, LRA 2,2 LU, **pico −0,4 dBFS** |
| Cortes | 1 corte em 2,40 s (plano médio → grande plano) + flash rosa de 2 quadros |
| Origem da arte | 262×513 px (look 1 da prancha), ampliada 4× (Lanczos) e depois ×0,82 no plano médio e ×1,5 no grande plano: ≈3,3× e ≈5× da origem |

Folha de contacto a 2 fps e análise sem som e com som feitas a 21/11.

## Análise por timecode

| Timecode | O que acontece | O que funciona | Problema | Grav. | Correção executada no LM-EP01 |
|---|---|---|---|---|---|
| 0,00–0,54 | Plano médio, «Oi!», legenda sobre o peito | Entrada imediata, boca abre no «Oi» | Começa pela apresentação da personagem, sem assunto: zero motivo para ficar | P0 (editorial) | Quadro 0 com a obra real (Coat of Arms) e a pergunta da Lisa sobre ela |
| 0,00–2,40 | Lisa encara a câmara o tempo todo | Respiração e balanço discretos | **Olhar fixo**: os olhos nunca mudam de direção. A personagem não «vê» nada, por isso não apresenta nada | P1 | Íris com direção (esquerda, direita, cima) e cabeça separada do corpo: olha para a carta e volta à câmara para perguntar |
| 0,40–2,40 | Tarja «LISA MARIE · VJ DO MULTIVERSO», legenda e aviso no topo ao mesmo tempo | Tarja legível e na paleta | 3 textos simultâneos; a tarja fica o plano inteiro | P1 | Uma frase principal por momento; a tarja entra só na primeira fala longa e sai |
| 0,99–2,24 | «Eu sou a Lisa Marie» com bocas Rhubarb | A sincronização acompanha as sílabas | Bocas vetoriais, de traço grosso e cor plana: parecem um autocolante sobre a pintura, e há trocas de 1 quadro que fazem a boca tremer | P1 | Bocas v2 com traço mais fino, tinta quente e suavização; segmentos de menos de 2 quadros fundidos |
| 1,30 / 3,70 / 5,20 | Piscar (pálpebra em elipse) | O piscar dá vida | No fechado, a elipse preta lê-se como um borrão | P2 | Mantido (sem arte nova não há solução honesta); fica registado para a ilustradora |
| 0,00–5,80 | Estúdio vetorial plano por trás | Paleta coerente com a série | Dois estilos em choque (vetor plano × ilustração pintada), sem sombra nem assentamento: a personagem parece colada | P1 | Filmagem urbana real tratada (exposição, saturação, realces comprimidos, vinheta, desfoque), sombra suave, harmonização de 6%, base escurecida e grão comum |
| 2,40–2,47 | Corte com flash rosa e scanlines | Marca o corte | Efeito sem função narrativa | P2 | Removido. Os cortes passam a ser motivados pelo conteúdo, e o Flip só existe entre cartas |
| 2,40–5,80 | Grande plano ≈5× da origem | A expressão lê-se melhor | Imagem mole, recorte serrilhado, papel da prancha visível junto ao pescoço | P1 | Grande plano limitado a ≈3× da origem e plano médio a ≈2× (35–55% da altura); papel limpo em `camadas.py` |
| 2,48–4,63 | «Isso aqui é um teste de boca» | — | A fala descreve a técnica, não um assunto | P0 (editorial) | Guião com pauta real e fontes |
| todo | Voz Piper masculina com tom subido | Permite testar a boca sem custo | Timbre robótico; pico −0,4 dBFS (acima de −1); 96 kHz | P1 | Continua provisória (não há voz aprovada), mas mais natural: formantes preservados, tempo 1,22, realce a 3 kHz, pico ≤ −2 dBFS, 48 kHz na entrega |
| todo | Lisa sozinha no quadro | Presença grande | Não há hierarquia: a personagem é o assunto | P0 (editorial) | Hierarquia: obra → Lisa → legenda → grafismos → cidade. Lisa sai de quadro nas cenas de análise |

## Notas (1–5) da prova original

| Critério | Nota | Evidência |
|---|---|---|
| 1. Presença da personagem | 3 | Ocupa o quadro e respira, mas não reage a nada nem olha para nada |
| 2. Expressividade dos olhos | 1 | Olhar sempre ao centro; só o piscar muda |
| 3. Naturalidade da boca | 2 | Sincronização certa, mas com desenho de autocolante e trocas de 1 quadro |
| 4. Integração com o cenário | 1 | Estilos em choque e nenhuma sombra |
| 5. Hierarquia visual | 2 | Três textos ao mesmo tempo e nenhum assunto para hierarquizar |
| 6. Legibilidade | 4 | Anton grande e contornado, dentro da zona segura |
| 7. Ritmo | 3 | Um corte em 5,8 s; para a duração serve, mas o corte não tem motivo |
| 8. Coerência editorial | 1 | Não há pauta; quadro 0 sem Magic |
| 9. Potencial de retenção | 1 | Nada promete uma descoberta |
| 10. Reconhecibilidade da Lisa | 3 | Silhueta, óculos e auscultadores leem-se bem; falta um comportamento próprio |

## Pergunta principal

**O que impede a Lisa de parecer uma apresentadora cultural, em vez de uma ilustração animada sobre um fundo?**

Ela **não olha para nada e não tem nada para mostrar**. Uma apresentadora existe em relação a uma evidência: aponta-a com o olhar, reage-lhe e volta ao público com uma leitura. Na prova, a Lisa encara a câmara 100% do tempo, fala de si mesma, não tem assunto e está colada sobre um fundo de outro estilo. A técnica (Rhubarb, piscar, respiração) funciona. O que falta é atenção dirigida e matéria editorial.

## As cinco melhorias de maior impacto (todas executadas)

1. **Assunto real no quadro 0** (obra oficial), com a Lisa a entrar sobre a evidência.
2. **Olhar e cabeça com intenção:** íris com direção e cabeça separada do corpo (olha para a carta, pensa, volta à câmara).
3. **Hierarquia e saída de quadro:** a carta ocupa o ecrã nas análises, uma frase principal por momento, tarja só quando informa.
4. **Integração com cidade real:** tratamento de cor, controlo de realces, sombra, assentamento e grão.
5. **Boca menos «autocolante» e sem tremor:** bocas v2 e fusão de segmentos curtos do Rhubarb. Voz provisória menos robótica e com pico corrigido.

Não melhorado de propósito (não muda o resultado sem arte nova): a elipse preta do piscar e a resolução da arte-conceito. Ambos ficam para a encomenda à ilustradora (`BRIEFING_ILUSTRADORA.md`).
