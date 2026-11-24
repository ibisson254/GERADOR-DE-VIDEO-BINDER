# Parcerias · próximas collabs

Painel vivo das collabs. MC-ESP03 corrigido a 19/11/2026 (parceiro-alvo Farpas de Mana). Versão de 16/11/2026, 17:31 (fundador): **método «episódio pronto primeiro»** — o BINDER produz o episódio completo e só depois o envia ao parceiro, a pedir a collab e a autorização para publicar. Substitui a versão das 17h (fechos de quentes e DM antes de produzir). Base de pesquisa: `nucleo/auditorias/2026-11-16_parcerias.md`.

As autorizações ficam em `<frente>/autorizacoes/`; os números de cada collab vão para `comum/insights/registo_posts.csv` na rotina de domingo.

## Collabs feitas (fechadas, não se reabrem)

| Parceiro | Conteúdo | Estado | Nota do fundador |
|---|---|---|---|
| Preconauta (@preconautamtg) | MC-ESP02 | collab aceite e publicada | um dos episódios com mais views (16/11; número a registar no domingo) |
| @montcardshop | MC-ESP01 | collab aceite e publicada | — |

Todos os outros conteúdos com terceiros já foram feitos, publicados e registados (fundador, 16/11).

## Método «episódio pronto primeiro»

**Porquê:** um parceiro diz «sim» mais facilmente a uma coisa que já vê pronta do que a uma ideia. A conta é pequena; o episódio pronto é o argumento.

**Regras para o método não sair caro nem arriscado:**
1. **Só material público e creditável.** Dados de sites públicos, cartas do Scryfall, obra publicada. Nada que precise de autorização para ser *produzido* (fotos pessoais, dados privados, logótipo, voz ou frase do parceiro). Assim o episódio existe sem depender do «sim».
2. **O vídeo não afirma parceria.** Nada de «em parceria com…» no ecrã nem na voz. A collab vive na legenda e no botão de collab do Instagram, que se ajustam depois da resposta. Se o parceiro disser não, o episódio não fica com mentira gravada.
3. **Plano B decidido antes de produzir** (campo «Se disser não» em cada projeto): publicar com crédito e marcação, ou arquivar. Se o plano B for arquivar, o episódio tem de ser barato (carrossel, sem voz).
4. **Créditos:** voz e imagem só com autorização do fundador, uma geração. Começa-se pelos formatos sem créditos.
5. **Pacote de envio** (o fundador envia por DM, do @binder_vision): o vídeo ou carrossel **final, sem marca «PRÉVIA»** (fundador, 23/11/2026: nunca marcar prévia, para não refazer trabalho; o que depende de autorização sai num re-render sem nova voz), a legenda já com o @ deles, uma frase curta a pedir duas coisas — collab e OK para publicar — e um prazo.
6. **Prazo:** resposta em até 5 dias. Os episódios com dados têm data de corte; depois de ~10 dias, refaz-se a conta ou cai o episódio.
7. **Ajustes pedidos pelo parceiro:** aceitam-se correções de facto e de crédito; mudanças de tese ou de tom passam pelo fundador.
8. **Registo:** a pauta entra no `REGISTRO_EDITORIAL.md` ao começar a produção (estado EM PRODUÇÃO); a resposta do parceiro vai para `<frente>/autorizacoes/`; só passa a PUBLICADO depois de o fundador publicar.
9. **Um envio por semana**, para cada resposta ter UTM e leitura própria (`utm_source=<handle>&utm_campaign=<ID>`; leitura a 48 h e 7 dias).

## Próximos episódios

| Ordem | ID provisório | Parceiro-alvo | Frente · formato | Créditos | Se disser não | Material em falta |
|---|---|---|---|---|---|---|
| 1 | **LL-ART20** | Caio Monteiro (@caiomonteiroart) | Lambe-lambe · carrossel | 0 | versão B (sem foto) com crédito e marcação | **pronto 16/11** · prévia por enviar · prazo 21/11 |
| 2 | **MC-ESP03** | Farpas de Mana (@farpasdemana), dono do portal Duel Commander 500 usado como fonte | Meta em Curto · Reel 25–35 s | voz (~1.500–2.200, estimativa) | publicar com crédito ao portal do Farpas (dados públicos), sem afirmar parceria | **EM PRODUÇÃO desde 19/11** (`oraculo/episodios/esp03_dc500/`); bloqueado no Gate A: números do portal por JavaScript, sem acesso daqui a 16/11 nem a 19/11 → capturas da lista `capturas/LEIA-ME.md` ou sessão com Claude in Chrome |
| 3 | **MC-ESP04** | Preconauta (parceiro ativo) | Meta em Curto · Reel | voz | não se aplica (autorização de 13/11 cobre os números dos sites deles) | prints das ligas mesão e 2x2 |

Pautas auditadas a 16/11 com `memoria.py pauta`: as três LIVRES.

### 1 · LL-ART20 · Caio Monteiro — «O carioca por trás de Shark Typhoon»
- **Porque primeiro:** custo zero (`lambe-lambe/kit_carrossel/motor_padrao.py`), artista brasileiro (formato já provado com a Nathanna Érica) e o artista tende a partilhar um carrossel que celebra o trabalho dele. Serve de teste do método.
- **Conteúdo:** 6–8 slides. Capa com Shark Typhoon (IKO 67; reimpressa em FRC 44 a 02/10/2026) · quem é (Rio de Janeiro; fonte Archon Arcana) · n.º de artes únicas no Scryfall, contado no dia · 3–4 artes mais jogadas segundo o EDHREC (Archmage Emeritus, Marauding Blight-Priest…) · slide final: «Qual é a sua arte favorita dele?» + scanner do BINDER Vision.
- **Não usar:** foto pessoal, falas inventadas, bastidores.
- **ID:** LL-ART14 a 19 ficam reservados aos seis carrosséis da branch `lambe/artistas-carrosseis` (`nucleo/DECISOES.md` 14/11).
- **Mensagem de envio:**
  > Oi, Caio! Sou o Ibisson, do BINDER Vision. A gente faz uma série de carrosséis sobre artistas brasileiros de Magic e fizemos um sobre o seu trabalho — segue a prévia. Toparia publicar em collab com a gente? Se quiser trocar alguma arte ou corrigir algo, é só falar. Tudo com crédito e link para o seu portfólio.

### 2 · MC-ESP03 · «O mais jogado é o que mais vence?» (Duel Commander 500)
- **Correção do fundador (19/11/2026, `nucleo/DECISOES.md`):** o parceiro-alvo é o **Farpas de Mana** e a fonte é o **portal próprio Duel Commander 500 do Farpas** (os artigos deles citam duelcommander500.com.br; endereço confirmado no dia da extração). Substitui a versão de 16/11, que punha o MTGDC500 / Lotus Games como dono dos dados deste episódio. A Lotus Games **não** é parceira escolhida deste piloto, e os números do MTGDC500 recolhidos a 16/11 (Cloud 467 listas, Ghalta 7 em 8) **não entram** no MC-ESP03. Nenhuma parceria está aceite.
- **Tese:** mais jogado não é mais forte, e a taxa de vitória ou de TOP mais alta pode ser só amostra pequena ou torneios pequenos (relatório §3.A e §6). A tese é do BINDER, não do Farpas.
- **Gancho:** provisório até haver os dados do portal. Modelo: dois comandantes reais na grelha 2×2 do MC-ESP01 (o mais jogado × o de maior taxa), com o número de cada um e «O mais jogado ou o que mais vence?» até 3 s. Os 7 campos (`nucleo/SHOWRUNNER.md` §4.1) preenchem-se com os números do portal, com data de corte, período, torneios e listas no ecrã; cálculos do BINDER marcados como tal; definições do portal (o que conta como vitória, TOP ou aparição) copiadas para a ficha.
- **Fim:** pergunta «Qual comandante você acha que só parece forte?» (sem frase do parceiro) + outro do scanner.
- **O vídeo não afirma parceria:** crédito «Dados: Duel Commander 500 (Farpas de Mana), <período>» no ecrã e na legenda; a collab só entra na legenda e no botão do Instagram depois do «sim», registado em `oraculo/autorizacoes/AAAA-MM-DD_farpas_dc500.md`.
- **Pré-requisito:** acesso ao portal. Daqui ele não abriu a 16/11; se continuar sem abrir, o fundador envia a exportação ou prints com data, período e amostra, ou o episódio espera. Sem dados verificáveis não há episódio.
- **Mensagem de envio** (o fundador envia do @binder_vision; nada foi enviado):
  > Fala, Farpas! Sou o Ibisson, do BINDER Vision (Meta em Curto, análise de meta no Instagram). Fizemos um vídeo com os dados públicos do portal de Duel Commander 500 de vocês: o comandante mais jogado é o que mais vence? Segue a prévia, com crédito e link. Toparia publicar em collab? Se algum número ou definição estiver errado, corrigimos antes.

### 3 · MC-ESP04 · Preconauta — «Mesa de 4 ou 2x2: o mesmo precon joga igual?»
- **Parceiro já ativo:** a autorização de 13/11 (`oraculo/autorizacoes/2026-11-13_preconauta_dados_2x2.md`) cobre collab e números dos sites deles; o envio pede só o OK desta peça.
- **Bloqueio:** o objeto «Taça Preconauta» está fechado (MC-ESP02). Usa só as ligas mesão e 2x2.
- **Tese provisória:** o mesmo precon na mesa de 4 (referência 25%) e no 2x2 (50% por dupla). Só avança se os dados tiverem desempenho por precon nos dois formatos; senão, muda de ângulo ou não se faz.
- **Material em falta:** prints ou exportação das ligas (presencial e online), com período e amostra — o site deles não abre a partir do ambiente do agente.
- **Leitura:** comparar com o MC-ESP02. Se cair muito, a terceira collab seguida com o Preconauta fica em pausa.

## MC-PAU02 · Tenda da Liliana (missão do fundador, 23/11/2026)
- **Antecipada pelo fundador**: a Tenda estava na lista «depois destes três»; a missão de 23/11 pede a collab já. Conflito com a regra «uma parceria nova de cada vez» (LL-ART20 e MC-ESP03 em aberto) **por confirmar com o fundador**.
- Peça: MC-PAU02 «68 cópias. 17 decks.» (`oraculo/episodios/pau02_tenda_snacker/`). Fonte do evento: artigo de Tiago Fuguete (27/08) e listas do Fuguete na Tenda 200 (23/08). A Tenda é parceira do evento, não dona dos dados de metagame.
- **Atualização 23/11, 02:05 (fundador):** collab **tripla** BINDER × Tiago Fuguete × Tenda da Liliana; sem marca PRÉVIA (o vídeo enviado é o final). Foto do Tiago e logótipo da Tenda no vídeo desde já; quem recusar sai num re-render sem nova voz.
- Se disser não ou não responder até 29/11: publicar a Versão B com crédito textual ao evento, sem logótipo.
- Material em falta: confirmação dos números (artigo e PauperPilot, fora do alcance da sessão), logótipo oficial (SVG/PNG transparente).
- Mensagem pronta: `oraculo/episodios/pau02_tenda_snacker/mensagem_collab.md`. Nada enviado.

## Depois destes três
Tenda da Liliana (Pauper), Cabrito Montês (reserva, só com atividade confirmada em 2026). Taverna Games fora. Lojas com dados próprios (ex.: Lotus Games / MTGDC500) só como pauta nova, depois do piloto com o Farpas e com decisão do fundador.

## Registo de resultados

| ID | Parceiro | Enviado | Resposta | Publicado | 48 h (visitas/1.000) | 7 dias (visitas/1.000) | Instalações UTM | Decisão |
|---|---|---|---|---|---|---|---|---|
| MC-ESP01 | @montcardshop | — | aceitou | sim | | | | termo de comparação |
| MC-ESP02 | Preconauta | — | aceitou | sim | | | | termo de comparação |
| LL-ART20 | Caio Monteiro | | | | | | | |
| MC-ESP03 | Farpas de Mana | | | | | | | |
| MC-PAU02 | Tiago Fuguete + Tenda da Liliana | | | | | | | |
| MB-EP17 | Magic Amador (@magicamador) | | collab aceite segundo o fundador (24/11); âmbito da reutilização por confirmar | | | | | |

Sem dado = vazio, nunca 0.
