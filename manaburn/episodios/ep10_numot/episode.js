// Ep. 10 · "O dragão flanelinha" (Numot, the Devastator · Commander 2011). Kit v2 + sala v3. Oracle conferido no Scryfall a 11/11/2026.
// pose por fala: [Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano]
const EP = {
  id: 'ep10_numot',
  poster: 'dragao',
  fx: { foco: true, tremor: true, poster: true, celular: true, scanner: false },
  outro: { assinatura: 'Escaneie suas cartas e organize seus decks.' },
  card: { img: 'cards/numot.png',
          cred: 'Na TV: Numot, the Devastator (Commander 2011), nº 215. Arte: Dan Dos Santos.<br>© Wizards of the Coast.' },
  pose: [
    ['point_tv', 'x', 'screen', 'x', 'angry', 'x', 'tv'],            // 1 B dragão que come terreno
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'tvtext2'],   // 2 M seis de mana, mais três pra destruir
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],       // 3 B flanelinha
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],          // 4 M Lê a carta
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'wide'],      // 5 B Wildfire (insert)
    ['rest', 'finger', 'other', 'cam', 'normal', 'up', 'cuM'],         // 6 M sacrifica, não destrói
    ['shrug', 'rest', 'other', 'other', 'up', 'flat', 'push'],         // 7 B morre junto?
    ['rest', 'rest', 'other', 'cam', 'normal', 'flat', 'cuM'],         // 8 M seis por seis
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'wide'],      // 9 B Augustin (insert)
    ['rest', 'chip', 'other', 'other', 'normal', 'flat', 'push'],      // 10 M um a mais / branca e azul um a menos
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'wide'],      // 11 B anão (insert)
    ['rest', 'rest', 'other', 'cam', 'normal', 'up', 'cuM'],           // 12 M só não básico
    ['point_cam', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],     // 13 B pergunta A/B
    ['rest', 'remote', 'other', 'cam', 'normal', 'up', 'cuM'],         // 14 M Comenta aí (TV desliga)
  ],
  inserts: [
    { file: 'cards/wildfire.png', line: 4, at: 0.30, until: 6,
      cred: 'Wildfire (Modern Masters 2015), nº 134. Arte: Rob Alexander.' },
    { file: 'cards/augustin.png', line: 8, at: 0.30, until: 10,
      cred: 'Grand Arbiter Augustin IV (Double Masters 2022), nº 221. Arte: Zoltan Boros & Gabor Szikszai.' },
    { file: 'cards/miner.png', line: 10, at: 0.30, until: 12,
      cred: 'Dwarven Miner (Mirage, 1996), nº 169. Arte: Jock.' },
  ],
  // destaques medidos no PNG 745x1040 (linhas de pixels escuros da caixa de texto), em frações da carta
  hl: {
    tvtext:  { rects: [[0.103, 0.756, 0.730, 0.032],     // "deals combat damage to a player,"
                       [0.103, 0.791, 0.796, 0.032],     // "you may pay {2}{R}. If you do, destroy"
                       [0.103, 0.827, 0.490, 0.032]],    // "up to two target lands."
               zoom: 1.5 },
    tvtext2: { rects: [[0.103, 0.791, 0.430, 0.032]],    // "you may pay {2}{R}."
               zoom: 1.5 },
  },
  tv: {
    channel: 'TV SAL', clock: '06:06',   // easter egg: 6/6, a resistência que o deixa sobreviver ao Wildfire
    // sem Salt Score do Numot no EDHREC (11/11/2026): o medidor mostra o dado do próprio Oracle
    meter: { title: 'DEMOLIÔMETRO', value: '2', fill: 1, calc: ['terrenos por ataque', 'texto Oracle (Scryfall)', '11/11/2026'],
             levels: [['DEVASTADOR', '#FF5A4E'], ['CHATO', '#F4B414'], ['DE BOA', '#6FB487']] },
    table: { label: ['JOGADORES', 'PUTOS'], value: '3 DE 4', note: ['o quarto é', 'o dono do dragão'] },
    news: [
      'URGENTE: dragão cobra três manas para demolir terreno alheio',
      'Juiz esclarece: Wildfire não destrói, cada jogador sacrifica quatro terrenos',
      'Dragão seis por seis sai ileso de incêndio que ele mesmo começou',
      'Augustin IV reajusta imposto: mágica de oponente custa um a mais',
      'Anão minerador poupa terreno básico; dual de grife pede proteção',
      'Numot completa 19 anos desde Planar Chaos e segue sem amigos na mesa',
      'Mesa de Commander adota Myr como moeda oficial depois do incêndio',
      'Plantão anterior: o ladrão que virou Papai Noel',
    ],
  },
};
