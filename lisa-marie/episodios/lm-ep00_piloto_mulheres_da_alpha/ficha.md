# LM-EP00 · Piloto sem voz · Elas no Multiverso: as cinco mulheres da Alpha

**Frente:** Lisa Marie no Ar (série em desenvolvimento) · quadro `Elas no Multiverso`  
**Estado:** EM PRODUÇÃO. Piloto para avaliação do fundador. A arte da Lisa ainda é conceito: publicar só com decisão do fundador.  
**Pedido do fundador (21/11/2026, 01:14):** «Refine essa ideia. Crie um episódio piloto sem voz e use também transição de Flip que estamos usando no TUBO e faça melhorias necessárias», com a missão em anexo («Evolução da prova de recorte para VJ cultural com cenário urbano real»).  
**Pauta:** `memoria.py pauta` → PAUTA LIVRE. A primeira versão da pauta bloqueou por Stasis (MB-EP02) e Dark Ritual (LL-R03): essas cartas saíram e a Fay Jones aparece só num painel de texto, sem a carta.  
**Motor:** `lisa-marie/motor/piloto_lm_ep00.py` · **cartas:** `cartas.py` (Scryfall, não versionadas) · **camadas da Lisa:** `kit/prova_recorte/` (conceito, não master).

## 1. Briefing

- **Público:** colecionadores e jogadores de Magic do Brasil e de Portugal, sobretudo quem gosta de cartas antigas e de arte. O tema interessa a toda a gente, não só a mulheres.
- **Objetivo:** apresentar o tom da Lisa e o quadro Elas no Multiverso com uma descoberta verificável e pedir sugestões de ilustradoras (ação única: comentar).
- **Mensagem única:** já no primeiro set de Magic, em 1993, cinco das 25 pessoas que o ilustraram eram mulheres, incluindo quem pintou o Shivan Dragon.
- **Território:** pessoa e trajetória (Lisa). Não analisa composição nem técnica (Conde) e não é curiosidade rápida sobre uma carta (Lambe-lambe), porque o eixo são as cinco pessoas.

### Gancho visual (SHOWRUNNER §4.1)

| # | Campo | Resposta |
|---|---|---|
| 1 | Quadro 0 | O Shivan Dragon inteiro sobre a cidade desfocada, com «O DRAGÃO MAIS FAMOSO DA ALPHA» já escrito |
| 2 | Objeto | Shivan Dragon (Alpha, 1993) |
| 3 | Ação | Aproximação lenta da carta; aos 2,9 s acende o destaque no crédito impresso «Illus. © Melissa Benson» |
| 4 | Som | Sinal de emissão original (0 s) e depois batida e brilho na revelação (2,9 s) |
| 5 | Descoberta até 3 s | «Foi pintado por uma mulher.» |
| 6 | Promessa | Quem eram as outras? |
| 7 | Pagamento | 22,5 s: painel «5 de 25» com os cinco nomes, depois das cartas de cada uma |

**Rubrica prevista (1–5):** relevância visual 5 · impacto inicial 4 · clareza 5.  
**Rubrica medida (folha de contacto sem som, render v1):** relevância 5 · impacto 4 (a carta prende, mas a revelação só chega aos 2,9 s) · clareza 5.

## 2. Ficha de factos (cada facto no ecrã tem fonte)

| # | Facto no ecrã | Fonte | Data/consulta |
|---|---|---|---|
| F1 | Shivan Dragon, Mind Twist, Giant Growth e Time Walk são da Alpha (Limited Edition Alpha, 1993); artistas Melissa A. Benson, Julie Baroh, Sandra Everingham e Amy Weber | API do Scryfall (`cartas_scryfall.json`, `released_at` 1993-08-05) e o crédito impresso em cada carta | 21/11/2026 |
| F2 | 25 artistas ilustraram a Alpha; 5 eram mulheres | Wargamer, «no babe art» (citando o diretor de arte original); StarCityGames, «Compulsive Research – The Artists Of Alpha» (25 artistas); Wikipedia, «List of Magic: The Gathering artists» | 21/11/2026 |
| F3 | As cinco: Amy Weber, Fay Jones, Julie Baroh, Melissa A. Benson, Sandra Everingham | Lista da Alpha (mtg.wiki «1993», Scryfall `set:lea`), cruzada com biografias: Wikipedia (Julie Baroh; Fay Jones), mtg.wiki (Melissa Benson; Amy Weber), Hipsters of the Coast (entrevista a Sandra Everingham). Andi Rusu e Anson Maddocks são homens (mtg.wiki «Andi Rusu») | 21/11/2026 |
| F4 | Julie Baroh ainda estudava artes quando fez as primeiras cartas | StarCityGames (Compulsive Research); mtg.wiki «Julie Baroh» (Cornish College of the Arts) | 21/11/2026 |
| F5 | Sandra Everingham: 12 ilustrações na Alpha | Scryfall `set:lea`, contagem por artista (12) | 21/11/2026 |
| F6 | Amy Weber: 16 ilustrações na Alpha, a que mais pintou entre as cinco | Scryfall `set:lea` (Weber 16, Everingham 12, Benson 7, Baroh 4, Jones 1) | 21/11/2026 |
| F7 | Fay Jones: 1 carta na Alpha, pintada a pedido do sobrinho, Richard Garfield | Wikipedia, «Fay Jones (artist)» («as a favor for her nephew, the game's designer Richard Garfield») | 21/11/2026 |
| F8 (comentário) | Melissa Benson disse que, se soubesse que a carta teria fundo vermelho, talvez não tivesse feito um dragão verde | Casual Hornan, «Interview with Melissa Benson», 09/2017 | 21/11/2026 |

Leitura da Lisa (opinião, marcada como fala dela, não como facto): «Primeiro set. 1993. E elas já estavam lá.»

Imagens: só as cartas (arte © Wizards of the Coast, conteúdo de fã não oficial, crédito no ecrã e na legenda). **Nenhuma foto de pessoa real**, nenhuma entrevista, nenhuma fala atribuída a uma convidada. Por isso não há autorizações a registar.

## 3. Roteiro definitivo (sem voz)

| Tempo | Cena | No ecrã | Lisa | Som |
|---|---|---|---|---|
| 0,00–2,90 | Quadro 0 | Shivan Dragon; «O DRAGÃO MAIS FAMOSO DA ALPHA» | — | sinal de emissão |
| 2,90–5,70 | Revelação | «FOI PINTADO POR UMA MULHER.»; destaque no crédito; etiqueta «MELISSA A. BENSON · Shivan Dragon · Alpha, 1993» | — | batida, brilho, tique |
| 5,70–9,50 | Lisa, plano médio (rua) | Fala «Peraí. Ela não era a única.»; tarja «LISA MARIE · NO AR · ELAS NO MULTIVERSO» (6,0–8,9 s) | entra a subir, boca em «o» em «Peraí», inclina a cabeça, pisca | sintonia, cama de cidade |
| 9,50–12,70 | Flip → Mind Twist | «JULIE BAROH · Ainda estudava artes quando fez as primeiras cartas.» | fora de quadro | flip |
| 12,70–15,90 | Flip → Giant Growth | «SANDRA EVERINGHAM · 12 ilustrações só na Alpha.» | — | flip |
| 15,90–19,10 | Flip → Time Walk | «AMY WEBER · 16 ilustrações na Alpha: a que mais pintou entre elas.» | — | flip |
| 19,10–22,50 | Flip → painel | «FAY JONES · 1 carta na Alpha. Pintou-a a pedido do sobrinho: Richard Garfield, o criador do jogo.» | — | flip |
| 22,50–26,00 | Flip → painel (pagamento) | «5 DE 25 · ARTISTAS DA ALPHA ERAM MULHERES» + os cinco nomes + fontes | — | flip, batida |
| 26,00–29,80 | Lisa, grande plano (chuva) | «Primeiro set. 1993. E elas já estavam lá.»; identificador pequeno | admiração: piscar lento, cabeça inclina | sintonia, cama |
| 29,80–34,00 | Lisa, plano médio (rua) | «Qual ilustradora você quer ver no Elas no Multiverso? Conta nos comentários.» | ligeiro balanço, pisca | cama |
| 34,00–37,87 | Fecho comum | `comum/outro/outro_binder_916.mp4` (corte seco) | — | silêncio |

Sem voz. Música de biblioteca com licença («Hazy After Hours», Mixkit), provisória e não oficial da série; a intro calma acompanha as cartas e o groove entra por volta dos 15 s. SFX originais gerados por código no motor.

## 4. Hierarquia visual aplicada

1. **Evidência:** a carta ou o painel ocupa o centro (745×1040, tamanho nativo do Scryfall, nunca ampliado). A cidade fica desfocada, mais escura e menos saturada atrás.
2. **Lisa:** apresenta e reage nas três cenas dela e sai de quadro durante as provas (CONTEXTO §4).
3. **Legendas:** grandes, no topo ou na caixa «LISA», sem tapar olhos, boca, carta nem crédito.
4. **Grafismos:** a tarja só aparece na primeira entrada da Lisa (6,0–8,9 s); o identificador só nas cenas finais; crédito da Wizards em letra pequena no rodapé.
5. **Cidade:** fundo subordinado (exposição 55–78%, saturação 70–80%, vinheta, desfoque 1,5–6 px).

## 5. Controlo de qualidade

| Item | v1 (21/11) |
|---|---|
| Formato | 1080×1920, 30 fps, 37,87 s, H.264 + AAC (render final 21/11) |
| Quadro 0 | Carta e título visíveis no quadro 0 ✔ |
| Mudança ≤ 3 s | ✔ (cenas da Lisa de 3,8–4,2 s têm entrada, fala, tarja ou piscar dentro do intervalo) |
| Corte lateral | Recorte da Lisa encostado à direita: a borda reta fica fora do quadro ✔ |
| Legendas sobre rosto/carta | nenhuma ✔ |
| Fontes no ecrã | painéis Fay Jones e 5 de 25 ✔ |
| Fecho | corte seco para o fecho comum ✔ |
| Som | SFX originais + «Hazy After Hours» (Mixkit, Alejandro Magaña, licença em `biblioteca_urbana/musica.csv`), que sobe no fecho; −15,1 LUFS, pico −2,1 dBFS; sem voz |
| Fundo urbano | Clipe real Pexels 14957612 (enviado pelo fundador, 21/11), usado em 3 tratamentos: desfocado atrás das cartas, rua no plano médio, recorte 1,25× no grande plano. Sem fundo provisório |
| Limite da arte | Lisa conceito (262 px de origem), ampliação real ≈2,1× no plano médio e ≈3× no grande plano; bocas e pálpebras provisórias. Não publicar com esta arte sem decisão do fundador |

Vídeo e prévia: entregues na conversa, não versionados.

## 6. Métrica principal (se for publicado)

Comentários com nomes de ilustradoras (alimentam a pauta do Elas no Multiverso). Secundárias: retenção aos 3 s e aos 22,5 s (pagamento), partilhas e guardados em relação ao alcance.

## 7. Comparação com a prova de 19/11

| | Prova de recorte (19/11) | LM-EP00 (21/11) |
|---|---|---|
| Função | Teste técnico da boca | Piloto com pauta, factos e fontes |
| Fundo | Estúdio vetorial do kit | Filmagem urbana real (Pexels), subordinada |
| Abertura | Apresentação da Lisa | Quadro 0 com o Shivan Dragon e a tese |
| Lisa | 2 planos, quase sempre presente | 3 aparições; sai de quadro durante as provas |
| Escala | ≈3,3× da origem no plano médio | ≈2,1× no médio, ≈3× no grande plano |
| Integração | Personagem colada | Sombra suave, harmonização de 6%, base escurecida, grão comum, borda fora do quadro |
| Transições | Flash rosa | Flip 3D das cartas + sintonia curta nas entradas da Lisa |
| Grafismos | Tarja durante todo o plano | Tarja só na primeira entrada; identificador pequeno no fim |
| Som | Voz sintética provisória | Sem voz; SFX originais + música licenciada |

Vídeo final e capa (quadro de 1,0 s): entregues na conversa a 21/11, não versionados.
