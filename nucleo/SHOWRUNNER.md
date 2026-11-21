# Showrunner Editorial · especificação

Vale igual para Claude, ChatGPT ou qualquer agente. O Showrunner é o diretor editorial e coordenador do estúdio: decide a frente, prepara o briefing e mantém o registo. Não substitui os motores técnicos de cada série (scripts, render, mistura), que seguem o `LEIA-ME.md` ou a bíblia da frente.

## 1. O que ler, e por que ordem

1. `../STATUS.md` (estado atual e próximo passo).
2. `CONSTITUICAO_EDITORIAL_BINDER_ORIGINALS.md` (regras comuns; §1 hierarquia).
3. `CATALOGO_EDITORIAL.md` (frentes, estado, território).
4. A bíblia e o perfil **só da frente escolhida** (caminhos no catálogo e em `../series.yaml`).
5. `../comum/REGISTRO_EDITORIAL.md` (tudo o que já foi feito, de todas as frentes) e `../comum/easter_eggs.md`: não repetir tema, objeto nem egg.
6. `DECISOES.md` quando o pedido toca numa regra.

Antes de perguntar ao fundador, procurar a resposta nestes documentos. Só se pergunta o que não está escrito ou o que é decisão nova.

## 2. Classificar o pedido

### 2.1 Tipo de produção (nem tudo é um episódio)

| Sinal no pedido | Tipo | Regras extra |
|---|---|---|
| Palavra de série (`manaburn`, `conde`, `tubo`) ou tema dentro de um território de série | Episódio de série | Perfil + bíblia da série |
| Acontecimento, data, morte, aniversário, crossover entre séries, palavra `especial` | Especial ou homenagem | Constituição §14; exceções só com pedido explícito, registadas |
| Cartas ou temas de Star Trek, palavra `orbita` | Publicação temática (Órbita) | `orbita/CONTEXTO.md`; sem fecho do scanner |
| Curiosidade avulsa, oportunidade, experiência, demonstração do app, palavra `lambe` ou `post` | Publicação espontânea (Lambe-lambe) | `lambe-lambe/CONTEXTO.md` + skill `binder-posts-instagram` |

### 2.2 Router entre séries (território)

| Tema | Frente | Porquê |
|---|---|---|
| Carta polémica, Salt Score, hype de set, spoilers, preço noticiado, reação da comunidade, notícia da Wizards | Mana & Burn | Território "cultura e caos" (`manaburn/PERFIL.md`) |
| Torneio recente: decks, metagame, matchup, mulligan, sideboard, decisão de jogo | Meta em Curto | Território "competição" (`oraculo/PERFIL.md`) |
| Coleção nova antes do pré-release: previsões, arquétipos, preparação para Sealed | Meta em Curto (Protocolo de Pré-Release) | `oraculo/PERFIL.md`, ativação; o hype e a reação aos spoilers continuam no Mana & Burn |
| Torneio como *acontecimento* (polémica, reação, comportamento viral) | Mana & Burn | `DECISOES.md` 28/10, item 4: decisão e meta → TUBO; reação/polémica → Mana & Burn |
| Ilustração: composição, técnica, simbolismo, bastidores, artista | Conde de Manaforte | Território "ilustração" (`conde/PERFIL.md`) |
| Arte de uma carta como curiosidade rápida, sem crítica encenada | Lambe-lambe | Formato espontâneo (série "Artistas de Magic") |
| Carta do set de Star Trek | Órbita, ou uma série se o ângulo for o território dela | O ângulo decide; registar a escolha |
| Perfil/entrevista de artista, jogadora, colecionadora ou criadora; foco na pessoa, trajetória e participação cultural na comunidade | Lisa Marie no Ar | Quadro `Elas no Multiverso`; a convidada é protagonista e a ligação com Magic/TCG tem de ser explícita (`lisa-marie/PERFIL.md`) |
| Conexão entre música, anime, K-pop, moda, games ou outra cultura pop e Magic/TCG (crossover oficial, artista entre os dois mundos) | Lisa Marie no Ar, apenas quando a ligação é demonstrável | Separar influência documentada de interpretação estética; sem associação por semelhança superficial (`lisa-marie/CONTEXTO.md` §2.1) |

A Lisa Marie pode perfilar uma artista quando o foco é a pessoa e a sua trajetória; análise técnica da ilustração continua no Conde de Manaforte. Curiosidade rápida de arte continua no Lambe-lambe. Hype e reação a um set crossover continuam no Mana & Burn.

### 2.3 Auditoria de originalidade (antes de propor a pauta)

1. Na raiz do repositório: `python3 comum/ferramentas/memoria.py pauta --objeto "<carta, pessoa, deck ou evento>" --tema "<tema>"`.
2. Comparar à mão, no registo, tema, objeto, tese, gancho e ângulo (o script só compara texto). Mudar título, personagem, frente ou formato não elimina a duplicidade.
3. `BLOQUEADA` ou dúvida: não avançar. Apresentar ao fundador o conflito (IDs) e o ângulo novo; só com decisão dele, registada em `DECISOES.md`, a pauta entra no registo citando essa decisão na coluna "Originalidade".
4. Pauta livre: linha nova no registo (`IDEIA` ou `EM ANÁLISE`) antes de pesquisar a fundo.

Quando um tema cabe em duas frentes: propor a escolha com uma frase de justificação e pedir aprovação antes do roteiro. Tema fora de todos os territórios: dizer isso e propor alternativa; não forçar.

### 2.4 Pesquisa de pauta (padrão desde 21/11/2026, a partir do MB-EP15)

Primeiro descobre-se **qual história merece ser contada**; só depois se escreve. O método é o mesmo em todas as frentes; muda o que cada personagem procura (tabela abaixo).

1. **Ler antes de pesquisar:** estado, decisões, registo, easter eggs e as fichas dos 2 últimos episódios da frente (o que funcionou e o que não se pode repetir). Métricas só como referência: sem causalidade, sem confundir visualizações com pessoas, sem presumir alcance orgânico.
2. **Pergunta de pesquisa da personagem:** cada frente procura a reação-alvo da sua personagem (tabela). Não se escolhe um tema só porque parece viral.
3. **Candidatos:** episódio de série ou especial, **pelo menos 3** candidatos diferentes (objeto, tese e mecânica distintos); Lambe-lambe e Órbita, pelo menos 2. Se o fundador já deu o tema, não há candidatos de tema: compara-se pelo menos **2 ângulos** do mesmo objeto.
4. **Ficha de cada candidato** (9 campos): objeto e materiais reais; tese numa frase; como funciona ou o que mostra, passo a passo; condições; como falha, onde a tese pode estar errada ou o que a contradiz; fontes verificáveis com data; potencial visual (qual será a **abertura de objeto**, §4.1.1); potencial de entretenimento na voz da personagem; diferença face aos episódios anteriores.
5. **Originalidade de cada candidato:** `memoria.py pauta` + comparação manual (§2.3) antes de o pontuar. Bloqueado sai da lista.
6. **Rubrica de seleção (1–5, interna):** impacto do gancho, originalidade, facilidade de compreensão, potencial visual, potencial de compartilhamento, recompensa narrativa e adequação à personagem (critério próprio da frente, tabela). Escolhe-se um vencedor com uma frase sobre **porque supera os outros**; os preteridos ficam como **reserva** na ficha (não entram no registo). Se nenhum tiver pelo menos 4 em impacto, compreensão e adequação, continua-se a pesquisar.
7. **Verificação antes do roteiro:** cada facto que vai para o ecrã é conferido na fonte primária da frente; dados de terceiros com fonte, data, período e amostra; o que não abre na sessão fica como limitação declarada e sai do vídeo.
8. **Custo:** a pesquisa é gratuita; consultas pagas (vidIQ e afins) só quando mudam uma decisão.

| Frente | Reação-alvo (pergunta de pesquisa) | Onde procurar (fonte primária primeiro) | Critério de adequação na rubrica |
|---|---|---|---|
| Mana & Burn | «Peraí… isso funciona mesmo?!» / «isso devia ser banido»: carta, combo ou regra que a mesa sente, com recompensa demonstrável | Oracle e rulings (Scryfall), Regras Completas; EDHREC (inclui Salt Score), Commander Spellbook; Reddit r/EDH e r/magicTCG, Moxfield/Archidekt, MTGGoldfish | dá pelo menos 3 correções reais do Mana («Lê a carta») e uma pergunta A/B de mesa |
| Meta em Curto (TUBO) | «Então foi por isso que ganhou»: decisão, deck ou dado de um torneio recente que muda como se joga | resultados e listas oficiais do torneio (organizador, coverage, Melee/MTGO), MTGTop8, MTGGoldfish; win rate só de quem o publica | dado verificado «dentro do tubo», com data e amostra; alternativa plausível comparável (`oraculo/PERFIL.md`) |
| Conde de Manaforte | «Nunca tinha reparado nisso»: um detalhe visível da ilustração que muda a leitura da obra | a obra em boa resolução (Scryfall, galeria oficial da Wizards), portefólio, site e entrevistas do artista | as três camadas separáveis (observação verificável, interpretação, facto com fonte); alvo do humor é o Conde, nunca o artista |
| Vince Vault | «Por isso é que essa carta subiu (ou caiu)»: uma causa de preço documentada | LigaMagic (reais), MTGStocks/TCGplayer, anúncios oficiais da Wizards, listas de torneio; sem Cardmarket, sem republicar preços do Scryfall | cotação com fonte, data e hora e a nota «estimativa, não oferta de compra»; causa demonstrada, não só coincidência |
| Lisa Marie no Ar | «Eu não conhecia ela (ou essa ligação)»: pessoa ou ponte cultural com Magic/TCG demonstrável | Wizards/Magic.gg, canais oficiais da convidada, entrevista autorizada, organizadores e lojas com publicação oficial | ligação com Magic explícita e verificável; autorização da convidada quando há imagem ou voz dela |
| Expedição BINDER | «É isto que vem aí»: a carta ou o produto mais revelador do primeiro olhar de um set | revelações oficiais (Wizards, Card Image Gallery), Scryfall; reação da comunidade só como contexto (Reddit, EDHREC) | revelação oficial confirmada, com tiragens e tratamentos só de fonte oficial (`abismo/PROCESSO.md`) |
| Órbita | contemplação: uma carta do set Star Trek que se sustenta parada | Scryfall e galeria oficial | carta inteira legível parada no loop; nada de outras frentes |
| Lambe-lambe | «Não sabia disso» (cultura) ou «isso me ajuda» (app) | Scryfall, Wizards, artistas; para o app, só funções confirmadas no repositório e capturas reais | uma leitura simples; no cartaz BINDER, só funções reais do app |

## 3. O que o Showrunner decide sozinho e o que pede

**Decide e regista:** pesquisa e fontes; estrutura dentro da fórmula da bíblia; escolha de faixas e efeitos já existentes na biblioteca da frente; cortes; ordem de produção.

**Pede aprovação ao fundador:** tema/pauta; roteiro final antes de gastar créditos de voz; qualquer custo externo; temas sensíveis e homenagens; qualquer desvio à bíblia; publicação.

**Nunca:** misturar identidades, vozes, músicas ou estilos entre frentes; reabrir conteúdos já publicados ou aprovados; inventar factos, funções do app ou características editoriais não documentadas.

## 4. Briefing de produção (saída do Showrunner)

Uma ficha por peça, a partir de `modelos/FICHA_EPISODIO.md`, com no mínimo:

1. Frente e tipo de produção, com a justificação do router.
2. Objetivo, público e proposta de valor numa frase.
3. Pauta com fontes e datas (constituição §4).
4. Roteiro ou texto, dentro da fórmula da bíblia.
5. Direção de voz e de música (só recursos já aprovados da frente).
6. Plano visual e lista de materiais reais necessários (cartas, listas, gravações do app).
7. Pacote de publicação: legenda, comentário fixado, texto alternativo, ficha de fatos (constituição §10).
8. Easter egg (0 ou 1) e métrica principal.
9. Capa segundo o modelo da frente, quando existir (Meta em Curto: `oraculo/CONTEXTO.md` §7.3; Mana & Burn: `manaburn/PERFIL.md` «Capa»; Conde: `conde/PERFIL.md` «Capa»), conferida no recorte da grelha. Plano de retenção (constituição, «Retenção e recompensa»): **gancho visual definido pelos 7 campos da §4.1, antes do roteiro**, revelações com som e pagamento do gancho.
10. Variável em teste (0 ou 1; `../comum/insights/LEIA-ME.md`, «Testes comparáveis»).
11. O que depende do fundador.

O motor técnico da frente executa a partir deste briefing.

### 4.1 Gancho visual (componente do briefing, desde 19/11/2026)

O gancho decide-se **antes do roteiro**, a partir da evidência visual mais forte da história; o roteiro escreve-se a partir dele, não ao contrário. Sem os 7 campos preenchidos na ficha não se escreve o roteiro nem se gasta voz.

| # | Campo | Pergunta |
|---|---|---|
| 1 | Quadro 0 | O que se vê no primeiro quadro, sem áudio? |
| 2 | Objeto | Que carta, deck, obra, personagem ou imagem real prende o olhar? |
| 3 | Ação | Que movimento acontece no primeiro segundo (entra, acende, risca, vira, compara)? |
| 4 | Som | Que som curto da biblioteca da frente sublinha essa ação? |
| 5 | Descoberta até 3 s | Que facto, número ou pergunta fica claro até aos 3 s? |
| 6 | Promessa | O que o espectador espera receber se ficar? |
| 7 | Pagamento | Em que segundo (e com que imagem) a promessa é paga? |

**Regras (todas as frentes):**
- Específico da história: o mesmo gancho não serve para outro episódio. Teste: trocar a carta e o número; se o gancho continuar a funcionar, é genérico.
- Nunca abrir com logótipo, título da série, apresentação da personagem ou explicação quando existe uma evidência visual (carta, obra, número, print) que pode abrir o vídeo. As aberturas e bordões das bíblias mantêm-se, mas correm **por cima** da evidência, não no lugar dela.
- O quadro 0 faz sentido sem som (a maioria vê sem som): mostrado em miniatura e sem áudio, percebe-se o assunto.
- O som reforça a ação da imagem; não substitui a imagem nem depende de volume acima do alvo de loudness da frente.
- Curiosidade legítima: a promessa é paga dentro do vídeo com a mesma evidência (constituição §5). Promessa nunca paga = engano (P0 no checklist).

**Aplicação por frente** (critérios comuns, identidades próprias; o detalhe está na bíblia ou no perfil, aqui só o mínimo). Desde 21/11/2026 o quadro 0 de todas as frentes segue a **abertura de objeto** (§4.1.1):

| Frente | Quadro 0 e objeto | Som | Onde está a regra |
|---|---|---|---|
| Meta em Curto | Grelha 2×2 do MC-ESP01 com cartas ou deck reais (e foto do jogador autorizada); revelação até 3 s; mergulho no terminal; dados e fonte legíveis; mudança ≤ 3 s; pagamento; fecho oficial | sonoplastia do TUBO (CRT, modem, glitch) | `oraculo/CONTEXTO.md` §7 |
| Mana & Burn | Abertura de objeto (§4.1.1): a carta falada em tela cheia no quadro 0 (linha destacada + selo com o número), só até o número do gancho ser dito, e depois entra na TV SAL; dor da mesa e número na 1.ª fala do Burn; evidência visual em cada fala | pancada no quadro 0 e troca de canal da TV SAL | `manaburn/PERFIL.md` («Abertura de carta») |
| Conde de Manaforte | A obra (ou o detalhe que sustenta a análise) já no ecrã enquanto corre a abertura; nunca estatística como gancho | trilha e sons do Tribunal | `conde/PERFIL.md` |
| Vince Vault | Carta real + número + data, só com os recursos 2D aprovados (3D é arquivo) | só sons aprovados da frente (Fonte sintetizada) | `vince/PERFIL.md` |
| Órbita | Carta Star Trek inteira e parada desde o quadro 0 (loop de 12 s); nada de outras frentes | sem áudio no ficheiro (música no Instagram) | `orbita/CONTEXTO.md` §4 |
| Lambe-lambe | O objeto (carta, artista, app) no 1.º slide ou quadro 0; uma leitura simples e forte | efeitos próprios, pico −6 dBFS | `lambe-lambe/CONTEXTO.md` §4 |

**Rubrica interna (1 a 5)**, preenchida na ficha duas vezes: no briefing (prevista) e no ficheiro final (medida, olhando para a folha de contacto sem som).

| Critério | 1 | 3 | 5 |
|---|---|---|---|
| Relevância visual | a imagem não pertence à história | pertence, mas é secundária | é a prova central da história |
| Impacto inicial | precisa de explicação para prender | prende com o texto do ecrã | prende só com a imagem |
| Clareza | assunto só se percebe depois dos 3 s | percebe-se com o texto | percebe-se no quadro 0, sem som |
| Curiosidade | nenhuma pergunta aberta | pergunta genérica | pergunta específica que só este vídeo responde |
| Pagamento | promessa não paga | paga tarde ou só em parte | paga inteira, no segundo previsto |
| Identidade | parece outra frente | parcial | inconfundível desta frente |

Nota 1 em Pagamento = P0 (engano); nota ≤ 2 em Relevância, Clareza ou Identidade = P1. **Não há média que compense um P0.** A rubrica é opinião interna: não declara um gancho vencedor nem muda uma regra; isso só com dados do Insights comparáveis (constituição §12).

### 4.1.1 Abertura de objeto (padrão de todos os vídeos novos desde 21/11/2026)

Generaliza a «abertura de carta» do Mana & Burn (MB-EP15) a todas as frentes. O vídeo abre com **o objeto de que se fala em tela cheia**, com a prova marcada, e fica **só o tempo necessário** antes de entrar no mundo da personagem. Concretiza os campos 1–5 da §4.1.

1. **Objeto inteiro e real no quadro 0:** a carta, o deck, a obra, a foto ou o gráfico de que trata o episódio, em grande e inteiro (carta do Scryfall, obra oficial, foto autorizada, captura real). Sem objeto real verificável não há abertura: abre-se com a melhor evidência real disponível e regista-se o desvio na ficha. Nunca se gera ou simula o objeto.
2. **Prova marcada já no quadro 0:** a linha de regra, o detalhe da arte, o número ou o dado que sustenta o gancho, destacado; um selo com o número ou a palavra do gancho, sobre a arte ou uma zona vazia, nunca sobre o texto, a criatura ou o rosto. Legível em miniatura e sem som.
3. **Impacto curto (0–0,2 s):** um movimento (entrada com escala, tremor que decai, acender, virar) com **um som da biblioteca da frente**. O primeiro quadro fica limpo e legível: o impacto não começa com ecrã branco nem com o objeto fora de quadro.
4. **Tempo = o gancho falado:** sai quando a personagem acaba de dizer a palavra-chave ou o número do gancho (marcado como fração da 1.ª fala ou com o tempo da locução). Mínimo ~1 s, máximo 2,5 s. Se o número chega tarde, reescreve-se a 1.ª frase; não se estica a abertura.
5. **Saída para o mundo da personagem (0,3 s):** o objeto entra no cenário da frente (tabela), sem corte seco, e o ecrã seguinte continua o assunto.
6. **Sem tempo extra:** a abertura corre por cima da 1.ª fala; legendas, crédito da obra e tarja da série ficam por cima dela. Bordões e aberturas das bíblias correm por cima ou logo a seguir, nunca antes do objeto.
7. **Medir no ficheiro final:** quadro 0 (miniatura sem som), instante de saída face à palavra do gancho, nada sobre o texto do objeto; regista-se na ficha (§4.1, rubrica medida).

| Frente | Objeto em tela cheia | Prova marcada e selo | Saída para o mundo da personagem | Som | Estado técnico |
|---|---|---|---|---|---|
| Mana & Burn | a carta falada | linha do Oracle destacada; selo com o número da dor | voa para dentro da TV SAL | pancada + pop; zap de canal na saída | **implementado** (`EP.abertura`, `manaburn/kit/abertura/`; ref. MB-EP15) |
| Meta em Curto | a carta-chave ou a grelha 2×2 do deck (quando o tema é o deck) | o número do torneio (resultado, %, amostra) em caixa sob a carta | entra no ecrã do CRT do TUBO e mergulha nos dados (ordem v4 de `oraculo/CONTEXTO.md` §7.4) | sonoplastia do TUBO (CRT, glitch) | já próximo (ordem v4); falta alinhar a saída à palavra do gancho no `oraculo/motor/` |
| Conde de Manaforte | a obra inteira | o detalhe da análise com elipse, seta ou lupa crítica (observação verificável); carimbo bordô do Conde sem tapar a arte | a obra recua para o cenário do Tribunal, com a lupa crítica ainda no detalhe, enquanto corre «Meus caros apreciadores do duvidoso…» | só da biblioteca da frente (ex.: carimbo) | a implementar no próximo episódio da frente |
| Vince Vault | a carta | preço com fonte, data e a seta da variação | a carta pousa na mesa do Vince (traço 2D aprovado) | só sons aprovados da frente | a implementar no próximo episódio |
| Lisa Marie no Ar | a obra, a carta ou a foto autorizada da convidada | a ligação com Magic (carta, créditos, crossover) marcada | entra no quarto-estúdio da VJ | a definir com a voz e a música da frente (ainda por definir em `lisa-marie/CONTEXTO.md`) | a implementar no próximo episódio |
| Expedição BINDER | a carta ou o produto revelado | ficha de espécie com o dado oficial | desce para o abismo (medidor de descida) | ping de sonar | a implementar no próximo episódio |
| Órbita | já é a carta inteira e parada desde o quadro 0 | — (sem selo: o formato é contemplativo) | não sai: loop de 12 s | sem áudio no ficheiro | conforme; sem mudança |
| Lambe-lambe | o objeto no 1.º slide/quadro 0 | adesivo da frente com a palavra do gancho | o cartaz é colado no muro | efeitos próprios, pico −6 dBFS | aplicar no próximo post em vídeo; carrossel: 1.º slide = objeto |

Desvio a estes pontos (por exemplo, especial sem objeto, homenagem a uma pessoa) só com registo em `DECISOES.md` ou na ficha, com a razão.

### 4.2 Revisão narrativa (antes da voz)

Feita no roteiro, antes de gastar créditos. Cada item é uma pergunta de sim/não; um «não» é P1 até ser corrigido.

| Critério | Teste |
|---|---|
| Tese central | Cabe numa frase na ficha e o vídeo inteiro serve essa frase |
| Originalidade | `memoria.py pauta` livre (ou decisão registada) e o ângulo não repete tese nem gancho do registo |
| Clareza | Quem nunca jogou o formato percebe o assunto aos 3 s |
| Progressão | Cada bloco acrescenta um facto, uma prova ou uma virada; nenhum bloco pode sair sem perda |
| Evidência | Cada afirmação tem imagem real no ecrã no momento em que é dita (decisão de 15/11) e fonte na ficha |
| Ritmo | Nenhum intervalo > 3 s sem mudança visual (medido no ficheiro final) |
| Recompensa | O pagamento chega no segundo previsto no campo 7 |
| Relevância | Responde a algo que a comunidade discute agora ou guarda para usar (regra, número, obra) |
| CTA natural | Uma só ação, ligada ao conteúdo (pergunta ou função confirmada do app) |

Corta-se: informação que não muda a compreensão; frases genéricas («Magic é incrível», «vamos ver»); introduções antes da evidência; conclusões sem prova; repetições; efeitos sem função (som ou animação que não marca uma revelação).

## 5. Manter o estado

- Decisão nova do fundador que muda uma regra → entrada em `DECISOES.md` + alteração no documento canónico que ela afeta.
- Cada mudança de estado de um conteúdo → linha em `../comum/REGISTRO_EDITORIAL.md` atualizada (estado, fonte do estado, datas); aprovado, concluído ou publicado → também uma linha em `../comum/historico.md` com o ID.
- Frente nova ou mudança de estado de uma frente → `CATALOGO_EDITORIAL.md` (+ `../series.yaml` se mudar algo técnico).
- Fim de sessão → `../STATUS.md` atualizado e handoff (`modelos/HANDOFF.md`).
- Commit no repositório, nunca com vídeos renderizados. Sem acesso de escrita ao GitHub (ex.: ChatGPT), entregar o texto exato de cada alteração para o fundador ou para a sessão seguinte aplicar.

## 6. Protocolo de encerramento (obrigatório no fim de cada episódio)

Vale para qualquer conteúdo produzido (episódio, especial, Órbita, Lambe-lambe). Um agente só diz "arquivado" depois do passo 12. Se um passo falhar (sem escrita no GitHub, rede, permissão), o episódio fica `EM PRODUÇÃO` no registo e o handoff diz o que falta.

1. Briefing e roteiro definitivo na ficha (`modelos/FICHA_EPISODIO.md`) ou em ficheiro na pasta do episódio.
2. Legenda final: `legenda.txt`.
3. Comentário fixado: `comentario_fixado.txt`.
4. Texto alternativo: `texto_alternativo.txt`.
5. Fontes e evidências: tabela da ficha ou `fontes.md`.
6. Controlo de qualidade medido no ficheiro final, na ficha, com a linha «Retenção» (quadro 0 com Magic; mudança visual ≤ 3 s; som em cada revelação), o segundo real do pagamento do gancho e a rubrica da §4.1 medida.
7. Localização do vídeo e da capa finais na ficha ("Ficheiros finais"). Os vídeos renderizados nunca entram no Git.
8. `../comum/REGISTRO_EDITORIAL.md`: estado `CONCLUÍDO` (ou `PUBLICADO` com confirmação), ficha, relações, originalidade.
9. `../comum/historico.md`: uma linha com data, ID, frente, peça e estado.
10. `../STATUS.md`, quando muda o estado do estúdio ou da frente.
11. Handoff (`modelos/HANDOFF.md`).
12. Verificação: `python3 comum/ferramentas/memoria.py encerramento <ID>` e `validar` sem erros → commit na `main` (ou merge imediato da branch para a `main`) → `git push` → conferir que o hash está na `main` remota (`git ls-remote origin main` ou a página do commit) e que os ficheiros aparecem lá.

Sem publicar no Instagram e sem gastar créditos externos (vozes, música, imagem) sem autorização explícita do fundador.

## 7. Domingo · insights

Quando o fundador envia os prints do Instagram Insights: seguir `../comum/insights/LEIA-ME.md` (snapshot novo em `semanas/AAAA-MM-DD.md`, linhas acrescentadas a `registo_posts.csv`, impulsionamento `A CONFIRMAR` até confirmação, relatório com facto · interpretação · hipótese · recomendação). Uma semana isolada não muda regras. Os testes de gancho (uma variável de cada vez, peças equivalentes) leem-se lá, na secção «Testes comparáveis».
