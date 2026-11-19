# Missão estrutural · evolução contínua, padrão profissional e retenção visual

19/11/2026 · Claude (sessão do projeto «Binder Marketing») · pedido do fundador com o mesmo título. Decisão registada em `nucleo/DECISOES.md` (19/11).

Âmbito: documentação e processo. Nada publicado, nenhuma mensagem enviada, nenhum crédito externo gasto, nenhum conteúdo publicado ou aprovado reaberto, nenhum ficheiro apagado.

## 1. Diagnóstico

A estrutura está sólida no que é **rigor e arquivo** (constituição, registo editorial, encerramento, validação automática no GitHub, registo de previsões do TUBO). Os pontos fracos estavam na **preparação**:

- O gancho existia como regra (constituição §6, 13/11; TUBO §7, 16/11; feedback visual, 15/11), mas entrava no briefing como uma linha («Gancho (0–3 s)») e era resolvido na montagem. Não havia campos para som, promessa nem segundo do pagamento, e nada media se a promessa foi paga.
- As regras de retenção estavam espalhadas por quatro sítios (constituição, DECISOES, perfis, checklist) e a ficha não tinha onde as conferir: a linha «Retenção» pedida pelo encerramento (`SHOWRUNNER.md` §6) não estava no modelo de ficha nem é verificada pelo `memoria.py`.
- Os gates P0/P1/P2 não cobriam identidade incorreta nem áudio defeituoso como bloqueadores, e o bloqueador «falta o fecho» ignorava as exceções já aprovadas.
- A aprendizagem tinha regra (constituição §12) mas não método de teste: a base do Mana & Burn (MB-EP11) foi fixada sobre um post com ≈57 % de views pagas, e os dados que o provam estão fora da `main`.
- Os perfis de duas frentes (TUBO e Vince) não acompanharam decisões posteriores.

## 2. Inconsistências encontradas

| # | Onde | Problema | Tipo | Estado |
|---|---|---|---|---|
| 1 | `oraculo/PERFIL.md` «Gancho» | «frase seca fora do tubo» contradiz `CONTEXTO.md` §7 (cartas no quadro 0, abre dentro do tubo, 16/11) | contraditória | corrigida |
| 2 | `oraculo/PERFIL.md` e `CONTEXTO.md` §7.2.4 | previsões registadas em `comum/historico.md`; desde 09–10/11 o canónico é `previsoes/registo.yaml` | contraditória | corrigida |
| 3 | TUBO, duração | constituição §6 «duração livre» × `CONTEXTO.md` §7 «25–35 s» (16/11) | interpretável de duas formas | explicitado no perfil: a decisão de 16/11 prevalece nesta série |
| 4 | `oraculo/CONTEXTO.md` §7 | regras numeradas 1, 6, 2, 3, 4, 5 | forma | corrigida (6 no fim) |
| 5 | `CHECKLIST_QUALIDADE.md` | quadro 0 de Magic é P1 em geral e P0 no TUBO, sem nota; o fundador disse «sempre» a 15/11 | interpretável | anotado; subir a P0 em todas as frentes fica para decisão (§8) |
| 6 | `CHECKLIST_QUALIDADE.md` bloqueador 4 e `AGENTS.md` §2 | «falta o fecho» sem as exceções de Órbita e Expedição (14/11) | contraditória | corrigida |
| 7 | `CHECKLIST_QUALIDADE.md` | P0 sem identidade incorreta, áudio defeituoso, parceria não autorizada, promessa não paga | critério em falta | corrigida |
| 8 | `SHOWRUNNER.md` §6 × modelo de ficha × `memoria.py` | linha «Retenção» exigida, sem campo no modelo e sem verificação automática | existe e não é verificado | campo criado na ficha; verificação automática proposta (§8) |
| 9 | constituição §6 «mudança visual ≤ 3 s» | sem medição prevista | existe e não é verificado | item P1 no bloco F e linha na ficha (cortes do `qc_video.py`) |
| 10 | `vince/PERFIL.md` | título «Vinci», «voz por escolher», 30–45 s fixos, depois da reconciliação de 12/11 | contraditória | corrigida (nome, voz mantida, duração livre com referência) |
| 11 | `nucleo/DECISOES.md` | «mais recente no topo», mas as entradas de 15/11 (ABISMO) e 16/11 estão no fim | forma | anotada na entrada de 19/11; não reordenado |
| 12 | MB-EP11 (Numot) | perfil chama-lhe base da série pelas 7.138 views sem dizer que ≈57 % foram pagas; pacote em `manaburn/ep10-numot`, snapshots em `insights/2026-11-13-numot` e `insights/2026-11-14`, fora da `main`; sem linha no registo; impulso `SIM` (13/11) × `A CONFIRMAR` (14/11) | melhoria não integrada + dado contraditório | contexto escrito no perfil; integração pendente (§8) |
| 13 | `comum/insights/` na `main` | último snapshot de 31/10; os de 13/11 e 14/11 estão em branches | melhoria não integrada | pendente (§8) |
| 14 | `STATUS.md` | «registo desatualizado desde 01/11» (já tem 98 conteúdos, atualizado a 16/11); vidIQ «ligado à conta pessoal» × instruções do projeto «@binder_vision ligada» | desatualizado | primeira corrigida; vidIQ a confirmar (§8) |
| 15 | `comum/parcerias.md`, `STATUS.md` | MC-ESP03 com MTGDC500 / Lotus Games como dono dos dados e alvo da collab | correção do fundador | corrigida |
| 16 | `AGENTS.md`, catálogo, `series.yaml` | ABISMO (kit aprovado a 15/11) não aparece em nenhum dos três; Expedição não está na tabela do `AGENTS.md` | melhoria não integrada | pendente (§8) |
| 17 | Regras de retenção | a mesma regra («quadro 0 com Magic») escrita em 5 sítios com redações diferentes | duplicada | não se apagou nada; `SHOWRUNNER.md` §4.1 passa a ser o ponto operacional único e os perfis remetem para ele |
| 18 | Skills `binder-*` | ainda mandam ler o Drive primeiro | conhecida | continua pendente (STATUS) |

## 3. Sistema de gancho visual consolidado

Canónico em `nucleo/SHOWRUNNER.md` §4.1 (princípio na constituição §6):

1. **7 campos antes do roteiro:** quadro 0 · objeto real · ação no 1.º segundo · som · descoberta até 3 s · promessa · pagamento (segundo e imagem). Sem eles não há roteiro nem voz.
2. **Regras comuns:** específico da história (teste da troca de carta); nunca logótipo, título ou apresentação antes da evidência (os bordões correm por cima dela); quadro 0 legível sem som; som que reforça sem volume acima do alvo; promessa sempre paga.
3. **Aplicação por frente:** tabela com o mínimo de cada uma e o ponteiro para a bíblia. TUBO: grelha do MC-ESP01. Mana & Burn: carta na TV SAL + dor da mesa e número. Conde: a obra ou o detalhe por baixo da abertura, nunca estatística. Vince: carta + número + data, só 2D aprovado. Órbita: carta inteira desde o quadro 0, sem áudio no ficheiro. Lambe-lambe: o objeto no 1.º slide.
4. **Rubrica 1–5** (relevância, impacto, clareza, curiosidade, pagamento, identidade) prevista no briefing e medida no ficheiro final; Pagamento 1 = P0; ≤ 2 em relevância, clareza ou identidade = P1; nunca decide um vencedor sem Insights.

## 4. Critérios de qualidade profissional

- **Gates** (`CHECKLIST_QUALIDADE.md`): tabela P0/P1/P2 com consequência; 12 bloqueadores medíveis (inclui identidade incorreta, áudio defeituoso, parceria não autorizada, promessa não paga); «nenhuma média compensa um P0»; critérios em segundos, píxeis, LUFS ou sim/não.
- **Bloco F** (gancho e narrativa): 9 itens com limiar (3,0 s, ± 3 s do pagamento, intervalo ≤ 3 s, notas da rubrica).
- **Revisão narrativa** (`SHOWRUNNER.md` §4.2): 9 critérios de sim/não antes da voz e lista do que se corta.
- **Rigor** (constituição §4 e §7): tipo «cálculo», limitações e capturas guardadas na ficha; crédito ≠ parceria; nunca afirmar colaboração sem autorização registada.
- **Resultados** (`comum/insights/LEIA-ME.md`): métricas que se leem e só essas; comparação só entre peças equivalentes (frente, formato, idade, impulso); testes de uma variável com leitura a 48 h e 7 dias; um par não muda regra.

## 5. Alterações documentais

| Ficheiro | Alteração | Justificação |
|---|---|---|
| `nucleo/SHOWRUNNER.md` | §4 itens 9–11; §4.1 gancho (campos, regras, frentes, rubrica); §4.2 revisão narrativa; §6 passo 6; §7 testes | missão §2–5; o briefing é o sítio onde o gancho nasce |
| `nucleo/CONSTITUICAO_EDITORIAL_BINDER_ORIGINALS.md` | v1.7: §4 «cálculo», limitações, capturas; §6 gancho no briefing; §7 parceiros | princípio curto; detalhe fica no Showrunner (sem duplicar) |
| `nucleo/CHECKLIST_QUALIDADE.md` | gates consolidados, bloqueadores 1–12, nota no quadro 0, bloco F | missão §8 |
| `nucleo/modelos/FICHA_EPISODIO.md` | variável em teste; secção «Gancho visual» + rubrica; tipo cálculo, limitações, capturas, autorizações; 6 linhas novas no controlo de qualidade | o critério passa a ter onde ser conferido |
| `comum/insights/LEIA-ME.md` | secção «Avaliar resultados e testes comparáveis» | missão §7 |
| `oraculo/PERFIL.md`, `oraculo/CONTEXTO.md` | gancho alinhado com §7; registo de previsões; duração; numeração | inconsistências 1–4 |
| `manaburn/PERFIL.md` | gancho com quadro 0; auditoria do MB-EP11 (facto, interpretação, hipótese, recomendação) | missão §3 e inconsistência 12 |
| `conde/PERFIL.md` | gancho visual: obra ou detalhe no quadro 0 | missão §3 |
| `vince/PERFIL.md` | nome, voz, duração; gancho só com 2D | missão §3 e inconsistência 10 |
| `orbita/CONTEXTO.md`, `lambe-lambe/CONTEXTO.md` | uma linha de gancho visual cada | missão §3 |
| `AGENTS.md` | §2: gancho e revisão antes do roteiro; exceção da Expedição no fecho | inconsistência 6 |
| `comum/parcerias.md` | MC-ESP03: Farpas de Mana + portal DC500 do Farpas; MTGDC500 fora; mensagem de envio nova; linha no registo de resultados | correção do fundador (missão §9) |
| `nucleo/auditorias/2026-11-16_parcerias.md` | adenda de 19/11 | o relatório antigo fica histórico, com a remissão |
| `nucleo/DECISOES.md`, `comum/historico.md`, `STATUS.md` | entrada, linha e estado | protocolo |
| este ficheiro | relatório e handoff | entrega |

## 6. Validações

Ver a secção «Validações» do handoff (§10) com os resultados desta sessão.

## 7. Auditoria do MB-EP11 (Numot), para o Mana & Burn

Feita sobre a ficha (`manaburn/ep10-numot:manaburn/episodios/ep10_numot/ficha.md`) e os snapshots de 13/11 e 14/11 (branches). Sem acesso ao vídeo final nesta sessão, por isso a rubrica não foi medida.

- **Gancho, humor, evidência, reação, pergunta:** a 1.ª fala junta dor da mesa e número («Cada pancada dele, somem dois!») com a carta na TV; o humor nasce do exagero do Burn e a evidência vem do «Lê a carta» do Mana (4 correções de regra); cada carta citada entra em insert; a reação do Burn é o ponto cómico; a pergunta A/B fecha.
- **O que os números dizem:** recorde de views, mas ≈57 % pagas e só 17 dos 73 seguidores vindos do anúncio; metade do público pago saiu antes dos 3 s. Os guardados (71) são o sinal mais limpo: conteúdo que ensina regra é guardado.
- **O que não se copia do TUBO:** grelha 2×2, terminal, sonoplastia CRT. O equivalente do Mana & Burn é a TV SAL e a reação da dupla.

## 8. Decisões que dependem do fundador

1. **MB-EP11 e insights de 13–14/11:** integrar na `main` o pacote do Numot (com a linha MB-EP11 no registo) e os dois snapshots, corrigindo o impulso do MB-EP11 em 14/11 para `SIM`? Sem isto, a base do Mana & Burn cita dados que a `main` não tem.
2. **Quadro 0 de Magic:** manter P1 nas outras frentes (P0 só no TUBO) ou subir a P0 em todas, como sugere o «sempre» de 15/11?
3. **Verificação automática:** fazer o `memoria.py encerramento` exigir a secção «Gancho visual» e a linha «Pagamento do gancho» nas fichas criadas a partir de 19/11?
4. **ABISMO** (e Expedição no `AGENTS.md`): classificar o ABISMO no catálogo (frente, edição da Expedição ou formato do Lambe-lambe) e acrescentar a palavra de arranque.
5. **MC-ESP03:** o portal do Farpas não abriu do ambiente do agente a 16/11. Se continuar assim, enviar exportação ou prints (data, período, amostra); depois, autorizar a voz (~1.500–2.200 créditos, estimativa) e a DM.
6. **vidIQ:** confirmar se a @binder_vision já está ligada (o STATUS diz conta pessoal; as instruções do projeto dizem @binder_vision).
7. Continuam do STATUS: kit 2D do Vince; skills `binder-*`; RLS em `spatial_ref_sys`.

## 9. Plano de evolução · próximas quatro produções

Uma variável de cada vez, sempre com os 7 campos, a rubrica prevista e a revisão narrativa antes da voz. LL-ART20 já está pronto e não conta.

| # | Peça | Frente | Gancho (proposta, a confirmar com a evidência real) | Variável em teste | Comparação | O que aprende |
|---|---|---|---|---|---|---|
| 1 | **MC-ESP03** (Farpas, DC500) | Meta em Curto | dois comandantes na grelha 2×2, número de cada um, «O mais jogado ou o que mais vence?» até 3 s | comparação de dois × apresentação de uma carta | MC-EP08B (campeão único), ambos sem impulso | se a comparação segura mais nos 3 s no público competitivo |
| 2 | **MB-EP12** | Mana & Burn | base do EP11 (dor + número + carta na TV) | nenhuma: **sem impulso**, para ter o primeiro termo orgânico limpo da base | parte orgânica do MB-EP11 | se a base funciona sem anúncio |
| 3 | **MC-ESP04** (Preconauta) | Meta em Curto | mesa de 4 × 2x2 com o mesmo precon, número por formato | carta estática × carta com scan no quadro 0 (scan = entrada no terminal, identidade do TUBO) | MC-ESP03 | se o movimento no quadro 0 baixa a taxa de saltos |
| 4 | **CM-EP006** | Conde de Manaforte | a obra ou o detalhe da «insolência» no quadro 0, abertura por cima | nenhuma (primeiro Conde com briefing de gancho) | CM-EP005 | se a obra no quadro 0 muda os 3 s da série |

Revelação imediata × progressiva fica para uma frente onde não é P0 (Mana & Burn ou Conde), depois do MB-EP12.

## 10. Handoff

```
HANDOFF · 19/11/2026 · Claude
Repositório: ibisson254/GERADOR-DE-VIDEO-BINDER · branch main · último commit <ver STATUS.md> (conferido no remoto: ver mensagem de entrega)

Objetivo atual: sistema de gancho visual, gates e testes comparáveis no núcleo; MC-ESP03 corrigido para o Farpas de Mana.

Conteúdos tocados (comum/REGISTRO_EDITORIAL.md):
- nenhum (MC-ESP03 continua só proposto; pauta «Duel Commander 500 × mais jogado vs mais vence» LIVRE a 19/11)

Encerramento: não se aplica (nenhum episódio produzido).

Decisões tomadas nesta sessão:
- Missão estrutural de 19/11 e correção do MC-ESP03 (registadas em nucleo/DECISOES.md: sim)

Documentos consultados:
- AGENTS.md, STATUS.md, nucleo/* (constituição, catálogo, showrunner, checklist, decisões, modelos, auditoria de parcerias), perfis e bíblias das frentes, comum/parcerias.md, comum/insights/LEIA-ME.md, comum/REGISTRO_EDITORIAL.md, comum/historico.md, memoria.py; branches insights/2026-11-13-numot, insights/2026-11-14 e manaburn/ep10-numot (só leitura)

Alterações realizadas: tabela da §5.

Insights (domingo): nada registado nesta sessão · posts com impulso A CONFIRMAR: os de 14/11 (branch)

Tarefas pendentes:
- §8, pontos 1–7 · dependem do fundador
- Próxima produção com o sistema novo: MC-ESP03 · depende do acesso ao portal do Farpas

Próximo passo concreto: fundador responde aos pontos 1 e 5 da §8; depois, `python3 comum/ferramentas/memoria.py pauta --objeto "Duel Commander 500" --tema "..."` e ficha do MC-ESP03 com os 7 campos.
```
