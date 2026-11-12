# Checklist de qualidade · BINDER Originals

Transversal. Cada `PERFIL.md` acrescenta os seus critérios. Proporcional ao risco: peça simples usa só os itens que se aplicam.

**Gravidade** (pedido do fundador, 02/11/2026): **P0** impede publicação (os "Defeitos bloqueadores" abaixo) · **P1** problema importante de qualidade: corrige-se antes de publicar ou o fundador aceita-o por escrito · **P2** refinamento opcional. Um episódio só está aprovado sem P0 e com os P1 corrigidos ou aceites.

**Passo automático:** `python3 -I comum/qc/qc_video.py VIDEO.mp4 --frente <frente>` (formato, duração, loudness, pico, fecho, cortes, folha de contacto com zona segura). Não dispensa o olho no bloco E.

## A. Antes de produzir

- [ ] Série, classe de conteúdo e objetivo identificados (ficha, Etapa 1).
- [ ] A pauta pertence ao território da série (perfil · "Fora do território").
- [ ] Proposta de valor numa frase.
- [ ] Auditoria de originalidade: `memoria.py pauta` livre (ou decisão do fundador registada) e linha no `comum/REGISTRO_EDITORIAL.md`; egg não repete `comum/easter_eggs.md`.
- [ ] Fontes necessárias acessíveis; se não, plano de bloqueio (constituição §11).
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
- [ ] Vídeo termina com `comum/outro/outro_binder_916.mp4`, sem encurtar (exceto Órbita e exceções registadas).
- [ ] Legenda termina com "baixe o BINDER Vision"; até 5 hashtags; sem emojis.
- [ ] Comentário fixado: pergunta fácil + complemento (+ "Tem um detalhe escondido. Diga o segundo." se houver easter egg).
- [ ] Texto alternativo escrito (descrição + texto do ecrã).
- [ ] Easter egg (0 ou 1) registado.
- [ ] Encerramento (`SHOWRUNNER.md` §6): `memoria.py encerramento <ID>` OK, registo e histórico atualizados, commit conferido no GitHub. Nenhum vídeo.

## E. Personagens, cena e montagem (ficheiro final, na folha de contacto)

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

1. Facto, número, citação ou jogada inventados ou sem fonte.
2. Função, tela ou número do app inventados; tela do app redesenhada.
3. Corte lateral ou carta cortada/tapada.
4. Falta o fecho do scanner.
5. Voz ou música sem licença comercial.
6. Imagem de transmissão de torneio ou de terceiros sem autorização.
7. Humor contra uma pessoa real identificável.
8. Segredo ou dado pessoal no vídeo ou no repositório.

## Melhorias opcionais (não bloqueiam)

Ritmo de um bloco, escolha de palavra, variação de CTA, detalhe visual extra, capa alternativa.

## D. Depois de publicar

- [ ] Números do Insights em `comum/insights/` (facto ≠ interpretação; impulso A CONFIRMAR até confirmação).
- [ ] Uma aprendizagem acionável, ou "nenhuma" se não houver.
- [ ] Previsões do TUBO revistas quando o evento acabar.
