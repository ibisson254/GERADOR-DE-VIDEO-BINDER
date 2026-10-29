# Ficha · Conde de Manaforte · EP003 · Voldaren Pariah: o rosto no meio da refeição

Render final de 29/10/2026 (47,3 s sem o fecho; 51,2 s no total). Publicação prevista: 31/10/2026, 21h de Lisboa (Halloween).
Scripts: `conde/montar_ep003.py` (copiado de `montar_ep002.py`), `conde/encurtar_narracao_ep003.py` (derivado de `encurtar_narracao.py`). Dados: `conde/ep003/` (imagens Scryfall, `audio/words_raw.json`, `audio/words_novo.json`).

## Classificação
- Série: Conde de Manaforte · O Tribunal Estético
- Classe: comentário sobre uma obra (+ contexto leve de artista, que passou para o comentário fixado)
- Complexidade: média (carta de dupla face)
- Estratégia: análise estética (observação / interpretação / facto separados)

## Editorial
- Objetivo: entreter o colecionador e fã de arte PT/BR e levá-lo ao comentário fixado e à legenda (BINDER Vision).
- Proposta de valor: o "defeito" do rosto da Voldaren Pariah é o próprio assunto da carta; a transformação está na tinta.
- Público: colecionador e fã de arte PT/BR.
- Hipótese a testar: a pergunta A/B no comentário fixado gera mais comentários do que a pergunta aberta dos Ep. 001–002.
- Tese (opinião do Conde): o rosto não está inacabado; está no meio da refeição.
- Gancho (0–3 s): "Meus caros apreciadores do duvidoso. O Tribunal recebe hoje uma dama de 2026."
- Callback: "Mais uma Voldaren. A família insiste." + rótulo "cf. processo nº 002" (Olivia Voldaren).

## Narração final (depois dos cortes)
Meus caros apreciadores do duvidoso. O Tribunal recebe hoje uma dama de 2026. Voldaren Pariah. Mais uma Voldaren. A família insiste. Vista de baixo, contra a luz, a figura se desfaz numa teia de sangue que leva o olho direto ao rosto. Mas o Tribunal vira a carta. E o rosto... não está terminado. Derrete. Mármore molhado. A artista é Véronique Meignaud. E o texto da carta esclarece: para transformar esta dama, sacrifique outras três criaturas. Ou seja: o rosto não está inacabado. Está no meio da refeição. O Tribunal retira a acusação. O monóculo, não. Parecer: obra notável. Feliz Halloween. A única máscara que caiu foi a da tinta. Qual réu o Tribunal julga a seguir?

## Camadas
| Camada | No episódio |
|---|---|
| Observação (verificável pausando) | figura vista de baixo (contrapicado); contraluz no fundo claro à direita; fitas vermelhas em teia que levam ao rosto; no verso, rosto diluído em manchas |
| Interpretação (opinião do Conde) | "mármore molhado", "no meio da refeição", "obra notável", "a única máscara que caiu foi a da tinta" |
| Facto (fonte) | texto Oracle (sacrifício de três criaturas), flavor, artista e nº no rodapé, ano 2026; "volta ao Magic" atribuída à Wizards no comentário fixado |

## Fontes e evidências (consulta 29/10/2026)
| Afirmação | Tipo | Fonte | Data |
|---|---|---|---|
| Voldaren Pariah // Abolisher of Bloodlines, SLD nº 1441, arte de Véronique Meignaud, lançada 12/10/2026 | facto | https://api.scryfall.com/cards/sld/1441 + rodapé da carta | 29/10/2026 |
| Oracle frente/verso e flavor da frente | facto | idem | 29/10/2026 |
| Conteúdo do drop (4 cartas) | facto | https://secretlair.wizards.com/eu/product/1253746/artist-series-veronique-meignaud · https://magic.wizards.com/en/news/announcements/secret-lair-corn-maze-superdrop | 29/10/2026 |
| "Véronique Meignaud returns to Magic…" | facto atribuído (afirmação da Wizards) | página oficial do produto (US e EU) | 29/10/2026 |
| Terrenos de arte completa ZEN (2009) e Expeditions EXP 16–20 (2015) | facto | Scryfall, pesquisa por artista | 29/10/2026 |
| Original: Eldritch Moon (2016), arte de James Ryman | facto | https://api.scryfall.com/cards/emn/111 | 29/10/2026 |
| Paleta: azul-petróleo, branco/azul-claro e vermelho dominam a frente | observação (pixéis medidos) | art_crop da frente | 29/10/2026 |
Lista completa: `ep003_fontes.txt`.

## Produção
- Recursos reutilizados: retrato e 4 expressões (`conde/assets`), tema `musica/tema.mp3`, layout e funções do Ep. 002, quadros reais do scanner (`comum/outro/scan/`) + logótipo para o fecho.
- Voz: ElevenLabs "Conde de Manaforte" (`bbnQVGWT7UMdmoK4URLr`), `eleven_v4`, **1 geração** (1 085 créditos), sem repetição. Grafia fonética no TTS para Voldaren, Pariah, Meignaud e Zendikar; legendas com a grafia real.
- Tempos por palavra: `eleven_scribe_v1` (alinhamento) → `encurtar_narracao_ep003.py`, com os tempos encostados aos silêncios reais.
- Música: tema emendado no compasso (CUT_A 22,09 s, recuo de 8 batidas de 0,882 s, crossfade 0,25 s), ducking sidechain (threshold 0.025, ratio 5), sobe no fim da fala e cobre o fecho; sting nos 4 carimbos.
- Arte: art_crop 626×457 → palco 1080×788 (STAGE_H = round(1080×457/626)), largura total, sem corte.
- Cenas: medalhão → arte da frente + RÉ · 2026 → carta inteira (nome) → "cf. processo nº 002" → contraluz / teia de sangue / seta pelas fitas até ao rosto → carta inteira, flip 2D horizontal (0,5 s), carta inteira do verso → lupa no rosto do verso ("derrete.", "mármore molhado") → rodapé do verso destacado (artista e nº) → linha Oracle destacada na carta da frente → citação Oracle → zoom no rosto do verso → flavor → ACUSAÇÃO RETIRADA (+ egg) → OBRA NOTÁVEL → verso ("máscara da tinta") → PARECER EMITIDO + "A · inacabado ou B · transformação?" → fecho do scanner.
- Easter egg: "III" bordô junto ao carimbo ACUSAÇÃO RETIRADA (~36,6–37,6 s) = os três sacrifícios.
- Riscos: texto atribuído à Wizards; licença da voz (ver limitações).

## Divergências com o briefing (e porquê)
1. **Take da voz com 81,8 s** (o briefing previa ~52 s). Como só há 1 geração, cortaram-se frases inteiras do áudio, sem regenerar: "De família antiga.", "Sim,", "A composição é de primeira ordem.", "Uma carta preta, pintada em azul, branco e vermelho. Ousadia.", "Escorre.", "a dos terrenos de Zendikar, que, segundo a Wizards, volta ao Magic com uma série própria." e "Derreter de propósito é mais difícil do que terminar." O contexto da artista e a atribuição à Wizards ficam no comentário fixado.
2. **atempo 1,15** em vez de 1,08 e pausa comum 0,20 s em vez de 0,24 s, para caber em 42–48 s (o take é mais lento do que o do Ep. 002). Pausas cómicas mantidas: 0,58 s antes de "Derrete." e antes de "Está no meio da refeição."; 0,36–0,45 s entre os blocos finais.
3. **Sem os discos de cor**: a frase das cores saiu no corte. A frase seria sustentável (pixéis medidos: azul-petróleo ~63,103,101; branco-azulado ~203,217,233; vermelho ~126,27,21), mas ficou sem fala que a sustente no ecrã.
4. **Abertura com o medalhão** (0–2,4 s, como no Ep. 002) antes da arte da frente, para o gancho mostrar o Conde.
5. **Ecrã final**: "A · inacabado ou B · transformação?" em vez de "Comente o próximo réu", alinhado com a hipótese A/B do comentário fixado. A fala mantém "Qual réu o Tribunal julga a seguir?".
6. **Legenda**: a frase da ponte ficou "Tem a Voldaren Pariah de 2016? Escaneie e guarde no seu Binder." e o CTA "→ Baixe o BINDER Vision no Android. Link na bio." (582 caracteres; a versão do briefing passava de 600).
7. **Envio nos EUA (15/12)** não confirmado: a página EU confirma "January 19th" (sem ano). Não é usado em nenhum texto público.
8. **Fecho reconstruído**: `comum/outro/outro_binder_916.mp4` continua fora do repositório e não está no Google Drive (pesquisa a 29/10/2026). O fecho foi reconstruído com os 45 quadros reais de `comum/outro/scan/` + logótipo, como no TUBO EP02. O script usa o MP4 oficial automaticamente quando ele existir.

## Controlo de qualidade (ficheiro final, 29/10/2026)
| Critério | Resultado |
|---|---|
| 1080×1920, 30 fps, H.264 + AAC 48 kHz | OK |
| Corte lateral (cropdetect em todos os quadros) | OK: crop=1080:1920:0:0 em todos os 1417 quadros medidos do episódio (o cropdetect salta os 2 primeiros). Nos 3,87 s do fecho o cropdetect acusa bordas escuras porque o fundo do scanner e do logótipo é quase preto; são quadros nativos 1080×1920, sem corte |
| Duração | 47,3 s sem o fecho (alvo 42–48); 51,2 s no total |
| Loudness | −14,1 LUFS integrados, pico real −1,7 dBFS |
| Legenda queimada | zona segura (y≈1372), sincronizada pelos tempos por palavra; início de cada frase conferido contra o arranque do som: 29/29 dentro de ±0,10 s |
| Carta e arte inteiras | OK: carta inteira com rodapé visível; arte em largura total |
| Observação / interpretação / facto | OK (tabela "Camadas") |
| Quadros conferidos | 14 quadros extraídos do MP4 final e vistos (abertura, RÉ, nome, composição, flip a meio, lupa, rodapé, Oracle, flavor, acusação retirada, obra notável, parecer emitido, scanner, logótipo) |
| Pronúncia | **não conferida de ouvido** nesta sessão (sem leitor de áudio; o upload para transcrição cega foi bloqueado pela rede) |
| Defeitos bloqueadores | Nenhum detetado no vídeo; licença da voz por confirmar (abaixo) |

## Limitações conhecidas
- Licença comercial da voz e da música: depende do plano ElevenLabs ativo, que esta sessão não consegue ver. Publicável só se a conta estiver no Starter ou superior.
- Pronúncia de "Voldaren", "Pariah" e "Véronique Meignaud" por ouvir.
- Fecho reconstruído (ver divergência 8).
- A lupa amplia um art_crop de 626 px: o rosto do verso fica um pouco granulado na ampliação.

## Entregáveis
- [x] Vídeo `Conde_Ep003_VoldarenPariah_916.mp4` · [x] Capa `Conde_Ep003_VoldarenPariah_capa.jpg` (quadro de 38,0 s, ACUSAÇÃO RETIRADA) · [x] Legenda · [x] Comentário fixado · [x] Fontes

## Depois de publicar
- Métrica principal: respostas A/B no comentário fixado + guardados.
- Resultado observado: (aguarda o print do Insights)
- Aprendizagem: (comparar comentários com Ep. 001–002)
