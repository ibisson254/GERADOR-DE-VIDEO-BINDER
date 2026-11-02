# Auditoria · Evolução visual e excelência das personagens · 02/11/2026

Missão do fundador "BINDER Originals — Master Engineering Directive · Visual Evolution & Character Excellence" (02/11/2026). Branch `evolucao-visual-2026-11`. Classificação: **P0** impede publicação · **P1** qualidade importante · **P2** refinamento.

Separação usada em todo o documento: **Implementado** (está no repositório e foi testado) · **Proposto** (precisa de aprovação do fundador) · **Pendente** · **Bloqueado**.

## 1. Fontes consultadas

`AGENTS.md`, `STATUS.md`, constituição v1.4, `CATALOGO_EDITORIAL.md`, `SHOWRUNNER.md`, `DECISOES.md`, `modelos/HANDOFF.md`, `CHECKLIST_QUALIDADE.md`, `manaburn/PERFIL.md`, `manaburn/LEIA-ME.md`, `oraculo/PERFIL.md`, `oraculo/CONTEXTO.md` (§3, §6, §10), `conde/PERFIL.md`, `conde/CONTEXTO.md` §10, `comum/outro/LEIA-ME.md`, `comum/historico.md`, `comum/easter_eggs.md`, `series.yaml`, `.gitignore`. Projeto claude.ai: `claude/gerador-manaburn/episodios/zapping_01.js`, `legendas/zapping01_legenda.txt`, excertos de `index.html` v2 (pesquisa).

**Drive (lido a 02/11, 01:00):** bíblia "BINDER Marketing — Série Mana & Burn · 24/10/2026" (doc `1fYkvk8x…`), "05 · Série Mana & Burn: como produzir um episódio + kit técnico", "06 · Mapa do Drive". O motor que gerou o Giro não está no Drive (pesquisa por "giro", "zapping", "TV SAL"). Revisão com a bíblia: §3a.

## 2. Vídeo analisado

`giro_2026-11-01_final.mp4` (enviado pelo fundador a 02/11). Visto inteiro: 69 quadros a 1 por segundo, recortes a 4 por segundo nas falas (15–19 s, 44–48 s) e no fim (62–65 s), deteção de cortes, loudness. Medido com `comum/qc/qc_video.py`:

| Medida | Valor | Regra | Estado |
|---|---|---|---|
| Formato | 1080×1920, 30 fps | séries 9:16 | OK |
| Duração | 69,0 s; 65,13 s sem o fecho | perfil 35–45 s | P2 · formato "Giro de domingo" não está no perfil (ver §7) |
| Loudness | −14,1 LUFS integrado, LRA 3,9 LU | −14 ± 1 | OK |
| Pico verdadeiro | −2,5 dBTP | < −1 | OK |
| Fecho do scanner | presente a partir de 65,13 s, diferença média 0,07/255 | obrigatório | OK |
| Cortes | 15,0 · 20,6 · 25,37 · 29,7 · 33,17 · 36,73 · 45,83 · 47,53 · 50,97 · 55,33 · 60,17 · 63,37 · 64,63 | — | — |
| Factos centrais | Dan Ayoub presidente da WotC (ex-Halo/343) · All Leylines' Eve com Leyline of Anticipation (WPN 2026) | fonte | Confirmados em fontes públicas (Retail Dive, iCv2, WPN); datas da agenda não reconferidas nesta sessão |

Estrutura observada: gancho escrito (0–4 s) → notícia 1 TV (4–15) → reação no sofá (15–25) → notícia 2 TV (25–29,7) → reação (29,7–36,7) → notícia 3 TV (36,7–45,8) → "Lê a carta" (45,8–51) → agenda TV (55,3–60,2) → pergunta e "Comenta aí" (60,2–64,6) → clarão branco → fecho (65,1–69).

## 3. Diagnóstico com timecodes

### P0

Nenhum (revisto depois da leitura da bíblia, §3a).

### Decisão pendente do fundador

| # | Tempo | Defeito | Regra |
|---|---|---|---|
| D-1 (era P0-1) | 15–20 s, 33–37 s, 51–55 s, 60–63 s | Nos planos do sofá a TV fica ao fundo, cortada pela margem direita, e a programação (manchete, carta da Leyline, agenda) aparece cortada. Em 51–55 s é a **carta** que está cortada | A bíblia e o doc 05 pedem a carta inteira nos planos de TV e nos zooms (cumprido). A TV ao fundo cortada já existia nos episódios aprovados, por isso não é P0. Proposta: P1 a partir do próximo episódio (TV ao fundo inteira, ou programação neutra sem carta quando não cabe) |

### P1

| # | Tempo | Defeito | Correção proposta |
|---|---|---|---|
| P1-1 | 0–4 s | O texto do gancho ("MORREU O PICARD…") passa por cima da cabeça do Burn | Gancho numa faixa própria acima da cabeça (y ≤ 300) ou cabeça fora do plano no gancho |
| P1-2 | Planos de TV (4–15, 25–29, 37–46, 55–60 s) | A bíblia manda "TV em primeiro plano, com ele [o Burn] atrás apontando". No Giro o braço a apontar só aparece no gancho (0–4 s); no resto fica só a cabeça por cima do móvel, que se lê como cabeça solta | Manter a composição da bíblia e mostrar sempre ombros + braço a apontar a TV |
| P1-3 | 4–15 s | A legenda queimada tapa a linha de fonte da TV SAL ("Fonte: TheGamer (29/10/2026), preço do TCGplayer") | Fonte acima da área da legenda; linha de fonte com ≥ 24 px de altura (constituição §3, Etapa 2) |
| P1-4 | 4–15 s, 25–29 s, 55–60 s | Corpo da TV SAL (linhas de apoio, fontes) com ~20 px no ficheiro final: ilegível no telemóvel | Mínimo 28 px para texto que se quer ler; abaixo disso, é só "para quem pausa" e não pode conter a fonte |
| P1-5 | Quase todo o vídeo | As linhas da legenda chegam a x ≈ 985 px e entram na coluna de botões do Instagram (zona segura aproximada: 140 px à direita) | Largura máxima da legenda 820 px, centrada a x ≈ 470 |
| P1-6 | 0–15 s, 25–29 s, 37–46 s, 55–60 s | Nos planos de TV, ~30% inferior do quadro é um chão roxo liso, sem informação | Subir a TV e aproximar (TV a ocupar 60–70% da largura e o centro ótico), ou usar o espaço para o rodapé da TV SAL |
| P1-7 | 15–25 s, 29,7–36,7 s, 50,97–55,3 s, 60–63 s | Dupla quase sempre de frente para a câmara; o Mana não olha para o Burn e mantém a mesma cara (pálpebra caída, olhar de lado) do princípio ao fim | Ver §4 (química) |
| P1-8 | 33–37 s e 51–55 s | A mesma pose do Burn (braços no ar, boca aberta) em duas falas com emoções diferentes ("Ex-Halo?" é ironia; "ninguém joga nada!" é euforia) | Biblioteca de poses por emoção (§4) |
| P1-9 | 64,63 s | Fim da cena: clarão branco em toda a sala, depois preto, depois o fecho. A bíblia (§1) manda: "o Mana desliga a TV, a imagem encolhe até virar um ponto, o ponto fica verde-esmeralda (#10B981) e vira o ponto da logo" | Repor o fecho da bíblia antes do fecho do scanner |
| P1-10 | 0–4 s | A notícia de abertura usa uma morte como gancho de mercado ("Morreu o Picard. No dia seguinte, a caixa dele subiu."). A fala seguinte condena o oportunismo, por isso o vídeo não ri da morte, mas o gancho isolado pode ser lido assim | Para pautas com morte: o gancho nomeia o alvo da crítica (o preço), não a morte. Decisão editorial: fica como proposta |

### P2

| # | Tempo | Defeito |
|---|---|---|
| P2-1 | Todo | Rótulo "MANA & BURN / TV SAL · GIRO DE DOMINGO" e crédito da carta (37–55 s) a ~16 px, dentro da zona do cabeçalho do Instagram: invisível na prática. O crédito completo já está na legenda |
| P2-2 | 0–1 s | Os marcadores mostram ① ② enquanto a voz já diz "Três notícias"; o ③ só aparece a 2 s |
| P2-3 | 15–25 s | Plano de reação com 10 s seguidos sem mudança de enquadramento (só a boca mexe) |
| P2-4 | Cenário | Mesmas posições de objetos (pôster do dragão, calendário 2019, quadro do pôr do sol, caixas BOOSTER) em todos os planos, sem variação de luz entre planos: coerente, mas plano |

### O que está bem (manter)

Loudness e pico dentro do alvo; fecho oficial intacto; legenda com palavras-chave em amarelo e contorno, legível; marcador de notícia (1, 2, 3, ?) ajuda a seguir; "Lê a carta" com o texto destacado na carta real; pergunta numérica ("Comenta 1, 2 ou 3") alinhada com a hipótese do histórico; factos centrais com fonte.

## 4. Relatório por personagem

### Mana (bíblia: alto e magro, cabelo comprido a cair no olho, gorro verde, cara de sono, pacote de salgadinho na mão; parece dormir mas sabe todas as regras)
- **Observado:** no modelo (gorro, cabelo no olho, salgadinho, cara de sono). Uma só expressão em todo o vídeo; nunca olha para o Burn.
- **Leitura com a bíblia:** a cara de sono é identidade e fica. O que falta é a reação dentro dela: as falas do Mana soam a narrador porque ele não reage ao Burn.
- **Proposto:** variações mínimas sobre a cara de sono, sem abrir os olhos de vez: uma sobrancelha a subir (dúvida), pálpebra a abrir meio ponto (surpresa curta, volta logo ao sono), canto da boca de lado (ironia). Poses: cabeça a virar para o Burn nas réplicas; apontar o controle para a câmara no "Comenta aí" (já está na bíblia, Ep. 1 e 2).

### Burn (bíblia: baixo e atarracado, cabelo raspado pintado de vermelho, camisa de flanela aberta, lata de refrigerante; boca quente, quer banir tudo)
- **Observado:** no modelo (cabelo raspado vermelho com textura de pontos, flanela aberta). A lata não se vê nos planos conferidos. 3 estados (neutro com sobrancelhas zangadas, boca aberta, braços no ar), encolher de ombros (46 s) e apontar para a câmara no fim. Boca a abrir e fechar alinhada com a voz (verificado 15–19 s); sobrancelhas zangadas mesmo em falas neutras.
- **Problema:** a impulsividade lê-se, mas a gama é curta e repete (P1-8).
- **Proposto:** sobrancelhas separadas da boca (zangado / espantado / triunfante), "pose de discordância" (mão aberta para o Mana), "corpo inclinado para a TV".

### Química entre os dois
- **Observado:** nenhum plano de resposta; quem não fala fica parado; não há olhares cruzados nem interrupções.
- **Proposto:** regra de montagem "quem ouve reage": em cada fala com mais de 2 s, o outro muda de expressão a meio; em 1 de cada 3 trocas, plano de resposta de 0,6–1 s só de quem ouve; olhar para o parceiro nas perguntas.

## 5. Cenário · proposta de evolução (sem estúdio moderno)

**Conferência com a bíblia (§1, "Cenário" e "Estética"):** presentes sofá verde com fita, TV de tubo (foto real) sobre caixas de booster, calendário de 2019, infiltração, rachaduras, papel de parede a descascar, carpete manchado, playmat na mesa. **Em falta no Giro:** ventilador de pé, palha de aço e paninho de crochê na antena, manta de crochê no sofá, benjamim na tomada, piso de taco. Completar estes elementos é cumprir a bíblia, não inventar.

**Proposto, a aprovar:**
1. **Cenário-mestre único** (`manaburn/cenario/sala_mestre.svg` + `sala_mestre.json` com as posições de cada objeto), lido pelo kit; deixa de haver variação acidental entre episódios. Os objetos atuais mantêm-se.
2. **Três planos fixos** com câmara definida no JSON: conjunto (sofá + TV inteira), TV (TV a 60–70% da largura, sem cabeças), contraplano (um personagem, ombro do outro em primeiro plano).
3. **Luz:** a TV como fonte de luz fria (halo azul-esverdeado na parede e nos rostos quando está ligada) e um candeeiro quente; resolve a separação primeiro plano/fundo sem mudar a paleta.
4. **Profundidade:** mesa de centro mais escura e desfocada em primeiro plano nos planos de conjunto; parede de fundo com 10–15% menos contraste.
5. **TV SAL:** grelha de 3 tamanhos (título 64 px · linha 36 px · fonte 28 px), fonte sempre acima de y = 1450.

## 6. Restantes frentes (consistência documental)

Sem vídeos do TUBO e do Conde nesta sessão: nenhuma conclusão visual sobre eles.
- **Meta em Curto:** a bíblia (`oraculo/CONTEXTO.md` §10) manda registar previsões em `comum/historico.md`; EP01 e EP02 registam "nenhuma". O contador "ERROS HUMANOS" não tem valor registado em nenhuma ficha (lacuna, não inventada). `ep01_render_v2.py` importa `render` inexistente (episódio publicado: não se mexe).
- **Conde:** lista "Não usar" em `conde/CONTEXTO.md` §10 é a memória de cartas; está atualizada até ao Ep. 003. `montar_ep002.py` com caminho absoluto (publicado: não se mexe).
- **Transversal:** o motor que renderizou o Giro não está no repositório nem nos documentos do projeto claude.ai (há o `zapping_01`, não há "giro"). Correções de motor ficam bloqueadas até ele subir.

## 3a. Revisão depois da leitura da bíblia (02/11, 01:00)

- O Giro foi **publicado** (fundador, 02/11, 01:05): não se reabre. Os defeitos valem como regra para os próximos. O print do post no telemóvel confirma o P1-3 (legenda por cima da linha de fonte).

- P0-1 passa a decisão pendente D-1: a bíblia exige a carta inteira nos planos de TV e nos zooms, que o Giro cumpre; a TV ao fundo cortada já existia em episódios aprovados.
- P1-2 deixa de propor tirar o Burn dos planos de TV: a composição "Burn atrás da TV a apontar" é da bíblia; o defeito é a execução (sem braço).
- P1-9 confirmado pela bíblia.
- Mana: a cara de sono é identidade; as propostas passam a ser variações dentro dela.
- Duração: o doc 05 do Drive (25/10) diz 35–53 s e os Ep. 5–7 tiveram 47–53 s; `manaburn/PERFIL.md` diz 35–45 s. Divergência para o fundador decidir; até lá vale o perfil (repositório).
- Lacuna que a bíblia não resolve: nenhuma ficha de personagens com folha de expressões (a bíblia lista "Ficha dos personagens e animação" como pendente).

## 7. Formato "Giro de domingo"

Formato de 3 notícias da semana (sucessor do Zapping nº 1, 816 views em `comum/historico.md`) com 65 s + fecho. Não está no `PERFIL.md` nem no catálogo. **Proposto:** registar no perfil do Mana & Burn como formato derivado, com duração própria (55–65 s), para o controlo de qualidade deixar de o marcar.

## 8. Implementado nesta sessão

- `comum/qc/qc_video.py` + `comum/qc/LEIA-ME.md`: controlo de qualidade automático (formato, duração, loudness, pico, fecho, cortes, folha de contacto com zona segura). Testado: Giro (OK, 0 P0), fecho isolado (detetado), Giro cortado a 60 s sem fecho (P0 detetado, código de saída 1).
- `nucleo/CHECKLIST_QUALIDADE.md`: classificação P0/P1/P2, bloco E (personagens, cena, montagem, TV SAL), bloqueador novo "texto a tapar fonte" e passo automático.
- `comum/continuidade/`: memória editorial por personagem, separada por frente, com índice comum.
- Este relatório; `nucleo/DECISOES.md`; `STATUS.md`.

Nenhum asset mestre, voz, música, episódio publicado ou script de episódio foi alterado.

## 9. Handoff

```
HANDOFF · 02/11/2026 · Claude
Repositório: ibisson254/GERADOR-DE-VIDEO-BINDER · branch evolucao-visual-2026-11 · último commit fdc9848 (+ este handoff)

Objetivo atual: evolução visual do BINDER Originals; auditoria do Giro de 01/11 feita, ferramentas de QC e memória implementadas, propostas identitárias a aguardar aprovação.

Decisões tomadas nesta sessão:
- Gravidade P0/P1/P2, bloco E da checklist, QC automático, memória de continuidade (registada em nucleo/DECISOES.md? sim)

Documentos consultados:
- ver §1 deste relatório

Alterações realizadas:
- comum/qc/qc_video.py, comum/qc/LEIA-ME.md · QC automático · fdc9848
- nucleo/CHECKLIST_QUALIDADE.md · P0/P1/P2 + bloco E · fdc9848
- comum/continuidade/ (4 ficheiros) · memória por série · fdc9848
- nucleo/auditorias/2026-11-02_evolucao_visual.md, nucleo/DECISOES.md, STATUS.md · fdc9848

Tarefas pendentes:
- Aprovar propostas §4, §5, §7 e o merge da branch · depende de fundador
- Motor que gerou o Giro (não está no repositório nem no projeto) · depende de fundador
- Confirmar publicação do Giro de 01/11 para comum/historico.md · depende de fundador
- Ler a bíblia do Mana & Burn no Drive antes de mexer nas personagens · depende de agente com acesso ao Drive

Próximo passo concreto: com o motor do Giro, corrigir P0-1 e P1-1 a P1-6 e validar com python3 -I comum/qc/qc_video.py <video> --frente manaburn
```
