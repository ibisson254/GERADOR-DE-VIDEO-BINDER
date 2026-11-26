// MB-EP18 · O Lagarto Infinito (26/11/2026). Basking Broodscale + Rosie Cotton of South Lane (fichas infinitas) + Corpse Knight (vitória).
// Factos: Oracle e rulings no Scryfall (26/11/2026); combo no Commander Spellbook / EDHREC (2433-5641); Salt EDHREC (26/11/2026).
// Plano de prova (EP.prova) para as leituras do Mana; reação do Burn em grande plano; TV SAL abre e fecha.
// pose por fala: [Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano]
const CR = '© Wizards of the Coast. Conteúdo de fã não oficial.';
const BRO = 'Na tela: Basking Broodscale (Modern Horizons 3, 2024), nº 145. Arte: Caio Monteiro.<br>' + CR;
const ROS = 'Na tela: Rosie Cotton of South Lane (O Senhor dos Anéis: Contos da Terra-média, 2023), nº 27. Arte: Claudiu-Antoniu Magherusan.<br>' + CR;
const CIC = 'Na tela: Rosie Cotton of South Lane (LTR 27), Basking Broodscale (MH3 145) e ficha Eldrazi Spawn (MH3, arte Aleksi Briclot).<br>' + CR;
const CKN = 'Na tela: Corpse Knight (March of the Machine Commander, 2023), nº 321. Arte: Karl Kopinski.<br>' + CR;
const VID = 'Na tela: exemplo de mesa de 4 a 40 de vida. Corpse Knight (MOC 321, arte Karl Kopinski).<br>' + CR;
const PUT = { title: 'PUTÔMETRO', value: '13%', fill: 0.13, calc: ['Salt EDHREC 0,53', '÷ 4 = 0,13', 'Broodscale · 26/11'],
              levels: [['DE BOA', '#6FB487'], ['PUTO', '#F4B414'], ['BANE!', '#FF5A4E']] };
// linhas medidas nos PNG do Scryfall (744x1040), 26/11/2026
const HL_BROOD = [[0.075, 0.757, 0.845, 0.130]];        // «Whenever one or more +1/+1 counters… Add ◇»
const HL_MAY = [[0.49, 0.788, 0.43, 0.040]];            // «you may create»
const HL_FOOD = [[0.075, 0.636, 0.85, 0.110]];          // «When Rosie… create a Food token»
const HL_TOKEN = [[0.075, 0.790, 0.85, 0.118]];         // «Whenever you create a token, put a +1/+1 counter…»
const HL_CK = [[0.075, 0.645, 0.85, 0.105]];            // «Whenever another creature… each opponent loses 1 life»
const TXT = [0.06, 0.60, 0.88, 0.28];
const EP = {
  id: 'ep18_lagarto_infinito',
  bug: 'TV SAL',
  poster: 'dragao',
  fx: { foco: true, tremor: true, poster: true, celular: true, scanner: false, tv_ligada: true },
  outro: { assinatura: 'Escaneie suas cartas e organize sua coleção.' },
  card: { img: 'cards/t00_lagarto.png', cred: BRO },
  abertura: { img: 'cards/broodscale.png', ate: 0.55, hl: HL_BROOD, selo: { txt: '2 MANAS → ∞', x: 0.07, y: 0.11, rot: -6, size: 54 } },
  legenda_paginas: 58,
  prova: { w: 620, top: 330, segs: [
    { fala: 1, de: 0, img: 'cards/broodscale.png', hl: HL_BROOD, zoom: { de: 0.35, alvo: TXT, s: 1.6 }, faixa: 'MARCADOR +1/+1 → FICHA' },
    { fala: 1, de: 0.72, img: 'cards/spawn.png', faixa: 'FICHA ELDRAZI SPAWN 0/1' },
    { fala: 3, de: 0, img: 'cards/rosie.png', hl: HL_FOOD, faixa: 'ENTRA: CRIA UMA COMIDA' },
    { fala: 3, de: 0.4, img: 'cards/food.png', faixa: 'FICHA DE COMIDA' },
    { fala: 3, de: 0.62, img: 'cards/rosie.png', hl: HL_TOKEN, zoom: { de: 0.7, alvo: TXT, s: 1.6 }, faixa: 'TODA FICHA → +1/+1 NO LAGARTO' },
    { fala: 5, de: 0, img: 'cards/t05a.png', tipo: 'tela' },
    { fala: 5, de: 0.36, img: 'cards/t05b.png', tipo: 'tela' },
    { fala: 5, de: 0.7, img: 'cards/t05c.png', tipo: 'tela' },
    { fala: 7, de: 0, img: 'cards/broodscale.png', hl: HL_MAY, zoom: { de: 0.25, alvo: TXT, s: 1.6 }, faixa: '«YOU MAY» = VOCÊ ESCOLHE' },
    { fala: 9, de: 0, img: 'cards/corpse_knight.png', hl: HL_CK, zoom: { de: 0.4, alvo: TXT, s: 1.6 }, faixa: 'CADA OPONENTE PERDE 1' },
    { fala: 11, de: 0, img: 'cards/t11_resposta.png', tipo: 'tela' },
  ] },
  pose: [
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'tv'],      // 1 B gancho (abertura → TV)
    ['rest', 'finger', 'other', 'x', 'normal', 'x', 'tv'],           // 2 M Lê a carta (prova: Broodscale → Spawn)
    ['arms_up', 'rest', 'cam', 'other', 'up', 'flat', 'cuB'],        // 3 B quem dá marcador? (rosto)
    ['rest', 'finger', 'other', 'x', 'normal', 'x', 'tv'],           // 4 M Rosie (prova: Rosie → Comida → Rosie)
    ['shrug', 'rest', 'cam', 'other', 'up', 'flat', 'cuB'],          // 5 B Comida é ficha?! (rosto)
    ['rest', 'finger', 'other', 'x', 'up', 'x', 'tv'],               // 6 M o ciclo (prova: painéis)
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],     // 7 B não acaba nunca?! (rosto, tremor)
    ['rest', 'finger', 'other', 'x', 'normal', 'x', 'tv'],           // 8 M pode criar (prova: Broodscale)
    ['point_cam', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],   // 9 B ficha 0/1 não mata (rosto)
    ['rest', 'finger', 'other', 'x', 'up', 'x', 'tv'],               // 10 M Corpse Knight (prova: flip)
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'tv'],      // 11 B quarenta Spawns (TV: vida 40 → 0)
    ['rest', 'finger', 'other', 'x', 'normal', 'x', 'tv'],           // 12 M se ninguém responder (prova: painel)
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'tv'],      // 13 B A/B (TV)
    ['rest', 'remote', 'other', 'cam', 'normal', 'up', 'cuM'],       // 14 M Comenta aí
  ],
  quadroDir: 'kit/v3/conde/',
  quadro: ['neutro', 'desconfiado', 'desconfiado', 'desconfiado', 'indignado', 'admirado', 'indignado', 'admirado',
           'desconfiado', 'admirado', 'indignado', 'admirado', 'neutro', 'neutro'],
  inserts: [],
  canais: [
    { de: 0, ch: 2, canal: 'O LAGARTO', img: 'cards/t00_lagarto.png', cred: BRO, meter: null, table: null },
    { de: 1, ch: 6, canal: 'LÊ A CARTA', img: 'cards/broodscale.png', cred: BRO, meter: null, table: null },
    { de: 3, ch: 11, canal: 'LÊ A CARTA', img: 'cards/rosie.png', cred: ROS, meter: null, table: null },
    { de: 5, ch: 14, canal: 'O CICLO', img: 'cards/t05c.png', cred: CIC, meter: null, table: null },
    { de: 9, ch: 21, canal: 'LÊ A CARTA', img: 'cards/corpse_knight.png', cred: CKN, meter: null, table: null },
    { de: 10, ch: 40, canal: 'MESA DE 4', img: 'cards/t10_vida.png', meio: { at: 0.5, img: 'cards/t10_vida_b.png' }, cred: VID, meter: null, table: null },
    { de: 11, ch: 41, canal: 'EM RESPOSTA', img: 'cards/t11_resposta.png', cred: BRO, meter: null, table: null },
    { de: 12, ch: 45, canal: 'E VOCÊ?', img: 'cards/t12_ab.png', meio: { at: 0.5, img: 'cards/t12_ab_b.png' }, cred: BRO, meter: null, table: null },
  ],
  tv: {
    channel: 'TV SAL', clock: '01:45',
    meter: PUT, table: null,
    news: [
      'PLANTÃO: lagarto de duas manas pede música de suspense',
      'Hobbit oferece comida e a mesa perde a fome de vez',
      'Ficha 0/1 jura que é inofensiva; ninguém acredita',
      'Contador de marcadores pede aumento de salário',
      'Cavaleiro cadáver cobra pedágio na entrada',
      'Remoção em resposta: a melhor amiga da mesa',
      'Plantão anterior: comandante dá carta e bate no sorteio',
    ],
  },
};
