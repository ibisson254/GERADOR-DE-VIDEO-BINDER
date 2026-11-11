// Ep. 10 · "97 terrenos" (Padrão v3, molde "Impossível"). Sanar, Innovative First-Year + Treasure Hunt + Magmakin Artillerist.
// Kit v2 + ganchos v3 (kit/v3/patch_index_v3.py). Factos conferidos a 11/11/2026: episodios/ep10_97_terrenos/ficha.md.
// pose por fala: [Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano]
const CRED = (c, s, a, n, art) => `Na TV: ${c} (${s}, ${a}), nº ${n}. Arte: ${art}.<br>© Wizards of the Coast.`;
const SANAR = CRED('Sanar, Innovative First-Year', 'Lorwyn Eclipsed', 2026, 241, 'Steven Belledin');
const HUNT = CRED('Treasure Hunt', 'Commander 2018', 2018, 109, 'Daren Bader');
const ARTI = CRED('Magmakin Artillerist', 'Aetherdrift', 2025, 137, 'Madeline Boni');
const TERRA = { title: 'TERRENÔMETRO', value: '97%', fill: 0.97, calc: ['97 de 100 cartas', 'são terreno'],
                levels: [['SÓ TERRA', '#FF5A4E'], ['MUITA', '#F4B414'], ['NORMAL', '#6FB487']] };
const EP = {
  id: 'ep10_97_terrenos',
  bug: 'PLANTÃO DO IMPOSSÍVEL',
  poster: 'mago',          // Sanar é Goblin Sorcerer
  fx: { foco: true, tremor: true, poster: true, celular: false, scanner: false },
  loop: true,              // versão a publicar: fim corta seco para o início (sem fecho do scanner)
  card: { img: 'cards/sanar.png', cred: SANAR },
  pose: [
    ['point_cam', 'rest', 'cam', 'other', 'angry', 'flat', 'pilha'],   // 1 B Esse deck tem 97 terrenos. E ganha no turno cinco.
    ['rest', 'rest', 'other', 'cam', 'normal', 'flat', 'cuM'],         // 2 M E só três cartas de verdade.
    ['shrug', 'rest', 'other', 'other', 'up', 'flat', 'wide'],         // 3 B Mentira. Três cartas não ganham de ninguém.
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],          // 4 M 1/3 Sanar
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],          // 5 M 2/3 Treasure Hunt
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],       // 6 B Não sobrou nenhuma. Travou.
    ['point_tv', 'x', 'screen', 'x', 'up', 'x', 'tvtext2'],            // 7 M Lê a carta. Tudo o que revelou vai pra mão.
    ['rest', 'rest', 'other', 'cam', 'normal', 'flat', 'cuM'],         // 8 M Mais de oitenta terrenos... O resto, descarta. (pilha na mão)
    ['point_tv', 'x', 'screen', 'x', 'angry', 'x', 'tvtext'],          // 9 M 3/3 Magmakin Artillerist (contador de dano)
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],       // 10 B Isso devia ser banido! ...Mato a Sanar.
    ['rest', 'finger', 'other', 'cam', 'normal', 'up', 'wide'],        // 11 M Tarde demais. Mas uma carta para. Qual?  (pancada depois)
    ['shrug', 'rest', 'cam', 'other', 'up', 'flat', 'cuB'],            // 12 B ...Quantos terrenos?  (silêncio, corta para a fala 1)
  ],
  cams: { pilha: { s: 2.2, cx: 450, cy: 1040, tx: 540, ty: 1060 } },
  gancho: { html: '97 TERRENOS.<br><span style="color:#fff">GANHA NO TURNO 5.</span>', fala: 0 },
  pilha: { x: 445, y: 1132, lata: true, mao: 7 },
  marca: { fala: 10 },
  // Conde de Manaforte: uma expressão por fala; só muda no início de cada plano (ver patch_index_v3.py)
  quadroDir: 'kit/v3/conde/',
  quadro: ['neutro', 'neutro', 'desconfiado', 'indignado', 'indignado', 'indignado', 'admirado', 'admirado', 'admirado', 'indignado', 'neutro', 'neutro'],
  calendario: { loja: 'BAZAR DA VILA', frase: 'Armarinho · Presentes', rodape: 'Feliz 1993!', mes: 'AGOSTO', ano: '1993', dia: 5, semana: 'QUINTA-FEIRA' },
  // degraus: cada carta entra na TV com o contador no placar (1/3, 2/3, 3/3)
  canais: [
    { de: 0, img: 'cards/sanar.png', cred: SANAR, ch: 1,
      table: { label: ['CARTAS QUE NÃO', 'SÃO TERRENO'], value: '3', note: ['de 100 no deck', '(contando a Sanar)'] } },
    { de: 3, img: 'cards/sanar.png', cred: SANAR, ch: 1, osd: '1/3',
      table: { label: ['CARTA'], value: '1/3', note: ['Sanar'] },
      hl: { tvtext: { rects: [[0.345, 0.668, 0.500, 0.026], [0.070, 0.699, 0.785, 0.026], [0.070, 0.731, 0.110, 0.026]], zoom: 1.5 } } },
    { de: 4, img: 'cards/treasure_hunt.png', cred: HUNT, ch: 2, osd: '2/3',
      table: { label: ['CARTA'], value: '2/3', note: ['Treasure Hunt'] },
      hl: { tvtext:  { rects: [[0.070, 0.639, 0.800, 0.028], [0.070, 0.675, 0.800, 0.028], [0.070, 0.711, 0.100, 0.028]], zoom: 1.5 },
            tvtext2: { rects: [[0.195, 0.711, 0.700, 0.028], [0.070, 0.746, 0.420, 0.028]], zoom: 1.5 } } },
    { de: 8, img: 'cards/artillerist.png', cred: ARTI, ch: 3, osd: '3/3', subir: 2.6,
      meter: { title: 'DANO', value: '85', fill: 1, calc: ['em cada oponente', '(vida: 40)'],
               levels: [['LETAL', '#FF5A4E'], ['40', '#F4B414'], ['0', '#6FB487']] },
      table: { label: ['CARTA'], value: '3/3', note: ['Magmakin', 'Artillerist'] },
      hl: { tvtext: { rects: [[0.087, 0.641, 0.800, 0.028], [0.087, 0.676, 0.790, 0.028], [0.087, 0.716, 0.575, 0.028]], zoom: 1.5 } } },
  ],
  tv: {
    channel: 'TV SAL', clock: '21:41',
    meter: TERRA,
    table: { label: ['CARTAS QUE NÃO', 'SÃO TERRENO'], value: '3', note: ['de 100 no deck', '(contando a Sanar)'] },
    news: [
      'URGENTE: deck com 97 terrenos ganha no turno cinco e ninguém acredita',
      'EDHREC conta 739 decks de Sanar; a loja de sleeves agradece',
      'Jogador embaralha 97 terrenos e pede música para passar o tempo',
      'Treasure Hunt, comum de 2010, enfim acha o tesouro: um deck só de terreno',
      'Mão de 92 cartas: juiz pede uma mesa maior',
      'Limite de mão continua em sete; o Burn continua sem acreditar',
      'Plantão anterior: o ladrão que virou Papai Noel',
      'Próximo plantão: a carta que para tudo isso. Qual?',
    ],
  },
};
