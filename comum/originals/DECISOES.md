# Registo de decisões · BINDER Originals

Uma entrada por alteração de regra: data · o quê · porquê · impacto. Mais recente no topo.

## 28/10/2026 · v1.0 do sistema BINDER Originals

**O quê:** constituição comum, checklist, modelos de ficha e de perfil, `PERFIL.md` por série, `CLAUDE.md` + `AGENTS.md` na raiz.
**Porquê:** as regras estavam espalhadas entre instruções do projeto, skills, documentos do Drive e conversas; cada série repetia regras comuns de forma diferente.
**Impacto:** todo agente começa pelo `CLAUDE.md`. Os `CONTEXTO.md` não foram alterados.

Divergências encontradas na auditoria e como ficaram:

1. **Nome do Conde.** Pedido de 28/10 diz "Conde de Terra Forte"; repositório, episódios e instruções do projeto dizem "Conde de Manaforte". Mantido **Manaforte** até o Ibisson confirmar outra coisa.
2. **Nome da série do TUBO.** Pasta `oraculo/` e `CONTEXTO.md` dizem "Oráculo de Tubo"; nome atual é "Meta em Curto". Pasta mantida (scripts dependem dela); perfil e `CLAUDE.md` usam o nome novo.
3. **Fecho da legenda e do comentário do Conde.** `conde/CONTEXTO.md` §8 tem frases anteriores ao sistema de easter eggs. Prevalece a regra comum ("baixe o BINDER Vision" / "Tem um detalhe escondido. Diga o segundo.").
4. **Território Mana & Burn × Meta em Curto.** O doc do Mana & Burn previa "episódio de campeonato". Regra: decisão e meta → Meta em Curto; reação/polémica de um torneio → Mana & Burn.
5. **Kit do Mana & Burn.** GitHub tem a v1; a skill usa a v2 do projeto claude.ai. Pendente subir a v2.
6. **Voz do TUBO.** `comum/historico.md` regista "Antonio de Jesus"; `oraculo/CONTEXTO.md` §3 diz "a escolher". Pendente confirmar.
7. **Arranque.** As instruções do projeto só conhecem `manaburn` e `conde`; o `CLAUDE.md` acrescenta `tubo`.
8. **Fecho do scanner ausente do repositório (bloqueador).** `.gitignore` ignora `*.mp4`, por isso `comum/outro/outro_binder_916.mp4` nunca subiu; só os 45 quadros de `comum/outro/scan/` estão no GitHub. Adicionada a exceção `!comum/outro/*.mp4` ao `.gitignore`. Falta o Ibisson enviar o ficheiro para ele ser commitado. Até lá, quem clona o kit não consegue cumprir a regra do fecho.
9. **"Dois prompts operacionais anteriores"** (auditoria / produção autónoma) não estão no repositório nem nos documentos do projeto; as regras deles que já estavam nas instruções foram absorvidas aqui.

Testes de coerência (28/10/2026), sem produzir vídeos:
- A · TUBO analisa jogada real → `oraculo/PERFIL.md` (reconstrução, VOD com minuto, Oracle, alternativas) + bloqueador "imagem de transmissão". OK.
- B · Mana & Burn sobre tendência recente → perfil (investigação aprofundada, 2 fontes, data da semana) + constituição §4 (datas). OK.
- C · Conde comenta uma obra → `conde/PERFIL.md` (observação / interpretação / facto separados). OK.
- D · Série nova → `modelos/PERFIL_SERIE.md` + linha na tabela §2; constituição intacta. OK.
- E · Fonte, ferramenta ou autorização indisponível → constituição §11. OK; o próprio teste revelou o bloqueador 8.
