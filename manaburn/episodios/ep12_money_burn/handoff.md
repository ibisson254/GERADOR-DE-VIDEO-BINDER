HANDOFF · 19/11/2026, ~21h (Lisboa) · Claude
Repositório: ibisson254/GERADOR-DE-VIDEO-BINDER · branch manaburn/ep12-money-burn · último commit: ver `git log -1` da branch (conferido no remoto antes do fecho da sessão)

Objetivo atual: produzir o MB-EP12 «MONEY BURN» (Mana & Burn) até ao vídeo final com voz.

Conteúdos tocados (comum/REGISTRO_EDITORIAL.md):
- MB-EP12 · (novo) → EM PRODUÇÃO

Encerramento:
- MB-EP12 · memoria.py encerramento: falta 1 — estado EM PRODUÇÃO (falta a voz e o vídeo final). validar: OK. validar_repo: 0 graves (1 P2 antigo: vince/kit/v1/).
- Prévia sem voz `MB_EP12_MoneyBurn_PREVIA_semvoz_916.mp4` (44,40 s) e capa entregues na conversa de 19/11; vídeo não versionado.

Decisões tomadas nesta sessão (dentro das regras, sem mudar identidade):
- ID MB-EP12 (o 11 é o Numot; há um rascunho «EP11» na branch niv-rodizio).
- Kit: opção `EP.fx.tv_ligada` (desligada por defeito) para o quadro 0 mostrar a carta; documentada em manaburn/LEIA-ME.md. Não registada em DECISOES.md (técnica, opcional) — o fundador pode vetar; sem ela, cortar 7 quadros no juntar_fecho como no Giro.
- Capa: Unfinished Business «Só falta uma carta · sempre» (2 alternativas testadas e descartadas, razões na ficha).
- Sem selo vermelho (nenhum dado real de mercado; o episódio não usa preços).

Documentos consultados: AGENTS.md, STATUS.md, constituição, catálogo, SHOWRUNNER, manaburn/PERFIL.md, skill binder-mana-burn-episodio, manaburn/LEIA-ME.md, REGISTRO_EDITORIAL, easter_eggs, DECISOES (15/11, 12/11, 08/11), CHECKLIST_QUALIDADE, ficha do Numot (branch manaburn/ep10-numot), vince/PERFIL.md.

Alterações realizadas:
- manaburn/episodios/ep12_money_burn/ · pasta nova (ficha, fontes, qc, legenda, comentário, alt, episode.json/js, faixas, scripts, capa, cartas)
- manaburn/index.html · opção EP.fx.tv_ligada
- manaburn/LEIA-ME.md · TV acesa no quadro 0; prévia sem voz
- comum/REGISTRO_EDITORIAL.md · linha MB-EP12 · comum/historico.md · comum/easter_eggs.md («10:20») · STATUS.md

Tarefas pendentes:
- Autorizar ≈1.000 créditos ElevenLabs (Talis 481 + Erik 497 caracteres, eleven_v4, 1 tomada cada; texto em faixas_elevenlabs.txt) · fundador
- Gerar vozes → process.py burn.mp3 mana.mp3 → render.py → juntar_fecho.py → qc_video.py + bordas.py → encerramento → merge na main · agente
- Capturas reais do scanner/Binder para o carrossel do par de publicação · fundador
- Escutar pronúncias (Unfinished Business, Price of Progress, Greed) · fundador

Próximo passo concreto: com a autorização, colar as duas faixas de manaburn/episodios/ep12_money_burn/faixas_elevenlabs.txt no ElevenLabs e correr `python3 process.py burn.mp3 mana.mp3` na pasta do kit com o episode.json/js do EP12.
