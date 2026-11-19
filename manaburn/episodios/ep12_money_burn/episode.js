// MB-EP12 · MONEY BURN · «Só falta uma carta» (custo do hobby: o deck que nunca fica pronto). Kit v2 + sala v3.
// Oracle de todas as cartas conferido no Scryfall a 19/11/2026. Uma tela da TV SAL por fala (EP.canais) ou insert nos cuB.
// pose por fala: [Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano]
const CR = '© Wizards of the Coast. Conteúdo de fã não oficial.';
const M_UB  = { title: 'CUSTO', value: '5', fill: 0.62, calc: ['3 + 2 brancas', 'feitiço', 'Oracle'], levels: [['CARO', '#FF5A4E'], ['MÉDIO', '#F4B414'], ['BARATO', '#6FB487']] };
const M_VOL = { title: 'CORES', value: '2', fill: 0.4, calc: ['azul ou', 'vermelha', 'Oracle'], levels: [['TODAS', '#FF5A4E'], ['DUAS', '#F4B414'], ['UMA', '#6FB487']] };
const M_OPP = { title: 'CUSTO', value: '6', fill: 0.75, calc: ['compra 4', 'cartas', 'Oracle'], levels: [['CARO', '#FF5A4E'], ['MÉDIO', '#F4B414'], ['BARATO', '#6FB487']] };
const M_GRE = { title: 'VIDA POR CARTA', value: '2', fill: 0.5, calc: ['1 preta + 2 vidas', '= 1 carta', 'Oracle'], levels: [['CARO', '#FF5A4E'], ['MÉDIO', '#F4B414'], ['BARATO', '#6FB487']] };
const M_POP = { title: 'POR NÃO BÁSICO', value: '2', fill: 1, calc: ['cada jogador', 'custa 2 manas', 'Oracle'], levels: [['DEVASTADOR', '#FF5A4E'], ['CHATO', '#F4B414'], ['DE BOA', '#6FB487']] };
const EP = {
  id: 'ep12_money_burn',
  bug: 'TV SAL',
  poster: 'artefato',
  fx: { foco: true, tremor: true, poster: true, celular: true, scanner: false, tv_ligada: true },
  outro: { assinatura: 'Escaneie suas cartas e organize seus decks.' },
  card: { img: 'cards/unfinished.png',
          cred: 'Na TV: Unfinished Business (Wilds of Eldraine Commander, 2023), nº 44. Arte: Mark Zug.<br>' + CR },
  pose: [
    ['point_tv', 'rest', 'tv', 'other', 'up', 'flat', 'tv'],        // 1 B deck pronto, só falta uma (quadro 0: Unfinished Business)
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tvtext'],   // 2 M março · destaque no nome da carta
    ['point_tv', 'rest', 'tv', 'other', 'up', 'flat', 'tv2'],        // 3 B dez básicos → grife (tela Montanha → Volcanic)
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],       // 4 M Lê a carta: azul ou vermelha
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'tv'],      // 5 B oportunidade (Opportunity)
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],       // 6 M seis de mana, compra quatro
    ['point_tv', 'rest', 'tv', 'other', 'up', 'flat', 'tv'],       // 7 B gastar é estratégia (Greed na TV)
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],       // 8 M duas de vida por carta · Pix
    ['arms_up', 'rest', 'cam', 'other', 'up', 'flat', 'cuB'],        // 9 B intocável (insert: as compras)
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],       // 10 M Price of Progress: dois por não básico
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],     // 11 B VINTE?! (insert: 20 de dano, tremor)
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tvtext2'],  // 12 M a resposta custa duas manas · destaque {1}{R}
    ['point_cam', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],   // 13 B pergunta A/B (insert: A/B)
    ['rest', 'remote', 'other', 'cam', 'normal', 'up', 'cuM'],       // 14 M Comenta aí (TV desliga)
  ],
  inserts: [
    { file: 'cards/i09_upgrades.png', line: 8, at: 0.05, until: 9,
      cred: 'Volcanic Island (VMA 324, Noah Bradley) · Opportunity (J25 338, Allen Williams) · Greed (MH2 274, Izzy).' },
    { file: 'cards/i11_vinte.png', line: 10, at: 0.05, until: 11,
      cred: 'Conta: 2 de dano × 10 terrenos não básicos (Oracle de Price of Progress).' },
    { file: 'cards/s13_ab.png', line: 12, at: 0.05, until: 13,
      cred: 'Unfinished Business (WOC 44, Mark Zug).' },
  ],
  canais: [
    { de: 0, ch: 3, canal: 'O DECK DO BURN', img: 'cards/unfinished.png',
      cred: 'Na TV: Unfinished Business (Wilds of Eldraine Commander, 2023), nº 44. Arte: Mark Zug.<br>' + CR,
      hl: { tvtext: { rects: [[0.075, 0.052, 0.50, 0.048]], zoom: 1.5 } }, meter: M_UB, table: null },
    { de: 2, ch: 4, canal: 'UPGRADE', img: 'cards/s03_grife.png',
      cred: 'Na TV: Mountain (Foundations, 2024), nº 279, arte Rebecca Guay; Volcanic Island (Vintage Masters, 2014), nº 324, arte Noah Bradley.<br>' + CR,
      meter: M_VOL, table: null },
    { de: 3, ch: 5, canal: 'LÊ A CARTA', img: 'cards/volcanic.png',
      cred: 'Na TV: Volcanic Island (Vintage Masters, 2014), nº 324. Arte: Noah Bradley.<br>' + CR,
      hl: { tvtext: { rects: [[0.13, 0.745, 0.74, 0.05]], zoom: 1.5 } }, meter: M_VOL, table: null },
    { de: 4, ch: 6, canal: 'PROMOÇÃO', img: 'cards/opportunity.png',
      cred: 'Na TV: Opportunity (Foundations Jumpstart, 2024), nº 338. Arte: Allen Williams.<br>' + CR,
      hl: { tvtext: { rects: [[0.77, 0.054, 0.16, 0.046], [0.09, 0.700, 0.68, 0.045]], zoom: 1.5 } }, meter: M_OPP, table: null },
    { de: 6, ch: 7, canal: 'ESTRATÉGIA', img: 'cards/greed.png',
      cred: 'Na TV: Greed (Modern Horizons 2, 2021), nº 274. Arte: Izzy.<br>' + CR,
      hl: { tvtext: { rects: [[0.086, 0.703, 0.60, 0.045]], zoom: 1.5 } }, meter: M_GRE, table: null },
    { de: 9, ch: 8, canal: 'PLANTÃO', img: 'cards/pop.png',
      cred: 'Na TV: Price of Progress (Eternal Masters, 2016), nº 141. Arte: Yohann Schepacz.<br>' + CR,
      hl: { tvtext: { rects: [[0.08, 0.674, 0.84, 0.036], [0.08, 0.710, 0.84, 0.036], [0.08, 0.745, 0.83, 0.036]], zoom: 1.5 },
            tvtext2: { rects: [[0.82, 0.054, 0.13, 0.046]], zoom: 1.5 } },
      meter: M_POP, table: { label: ['DANO', 'NO BURN'], value: '20', note: ['2 × 10 terrenos', 'não básicos'] } },
    { de: 12, ch: 9, canal: 'COMENTA A OU B', img: 'cards/s13_ab.png',
      cred: 'Na TV: Unfinished Business (Wilds of Eldraine Commander, 2023), nº 44. Arte: Mark Zug.<br>' + CR,
      meter: M_UB, table: null },
  ],
  tv: {
    channel: 'TV SAL', clock: '10:20',   // easter egg: 10 terrenos de grife, 20 de dano do Price of Progress
    meter: M_UB, table: null,
    news: [
      'URGENTE: deck pronto pede só mais uma carta',
      'Juiz confirma: Volcanic Island faz azul ou vermelha, e mais nada',
      'Opportunity: seis manas para comprar quatro cartas',
      'Greed cobra duas de vida por carta desde 1994',
      'Price of Progress volta a assustar mesas de Commander',
      'Price of Progress: duas de dano por terreno não básico',
      'Sofá estuda trocar a Montanha por outra Montanha',
      'Plantão anterior: o dragão flanelinha',
    ],
  },
};
