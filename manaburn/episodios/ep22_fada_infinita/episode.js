// MB-EP22 · A Fada Infinita (28/11/2026). Splinter Twin + Pestermite: fichas infinitas com ímpeto no turno 4, sem acelerar mana.
// Pedido do fundador (28/11/2026): «uma carta, um combo, um número no hook»; ideia sugerida com Kiki-Jiki + Pestermite, trocada pela
// Splinter Twin porque o Kiki custa 5 e só fecha no turno 4 com aceleração (ficha, «Pesquisa de pauta»).
// Factos: Oracle e rulings no Scryfall (28/11/2026); combo no Commander Spellbook 2905-4702 (1.277 listas); EDHREC (Salt da Twin 0,47);
// anúncio de banidas e restritas da Wizards de 16/12/2024 (Twin liberada no Modern, banida em 2016).
// pose por fala: [Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano]
const CR = '© Wizards of the Coast. Conteúdo de fã não oficial.';
const TWIN = 'Na tela: Splinter Twin (Modern Masters 2015), nº 129. Arte: Goran Josic.<br>' + CR;
const PEST = 'Na tela: Pestermite (Foundations Jumpstart, 2024), nº 343. Arte: Christopher Moeller.<br>' + CR;
const DUO = 'Na tela: Pestermite (J25 343, arte Christopher Moeller) e Splinter Twin (MM2 129, arte Goran Josic).<br>' + CR;
const MESA = 'Na tela: exemplo de mesa de 4. Pestermite (J25 343, arte Christopher Moeller).<br>' + CR;
const BAN = 'Na tela: anúncio de banidas e restritas da Wizards (16/12/2024). Splinter Twin (MM2 129, arte Goran Josic).<br>' + CR;
// medidor: Salt Score da Splinter Twin no EDHREC ÷ 4 (putômetro, manaburn/PERFIL.md)
const PUT = { title: 'PUTÔMETRO', value: '12%', fill: 0.12, calc: ['Salt EDHREC 0,47', '÷ 4 = 0,12', 'Twin · 28/11'],
              levels: [['DE BOA', '#6FB487'], ['PUTO', '#F4B414'], ['BANE!', '#FF5A4E']] };
// linhas medidas no PNG do Scryfall (twin mm2/129, 745x1040; pestermite j25/343, 744x1040), 28/11/2026
const HL_TWIN = [[0.08, 0.704, 0.84, 0.062]];     // «Enchanted creature has "{T}: Put a token that's a copy of this creature onto the»
const HL_HASTE = [[0.08, 0.768, 0.84, 0.03]];     // «battlefield. That token has haste. Exile it»
const HL_ETB = [[0.08, 0.752, 0.84, 0.07]];       // «When Pestermite enters, you may tap or untap target permanent.»
const HL_ALVO = [[0.08, 0.791, 0.84, 0.03]];      // «untap target permanent.»
const TXT_T = [0.06, 0.64, 0.88, 0.25];
const TXT_P = [0.06, 0.62, 0.88, 0.24];
const EP = {
  id: 'ep22_fada_infinita',
  bug: 'TV SAL',
  poster: 'dragao',
  fx: { foco: true, tremor: true, poster: true, celular: true, scanner: false, tv_ligada: true },
  outro: { assinatura: 'Escaneie suas cartas e organize sua coleção.' },
  card: { img: 'cards/t00_combo.png', cred: DUO },
  abertura: { img: 'cards/twin.png', ate: 0.6, hl: HL_TWIN, selo: { txt: '2 CARTAS · TURNO 4', x: 0.05, y: 0.118, rot: -4, size: 32 } },
  legenda_paginas: 58,
  prova: { w: 690, top: 300, segs: [  // v2: maior que o padrão (620) a pedido do fundador (28/11, hierarquia visual)
    { fala: 1, de: 0, img: 'cards/pestermite.png', hl: HL_ETB, zoom: { de: 0.3, alvo: TXT_P, s: 1.4 }, faixa: 'LAMPEJO · VIRA OU DESVIRA' },
    { fala: 3, de: 0, img: 'cards/pestermite.png', hl: HL_ALVO, zoom: { de: 0.0, alvo: TXT_P, s: 1.4 }, faixa: 'QUALQUER PERMANENTE' },
    { fala: 3, de: 0.45, img: 'cards/t04_turnos.png', tipo: 'tela' },
    { fala: 5, de: 0, img: 'cards/twin.png', hl: HL_HASTE, zoom: { de: 0.25, alvo: TXT_T, s: 1.4 }, faixa: 'A FICHA TEM ÍMPETO' },
    { fala: 5, de: 0.55, img: 'cards/t06_loop.png', tipo: 'tela' },
    { fala: 7, de: 0, img: 'cards/t08_ruling.png', tipo: 'tela' },
    { fala: 7, de: 0.55, img: 'cards/t08_conta.png', tipo: 'tela' },
    { fala: 9, de: 0, img: 'cards/t10_ban.png', tipo: 'tela' },
    { fala: 9, de: 0.6, img: 'cards/t10_quote.png', tipo: 'tela' },
    { fala: 11, de: 0, img: 'cards/t12_resp.png', tipo: 'tela' },
  ] },
  pose: [
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'tv'],      // 1 B gancho (abertura → TV)
    ['rest', 'finger', 'other', 'x', 'normal', 'x', 'tv'],           // 2 M a Pestermite (prova)
    ['shrug', 'rest', 'cam', 'other', 'up', 'flat', 'cuB'],          // 3 B uma manazinha (rosto)
    ['rest', 'finger', 'other', 'x', 'normal', 'x', 'tv'],           // 4 M Lê a carta + turnos (prova)
    ['point_cam', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],   // 5 B nasce enjoada (rosto)
    ['rest', 'finger', 'other', 'x', 'up', 'x', 'tv'],               // 6 M ímpeto + loop (prova)
    ['arms_up', 'rest', 'cam', 'other', 'up', 'flat', 'cuB'],        // 7 B fada ao quadrado (rosto)
    ['rest', 'finger', 'other', 'x', 'up', 'x', 'tv'],               // 8 M ruling + conta (prova)
    ['arms_up', 'rest', 'tv', 'other', 'angry', 'flat', 'tv'],       // 9 B banido! (TV: mesa 40 → 0)
    ['rest', 'finger', 'other', 'x', 'normal', 'x', 'tv'],           // 10 M já foi (prova: ban/unban)
    ['point_cam', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],   // 11 B ninguém para (rosto)
    ['rest', 'finger', 'other', 'x', 'normal', 'x', 'tv'],           // 12 M em resposta (prova)
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'tv'],      // 13 B pergunta A/B (TV)
    ['rest', 'remote', 'other', 'cam', 'normal', 'up', 'cuM'],       // 14 M Comenta aí
  ],
  quadroDir: 'kit/v3/conde/',
  quadro: ['neutro', 'desconfiado', 'indignado', 'desconfiado', 'indignado', 'admirado', 'indignado', 'admirado',
           'indignado', 'admirado', 'indignado', 'desconfiado', 'neutro', 'neutro'],
  inserts: [],
  canais: [
    { de: 0, ch: 2, canal: 'DUAS CARTAS', img: 'cards/t00_combo.png', cred: DUO, meter: null, table: null },
    { de: 1, ch: 3, canal: 'LÊ A CARTA', img: 'cards/pestermite.png', cred: PEST, meter: null, table: null },
    { de: 3, ch: 4, canal: 'TURNO 4', img: 'cards/t04_turnos.png', cred: DUO, meter: null, table: null },
    { de: 5, ch: 9, canal: 'LÊ A CARTA', img: 'cards/twin.png', cred: TWIN, meter: null, table: null },
    { de: 7, ch: 21, canal: 'RULING', img: 'cards/t08_ruling.png', meio: { at: 0.55, img: 'cards/t08_conta.png' }, cred: TWIN, meter: null, table: null },
    { de: 8, ch: 40, canal: 'MESA DE 4', img: 'cards/t09_mesa.png', meio: { at: 0.5, img: 'cards/t09_mesa_b.png' }, cred: MESA, meter: null, table: null },
    { de: 9, ch: 16, canal: 'MODERN', img: 'cards/t10_ban.png', cred: BAN, meter: null, table: null },
    { de: 11, ch: 27, canal: 'EM RESPOSTA', img: 'cards/t12_resp.png', cred: DUO, meter: null, table: null },
    { de: 12, ch: 45, canal: 'E VOCÊ?', img: 'cards/t13_ab.png', meio: { at: 0.5, img: 'cards/t13_ab_b.png' }, cred: DUO, meter: null, table: null },
  ],
  tv: {
    channel: 'TV SAL', clock: '20:16',
    meter: PUT, table: null,
    news: [
      'PLANTÃO: fada de três manas desvira a amiga e ninguém dorme',
      'Aura de 2010 volta ao Modern depois de oito anos de castigo',
      'Cartório informa: cópia não herda Aura nenhuma',
      'Etapa final promete exilar todas as fadas; mesa duvida que chegue lá',
      'Goblin de cinco manas diz que também fazia isso, mas no turno cinco',
      'Pilha lotada: «mata em resposta» vira hit da madrugada',
      'Plantão anterior: capacete de 1996 esvazia biblioteca',
    ],
  },
};
