# Ficha · Multiverse Capital (Vince Vault) · VV-EP01 · O Pregão de Véspera

Estado: **CONCLUÍDO** (12/11/2026, 17h Lisboa) — produzido e conferido; publicação por decidir pelo fundador.
Ordem de produção: fundador, 12/11/2026 16:34 — «Comece a produção do vídeo e só pare quando terminar» (lido como aprovação da pauta e da voz; registado em `nucleo/DECISOES.md`).

## Classificação
- Série: Multiverse Capital, apresentada pelo Vince Vault (frente aprovada a 12/11)
- Classe de conteúdo: mercado
- Complexidade: média
- Estratégia: explicar um número que parece grande e mostrar o que está por trás dele (causa única: preço de pré-venda assente numa venda)

## Editorial
- Objetivo: estreia da série com o sistema de edição «Pregão» (`vince/EDICAO.md`, branch `vince/kit-v1`)
- Proposta de valor numa frase: o Spock de US$ 299,98 tem esse preço por causa de uma venda; antes do lançamento, preço é o que o vendedor pede
- Público: jogador brasileiro adulto que abre Collector Booster ou guarda cartas
- Hipótese a testar: o arco euforia → telefonema → lucidez segura a retenção aos 3 s e gera guardados (o pagamento é útil)
- Gancho (0–3 s): «Trezentos dólares!» falado e escrito no painel, a contar, desde o primeiro quadro
- Fecho: `comum/outro/outro_binder_916.mp4`
- Easter egg: nenhum

## Roteiro definitivo (voz do Vince, PT-BR)

| Vídeo | Fala | Plano |
|---|---|---|
| 0,0 | Trezentos dólares! | Cena · aponta · painel US$ 299,98 (contador 0,8 s) |
| 1,9 | Num Spock de Star Trek que nem saiu da caixa. | Carta #535 (drop aos 1,71 s) → placa NEM SAIU DA CAIXA → pitch |
| 5,6 | Primeiro lugar do ranking! | Placa 1º NO RANKING |
| 7,3 | E a carta só chega nas lojas dia treze. | Cena · painel com top 3 → placa 13/11 |
| 10,4 | Trezentos dólares, meu amigo. É o pregão do século! | Grande plano (boca sincronizada) → dinheiro → placa PREGÃO DO SÉCULO |
| 15,6 | Buy the d— | Placa BUY THE D— · cortado pelo toque (bordão desmentido em cena) |
| 16,3 | (toque) | A bateria pára · choque → pega no telefone |
| 17,3 | Fala. / …Quantas vendas? / …Uma? | Ao telefone · Fonte: `fonte_hesita`, `fonte_confirma`, `telefone_pousa` |
| 21,6 | Uma venda. Uma. | Placa vermelha 1 VENDA |
| 23,9 | O preço de mercado é essa venda. | Testa → painel PREÇO DE MERCADO = 1 VENDA |
| 26,2 | E o anúncio mais barato hoje? Cento e sessenta. | Grande plano → braços → placa US$ 159,98 ≈ R$ 893 |
| 30,2 | Pré-venda não é mercado. O preço de verdade nasce quando a carta chega. | Confidência → placa PRÉ-VENDA ≠ MERCADO → grande plano |
| 35,2 | Quer saber quanto vale a sua pasta? Escaneia no BINDER Vision. | Painel QUANTO VALE A SUA PASTA? → placa CTA |
| 40,0 | — | Fecho do scanner (3,87 s) |

## Fontes e evidências

| Afirmação | Tipo | Fonte | Data |
|---|---|---|---|
| #535 = Mr. Spock, Science Officer, mítica, Showcase, só surge foil, arte de Grant Griffin, lança 13/11/2026 | facto | Scryfall API `cards/trk/535` | 12/11/2026 |
| Preço de mercado US$ 299,98; venda mais baixa = venda mais alta = US$ 299,98; 12 anúncios, o mais barato a US$ 159,98; item de pré-venda com envio previsto a 13/11 | facto | TCGplayer, produto 725123 (página lida via índice de pesquisa; a página direta exige JavaScript) | 12/11/2026 |
| O US$ 299,98 corresponde a uma venda | facto (fonte secundária) | NerdSnack, «MTG Star Trek Chase Cards», tabela de 06/11: «$299.98 (1 sale)» | 06/11/2026 |
| Ranking: 1º Spock #535 US$ 299,98 · 2º Picard #497 US$ 297,99 · 3º Kirk #542 US$ 168,99 (preços TCGplayer) | facto | TCGIndex, página do set Star Trek | 12/11/2026 |
| Conversão ≈ R$ 893 (US$ 159,98 × R$ 5,58) | cálculo | dólar comercial de fecho de 10/11/2026, R$ 5,58 (Metrópoles) | 10/11/2026 |
| Lançamento a 13/11/2026 | facto | Scryfall (released_at) e TCGplayer (envio previsto) | 12/11/2026 |

Não entra no vídeo (decisão do briefing v2): a taxa de 1 % do slot de Collector Booster (é de uma categoria, não do #535) e «a carta mais cara de Star Trek» (outros rastreadores dão valores maiores ao #353 foil; diz-se só «primeiro do ranking»).

**Verificar antes de publicar (P1):** abrir no navegador a página do TCGplayer do #535 e confirmar em «Latest Sales» que continua a haver uma só venda. Se houver mais, as falas «Uma venda. Uma.» e a placa 1 VENDA deixam de ser verdade e o episódio não sai assim.

## Produção
- Kit: `vince/kit/v1/` da branch `vince/kit-v1` (PR #23, sem merge). O render lê o kit por argumento.
- Montagem: `render.py` (PIL → ffmpeg, 1080×1920, 30 fps) e `mistura.py` (voz no relógio do vídeo, Fonte, efeitos, faixa, −14 LUFS, fecho). Divergência do `PROMPT_EPISODIO.md`: não se reaproveitou o motor HTML do Mana & Burn; o Vince é composição de camadas 2D e um renderizador Python dedicado foi mais simples e determinístico.
- Música: `sweat_on_the_walls.mp3`, escolhida e enviada pelo fundador; 140 BPM; trecho 53,24–97,11 s da faixa (beat-map em `beatmap.json`). A bateria pára aos 16,28 s do vídeo, onde entra o telefonema. Não versionada.
- Voz do Vince: ElevenLabs `nDJxgaKfMo1DDJJqNg0f`, `eleven_v3`, uma geração (37,6 s, 578 créditos). Flow `1OZhISAeTjWGjnkig55F`, geração `I1pCHshxN0tr5PkoKjHb`. Cortada em 19 frases por deteção de silêncio e reposicionada na batida. Não versionada (`voz.mp3` recupera-se do flow).
- Fonte e telefone: `vince/audio/fonte.py` (custo zero). A Fonte não fala palavras nem tem legenda.
- Movimento (bíblia §7B): respiração, entrada a 3 % com assentamento de 120 ms, deriva de câmara, contador do painel uma vez, boca sincronizada ao envelope da voz nos grandes planos, piscar.
- Cenário sem telefone (`assets/cenario_sem_telefone.png`): o telefone da mesa retirado do `cenario_916.png` para os planos em que ele está na mão do Vince.

## Controlo de qualidade (ficheiro final)
`python3 -I comum/qc/qc_video.py … --frente lambe` (o QC ainda não tem perfil `vince`; o formato é o mesmo 9:16): 1080×1920 · 30 fps · 43,87 s (40,0 s + fecho) · −14,0 LUFS · pico −1,6 dBTP · fecho presente aos 40,0 s · **sem problemas mensuráveis**. `cropdetect`: 1080:1920:0:0 em todos os quadros (sem corte lateral). Folha de contacto conferida a olho: legenda, placas e carta dentro da zona segura; nenhuma tipografia por cima da carta; um só plano com flash vermelho (1 VENDA). Detalhe em `qc.json`.

A conferir pelo fundador: pronúncia da voz (sem transcrição automática disponível neste ambiente) e a verificação P1 acima.

## Ficheiros finais (fora do Git)
- `MultiverseCapital_Ep01_PregaoDeVespera_916.mp4` e `capa.png`: entregues ao fundador na conversa de 12/11/2026 (claude.ai, projeto Binder Marketing). A capa também está nesta pasta.
- Recriar: `python3 render.py --kit <vince/kit/v1> --assets assets --saida mudo.mp4` e `python3 mistura.py final --assets <pasta com voz.mp3> --fonte vince/audio/saida --musica sweat_on_the_walls.mp3 --video mudo.mp4 --fecho comum/outro/outro_binder_916.mp4 --saida final.mp4` (antes: `mistura.py voz` para gerar `env_voz.npy`).

## Entregáveis
- [x] Vídeo · [x] Capa · [x] Legenda (`legenda.txt`) · [x] Comentário fixado (`comentario_fixado.txt`) · [x] Texto alternativo (`texto_alternativo.txt`) · [x] Fontes (esta ficha)

## Depois de publicar
- Métrica principal: guardados por 1.000 views; secundária: retenção aos 3 s.
- Resultado observado: —
- Aprendizagem: —
