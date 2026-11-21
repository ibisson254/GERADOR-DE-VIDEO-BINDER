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

## Pesquisa de pauta* (`nucleo/SHOWRUNNER.md` §2.4)
- Reação-alvo da personagem: 
- Candidatos (≥ 3 em série/especial; ≥ 2 em Lambe-lambe/Órbita; ≥ 2 ângulos se o tema veio do fundador), cada um com os 9 campos: 
- Rubrica (1–5: gancho, originalidade, compreensão, visual, compartilhamento, recompensa, adequação à personagem) e totais: 
- Vencedor e porque supera os outros*: 
- Reserva (candidatos preteridos, sem entrar no registo): 
- Limitações das fontes (o que não abriu ou não se confirmou e saiu do vídeo): 

## Editorial (briefing)
- Objetivo*: 
- Proposta de valor numa frase*: 
- Público: 
- Hipótese a testar (o que esperamos aprender): 
- Variável em teste (0 ou 1; peça de comparação; `comum/insights/LEIA-ME.md`): 
- Tese (uma frase)*: 

## Gancho visual* (`nucleo/SHOWRUNNER.md` §4.1; preencher antes do roteiro)
1. Quadro 0 (o que se vê, sem áudio)*: 
2. Objeto real que prende o olhar*: 
3. Ação no primeiro segundo*: 
4. Som que reforça a ação*: 
5. Descoberta ou pergunta até 3 s*: 
6. Promessa*: 
7. Pagamento (segundo e imagem)*: 

Abertura de objeto* (§4.1.1): objeto em tela cheia · prova marcada e selo · instante de saída (palavra do gancho e segundo) · saída para o mundo da personagem · som. Medido no final: 

| Rubrica (1–5) | Prevista | Medida no final |
|---|---|---|
| Relevância visual | | |
| Impacto inicial | | |
| Clareza | | |
| Curiosidade | | |
| Pagamento | | |
| Identidade | | |

## Roteiro definitivo*
(Texto final tal como foi gravado, ou caminho do ficheiro: `roteiro.json`, `episode.json`, `guiao_definitivo.md`.)

## Fontes e evidências*
| Afirmação | Tipo (facto/cálculo/inferência/opinião/previsão) | Fonte (URL) | Data |
|---|---|---|---|
| | | | |

Limitações (amostra, período, o que a fonte não publica): 
Capturas ou exportações guardadas em: 
Créditos e autorizações de terceiros (`<frente>/autorizacoes/`): 

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
| Quadro 0 | campo 1 do gancho, legível sem som | | |
| Descoberta | ≤ 3,0 s | | |
| Pagamento do gancho | segundo do campo 7 (± 3 s) | | |
| Maior intervalo sem mudança visual | ≤ 3 s | | |
| Retenção | quadro 0 com Magic · mudança ≤ 3 s · som em cada revelação | | |
| P0 / P1 abertos | 0 / 0 (ou P1 aceites por escrito) | | |

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
