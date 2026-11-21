// MB-EP16 · O comandante que dá carta e bate no sorteio · Alexander, Ship's Fool: cada jogador revela o topo e compra;
// o maior custo revelado vira dano num oponente aleatório; a carta revelada é a comprada (a mesa vê) e, com Rule of Law, só uma mágica por turno.
// Factos: Oracle e ruling oficial (07/10/2026) no Scryfall; Rule of Law e Thousand-Year Elixir em listas de Alexander no EDHREC (21/11/2026).
// Ficha: episodios/ep16_alexander/ficha.md. Kit v2 + sala v3 + quadro do Conde + abertura de carta (padrões de 21/11/2026).
// pose por fala: [Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano]
const CR = '© Wizards of the Coast. Conteúdo de fã não oficial.';
const ALX = "Na TV: Alexander, Ship's Fool (Star Trek Commander, 2026), nº 81. Arte: Javier Charro.<br>" + CR;
const RUL = "Na TV: ruling oficial do Alexander, Ship's Fool (Wizards, 07/10/2026, via Scryfall).<br>" + CR;
const ROL = 'Na TV: Rule of Law (Core Set 2020), nº 35. Arte: Scott M. Fischer. Em listas de Alexander no EDHREC (21/11/2026).<br>' + CR;
const ELX = 'Na TV: Thousand-Year Elixir (Commander 2021), nº 271. Arte: Richard Sardinha. Exemplo de efeito de desvirar.<br>' + CR;
const M4 = { title: 'COMPRAM', value: '4', fill: 0.8, calc: ['mesa de 4', '1 por jogador', 'Oracle TRC 81'],
             levels: [['TODOS', '#6FB487'], ['4', '#F4B414'], ['1 APANHA', '#FF5A4E']] };
const STP = 'Swords to Plowshares (Star Trek Commander, 2026, nº 429, arte Pablo Mendoza). Exemplo.';
// linhas de texto medidas nos PNG trc/81, m20/35 e c21/271 (744x1040), 21/11/2026
const HL_REVEAL = [[0.080, 0.676, 0.720, 0.036], [0.080, 0.711, 0.640, 0.036]];
const HL_DANO = [[0.080, 0.744, 0.800, 0.036], [0.080, 0.777, 0.810, 0.036], [0.080, 0.810, 0.730, 0.036]];
const HL_ROL = [[0.080, 0.665, 0.830, 0.040], [0.080, 0.705, 0.360, 0.040]];
const HL_ELX = [[0.080, 0.746, 0.540, 0.040]];
const EP = {
  id: 'ep16_alexander',
  bug: 'TV SAL',
  poster: 'dragao',
  fx: { foco: true, tremor: true, poster: true, celular: true, scanner: false, tv_ligada: true },
  outro: { assinatura: 'Escaneie suas cartas e organize sua coleção.' },
  card: { img: 'cards/s01_quatro.png', cred: ALX },
  // abertura de carta: Alexander inteiro no quadro 0, a linha «revela e compra» destacada e o selo do gancho;
  // sai para a TV quando o Burn acaba de dizer «QUATRO» (52 % da fala 1)
  abertura: { img: 'cards/alexander.png', ate: 0.52, hl: HL_REVEAL, selo: { txt: '4 COMPRAM', x: 0.07, y: 0.12, rot: -6, size: 58 } },
  pose: [
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'tv'],      // 1 B dá carta pra quatro; um apanha
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],        // 2 M Lê a carta: revela e compra
    ['arms_up', 'rest', 'cam', 'other', 'up', 'flat', 'cuB'],        // 3 B instituição de caridade (insert)
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tvtext'],    // 4 M maior custo = dano, aleatório
    ['shrug', 'rest', 'cam', 'other', 'up', 'flat', 'cuB'],          // 5 B posso nem apanhar (insert: 2 em 3)
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],        // 6 M ruling: revelada = comprada
    ['point_cam', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],   // 7 B comprei uma remoção (insert)
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tv'],            // 8 M todo mundo sabe
    ['point_cam', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],   // 9 B jogo agora (insert)
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tvtext'],    // 10 M Rule of Law
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],     // 11 B UMA?! (insert, tremor)
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],        // 12 M habilidade não é mágica; desvirar
    ['point_cam', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],   // 13 B ameaça com brinde + A/B (insert)
    ['rest', 'remote', 'other', 'cam', 'normal', 'up', 'cuM'],       // 14 M Comenta aí (TV desliga)
  ],
  quadroDir: 'kit/v3/conde/',
  quadro: ['neutro', 'neutro', 'indignado', 'desconfiado', 'desconfiado', 'admirado', 'indignado', 'admirado',
           'indignado', 'admirado', 'indignado', 'admirado', 'neutro', 'neutro'],
  inserts: [
    { file: 'cards/i03_caridade.png', line: 2, at: 0.05, until: 3, cred: "Cada jogador compra uma carta. Alexander, Ship's Fool (TRC 81)." },
    { file: 'cards/i05_sorteio.png', line: 4, at: 0.05, until: 5, cred: 'Exemplo de mesa de 4: o dano cai num dos 3 oponentes, ao acaso.' },
    { file: 'cards/i05_sorteio_b.png', line: 4, at: 0.55, until: 5, cred: 'Exemplo de mesa de 4: o dano cai num dos 3 oponentes, ao acaso.' },
    { file: 'cards/i07_swords.png', line: 6, at: 0.05, until: 7, cred: STP },
    { file: 'cards/i09_agora.png', line: 8, at: 0.05, until: 9, cred: STP },
    { file: 'cards/i11_uma.png', line: 10, at: 0.05, until: 11, cred: 'Com Rule of Law: uma mágica por turno, por jogador. Rule of Law (M20 35).' },
    { file: 'cards/s13_ab.png', line: 12, at: 0.05, until: 13, cred: "Alexander, Ship's Fool (TRC 81, arte Javier Charro)." },
  ],
  canais: [
    { de: 0, ch: 4, canal: 'TODO MUNDO COMPRA', img: 'cards/s01_quatro.png', meio: { at: 0.6, img: 'cards/s01_quatro_b.png' }, cred: ALX, meter: null, table: null },
    { de: 1, ch: 6, canal: 'LÊ A CARTA', img: 'cards/alexander.png', meio: { at: 0.55, img: 'cards/c02_compra.png' }, cred: ALX,
      hl: { tvtext: { rects: HL_REVEAL, zoom: 1.5 } }, meter: null, table: null },
    { de: 3, ch: 9, canal: 'LÊ A CARTA', img: 'cards/alexander.png', meio: { at: 0.5, img: 'cards/c04_dano.png' }, cred: ALX,
      hl: { tvtext: { rects: HL_DANO, zoom: 1.5 } }, meter: null, table: null },
    { de: 5, ch: 15, canal: 'LÊ A RULING', img: 'cards/s06_ruling.png', meio: { at: 0.55, img: 'cards/s06_ruling_b.png' }, cred: RUL,
      hl: { tvtext: { rects: [[0.083, 0.515, 0.834, 0.063], [0.083, 0.590, 0.834, 0.063]], zoom: 1.5 } }, meter: null, table: null },
    { de: 7, ch: 20, canal: 'MÃO ABERTA', img: 'cards/s08_mesa.png', cred: 'Na TV: exemplo de mesa de 4. ' + STP + '<br>' + CR, meter: null, table: null },
    { de: 9, ch: 25, canal: 'LÊ A CARTA', img: 'cards/rule_of_law.png', meio: { at: 0.55, img: 'cards/c10_uma.png' }, cred: ROL,
      hl: { tvtext: { rects: HL_ROL, zoom: 1.5 } }, meter: null, table: null },
    { de: 11, ch: 30, canal: 'NÃO É MÁGICA', img: 'cards/elixir.png', meio: { at: 0.5, img: 'cards/c12_denovo.png' }, cred: ELX,
      hl: { tvtext: { rects: HL_ELX, zoom: 1.5 } }, meter: null,
      table: { label: ['MÁGICAS', 'POR TURNO'], value: '1', note: ['por jogador'] } },
  ],
  tv: {
    channel: 'TV SAL', clock: '20:44',   // easter egg: mesa de 4, 4 compram
    meter: M4, table: null,
    news: [
      'PLANTÃO: klingon distribui cartas e a mesa desconfia',
      'Sorteio de dano: mesa pede auditoria independente',
      'Remoção revelada vira assunto do bairro inteiro',
      'Rule of Law: fila única para conjurar, uma por pessoa',
      'Habilidade ativada jura que não é mágica',
      'Plantão anterior: gato ganha com 40 de vida',
    ],
  },
};
