# Integração Data Binder + BINDER Originals · diagnóstico (fase zero), reconciliação e pré-merge

28/11/2026, missão de engenharia do fundador (02:13). **Nenhuma integração foi implementada antes deste diagnóstico.** Depois dele, o fundador escolheu implementar o evento (§6). Sem push, sem merge, 0 créditos, nenhuma conta ligada.

## 1. Onde está o Data Binder (fase zero)

| Onde | O que é | Estado verificado |
|---|---|---|
| Repo `ibisson254/-Binder-Dados` (privado) | Fluxo de trabalho: AGENTS, STATUS, PROMPT_PROJETO, 3 consultas SQL (`semanal`, `funil_30d`, `uso_funcoes_mes`) e 1 relatório (`2026-11-21_funil_inicial.md`) | 1 commit (27b4b15, 21/11). Sem código de ingestão, API, base de dados, eventos ou automação |
| Drive «ANALYTIC BINDER.txt» | *BINDER Data Intelligence Master v1.2* (02/10/2026): plano do esquema `analytics` (events, card_price_daily, fx_daily, area_card_daily), RPC `track_events()`, contrato de evento, qualidade de dados, k ≥ 5 | Fase DISCOVERY, antes de F0. Domínio: **app** BINDER Vision. Dashboard, ML e API proibidos em F0 |
| Supabase `rfucohyfvjqmfwuqcjrd` | Base do app (profiles 68, portfolio_items 792, trades 74, messages 131, auth.users 224) | **Não existe** esquema `analytics` nem tabela de eventos. Leitura só por contagens |
| vidIQ | `@ibisson.mendes` ligado por OAuth com `instagram_business_manage_insights`; `@binder_vision` só «manual», `connectionActive: false` | Ler insights do @binder_vision exige ligar a conta (OAuth do fundador) |

### As 12 perguntas

1. **O que é?** Um repositório de método (consultas + relatórios) para o funil do app, mais um plano de plataforma analítica que ainda não foi construído.
2. **Onde vive?** Repo `-Binder-Dados`, documento no Drive, consultas que correm no Supabase do app.
3. **Que dados tem?** Contagens agregadas do app (perfis, cartas, trocas, mensagens). Nenhum dado de audiência dos Originals.
4. **Que métricas calcula?** Funil semanal e de 30 dias, uso de funções por mês (app). Nenhuma métrica de episódio.
5. **De onde vêm?** Supabase em só-leitura; Play Console para instalações; vidIQ ou capturas para Instagram (previsto, não feito).
6. **Tem API, eventos ou webhooks?** Não. O contrato de evento existe só no papel e é do app.
7. **Quem atualiza?** Manualmente, em sessão. Último relatório: 21/11.
8. **Guarda números dos Originals?** Não. O seu AGENTS §2 manda que os números do estúdio fiquem em `comum/insights/` do GERADOR, **fonte única**, e que o Data Binder acrescente lá.
9. **Que identificadores usa?** Do app (user/print/oracle). Nenhum `episode_id`.
10. **Há automação?** Nenhuma (nem Actions, nem n8n).
11. **Custos?** Zero hoje; vidIQ diz `0 credit(s) per call` para `vidiq_social_account_list` e `vidiq_instagram_owner_insights` (não chamada).
12. **O que falta para receber um `episode.completed`?** Um recetor. Hoje não existe nenhum; criar um seria construir o segundo sistema de analytics que a missão proíbe.

## 2. Mapa de integração

```
 BINDER Originals (GERADOR)               Data Binder (-Binder-Dados)            BINDER Vision (app)
 ────────────────────────────             ───────────────────────────            ───────────────────
 fichas → render → QC → aprovação  ──►  comum/eventos/ (proposta, JSONL)  ──►  lê, analisa, escreve
 humana → REGISTRO_EDITORIAL              comum/insights/registo_posts.csv ◄──  números observados
                                                                                Supabase (só leitura)
                                                                                funil, uso, trocas
                                          relatórios do app  ◄────────────────  (domínio separado)
```

| Informação | Dono | Onde mora | Partilhada? |
|---|---|---|---|
| Estado editorial (IDEIA … PUBLICADO) | Originals (fundador aprova) | `comum/REGISTRO_EDITORIAL.md` | Lida pelo Data Binder |
| Ficha técnica do vídeo (duração, formato, fps, QC) | Originals | ficha da frente + `comum/qc/` | Lida |
| Evento de conclusão | Originals (emite) | proposta: `comum/eventos/episodios.jsonl` | Lido |
| Métricas de audiência por publicação | Data Binder (recolhe) | `comum/insights/registo_posts.csv` | Escrito pelo Data Binder, lido pela inteligência cultural |
| Métricas do app | Data Binder | Supabase + relatórios do repo `-Binder-Dados` | **Não** se misturam com audiência |
| Oportunidades e critérios | Inteligência cultural | `comum/inteligencia/` | — |

**Regra de não-mistura:** uma métrica do app (ex.: instalações) só se cruza com um episódio quando houver atribuição explícita (UTM, código, link na bio datado). Até lá, cada lado reporta em separado.

## 3. Métricas: disponibilidade e definição

| Métrica | Coluna | Fonte | Disponível hoje |
|---|---|---|---|
| Visualizações, gostos, comentários, partilhas, guardados, alcance | já existentes | Instagram (captura ou vidIQ owner insights) | 10 de 90 publicados |
| Tempo médio, % assistida, taxa de saltos | `tempo_medio_s`, `pct_assistida`, `taxa_saltos` (28/11) | Instagram Insights do Reel | só MB-EP13 tem tempo médio |
| Duração | `duracao_s` | ficha / ffprobe | preenchível sem custo |
| Data de publicação | `publicado_em` | fundador / Instagram | quase toda «por confirmar» |

Cada leitura guarda origem, data de recolha e período; métrica sem fonte fica **vazia**, nunca estimada.

**Identificador comum:** `id_editorial` (ex. `MB-EP13`, já usado nas duas pontas) → `publicacao_id` (URL/shortcode do Instagram, quando conhecido) → `campanha_id` (só se houver colaboração) → linhas de métricas. Os IDs históricos não mudam.

## 4. Reconciliação histórica (aplicada nesta branch, auditável)

O fundador disse a 28/11 (02:13): «os episódios que já foram criados e finalizados também já foram publicados».

- 38 linhas passaram a PUBLICADO. Só mudaram `Estado`, `Publicação` (`até 28/11/2026 (data exata por confirmar…)`) e o acrescento na `Fonte`; o script confirmou as outras colunas iguais. Nenhum ID mudou, nenhuma linha saiu.
- Antes e depois de cada linha: `comum/reconciliacao/2026-11-28_publicados.csv` (com evidência e o que confirmar).
- Novo `memoria.py painel`: ciclo de vida real (em desenvolvimento 1, aprovado por produzir 1, em produção 4, concluído por publicar 0, publicado 90 dos quais **80 à espera de métricas**, fora do ciclo 33).

### Divergências que precisam do fundador (não decidi sozinho)

| ID | Divergência |
|---|---|
| MB-EP17, MC-ESP03, MB-ESP05, LL-ART21, AB-04, MC-EP09, MC-EP10, LL-ECO01 | Qual versão foi publicada (ou se havia condição: OK do parceiro, licença de imagem, plano A/B) |
| AB-01 | Estado PUBLICADO mas a coluna Publicação diz «não publicada» (já vinha assim) |
| ORB-21 | Continua APROVADO «agendado 06/11»: foi publicado? |
| MB-GIRO01, EX-01 | EM PRODUÇÃO há semanas: já saíram? |
| 30 linhas POR AUDITAR | Fora do ciclo até auditoria |

Limite: fichas, ficheiros finais e QC não foram cruzados episódio a episódio (os vídeos não estão no git).

## 5. Revisão pré-merge

| | A · `auditoria/motor-producao-2026-11-27` | B · `inteligencia-cultural-binder` |
|---|---|---|
| Base | eadaa1f^ (main antes do MC-EP10 v2) | mesma base |
| Commits | e9dc3d4 | 17235b8, bc3ed5d |
| Ficheiros | 17 (6 novos, 11 alterados), +641/−45 | 17 (7 novos, 10 alterados), +1049/−21 |
| `diff --check` | limpo | limpo |
| Remoções | nenhuma | nenhuma |
| Configuração | `validar.yml` (passo dos testes do QC), `requisitos.txt`, `preparar_ambiente.sh` | nenhuma (o passo dos testes entra no merge) |
| Dados históricos | nenhum | `registo_posts.csv`: só colunas vazias acrescentadas; linhas antigas iguais |
| Motores | `kit_carrossel/compor.py`, `kit_video/motor_video.py`, QC | nenhum |
| Conflitos | nenhum com main | `comum/historico.md` com main/A: resolvido mantendo as duas linhas por ordem horária |

Ensaio numa worktree local (`premerge/teste-2026-11-28`): A → B → passo no workflow. Suite completa verde: `validar_repo` (1 aviso antigo não grave, `vince/kit/v1/`), `memoria validar`, `ciclo validar` (8 previsões), `test_memoria` 18, `test_ciclo`, `test_qc` 5 (ffmpeg+numpy), `inteligencia validar`, `test_inteligencia` 18.

**Riscos:** A mexe nos motores de vídeo e carrossel (rever um render antes do próximo episódio); STATUS.md passa de 6 KB depois das três branches (compactar no merge).
**Ordem recomendada:** A, depois B, depois o passo no `validar.yml`, depois esta reconciliação (toca `memoria.py`, `STATUS`, `DECISOES`, `historico`; rebase trivial).
**Prontidão:** pronto para merge assim que o fundador autorizar.

## 6. Evento `episode.completed` (implementado a 28/11, 03h, depois da escolha do fundador; ver `comum/eventos/LEIA-ME.md`)

- **Onde:** `comum/eventos/episodios.jsonl` no repo (append-only). Sem servidor, sem base, sem custo.
- **Quando:** `eventos.py concluir <ID> --qc qc.json` exige QC sem P0, a linha «Aprovação final: <nome> · <data>» na ficha e o pacote do `memoria.py encerramento`; só então escreve o evento e marca CONCLUÍDO. O modelo nunca aprova.
- **Idempotência:** `event_id = sha256(episode_id + "episode.completed" + event_version)`; repetir não duplica.
- **Campos:** os 15 da missão (episode_id, series_id, production_status, approval_status, qc_status, created_at, completed_at, video_path, duration_s, format, resolution, fps, creative_attributes, source_branch, event_version).
- **Sync:** cada evento nasce pendente; `eventos.py sincronizar --destino <pasta do Data Binder>` entrega-o (idempotente) e regista a tentativa em `comum/eventos/sync.jsonl`. O que falha fica pendente e é retomado na próxima vez. Nada se perde.
- **Testes 1–10 (`test_eventos.py`, 23 casos, no workflow):** conclusão normal, duplicado, falha de sync, render sem aprovação (recusa), QC falhado (recusa), reconciliação histórica, métrica ausente fica vazia, consulta preserva origem/período/definição/id, validações entre branches, reexecução sem duplicar. Tudo com mocks, 0 créditos.
- **Custo de manutenção:** zero diário; corre só quando se encerra um episódio.

## 7. Outros achados

- **Supabase:** RLS desligado em `public.spatial_ref_sys` (já nas pendências do fundador). Correção, se quiser: `ALTER TABLE "public"."spatial_ref_sys" ENABLE ROW LEVEL SECURITY;`. Não apliquei.
- **vidIQ:** owner insights a 0 créditos é a via mais barata para encher as 80 linhas sem números, mas precisa de o fundador ligar o @binder_vision. Nada foi ligado nem chamado.
