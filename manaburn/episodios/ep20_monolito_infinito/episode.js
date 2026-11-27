// MB-EP20 · O Monólito Infinito (27/11/2026). Basalt Monolith + Rings of Brighthearth: mana incolor infinita; Walking Ballista como finalizador (à parte do combo de 2 cartas).
// Factos: Oracle e rulings no Scryfall (27/11/2026); passo a passo no Commander Spellbook 4131-4235; contagem de decks no EDHREC (27/11/2026).
// Sem Salt nem bracket no ecrã (amostras pequenas: Salt do Spellbook 2,0 sem amostra; voto de bracket EDHREC com 15 votos). O medidor da TV mostra a conta do ciclo (Oracle), não o putômetro.
// Painéis do ciclo (cards/p1–p7) na ordem exata da pilha e da fala. Plano de prova para as leituras do Mana; TV SAL abre e fecha.
// pose por fala: [Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano]
const CR = '© Wizards of the Coast. Conteúdo de fã não oficial.';
const MON = 'Na tela: Basalt Monolith (Double Masters, 2020), nº 232. Arte: Yeong-Hao Han.<br>' + CR;
const RIN = 'Na tela: Rings of Brighthearth (Commander Legends, 2020), nº 335. Arte: Howard Lyon.<br>' + CR;
const BAL = 'Na tela: Walking Ballista (Double Masters, 2020), nº 306. Arte: Daniel Ljunggren.<br>' + CR;
const CIC = 'Na tela: Basalt Monolith (2XM 232, arte Yeong-Hao Han) e Rings of Brighthearth (CMR 335, arte Howard Lyon).<br>' + CR;
const ABQ = 'Na tela: Walking Ballista (2XM 306, arte Daniel Ljunggren) e Ulamog, the Ceaseless Hunger (CMM 5, arte Michael Komarck).<br>' + CR;
// conta do ciclo (Oracle do Basalt Monolith e do Rings of Brighthearth), não é Salt nem bracket
const SALDO = { title: 'MANA', value: '+1', fill: 1.0, calc: ['+3 −3 −2 +3', '= +1 por ciclo', 'Oracle · 27/11'],
                levels: [['∞', '#FF5A4E'], ['MUITA', '#F4B414'], ['2 MANAS', '#6FB487']] };
// linhas medidas nos PNG do Scryfall (744x1040), 27/11/2026
const HL_NAO_DESVIRA = [[0.07, 0.690, 0.86, 0.080]];   // «Basalt Monolith doesn't untap during your untap step.»
const HL_COPIA = [[0.07, 0.633, 0.86, 0.034], [0.07, 0.664, 0.86, 0.070]];  // «Whenever you activate an ability…» + «…may pay {2}. If you do, copy that ability»
const HL_PAGA = [[0.07, 0.664, 0.86, 0.070]];          // «you may pay {2}. If you do, copy that ability.»
const HL_X = [[0.80, 0.040, 0.15, 0.058], [0.07, 0.636, 0.86, 0.072]];  // custo {X}{X} + «enters … with X +1/+1 counters»
const HL_REMOVE = [[0.07, 0.802, 0.86, 0.125]];        // «Remove a +1/+1 counter…: It deals 1 damage to any target.»
const TXT_R = [0.06, 0.60, 0.88, 0.20];
const TXT_B = [0.06, 0.60, 0.88, 0.34];
const EP = {
  id: 'ep20_monolito_infinito',
  bug: 'TV SAL',
  poster: 'dragao',
  fx: { foco: true, tremor: true, poster: true, celular: true, scanner: false, tv_ligada: true },
  outro: { assinatura: 'Escaneie suas cartas e organize sua coleção.' },
  card: { img: 'cards/t00_monolito.png', cred: MON },
  abertura: { img: 'cards/monolith.png', ate: 0.3, hl: HL_NAO_DESVIRA, selo: { txt: 'MANA INFINITA', x: 0.62, y: 0.125, rot: -3, size: 36 } },
  legenda_paginas: 58,
  prova: { w: 620, top: 330, segs: [
    { fala: 1, de: 0, img: 'cards/rings.png', hl: HL_COPIA, zoom: { de: 0.35, alvo: TXT_R, s: 1.6 }, faixa: 'COPIA HABILIDADE ATIVADA' },
    { fala: 2, de: 0, img: 'cards/p1.png', tipo: 'tela' },
    { fala: 2, de: 0.5, img: 'cards/p2.png', tipo: 'tela' },
    { fala: 3, de: 0, img: 'cards/rings.png', hl: HL_PAGA, zoom: { de: 0.0, alvo: TXT_R, s: 1.6 }, faixa: 'PAGA MAIS 2 = CÓPIA' },
    { fala: 3, de: 0.5, img: 'cards/p3.png', tipo: 'tela' },
    { fala: 4, de: 0, img: 'cards/t05_ruling.png', tipo: 'tela' },
    { fala: 5, de: 0, img: 'cards/p4.png', tipo: 'tela' },
    { fala: 5, de: 0.5, img: 'cards/p5.png', tipo: 'tela' },
    { fala: 6, de: 0, img: 'cards/p5b.png', tipo: 'tela' },
    { fala: 7, de: 0, img: 'cards/p6.png', tipo: 'tela' },
    { fala: 7, de: 0.42, img: 'cards/p7.png', tipo: 'tela' },
    { fala: 7, de: 0.78, img: 'cards/p7b.png', tipo: 'tela' },
    { fala: 9, de: 0, img: 'cards/t10_incolor.png', tipo: 'tela' },
    { fala: 9, de: 0.5, img: 'cards/t10_incolor_b.png', tipo: 'tela' },
    { fala: 11, de: 0, img: 'cards/ballista.png', hl: HL_X, faixa: 'ENTRA COM X MARCADORES' },
    { fala: 11, de: 0.2, img: 'cards/ballista.png', hl: HL_REMOVE, zoom: { de: 0.0, alvo: TXT_B, s: 1.5 }, faixa: 'TIRA 1 = 1 DE DANO' },
    { fala: 11, de: 0.42, img: 'cards/t12_conta.png', tipo: 'tela' },
    { fala: 11, de: 0.62, img: 'cards/t12_vida.png', tipo: 'tela' },
    { fala: 11, de: 0.8, img: 'cards/t12_vida_b.png', tipo: 'tela' },
  ] },
  pose: [
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'tv'],      // 1 B gancho (abertura → TV)
    ['rest', 'finger', 'other', 'x', 'normal', 'x', 'tv'],           // 2 M Rings (prova: carta)
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'tv'],      // 3 B gera 3, cobra 3 (prova: painéis 1–2)
    ['rest', 'finger', 'other', 'x', 'normal', 'x', 'tv'],           // 4 M Rings copia (prova: carta → painel 3)
    ['shrug', 'rest', 'tv', 'other', 'up', 'flat', 'tv'],            // 5 B a cópia resolve primeiro? (prova: ruling)
    ['rest', 'finger', 'other', 'x', 'up', 'x', 'tv'],               // 6 M desvira e vira (prova: painéis 4–5)
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'tv'],      // 7 B a original ainda na pilha (prova: painel 5b)
    ['rest', 'finger', 'other', 'x', 'normal', 'x', 'tv'],           // 8 M resolve; saldo +1 (prova: painéis 6–7)
    ['arms_up', 'rest', 'tv', 'other', 'angry', 'flat', 'tv'],       // 9 B repete (TV: loop)
    ['rest', 'finger', 'other', 'x', 'normal', 'x', 'tv'],           // 10 M incolor; mana ≠ vitória (prova: painel)
    ['point_cam', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],   // 11 B quem transforma em dano? (rosto)
    ['rest', 'finger', 'other', 'x', 'up', 'x', 'tv'],               // 12 M Walking Ballista (prova: carta → conta → mesa)
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'tv'],      // 13 B pergunta A/B (TV)
    ['rest', 'remote', 'other', 'cam', 'normal', 'up', 'cuM'],       // 14 M Comenta aí
  ],
  quadroDir: 'kit/v3/conde/',
  quadro: ['neutro', 'admirado', 'desconfiado', 'admirado', 'desconfiado', 'admirado', 'indignado', 'admirado',
           'indignado', 'desconfiado', 'desconfiado', 'admirado', 'neutro', 'neutro'],
  inserts: [],
  canais: [
    { de: 0, ch: 3, canal: 'O MONÓLITO', img: 'cards/t00_monolito.png', meio: { at: 0.62, img: 'cards/t00_monolito_b.png' }, cred: MON, meter: null, table: null },
    { de: 1, ch: 6, canal: 'LÊ A CARTA', img: 'cards/rings.png', cred: RIN, meter: null, table: null },
    { de: 2, ch: 9, canal: 'O CICLO', img: 'cards/p1.png', meio: { at: 0.5, img: 'cards/p2.png' }, cred: CIC, meter: null, table: null },
    { de: 4, ch: 12, canal: 'RULING', img: 'cards/t05_ruling.png', cred: RIN, meter: null, table: null },
    { de: 5, ch: 13, canal: 'O CICLO', img: 'cards/p4.png', meio: { at: 0.5, img: 'cards/p5.png' }, cred: CIC, meter: null, table: null },
    { de: 8, ch: 21, canal: 'REPETE', img: 'cards/t09_loop.png', cred: CIC, meter: null, table: null },
    { de: 9, ch: 22, canal: 'INCOLOR', img: 'cards/t10_incolor.png', cred: CIC, meter: null, table: null },
    { de: 11, ch: 40, canal: 'LÊ A CARTA', img: 'cards/ballista.png', cred: BAL, meter: null, table: null },
    { de: 12, ch: 45, canal: 'E VOCÊ?', img: 'cards/t13_ab.png', meio: { at: 0.5, img: 'cards/t13_ab_b.png' }, cred: ABQ, meter: null, table: null },
  ],
  tv: {
    channel: 'TV SAL', clock: '03:32',
    meter: SALDO, table: null,
    news: [
      'PLANTÃO: monólito de basalto se recusa a acordar sozinho',
      'Anéis copiam habilidade e cobram só duas manas de taxa',
      'Pilha confirma: quem chega por último resolve primeiro',
      'Mana incolor infinita ainda não ganhou nenhum jogo sozinha',
      'Balista ambulante aceita pagamento em X dobrado',
      'Eldrazi colossal aguarda na fila da mão',
      'Plantão anterior: robô que não morre volta pra sempre',
    ],
  },
};
