# AGENTS.md · Estúdio BINDER (@binderthetrade)

Ponto de entrada para qualquer agente (Claude, ChatGPT ou outro). As instruções de cada plataforma só remetem para este ficheiro (textos prontos em `nucleo/prompts/`). Este repositório é a fonte de verdade do estúdio (constituição §1).

## 1. Ordem de leitura

1. `STATUS.md`: estado atual, bloqueios e próxima tarefa.
2. `nucleo/CONSTITUICAO_EDITORIAL_BINDER_ORIGINALS.md`: regras do estúdio; §1 tem a hierarquia documental.
3. `nucleo/CATALOGO_EDITORIAL.md`: frentes, classificação e estado.
4. `nucleo/SHOWRUNNER.md`: como classificar o pedido, escolher a frente e preparar o briefing.
5. Bíblia e perfil da frente, e só dessa frente:

   | Palavra | Frente | Tipo | Ler |
   |---|---|---|---|
   | `manaburn` | Mana & Burn | Série | `manaburn/PERFIL.md` → doc da série no Drive / skill `binder-mana-burn-episodio` → `manaburn/LEIA-ME.md` |
   | `tubo` / `meta` / `oraculo` | Meta em Curto | Série | `oraculo/PERFIL.md` → `oraculo/CONTEXTO.md` |
   | `tubo segunda` / `tubo quinta` | Meta em Curto · ciclo semanal | Série | `oraculo/CICLO_SEMANAL.md` → `python3 -I oraculo/previsoes/ciclo.py segunda` ou `quinta` |
   | `conde` | Conde de Manaforte | Série | `conde/PERFIL.md` → `conde/CONTEXTO.md` |
   | `especial` | Especiais e homenagens | Pontual | constituição §14 + bíblias das séries envolvidas |
   | `orbita` | Órbita · Star Trek | Temática | `orbita/CONTEXTO.md` → `orbita/gerador/LEIA-ME.md` |
   | `lambe` / `post` | Lambe-lambe | Espontânea | `lambe-lambe/CONTEXTO.md` → skill `binder-posts-instagram` |
   | `vince` / `vinci` / `mercado` / `preco` | Vince Vault · Multiverse Capital (frente aprovada 12/11, em desenvolvimento) | Série | `vince/PERFIL.md` → `vince/CONTEXTO.md` (direção 2D; o material 3D é arquivo: `vince/MODELO_3D.md`, `vince/V03_PLANO.md`) |

6. `comum/REGISTRO_EDITORIAL.md` (memória editorial de todas as frentes) e `comum/easter_eggs.md`: não repetir tema, objeto nem egg. Auditoria de originalidade em `nucleo/SHOWRUNNER.md` §2.3.
7. Domingo, com prints do Instagram Insights: `comum/insights/LEIA-ME.md`.

`series.yaml` tem a configuração técnica de cada frente (pastas, vozes, trilhas, episódio de referência).

## 2. Produzir um conteúdo

1. Pauta: auditoria de originalidade (`python3 comum/ferramentas/memoria.py pauta …`) e linha nova em `comum/REGISTRO_EDITORIAL.md`.
2. Ficha a partir de `nucleo/modelos/FICHA_EPISODIO.md`; estratégia pela constituição §3.
3. Produzir; validar com `nucleo/CHECKLIST_QUALIDADE.md` e os critérios do perfil.
4. Entregar: vídeo, capa, legenda, comentário fixado, texto alternativo, fontes, e as limitações reais.
5. **Encerramento obrigatório** (`nucleo/SHOWRUNNER.md` §6): pacote e ficha na pasta do episódio, registo, histórico, STATUS, handoff, `memoria.py encerramento <ID>` OK, commit enviado e conferido no GitHub. Nunca vídeos renderizados. Não se declara um episódio arquivado sem o commit conferido.

Previsões do TUBO: toda produção de Meta em Curto começa por `python3 -I oraculo/previsoes/ciclo.py continuacao` e toda previsão nova entra em `oraculo/previsoes/registo.yaml` antes da voz (`oraculo/CICLO_SEMANAL.md` §0).

Regras que nunca mudam: não inventar factos nem funções/telas do app; todo vídeo termina com `comum/outro/outro_binder_916.mp4` (exceto Órbita e exceções registadas em especiais); sem corte lateral no formato da frente, conferido no ficheiro final.

Frente nova: fim de `nucleo/CATALOGO_EDITORIAL.md`. Mudança de regra: `nucleo/DECISOES.md`. Conteúdos publicados ou aprovados não se reabrem.

## 3. Segurança

- Não apagar ficheiros sem autorização do Ibisson.
- Nada de force push nem de merge automático para `main`.
- Não sobrescrever originais nem versões sem comparar.
- Nunca versionar credenciais, chaves API ou dados de testadores.
- Não publicar no Instagram.
- Não gastar créditos de serviços externos (ElevenLabs, música, imagem, vídeo) sem autorização explícita.
- Não mudar a identidade visual, sonora ou editorial de uma série por preferência própria.
- Perante uma decisão irreversível, um conflito de versões ou um custo: parar só essa ação, preservar o estado e pedir autorização.

## 4. Retoma entre sessões e plataformas

- Clonar com profundidade 1 e ler `STATUS.md` antes de qualquer outra coisa.
- No fim de cada sessão: commit, `STATUS.md` atualizado e handoff no formato de `nucleo/modelos/HANDOFF.md`.
- Nada do que importa fica só na conversa: decisões em `nucleo/DECISOES.md`, conteúdos e estados em `comum/REGISTRO_EDITORIAL.md`, cronologia em `comum/historico.md`, números em `comum/insights/`, episódios nas fichas.
- Antes de fechar: `python3 comum/ferramentas/memoria.py validar` sem erros.
