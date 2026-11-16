# MC-EP08B · «Campeão primeiro» (corte do MC-EP08) · 16/11/2026

Estado: **CONCLUÍDO, não publicado.** Pedido do fundador (08:48): refazer o EP08 com o gancho visual de cartas no início, como padrão daqui para a frente (`nucleo/DECISOES.md`, 16/11 08:48; regra em `oraculo/CONTEXTO.md` §7). Peça nova: o MC-EP08 fica no ar para comparação.

## Briefing

Mesma matéria do MC-EP08 (Mundial 32), por ordem inversa: a revelação (campeão com um deck de 1,6%) no quadro 0–3 s, as previsões e o placar depois. 30,4 s com fecho.

## Roteiro definitivo

Voz aprovada do EP08 (tomada 2, `P8i1X70szTFXue4174Mj`) reordenada por `oraculo/episodios/ep08b_voz.py`, sem créditos novos:
- Dentro: «Stefan Schütz, da Áustria, com Izzet Mission. Dois jogadores em cento e vinte e oito levaram esse deck. A carta que dá nome a ele é de Star Trek e entrou no formato uma semana antes.»
- Fora: «Previ três coisas sobre o Mundial. Acertei duas. Nenhuma delas era o campeão.» · «Placar: duas de três.» · «Você levaria ao Mundial um deck que só dois jogadores levaram?» · «Probabilidade calculada. Humanos, imprevisíveis.»

## Cenas (v2, 16/11 09:12: abertura no modelo do MC-ESP01 + lista do deck)

1. 0 s: **grelha 2×2 em ecrã inteiro** sobre o TUBO escurecido: foto do campeão (selo «CAMPEÃO»), Anthropological Mission («4 cópias»), Ral, Crackling Wit e Into the Flood Maw («3 cópias»); cabeçalho «CAMPEÃO DO MUNDO · MAGIC».
2. 1,8 s: a foto acende a verde, o selo vira «IZZET MISSION», o resto escurece.
3. 3,2 s: caixa «1,6% · 2 em 128 jogadores».
4. 6,0 s: os quadros sobem para a fila por cima do TUBO, a Anthropological Mission acende e aparece no ecrã dele; mergulho aos 6,5 s.
5. 7–11 s: **lista campeã completa** (60 cartas, Melee via MTGTop8) com Anthropological Mission a verde e em insert; «STAR TREK (TRK 46) · entrou no formato 1 semana antes do Mundial».
6. 11,1 s: sai do tubo; «Minhas 3 previsões» com ✔ ✔ ✘ e «Nenhuma era o campeão»; placar 2/3; pergunta SIM/NÃO; assinatura; fecho do scanner.
Easter egg: «MOCS» na chuva de código da lista (~7–11 s).

## Fontes

`fontes.txt` (cópia das do MC-EP08).

## Controlo de qualidade (ficheiro final)

`qc_video.py --frente tubo` (v2): 1080×1920, 30 fps, 30,40 s (26,53 s sem fecho), −14,1 LUFS, pico −1,9 dBTP, fecho presente, «sem problemas mensuráveis». Folha de contacto conferida a olho.
Retenção: **Quadro 0: grelha 2×2 (foto do campeão + Anthropological Mission, Ral, Crackling Wit, Into the Flood Maw), modelo do MC-ESP01.** Revelação (campeão) no quadro 0, «1,6%» aos 3,2 s; mudança visual ≤ 3 s; som em cada revelação (foto, selo, 2/128, carta, ✔ ✔ ✘, placar).

## Ficheiros finais

Vídeo e capa fora do Git (enviados ao fundador a 16/11). Recriar: pasta de trabalho → `python3 ep08b_voz.py <pasta do EP08 com voz.mp3 e words.json>` → `python3 ep08b_audio.py <kit>` → `python3 ep08b_render.py <kit>` → `… capa`. Capa: «O DECK CAMPEÃO» → **1,6%** → foto + 3 cartas → faixa «META EM CURTO · MUNDIAL 32 | 2 EM 128».
Legenda, comentário fixado e texto alternativo: nesta pasta.

## Para medir

Comparar com o MC-EP08 (7 s de tempo médio em 59 s): tempo médio, % de visualização e alcance em não seguidores às 6 h e às 24 h.
