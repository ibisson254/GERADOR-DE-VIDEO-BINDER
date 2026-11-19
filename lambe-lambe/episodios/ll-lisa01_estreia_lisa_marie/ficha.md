# Ficha · Lambe-lambe · LL-LISA01 · Teaser de estreia da Lisa Marie no Ar

## Identificação
- ID editorial: LL-LISA01
- Estado no registo: CONCLUÍDO (não publicado; a publicação é do fundador)
- **Versão a publicar: v2** (19/11/2026, 19:29, pedido do fundador: «coloque todas as 10 imagens… refine essa ideia»). A v1 (4 looks, motor do Story) fica como histórico.
- Origem: pedido do fundador, 19/11/2026 (19:22): «Faz trailer de estreia da Lisa no formato lambe-lambe», resposta à decisão (a) de `nucleo/DECISOES.md` (19/11, 19:11)

## Classificação
- Frente: **Lambe-lambe** (publicação espontânea de divulgação). Não é episódio da série Lisa Marie no Ar e não usa a identidade de estúdio da série; usa a identidade do Lambe-lambe, como pedido.
- Formato: Reel/Story 9:16, 1080×1920, 30 fps, 9 s + fecho do scanner (12,87 s), sem áudio (música escolhida no Instagram, regra do kit do Story)
- Estratégia: `lambe-lambe/kit_story/motor_story.py` (não alterado) + capa com o motor-padrão do carrossel (`capa.py`); zero créditos

## Originalidade
- `memoria.py pauta --objeto "Lisa Marie" --tema "estreia nova personagem Lisa Marie no Ar teaser"`: LIVRE (19/11/2026)

## Editorial
- Tese: há uma personagem nova no BINDER Originals, a VJ cultural ligada à cultura pop, e o quadro de estreia é Elas no Multiverso
- Objetivo: anunciar a série e recolher sugestões de convidadas para o primeiro ciclo (comentário fixado)
- Métrica principal: comentários com sugestões de convidadas e partilhas por alcance; seguidores ganhos

## v2 · os 10 looks (19/11/2026, 19:29)
- Script próprio do episódio: `teaser_v2.py` (peças do motor-padrão e o muro do kit do Story; o motor do Story não foi alterado).
- 0–2,4 s: o cartaz de estreia já está a entrar no quadro 0, fitas, etiqueta «CONHEÇA OS 10 LOOKS».
- 2,4–12,4 s: os 10 looks colados um por segundo, empilhados como cartazes, cada um com etiqueta kraft «NN NOME» + tema pop (a etiqueta anterior sai quando chega a seguinte).
- 12,6–16 s: corte seco com clarão de papel; parede completa em grelha 5×2, título «10 JEITOS DE ESTAR NO AR», faixa «LISA MARIE NO AR · Estreia em breve · BINDER Originals» com créditos.
- 16–19,87 s: fecho do scanner.
- Looks 04 e 06 (símbolo de planeswalker e verso da carta) entram por pedido explícito do fundador; crédito «Símbolo e verso de carta de Magic © Wizards of the Coast» na faixa final.
- Recortes ampliados 2× (Lanczos) com nitidez leve.
- Mudança visual a cada ≤ 1 s na fase dos looks; quadro 0 já com o cartaz.

## Gancho visual (SHOWRUNNER §4.1) · v1
1. Quadro 0: muro rosa vazio com a sombra do cartaz a chegar (padrão do kit do Story; limitação: não há carta de Magic no quadro 0)
2. Objeto: cartaz «Lisa Marie» com a ilustração da personagem
3. Ação: o cartaz cai e bate no muro (1,15–1,77 s)
4. Som: nenhum no ficheiro (música no Instagram)
5. Descoberta até 3 s: «Estreia no BINDER Originals: Lisa Marie no Ar»
6. Promessa: conhecer a personagem nova
7. Pagamento: 7,2–9,0 s, faixa «LISA MARIE NO AR · Nova série · BINDER»

## Imagens e direitos
- Só imagens da prancha de 19/11 enviada pelo fundador (`lisa-marie/referencias/inspiracoes_2026-11-19/`): looks 01 (capa), 03, 02 e 08. Recortadas sem a faixa rosa do topo e sem a etiqueta numerada.
- Evitados os looks 04 e 06 (símbolo de planeswalker e verso da carta, marcas da Wizards) e as coroas.
- Rótulo «imagem conceitual» na capa e nos créditos: a personagem-mestre ainda não existe (`lisa-marie/KIT_PRODUCAO.md`).
- O selo azul do motor («Artistas de Magic») não foi usado; no lugar, etiqueta «NOVA SÉRIE».
- Nada sobre voz, data de estreia ou funções novas do app.

## Produção
v2: `python3 -I capa.py <saida>` e depois `python3 -I teaser_v2.py <saida>` (~2,5 min). v1:
1. `python3 -I lambe-lambe/episodios/ll-lisa01_estreia_lisa_marie/capa.py <saida>` (gera `01_capa.png` e os recortes limpos dos looks)
2. Ajustar os caminhos de `story/story.json` à `<saida>`
3. `python3 -I lambe-lambe/kit_story/motor_story.py story/story.json <saida>/LL-LISA01_teaser.mp4` (~40 s)
Fontes do kit: `sh lambe-lambe/kit_carrossel/preparar_fontes.sh`.

## Controlo de qualidade (19/11/2026)
- **v2:** `qc_video.py --frente lambe`: 1080×1920, 30 fps, 19,87 s (16,0 s + fecho), fecho presente a partir de 16,0 s; único aviso «sem faixa de áudio» (esperado). Frames-chave conferidos: etiquetas legíveis, grelha final afastada das bordas (centros 136–944 px), faixa na zona segura.
- **v1:**
- `comum/qc/qc_video.py --frente lambe`: 1080×1920, 30 fps, 12,87 s (9,0 s + fecho), fecho presente a partir de 9,0 s; único aviso «sem faixa de áudio» (esperado no kit do Story).
- Folha de contacto conferida: cartaz e textos legíveis, sem corte lateral, faixa final na zona segura.
- Limitações: quadro 0 sem objeto de Magic (padrão do motor do Story); os recortes da prancha têm resolução baixa (~262 px de largura) e ficam um pouco suaves quando ampliados; o detalhe central (livros ANIME/K-POP/MAGIC do look 08) fica em parte tapado pela faixa final.

## Ficheiros finais
- `LL-LISA01_teaser_v2.mp4` (19,87 s, versão a publicar), `LL-LISA01_teaser.mp4` (v1, 12,87 s) e `01_capa.png` (1080×1350): entregues na conversa a 19/11/2026, não versionados; recriam-se com os comandos de «Produção».

## Entrega
- Legenda, comentário fixado e texto alternativo nesta pasta.
- Publicar como Reel (e opcionalmente repostar no Story). Música: escolher no Instagram, sem jingles ou faixas que imitem a MTV.
