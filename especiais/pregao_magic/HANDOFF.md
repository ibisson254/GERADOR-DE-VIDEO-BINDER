```
HANDOFF · 13/11/2026 · Claude
Repositório: ibisson254/GERADOR-DE-VIDEO-BINDER · branch especial/pregao-magic · último commit (ver git log; conferido no remoto no fim da sessão)

Objetivo atual: fechar o ESP-2026-02 «PREGÃO MAGIC — a bolsa abriu» com narração e levá-lo para a main.

Conteúdos tocados (comum/REGISTRO_EDITORIAL.md):
- ESP-2026-02 · (novo) → EM PRODUÇÃO

Encerramento:
- ESP-2026-02 · memoria.py encerramento: 1 falta (estado EM PRODUÇÃO) — por isso fica nesta branch e não na main (AGENTS.md §3)
- Vídeo PREGAO_MAGIC_v4_semvoz.mp4 (46,87 s) e capa_pregao_magic.png: entregues ao fundador na conversa de 13/11 (não versionados)

Decisões tomadas nesta sessão:
- Sem personagem e sem identidade do Vince (pedido do fundador); especial entre séries, não frente nova (nucleo/DECISOES.md: não, não mudou regra)
- Khan/Sheoldred (Stardates) excluído por ter o retrato de um ator real (fontes.md)
- Reais por conversão (R$ 5,59, 10/11) porque LigaMagic/MTGStocks estavam bloqueados neste ambiente; dito no ecrã

Documentos consultados:
- AGENTS.md, STATUS.md, vince/PERFIL.md, nucleo/DECISOES.md, nucleo/SHOWRUNNER.md §6, nucleo/modelos/FICHA_EPISODIO.md, comum/qc/LEIA-ME.md

Alterações realizadas:
- especiais/pregao_magic/ · pacote completo + motor (render.py, audio.py, capa.py, mux.sh, cartas.sh, dados.json)
- comum/REGISTRO_EDITORIAL.md · linha ESP-2026-02
- comum/historico.md · linha de 13/11
- STATUS.md · secção «Em produção» e ponteiro de handoff

Tarefas pendentes:
- Narração: autorizar ElevenLabs (~1.400 créditos, 2 tomadas, voz nova de corretor) · depende do fundador
  → depois: python3 audio.py musica.mp3 trilha.wav --voz voz.wav; mux.sh; QC; estado CONCLUÍDO; encerramento; merge na main
- Ou: fundador decide publicar a v4 sem voz → estado CONCLUÍDO, encerramento, merge
- (Opcional) conferir as 4 cotações na LigaMagic e trocar a linha de reais em dados.json
- Publicar até sábado 14/11 (os preços de Star Trek mudam depressa)

Próximo passo concreto: resposta do fundador sobre a voz; se sim, gerar com o texto de especiais/pregao_magic/roteiro.md («Narração final»).
```
