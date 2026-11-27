# Kit do carrossel Lambe-lambe · modelo pronto (sem ElevenLabs)

Padrão aprovado pelo fundador a 13/11/2026 («Modelo aceito se torne padrão para carrocel de lambe lambe»); reutilização sem custo a 14/11/2026 (`nucleo/DECISOES.md`).

## Peças versionadas
- `../referencias/carrossel_padrao_01.png` (capa) e `carrossel_padrao_02.png` (editorial): os dois modelos aprovados, sem texto. Fonte única do muro, da folha, do selo azul e da faixa preta.
- `kit_papel.png`, `kit_fita.png`, `mask_pintura_*.png`.
- `kit.py`, `compor.py` (camadas de texto em HTML impressas no papel), `recorte_foto.py` (foto do artista em recorte P&B).
- `motor_padrao.py`: `fundo(seed)`, `selo`, `papel`, `impressa` (arte com margem e fita), `carta` (carta inteira, fita nos cantos de cima, `fl` = largura da fita), `rodape` + `rodape_txt`, `traco`, `render`.
- `preparar_fontes.sh` + `desgaste.py`: instalam as fontes livres em `fontes/` (Archivo Black, Barlow Condensed, Rubik, Caveat Brush, Playfair Display, Geist).

## Fazer um carrossel novo
1. `sh lambe-lambe/kit_carrossel/preparar_fontes.sh` (uma vez por ambiente; precisa de npm e do Playwright; o Chrome é o da variável `CHROME`, o `/usr/bin/google-chrome` ou o Chromium do Playwright; tudo de uma vez: `sh comum/ferramentas/preparar_ambiente.sh`).
2. Descarregar do Scryfall `png` e `art_crop` das cartas (não versionar).
3. Copiar `lambe-lambe/episodios/ll-art13_nathanna_sete_cartas/carrossel.py`, trocar textos e cartas.
4. `python3 -I carrossel.py <cartas> <foto.png> <foto_mask.png> <saida>` → slides 1080×1350.

## Regras
Carta real inteira; fita só nos cantos de cima; nada sobre o rodapé da carta; sem texto sobre arte; crédito «carta (set nº) · artista · © Wizards of the Coast» em cada slide. Foto do artista só a enviada pelo fundador (ele pede a autorização ao artista), em recorte P&B que não tapa a arte. Sem geração de imagem nem créditos externos.

## Story do carrossel
Todo carrossel novo leva também o Story animado: `../kit_story/LEIA-ME.md` (padrão de 16/11/2026).
