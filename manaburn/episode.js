// Ep. 8 · Plantão do Banimento: The Tabernacle at Pendrell Vale (Legends, 1994)
// pose por fala: [Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano]
const EP = {
  card: { img: 'cards/main.png',
          cred: 'Na TV: The Tabernacle at Pendrell Vale (Legends, 1994), nº 307. Arte: Nicola Leonard.<br>© Wizards of the Coast.' },
  pose: [
    ['tvpoint','x','screen','x','angry','x','tv'],          // 1 B  gancho: abre com a carta grande
    ['rest','rest','other','cam','normal','flat','cuM'],      // 2 M  "Tabernacle de 1994."
    ['tvpoint','x','screen','x','angry','x','tvtext'],      // 3 B  destaque: não gera mana!
    ['rest','finger','other','other','up','flat','wide'],     // 4 M  "Cobra pedágio..."
    ['arms_up','rest','cam','other','angry','flat','wide'],   // 5 B  "E se o cara tiver dez fichas..."
    ['tvpoint','x','left','x','up','x','tvtext2'],          // 6 M  destaque: destruída
    ['shrug','rest','other','other','up','flat','cuB'],       // 7 B  "Isso não é terreno, é um bancário..."
    ['rest','finger','other','other','normal','up','wide'],   // 8 M  "Genocídio parcelado..."
    ['tvpoint','x','screen','x','normal','x','tv2'],        // 9 B  "Mas e as criaturas do dono..."
    ['rest','chip','other','other','normal','flat','push'],   // 10 M "Ele não usa criatura. Joga de controle."
    ['arms_up','chip','other','other','angry','flat','push'], // 11 B "Três mil e quinhentos dólares pra ninguém jogar?!"
    ['rest','rest','other','cam','normal','flat','cuM'],      // 12 M "Magic como ele deve ser."
    ['point_cam','rest','cam','other','angry','flat','cuB'],  // 13 B CTA
    ['rest','remote','other','cam','normal','up','cuM'],      // 14 M "Comenta aí." + TV desliga
  ],
  inserts: [],
  // destaques no texto impresso do Tabernacle Legends (fração da carta, medidos no PNG 745x1040)
  hl: {
    tvtext:  { rects: [[0.145, 0.642, 0.575, 0.036], [0.145, 0.675, 0.710, 0.036]], zoom: 1.5 }, // "All creatures in play require an upkeep cost of 1 extra mana"
    tvtext2: { rects: [[0.145, 0.738, 0.690, 0.036], [0.145, 0.770, 0.700, 0.036]], zoom: 1.5 }, // "that creature is immediately destroyed."
  },
  // o que passa na TV, atrás da carta: canal pirata "TV SAL" com plantão e saleirômetro (para quem pausar)
  tv: {
    channel: 'TV SAL', clock: '04:20',
    // putômetro: Salt Score do Tabernacle (2,68) na escala de votação do EDHREC (0 a 4) = 67%
    meter: { title: 'PUTÔMETRO', value: '67%', fill: 2.68 / 4, calc: ['2,68 de 4 no', 'Salt Score', 'EDHREC 2026'],
             levels: [['PUTO', '#FF5A4E'], ['BUFANDO', '#F4B414'], ['DE BOA', '#6FB487']] },
    // mesa de Commander: o pedágio de 1 mana por criatura
    table: { label: ['PEDÁGIO', 'POR TURNO'], value: '{1} MANA', note: ['por criatura', 'na mesa'] },
    news: [
      'URGENTE: jogador de fichas entra em recuperação judicial no turno 3',
      'The Tabernacle at Pendrell Vale: o terreno que não gera mana mas cobra condomínio',
      'Reserved List: carta de 1994 bate R$ 20.000 e jogadores choram em posição fetal',
      'Salt Score 2026 do EDHREC coloca Tabernacle no topo do sofrimento',
      'Stasis manda flores para o Tabernacle: amizade stax fortalecida',
      'Juiz confirma: se não pagar o pedágio, o bicho vai pro cemitério sim',
      'Jogador casual pergunta: por que alguém gastaria um carro nisso?',
      'Próximo plantão: Winter Orb e o fim das amizades de infância',
    ],
  },
};
