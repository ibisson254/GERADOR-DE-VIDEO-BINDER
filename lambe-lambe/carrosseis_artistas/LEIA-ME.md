# Carrosséis "Artistas de Magic" · padrão oficial do Lambe-lambe (12/11/2026)

Seis carrosséis 4:5 (5 imagens 1080×1350 cada), LL-ART13 a LL-ART18: John Avon, Mark Poole, Kev Walker, Magali Villeneuve, Raymond Swanland e Seb McKinnon. Cada pasta tem `FICHA.md` (fontes), `legenda.txt`, `comentario_fixado.txt` e `texto_alternativo.txt`.

## Estrutura fixa (5 slides)
1. Capa: selo azul "Artistas de Magic", gancho em cartaz pop, ilustração vetorial original, nome do artista em faixa marinho, chip amarelo e linha de contexto, "arrasta →".
2. "Quem pintou?": carta real inteira + nome a marcador + quem é.
3. Número grande (cartaz amarelo) + carta real + frase.
4. A história + carta real.
5. Pergunta para os comentários + cartaz preto BINDER (ponte: scanner) + "Beta para Android · link na bio".

Créditos das cartas no rodapé dos slides 2–4. Cartas inteiras, fita só nos cantos de cima.

## Gerar
Na pasta `gerador/` acrescentar (não versionados): `cartas/<chave>.png` (PNG do Scryfall, chaves em `creditos.json`), `logo_mark.png` (`manaburn/logo/`), `Geist-Bold.woff2`, `Geist-Medium.woff2`, `anton-latin-400-normal.woff2`, `permanent-marker-latin-400-normal.woff2` (@fontsource). Depois:

    python3 -I render.py . <saida> avon poole walker magali swanland seb
    python3 -I pacotes.py cartas/creditos.json <saida_pacotes>

Artista novo: entrada em `conteudo.js` (textos), em `ilustracoes.js` (SVG original) e as cartas em `creditos.json`.
