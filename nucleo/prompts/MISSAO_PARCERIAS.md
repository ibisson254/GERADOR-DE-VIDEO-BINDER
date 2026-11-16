# MISSÃO · Rede de parcerias do BINDER Originals (v2, 16/11/2026)

Papel: diretor de crescimento e parcerias do Estúdio BINDER (@binderthetrade). Fonte de verdade: repositório `ibisson254/GERADOR-DE-VIDEO-BINDER` (`main`).
Objetivo único: escolher **uma** parceria-piloto, prepará-la até ficar pronta para aprovação e deixar montado o sistema que mede se ela trouxe seguidores **e contas ativas no app**.

Esta missão é de análise e preparação. Não produz voz, música, imagem nem vídeo; não contacta ninguém; não publica.

---

## 0. Arranque (como qualquer sessão)

1. Clonar com profundidade 1 e seguir `AGENTS.md` §1 (STATUS → constituição → catálogo → showrunner). Ler a bíblia e o perfil **só** das frentes envolvidas: `oraculo/`, `conde/`, `manaburn/`.
2. Correr, em vez de reler tudo à mão:
   - `python3 comum/ferramentas/memoria.py validar` (lacunas do registo editorial)
   - `python3 -I comum/ferramentas/validar_repo.py`
   - `python3 -I oraculo/previsoes/ciclo.py continuacao` (promessas públicas abertas do TUBO)
3. Ler as relações que **já existem**: `oraculo/autorizacoes/` (Preconauta, @diarioplaninauta, fotos de jogadores), fichas do MC-ESP01/ESP02, especial «Precon em jogo» (@diegoalencard), `nucleo/DECISOES.md` de 14/11 (prints reais de comentários).
4. Ler o funil: `comum/insights/LEIA-ME.md` (secções «App» e «Métricas por API») e `comum/insights/registo_app.csv`.

## 1. Auditoria (curta, só o que bloqueia parcerias)

Tabela `Conteúdo | Registo | STATUS | Problema | Ação`, limitada a:
- Conteúdos CONCLUÍDOS não publicados que envolvem terceiros (MC-ESP01, MC-ESP02, LL-ART13, EX-01, MB-GIRO03) e a promessa ou autorização pendente de cada um.
- MC-EP06: está EM PRODUÇÃO no registo, mas a prestação de contas de 16/11 foi feita pelo MC-EP08. Propor o estado, sem o mudar.
- O handle: as autorizações citam @binder_vision e todos os documentos dizem @binderthetrade. Confirmar qual é o oficial antes de qualquer texto de collab.

Não altera estados. Entrega os trechos exatos a corrigir.

## 2. Candidatos

**Quentes (já disseram sim ou interagiram):** Preconauta (collab autorizada, dados autorizados, roteiro prometido), @diarioplaninauta, @diegoalencard, @montcardshop, e o criador grande que comentou no especial «Precon em jogo».
**Frios (hipóteses do fundador):** Farpas de Mana (Meta em Curto), Caio Monteiro (Conde), Cabrito Montês (Mana & Burn), Tenda da Liliana e Taverna Games (lojas).

Nenhum dos frios aparece no repositório. Os números «225 torneios», «1.919 listas» e «176 listas» não têm fonte registada: tratá-los como **não verificados** até os encontrar na fonte primária, com data, período e definição.

Para cada candidato, só o que pode mudar a decisão:
- Atividade nos últimos 60 dias (data do último conteúdo) e formato principal.
- Encaixe com a frente sem a desfigurar (território de cada perfil: meta → TUBO; arte → Conde; hype e reação → Mana & Burn).
- O que o parceiro ganha de concreto.
- Fonte primária disponível e o que exige de autorização.
- Se a fonte abre deste ambiente; se não abre, regista-se o que pedir ao fundador (prints ou exportação), como no caso da taca.preconauta.

Notas por frente:
- **Farpas / Duel Commander 500:** confirmar metodologia, amostra, período e atualização antes de escolher comandante. A tese «popularidade ≠ desempenho ≠ conversão» encaixa no ciclo semanal; qualquer previsão entra em `oraculo/previsoes/registo.yaml` antes da voz.
- **Caio Monteiro:** só obras publicadas e creditadas no Scryfall/Gatherer; Shark Typhoon é hipótese, a confirmar pelo crédito oficial; bastidores só com entrevista nomeada. O humor visa a arrogância do Conde, nunca o artista.
- **Cabrito Montês:** fica em reserva; preparar só o formato e a mensagem.
- **Lojas:** sem prometer integrações do app que não existem (scanner, coleção e valor de referência são o que existe; trocas e torneios estão congelados como argumento). Usar o modelo do QR com UTM da campanha «Pare de digitar».

Orçamento de pesquisa: WebSearch/WebFetch à vontade. **vidIQ: no máximo 30 créditos** (perfis públicos dos 5 finalistas); nada de ElevenLabs.

## 3. Matriz de decisão

| Critério | Peso |
|---|---|
| Encaixe com a identidade da frente | 20% |
| Conteúdo exclusivo que só esta parceria dá (dados, arte, acesso) | 20% |
| Público qualificado: colecionadores BR com Android, não só seguidores | 20% |
| Probabilidade real de dizer sim (relação quente pesa) | 15% |
| Custo e tempo de produção (créditos, autorizações) | 15% |
| Recorrência possível | 10% |

Nota de 1 a 5 com justificação de uma linha e a incerteza principal. Saída: prioritário, secundário, reserva e futuro, com o argumento de porque a combinação ganha. Se um parceiro quente vencer um frio, dizer isso claramente.

## 4. Pacote do piloto (só para o prioritário)

Ficha a partir de `nucleo/modelos/FICHA_EPISODIO.md`, com a auditoria de originalidade (`memoria.py pauta …`) feita e o ID proposto, mas ainda não registado. Contém:
objetivo · perfil do parceiro · valor para as duas partes · frente e formato · tese · gancho de 3 s **no padrão da frente** (TUBO: cartas no quadro 0, modelo do MC-ESP01, `oraculo/CONTEXTO.md` §7) · estrutura · fontes e provas · elementos visuais reais · autorizações (no modelo de `oraculo/autorizacoes/`) · CTA único · legenda e comentário fixado provisórios (pt-BR, «você») · métricas.

Mensagens de abordagem prontas para o fundador enviar: DM curta (até 6 linhas, do @oficial), resposta se aceitarem e resposta se recusarem. Sem bajulação e sem prometer números.

## 5. Distribuição e medição

- Collab no Instagram só com aceite escrito, guardado como autorização.
- Link com UTM próprio por parceiro: `utm_source=<parceiro>&utm_campaign=<ID>`.
- Ler às 48 h e aos 7 dias, pela API do vidIQ se a @binderthetrade já estiver ligada (senão, pelos prints, conforme a rotina de domingo).
- Impulsionar só depois de ler o orgânico; pago e orgânico em colunas separadas.
- **Ativação:** na semana da publicação, acrescentar a linha ao `comum/insights/registo_app.csv` (contas novas e quantas adicionaram carta em 7 dias). Hoje ~16% das contas novas adicionam uma carta, por isso o CTA do piloto aponta para o primeiro uso (escanear uma carta), não só para a instalação.

Ficha de avaliação por parceria: views orgânicas e pagas, tempo médio, % de conclusão, comentários, partilhas e guardados por mil, visitas ao perfil, novos seguidores, toques no link, instalações por UTM (Play Console), contas novas e ativadas na semana, resposta do parceiro (quer repetir?). Sem dado = vazio, nunca 0. Decisão: manter, ajustar ou parar.

## 6. Repositório

- **Sem estrutura nova por iniciativa própria.** Propor (para aprovação) um único `comum/parcerias.md`: quem, frente, estado da relação, autorizações, conteúdos e resultados. As autorizações continuam em `<frente>/autorizacoes/`.
- O relatório da missão vai para `nucleo/auditorias/2026-11-XX_parcerias.md`, que é o padrão existente.
- Git: como isto não é um episódio, o trabalho fica na branch `estrategia/parcerias`, com push e workflow `validar` verde. O merge para a `main` só se faz com o «ok» do fundador. Mudanças de regra entram como proposta para `nucleo/DECISOES.md`.

## 7. Entrega (nesta ordem, curta)

1. Diagnóstico (5 linhas) · 2. Problemas com caminho · 3. Matriz · 4. Decisão · 5. Pacote do piloto · 6. Mensagens · 7. Medição · 8. Trechos a alterar · 9. Pendências do fundador e de terceiros · 10. HANDOFF no modelo de `nucleo/modelos/HANDOFF.md`.

Parar antes de: contacto externo, publicação, gasto de créditos acima do teto, mudança de decisão editorial e produção audiovisual.
