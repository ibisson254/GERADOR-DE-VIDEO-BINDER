// EP10 · "O gato zumbi que cobra a mesa" (Olag and Miau, New Friends · Mystery Booster Commander Edition, 2026)
// Kit v2 do repositório (manaburn/). Dados conferidos a 11/11/2026 (Oracle via API Scryfall + Release Notes da Wizards).
// pose por fala: [Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano]
const EP = {
  id: 'ep10_olag',
  poster: 'dragao',
  // fecho: scanner do kit desligado; o fecho oficial (comum/outro/outro_binder_916.mp4) entra por concat, sem logo dupla.
  fx: { foco: true, tremor: true, poster: false, celular: true, scanner: false },
  outro: { assinatura: 'Escaneie suas cartas e organize seus decks.' },
  card: { img: 'cards/olag.png',
          cred: 'Na TV: Olag and Miau, New Friends (Mystery Booster Commander Edition, 2026), nº 48. Arte: Steve Argyle.<br>© Wizards of the Coast.' },
  pose: [
    ['point_tv', 'x', 'screen', 'x', 'angry', 'x', 'tv'],            // 1 B gato zumbi que cobra vida da mesa
    ['rest', 'chip', 'other', 'cam', 'normal', 'flat', 'cuM'],       // 2 M três manas, três cores, 3/3
    ['shrug', 'rest', 'cam', 'other', 'up', 'flat', 'wide'],         // 3 B Isso devia ser banido. Do sofá
    ['point_tv', 'finger', 'left', 'x', 'up', 'x', 'tvtext'],        // 4 M Lê a carta: marcadores
    ['arms_up', 'rest', 'cam', 'other', 'up', 'flat', 'push'],       // 5 B abrigo de animais do necrotério
    ['point_tv', 'finger', 'screen', 'x', 'normal', 'x', 'tvtext2'], // 6 M etapa final, virados
    ['arms_up', 'x', 'screen', 'x', 'angry', 'x', 'tv'],             // 7 B três viradas = três de cada (placar EXEMPLO)
    ['rest', 'finger', 'other', 'other', 'normal', 'up', 'cuM'],     // 8 M conta a quantidade
    ['shrug', 'rest', 'other', 'other', 'up', 'flat', 'cuB'],        // 9 B fraude no censo felino
    ['point_tv', 'x', 'screen', 'x', 'normal', 'x', 'tv'],           // 10 M conta uma vez só (Censômetro)
    ['arms_up', 'x', 'screen', 'x', 'angry', 'x', 'tv2'],            // 11 B Wand of Orcus (insert)
    ['rest', 'chip', 'other', 'cam', 'normal', 'flat', 'wide'],      // 12 M mesmo pote
    ['point_cam', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],   // 13 B pergunta A/B
    ['rest', 'remote', 'other', 'cam', 'normal', 'up', 'cuM'],       // 14 M Comenta aí. (TV desliga)
  ],
  // carta citada na fala 11: Wand of Orcus (PNG real do Scryfall, afc 297, arte estendida)
  inserts: [ { file: 'cards/wand_orcus.png', line: 10, at: 0.30, until: 11,
               cred: 'Wand of Orcus (Forgotten Realms Commander, 2021), nº 297. Arte: Andrew Mar.' } ],
  // destaques medidos no PNG 744x1040 (linhas de pixels escuros da caixa de texto), em frações da carta
  hl: {
    tvtext:  { rects: [[0.081, 0.661, 0.815, 0.030],   // "Whenever another Zombie you control enters,"
                       [0.081, 0.690, 0.828, 0.030],   // "put a +1/+1 counter on target Cat you control."
                       [0.081, 0.730, 0.814, 0.030],   // "Whenever another Cat you control enters, put"
                       [0.081, 0.758, 0.828, 0.030]],  // "a +1/+1 counter on target Zombie you control."
               zoom: 1.5 },
    tvtext2: { rects: [[0.081, 0.797, 0.696, 0.030],   // "At the beginning of your end step, each"
                       [0.081, 0.825, 0.753, 0.030],   // "opponent loses life equal to the number of"
                       [0.081, 0.853, 0.727, 0.030]],  // "tapped Cats and/or Zombies you control."
               zoom: 1.5 },
  },
  tv: {
    channel: 'TV SAL', clock: '00:48',   // easter egg: nº 48 da carta na coleção
    // sem Salt Score verificado: o medidor mostra a regra oficial (Release Notes), não uma estatística
    meter: { title: 'CENSÔMETRO', value: '1', fill: 0.5, calc: ['Gato + Zumbi', '= 1 vez só', 'Wizards'],
             levels: [['FRAUDE', '#FF5A4E'], ['DOIS TIPOS', '#F4B414'], ['UMA VEZ', '#6FB487']] },
    table: { label: ['EXEMPLO:', '3 VIRADAS'], value: '−3', note: ['de vida para', 'cada oponente'] },
    news: [
      'ALERTA: GATOS E ZUMBIS DIVIDEM O MESMO POTE',
      'SÍNDICO PEDE AVISO ANTES DO ATAQUE',
      'NOVO CONDOMÍNIO: PAGAMENTO NA ETAPA FINAL',
      'Censo felino: bicho Gato e Zumbi conta uma vez só',
      'Pet shop do necrotério abre vagas para ronronar',
      'Varinha de 2021 se oferece de babá de Zumbi',
      'Gato zumbi chega na Mystery Booster de Commander',
      'Plantão anterior: o ladrão que virou Papai Noel',
    ],
  },
};
