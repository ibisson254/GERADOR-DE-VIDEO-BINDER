// Mana & Burn · TV SAL · Giro de domingo nº 2 (semana 02–08/11/2026)
// Kit v2 do repositório (manaburn/, sala v3 de 08/11 com a luz no cenário). Oito canais da TV SAL (EP.canais, motor do zapping).
// Bloco A: 3 notícias (cinema · Secret Lair · pré-release). Bloco B: a semana no BINDER, só com publicações confirmadas pelo fundador
// (Conde Ep. 004, especial "Burn foi assimilado", Meta em Curto EP05). Bloco C: a previsão do TUBO com as palavras do EP05.
// Telas da retrospectiva = quadros reais renderizados pelos motores dos próprios episódios (ver ficha.md). Fontes: ficha_fontes.md.
// Sem cuB nem push: nenhum zoom que corte a TV (preferência do fundador, especial de 06/11).
// pose por fala: [Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano]
const CR = '© Wizards of the Coast. Conteúdo de fã não oficial.';
const EP = {
  id: 'giro_2026-11-08',
  bug: 'TV SAL · GIRO DE DOMINGO',
  poster: 'artefato',
  calendario: '1996',   // ano do calendário da parede (pedido do fundador, 08/11/2026, só neste episódio; o kit continua com 2019 por defeito)
  fx: { foco: true, tremor: true, poster: true, celular: true, scanner: false },
  outro: { assinatura: 'Escaneie suas cartas e organize seus decks.' },
  card: { img: 'cards/giro_abre.png', cred: 'TV SAL · notícias de 02 a 08/11/2026. Fontes na legenda.' },
  pose: [
    ['point_tv', 'rest', 'tv', 'other', 'up', 'flat', 'tv'],          // 1 B TV SAL, giro de domingo
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tv2'],        // 2 M Um. Maya Hawke (canal 1)
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'wide'],     // 3 B embaralhar cem cartas
    ['rest', 'rest', 'other', 'cam', 'normal', 'flat', 'cuM'],        // 4 M papel em segredo
    ['point_tv', 'x', 'screen', 'x', 'up', 'x', 'tv'],                // 5 B Dois! Secret Lair (canal 2)
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tv2'],        // 6 M metade pro hospital
    ['shrug', 'rest', 'cam', 'other', 'up', 'flat', 'wide'],          // 7 B que carta vem?
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],         // 8 M Lê a carta (destaque)
    ['arms_up', 'rest', 'cam', 'other', 'up', 'flat', 'wide'],        // 9 B não baniria
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tv2'],        // 10 M Três. pré-release (canal 3)
    ['point_tv', 'rest', 'tv', 'other', 'up', 'flat', 'wide'],        // 11 B a semana no BINDER (canal 4: Conde)
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tv2'],        // 12 M Conde: obra notável
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'wide'],     // 13 B nem descruza o braço
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tv2'],        // 14 M Cubo Borg (canal 5)
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'wide'],     // 15 B devia ser banido
    ['rest', 'finger', 'other', 'cam', 'normal', 'up', 'cuM'],        // 16 M não artefato
    ['point_tv', 'x', 'screen', 'x', 'up', 'x', 'tv'],                // 17 B TUBO 3,8% (canal 6)
    ['rest', 'chip', 'other', 'cam', 'normal', 'flat', 'cuM'],        // 18 M impulsionamento pago
    ['point_tv', 'rest', 'tv', 'other', 'up', 'flat', 'wide'],        // 19 B deixou um recado (canal 7)
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tv'],         // 20 M palavras dele
    ['shrug', 'rest', 'cam', 'other', 'up', 'flat', 'wide'],          // 21 B ele acertou?
    ['rest', 'finger', 'other', 'cam', 'normal', 'up', 'cuM'],        // 22 M segunda, prestar contas
    ['point_cam', 'rest', 'cam', 'other', 'angry', 'flat', 'wide'],   // 23 B Comenta 1, 2 ou 3
    ['rest', 'remote', 'other', 'cam', 'normal', 'up', 'cuM'],        // 24 M Comenta aí (TV desliga)
  ],
  inserts: [],
  canais: [
    { de: 0, ch: 8, canal: 'ABERTURA', img: 'cards/giro_abre.png', cred: 'TV SAL · notícias de 02 a 08/11/2026. Fontes na legenda.',
      meter: { title: 'NOTÍCIAS', value: '3', fill: 0.6, calc: ['semana', '02 a 08/11', 'na legenda'],
               levels: [['QUENTE', '#FF5A4E'], ['MORNA', '#F4B414'], ['FRIA', '#6FB487']] },
      table: null },
    { de: 1, ch: 1, canal: '1 · CINEMA', img: 'cards/giro_filme.png', cred: 'Fontes: Deadline e TheWrap (04/11/2026).',
      meter: { title: 'ELENCO ANUNCIADO', value: '1', fill: 0.25, calc: ['Maya Hawke', 'Deadline', '04/11/2026'],
               levels: [['COMPLETO', '#FF5A4E'], ['METADE', '#F4B414'], ['COMEÇANDO', '#6FB487']] },
      table: { label: ['PAPEL DELA', 'NO FILME'], value: '???', note: ['não divulgado', 'Deadline'] } },
    { de: 4, ch: 2, canal: '2 · SECRET LAIR', img: 'cards/giro_pyromancer.png',
      cred: 'Na TV: Young Pyromancer (Magic 2014), nº 163. Arte: Cynthia Sheppard.<br>' + CR,
      hl: { tvtext: { rects: [[0.100, 0.668, 0.800, 0.030], [0.100, 0.704, 0.800, 0.034], [0.100, 0.738, 0.520, 0.030]], zoom: 1.5 } },
      meter: { title: 'PRA CARIDADE', value: '50%', fill: 0.5, calc: ['menos taxas', 'Wizards', '03/11/2026'],
               levels: [['TUDO', '#FF5A4E'], ['METADE', '#F4B414'], ['NADA', '#6FB487']] },
      table: { label: ['À VENDA', 'SECRET LAIR'], value: '16–30/11', note: ['Rise of the', 'Polygons'] } },
    { de: 9, ch: 3, canal: '3 · PRA JOGAR', img: 'cards/giro_prerelease.png', cred: 'Fonte: Wizards of the Coast (guia do pré-release; MTG Arena, 02/11/2026).',
      meter: { title: 'DIAS DE PRÉ-RELEASE', value: '7', fill: 0.7, calc: ['de 6 a 12/11', 'Sealed', 'Wizards'],
               levels: [['CORRE', '#FF5A4E'], ['DÁ TEMPO', '#F4B414'], ['FOLGA', '#6FB487']] },
      table: { label: ['STAR TREK', 'NO ARENA'], value: '10/11', note: ['nas lojas:', '13/11'] } },
    { de: 10, ch: 4, canal: 'A SEMANA · CONDE', img: 'cards/giro_conde.png',
      cred: 'Na TV: O Tribunal Estético, processo nº 004 (Conde de Manaforte). Joven (Homelands, 1995), nº 77. Arte: Douglas Shuler.<br>' + CR,
      meter: { title: 'PROCESSO Nº', value: '004', fill: 1, calc: ['Conde de', 'Manaforte', 'no perfil'],
               levels: [['NOTÁVEL', '#FF5A4E'], ['DUVIDOSO', '#F4B414'], ['ARQUIVADO', '#6FB487']] },
      table: { label: ['PARECER', 'DO CONDE'], value: 'NOTÁVEL', note: ['réu: Joven', '1995'] } },
    { de: 13, ch: 5, canal: 'A SEMANA · BURN FOI ASSIMILADO', img: 'cards/giro_burn.png',
      cred: 'Na TV: especial "Burn foi assimilado!". Resistance Is Futile (Magic: The Gathering | Star Trek, 2026), nº 125. Arte: Matt Stewart.<br>© Wizards of the Coast. Star Trek © CBS. Conteúdo de fã não oficial.',
      meter: { title: 'BORG DESTRUÍDOS', value: '0%', fill: 0, calc: ['todo Borg', 'é artefato', 'Oracle'],
               levels: [['TODOS', '#FF5A4E'], ['ALGUNS', '#F4B414'], ['NENHUM', '#6FB487']] },
      table: null },
    { de: 16, ch: 6, canal: 'A SEMANA · META EM CURTO', img: 'cards/giro_tubo.png',
      cred: 'Na TV: Meta em Curto EP05, com o TUBO (BINDER Originals).<br>Star Trek © CBS. Conteúdo de fã não oficial.',
      meter: { title: 'CHANCE DE ABRIR', value: '3,8%', fill: 0.15, calc: ['mítica', '6 boosters', 'EP05'],
               levels: [['SORTE', '#FF5A4E'], ['TALVEZ', '#F4B414'], ['ESQUECE', '#6FB487']] },
      table: { label: ['VISUALIZAÇÕES', 'COM IMPULSO PAGO'], value: '5.334', note: ['Instagram', 'dado do fundador'] } },
    { de: 18, ch: 7, canal: 'RECADO DO TUBO', img: 'cards/giro_previsao.png',
      cred: 'Na TV: Meta em Curto EP05 (05/11/2026), previsão registrada.<br>Conteúdo de fã não oficial.',
      meter: { title: 'GRAU DE CERTEZA', value: 'BAIXA', fill: 0.2, calc: ['opinião', '17Lands', 'até 01/12'],
               levels: [['ALTA', '#FF5A4E'], ['MÉDIA', '#F4B414'], ['BAIXA', '#6FB487']] },
      table: { label: ['PRESTAÇÃO', 'DE CONTAS'], value: '9/11', note: ['segunda', 'Meta em Curto'] } },
  ],
  tv: {
    channel: 'TV SAL', clock: '08:11',
    meter: { title: 'NOTÍCIAS', value: '3', fill: 0.6, calc: ['semana', '02 a 08/11', 'na legenda'],
             levels: [['QUENTE', '#FF5A4E'], ['MORNA', '#F4B414'], ['FRIA', '#6FB487']] },
    table: null,
    news: [
      'URGENTE: Secret Lair que tinha vazado agora é oficial',
      'Pré-release de Star Trek vai até quinta, 12/11',
      'Star Trek chega ao MTG Arena na terça, 10/11',
      'Filme de Magic: papel da Maya Hawke segue em segredo',
      'Burn segue assimilado; sofá pede paciência',
      'Mesa de Sealed descobre que nave também estaciona',
      'Plantão anterior: o Burn foi assimilado no pré-release',
      'Próximo plantão: segunda, o TUBO presta contas',
    ],
  },
};
