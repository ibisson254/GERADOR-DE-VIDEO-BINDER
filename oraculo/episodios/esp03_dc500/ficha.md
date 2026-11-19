# Ficha · Meta em Curto · ESP03 · O mais jogado é o que mais vence? (Duel Commander 500)

## Identificação*
- ID editorial*: `MC-ESP03`
- Estado no registo*: EM PRODUÇÃO (desde 19/11/2026, 15:10) · Gate A resolvido às 16:45 · voz autorizada pelo fundador às ~16:55 («Sim, gerar a voz») · vídeo final renderizado às 17:05 · **publicação e envio ao Farpas dependem do fundador**
- Aprovação do fundador: pauta e parceiro-alvo decididos a 19/11/2026 (`nucleo/DECISOES.md`, `comum/parcerias.md`). Tese final, voz e envio ainda não aprovados.

## Classificação*
- Frente*: Meta em Curto (TUBO) · especial com parceiro-alvo
- Classe de conteúdo*: meta (Relatório do Meta, `oraculo/PERFIL.md`)
- Complexidade: média
- Estratégia: análise de dados — separar **representação** (listas), **desempenho** (win rate ou conversão, conforme o portal publica) e **amostra** (denominador)

## Originalidade*
- Objeto*: portal Duel Commander 500 (Farpas de Mana); Cloud, Midgar Mercenary (FIN 10) × Phelia, Exuberant Shepherd (MH3 40)
- `memoria.py pauta --objeto "Duel Commander 500" --tema "popularidade versus desempenho competitivo dos comandantes"`* (19/11/2026, 15:08): **PAUTA LIVRE**. Conferido à mão: nenhum MC/MB/CM/LL trata DC500 nem popularidade × desempenho de comandantes; o MC-EP01 (conversão por arquétipo no AC13) é outro formato, outro evento e outra fonte.
- Relações: MC-ESP01 e MC-ESP02 (modelo de abertura e de parceria); MC-EP01 (mesmo tipo de raciocínio, representação × conversão).
- Previsões abertas do TUBO (`ciclo.py continuacao`, 19/11): PR-TRK-01..04 — nenhuma toca este episódio; o MC-ESP03 não faz previsão.

## Editorial (briefing)
- Objetivo*: ensinar ao jogador de Duel Commander a não confundir «muito jogado» com «forte», com os dados públicos do portal do Farpas; servir de prévia para a collab.
- Proposta de valor*: em 30 s você sabe se o comandante mais jogado do DC500 é mesmo o que mais vence — e quanto a amostra aguenta.
- Público: jogadores de Duel Commander 500 no Brasil (público do Farpas) e jogadores competitivos de Commander.
- Hipótese a testar: a comparação de dois comandantes na grelha segura mais os 3 s do que a apresentação de um só (termo de comparação: MC-EP08B, ambos sem impulso).
- Variável em teste: 1 — abertura com comparação de dois × campeão único (MC-EP08B).
- Tese*: **o mais jogado também é o que mais vence — mas a vantagem sobre o 2.º ainda cabe na margem de erro** (cenário `A_melhor_margem`, devolvido por `dados/calcular.py` a 19/11, 16:45). Responde ao título sem o forçar. Evidência mais forte: Cloud 1.º em decks (522) e em win rate (63,1 %, 1.323 partidas). Contra-argumento: a 2.ª (Phelia, 61,3 %) fica a 1,8 ponto, margem −2,9 a +6,5. Grau de certeza: alto para «lidera hoje», baixo para «é melhor». Risco de leitura errada: ouvir «o Cloud é o melhor» — o painel da diferença e a frase da margem existem para isso. O espectador aprende: popularidade ≠ desempenho, e uma vantagem pequena precisa de amostra. Tabela de teses fixada antes dos dados:

| Veredito do cálculo | Tese que se grava | Grau de certeza |
|---|---|---|
| A (mais listas) também tem o melhor indicador comparável | «O mais jogado também é o que mais vence — desta vez o hype acerta.» | o do intervalo |
| B supera A e o intervalo de 95 % de B fica acima do valor de A | «Popularidade e vitória contam histórias diferentes.» (título de trabalho mantém-se) | alto para este período |
| B supera A mas o intervalo inclui o valor de A | «Um comandante menos jogado tem números melhores — mas a amostra ainda não prova.» (tese ajustada: vai ao fundador antes da voz) | baixo; dito no ecrã |
| O portal não publica win rate com denominador, só conversão | pergunta passa a «O mais jogado é o que mais chega ao Top 4?» (ajuste de tese, vai ao fundador) | conforme o intervalo |
| Nenhum indicador comparável | não se grava; pauta alternativa: «O que é popular no DC500 em <período>» (só representação) ou cai | — |

Regras da escolha de B (fixadas **antes** de ver os números, para não escolher o contraste): mesmo período e filtros; sem alertas do script (≥ 20 listas, ≥ 50 partidas quando houver win rate, ≥ 3 torneios, ≤ 50 % das listas num só torneio); B = melhor indicador entre os que passam; nunca win rate de um contra conversão de outro.

**Método estatístico (corrigido a 19/11, 16h):** a diferença B − A avalia-se com o intervalo de Newcombe a 95 % (método 10, híbrido de Wilson), validado no exemplo publicado. Os intervalos de Wilson de cada comandante não provam diferença e deixam de servir de veredito. Pressupostos que os totais não verificam (independência — jogos A×B contam nos dois lados; unidade partida × jogo; empates; universo dos 20) ficam escritos no ecrã e em `fontes.md`. Códigos do veredito: `B_fora_margem`, `dentro_margem`, `A_melhor`.

## Gancho visual* (`nucleo/SHOWRUNNER.md` §4.1) — v2, 19/11 · estrutura fechada, números pendentes

1. Quadro 0*: grelha 2×2 completa sobre o TUBO escurecido — carta Cloud · «MAIS JOGADO · DECKS · 1.º do portal» (522 entra aos 1,0 s) · «2.º MAIOR WIN RATE · WIN RATE · em 603 partidas» (61,3 % aos 1,0 s) · carta Phelia; «DUEL COMMANDER 500 · acumulado até 19/11/2026» e linha de fonte. O «2.º» abre a pergunta: quem é o 1.º?
2. Objeto real*: Cloud, Midgar Mercenary (FIN 10, Kazto Furuya) e Phelia, Exuberant Shepherd (MH3 40, Rudy Siswanto), imagens oficiais do Scryfall, inteiras (`cartas/creditos.json`).
3. Ação no 1.º segundo*: as peças assentam (1,05 → 1); 0,3–0,8 s scan verde sobre a carta A e contorno.
4. Som*: tum de CRT a 0,0 s, quatro cliques, modem no scan, pop nos números (1,0 s) e no salto para B (1,6 s).
5. Descoberta até 3 s*: aos 1,0 s «522 DECKS» × «61,3 % WIN RATE em 603 partidas»; aos 2,0 s «O MAIS JOGADO É O QUE MAIS VENCE?» (completa aos 2,6 s).
6. Promessa*: dizer quem vence mais e se a diferença é real ou só amostra.
7. Pagamento*: 8,5–10,4 s (Cloud 63,1 %: o mais jogado é o 1.º) e 19,0 s (veredito «LIDERA, MAS DENTRO DA MARGEM» ao lado do ponto +1,8 e da margem −2,9 a +6,5).

| Rubrica (1–5) | Prevista | Medida na prévia v2 (sem dados) |
|---|---|---|
| Relevância visual | 5 | 5 (versão sem voz de 19/11, 16h50: cartas reais) |
| Impacto inicial | 4 | 4 |
| Clareza | 4 | 4 (unidades e pergunta legíveis em miniatura) |
| Curiosidade | 5 | 4 |
| Pagamento | 4 | 4 (pago aos 8,5 e 19,0 s; o «por pouco» pode soar a anticlímax) |
| Identidade | 5 | 5 |

## Roteiro definitivo*
**Definitivo** em `roteiro.md` (topo) e `locucao.txt`, por gravar. Roteiro v2 em `roteiro.md` (texto comum + três cenários). Revisão narrativa (§4.2) feita sobre a estrutura; repete-se com os números. Auditoria da prévia v1 e correções: `auditoria_previa.md`.

## Fontes e evidências*
Ver `fontes.md` (verificado V1–V5, tentativas de acesso, tabela final por preencher). Capturas em `capturas/` (lista do que falta em `capturas/LEIA-ME.md`). Cálculos em `dados/calcular.py` (testado com dados sintéticos; `extracao.csv` vazio).

Limitações: ver `fontes.md` §Limitações.
Créditos e autorizações: nenhuma autorização do Farpas existe. Nada em `oraculo/autorizacoes/`.

## Produção
- Recursos reutilizados: `oraculo/esp01/esp01_render.py` (`hook()`, terminal, chuva, TUBO) e `oraculo/episodios/ep08b_render.py` como base do `esp03_render.py`; `oraculo/esp01/esp01_audio.py` para mix; `oraculo/assets/tubo_mestra_916.png`; `oraculo/musica/tubo_tema.mp3`; `comum/outro/outro_binder_916.mp4`. O TUBO não é regenerado.
- Script de render: `esp03_render.py` (19/11, derivado do ESP01): grelha dupla, mergulho, terminal com barras no mesmo eixo 0–100 %, faixa de 95 %, TUBO (imagem-mestra intacta), legendas terminal, trilha + SFX, fecho do scanner, capa e recorte da grelha. Lê `dados/episodio.json`; sem valor, mostra o marcador e a marca «PRÉVIA TÉCNICA · SEM DADOS», e nunca desenha barra sem número. Falta para a versão final: cartas do Scryfall, `episodio.json` com os números, tempos a partir de `words.json` da voz.
- **v4 (19/11, 17h40, pedido do fundador):** cartas no quadro 0 (0–1,7 s) → TUBO a falar com o LED a pulsar com a voz e as cartas ao lado da cabeça → a carta Cloud voa para o ecrã do TUBO (2,6 s) e o vídeo mergulha (2,95–3,35 s), como nos episódios antigos; mergulho no ecrã também ao voltar do TUBO aos dados (24,85 s) e saída do ecrã ao entrar no TUBO (21,25 s e 31,4 s); chuva de código verde estilo Matrix visível no fundo de todos os planos de cartas (painel da diferença com fundo escuro para se ler). Sem créditos novos. QC: 34,93 s + fecho, −14,0 LUFS, pico −4,0 dBTP, fecho presente, sem problemas mensuráveis; maior intervalo sem mudança relevante 3,0 s.
- **v3 (19/11, 17h45, pedido do fundador com vídeo de referência):** legenda grande no topo sincronizada com a voz, carta grande ao centro com troca em rotação 3D, número em caixa por baixo da carta, capturas reais do portal (matriz e galeria) como prova, selo «FONTE: portal Duel Commander 500 · @farpasdemana» com o cabeçalho do portal em todos os planos de dados, TUBO só na leitura e no fecho, trilha até ao fim do fecho. Frase de abertura gravada (48 créditos, geração `9yjcYfXw6loEyPtVMywv`, −2 dB para nivelar); pausas da tomada principal encurtadas para 0,10 s (0,45 s antes da diferença, 0,25 s antes da assinatura) para caber em 35 s sem mudar o atempo. Voz montada: 34,81 s; tempos em `dados/episodio.json` (`voz_tempos`, `seq`). Créditos totais do episódio: 460.
- Voz: Antonio de Jesus (`MK5tXPmT83J5SUlpUo4K`, eleven_v4, atempo 1,10), **1 tomada, 412 créditos** (estimativa prévia confirmada; «1.323» escrito por extenso para a pronúncia). Flow ElevenLabs `LtUgaMWrnvu8UFurYG93`, geração `MKgHjfpDwkVjVQByV40l`. Voz entra aos 2,0 s; pausa de 0,4 s antes da diferença (corte seco). Frases sincronizadas por deteção de pausas (sem transcrição paga); tempos em `dados/episodio.json` (`vo`, `beats`). Recriar: descarregar a geração → `ffmpeg -i voz.mp3 -af atempo=1.10 -ar 48000 -ac 1 voz_rapida.wav` → `python3 -I esp03_render.py <raiz> final voz_rapida.wav`.
- Easter egg: nenhum (0).
- Riscos: P0 se um número sair sem denominador ou se win rate e conversão se misturarem; risco de parceria se o vídeo sugerir collab.

## Controlo de qualidade*
Medido no ficheiro final `ESP03_META_EM_CURTO.mp4` (19/11/2026, 17:05) com `qc_video.py --frente tubo` (`qc_final.json`), cropdetect e medição de mudanças visuais.

| Critério | Alvo | Medido | OK |
|---|---|---|---|
| Resolução / fps | 1080×1920 · 30 | 1080×1920 · 30,0 | sim |
| Duração | 25–35 s sem fecho | v3: 34,93 s + fecho (38,80 s) | sim |
| Corte lateral (cropdetect) | nenhum | 1080:1920 em 961/991 amostras; o resto são cenas escuras do terminal | sim |
| Loudness / pico | −14 ± 1 LUFS / < −1 dBTP | v3: −14,0 LUFS / −4,0 dBTP; trilha audível por baixo do fecho (−14 dB médio a 35,5–37 s) | sim |
| Fecho do scanner | presente, inteiro | v3: presente a partir de 34,93 s (dif. média 0,06) | sim |
| Factos = ficha | sim | todos os números do ecrã e da voz estão em `fontes.md` | sim |
| Quadro 0 | campo 1, legível sem som | grelha com Cloud e Phelia, rótulos e unidades | sim |
| Descoberta | ≤ 3,0 s | v3: pergunta e cartas no quadro 0; voz cita a fonte de 0 a 3,1 s | sim |
| Pagamento do gancho | campo 7 (± 3 s) | v3: Cloud 63,1 % aos 12,7 s; veredito aos 27,1 s | sim |
| Maior intervalo sem mudança visual | ≤ 3 s | v3: 3,0 s (18,3–21,3 s, plano das duas cartas) | sim (no limite) |
| Retenção | Magic no quadro 0 · mudança ≤ 3 s · som em cada revelação | sim · sim · sim | sim |
| Zona segura | conteúdo em x 80–940, y 220–1540 | conferido na folha de contacto (HUD da série fora, como nos episódios anteriores) | sim |
| P0 / P1 abertos | 0 / 0 | 0 / 0 (P2: a trilha entra cheia a meio de um bloco; fecho do TUBO varia só a expressão) | sim |

## Ficheiros finais*
- Vídeo final: `ESP03_META_EM_CURTO.mp4` (v3) · 38,80 s (34,93 s + fecho) · entregue ao fundador na conversa de 19/11/2026 (não versionado; recria-se com `esp03_render.py final`). Versões anteriores (prévias técnicas v1, v2 e sem voz) só na conversa.
- Capa: `ESP03_CAPA.png` («LIDERA POR POUCO · 63,1%», TUBO desconfiado, cartas Cloud e Phelia ao fundo) + `ESP03_CAPA_grelha.png` (recorte 3:4, conferido em miniatura), entregues na conversa de 19/11/2026 (`esp03_render.py capa`).

## Pacote de publicação* (rascunhos nesta pasta, com marcadores `[PENDENTE]`)
- [x] `legenda.txt` · [x] `comentario_fixado.txt` · [x] `texto_alternativo.txt` · [x] `fontes.md` · [x] `mensagem_farpas.txt` (pronta, não enviada; prazo de 5 dias a contar do envio)
- Plano B (se o Farpas não aceitar): publicar com crédito ao portal e marcação, sem afirmar parceria (`comum/parcerias.md`).

## Encerramento*
- [x] Briefing e roteiro definitivo nesta ficha
- [x] Legenda, comentário fixado e texto alternativo na pasta
- [x] Fontes e evidências (`fontes.md`, `capturas/`, `dados/`)
- [x] Controlo de qualidade preenchido
- [x] Localização do vídeo e da capa
- [x] `comum/REGISTRO_EDITORIAL.md` atualizado
- [x] `comum/historico.md`
- [x] Easter egg: nenhum
- [x] `STATUS.md`
- [x] `memoria.py encerramento MC-ESP03` = ENCERRAMENTO OK (19/11, 17h10)
- [ ] Commit conferido no GitHub (ver handoff)
- [ ] Resposta do Farpas em `oraculo/autorizacoes/` (só quando existir)
