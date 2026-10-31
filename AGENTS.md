# AGENTS.md · Estúdio BINDER (@binderthetrade)

Ponto de entrada para qualquer agente (Claude, ChatGPT ou outro). As instruções de cada plataforma só remetem para este ficheiro. Este repositório é a fonte de verdade do estúdio (constituição §1).

## 1. Ordem de leitura

1. `STATUS.md`: estado atual, bloqueios e próxima tarefa.
2. `nucleo/CONSTITUICAO_EDITORIAL_BINDER_ORIGINALS.md`: processo, rigor, entrega, bloqueios, especiais.
3. `series.yaml`: escolher a série pela palavra de arranque.
4. Perfil e identidade da série, e só dessa série:

   | Palavra | Série | Ler |
   |---|---|---|
   | `manaburn` | Mana & Burn | `manaburn/PERFIL.md` → doc da série no Drive / skill `binder-mana-burn-episodio` → `manaburn/LEIA-ME.md` |
   | `tubo` / `meta` | Meta em Curto (TUBO) | `oraculo/PERFIL.md` → `oraculo/CONTEXTO.md` |
   | `conde` | Conde de Manaforte | `conde/PERFIL.md` → `conde/CONTEXTO.md` |
   | `post` | Posts estáticos e carrosséis | skill `binder-posts-instagram` (pasta própria a criar) |

5. `comum/historico.md` e `comum/easter_eggs.md`: não repetir tema nem egg.

## 2. Produzir um conteúdo

1. Ficha a partir de `nucleo/modelos/FICHA_EPISODIO.md`; estratégia pela constituição §3.
2. Produzir; validar com `nucleo/CHECKLIST_QUALIDADE.md` e os critérios do perfil.
3. Entregar: vídeo, capa, legenda, comentário fixado, texto alternativo, fontes, e as limitações reais.
4. Commit: ficha/roteiro, legenda, fontes, histórico, easter egg. Nunca vídeos renderizados.

Regras que nunca mudam: não inventar factos nem funções/telas do app; todo vídeo termina com `comum/outro/outro_binder_916.mp4`; 9:16 sem corte lateral, conferido no ficheiro final.

Série nova: `nucleo/modelos/PERFIL_SERIE.md` + entrada em `series.yaml`. Mudança de regra: `nucleo/DECISOES.md`.

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
- No fim de cada sessão: commit, `STATUS.md` atualizado (feito, falta, bloqueios, próximo passo) e um texto curto de retoma para colar no chat seguinte.
- Nada do que importa fica só na conversa: decisões em `nucleo/DECISOES.md`, desempenho em `comum/historico.md`, episódios nas fichas.
