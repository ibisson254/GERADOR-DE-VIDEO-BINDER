# Ficha · Conde de Manaforte · EP004 · Joven: o réu que não explica nada

Render final de 03/11/2026 (55,1 s sem o fecho; 58,97 s no total). **Produzido, não publicado.**
Scripts: `conde/montar_ep004.py` (copiado de `montar_ep003.py`), `conde/encurtar_narracao_ep004.py`. Dados: `conde/ep004/`.

## Classificação
- Série: Conde de Manaforte · O Tribunal Estético
- Classe: comentário sobre uma obra
- Complexidade: baixa
- Estratégia: análise estética (observação / interpretação / facto separados); só análise visual, sem bastidores nem intenção artística

## Editorial
- Objetivo: entreter o colecionador e levá-lo ao comentário fixado e à legenda.
- Proposta de valor: um retrato de autoridade cuja legenda de ambientação desmonta a reputação do retratado.
- Público: colecionadores e apreciadores de ilustração de Magic.
- Hipótese a testar: pergunta A/B com dois réus concretos gera mais respostas do que a pergunta sobre a obra do Ep. 003.
- Gancho (0–3 s): "Meus caros apreciadores do duvidoso… Apresento-lhes Joven."

## Narração final
Meus caros apreciadores do duvidoso… Apresento-lhes Joven. Observem a postura. Os braços cruzados. O olhar. A serenidade de quem parece acreditar que o mundo inteiro está aguardando sua próxima decisão. A composição nos oferece um homem que não parece disposto a explicar absolutamente nada. E talvez nem precise. Afinal, sua especialidade é destruir artefatos. Os que não são criaturas. Três manas vermelhos, um gesto de exaustão… e um objeto deixa de fazer parte da paisagem. No texto da carta, o próprio Chandler concede que Joven é quase tão bom ladrão quanto ele. Mas Eron o detesta ainda mais. Uma reputação, convenhamos, bastante específica. Parecer: obra notável. Um retrato de autoridade, autoconfiança e uma quantidade admirável de problemas com a vizinhança. Qual réu o Tribunal julga a seguir?

## Correções factuais ao roteiro aprovado
1. A habilidade só destrói artefatos **que não são criaturas** (Oracle): acrescentado "Os que não são criaturas."
2. O flavor é **uma fala de Chandler**, não uma informação da carta: a frase passou de "O próprio texto da carta informa que Joven é…" para "No texto da carta, o próprio Chandler concede que Joven é quase tão bom ladrão quanto ele. Mas Eron o detesta ainda mais."

## Camadas
| Camada | No episódio |
|---|---|
| Observação | braços cruzados; olhos pintados de preto; figura vista de baixo; placa ao fundo |
| Interpretação (opinião do Conde) | serenidade, "não disposto a explicar", "problemas com a vizinhança", "obra notável" |
| Facto (fonte) | dados da carta, Oracle e flavor |

## Fontes e evidências
| Afirmação | Tipo | Fonte | Data |
|---|---|---|---|
| Joven, Homelands, 1995, nº 77, Douglas Shuler; custo da habilidade | facto | https://scryfall.com/card/hml/77/joven | 03/11/2026 |
| Oracle e flavor (fala de Chandler) | facto | idem | 03/11/2026 |
Lista completa: `ep004_fontes.txt`.

## Produção
- Recursos reutilizados: medalhão e 4 expressões, tema, layout e motor do Ep. 003, fecho oficial.
- Voz: 1 geração, 909 créditos; take de 66,5 s. Grafia fonética no TTS para Joven, Chandler e Eron. atempo 1,15 (como o Ep. 003), sem cortar frases.
- Música (sincronia revista a 03/11): grelha medida no tema (136 BPM, fase 0,03 s); emenda em 22,09 s, recuo de 16 pulsos, crossfade 0,25 s; entrada 0,22 s depois do início; andamento ajustado entre âncoras (0,963–1,000, sem mudar a altura) para os pulsos caírem em RÉU, na entrada da habilidade, na entrada do texto de ambientação, em OBRA NOTÁVEL, em PARECER EMITIDO e no corte para o fecho (erro medido ≤ 24 ms). O fim real do tema cai sob o fade do fecho. Sting em 3 carimbos.
- Arte: art_crop 582×467 → palco 1080×867, largura total.
- Easter egg: nenhum.

## Decisões de montagem
- **Sem zoom na arte:** a aproximação ao olhar é feita com a lupa, para a arte continuar inteira (checklist E).
- **Inserto e carimbo do veredito** na coluna da parede, à esquerda, fora da figura; carimbo de réu na margem da carta. Assinatura do artista livre.
- **Placa ao fundo** marcada como "a vizinhança" (ligação visual à fala). Lê-se "SNARGS HOUSE OF"; a terceira linha fica como pergunta, sem transcrição afirmada.
- **Ecrã final:** A · Hyalopterous Lemure ou B · Sorrow's Path (candidatos de `conde/CONTEXTO.md` §10), para a pergunta da fala ter resposta de uma letra.
- **Legenda:** hashtags antes da linha final, para terminar mesmo em "baixe o BINDER Vision".

## Controlo de qualidade (ficheiro final, 03/11/2026)
| Critério | Resultado |
|---|---|
| `qc_video.py --frente conde` | sem problemas mensuráveis |
| Formato | 1080×1920, 30 fps, H.264 + AAC 48 kHz |
| Duração | 55,1 s + fecho = 58,97 s |
| Loudness | −13,9 LUFS, pico −1,5 dBTP |
| Fecho oficial | presente a partir de 55,1 s (dif. 0,06) |
| Corte lateral | crop=1080:1920:0:0 nos 1653 quadros medidos do episódio |
| Quadros vistos | folha de contacto (1 quadro/s) e quadros extraídos do MP4 final |
| Defeito corrigido | clarão de papel vazio nas transições, elipse sobre o crédito, música curta para o fecho |
| Pronúncia e mistura | **não conferidas de ouvido** (sem audição nesta sessão; o Scribe recebeu alinhamento, não serve de prova) |

## Limitações conhecidas
- Pronúncia de "Joven", "Chandler" e "Eron" por ouvir.
- A arte em largura total entra nos 140 px da margem direita da zona segura, como em todos os episódios do Conde; textos e legendas ficam fora.
- A carta fica em ecrã cerca de 19 s (21–40 s); os destaques mudam, mas é o trecho mais parado.

## Entregáveis
- [x] Vídeo `EP004_CONDE_JOVEN.mp4` · [x] Capa `EP004_CONDE_JOVEN_capa.jpg` · [x] Legenda · [x] Comentário fixado · [x] Texto alternativo · [x] Fontes

## Depois de publicar
- Métrica principal: respostas A/B + guardados.
- Resultado observado: (aguarda o print do Insights)
- Aprendizagem: (por preencher)
