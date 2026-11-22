// MB-EP16 v2 · versão de teste (22/11/2026) · PROPOSTA DE REVISÃO, AGUARDA APROVAÇÃO DO FUNDADOR. A v1 fica intacta em ../episode.js.
// Direção: a carta é a protagonista da prova (EP.prova: grande, inteira, por cima da sala escurecida); o Burn reage em grande plano
// sem cartas por cima do rosto (sem EP.inserts); troca de carta = flip 3D (Alexander → Rule of Law → Thousand-Year Elixir);
// mesma carta = só muda o destaque ou a aproximação ao texto. Precisa do index.html com kit/prova/patch_prova.py (opcional, retrocompatível).
// Factos: Oracle e ruling (07/10/2026) no Scryfall; Rule of Law e Thousand-Year Elixir em listas de Alexander no EDHREC (21/11/2026).
// pose por fala: [Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano]
const CR = '© Wizards of the Coast. Conteúdo de fã não oficial.';
const ALX = "Na tela: Alexander, Ship's Fool (Star Trek Commander, 2026), nº 81. Arte: Javier Charro.<br>" + CR;
const MESA = "Na tela: exemplo de mesa de 4. Alexander, Ship's Fool (TRC 81, arte Javier Charro).<br>" + CR;
const RUL = "Na tela: ruling oficial do Alexander, Ship's Fool (Wizards, 07/10/2026, via Scryfall). Exemplo: Swords to Plowshares (TRC 429, arte Pablo Mendoza).<br>" + CR;
const STP = 'Na tela: Swords to Plowshares (Star Trek Commander, 2026), nº 429. Arte: Pablo Mendoza. Exemplo de remoção.<br>' + CR;
const ROL = 'Na tela: Rule of Law (Core Set 2020), nº 35. Arte: Scott M. Fischer. Em listas de Alexander no EDHREC (21/11/2026).<br>' + CR;
const ELX = 'Na tela: Thousand-Year Elixir (Commander 2021), nº 271. Arte: Richard Sardinha. Exemplo de efeito de desvirar.<br>' + CR;
const M4 = { title: 'COMPRAM', value: '4', fill: 0.8, calc: ['mesa de 4', '1 por jogador', 'Oracle TRC 81'],
             levels: [['TODOS', '#6FB487'], ['4', '#F4B414'], ['1 APANHA', '#FF5A4E']] };
// linhas de texto medidas nos PNG do Scryfall (744x1040), 22/11/2026
const HL_REVEAL = [[0.072, 0.673, 0.81, 0.068]];   // um bloco por frase: caixas sobrepostas cortavam o texto na aproximação (2.ª auditoria)
const HL_DANO = [[0.072, 0.738, 0.84, 0.100]];
const HL_ROL = [[0.075, 0.668, 0.835, 0.036], [0.075, 0.704, 0.36, 0.036]];
const HL_ELX = [[0.075, 0.748, 0.62, 0.036]];
const TXT_ALX = [0.06, 0.63, 0.88, 0.24], TXT_ROL = [0.06, 0.64, 0.88, 0.12], TXT_ELX = [0.06, 0.63, 0.88, 0.16];
const EP = {
  id: 'ep16_alexander_v2',
  bug: 'TV SAL',
  poster: 'dragao',
  fx: { foco: true, tremor: true, poster: true, celular: true, scanner: false, tv_ligada: true },
  outro: { assinatura: 'Escaneie suas cartas e organize sua coleção.' },
  card: { img: 'cards/t01_mesa.png', cred: MESA },
  abertura: { img: 'cards/alexander.png', ate: 0.36, hl: HL_REVEAL, selo: { txt: '4 COMPRAM', x: 0.07, y: 0.12, rot: -6, size: 58 } },
  legenda_paginas: 58,   // fala longa em duas páginas de até 2 linhas (patch_prova.py)
  prova: { w: 620, top: 330, segs: [
    { fala: 1, de: 0, img: 'cards/alexander.png', hl: HL_REVEAL, zoom: { de: 0.45, alvo: TXT_ALX, s: 1.6 }, faixa: 'CADA JOGADOR REVELA E COMPRA' },
    { fala: 3, de: 0, img: 'cards/alexander.png', hl: HL_DANO, zoom: { de: 0.12, alvo: TXT_ALX, s: 1.6 }, faixa: 'DANO = MAIOR VALOR DE MANA' },
    { fala: 3, de: 0.55, img: 'cards/t04_dano.png', tipo: 'tela' },
    { fala: 4, de: 0.45, img: 'cards/swords.png', faixa: 'EXEMPLO DE REMOÇÃO' },
    { fala: 5, de: 0, img: 'cards/t06_ruling.png', tipo: 'tela' },
    { fala: 5, de: 0.58, img: 'cards/t06_mesa.png', tipo: 'tela' },
    { fala: 7, de: 0, img: 'cards/rule_of_law.png', hl: HL_ROL, zoom: { de: 0.5, alvo: TXT_ROL, s: 1.6 }, faixa: '1 MÁGICA POR TURNO · CADA JOGADOR' },
    { fala: 9, de: 0, img: 'cards/elixir.png', hl: HL_ELX, zoom: { de: 0.22, alvo: TXT_ELX, s: 1.6 }, faixa: 'EXEMPLO DE EFEITO DE DESVIRAR' },
    { fala: 9, de: 0.6, img: 'cards/t10_desvira.png', tipo: 'tela' },
  ] },
  pose: [
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'tv'],      // 1 B quatro compram (abertura → TV: mesa de 4)
    ['rest', 'finger', 'other', 'x', 'normal', 'x', 'tv'],           // 2 M Lê a carta (prova: Alexander)
    ['arms_up', 'rest', 'cam', 'other', 'up', 'flat', 'cuB'],        // 3 B group hug? (rosto)
    ['rest', 'finger', 'other', 'x', 'normal', 'x', 'tv'],           // 4 M valor de mana, aleatório (prova: Alexander → painel)
    ['shrug', 'rest', 'cam', 'other', 'up', 'flat', 'cuB'],          // 5 B vem pra minha mão? (rosto → prova: Swords, exemplo)
    ['rest', 'finger', 'other', 'x', 'up', 'x', 'tv'],               // 6 M ruling (prova: painéis)
    ['point_cam', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],   // 7 B conhecimento público (rosto)
    ['rest', 'finger', 'other', 'x', 'normal', 'x', 'tv'],           // 8 M Rule of Law (prova: flip)
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],     // 9 B uma só?! (rosto, tremor)
    ['rest', 'finger', 'other', 'x', 'up', 'x', 'tv'],               // 10 M não é mágica (prova: flip → painel)
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'tv'],      // 11 B ameaça com brinde + A/B (TV)
    ['rest', 'remote', 'other', 'cam', 'normal', 'up', 'cuM'],       // 12 M Comenta aí
  ],
  quadroDir: 'kit/v3/conde/',
  quadro: ['neutro', 'neutro', 'desconfiado', 'desconfiado', 'desconfiado', 'admirado', 'indignado', 'admirado',
           'indignado', 'admirado', 'neutro', 'neutro'],
  inserts: [],
  canais: [
    { de: 0, ch: 4, canal: 'MESA DE 4', img: 'cards/t01_mesa.png', cred: MESA, meter: null, table: null },
    { de: 1, ch: 6, canal: 'LÊ A CARTA', img: 'cards/alexander.png', cred: ALX, meter: null, table: null },
    { de: 4, ch: 12, canal: 'EXEMPLO', img: 'cards/swords.png', cred: STP, meter: null, table: null },
    { de: 5, ch: 15, canal: 'LÊ A RULING', img: 'cards/t06_ruling.png', cred: RUL, meter: null, table: null },
    { de: 7, ch: 25, canal: 'LÊ A CARTA', img: 'cards/rule_of_law.png', cred: ROL, meter: null, table: null },
    { de: 9, ch: 30, canal: 'NÃO É MÁGICA', img: 'cards/elixir.png', cred: ELX, meter: null, table: null },
    { de: 10, ch: 40, canal: 'E VOCÊ?', img: 'cards/t11_ab.png', meio: { at: 0.5, img: 'cards/t11_ab_b.png' }, cred: ALX, meter: null, table: null },
  ],
  tv: {
    channel: 'TV SAL', clock: '20:44',
    meter: M4, table: null,
    news: [
      'PLANTÃO: klingon distribui cartas e a mesa desconfia',
      'Sorteio de dano: mesa pede auditoria independente',
      'Remoção revelada vira assunto do bairro inteiro',
      'Rule of Law: fila única para conjurar, uma por pessoa',
      'Habilidade ativada jura que não é mágica',
      'Plantão anterior: gato ganha com 40 de vida',
    ],
  },
};
