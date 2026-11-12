# Campanha de aquisição BR · Carrossel "Pare de digitar carta por carta"

11/11/2026 · Frente: Lambe-lambe (post de produto) · Canal: Instagram @binderthetrade → Google Play Brasil
Estado: **pronta para aprovação, não publicar antes dos portões da §0**.

## 0. Leitura direta (o que muda no briefing)

1. **A premissa da LigaMagic está errada.** Os valores do BINDER **não vêm da LigaMagic**. Vêm do Scryfall, em dólar (`prices.usd`, depois foil, etched, euro × 1,10), convertidos com câmbio **fixo de 5,60** (`src/constants/economy.ts`); o overlay do scanner usa **6,0** (`LootOverlay.tsx`). Cache local de 24 h. Fonte: código em `main` (a0a85bd) e Master Técnico v2.6. Anunciar "valores da LigaMagic" seria falso.
2. **O que existe de verdade com a LigaMagic é a exportação.** No Binder (e no inventário da loja) há "Exportar para LigaMagic": copia a coleção em **Texto Rápido (Lista)** para o "Cadastro por Lista" ou em **Planilha (CSV)** para "Importar Coleção (CSV)" (`src/utils/ligamagic.ts`, `VaultScreen.tsx`). Não há parceria; não usar o logótipo. Este é o diferencial anunciável.
3. **O Conceito A (valor da coleção) não pode ir para a rua agora.** A aba Binder mostra "Investido" = 85 % do valor e "Lucro" = +15 %, **sempre**, por um cálculo provisório (`VaultScreen.tsx:291`, "Mock ratio"). Um colecionador experiente vê isso no primeiro minuto e deixa de confiar em tudo. Somam-se o câmbio fixo sem data e a etiqueta "VALOR DE MERCADO" no scanner (é referência, não mercado).
4. **Portões antes de publicar (decisão do fundador de 22/10: DSC-1 é P0 antes de qualquer aquisição).**
   - Servidor: v11_12_0 e v11_13_0 aplicadas (lista de migrações conferida a 11/11). Coordenadas fora do feed. ✅
   - Cliente: OS-01/OS-02 (colunas explícitas, faixas, modo visitante) estão no ramo `feature/zf-01`, **sem build v7 em produção registado**. Confirmar se o v7 saiu. Se não saiu, o 03_STATE ainda marca o P0 como bloqueio.
   - Sem telemetria de funil (schema analytics não existe): a instalação mede-se pela Play (UTM); a "primeira ação" não se mede ainda.
5. **Preferência registada:** o Ibisson prefere uma imagem por post. O briefing pede carrossel; o carrossel está feito e os slides 01, 04 e 07 funcionam sozinhos como posts avulsos.

## 1. Diagnóstico

| | |
|---|---|
| Diferenciais comprovados | Scanner com câmera (OCR do título + escolha da impressão); exportação no formato da LigaMagic (lista ou CSV); português; colecionador e loja no mesmo app |
| Anunciáveis | Scanner; Binder; exportação para a LigaMagic (falta captura real); valor de referência **com fonte e "estimativa"** |
| Não anunciar ainda | Valores "da LigaMagic"; Investido/Lucro; torneios e lojas (congelados a 21/10); Explorar/trocas como argumento (base de 21 colecionadores); "grátis"; iPhone; leitura de cartas em português |
| Principal dor BR | Cadastrar a coleção carta a carta (nome em inglês, sigla da edição) para vender, trocar ou só saber o que tem |
| Porta de entrada | O scanner: resultado em segundos, demonstrável num quadro |
| Objeções | "Mais um app"; "funciona com carta em português?"; "só Android"; "vou ter de criar conta?" (o modo visitante resolve, quando sair no v7) |
| Oportunidade imediata | Quem vende na LigaMagic: público grande, dor clara, a exportação é exatamente o atalho |

## 2. Público

- **Primário:** colecionadores e jogadores brasileiros de Magic (sobretudo Commander), 18+, Android, que já usam a LigaMagic para comprar ou vender. Maior intensidade de dor (cadastro), maior facilidade de demonstração, uso recorrente (cada booster aberto, cada lote).
- **Secundário:** colecionador casual com fichário parado ("não sei o que tenho").
- Fora desta fase: lojistas (Arena congelada), quem está começando (pouca coleção para escanear), competitivo puro.
- Mensagem que melhor converte (hipótese): **"Escaneie com a câmera e leve a coleção para a LigaMagic sem digitar."**

## 3. Conceitos e escolha

| Critério (0–10) | A · Valor da coleção | B · Organização (variante: atalho para a LigaMagic) | C · O colecionismo evoluiu |
|---|---|---|---|
| Impacto inicial | 9 | 8 | 5 |
| Identificação | 8 | 9 | 4 |
| Clareza | 7 | 9 | 4 |
| Diferenciação | 4 (ManaBox, Delver e a própria Liga mostram preço) | 8 (exportação no formato BR) | 3 |
| Compartilhamento | 7 | 6 | 3 |
| Instalação | 7 | 8 | 3 |
| Execução honesta hoje | **2** (mock de lucro, câmbio fixo) | 8 | 6 |
| **Total** | 44 | **56** | 28 |

**Vencedor: B, na variante "Pare de digitar carta por carta".** O A ganha em impacto, mas hoje a experiência pública contradiz a promessa; fica pronto para o teste A/B depois das correções da §8.

## 4. Carrossel (7 slides, 1080×1350)

Ficheiros: `png/01_hook.png` … `07_cta.png`; fonte editável `src/build.py` (Geist, #050A10, #0F172A, #10B981). Telas: quadros 22 e 40 da gravação real de 24/10/2026 (`comum/outro/scan/`).

| # | Objetivo psicológico | Texto principal | Texto secundário | Visual / composição | Transição |
|---|---|---|---|---|---|
| 01 Hook | Pattern interrupt + identificação | Seu fichário tem 300 cartas. / Você vai digitar uma por uma? | "arraste →" | Só tipografia, grande, metade inferior em espaço negativo, brilho verde baixo | Pergunta sem resposta |
| 02 Identificação | Self-identification, perda de tempo | Todo colecionador já fez isso. | Nome em inglês, edição certa, foil ou não. E repete. | Lista em monoespaçada num cartão #0F172A, cursor verde, "faltam 295" | A dor fica concreta |
| 03 Curiosidade | Curiosity gap | E se a câmera fizesse a parte chata? | — | Tipografia centrada, respiro | Promete a solução |
| 04 Descoberta | Demonstration effect | Aponte. Pronto. | O BINDER Vision lê a carta pela câmera e ajuda a identificá-la. | Tela real do scanner com moldura verde, à direita | "e depois?" |
| 05 Demonstração | Micro-recompensa | Confirme. Já está no seu Binder. | Nome, coleção e um valor de referência na mesma tela. | Tela real do resultado (R$ 15,00) + nota de fonte e data | Coleção montada → o que fazer com ela |
| 06 Diferencial | Relevância BR, social identity | Coleção escaneada? Leve para a LigaMagic. | 01 Escaneie · 02 Exporte (lista ou CSV) · 03 Cole na LigaMagic | Três passos tipográficos (sem tela inventada), aviso de não-vínculo | Benefício completo |
| 07 Conversão | Ação única | Escaneie aqui. Pare de digitar. | BINDER Vision · beta para Android | Botão verde "Baixe no Google Play · link na bio" | — |

Iluminação: halo esmeralda difuso vindo de baixo (gradiente radial 16 %), sem brilhos gratuitos. Tipografia: Geist Bold 72–92 px nos títulos, Medium 36 px no apoio, 20 px nas notas legais.

**Screenshots que faltam para a versão definitiva** (pedir ao Ibisson, gravação no Redmi):
1. Menu "Exportar para LigaMagic" aberto com as duas opções (substitui os três passos do slide 06).
2. A LigaMagic com a lista colada no "Cadastro por Lista" (prova do fim do fluxo; sem logótipo em destaque).
3. O carrossel de impressões carregado (o quadro 40 mostra o spinner).
4. Confirmar no aparelho que a exportação funciona no build em produção e que siglas fora da lista branca são avisadas (`debugSetCodes`).

**Prompts de imagem (opcional, só ambientação, nunca no lugar do app):**
- "Overhead shot of a worn black 9-pocket trading card binder open on a dark slate desk, generic card backs with no artwork or logos, single soft emerald rim light from the bottom edge, deep black background #050A10, cinematic product photography, shallow depth of field, lots of negative space at top, 4:5"
- "Close-up of a hand holding an Android phone above a blank trading card, phone screen off and black, dark studio, subtle green volumetric haze, premium tech ad style, no text, no logos, 4:5"
Usar atrás dos slides 01 ou 03 com 30–40 % de opacidade; nada de cartas reais geradas por IA.

Sequência de publicação: 01 → 07, nesta ordem. Capa = 01.

## 5. Copy

Headlines para a capa:
1. Seu fichário tem 300 cartas. Você vai digitar uma por uma? ← escolhida
2. Cadastrar coleção na mão é coisa do passado.
3. A câmera do seu celular faz a parte chata.
4. Escaneou, exportou, colou. Coleção na LigaMagic.
5. Quantas cartas você tem? O BINDER conta pra você.

Narrativas completas:
- **N1 · Pare de digitar (escolhida):** o carrossel da §4.
- **N2 · O fichário da gaveta:** "Aquele fichário parado tem quantas cartas?" → "Você não sabe. Ninguém sabe." → "Aponte a câmera, uma por uma, sem digitar" → tela do scanner → "Pronto: sua coleção numa lista" → CTA.
- **N3 · Antes de vender** (pede a captura 2): "Vai anunciar na LigaMagic?" → "Primeiro, cadastrar tudo" → "Escaneie no BINDER" → "Exporte a lista" → "Cole e siga" → CTA.

CTAs: **A** "Baixe o BINDER Vision no Google Play: link na bio." · **B** "Escaneie sua primeira carta hoje. Beta para Android, link na bio."

Textos de publicação (legendas, Stories, comunidades): `publicacao.txt`.

## 6. Distribuição (custo baixo, nesta ordem)

1. **Orgânico (semana 1).** Carrossel numa terça ou quarta à noite (19h–21h de Brasília). Stories no mesmo dia (3 quadros, §publicação) com sticker de link para o Play com `utm_content=stories`.
2. **Reel do mesmo conceito (semana 1–2).** 15–20 s: hook falado "300 cartas, uma por uma?", tela do scanner (gravação real), exportação (captura 1), cola na LigaMagic (captura 2), fecho obrigatório `comum/outro/outro_binder_916.mp4`. Reaproveita a copy do carrossel; o Reel é o candidato a impulsionar.
3. **Comunidades BR.** Grupos de Facebook e WhatsApp/Discord de Commander e de compra e venda, só onde as regras permitem divulgação (ler as regras, pedir ao admin). Texto em `publicacao.txt`, link com `utm_source` próprio por grupo. Um grupo por dia, responder a todas as dúvidas.
4. **Lojas.** Monster Trainer primeiro, com autorização: QR no balcão com UTM `utm_source=loja_monstertrainer`. Arena e torneios fora do argumento (congelados).
5. **Criadores.** Formato proposto: "escaneei meu fichário inteiro" (desafio de organização, demonstração honesta, sem pagamento por instalação). Escolher criadores de Commander BR pequenos e médios; a lista sai de pesquisa à parte, sem inventar nomes nem audiências.
6. **Meta Ads (só depois de validar).** Condição: v7 com DSC-1 em produção **e** carrossel ou Reel orgânico com CTR do link ≥ 1 % e pelo menos 5 instalações atribuídas. Campanha de instalação de app (Android, Brasil, 18–45, interesses Magic: The Gathering / trading card games / LigaMagic como interesse se existir). Criativo: o Reel. Teste: R$ 20/dia por 7 dias (R$ 140). Escalar se custo por instalação ≤ R$ 4 e ≥ 20 % abrir o scanner (quando a telemetria existir); parar se CPI > R$ 8 após 3 dias ou CTR < 0,7 %. Antes: rever a política de fan content da Wizards para anúncio pago com cartas.

## 7. Mensuração e A/B

- Link com UTM por peça: `https://play.google.com/store/apps/details?id=com.binderstudios.vision&referrer=utm_source%3Dinstagram%26utm_medium%3Dcarrossel%26utm_campaign%3Dpare_de_digitar` (Stories: `utm_medium=stories`; grupos: `utm_source=<grupo>`).
- Ferramentas: Instagram Insights (alcance, salvamentos, compartilhamentos, visitas ao perfil, toques no link) e Play Console > Aquisição de utilizadores (visitas à página e instalações por UTM). **Não existe** medição da primeira ação no app; contas novas contam-se em `profiles.created_at` (pedido ao arquiteto), sem ligar a UTM.
- Critério de sucesso do carrossel (orgânico, conta pequena): salvamentos ≥ 3 % do alcance; toques no link ≥ 1 % das contas alcançadas; ≥ 3 instalações com `utm_campaign=pare_de_digitar` em 7 dias. Abaixo disto, trocar o hook, não o conceito.
- **A/B:** Variação B (esta) já. Variação A ("Você sabe quanto vale o seu fichário?") só depois das correções da §8, com o mesmo layout, mesma hora, semana seguinte. Métrica de decisão: instalações por 1.000 alcançados.
- Não confundir curtidas com aquisição. Não inventar taxas.

## 8. Correções no app que desbloqueiam o Conceito A (para o arquiteto, sem tocar no código agora)

1. Tirar "Investido" e "Lucro" da aba Binder enquanto não houver preço de compra real (o perfil já calcula com o preço gravado).
2. Um só câmbio (5,60 vs 6,0) e com data visível; idealmente atualizado.
3. Etiqueta "Valor de referência (Scryfall, US$ convertido)" em vez de "VALOR DE MERCADO".
4. Formatos já registados: três casas decimais e "R$ 1.20".
Se um dia os valores passarem a vir da LigaMagic, é preciso autorização deles (os termos regem o uso do portal) antes de anunciar.

## 9. Google Play (auditoria parcial)

A página não abriu nesta sessão (bloqueada no ambiente); vale a leitura de 19/10. Prioridades para casar com a campanha, **sem publicar sem autorização**:
1. Descrição curta a abrir pela dor: "Escaneie suas cartas de Magic com a câmera e exporte a coleção para a LigaMagic."
2. Primeira screenshot = scanner com moldura verde; segunda = exportação (captura 1).
3. Descrição completa: dizer que os valores são referência do Scryfall convertida, e que só há Android.
4. Ícone e nome: manter (consistência com o perfil).
5. Vídeo promocional: o Reel da §6.

## 10. Auditoria final

| Pergunta | Colecionador novo | Jogador experiente | Diretor de marketing | Aquisição | Criação |
|---|---|---|---|---|---|
| Pararia de rolar? | Sim (300 cartas) | Sim | Sim | Sim | Sim, tipografia forte |
| Entende o benefício? | Sim no 04 | Sim | Sim | Sim | Sim |
| Necessidade real? | Média | Alta (vende na Liga) | — | — | — |
| Entende a LigaMagic? | Sim, no 06 | Sim | Sim | Sim | Sim |
| Confia nos valores? | Sim no 05 (nota de fonte) | **Não, se abrir a aba Binder (Lucro +15 %)** | Risco | Risco de desinstalação | — |
| Feito para a minha realidade? | Sim | Sim | Sim | — | — |
| Motivo concreto para instalar? | Sim | Sim | Sim | Sim | — |
| Experiência pública = promessa? | Sim, se a exportação for confirmada no aparelho | Parcial (mock) | Depende do v7 | Depende do v7 | — |

Revisão aplicada: o valor saiu da promessa principal (fica só como nota com fonte no 05), a LigaMagic entra como destino da exportação e não como fonte de preço. Pendente fora do meu alcance: correção 8.1, captura 1–2 e build v7.

## Fontes

- Código: `ibisson254/aethervault-app` `main` a0a85bd (`src/services/scryfall.ts`, `src/constants/economy.ts`, `src/components/scanner/LootOverlay.tsx`, `src/screens/VaultScreen.tsx`, `src/utils/ligamagic.ts`); `feature/zf-01` c15ee72 e `.ai/03_STATE.md`.
- Supabase: lista de migrações (11/11/2026).
- Drive: [ATUAL] BINDER — Master Technical Documentation v2.6 (22/10/2026); 02 · Contexto do produto BINDER Vision (25/10).
- Projeto: `claude/00-comece-aqui.md`, `claude/agente-binder-posts-instagram.md`.
- Repositório do estúdio: `comum/outro/LEIA-ME.md` (origem da gravação do scanner).

Fontes: copiar Geist-*.woff2 de manaburn/node_modules/geist/dist/fonts/geist-sans/ para src/ antes de correr build.py.

## v2 (11/11/2026, pedido do fundador)
Paleta clara (papel #F2EEE6, tinta #0A0F14, esmeralda #0E9F6E, ouro #E0A526), 6 slides, `src/build_v2.py`, textos em `publicacao_v2.txt`. A LigaMagic aparece como destino da exportação e onde se confere o preço da Liga; o valor do app fica como referência (Scryfall). Telas novas do Perfil cortadas sem rostos nem nomes de terceiros.

## v3 (11/11/2026, "refina essa ideia")
Capa com Sol Ring, The One Ring e Rhystic Study (Scryfall); grade de 6 staples na dor; scanner em painel escuro; R$ 396 como herói; tela real do Binder com o botão Exportar (sem a linha Investido/Lucro); CTA com selo. `src/build_v3.py`; as imagens das cartas baixam-se de novo com `cartas/creditos.json`. Textos: `publicacao_v3.txt`.
