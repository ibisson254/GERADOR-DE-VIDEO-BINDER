# STATUS · Operação de Consolidação do Estúdio BINDER

Branch de trabalho: `consolidacao-estudio` (nunca `main`). Prompt da operação: "Operação de Consolidação — Estúdio BINDER" (31/10/2026).

## Fases

| Fase | Estado | Data | Entrega |
|---|---|---|---|
| 0 · Inventário (só leitura) | Concluída | 31/10/2026 | `INVENTARIO.md` |
| 1 · Núcleo | **Concluída** | 31/10/2026 | `nucleo/`, `series.yaml`, `AGENTS.md`, constituição v1.2 |
| 2 · Séries (M&B → Conde → TUBO → Posts) | Pendente · **próxima: Mana & Burn** | — | — |
| 3 · Showrunner e arranque | Pendente | — | — |
| 4 · Testes e relatório | Pendente | — | — |

## Decisões tomadas por defeito (31/10, "Prossiga" sem resposta a P1–P4)

Todas reversíveis nesta branch; registadas em `nucleo/DECISOES.md`.

- P1 · Opção B: `manaburn/`, `oraculo/`, `conde/` e `comum/outro/` ficam no lugar; `series.yaml` liga slug → pasta.
- P2 · Órbita e Lambe-lambe: registadas como `arquivada`.
- P3 · TUBO: silhueta em vez de foto de jogador (regra de 29/10).
- P4 · `especial/sir-patrick` integrada por merge (constituição v1.1 §14, Picard v2).

## Feito na Fase 1

- Merge de `especial/sir-patrick` sem conflitos (commit 4e6af96).
- `comum/originals/` → `nucleo/` (nomes de ficheiro mantidos; referências dos perfis atualizadas; `comum/LEIA-ME.md` explica a mudança).
- Constituição v1.2: §1 repositório como fonte de verdade; §2 com `especiais/`, `nucleo/` e `series.yaml`; §10 e checklist com texto alternativo.
- `nucleo/README.md`: índice das regras comuns e marca/posicionamento (só com o que as fontes dizem).
- `series.yaml`: 4 séries do estúdio + 2 arquivadas; voice_id do TUBO e do Conde; Talis/Erik sem voice_id registado (null).
- `AGENTS.md` reescrito como entrada neutra (leitura, produção, segurança, retoma); `CLAUDE.md` só remete para ele; `README.md` com a estrutura nova.

## Falta

- Fase 2 · Mana & Burn: subir o motor v2 do projeto claude.ai para o repositório, criar `biblia.md`/`visual.md`/`sonoro.md`/`roteiro-modelo.md`/`historico.md` a partir do doc da série no Drive e reproduzir o Ep. 09 com as vozes já existentes (sem gastar créditos).
- Fase 3: `nucleo/router.md`, `nucleo/showrunner.md`, skills, instruções do projeto claude.ai, `LEIA-ME` no Drive.

## Bloqueios

1. `comum/outro/outro_binder_916.mp4` não existe no repositório (Ibisson envia).
2. `ManaBurn_kit.zip` não aberto (conector só em base64; computador não ligado à bridge).
3. `concrete_teeth.mp3` em falta (só para reproduzir os Ep. 5–7).
4. Vozes do Ep. 09 (MP3 do Burn e do Mana): não estão no repositório; sem elas, o teste de referência do Mana & Burn não corre sem gastar créditos.
5. Escrita no Drive e nas instruções do projeto claude.ai precisa de autorização (Fase 3).

## Retoma

Numa sessão nova: colar o prompt da operação e escrever "Lê `STATUS.md` no repositório e continua a partir da próxima fase pendente." O agente clona o repositório, faz checkout de `consolidacao-estudio` e lê este ficheiro, o `AGENTS.md` e o `INVENTARIO.md`.
