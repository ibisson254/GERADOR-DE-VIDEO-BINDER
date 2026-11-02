# Relatório de QC · 02/11/2026

Ficheiro: `LAMBE_LAMBE_PRERELEASE_STAR_TREK_2026_FINAL.mp4` · SHA-256 `3e132426…0a574`.

## Resultado: NÃO APROVADO PARA PUBLICAÇÃO (0 P0, 4 P1 por resolver)

| Verificação | Resultado |
|---|---|
| Duração / quadros | 20,00 s · 600 quadros |
| Formato | 1080×1920 · 30 fps · H.264 High yuv420p · AAC 48 kHz |
| Conteúdo original / fecho | 484 + 116 quadros |
| Fecho sem alterações | Sim: framemd5 dos 116 quadros idêntico ao original |
| `qc_video.py --frente lambe` | Fecho presente em 16,13 s, dif. 0,0; 1 P1 (loudness) |
| Quadros pretos acidentais (0–16,1 s) | 0 |
| Carta fora do quadro | 0 quadros (geometria de todos os quadros) |
| Carta em repouso fora da zona segura | 0 |
| Sobreposição entre cartas | 0 |
| Texto sobre carta | 0: ordem de desenho + conferência visual |
| Carta contra imagem original | Retificação: diferença média 4,3–5,6 em 0–255 nas 8 cartas grandes (rodapé 5,1–6,1), consistente com escala e compressão |
| Rodapés visíveis | Sim, nas cartas grandes legíveis; nas pequenas, inteiros mas não legíveis em telemóvel (por tamanho) |
| Inspeção visual | Folha de contacto oficial, contact sheet e recortes a tamanho real |
| Texto | ≥ 30 px, dentro da zona segura; carimbo PRÉVIA em cima, de propósito |
| Pico dos efeitos | −6,0 dBFS na mistura (−5,9 dBTP no AAC) |

## Problemas

| Grav. | Problema | Quem resolve |
|---|---|---|
| P1 | Direitos por confirmar (Star Trek e peça promocional) | Fundador |
| P1 | −27,6 LUFS contra alvo −14: só há efeitos a −6 dBFS, como pedido; música entra no Instagram. Medir depois, ou aceitar por escrito | Fundador |
| P1 | Sincronização com a música real por validar: montada sem ouvir a faixa | Fundador, no Instagram |
| P1 | Imagens do Scryfall em vez dos ficheiros da galeria oficial | Fundador aceita, ou envia os ficheiros |
| P2 | Rasgo de transição cobre a carta durante 3 quadros em cada corte com rasgo | Opcional: trocar por corte seco |
| P2 | Cartas pequenas nos blocos C e D sem texto legível | Opcional |

Provas: contact sheet e `folha_contacto.png`, entregues fora do repositório.
