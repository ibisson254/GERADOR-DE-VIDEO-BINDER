# AB-05 · Story · Merfolk Regiment (ABISMO, campanha Nauctis)

- **Pedido:** missão de expansão editorial do fundador, 20/11/2026 (10:05). Extensão da pauta AB-04 (decisão em `nucleo/DECISOES.md`, 20/11).
- **Mensagem única:** Um exército que cresce nas profundezas. **Objetivo:** resposta ao Story. **Público:** jogadores de Commander PT-BR.
- **Conceito próprio:** eco: no drop, ecos esmaecidos da caixa abrem-se para os dois lados (presença coletiva, «go wide»), atrás da caixa.

## Gancho visual (§4.1)
1. Quadro 0: a caixa oficial (escurecida) sob «UM EXÉRCITO QUE CRESCE NAS PROFUNDEZAS». 2. Objeto: embalagem oficial do Merfolk Regiment. 3. Ação: a caixa pisca e aproxima-se; acende com a faixa de luz aos 1,71 s. 4. Som: descida. 5. Até 3 s: nome do deck e a caixa a acender. 6. Promessa: o que o deck faz. 7. Pagamento: 3,43 s (drop, «TAP AND CONVOKE» em destaque) e 4,3 s (descrição).
Rubrica prevista/medida: relevância 5/5 · impacto 4/4 · clareza 5/5 · curiosidade 4/4 · pagamento 5/5 · identidade 5/5.

## Roteiro definitivo (sem voz)
| Batida | Tempo | Ecrã |
|---|---|---|
| 0 | 0,00 | «UM EXÉRCITO QUE CRESCE NAS PROFUNDEZAS» sobre a caixa escurecida |
| 4 | 1,71 | Caixa acende · pílula «COMMANDER · NAUCTIS · guilda · cores» · nome do deck |
| 8 | 3,43 | **Drop** · efeito (eco) · chamadas da caixa, «TAP AND CONVOKE» a amarelo |
| 10 | 4,29 | Descrição curta em português |
| 24–32 | 10,29–13,72 | «Você prefere encher a mesa de criaturas?» |

## Produção
- Formato: Story ABISMO (`modelos/story.json`): 32 batidas, 13,72 s, «Auction of Power» batidas 56–64 e 64–88, drop na batida 8 (3,43 s). Sem voz; sons descida (1,71 s) e swell até ao drop. Custo zero.
- Hierarquia: 1) nome do deck (Inter Display Black 100); 2) chamadas impressas na caixa (a destacada a amarelo, 64 px; a outra branca, 42 px); 3) descrição curta (Inter SemiBold 34). Crédito «Embalagem oficial» sempre visível com a caixa.
- Fontes: `../CAMPANHA_NAUCTIS_EMBALAGENS.md`. QC: secção «QC» da campanha.
- Recriar: `python3 -I abismo/motor/abismo.py abismo/publicacoes/AB-05-merfolk-story` (precisa das embalagens em `abismo/kit/embalagens_nauctis/saida/`).
- Ficheiro final (não versionado): `abismo/publicacoes/AB-05-merfolk-story/saida/AB-05-merfolk-story_story.mp4`.

## Controlo de qualidade
1080×1920, 30 fps, H.264/AAC 48 kHz, 13,72 s; −14,1 LUFS, pico −2,1 dBTP. Folha de contacto (0,05; 2,2; 3,6; 5,5; 12,5 s) sem sobreposição de texto, caixa identificável com crédito «Embalagem oficial», pergunta/CTA dentro da zona segura (base 1580), sem narração. Detalhe: `../CAMPANHA_NAUCTIS_EMBALAGENS.md` («QC»).

## Ficheiros finais (não versionados)
`abismo/publicacoes/AB-05-merfolk-story/saida/AB-05-merfolk-story_story.mp4` (Story: sem capa; o quadro 0 é a abertura).
