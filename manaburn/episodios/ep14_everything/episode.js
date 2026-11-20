// MB-EP14 · EVERYTHING, MENOS TUDO · Secret Lair x Duna (My Arrakis, My Superdrop): o Desert Power Everything Bundle leva 2 dos 3 drops.
// Factos: anúncio oficial da Wizards (18/11/2026). Cartas: PNG do Scryfall (Secret Lair Drop 2912–2930, 20/11/2026). Kit v2 + sala v3.
// Uma tela da TV SAL por assunto (EP.canais) ou insert nos cuB; falas longas trocam para a variante da tela a meio (EP.canais[].meio, opção nova do kit). pose por fala: [Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano]
const CR = '© Wizards of the Coast. Conteúdo de fã não oficial.';
const FW = 'Anúncio oficial da Wizards, 18/11/2026';
const M_DROPS = { title: 'DROPS NO BUNDLE', value: '2', fill: 0.67, calc: ['2 de 3 drops', 'Spice fora', FW.replace('Anúncio oficial da ', '')], levels: [['TUDO', '#6FB487'], ['QUASE', '#F4B414'], ['NADA', '#FF5A4E']] };
const M_SPICE = { title: 'SPICE (EUA)', value: '$59,99', fill: 0.26, calc: ['Halo Foil, sozinho', 'fora do bundle', 'Wizards, 18/11/2026'], levels: [['3 DROPS', '#FF5A4E'], ['BUNDLE', '#F4B414'], ['SPICE', '#6FB487']] };
const M_BUNDLE = { title: 'BUNDLE (EUA)', value: '$174,99', fill: 0.74, calc: ['4 edições, 2 drops', 'sem o Spice', 'Wizards, 18/11/2026'], levels: [['3 DROPS', '#FF5A4E'], ['BUNDLE', '#F4B414'], ['SPICE', '#6FB487']] };
const M_TOTAL = { title: 'OS 3 DROPS (EUA)', value: '$234,98', fill: 1, calc: ['174,99 + 59,99', 'conta do BINDER', 'Wizards, 18/11/2026'], levels: [['3 DROPS', '#FF5A4E'], ['BUNDLE', '#F4B414'], ['SPICE', '#6FB487']] };
const M_DATA = { title: 'VENDA', value: '30/11', fill: 0.8, calc: ['9h PT · 14h Brasília', '17h Lisboa', 'Wizards, 18/11/2026'], levels: [['VENDA', '#FF5A4E'], ['FILA', '#F4B414'], ['ANÚNCIO', '#6FB487']] };
const T_DESC = { label: ['DESCONTO', 'DO BUNDLE'], value: '$4,97', note: ['avulso 179,96', 'bundle 174,99'] };
const EP = {
  id: 'ep14_everything',
  bug: 'TV SAL',
  poster: 'artefato',
  fx: { foco: true, tremor: true, poster: true, celular: true, scanner: false, tv_ligada: true },
  outro: { assinatura: 'Escaneie suas cartas e organize sua coleção.' },
  card: { img: 'cards/s01_tres.png',
          cred: 'Na TV: Paul Atreides, Ducal Heir (SLD 2912, Jodie Muir) · Shai-Hulud (SLD 2920, Grzegorz Rutkowski) · Water of Life (SLD 2926, Svetlin Velinov).<br>' + CR },
  pose: [
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'tv'],      // 1 B três drops, bundle leva dois (quadro 0: os 3 drops)
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],        // 2 M Lê o anúncio: 4 linhas do bundle destacadas
    ['point_tv', 'rest', 'tv', 'other', 'up', 'flat', 'tv2'],        // 3 B Spice de brinde?
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],        // 4 M só Halo Foil · vendido à parte (destacado)
    ['point_cam', 'rest', 'cam', 'other', 'up', 'flat', 'cuB'],      // 5 B quanto custa o tempero? (insert: $?)
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tv'],        // 6 M US$ 59,99
    ['point_tv', 'rest', 'tv', 'other', 'up', 'flat', 'tv'],         // 7 B descontão?
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],        // 8 M 174,99 · desconto 4,97 (destacado)
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],     // 9 B cinco dólares e falta UM?! (insert: −$4,97, tremor)
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tv2'],       // 10 M os três: 234,98
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],     // 11 B o pacote de TUDO deixa coisa de fora (insert: EVERYTHING*)
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],        // 12 M 30 de novembro, 14h (destacado)
    ['point_cam', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],   // 13 B pergunta A/B (insert: A/B)
    ['rest', 'remote', 'other', 'cam', 'normal', 'up', 'cuM'],       // 14 M Comenta aí (TV desliga)
  ],
  inserts: [
    { file: 'cards/i05_tempero.png', line: 4, at: 0.05, until: 5,
      cred: 'Harkonnen Spice Harvester (SLD 2928, Raphael Lacoste) · Revel in Riches (SLD 2927, Raymond Swanland).' },
    { file: 'cards/i09_desconto.png', line: 8, at: 0.05, until: 9,
      cred: 'Conta: 179,96 (4 edições avulsas) − 174,99 (bundle) = 4,97. Preços oficiais nos EUA, Wizards, 18/11/2026.' },
    { file: 'cards/i11_menos.png', line: 10, at: 0.05, until: 11,
      cred: 'Water of Life (SLD 2926, Svetlin Velinov) · Pain Box (SLD 2930, Alexander Mokhov).' },
    { file: 'cards/s13_ab.png', line: 12, at: 0.05, until: 13,
      cred: 'Preços oficiais nos EUA (Wizards, 18/11/2026). Water of Life (SLD 2926).' },
  ],
  canais: [
    { de: 0, ch: 3, canal: 'SECRET LAIR x DUNA', img: 'cards/s01_tres.png', meio: { at: 0.5, img: 'cards/s01_tres_b.png' },
      cred: 'Na TV: Paul Atreides, Ducal Heir (SLD 2912, Jodie Muir) · Shai-Hulud (SLD 2920, Grzegorz Rutkowski) · Water of Life (SLD 2926, Svetlin Velinov).<br>' + CR,
      meter: M_DROPS, table: null },
    { de: 1, ch: 4, canal: 'LÊ O ANÚNCIO', img: 'cards/s02_anuncio.png', meio: { at: 0.55, img: 'cards/s02_anuncio_b.png' },
      cred: 'Na TV: ' + FW + '. Paul Atreides (SLD 2912) · Shai-Hulud (SLD 2920).<br>' + CR,
      hl: { tvtext: { rects: [[0.083, 0.488, 0.834, 0.064], [0.083, 0.563, 0.834, 0.064], [0.083, 0.638, 0.834, 0.064], [0.083, 0.713, 0.834, 0.064]], zoom: 1.5 } },
      meter: M_DROPS, table: null },
    { de: 2, ch: 5, canal: 'BRINDE?', img: 'cards/s03_brinde.png',
      cred: 'Na TV: Water of Life (SLD 2926, Svetlin Velinov) · Pain Box (SLD 2930, Alexander Mokhov) · Revel in Riches (SLD 2927, Raymond Swanland).<br>' + CR,
      meter: M_DROPS, table: null },
    { de: 3, ch: 6, canal: 'LÊ O ANÚNCIO', img: 'cards/s04_spice.png', meio: { at: 0.55, img: 'cards/s04_spice_b.png' },
      cred: 'Na TV: ' + FW + '. Water of Life (SLD 2926) · Pain Box (SLD 2930) · Harkonnen Spice Harvester (SLD 2928, Raphael Lacoste).<br>' + CR,
      hl: { tvtext: { rects: [[0.083, 0.508, 0.834, 0.064], [0.083, 0.594, 0.834, 0.064]], zoom: 1.5 } },
      meter: M_DROPS, table: null },
    { de: 5, ch: 7, canal: 'PREÇO DO SPICE', img: 'cards/s06_spice_preco.png',
      cred: 'Na TV: ' + FW + ' (preço nos EUA). Water of Life (SLD 2926, Svetlin Velinov).<br>' + CR,
      meter: M_SPICE, table: null },
    { de: 6, ch: 8, canal: 'DESCONTÃO?', img: 'cards/s07_descontao.png',
      cred: 'Na TV: Balance of Power (SLD 2912, Jodie Muir) e Deserts of Arrakis (SLD 2920, Grzegorz Rutkowski), foil e não foil.<br>' + CR,
      meter: M_BUNDLE, table: null },
    { de: 7, ch: 9, canal: 'LÊ O ANÚNCIO', img: 'cards/s08_bundle_preco.png', meio: { at: 0.5, img: 'cards/s08_bundle_preco_b.png' },
      cred: 'Na TV: ' + FW + ' (preços nos EUA). Desconto calculado pelo BINDER.<br>' + CR,
      hl: { tvtext: { rects: [[0.083, 0.506, 0.834, 0.106]], zoom: 1.5 } },
      meter: M_BUNDLE, table: T_DESC },
    { de: 9, ch: 10, canal: 'OS TRÊS DROPS', img: 'cards/s10_tres_drops.png', meio: { at: 0.5, img: 'cards/s10_tres_drops_b.png' },
      cred: 'Na TV: conta do BINDER com os preços do ' + FW.toLowerCase() + '.<br>' + CR,
      meter: M_TOTAL, table: T_DESC },
    { de: 11, ch: 11, canal: 'QUANDO', img: 'cards/s12_data.png', meio: { at: 0.5, img: 'cards/s12_data_b.png' },
      cred: 'Na TV: ' + FW + '. Shai-Hulud (SLD 2920, Grzegorz Rutkowski).<br>' + CR,
      hl: { tvtext: { rects: [[0.083, 0.460, 0.834, 0.092], [0.083, 0.567, 0.834, 0.073]], zoom: 1.5 } },
      meter: M_DATA, table: null },
  ],
  tv: {
    channel: 'TV SAL', clock: '14:00',   // easter egg: hora da venda em Brasília (30/11, 9h PT)
    meter: M_DROPS, table: null,
    news: [
      'URGENTE: pacote Everything esquece um drop',
      'Bundle reúne 4 edições de 2 drops',
      'Spice só em Halo Foil e vendido à parte',
      'Desconto do bundle: US$ 4,97',
      'Shai-Hulud destrói artefatos e encantamentos ao entrar',
      'Thumper bate na areia; o Spice não aparece',
      'Venda em 30/11, 9h PT (14h de Brasília)',
      'Plantão anterior: o deck que nunca fica pronto',
    ],
  },
};
