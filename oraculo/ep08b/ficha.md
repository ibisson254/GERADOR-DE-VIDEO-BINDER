# MC-EP08B · «Campeão primeiro» (corte do MC-EP08) · 16/11/2026

Estado: **CONCLUÍDO, não publicado.** Pedido do fundador (08:48): refazer o EP08 com o gancho visual de cartas no início, como padrão daqui para a frente (`nucleo/DECISOES.md`, 16/11 08:48; regra em `oraculo/CONTEXTO.md` §7). Peça nova: o MC-EP08 fica no ar para comparação.

## Briefing

Mesma matéria do MC-EP08 (Mundial 32), por ordem inversa: a revelação (campeão com um deck de 1,6%) no quadro 0–3 s, as previsões e o placar depois. 29,7 s com fecho.

## Roteiro definitivo

Voz aprovada do EP08 (tomada 2, `P8i1X70szTFXue4174Mj`) reordenada por `oraculo/episodios/ep08b_voz.py`, sem créditos novos:
- Dentro: «Stefan Schütz, da Áustria, com Izzet Mission. Dois jogadores em cento e vinte e oito levaram esse deck. A carta que dá nome a ele é de Star Trek e entrou no formato uma semana antes.»
- Fora: «Previ três coisas sobre o Mundial. Acertei duas. Nenhuma delas era o campeão.» · «Placar: duas de três.» · «Você levaria ao Mundial um deck que só dois jogadores levaram?» · «Probabilidade calculada. Humanos, imprevisíveis.»

## Cenas

1. 0 s: **quadro 0 = Ral, Crackling Wit + Anthropological Mission + Into the Flood Maw em leque**, «CAMPEÃO DO MUNDO DE MAGIC», «O DECK QUE GANHOU O MUNDIAL».
2. 0,2 s: foto do campeão (autorizada) + «STEFAN SCHÜTZ · ÁUSTRIA», cartas na base; 1,8 s: selo «IZZET MISSION»; corte seco curto da trilha.
3. 3,2 s: «2 / 128» e grelha de 128 decks, só 2 verdes; «126 levaram outra coisa».
4. 6,0 s: Anthropological Mission em grande, «STAR TREK · ENTROU 1 SEMANA ANTES».
5. 10,4 s: sai do tubo; «Minhas 3 previsões» com ✔ ✔ ✘ e «Nenhuma era o campeão»; placar 2/3.
6. Pergunta SIM/NÃO, assinatura, fecho do scanner.
Easter egg: «MOCS» na chuva de código (~3–6 s), o mesmo do EP08.

## Fontes

`fontes.txt` (cópia das do MC-EP08).

## Controlo de qualidade (ficheiro final)

`qc_video.py --frente tubo`: 1080×1920, 30 fps, 29,70 s (25,83 s sem fecho), −14,1 LUFS, pico −1,7 dBTP, fecho presente, «sem problemas mensuráveis». Folha de contacto conferida a olho.
Retenção: **Quadro 0: Ral, Crackling Wit · Anthropological Mission · Into the Flood Maw (ecrã inteiro).** Revelação (campeão) aos 0,2 s; mudança visual ≤ 3 s; som em cada revelação (foto, selo, 2/128, carta, ✔ ✔ ✘, placar).

## Ficheiros finais

Vídeo e capa fora do Git (enviados ao fundador a 16/11). Recriar: pasta de trabalho → `python3 ep08b_voz.py <pasta do EP08 com voz.mp3 e words.json>` → `python3 ep08b_audio.py <kit>` → `python3 ep08b_render.py <kit>` → `… capa`. Capa: «O DECK CAMPEÃO» → **1,6%** → foto + 3 cartas → faixa «META EM CURTO · MUNDIAL 32 | 2 EM 128».
Legenda, comentário fixado e texto alternativo: nesta pasta.

## Para medir

Comparar com o MC-EP08 (7 s de tempo médio em 59 s): tempo médio, % de visualização e alcance em não seguidores às 6 h e às 24 h.
