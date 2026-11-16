# Parcerias · próximas collabs

Painel vivo das collabs. Versão de 16/11/2026, 17:31 (fundador): **método «episódio pronto primeiro»** — o BINDER produz o episódio completo e só depois o envia ao parceiro, a pedir a collab e a autorização para publicar. Substitui a versão das 17h (fechos de quentes e DM antes de produzir). Base de pesquisa: `nucleo/auditorias/2026-11-16_parcerias.md`.

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
5. **Pacote de envio** (o fundador envia por DM, do @binder_vision): o vídeo ou carrossel final com marca «PRÉVIA», a legenda já com o @ deles, uma frase curta a pedir duas coisas — collab e OK para publicar — e um prazo.
6. **Prazo:** resposta em até 5 dias. Os episódios com dados têm data de corte; depois de ~10 dias, refaz-se a conta ou cai o episódio.
7. **Ajustes pedidos pelo parceiro:** aceitam-se correções de facto e de crédito; mudanças de tese ou de tom passam pelo fundador.
8. **Registo:** a pauta entra no `REGISTRO_EDITORIAL.md` ao começar a produção (estado EM PRODUÇÃO); a resposta do parceiro vai para `<frente>/autorizacoes/`; só passa a PUBLICADO depois de o fundador publicar.
9. **Um envio por semana**, para cada resposta ter UTM e leitura própria (`utm_source=<handle>&utm_campaign=<ID>`; leitura a 48 h e 7 dias).

## Próximos episódios

| Ordem | ID provisório | Parceiro-alvo | Frente · formato | Créditos | Se disser não | Material em falta |
|---|---|---|---|---|---|---|
| 1 | **LL-ART20** | Caio Monteiro (artista) | Lambe-lambe · carrossel | 0 | publicar com crédito e marcação | handle confirmado |
| 2 | **MC-ESP03** | MTGDC500 / Lotus Games (dono dos dados) | Meta em Curto · Reel 25–35 s | voz (~1.500–2.200, estimativa) | publicar com crédito ao site (dados públicos) | nada; extração no dia |
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
- **Mudança em relação ao piloto do relatório:** com o episódio feito primeiro, a fonte tem de ser pública e escolhida por nós: o **MTGDC500** (mtgdc500.com.br, «Lotus Games»). Por isso o alvo da collab passa a ser **quem assina os dados** (MTGDC500 / Lotus Games), não o Farpas de Mana — mandar ao Farpas um vídeo com os números de outro portal, sem saber se concorrem, é arriscado. O Farpas fica para um episódio com fonte deles, quando o site deles abrir ou eles a indicarem.
- **Tese:** mais jogado não é mais forte, e a taxa de TOP 4 mais alta pode ser só amostra pequena ou torneios pequenos (relatório §3.A e §6).
- **Gancho:** Cloud, Midgar Mercenary («467 listas») × Ghalta, Primal Hunger («7 de 8»); «O mais jogado ou o que mais vence?». Números refeitos no dia da produção, com data de corte, período, torneios e listas no ecrã; cálculos do BINDER marcados como tal.
- **Fim:** pergunta «Qual comandante você acha que só parece forte?» (sem frase do parceiro) + outro do scanner.
- **Pré-requisito:** confirmar o @ da Lotus Games / MTGDC500 no Instagram antes de produzir; se não houver perfil ativo, o fundador decide entre o Farpas (com a ressalva acima) ou publicar sem collab.
- **Mensagem de envio:**
  > Oi, pessoal do MTGDC500! Sou o Ibisson, do BINDER Vision (Meta em Curto, análise de meta no Instagram). Fizemos um vídeo com os dados públicos do site de vocês: o comandante mais jogado do DC500 é o que mais vence? Segue a prévia, com crédito e link. Toparia publicar em collab? Se algum número ou definição estiver errado, corrigimos antes.

### 3 · MC-ESP04 · Preconauta — «Mesa de 4 ou 2x2: o mesmo precon joga igual?»
- **Parceiro já ativo:** a autorização de 13/11 (`oraculo/autorizacoes/2026-11-13_preconauta_dados_2x2.md`) cobre collab e números dos sites deles; o envio pede só o OK desta peça.
- **Bloqueio:** o objeto «Taça Preconauta» está fechado (MC-ESP02). Usa só as ligas mesão e 2x2.
- **Tese provisória:** o mesmo precon na mesa de 4 (referência 25%) e no 2x2 (50% por dupla). Só avança se os dados tiverem desempenho por precon nos dois formatos; senão, muda de ângulo ou não se faz.
- **Material em falta:** prints ou exportação das ligas (presencial e online), com período e amostra — o site deles não abre a partir do ambiente do agente.
- **Leitura:** comparar com o MC-ESP02. Se cair muito, a terceira collab seguida com o Preconauta fica em pausa.

## Depois destes três
Farpas de Mana (fonte própria), Tenda da Liliana (Pauper), Cabrito Montês (reserva, só com atividade confirmada em 2026). Taverna Games fora.

## Registo de resultados

| ID | Parceiro | Enviado | Resposta | Publicado | 48 h (visitas/1.000) | 7 dias (visitas/1.000) | Instalações UTM | Decisão |
|---|---|---|---|---|---|---|---|---|
| MC-ESP01 | @montcardshop | — | aceitou | sim | | | | termo de comparação |
| MC-ESP02 | Preconauta | — | aceitou | sim | | | | termo de comparação |

Sem dado = vazio, nunca 0.
