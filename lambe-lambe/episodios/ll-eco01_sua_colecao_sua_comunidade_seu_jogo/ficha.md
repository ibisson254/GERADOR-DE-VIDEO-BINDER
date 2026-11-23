# LL-ECO01 · «Sua coleção. Sua comunidade. Seu jogo.»

Frente: Lambe-lambe (campanha de posicionamento do BINDER Vision). Pedido do fundador: 23/11/2026 (16:52), prompt «Binder Vision · vídeo de posicionamento» + «quero vídeo para story, reels e carrossel; pode usar cartas Secret Lair». Estado: **CONCLUÍDO; publicação com o fundador.** Zero créditos externos.

## Objetivo e mensagem
- Público: jogadores e colecionadores de Magic no Brasil e em Portugal que ainda não conhecem o app.
- Mensagem única: o BINDER não é só um organizador; é um ecossistema que liga coleção, comunidade e jogo, e é gratuito.
- Ordem de persuasão: identificação com Magic → valor (coleção) → dimensão social → jogo → marca → gratuidade e convite.
- Métrica principal: toques no sticker/link (`utm_campaign=LL-ECO01`) e contas novas na semana seguinte; secundária: partilhas do Reel.

## Gancho visual (SHOWRUNNER §4.1)
Objeto: carta Lightning Bolt (SLD 901, arte original de Christopher Rush) inteira, em tela cheia no quadro 0 (abertura de objeto, câmara recua em 0,6 s); selo/texto: «MAGIC É MUITO MAIS DO QUE… CARTAS.» colado aos 0,3 s e 0,95 s. Rubrica própria: 4/5.

## Peças entregues (não versionadas; recriam-se com os scripts)
| Peça | Duração / formato | Comando |
|---|---|---|
| Story | 16,0 s + fecho 3,87 = 19,87 s · 1080×1920 · 30 fps · H.264 · sem áudio (música no Instagram) | `python3 -I campanha.py video config.json LL-ECO01_story.mp4` |
| Reel com som | tempos ×1,15: 18,4 s + fecho = 22,27 s · efeitos sintetizados próprios, pico −6,0 dBFS | `… video config.json LL-ECO01_reel.mp4 --reel --audio` |
| Reel mudo | igual, sem áudio | `… video config.json LL-ECO01_reel_mudo.mp4 --reel` |
| Carrossel | 7 × 1080×1350 PNG | `… carrossel config.json <pasta>` |

## Guião (Story; o Reel é igual, 15 % mais lento)
| Tempo | Cena | Texto |
|---|---|---|
| 0–2,4 | Universo: Lightning Bolt em tela cheia; adesivos de localização, conversa e troféu | Magic é muito mais do que · cartas. |
| 2,4–5,3 | Coleção: Reliquary Tower + Mystical Tutor; ícone LigaMagic | Organize sua coleção. · Identifique suas cartas. · Exporte para a LigaMagic. |
| 5,3–7,9 | Comunidade: Command Tower, alfinetes, ondas de proximidade, avatares e balões simbólicos | Encontre jogadores perto de você. · Converse. Conecte-se. |
| 7,9–10,2 | Jogo: chaveamento desenhado a marcador (sem nomes), Lightning Bolt (SLD 83), troféu | Crie campeonatos. · Reúna a comunidade. Jogue. |
| 10,2–13,2 | Marca: cartaz preto BINDER; logos Magic, BINDER Vision, LigaMagic (ligada à exportação); nota de independência | Não é só um aplicativo. · É um ecossistema para quem vive [MAGIC] |
| 13,2–16,0 | Gratuidade e CTA: Generous Gift | Tudo isso, gratuitamente. · Conheça o BINDER Vision. · Beta para Android · Link na bio |
| 16,0–19,87 | Fecho oficial do scanner | — |

Easter eggs (comentário fixado): Reliquary Tower = sem limite de mão; Command Tower = ponto de encontro; Generous Gift = presente/grátis; Mystical Tutor de um ilustrador carioca (Mateus Manhanini); escondido: o Lightning Bolt de abertura é a arte original de Christopher Rush (Alpha) reeditada em Secret Lair.

## v2 · cartaz da marca verde-esmeralda e selo do Google Play (23/11/2026, 18h10)
Pedido do fundador (17:46): «Escolha outra cor que não seja o preto para servir de fundo [...] use logo oficial da Google play. Refine essa ideia.»
- Fundo do cartaz da marca (cena 5 do vídeo e slide 7): **verde-esmeralda** (papel kraft tingido de #10B981). É a cor da marca, contrasta com o muro rosa (complementar) e com o creme/kraft das outras cenas, e deixa o texto preto legível. O preto passa a etiqueta: Magic e BINDER Vision entram como autocolantes pretos colados no cartaz (os dois logótipos precisam de fundo escuro; nada é tingido nem redesenhado). «ECOSSISTEMA» em faixa preta.
- Selo oficial «Disponível no Google Play» (pt-BR): no slide 7 e por baixo da chamada para ação da cena 6; sem rotação, fita, textura ou sombra por cima. Nota de marcas atualizada com «Google Play e o logotipo do Google Play são marcas da Google LLC.»
- Selo: arte vetorial oficial do Google (EPS do kit de selos, variante pt-BR) via pacote npm `localized-responsive-google-play-badge` 1.0.2; o site de selos do Google não é acessível a partir da sessão. É o desenho de 2016 do logótipo Play; se o fundador quiser o PNG atual de play.google.com/intl/pt-BR/badges, basta substituir `comum/marcas/google_play_badge_ptbr.png`.
- Durações iguais (Story 19,87 s, Reel 22,27 s); QC igual ao da v1.

## v3 · capa a partir do slide da comunidade (23/11/2026, 18h30)
Pedido do fundador (18:06): «Quero essa imagem para usar de capa, coloque nas proporções exatas, e [...] algum elemento para que quando o seguidor olhar o Instagram fique com vontade de clicar.»
- Formatos: `LL-ECO01_capa_4x5_1080x1350.png` (1.º slide do carrossel, 4:5) e `LL-ECO01_capa_reel_1080x1920.png` (capa do Reel, 9:16, com tudo dentro do recorte 3:4 da grelha do perfil, y 240–1680; prévia `LL-ECO01_capa_grelha_3x4_previa.png`). Comando: `python3 -I campanha.py capa config.json <pasta>`.
- Grelha do perfil (18:23): o Instagram cortava os lados da capa 4:5; nova `LL-ECO01_capa_grelha_1080x1440.png` em 3:4 exato, com tudo dentro e margem nas bordas. É esta que se usa em «Cortar imagem do perfil».
- Elementos de clique (lacuna de curiosidade + recompensa, sem prometer nada que não exista): «?» dentro do alfinete (quem está perto?), nota a marcador rosa «quem joga perto de você?», selo amarelo «GRÁTIS» (confirmado pelo fundador) e, só no carrossel, «arrasta pro lado →». Nada sobre a arte nem sobre o rodapé da carta.
- Carrossel reordenado: comunidade (capa) → Magic é muito mais → coleção → LigaMagic → jogo → grátis → marca (7 slides; o antigo slide 4 passou a capa).
- Correção encontrada: os ícones dos autocolantes saíam meio fora do papel (camada SVG ancorada ao centro); corrigido em `caixa()`, vídeos re-renderizados.

## Materiais reutilizados
- Física de colagem do Story aprovado (`kit_story/motor_story.py`, 16/11): voo com aceleração, curvatura, impacto com mola, tremor de câmara, sombra projetada. Copiada para `campanha.py` sem alterar o motor.
- Muro rosa com restos dos modelos aprovados (`referencias/carrossel_padrao_01/02.png`), kraft, fita, carta com fita nos cantos de cima, faixa preta, fontes livres (`kit_carrossel/motor_padrao.py`, `compor.py`), sem alterações.
- Fundo do carrossel: `motor_padrao.fundo()` (modelo aprovado de 13/11).
- Fecho oficial `comum/outro/outro_binder_916.mp4`; lockup BINDER Vision tirado desse fecho (quadro de 3,0 s), sem redesenho.
- Logótipo Magic: `comum/marcas/magic_logo_recortado.png` (autorizado a 16/11). LigaMagic: ícone enviado pelo fundador a 23/11 (`comum/marcas/ligamagic_icone.jpg`).
- Não reutilizado: LL-LISA01 (outra frente), teaser do Sheoldred e peças pendentes de aprovação.

## Controlo de qualidade (`comum/qc/qc_video.py --frente lambe`)
- Story: 1080×1920, 30 fps, H.264, 19,87 s; fecho detetado a 16,0 s; P1 «sem faixa de áudio» esperado (regra do kit do Story).
- Reel: 22,27 s; fecho a 18,4 s; áudio −23,3 LUFS, pico −6,0 dBTP. O QC pede −14 LUFS; a regra do Lambe-lambe é efeitos com pico −6 dBFS e música escolhida no Instagram, por isso fica assim (P1 aceite, registado).
- Sem corte lateral: todas as peças compostas no canvas 1080×1920; câmara com zoom ≥ 1,025 (sem bordas pretas).
- Zona segura: textos principais entre 280 e 1500 px (cabe nos Stories e nos Reels); nota de independência a ~1505 px no Story (pode ficar perto da barra de resposta, é discreta de propósito).
- Cartas inteiras, sem filtros; fitas só nos cantos de cima; nenhum texto ou ícone sobre arte ou rodapé (ondas de proximidade limitadas ao lado esquerdo da Command Tower).
- Sem telas do app inventadas, sem mapas, perfis, conversas ou resultados: ícones conceituais e chaveamento vazio. A única tela real é o fecho do scanner.

## Revisão crítica (antes e depois das correções)
| Critério | v1 | Defeito encontrado | Final |
|---|---|---|---|
| Clareza do posicionamento | 7 | textos cortados (2.ª linha fora do papel) | 8 |
| Força do primeiro segundo | 6 | carta pequena num muro vazio | 8 (carta em tela cheia no quadro 0 e recuo) |
| Qualidade estética | 7 | cena 6 colada por cima do cartaz da marca (confusão) | 8 (cartaz novo na cena 6) |
| Compreensão das funcionalidades | 7 | «Exporte» tapado pela fita; «gratuitamente» sem ponto | 8 |
| Percepção de ecossistema | 8 | marca só 0,75 s em ecrã | 8 (marca 3 s) |
| Credibilidade | 7 | — | 8 (nota de independência; só funções confirmadas pelo fundador) |
| Potencial de partilha | 7 | — | 7,5: depende das cartas e dos easter eggs; é uma peça de marca, partilha menos que humor |
| Força do CTA | 8 | CTA partido em duas linhas | 8 |

Defeitos que ficam (honestos):
1. Partilha 7,5 (< 8): peças de posicionamento partilham-se pouco; a alavanca é o comentário fixado com os eggs. Não se força com mais efeitos.
2. Metade de baixo dos cartazes das cenas 2 e 3 fica com papel vazio (zona onde o Instagram põe a legenda/barra). Aceite para não pôr texto em zona insegura.
3. Risco de credibilidade do produto, não do vídeo: `PRODUTO.md` dizia que o Explorar e o chat com base pequena «contradizem a promessa». O fundador confirmou as funções; se o recém-chegado encontrar o feed vazio, a promessa «encontre jogadores perto de você» falha. Medir contas novas que abrem o Explorar/Chat.
4. Torneios no código estão no perfil de loja (Arena); «crie campeonatos» assume que qualquer utilizador consegue. Confirmado pelo fundador a 23/11; se for só para lojas, trocar a frase.
5. O Reel com efeitos fica a −23 LUFS (regra da frente). Se o fundador quiser publicá-lo sem música, normalizar a −14.

## Fontes e créditos
Cartas (Scryfall, imagens oficiais, © Wizards of the Coast): Lightning Bolt (SLD 901, Secret Lair Promo) · Christopher Rush; Reliquary Tower (SLD 7104) · Arthur Yuan; Mystical Tutor (SLD 334) · Mateus Manhanini; Command Tower (SLD 7029) · Dan Black; Lightning Bolt (SLD 83) · Noah Bradley; Generous Gift (SLD 369) · Ayako Ishiguro. Todas fora de Universes Beyond (`-is:ub`), para não usar personagens licenciados. Mateus Manhanini, ilustrador carioca: CCXP (ccxp.com.br/en/lineup/62) e Legião dos Heróis (2022).
Logótipos: Magic: The Gathering (Wizards of the Coast) e LigaMagic (titulares), uso autorizado pelo fundador a 23/11/2026 sem indicar parceria; BINDER Vision do fecho oficial.
Funções: confirmação expressa do fundador (23/11/2026) de que coleção, impressão, exportação LigaMagic, jogadores próximos, chat e campeonatos funcionam e são gratuitos; exportação «em lista ou CSV» em `binder-vision/PRODUTO.md`.

## Ficheiros finais
Vídeos (`LL-ECO01_story.mp4`, `LL-ECO01_reel.mp4`, `LL-ECO01_reel_mudo.mp4`), carrossel (`LL-ECO01_carrossel_01.png` a `_07.png`; capa = slide 1) e folhas de contacto entregues na conversa de 23/11/2026; não versionados (regra do estúdio). Recriam-se com os comandos da tabela «Peças entregues».

## Publicação (fundador)
1. Carrossel no feed com `legenda.txt`; fixar `comentario_fixado.txt`.
2. Reel (com som ou mudo + música da biblioteca) com a mesma legenda; capa = slide 1 do carrossel.
3. Story logo depois, com o sticker de `story_texto.txt` (`utm_campaign=LL-ECO01`).
Não publicar nada que sugira parceria com a Wizards ou a LigaMagic.
