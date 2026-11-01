# Ficha · <FRENTE> · EP<NN> · <tema curto>

Copiar para a pasta do episódio (`<pasta da frente>/episodios/epNN_<slug>/ficha.md`; especiais entre séries em `especiais/<nome>/ficha.md`). Preencher só o que acrescenta valor; campos marcados * são obrigatórios. O encerramento (fim desta ficha) é obrigatório: o episódio só se dá por arquivado quando a ficha e o pacote estão no GitHub (`nucleo/SHOWRUNNER.md` §6).

## Identificação*
- ID editorial*: (linha em `comum/REGISTRO_EDITORIAL.md`, ex.: `MB-EP10`)
- Estado no registo*: IDEIA · EM ANÁLISE · APROVADO · EM PRODUÇÃO · CONCLUÍDO · PUBLICADO
- Aprovação do fundador (data e onde): 

## Classificação*
- Frente*:
- Classe de conteúdo*: (leitura de carta · jogada · meta · notícia · tendência · mercado · arte · artista · história · opinião · promocional)
- Complexidade: baixa / média / alta
- Estratégia (constituição §3): 

## Originalidade*
- Objeto (carta, pessoa, deck, evento)*: 
- Resultado de `python3 comum/ferramentas/memoria.py pauta --objeto "…" --tema "…"`*: LIVRE / BLOQUEADA (IDs)
- Se bloqueada: decisão do fundador que liberta (data em `nucleo/DECISOES.md`) e porque o ângulo é novo:
- Relações com conteúdos anteriores (IDs): 

## Editorial (briefing)
- Objetivo*: 
- Proposta de valor numa frase*: 
- Público: 
- Hipótese a testar (o que esperamos aprender): 
- Tese: 
- Gancho (0–3 s)*: 

## Roteiro definitivo*
(Texto final tal como foi gravado, ou caminho do ficheiro: `roteiro.json`, `episode.json`, `guiao_definitivo.md`.)

## Fontes e evidências*
| Afirmação | Tipo (facto/inferência/opinião/previsão) | Fonte (URL) | Data |
|---|---|---|---|
| | | | |

## Produção
- Recursos reutilizados: 
- Estrutura narrativa: 
- Ferramentas confirmadas disponíveis: 
- Vozes e créditos gastos: 
- Easter egg (0 ou 1): 
- Riscos (factuais, técnicos, direitos): 
- Limitações conhecidas: 

## Controlo de qualidade*
Medido no ficheiro final (não na prévia), com `nucleo/CHECKLIST_QUALIDADE.md` e os critérios do perfil.

| Critério | Alvo | Medido | OK |
|---|---|---|---|
| Resolução / fps | formato da frente | | |
| Duração | perfil (ou especial §14) | | |
| Corte lateral (cropdetect) | nenhum | | |
| Loudness / pico | −14 LUFS / < −1 dBFS | | |
| Fecho do scanner | presente (exceto Órbita e exceções registadas) | | |
| Factos = ficha | sim | | |

## Ficheiros finais*
Vídeos renderizados não entram no Git. Registar onde estão:
- Vídeo final: `<nome>.mp4` · duração · onde está (ex.: entregue ao fundador na conversa de DD/MM, Drive `<pasta>`, máquina do fundador)
- Capa: `<nome>.jpg` · onde está
- Carrossel / Stories (se houver): 

## Pacote de publicação* (ficheiros nesta pasta)
- [ ] `legenda.txt` (PT-BR, "você", termina com "baixe o BINDER Vision", até 5 hashtags, sem emojis)
- [ ] `comentario_fixado.txt`
- [ ] `texto_alternativo.txt`
- [ ] Fontes: tabela acima ou `fontes.md`

## Encerramento* (`nucleo/SHOWRUNNER.md` §6)
- [ ] Briefing e roteiro definitivo nesta ficha
- [ ] Legenda, comentário fixado e texto alternativo na pasta
- [ ] Fontes e evidências
- [ ] Controlo de qualidade preenchido
- [ ] Localização do vídeo e da capa (secção "Ficheiros finais")
- [ ] `comum/REGISTRO_EDITORIAL.md` atualizado (estado CONCLUÍDO, ficha, relações, originalidade)
- [ ] `comum/historico.md` com uma linha com o ID
- [ ] Easter egg em `comum/easter_eggs.md` (se houver)
- [ ] `STATUS.md` (se mudou o estado do estúdio)
- [ ] `python3 comum/ferramentas/memoria.py encerramento <ID>` = ENCERRAMENTO OK
- [ ] Commit enviado e conferido no GitHub (hash: )
- [ ] Handoff entregue

## Depois de publicar
- Data e hora de publicação (confirmada por): 
- Métrica principal (do perfil): 
- Resultado observado (`comum/insights/semanas/…`): 
- Aprendizagem: 
