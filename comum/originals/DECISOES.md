# Registo de decisões · BINDER Originals

Uma entrada por alteração de regra: data · o quê · porquê · impacto. Mais recente no topo.

## 29/10/2026 · Especiais e homenagens (constituição v1.1, secção 14)

**O quê:** nova secção 14 na constituição e um item no checklist (A). Especiais, homenagens e acontecimentos extraordinários podem existir em qualquer série, sem limite rígido de duração; homenagens priorizam celebração, admiração, legado, inspiração, personalidade e reconhecimento, com humor subtil quando adequado; velocidade editorial nunca à custa de rigor, identidade da marca ou qualidade narrativa.
**Porquê:** regra enviada pelo Ibisson a 29/10/2026, depois do especial de Sir Patrick Stewart.
**Impacto:** a exceção de duração registada para o especial de Sir Patrick (entrada abaixo, ponto 4) passa a estar coberta pela regra geral. O especial entregue a 29/10 tem tom contido e melancólico (noite, piano lento, sem humor), pedido no brief original; não segue a nova orientação de celebração até ser refeito.

## 29/10/2026 · Mana & Burn · especial de homenagem (Sir Patrick Stewart): exceções pontuais

**O quê:** o especial `manaburn/episodios/esp01_sir_patrick/` não segue quatro regras da série e da constituição: (1) sem fecho do scanner (`outro_binder_916.mp4`); o vídeo termina no ponto verde e na assinatura "BINDER Originals", sem "Disponível no Google Play"; (2) legenda sem "baixe o BINDER Vision" nem CTA do app; (3) comentário fixado sem "Tem um detalhe escondido. Diga o segundo." e sem easter egg; (4) formato fora do perfil: 54,8 s, locução contínua do Mana + uma fala do Burn, em vez de 14 falas em bate-volta e 35–45 s.
**Porquê:** pedido explícito do Ibisson no brief do especial (nível 1 da hierarquia, §1): homenagem sem promoção do app, sem humor e sem parecer exploração comercial do luto.
**Impacto:** só este episódio. As regras voltam a valer no episódio seguinte. Cena própria (`homenagem.html`) feita com os desenhos do `manaburn/index.html` sem alterá-lo; trilha original sintetizada (`musica.py`) em vez da trilha rock da série.

## 29/10/2026 · Meta em Curto EP02 e regra de evidência visual

**O quê:** `oraculo/CONTEXTO.md` passa a v6 com a secção 6.4: deck citado → lista completa no ecrã; carta citada → imagem oficial do Scryfall; jogador citado → ficha de jogador com silhueta, sem fotos. Novo modo «Leitura da Final» para quando não há VOD analisável. Estreia do Erro de sistema.
**Porquê:** pedido do Ibisson (29/10/2026): quem vê deve poder conferir a lista, a carta e quem é o jogador. Fotos de jogadores ficam de fora por direitos de imagem e de autor (cobertura SCG/WotC); só entram com autorização registada em `oraculo/autorizacoes/`.
**Impacto:** episódios do TUBO ficam mais longos de produzir (listas e cartas), mas reutilizam `ep02_render.py`. A lista também sai no comentário fixado e no carrossel.

## 29/10/2026 · Análise do Meta em Curto EP01 (render final)

**O quê:** ficha com controlo de qualidade (`oraculo/episodios/ep01_ac13_ficha.md`); `oraculo/CONTEXTO.md` passa a v5 (voz definida, silêncio alinhado à revelação, elementos fixados no EP01, pendentes atualizados); duração do perfil conta sem o fecho.
**Porquê:** o EP01 resolveu decisões que o `CONTEXTO.md` ainda dava como pendentes.
**Impacto:** a divergência 6 (voz do TUBO) da entrada de 28/10 fica resolvida: "Antonio de Jesus". Sem defeitos bloqueadores no EP01; 2 melhorias para o EP02 (tamanho das fontes no ecrã, −14 LUFS).

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
