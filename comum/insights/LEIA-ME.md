# Insights · histórico de audiência do @binder_vision

Sistema permanente de métricas do Instagram. Criado a 01/11/2026 (`nucleo/DECISOES.md`). Substitui as tabelas de números do `comum/historico.md` (as antigas ficam lá como histórico, e foram migradas para aqui).

## O que há aqui

| Ficheiro | Para quê |
|---|---|
| `registo_posts.csv` | Base acumulada: uma linha por publicação por snapshot. Só se acrescentam linhas |
| `registo_conta.csv` | Totais da conta por snapshot (Visão geral, seguidores). Só se acrescentam linhas |
| `semanas/AAAA-MM-DD.md` | Relatório de cada snapshot (data = último dia do período do print). Um ficheiro novo por domingo; nunca se reescreve um anterior |
| `MODELO_SEMANAL.md` | Modelo do relatório |

## Rotina de domingo (prints do fundador)

1. `python3 comum/ferramentas/memoria.py semana AAAA-MM-DD` cria o relatório a partir do modelo (recusa se já existir).
2. Ler os prints: período exato dos dados (ex.: "últimos 7 dias", "1–7 nov"), Visão geral da conta e Conteúdo.
3. Identificar cada publicação pelo início da legenda e associá-la ao ID de `comum/REGISTRO_EDITORIAL.md`. Sem correspondência segura: `SEM-ID` e a dúvida nas notas.
4. Copiar só os números **visíveis** no print. O que não aparece fica vazio (nunca 0, nunca estimado). Valores arredondados pelo Instagram ("3,6 mil") entram como inteiro (3600) com a nota "arredondado no print".
5. Impulsionamento, por publicação: `SIM`, `NÃO`, `PARCIAL` ou `A CONFIRMAR`.
   - `SIM`/`PARCIAL`/`NÃO` só com confirmação do fundador ou um print do Gestor de Anúncios / "Ver insights do anúncio".
   - Sem confirmação: `A CONFIRMAR`. **Nunca inferir pelo volume de visualizações.**
   - Investimento, moeda, período da campanha e objetivo só quando confirmados.
   - Alcance pago vai na coluna `alcance_pago`; o resto não é "orgânico" enquanto o impulsionamento estiver `A CONFIRMAR`.
6. Acrescentar os totais da conta a `registo_conta.csv` e as linhas por publicação ao `registo_posts.csv` (no fim; não editar linhas antigas, salvo erro de transcrição, corrigido com nota e registado no relatório da semana).
7. Escrever o relatório (Fase 6: facto observado · interpretação · hipótese · recomendação) e comparar com as semanas anteriores.
8. `python3 comum/ferramentas/memoria.py validar` → commit.

## App: contas novas e primeira ação (desde 16/11/2026)

`registo_app.csv` liga a audiência ao produto, sem dados pessoais: por semana (segunda a domingo), contas novas (`public.profiles.created_at`) e quantas delas adicionaram pelo menos uma carta à coleção nos primeiros 7 dias (`public.portfolio_items`). Só contagens; nunca nomes, ids ou emails.

Consulta (Supabase MCP, só leitura; um agente com o conector Supabase corre-a no domingo e acrescenta as semanas fechadas):

```sql
select date_trunc('week', p.created_at)::date as semana_inicio, count(*) as contas_novas,
  count(*) filter (where exists (select 1 from public.portfolio_items i
    where i.user_id = p.id and i.created_at < p.created_at + interval '7 days')) as com_carta_7d
from public.profiles p where p.created_at >= '2026-09-01' group by 1 order by 1;
```

Limites: contas novas não são instalações (a Play Console continua a ser a fonte das instalações por UTM); a tabela inclui contas de teste do fundador e de testadores; não há ligação conta ↔ UTM (precisa da Play Install Referrer API no app, decisão do arquiteto).

## Métricas por API (vidIQ)

O conector vidIQ lê os Insights do Instagram como dono (visualizações, alcance, guardados, partilhas, tempo médio, % assistida, taxa de saltos dos Reels), sem prints. A 16/11/2026 a conta ligada é a pessoal do fundador, **não** a @binder_vision: falta o fundador ligar a @binder_vision no vidIQ (OAuth). Depois disso, a rotina de domingo usa `vidiq_instagram_owner_insights` (modo `reels` e `media`) e os prints ficam só para o que a API não trouxer (ex.: toques no link, se não vier).

## Regras

- Guardar números, não screenshots. Nenhum dado pessoal: sem nomes de quem comentou, sem @ de terceiros, sem identificadores de conta de anúncios.
- Um snapshot por data. Os anteriores não se apagam nem se substituem.
- Comparar publicações com idades parecidas; anotar a idade de cada uma.
- Views não são instalações. Instalações só com o relatório da Play Console por UTM.
- Uma semana isolada não vira regra (constituição §12): uma regra nova precisa de padrão em 2+ semanas ou de decisão do fundador.

## Avaliar resultados e testes comparáveis (desde 19/11/2026)

**Métricas que se leem**, só quando o Instagram, a Play Console ou o Supabase as mostram (o que não aparece fica vazio): visualizações e alcance · retenção inicial (taxa de saltos do Reel ou reproduções de 3 s do anúncio) · tempo médio e % assistida · partilhas · guardados · comentários · visitas ao perfil · seguidores novos · toques no link · instalações por UTM (`utm_campaign=<ID>`, Play Console) · contas novas e primeira carta em 7 dias (`registo_app.csv`, sem atribuição a um post). Nenhuma métrica se estima nem se deriva de outra sem o dizer.

**Seguidores qualificados e conversões:** só se atribuem a um post com UTM ou com um pico isolado no mesmo dia, dito como hipótese. Views não são instalações.

**Comparar só peças equivalentes:** mesma frente e formato, duração parecida, idade parecida no momento do print, e o mesmo estado de impulso (`NÃO` com `NÃO`; nunca pago com orgânico). Peças de formatos diferentes só se comparam com o contexto escrito ao lado.

**Testes (uma variável de cada vez):** a ficha do episódio diz a variável e a peça de comparação; o resto do formato fica estável. Variáveis em fila:
- carta estática × carta com scan no quadro 0;
- revelação imediata × revelação progressiva (nunca no Meta em Curto, onde a revelação até 3 s é P0);
- comparação de dois decks ou cartas × apresentação de uma única carta.

Leitura a 48 h e a 7 dias, na tabela abaixo. Um par de peças não muda uma regra; uma regra nova precisa de padrão em 2+ semanas ou de decisão do fundador (constituição §12).

| Teste | Variável | Peça A | Peça B | Métrica | 48 h | 7 dias | Leitura (facto · interpretação · hipótese · recomendação) |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

## Colunas do CSV

`semana_fim` (AAAA-MM-DD) · `periodo` (como o print o diz) · `id_editorial` (ID do registo ou `SEM-ID`) · `frente` · `post_ref` (início da legenda ou nome no print) · `formato` · `idade` (no momento do print) · `visualizacoes` · `alcance` · `impressoes` · `curtidas` · `comentarios` · `guardados` · `partilhas` · `visitas_perfil` · `novos_seguidores` · `cliques_link` · `outras_acoes` · `impulsionado` (SIM/NÃO/PARCIAL/A CONFIRMAR) · `investimento` · `moeda` · `campanha_periodo` · `objetivo_anuncio` · `alcance_pago` · `fonte` · `notas`.
