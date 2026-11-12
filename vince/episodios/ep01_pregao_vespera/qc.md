# VV-EP01 v2 · relatório de controlo de qualidade (12/11/2026)

Ferramenta: `python3 -I comum/qc/qc_video.py MultiverseCapital_Ep01_PregaoDeVespera_v2_916.mp4 --frente vince` (perfil `vince` acrescentado ao QC nesta sessão: 1080×1920, 30 fps, 30–45 s, fecho obrigatório). Resultado: `qc.json`; folha: `folha_contacto.jpg`.

## Medido
| Critério | Alvo | Resultado |
|---|---|---|
| Formato | 1080×1920, 30 fps | OK |
| Duração | 30–45 s | 44,77 s com fecho (40,9 s sem) · OK |
| Loudness | −14 ± 1 LUFS | −14,3 · OK |
| Pico verdadeiro | < −1 dBTP | −1,3 · OK |
| Fecho oficial | presente | aos 40,9 s, diferença 0,06 · OK |
| Corte lateral | nenhum | `cropdetect` 1080:1920:0:0 em todos os quadros · OK |
| P0 / P1 / P2 | 0 | 0 / 0 / 0 |

## Conferido a olho (folha de contacto do ficheiro final)
- Tese compreensível: número → carta → «quantas vendas?» → má notícia → dado → menor anúncio → conclusão. OK
- Todos os números no ecrã têm fonte e data/hora; reais com conversão documentada. OK
- Carta inteira, sem nada por cima; créditos legíveis. OK
- Textos e legendas fora da zona da interface (220 px em cima, 380 px em baixo, 140 px à direita). OK
- Personagem no modelo aprovado; poses diferentes para emoções diferentes; quem ouve reage (ao telefone → palma na testa). OK
- Regra da Fonte: um telefonema; sem voz, sem legenda, sem imagem. OK
- BINDER Vision: só o fecho oficial, gravação real; nenhuma tela simulada. OK

## Defeitos encontrados e corrigidos nesta versão
1. P1 · pico −0,5 dBTP → limitador de pico na mistura → −1,3 dBTP.
2. P1 · fim das linhas do painel dentro da faixa direita da interface → planos de painel recentrados (zoom 1,25, painel a terminar em 922 px).
3. Editorial (v1 → v2): afirmações sem prova retiradas (ver ficha); ritmo de 0,4–1,7 s → 3–4,5 s; placas pretas, flashes, sincronia labial e efeitos sonoros decorativos retirados; capa da v1 («1 VENDA.») substituída.

## Fica para o fundador (não bloqueia o QC)
- Ouvir a voz (sem transcrição automática neste ambiente).
- Confirmar a licença da faixa para o Instagram.
- Os preços de pré-venda mudam depressa: se publicar depois de 13/11, atualizar os números do painel e da legenda.
