// Ep. 2 · Plantão do Banimento: Stasis (Salt Score 2026 do EDHREC)
// pose por fala: [Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano]
const EP = {
  card: { img: 'cards/main.png',
          cred: 'Na TV: Stasis (Limited Edition Alpha, 1993). Arte: Fay Jones.<br>© Wizards of the Coast.' },
  pose: [
    ['tvpoint','x','screen','x','angry','x','tv'],          // 1 B  gancho: abre com a carta grande
    ['rest','rest','other','cam','normal','flat','cuM'],      // 2 M  "Carta de 1993."
    ['tvpoint','x','screen','x','angry','x','tvtext'],      // 3 B  destaque: ninguém desvira
    ['rest','finger','other','other','up','flat','wide'],     // 4 M  "Greve geral na mesa."
    ['arms_up','rest','cam','other','angry','flat','wide'],   // 5 B  "Inclusive pra quem jogou!"
    ['tvpoint','x','left','x','up','x','tvtext2'],          // 6 M  destaque: paga uma azul
    ['shrug','rest','other','other','up','flat','cuB'],       // 7 B  "Sem desvirar? Com que mana?"
    ['rest','finger','other','other','normal','up','wide'],   // 8 M  "Baixa uma Ilha nova..."
    ['tvpoint','x','screen','x','normal','x','tv2'],        // 9 B  "...aluguel da cela com Ilha."
    ['rest','chip','other','other','normal','flat','push'],   // 10 M "E quando cansar, é só não pagar."
    ['arms_up','chip','other','other','angry','flat','push'], // 11 B "Então ele decide quando a greve acaba?!"
    ['rest','rest','other','cam','normal','flat','cuM'],      // 12 M "Greve com patrão."
    ['point_cam','rest','cam','other','angry','flat','cuB'],  // 13 B CTA
    ['rest','remote','other','cam','normal','up','cuM'],      // 14 M "Comenta aí." + TV desliga
  ],
  // carta citada: uma Ilha quando o Mana fala dela (só aparece se o PNG existir)
  inserts: [ { file: 'cards/island.png', line: 7, at: 0.12, until: 9, cred: '' } ],
  // destaques no texto impresso da Stasis Alpha (fração da carta, medidos no PNG 745x1040)
  hl: {
    tvtext:  { rects: [[0.250, 0.616, 0.527, 0.049], [0.215, 0.669, 0.464, 0.050]], zoom: 1.5 }, // "Players do not get an untap phase."
    tvtext2: { rects: [[0.698, 0.669, 0.118, 0.050], [0.235, 0.721, 0.571, 0.097]], zoom: 1.5 }, // "Pay {U} during upkeep or Stasis is destroyed."
  },
  // o que passa na TV, atrás da carta: canal pirata "TV SAL" com plantão e saleirômetro (para quem pausar)
  tv: {
    channel: 'TV SAL', clock: '03:47',
    // putômetro: Salt Score da Stasis (3,05) na escala de votação do EDHREC (0 a 4) = 76%
    meter: { title: 'PUTÔMETRO', value: '76%', fill: 3.05 / 4, calc: ['3,05 de 4 no', 'Salt Score', 'EDHREC 2026'],
             levels: [['PUTO', '#FF5A4E'], ['BUFANDO', '#F4B414'], ['DE BOA', '#6FB487']] },
    // mesa de Commander com 4 jogadores: a Stasis trava todo mundo, inclusive quem jogou
    table: { label: ['JOGADORES', 'PUTOS'], value: '4 DE 4', note: ['inclusive', 'quem jogou'] },
    news: [
      'URGENTE: mesa de Commander está há 40 minutos sem desvirar',
      'Jogador garante que o deck é casual e baixa Stasis no turno 2',
      'Previsão do tempo: chuva de sal no EDHREC',
      'Ilha nova: a única que entra desvirada',
      'Armageddon sobe do 7º para o 2º e comemora',
      "Sensei's Top segue de luto depois do Q",
      'Próximo plantão: o pedágio do Tabernacle',
      'Juiz pede calma: lê a carta',
    ],
  },
};
