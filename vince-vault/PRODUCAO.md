# Vince Vault · direção de animação e plano de produção (proposta)

Versão 0.1 · 07/11/2026 · **proposta, não ativa**. Marcas [CONFIRMADO]/[PROPOSTA]/[HIPÓTESE]/[PENDENTE]: ver `PROPOSTA.md`.

**[CONFIRMADO]** Meta: **um episódio por semana**. Nada aqui é dimensionado para mais.

## 1. Ferramentas efetivamente disponíveis (verificado a 07/11/2026)

| Ferramenta | Estado nesta sessão | Serve para |
|---|---|---|
| Python 3 + Pillow + numpy | Disponível | Recortes, composição, gráficos, scripts do radar |
| ffmpeg | Disponível | Áudio, montagem, loudness |
| Node 22 + Playwright/Chromium (padrão do kit do Mana & Burn) | Disponível no padrão do estúdio | Render HTML → MP4 da cena animada |
| `comum/qc/qc_video.py` | No repositório | Controlo de qualidade automático |
| ElevenLabs (vozes) | Ligado | Voz de Vince e do assistente **com créditos autorizados pelo fundador** |
| ElevenLabs (imagem, vídeo, música) | **Não disponível**: o conector desta sessão recusa nós de imagem, vídeo e música (descrição da própria ferramenta) | — |
| Geração de imagem pelo Claude | **Não existe**: o Claude escreve código (SVG, HTML, CSS, Python), não gera imagens 3D nem fotografias | — |
| vidIQ (geração de vídeo, b-roll, motion graphics) | Ligado, **não testado**: gasta créditos e não garante consistência da personagem | Eventual opção D, só com autorização |
| Blender | Não instalado no ambiente | Só seria preciso na opção A |
| Rhubarb Lip Sync | Não instalado; ferramenta de linha de comando aberta que gera bocas a partir de áudio ([repositório](https://github.com/DanielSWolf/rhubarb-lip-sync)) | Sincronização labial da opção C |

**O que o Claude consegue executar:** roteiro, pesquisa e verificação de preços (web), cálculo das variações, boletas e gráficos, recorte e montagem das camadas da personagem a partir de imagens fornecidas, a cena animada em HTML, o render, a mistura, o QC e o pacote de publicação. **O que não consegue:** criar a imagem-mestra da personagem em estilo 3D cartoon. Essa etapa exige uma ferramenta visual externa.

## 2. Avaliação técnica das alternativas

Escala: ●●● bom · ●● aceitável · ● fraco.

| Critério | A. 3D com rig completo | B. 3D com animação limitada (vídeo gerado por IA por plano) | C. 2.5D com poses e camadas reutilizáveis | D. Híbrido (C + clipes curtos gerados) |
|---|---|---|---|---|
| Consistência facial | ●●● (modelo único) | ● (a cara deriva entre gerações) | ●●● (mesmos pixéis sempre) | ●● (os clipes podem derivar) |
| Qualidade visual | ●●● | ●● | ●● (bonito parado; movimento limitado) | ●●● nos momentos-chave |
| Sincronização labial PT-BR | ●● (exige rig facial e trabalho) | ● (ferramentas de lip-sync pagas, resultado variável) | ●● (6–9 bocas + Rhubarb ou energia do áudio) | ●● |
| Tempo de render | ● (horas) | ●● (fila do serviço) | ●●● (minutos, local) | ●● |
| Facilidade de atualizar números | ●● | ● (texto gerado por IA não é legível) | ●●● (HTML editável até ao fim) | ●●● |
| Custo inicial | ● (modelação, rig, ou encomenda) | ●●● | ●● (pacote de imagens, uma vez) | ●● |
| Custo por episódio | ●● (tempo) | ● (créditos por segundo) | ●●● (só voz e tempo) | ●● |
| Limites reais | Exige perícia em Blender que o estúdio não tem hoje | Não escreve dados; cada plano é uma aposta | Movimento menos fluido | Mais uma ferramenta paga |
| 1 episódio/semana sustentável | ● | ● | ●●● | ●● (depois de C estável) |

**[PROPOSTA] Recomendação: C agora; D como evolução opcional depois da validação; A só se a série crescer e houver orçamento.**

Porquê: C entrega o aspeto "cartoon 3D" (vem das imagens do pacote), a consistência total e números sempre editáveis, com o mesmo motor que o estúdio já domina (HTML + Playwright + ffmpeg, kit do Mana & Burn). O que se perde é fluidez; compensa-se com câmara (zooms, empurrões, tremor), troca rápida de poses, squash nos gestos e o ritmo do bate-volta com o assistente. B não serve como base: não escreve números legíveis e cada plano pode mudar a cara do Vince. A é a melhor qualidade, mas é a pior escolha para um estúdio de uma pessoa com um episódio por semana.

## 3. Ferramenta visual externa (etapa única do pacote)

**[PENDENTE]** Escolha e custo são do fundador. Critérios para escolher:
1. Gera personagem em estilo cartoon 3D estilizado a partir de texto.
2. Aceita **imagem de referência da personagem** para gerar as outras vistas e expressões com a mesma cara.
3. Permite **edição localizada** (trocar só a boca ou os olhos) para as bocas e expressões.
4. Licença de uso comercial no plano usado.
5. Exporta em alta resolução (≥ 2048 px no lado maior).

Não se gastam créditos nem se assina nada sem autorização (AGENTS.md §3). Os prompts estão prontos em `CHARACTER_PACK.md` §9.

Alternativa sem custo de ferramenta **[HIPÓTESE]**: encomendar a um ilustrador o pacote de camadas (paga-se uma vez; consistência garantida; prazo maior). Fica registada como opção.

## 4. Como funciona a opção C (desenho técnico para a fase 0)

- **Kit próprio em `vince-vault/kit/`** (a criar na fase 0), copiando a estrutura do kit do Mana & Burn (cena HTML, `episode.json`, `process.py`, `render.py`) **sem alterar nenhum ficheiro de `manaburn/`**.
- **Camadas** (detalhe em `CHARACTER_PACK.md` §6): corpo por pose, cabeça, olhos, sobrancelhas, bocas, braços de gesto, adereços. A cena troca camadas por evento.
- **Sincronização labial [HIPÓTESE, a testar no piloto]:** Rhubarb com o reconhecedor fonético (independente da língua) sobre a faixa de voz de Vince; se o resultado em português não convencer, plano B: três bocas (fechada, meia, aberta) guiadas pela energia do áudio.
- **Assistente:** só áudio + impressora + objetos que entram de fora de campo. Nenhum asset de corpo.
- **Dados:** boleta em HTML (papel de formulário contínuo), painel de cotações em HTML, gráficos simples gerados por script a partir da ficha de fontes. Nada de números dentro de imagens geradas.
- **Cenário:** um plano-mestre do escritório (imagem do pacote) + 3 enquadramentos fixos tirados dele (conjunto, Vince à secretária, impressora/painel). Mesma lógica de cenário-mestre proposta para o Mana & Burn na auditoria de 02/11.
- **Fecho:** `comum/outro/outro_binder_916.mp4`, sem alterações.
- **QC:** hoje `comum/qc/qc_video.py` só aceita `--frente manaburn|tubo|conde|orbita|lambe`. Até à ativação, usar `--frente manaburn` (mesmo formato 9:16, 30 fps, com fecho); acrescentar a entrada `vince` ao script só quando a série for ativada.

## 5. Pipeline semanal (um Reel)

Tempos são **[HIPÓTESE]** até ao piloto; medem-se e registam-se.

| # | Etapa | Quem | O quê | Tempo estimado |
|---|---|---|---|---|
| 1 | Pesquisa semanal (radar) | Claude | MTGGoldfish semanal + Cardmarket + TCGplayer; aplica os filtros de `PERFIL.md`; 3–5 candidatos | 30–60 min |
| 2 | Verificação | Claude; fundador onde o site bloqueia leitura automática | Confirmar vendido × anunciado, nº de vendas, 2 mercados, causa com fonte; preencher `epNN_fontes.txt` | 30–60 min |
| 3 | Escolha da pauta | **Fundador** | Aprova 1 de 3 propostas (uma linha cada) | 5 min |
| 4 | Roteiro | Claude → **fundador aprova** | Roteiro dentro da fórmula de `CONTEXTO.md` §10; boleta; pergunta ▲/▼ | 30 min |
| 5 | Voz | **Fundador autoriza créditos**; Claude prepara as faixas | ElevenLabs: Vince + assistente; ouvir pronúncias (Vault, nomes de cartas) | 20–40 min |
| 6 | Animação | Claude | `episode.json`, poses por fala, bocas, eventos de impressora/painel | 30–60 min |
| 7 | Montagem | Claude | Mistura -14 LUFS, trilha, SFX, fecho do scanner | 15 min |
| 8 | Controlo de qualidade | Claude + **fundador vê no telemóvel** | `qc_video.py`, bordas, zona segura, checklist P0/P1/P2, critérios do perfil | 15–20 min |
| 9 | Pacote de publicação | Claude → **fundador publica** | Legenda (termina com "baixe o BINDER Vision"), comentário fixado ▲/▼ com fontes, texto alternativo, ficha, histórico | 20 min |

**Janela de dados [PROPOSTA]:** "semana de mercado" = 7 dias que terminam no dia da recolha, dita no ecrã. Recolha 1–2 dias antes da publicação para os números não envelhecerem.

**Reutilizável de episódio para episódio:** pacote da personagem, cenário, kit, trilha, SFX, layout da boleta, scripts do radar, modelo de legenda e de comentário. **Novo em cada episódio:** dados, roteiro, vozes, imagem da carta (Scryfall), `episode.json`.

**Automatizável [PROPOSTA, fase 1]:** `vince-vault/ferramentas/radar.py` que lê os ficheiros públicos (guia de preços do Cardmarket, MTGJSON) e devolve os candidatos filtrados. Só se constrói depois de confirmados os termos de uso e de 2–3 episódios manuais mostrarem que a etapa 1 é o gargalo (constituição §8: automatizar só o que se repete). Nada de infraestrutura antes disso.

**Sempre humano:** aprovar pauta e roteiro, autorizar créditos, ouvir a voz, ver no telemóvel, publicar, enviar o print semanal do Insights.

## 6. Viabilidade com o Claude Pro

Factos (Central de Ajuda da Anthropic, consultada a 07/11/2026):
- O plano Pro tem um limite por sessão de cinco horas e um limite semanal que se aplica a todos os modelos ([O que é o plano Pro](https://support.claude.com/en/articles/8325606-what-is-the-pro-plan)).
- O uso do Claude Code conta para os mesmos limites do Claude ([Uso do plano Pro](https://support.anthropic.com/en/articles/8324991-about-claude-s-pro-plan-usage)).
- A Anthropic não publica um número de mensagens; o consumo depende do tamanho da conversa, dos ficheiros, das ferramentas e do modelo.

Leitura **[HIPÓTESE]**: um episódio por semana, feito num chat próprio (constituição §8: 1 chat = 1 entrega), cabe no Pro se o render e a pesquisa forem feitos por scripts e não página a página na conversa. Não há forma honesta de prometer uma quantidade. **[PROPOSTA]** No piloto, anotar na ficha o consumo visto em Definições › Uso antes e depois do episódio; com 2–3 medições sabe-se a margem real. O mesmo plano serve as outras 6 séries da semana: o Vince não pode ser o episódio mais caro em uso.

| Pergunta | Resposta |
|---|---|
| Pode ser feito com o Claude | Pesquisa, verificação, cálculo, roteiro, boletas, cena animada, render, mistura, QC, pacote, registo no repositório |
| Exige ferramenta visual externa | Imagem-mestra e expressões da personagem (uma vez); eventuais clipes da opção D |
| Pode ser automatizado | Radar de candidatos; geração do `episode.json` a partir do roteiro; QC; legenda a partir da ficha |
| Precisa de intervenção humana | Aprovações, créditos, escuta, publicação, Insights; verificação em sites que bloqueiam leitura automática |
| Reutilizável | Pacote, cenário, kit, trilha, SFX, layouts, modelos |

## 7. Custos e gargalos

| Item | Tipo | Estimativa |
|---|---|---|
| Pacote da personagem (ferramenta de imagem ou ilustrador) | Único | **[PENDENTE]** depende da ferramenta escolhida; não se gasta sem autorização |
| Voice Design de 2 vozes + trilha | Único | Créditos ElevenLabs do plano do fundador |
| Vozes por episódio | Semanal | Créditos ElevenLabs (~1 minuto de fala por episódio, mais repetições de pronúncia) |
| Claude Pro | Já existente | Partilhado com as outras séries |
| Opção D (clipes gerados) | Semanal, opcional | Só depois da validação e com orçamento aprovado |

**Gargalos prováveis:**
1. **Verificação de preço vendido**: sites que bloqueiam leitura automática obrigam a consulta manual. Mitigação: ficheiros públicos (Cardmarket) e janela fixa.
2. **Consistência do pacote**: se a ferramenta de imagem não mantiver a cara, a fase 0 atrasa. Mitigação: critério 2 do §3; alternativa do ilustrador.
3. **Pronúncia** de "Vault" e de nomes de cartas em inglês. Mitigação: ficheiro fonético da série.
4. **Tempo do fundador** (aprovações, publicação) numa semana com 7 Reels.

## 8. Fase inicial de validação [PROPOSTA]

**Fase 0 · Construção (sem publicar)**
1. Fundador decide nome, empresa, ferramenta de imagem, vozes (`PROPOSTA.md` §8).
2. Gerar o pacote (`CHARACTER_PACK.md`), aprovar a imagem-mestra antes de tudo o resto.
3. Kit em `vince-vault/kit/`; teste de bocas (Rhubarb fonético × energia do áudio).
4. **Episódio 0 interno** com dados reais da semana, não publicado. Medir tempo por etapa e consumo do Pro.
5. Fundador aprova o episódio 0 → ativação (catálogo, `series.yaml`, perfil final).

**Fase 1 · Validação pública: 6 semanas, 1 episódio por semana**

Métricas por episódio (do print do Insights, registadas em `comum/historico.md`):
- Retenção média e percentagem de conclusão.
- Guardados e partilhas por 1.000 visualizações (métrica principal).
- Respostas ▲/▼ por 1.000 visualizações.
- Menções espontâneas a "Vaultinho" (contagem manual nos comentários).
- Visitas ao perfil e toques no link, quando o print os mostrar.
- Tempo de produção e consumo do Pro.

**Marcos de decisão (semana 6) [PROPOSTA; constituição §12: um resultado isolado não muda a estratégia]:**
- **Continuar a 1/semana** se a mediana de guardados+partilhas por 1.000 views estiver ao nível da mediana das outras séries no mesmo período e a produção couber no tempo semanal.
- **Rever o formato** se a retenção ficar abaixo das outras séries em 4 de 6 episódios.
- **Propor 2/semana** só se: métricas acima da mediana em 4 de 6 episódios, tempo de produção estável, margem no Pro, e **decisão expressa do fundador**. Nunca automático.

## 9. O que não se faz nesta fase

Nenhum ficheiro de outras séries alterado; nenhum `series.yaml` ativado; nenhum crédito gasto; nenhuma imagem gerada; nenhum vídeo renderizado ou commitado.
