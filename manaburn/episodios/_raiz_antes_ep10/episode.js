// Ep. 9 · Plantão do Banimento: "O ladrão que virou Papai Noel" (Dack Fayden, Helping Hand · Reality Fracture Commander, 2026)
// Kit v2 (projeto claude.ai Binder Marketing, claude/gerador-manaburn/). Dados conferidos a 29/10/2026.
// pose por fala: [Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano]
const EP = {
  id: 'ep9_dack',
  poster: 'mago',      // Dack é Human Advisor: o pôster mais próximo de criatura humana no kit
  // fecho: o bloco do scanner do kit fica desligado; o fecho oficial (scanner real + logo) entra depois, por concat.
  // Assim o vídeo não repete a logo: TV desliga → ponto verde → fecho do scanner.
  fx: { foco: true, tremor: true, poster: true, celular: true, scanner: false },
  outro: { assinatura: 'Escaneie suas cartas e organize seus decks.' },
  card: { img: 'cards/main.png',
          cred: 'Na TV: Dack Fayden, Helping Hand (Reality Fracture Commander, 2026), nº 4. Arte: Josiah “Jo” Cameron.<br>© Wizards of the Coast.' },
  pose: [
    ['point_tv', 'x', 'screen', 'x', 'angry', 'x', 'tv'],            // 1 B Plantão do Banimento, mano! O maior ladrão do Magic virou Papai Noel!
    ['rest', 'rest', 'other', 'cam', 'normal', 'flat', 'cuM'],         // 2 M Dack Fayden. Veio no precon do Jace. Outubro.
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'wide'],      // 3 B Ele dá criatura pros adversários, véi! Isso é jogada?!
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],          // 4 M Lê a carta: revela até achar uma criatura por adversário...
    ['point_tv', 'x', 'screen', 'x', 'angry', 'x', 'tvtext2'],         // 5 B E o presente ainda vem obrigado a atacar?!
    ['rest', 'rest', 'other', 'cam', 'normal', 'flat', 'cuM'],         // 6 M Goad. Ele bate nos outros. Não em você.
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'push'],      // 7 B Amigo secreto onde o presente morde a visita!
    ['rest', 'finger', 'other', 'other', 'normal', 'up', 'push'],      // 8 M E o gatilho de entrada... continua teu.
    ['shrug', 'rest', 'other', 'other', 'up', 'flat', 'cuB'],          // 9 B A criatura é deles e quem mira sou eu?! Sacanagem!
    ['rest', 'chip', 'other', 'other', 'normal', 'flat', 'wide'],      // 10 M Por isso já ganhou torneio de cEDH. Pegou a visão?
    ['arms_up', 'x', 'screen', 'x', 'angry', 'x', 'tv2'],              // 11 B E o presente hypou: dinossauro de precon subiu 327%!
    ['rest', 'rest', 'other', 'cam', 'normal', 'flat', 'cuM'],         // 12 M Ninguém quer ganhar o presente. Todo mundo quer dar.
    ['point_cam', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],     // 13 B Isso devia ser banido. Ou não? A, bane. B, aceita o presente.
    ['rest', 'remote', 'other', 'cam', 'normal', 'up', 'cuM'],         // 14 M Comenta aí. (TV desliga)
  ],
  // carta citada na fala 11: Bronzebeak Foragers (PNG real do Scryfall, lcc 69)
  inserts: [ { file: 'cards/bronzebeak.png', line: 10, at: 0.30, until: 11,
               cred: 'Bronzebeak Foragers (The Lost Caverns of Ixalan Commander, 2023), nº 69. Arte: Brian Valeza.' } ],
  // destaques medidos no PNG 744x1040 (linhas de pixels escuros da caixa de texto), em frações da carta
  hl: {
    tvtext:  { rects: [[0.563, 0.647, 0.206, 0.029],     // "reveal cards"
                       [0.085, 0.675, 0.749, 0.029],     // "from the top of your library until you reveal"
                       [0.085, 0.703, 0.299, 0.029],     // "X creature cards,"
                       [0.085, 0.839, 0.806, 0.029],     // "Each opponent gains control of the permanent"
                       [0.085, 0.867, 0.480, 0.029]],    // "for which they were chosen."
               zoom: 1.5 },
    tvtext2: { rects: [[0.646, 0.758, 0.140, 0.029],     // "They're"
                       [0.085, 0.785, 0.553, 0.029]],    // "goaded for the rest of the game."
               zoom: 1.5 },
  },
  tv: {
    channel: 'TV SAL', clock: '02:10',   // easter egg: 02/10, dia de lançamento do precon
    // sem Salt Score do Dack no EDHREC (29/10): o medidor mostra a conversão para top cut no EDHTop16
    meter: { title: 'CONVERSÔMETRO', value: '50%', fill: 0.5, calc: ['top cut no cEDH', 'EDHTop16', '29/10/2026'],
             levels: [['QUEBRADO', '#FF5A4E'], ['FORTE', '#F4B414'], ['NORMAL', '#6FB487']] },
    table: { label: ['PRESENTES', 'ENTREGUES'], value: '3 DE 3', note: ['um por adversário', '(mesa de 4)'] },
    news: [
      'URGENTE: maior ladrão do Multiverso abre ONG e distribui criaturas',
      'Precon de outubro vence torneio de cEDH; caixa de sapato comemora',
      'Dinossauro de precon sobe 327%: ninguém quer receber, todo mundo quer dar',
      'Polymorph sobe uns 600% por causa do Jace do mesmo precon',
      'Juiz confirma: presente do Dack não tem nota fiscal nem devolução',
      'Amigo secreto do Commander: o presente já vem atacando',
      'Plantão anterior: o pedágio do Tabernacle',
      'Winter Orb atrasou o plantão: só conseguiu desvirar um terreno',
    ],
  },
};
