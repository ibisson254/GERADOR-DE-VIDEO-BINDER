# MB-EP12 · controlo de qualidade (ficheiro final com voz)

Ficheiro medido: `MB_EP12_MoneyBurn_916.mp4` (19/11/2026, com as vozes), não a prévia do navegador. A tabela da prévia sem voz ficou no histórico do Git (commit 55c8651).
Ferramentas: `comum/qc/qc_video.py --frente manaburn`, `manaburn/bordas.py`, `ffmpeg cropdetect`, medição de mudança visual por diferença de quadros, folha de contacto vista a olho.

| Critério | Alvo | Medido | OK |
|---|---|---|---|
| Resolução / fps | 1080×1920 · 30 | 1080×1920 · 30 fps (H.264 + AAC 48 kHz) | sim |
| Duração | livre (ref. MB-EP11 ~48 s + fecho) | 45,50 s (41,63 s + fecho 3,87 s) | sim |
| Corte lateral (cropdetect) | nenhum | crop=1080:1920:0:0 em todos os quadros; `bordas.py` OK (953 quadros de TV, laterais 10–1068 px, topo 300 px) | sim |
| Loudness / pico | −14 ± 1 LUFS / < −1 dBTP | −15,0 LUFS / −1,3 dBTP | sim |
| Fecho do scanner | presente, sem encurtar | a partir de 41,63 s (3,87 s) | sim |
| Factos = ficha | sim | Oracle de 6 cartas conferido no Scryfall; sem preços nem estatísticas | sim |
| Quadro 0 | Unfinished Business inteira na TV SAL, legível sem som | sim (`EP.fx.tv_ligada`) | sim |
| Descoberta | ≤ 3,0 s | «o deck tá pronto, só falta UMA carta» de 0,35 a 3,1 s | sim |
| Pagamento do gancho | ~27–33 s (campo 7) | Price of Progress aos 27,3 s; «20 de dano» aos 30,7 s; A/B aos 36,6 s | sim |
| Maior intervalo sem mudança visual | ≤ 3 s | 2,97 s (36,87–39,83 s) | sim |
| Retenção | quadro 0 com Magic · mudança ≤ 3 s · som em cada revelação | sim · sim · troca de canal (6), destaque (6), raiva (4), carta (3) | sim |
| Feedback visual por fala | imagem real em cada fala | 14/14 (TV ou insert); nenhuma «FOTO EM FALTA» | sim |
| Vozes | Talis / Erik, eleven_v4, licença comercial (Starter) | sim, 1 tomada cada; cortes do `process.py` batem com as 14 falas (7 + 7) | sim |
| Sincronização fala/legenda | legenda com a fala | legendas vêm dos cortes reais (`data.js`) | sim |

## Problemas

- P0: nenhum. P1: nenhum aberto.
- A conferir pelo fundador na escuta: pronúncia de «Unfinished Business», «Greed» e «Price of Progress» (grafia fonética no `tts`). Não foi possível ouvir nesta sessão.
- P1 corrigidos nesta sessão: tarja «undefined» (faltava `EP.bug`); quadro 0 com a TV a ligar (7 quadros sem carta) → `EP.fx.tv_ligada`; título do medidor cortado («POR NÃO BÁSICO»); três falas do Mana encurtadas para manter mudança visual ≤ 3 s; loudness e pico da prévia sem voz corrigidos; cartas cortadas nas telas compostas.
- P2 · o medidor da TV sobe a partir de 0 no quadro 0 (animação do kit; a 0,5 s mostra o valor certo).
- P2 · `cards/google_play.png` não existe no repositório (o fecho do kit esconde o selo; o fecho do scanner tem o seu).

## Rubrica do gancho (medida na folha de contacto do ficheiro final, sem som)

Relevância visual 4 · Impacto inicial 4 · Clareza 4 · Curiosidade 4 · Pagamento 5 · Identidade 5. Nenhuma nota ≤ 2.
