// MB-EP15 · O gato dos 40 · Felidar Sovereign: vence na sua manutenção com 40 de vida, e o Commander começa com 40.
// Factos: Oracle e ruling oficial (25/08/2015) no Scryfall; vida inicial 40 (Regras Completas 903.7). Ficha: episodios/ep15_felidar/ficha.md.
// Kit v2 + sala v3 + quadro do Conde (kit/v3, padrão desde 21/11/2026). Uma tela da TV SAL por fala (EP.canais) ou insert nos cuB.
// pose por fala: [Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano]
const CR = '© Wizards of the Coast. Conteúdo de fã não oficial.';
const FEL = 'Na TV: Felidar Sovereign (Foundations Jumpstart, 2024), nº 198. Arte: Zoltan Boros & Gabor Szikszai.<br>' + CR;
const RUL = 'Na TV: ruling oficial do Felidar Sovereign (Wizards, 25/08/2015, via Scryfall).<br>' + CR;
const VIDA = (v, fill) => ({ title: 'SUA VIDA', value: String(v), fill, calc: ['exemplo', 'início: 40', 'regra 903.7'],
                             levels: [['VENCE', '#6FB487'], ['40', '#F4B414'], ['NÃO', '#FF5A4E']] });
const V40 = VIDA(40, 0.8), V38 = VIDA(38, 0.76), V39 = VIDA(39, 0.78), V44 = VIDA(44, 0.88);
// linhas de texto medidas no PNG j25/198 (744x1040), 21/11/2026
const HL_UPKEEP = [[0.080, 0.800, 0.810, 0.042], [0.080, 0.837, 0.760, 0.040], [0.080, 0.874, 0.230, 0.036]];
const HL_KEYW = [[0.080, 0.636, 0.830, 0.042], [0.080, 0.678, 0.340, 0.036], [0.080, 0.718, 0.840, 0.042], [0.080, 0.755, 0.810, 0.042]];
const EP = {
  id: 'ep15_felidar',
  bug: 'TV SAL',
  poster: 'dragao',
  fx: { foco: true, tremor: true, poster: true, celular: true, scanner: false, tv_ligada: true },
  outro: { assinatura: 'Escaneie suas cartas e organize sua coleção.' },
  card: { img: 'cards/s01_quarenta.png', cred: FEL },
  // abertura de carta (padrão desde 21/11/2026): o Felidar inteiro em grande no quadro 0, com a linha da vitória destacada
  // e o selo do gancho; sai para dentro da TV quando o Burn acaba de dizer «40 de vida» (46 % da fala 1)
  abertura: { img: 'cards/felidar.png', ate: 0.46, hl: HL_UPKEEP, selo: { txt: '40 = VITÓRIA', x: 0.07, y: 0.44, rot: -6, size: 58 } },
  pose: [
    ['point_tv', 'rest', 'tv', 'other', 'angry', 'flat', 'tv'],      // 1 B ganha com 40, começa com 40 (quadro 0: carta + 40)
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],        // 2 M Lê a carta: manutenção destacada; custo 6
    ['point_cam', 'rest', 'cam', 'other', 'up', 'flat', 'cuB'],      // 3 B turno 6, ganho no 7 (insert)
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tv'],        // 4 M a mesa inteira joga antes
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],     // 5 B Oloro, 38 vira 40 (insert)
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],        // 6 M ruling: nem dispara
    ['shrug', 'rest', 'other', 'other', 'up', 'flat', 'wide'],       // 7 B disparou? já era
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],        // 8 M ruling: confere de novo; −1
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],     // 9 B UM PONTO?! (insert, tremor)
    ['point_tv', 'finger', 'left', 'x', 'normal', 'x', 'tvtext'],    // 10 M vigilância e vínculo (destacados)
    ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],     // 11 B a mesa tem que me bater (insert: placar)
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tv'],            // 12 M manutenção, 40, vitória (pagamento)
    ['point_cam', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],   // 13 B pergunta A/B (insert)
    ['rest', 'remote', 'other', 'cam', 'normal', 'up', 'cuM'],       // 14 M Comenta aí (TV desliga)
  ],
  // Conde de Manaforte na parede (padrão desde 21/11/2026): uma expressão por fala; só muda no início de cada plano
  quadroDir: 'kit/v3/conde/',
  quadro: ['neutro', 'neutro', 'desconfiado', 'desconfiado', 'indignado', 'desconfiado', 'admirado', 'admirado',
           'indignado', 'admirado', 'indignado', 'admirado', 'neutro', 'neutro'],
  inserts: [
    { file: 'cards/i03_turno.png', line: 2, at: 0.05, until: 3, cred: 'Um terreno por turno, sem aceleração. Felidar Sovereign (J25 198).' },
    { file: 'cards/i05_oloro.png', line: 4, at: 0.05, until: 5, cred: 'Oloro, Ageless Ascetic (Commander 2013, nº 203, arte Eric Deschamps).' },
    { file: 'cards/i05_oloro_b.png', line: 4, at: 0.5, until: 5, cred: 'Oloro, Ageless Ascetic (Commander 2013, nº 203, arte Eric Deschamps).' },
    { file: 'cards/i09_um.png', line: 8, at: 0.05, until: 9, cred: 'Ruling oficial do Felidar Sovereign (Wizards, 25/08/2015).' },
    { file: 'cards/i11_mesa.png', line: 10, at: 0.05, until: 11, cred: 'Para parar o Felidar: baixar sua vida, tirar o gato ou 1 ponto em resposta (cravado em 40).' },
    { file: 'cards/s13_ab.png', line: 12, at: 0.05, until: 13, cred: 'Felidar Sovereign (J25 198, arte Zoltan Boros & Gabor Szikszai).' },
  ],
  canais: [
    { de: 0, ch: 4, canal: 'O GATO DOS 40', img: 'cards/s01_quarenta.png', meio: { at: 0.65, img: 'cards/s01_quarenta_b.png' }, cred: FEL, meter: V40, table: null },
    { de: 1, ch: 6, canal: 'LÊ A CARTA', img: 'cards/felidar.png', meio: { at: 0.55, img: 'cards/c02_custo.png' }, cred: FEL,
      hl: { tvtext: { rects: HL_UPKEEP, zoom: 1.5 } }, meter: V40, table: null },
    { de: 3, ch: 9, canal: 'UMA VOLTA', img: 'cards/s04_mesa.png', meio: { at: 0.5, img: 'cards/s04_mesa_b.png' },
      cred: 'Na TV: exemplo de mesa de 4. Vida inicial 40 (Regras Completas 903.7).<br>' + CR, meter: V40, table: null },
    { de: 5, ch: 15, canal: 'LÊ A RULING', img: 'cards/s06_ruling.png', meio: { at: 0.5, img: 'cards/s06_ruling_b.png' }, cred: RUL,
      hl: { tvtext: { rects: [[0.083, 0.515, 0.834, 0.063], [0.083, 0.590, 0.834, 0.063]], zoom: 1.5 } }, meter: V38, table: null },
    { de: 6, ch: 20, canal: 'NA PILHA', img: 'cards/s07_gatilho.png', cred: FEL, meter: V40, table: null },
    { de: 7, ch: 25, canal: 'LÊ A RULING', img: 'cards/s08_ruling2.png', meio: { at: 0.5, img: 'cards/s08_ruling2_b.png' }, cred: RUL,
      hl: { tvtext: { rects: [[0.083, 0.440, 0.834, 0.063], [0.083, 0.515, 0.834, 0.063]], zoom: 1.5 } }, meter: V39, table: null },
    { de: 9, ch: 30, canal: 'LÊ A CARTA', img: 'cards/felidar.png', meio: { at: 0.5, img: 'cards/c10_vida.png' }, cred: FEL,
      hl: { tvtext: { rects: HL_KEYW, zoom: 1.5 } }, meter: V44, table: null },
    { de: 11, ch: 40, canal: 'SUA MANUTENÇÃO', img: 'cards/s12_vitoria.png', meio: { at: 0.62, img: 'cards/s12_vitoria_b.png' }, cred: FEL, meter: V40,
      table: { label: ['JOGADORES', 'PUTOS'], value: '3', note: ['de 3'] } },
  ],
  tv: {
    channel: 'TV SAL', clock: '20:40',   // easter egg: os 20 de vida para que o Felidar foi feito e os 40 do Commander
    meter: V40, table: null,
    news: [
      'PLANTÃO: gato de 2009 descobre que o Commander começa com 40',
      'Mesa pacifista convocada para reunião de emergência',
      'Pinger de 1 de dano é promovido a herói da mesa',
      'O «se» confere duas vezes, igual mãe na porta',
      'Vigilância: o gato bate e continua de guarda',
      'Two-Headed Giant: a vida é da dupla, diz a ruling',
      'Plantão anterior: 97 terrenos e vitória no turno 5',
    ],
  },
};
