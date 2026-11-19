# Ficha · Meta em Curto · ESP03 · O mais jogado é o que mais vence? (Duel Commander 500)

## Identificação*
- ID editorial*: `MC-ESP03`
- Estado no registo*: EM PRODUÇÃO (desde 19/11/2026, 15:10) · **bloqueado no Gate A (dados)**
- Aprovação do fundador: pauta e parceiro-alvo decididos a 19/11/2026 (`nucleo/DECISOES.md`, `comum/parcerias.md`). Tese final, voz e envio ainda não aprovados.

## Classificação*
- Frente*: Meta em Curto (TUBO) · especial com parceiro-alvo
- Classe de conteúdo*: meta (Relatório do Meta, `oraculo/PERFIL.md`)
- Complexidade: média
- Estratégia: análise de dados — separar **representação** (listas), **desempenho** (win rate ou conversão, conforme o portal publica) e **amostra** (denominador)

## Originalidade*
- Objeto*: portal Duel Commander 500 (Farpas de Mana); comandantes a definir pelos dados
- `memoria.py pauta --objeto "Duel Commander 500" --tema "popularidade versus desempenho competitivo dos comandantes"`* (19/11/2026, 15:08): **PAUTA LIVRE**. Conferido à mão: nenhum MC/MB/CM/LL trata DC500 nem popularidade × desempenho de comandantes; o MC-EP01 (conversão por arquétipo no AC13) é outro formato, outro evento e outra fonte.
- Relações: MC-ESP01 e MC-ESP02 (modelo de abertura e de parceria); MC-EP01 (mesmo tipo de raciocínio, representação × conversão).
- Previsões abertas do TUBO (`ciclo.py continuacao`, 19/11): PR-TRK-01..04 — nenhuma toca este episódio; o MC-ESP03 não faz previsão.

## Editorial (briefing)
- Objetivo*: ensinar ao jogador de Duel Commander a não confundir «muito jogado» com «forte», com os dados públicos do portal do Farpas; servir de prévia para a collab.
- Proposta de valor*: em 30 s você sabe se o comandante mais jogado do DC500 é mesmo o que mais vence — e quanto a amostra aguenta.
- Público: jogadores de Duel Commander 500 no Brasil (público do Farpas) e jogadores competitivos de Commander.
- Hipótese a testar: a comparação de dois comandantes na grelha segura mais os 3 s do que a apresentação de um só (termo de comparação: MC-EP08B, ambos sem impulso).
- Variável em teste: 1 — abertura com comparação de dois × campeão único (MC-EP08B).
- Tese*: **pendente dos dados** (Gate B). Três teses possíveis, escolhidas só pelo veredito de `dados/calcular.py`:

| Veredito do cálculo | Tese que se grava | Grau de certeza |
|---|---|---|
| A (mais listas) também tem o melhor indicador comparável | «O mais jogado também é o que mais vence — desta vez o hype acerta.» | o do intervalo |
| B supera A e o intervalo de 95 % de B fica acima do valor de A | «Popularidade e vitória contam histórias diferentes.» (título de trabalho mantém-se) | alto para este período |
| B supera A mas o intervalo inclui o valor de A | «Um comandante menos jogado tem números melhores — mas a amostra ainda não prova.» (tese ajustada: vai ao fundador antes da voz) | baixo; dito no ecrã |
| O portal não publica win rate com denominador, só conversão | pergunta passa a «O mais jogado é o que mais chega ao Top 4?» (ajuste de tese, vai ao fundador) | conforme o intervalo |
| Nenhum indicador comparável | não se grava; pauta alternativa: «O que é popular no DC500 em <período>» (só representação) ou cai | — |

Regras da escolha de B (fixadas **antes** de ver os números, para não escolher o contraste): mesmo período e filtros; sem alertas do script (≥ 20 listas, ≥ 50 partidas quando houver win rate, ≥ 3 torneios, ≤ 50 % das listas num só torneio); B = melhor indicador entre os que passam; nunca win rate de um contra conversão de outro.

## Gancho visual* (`nucleo/SHOWRUNNER.md` §4.1) — estrutura fechada, números pendentes

1. Quadro 0*: grelha 2×2 em ecrã inteiro sobre o TUBO escurecido. Quadros: carta A (cima, esq.) · número A (cima, dir.) · número B (baixo, esq.) · carta B (baixo, dir.). Cabeçalho mono «DUEL COMMANDER 500 · <período>»; selo em cada carta: A «<n> LISTAS», B «<x>% WIN RATE · <p> PARTIDAS» (ou conversão, conforme o portal). Linha de fonte por baixo: «Dados: Duel Commander 500 (Farpas de Mana) · <período>».
   *Porquê esta composição:* com dois comandantes, uma carta por quadro deixa-a inteira (arte e rodapé visíveis) e cada número fica ao lado da sua carta, em diagonal com o rival. Fica no render como `grelha_dupla()`.
2. Objeto real*: **pendente** — as duas cartas de comandante (imagem oficial Scryfall, impressão a registar) definidas pelos dados.
3. Ação no 1.º segundo*: 0–0,3 s as quatro peças entram com um passo (sem fade de preto); 0,3–1 s scan verde passa sobre a carta A, contorno verde acende e o número de A sobe em contagem.
4. Som*: «tum» de desmagnetização do CRT a 0,0 s; chiado curto de modem no scan (0,3 s); bip seco no destaque (biblioteca do TUBO, `CONTEXTO.md` §7.2.1). Trilha do TUBO quase em silêncio.
5. Descoberta até 3 s*: 1–3 s o destaque salta para B (resto escurece) e aparece a pergunta «O MAIS JOGADO É O QUE MAIS VENCE?» com os dois números lado a lado e os denominadores. Compreensível sem som.
6. Promessa*: «vou mostrar se a diferença é real ou só amostra».
7. Pagamento*: ~16 s, imagem do intervalo (barras com a faixa de 95 % de A e de B no mesmo eixo, a partir de 0) + veredito a verde ou âmbar; segundo exato depois da voz.

| Rubrica (1–5) | Prevista | Medida no final |
|---|---|---|
| Relevância visual | 5 (as cartas são a prova) | |
| Impacto inicial | 4 | |
| Clareza | 4 (dois números + pergunta; depende de legibilidade do denominador) | |
| Curiosidade | 5 (pergunta específica do formato) | |
| Pagamento | 4 (o intervalo paga; risco: veredito «não distinguível» parecer anticlímax) | |
| Identidade | 5 (grelha + terminal + som do TUBO) | |

## Roteiro definitivo*
**Pendente de dados.** Três versões prontas por cenário em `roteiro.md`; a gravada será uma delas com os números do portal. Revisão narrativa (§4.2) feita sobre a estrutura; repete-se com os números.

## Fontes e evidências*
Ver `fontes.md` (verificado V1–V5, tentativas de acesso, tabela final por preencher). Capturas em `capturas/` (lista do que falta em `capturas/LEIA-ME.md`). Cálculos em `dados/calcular.py` (testado com dados sintéticos; `extracao.csv` vazio).

Limitações: ver `fontes.md` §Limitações.
Créditos e autorizações: nenhuma autorização do Farpas existe. Nada em `oraculo/autorizacoes/`.

## Produção
- Recursos reutilizados: `oraculo/esp01/esp01_render.py` (`hook()`, terminal, chuva, TUBO) e `oraculo/episodios/ep08b_render.py` como base do `esp03_render.py`; `oraculo/esp01/esp01_audio.py` para mix; `oraculo/assets/tubo_mestra_916.png`; `oraculo/musica/tubo_tema.mp3`; `comum/outro/outro_binder_916.mp4`. O TUBO não é regenerado.
- Script de render: **não escrito ainda** — depende de quantas cartas, do indicador e do texto final; escrevê-lo antes seria trabalho a refazer. Estimativa: 1 sessão curta depois dos dados.
- Voz: Antonio de Jesus (`MK5tXPmT83J5SUlpUo4K`, eleven_v4, atempo 1,10). Não gerada.
- Easter egg: a decidir com os números (no máx. 1, chuva de código, registado em `comum/easter_eggs.md`).
- Riscos: P0 se um número sair sem denominador ou se win rate e conversão se misturarem; risco de parceria se o vídeo sugerir collab.

## Controlo de qualidade*
Não medido: não existe ficheiro final. Os testes só se declaram quando forem executados (`python3 -I comum/qc/qc_video.py VIDEO.mp4 --frente tubo`).

## Ficheiros finais*
- Vídeo final: não existe.
- Capa: não existe (precisa do número principal e das cartas).

## Pacote de publicação* (rascunhos nesta pasta, com marcadores `[PENDENTE]`)
- [ ] `legenda.txt` · [ ] `comentario_fixado.txt` · [ ] `texto_alternativo.txt` · [x] `fontes.md` (parcial) · [x] `mensagem_farpas.txt` (rascunho, não enviada)

## Encerramento*
Não se aplica: episódio EM PRODUÇÃO, bloqueado no Gate A.
