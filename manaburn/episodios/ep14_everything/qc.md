# MB-EP14 · controlo de qualidade (ficheiro final com voz)

Ficheiro medido: `MB_EP14_Everything_916.mp4` (20/11/2026, com as vozes), não a prévia sem voz.
Ferramentas: `comum/qc/qc_video.py --frente manaburn`, `manaburn/bordas.py`, `ffmpeg cropdetect`, lista de eventos visuais a partir do `data.js` (trocas de canal, cortes, destaques, variantes `meio`, inserts) e diferença de quadros, folha de contacto (um quadro a cada 1,5 s) e quadros ampliados dos destaques, vistos a olho.

| Critério | Alvo | Medido | OK |
|---|---|---|---|
| Resolução / fps | 1080×1920 · 30 | 1080×1920 · 30 fps (H.264 + AAC 48 kHz) | sim |
| Duração | livre (ref. MB-EP12 45,5 s) | 46,70 s (42,83 s + fecho 3,87 s) | sim |
| Corte lateral (cropdetect) | nenhum | crop=1080:1920:0:0 em 1.399/1.399 amostras; `bordas.py` OK (925 quadros de TV, laterais 10–1068 px, topo 300 px) | sim |
| Loudness / pico | −14 ± 1 LUFS / < −1 dBTP | −14,9 LUFS / −1,2 dBTP | sim |
| Fecho do scanner | presente, sem encurtar | a partir de 42,83 s (3,87 s); trilha continua por baixo do fecho | sim |
| Factos = ficha | sim | todos os números são do anúncio oficial (18/11) ou contas com eles; cartas do Scryfall | sim |
| Quadro 0 | três drops na TV SAL, legível sem som | sim: «3 DROPS», três cartas, chaveta, «FORA», «EVERYTHING LEVA 2» | sim |
| Descoberta | ≤ 3,0 s | no ecrã desde o quadro 0; na fala 0,35–3,6 s | sim |
| Pagamento do gancho | campo 7 (10,7 / 16,2 / 28,0 s) | «Só em Halo Foil · Vendido à parte» aos 10,7 s (destaque aos 11,2 s); «$59,99» aos 16,2 s; «$234,98» aos 28,0 s | sim |
| Maior intervalo sem mudança visual | ≤ 3 s | 2,97 s (38,07–41,04 s, insert A/B até ao «Comenta aí»); antes das variantes `meio` era 4,3 s (fala 2) → corrigido | sim |
| Retenção | quadro 0 com Magic · mudança ≤ 3 s · som em cada revelação | sim · sim · troca de canal (8), destaque (4), raiva (4), carta/insert (4) | sim |
| Feedback visual por fala | imagem real em cada fala | 14/14 (TV ou insert); nenhuma «FOTO EM FALTA» | sim |
| Leitura com linha destacada | falas 2, 4, 8, 12 | destaques alinhados às linhas (conferido ampliado aos 6,0 / 13,0 / 22,5 / 36,5 s) | sim |
| Vozes | Talis / Erik, eleven_v4 | sim, 1 tomada cada; cortes impressos batem com as 14 falas (7 + 7) depois do corte pelo `tts` | sim |
| Sincronização fala/legenda | legenda com a fala | legendas vêm dos cortes reais (`data.js`) | sim |
| Legendas na zona segura | fora da coluna de botões | legenda do kit (`left 80 / right 160`), conferida na folha de contacto | sim |

## Problemas

- P0: nenhum. P1: nenhum aberto.
- P1 corrigidos nesta sessão: falas 8–12 do Mana desalinhadas no corte (legenda em algarismos × voz por extenso) → `processar_vozes.py`; intervalos de 3,3–4,3 s sem mudança nas falas 1, 2, 4, 8, 10 e 12 → variantes `meio`; destaques deslocados 18 px (moldura da tela) → frações corrigidas; cartas cortadas pela moldura e carimbos por cima de cartas nas telas compostas → reposicionados.
- A conferir pelo fundador na escuta: pronúncia de «Everything», «Halo Foil», «Balance of Power», «Deserts of Arrakis» e dos preços por extenso. Não foi possível ouvir nesta sessão (a duração de cada corte bate com o texto).
- P2 · o medidor da TV sobe a partir de 0 no quadro 0 (animação do kit; aos 0,5 s mostra «2»).
- P2 · `cards/google_play.png` não existe no repositório (herdado; o fecho do scanner tem o seu selo).

## Rubrica do gancho (folha de contacto do ficheiro final, sem som)

Relevância visual 5 · Impacto inicial 4 · Clareza 4 · Curiosidade 4 · Pagamento 5 · Identidade 5. Nenhuma nota ≤ 2.
