# Meta em Curto · EP06 · Prestação de contas: placar zero (segunda, 09/11/2026)

Primeiro episódio do ciclo «quinta prevê, segunda presta contas» (`../CICLO_SEMANAL.md`). Briefing: `python3 -I oraculo/previsoes/ciclo.py segunda 2026-11-09`. Cumpre a promessa do Giro de 08/11 («o TUBO volta segunda pra prestar contas») sem inventar placar: o Sealed de Star Trek só abre no Arena a 10/11.

Mensagem única: **opinião não mexe no placar.** A previsão de quinta continua de pé, com o mesmo grau de certeza, até haver jogos medidos.

## Narração (PT-BR, voz do TUBO; contagem e duração na ficha)

1. Quinta, eu cravei Rakdos. O primeiro relato de quem já jogou diz: cinco cores. Placar oficial: zero jogos.
2. Prestação de contas. Previsão original, sem editar: Rakdos no top três do Sealed de Star Trek, no 17Lands, em primeiro de dezembro.
3. O Sealed de Star Trek só abre no Arena terça, dia dez. Jogos medidos: zero.
4. O que chegou foi opinião: Strange New Worlds acima de tudo. Sopa de cinco cores.
5. Carta-símbolo: The Traveler, Simic. Força igual aos terrenos de nomes diferentes.
6. No meu modelo, Simic ligou o motor em um de cada quatro pools. Rakdos, em quase dois de cada três.
7. E uma previsão que não entrou no vídeo: três cores ou mais abaixo de duas. Se a sopa ganhar, erro duas.
8. Opinião não mexe no placar. *(corte seco da trilha)*
9. Certeza: a mesma. Baixa. Placar parcial: segunda que vem.
10. Quem fica mais alto no 17Lands? A: Rakdos. B: Simic. C: nenhum no top três.
11. Probabilidade calculada. Humanos, imprevisíveis.

## Storyboard

| # | Tempo (estim.) | Onde · expressão | Ecrã | Som |
|---|---|---|---|---|
| 1 | 0–5 s | Fora · desconfiado (monitor inclinado, código congela em «zero jogos») | Sobreposição em 3 linhas: `QUINTA: RAKDOS` · `1º RELATO: 5 CORES` · `PLACAR: 0 JOGOS` (a última a âmbar) | arranque CRT + batidas soltas |
| 2 | 5–5,5 s | Mergulho | push-in no vidro | modem |
| 3 | 5,5–13 s | Dentro | Cabeçalho `ARQUIVO: PR-TRK-01 · registrada 05/11/2026 · estado: PENDENTE`. Texto original em fósforo, palavra a palavra, com carimbo `TEXTO ORIGINAL · NÃO EDITADO`. Linha de fonte: «oraculo/previsoes/registo.yaml · fala do EP05» | banda entra |
| 4 | 13–17 s | Dentro | Painel `17LANDS · SEALED TRK` com `JOGOS: 0` e `ABRE NO ARENA: 10/11`. Fonte: «calendário do Arena, Wizards · consulta 05/11/2026» | zumbido curto em «zero» (como no EP05) |
| 5 | 17–22 s | Dentro | Tabela `EVIDÊNCIA RECEBIDA`: `TIPO O · MTG Rocks · Early Access no Arena · 05/11` / «Strange New Worlds acima do resto · Sealed puxa pra 5 cores» / `MUDA O PLACAR? NÃO` (a vermelho) | ticks |
| 6 | 22–27 s | Dentro | The Traveler (TRK 254) em scan linha a linha, ≥ 60 % da largura. Crédito: «The Traveler · Star Trek nº 254 · arte de Ioannis Fiore · Cartas © Wizards of the Coast · imagens via Scryfall · Star Trek © CBS» | — |
| 7 | 27–32 s | Dentro | Duas barras do EP05 (mesmo gráfico, mesmas cores): `RAKDOS 65` · `SIMIC 25 (teto)`. Carimbo `MODELO, NÃO JOGO · EP05` | — |
| 8 | 32–38 s | Dentro → sai | Cartão `PR-TRK-03 · SÓ REGISTRO · revelada hoje`: «3+ cores abaixo de 2 cores · Sealed TRK · 17Lands · 01/12». Contador `PREVISÕES EM RISCO: 2` | — |
| 9 | 38–40 s | Fora · confiante | `OPINIÃO ≠ PLACAR` | **corte seco** depois da frase (~1,2 s) |
| 10 | 40–44 s | Fora · analítico | Medidor GRAU DE CERTEZA 2/5, rótulo «igual a quinta · nada mensurável chegou». `PRÓXIMA CONFERÊNCIA: 16/11 · parcial · final 01/12` | banda volta |
| 11 | 44–50 s | Fora · analítico | «Quem termina mais alto no 17Lands?» + chips `A · RAKDOS` `B · SIMIC` `C · NENHUM NO TOP 3` | — |
| 12 | 50–55 s | Fora | Cartão de assinatura «META EM CURTO · com TUBO · BINDER Originals» + linha pequena `QUINTA: PREVISÃO DO MUNDIAL` + frase de fecho | — |
| fim | +3,9 s | — | `comum/outro/outro_binder_916.mp4` | — |

Rodapé do terminal em todos os planos de dentro: `● BINDER` à esquerda, `META EM CURTO · EP06` à direita. Legendas em estilo terminal, palavra a palavra.

Easter egg (proposta): «KOBAYASHI MARU» na vertical na chuva de código do bloco 4 (o teste sem vitória possível: um placar que ainda não pode ser ganho), ~14–16 s, canto inferior direito. Registar em `comum/easter_eggs.md` se aprovado.

## Notas de rigor

- «O primeiro relato de quem já jogou»: um artigo (MTG Rocks, 05/11), de quem jogou o Early Access a convite da Wizards. Não é «a internet» nem «a comunidade»: é uma opinião (tipo O).
- «Sopa de cinco cores»: o artigo diz que Strange New Worlds recompensa ir para cinco cores. Paráfrase, não citação.
- «Simic»: The Traveler é {G}{U} (Scryfall, TRK 254). A ligação Simic = Strange New Worlds é dos guias de arquétipos (Ultimate Guard, Draftsim); o MTG Rocks não fala em Simic. Por isso a narração diz «carta-símbolo», não «a carta que eles apontam».
- Números do bloco 7: os mesmos do EP05 (`oraculo/ep05/resultados/`, branch `meta-em-curto-ep05`). «Um de cada quatro» = 25; «quase dois de cada três» = 65.
- PR-TRK-03 era «só registo»; revelá-la não muda o texto nem o critério.
- «Terça, dia dez» em vez de «amanhã»: o vídeo continua certo se sair depois de segunda.
