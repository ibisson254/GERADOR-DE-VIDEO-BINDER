// Ep. 11 · "O rodízio de combo" (Niv-Mizzet Reborn · War of the Spark, 2019, nº 208)
// Kit v2 (manaburn/). Dados conferidos a 13/11/2026 (Scryfall API: Oracle e impressões).
// Inspiração: Reel de terceiros "The 2 Color Conundrum" (deck de Niv com um combo por par de cores), recebido do fundador a 13/11.
// Ângulo próprio: o Niv só traz a metade de duas cores; a outra peça de cada combo é monocolor ou incolor.
// pose por fala: [Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano]
const EP = {
  id: 'ep11_niv_rodizio',
  bug: 'RODÍZIO DE COMBO',
  poster: 'dragao',    // a carta é um dragão
  fx: { foco: true, tremor: true, poster: true, celular: true, scanner: false },
  outro: { assinatura: 'Escaneie suas cartas e organize seus decks.' },
  card: { img: 'cards/main.png',
          cred: 'Na TV: Niv-Mizzet Reborn (War of the Spark, 2019), nº 208. Arte: Raymond Swanland. © Wizards of the Coast.' },
  pose: [
    ['point_tv', 'x', 'screen', 'x', 'angry', 'x', 'tv'],            // 1 B Mano, a internet achou um deck … combo infinito!
    ['rest', 'rest', 'other', 'cam', 'normal', 'flat', 'cuM'],         // 2 M É o Niv-Mizzet Reborn. Tá na TV.
    ['point_tv', 'x', 'screen', 'x', 'up', 'x', 'tvtext2'],            // 3 B Ele entra, vira dez cartas … Rodízio de combo!
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],          // 4 M Lê a carta: … exatamente daquelas duas cores.
    ['shrug', 'rest', 'other', 'other', 'up', 'flat', 'cuB'],          // 5 B E daí? O Savage Ventmaw … Ele vem! (+ Ventmaw)
    ['rest', 'chip', 'other', 'other', 'normal', 'flat', 'wide'],      // 6 M Vem. Mas o combo dele é com Aggravated Assault … (+ Assault)
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'push'],      // 7 B Então troca! Duskmantle Guildmage com Mindcrank! (+ Mindcrank)
    ['rest', 'finger', 'other', 'cam', 'normal', 'up', 'cuM'],         // 8 M Mindcrank é incolor. O Niv nem olha.
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],       // 9 B Witherbloom Apprentice com Chain of Smog?! (+ Chain of Smog)
    ['rest', 'chip', 'other', 'other', 'normal', 'flat', 'wide'],      // 10 M Chain of Smog é só preta. O garçom traz o arroz …
    ['point_tv', 'x', 'screen', 'x', 'angry', 'x', 'tv2'],             // 11 B Então o deck infinito é meio combo?!
    ['rest', 'rest', 'other', 'cam', 'normal', 'flat', 'cuM'],         // 12 M Metade vem no Niv. A outra metade vem na reza.
    ['point_cam', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],     // 13 B O Niv virou dez cartas. Quantas vêm pra sua mão? Chuta de 0 a 10.
    ['rest', 'remote', 'other', 'cam', 'normal', 'up', 'cuM'],         // 14 M Comenta aí. (TV desliga)
  ],
  // cartas citadas: PNG oficial (Scryfall), primeira impressão de cada uma
  inserts: [
    { file: 'cards/ventmaw.png', line: 4, at: 0.3, until: 5,
      cred: 'Savage Ventmaw (Dragons of Tarkir, 2015), nº 231. Arte: Slawomir Maniak.' },
    { file: 'cards/assault.png', line: 5, at: 0.4, until: 6,
      cred: 'Aggravated Assault (Onslaught, 2002), nº 185. Arte: Greg Staples.' },
    { file: 'cards/mindcrank.png', line: 6, at: 0.5, until: 8,
      cred: 'Mindcrank (New Phyrexia, 2011), nº 144. Arte: Chris Rahn.' },
    { file: 'cards/smog.png', line: 8, at: 0.45, until: 10,
      cred: 'Chain of Smog (Onslaught, 2002), nº 132. Arte: Greg Staples.' },
  ],
  // destaques medidos no PNG 745x1040 (linhas de pixels escuros da caixa de texto), em frações da carta
  hl: {
    tvtext2: { rects: [[0.081, 0.711, 0.762, 0.031]], zoom: 1.5 },                                   // "battlefield, reveal the top ten cards of"
    tvtext:  { rects: [[0.081, 0.744, 0.812, 0.031], [0.081, 0.776, 0.770, 0.031]], zoom: 1.5 },     // "For each color pair, choose / a card that's exactly those colors"
  },
  tv: {
    channel: 'TV SAL', clock: '10:10',   // easter egg: 10 cartas reveladas, 10 pares de cores
    // a carta não está no Salt Score: o medidor mostra a conta das peças dos três combos do episódio (Oracle)
    meter: { title: 'COMBÔMETRO', value: '50%', fill: 0.5, calc: ['3 de 6 peças', 'o Niv acha', 'Oracle · Scryfall'],
             levels: [['COMBO', '#FF5A4E'], ['MEIO COMBO', '#F4B414'], ['REZA', '#6FB487']] },
    table: { label: ['PARES DE', 'CORES'], value: '10', note: ['cartas viradas:', 'só 10'] },
    news: [
      'URGENTE: Niv vira 10 cartas e o jogador reza por 10 pares',
      'Aggravated Assault é só vermelho desde 2002',
      'Mindcrank continua incolor; o Niv continua sem enxergar',
      'Rodízio de combo: o garçom só serve prato de duas cores',
      'Carta de três cores barrada na porta do Niv',
      'Niv-Mizzet Reborn custa uma mana de cada cor. O combo, não',
      'Plantão anterior: a febre do autógrafo',
      'Próximo plantão: domingo tem Giro',
    ],
  },
};
