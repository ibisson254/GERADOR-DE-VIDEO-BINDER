// MB-EP21 · O Capacete Que Nunca Para (27/11/2026). Helm of Obedience + Rest in Peace: o grimório inteiro de um oponente vai para o exílio.
// Inspirado no formato de um Reel enviado pelo fundador (combo de duas cartas explicado passo a passo); roteiro, cartas na tela e piadas próprios.
// Factos: Oracle e rulings no Scryfall (27/11/2026); combo no Commander Spellbook 3002-5065 (4.387 decks); Salt do Helm no EDHREC (0,60, 27/11/2026).
// Plano de prova (EP.prova) para as leituras do Mana; reação do Burn em grande plano; TV SAL abre e fecha.
// pose por fala: [Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano]
const CR = '© Wizards of the Coast. Conteúdo de fã não oficial.';
const HELM = 'Na tela: Helm of Obedience (Alliances, 1996), nº 121. Arte: Brian Snõddy.<br>' + CR;
const RIP = 'Na tela: Rest in Peace (The Big Score, 2024), nº 4. Arte: Grady Frederick.<br>' + CR;
const DUO = 'Na tela: Helm of Obedience (ALL 121, arte Brian Snõddy) e Rest in Peace (BIG 4, arte Grady Frederick).<br>' + CR;
const EP19 = 'Na tela: capa do MB-EP19 (BINDER) e Rest in Peace (BIG 4, arte Grady Frederick).<br>' + CR;
const MESA = 'Na tela: exemplo de mesa de 4. Helm of Obedience (ALL 121, arte Brian Snõddy).<br>' + CR;
// medidor: Salt Score do Helm no EDHREC ÷ 4 (putômetro, manaburn/PERFIL.md)
const PUT = { title: 'PUTÔMETRO', value: '15%', fill: 0.15, calc: ['Salt EDHREC 0,60', '÷ 4 = 0,15', 'Helm · 27/11'],
              levels: [['DE BOA', '#6FB487'], ['PUTO', '#F4B414'], ['BANE!', '#FF5A4E']] };
// linhas medidas no PNG do Scryfall (all/121, 745x1040; rip big/4, 744x1040), 27/11/2026
const HL_ATIVA = [[0.125, 0.627, 0.79, 0.034]];   // «X, {T}: Put the top card of target opponent's library…»
const HL_ATE = [[0.125, 0.661, 0.79, 0.083]];     // «Continue doing this until you have put X cards or a creature card into that graveyard»
const HL_RIP = [[0.08, 0.758, 0.84, 0.106]];      // «If a card or token would be put into a graveyard from anywhere, exile it instead.»
const TXT_H = [0.10, 0.60, 0.82, 0.27];
const TXT_R = [0.06, 0.66, 0.88, 0.24];
const EP = {
  id: 'ep21_capacete_obediencia',
  bug: 'TV SAL',
  poster: 'dragao',
  fx: { foco: true, tremor: true, poster: true, celular: true, scanner: false, tv_ligada: true },
  outro: { assinatura: 'Escaneie suas cartas e organize sua coleção.' },
  card: { img: 'cards/t00_capacete.png', cred: HELM },
  abertura: { img: 'cards/helm.png', ate: 0.36, hl: HL_ATIVA, selo: { txt: '1 MANA → TUDO', x: 0.62, y: 0.135, rot: -3, size: 36 } },
  legenda_paginas: 58,
  prova: { w: 620, top: 330, segs: [
    { fala: 1, de: 0, img: 'cards/helm.png', hl: HL_ATIVA, zoom: { de: 0.25, alvo: TXT_H, s: 1.6 }, faixa: 'PAGA X E VIRA' },
    { fala: 1, de: 0.5, img: 'cards/helm.png', hl: HL_ATE, zoom: { de: 0.0, alvo: TXT_H, s: 1.6 }, faixa: 'MÓI ATÉ X CARTAS CHEGAREM' },
    { fala: 3, de: 0, img: 'cards/helm.png', hl: HL_ATE, zoom: { de: 0.0, alvo: TXT_H, s: 1.6 }, faixa: 'PARA QUANDO A CARTA CHEGA' },
    { fala: 3, de: 0.5, img: 'cards/t02_oracle.png', tipo: 'tela' },
    { fala: 5, de: 0, img: 'cards/rip.png', hl: HL_RIP, zoom: { de: 0.35, alvo: TXT_R, s: 1.5 }, faixa: 'CEMITÉRIO → EXÍLIO' },
    { fala: 7, de: 0, img: 'cards/t08_ruling.png', tipo: 'tela' },
    { fala: 7, de: 0.5, img: 'cards/t08a.png', tipo: 'tela' },
    { fala: 7, de: 0.76, img: 'cards/t08b.png', tipo: 'tela' },
    { fala: 9, de: 0, img: 'cards/t10_regra.png', tipo: 'tela' },
    { fala: 11, de: 0, img: 'cards/t12_mesa.png', tipo: 'tela' },
    { fala: 11, de: 0.36, img: 'cards/t12_mesa_b.png', tipo: 'tela' },
    { fala: 11, de: 0.62, img: 'cards/t12_resp.png', tipo: 'tela' },
  ] },
  pose: [
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'tv'],      // 1 B gancho (abertura → TV)
    ['rest', 'finger', 'other', 'x', 'normal', 'x', 'tv'],           // 2 M o Helm (prova: Helm)
    ['shrug', 'rest', 'cam', 'other', 'up', 'flat', 'cuB'],          // 3 B X = 1, fraco (rosto)
    ['rest', 'finger', 'other', 'x', 'normal', 'x', 'tv'],           // 4 M Lê a carta (prova: Helm + Oracle)
    ['point_cam', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],   // 5 B moeu, caiu, gênio (rosto)
    ['rest', 'finger', 'other', 'x', 'up', 'x', 'tv'],               // 6 M Rest in Peace (prova)
    ['arms_up', 'rest', 'tv', 'other', 'up', 'flat', 'tv'],          // 7 B a mesma do robô?! (TV: EP19)
    ['rest', 'finger', 'other', 'x', 'up', 'x', 'tv'],               // 8 M ruling + grimório 60 → 0 (prova)
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],     // 9 B Ganhei! (rosto)
    ['rest', 'finger', 'other', 'x', 'normal', 'x', 'tv'],           // 10 M ainda não: 704.5b (prova)
    ['point_cam', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],   // 11 B mesa inteira (rosto)
    ['rest', 'finger', 'other', 'x', 'normal', 'x', 'tv'],           // 12 M um por vez + resposta (prova)
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'tv'],      // 13 B pergunta A/B (TV)
    ['rest', 'remote', 'other', 'cam', 'normal', 'up', 'cuM'],       // 14 M Comenta aí
  ],
  quadroDir: 'kit/v3/conde/',
  quadro: ['neutro', 'desconfiado', 'indignado', 'desconfiado', 'indignado', 'admirado', 'admirado', 'admirado',
           'indignado', 'desconfiado', 'indignado', 'desconfiado', 'neutro', 'neutro'],
  inserts: [],
  canais: [
    { de: 0, ch: 3, canal: 'O CAPACETE', img: 'cards/t00_capacete.png', cred: HELM, meter: null, table: null },
    { de: 1, ch: 6, canal: 'LÊ A CARTA', img: 'cards/helm.png', cred: HELM, meter: null, table: null },
    { de: 5, ch: 9, canal: 'LÊ A CARTA', img: 'cards/rip.png', cred: RIP, meter: null, table: null },
    { de: 6, ch: 19, canal: 'NO EP. 19', img: 'cards/t07_ep19.png', cred: EP19, meter: null, table: null },
    { de: 7, ch: 21, canal: 'RULING', img: 'cards/t08_ruling.png', meio: { at: 0.5, img: 'cards/t08b.png' }, cred: DUO, meter: null, table: null },
    { de: 9, ch: 27, canal: 'REGRA', img: 'cards/t10_regra.png', cred: CR, meter: null, table: null },
    { de: 11, ch: 40, canal: 'MESA DE 4', img: 'cards/t12_mesa.png', meio: { at: 0.5, img: 'cards/t12_mesa_b.png' }, cred: MESA, meter: null, table: null },
    { de: 12, ch: 45, canal: 'E VOCÊ?', img: 'cards/t13_ab.png', meio: { at: 0.5, img: 'cards/t13_ab_b.png' }, cred: HELM, meter: null, table: null },
  ],
  tv: {
    channel: 'TV SAL', clock: '06:21',
    meter: PUT, table: null,
    news: [
      'PLANTÃO: capacete de 1996 esvazia biblioteca sem pedir licença',
      'Cemitério fecha para obras; tudo segue direto para o exílio',
      'Bibliotecário em greve: «X igual a um não é desculpa»',
      'Grimório vazio garante: «ainda não perdi, só não compro»',
      'Rest in Peace troca de lado: de heroína a cúmplice',
      'Plantão anterior: robô de seis manas volta do cemitério',
    ],
  },
};
