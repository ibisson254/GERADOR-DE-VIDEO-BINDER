# Vince Vault · Character Pack (especificação e prompts)

Versão 0.1 · 07/11/2026 · **proposta, não ativa**. Marcas [CONFIRMADO]/[PROPOSTA]/[HIPÓTESE]/[PENDENTE]: ver `PROPOSTA.md`.

**Estado:** nenhuma imagem foi gerada. Não há ferramenta de imagem nesta sessão e não se gastam créditos sem autorização (AGENTS.md §3). Este ficheiro deixa tudo pronto para a etapa seguinte: lista, especificações, paleta, proporções, guia de consistência e prompts.

## 1. Princípio

O pacote gera-se **uma vez**, aprova-se, e a partir daí **a personagem não se regenera** (constituição §6: reutilizar recursos mestres). Cada episódio só combina peças do pacote. Imagem que não passa no guia de consistência (§8) deita-se fora; nunca se "corrige" num episódio.

Ordem obrigatória: imagem-mestra → aprovação do fundador → vistas → expressões → poses e gestos → bocas e olhos → cenário.

## 2. Lista do pacote mínimo

| # | Ficheiro | Peça | Uso |
|---|---|---|---|
| 1 | `00_mestre.png` | **Imagem-mestra**: corpo inteiro, três quartos, neutro-confiante, telefone na mão | Referência de tudo; capa |
| 2 | `01_frente.png` | Vista frontal, corpo inteiro, braços ligeiramente afastados | Folha de modelo |
| 3 | `02_perfil.png` | Vista lateral (perfil esquerdo) | Folha de modelo; silhueta |
| 4 | `03_costas.png` | Vista traseira (mostra o cabelo e os suspensórios em X) | Folha de modelo; plano de costas na janela |
| 5 | `10_neutro.png` | Expressão neutra (busto) | Escuta, transições |
| 6 | `11_sorriso_arrogante.png` | Sorriso de canto, uma sobrancelha levantada | Gancho, "eu avisei" |
| 7 | `12_gargalhada.png` | Gargalhada, cabeça para trás | Euforia, Placar com acerto |
| 8 | `13_irritacao_vaultinho.png` | Olhos semicerrados, veia na testa, maxilar travado | Escada do Vaultinho |
| 9 | `14_panico.png` | Olhos arregalados, mãos na cabeça, cabelo a desmanchar-se num tufo | Desastre financeiro |
| 10 | `15_euforia.png` | Boca aberta, punhos no ar | To the Moon |
| 11 | `20_pe.png` · `21_sentado.png` | Em pé atrás da secretária; sentado na cadeira executiva (pernas fora de campo) | Planos de conjunto e de secretária |
| 12 | `30_telefone.png` · `31_apontar.png` · `32_suspensorios.png` · `33_gravata.png` · `34_bater_pasta.png` · `35_maos_cabeca.png` | Gestos característicos (ver `CONTEXTO.md` §12) | Troca por evento |
| + | `40_boca_A…F,X.png` | Bocas para sincronização labial (§6) | Fala |
| + | `50_olhos_aberto/semi/fechado/arregalado.png` | Olhos separados | Piscar, reações |
| + | `60_cenario_mestre.png` · `61_secretaria.png` · `62_impressora_painel.png` | Cenário-mestre e dois enquadramentos | Fundos fixos |
| + | `70_telefone_tijolo.png` · `71_pasta_cofre.png` · `72_impressora.png` | Adereços soltos | Animação de objetos |

Os itens 1–12 são o mínimo pedido pelo fundador. Os itens "+" são o que a opção C de `PRODUCAO.md` precisa para animar.

## 3. Paleta [PROPOSTA]

| Cor | Hex | Onde |
|---|---|---|
| Azul-marinho do fato | `#1C2541` | Fato, logótipo da Multiverse Capital |
| Risca de giz | `#C8CCD6` | Riscas finas do fato |
| Camisa azul-clara | `#CFE0F2` | Camisa |
| Colarinho branco | `#FFFFFF` | Colarinho e punhos (camisa de colarinho contrastante) |
| Vermelho-poder | `#B3202A` | Gravata, suspensórios, ▼ |
| Dourado | `#D4A72C` | Relógio, botões, abotoaduras, anel, ▲ |
| Cabelo | `#1A1412` | Cabelo, sobrancelhas |
| Mogno | `#5B2C1A` | Secretária, painéis de madeira |
| Couro bordô | `#6E1F24` | Cadeira executiva |
| Âmbar de monitor | `#FFB000` | Monitores CRT, pastilhas do painel de cotações |
| Preto do painel | `#111111` | Fundo do painel de cotações |
| Papel de formulário | `#F4EEDC` | Boleta da impressora (faixas `#E6EEF5`, azul-pálido) |

**Proibido na personagem e no cenário:** verde (o verde de terminal é do TUBO; o verde-esmeralda `#10B981` é do BINDER e só aparece no fecho). Neon, cromados futuristas e ecrãs planos modernos.

## 4. Proporções [PROPOSTA]

- Altura total: 6 cabeças (cartoon heroico; cabeça ligeiramente grande para as expressões lerem no telemóvel).
- Ombros: 2,8 larguras de cabeça (ombreiras de 1989). Cintura: 1,3. Tronco em triângulo invertido.
- Mãos grandes (0,8 da altura da cabeça) para os gestos lerem a 1080 px.
- Maxilar quadrado, queixo forte; olhos grandes castanhos; sobrancelhas grossas e muito móveis.
- Dentes brancos e perfeitos de mais (piada visual permanente).
- Idade aparente: início dos 40.
- Pele [PROPOSTA, confirmar]: bronzeado artificial de solário dos anos 80 (tom médio dourado). Fica fixo no pacote.
- Cabelo: escuro, volumoso, penteado para trás, rente à frente e com volume atrás; **não** é topete em onda.

## 5. Figurino [CONFIRMADO no essencial; detalhes PROPOSTA]

- Fato trespassado azul-marinho de risca de giz, lapelas largas, 6 botões dourados (2 apertados).
- Camisa azul-clara com colarinho e punhos brancos; abotoaduras douradas.
- Gravata vermelha com pequenos pontos dourados; suspensórios vermelhos (visíveis quando abre o casaco e nas costas, em X).
- Relógio dourado grosso no **pulso esquerdo**; anel dourado no **mindinho direito**.
- Lenço de bolso branco, sempre igual.
- Adereços: telefone-tijolo genérico (sem marca), pasta-cofre de couro bordô com fechadura de cofre dourada.
- **Sem:** charuto, bebida, óculos de sol, logótipos reais.

## 6. Camadas para a animação 2.5D (opção C)

| Camada | Variantes | Notas |
|---|---|---|
| Corpo + pose | `20_pe`, `21_sentado`, gestos 30–35 | Cada pose é uma imagem inteira sem cabeça (a cabeça vai por cima) ou com cabeça, conforme o que a ferramenta conseguir manter consistente |
| Cabeça base | Uma por ângulo (frente, três quartos) | Sem olhos nem boca, ou com olhos neutros |
| Olhos | aberto, semicerrado, fechado, arregalado | Piscar a cada 3–5 s; arregalado no pânico |
| Sobrancelhas | neutra, levantada (uma), franzida, preocupada | Separadas se a ferramenta o permitir; senão vêm nas expressões 10–15 |
| Bocas (Rhubarb) | A fechada (M, B, P) · B ligeiramente aberta com dentes · C aberta (E) · D muito aberta (A) · E arredondada (O) · F franzida (U, W) · X repouso | Mínimo A–F + X; G (F/V) e H (L) opcionais |
| Adereços | telefone, pasta, impressora | Movem-se como objetos |

Alinhamento: todas as camadas de cabeça partilham o mesmo ponto de ancoragem (centro do nariz) e a mesma escala; exportar com tela do mesmo tamanho para encaixar sem cálculo.

## 7. Referências visuais (descritivas, para orientar sem copiar)

- Iluminação e materiais de animação 3D familiar contemporânea: pele suave, formas limpas, cor saturada mas não neon.
- Moda masculina de escritório 1985–1992: ombreiras, riscas de giz, colarinho contrastante, suspensórios.
- Escritório de corretora de fim dos anos 80: mogno, latão, monitores CRT âmbar, telefones de secretária com fio e botões de linha, calculadora de fita, impressora matricial de formulário contínuo, painel de cotações de pastilhas.
- **Não usar** como referência direta nenhum filme, desenho ou pessoa real (ver `CONTEXTO.md` §13).

## 8. Guia de consistência (conferir cada imagem nova ao lado da mestra)

1. Linha do cabelo e volume atrás iguais; nenhum fio a cair na testa (exceto na expressão de pânico).
2. Sobrancelhas da mesma grossura; olhos castanhos; maxilar quadrado.
3. Fato: risca de giz visível, 6 botões dourados, lapelas largas; gravata com pontos dourados.
4. Relógio no pulso esquerdo; anel no mindinho direito; lenço branco no bolso.
5. Luz principal de cima à esquerda; contraluz quente à direita. Mesma lente aparente (sem grande-angular deformante).
6. Fundo cinzento neutro liso nas peças da personagem (para recorte limpo).
7. Nenhum texto, logótipo ou marca de água.
8. Registar na ficha do pacote: ferramenta, data, prompt exato e semente (se existir) de cada imagem aprovada.

Imagem que falha em 1–4 é rejeitada.

## 9. Prompts de geração (em inglês, porque as ferramentas de imagem respondem melhor)

### 9.1 Imagem-mestra (`00_mestre.png`)

```
Original cartoon character, stylized 3D animated-film look (soft skin shading,
clean appealing shapes, slightly exaggerated proportions), full body, three-quarter
front view, standing with an expansive confident posture.
A late-1980s Wall Street stockbroker in his early forties: athletic heroic build,
very broad shoulders, square jaw, big expressive brown eyes, thick mobile dark
eyebrows, voluminous dark hair slicked straight back (close at the front, volume at
the back, NOT a pompadour), 1980s tanning-bed tan, unnaturally perfect white teeth,
smug half-smile.
Navy double-breasted pinstripe suit with wide lapels and six gold buttons, light blue
shirt with white contrast collar and cuffs, red power tie with tiny gold dots, red
suspenders, white pocket square, chunky gold watch on the left wrist, gold pinky ring
on the right hand. Holding a large generic 1980s brick-style mobile phone (no brand).
Plain light grey studio background, soft key light from upper left, warm rim light
from the right. Character design quality, crisp readable silhouette.
Original design, not resembling any real person, actor or existing character.
No text, no logos, no watermark.
```

Negativo (se a ferramenta aceitar):
```
photorealistic, real person likeness, celebrity, existing cartoon character, logo,
brand name, text, watermark, futuristic, cyberpunk, neon, green screens, cigar,
cigarette, alcohol, anime style, extra fingers, deformed hands
```

### 9.2 Vistas (com a imagem-mestra como referência de personagem)

```
Same character as the reference image: identical face, hair, body proportions,
suit, colors and accessories. Character turnaround, [front view | left side
profile view | back view showing the red suspenders crossing in an X], neutral
standing pose, arms slightly away from the body, plain light grey background,
same lighting. No text.
```

### 9.3 Expressões (busto, mesma referência)

```
Same character as the reference image, identical face, hair and outfit. Bust shot,
three-quarter view, plain light grey background, same lighting.
Expression: [EXPRESSÃO]
```

| Ficheiro | [EXPRESSÃO] |
|---|---|
| `10_neutro` | calm, attentive, mouth closed, slight confidence |
| `11_sorriso_arrogante` | smug lopsided smirk, one eyebrow raised, chin slightly up |
| `12_gargalhada` | big triumphant laugh, head tilted back, eyes squeezed shut, perfect teeth showing |
| `13_irritacao_vaultinho` | offended outrage held back: narrowed eyes, clenched jaw, a vein on the forehead, nostrils flared, still dignified (not childish) |
| `14_panico` | financial panic: eyes wide open, both hands on his head, one strand of the slicked hair popping loose |
| `15_euforia` | euphoric celebration: mouth wide open shouting, both fists in the air |

### 9.4 Poses e gestos (corpo inteiro ou plano médio, mesma referência)

| Ficheiro | Pose |
|---|---|
| `20_pe` | standing behind a large mahogany desk, hands planted on the desk, leaning forward |
| `21_sentado` | sitting back in an oversized burgundy leather executive chair, legs out of frame |
| `30_telefone` | brick phone pressed to his ear, elbow raised high, shouting a deal |
| `31_apontar` | pointing both index fingers straight at the camera |
| `32_suspensorios` | thumbs hooked in his red suspenders, snapping them, chest out |
| `33_gravata` | adjusting his tie knot with one hand, smug |
| `34_bater_pasta` | knocking twice on a burgundy leather briefcase with a gold safe lock |
| `35_maos_cabeca` | both hands on his head, panicked |

### 9.5 Bocas (edição localizada da cabeça neutra)

```
Edit only the mouth of the reference head, keep everything else pixel-identical.
Mouth shape: [A: lips closed pressed (M/B/P) | B: slightly open, teeth visible |
C: open, as saying "eh" | D: wide open, as saying "ah" | E: rounded, as saying "oh" |
F: puckered, as saying "oo" | X: relaxed closed]
```

### 9.6 Cenário-mestre (`60_cenario_mestre.png`)

```
Interior of a late-1980s stockbroker's corner office at golden hour, stylized 3D
animated-film look, vertical 9:16 composition. Large mahogany desk with brass details,
oversized burgundy leather executive chair, two beige CRT monitors with amber
phosphor text, a beige desk phone with many line buttons and a coiled cord, a
calculator with paper tape, a dot-matrix printer feeding continuous-form paper,
an amber dot-matrix stock ticker board on the wall, a big window with a generic
painted retro city skyline (no real recognizable buildings). Warm, luxurious,
retro, no people. No green screens, no modern flat screens, no futuristic elements,
no text, no logos.
```

## 10. Entrega técnica

- PNG com transparência para personagem e adereços; PNG opaco para cenário.
- Personagem: ≥ 2048 px no lado maior. Cenário: 2160×3840 (2× o Reel), para permitir zoom sem perder nitidez.
- Mesma tela e mesmo ponto de ancoragem em todas as variantes de cabeça.
- Pasta: `vince-vault/assets/` (PNG pequenos o suficiente para o repositório; originais grandes ficam fora, como nas outras séries).
- Ficha do pacote: `vince-vault/assets/PACOTE.md` com ferramenta, data, prompt, semente e aprovação do fundador de cada peça.

## 11. Layout do Reel [PROPOSTA]

- Metade de cima: carta inteira (quando há carta) ou painel de cotações; nada por cima da carta.
- Metade de baixo: Vince à secretária; a boleta da impressora entra pela esquerda.
- Legenda de fala dentro da zona segura (mesmas margens do kit v2 do Mana & Burn: `left: 80px; right: 160px`), longe da coluna de botões do Instagram.
- Linha de fontes ≥ 24 px de altura, sempre visível enquanto o número está no ecrã.
