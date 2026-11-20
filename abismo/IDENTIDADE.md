# ABISMO · Identidade (valores em `identidade.json`)

## Fundo mestre
O fundo das duas últimas cartas do vídeo de referência (Tecton e Abyssal Lotus), gerado pelo **mesmo código**
(`expedicao/template/fundo.py`, semente 11, camada `abismo`) e não por cópia de imagem:
- base carvão/azul-marinho com grão; feixe horizontal luminoso branco → magenta → ciano a ~44% da altura;
- coluna vertical espectral complementar; reflexos e partículas; `lotus` controla a intensidade do feixe.
- Estados: **tensão** (`lotus 0`) até ao momento de impacto; **mestre** (`lotus 1`) depois.
- Placas fixas: `kit/fundo_mestre_916.png`, `kit/fundo_mestre_45.png` (recorte y 285 do 9:16).

## Vida («o abismo respira») — `motor/vida.py`, valores em `identidade.json` → `vida`
**Hierarquia: a carta é o único destaque.** O fundo dá profundidade, não disputa a atenção.
1. Carta (pulsação no 1.º tempo do compasso: +1,2%, +2% depois do drop) → 2. texto e painel → 3. feixe de luz → 4. medusas e cáusticas.
- **Medusas** procedurais (ciano/magenta do feixe) que **atravessam o ecrã**: deriva lenta + impulso no fim de cada contração
  (a cada 4 batidas), rumo próprio, saem por um lado e voltam pelo outro. Profundidade = mais longe, menor, mais desfocada, mais fraca.
- **Quase impercetíveis**: força global 0,42, sem flash; no máximo cerca de 1/5 do brilho dos realces da carta (medido: pico 44/255 contra p95 213 da carta).
- **Zonas de calma**: atrás da carta o movimento cai para 12% e junto ao painel e legendas para 35%, com transição suave de 170 px.
- **Cáusticas** a 2,5%. Desligar tudo por post com `"vida": false`.

## Sistema gráfico
- **Medidor lateral** (x 44): RASOS · GRANDE MARINHO · ABISMO, marcador esmeralda desce até à camada da carta.
  Contador `n/N` só quando o post é uma sequência (`"sequencia": [n, N]`); nunca 1/6 para uma carta só.
- **Carta**: cantos arredondados, sombra suave, entrada com faixa de luz diagonal; crédito por baixo
  (`Nome · Coleção · Arte: Artista · © Wizards of the Coast`) sempre visível com a carta.
- **Ficha**: pílula escura `NOME · Tipo · Camada` antes da informação.
- **Cartão informativo**: fundo tinta #050A10 a ~78%, filete esmeralda à esquerda, sobretítulo esmeralda, título Inter Display Black;
  etiquetas só quando informam: verde = vantagem, vermelho = condição/custo, branco = dado neutro.
- **Etiqueta de leitura** (desde 20/11/2026): contorno branco sem preenchimento = interpretação estratégica (não confirmada); branco preenchido = facto oficial; vermelho = condição ou vazamento.
- **Modo «decks»** (Reel com vários decks, AB-04): cada deck só se distingue pelas suas cores de mana (pontos e filete do espaço da carta, nomes das cores por extenso); deck sem carta pública = espaço de carta vazio com «?». Layout em `modelos/reel.json` → `decks`.
- **Legendas de ecrã** (Reel; no Story o cartão informativo substitui-as, para não sobrepor): Inter Display Black 58, branco com palavras-chave a amarelo #FFD640, contorno tinta.
- **Marca**: só o logótipo oficial (`manaburn/logo/logo_mark.png`), canto superior direito a 60%; assinatura final
  com logótipo, "BINDER Vision" e "Link na bio". O símbolo nunca é redesenhado.
- Tipografia: Inter / Inter Display (sistema). Cores: esmeralda #10B981, tinta #050A10, amarelo #FFD640, condição #C82830.

## Som
- Música: **Auction of Power** (propriedade do fundador), 140 BPM, período 0,42865 s, offset 0,0349 s.
  Só se corta em batidas inteiras; a composição não é alterada. Marcas: intro 0, secção A 16, pausa 62–63, **drop 64**, fim B 96, cauda.
- Sincronia (modelos): introdução → entrada da carta (+4 batidas) → informação → **maior impacto no drop** → encerramento.
- Sons existentes: descida (entrada da carta), swell (sobe até ao drop), glitch (etiquetas vermelhas). Sem sons novos.
- Mistura −14 LUFS, pico ≤ −1,5 dBTP. Se houver voz: música ≥ 15 dB abaixo (tradução automática do Instagram).
