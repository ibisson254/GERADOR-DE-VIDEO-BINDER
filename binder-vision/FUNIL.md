# BINDER Vision · funil e números do app

Leitura de 21/11/2026 (Supabase, só contagens; nenhum nome, id ou e-mail). Atualização semanal: `comum/insights/registo_app.csv` (rotina de domingo, `comum/insights/LEIA-ME.md`).

## 1. O funil completo e o que sabemos de cada etapa

| Etapa | Fonte | Leitura a 21/11/2026 |
|---|---|---|
| Visualizações no Instagram | Insights | ~100 mil num mês (estimativa do fundador, 21/11; sem print no repositório). Último dado registado: 13 mil em 1–31/10 |
| Visitas ao perfil | Insights | **sem dado** |
| Toques no link da bio / sticker | Insights | **sem dado** |
| Visitas à página da Play | Play Console | **sem dado** |
| Instalações | Play Console (UTM) | **sem dado** |
| Contas criadas | Supabase `profiles` | 23 nos últimos 30 dias |
| Onboarding concluído | `profiles.has_onboarded` | 16 das 23 |
| Primeira carta | `portfolio_items` | 7 das 23, **todas nas primeiras 24 h** |
| Ativos na última semana | `profiles.last_seen` | 6 das 23 |

Leitura aritmética (ordem de grandeza, não taxa oficial): ~100 mil visualizações → 23 contas ≈ **0,2 contas por 1.000 visualizações**. Não se sabe em que etapa entre a visualização e a conta a perda acontece: é a primeira coisa a medir (`ESTRATEGIA.md` §2).

## 2. Contas novas por semana (desde a beta)

| Semana (início) | Contas novas | Carta em 7 dias |
|---|---|---|
| 21/09 | 1 | 0 |
| 28/09 | 14 | 1 |
| 05/10 | 2 | 0 |
| 12/10 | 1 | 0 |
| 19/10 | 2 | 1 |
| 26/10 | 5 | 2 |
| 02/11 | 3 | 0 |
| 09/11 | 9 | 2 |
| 16/11 (até 21/11) | 4 | 2 |
| **Total** | **41** | **8 (~20 %)** |

Por mês (contas no Auth, sem as 162 contas de teste de carga de junho): setembro 5 · outubro 10 · novembro 16 (até dia 21). A tabela inclui contas de teste do fundador e de testadores; não há forma de as separar sem dados pessoais.

## 3. Uso das funções (registos criados por mês)

| | Set | Out | Nov (até 21) |
|---|---|---|---|
| Cartas adicionadas ao Binder | 47 | 11 | 89 |
| Pessoas que adicionaram cartas | 1 | 5 | 5 |
| Trocas abertas | 6 | 6 | 6 |
| Mensagens de chat | 13 | 13 | 18 |
| Ligações (seguir) | 4 | 5 | 6 |
| Favoritos | 2 | 2 | 16 |
| Insígnias atribuídas | 3 | 10 | 13 |
| Eventos (torneios) criados | 3 | 1 | 0 |

Desde sempre: 12 pessoas têm cartas no Binder (3 com 21+ cartas concentram a maioria das 544); 59 perfis (44 colecionadores, 15 operadores); 8 arenas ativas. Login: e-mail 188, Google 24, Discord 1 (inclui as contas de teste de junho).

## 4. O que os números dizem (facto · interpretação · hipótese)

1. **Facto:** a conversão visualização → conta é muito baixa (~0,2 por 1.000). **Hipótese:** a perda maior está antes da Play (o app aparece só nos últimos segundos de vídeos de entretenimento, e o caminho é perfil → bio → Play). Só se confirma com visitas ao perfil, toques no link e visitas à Play.
2. **Facto:** quem adiciona carta fá-lo no primeiro dia; ninguém volta para a primeira carta depois. **Interpretação:** a primeira sessão decide tudo. **Hipótese:** o login obrigatório antes de ver o app e um onboarding que não leva direto ao scanner perdem gente (7 dos 23 nem concluem o onboarding).
3. **Facto:** novembro já tem mais contas que outubro (16 × 10) com ritmo editorial maior. Uma semana isolada não vira regra (constituição §12).
4. **Facto:** as funções sociais e de loja têm uso residual. **Interpretação:** coerente com a decisão de 21/10 de não as usar como argumento; o argumento é o scanner e o Binder.

## 5. Dados que faltam (pedido ao fundador)

1. Insights do Instagram dos últimos 30 dias: visualizações, **visitas ao perfil** e **toques no link** (prints ou ligar a @binder_vision no vidIQ).
2. Play Console › Aquisição de utilizadores, últimos 30 dias: visitantes da página, instalações e taxa de conversão da página; e por UTM, se houver.
3. Confirmar a versão em produção na Play (v6 2.4.5 ou v7 com modo visitante).

## 6. Consultas (só leitura)

```sql
-- últimos 30 dias
select count(*) contas, count(*) filter (where has_onboarded) onboarding,
  count(*) filter (where exists (select 1 from portfolio_items i where i.user_id=p.id)) com_carta,
  count(*) filter (where exists (select 1 from portfolio_items i where i.user_id=p.id
    and i.created_at < p.created_at + interval '1 day')) com_carta_24h,
  count(*) filter (where last_seen > now() - interval '7 days') ativos_7d
from profiles p where created_at >= now() - interval '30 days';
```

A consulta semanal está em `comum/insights/LEIA-ME.md`.
