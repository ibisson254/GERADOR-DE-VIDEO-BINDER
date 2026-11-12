// Ep. 10 · "A febre do autógrafo" (Captain James T. Kirk, carta de autógrafo nº 1701 · Magic: The Gathering | Star Trek, 2026)
// Kit v2 (manaburn/). Dados conferidos a 07/11/2026 (Scryfall API + Wizards "Collecting Star Trek", 20/10/2026).
// pose por fala: [Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano]
const EP = {
  id: 'ep10_cartas_especiais',
  bug: 'PLANTÃO DO PACOTE',   // cumpre a promessa do Zapping nº 1 ("Plantão do Pacote"), com atraso assumido na TV SAL
  poster: 'mago',      // nenhum pôster do kit é "capitão"; mago é o mais próximo de criatura humana (igual ao Ep. 9)
  // fecho: bloco do scanner do kit desligado; o fecho oficial (comum/outro/outro_binder_916.mp4) entra por concat.
  fx: { foco: true, tremor: true, poster: true, celular: true, scanner: false },
  outro: { assinatura: 'Escaneie suas cartas e organize seus decks.' },
  card: { img: 'cards/main.png',
          cred: 'Na TV: Captain James T. Kirk (Star Trek, 2026), nº 1701, carta de autógrafo. Arte: Chris Rallis.<br>Imagem oficial: o painel da assinatura aparece vazio. © Wizards of the Coast. Star Trek © CBS.' },
  pose: [
    ['point_tv', 'x', 'screen', 'x', 'angry', 'x', 'tv'],            // 1 B Mano, hoje eu abro um Kirk assinado no pré-release. Tô sentindo!
    ['rest', 'rest', 'other', 'cam', 'normal', 'flat', 'cuM'],         // 2 M Assinado à mão pelo ator. Sete cartas. Umas 250 de cada.
    ['arms_up', 'rest', 'cam', 'other', 'up', 'flat', 'wide'],         // 3 B 250 no planeta e uma vai brotar no meu pacote!
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],          // 4 M Lê a carta: não tem texto. Só o espaço da assinatura.
    ['shrug', 'rest', 'other', 'other', 'up', 'flat', 'cuB'],          // 5 B Então ela faz o quê na mesa?!
    ['rest', 'chip', 'other', 'other', 'normal', 'flat', 'wide'],      // 6 M O mesmo que o Kirk nº 142. Camisa autografada não faz gol. (+ insert 142)
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'push'],      // 7 B Mas fica linda na parede! Já comprei até a moldura!
    ['rest', 'finger', 'other', 'other', 'normal', 'up', 'push'],      // 8 M Pré-release é Play Booster. Assinada só vem no Collector.
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],       // 9 B Seis pacotes de esperança e zero autógrafo?!
    ['rest', 'rest', 'other', 'cam', 'normal', 'flat', 'cuM'],         // 10 M Zero. Mas Stardate e LCARS saem no Play. Ilusão liberada.
    ['point_tv', 'x', 'screen', 'x', 'angry', 'x', 'tv2'],             // 11 B E a internet rachou: uns acham genial, outros dizem que virou loteria!
    ['rest', 'chip', 'other', 'other', 'normal', 'flat', 'wide'],      // 12 M Na mesa, todo Kirk faz igual. Só um faz a mão tremer.
    ['point_cam', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],     // 13 B Autógrafo dentro do booster: A, genial. B, loteria.
    ['rest', 'remote', 'other', 'cam', 'normal', 'up', 'cuM'],         // 14 M Comenta aí. (TV desliga)
  ],
  // carta citada na fala 6: o Kirk normal (mesmo oracle_id do 1701 no Scryfall), PNG oficial
  inserts: [ { file: 'cards/kirk142.png', line: 5, at: 0.25, until: 6,
               cred: 'Captain James T. Kirk (Star Trek, 2026), nº 142. Arte: Jason Pastrana.' } ],
  // destaque medido no PNG 744x1040: painel prateado da assinatura (sem caixa de texto), em frações da carta
  hl: {
    tvtext: { rects: [[0.070, 0.661, 0.845, 0.152]], zoom: 1.5 },
  },
  tv: {
    channel: 'TV SAL', clock: '17:01',   // easter egg: 1701 = nº da carta de autógrafo do Kirk (e matrícula NCC-1701 da Enterprise)
    // sem Salt Score (carta nova): o medidor mostra um facto da Wizards, sem probabilidade inventada
    meter: { title: 'ASSINÔMETRO', value: '0%', fill: 0, calc: ['no Play Booster', 'Wizards', '20/10/2026'],
             levels: [['ASSINADA', '#FF5A4E'], ['SÓ NO', '#F4B414'], ['COLLECTOR', '#6FB487']] },
    table: { label: ['ASSINADAS', 'NO MUNDO'], value: '< 1.750', note: ['7 cartas ×', 'menos de 250'] },
    news: [
      'URGENTE: jogador procura autógrafo até no token do Play Booster',
      'Assinatura não dá poder: o Kirk continua 2/2',
      'Stardate aparece em 1 de cada 25 Play Boosters, diz a Wizards',
      'Kirk nº 142 e Kirk assinado: mesma carta, só um ganhou capinha dupla',
      'Europa: Collector Booster atrasado; a esperança chegou no horário',
      'Plantão do Pacote: atrasou, mas chegou',
      'Plantão anterior: o Giro de domingo',
      'Próximo plantão: dia 13 o set chega às lojas',
    ],
  },
};
