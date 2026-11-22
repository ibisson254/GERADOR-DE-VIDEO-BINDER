# Ficha · Mana & Burn · EP16 · «O comandante que dá carta e bate no sorteio» (Alexander, Ship's Fool)

Estado: **EM PRODUÇÃO · prévia sem voz** (21/11/2026). Roteiro e vozes por aprovar. Zero créditos gastos.
Origem: tema aprovado pelo fundador a 21/11/2026 (conversa com o ChatGPT, entregue a esta sessão em anexo), primeira aplicação do método comparativo (`manaburn/PERFIL.md`).

## 1. Identificação e classificação

| Campo | Valor |
|---|---|
| ID | MB-EP16 |
| Frente | Mana & Burn (série) |
| Classe | Carta polémica / leitura de regra (verificação rápida: Oracle + ruling + EDHREC com data) |
| Formato | episódio base, 14 falas, Commander |
| Objeto | Alexander, Ship's Fool (Star Trek Commander, TRC nº 81, 13/11/2026) |
| Público | jogador casual e de Commander no Brasil |

## 2. Tese e objetivo

**Tese:** o Alexander parece *group hug* (todo mundo compra), mas a carta revelada é a carta comprada: a mesa inteira fica a saber o que cada um tem, o dano cai num oponente ao acaso e, com Rule of Law, cada jogador só gasta uma mágica por turno. A habilidade dele não é mágica, então com efeitos de desvirar ele repete.
**Objetivo:** respostas à pergunta A/B (métrica da série); secundária: partilhas.

## 3. Auditoria de originalidade

- `python3 comum/ferramentas/memoria.py pauta --objeto "Alexander, Ship's Fool" --tema "Commander: compra coletiva, dano aleatório e pressão psicológica"` → **PAUTA LIVRE** (21/11/2026).
- Comparação manual: MB-EP11 (Numot, terreno), MB-EP13 (Sanar, 97 terrenos), MB-EP15 (Felidar, 40 de vida): outro objeto, outra mecânica, outra tese. Star Trek já apareceu no MB-EP10 (Kirk, autógrafo) e no Órbita (contemplação): ângulo diferente (regras de mesa, não coleção nem arte).

## 4. Análise comparativa de desempenho (método de 21/11/2026)

Fonte: prints do perfil @binder_vision enviados pelo fundador (21/11/2026, 16:41), aba Reels. Só visualizações; sem alcance, retenção, guardados nem estado de impulso.

| Post | Views | Impulso | Observação |
|---|---|---|---|
| MB-EP13 · Sanar, «97 terrenos, ganha no turno 5» | 16,6 mil | A CONFIRMAR | o mais visto do perfil |
| MB-EP11 · Numot, «o dragão que come terreno» | 9.664 | SIM (57 % pago a 13/11) | não comparável com orgânico |
| MB-EP15 · Felidar, «começa com 40» | 1.911 | A CONFIRMAR | mais recente: idade menor |
| MB-EP12 (Instagram) · Olag and Miau, «gato zumbi que cobra vida» | 584 | A CONFIRMAR | ver nota de ID abaixo |
| MB-EP10 · Kirk, «assinado no pré-release? zero» | 873 | A CONFIRMAR | coleção, não regra |

- **Facto observado:** os dois MB mais vistos (EP13 e EP11) são Commander, abrem com um comandante lendário em tela cheia e têm um número paradoxal no gancho («97 terrenos / turno 5», «−2 por pancada»). Os de regra de mesa (EP11, EP13, EP15) estão todos acima dos de coleção (EP10).
- **Interpretação:** o que distingue os dois de topo é a sensação «isso não pode funcionar» resolvida pela leitura da carta.
- **Hipótese testável:** um comandante novo cuja habilidade parece ajudar a mesa e na verdade a ameaça, com um número no gancho, segura o público de Commander como o EP13. Teste: MB-EP16 **sem impulso**, comparado com o EP15 às 48 h e aos 7 dias.
- **Limites:** idades diferentes, impulso por confirmar em quase todos; não se tira causalidade de visualizações.
- **Nota de ID (para o fundador):** no Instagram, a capa «MANA & BURN · EP. 12» é o Olag and Miau; no registo, MB-EP12 é «MONEY BURN» (não publicado). Os IDs não se reutilizam: falta decidir como registar o Olag.

## 5. Ângulos (tema dado pelo fundador: 2+ ângulos, SHOWRUNNER §2.4)

| Ângulo | Impacto | Origin. | Compr. | Visual | Partilha | Recomp. | Adequação | Total |
|---|---|---|---|---|---|---|---|---|
| A · «dá carta e bate no sorteio» (só a habilidade) | 4 | 4 | 5 | 4 | 3 | 3 | 4 | 27 |
| B · **«a mesa vê o que você comprou» + Rule of Law** — VENCEDOR | 5 | 5 | 4 | 4 | 4 | 5 | 5 | 32 |
| C · «desvirar para multiplicar o caos» (combos) | 4 | 3 | 3 | 3 | 3 | 4 | 3 | 23 |

B supera os outros porque a reviravolta vem de uma ruling oficial (revelada = comprada), dá quatro leituras reais ao Mana e acaba numa escolha de mesa. Reserva: C (combos de desvirar com Commander Spellbook), noutro episódio.

## 6. Fontes e evidências

| Facto no ecrã | Fonte (consultada a 21/11/2026) |
|---|---|
| Habilidade do Alexander (vigilância, ímpeto; {T}: cada jogador revela o topo e compra; X = maior valor de mana revelado; dano num oponente aleatório) | Oracle, Scryfall trc/81 |
| «Exceto em casos muito raros, a carta que cada jogador revela é a que vai comprar» | Ruling oficial de 07/10/2026, Scryfall |
| Rule of Law: «Each player can't cast more than one spell each turn.» | Oracle, Scryfall m20/35 |
| Rule of Law em listas de Alexander | EDHREC, Alexander, filtro «expensive» (9 decks) |
| Efeitos de desvirar nas listas | EDHREC, Alexander: tag Tap/Untap (5 de 244 decks); Thousand-Year Elixir em Utility Artifacts |
| Thousand-Year Elixir: «{1}, {T}: Untap target creature.» | Oracle, Scryfall c21/271 |
| Swords to Plowshares (exemplo de remoção revelada) | Oracle, Scryfall trc/429 |
| Mesa de 4 = 4 compram; dano num de 3 oponentes (2 em 3 não é você) | aritmética sobre o Oracle; marcado «exemplo de mesa de 4» |

**Correções ao briefing do ChatGPT (aplicadas no roteiro):**
1. A publicação do Reddit de 17/11 citada como fonte da «estratégia psicológica» **não abriu nesta sessão** (Reddit fora do alcance; a pesquisa na web não a encontrou). Sai do vídeo: nada se atribui a «o construtor». A pressão passa a apoiar-se só na ruling oficial (a mesa vê a carta comprada), que é facto, e a leitura de «ameaça» é opinião do Burn.
2. «O construtor enche a estratégia de remoções» e «Solphim na lista»: não verificados; fora do roteiro.
3. «A carta revelada normalmente é a que você acabou de comprar» → é revelada **antes** e é a que se vai comprar (ruling).
4. Selo da capa: **ALEATÓRIO**, não «1 ALVO» (a habilidade não escolhe alvo). O selo da abertura passa a «4 COMPRAM» para o gancho ter número (perfil: dor da mesa + número).
5. Legenda: a frase final obrigatória e a de 21/11 do ChatGPT convergem em «baixe o BINDER Vision».

## 7. Cartas e imagens (todas reais, PNG do Scryfall em `cards/src/`)

Alexander, Ship's Fool (TRC 81, arte Javier Charro) · Rule of Law (M20 35, arte Scott M. Fischer) · Thousand-Year Elixir (C21 271, arte Richard Sardinha) · Swords to Plowshares (TRC 429, arte Pablo Mendoza). Telas e inserts: `telas_alexander.py` (15 PNG em `cards/`).

## 8. Gancho visual (7 campos)

| Campo | Decisão |
|---|---|
| Quadro 0 | Alexander em tela cheia, linha «reveals the top card… then draws» destacada |
| Objeto | carta oficial (Scryfall) |
| Ação | entra com impacto 0,18 s e voa para a TV quando o Burn diz «QUATRO» (`ate` 0,52 ≈ 2,2 s) |
| Som | pancada + pop da biblioteca da série |
| Descoberta | todos compram; um oponente apanha ao acaso |
| Promessa | porque é que carta grátis pode ser perigosa |
| Pagamento | ruling (a mesa vê) + Rule of Law + habilidade que não é mágica |

Selo da abertura: **4 COMPRAM**. Rubrica do gancho: impacto 4, clareza 5, número 4.

## 9. Roteiro proposto (14 falas; *asteriscos* = amarelo na legenda)

01 · BURN — Esse comandante dá carta pra *QUATRO*. E *um* oponente apanha no sorteio!
02 · MANA — *Lê a carta.* Ele vira, e *cada jogador* revela o topo e *compra*.
03 · BURN — Carta de graça pra mesa toda? Isso é deck ou *instituição de caridade*?!
04 · MANA — O *maior custo* revelado vira *dano*. Num oponente *aleatório*.
05 · BURN — Eu ganho carta *e* posso nem apanhar? Tô *dentro*!
06 · MANA — *Lê a ruling.* A carta que você revela é *a que você compra*. A mesa *viu*.
07 · BURN — E daí? Eu comprei uma *remoção*!
08 · MANA — E todo mundo sabe. *Inclusive* o dono do Alexander.
09 · BURN — Então eu jogo ela *agora*!
10 · MANA — Tem lista com *Rule of Law*: cada jogador só conjura *uma mágica* por turno.
11 · BURN — *UMA?!* Ou eu tiro o Alexander, ou faço a *minha* jogada?!
12 · MANA — E a habilidade *não* é mágica. Com algo que *desvira*, ele revela e bate *de novo*.
13 · BURN — Isso não é group hug, é *ameaça com brinde*! *A*: encaro. *B*: troco de deck.
14 · MANA — Comenta aí.

Leituras reais do Mana: Oracle (02, 04), ruling (06), Rule of Law (10), Thousand-Year Elixir + regra «habilidade ativada não é mágica» (12). Pronúncias no `episode.json` (`tts`): Aléxander, Rúl óf Ló, grup râg.

## 10. Storyboard (tempos da prévia sem voz; refazer com as vozes)

| Tempo | Fala | Plano | Imagem |
|---|---|---|---|
| 0,00–2,2 s | 01 | abertura | Alexander em tela cheia, selo 4 COMPRAM |
| 2,2–3,9 | 01 | TV | «4 COMPRAM» → carimbo «1 APANHA» |
| 3,9–7,3 | 02 | tvtext | Oracle destacado → «+1 PRA CADA» |
| 7,3–10,8 | 03 | cuB | insert «4 × +1 · GROUP HUG?» |
| 10,8–14,1 | 04 | tvtext | linhas do dano → «MAIOR CUSTO = DANO / ALVO? SORTEIO» |
| 14,1–16,7 | 05 | cuB | insert «2 EM 3» → «TÔ DENTRO!» |
| 16,7–20,5 | 06 | tvtext | ruling destacada → «A MESA VIU» |
| 20,5–22,4 | 07 | cuB | Swords to Plowshares, «REVELADA = COMPRADA» |
| 22,5–25,3 | 08 | TV | mesa: todos viram a sua carta |
| 25,3–27,0 | 09 | cuB | «AGORA!» |
| 27,1–31,0 | 10 | tvtext | Rule of Law destacada → «1 POR TURNO» |
| 31,0–33,9 | 11 | cuB | «TIRO O ALEXANDER ou FAÇO A MINHA JOGADA» |
| 33,9–38,2 | 12 | tvtext | Elixir destacado → «HABILIDADE ≠ MÁGICA» |
| 38,2–41,8 | 13 | cuB | A/B |
| 42,2–48,2 | 14 | cuM | «Comenta aí», TV desliga (43,4 s), fim |

Retrato do Conde com uma expressão por fala; `check_quadro.py`: todas as trocas caem num corte.

## 11. TV SAL

Medidor «COMPRAM 4» (mesa de 4, 1 por jogador, Oracle TRC 81). Tabela na fala 12: «1 mágica por turno, por jogador». Manchetes: piadas sem pessoas reais. Relógio 20:44 (easter egg: mesa de 4, 4 compram).

## 12. Capa

`capas/capa_mb.py`: Alexander em largura total, frase DÁ CARTA PRA TODOS, foco ARMADILHA, selo ALEATÓRIO, faixa MANA & BURN · EP. 16, COMMANDER. Recorte 3:4 conferido em `MB_EP16_CAPA_grelha.png`.

## 13. Pacote editorial

`legenda.txt`, `comentario_fixado.txt`, `texto_alternativo.txt`, `fontes.md`. UTM sugerida para o link: `utm_campaign=MB-EP16`.

## 14. Métrica e avaliação

Métrica principal: respostas A/B no comentário fixado. Avaliar às 48 h e aos 7 dias contra o MB-EP15 (mesmo formato e duração, ambos sem impulso se o fundador confirmar).

## 15. Controlo de qualidade (prévia sem voz, 21/11/2026)

- `bordas.py`: **OK** (761 quadros de TV; laterais 12–1068 px; topo ≥ 300 px).
- `kit/v3/check_quadro.py`: **OK**.
- Uma imagem real por fala; troca ≤ 3 s com variantes `meio`; nenhuma carta inventada; destaques medidos nos PNG.
- Prévia com o fecho (`juntar_fecho.py`): 47,80 s (43,93 s + fecho de 3,87 s); `qc_video.py`: fecho presente, 13 cortes, pico −1,4 dBTP; **P1 −17,0 LUFS esperado** (só música, sem vozes). Não publicável.
- Falta (depende das vozes): ritmo real, −14 LUFS, `qc_video.py` no ficheiro final, escuta das pronúncias.
- Reproduzir a prévia: kit numa cópia de trabalho, `episode.js`/`episode.json` na raiz, `cards/src/` com os 4 PNG do Scryfall, `python3 telas_alexander.py`, `python3 previa_sem_voz.py`, `python3 render.py`, `python3 juntar_fecho.py`.

## 16. Depende do fundador

1. Aprovar o roteiro (sobretudo as correções do §6) e a troca do selo da abertura para «4 COMPRAM».
2. Autorizar as vozes (estimativa: ~1.050 caracteres, 514 Burn + 539 Mana; uma geração).
3. Se quiser a referência do Reddit no episódio: enviar o link da publicação de 17/11.
4. Decidir o registo do «EP. 12» do Olag publicado no Instagram.

## 17. Versão de teste v2 (22/11/2026) · direção artística e refinamento

Missão do fundador de 22/11 (00:05). **Estado sem mudança: EM PRODUÇÃO · prévia sem voz.** A v1 fica intacta; a v2 está em `v2/` (`episode.js`, `episode.json`, `telas_v2.py`, `cards/`, `AUDITORIA_V2.md`).
- **Executado:** auditoria da v1 em quadros 1080×1920; plano de prova com a carta grande e inteira, aproximação ao texto, flip 3D só na troca de carta (Alexander → Rule of Law → Thousand-Year Elixir), reações do Burn sem cartas sobre o rosto, painéis com 3 níveis, legenda paginada; roteiro de 12 falas como **PROPOSTA DE REVISÃO — AGUARDA APROVAÇÃO DO FUNDADOR** (verificação fala a fala em `v2/AUDITORIA_V2.md` §3).
- **Motor:** `kit/prova/patch_prova.py`, opcional e retrocompatível (MB-EP15 igual píxel a píxel e com o mesmo MD5 de mistura). Não é padrão da série sem decisão do fundador.
- **Controlos e prévia:** ver `v2/AUDITORIA_V2.md` §4.

## 18. Produção final (22/11/2026, 01:03–01:45)

Fundador, 01:03: «Aprovado pode colocar as vozes e que agora a esse estilo de edição se torne padrão.» Roteiro v2 de 12 falas aprovado (fala 6 com «na maioria dos casos»); plano de prova passa a padrão da série (`nucleo/DECISOES.md`, `manaburn/PERFIL.md`).
- **Vozes:** ElevenLabs eleven_v4, flow «Mana & Burn — MB-EP16 v2 (Alexander)» (VxpFnbideg7SBtXJtLTA). Burn: Talis (E9a8LlXPNWtyvvSoZzrb), 473 créditos, 24,0 s. Mana: Erik (nfiLpQ54jEQninp3nNqL), 501 créditos, 31,84 s. **Total 974 créditos**, uma geração cada, sem repetição. Faixas: `v2/faixas_elevenlabs.txt`. Corte pelo `tts` (`v2/processar_vozes.py`), conferido contra os silêncios das faixas.
- **Montagem:** kit da `main` com o plano de prova; `v2/telas_v2.py` → `cards/`; `processar_vozes.py burn.mp3 mana.mp3` → `render.py` → `juntar_fecho.py`.
- **QC final:** 44,13 s (40,27 s + fecho), 1080×1920, 30 fps; −14,7 LUFS; pico −1,3 dBTP; fecho presente; `qc_video.py`: sem problemas mensuráveis; `bordas.py` OK; `check_quadro.py` OK; conferência a olho dos planos de prova, flips (falas 5, 8, 10) e legendas (`v2/folha_contacto_final.png`).
- **Legenda, comentário fixado e texto alternativo** atualizados para a v2 (valor de mana, condicional da Rule of Law, ressalva da ruling).

### Ficheiros finais
- Vídeo: `MB_EP16_Alexander_FINAL_916.mp4` (entregue na conversa a 22/11/2026; não versionado).
- Capa: `MB_EP16_CAPA.png` (nesta pasta; selo ALEATÓRIO).
