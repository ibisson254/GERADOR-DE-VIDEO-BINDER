# Ficha · Vince Vault (formato Pregão) · VV-PG01 · Pregão Magic · Brutal Bass Edition

## Identificação
- ID editorial: `VV-PG01`
- Estado no registo: **EM PRODUÇÃO** — v1 renderizada e conferida sem voz; falta a narração (créditos ElevenLabs por autorizar) e o ok do fundador.
- Aprovação do fundador: missão «MISSÃO MASTER — PREGÃO MAGIC · BRUTAL BASS EDITION» (14/11/2026, 00:02), com desvio autorizado: sem personagem (`nucleo/DECISOES.md`, 14/11).

## Classificação
- Frente: Vince Vault · formato alternativo **Pregão sem personagem**
- Classe de conteúdo: mercado
- Complexidade: alta (produção nova do zero, motor novo)
- Estratégia: análise de dados com fonte e data no ecrã; montagem comandada pela música (`MUSIC_MAP.md`)

## Originalidade
- Objetos: Urza, Chief Artificer; Uchuulon; Captain Jean-Luc Picard; Overgrown Tomb; Watery Grave (+ shocklands do Star Trek).
- `memoria.py pauta`: Urza → BLOQUEADA por tema (MB-GIRO02, VV-EP00: "boletim semanal"); Uchuulon → LIVRE; Picard → BLOQUEADA por objeto (MB-ESP01/02, ORB-13/16/20/21); Overgrown Tomb/Star Trek → BLOQUEADA por tema (MB-EP01, MB-ESP03, MC-EP05, LL-PRETRK).
- Libertada pela missão do fundador (`nucleo/DECISOES.md`, 14/11/2026): o ângulo é preço (território exclusivo desta frente); VV-EP00 está pausado; nas outras frentes o Picard/Star Trek foi humor, arte ou meta, nunca cotação.
- Referência negativa da missão (`1000153486.mp4`): **não foi enviado nesta sessão**; não se usou nem consultou. Nada da edição anterior foi reaproveitado.

## Editorial (briefing)
- Objetivo: provar um formato de boletim de mercado sem personagem, com retenção de trailer e informação verificável, que leve ao scanner do BINDER Vision.
- Proposta de valor: em 41 s, o que subiu, o que caiu e o que está no radar na semana do Star Trek, com preço, fonte e data em cada plano.
- Público: jogador brasileiro adulto com cartas guardadas (perfil da frente).
- Hipótese: montagem cinematográfica na música (sem apresentador) retém mais aos 3 s e gera mais guardados por 1.000 views do que boletins com personagem.
- Tese: na semana do lançamento do Star Trek, o mercado mexeu nos dois sentidos — e a mesma coleção teve cartas a cair e a subir.
- Gancho (0–3 s): quadro 0 = parede de cartas reais; uma carta atravessa; a moldura vira gráfico; **+104% em 7 dias** no primeiro grande impacto (3,16 s), com "13/11/2026" escrito desde 0,18 s. Funciona sem som.
- Retenção e recompensa (constituição): Magic no quadro 0; mudança visual ≤ 3 s; micro-recompensa sonora em cada revelação; ciclo aberto ("+ ? ? %" antes do drop) pago aos 13,72 s; pergunta no comentário fixado.

## Roteiro definitivo
`roteiro.md` (narração cronometrada, por gravar) · texto do ecrã em `../motor/pregao.js` · tempos em `MUSIC_MAP.md`.

## Fontes e evidências
`fontes.md` (ficha de verificação completa, com URLs, datas e o que ficou de fora).

## Produção
- Trilha: "Auction of Power" (ElevenLabs Music, fundador), sem alteração de composição. **Licença comercial a confirmar pelo fundador** (depende do plano ElevenLabs em que foi gerada).
- Motor: `vince/pregao/motor/` (canvas por código, Playwright, FFmpeg, som sintetizado em Python). Componentes reutilizáveis para os próximos pregões. Nenhuma imagem gerada; só imagens oficiais do Scryfall.
- Edição: `EDICAO.md` (projeto de edição: cenas, transições, regras).
- Sound design: foley de cartas, impactos curtos, whooshes direcionais (só em 4 movimentos), tiques e placas mecânicas, micro-recompensas, um ping no break. Nada de caixa registadora, moedas, alarmes. Efeitos 10–15 dB abaixo da música.
- Vozes e créditos gastos: **0**. Pedido de autorização feito (14/11, 00:18); resposta sem preferência = sem autorização.
- Personagem: nenhum (desvio autorizado). Bíblia do Vince intacta.
- Easter egg: nenhum.
- Riscos: licença da trilha (a confirmar); preços mudam rápido (o vídeo data tudo a 13/11); conversão para reais é aproximação.
- **Limitações reais:**
  1. Sem narração: a missão pede voz como "inteligência"; a v1 depende só do texto do ecrã. Integração pronta (`som.py … voz.wav`).
  2. LigaMagic inacessível (proxy): reais por conversão do dólar BCB, não preço de mercado brasileiro.
  3. Câmbio de 11/11 (último fechamento do BCB com valor encontrado), não de 13/11.
  4. MTGGoldfish lido por extração de página (duas leituras consistentes às 15:46 UTC); valores do MTGGoldfish mudam várias vezes por dia.
  5. Kinocut, FFmpeg Skill e Motion Video Director não instalados: não estavam disponíveis no ambiente e não se executou código remoto sem inspeção; FFmpeg e Playwright locais bastaram.
  6. Vídeo de referência negativa não recebido.
  7. Audição: a mistura foi verificada por medição (loudness, pico, correlação L/R 0,78, compatibilidade mono −0,5 dB, sem clipping, níveis por evento), não por ouvido humano. Ouvir no telemóvel antes de publicar.

## Controlo de qualidade
Relatório completo: `QC.md`. Medido no ficheiro final `PregaoMagic_VV-PG01_v1_916.mp4`.

| Critério | Alvo | Medido | OK |
|---|---|---|---|
| Resolução / fps | 1080×1920, 30 | 1080×1920, 30 | sim |
| Duração | 30–45 s + fecho | 41,2 s + 3,87 s = 45,07 s | sim |
| Corte lateral (cropdetect) | nenhum | 1080:1920:0:0 em todos os quadros | sim |
| Loudness / pico | −14 LUFS / < −1 dBTP | −14,1 LUFS / −1,5 dBTP | sim |
| Fecho do scanner | presente, sem encurtar | a partir de 41,2 s (dif. 0,04) | sim |
| Factos = ficha | sim | conferido número a número com `fontes.md` | sim |
| Retenção | quadro 0 Magic; ≤ 3 s; recompensa nas revelações | sim (ver QC.md) | sim |
| Narração | voz clara | **sem voz** | não (pendente) |

## Ficheiros finais
- Vídeo: `PregaoMagic_VV-PG01_v1_916.mp4` · 45,07 s · entregue ao fundador na conversa de 14/11/2026 (não versionado).
- Capa: `PregaoMagic_VV-PG01_capa.png` (1080×1920) · idem.
- Stems: `stems/musica.wav`, `stems/efeitos.wav`, `stems/voz.wav` (silêncio) e `mix.wav` · idem.

## Pacote de publicação
- [x] `legenda.txt` · [x] `comentario_fixado.txt` · [x] `texto_alternativo.txt` · [x] `fontes.md`

## Encerramento
- [x] Briefing e roteiro · [x] Legenda, comentário, alt · [x] Fontes · [x] QC · [x] Ficheiros finais
- [x] Registo (EM PRODUÇÃO) · [x] Histórico · [x] STATUS
- [ ] `memoria.py encerramento VV-PG01` = OK — **não**: estado EM PRODUÇÃO até haver voz e ok do fundador. Por isso o trabalho fica na branch `vince/pregao-ep01-brutal-bass`, não na `main` (`AGENTS.md` §3).
- [ ] Publicação: só o fundador.
