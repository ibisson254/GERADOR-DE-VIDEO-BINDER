HANDOFF · 20/11/2026, ~02h (Lisboa) · Claude
Repositório: ibisson254/GERADOR-DE-VIDEO-BINDER · main (merge da branch manaburn/ep13-everything) · hash conferido no remoto (ver histórico do Git e a resposta da sessão)

Objetivo atual: MB-EP13 «EVERYTHING, MENOS TUDO» concluído; resta a publicação pelo fundador, antes da venda (30/11, 14h de Brasília).

Conteúdos tocados (comum/REGISTRO_EDITORIAL.md):
- MB-EP13 · (novo) → EM PRODUÇÃO (pauta registada antes da produção) → CONCLUÍDO

Encerramento:
- MB-EP13 · memoria.py encerramento: OK. validar: OK. validar_repo: 0 graves (1 P2 antigo: vince/kit/v1/). ciclo.py validar, test_memoria, test_ciclo: OK.
- Vídeo final `MB_EP13_Everything_916.mp4` (46,70 s) e capa `MB_EP13_CAPA.png` entregues na conversa de 20/11; vídeo não versionado. Vozes: flow ElevenLabs 73clfpsdXBcSv56XayXW (1.036 créditos, saldo pré-pago, autorizado na missão).

Decisões tomadas nesta sessão (dentro das regras, sem mudar identidade):
- ID MB-EP13 (nenhuma branch, ficha ou linha do registo usava EP13).
- Roteiro do briefing revisto com as fontes: «Lê o anúncio» como leitura do Mana (classe notícia), falsa expectativa do brinde, desconto US$ 4,97 e total US$ 234,98 (contas com preços oficiais), hora de Brasília.
- Kit: opção `EP.canais[].meio` (desligada por defeito) e pré-carregamento dessas imagens, para falas longas manterem mudança visual ≤ 3 s. Documentada em manaburn/LEIA-ME.md; não registada em DECISOES.md (técnica, opcional) — o fundador pode vetar.
- `processar_vozes.py` (episódio): corte das faixas pelo texto falado; o process.py do kit não foi alterado.
- Imagem oficial do bundle não usada (domínio bloqueado no proxy); cartas reais do Scryfall em todas as telas.
- Capa: Shai-Hulud «O PACOTE DE TUDO · QUASE», selo «2 DE 3 DROPS».

Documentos consultados: AGENTS.md, STATUS.md, nucleo/SHOWRUNNER.md (§4.1, §4.2, §6), nucleo/CHECKLIST_QUALIDADE.md, nucleo/DECISOES.md (13/11, 15/11), nucleo/modelos/FICHA_EPISODIO.md e HANDOFF.md, manaburn/PERFIL.md, manaburn/LEIA-ME.md, skill binder-mana-burn-episodio, comum/REGISTRO_EDITORIAL.md, comum/easter_eggs.md, pacote do MB-EP12. Não lidos nesta sessão: constituição e catálogo na íntegra, bíblia do Drive (identidade seguida pelo kit e pela skill).

Alterações realizadas:
- manaburn/episodios/ep13_everything/ · pasta nova (ficha, fontes, qc, legenda, comentário, alt, episode.json/js, data.js, faixas, telas_everything.py, processar_vozes.py, previa_sem_voz.py, juntar_fecho.py, capa, cartas e telas)
- manaburn/index.html · opção EP.canais[].meio + pré-carregamento
- manaburn/LEIA-ME.md · troca de tela a meio da fala; nota sobre frações do hl; corte pelo tts
- comum/REGISTRO_EDITORIAL.md · linha MB-EP13 · comum/historico.md · comum/easter_eggs.md («14:00») · STATUS.md

Tarefas pendentes:
- Ouvir as pronúncias (Everything, Halo Foil, Balance of Power, Deserts of Arrakis, preços por extenso) e publicar antes de 30/11 · fundador
- Capturas reais do scanner/Binder para o carrossel do par de publicação · fundador
- Domingo: medir respostas A/B por 1.000 views contra o MB-EP12 (sem impulso pago antes de medir) · agente

Próximo passo concreto: fundador publica o MB-EP13 com a legenda e o comentário de manaburn/episodios/ep13_everything/ e confirma a data, para passar a PUBLICADO no registo.
