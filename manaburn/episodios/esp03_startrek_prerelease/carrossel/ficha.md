# Carrossel · Especial pré-release Star Trek · "5 armadilhas do pré-release"

Derivado do especial "BURN FOI ASSIMILADO!" (06/11/2026). 8 slides 1080×1350. Produzido, não publicado.

## Ideia refinada
O Reel diverte; o carrossel é o **guia de bolso para levar à loja**. Em vez de repetir o vídeo, cada ato vira uma armadilha com a regra que a desarma:
capa → 5 armadilhas (fala do Burn = o erro; carta real inteira + recorte do texto com o destaque do vídeo + "A regra" + resposta do Mana) → as 3 apostas do Mana com barra de certeza → pergunta A/B + scanner real.
- Objetivo: **guardados** (o leitor salva para consultar no pré). Secundário: respostas A/B.
- Hipótese: o carrossel-guia tem mais guardados por alcance do que o Reel do mesmo tema.
- Publicar no fim de semana do pré-release (6–12/11), depois do Reel, e partilhar nos Stories.

## Construção
- Personagens e TV: recortes do render do especial (nada redesenhado). Cartas: PNGs do Scryfall, inteiras, rodapé livre; os destaques ficam só no recorte ampliado do texto.
- Recriar: copiar `carrossel.html` e `gerar_carrossel.py` para `<kit>/carrossel/`, criar `assets/` com os recortes (quadros do render em kit-time: TV 2,4 s; Burn 66,5 s e 20,5 s; Mana 23 s e 37 s; sofá 87 s; `comum/outro/scan/017.jpg`) e correr `python3 gerar_carrossel.py`.

## Fatos
Todos vêm de `../ficha_fontes.md` (Oracle via Scryfall, notas de lançamento e guia de pré-release da Wizards, 06/11/2026). Novo só "drones custam 2" (Vexing Drone e Tenacious Drone, Oracle TRK 45 e 133, {1}{W} e {1}{B}).

## Conferência
- [x] Cartas reais, inteiras, sem nada por cima do rodapé; créditos em cada slide
- [x] Textos dentro da margem de 40 px; legível a 540 px de largura (folha de contacto)
- [x] Legenda 790 caracteres (faixa do carrossel 600–1.100), gancho com 72, 5 hashtags, CTA diferente do Reel
- [x] Comentário fixado 753 caracteres, pergunta na primeira linha
- [x] Previsões marcadas como apostas; certeza = opinião do Mana
- Métrica principal: guardados por 1.000 alcançados. Resultado: —
