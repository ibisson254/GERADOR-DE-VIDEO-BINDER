# INVENTARIO · Fase 0 da Operação de Consolidação do Estúdio BINDER

31/10/2026 · só leitura · branch `consolidacao-estudio` (criada a partir de `main` 50cb4f8)

Nenhum ficheiro existente foi alterado, movido ou apagado. Esta fase só acrescenta este inventário e o `STATUS.md`.

Ponto de partida: a auditoria de 30/10 (`claude/comum/BINDER_INTELLIGENT_PUBLISHER_AUDIT.md`, no Project) já cobriu infraestrutura, custos, Supabase e n8n. Aqui só se repete o que importa para o estúdio e regista-se o que mudou desde então.

---

## 1. O que foi inspecionado

| Origem | Acesso | O que foi aberto |
|---|---|---|
| GitHub `ibisson254/gerador-de-video-binder` | Sim | `main` e `especial/sir-patrick` (histórico de 200 commits), árvore completa, docs da raiz, `comum/`, perfis, `CONTEXTO.md` (secções de som), imports de todos os `.py` |
| Claude Project "Binder Marketing" | Sim | Lista dos 81 docs, instruções do Project, `claude/gerador-manaburn/LEIA-ME.md`, `index.html`, `process.py`, `claude/00-motor-de-arranque.md`, auditoria de 30/10 |
| Google Drive | Sim | Pasta "BINDER Marketing — Instagram" e subpastas (listadas); doc da série Mana & Burn (lido) |
| Skills | Sim | `binder-mana-burn-episodio`, `binder-motor-de-arranque`, `binder-posts-instagram` (SKILL.md lidos) |
| Computador do Ibisson | **Não** | O computador não estava ligado à bridge nesta sessão |
| `ManaBurn_kit.zip` (Drive, 12 MB, 24/10 15:59) | **Não aberto** | O conector só o entrega em base64 dentro da conversa (~16 MB de texto). Precisa de ser anexado ou de o computador estar ligado |

Não inspecionado: ElevenLabs (vozes e flows), restantes docs do Project um a um, documento mestre do Drive (já auditado a 30/10).

---

## 2. Repositório GitHub

### 2.1 Branches

| Branch | Último commit | Conteúdo exclusivo |
|---|---|---|
| `main` | 50cb4f8 · 31/10 00:02 · Especial de Halloween 2026 | `especiais/halloween_2026/` (11 ficheiros), linhas do Halloween em `historico.md` e `easter_eggs.md` |
| `especial/sir-patrick` | 1a7f40b · 29/10 23:56 | Constituição **v1.1 (§14 especiais e homenagens)**, 3 entradas em `DECISOES.md`, item no checklist, `manaburn/episodios/esp01_sir_patrick/` (v1, não publicável), `esp02_picard_v2/`, `manaburn/musica/beyond_the_last_horizon.mp3` |

Base comum: 49d1b84. As duas branches divergiram e **nenhuma tem as duas coisas**. A regra §14 (que o Ibisson deu a 29/10) não está em `main`.

### 2.2 Estrutura atual (main)

```
CLAUDE.md, AGENTS.md (aponta para CLAUDE.md), README.md, .gitignore
comum/      originals/ (constituição v1.0, DECISOES, CHECKLIST, modelos/), outro/ (LEIA-ME + scan/ 45 quadros),
            historico.md, easter_eggs.md
manaburn/   PERFIL, LEIA-ME (v1), motor v1 (index.html, process.py, render.py, preview.py, sfx.py, generate_voices.py),
            episodios/ep08_tabernacle, ep09_dack, extras/ep1, ep2, cards/, musica/, logo/, node_modules/ (4 fontes)
oraculo/    (Meta em Curto · TUBO) PERFIL, CONTEXTO v6, editar_tema.py, assets/, musica/, ep02/cartas/, episodios/ (ep01, ep02)
conde/      PERFIL, CONTEXTO, montar_ep002.py, montar_ep003.py, encurtar_narracao*.py, assets/, ep003/, episodios/, legendas/, musica/
especiais/  halloween_2026/ (crossover das três séries)
```

191 ficheiros, 49 MB. Nenhum segredo encontrado.

### 2.3 Problemas encontrados

| # | Problema | Evidência | Gravidade |
|---|---|---|---|
| R1 | Fecho do scanner `comum/outro/outro_binder_916.mp4` ausente em todas as branches | `git ls-tree`; `CLAUDE.md` e constituição §6 exigem-no | **Bloqueador** (já registado em `DECISOES.md` item 8) |
| R2 | Motor do Mana & Burn no repositório é a v1; Ep. 09 não é reprodutível | `manaburn/episodios/ep09_dack/process.py` importa `trilha`, `roteiro`, `cortes`, que não existem no repositório | **Bloqueador** |
| R3 | `oraculo/episodios/ep01_render_v2.py` importa `render`, inexistente em `oraculo/` | análise de imports | Provável script partido |
| R4 | `manaburn/generate_voices.py` usa `edge_tts` (Microsoft), não ElevenLabs | import | Resto da v1, não usado |
| R5 | Caminho absoluto `BASE = "/home/claude/conde"` | `conde/montar_ep002.py:9` | Médio |
| R6 | 9 pares de ficheiros duplicados (md5 igual): cópias do Ep. 09 na raiz de `manaburn/` (`episode.*`, `legenda.txt`, `comentario_fixado.txt`, `ficha_fontes.md`), `musica.mp3` = `musica/musica.mp3`, vozes do Ep. 2 em dois sítios, `cards/tabernacle.png` = `ep08/cards/main.png` | `md5sum` | Baixo (confusão) |
| R7 | A trilha `concrete_teeth.mp3` (Ep. 5–7, segundo o kit v2) não está no repositório; `musica_manaburn.mpeg` (152,6 s) não é citada em nenhum doc nem script. O Ep. 09 não define `music`, logo usa a faixa padrão do `trilha.py` v2 (midnight_throttle) | `git ls-files`, `ffprobe`, `ep09_dack/episode.json` | Médio (não bloqueia o episódio de referência) |
| R8 | Pasta `oraculo/autorizacoes/` citada em `DECISOES.md` não existe | `ls` | Baixo (só necessária quando houver autorização) |

---

## 3. Claude Project

| Item | Estado |
|---|---|
| **Campo "instruções" do Project** | Contém o rascunho do comentário fixado do TUBO ("O resultado da final é conhecido…"), não instruções. A constituição §1 põe estas instruções no topo da hierarquia. **Bloqueador de governação** (já assinalado a 30/10, continua igual) |
| Descrição do Project | "Master prompt para Claude Designer" (Reels de aquisição 20–25 s, demonstração do app). Não menciona as séries Originals nem o repositório |
| `claude/gerador-manaburn/` | **Motor v2 do Mana & Burn** (24–25/10): `index.html` com zapping, `encaixa()` contra corte lateral, bloco do scanner, pôster; `process.py` com `trilha`, `roteiro`, `cortes`, respiro, ducking em dB; mais `sfx.py`, `trilha.py`, `cortes.py`, `roteiro.py`, `foneticos.json`, `escolher_tomadas.py`, `tomadas.json`, `scryfall.py`, `lote.py`, `montar.py`, `testes.py`, `formatos.py/.js`, `copys.py`, `bordas.py`, `extrair_fecho.py`, episódios 1, 2, 5, 6, 7 e zapping 01 |
| `claude/gerador/` | Gerador da série Órbita (Star Trek, 4:5): build, batch, captions, anim.js, paint.js |
| `claude/oraculo/`, `claude/conde-manaforte/`, `claude/comum/historico.md` | Versões **anteriores** às do repositório (CONTEXTO do TUBO de 27/10; histórico de 26/10) |
| Outros | `00-motor-de-arranque.md` e `00-comece-aqui.md` (funções confirmadas do app, 19/10), `agente-binder-posts-instagram.md`, `contexto-binder-instagram.md`, `serie-star-trek-bauhaus.md`, `reel-lambe-lambe-pop.md` |

### Versão funcional do motor do Mana & Burn

Há três versões e nenhuma está completa num só sítio:

| Versão | Onde | Data | Notas |
|---|---|---|---|
| v1 | GitHub `manaburn/` | 24/10 | 131 linhas no `process.py`, sem módulos; reproduz Ep. 1–4 |
| v2 | Project `claude/gerador-manaburn/` | 24–25/10 | A mais completa; usada nos Ep. 5–7 e no 09 ("kit v2 do projeto + assets do repositório", `historico.md`) |
| v2.1 (só `process.py`) | GitHub `manaburn/episodios/ep09_dack/` | 29/10 | Acrescenta `respiro_fala` à v2; precisa dos módulos que só estão no Project |
| ZIP | Drive `ManaBurn_kit.zip` | 24/10 15:59 | Não aberto. Pela data, anterior às atualizações de 24/10 22:42 e 25/10 do Project |

**Conclusão provisória:** a versão funcional é a v2 do Project + o `process.py` do Ep. 09 + os assets do GitHub. Confirmar na Fase 2 reproduzindo o Ep. 09.

---

## 4. Google Drive

```
BINDER Marketing — Instagram/
├── 00 · Motor de arranque · BINDER Instagram (24/10)
├── BINDER Marketing — Instagram · 23/10/2026 (documento mestre, última edição 24/10)
├── 00 · Pacote para outra IA/ (25/10): LEIA PRIMEIRO, PROMPT MESTRE, 02 produto, 03 Instagram, 04 regras, 05 Mana & Burn + kit, 06 mapa do Drive
├── 01 · Série Mana & Burn/: doc da série (editado 29/10), "arquivos e como gerar", roteiros Ep. 5–7, ManaBurn_kit.zip
├── 02 · Série Órbita · Star Trek/: índice, Reel 22
├── 03 · Lambe-lambe, Scanner e Na prática/: índice
├── 04 · Radar de pautas/: Radar de pautas (24/10)
└── 06 · Série Meta em Curto (TUBO)/: EP02 ficha, EP02 legenda e comentário (29/10)
```

- **Não há pasta do Conde de Manaforte** (nem 05). O prompt da operação prevê uma pasta por série.
- O doc da série Mana & Burn é o único doc do Drive atualizado depois de 25/10 (entradas do Ep. 09 e do especial Sir Patrick). Continua a ser a "autoridade" de identidade do Mana & Burn segundo `manaburn/PERFIL.md` e a constituição §2.
- O documento mestre e o motor de arranque do Drive estão parados em 24/10 e não conhecem o TUBO, o Conde, a constituição nem o repositório.

---

## 5. Skills

| Skill | Aponta para | Divergências |
|---|---|---|
| `binder-motor-de-arranque` | Drive (motor, mestre, radar) e Project (`claude/…`) | Não conhece o repositório, `CLAUDE.md`, TUBO nem Conde; diz que "o Scryfall não abre" (o EP02 do TUBO e a auditoria de 30/10 acederam à API); séries listadas: Mana & Burn, Órbita, Lambe-lambe |
| `binder-mana-burn-episodio` | Doc da série no Drive e `claude/gerador-manaburn/` (Project) | Manda pedir o ZIP; Scryfall "não abre"; não menciona o fecho `comum/outro/` |
| `binder-posts-instagram` | Drive (mestre manda) | Regras de pacote coincidem com o núcleo; formatos citados incluem Órbita 4:5 |

Não existem skills para TUBO nem Conde (previsto para a Fase 3).

---

## 6. Identidade sonora recuperada (ponto de partida para os `sonoro.md`)

| Série | Voz | Música | Efeitos e mistura | Lacunas |
|---|---|---|---|---|
| Mana & Burn | ElevenLabs `eleven_v4`. Burn: "Talis - Natural, Descontraído, Real". Mana: "Erik - Calmo e Introspectivo". Uma faixa por personagem com `[long pause]`; Burn ×1,06, Mana ×1,12, respiro 0,14 s; `foneticos.json` (Project) | Rock cru estilo Motörhead com riff próprio. "midnight_throttle" (Ep. 1–2, Gemini, Ibisson) = `musica.mp3` 180,6 s; "concrete_teeth" (Ep. 5+), **ausente do repo**. Parada seca no "Comenta aí" | `sfx.py` v2: estática nos cortes para a TV, marca-texto, estalo de carta, impacto na raiva, zapping; ducking intro 0 / falas −14 / pausas −6 / fecho 0 dB (40 ms/300 ms); −14 LUFS, TP −1 | voice_id de Talis e Erik não registados; licença comercial das vozes por confirmar por episódio; `musica_manaburn.mpeg` sem descrição |
| Meta em Curto (TUBO) | "Antonio de Jesus" `MK5tXPmT83J5SUlpUo4K`, `eleven_v4`, atempo 1,10. Voz = LED a acender com a amplitude | "Paper Thin Alibi" (Ibisson): `tubo_tema.mp3` 40,7 s editado de `tubo_tema_original.mp3` 62,4 s por `editar_tema.py` (2 cortes, EQ, −16 LUFS) | "Tum" de desmagnetização de CRT + chiado de modem; Erro de sistema; mix −14 LUFS | O prompt fala em "jazz estilo Whiplash" e o `CONTEXTO.md` em "jazz de precisão": coerentes, só confirmar a redação |
| Conde de Manaforte | Voz desenhada "Conde de Manaforte" `bbnQVGWT7UMdmoK4URLr`, `eleven_v4`; pausas 0,24/0,55–0,6/0,40–0,45 s; atempo 1,08 (`encurtar_narracao.py`) | "Verdict in Varnish and Vellum" (ElevenLabs Music, 25/10), 30 s, ~136 BPM; `conde/musica/tema.mp3` mede **44,2 s** | Sidechain (threshold 0,025, ratio 5); sting no carimbo "Parecer emitido"; −14 LUFS | Duração do ficheiro (44,2 s) ≠ descrita (30 s); licença comercial da voz pendente (`historico.md`) |
| Comum | — | Faixa "Beyond the Last Horizon" (Ibisson) só na branch `especial/sir-patrick`; licença pendente (auditoria 30/10) | Fecho do scanner: música sobe, sem narração, fade final | Som do fecho não documentado à parte |

---

## 7. Mapa de divergências

| # | Tema | Fonte A | Fonte B | Proposta |
|---|---|---|---|---|
| D1 | Constituição | `main`: v1.0 | `especial/sir-patrick`: v1.1 (§14) | Trazer a §14 para a consolidação (é regra do Ibisson) |
| D2 | Motor M&B | GitHub v1 | Project v2 (+ v2.1 no Ep. 09) | Subir a v2 ao repositório na Fase 2 como `motor/` |
| D3 | Fonte de verdade | Constituição §1: instruções do Project no topo | Skills e Drive: "vale o documento mestre do Drive" | Prompt da operação: GitHub manda; Project, Drive e skills apontam para ele |
| D4 | Instruções do Project | Deviam ser instruções | Contêm um rascunho de comentário | Repor na Fase 3 (texto curto que manda ler `AGENTS.md`) |
| D5 | Fotos de jogadores no TUBO | Prompt da operação §4: "foto do jogador quando possível" | `DECISOES.md` 29/10: silhueta, sem fotos (direitos), salvo autorização em `oraculo/autorizacoes/` | Prevalece a bíblia (regra do próprio prompt): silhueta. Ver pergunta P3 |
| D6 | Scryfall | Skills: "não abre nas sessões" | EP02 e auditoria 30/10: API acessível | Corrigir as skills na Fase 3 |
| D7 | Pasta do TUBO | `oraculo/` (nome antigo) | Série "Meta em Curto", palavra `tubo` | Ver proposta de estrutura |
| D8 | Histórico | Repo `comum/historico.md` (até 31/10) | Project `claude/comum/historico.md` (26/10) | Repositório manda; o do Project passa a apontar |
| D9 | Séries no Drive | Prompt: pasta por série | Sem pasta do Conde | Criar na Fase 3 com `LEIA-ME` (precisa de autorização para escrever no Drive) |
| D10 | Território M&B × TUBO | Prompt: polémicas → M&B; torneio → TUBO | `DECISOES.md` 28/10 item 4: decisão e meta → TUBO; reação/polémica de torneio → M&B | Coincidem; documentar no `router.md` com este exemplo |
| D11 | Formato Órbita/Lambe-lambe | Drive e Project: 4:5 e 1080×1350 | Prompt: séries ativas M&B, Conde, TUBO, posts | Ver pergunta P2 (registar como arquivadas?) |
| D12 | Duração do tema do Conde | `CONTEXTO.md`: 30 s | Ficheiro: 44,2 s | Confirmar na Fase 2 |

---

## 8. Proposta de estrutura de diretórios

Princípio: **mudar o mínimo de caminhos** nesta operação. Os scripts dos episódios publicados usam caminhos relativos às pastas atuais, e mover `oraculo/` ou `conde/` parte esses scripts. Por isso a proposta mantém as pastas das séries no lugar e acrescenta as camadas que faltam.

```
/
├── AGENTS.md            ← ponto de entrada neutro (reescrito: ordem de leitura, segurança, retoma)
├── CLAUDE.md            ← passa a só remeter para AGENTS.md
├── STATUS.md            ← estado da operação e de cada série
├── INVENTARIO.md        ← este ficheiro
├── series.yaml          ← registo: slug, palavra de arranque, pasta, vozes, trilha, referência, estado
├── nucleo/
│   ├── README.md        ← índice do núcleo
│   ├── constituicao.md  ← movida de comum/originals/ (v1.1 com §14)
│   ├── decisoes.md, checklist.md, modelos/
│   ├── router.md, showrunner.md, easter_eggs.md (movido)
│   └── fecho/           ← comum/outro/ (LEIA-ME, scan/, outro_binder_916.mp4)
├── motor/               ← motor v2 do Mana & Burn (vindo do Project) + qc.py; recebe a configuração de series.yaml
├── series/
│   ├── manaburn/  → hoje manaburn/   (bíblia, visual, sonoro, roteiro-modelo, referencia/, historico + episodios/)
│   ├── tubo/      → hoje oraculo/
│   ├── conde/     → hoje conde/
│   └── posts/     ← novo (posts estáticos e carrosséis)
├── especiais/           ← fica (crossovers que não pertencem a uma série)
└── comum/historico.md   ← fica como registo de desempenho (ou nucleo/historico.md)
```

**Duas opções para as pastas das séries** (é a decisão principal desta fase):

- **Opção A · mover agora** (`git mv manaburn series/manaburn` etc.), corrigindo os caminhos dos scripts e testando cada episódio de referência na Fase 2. Fica limpo, mas mexe em todos os scripts.
- **Opção B · manter `manaburn/`, `oraculo/`, `conde/` na raiz** e criar dentro de cada uma os ficheiros novos (`biblia.md`, `visual.md`, `sonoro.md`…); `series.yaml` liga o slug `tubo` à pasta `oraculo/`. Não parte nada; a estrutura `series/` fica só no registo. **Recomendada**: cumpre o objetivo do prompt (agente lê núcleo + bíblia da série) sem risco para episódios publicados.

Em ambas, `comum/originals/` passa para `nucleo/` com um `LEIA-ME` no lugar antigo durante uma transição, e os `CONTEXTO.md`/`PERFIL.md` não são reescritos: a `biblia.md` de cada série nasce deles e eles ficam como fonte até a Fase 2 de cada série terminar.

### Séries a registar em `series.yaml`

| Slug | Nome | Palavra | Pasta | Formato | Estado proposto | Episódio de referência proposto |
|---|---|---|---|---|---|---|
| manaburn | Mana & Burn | `manaburn` | `manaburn/` | Reel 9:16 | ativa | Ep. 09 Dack Fayden (único com ficha e QC no repo) |
| tubo | Meta em Curto (TUBO) | `tubo` / `meta` | `oraculo/` | Reel 9:16 + carrossel | ativa | EP02 Hartford (último com QC) |
| conde | Conde de Manaforte | `conde` | `conde/` | Reel 9:16 | ativa | Ep. 003 Voldaren Pariah |
| posts | Posts estáticos e carrosséis | `post` | `posts/` (novo) | 1080×1350 | em desenvolvimento | — |
| orbita | Órbita · Star Trek | — | só Project/Drive | Reel 4:5 | arquivada? (P2) | — |

---

## 9. Bloqueios e decisões pendentes

**Bloqueios (precisam de ação do Ibisson):**

1. `outro_binder_916.mp4`: enviar o ficheiro ou ligar o computador para o trazer.
2. `ManaBurn_kit.zip`: anexar à conversa (ou ligar o computador) para comparar com o Project. Sem ele, a Fase 2 usa a v2 do Project.
3. `concrete_teeth.mp3`: enviar a faixa ou indicar onde está (só para reproduzir os Ep. 5–7; não trava o Ep. 09).
4. Autorização para escrever no Drive (pasta do Conde, `LEIA-ME` por série) e para alterar as instruções do Project (Fase 3).

**Perguntas (a resposta muda a Fase 1):**

- **P1.** Estrutura: Opção B (recomendada, pastas no lugar) ou Opção A (mover para `series/`)?
- **P2.** Órbita e Lambe-lambe ficam registadas como arquivadas, ou fora do estúdio?
- **P3.** TUBO: mantém-se a regra de 29/10 (silhueta, foto só com autorização), certo? O prompt diz "foto quando possível".
- **P4.** A branch `especial/sir-patrick` (§14, Picard v2) entra na consolidação? Proposta: sim, por merge para `consolidacao-estudio` na Fase 1, sem tocar em `main`.
