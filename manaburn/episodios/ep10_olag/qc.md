# QC · Mana & Burn · EP10 · `ManaBurn_Ep10_OlagMiau_916.mp4` (11/11/2026)

Automático: `python3 -I comum/qc/qc_video.py ManaBurn_Ep10_OlagMiau_916.mp4 --frente manaburn` → "Sem problemas mensuráveis" (0 P0, 0 P1).

| Critério | Alvo | Medido no ficheiro final | OK |
|---|---|---|---|
| Resolução / fps | 1080×1920, 30 | 1080×1920, 30/1 | sim |
| Codecs | H.264 + AAC 48 kHz | h264 + aac 48000 Hz | sim |
| Duração | livre (constituição §6) | 69,83 s (65,97 s + fecho 3,87 s, sem encurtar) | sim (ver nota) |
| Loudness integrado | −14 LUFS | −14,1 LUFS | sim |
| Pico verdadeiro | < −1 dBTP | −1,4 dBTP (1.º render dava +2,6 dBTP entre 40 e 60 s pelo AAC: corrigido com limitador no `juntar_fecho.py`) | sim |
| Sem corte lateral | cropdetect 1080:1920 | 2093/2093 quadros = crop=1080:1920:0:0 | sim |
| Bordas dos planos da TV | laterais 0–1080, topo ≥ 295 | `bordas.py`: 931 quadros de TV, laterais 10–1068 px, topo ≥ 300 px | sim |
| Carta inteira, rodapé e crédito | — | Olag (0,05 / 2,5 / 18 / 28 / 34 / 46 s) e Wand of Orcus (51 s) inteiras, rodapé visível, crédito no topo | sim |
| Destaques alinhados | — | 18 s: 4 linhas das habilidades de marcadores; 28 s: 3 linhas da etapa final | sim |
| Medidor/placar | dado real ou regra com fonte | Censômetro "Gato + Zumbi = 1 vez só · Wizards" (ruling); placar "EXEMPLO: 3 viradas, −3" | sim |
| Legenda queimada | zona segura, legível | dentro da zona (folha de contacto); amarelos nas palavras-chave | sim |
| Bordões | intactos | "Lê a carta" (f4), "Isso devia ser banido" (f3), "Comenta aí" (f14) | sim |
| Pergunta A/B | igual à do comentário fixado | "Na sua mesa: A, montava Olag e Miau; ou B, removia antes do primeiro ronronar?" (1.ª linha do comentário) | sim |
| "Comenta aí" na parada seca; pancada desliga a TV | — | Comenta aí 64,19 s; pancada 65,44 s | sim |
| Fecho | ponto verde → fecho oficial, logo uma só vez | 65,93 s ponto verde; 65,97 s começa `outro_binder_916.mp4` (dif. média 0,07); logo do kit cortada antes de crescer; logo só no fecho (68–69 s) | sim |
| Telas do app | só gravação real | apenas o fecho oficial; scanner do kit desligado | sim |
| Sincronização voz/cortes | — | cortes do `process.py` batem com os tempos das palavras do Scribe (14/14 falas) | sim |
| Texto dito | igual ao roteiro | Scribe (0 créditos) devolveu o texto pedido palavra a palavra nas duas faixas | sim* |

\* Limitação real: o agente não ouve áudio. Não foi possível "assistir com áudio": a verificação sonora foi por medição (loudness, pico, envelope) e transcrição. Pronúncia de "Olag and Miau", "Wand of Orcus" e "Wizards" e a naturalidade das tags têm de ser ouvidas pelo fundador antes de publicar (P1 por confirmar).

Nota de duração: 66 s antes do fecho, acima dos 35–53 s históricos da série (próximo do Giro, 65 s). Não é defeito pela constituição §6; o roteiro de 14 falas foi usado como veio.

Visto quadro a quadro: folha de contacto 1 qps (70 quadros) + 16 quadros extraídos do ficheiro final.
