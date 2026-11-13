# Ficha · Especial · ESP-2026-02 · PREGÃO MAGIC — A bolsa abriu (13/11/2026)

## Identificação
- ID editorial: `ESP-2026-02`
- Estado no registo: **EM PRODUÇÃO** — vídeo v4 renderizado e conferido **sem narração**; falta a voz (ElevenLabs, à espera de autorização do fundador) ou a decisão de publicar a versão só com música.
- Aprovação do fundador: pedido explícito «PROMPT DE ENGENHARIA AVANÇADA — PREGÃO MAGIC» + música `sweat_on_the_walls.mp3` (chat de 13/11/2026, 18:13–18:15).

## Classificação
- Frente: especial entre séries, território de mercado (o mesmo do Vince Vault), **sem personagem e sem a identidade do Vince** (pedido do fundador). Se virar formato recorrente, o fundador decide a frente no catálogo.
- Classe de conteúdo: mercado
- Complexidade: alta
- Estratégia: retenção por revelação (gancho com o maior número, ciclo aberto «outra triplicou» pago no bloco B, inversão de atmosfera no bloco C, recapitulação «guarde este pregão» no fim).

## Originalidade
- Objetos: Uthros Research Craft; Moonshadow; Watery Grave LCARS; Steam Vents LCARS; shocklands; Mundial 32.
- `memoria.py pauta` (13/11, tema «pregão: altas e quedas de preço da semana»): **LIVRE** para os cinco objetos.
- Relações: VV-EP00 (mesmo território, piloto pausado); MB-ESP03 (Star Trek, ângulo de humor, não de preço); MC-EP07 (Mundial 32, ângulo competitivo).

## Editorial (briefing)
- Objetivo: mostrar ao jogador brasileiro, em 45 s, quais cartas subiram e caíram nesta semana e porquê, e ligar isso ao valor da pasta dele (scanner do BINDER Vision).
- Proposta de valor: «Quem sobe, quem cai — e por quê.»
- Público: jogador adulto de Commander/Modern com cartas guardadas.
- Hipótese a testar: um formato de mercado sem personagem, só cartas + números + música, gera mais guardados por 1.000 views do que os episódios com personagem.
- Gancho (0–3 s): quatro cartas reais explodem; Watery Grave LCARS **−74,7% em 7 dias**; whip pan para Uthros **mais de 3× em um mês**.

## Roteiro definitivo
Ver `roteiro.md` (narração cronometrada por janela, storyboard com timecodes e os 9 match cuts).

## Fontes e evidências
Ver `fontes.md` (ficha de verificação por carta: versão, antes, depois, período, fonte, causa; limitações; descartados).

## Produção
- Recursos: música fornecida pelo fundador (editada na grelha de 184,6 BPM); imagens das cartas do Scryfall; fontes Geist (OFL, npm); fecho oficial `comum/outro/outro_binder_916.mp4`.
- Motor: `render.py` (quadros), `audio.py` (edição musical + efeitos sintetizados), `capa.py`, `mux.sh`, `cartas.sh`, `dados.json` — ver `LEIA-ME.md`.
- Vozes e créditos gastos: **zero**. Nenhum serviço pago usado.
- Easter egg: nenhum.
- Riscos: preços mudam depressa (Star Trek saiu hoje); publicar até sábado 14/11 ou rever os números.
- Limitações conhecidas:
  1. **Sem narração**: a voz do ElevenLabs precisa de autorização (~1.400 créditos, 2 tomadas, voz nova de corretor — não pode ser voz de outra série). A alternativa gratuita disponível (Piper, voz pt-BR «edresson low», 16 kHz) perde as nasais («pregão», «alta») e não tem qualidade de publicação. O vídeo foi desenhado para funcionar sem som; as janelas da narração já estão marcadas e `audio.py --voz` faz o ducking.
  2. **Sem cotação da LigaMagic**: domínio bloqueado neste ambiente; reais = conversão a R$ 5,59 (10/11), dito no ecrã.
  3. Khan/Sheoldred (Stardates) ficou de fora por ter o retrato de um ator real.

## Controlo de qualidade
Medido no ficheiro final `PREGAO_MAGIC_v4_semvoz.mp4` com `comum/qc/qc_video.py --frente lambe` (13/11/2026).

| Critério | Alvo | Medido | OK |
|---|---|---|---|
| Resolução / fps | 1080×1920 / 30 | 1080×1920 / 30,0 | sim |
| Duração | 30–45 s (+ fecho) | 43,0 s + fecho 3,87 s = 46,87 s | sim |
| Corte lateral (cropdetect) | nenhum | crop=1080:1920:0:0 em todos os quadros | sim |
| Loudness / pico | −14 LUFS / < −1 dBTP | −14,1 LUFS / −2,0 dBTP | sim |
| Fecho do scanner | presente | a partir de 43,0 s (dif. 0,04) | sim |
| Factos = ficha | sim | conferido número a número com `fontes.md` e `dados.json` | sim |
| Codec | H.264 + AAC | H.264 yuv420p + AAC 256 kb/s 48 kHz, faststart | sim |

**Retenção:**
- Quadro 0 com Magic: sim — quatro cartas reais inteiras no ecrã desde o primeiro quadro.
- Mudança visual ≤ 3 s: cortes medidos a 0,03 · 0,33 · 3,93 · 5,23 · 5,87 · 11,07 · 22,13 · 25,37 · 30,57 · 31,87 · 33,17 · 38,37 s, mais revelações animadas (número, contador, causa com «punch» na carta) a cada 1,3–2,6 s. Maior janela sem corte nem revelação forte: 3,8 s (33,2–37,0), com duas entradas de texto e a linha de leitura em movimento — aceite.
- Som em cada revelação: sim — impacto/alerta/ding em cada percentagem, contadores com cliques, crash + passa-baixo na entrada das quedas, pings no radar.
- Conferência a olho (folha de contacto): cartas inteiras e sem texto por cima em todos os planos; números e fontes legíveis e dentro da zona segura; recapitulação final dentro da zona segura.

## Ficheiros finais
Vídeos renderizados não entram no Git.
- Vídeo: `PREGAO_MAGIC_v4_semvoz.mp4` · 46,87 s · entregue ao fundador na conversa de 13/11/2026 (claude.ai, projeto Binder Marketing). Recria-se com `LEIA-ME.md`.
- Capa: `capa_pregao_magic.png` (1080×1920; recorte 3:4 seguro) · entregue na mesma conversa. Recria-se com `python3 capa.py`.

## Pacote de publicação
- [x] `legenda.txt`
- [x] `comentario_fixado.txt`
- [x] `texto_alternativo.txt`
- [x] `fontes.md`

## Encerramento
- [x] Briefing e roteiro definitivo
- [x] Legenda, comentário fixado e texto alternativo
- [x] Fontes e evidências
- [x] Controlo de qualidade preenchido
- [x] Localização do vídeo e da capa
- [x] `comum/REGISTRO_EDITORIAL.md` (EM PRODUÇÃO)
- [x] `comum/historico.md`
- [ ] Narração (ou decisão de publicar sem voz) → depois disso, estado CONCLUÍDO e merge na `main`
