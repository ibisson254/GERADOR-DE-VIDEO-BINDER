# Checklist de qualidade · BINDER Originals

Transversal. Cada `PERFIL.md` acrescenta os seus critérios. Proporcional ao risco: peça simples usa só os itens que se aplicam.

**Gravidade** (02/11/2026, consolidada a 19/11/2026):

| Nível | O que é | Consequência |
|---|---|---|
| **P0 · Bloqueador** | Erro factual ou informação inventada; identidade incorreta (voz, trilha, personagem, fecho ou nome de outra frente); direitos (licença, autorização, crédito); corte lateral; áudio defeituoso. Lista medível em «Defeitos bloqueadores» | Não se publica. Nem o fundador o aceita por escrito: corrige-se |
| **P1 · Correção obrigatória** | Problema relevante de narrativa, legibilidade, ritmo, enquadramento, som ou retenção (itens marcados P1) | Corrige-se antes de publicar ou o fundador aceita-o por escrito, com a razão na ficha |
| **P2 · Melhoria** | Polimento visual, microanimações, pequenos ajustes de ritmo ou acabamento | Opcional; regista-se se ficar para o próximo |

Um conteúdo só está aprovado sem P0 e com os P1 corrigidos ou aceites. **Nenhuma média, nota de rubrica ou desempenho noutro critério compensa um P0.** Os critérios são medidos (segundos, píxeis, LUFS, sim/não), nunca adjetivos («bonito», «cinematográfico», «profissional»).

**Passo automático:** `python3 -I comum/qc/qc_video.py VIDEO.mp4 --frente <frente>` (formato, duração, loudness, pico, fecho, cortes, folha de contacto com zona segura). Não dispensa o olho no bloco E.

## A. Antes de produzir

- [ ] Série, classe de conteúdo e objetivo identificados (ficha, Etapa 1).
- [ ] A pauta pertence ao território da série (perfil · "Fora do território").
- [ ] Proposta de valor numa frase.
- [ ] Auditoria de originalidade: `memoria.py pauta` livre (ou decisão do fundador registada) e linha no `comum/REGISTRO_EDITORIAL.md`; egg não repete `comum/easter_eggs.md`.
- [ ] Fontes necessárias acessíveis **e números lidos antes de qualquer render** (nada de prévias com marcadores); se não, plano de bloqueio (constituição §11).
- [ ] Texto da voz cabe na duração da frente antes de gravar (orçamento de caracteres no perfil da frente); uma geração por fala, aprovada com o custo.
- [ ] Recursos do kit inspecionados e na versão atual.
- [ ] Estratégia proporcional (constituição §3, Etapa 2).
- [ ] Especial ou homenagem: constituição §14 (duração pela história, tom de celebração e legado, humor subtil quando couber, rigor intacto).

## B. Antes de exportar

- [ ] Tese sustentada pelas fontes; cada número com fonte e data.
- [ ] Texto de carta conferido no Oracle; regras não explicadas de memória.
- [ ] Factos, opiniões e previsões distinguíveis na fala ou no ecrã.
- [ ] Voz, ritmo, visual e humor da série (não de outra).
- [ ] Direitos: crédito de artista e Wizards, "conteúdo de fã não oficial", voz/música com licença.
- [ ] Nenhuma função do app fora da lista confirmada (constituição §9).

## C. Antes de entregar (ficheiro final, não prévia)

- [ ] Quadros do ficheiro final conferidos no formato da frente (9:16 ou 4:5), **sem corte lateral**, carta inteira.
- [ ] Legenda queimada dentro da zona segura e legível.
- [ ] Loudness medido no ficheiro final.
- [ ] Voz sem silêncio no início (o gancho visual corre por baixo da primeira fala) e trilha a tocar por baixo do fecho até ao fim (o fecho não tem áudio próprio).
- [ ] Folha de fotogramas conferida antes do render final; um render final por versão.
- [ ] Vídeo termina com `comum/outro/outro_binder_916.mp4`, sem encurtar (exceto Órbita e exceções registadas).
- [ ] Legenda termina com "baixe o BINDER Vision"; até 5 hashtags; sem emojis.
- [ ] Comentário fixado: pergunta fácil + complemento (+ "Tem um detalhe escondido. Diga o segundo." se houver easter egg).
- [ ] Texto alternativo escrito (descrição + texto do ecrã).
- [ ] Easter egg (0 ou 1) registado.
- [ ] Encerramento (`SHOWRUNNER.md` §6): `memoria.py encerramento <ID>` OK, registo e histórico atualizados, commit conferido no GitHub. Nenhum vídeo.

## E. Personagens, cena e montagem (ficheiro final, na folha de contacto)

- [ ] P0 · Feedback visual (15/11/2026): cada fala das personagens tem uma imagem real do que está a ser dito, na TV ou em insert; nenhuma tela «FOTO EM FALTA» no ficheiro a publicar.
- [ ] P1 · Quadro 0 com imagem de Magic (carta ou objeto reconhecível). No Meta em Curto é P0 (item seguinte, decisão de 16/11).
- [ ] P0 (Meta em Curto) · Quadro 0 com cartas reais em ecrã inteiro e revelação principal nos primeiros 3 s (`oraculo/CONTEXTO.md` §7). Falhou = não sai.
- [ ] P1 · Toda leitura de regra mostra a carta com a linha destacada.
- [ ] P0 · Carta inteira nos planos de TV e nos zooms.
- [ ] P1 (a confirmar pelo fundador) · Na TV ao fundo dos planos de conjunto, carta e programação não aparecem cortadas pela margem.
- [ ] P1 · Nenhum texto (legenda, gancho) por cima de rosto, carta ou linha de fonte.
- [ ] P1 · Linha de fonte com ≥ 24 px de altura no ficheiro final; texto que se quer ler ≥ 28 px.
- [ ] P1 · Legendas e textos dentro da zona segura (folha de contacto: fora do vermelho).
- [ ] P1 · Personagens inteiros ou cortados por um enquadramento intencional (sem cabeças soltas a espreitar).
- [ ] P1 · Personagens no modelo dos recursos mestres (rosto, proporções, roupa, cores); nada regenerado.
- [ ] P1 · Quem ouve reage: nenhuma pose ou expressão repetida para emoções diferentes; olhares coerentes com quem fala.
- [ ] P1 · Assinatura da série no fim (ex.: TV desliga → ponto verde no Mana & Burn), depois o fecho.
- [ ] P2 · Nenhum plano parado mais de ~5 s sem mudança de enquadramento ou de expressão.
- [ ] P2 · Continuidade do cenário entre planos (objetos, luz, posição da TV).
- [ ] P1 · Mana & Burn: luz do cenário presente (sala v3), sem costuras à volta da TV, das legendas ou da tarja; tela da TV e carta iguais à versão sem luz.
- [ ] P1 · Mana & Burn: áudio do ficheiro final igual ao da montagem (a luz não recodifica o áudio).

## Defeitos bloqueadores (não publicar)

Todos P0.

1. Facto, número, citação ou jogada inventados ou sem fonte; cálculo do BINDER apresentado como dado da fonte.
2. Função, tela ou número do app inventados; tela do app redesenhada.
3. Corte lateral ou carta cortada/tapada (conferido em quadros do ficheiro final).
4. Falta o fecho do scanner (exceto Órbita, Expedição com fecho próprio de 14/11 e exceções registadas em especiais).
5. Voz ou música sem licença comercial.
6. Imagem de transmissão de torneio ou de terceiros sem autorização.
7. Humor contra uma pessoa real identificável.
8. Segredo ou dado pessoal no vídeo ou no repositório.
9. Identidade incorreta: voz, trilha, personagem, cenário ou fecho de outra frente; personagem regenerado em vez do recurso mestre; nome de carta, artista, jogador ou série errado no ecrã ou na legenda.
10. Áudio defeituoso: clipping audível ou pico ≥ 0 dBFS; estalo, corte ou silêncio não intencional; voz trocada, cortada a meio de palavra ou ininteligível; dessincronia visível entre fala e legenda. (Loudness fora de −14 ± 1 LUFS ou pico ≥ −1 dBTP é P1, como mede o `qc_video.py`.)
11. Parceria ou colaboração afirmada sem autorização registada; crédito de autoria de dados ou de obra em falta.
12. Gancho que promete algo que o vídeo nunca paga (rubrica: Pagamento = 1).

## F. Gancho e narrativa (briefing e ficheiro final; `SHOWRUNNER.md` §4.1 e §4.2)

- [ ] P1 · Os 7 campos do gancho preenchidos na ficha antes do roteiro (quadro 0, objeto, ação, som, descoberta até 3 s, promessa, pagamento).
- [ ] P1 · Quadro 0 mostrado em miniatura e sem som: o assunto percebe-se.
- [ ] P1 · Nenhum logótipo, título da série ou apresentação antes da evidência visual (as aberturas das bíblias correm por cima dela).
- [ ] P1 · Descoberta ou pergunta clara até aos 3,0 s (medido no ficheiro final).
- [ ] P1 · Pagamento no segundo previsto no campo 7 (± 3 s) ou desvio explicado na ficha; nunca pago = P0 (bloqueador 12).
- [ ] P1 · Maior intervalo sem mudança visual ≤ 3 s, medido nos cortes do `qc_video.py` (exceto o loop do Órbita).
- [ ] P1 · Rubrica medida na ficha; nenhuma nota ≤ 2 em Relevância, Clareza ou Identidade.
- [ ] P1 · Revisão narrativa da §4.2 sem «não» (tese, progressão, evidência, recompensa, CTA único).
- [ ] P2 · Som do gancho dentro da biblioteca da frente e sem pico acima do resto da mistura.

## Melhorias opcionais (não bloqueiam)

Ritmo de um bloco, escolha de palavra, variação de CTA, detalhe visual extra, capa alternativa.

## D. Depois de publicar

- [ ] Números do Insights em `comum/insights/` (facto ≠ interpretação; impulso A CONFIRMAR até confirmação).
- [ ] Uma aprendizagem acionável, ou "nenhuma" se não houver.
- [ ] Previsões do TUBO revistas quando o evento acabar.
