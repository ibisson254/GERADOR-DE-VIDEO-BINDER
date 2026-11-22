# MB-EP16 · auditoria audiovisual da prévia v1 e direção da v2 (22/11/2026)

Estado do episódio: **EM PRODUÇÃO · prévia sem voz** (não muda). A v2 é uma **versão de teste**; a v1 (`../episode.js`, `../episode.json`) fica intacta. Roteiro de 12 falas: **PROPOSTA DE REVISÃO — AGUARDA APROVAÇÃO DO FUNDADOR**. Zero créditos.

## 1. Auditoria da v1 (vídeo de 47,80 s, quadros em 1080×1920)

| Momento | Problema observado | Impacto | Origem no motor | Alteração | Prioridade |
|---|---|---|---|---|---|
| 7,3–10,8 · 14,1–16,7 · 20,5–22,4 · 25,3–27,0 · 31,0–33,9 · 38,2–41,8 s (planos `cuB`) | Insert de 300×419 px por cima e ao lado da cabeça do Burn, com a carta reduzida a ~110 px dentro do painel | carta ilegível no telemóvel; disputa a atenção com o rosto na piada | `EP.inserts` + CSS `#ins img{width:300px}`, posição fixa x 615 / y 330 em `render()` | sem inserts: a reação fica com o rosto; a prova passa para o plano de prova | bloqueador |
| 3,9–7,3 · 10,8–14,1 · 16,7–20,5 · 27,1–31,0 · 33,9–38,2 s (`tvtext`) | carta dentro da TV a ~500 px de largura, ao lado do medidor e das manchetes; 40 % de baixo do quadro vazio | texto de regra pequeno; três elementos competem com a prova | `EP.canais` + plano `tvtext` (zoom máx. 1,506 na tela da TV) | plano de prova: carta inteira a 620 px e aproximação 1,6× ao texto, sobre a sala escurecida | bloqueador |
| todas as trocas de carta | a troca é um «zapping» com estática; trocar de carta e trocar de destaque na mesma carta parecem iguais | o espectador não percebe quando a conversa muda de carta | `canalState()` (burst/OSD); o `flip` do motor é rotação de canais a cada 0,42 s, não um flip de carta | flip 3D no eixo Y só quando muda a carta (Alexander → Rule of Law → Thousand-Year Elixir) | importante |
| falas 1, 3, 6, 10, 12, 13 | legenda em 3 linhas | tapa a cena e fica difícil de ler | `#sub` 840 px úteis a 47 px | legenda paginada (2 páginas de até 2 linhas) e falas mais curtas | importante |
| telas s01, i03, i05, c02, c04, c10, c12 | até 5 níveis de texto e carimbos por cima da arte | hierarquia confusa; carimbos tapam arte | `telas_alexander.py` | painéis com 3 níveis; nada por cima das cartas; a explicação vai numa faixa por baixo da carta | importante |
| 14,1–16,7 s | «2 EM 3» (probabilidade) | regra nova: sem probabilidades | `i05_sorteio` | removido | importante |
| planos `tvtext` | medidor «COMPRAM 4 / 1 APANHA» ao lado da carta | ruído na prova | `EP.tv.meter` | o medidor só aparece nos planos da TV (falas 1 e 11) | acabamento |
| planos do sofá | `#smallcard` (136×190 px, `const CARD`) na TV do fundo | é cenário, não prova | `tvSmallCard` | mantido (fundo, fora do rosto) | acabamento |
| créditos | 17 px Geist sobre fundo translúcido | legível a 1080×1920; nível 3 no telemóvel | `#cred` | mantido; nenhum crédito retirado | acabamento |

## 2. Direção da v2

- **Hierarquia:** carta em destaque quando a fala é sobre a carta ou a regra; rosto do Burn quando reage; texto de apoio numa única faixa por baixo da carta. Máximo três níveis por quadro.
- **Flip:** só quando muda a carta (falas 8 e 10). Mesma carta = muda o destaque (falas 2 → 4) ou entra a aproximação ao texto. Painéis (mesa de 4, ruling, desvirar) entram com corte seco.
- **Sequência:** 1 abertura (Alexander, «4 COMPRAM») → TV com a mesa de 4 · 2 prova Alexander, linhas «revela e compra», aproximação · 3 Burn · 4 prova Alexander, linhas do dano → painel «5 DE DANO num oponente aleatório» (exemplo) · 5 Burn · 6 painel da ruling com a ressalva destacada → painel «a mesa inteira vê» (Swords to Plowshares como exemplo) · 7 Burn · 8 flip para Rule of Law, linha destacada, aproximação, «1 MÁGICA POR TURNO · CADA JOGADOR» · 9 Burn · 10 flip para Thousand-Year Elixir → painel «virado → desvirado: ativa de novo» · 11 TV com A/B · 12 Mana.
- **Tipografia:** sem fontes novas (Bangers, Geist; Comic Neue só na assinatura). Amarelo #FFD84A para o principal, vermelho para alerta, verde para positivo.
- **Motor:** `kit/prova/patch_prova.py` (opcional, retrocompatível; ver `manaburn/LEIA-ME.md`). MB-EP15 conferido: quadros iguais píxel a píxel e mistura com o mesmo MD5.

## 3. Roteiro de 12 falas · PROPOSTA DE REVISÃO — AGUARDA APROVAÇÃO DO FUNDADOR

| # | Quem | Fala | Verificação |
|---|---|---|---|
| 01 | Burn | *Quatro* compram carta. E um oponente *aleatório* leva o dano! | Oracle TRC 81; «quatro» só no exemplo de mesa de 4 (escrito no ecrã) |
| 02 | Mana | *Lê a carta.* Ele vira: *cada jogador* revela o topo e *compra uma carta*. | Oracle ({T}: each player reveals… then draws a card) |
| 03 | Burn | Isso é *group hug*! Cadê a pegadinha? | opinião |
| 04 | Mana | O maior *valor de mana* revelado define o dano. E ele atinge um oponente *aleatório*. | Oracle (X = greatest mana value; random opponent) |
| 05 | Burn | Peraí… se eu revelar uma *remoção*, essa carta também vem pra minha mão? | pergunta |
| 06 | Mana | *Lê a ruling.* Na *maioria dos casos*, sim. E a mesa *inteira* vê. | ruling de 07/10/2026; revelar = mostrar a todos os jogadores. **Nota:** a ruling diz «exceto em casos muito raros»; «quase sempre» é mais fiel do que «na maioria dos casos». Mantive a formulação pedida; o painel traduz a ruling à letra |
| 07 | Burn | Então minha remoção já virou *conhecimento público*! | opinião |
| 08 | Mana | E *se* a Rule of Law estiver na mesa, cada jogador só conjura *uma mágica* por turno. | Oracle M20 35; condicional |
| 09 | Burn | *Uma só?!* Ou tiro o Alexander, ou faço a *minha jogada*?! | opinião; encurtada para caber em 2 linhas (original: «Gasto minha única mágica tirando o Alexander ou fazendo minha jogada?») |
| 10 | Mana | A habilidade do Alexander *não é mágica*. Se o dono *desvirar* ele, ativa *de novo*. | habilidade ativada não é mágica; custo {T}. «o dono» em vez de «você» para não parecer que quem desvira é o Burn |
| 11 | Burn | Isso não é group hug. É *ameaça com brinde*! *A*: encaro. *B*: troco de deck. | opinião + pergunta A/B (= comentário fixado) |
| 12 | Mana | Comenta aí. | — |

Não se afirma que Rule of Law está em todas as listas, nem combo, nem estatística. Nenhuma faixa de voz gerada.

## 4. Prévia v2 e controlos (22/11/2026)

Prévia sem voz: `MB_EP16_V2_PREVIA_SEM_VOZ_FECHO_916.mp4` (44,70 s com o fecho; 40,83 s sem ele), entregue na conversa, não versionada. **Não publicável.**

| Controlo | Resultado |
|---|---|
| 1080×1920, 30 fps | OK (`ffprobe` e `qc_video.py`) |
| `bordas.py` (TV) | OK: 830 quadros de TV, laterais 58–804 px |
| Carta do plano de prova | centrada, x 230–850 (`w: 620`), inteira antes de cada aproximação; a aproximação é recortada pela janela do plano |
| `kit/v3/check_quadro.py` | OK: todas as trocas de expressão do Conde caem num corte |
| Flip só na troca de carta | OK: falas 5 (Alexander → Swords, exemplo), 8 (→ Rule of Law), 10 (→ Thousand-Year Elixir); falas 2 → 4 mesma carta sem flip; painéis com corte seco |
| Renovação visual ≤ 3 s | OK no plano: maior intervalo ~2,8 s (fala 7, reação do Burn); falas longas com aproximação, painel ou troca a meio |
| Quadro 0 com Magic sem áudio | OK: Alexander inteiro, linha destacada, selo «4 COMPRAM» |
| Legendas | máx. 2 linhas por página; nenhuma sobre carta ou rosto (nos `cuB` ficam sobre o tronco) |
| Créditos | presentes em todas as cartas e painéis; Swords com crédito próprio |
| Retrocompatibilidade do motor | MB-EP15: quadros iguais píxel a píxel; `trilha_final.wav` com o mesmo MD5 |
| 2.ª auditoria (quadros em tamanho real) | corrigido: caixas de destaque sobrepostas cortavam o texto na aproximação → um bloco por frase |
| Áudio | **PENDENTE (não aplicável à prévia):** −17 LUFS e pico −0,7 dBTP, só música e efeitos, sem vozes. A versão final tem de ficar em −14 LUFS e pico < −1 dBFS |

Pendentes do fundador: aprovar (ou não) a direção v2 e o roteiro de 12 falas; decidir «na maioria dos casos» × «quase sempre» (fala 6); autorizar as vozes; decidir se o plano de prova passa a padrão da série (hoje é opcional).
