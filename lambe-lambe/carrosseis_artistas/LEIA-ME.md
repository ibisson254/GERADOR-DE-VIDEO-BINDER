# Carrosséis "Artistas de Magic" · padrão oficial do Lambe-lambe (v2, 12/11/2026)

Seis carrosséis 4:5 (5 imagens 1080×1350 cada), LL-ART13 a LL-ART18: John Avon, Mark Poole, Kev Walker, Magali Villeneuve, Raymond Swanland e Seb McKinnon. Cada pasta tem `FICHA.md` (fontes), `legenda.txt`, `comentario_fixado.txt` e `texto_alternativo.txt`.

**v2 (12/11, 12:04, pedido do fundador: «Tem que ser todos nesse padrão do ficheiro que lhe enviei»)**: segue as duas referências do fundador. Muro rosa áspero, cartaz creme rasgado a ocupar o slide, selo azul «Artistas de Magic» (sem o símbolo de Magic, marca da Wizards), gancho em letra condensada pesada com a palavra-chave em Archivo Black e risco rosa, imagem grande, faixa preta com o nome, linha creme e chip amarelo. A pintura grande é um **detalhe ampliado da arte real** da carta do artista (escolha do fundador), e a carta inteira aparece no carrossel. Sem retrato do artista: o da referência era um rosto gerado, não a pessoa real. A v1 (ilustração vetorial plana) foi reprovada e fica em `v1_reprovada/`.

## Estrutura (5 slides)
1. Capa (referência «Quem transforma terrenos em paisagens?»).
2. Editorial (referência «Jhon Avon», com a carta real no lugar do retrato): nome, frase manuscrita, número em papel, faixa preta.
3. Número grande + arte + carta inteira + faixa preta.
4. A história + arte + carta inteira.
5. Pergunta para os comentários + cartaz preto BINDER (ponte: scanner) + «Beta para Android · link na bio».

## Gerar
Em `gerador/` (não versionados): `cartas/<chave>.png` e `hd/<chave>.jpg` (art_crop do Scryfall ampliado 2,4× com Lanczos), `logo_mark.png`, woff2 de Archivo Black, Barlow Condensed 600/800, Kalam 700 e Geist 500/700 (@fontsource), e as texturas (`python3 -I texturas.py`). Depois:

    python3 -I render.py . <saida> avon poole walker magali swanland seb
    python3 -I pacotes.py cartas/creditos.json <saida_pacotes>
