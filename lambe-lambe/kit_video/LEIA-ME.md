# kit_video · motor de vídeo do Lambe-lambe (padrão desde 26/11/2026)

Decisão do fundador (26/11/2026, 22:41): «torne padrão esse vídeo para todos os vídeos do lambe lambe», sobre o vídeo do LL-ECO01. O motor saiu do `campanha.py` do LL-ECO01 (que fica intacto, para reproduzir a peça) e generaliza-o.

## Linguagem
1. Quadro 0: o objeto (carta, logótipo, tela real) já colado, em tela cheia; a câmara recua em 0,6 s (`abertura`, `zoom0`).
2. Cada cena começa com **um cartaz grande** (1010×1560) colado por cima do anterior: `peca_folha(1010, 1560, tipo, seed)`, `de=(0, -1900)`, `som='grande'`. Alternar creme, kraft, preto (e amarelo/verde quando há razão).
3. Dentro da cena: faixas de papel com texto (`T`, `caixa`), cartas (`peca_carta`), imagens/logos (`peca_img`), autocolantes (`modo='pop'`), texto carimbado (`modo='carimbo'`). Uma ideia por faixa; 2 a 4 peças por cena; 2,5 a 4 s por cena.
4. Fecho oficial do scanner (`comum/outro/outro_binder_916.mp4`) sempre.

## Regras
- Zona segura do texto: y 280–1500, x 80–1000 (cabe nos Stories e nos Reels).
- Cartas grandes: `peca_carta_recortada(png, larg)` (carta inteira dentro de uma margem branca cortada à tesoura, fita nos cantos de cima). **Uma carta de cada vez**, grande (≥ 560 px de largura), colada por cima da anterior; nada de cartas lado a lado pequenas nem mosaicos ilegíveis (pedido do fundador, 26/11/2026, 23:27). Uma etiqueta curta por carta (nº, nome) fora da carta.
- Foto de pessoa: cartaz P&B fotocopiado (`kit_carrossel/recorte_foto.py`, máscara retangular), só com autorização da imagem registada para publicar.
- Carta inteira, sem filtro; fita só nos cantos de cima; nada sobre a arte nem sobre o rodapé (artista e ©). Para repetir cartas no mesmo sítio, colar a nova **por cima e do mesmo tamanho**.
- Texto: nunca maior do que o papel (o `caixa()` centra; use `white-space:nowrap` em palavras longas e confira na folha de contacto).
- Som: `audio=True` gera os efeitos (papel, cola, autocolante, carimbo) + leito de ar; pico real ≤ −6 dBFS verificado depois do AAC. `som='nada'` para peças em série (mosaicos).
- Zero créditos externos; texto pelo Chrome (Playwright): variável `CHROME`, senão `/usr/bin/google-chrome`, senão o Chromium do Playwright (funciona no PC do fundador desde 27/11/2026); fontes e dependências: `sh comum/ferramentas/preparar_ambiente.sh`.

## Uso
```python
import sys; sys.path.insert(0, '<raiz>/lambe-lambe/kit_video'); import motor_video as V
t = {'a': V.caixa(860, 240, V.T('Texto<br><span class="k">rosa</span>', 90))}
V.render_textos()
L = [V.Peca(V.peca_carta('carta.png', 460), 540, 990, 0, modo='fixa'),
     V.Peca(V.peca_folha(900, 270, 'creme', 1, -1.2, t['a'], fitas=((-.94, -1, -40), (.94, -1, 40))), 540, 500, .3, .4, de=(-80, -1500), rot0=-8),
     V.Peca(V.peca_folha(1010, 1560, 'kraft', 6), 540, 945, 3.2, .4, de=(0, -1900), rot0=-4, z0=1.15, som='grande')]
V.render(L, dur, 'saida.mp4', audio=True)          # + fecho; '--mudo' → audio=False
V.folha_contacto('saida.mp4', 'folha.jpg', [0, 1, 2.5, ...])
```
Classes de cor no texto: `k` rosa #E61E6E, `g` verde #10B981. Fonte `JP` para kanji (Noto Serif CJK).

## Desempenho e regressão (27/11/2026, `nucleo/auditorias/2026-11-27_motor_producao.md`)
- Cada peça compõe-se só na região que ocupa no quadro (antes: o quadro inteiro por peça, 42 % do render). LL-ART21 V4 (44,1 s, 4 núcleos): **264,6 s → 190,2 s (−28 %)**. Imagem: 1 píxel com ±1 nível em 14 de 1324 quadros compostos (arredondamento da interpolação), invisível.
- Onde o tempo vai agora: ~50 % no render dos quadros, ~35 % na preparação das peças (`matte`, 2 desenhos em tela cheia por peça, via `kit_carrossel/compor.py`), ~10 % no texto pelo Chrome. Próximo ganho possível: `matte` (ver o relatório, P2).
- Antes de integrar uma alteração que não deva mudar a imagem: renderizar antes e depois e `python3 -I comum/qc/comparar_videos.py ANTES.mp4 DEPOIS.mp4`.
- Pré-existente, não alterado: com `audio=True` o `-shortest` corta os 3 últimos quadros do fade final do fecho (1321 vs 1324).

## Exemplos
- `lambe-lambe/episodios/ll-eco01_sua_colecao_sua_comunidade_seu_jogo/campanha.py` (origem; versão própria do motor)
- `lambe-lambe/episodios/ll-art21_will_murai_alem_das_cartas/reel_v3.py` (primeiro episódio no kit)
