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

## Vince Vault (09/11/2026)

Personagem em desenvolvimento, ainda sem frente. Bíblia: `vince/BIBLIA_PERSONAGEM.md`. Tudo na branch `vince-vault`, por aprovar em PR #11.
**Vince 3D: começar por `vince/MODELO_3D.md` → secção "Retomar aqui".** Modelo v02 feito a 09/11 (noite): malha gerada pelo TRELLIS.2 local a partir da vista de frente em pose A, com rig de corpo, olhos, pálpebras, boca, queixo e sobrancelhas a funcionar, e óculos escondidos por ordem do fundador (`Documentos\Vince\vince_modelo_v02.blend`, no PC do fundador). Defeitos conhecidos listados no mesmo documento (botões a mais, colarinho, anel, dedos sem ossos). Próximo passo: o fundador vê os renders e decide entre corrigir este modelo ou gerar outra imagem.
Fantoche 2D (08/11): base para falar 9:16, mesa com ecrã verde e pose extra em `vince/referencias/`; proposta de formato em `vince/PROPOSTA_FORMATO.md` (boletim semanal da bolsa de cartas); piloto EP00 em animatic, sem voz (`vince/episodios/ep00_fechamento_ficha.md`). Falta o fundador aprovar o animatic e os 670 créditos da narração.

## Depende do fundador

- Aprovar um esboço das expressões novas do Mana e do Burn (auditoria §4) antes de as desenhar no kit.
- Enviar ou subir o motor que gerou o Giro (não há "giro" em `claude/gerador-manaburn/`).
- Drive atualizado a 02/11 (notas de fonte de verdade na bíblia, no doc 05 e no Mapa do Drive; secção de estado na bíblia).

## Pendências técnicas (não bloqueiam a governação)

- Motor v2 do Mana & Burn: núcleo no repositório desde 02/11 (`manaburn/`, v1 em `manaburn/extras/v1/`); ficaram no projeto claude.ai `montar.py`, `scryfall.py`, `lote.py`, `testes.py`, `formatos.*` e episódios 1, 5–7. O motor do Giro foi feito noutro chat e não está disponível.
- Gerador do Órbita já no repositório (`orbita/gerador/`); para renderizar faltam os PNGs das cartas (`BINDER_gerador_orbita.zip`) e as fontes em `node_modules/`.
- `oraculo/episodios/ep01_render_v2.py` importa `render`, que não existe; `conde/montar_ep002.py` tem caminho absoluto. Não se mexe em scripts de episódios publicados sem necessidade.
- Skills `binder-*` ainda mandam ler primeiro o Drive e dizem que o Scryfall não abre; alinhar com o repositório quando o fundador quiser.

## Próximo passo concreto

Conde Ep. 004 (Joven) produzido a 03/11/2026 e por publicar: o fundador ouve a pronúncia de "Joven", "Chandler" e "Eron" e publica o pacote (`conde/legendas/ep004_joven_legenda.txt`, ficha em `conde/episodios/ep004_joven_ficha.md`; o vídeo não está no repositório, recria-se com `python3 conde/montar_ep004.py`, desde que `conde/ep004/audio/narracao.wav` exista: se faltar, ver o flow ElevenLabs em `conde/episodios/ep004_fontes.txt`). Depois: próximo Giro ou episódio do Mana & Burn com o kit v2 de `manaburn/`; validar com `python3 -I comum/qc/qc_video.py`.

## Handoff

Último: 09/11/2026 (noite), Vince Vault 3D v02 (handoff abaixo e `vince/MODELO_3D.md`). Anterior: 09/11/2026, Vince Vault 3D (pipeline).

```
HANDOFF · 09/11/2026 20:50 · Claude
Repositório: ibisson254/GERADOR-DE-VIDEO-BINDER · branch vince-vault

Objetivo atual: Vince Vault em 3D de nível profissional, com rig, expressões e lip sync.

Decisões tomadas nesta sessão:
- Nenhuma decisão editorial nova. Técnica: o v02 vive num ficheiro novo (vince_modelo_v02.blend); o v01 não foi alterado.

Documentos consultados:
- vince/MODELO_3D.md, vince/FICHA_VISUAL.md, vince/BIBLIA_PERSONAGEM.md, vince/blender/vince_ferramentas.py

Alterações realizadas:
- vince/MODELO_3D.md · estado do v02, defeitos conhecidos, geração sem navegador, notas de trabalho
- vince/blender/vince_ferramentas.py · pose(), repouso(), piscar(), olhar()
- STATUS.md · secção Vince Vault e este handoff
- No PC do fundador (fora do repositório): Vince_00002.glb, vince_modelo_v02.blend, renders em Documentos\Vince

Tarefas pendentes:
- Ver os renders e escolher: corrigir o v02 (botões, colarinho, anel, dedos) ou gerar nova imagem · fundador
- Dizer se os óculos saem de vez do personagem (a bíblia §2 trata-os como assinatura) · fundador
- Teste de lip sync com fala real (precisa de .wav; ElevenLabs só com autorização) · fundador + agente
- Dedos com um osso cada, anel, botões, colarinho · agente
- Aprovar o uso do 3D em produção e o PR #11 · fundador

Próximo passo concreto: ler vince/MODELO_3D.md → "Retomar aqui".
```
