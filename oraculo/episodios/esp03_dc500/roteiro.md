# MC-ESP03 · roteiro v2 (PENDENTE DE DADOS)

Voz: Antonio de Jesus (eleven_v4, atempo 1,10). PT-BR, «você». Trilha: `oraculo/musica/tubo_tema.mp3`. Alvo: 27–29 s sem o fecho.
Marcadores vêm de `dados/episodio.json` (gerado por `dados/calcular.py`): `[A]`, `[B]`, `[nA]`, `[nB]` listas; `[qA]` quota do meta; `[iA]`, `[iB]` win rate (ou conversão Top 4, nunca os dois); `[dA]`, `[dB]` partidas (ou listas); `[dif]` diferença B − A; `[per]` período. Nenhum marcador chega à voz sem valor em `fontes.md`.
Pausas: `/` = 0,3 s · `//` = 0,6 s (corte seco da trilha).

Muda em relação à v1: popularidade e desempenho em blocos separados; a conclusão sai da margem da **diferença** (Newcombe), não dos intervalos individuais; o TUBO fala só duas vezes; a pergunta final nasce da descoberta.

## Texto comum (todos os cenários)

| Tempo | Bloco | Locução | Evidência no ecrã |
|---|---|---|---|
| 0–3 s | Gancho | — (sem voz: a grelha e a pergunta fazem o gancho; a voz entra no mergulho) | cartas A e B, «[nA] LISTAS», «[iB] WIN RATE em [dB] partidas», pergunta |
| 3–4 s | Mergulho | «[A]: / [nA] listas.» | o número no ecrã do TUBO |
| 4–8,5 s | Popularidade | «O mais jogado do portal, / [qA] do meta. // [B]: / só [nB] listas.» | painel POPULARIDADE, barras de listas, cartas A e B |
| 8,5–13,5 s | Desempenho | «No win rate, / [A] faz [iA]. / [B], / [iB]. // Em [dA] e [dB] partidas.» | painel DESEMPENHO, 0–100 %, linha de 50 %, denominadores a âmbar |
| 13,5–16,5 s | Leitura (TUBO) | «Popularidade mede quem *escolhe*. / Win rate mede quem *ganha*.» | TUBO; «ESCOLHE ≠ GANHA» no ecrã |
| 16,5–21,5 s | Diferença | por cenário (abaixo) | painel A DIFERENÇA: ponto, margem de 95 %, zero marcado, nota de independência |
| 21,5–24,5 s | Pergunta | por cenário (abaixo) | cartas A × B com os números |
| 24,5–27,5 s | Fecho | «Probabilidade calculada. / Humanos, imprevisíveis.» | TUBO |

## Por cenário (o código sai de `calcular.py`)

| Cenário | Diferença (16,5–21,5 s) | Pergunta (21,5–24,5 s) | Tese | Expressão do TUBO |
|---|---|---|---|---|
| `B_fora_margem` | «A diferença: / [dif]. // Mesmo com a margem de erro, / [B] fica à frente.» | «Você trocaria [A] por [B]?» | popularidade e vitória contam histórias diferentes | Confiante |
| `dentro_margem` *(ajuste de tese → fundador)* | «A diferença: / [dif]. // Mas com essa amostra, / cabe na margem de erro.» | «Você apostaria em [B] com tão poucas partidas?» | números melhores, amostra curta | Desconfiado |
| `A_melhor` | «[A] também lidera no win rate. // Desta vez, / a multidão fez a conta.» | «Alguém derruba [A] no próximo mês?» | o hype acertou | Confiante |

Se o portal só publicar conversão para Top 4: «win rate» passa a «conversão para o Top 4», «partidas» a «listas», e a pergunta do gancho a «O mais jogado é o que mais chega ao Top 4?» (ajuste de tese → fundador). Top 4 nunca é chamado de vitória.

Nunca dizer: «a diferença é real», «é mais forte», «prova». A frase do cenário `B_fora_margem` só se grava se o intervalo de Newcombe excluir zero **e** a definição do portal confirmar a unidade e os denominadores; a nota de independência fica no ecrã.

## Revisão narrativa (`SHOWRUNNER.md` §4.2) — v2, sobre a estrutura

| Critério | Resultado |
|---|---|
| Tese central | sim (uma por cenário, escolhida pelo cálculo) |
| Originalidade | sim (pauta livre 19/11) |
| Clareza | sim: quadro 0 com as quatro peças e as unidades |
| Progressão | sim: conflito → popularidade → desempenho → leitura → diferença → pergunta; nenhum bloco repete o anterior |
| Evidência | sim: cada número dito está no ecrã com fonte no mesmo segundo |
| Ritmo | medido na prévia: maior intervalo 2,6 s |
| Recompensa | sim: promessa (é real ou é amostra?) paga aos 19,0 s com o veredito ao lado da margem |
| Relevância | sim |
| CTA natural | sim: uma pergunta ligada à descoberta |

Repete-se com os números antes da voz.

## Custo da voz
Texto do cenário `B_fora_margem` com nomes e números típicos: ≈ 430 caracteres → ≈ 430 créditos por tomada no eleven_v4 (cobrança por caractere; preço do plano por confirmar). Pedido ao fundador: 1 tomada (≈ 430) ou 2 (≈ 860). Conta final sobre o texto gravado.
