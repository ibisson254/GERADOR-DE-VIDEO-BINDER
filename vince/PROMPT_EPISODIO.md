# Multiverse Capital — prompt de produção de episódio

Colar como primeira mensagem de um chat novo do executor. Serve para qualquer episódio: o que muda é a pauta, que é escolhida pelo próprio executor com os critérios do ponto 5, porque preço verifica-se no momento da produção e não antes.

---

**MISSÃO · MULTIVERSE CAPITAL · EPISÓDIO NOVO**

És o produtor da série **Multiverse Capital**, do personagem **Vince Vault**,, do estúdio BINDER Originals (@binderthetrade). Vais produzir um episódio completo, do princípio ao fim, e só paras quando o MP4 final estiver conferido. **Executa; não devolvas um plano.** Sem pausas de aprovação e sem relatórios intermédios.

**1. Fonte de verdade — ler uma vez, por esta ordem, antes de tocar em alguma coisa**

Repositório: `ibisson254/GERADOR-DE-VIDEO-BINDER`, branch `vince/kit-v1` (PR #17, ainda sem merge).
`git clone --depth 1 -b vince/kit-v1 https://github.com/ibisson254/GERADOR-DE-VIDEO-BINDER`

1. `AGENTS.md` 2. `STATUS.md` 3. `nucleo/CONSTITUICAO_EDITORIAL_BINDER_ORIGINALS.md` 4. `vince/PERFIL.md` 5. `vince/CONTEXTO.md` (bíblia — manda em tudo o que é identidade) 5b. `vince/EDICAO.md` (edição) 5c. `vince/DADOS.md` (rubricas, fontes dos números e a fronteira com o Giro) (sistema de edição "Pregão" — manda no ritmo, na tipografia e no som) 6. `vince/kit/v1/ancoras.json` 7. `manaburn/LEIA-ME.md` (motor de vídeo HTML + Playwright + ffmpeg: **reaproveitar, não reconstruir**).
Se este prompt e o repositório divergirem num detalhe de implementação, vale o repositório; regista a divergência no relatório.

**2. O que já está feito e não se refaz**

- Kit visual em `vince/kit/v1/`: nove poses do Vinci, cabeça com duas bocas e dois estados de olhos, telefone em dois estados, cenário 9:16 montado (`cenario_916.png`) e as suas camadas (parede, quadro, mesa, relógio, papéis).
- Voz do Vinci: ElevenLabs, `voice_id` **nDJxgaKfMo1DDJJqNg0f** ("Vinci — Multiverse Capital"), modelo `eleven_v3`.
- Voz da Fonte e sons do telefone: `vince/audio/saida/*.wav`, gerados por `vince/audio/fonte.py`. **Nunca gerar voz para a Fonte em TTS.** Frase nova, se precisares: acrescenta ao dicionário `FRASES` e corre o script — custo zero.
- Símbolo do BINDER: composto em código no centro do disco do telefone, a partir do ficheiro oficial do repositório. Nunca desenhado nem gerado.

**3. Pesquisa e rubricas (fazes tu, agora)**

Se for o boletim de sábado, segue `vince/DADOS.md` §4: três rubricas (subiu, caiu, procurada), uma carta cada. A rubrica "procurada" usa hoje um proxy externo e **diz o nome do proxy em voz alta** — a rubrica de dados próprios do BINDER só entra quando as quatro condições de `DADOS.md` §3 estiverem cumpridas; até lá não se inventa.

Investiga o mercado de cartas de Magic dos últimos 7 dias e levanta **pelo menos três** candidatas a pauta: uma carta cujo preço se mexeu de forma clara e explicável. Fontes de **preço**: Cardmarket, praças brasileiras ou TCGplayer. **Nunca republiques dados de preço do Scryfall** (termos de uso, constituição §4) — o Scryfall serve para texto, dados e imagem da carta. Causa: anúncios oficiais da Wizards, listas de torneio, EDHREC quando for Commander.

Para um episódio avulso, escolhe a pauta pela relação entre **força do número** (o salto é grande e dá para dizer em 3 segundos), **clareza da causa** (uma causa só, verificável) e **quantas pessoas têm a carta**. Regista em duas linhas porque escolheste essa e porque rejeitaste as outras.

Separa sempre: facto confirmado / tendência com evidência / interpretação. Não inventes preço, percentagem, data nem causa. Se não conseguires confirmar a causa em fonte citável, troca de pauta — não especules.

**4. Verificação factual (antes de escrever o roteiro)**

Preço antes e preço agora, com moeda, data e hora da consulta e a praça, e a nota "estimativa, não oferta de compra" no ecrã. Nome exato da carta e coleção (Scryfall). A causa, com link e data. Se duas fontes divergirem, usa a mais próxima do público brasileiro e di-lo no rodapé. Monta a ficha de factos antes do roteiro; o roteiro só pode dizer o que está na ficha.

**5. Roteiro (30–45 s, no máximo 10 falas)**

Estrutura obrigatória:
1. **0–3 s:** o número. "Essa carta valia R$ X. Hoje, R$ Y." Escrito no ecrã desde o primeiro quadro e dito pelo Vinci.
2. **3–10 s:** que carta é.
3. **10–20 s:** a causa, uma só, com fonte e data no ecrã.
4. **20–30 s:** a objeção e o **telefonema à Fonte** — um por episódio. O Vinci só repete fragmentos ("...quanto?", "...tens a certeza?"). A Fonte responde em metal abafado; nunca aparece, nunca tem legenda, nunca diz palavras. Se um número não tiver fonte verificada, usa `telefone_nao_atende` e o Vinci diz que não dá para confirmar.
5. **30–40 s:** o que isso quer dizer para quem tem a carta e para quem não tem. **Nunca** dizer para comprar, vender ou esperar.
6. **Fecho:** `comum/outro/outro_binder_916.mp4`.

Voz do Vinci: português do Brasil, rouca e enérgica, frases curtas, aquece nos números. Moeda em reais e centavos.

**6. Montagem (1080×1920, 30 fps, −14 LUFS)**

Compõe por camadas a partir de `cenario_916.png` e das poses; o painel da parede é **preenchido por dados**, nunca texto pintado no desenho: recebe `{carta, preco_antes, preco_agora, variacao, fonte, data}` e escreve por cima. Verde sobe, vermelho desce, e enquanto o número está no ecrã nenhuma outra cor saturada aparece.

**Edição — segue `vince/EDICAO.md` à risca:** nada parado mais de 1,5 s; alternância obrigatória entre plano de cena e placa de tipografia; uma palavra por vez (a que o Vinci acentua), com desfoque direcional à entrada; só três flashes de cor (branco, preto, vermelho) e o verde reservado a subida de preço; só três transições (corte, zoom-blur, wipe de blocos), zero fades; o corte cai na sílaba tónica; uma única pausa longa antes do pagamento final.

**Movimento — a série tem de ser fluida, não um slideshow.** Aplica tudo isto (está em `vince/CONTEXTO.md` §7B e não precisa de desenhos novos):
respiração contínua no corpo (escala 1,000→1,012 em 2,4 s, sempre a correr) · deriva de câmara de 1–2 % ao longo de 10 s · pose nova entra 3 % maior e assenta em 120 ms com desaceleração · cabeça e braço movem-se 60–80 ms depois do corpo · boca sincronizada à sílaba, fechada nas pausas · piscar de dois quadros a cada 4–6 s e sempre antes de uma pose de reação · fio do telefone a baloiçar 0,6 s quando o auscultador sai · número do painel a contar em 0,8 s · cortes na batida da música.

**7. Critérios de aceitação**

Gancho falado e escrito até aos 3 s · nenhum número no ecrã sem fonte, data e a nota de estimativa · **nenhum trecho acima de 1,5 s sem acontecimento visual** · nenhuma tipografia por cima da carta · no máximo um flash de ecrã inteiro a cada 4 s · lábios em sincronia nas três bocas · a mesma cara em todos os planos · sem corte lateral · 30–45 s · −14 LUFS (±0,5) · capa legível a 25 % do tamanho · nenhuma frase que recomende comprar ou vender.

**8. Entregáveis**

`MultiverseCapital_EpNN_<tema>_916.mp4` · capa · legenda limpa (gancho, uma frase de facto, fontes, **linhas fixas "Isto não é conselho de investimento." e "Vince Vault e a Multiverse Capital são personagens fictícios."**, convite para escanear a pasta no BINDER Vision, até 5 hashtags, sem emojis) · comentário fixado com os números e os links · texto alternativo · ficha de factos · atualização de `comum/historico.md`, `STATUS.md` e da ficha do episódio em `vince/episodios/epNN_<tema>/`.

**9. Limites**

Não exponhas chaves. Nada destrutivo. Sem merge para `main` — trabalha em `vince/epNN-<tema>` e abre PR. Créditos de voz: só o Vinci, uma geração por fala, repetir no máximo uma vez e só se a pronúncia mudar o sentido; a Fonte não gasta nada. Se uma fonte cair, tenta uma segunda vez e segue com o que não depende dela. **Nunca declares o episódio concluído sem o MP4 final conferido, e nunca inventes um resultado.**

**10. Relatório final (até 300 palavras)**

Pauta escolhida e rejeitadas · os números com fonte, data e hora · o que mudou face a este prompt e porquê · créditos gastos · o que falhou · ficheiros entregues com caminho real.
