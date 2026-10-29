# Ficha · Mana & Burn · EP09 · O ladrão que virou Papai Noel (Dack Fayden, Helping Hand)

## Classificação
- Série: Mana & Burn · Plantão do Banimento
- Classe de conteúdo: tendência / reação da comunidade + carta polémica
- Complexidade: média
- Estratégia (constituição §3): investigação aprofundada (2 fontes independentes, data da semana) + Oracle para a regra

## Editorial
- Objetivo: respostas A/B no comentário fixado; levar o jogador de Commander a conhecer o BINDER Vision pelo fecho do scanner.
- Proposta de valor: o maior ladrão do Magic agora dá presentes, e o presente é uma arma.
- Público: jogador casual e de Commander no Brasil.
- Hipótese a testar: a pergunta A/B com o bordão ("A, bane. B, aceita o presente.") gera mais respostas por 1.000 views do que a pergunta aberta do Ep. 5. Secundária: partilhas ≥ 0,6% das views.
- Gancho (0–3 s): "Plantão do Banimento, mano! O maior ladrão do Magic virou Papai Noel!" com a carta na TV.
- Território: acontecimento e cultura. Sem lista de cEDH, sem peças nem passo a passo do combo, sem nomes de jogadores.

## Fontes e evidências
Ver `ficha_fontes.md` (afirmação · tipo · fonte · data). Resumo:
- Oracle e PNG: API Scryfall frc/4 (29/10). Texto confere com o esperado no brief, palavra a palavra.
- Regra da fala 8: CR 603.3a + EDHREC (13/10). Sustenta "o gatilho de entrada continua teu": as criaturas entram sob o seu controlo e os gatilhos vão para a pilha já com elas do outro lado; quem escolhe os alvos é você. O Draftsim (05/10) diz o mesmo de forma menos explícita.
- Goad: CR 701.15b (versão de 16/01/2026, via mtg.wiki).
- "Já ganhou torneio de cEDH": EDHTop16, 1.º lugar a 03/10 (119 jogadores) e 04/10 (69). Conversão 50% (1 ano, 50+ jogadores) a 29/10. Sem mudança desde o brief.
- Bronzebeak Foragers US$ 0,77 → 3,29 (+327%), quase 1.000 decks: MTG Rocks 28/10. Sem mudança.
- Pedidos de banimento: MTG Rocks 22/10 (na altura citava 56,25% de conversão). Nenhum anúncio oficial.
- Salt Score do Dack: o EDHREC não mostra (29/10) → Conversômetro em vez de Putômetro.

## Produção
- Kit: **v2** (código do projeto claude.ai Binder Marketing, `claude/gerador-manaburn/`: index.html, process.py, cortes.py, trilha.py, sfx.py, roteiro.py, foneticos.json, render.py, preview.py, bordas.py) + assets do repositório (sala/dupla no index.html, tv_asset.png, musica.mp3 midnight_throttle, logo, fontes, comum/outro/scan). O repositório tem o v1 (sem travão de bordas `encaixa`, sem pôster, sem respiro/ritmo); por isso o v2.
- Alterações ao kit (só parâmetros + uma opção nova, documentada):
  - `process.py`: opção `"respiro_fala": {"8": 0.45}` no episode.json (uma fala com respiro interno maior que o `respiro_max` 0,14). Usada para a pausa antes de "continua *teu*".
  - Faixa do Mana: +0,18 s de silêncio de sala (copiado do próprio silêncio da faixa) antes de "continua teu" → pausa medida no vídeo ≈ 0,42 s.
  - `juntar_fecho.py`: corta o vídeo do kit em T_SLAM + 0,52 s (ponto já verde, antes de a logo do kit crescer) e cola o fecho do scanner. Também tira os 7 primeiros quadros (animação de ligar a TV, achatada sobre preto).
  - `fecho_scanner.py`: reconstrói o fecho de marca como no `oraculo/episodios/ep02_render.py` (45 quadros reais de `comum/outro/scan/` + logótipo, 3,87 s).
- Vozes: ElevenLabs eleven_v4, flow "Mana & Burn — Ep. 9 (Dack Fayden)" (8E5P0vbsPq5NqBakX3xy). Burn: Talis (E9a8LlXPNWtyvvSoZzrb), Mana: Erik (nfiLpQ54jEQninp3nNqL). 1 geração por voz (555 + 467 créditos). Ritmo Burn ×1,06, Mana ×1,12, respiro 0,14 s. Grafias: Déqui Fêiden, Gôud, cê é dê agá, raipou, Jêice, "Á, bâne. Bê, aceita". Precon ficou "precon" (não foi preciso "pricón"). A transcrição Scribe devolveu exatamente o texto pedido (não substitui ouvir).
- Cortes do process.py: 14 falas, todas batem com os tempos das palavras da transcrição.
- Planos (nomes reais do kit): 1 tv · 2 cuM · 3 wide · 4 tvtext · 5 tvtext2 · 6 cuM · 7 push · 8 push · 9 cuB · 10 wide · 11 tv2 (+ insert Bronzebeak) · 12 cuM · 13 cuB (point_cam) · 14 cuM (remote; TV desliga).
- Poses: o kit não tem "tvpoint" como pose de braço; usei `point_tv` (nome real). Burn point_tv 1/3/5, arms_up 7/11, shrug 9, point_cam 13. Mana finger 4/8, chip 10, remote 14.
- Destaques (medidos nas linhas de pixels escuros do PNG 744×1040): tvtext = "reveal cards / from the top… until you reveal / X creature cards," + "Each opponent gains control of the permanent / for which they were chosen."; tvtext2 = "They're / goaded for the rest of the game." Zoom 1,5 (tela inteira da TV).
- Pôster da parede: `mago` (Dack é Human Advisor).
- TV SAL: relógio 02:10; Conversômetro 50% com "top cut no cEDH · EDHTop16 · 29/10/2026"; placar "PRESENTES ENTREGUES 3 DE 3 · um por adversário (mesa de 4)"; 8 manchetes (a 4 ficou "sobe uns 600%": a Wargamer dá US$ 1,30 → 9–10 = +592% a +669%).
- Insert fala 11: Bronzebeak Foragers, PNG real (lcc 69, Brian Valeza, 2023), crédito no topo.
- Easter egg: relógio 02:10 = 02/10, lançamento do precon (registado em `comum/easter_eggs.md`).
- Riscos: fecho reconstruído (falta o MP4 oficial); licença das vozes depende do plano ativo no momento da geração (não verificável por esta ligação).

## QC medido no ficheiro final (`ManaBurn_Ep9_DackFayden_916.mp4`, 29/10/2026)
| Critério | Alvo | Medido | OK |
|---|---|---|---|
| Resolução / fps | 1080×1920, 30 | 1080×1920, 30/1 (1442 quadros) | sim |
| Codecs | H.264 + AAC 48 kHz | h264 + aac 48000 Hz | sim |
| Duração antes do fecho | 36–45 s | 44,20 s | sim |
| Duração total | — | 48,10 s (fecho 3,87 s, sem encurtar) | sim |
| Loudness integrado | −14 ±0,5 LUFS | −14,0 LUFS | sim |
| True peak | < −1 dBFS | −1,2 dBFS | sim |
| cropdetect (24:2:0, como no brief) | 1080:1920:0:0 em todos | 1440/1440 quadros reportados = crop=1080:1920:0:0 | sim |
| cropdetect por quadro (24:2:1, mais exigente) | — | quadros 0–1310 (0–43,67 s, todo o episódio) = 1080:1920. Os 130 seguintes (TV a desligar, ponto verde, fecho do scanner com fundo escuro e fade final) dão caixas menores porque o fundo é preto de propósito; não há imagem cortada | sim (por desenho) |
| Bordas dos planos da TV | laterais 0–1080, topo ≥ 295 | bordas.py: 462 quadros de TV, laterais 10–1068 px, topo ≥ 300 px | sim |
| Carta inteira, rodapé visível, nada por cima | — | conferido em 14 quadros extraídos do ficheiro final (0,0; 0,04; 2,5; 13,4; 16,4; 23,6; 33,6; 39,0; 42,6; 43,75; 44,12; 44,6; 46,4; 47,95 s) | sim |
| Destaques alinhados | — | 13,4 s e 16,4 s: retângulos sobre as linhas certas | sim |
| Insert Bronzebeak | PNG real + crédito | 33,6 s: carta inteira, crédito "Na tela:" no topo | sim |
| Medidor com conta e fonte | todas as tomadas da TV | visível em 2,5 / 13,4 / 16,4 / 33,6 s | sim |
| Legenda queimada | zona segura, amarelos certos | bottom 440 px; amarelos conferidos nos quadros | sim |
| Bordões | intactos | "Lê a carta", "Isso devia ser banido", "Comenta aí" | sim |
| Pausa antes de "continua teu" | 0,4 s | ≈ 0,42 s (envelope da fala 8) | sim |
| "Comenta aí" na parada seca; pancada desliga a TV | — | Comenta aí 42,43 s; pancada 43,68 s (tempos do vídeo final) | sim |
| Fecho | TV desliga → ponto verde → fecho do scanner, logo uma só vez | conferido em 43,75 / 44,12 / 44,6 / 46,4 s | sim (reconstruído) |

## Entregáveis
- [x] Vídeo · [x] Capa (2,5 s, fala 1) · [x] Legenda (597 caracteres) · [x] Comentário fixado (≤ 1.000) · [x] Fontes

## Divergências registadas
- Brief vs repositório: o brief chama "tvpoint" a uma pose; no kit a pose de braço é `point_tv` (tvpoint só existe como etiqueta nos episode.js antigos, sem efeito).
- Brief: "TV desliga → ponto verde → logo → outro_binder_916.mp4". A lacuna do PERFIL confirmou-se: o kit tem logo própria e o fecho do scanner também. Mantido o do scanner, encurtado o do kit (corte antes de a logo do kit aparecer).
- Legenda do brief tinha 748 caracteres (limite 300–600): encurtada para 597, sem mudar factos; a frase "as cartas que ele dá subiram de preço" saiu da legenda (o preço fica no vídeo e no comentário, atribuído à MTG Rocks).
- Comentário do brief, com o Oracle completo, passava de 1.000 caracteres: passos encurtados, Oracle completo mantido.
- O comentário fixado do Ep. 08 citava preço do Scryfall (contra o PERFIL); não foi alterado (regra: não mexer no Ep. 08).

## Depois de publicar
- Métrica principal: respostas A/B por 1.000 views. Secundária: partilhas ≥ 0,6% das views.
- Resultado observado: —
- Aprendizagem: —
