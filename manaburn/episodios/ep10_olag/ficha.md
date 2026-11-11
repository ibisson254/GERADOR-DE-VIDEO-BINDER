# Ficha · Mana & Burn · EP10 · O gato zumbi que cobra a mesa (Olag and Miau, New Friends)

## Classificação
- Série: Mana & Burn
- Classe: leitura de carta + comentário sobre Commander
- Complexidade: média
- Estratégia (constituição §3): verificação rápida (Oracle + Release Notes oficiais)

## Editorial
- Objetivo: entreter, explicar a mecânica e gerar respostas A/B.
- Proposta de valor: um comandante que mistura Gatos e Zumbis e transforma criaturas viradas numa cobrança de vida para cada adversário.
- Público: jogador casual e de Commander no Brasil.
- Hipótese: a pergunta A/B concreta gera mais comentários por 1.000 views do que uma pergunta aberta.
- Gancho (0–3 s): "O Magic lançou um gato zumbi que cobra vida da mesa no fim do turno." com a carta na TV.

## Fontes
Ver `ficha_fontes.md`. Oracle e PNG pela API Scryfall (mbc/48 e afc/297), ruling "conta só uma vez" nas Release Notes da Wizards (29/07/2026), CR 608.2h para "vale quem continua virado quando resolve". Sem EDHREC, preço ou Salt Score.

## Roteiro final (14 falas, brief do fundador)
Alterações mínimas, só de naturalidade e de factos: f2 "Criatura lendária, Zumbi e Gato" (era "zumbi-gato"); f8 sem "nem o dano"; f13 "Olag e Miau" (forma falada, igual no comentário fixado). Bordões intactos.

## Produção
- Kit v2 de `manaburn/` sem alterações ao motor (index.html, process.py, render.py, bordas.py tal como estão em `main`).
- Vozes: ElevenLabs eleven_v4, flow "Mana & Burn — Ep. 10 (Olag and Miau)" (Pd0P4C3y6A8nk1zpNL4X). Burn: Talis (E9a8LlXPNWtyvvSoZzrb), 717 créditos; Mana: Erik (nfiLpQ54jEQninp3nNqL), 744 créditos. 1 geração por voz, autorizada pelo fundador a 11/11. Ritmo Burn ×1,06, Mana ×1,12, respiro 0,14 s. Grafias TTS: Ólag én Miáu, Niú Fréndis; Uónd óf Órcus; Uízards; Á / Bê. Scribe: 0 créditos, texto idêntico ao pedido.
- Planos: 1 tv · 2 cuM · 3 wide · 4 tvtext · 5 push · 6 tvtext2 · 7 tv (placar EXEMPLO) · 8 cuM · 9 cuB · 10 tv (Censômetro) · 11 tv2 + insert Wand of Orcus · 12 wide · 13 cuB (point_cam) · 14 cuM (remote; TV desliga).
- Destaques medidos no PNG 744×1040: tvtext = 4 linhas das habilidades de marcadores; tvtext2 = 3 linhas da etapa final. Zoom 1,5.
- TV SAL: sem Putômetro (sem Salt Score verificado). Medidor "CENSÔMETRO" com a regra oficial (Gato + Zumbi = 1 vez só · Wizards); placar "EXEMPLO: 3 VIRADAS · −3 de vida para cada oponente"; 8 manchetes (as 3 do brief + 5, sem estatísticas; chamada do Ep. 9).
- Easter egg: relógio da TV SAL em "00:48" = nº 48 da carta na coleção.
- Fecho: `juntar_fecho.py` (do Ep. 9) corta o vídeo do kit em T_SLAM + 0,52 s (ponto verde, antes da logo do kit) e cola o fecho oficial `comum/outro/outro_binder_916.mp4` sem encurtar. Acrescentado ganho +0,6 dB e limitador antes do AAC (pico verdadeiro).
- Capa: quadro de 2,5 s (Burn a apontar a TV com a carta).

## QC
Ver `qc.md`: 0 P0; 0 P1 medidos; 1 P1 por confirmar pelo fundador (ouvir pronúncia; o agente não ouve áudio).

## Entregáveis
- [x] Vídeo (fora do Git) · [x] Capa (fora do Git) · [x] Legenda (`legenda.txt`, 601 caracteres) · [x] Comentário fixado (951) · [x] Texto alternativo · [x] Fontes · [x] QC

## Estado
Produzido, não aprovado, não publicado.

## Depois de publicar
- Métrica principal: respostas A/B por 1.000 views. Secundária: partilhas.
- Resultado observado: —
- Aprendizagem: —
