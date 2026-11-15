// Mana & Burn · TV SAL · Giro de domingo nº 3 (semana 09–15/11/2026)
// Kit v2 do repositório (manaburn/, sala v3 com a luz no cenário). Motor de canais (EP.canais), como o Giro nº 2.
// Bloco 1: Burger King Itália × Magic. Bloco 2: Netflix PLANESWALKER + "Lê a carta" da Chandra.
// Bloco «A semana no BINDER» (publicações confirmadas pelo fundador a 15/11, 02:10): MB-EP11 Numot, CM-EP005, MC-EP07, MC-ESP01, MC-ESP02, EX-01.
// Bloco 3: Mundial 32 termina hoje; o TUBO presta contas segunda 16/11 (sem antecipar o Top 8). Fontes: fontes.md.
// Sem cuB nem push: nenhum zoom que corte a TV.
// pose por fala: [Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano]
const HL_NUMOT = [[0.100, 0.792, 0.800, 0.030], [0.100, 0.826, 0.500, 0.030]];  // «you may pay {2}{R}… up to two target lands», medido no PNG
const CR = '© Wizards of the Coast. Conteúdo de fã não oficial.';
const EP = {
  id: 'giro_2026-11-15',
  bug: 'TV SAL · GIRO DE DOMINGO',
  poster: 'artefato',
  fx: { foco: true, tremor: true, poster: true, celular: true, scanner: false },
  outro: { assinatura: 'Escaneie suas cartas e organize seus decks.' },
  card: { img: 'cards/giro_abre.png', cred: 'TV SAL · notícias de 09 a 15/11/2026. Fontes na legenda.' },
  pose: [
    ['point_tv', 'rest', 'tv', 'other', 'up', 'flat', 'tv'],  // 1 B giro de domingo
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tv2'],  // 2 M Um. Burger King (canal 1)
    ['arms_up', 'rest', 'cam', 'other', 'up', 'flat', 'wide'],  // 3 B larguei a batata
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tv2'],  // 4 M 19,90, só Itália
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'wide'],  // 5 B vem pra cá
    ['rest', 'finger', 'other', 'cam', 'normal', 'up', 'cuM'],  // 6 M Rosewater
    ['point_tv', 'x', 'screen', 'x', 'up', 'x', 'tv'],  // 7 B Dois! PLANESWALKER (canal 3)
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tv2'],  // 8 M Chandra
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'wide'],  // 9 B queimar o elenco
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],  // 10 M Lê a carta −3 (canal 4)
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'wide'],  // 11 B devia ser banido
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tv2'],  // 12 M semana no BINDER: Numot (canal 6)
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'wide'],  // 13 B dois terrenos
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],  // 14 M Lê a carta: paga 3, até dois
    ['point_tv', 'rest', 'tv', 'other', 'up', 'flat', 'wide'],  // 15 B o Conde (canal 7)
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tv2'],  // 16 M obra notável
    ['point_tv', 'rest', 'tv', 'other', 'up', 'flat', 'wide'],  // 17 B TUBO (canal 11)
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tv2'],  // 18 M 66%
    ['arms_up', 'rest', 'cam', 'other', 'up', 'flat', 'wide'],  // 19 B spoiler Nauctis (canal 9)
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tv2'],  // 20 M tem um Lotus (TV: Expedição)
    ['point_tv', 'x', 'screen', 'x', 'up', 'x', 'tv'],  // 21 B Três! Mundial (canal 10)
    ['rest', 'finger', 'other', 'cam', 'normal', 'up', 'cuM'],  // 22 M sem spoiler
    ['point_cam', 'rest', 'cam', 'other', 'angry', 'flat', 'wide'],  // 23 B Comenta 1, 2 ou 3
    ['rest', 'remote', 'other', 'cam', 'normal', 'up', 'cuM'],  // 24 M Comenta aí (TV desliga)
  ],
  inserts: [],
  canais: [
    { de: 0, ch: 8, canal: 'ABERTURA', img: 'cards/giro_abre.png', cred: 'TV SAL · notícias de 09 a 15/11/2026. Fontes na legenda.',
      meter: { title: 'NOTÍCIAS', value: '3', fill: 0.6, calc: ['semana', '09 a 15/11', 'na legenda'],
               levels: [['QUENTE', '#FF5A4E'], ['MORNA', '#F4B414'], ['FRIA', '#6FB487']] },
      table: null },
    { de: 1, ch: 1, canal: '1 · LANCHE', img: 'cards/giro_bk.png',
      cred: 'Fontes: Burger King Itália (site oficial), via Dexerto, ICv2 e MTG Rocks (10–11/11/2026).',
      meter: { title: 'PREÇO DO COMBO', value: '€19,90', fill: 0.5, calc: ['lanche + deck box', '+ 100 sleeves', 'BK Itália'],
               levels: [['CARO', '#FF5A4E'], ['JUSTO', '#F4B414'], ['BARATO', '#6FB487']] },
      table: { label: ['SÓ NA', 'ITÁLIA'], value: 'ATÉ 30/11', note: ['final do torneio:', '27/11, Milão'] } },
    { de: 6, ch: 3, canal: '2 · STREAMING', img: 'cards/giro_netflix.png',
      cred: 'Fontes: Netflix Tudum e Deadline (13/11/2026).',
      meter: { title: 'ESTREIA', value: '2027', fill: 0.3, calc: ['sem data', 'definida', 'Netflix'],
               levels: [['JÁ', '#FF5A4E'], ['LOGO', '#F4B414'], ['ESPERA', '#6FB487']] },
      table: { label: ['PROTAGONISTA', ''], value: 'CHANDRA', note: ['showrunner:', 'Terry Matalas'] } },
    { de: 9, ch: 4, canal: '2 · LÊ A CARTA', img: 'cards/giro_chandra.png',
      cred: 'Na TV: Chandra, Torch of Defiance (Kaladesh, 2016), nº 110. Arte: Magali Villeneuve.<br>' + CR,
      hl: { tvtext: { rects: [[0.050, 0.748, 0.880, 0.026], [0.120, 0.773, 0.300, 0.026]], zoom: 1.5 } },
      meter: { title: 'ALVOS DO −3', value: '1', fill: 0.1, calc: ['criatura alvo', '4 de dano', 'Oracle'],
               levels: [['ELENCO TODO', '#FF5A4E'], ['ALGUNS', '#F4B414'], ['UM SÓ', '#6FB487']] },
      table: null },
    { de: 11, ch: 6, canal: 'A SEMANA · MANA & BURN', img: 'cards/giro_numot.png',
      cred: 'Na TV: Numot, the Devastator (Commander 2011), nº 215. Arte: Dan Dos Santos. Mana & Burn EP11.<br>' + CR,
      hl: { tvtext: { rects: HL_NUMOT, zoom: 1.5 } },
      meter: { title: 'TERRENOS', value: 'ATÉ 2', fill: 0.5, calc: ['pagando', '{2}{R}', 'Oracle'],
               levels: [['TODOS', '#FF5A4E'], ['DOIS', '#F4B414'], ['NENHUM', '#6FB487']] },
      table: { label: ['NO PERFIL', 'DESDE'], value: '11/11', note: ['Mana & Burn', 'EP11'] } },
    { de: 14, ch: 7, canal: 'A SEMANA · CONDE', img: 'cards/giro_conde.png',
      cred: 'Na TV: capa do Conde de Manaforte EP005. Hyalopterous Lemure (Ice Age, 1995). Arte: Richard Thomas.<br>' + CR,
      meter: { title: 'PROCESSO Nº', value: '005', fill: 1, calc: ['Conde de', 'Manaforte', 'no perfil'],
               levels: [['NOTÁVEL', '#FF5A4E'], ['DUVIDOSO', '#F4B414'], ['ARQUIVADO', '#6FB487']] },
      table: { label: ['PARECER', 'DO CONDE'], value: 'NOTÁVEL', note: ['errou de', 'mitologia'] } },
    { de: 16, ch: 11, canal: 'A SEMANA · META EM CURTO', img: 'cards/giro_tubo.png',
      cred: 'Na TV: Meta em Curto EP07, ESP01 e ESP02, com o TUBO (BINDER Originals). Dados da Taça Preconauta (@preconautamtg).',
      meter: { title: 'QUEM COMEÇA', value: '66%', fill: 0.66, calc: ['jogo 1', 'Taça Preconauta', 'ESP02'],
               levels: [['SEMPRE', '#FF5A4E'], ['QUASE', '#F4B414'], ['TANTO FAZ', '#6FB487']] },
      table: { label: ['EPISÓDIOS', 'DO TUBO'], value: '3', note: ['Mundial +', '2 especiais'] } },
    { de: 18, ch: 9, canal: 'A SEMANA · EXPEDIÇÃO', img: 'cards/giro_nauctis.png',
      cred: 'Na TV: Expedição BINDER #01, Nauctis: Primeiro Mergulho (BINDER Originals).<br>' + CR,
      meter: { title: 'PROFUNDIDADE', value: 'FUNDO', fill: 0.9, calc: ['3 camadas', '6 espécies', 'EX-01'],
               levels: [['ABISMO', '#FF5A4E'], ['MEIO', '#F4B414'], ['RASO', '#6FB487']] },
      table: { label: ['NO FUNDO', 'DO MAR'], value: 'LOTUS', note: ['Nauctis:', 'The Sunken Realm'] } },
    { de: 20, ch: 10, canal: '3 · MUNDIAL', img: 'cards/giro_mundial.png',
      cred: 'Fontes: magic.gg (ficha do Mundial 32) e anúncios do MTG Arena (09/11/2026). Previsão: Meta em Curto EP07.',
      meter: { title: 'GRAU DE CERTEZA', value: '3/5', fill: 0.6, calc: ['previsão', 'Meta em Curto', 'EP07'],
               levels: [['ALTA', '#FF5A4E'], ['MÉDIA', '#F4B414'], ['BAIXA', '#6FB487']] },
      table: { label: ['PRESTAÇÃO', 'DE CONTAS'], value: '16/11', note: ['segunda', 'Meta em Curto'] } },
  ],
  tv: {
    channel: 'TV SAL', clock: '15:11',
    meter: { title: 'NOTÍCIAS', value: '3', fill: 0.6, calc: ['semana', '09 a 15/11', 'na legenda'],
             levels: [['QUENTE', '#FF5A4E'], ['MORNA', '#F4B414'], ['FRIA', '#6FB487']] },
    table: null,
    news: [
      'URGENTE: lanche de Magic com deck box, só na Itália',
      'Torneio do lanche: final dia 27/11, em Milão',
      'PLANESWALKER: série de Magic na Netflix em 2027',
      'Torneio do lanche em 9 restaurantes da Itália',
      'Mundial 32: decisão hoje, em Atlanta',
      'Sofá tenta pedir deck box no delivery; não tem',
      'Plantão anterior: Maya Hawke no filme de Magic',
      'Nesta semana: Numot, Lêmure, TUBO em dobro e Nauctis',
      'Próximo plantão: segunda, o TUBO presta contas',
    ],
  },
};
