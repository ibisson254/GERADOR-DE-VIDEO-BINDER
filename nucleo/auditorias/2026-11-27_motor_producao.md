# Auditoria do motor de produção audiovisual · 27/11/2026

Pedido do fundador (27/11/2026, 23:06, «Prompt-mestre · auditoria forense, otimização e evolução do motor»). Continua a missão de engenharia de 26/11 (`2026-11-26_engenharia.md`), que já cobriu o Mana & Burn e o Meta em Curto: aqui não se repete o que lá está.

**Regras desta missão:** branch `auditoria/motor-producao-2026-11-27`, **sem push nem merge** (o fundador decide); zero créditos (ElevenLabs, vidIQ, imagem); nenhuma regra editorial, bíblia, identidade, voz, música ou episódio publicado alterado; nada substituído sem medir antes e depois.

**Ambiente das medições:** sessão Linux do Claude na cloud, 4 núcleos, 15 GB RAM, sem GPU, Python 3.13, ffmpeg 6.1.1, Chrome do sistema. Uma execução por caso salvo indicação; os números valem para esta máquina.

---

## A. Arquitetura atual (mapa)

Quatro motores de vídeo, uma camada comum de QC e um fluxo editorial documentado no repositório. Não há orquestrador central: o agente segue `AGENTS.md` → `SHOWRUNNER.md` → bíblia da frente → script do episódio.

| Etapa | Ferramenta / ficheiro | Entrada → saída | Manual? | APIs pagas |
|---|---|---|---|---|
| Ideia e escuta | `SHOWRUNNER.md` §2.4; radar semanal `comum/radar/` | conversa + pesquisa web → pauta | sim (fundador escolhe) | vidIQ só quando muda uma decisão |
| Originalidade | `comum/ferramentas/memoria.py pauta` | pauta → bloqueio/liberação | não | — |
| Pesquisa e verificação | WebSearch, agente web-fetch, Scryfall, EDHREC, Commander Spellbook | fontes → `fontes.md`, ficha | parcial | — |
| Roteiro | ficha (`nucleo/modelos/FICHA_EPISODIO.md`); ChatGPT pela §4.3 | pauta → roteiro + gancho (7 campos) | sim (aprovação) | — |
| Storyboard / arte | `telas_*.py` por episódio (MB), `episodio.json` (TUBO), script do episódio (Lambe) | roteiro → telas/peças | parcial | — |
| Assets (cartas) | scripts por episódio; Expedição `baixar_cartas.py`; LL-ART21 `catalogo_cartas.py`; **novo** `comum/ferramentas/cartas.py` | nomes → PNG + `creditos.json` | era manual | — |
| Voz | ElevenLabs (MB ~1.000–1.400 créditos; TUBO ~400–460) | texto → mp3 | autorização | **sim, o único custo recorrente** |
| Áudio | MB `process.py`/`sfx.py`/`trilha.py`; TUBO `mc_voz.py`; Lambe `motor_video.sfx` (sintetizado) | voz + trilha → mistura −14 LUFS | não | — |
| Animação e render | MB `index.html` + Playwright (`render.py`); TUBO `mc_render.py` (OpenCV/Pillow); Lambe `kit_video/motor_video.py` (OpenCV + texto pelo Chrome); Conde/Abismo/Expedição/Lisa Marie com motores próprios | cena → MP4 + fecho | não | — |
| Prévia barata | MB `previa_sem_voz.py`, TUBO modo `previa`/`stills`, Lambe `--mudo` | — | não | — |
| QA técnico | `comum/qc/qc_video.py`, `bordas.py`/`check_quadro.py` (MB), `mc_render_regressao.py` (TUBO), **novo** `comum/qc/comparar_videos.py` | MP4 → `qc.json` + folha de contacto | olho humano na folha | — |
| QA editorial | `nucleo/CHECKLIST_QUALIDADE.md`, revisão narrativa §4.2 | ficha → aprovação | sim (fundador) | — |
| Publicação | fundador no Instagram | pacote → post | sim, por regra | — |
| Análise | `comum/insights/` (CSV semanal a partir de prints) | prints → `registo_posts.csv` | sim | — |
| Encerramento | `memoria.py encerramento`, `validar_repo.py`, workflow `validar` | — | não | — |

Tempo de cada etapa por episódio: **DADO NÃO DISPONÍVEL** (as fichas registam créditos e duração do vídeo, não o tempo de trabalho). Consumo de tokens por etapa: **DADO NÃO DISPONÍVEL**; só o custo de arranque é medível em bytes (§D5).

## B. Diagnóstico (por impacto, com evidência)

| # | Achado | Evidência | Impacto |
|---|---|---|---|
| B1 | Motor do Lambe-lambe compunha cada peça no quadro inteiro (1080×1920, 2 a 6 vezes por quadro) | perfil cProfile do LL-ART21 V4: `blend` 115 s de 272 s (42 %) | tempo de render, iteração lenta das prévias |
| B2 | QC dava P1 de loudness em **todos** os vídeos do Lambe-lambe, aceite à mão (a bíblia pede pico −6 dBFS e música no Instagram) | fichas LL-ART21 V3/V4: «P1 de loudness aceite»; `qc_video.py` com −14 LUFS fixo para todas as frentes | ruído no QC = alertas reais ignorados; o TUBO também não tinha a regra de 25–35 s |
| B3 | QC não media codec, quadros pretos, silêncios nem dessincronia áudio/vídeo | `qc_video.py` (antes) | defeitos técnicos só apanhados a olho |
| B4 | Ambiente reinstalado à mão em cada sessão, com falha conhecida (`num2words` → `docopt` não compila) | memória do projeto; reproduzido nesta sessão (1.ª tentativa de `pip` falhou) | minutos e tokens perdidos por sessão |
| B5 | Chrome em caminho fixo `/usr/bin/google-chrome` nos kits do Lambe-lambe | 5 ficheiros; a skill do MB manda editar à mão `preview.py`/`render.py`/`bordas.py`; três padrões diferentes no repositório | os kits não correm no PC do fundador (Windows) sem editar código |
| B6 | Descarregar cartas e montar a linha de créditos refeito por episódio | 6 scripts próprios com `api.scryfall.com`; TUBO passo 2 manual | trabalho repetido; risco de crédito errado |
| B7 | Duas das três skills `binder-*` contradizem o repositório | `binder-posts-instagram`: «vale o documento mestre [do Drive]» e «atualizar o Registo de sessões no Drive»; «nada de grátis» (permitido desde 23/11). `binder-motor-de-arranque`: lê 4 docs do Drive, `claude/gerador-manaburn/`, pede o ZIP do kit (no repositório desde 02/11) | contexto desperdiçado e risco de seguir regra velha (constituição §1 diz que vale o repositório) |
| B8 | `STATUS.md` com 10,2 KB, acima do alvo de 6 KB decidido a 26/11 | `wc -c`; «Última sessão» repete o quadro «Prontos» | ~1 mil tokens a mais por sessão |
| B9 | 39 scripts fazem a sua própria normalização de loudness (`ebur128`/`loudnorm`) | `grep` | duplicação; não se mexe em episódios publicados |
| B10 | Conflito de alvo de pico no Abismo: −1,5 dBTP (`abismo/IDENTIDADE.md`) vs −1 dBTP (`abismo/PROCESSO.md`) | leitura | ambiguidade no QC do Abismo (fora do `qc_video.py`) |
| B11 | `registo_posts.csv` sem tempo médio de visualização, retenção aos 3 s nem atributos do vídeo (duração, tipo de gancho) | cabeçalho do CSV (14 linhas) | a aprendizagem de retenção pedida na Fase 6 não tem onde viver |

Não encontrado (procurado): processos paralelos que valha a pena paralelizar no TUBO (medido a 26/11, sem ganho); gerações de imagem desnecessárias (nenhuma: as imagens são cartas do Scryfall e telas desenhadas por código); modelos de IA caros em tarefas simples dentro do motor (o motor não chama modelos; o único serviço pago é a voz).

## C. Melhorias implementadas e medidas

| Melhoria | Ficheiros | Problema | Resultado | Teste |
|---|---|---|---|---|
| Composição só na região da peça | `lambe-lambe/kit_video/motor_video.py` (`blend`, `_roi`, `desenha`) | B1 | LL-ART21 V4 mudo: **264,6 s → 190,2 s (−28 %)**; CPU 434 → 357 s; memória igual (1,68 GB) | ver «Regressão» abaixo |
| QC por frente + verificações novas | `comum/qc/qc_video.py` | B2, B3 | Lambe-lambe sem falso P1; TUBO com 25–35 s; codec, pretos, silêncios, A/V; tempo do QC 13–14 s → 11–12 s (o vídeo é descodificado uma vez a menos) | MC-EP10, MB-EP21 final e prévia, LL-ART21 V4 e um vídeo sintético com defeitos (preto, silêncio, sem fecho): todos classificados como esperado |
| Regressão de vídeo para qualquer motor | `comum/qc/comparar_videos.py` (novo) | só o TUBO tinha prova de «imagem igual» | 1324 quadros em ~11 s | usado nesta missão |
| Testes do QC no CI | `comum/qc/test_qc.py` (novo), `.github/workflows/validar.yml` | QC sem testes | 5 testes OK em 42 s (local) | **o workflow alterado não correu no GitHub** (sem push) |
| Ambiente num comando | `comum/ferramentas/preparar_ambiente.sh`, `requisitos.txt` (novos) | B4 | venv limpo → pronto em 8 s, com o contorno do `num2words` | testado em venv novo |
| Chrome sem caminho fixo nos kits do Lambe-lambe | `kit_carrossel/compor.py` (`navegador()`), `motor_video.py` | B5 | `CHROME` → `/usr/bin/google-chrome` → Chromium do Playwright | na cloud usa o mesmo Chrome (imagem igual); **no Windows não testado** |
| Cartas + créditos num comando | `comum/ferramentas/cartas.py` (novo) | B6 | 3 cartas + `creditos.json` + linha da legenda em 2,0 s; mesmo formato do `creditos.json` da Expedição/TUBO | testado com Sol Ring (C21), Delver (ISD 51), Opt |
| Documentação | `comum/qc/LEIA-ME.md`, `kit_video/LEIA-ME.md`, `kit_carrossel/LEIA-ME.md`, `README.md`, `CHECKLIST_QUALIDADE.md` (2 linhas) | — | — | — |

**Regressão do motor do Lambe-lambe.** A base é determinística (duas execuções do código antigo: 1324/1324 quadros iguais). Depois da alteração, no vídeo codificado: 1312/1324 iguais; 12 quadros seguidos (312–323) diferem em ≤ 87 píxeis, diferença máxima 13, PSNR ≥ 79,5 dB. A causa foi isolada nos quadros compostos, antes do H.264: **1 píxel com ±1 nível em 14 quadros** (a interpolação numa janela menor arredonda 3·10⁻⁵ de forma diferente); o H.264 espalha essa diferença pelo bloco. Invisível, mas não é «igual bit a bit»: fica registado, como no Mana & Burn a 26/11.

**Medido e não feito:** a preparação das peças (`matte`) passou a ser ~35 % do render (65 s). Exige mexer em `kit_carrossel/compor.py`, partilhado com o carrossel; fica como P2 com regressão própria.

## D. Capacidades do Claude

1. **Skills.** As cinco skills pedidas (pesquisa, storytelling, direção de arte, motion & som, retenção & QC) **já existem como documentos do repositório**: `SHOWRUNNER.md` §2.4 (pesquisa e fontes), §4.1–4.2 (gancho em 7 campos, revisão narrativa), bíblias `CONTEXTO.md`/`PERFIL.md` (arte, som, movimento por frente), `CHECKLIST_QUALIDADE.md` + `qc_video.py` (QC), `comum/insights/` (aprendizagem). Criar SKILL.md com o mesmo conteúdo duplicaria regras (proibido por `AGENTS.md`) e somaria contexto. **Não se criaram skills novas.** O que falta é corrigir as três que existem (B7): proposta de edição entregue ao fundador no cartão de skills desta conversa (só ele as grava).
2. **Subagents.** A constituição §3 (etapa 3) já decide bem: um agente em sequência; separado só com ganho real. O único caso que compensa é a **verificação independente de factos** numa peça de risco alto (ex.: torneio com nomes de jogadores e lojas). Cada subagente relê o arranque (~79 KB), por isso dividir por função num episódio simples custa mais do que poupa. Nada implementado.
3. **MCP.** Scryfall abre por HTTP simples (agora com `cartas.py`); GitHub, ElevenLabs e vidIQ já estão ligados. Nenhum servidor MCP novo traria ganho comprovado. Nada instalado.
4. **Hooks.** Candidato: `SessionStart` a correr `preparar_ambiente.sh` só na cloud (`CLAUDE_CODE_REMOTE=true`). Não implementado: corre em todas as sessões (também nas que não renderizam), instala pacotes e no PC Windows o `sh` pode não existir. Decisão do fundador (P2); o comando manual já resolve num passo.
5. **Contexto.** Arranque obrigatório (`AGENTS`+`STATUS`+constituição+catálogo+`SHOWRUNNER`) = **78,9 KB** (~20 mil tokens, estimativa a ~4 bytes/token), mais a bíblia da frente (8–36 KB). O `SHOWRUNNER.md` (29,9 KB) é o maior. `STATUS.md` acima do alvo (B8). As skills de conta somam 37,8 KB e duas mandam ler ainda o Drive.

## E. Remotion

Não instalado. O Mana & Burn já trabalha no modelo do Remotion (cena HTML capturada quadro a quadro por um Chromium) e a auditoria de 26/11 mediu que **97 % do tempo é essa captura** (~290 ms/quadro, sem GPU). Os motores OpenCV são mais rápidos por quadro: TUBO ~35 ms de composição (26/11), Lambe-lambe ~144 ms por quadro com tudo incluído (hoje), contra ~290 ms só de captura no Mana & Burn. O Remotion poria todas as frentes na classe mais lenta, traria Node/React como segunda cadeia de ferramentas e tem licença própria a verificar para uso por empresa. Duplicaria o que os quatro motores já fazem. **Veredicto: não adotar.** Reavaliar só se surgir uma frente cujo desenho seja sobretudo tipografia/HTML e que hoje não tenha motor.

## F. Matriz de oportunidades

Escala 1–5 (risco e manutenção: 5 = baixo).

| Oportunidade | Qualidade | Custo | Tempo | Facilidade | Risco | Manut. | Prioridade | Estado |
|---|---|---|---|---|---|---|---|---|
| QC por frente (falso P1 do Lambe-lambe, TUBO 25–35 s) | 4 | 2 | 3 | 5 | 5 | 5 | **P1** | feito |
| Pretos, silêncio, codec, A/V no QC | 4 | 1 | 3 | 5 | 5 | 5 | **P1** | feito |
| Corrigir as skills `binder-*` | 3 | 4 | 3 | 5 | 5 | 5 | **P1** | proposta (fundador grava) |
| Ambiente num comando | 2 | 3 | 4 | 5 | 5 | 5 | **P1** | feito |
| Render do Lambe-lambe −28 % | 1 | 2 | 4 | 4 | 4 | 4 | **P1** | feito |
| Regressão de vídeo genérica + testes no CI | 3 | 1 | 2 | 5 | 5 | 4 | **P1** | feito (CI por confirmar) |
| Cartas + créditos num comando | 3 | 1 | 3 | 5 | 5 | 4 | **P2** | feito |
| Chrome sem caminho fixo (Lambe-lambe) | 1 | 1 | 2 | 5 | 5 | 5 | **P2** | feito |
| `matte` mais rápido (`compor.py`) | 1 | 1 | 3 | 3 | 3 | 3 | P2 | proposto |
| `STATUS.md` de volta a ≤ 6 KB | 1 | 3 | 2 | 5 | 4 | 5 | P2 | proposto (evitar conflito com outros chats) |
| Colunas de retenção no `registo_posts.csv` | 4 | 1 | 1 | 4 | 4 | 4 | P2 | proposto (decisão do fundador) |
| Hook `SessionStart` na cloud | 1 | 2 | 3 | 4 | 3 | 4 | P3 | proposto |
| Módulo de áudio comum (loudness) para motores novos | 2 | 1 | 2 | 3 | 4 | 3 | P3 | proposto (episódios publicados não se mexem) |
| Remotion | — | — | — | 1 | 2 | 1 | — | rejeitado (§E) |

Não há P0: nenhum defeito impede publicar o que está pronto.

## G. Piloto · LL-ART21 Will Murai (Lambe-lambe)

Os materiais do episódio estão no repositório (ficha, fontes, `catalogo_cartas.py`, `reel_v4.py`). O conteúdo está **concluído e à espera do fundador**, por isso o piloto **não refez pesquisa, roteiro nem storyboard** (conteúdos aprovados não se reabrem) e serviu para validar a arquitetura: reproduzir a V4 sem foto do zero numa sessão nova e passá-la pelo QC.

| Passo | Antes desta missão | Agora |
|---|---|---|
| Ambiente | `pip` falha no `num2words`; instalar à mão | `sh comum/ferramentas/preparar_ambiente.sh` (0,3 s quando já está; 8 s num venv novo) |
| Cartas | `catalogo_cartas.py` (54 ilustrações, 18,8 s, Scryfall 27/11: 54/54) | igual (script do episódio; o `cartas.py` serve episódios novos) |
| Render (mudo) | 264,6 s | 190,2 s |
| Render (com som) | — | 195,2 s (com outra tarefa a correr ao mesmo tempo) |
| QC | P1 de loudness aceite à mão | «Sem problemas mensuráveis»: −20,4 LUFS (informativo), pico −6,5 dBTP (< −6), h264/yuv420p, fecho a 40,27 s |
| Regressão | não havia para este motor | `comparar_videos.py` (§C) |
| Intervenção manual | edição do caminho do Chrome fora da cloud; aceitar o P1 | nenhuma na cloud |

Folha de contacto conferida a olho: cartas inteiras, textos dentro dos papéis, fecho intacto. Diferença encontrada: nesta máquina não há Noto Serif CJK, por isso o kanji 秀樹 sai noutra fonte (o `preparar_ambiente.sh` avisa). Qualidade narrativa e visual: **não avaliada** (é a do episódio já aprovado; não mudou).

Comparação de custo: zero créditos nas duas versões. Melhoria percentual só no render e no QC, onde há números comparáveis; o tempo total de produção de um episódio **não é comparável** (DADO NÃO DISPONÍVEL para o método anterior).

## H. Documentação

Os ficheiros pedidos já têm equivalente e não se duplicaram: arquitetura e fluxo = `AGENTS.md` + `SHOWRUNNER.md` + `series.yaml` + os `LEIA-ME.md` de cada motor (mapa resumido no §A); procedimento de episódio = `SHOWRUNNER.md` §6 e skill da frente; QC = `CHECKLIST_QUALIDADE.md` + `comum/qc/LEIA-ME.md`; custos e roadmap = este relatório (§B, §F, §I) e `2026-11-26_engenharia.md`. Atualizados: os LEIA-ME e as duas linhas do checklist.

## I. Pendências (decisão do fundador)

1. **Integrar a branch** `auditoria/motor-producao-2026-11-27` na `main` (merge ou PR). Depois do push, confirmar o workflow `validar` verde (o passo novo dos testes do QC não correu no GitHub).
2. **Gravar a correção das skills** `binder-motor-de-arranque` e `binder-posts-instagram` (cartão nesta conversa).
3. Testar no PC: `CHROME` por definir → o kit usa o Chromium do Playwright (`python -m playwright install chromium`).
4. P2/P3 do §F: `matte`, `STATUS.md`, colunas de retenção, hook, módulo de áudio; Abismo: escolher −1 ou −1,5 dBTP.

## Handoff

```
HANDOFF · 27/11/2026 (~00h15 UTC de 28/11) · Claude
Repositório: ibisson254/GERADOR-DE-VIDEO-BINDER · branch auditoria/motor-producao-2026-11-27 · commit local (sem push, a pedido do fundador)

Objetivo atual: auditoria do motor de produção; melhorias implementadas e medidas, à espera de integração.

Conteúdos tocados (comum/REGISTRO_EDITORIAL.md):
- nenhum (LL-ART21 só re-renderizado na sessão, para medir; nada entregue nem alterado)

Decisões tomadas nesta sessão:
- nenhuma regra editorial mudou; o QC passou a aplicar o alvo de áudio que a bíblia do Lambe-lambe já tinha (DECISOES.md: não)

Documentos consultados:
- AGENTS.md, STATUS.md, constituição, INVENTARIO.md, 2026-11-26_engenharia.md, comum/qc/*, lambe-lambe/kit_video/*, kit_carrossel/compor.py, manaburn/LEIA-ME.md, oraculo/motor/LEIA-ME.md, ficha LL-ART21, CHECKLIST_QUALIDADE.md, series.yaml, skills binder-*

Alterações realizadas:
- lambe-lambe/kit_video/motor_video.py · composição por região + Chrome
- lambe-lambe/kit_carrossel/compor.py · navegador()
- comum/qc/qc_video.py · alvos por frente, codec, pretos, silêncios, A/V
- comum/qc/comparar_videos.py, comum/qc/test_qc.py · novos
- comum/ferramentas/preparar_ambiente.sh, requisitos.txt, cartas.py · novos
- .github/workflows/validar.yml · testes do QC
- LEIA-ME (qc, kit_video, kit_carrossel), README.md, CHECKLIST_QUALIDADE.md, comum/historico.md, STATUS.md, este relatório

Insights (domingo): não se aplica

Tarefas pendentes:
- integrar a branch e confirmar o validar verde · depende do fundador
- gravar a correção das skills binder-* · depende do fundador
- P2/P3 do §F · depende do fundador

Próximo passo concreto: o fundador decide o merge da branch; depois, `sh comum/ferramentas/preparar_ambiente.sh` passa a ser o 1.º comando de cada sessão que renderiza.
```
