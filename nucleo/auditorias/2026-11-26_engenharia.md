# Missão de engenharia · auditoria, benchmark e otimização (26/11/2026)

Pedido do fundador (26/11/2026, 13:18): auditar o sistema de produção, medir os motores, implementar as melhorias técnicas seguras e propor o resto. **Nenhuma regra editorial, bíblia, perfil, identidade, voz, música ou asset mestre foi alterado. Zero créditos.**

Ambiente das medições: sessão Linux do Claude, **2 núcleos**, 7 GB RAM, sem GPU (Chromium 158 em rasterização por software), Pillow 12.3, ffmpeg do sistema. Os números valem para esta máquina; num PC com mais núcleos a captura paralela do Mana & Burn deve ganhar mais, o que **não foi medido**.

## A. Diagnóstico (por impacto)

### A1. Motores (medido)

| Motor | Onde vai o tempo (perfil) | Causa |
|---|---|---|
| Mana & Burn (`render.py`) | 97 % na captura do Chromium (~290 ms/quadro; `render(t)` só ~3 ms) | página 1080×1920 rasterizada por software; o processo deixa ~40 % da CPU ociosa (renderizador e compositor alternam) |
| Meta em Curto (`mc_render.py`) | 45 % em `GaussianBlur` sobre camadas do **quadro inteiro** para brilhos pequenos (`glow_box`, `circulo`, flash); ~13 s numa **segunda codificação completa** só para juntar o fecho | um desfoque de 1080×1920 por brilho e por quadro (cenas `creditos`/`barras`: 137–144 ms/quadro); `corpo.mp4` codificado a CRF 18 e recodificado inteiro |

Outras observações: o `mc_render.py` redefine `frame`, `term_base`, `cena_tubo` e `cena_carta` em camadas (v3 → v4 → cenas de 23/11). Funciona e está coberto pelo teste de regressão novo; reestruturar só por estética não compensa (regra da missão). A prévia sem voz já existe nos dois motores (`previa_sem_voz.py` no Mana & Burn, modo `previa` no TUBO), por isso não se criou outra.

### A2. Fluxo editorial (lido nos documentos; não medido em tempo)

| Achado | Evidência | Risco protegido | Leitura |
|---|---|---|---|
| A mesma verificação de originalidade aparece 4 vezes | `SHOWRUNNER.md` §2.3, §2.4 passo 5, §4.2 («Originalidade»), `CHECKLIST_QUALIDADE.md` A | repetição de pauta | é o mesmo risco; basta correr uma vez e citar o resultado na ficha nas outras três |
| Regras do gancho escritas em 4 sítios | constituição §6, `SHOWRUNNER.md` §4.1 e §4.1.1, checklist F | gancho genérico / promessa não paga | duplicação documental (custo de contexto), não de trabalho |
| Escuta em três regiões refeita por episódio | `SHOWRUNNER.md` §2.4 2a | achismo | o levantamento serve várias frentes na mesma semana → candidato ao Radar Semanal (pendência E2) |
| `STATUS.md` com 37 KB e 39 secções, 18 delas episódios já CONCLUÍDOS | leitura obrigatória em toda sessão (`AGENTS.md` §1 e §4) | retoma entre sessões | a maior parte é histórico; ≈ 10 mil tokens por sessão antes de qualquer trabalho |
| Leitura de arranque ≈ 101 KB (AGENTS + STATUS + constituição + catálogo + Showrunner) | medido em bytes | — | ≈ 30 mil tokens antes da frente; o `DECISOES.md` (92 KB) e o registo (69 KB) somam se forem lidos inteiros |

**Capacidade (7 → 14 vídeos/semana).** O render não é o gargalo: mesmo antes, 7 episódios do Mana & Burn eram ~45 min de máquina por semana. Os gargalos são o **contexto do Claude** (leitura de arranque, conversas longas) e as **aprovações** (roteiro, créditos, publicação). As poupanças de render ajudam a iterar prévias; as de contexto pedem decisões documentais do fundador (E1–E3).

## B. Melhorias implementadas

| Melhoria | Ficheiro | Problema resolvido | Resultado medido | Teste |
|---|---|---|---|---|
| Captura em paralelo (1 Chromium por núcleo, até 4; aquecimento do DOM antes de cada bloco); `--workers=1` / `MB_WORKERS=1` = modo antigo | `manaburn/render.py` | CPU ociosa na captura | MB-EP16 prévia (1445 quadros): **371 s → 240 s (−35 %)** | 1437/1445 quadros iguais byte a byte; os 8 restantes diferem em ≤ 150 píxeis (PSNR 62–91 dB), e o render sequencial repetido difere nesses mesmos quadros (variação do Chromium) |
| Desfoque só da zona do brilho (`_desfoque_local`) | `oraculo/motor/mc_render.py` | desfoque do quadro inteiro por brilho | 71 → 35 ms/quadro (MC-PAU08); 70 → 32 (MC-PAU02) | `mc_render_regressao.py`: **744 quadros de 4 episódios iguais píxel a píxel** |
| Uma só codificação (quadros em bruto direto no grafo que junta o fecho) | `oraculo/motor/mc_render.py` | recodificação completa e geração de compressão extra | −13 s por episódio; PSNR face aos quadros compostos **+0,1 a +1,8 dB**; fecho idêntico bit a bit | nº de quadros, duração e áudio (MD5 do PCM) iguais; `qc_video.py` sem problemas (prévia e final) |
| Teste de regressão do motor do TUBO | `oraculo/motor/mc_render_regressao.py` (novo) | nenhuma forma de provar que uma otimização não muda a imagem | — | corre contra `HEAD` ou `--ref` |
| QC com mensagem clara para ficheiro inexistente | `comum/qc/qc_video.py` | traceback quando o nome do vídeo está errado (aconteceu nesta sessão: o motor grava `D['saida']`, não `MC_FINAL.mp4`) | código 2 + mensagem | testado |

**Medido e revertido:** composição paralela no TUBO (2 processos): 62,4 s → 62,1 s, sem ganho (o ffmpeg disputa a CPU). Saiu, conforme a regra «sem ganho comprovado, reverte».

## C. Benchmark antes e depois

| Caso | Antes | Depois | Diferença | % | Memória (pico) |
|---|---|---|---|---|---|
| Mana & Burn · MB-EP16 prévia sem voz, 48,16 s, render completo | 371,4 s (3,9 quadros/s) | 239,9 s (6,0 quadros/s) | −131,5 s | −35 % | não medida por processo (2 Chromium ≈ 2 × 350 MB de RSS observados no `top`) |
| Meta em Curto · MC-PAU08 `previa`, 42,5 s com fecho | 105,3 s · 107,9 s (2 execuções) | 51,3 s · 49,0 s | −56 s | −53 % | 373 → 375 MB |
| Meta em Curto · CPU total da prévia | 139,3 s | 68,7 s | −70,6 s | −51 % | — |
| Meta em Curto · `final` com voz provisória sintética (sem ElevenLabs) | não medido antes | 55,6 s | — | — | 379 MB |

Limitações: uma máquina de 2 núcleos; caches frias e quentes não diferem de forma relevante (arranque do Chromium 0,8 s, carga do motor do TUBO 0,25 s); duas execuções no TUBO, uma no Mana & Burn; nenhum episódio publicado foi re-renderizado para publicação.

## D. Qualidade

- TUBO: menos uma geração de compressão no corpo do vídeo (medido em PSNR); fecho intacto.
- Mana & Burn: imagem inalterada (dentro da variação do próprio Chromium).
- Regressão: mudanças futuras no motor do TUBO passam a ter prova automática de «imagem igual».

## E. Pendências (decisão do fundador)

**E1 · `STATUS.md` só com o estado ativo.** Problema: 37 KB lidos em todas as sessões, com sobretudo histórico. Proposta: mover as secções de conteúdos CONCLUÍDOS/PUBLICADOS e das missões fechadas para `comum/status_arquivo.md` (sem apagar nada) e manter no `STATUS.md` só os conteúdos em produção, o que depende do fundador e o próximo passo (alvo ≤ 6 KB). Ganho esperado: ≈ 8–9 mil tokens a menos por sessão. Risco: perder contexto na retoma; mitigado pelo arquivo e pelo `comum/historico.md`. Texto a acrescentar a `AGENTS.md` §4: «O `STATUS.md` guarda só o estado ativo; o que fecha passa para `comum/status_arquivo.md`.»

**E2 · Radar Editorial Semanal** (reutilizar a escuta em três regiões entre episódios). Problema: `SHOWRUNNER.md` §2.4 2a obriga a refazer a escuta a cada episódio. Proposta: acrescentar ao 2a «Se existir `comum/radar/AAAA-SS.md` com menos de 7 dias, a escuta parte dele e só se atualiza o que mudou; cada linha tem região, assunto, fonte com data, validade e frentes possíveis.» Ganho: menos pesquisa repetida no 2.º e seguintes episódios da semana. Risco: usar tendência velha; mitigado pela validade de 7 dias. A escolha da pauta continua no Showrunner.

**E3 · Originalidade verificada uma vez.** Proposta em `SHOWRUNNER.md` §4.2, linha «Originalidade»: trocar o teste por «a ficha cita o resultado de `memoria.py pauta` (§2.3) e a data»; o mesmo no checklist A. Sem perda de proteção (é a mesma verificação).

**E4 · Relatório semanal de Insights** com facto · interpretação · hipótese · recomendação: já existe em `comum/insights/LEIA-ME.md`; não se criou outro. Falta o que o fundador já tem pendente (ecrã Conteúdo, visitas ao perfil, toques no link).

**E5 · Testar a captura paralela no PC do fundador**, se os renders do Mana & Burn passarem a correr lá: `python3 render.py X.mp4` usa os núcleos até 4; comparar com `--workers=1`.

## Handoff

```
HANDOFF · 26/11/2026 · Claude
Repositório: ibisson254/GERADOR-DE-VIDEO-BINDER · branch main · último commit: ver o commit desta missão (conferido no remoto no fim da sessão)

Objetivo atual: missão de engenharia (auditoria, benchmark e otimização dos motores) — implementado e medido; propostas E1–E3 aguardam o fundador.

Conteúdos tocados (comum/REGISTRO_EDITORIAL.md):
- nenhum (só motores e documentação técnica)

Decisões tomadas nesta sessão:
- nenhuma regra editorial mudou; alterações técnicas reversíveis registadas aqui e em comum/historico.md (DECISOES.md: não)

Documentos consultados:
- AGENTS.md, STATUS.md, constituição, catálogo, SHOWRUNNER.md, CHECKLIST_QUALIDADE.md, HANDOFF.md, manaburn/LEIA-ME.md, oraculo/motor/LEIA-ME.md, mc_render.py, render.py, qc_video.py

Alterações realizadas:
- manaburn/render.py · captura em paralelo (--workers=1 = antigo)
- oraculo/motor/mc_render.py · desfoque local + uma só codificação
- oraculo/motor/mc_render_regressao.py · teste novo
- comum/qc/qc_video.py · mensagem para ficheiro inexistente
- manaburn/LEIA-ME.md, oraculo/motor/LEIA-ME.md, este relatório, comum/historico.md, STATUS.md

Insights (domingo): não se aplica

Tarefas pendentes:
- E1 STATUS só ativo · depende do fundador
- E2 Radar Editorial Semanal · depende do fundador
- E3 originalidade verificada uma vez · depende do fundador
- E5 medir a captura paralela num PC com mais núcleos · depende do fundador

Próximo passo concreto: o fundador responde a E1–E3; se aprovar E1, mover as secções fechadas do STATUS.md para comum/status_arquivo.md.
```
