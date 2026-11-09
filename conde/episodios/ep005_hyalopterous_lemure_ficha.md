# Ficha · Conde de Manaforte · EP005 · Hyalopterous Lemure: o réu que errou de mitologia

Estado a 09/11/2026: **em produção · roteiro por aprovar.** Existe uma prévia muda (tempos estimados, sem voz); **não é o episódio**. Voz, vídeo final e QC final dependem da aprovação do roteiro pelo fundador.
Scripts: `conde/montar_ep005.py` (copiado de `montar_ep004.py`), `conde/capa_ep005.py`, `conde/ep005/tempos_previa.py`. Dados: `conde/ep005/`.

## Classificação
- Série: Conde de Manaforte · O Tribunal Estético
- Classe: arte (comentário sobre uma obra) + bastidor da arte
- Complexidade: média
- Estratégia: análise estética + investigação (fonte primária da Wizards); observação / interpretação / facto separados
- Router: ilustração e bastidor de arte → Conde (`nucleo/SHOWRUNNER.md` §2.2). Réu escolhido pelo fundador e já na lista de candidatos (`conde/CONTEXTO.md` §10) e na opção A do Ep. 004.

## Editorial
- Objetivo: entreter o colecionador com o erro de arte mais famoso de Magic, contado com rigor, e levá-lo ao comentário fixado.
- Proposta de valor: o Conde elogia a sério uma ilustração que está tecnicamente certa e descobre que o réu é da espécie errada.
- Público: colecionadores, jogadores veteranos (Ice Age, Premodern, Old School) e apreciadores de ilustração.
- Hipótese a testar: um bastidor famoso com fonte primária gera mais guardados e partilhas do que a análise só visual do Ep. 004. Pergunta A/B com réus concretos (mantida do Ep. 004 para comparar).
- Tese: a arte de 1995 acerta no "hyalopterous" e falha no "lemure"; o erro é de identidade, não de execução.
- Gancho (0–3 s): "Meus caros apreciadores do duvidoso… O Tribunal recebe hoje um réu de 1995."

## Roteiro (para aprovação)

> **Nota:** a missão manda usar o roteiro fornecido pelo fundador como base. Esse roteiro **não veio anexado** e não está no repositório. Este texto foi escrito na fórmula de `conde/CONTEXTO.md` §3, cobrindo os 8 pontos pedidos (abertura, solenidade, análise verdadeira, revelação, facto, ferroada, veredito com carimbo, pergunta final). Se o fundador tiver o seu texto, troca-se em `conde/ep005/roteiro.txt` e corre-se `python3 conde/ep005/tempos_previa.py`; as cenas ancoram em palavras e ajustam-se.

Legendas (grafia real), 156 palavras, narração estimada ~65 s (+ fecho 3,87 s):

1. **Abertura** · Meus caros apreciadores do duvidoso... O Tribunal recebe hoje um réu de 1995. Hyalopterous Lemure.
2. **Análise séria** · Observem a composição: uma diagonal de gelo e, ao centro, um olho âmbar que não pede licença. As asas, translúcidas, nervuradas como as de um inseto. Hyalopterous: asas de vidro. Nisso, a obra é irrepreensível.
3. **A insolência** · Agora, o corpo. Pelagem densa. Máscara escura. Garras cravadas na rocha. Senhores... isto é um lêmure.
4. **A revelação** · Em inglês, lemur, sem "e", é o primata. Lemure, com "e", é um espírito dos mortos da Roma antiga.
5. **O facto** · Em 2003, Mark Rosewater, da Wizards, contou que os criadores de Ice Age queriam um espírito atormentado. A arte chegou com um mamífero felpudo.
6. **A ferroada** · O texto da carta jura que os Lemures pareciam inofensivos. Até restarem só os ossos. Na primeira metade, a ilustração concorda com a testemunha.
7. **Veredito** · Parecer: obra notável. A asa está certa. O olhar também. A criatura só errou de mitologia.
8. **Fecho** · Qual réu o Tribunal julga a seguir?

Decisões de texto:
- Sem culpa atribuída ao artista: a fala segue a formulação da Wizards ("a arte chegou com…"), sem dizer quem errou nem porquê. O artigo de Rosewater fala de um artista que desenhou o item errado; o que estava escrito no pedido de arte de 1995 não é público, por isso não se afirma.
- Em português "lêmure" serve para os dois sentidos; a diferença só existe em inglês (lemur/lemure). Por isso a fala diz "em inglês" e o painel mostra as duas grafias.
- "Mamífero felpudo" parafraseia "nocturnal, fuzzy mammal" (Rosewater). O painel diz "paráfrase".
- A ferroada usa o flavor completo: a primeira metade ("looked harmless") concorda com a arte; a segunda ("only bones remained") não. Daí "na primeira metade".
- Ficaram fora da fala (vão para o comentário): Lineu e o nome dos primatas; Viscid Lemures (2006).
- Duração: ~65 s, acima do Ep. 004 (55 s). Duração é livre (constituição §6). Se o fundador quiser encurtar, os cortes seguros são "Uma diagonal de gelo e," e "Até restarem só os ossos. Na primeira metade," (a ferroada fica "a ilustração concorda com a testemunha"), ~5 s.

### Texto para o TTS (só depois da aprovação)
Tags de `CONTEXTO.md` §4; grafia fonética a confirmar de ouvido (hipóteses, não testadas):

```
[calm, dry, aristocratic] Meus caros apreciadores do duvidoso... [pause] O Tribunal recebe hoje um réu de mil novecentos e noventa e cinco. Raialópterus Lêmiur. [pause] Observem a composição: uma diagonal de gelo e, ao centro, um olho âmbar que não pede licença. As asas, translúcidas, nervuradas como as de um inseto. Raialópterus: asas de vidro. Nisso, a obra é irrepreensível. [pause] [slow] Agora, o corpo. Pelagem densa. Máscara escura. Garras cravadas na rocha. [pause] [deadpan] Senhores... isto é um lêmure. [pause] Em inglês, lí-mur, sem "é", é o primata. Lêmiur, com "é", é um espírito dos mortos da Roma antiga. [pause] Em dois mil e três, Mark Rôuzuóter, da Uízards, contou que os criadores de Ais Eidj queriam um espírito atormentado. A arte chegou com um mamífero felpudo. [pause] O texto da carta jura que os Lêmiurs pareciam inofensivos. Até restarem só os ossos. [slow] Na primeira metade, [deadpan] a ilustração concorda com a testemunha. [pause] Parecer: obra notável. A asa está certa. O olhar também. A criatura só errou de mitologia. [pause] Qual réu o Tribunal julga a seguir?
```
Depois: Scribe → copiar `encurtar_narracao_ep004.py` para `encurtar_narracao_ep005.py` (GRAFIA: Raialópterus→Hyalopterous, Lêmiur→Lemure, lí-mur→lemur, Rôuzuóter→Rosewater, Uízards→Wizards, Ais Eidj→Ice Age, "é"→"e", mil novecentos…→1995., dois mil e três→2003,) → `narracao.wav` + `words_novo.json` → `python3 conde/montar_ep005.py` (sai da prévia sozinho).

## Camadas
| Camada | No episódio |
|---|---|
| Observação (verificável pausando) | diagonal de gelo; olho âmbar ao centro; asa translúcida com nervuras; pelagem; máscara escura à volta do olho; garras na rocha; linha impressa "Summon Lemure" |
| Interpretação (opinião do Conde) | "não pede licença", "irrepreensível", "isto é um lêmure", "obra notável", "errou de mitologia", a ilustração "concorda com a testemunha" |
| Facto (com fonte) | dados e flavor da carta (Scryfall); significado de lemure e lemur; relato de Rosewater, 10/11/2003 |

## Fontes e evidências
| Afirmação | Tipo | Fonte | Data |
|---|---|---|---|
| Ice Age, 1995, nº 133, Richard Thomas, flavor de Lucilde Fiksdotter | facto | https://scryfall.com/card/ice/133/hyalopterous-lemure | consulta 09/11/2026 |
| Lemure = espírito torturado dos mortos; designers queriam essa criatura; a arte chegou como lemur, mamífero noturno e felpudo | facto (fonte primária, atribuído) | Mark Rosewater, "Make No Mistake", Making Magic, 10/11/2003 | 10/11/2003 |
| A entrada do Lemure tem 1 erro escondido, que é o artista de Urza's Mine (não o Lemure) | facto | Rosewater, "Up, Up and Away", 17/11/2003 | 17/11/2003 |
| Lemures: espíritos dos mortos sem descanso na religião romana | facto | https://en.wikipedia.org/wiki/Lemures | consulta 09/11/2026 |
| Hyalopterous = hýalos (vidro) + pterón (asa) | facto lexical (composição) | etimologia grega; Commander's Herald como apoio | consulta 09/11/2026 |
| Lineu deu o nome aos primatas por andarem de noite e devagar (só no comentário) | facto | etymonline (Dunkel et al., Lemur News 16) | consulta 09/11/2026 |
Lista completa, notas de acesso e fontes rejeitadas: `ep005_fontes.txt`.

## Plano visual (como está na prévia)
| # | Plano pedido | Trecho | Execução |
|---|---|---|---|
| 1 | Conde e Tribunal | 0–2,5 s | medalhão em escala, cabeçalho do Tribunal |
| 2 | Entrada integral da carta | 2,5–6,9 s | carta inteira; "RÉU · 1995" na margem esquerda; nome destacado |
| — | Composição | 6,9–13,2 s | arte inteira em largura total; seta de tinta pela diagonal; lupa no olho |
| 3 | Asas translúcidas | 13,2–21,7 s | elipse na asa; inserto "admirado" sobre o gelo em "irrepreensível" |
| 4 | Corpo da criatura | 21,7–29,5 s | elipses sucessivas: pelagem, máscara, garras; inserto "desconfiado" → "indignado" |
| 5 | lemur ≠ lemure | 29,5–36,4 s | painel de papel (verbete) no lugar do palco; "e" em bordô |
| 6 | Facto histórico | 36,4–45,8 s | painel "Make No Mistake · Mark Rosewater · 10/11/2003", paráfrase marcada |
| — | Ferroada | 45,8–55,5 s | carta inteira; flavor destacado por partes; depois arte + 1.ª metade |
| 7 | Veredito e carimbo | 55,5–62,4 s | carta inteira; destaques asa → olho → arte; "OBRA NOTÁVEL" na margem direita |
| 8 | Fecho oficial | 62,4 s → | Conde + "PARECER EMITIDO" + A/B; depois `outro_binder_916.mp4` |

Regras cumpridas por desenho: nenhum texto por cima da ilustração (rótulos passaram para painéis de papel; na arte só seta, elipses, lupa e o inserto do Conde sobre o gelo); carimbos nas margens da carta; arte e carta sempre inteiras (sem zoom). Tempos a reconfirmar com a voz real.

## Produção
- Recursos reutilizados: medalhão e 4 expressões (sem alteração), paleta e Lora, layout e motor do Ep. 004, tema "Verdict in Varnish and Vellum", fecho oficial.
- Novo no motor (só neste script): painéis de papel; música com uma volta extra de 16 pulsos quando a narração passa do tema (a emenda é a mesma do Ep. 004); âncoras de música calculadas (andamento 0,94–1,03); modo prévia.
- Música (prévia): 1 volta extra; pulsos em RÉU, verbete, Rosewater, flavor, OBRA NOTÁVEL, PARECER EMITIDO e no corte para o fecho. O trecho final corre a 0,943: conferir de ouvido com a voz real.
- Easter egg: nenhum.
- Riscos: pronúncia de "Hyalopterous", "Lemure", "lemur", "Rosewater" (hipóteses fonéticas acima); duração.

## Controlo de qualidade da PRÉVIA (09/11/2026, não vale como QC final)
| Critério | Resultado |
|---|---|
| `qc_video.py --frente conde` | sem problemas mensuráveis |
| Formato | 1080×1920, 30 fps |
| Duração | 66,0 s + fecho = 69,87 s (tempos estimados) |
| Loudness | −13,8 LUFS, pico −1,9 dBTP (só música e carimbos: não representa a mistura com voz) |
| Fecho oficial | presente a partir de 66,0 s (dif. 0,06) |
| Folha de contacto | vista: carta e arte inteiras em todos os planos; legendas na zona segura; nenhum texto sobre a arte ou o rosto; arte em largura total entra nos 140 px da margem direita, como em todos os episódios do Conde |
| Voz, sincronia, mistura | **não testáveis** (sem voz) |

## Entregáveis
- [ ] Vídeo final (depende da voz) · [x] Prévia muda · [x] Capa `EP005_CONDE_LEMURE_capa.jpg` (gerada por `capa_ep005.py`; não versionada) · [x] Legenda · [x] Comentário fixado · [x] Texto alternativo · [x] Fontes

## Depois de publicar
- Métrica principal: respostas A/B + guardados (comparar com o Ep. 004).
- Resultado observado: (aguarda)
- Aprendizagem: (por preencher)
