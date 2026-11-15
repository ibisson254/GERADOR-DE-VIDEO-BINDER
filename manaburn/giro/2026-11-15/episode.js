// Mana & Burn · TV SAL · Giro de domingo nº 3 (semana 09–15/11/2026) · v2 «feedback visual em cada fala» (fundador, 15/11/2026 03:08)
// Kit v2 (sala v3, luz no cenário). Uma tela da TV SAL por fala (EP.canais) com a coisa de que a personagem fala;
// nos grandes planos de reação (cuB), a imagem entra como insert ao lado (estratégia do MB-EP11, o mais visto da série).
// Telas: telas_visuais.py (+ giro_chandra/giro_numot/giro_conde). Fontes: fontes.md. Voz igual à v1 (sem créditos novos).
// pose por fala: [Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano]
const CR = '© Wizards of the Coast. Conteúdo de fã não oficial.';
const EP = {
  id: 'giro_2026-11-15',
  bug: 'TV SAL · GIRO DE DOMINGO',
  poster: 'artefato',
  fx: { foco: true, tremor: true, poster: true, celular: true, scanner: false },
  outro: { assinatura: 'Escaneie suas cartas e organize seus decks.' },
  card: { img: 'cards/v01_abre.png', cred: 'TV SAL · notícias de 09 a 15/11/2026. Fontes na legenda.' },
  pose: [
    ['point_tv', 'rest', 'tv', 'other', 'up', 'flat', 'tv'],  // 1 B giro de domingo · TV: cartas de Magic (quadro 0)
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tv2'],  // 2 M BK · TV: foto da deck box
    ['arms_up', 'rest', 'cam', 'other', 'up', 'flat', 'cuB'],  // 3 B larguei a batata · insert: deck box
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tv2'],  // 4 M €19,90 · TV: preço
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],  // 5 B vem pra cá · insert: Itália sim, Brasil não
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tv2'],  // 6 M Rosewater · TV: nada decidido
    ['point_tv', 'x', 'screen', 'x', 'up', 'x', 'tv'],  // 7 B Dois! Netflix · TV: imagem de PLANESWALKER
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tv2'],  // 8 M Chandra · TV: carta da Chandra
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],  // 9 B queimar o elenco · insert: Chandra
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],  // 10 M Lê a carta −3 · destaque
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],  // 11 B devia ser banido · insert: Chandra
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tv2'],  // 12 M semana no BINDER · TV: capa do EP11
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],  // 13 B dois terrenos · insert: Numot
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],  // 14 M Lê a carta Numot · destaque
    ['point_tv', 'rest', 'tv', 'other', 'up', 'flat', 'tv'],  // 15 B Conde · TV: capa do CM-EP005
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tv2'],  // 16 M obra notável · TV: carta + carimbo
    ['point_tv', 'rest', 'tv', 'other', 'up', 'flat', 'tv'],  // 17 B TUBO · TV: TUBO + 3 episódios
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tv2'],  // 18 M 66% · TV: print da Preconauta
    ['point_tv', 'x', 'screen', 'x', 'up', 'x', 'tv'],  // 19 B Nauctis · TV: cartas de Nauctis
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tv2'],  // 20 M Lotus · TV: Abyssal Lotus
    ['point_tv', 'x', 'screen', 'x', 'up', 'x', 'tv'],  // 21 B Mundial · TV: cartas de Jund Sacrifice
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tv2'],  // 22 M sem spoiler · TV: TUBO 16/11
    ['point_tv', 'x', 'screen', 'x', 'angry', 'x', 'tv'],  // 23 B Comenta 1, 2 ou 3 · TV: as três opções
    ['rest', 'remote', 'other', 'cam', 'normal', 'up', 'cuM'],  // 24 M Comenta aí (TV desliga)
  ],
  inserts: [
    { file: 'cards/ins_bk.png', line: 2, at: 0.05, until: 3, cred: 'Burger King Itália × Magic (foto de divulgação).' },
    { file: 'cards/ins_brasil.png', line: 4, at: 0.05, until: 5, cred: 'Promoção só na Itália, até 30/11/2026.' },
    { file: 'cards/giro_chandra.png', line: 8, at: 0.05, until: 9, cred: 'Chandra, Torch of Defiance (KLD 110). Arte: Magali Villeneuve.' },
    { file: 'cards/giro_chandra.png', line: 10, at: 0.05, until: 11, cred: 'Chandra, Torch of Defiance (KLD 110). Arte: Magali Villeneuve.' },
    { file: 'cards/giro_numot.png', line: 12, at: 0.05, until: 13, cred: 'Numot, the Devastator (CMD 215). Arte: Dan Dos Santos.' },
  ],
  canais: [
    { de: 0, ch: 1, canal: 'ABERTURA', img: 'cards/v01_abre.png',
      cred: 'TV SAL · notícias de 09 a 15/11/2026. Na TV: Chandra, Torch of Defiance (KLD 110, Magali Villeneuve) e Numot, the Devastator (CMD 215, Dan Dos Santos).<br>© Wizards of the Coast. Conteúdo de fã não oficial.',
      meter: { title: 'NOTÍCIAS', value: '3', fill: 0.6, calc: ['semana', '09 a 15/11', 'na legenda'], levels: [['QUENTE', '#FF5A4E'], ['MORNA', '#F4B414'], ['FRIA', '#6FB487']] },
      table: null },
    { de: 1, ch: 2, canal: '1 · LANCHE', img: 'cards/v02_bk.png',
      cred: 'Foto: divulgação Burger King × Magic. Fontes: Dexerto e ICv2 (10/11/2026).',
      meter: { title: 'PREÇO DO COMBO', value: '€19,90', fill: 0.5, calc: ['lanche + deck box', '+ 100 sleeves', 'BK Itália'], levels: [['CARO', '#FF5A4E'], ['JUSTO', '#F4B414'], ['BARATO', '#6FB487']] },
      table: { label: ['SÓ NA', 'ITÁLIA'], value: 'ATÉ 30/11', note: ['final do torneio:', '27/11, Milão'] } },
    { de: 3, ch: 3, canal: '1 · LANCHE', img: 'cards/v04_preco.png',
      cred: 'Fontes: Burger King Itália, via Dexerto e MTG Rocks (10/11/2026).',
      meter: { title: 'PREÇO DO COMBO', value: '€19,90', fill: 0.5, calc: ['lanche + deck box', '+ 100 sleeves', 'BK Itália'], levels: [['CARO', '#FF5A4E'], ['JUSTO', '#F4B414'], ['BARATO', '#6FB487']] },
      table: { label: ['SÓ NA', 'ITÁLIA'], value: 'ATÉ 30/11', note: ['final do torneio:', '27/11, Milão'] } },
    { de: 5, ch: 4, canal: '1 · E O BRASIL?', img: 'cards/v06_rosewater.png',
      cred: 'Paráfrase de Mark Rosewater (Blogatog), via MTG Rocks (11/11/2026).',
      meter: { title: 'PREÇO DO COMBO', value: '€19,90', fill: 0.5, calc: ['lanche + deck box', '+ 100 sleeves', 'BK Itália'], levels: [['CARO', '#FF5A4E'], ['JUSTO', '#F4B414'], ['BARATO', '#6FB487']] },
      table: null },
    { de: 6, ch: 5, canal: '2 · STREAMING', img: 'cards/v07_netflix.png',
      cred: 'Imagem: Netflix (logótipo). Fontes: Netflix Tudum e Deadline (13/11/2026).',
      meter: { title: 'ESTREIA', value: '2027', fill: 0.3, calc: ['sem data', 'definida', 'Netflix'], levels: [['JÁ', '#FF5A4E'], ['LOGO', '#F4B414'], ['ESPERA', '#6FB487']] },
      table: { label: ['PROTAGONISTA', ''], value: 'CHANDRA', note: ['showrunner:', 'Terry Matalas'] } },
    { de: 7, ch: 6, canal: '2 · LÊ A CARTA', img: 'cards/giro_chandra.png',
      cred: 'Na TV: Chandra, Torch of Defiance (Kaladesh, 2016), nº 110. Arte: Magali Villeneuve.<br>© Wizards of the Coast. Conteúdo de fã não oficial.',
      hl: { tvtext: { rects: [[0.050, 0.748, 0.880, 0.026], [0.120, 0.773, 0.300, 0.026]], zoom: 1.5 } },
      meter: { title: 'ALVOS DO −3', value: '1', fill: 0.1, calc: ['criatura alvo', '4 de dano', 'Oracle'], levels: [['ELENCO TODO', '#FF5A4E'], ['ALGUNS', '#F4B414'], ['UM SÓ', '#6FB487']] },
      table: null },
    { de: 11, ch: 7, canal: 'A SEMANA · MANA & BURN', img: 'cards/v12_numot_ep.png',
      cred: 'Na TV: capa do Mana & Burn EP11. Numot, the Devastator (Commander 2011), nº 215. Arte: Dan Dos Santos.<br>© Wizards of the Coast. Conteúdo de fã não oficial.',
      meter: { title: 'TERRENOS', value: 'ATÉ 2', fill: 0.5, calc: ['pagando', '{2}{R}', 'Oracle'], levels: [['TODOS', '#FF5A4E'], ['DOIS', '#F4B414'], ['NENHUM', '#6FB487']] },
      table: { label: ['NO PERFIL', 'DESDE'], value: '11/11', note: ['Mana & Burn', 'EP11'] } },
    { de: 13, ch: 8, canal: 'A SEMANA · LÊ A CARTA', img: 'cards/giro_numot.png',
      cred: 'Na TV: Numot, the Devastator (Commander 2011), nº 215. Arte: Dan Dos Santos.<br>© Wizards of the Coast. Conteúdo de fã não oficial.',
      hl: { tvtext: { rects: [[0.100, 0.792, 0.800, 0.030], [0.100, 0.826, 0.500, 0.030]], zoom: 1.5 } },
      meter: { title: 'TERRENOS', value: 'ATÉ 2', fill: 0.5, calc: ['pagando', '{2}{R}', 'Oracle'], levels: [['TODOS', '#FF5A4E'], ['DOIS', '#F4B414'], ['NENHUM', '#6FB487']] },
      table: null },
    { de: 14, ch: 9, canal: 'A SEMANA · CONDE', img: 'cards/giro_conde.png',
      cred: 'Na TV: capa do Conde de Manaforte EP005. Hyalopterous Lemure (Ice Age, 1995). Arte: Richard Thomas.<br>© Wizards of the Coast. Conteúdo de fã não oficial.',
      meter: { title: 'PROCESSO Nº', value: '005', fill: 1, calc: ['Conde de', 'Manaforte', 'no perfil'], levels: [['NOTÁVEL', '#FF5A4E'], ['DUVIDOSO', '#F4B414'], ['ARQUIVADO', '#6FB487']] },
      table: { label: ['PARECER', 'DO CONDE'], value: 'NOTÁVEL', note: ['errou de', 'mitologia'] } },
    { de: 15, ch: 10, canal: 'A SEMANA · CONDE', img: 'cards/v16_lemure.png',
      cred: 'Na TV: Hyalopterous Lemure (Ice Age, 1995), nº 133. Arte: Richard Thomas.<br>© Wizards of the Coast. Conteúdo de fã não oficial.',
      meter: { title: 'PROCESSO Nº', value: '005', fill: 1, calc: ['Conde de', 'Manaforte', 'no perfil'], levels: [['NOTÁVEL', '#FF5A4E'], ['DUVIDOSO', '#F4B414'], ['ARQUIVADO', '#6FB487']] },
      table: { label: ['PARECER', 'DO CONDE'], value: 'NOTÁVEL', note: ['errou de', 'mitologia'] } },
    { de: 16, ch: 11, canal: 'A SEMANA · META EM CURTO', img: 'cards/v17_tubo.png',
      cred: 'Na TV: o TUBO (Meta em Curto, BINDER Originals).',
      meter: { title: 'QUEM COMEÇA', value: '66%', fill: 0.66, calc: ['jogo 1', 'Taça Preconauta', 'ESP02'], levels: [['SEMPRE', '#FF5A4E'], ['QUASE', '#F4B414'], ['TANTO FAZ', '#6FB487']] },
      table: { label: ['EPISÓDIOS', 'DO TUBO'], value: '3', note: ['Mundial +', '2 especiais'] } },
    { de: 17, ch: 12, canal: 'A SEMANA · META EM CURTO', img: 'cards/v18_taca.png',
      cred: 'Na TV: comentário de @preconautamtg; dados da Taça Preconauta 2x2 (Meta em Curto ESP02).',
      meter: { title: 'QUEM COMEÇA', value: '66%', fill: 0.66, calc: ['jogo 1', 'Taça Preconauta', 'ESP02'], levels: [['SEMPRE', '#FF5A4E'], ['QUASE', '#F4B414'], ['TANTO FAZ', '#6FB487']] },
      table: null },
    { de: 18, ch: 13, canal: 'A SEMANA · EXPEDIÇÃO', img: 'cards/v19_nauctis.png',
      cred: 'Na TV: Calmwater Mentor (NAU 5, arte Danny Schwartz) e Abyssal Lotus (NAU 234, arte Sarah Finnigan).<br>© Wizards of the Coast. Conteúdo de fã não oficial.',
      meter: { title: 'PROFUNDIDADE', value: 'FUNDO', fill: 0.9, calc: ['3 camadas', '6 espécies', 'EX-01'], levels: [['ABISMO', '#FF5A4E'], ['MEIO', '#F4B414'], ['RASO', '#6FB487']] },
      table: { label: ['NO FUNDO', 'DO MAR'], value: 'LOTUS', note: ['Nauctis:', 'The Sunken Realm'] } },
    { de: 19, ch: 14, canal: 'A SEMANA · EXPEDIÇÃO', img: 'cards/v20_lotus.png',
      cred: 'Na TV: Abyssal Lotus (Nauctis: The Sunken Realm), nº 234. Arte: Sarah Finnigan.<br>© Wizards of the Coast. Conteúdo de fã não oficial.',
      meter: { title: 'PROFUNDIDADE', value: 'FUNDO', fill: 0.9, calc: ['3 camadas', '6 espécies', 'EX-01'], levels: [['ABISMO', '#FF5A4E'], ['MEIO', '#F4B414'], ['RASO', '#6FB487']] },
      table: null },
    { de: 20, ch: 15, canal: '3 · MUNDIAL', img: 'cards/v21_jund.png',
      cred: 'Na TV: Biotech Specialist (Edge of Eternities 214, Alexandre Honoré) e The Sackville-Bagginses (The Hobbit 83, Denman Rooke).<br>© Wizards of the Coast. Conteúdo de fã não oficial.',
      meter: { title: 'GRAU DE CERTEZA', value: '3/5', fill: 0.6, calc: ['previsão', 'Meta em Curto', 'EP07'], levels: [['ALTA', '#FF5A4E'], ['MÉDIA', '#F4B414'], ['BAIXA', '#6FB487']] },
      table: { label: ['PRESTAÇÃO', 'DE CONTAS'], value: '16/11', note: ['segunda', 'Meta em Curto'] } },
    { de: 21, ch: 16, canal: '3 · MUNDIAL', img: 'cards/v22_contas.png',
      cred: 'Na TV: o TUBO. Previsão registrada no Meta em Curto EP07.',
      meter: { title: 'GRAU DE CERTEZA', value: '3/5', fill: 0.6, calc: ['previsão', 'Meta em Curto', 'EP07'], levels: [['ALTA', '#FF5A4E'], ['MÉDIA', '#F4B414'], ['BAIXA', '#6FB487']] },
      table: { label: ['PRESTAÇÃO', 'DE CONTAS'], value: '16/11', note: ['segunda', 'Meta em Curto'] } },
    { de: 22, ch: 17, canal: 'COMENTA 1, 2 OU 3', img: 'cards/v23_comenta.png',
      cred: 'Imagens: divulgação Burger King × Magic; Netflix; Biotech Specialist (EOE 214). © Wizards of the Coast. Conteúdo de fã não oficial.',
      meter: { title: 'NOTÍCIAS', value: '3', fill: 0.6, calc: ['semana', '09 a 15/11', 'na legenda'], levels: [['QUENTE', '#FF5A4E'], ['MORNA', '#F4B414'], ['FRIA', '#6FB487']] },
      table: null },
  ],
  tv: {
    channel: 'TV SAL', clock: '15:11',
    meter: { title: 'NOTÍCIAS', value: '3', fill: 0.6, calc: ['semana', '09 a 15/11', 'na legenda'], levels: [['QUENTE', '#FF5A4E'], ['MORNA', '#F4B414'], ['FRIA', '#6FB487']] },
    table: null,
    news: [
      'URGENTE: lanche de Magic com deck box, só na Itália',
      'Torneio do lanche: final dia 27/11, em Milão',
      'PLANESWALKER: série de Magic na Netflix em 2027',
      'Torneio do lanche em 9 restaurantes da Itália',
      'Mundial 32: decisão hoje, em Atlanta',
      'Sofá tenta pedir deck box no delivery; não tem',
      'Nesta semana: Numot, Lêmure, TUBO em dobro e Nauctis',
      'Próximo plantão: segunda, o TUBO presta contas',
    ],
  },
};
