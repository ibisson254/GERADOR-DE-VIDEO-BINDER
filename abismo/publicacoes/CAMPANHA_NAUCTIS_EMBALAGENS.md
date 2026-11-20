# ABISMO · Campanha Nauctis — embalagens oficiais (20/11/2026)

Missão de expansão editorial do fundador (20/11/2026, 10:05): correção pontual do AB-04 com as embalagens oficiais, 4 Stories individuais, 1 Story interativo e 1 carrossel. Nada publicado.

## Peças
| ID | Peça | Formato | Duração | Estado |
|---|---|---|---|---|
| AB-04 v2 | Reel «Os 4 decks de Commander de Nauctis» com as embalagens | Reel 1080×1920 | 20,57 s | CONCLUÍDO (alternativa; v1 intacto) |
| AB-05 | Story «Um exército que cresce nas profundezas» · Merfolk Regiment | Story 1080×1920 | 13,72 s | CONCLUÍDO |
| AB-06 | Story «As criaturas do abismo não ficam no cemitério» · Terrors of the Abyss | Story | 13,72 s | CONCLUÍDO |
| AB-07 | Story «Quando os tubarões atacam, o mar fica vermelho» · Blood in the Water | Story | 13,72 s | CONCLUÍDO |
| AB-08 | Story «No fundo do mar, até as negociações têm preço» · Seal the Deal | Story | 13,72 s | CONCLUÍDO |
| AB-09 | Story interativo «Qual desses decks você levaria para sua mesa?» | Story + caixa de perguntas nativa | 13,72 s | CONCLUÍDO |
| AB-10 | Carrossel «Nauctis: quatro decks, quatro identidades» | 5 slides 1080×1350 | — | CONCLUÍDO |

## Fase 3 · Auditoria do AB-04 (v1)
1. As quatro embalagens oficiais aparecem? **Não.**
2. Há espaços vazios com «?»? **Sim, três** (Merfolk, Blood, Seal).
3. A carta NAC 6 é imagem principal de mais de um momento? **Sim:** gancho (silhueta) e deck 2 — o Reel abria com o Terrors, desequilibrando os quatro produtos.
4. Hierarquia equilibrada entre os quatro? **Não:** só o Terrors tinha imagem real.
5. A capa apresenta os quatro produtos? **Não:** uma carta e três «?».
Erro factual adicional (P1): o v1 marcou «convoke» como LEITURA (está impresso na caixa: «TAP AND CONVOKE») e mostrou «LEITURA · VIDA POR TESOUROS», mecânica sem fonte. O v2 troca as etiquetas pelas chamadas impressas em cada caixa.
**Decisão:** v2 alternativo em `AB-04-nauctis-decks-reel-v2/` (vídeo `AB-04-nauctis-decks-reel-v2_reel.mp4`), v1 intacto. Preservados: 48 batidas / 20,57 s, «Auction of Power» (batidas 44–92), Blood in the Water no drop (batida 20), timeline, tipografia, sons e assinatura. Mudou só: gancho com as 4 caixas (sem a carta NAC 6), a caixa no lugar do «?»/carta, as etiquetas (chamadas da caixa), as miniaturas na grelha-resumo e a capa 2×2 com as caixas.

## Fontes (consultadas a 20/11/2026)
| Tipo | Fonte | O que sustenta |
|---|---|---|
| Oficial Wizards | «Collecting Nauctis: The Sunken Realm», 13/11/2026 — https://magic.wizards.com/news/feature/collecting-nauctis-the-sunken-realm | nomes dos 4 decks; 2 comandantes novos (face + featured) + 10 cartas novas por deck; Premium Edition em foil; NAC; imagens de produto padrão e Premium Edition |
| Oficial Wizards | Página do produto — https://magic.wizards.com/products/nauctis-the-sunken-realm | «Sharks, Merfolk, Abyssal Monsters, Seals» |
| **Texto impresso nas embalagens** | imagens de produto da Wizards (enviadas pelo fundador a 20/11, 1920×1080) | cores pelos símbolos de mana; chamadas: Merfolk Regiment «GO WIDE MERFOLK / TAP AND CONVOKE»; Terrors of the Abyss «DISCARD AND MILL / REANIMATE SEA MONSTERS»; Blood in the Water «SHARK ATTACKERS / DRAW BLOOD AND DISCARD»; Seal the Deal «GROUP HUG / TRADE PAIN FOR TREASURE»; «2 NEW FOIL MYTHICS» (padrão) |
| Descrição comercial dos produtos | listagens de venda, reproduzidas pelo Draftsim (16/11) — https://draftsim.com/?p=329851 | Captain Hanno Corolean; The Noble Serpent; Shredmouth (tubarões criam fichas de Sangue ao atacar); Gallorte («mercantile mastery») |
| Imprensa | Wargamer, 13/11 — https://www.wargamer.com/magic-the-gathering/nauctis-decks-teased | confirmação complementar das combinações de cores |
| Vazamento | Scryfall NAC 6 e NAC 8 (https://scryfall.com/card/nac/6, https://scryfall.com/card/nac/8); MTG Rocks e Draftsim (16/11) | duas faces de comandante do Terrors em japonês; traduções inglesas divergentes («The Ignoble Serpent» / «The Noble Sea Serpent»; «Zekes, Acid Rock Fan» / «Zekes, Follower of Lewenism» / «Zekes, Revenist Devotee») — **não são nomes finais**. Não usados nas peças novas (AB-03 já os tratou). |
| Interpretação editorial | BINDER | «A proposta» do carrossel e a 3.ª linha das Stories: explicação em português das chamadas da caixa (convoke = virar criaturas para ajudar a pagar; ficha de Sangue = descartar um card para comprar outro; group hug = dar recursos à mesa). Nunca «pagar vida por Tesouro». |

Formulação factual: «Terrors of the Abyss é o único dos quatro decks com duas faces de comandantes vazadas em japonês conhecidas até esta pesquisa. Os outros três decks ainda não têm faces de comandantes reveladas. Os quatro, entretanto, possuem imagens oficiais das embalagens.»
Verificação de última hora (20/11, ~10h40): nenhuma face de comandante nova oficial desde 16/11 (Draftsim, página de spoilers NAC; pesquisa web).

## Imagens reutilizadas e créditos
- Embalagens oficiais © Wizards of the Coast: Merfolk Regiment, Terrors of the Abyss, Blood in the Water (padrão) e **Seal the Deal (Premium Edition** — a imagem enviada; nas peças o crédito diz «Premium Edition»). Recorte do fundo branco por `abismo/kit/embalagens_nauctis/preparar.py`; a arte não é alterada. Identificadas como «Embalagem oficial» em todas as peças; nunca usadas como carta.
- Música «Auction of Power» (fundador). Sons descida/swell/glitch (kit da Expedição). Fundo `expedicao/template/fundo.py` (semente 11). Logótipo oficial BINDER. Inter / Inter Display.

## Recursos reaproveitados (sem créditos gastos)
Motor `abismo/motor/abismo.py` (estendido, não reconstruído), fundo mestre, vida (medusas, cáusticas, pulsação), cartão informativo, etiquetas, pílula de deck e pontos de cor do AB-04, legendas de ecrã, assinatura, música e sons, modelos `story.json`/`reel.json`/`carrossel.json`, pesquisa do AB-04. Zero voz, zero imagem gerada, zero ElevenLabs.

## Alterações ao motor (razão, impacto, regressão)
- Razão: usar as embalagens oficiais como protagonistas (missão de 20/11) sem criar motor novo.
- Novo: `embalagem()` (caixa recortada, sem cantos de carta), crédito «Embalagem oficial»; no modo `decks`, `"embalagem"` por deck e `"gancho_embalagens"`; Story `"modo": "deck"` (efeitos `eco`, `ascensao`, `mare`, `acordo`) e `"modo": "votacao"`; carrossel com slides `nauctis_capa` e `deck`; `capa.py` aceita embalagens.
- Impacto: só ABISMO; posts sem estas chaves seguem o caminho antigo.
- Regressão: AB-04 v1 (stills 0/10/19,5 s e capa) e AB-03 (stills e capa) gerados de novo sem diferença visível (ver ficha da campanha, QC).

## Limitações reais
- A imagem do Seal the Deal é a da **Premium Edition** (o fundador enviou essa); a caixa padrão não foi vista. Para trocar: correr `preparar.py seal=<imagem padrão>` e voltar a renderizar (custo zero).
- As imagens vêm em 1920×1080 com a caixa a ~670×1055 px: nos tamanhos usados (até 660 px de altura) não há ampliação.
- As cores e chamadas foram lidas nas imagens; as listas, os comandantes e as cartas dos decks continuam por revelar.
- Instagram: não verifiquei na app se a «Enquete» aceita 4 opções na conta; a instrução do AB-09 deixa a caixa de perguntas como principal.
- `media.wizards.com` está bloqueado neste ambiente: as imagens entraram pelo fundador e não estão no repositório (© Wizards); recriar exige voltar a pô-las em `abismo/kit/embalagens_nauctis/saida/`.

## QC (ficheiros finais, 20/11/2026)
| Peça | Medidas | Folha de contacto (quadros vistos) | Resultado |
|---|---|---|---|
| AB-04 v2 | 1080×1920, 30 fps, H.264/AAC 48 kHz, 20,57 s; −14,1 LUFS, pico −1,8 dBTP | 0; 2,5; 3,4; 5,8; 6,4; 8,7; 9,6; 10; 13; 13,5; 16,5; 17,9; 19,5 s, lado a lado com o v1 nos mesmos tempos | OK. Mesma timeline do v1; música e sons iguais exceto o glitch da antiga etiqueta vermelha «VAZADO» (saiu com a etiqueta). Gancho v1 → v2 interno: caixas sobrepostas tapavam nomes (P1) → fila sem sobreposição |
| AB-05 Merfolk | 1080×1920, 30 fps, 13,72 s; −14,1 LUFS, pico −2,1 dBTP | 0,05; 2,2; 3,6; 5,5; 6; 11; 12,5 s | OK. Ecos atenuados (competiam com a caixa) e caixa 22 px abaixo do título antes do render |
| AB-06 Terrors | idem | idem | OK. Sem cartas vazadas |
| AB-07 Blood | idem | idem | OK |
| AB-08 Seal | idem | idem | OK. Crédito diz Premium Edition |
| AB-09 votação | idem | idem + quadro 11 s em tamanho real | OK. Zona do sticker livre (y 1260–1580) |
| AB-10 carrossel | 5 × 1080×1350 PNG | 5 slides + capa com o recorte 3:4 marcado | OK (v2): cartão por trás do texto, capa sem sobreposição, PT-BR corrigido |
Regressão do motor: AB-04 v1 (stills 0/10/19,5 s e capa; quadro 10 s difere em média 1,5/255 do vídeo original, ruído de compressão) e AB-03 (stills 0/10 s) sem alterações visíveis. Ficheiros temporários do teste no AB-03 apagados (nada versionado mudou).
Textos: português do Brasil, «você»; chamadas das caixas em inglês, como impressas.

## Ficheiros finais (não versionados)
- `AB-04-nauctis-decks-reel-v2/saida/AB-04-nauctis-decks-reel-v2_reel.mp4`, `_capa.png`
- `AB-05-merfolk-story/saida/AB-05-merfolk-story_story.mp4` (idem AB-06, AB-07, AB-08, AB-09)
- `AB-10-nauctis-carrossel/saida/AB-10-nauctis-carrossel_carrossel_01.png` a `_05.png`
- Texto: `legenda.txt` (AB-04 v2, AB-10), `comentario_fixado.txt` (AB-04 v2, AB-10), `legenda.txt` (texto de apoio; Stories não têm legenda) (AB-05 a AB-09), `texto_alternativo.txt` (todas), `ficha.md` (todas).
