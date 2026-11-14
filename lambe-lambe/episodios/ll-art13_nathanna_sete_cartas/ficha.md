# Ficha · Lambe-lambe · LL-ART13 · Nathanna Érica: sete cartas em Special Guests

## Identificação
- ID editorial: LL-ART13
- Estado no registo: CONCLUÍDO (não publicado)
- Aprovação do fundador: missão de produção de 14/11/2026 (16:22), novo ângulo autorizado; padrão visual sem ElevenLabs pedido a 14/11/2026 (16:30)

## Classificação
- Frente: Lambe-lambe (série «Artistas de Magic»), carrossel 4:5
- Classe de conteúdo: artista
- Complexidade: baixa
- Estratégia: reutilização do motor-padrão do carrossel; zero créditos externos

## Originalidade
- Objeto: Nathanna Érica; Kinsbaile Cavalier; Faerie Macabre; Wanderwine Prophets; Goblin Chieftain; Regal Force; Risen Reef; Helix Pinnacle
- `memoria.py pauta`: BLOQUEADA (LL-ART02, mesmo objeto «Nathanna Érica (Faerie Macabre)»; LL-R02, Faerie Macabre numa colagem de 0,2 s)
- Decisão que liberta: fundador, 14/11/2026 (`nucleo/DECISOES.md`): ângulo novo = variedade das sete ilustrações Special Guests de Lorwyn Eclipsed e presença da artista no conjunto. LL-ART02 (transição de advogada a ilustradora) não é reaberto e o tema não é retomado.
- Relações: LL-ART02, LL-R02

## Editorial
- Objetivo: mostrar uma artista brasileira com 7 dos 20 Special Guests de Lorwyn Eclipsed e gerar comentários (escolha de uma carta)
- Proposta de valor: as sete cartas da Nathanna numa lista que se guarda
- Público: colecionadores de Magic no Brasil, sobretudo os que abrem Lorwyn Eclipsed
- Hipótese: a lista guardável (slide 5) gera mais salvamentos do que os carrosséis de artista anteriores
- Gancho: «7 CARTAS. UMA ARTISTA BRASILEIRA.»

## Roteiro definitivo
`roteiro_carrossel.md` nesta pasta.

## Fontes e evidências
`fontes.md` nesta pasta.

## Produção
- Recursos reutilizados: `lambe-lambe/referencias/carrossel_padrao_01.png` e `_02.png` (modelos aprovados), `lambe-lambe/kit_carrossel/motor_padrao.py`, papel, fita e fontes do kit
- Ferramentas: Python (OpenCV), Chrome headless (Playwright) para os textos
- Vozes e créditos gastos: 0 (sem ElevenLabs, sem geração de imagem)
- Easter egg: nenhum
- Riscos: foto da artista usada com a autorização a pedir pelo fundador (regra de 13/11); artes do Scryfall ampliadas (art_crop 626×457) nas impressões grandes dos slides 6 e 7, ligeiramente suaves de perto
- Limitações: portfólio oficial, entrevista e release notes inacessíveis nesta sessão (ver `fontes.md`); «storytelling» do briefing ficou de fora por não estar confirmado

## Controlo de qualidade
Medido nos 7 ficheiros finais e na folha de contacto (14/11/2026).

| Critério | Alvo | Medido | OK |
|---|---|---|---|
| Resolução | 1080×1350 (4:5) | 7/7 com 1080×1350 | sim |
| Ordem | 01 a 07 | nomes numerados 01_… a 07_… | sim |
| Referências aplicadas | modelos 01/02 do padrão | muro, folha, selo azul, faixa preta, papéis e fitas tirados dos modelos | sim |
| Cartas inteiras | sem corte, filtro nem deformação | 7 cartas inteiras, cantos arredondados, proporção original | sim |
| Fita | só nos cantos de cima | dois cantos de cima; nome e custo visíveis (corrigido na passagem 2) | sim |
| Rodapé da carta (artista, ©) | visível | visível em todas | sim |
| Texto sobre a arte | nenhum | nenhum texto sobre cartas ou impressões de arte | sim |
| Nomes e números | = Scryfall | conferidos | sim |
| Legibilidade em telemóvel | texto ≥ 24 px; créditos legíveis | títulos 52–104 px, etiquetas 25–30 px; crédito 18 px (corrigido de 15 px) | sim |
| Ortografia | sem erros | revisto | sim |
| Coerência entre páginas | um só sistema | mesmo selo, folha, faixa e tipografia | sim |
| Direitos | créditos + «não oficial» | créditos em cada página e na legenda; «Conteúdo de fã não oficial» na legenda | sim |
| BINDER Vision | sem capturas fabricadas | nenhuma captura; uma função real na legenda (lista de desejos) | sim |
| Retenção | capa com Magic no quadro 0; revelação a cada página | carta real na capa; um par de cartas novo por página | sim |

Passagem corretiva (1): fitas encostadas ao nome das cartas, etiquetas sobrepostas no slide 2, «NA CAPA» fora do papel, crédito pequeno, afirmação não verificada («elemental da floresta») retirada.

## Ficheiros finais
Imagens não versionadas (recriam-se com `python3 -I carrossel.py <cartas> <foto.png> <foto_mask.png> <saida>`):
- `01_capa.png` … `07_encerramento.png` + `folha_de_contacto.jpg`: entregues ao fundador na conversa de 14/11/2026
- Capa: `01_capa.png`

## Pacote de publicação
- [x] `legenda.txt`
- [x] `comentario_fixado.txt`
- [x] `texto_alternativo.txt`
- [x] `fontes.md`

## Antes de publicar (fundador)
- Confirmar a autorização da Nathanna para a foto do slide 6 (ou pedir para trocar o slide sem foto).
