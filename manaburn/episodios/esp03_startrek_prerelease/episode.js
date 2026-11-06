// Especial pré-release · "BURN FOI ASSIMILADO!" (Magic: The Gathering | Star Trek, TRK, 2026)
// Kit v2 do repositório (manaburn/). Seis atos = seis canais da TV SAL (EP.canais, motor do zapping de 25/10).
// Textos Oracle e PNGs: API Scryfall (set:trk), 06/11/2026. Regras: notas de lançamento da Wizards (30/10/2026).
// Sem cuB nem push: o fundador proíbe zoom que corte a TV em qualquer plano (wide mostra a TV inteira; cuM não a mostra).
// pose por fala: [Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano]
const CR = '© Wizards of the Coast. Star Trek © CBS. Conteúdo de fã não oficial.';
const cred = (nome, n, artista) => `Na TV: ${nome} (Magic: The Gathering | Star Trek, 2026), nº ${n}. Arte: ${artista}.<br>${CR}`;
const EP = {
  id: 'esp03_startrek_prerelease',
  bug: 'ESPECIAL PRÉ-RELEASE STAR TREK',
  poster: 'artefato',   // Borg = criaturas artefato
  // fecho: bloco do scanner do kit desligado; o fecho oficial (comum/outro/outro_binder_916.mp4) entra por concat
  fx: { foco: true, tremor: true, poster: true, celular: true, scanner: false },
  outro: { assinatura: 'Escaneie suas cartas e organize seus decks.' },
  card: { img: 'cards/borgcube.png', cred: cred('Borg Cube', 227, 'Alexander Forssberg') },
  pose: [
    ['arms_up', 'x', 'screen', 'x', 'angry', 'x', 'tv'],            // 1 B Abri um Cubo Borg! Fui assimilado!
    ['rest', 'rest', 'other', 'cam', 'normal', 'flat', 'cuM'],        // 2 M Faltam as outras 39 cartas
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'wide'],     // 3 B Ele é o deck!
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],         // 4 M Lê a carta: doze marcadores
    ['point_tv', 'x', 'screen', 'x', 'up', 'x', 'tv2'],               // 5 B cinco cores! (canal 2: The Traveler)
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],         // 6 M Lê a carta: nome diferente
    ['arms_up', 'rest', 'cam', 'other', 'up', 'flat', 'wide'],        // 7 B Risa, Orion, Vulcan (insert Orion)
    ['rest', 'rest', 'other', 'cam', 'normal', 'flat', 'cuM'],        // 8 M entram virados
    ['shrug', 'rest', 'cam', 'other', 'angry', 'flat', 'wide'],       // 9 B Devagar?!
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],         // 10 M Locutus turno dois (canal 3, CH 47)
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'wide'],     // 11 B cobrar o aluguel (insert Vexing Drone)
    ['rest', 'finger', 'other', 'cam', 'normal', 'up', 'cuM'],        // 12 M a sua vida já encolheu
    ['point_tv', 'x', 'screen', 'x', 'up', 'x', 'tvtext2'],           // 13 B Voyager bota dois terrenos (canal 4)
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tvtext'],     // 14 M Station: até oito
    ['shrug', 'rest', 'other', 'other', 'up', 'flat', 'wide'],        // 15 B estacionando a nave?!
    ['rest', 'chip', 'other', 'cam', 'normal', 'flat', 'wide'],       // 16 M não bloqueia; não uma frota
    ['point_tv', 'x', 'screen', 'x', 'up', 'x', 'tv2'],               // 17 B Resistance Is Futile (canal 5)
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tvtext'],     // 18 M não artefato
    ['rest', 'x', 'screen', 'x', 'up', 'x', 'tv2'],                  // 19 B ... e os Borg são...
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext2'],        // 20 M Artefato. Traz Borg de volta
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'wide'],     // 21 B Isso devia ser banido!
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tvtext'],     // 22 M destrói um artefato (canal 6)
    ['point_tv', 'rest', 'tv', 'other', 'up', 'flat', 'wide'],        // 23 B Veredito, Spock!
    ['rest', 'chip', 'other', 'cam', 'normal', 'flat', 'cuM'],        // 24 M três apostas
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'wide'],     // 25 B Cubo, cinco cores e três naves
    ['rest', 'rest', 'other', 'cam', 'normal', 'up', 'cuM'],          // 26 M mudança interplanetária
    ['point_cam', 'rest', 'cam', 'other', 'angry', 'flat', 'wide'],   // 27 B A, Borg. B, cinco cores
    ['rest', 'remote', 'other', 'cam', 'normal', 'up', 'cuM'],        // 28 M Comenta aí (TV desliga)
  ],
  inserts: [
    { file: 'cards/orion.png', line: 6, at: 0.35, until: 7,
      cred: 'Orion (Magic: The Gathering | Star Trek, 2026), nº 288. Arte: Simon Dominic.' },
    { file: 'cards/vexing.png', line: 10, at: 0.30, until: 11,
      cred: 'Vexing Drone (Magic: The Gathering | Star Trek, 2026), nº 45. Arte: Kristina WermoongRey.' },
  ],
  // destaques medidos no PNG 744x1040 (linhas de pixels escuros da caixa de texto), em frações da carta
  canais: [
    { de: 0, ch: 1, canal: 'ASSIMILAÇÃO', img: 'cards/borgcube.png', cred: cred('Borg Cube', 227, 'Alexander Forssberg'),
      hl: { tvtext: { rects: [[0.105, 0.864, 0.645, 0.027]], zoom: 1.5 } },          // "12+ Artifact creatures you control have flying."
      meter: { title: 'MARCADORES P/ VOAR', value: '12', fill: 1, calc: ['Station 12+', 'Oracle · Scryfall', '06/11/2026'],
               levels: [['VOANDO', '#FF5A4E'], ['QUASE', '#F4B414'], ['NO CHÃO', '#6FB487']] },
      table: { label: ['CARTAS QUE', 'FALTAM NO DECK'], value: '39', note: ['sealed:', 'deck de 40'] } },
    { de: 4, ch: 2, canal: 'NOVOS MUNDOS', img: 'cards/traveler.png', cred: cred('The Traveler', 254, 'Ioannis Fiore'),
      hl: { tvtext: { rects: [[0.090, 0.690, 0.767, 0.027], [0.089, 0.721, 0.769, 0.021], [0.089, 0.751, 0.333, 0.021]], zoom: 1.5 } },
      meter: { title: 'NOMES DIFERENTES', value: '4', fill: 0.5, calc: ['Floresta + Ilha', '+ Earth + Orion', '= poder 4'],
               levels: [['GIGANTE', '#FF5A4E'], ['MÉDIO', '#F4B414'], ['NANICO', '#6FB487']] },
      table: { label: ['PLANETAS', 'ENTRAM VIRADOS'], value: '10/10', note: ['Oracle', 'Scryfall'] } },
    { de: 9, ch: 47, canal: 'OS BORG', img: 'cards/locutus.png', cred: cred('Locutus, the One Who Speaks', 245, 'Ariel Orea'),
      hl: { tvtext: { rects: [[0.087, 0.634, 0.712, 0.032], [0.091, 0.671, 0.138, 0.022]], zoom: 1.5 } },   // "Artifact creatures you control get / +1/+1."
      meter: { title: 'BÔNUS BORG', value: '+1/+1', fill: 0.7, calc: ['cada criatura', 'artefato', 'Oracle · Scryfall'],
               levels: [['PRESSÃO', '#FF5A4E'], ['CHATO', '#F4B414'], ['TRANQUILO', '#6FB487']] },
      table: { label: ['CUSTO DO', 'LOCUTUS'], value: '2', note: ['branco + preto', 'turno 2'] } },
    { de: 12, ch: 4, canal: 'AS NAVES', img: 'cards/voyager.png', cred: cred('U.S.S. Voyager, Lone Wanderer', 222, 'Hector Ortiz'),
      hl: { tvtext2: { rects: [[0.087, 0.641, 0.757, 0.022], [0.089, 0.665, 0.769, 0.018], [0.090, 0.690, 0.767, 0.022]], zoom: 1.5 },  // entra: dois terrenos
            tvtext:  { rects: [[0.090, 0.751, 0.766, 0.022], [0.089, 0.776, 0.755, 0.022], [0.089, 0.801, 0.696, 0.022]], zoom: 1.5 } },// Station
      meter: { title: 'MARCADORES', value: '8', fill: 1, calc: ['p/ virar criatura', 'Station 8+', 'Oracle · Scryfall'],
               levels: [['VOANDO', '#FF5A4E'], ['QUASE', '#F4B414'], ['GARAGEM', '#6FB487']] },
      table: { label: ['TRIPULANTE', 'QUE ESTACIONA'], value: 'VIRADO', note: ['não bloqueia', 'até desvirar'] } },
    { de: 16, ch: 5, canal: 'O DILEMA', img: 'cards/resistance.png', cred: cred('Resistance Is Futile', 125, 'Matt Stewart'),
      hl: { tvtext:  { rects: [[0.090, 0.723, 0.767, 0.032]], zoom: 1.5 },                                   // "Destroy target nonartifact creature."
            tvtext2: { rects: [[0.090, 0.763, 0.767, 0.025], [0.121, 0.799, 0.737, 0.025], [0.121, 0.832, 0.615, 0.025]], zoom: 1.5 } },
      meter: { title: 'BORG DESTRUÍDOS', value: '0%', fill: 0, calc: ['todo Borg do set', 'é artefato', 'Oracle · Scryfall'],
               levels: [['TODOS', '#FF5A4E'], ['ALGUNS', '#F4B414'], ['NENHUM', '#6FB487']] },
      table: { label: ['ESCOLHER', '= DILEMA'], value: '2', note: ['modos', 'notas oficiais'] } },
    { de: 21, ch: 6, canal: 'O VEREDITO', img: 'cards/perils.png', cred: cred('Perils of the Past', 161, 'Zoltan Boros'),
      hl: { tvtext: { rects: [[0.090, 0.752, 0.766, 0.032], [0.124, 0.792, 0.161, 0.020]], zoom: 1.5 } },     // "Destroy the Relic — Destroy target / artifact."
      meter: { title: 'REMOÇÕES NO DECK', value: '5+', fill: 0.8, calc: ['mínimo sugerido', 'guia de pré-release', 'Wizards'],
               levels: [['SOBRA', '#FF5A4E'], ['OK', '#F4B414'], ['FALTA', '#6FB487']] },
      table: { label: ['APOSTAS', 'DO MANA'], value: '3', note: ['evidência e risco', 'no comentário'] } },
  ],
  tv: {
    channel: 'TV SAL', clock: '06:11',
    meter: { title: 'MARCADORES P/ VOAR', value: '12', fill: 1, calc: ['Station 12+', 'Oracle · Scryfall', '06/11/2026'],
             levels: [['VOANDO', '#FF5A4E'], ['QUASE', '#F4B414'], ['NO CHÃO', '#6FB487']] },
    table: null,
    news: [
      'URGENTE: pré-release de Star Trek começa hoje e vai até 12/11',
      'Kit de pré-release: 6 boosters e 1 promo foil rara ou mítica',
      'Dois "New Planet" contam como um nome só. Até o universo repete nome',
      'Star Trek chega ao Arena dia 10/11 e às lojas dia 13',
      'Manobrista de nave é a profissão do ano no Limited',
      'Borg prometem assimilar a mesa; a mesa pede mais dois turnos',
      'Plantão anterior em Star Trek: o Q bagunçou o deck de todo mundo',
      'Próximo plantão: o que o pré-release mostrou de verdade',
    ],
  },
};
