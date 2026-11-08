# Vince Vault · Ficha visual

Características visuais fixas do personagem, para quem gera imagens, anima em código ou confere uma geração nova. Fonte: `referencias/01_turnaround_OFICIAL.jpg` (manda sobre tudo), mais as expressões e poses aprovadas. O bloco de prompt para geração está na bíblia (§2) e não se repete aqui. Atualizado a 08/11/2026.

## 1. Estilo

- Personagem 3D estilizado, render de longa-metragem de animação: pele com subsurface suave, luz cinematográfica, materiais limpos.
- Caricatura: proporções heroicas exageradas, sem realismo fotográfico.
- Sempre o mesmo rosto, o mesmo cabelo, a mesma roupa. Muda só a expressão, a pose e o cenário.

## 2. Silhueta e proporções

| Traço | Medida (turnaround, vista de frente) |
|---|---|
| Altura total | ~3,6 cabeças (do topo do topete ao queixo) |
| Topete | ~40% da altura da cabeça, acima das sobrancelhas |
| Ombros | muito largos, ~3,5× a largura do rosto; tronco em V |
| Mandíbula | quadrada e enorme, tão larga quanto a testa; queixo saliente |
| Pernas | relativamente curtas e direitas; pés pequenos para o corpo |
| Mãos | grandes, sempre com 5 dedos |

Leitura da silhueta a preto: topete alto e inclinado para trás + ombros largos + mandíbula grande. Se a silhueta não se reconhece, a geração falha.

## 3. Cabeça e rosto

- Adulto, início dos 40. Pele morena quente.
- Sobrancelhas grossas, escuras e arqueadas, muito expressivas.
- Olhos castanho-escuros, médios; olhar confiante.
- Nariz reto e largo, sem exagero.
- Costeletas pretas compridas, até meio da orelha.
- Sorriso de vendedor: de lado (confiante) ou aberto com dentes brancos (eufórico, a rir).
- Topete: preto brilhante, alto, penteado para trás, sempre com o mesmo perfil. Em cenários roxos ganha um reflexo violeta; com luz neutra, cinza-carvão.

## 4. Óculos

- Aviador com armação dourada fina e lentes castanho-fumado.
- **Um par só**, numa de duas posições: na cara ou levantado no topete.
- No lip sync e quando o olhar importa: no topete, olhos à vista.

## 5. Roupa

| Peça | Detalhe |
|---|---|
| Fato | Trespassado, azul-marinho-carvão com riscas de giz finas e claras; lapela de bico; 6 botões dourados na frente (2 colunas × 3); botões dourados nos punhos |
| Camisa | Branca, colarinho clássico; punho branco visível abaixo da manga |
| Gravata | Vermelha de seda com padrão paisley em vermelho mais escuro; nó médio |
| Lenço | Vermelho, no bolso do peito, do lado esquerdo do personagem (direita de quem vê) |
| Calças | Do mesmo tecido do fato, vinco direito |
| Sapatos | Pretos de couro, sociais, engraxados com brilho |

## 6. Acessórios

- Relógio dourado grosso, bracelete de elos, no **pulso esquerdo**.
- Anel de sinete dourado na **mão direita**.
- Desvio aceite: anel também na mão do relógio (aparece na base para falar e nas poses). Não é preciso refazer por isso.

## 7. Paleta de referência

Valores aproximados, amostrados nas referências; a luz do cenário altera-os. Servem para conferir gerações e para elementos desenhados em código (molduras, legendas, gráficos).

| Elemento | HEX |
|---|---|
| Pele (luz) | `#B07A55` |
| Pele (sombra) | `#9B643F` |
| Cabelo | `#0F0F11` |
| Reflexo do cabelo (luz neutra) | `#2A2A30` |
| Fato | `#1E1F2A` |
| Riscas do fato | `#9AA0B4` |
| Camisa | `#D9DADD` |
| Gravata | `#943838` |
| Paisley da gravata | `#6E2226` |
| Lenço | `#7E1719` |
| Dourado (botões, relógio, anel, armação) | `#C9A45C` |
| Dourado (sombra) | `#6A4A1E` |
| Lentes | `#2A1510` |
| Sapatos | `#141416` |

## 8. Expressões e poses aprovadas

| Nome em código | Origem | Uso |
|---|---|---|
| `neutro`, `confiante`, `rindo` | Grelha C, linha 1 | Apresentação, comentário |
| `furioso`, `chocado`, `desesperado` | Grelha C, linha 2 | Queda de preço, susto |
| `sarcastico`, `pensativo`, `euforico` | Grelha C, linha 3 | Ironia, análise, alta |
| Grelha A | `02_expressoes_A.png` | Alternativa; no "furioso" o rosto fica vermelho (efeito cómico) |
| `pose_andar`, `pose_piscadela` | Corpo inteiro, fundo cinza | Entradas e chamada para ação |
| `pose_confiante_pregao` | Corpo inteiro no cenário | Plano de apresentação |
| Base para falar | `03_base_falar_916.jpg` | Só lip sync do gancho |

Recorte para fantoche: `episodios/ep00/recortes.py` tira o fundo cinza das expressões e poses. Atenção: o `desesperado` tem cinza preso entre os braços e precisa de recorte manual antes de ser usado.

## 9. Cenário e luz

- Pregão da bolsa à noite: roxo e índigo, monitores CRT com brilho violeta e verde, candeeiros âmbar, madeira escura e latão.
- Monitores de fundo só com gráficos abstratos, sem números nem texto.
- Ecrã de leitura em verde (#00B140) para compor dados e telas reais do app.
- Gráficos e números desenhados em código: verde `#10B981` para alta, vermelho `#EF4444` para baixa, âmbar `#FBBF24` para radar, fundo `#050A10`.

## 10. Animação em fantoche (código)

- Movimentos permitidos: respiração lenta, entrada lateral com mola, balanço curto ao falar, troca de expressão no corte, flash curto no corte.
- Nunca: deformar o rosto, esticar o personagem fora de proporção, espelhar a imagem (troca o relógio e o lenço de lado).
- O lip sync fica só no gancho (3–5 s); o resto é fantoche.
- Cartas mostradas pelo Vince ficam inteiras, sem nada por cima, e nada corta as laterais do vídeo.

## 11. Conferir uma geração nova

1. A silhueta bate com o turnaround?
2. Um só par de óculos, dourado?
3. Relógio no pulso esquerdo e lenço do lado esquerdo do personagem?
4. Gravata vermelha paisley, fato risca de giz, 6 botões dourados?
5. Mãos com 5 dedos?
6. Sem texto, letras nem logótipos na imagem?
7. Formato pedido (9:16) e enquadramento com folga?

O controlo de qualidade completo das gerações do Gemini está em `PROMPTS_GEMINI.md`.
