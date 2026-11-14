# Roteiro definitivo · VV-PG01 · Pregão Magic · Brutal Bass Edition

Formato alternativo do Pregão (fundador, 14/11/2026): **sem personagem, mascote, avatar ou apresentador visual.** A história é contada por cartas reais, números, montagem e música. A narração (abaixo) está escrita e cronometrada pelo `MUSIC_MAP.md`, mas **ainda não foi gravada**: falta a autorização de créditos do ElevenLabs (pedida a 14/11, 00:18, sem resposta afirmativa). A v1 entregue funciona só com o texto do ecrã, a música e o sound design.

Voz prevista: Vince Vault (`L93SDe6kGQj79D6svMgA`, voz da frente; nenhuma voz de outra série), `eleven_v3`, PT-BR, frases curtas, energia de corretor. ~610 caracteres por tomada.

## Narração (PT-BR, "você")

| Janela | Bloco | Texto | No ecrã ao mesmo tempo |
|---|---|---|---|
| 0,2–3,1 | V1 · Abertura | "O pregão abriu. E uma carta dobrou de preço em sete dias." | parede de cartas → Urza atravessa → gráfico → **+104%** em 3,16 |
| 4,7–6,8 | V2 · Alta | "Urza, Chief Artificer. Commander de The Brothers' War." | carta, edição, preço em reais |
| 7,2–10,8 | V3 · Causa | "Segundo o MTGStocks, os guias de upgrade do deck dos Borg, do Star Trek, colocaram o Urza na lista." | tipografia cinética da causa |
| 11,5–13,6 | — | (silêncio de voz: a música cresce) | "+ ? ? %" |
| 13,9–18,6 | V4 · Alta 2 | "Uchuulon: mais quarenta e oito. Dois comandantes novos do Mystery Booster pedem ele no deck." | +48%, causa |
| 18,9–20,4 | V5a · Virada | "Do outro lado do pregão…" | seta vira vermelha |
| 20,9–26,3 | V5b · Queda | "Capitão Picard: menos quarenta e seis por cento. Na semana do lançamento do Star Trek." | −46%, contexto |
| 26,55–27,40 | — | (break: silêncio total) | RADAR |
| 27,7–33,9 | V6 · Radar | "No radar, as shocklands do Star Trek. Mesma coleção, dois sentidos: Overgrown Tomb caiu pela metade. Watery Grave subiu quarenta e quatro." | split screen, leque, tabela |
| 34,4–37,5 | V7a · Fecho | "Fechamento da semana." | painel de fecho |
| 37,8–41,0 | V7b · Ponte | "Você acabou de ver como o mercado se mexeu. Agora veja o valor de referência da sua coleção no BINDER Vision." | E A SUA PASTA? → BINDER Vision |
| 41,2–45,07 | — | (sem voz: fecho oficial, a música sobe) | scanner real |

Regras aplicadas: a voz não lê o que o ecrã já escreve palavra por palavra (o ecrã tem edição, preço, conversão e fonte; a voz dá o sentido); nenhuma previsão, nenhuma recomendação, nenhuma causa que a fonte não dê.

## Integração quando a voz existir

`python3 som.py MUSICA.mp3 SAIDA voz.wav` (ducking de −7 dB na música onde há voz, envolvente de 120 ms) e `montar.py` com o novo `mix.wav`. As janelas acima já cabem nas frases; se uma tomada sair mais longa, encurtar a frase, não acelerar a voz.
