// MB-EP17 · React collab @magicamador (24/11/2026). Personagens só nos blocos de reação; o vídeo original
// (Reel de @magicamador, 12/12/2025) entra entre blocos na montagem final (montar_react.py).
// Factos: Oracle em PT no Scryfall (24/11/2026); regra 702.15b (vínculo com a vida = dano causado); dano prevenido não é causado.
// pose por fala: [Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano]
const CR = '© Wizards of the Coast. Conteúdo de fã não oficial.';
const VIN = 'Na tela: Vingadora Phyrexiana (Phyrexia: All Will Be One, 2023), nº 27. Arte: Denys Tsiperko.<br>' + CR;
const OCE = 'Na tela: Bando de Ocelot (Modern Horizons 3, 2024), nº 38. Arte: Chris Seaman.<br>' + CR;
const LUZ = 'Na tela: Bando de Ocelot (MH3, 2024), nº 38, arte Chris Seaman · Luz da Promessa (M21, 2020), nº 25, arte Cristi Balanescu.<br>' + CR;
const CRED_AB = 'Partida original: @magicamador. Cartas © Wizards of the Coast. Conteúdo de fã não oficial.';
const M16 = { title: 'DANO', value: '16', fill: 0.8, calc: ['16/16 na mesa', 'partida @magicamador', 'Oracle ONE 27'],
             levels: [['PREVINE', '#6FB487'], ['16', '#F4B414'], ['DEVOLVE', '#FF5A4E']] };
const HL_PREV = [[0.07, 0.676, 0.86, 0.06]];
const HL_ALVO = [[0.07, 0.736, 0.86, 0.09]];
const HL_VINC = [[0.05, 0.645, 0.50, 0.036]];
const HL_LUZ = [[0.05, 0.680, 0.90, 0.112]];
const TXT_VIN = [0.06, 0.62, 0.88, 0.22], TXT_OCE = [0.04, 0.62, 0.92, 0.10], TXT_LUZ = [0.05, 0.63, 0.90, 0.18];
const EP = {
  id: 'ep17_react_magicamador',
  bug: 'TV SAL',
  poster: 'dragao',
  fx: { foco: true, tremor: true, poster: true, celular: true, scanner: false, tv_ligada: true },
  outro: { assinatura: 'Escaneie suas cartas e organize sua coleção.' },
  card: { img: 'cards/vingadora.png', cred: VIN },
  abertura: { img: 'cards/vingadora.png', ate: 0.55, hl: HL_ALVO, selo: { txt: '16 DE VOLTA', x: 0.07, y: 0.12, rot: -6, size: 58 } },
  legenda_paginas: 58,
  prova: { w: 620, top: 330, segs: [
    { fala: 3, de: 0, img: 'cards/vingadora.png', hl: HL_PREV, zoom: { de: 0.3, alvo: TXT_VIN, s: 1.6 }, faixa: 'O DANO NELA É PREVENIDO' },
    { fala: 3, de: 0.5, img: 'cards/vingadora.png', hl: HL_ALVO, zoom: { de: 0.5, alvo: TXT_VIN, s: 1.6 }, faixa: 'ELA ESCOLHE O OUTRO ALVO' },
    { fala: 4, de: 0.4, img: 'cards/ocelot.png', hl: HL_VINC, faixa: 'VÍNCULO COM A VIDA' },
    { fala: 5, de: 0, img: 'cards/ocelot.png', hl: HL_VINC, zoom: { de: 0.05, alvo: TXT_OCE, s: 1.6 }, faixa: 'DANO PREVENIDO NÃO É CAUSADO' },
    { fala: 5, de: 0.55, img: 'cards/luz.png', hl: HL_LUZ, zoom: { de: 0.7, alvo: TXT_LUZ, s: 1.5 }, faixa: 'SEM VIDA, SEM MARCADOR' },
  ] },
  pose: [
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'tv'],      // 1 B gancho (abertura → TV)
    ['rest', 'finger', 'other', 'cam', 'normal', 'x', 'wide'],       // 2 M ouve a proposta
    ['arms_up', 'rest', 'cam', 'other', 'up', 'flat', 'cuB'],        // 3 B correto?!
    ['rest', 'finger', 'other', 'x', 'normal', 'x', 'tv'],           // 4 M lê a carta (prova Vingadora)
    ['shrug', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],       // 5 B vínculo (rosto → prova Ocelot)
    ['rest', 'finger', 'other', 'x', 'up', 'x', 'tv'],               // 6 M não ganha (prova Ocelot → Luz)
    ['point_cam', 'rest', 'cam', 'other', 'up', 'flat', 'cuB'],      // 7 B a 51
    ['rest', 'finger', 'other', 'cam', 'normal', 'up', 'cuM'],       // 8 M lê o rótulo
    ['arms_up', 'rest', 'cam', 'other', 'up', 'flat', 'cuB'],        // 9 B roubou a cena
    ['rest', 'finger', 'other', 'cam', 'normal', 'x', 'wide'],       // 10 M ninguém quer ser o alvo
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'tv'],      // 11 B A/B
    ['rest', 'remote', 'other', 'cam', 'normal', 'up', 'cuM'],       // 12 M Comenta aí
  ],
  quadroDir: 'kit/v3/conde/',
  quadro: ['neutro', 'neutro', 'indignado', 'admirado', 'desconfiado', 'admirado', 'indignado', 'desconfiado',
           'indignado', 'neutro', 'neutro', 'neutro'],
  inserts: [],
  canais: [
    { de: 0, ch: 27, canal: 'LÊ A CARTA', img: 'cards/vingadora.png', cred: VIN, meter: M16, table: null },
    { de: 4, ch: 38, canal: 'LÊ A CARTA', img: 'cards/ocelot.png', cred: OCE, meter: M16, table: null },
    { de: 5, ch: 25, canal: 'LÊ A CARTA', img: 'cards/luz.png', cred: LUZ, meter: M16, table: null },
    { de: 9, ch: 51, canal: 'E VOCÊ?', img: 'cards/t_ab.png', cred: CRED_AB, meter: M16, table: null },
  ],
  tv: {
    channel: 'TV SAL', clock: '21:51',
    meter: M16, table: null,
    news: [
      'PLANTÃO: proposta política abala mesa de Commander',
      'Vingadora devolve dano e não aceita reclamação',
      'Gato 16/16 procura advogado',
      'Dano prevenido não rende vida, confirma o Oracle',
      'Ninguém se voluntaria para ser o alvo',
    ],
  },
};
