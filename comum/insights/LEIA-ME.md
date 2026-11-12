# Insights · histórico de audiência do @binderthetrade

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

## Regras

- Guardar números, não screenshots. Nenhum dado pessoal: sem nomes de quem comentou, sem @ de terceiros, sem identificadores de conta de anúncios.
- Um snapshot por data. Os anteriores não se apagam nem se substituem.
- Comparar publicações com idades parecidas; anotar a idade de cada uma.
- Views não são instalações. Instalações só com o relatório da Play Console por UTM.
- Uma semana isolada não vira regra (constituição §12): uma regra nova precisa de padrão em 2+ semanas ou de decisão do fundador.

## Colunas do CSV

`semana_fim` (AAAA-MM-DD) · `periodo` (como o print o diz) · `id_editorial` (ID do registo ou `SEM-ID`) · `frente` · `post_ref` (início da legenda ou nome no print) · `formato` · `idade` (no momento do print) · `visualizacoes` · `alcance` · `impressoes` · `curtidas` · `comentarios` · `guardados` · `partilhas` · `visitas_perfil` · `novos_seguidores` · `cliques_link` · `outras_acoes` · `impulsionado` (SIM/NÃO/PARCIAL/A CONFIRMAR) · `investimento` · `moeda` · `campanha_periodo` · `objetivo_anuncio` · `alcance_pago` · `fonte` · `notas`.
