// MB-EP19 · O Robô Que Não Morre (26/11/2026). Mikaeus, the Unhallowed + Triskelion («Mike e Trike»): dano infinito com undying.
// Factos: Oracle e rulings no Scryfall (26/11/2026); combo no Commander Spellbook / EDHREC (628-1495). Sem Salt verificado nesta sessão: o medidor da TV mostra o bracket mínimo do combo (EDHREC, 26/11/2026), não o putômetro.
// Plano de prova (EP.prova) para as leituras do Mana; reação do Burn em grande plano; TV SAL abre e fecha.
// pose por fala: [Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano]
const CR = '© Wizards of the Coast. Conteúdo de fã não oficial.';
const TRI = 'Na tela: Triskelion (March of the Machine Commander, 2023), nº 387. Arte: Christopher Moeller.<br>' + CR;
const MIK = 'Na tela: Mikaeus, the Unhallowed (Commander Masters, 2023), nº 173. Arte: Chris Rahn.<br>' + CR;
const LOOP = 'Na tela: Triskelion (MOC 387, arte Christopher Moeller) e Mikaeus, the Unhallowed (CMM 173, arte Chris Rahn).<br>' + CR;
const VID = 'Na tela: exemplo de mesa de 4 a 40 de vida. Triskelion (MOC 387, arte Christopher Moeller).<br>' + CR;
const RIP = 'Na tela: Rest in Peace (The Big Score, 2024), nº 4. Arte: Grady Frederick.<br>' + CR;
// linhas medidas nos PNG do Scryfall (744x1040), 26/11/2026
const BRK = { title: 'BRACKET', value: '3+', fill: 0.6, calc: ['combo de 2 cartas', 'fora do 1 e do 2', 'EDHREC · 26/11'],
              levels: [['CASUAL', '#6FB487'], ['UPGRADED', '#F4B414'], ['cEDH', '#FF5A4E']] };
const HL_UNDY = [[0.07, 0.748, 0.85, 0.062]];          // «Other non-Human creatures… +1/+1 and have undying»
const HL_SEM = [[0.07, 0.806, 0.85, 0.032]];           // «…dies, if it had no +1/+1 counters on it»
const HL_ENTRA = [[0.07, 0.659, 0.86, 0.058]];         // «enters the battlefield with three +1/+1 counters»
const HL_REMOVE = [[0.07, 0.735, 0.86, 0.058]];        // «Remove a +1/+1 counter…: 1 damage to any target»
const HL_SEIS = [[0.83, 0.040, 0.08, 0.058], [0.80, 0.885, 0.13, 0.06]];  // custo {6} e 1/1
const TXT = [0.06, 0.60, 0.88, 0.28];
const EP = {
  id: 'ep19_robo_imortal',
  bug: 'TV SAL',
  poster: 'dragao',
  fx: { foco: true, tremor: true, poster: true, celular: true, scanner: false, tv_ligada: true },
  outro: { assinatura: 'Escaneie suas cartas e organize sua coleção.' },
  card: { img: 'cards/t00_robo.png', cred: TRI },
  abertura: { img: 'cards/triskelion.png', ate: 0.42, hl: HL_REMOVE, selo: { txt: '2 TIROS → ∞', x: 0.07, y: 0.11, rot: -6, size: 54 } },
  legenda_paginas: 58,
  prova: { w: 620, top: 330, segs: [
    { fala: 1, de: 0, img: 'cards/mikaeus.png', hl: HL_UNDY, zoom: { de: 0.4, alvo: TXT, s: 1.6 }, faixa: 'NÃO HUMANAS GANHAM UNDYING' },
    { fala: 3, de: 0, img: 'cards/mikaeus.png', hl: HL_SEM, zoom: { de: 0.35, alvo: TXT, s: 1.6 }, faixa: 'SÓ VOLTA SEM MARCADOR +1/+1' },
    { fala: 5, de: 0, img: 'cards/t05_ruling.png', tipo: 'tela' },
    { fala: 6, de: 0, img: 'cards/triskelion.png', hl: HL_SEIS, faixa: '6 MANAS · 1/1' },
    { fala: 7, de: 0, img: 'cards/triskelion.png', hl: HL_ENTRA, zoom: { de: 0.0, alvo: TXT, s: 1.6 }, faixa: 'ENTRA COM 3 MARCADORES' },
    { fala: 7, de: 0.5, img: 'cards/triskelion.png', hl: HL_REMOVE, zoom: { de: 0.0, alvo: TXT, s: 1.6 }, faixa: 'TIRA 1 = 1 DE DANO' },
    { fala: 9, de: 0, img: 'cards/t09c.png', tipo: 'tela' },
    { fala: 9, de: 0.6, img: 'cards/t09a.png', tipo: 'tela' },
    { fala: 11, de: 0, img: 'cards/t10_vida_b.png', tipo: 'tela' },
    { fala: 11, de: 0.42, img: 'cards/t11_rip.png', tipo: 'tela' },
  ] },
  pose: [
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'tv'],      // 1 B gancho (abertura → TV)
    ['rest', 'finger', 'other', 'x', 'normal', 'x', 'tv'],           // 2 M Mike e Trike (prova: Mikaeus)
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],     // 3 B undying volta sempre (rosto)
    ['rest', 'finger', 'other', 'x', 'normal', 'x', 'tv'],           // 4 M Lê a carta: sem marcador (prova)
    ['shrug', 'rest', 'cam', 'other', 'up', 'flat', 'cuB'],          // 5 B Mikaeus dá +1/+1 (rosto)
    ['rest', 'finger', 'other', 'x', 'up', 'x', 'tv'],               // 6 M ruling (prova: painel)
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'tv'],      // 7 B seis manas num 1/1 (prova: Triskelion)
    ['rest', 'finger', 'other', 'x', 'normal', 'x', 'tv'],           // 8 M três marcadores (prova: Triskelion)
    ['point_cam', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],   // 9 B não morreu, gênio (rosto)
    ['rest', 'finger', 'other', 'x', 'up', 'x', 'tv'],               // 10 M o loop (prova: painéis)
    ['arms_up', 'rest', 'tv', 'other', 'angry', 'flat', 'tv'],       // 11 B dois na mesa (TV: vida 40 → 0)
    ['rest', 'finger', 'other', 'x', 'normal', 'x', 'tv'],           // 12 M Rest in Peace (prova: painel)
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'tv'],      // 13 B pergunta A/B (TV)
    ['rest', 'remote', 'other', 'cam', 'normal', 'up', 'cuM'],       // 14 M Comenta aí
  ],
  quadroDir: 'kit/v3/conde/',
  quadro: ['neutro', 'desconfiado', 'indignado', 'desconfiado', 'indignado', 'admirado', 'desconfiado', 'admirado',
           'indignado', 'admirado', 'indignado', 'desconfiado', 'neutro', 'neutro'],
  inserts: [],
  canais: [
    { de: 0, ch: 3, canal: 'O ROBÔ', img: 'cards/t00_robo.png', cred: TRI, meter: null, table: null },
    { de: 1, ch: 6, canal: 'LÊ A CARTA', img: 'cards/mikaeus.png', cred: MIK, meter: null, table: null },
    { de: 5, ch: 12, canal: 'RULING', img: 'cards/t05_ruling.png', cred: MIK, meter: null, table: null },
    { de: 6, ch: 13, canal: 'LÊ A CARTA', img: 'cards/triskelion.png', cred: TRI, meter: null, table: null },
    { de: 9, ch: 21, canal: 'O LOOP', img: 'cards/t09a.png', cred: LOOP, meter: null, table: null },
    { de: 10, ch: 40, canal: 'MESA DE 4', img: 'cards/t10_vida.png', meio: { at: 0.5, img: 'cards/t10_vida_b.png' }, cred: VID, meter: null, table: null },
    { de: 11, ch: 41, canal: 'CEMITÉRIO FECHADO', img: 'cards/t11_rip.png', cred: RIP, meter: null, table: null },
    { de: 12, ch: 45, canal: 'E VOCÊ?', img: 'cards/t12_ab.png', meio: { at: 0.5, img: 'cards/t12_ab_b.png' }, cred: LOOP, meter: null, table: null },
  ],
  tv: {
    channel: 'TV SAL', clock: '06:03',
    meter: BRK, table: null,
    news: [
      'PLANTÃO: robô de seis manas marca consulta no cemitério',
      'Zumbi clérigo distribui segunda chance para não humanos',
      'Marcador +1/+1 e bônus +1/+1 brigam por herança',
      'Cemitério reclama de excesso de visitas do mesmo robô',
      'Exílio fecha a porta: «aqui não volta ninguém»',
      'Humanos fora da festa do Mikaeus, de novo',
      'Plantão anterior: lagarto de duas manas cria infinito',
    ],
  },
};
