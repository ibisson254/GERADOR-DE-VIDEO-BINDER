// MB-ESP05 · A Nova Aliança — especial de parceria BINDER × Taverna de Avalon (26/11/2026).
// Exceção pontual de cenário (taverna em vez da sala), autorizada pelo fundador a 26/11/2026; figurinos pontuais.
// Dados: MTGDC500, página da loja Taverna De Avalon, números informados pelo fundador a 26/11/2026 (a página recusa acesso automático: 401).
// pose por fala: [Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano]
const EP = {
  id: 'esp05_taverna_avalon',
  bug: 'ESPECIAL · TAVERNA DE AVALON',
  fx: { foco: false, tremor: false, poster: false, celular: false, scanner: false, tv_ligada: true },
  outro: { assinatura: 'Escaneie suas cartas e organize sua coleção.' },
  card: { img: '', cred: '' },
  legenda_paginas: 58,
  gancho: { fala: 0, html: 'A NOVA<br>ALIANÇA' },
  placas: { fala: 1, ate: 2,
    fonte: { right: 510, y: 236, txt: 'Registros do MTGDC500 · consulta em 26/11/2026' },
    itens: [
      { at: 0.14, n: '20', r: 'TORNEIOS', x: 56, y: 280, w: 250, h: 110, rot: -2 },
      { at: 0.33, n: '162', r: 'JOGADORES REGISTRADOS', x: 320, y: 280, w: 250, h: 110, rot: 1.5 },
      { at: 0.545, n: '134', r: 'DECKS', x: 56, y: 400, w: 250, h: 110, rot: 1 },
      { at: 0.75, n: '49', r: 'COMANDANTES', x: 320, y: 400, w: 250, h: 110, rot: -1.5 } ] },
  cams: { cuM: { s: 1.42, cx: 250, cy: 650, tx: 540, ty: 920 } },
  est: { dur: 1.5, cam: { s: 1.6, cx: 740, cy: 230, tx: 540, ty: 650 } },
  selo: { fala: 7, de: 0.22 },
  pergaminho: { fala: 3, de: 0.06, x: 56, y: 236, w: 514,
    titulo: 'NA TAVERNA DE AVALON',
    linhas: ['Etapas 1 a 6 · CLM15 · set.–nov. 2025', 'Final Interlojas Duel Commander 500 · 28/10/2025', 'Top 8 · CLM17 · 20/10/2026'],
    fonte: 'Registros do MTGDC500 · consulta em 26–27/11/2026' },
  pose: [
    ['point_tv', 'rest', 'tv', 'other', 'up', 'normal', 'wide'],
    ['rest', 'finger', 'other', 'cam', 'up', 'up', 'wide'],
    ['arms_up', 'rest', 'cam', 'other', 'up', 'normal', 'cuB'],
    ['rest', 'finger', 'other', 'cam', 'up', 'up', 'wide'],
    ['arms_up', 'rest', 'cam', 'other', 'up', 'normal', 'cuB'],
    ['rest', 'finger', 'other', 'cam', 'normal', 'up', 'cuM'],
    ['point_cam', 'rest', 'cam', 'other', 'up', 'normal', 'cuB'],
    ['rest', 'finger', 'tv', 'tv', 'up', 'up', 'est'],
    ['arms_up', 'rest', 'cam', 'other', 'up', 'normal', 'wide'],
    ['rest', 'rest', 'other', 'cam', 'normal', 'normal', 'cuM'],
    ['arms_up', 'finger', 'cam', 'cam', 'up', 'up', 'wide'],
    ['arms_up', 'remote', 'cam', 'cam', 'up', 'up', 'wide']
  ]
};
