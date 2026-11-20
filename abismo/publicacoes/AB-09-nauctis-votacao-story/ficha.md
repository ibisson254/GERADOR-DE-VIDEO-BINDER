# AB-09 · Story interativo · Qual desses decks você levaria para sua mesa? (ABISMO, campanha Nauctis)

- **Pedido:** missão do fundador, 20/11/2026 (10:05). Extensão da pauta AB-04.
- **Objetivo:** participação; descobrir qual produto interessa mais **entre quem responde** (não é pesquisa representativa).
- **Interação real, aplicada na app:** caixa de perguntas nativa com «Responda com 1, 2, 3 ou 4.» na zona livre y 1260–1580 (instruções em `legenda.txt` (texto de apoio; Stories não têm legenda)). O vídeo não simula sticker.

## Gancho visual (§4.1)
1. Quadro 0: «QUAL DESSES DECKS VOCÊ LEVARIA PARA SUA MESA?» + 4 caixas lado a lado (escurecidas), numeradas 1–4. 2. Objeto: as 4 embalagens oficiais. 3. Ação: acendem uma a uma nas batidas 4–7. 4. Som: descida + swell. 5. Até 3 s: pergunta e as 4 opções. 6. Promessa: escolher. 7. Pagamento: 3,43 s (drop, as quatro acesas).

## Roteiro definitivo (sem voz)
Batida 0: pergunta + 4 caixas escurecidas e numeradas · batidas 4–7: cada caixa acende (descida na 4) · batida 8: drop, as 4 acesas · até 32: tudo parado para responder.

## Layout
Pergunta (Inter Display Black 80, última linha a amarelo) · 4 caixas de 360 px de altura, mesma escala · círculo esmeralda com o número · nome do deck em 2 linhas · crédito «Embalagens oficiais (Seal the Deal: Premium Edition)» · «Responda com 1, 2, 3 ou 4.» · zona livre para o sticker.

- Formato: Story 13,72 s, música batidas 56–88. Recriar: `python3 -I abismo/motor/abismo.py abismo/publicacoes/AB-09-nauctis-votacao-story`. Ficheiro final (não versionado): `saida/AB-09-nauctis-votacao-story_story.mp4`.
- Fontes e QC: `../CAMPANHA_NAUCTIS_EMBALAGENS.md`.

## Controlo de qualidade
1080×1920, 30 fps, H.264/AAC 48 kHz, 13,72 s; −14,1 LUFS, pico −2,1 dBTP. Folha de contacto (0,05; 2,2; 3,6; 5,5; 12,5 s) sem sobreposição de texto, caixa identificável com crédito «Embalagem oficial», pergunta/CTA dentro da zona segura (base 1580), sem narração. Detalhe: `../CAMPANHA_NAUCTIS_EMBALAGENS.md` («QC»).

## Ficheiros finais (não versionados)
`abismo/publicacoes/AB-09-nauctis-votacao-story/saida/AB-09-nauctis-votacao-story_story.mp4` (Story: sem capa; o quadro 0 é a abertura).
