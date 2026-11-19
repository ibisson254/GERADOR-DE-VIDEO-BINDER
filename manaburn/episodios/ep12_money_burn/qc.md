# MB-EP12 · controlo de qualidade (prévia sem voz, ficheiro final da prévia)

Ficheiro medido: `MB_EP12_MoneyBurn_PREVIA_semvoz_916.mp4` (19/11/2026), não a prévia do navegador.
Ferramentas: `comum/qc/qc_video.py --frente manaburn`, `manaburn/bordas.py`, `ffmpeg cropdetect`, medição de mudança visual por diferença de quadros, folha de contacto vista a olho.

| Critério | Alvo | Medido | OK |
|---|---|---|---|
| Resolução / fps | 1080×1920 · 30 | 1080×1920 · 30 fps (H.264 + AAC 48 kHz) | sim |
| Duração | livre (ref. MB-EP11 ~48 s + fecho) | 44,40 s (40,53 s + fecho 3,87 s) — tempos estimados, sem voz | sim |
| Corte lateral (cropdetect) | nenhum | crop=1080:1920:0:0 em todos os quadros; `bordas.py` OK (928 quadros de TV, laterais 10–1068 px, topo 300 px) | sim |
| Loudness / pico | −14 ± 1 LUFS / < −1 dBTP | −14,6 LUFS / −1,7 dBTP | sim |
| Fecho do scanner | presente, sem encurtar | a partir de 40,53 s (3,87 s) | sim |
| Factos = ficha | sim | Oracle de 6 cartas conferido no Scryfall; sem preços nem estatísticas | sim |
| Quadro 0 | Unfinished Business inteira na TV SAL, legível sem som | sim (TV já acesa: `EP.fx.tv_ligada`) | sim |
| Descoberta | ≤ 3,0 s | legenda «o deck tá pronto, só falta UMA carta» de 0,35 a 2,8 s; nome da carta destacado aos 3,3 s | sim |
| Pagamento do gancho | ~27–33 s (campo 7) | Price of Progress aos 27,0 s; «20 de dano» aos 30,3 s; A/B aos 35,8 s | sim |
| Maior intervalo sem mudança visual | ≤ 3 s | 2,67 s (36,07–38,73 s) | sim |
| Retenção | quadro 0 com Magic · mudança ≤ 3 s · som em cada revelação | sim · sim · troca de canal (6), destaque (6), raiva (5), carta (3) | sim |
| Feedback visual por fala | imagem real em cada fala | 14/14 (TV ou insert); nenhuma «FOTO EM FALTA» | sim |
| Vozes e pronúncias | Talis / Erik, eleven_v4 | **não geradas** (créditos não autorizados) | P0 aberto |
| Sincronização fala/legenda | — | por medir com as vozes reais | pendente |

## Problemas

- **P0 · sem voz.** Prévia não publicável. Desbloqueio: autorização de ≈ 1.000 créditos (978 caracteres, 1 tomada por personagem), depois `process.py burn.mp3 mana.mp3`, render, `juntar_fecho.py`, novo QC.
- P1 corrigidos nesta sessão: tarja «undefined» (faltava `EP.bug`); quadro 0 com a TV a ligar (7 quadros sem carta) → `EP.fx.tv_ligada`; título do medidor cortado («POR NÃO BÁSICO»); três falas do Mana encurtadas para manter mudança visual ≤ 3 s; pico verdadeiro −0,1 dBTP → limitador (−1,7 dBTP); loudness −16,5 → −14,6 LUFS; cartas cortadas nas telas compostas.
- P2 · o medidor da TV sobe a partir de 0 no quadro 0 (animação do kit; a 0,5 s mostra o valor certo).
- P2 · `cards/google_play.png` não existe no repositório (o fecho do kit esconde o selo; o fecho do scanner tem o seu).

## Rubrica do gancho (medida na folha de contacto, sem som)

Relevância visual 4 · Impacto inicial 4 · Clareza 4 · Curiosidade 4 · Pagamento 5 · Identidade 5. Nenhuma nota ≤ 2.
