# AB-04 · Nauctis: os quatro decks de Commander (Reel ABISMO)

- **Pedido:** fundador, 20/11/2026 (09:28) — «Missão de produção — Nauctis: os quatro Commander decks»: Reel 9:16 sem narração, «Auction of Power», ~20,58 s, os quatro decks com identidades e estratégias anunciadas, sem inventar cartas e separando oficial de interpretação. Não publicar.
- **Público:** jogadores de Commander PT-BR que ainda não escolheram precon de Nauctis. **Objetivo:** guardar/comentar (pergunta de número). **Mensagem única:** os quatro decks já têm nome, cores e tema; as listas ainda não.
- **Formato:** Reel ABISMO, 48 batidas (20,57 s), modo novo `"modo": "decks"` do motor (mesmo fundo, vida, cartão, etiquetas, música, sons e assinatura). Medidor desligado (cartas sem camada). Sem voz, custo zero.
- **Pauta:** `memoria.py pauta --objeto "decks de Commander de Nauctis" --tema "os quatro precons de Nauctis"` → livre (20/11). Relação: AB-03 (só Terrors, comandantes) e AB-01 (Crucible, mesmo set).

## Gancho visual (§4.1)
1. **Quadro 0:** silhueta da carta da serpente (NAC 6) sob «OS 4 DECKS DE COMMANDER / DE NAUCTIS» e quatro pílulas «1 BANT · 2 SULTAI · 3 IZZET · 4 BOROS» com as cores.
2. **Objeto:** carta real do precon do abismo + as quatro identidades de cor.
3. **Ação:** a silhueta pisca e aproxima-se (zoom 1,00 → 1,08).
4. **Som:** descida na entrada do 1.º deck (1,71 s).
5. **Descoberta até 3 s:** são quatro decks, com estas cores; aos 1,71 s já entra o 1.º.
6. **Promessa:** ver o que cada um faz.
7. **Pagamento:** 1,71 s (Merfolk), 5,14 s (Terrors, carta real), **8,57 s (Blood in the Water no drop)**, 12,0 s (Seal), 15,4 s (grelha-resumo).

Rubrica prevista / medida (folha de contacto sem som): relevância 4/4 · impacto 3/3 · clareza 5/5 · curiosidade 4/4 · pagamento 5/5 · identidade 5/5. Impacto fica em 3: só um dos quatro decks tem carta revelada; três entram com espaço «?».

## Roteiro definitivo (sem voz; batidas da montagem = faixa + 44)
| Batida | Tempo | Ecrã | Som |
|---|---|---|---|
| 0 | 0,00 | Gancho: silhueta NAC 6 · «OS 4 DECKS DE COMMANDER / DE NAUCTIS» · pílulas 1–4 | intro |
| 4 | 1,71 | **DECK 1/4 · BANT** · MERFOLK REGIMENT · espaço «?» · OFICIAL · CAPTAIN HANNO COROLEAN · LEITURA · CONVOKE E IR LARGO · «Tritões de toda a história do Magic.» | descida |
| 12 | 5,14 | **DECK 2/4 · SULTAI** · TERRORS OF THE ABYSS · carta NAC 6 + crédito · OFICIAL · MONSTROS COLOSSAIS · VAZADO · NOME PROVISÓRIO · «Monstros marinhos voltam do cemitério.» | descida, glitch na etiqueta vermelha, swell |
| 20 | 8,57 | **DROP** · fundo passa a mestre (feixe aceso) · **DECK 3/4 · IZZET** · BLOOD IN THE WATER · espaço «?» com brilho · OFICIAL · SHREDMOUTH · OFICIAL · DESCARTE · LEITURA · DECK AGRESSIVO · «Tubarões atacam e criam fichas de Sangue.» | drop + descida |
| 28 | 12,00 | **DECK 4/4 · BOROS** · SEAL THE DEAL · espaço «?» · OFICIAL · GALLORTE · OFICIAL · GROUP HUG · LEITURA · VIDA POR TESOUROS · «Troque dor por Tesouro.» | descida |
| 36 | 15,43 | Grelha 2×2 · «LISTAS AINDA NÃO REVELADAS» · selo «LANÇAMENTO · 05/02/2027» · «QUAL VOCÊ QUER? / COMENTE 1, 2, 3 OU 4» | — |
| 44–48 | 18,86–20,57 | Assinatura BINDER Vision · Link na bio | cauda |

## Design (revisão pedida)
- **Hierarquia:** 1) carta ou espaço da carta; 2) nome do deck (Inter Display Black 104, duas linhas, mesma escala nos quatro); 3) pílula «DECK n/4 · guilda · cores»; 4) etiquetas; 5) legenda de ecrã Inter Display Black 58 com palavras-chave a amarelo.
- **Identidade por deck dentro do sistema:** só as cores de mana (pontos e filete do espaço da carta), legenda das cores por extenso. Esmeralda, tinta, amarelo e vermelho de condição mantêm a função de sempre.
- **Oficial × leitura:** etiqueta branca preenchida = oficial; vermelha = vazado/condição; **contorno branco sem preenchimento = leitura** (novo estilo, documentado em `abismo/IDENTIDADE.md`).
- **Legibilidade móvel:** nada abaixo de 21 px exceto o crédito da carta (19 px, padrão do motor); textos com contorno tinta; zonas seguras topo 236 / base 1640 respeitadas.
- **Ritmo:** cada deck dura 8 batidas (3,43 s); entra a deslizar 0,25 s, etiquetas às batidas +2/+3/+4, sai 0,16 s antes do próximo; nenhuma transição além do glitch de 2,5 quadros nas entradas e no drop.

## Controlo de qualidade (ficheiro final)
- `ffprobe`: 1080×1920, 30 fps, H.264 / AAC 48 kHz, 20,57 s. Loudness −14,1 LUFS, pico −1,8 dBTP. Cortes da música em batidas inteiras (44–64, 64–92).
- Folha de contacto (0; 1,75; 3,4; 6,4; 8,6; 9,0; 10; 12,9; 13,5; 15,5; 17,2; 17,9; 19,5 s): gancho legível no quadro 0; títulos, pílulas, etiquetas e legenda sem sobreposição; crédito visível sempre que a carta está no ecrã; assinatura com o logótipo oficial.
- v1 → v2 (stills): título encostado ao espaço da carta e nota «Wizards ainda não mostrou…» por baixo das etiquetas → carta 0,44 da largura, etiquetas a y 1340; pílulas do gancho invisíveis no quadro 0 e guilda sobre os pontos → visíveis desde o quadro 0, largura corrigida; texto do espaço «?» proporcional na capa.
- Capa: «OS 4 DECKS / DE NAUCTIS», sub «COMMANDER · O QUE JÁ FOI REVELADO», grelha 2×2 (carta real no Terrors, «?» nos outros) toda dentro do recorte 3:4 (y 240–1680); crédito da carta no fundo da capa 9:16.
- Regressão: AB-03 renderiza stills e capa sem diferenças com o motor alterado (assinatura extraída para função, comportamento igual).
- Factos do ecrã = `fontes.md`. Português do Brasil.

## Limitações reais
- Só um dos quatro decks tem carta pública; as outras três posições mostram «?» (decisão honesta, não falha). Quando a Wizards revelar comandantes, basta pôr `"carta"` no deck do `post.json` e voltar a renderizar.
- As cores vêm das caixas (relato da Wargamer); a página da Wizards não as escreve.
- Sem fecho do scanner (`comum/outro`): o Reel ABISMO usa a própria assinatura, como AB-01 e AB-03.

## Ficheiros finais (não versionados)
- `abismo/publicacoes/AB-04-nauctis-decks-reel/saida/AB-04-nauctis-decks-reel_reel.mp4` e `_capa.png`
- Recriar: `python3 -I abismo/motor/abismo.py abismo/publicacoes/AB-04-nauctis-decks-reel` (custo zero).
