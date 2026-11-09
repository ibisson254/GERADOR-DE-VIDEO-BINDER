# STATUS · Estúdio BINDER

Branch principal: `main` (consolidação integrada a 31/10/2026, PR #1, aprovado pelo fundador). A branch `consolidacao-estudio` fica como histórico.
Missão "Visual Evolution & Character Excellence" (02/11/2026) integrada em `main` por PR (aprovação do fundador, 02/11, 01:27). Anterior: "Consolidação estrutural do BINDER Originals" (31/10/2026), concluída.

## Estado editorial

Giro de domingo de 01/11 publicado (registado em `comum/historico.md`, 02/11). Frentes ativas: Mana & Burn, Conde de Manaforte, Meta em Curto (séries); Órbita (temática); Lambe-lambe (espontânea); especiais. Tudo o que está no repositório está aprovado e lançado; Halloween 2026 e Star Trek publicados. Detalhe: `nucleo/CATALOGO_EDITORIAL.md`.

## Consolidação

| Bloco | Estado | Onde |
|---|---|---|
| Inventário | Concluído | `INVENTARIO.md` (histórico) |
| Integração de `especial/sir-patrick` | Concluído, sem conflitos | commit 4e6af96 |
| Núcleo e fonte de verdade | Concluído | `nucleo/`, constituição v1.4 |
| Catálogo editorial (Órbita e Lambe-lambe ativos) | Concluído | `nucleo/CATALOGO_EDITORIAL.md` |
| Hierarquia documental | Concluído | constituição §1, `nucleo/README.md` |
| Showrunner + handoff | Concluído | `nucleo/SHOWRUNNER.md`, `nucleo/modelos/HANDOFF.md` |
| Prompts Claude Project e ChatGPT | Texto pronto | `nucleo/prompts/` |
| Instruções do projeto claude.ai | Aplicadas pelo fundador (31/10) | `nucleo/prompts/CLAUDE_PROJECT.md` |
| Respostas Q1–Q3 aplicadas (nome Meta em Curto, Órbita sem fecho, Órbita e Lambe-lambe no repositório) | Concluído | `orbita/`, `lambe-lambe/`, constituição v1.4 |
| Fecho do scanner no repositório | Concluído (cortado do fim do Ep. 6, rótulo tapado) | `comum/outro/outro_binder_916.mp4`, `comum/outro/gerar_fecho.py` |
| Merge para `main` | Concluído, aprovado pelo fundador | GitHub, PR #1 |
| Prompt do ChatGPT a apontar para `main` | Concluído | `nucleo/prompts/CHATGPT.md` |

## Evolução visual (02/11/2026)

| Bloco | Estado | Onde |
|---|---|---|
| Auditoria do Giro de domingo (01/11) com timecodes, revista com a bíblia do Drive | Concluído: 0 P0, 10 P1, 4 P2, 1 decisão pendente | `nucleo/auditorias/2026-11-02_evolucao_visual.md` |
| Controlo de qualidade automático | Implementado e testado | `comum/qc/` |
| Checklist P0/P1/P2 + bloco E | Implementado | `nucleo/CHECKLIST_QUALIDADE.md` |
| Memória de continuidade por série | Implementado (semente) | `comum/continuidade/` |
| Expressões e poses novas do Mana e do Burn, regra "quem ouve reage" | Proposto | auditoria §4 |
| Cenário-mestre, planos fixos, luz da TV, grelha da TV SAL | Proposto | auditoria §5 |
| Formato "Giro de domingo" no perfil | Proposto | auditoria §7 |
| Correções no motor que gerou o Giro | Bloqueado: motor feito noutro chat | auditoria §6 |
| Kit v2 no repositório + melhorias (legenda na zona segura, fonte do medidor, ventilador, antena, paninho) | Implementado e testado (bordas OK) | `manaburn/LEIA-ME.md` |
| Duração livre nas séries | Implementado (constituição v1.5) | `nucleo/DECISOES.md` |

## Depende do fundador

- Aprovar um esboço das expressões novas do Mana e do Burn (auditoria §4) antes de as desenhar no kit.
- Enviar ou subir o motor que gerou o Giro (não há "giro" em `claude/gerador-manaburn/`).
- Drive atualizado a 02/11 (notas de fonte de verdade na bíblia, no doc 05 e no Mapa do Drive; secção de estado na bíblia).

## Pendências técnicas (não bloqueiam a governação)

- Motor v2 do Mana & Burn: núcleo no repositório desde 02/11 (`manaburn/`, v1 em `manaburn/extras/v1/`); ficaram no projeto claude.ai `montar.py`, `scryfall.py`, `lote.py`, `testes.py`, `formatos.*` e episódios 1, 5–7. O motor do Giro foi feito noutro chat e não está disponível.
- Gerador do Órbita já no repositório (`orbita/gerador/`); para renderizar faltam os PNGs das cartas (`BINDER_gerador_orbita.zip`) e as fontes em `node_modules/`.
- `oraculo/episodios/ep01_render_v2.py` importa `render`, que não existe; `conde/montar_ep002.py` tem caminho absoluto. Não se mexe em scripts de episódios publicados sem necessidade.
- Skills `binder-*` ainda mandam ler primeiro o Drive e dizem que o Scryfall não abre; alinhar com o repositório quando o fundador quiser.

## Especial em espera de publicação

`especiais/precon_em_jogo/`: vídeo final conferido (02/11), publicação prevista a 04/11/2026. Depende do fundador: ouvir, avisar @diegoalencard e publicar.

## Especial "Precon em jogo" · V2 para impulsionamento (03/11/2026)

Branch `especial/precon-em-jogo-v2` (a partir de `especial/precon-em-jogo`). V2 com luz e profundidade em pós-produção (`especiais/precon_em_jogo/polimento_v2.py`), áudio idêntico, QC sem problemas (`qc_v2.md`). Bloqueado: objetos novos e reenquadramento (faltam vozes, `data.js` e quadros do TUBO deste especial no repositório). Aguarda aprovação do fundador.

## Sala v3 do Mana & Burn (08/11/2026)

Aprovada e aplicada no `manaburn/index.html`: mesa de Commander, mesa acima das legendas, taco, luz no cenário (`luz.py` passa a opcional). `bordas.py` OK com o Ep. 2 (laterais 10–1068 px, topo 300 px). Burn no plano da TV corrigido (cabelo, camisa e ombros; 08/11, 00:05). Pendente: primeiro episódio completo com a sala v3.

## Luz padrão do Mana & Burn (07/11/2026)

Aprovada pelo fundador (`nucleo/DECISOES.md`). Fase 1 implementada e integrada na `main` (07/11, "Prossiga" do fundador): `manaburn/luz.py` + `render.py` (por defeito), docs e checklist. Por aprovar: fase 2 (luz no `index.html`); objetos novos e planos fixos. Especial "Precon em jogo" e V2 integrados na `main` no mesmo merge.

## Conde Ep. 005 · Hyalopterous Lemure (09/11/2026)

Branch `conde/ep005-lemure` (sem merge para `main`). **Produzido, não publicado.** Roteiro aprovado pelo fundador (09/11, 11:52, sem cortes); voz gerada (1 geração, 1 099 créditos); render final 69,1 s + fecho = 72,97 s, refeito às 12:10 depois de o fundador apontar a música (o 1.º render tinha ruído no lugar do tema por um erro de tipo na emenda; corrigido e verificado); QC automático sem problemas (−14,0 LUFS, pico −1,8 dBTP, fecho completo), carta e arte inteiras conferidas no ficheiro final. Pacote editorial completo. Ficha: `conde/episodios/ep005_hyalopterous_lemure_ficha.md`. Único P1 aberto: pronúncia e equilíbrio voz/música por ouvir.

## Próximo passo concreto

1. Fundador: ouvir o `EP005_CONDE_LEMURE.mp4` (pronúncia de "Hyalopterous", "Lemure", "lemur", "Rosewater", "Wizards", "Ice Age" e equilíbrio voz/música), abrir o link do artigo de Rosewater, e aprovar o episódio e o merge da branch `conde/ep005-lemure`. Publicar é decisão do fundador.
2. Se a pronúncia falhar: nova geração só com autorização (créditos); o resto do pipeline está pronto (`conde/encurtar_narracao_ep005.py` → `conde/montar_ep005.py`).
3. Continua pendente: Conde Ep. 004 (Joven) produzido e por publicar (pronúncia de "Joven", "Chandler" e "Eron" por ouvir). Depois: próximo Giro ou episódio do Mana & Burn com o kit v2.

## Handoff

Último: 09/11/2026, Conde Ep. 005 (abaixo). Anterior: 02/11/2026, no fim de `nucleo/auditorias/2026-11-02_evolucao_visual.md`.

```
HANDOFF · 09/11/2026 ~12:15 Lisboa · Claude
Repositório: ibisson254/GERADOR-DE-VIDEO-BINDER · branch conde/ep005-lemure · último commit: ver git log da branch

Objetivo atual: Conde de Manaforte Ep. 005 (Hyalopterous Lemure, arte original de Richard Thomas): produzido; falta audição e aprovação do fundador.

Decisões tomadas nesta sessão:
- Roteiro aprovado pelo fundador sem cortes (09/11, 11:52) → voz autorizada. Nenhuma regra mudou (DECISOES.md não alterado). Escolhas de produção na ficha: nenhum texto sobre a ilustração, carimbos nas margens, pergunta A/B Sorrow's Path × Urza's Mine, sem easter egg.

Documentos consultados:
- AGENTS.md, STATUS.md, nucleo/ (constituição, catálogo, SHOWRUNNER, DECISOES, CHECKLIST, modelos), conde/PERFIL.md, conde/CONTEXTO.md, comum/historico.md, comum/easter_eggs.md, comum/continuidade/conde.md, fichas e montadores dos Ep. 002–004.

Alterações realizadas:
- conde/montar_ep005.py, conde/encurtar_narracao_ep005.py, conde/capa_ep005.py, conde/ep005/ (art.jpg, card.png, roteiro.txt, tempos_previa.py, audio/words_previa.json, audio/words_raw.json, audio/words_novo.json)
- conde/episodios/ep005_hyalopterous_lemure_ficha.md, conde/episodios/ep005_fontes.txt, conde/legendas/ep005_lemure_legenda.txt
- comum/historico.md, comum/continuidade/conde.md, STATUS.md
- Não versionados (regra): EP005_CONDE_LEMURE.mp4, capa, narracao.wav/mp3. Take no flow ElevenLabs ORXBjdQIsTKsO0axku7X.

Tarefas pendentes:
- Ouvir pronúncia e mistura (P1) · fundador
- Aprovar o episódio, merge para main e publicação · fundador

Próximo passo concreto: o fundador ouve EP005_CONDE_LEMURE.mp4 e responde "aprovado" (→ merge e registo como aprovado) ou indica a palavra mal pronunciada (→ pedir autorização para nova geração).
```
