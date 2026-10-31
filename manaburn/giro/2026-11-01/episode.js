// Giro de Domingo nº 1 · semana 26–31/10/2026 · o que muda por semana está todo aqui (e no guiao.json)
const GIRO = {
  bug: 'TV SAL · GIRO DE DOMINGO',
  manchete: 'MORREU O PICARD.<br>NO DIA SEGUINTE,<br>A CAIXA DELE SUBIU.',
  faixas: { n1: ['1', 'NOTÍCIA QUENTE'], n2: ['2', 'DA CASA'], n3: ['3', 'PRA VOCÊ JOGAR'], voto: ['?', 'COMENTA 1, 2 OU 3'] },
  card: { img: 'cards/main.png' },
  // destaque no texto da carta (frações do PNG 744x1040; linhas medidas: 831–863 e 868–893)
  hl: [[0.083, 0.797, 0.847, 0.034], [0.083, 0.832, 0.215, 0.028]],
  telas: {
    abre: { sub: 'SEMANA DE 26 A 31/10', cred: '' },
    n1: { kicker: 'STAR TREK · MERCADO', titulo: ['Collector Booster', 'subiu no dia seguinte'],
          linhas: ['28/10: morre Sir Patrick Stewart', 'é a única caixa com o Picard autografado', 'o set sai a 13/11'],
          fonte: 'Fonte: TheGamer (29/10/2026), preço do TCGplayer', cred: '' },
    n2: { kicker: 'WIZARDS OF THE COAST', titulo: ['Dan Ayoub', 'é o novo presidente'],
          linhas: ['ex-chefe de estúdio de Halo (343 Industries)', 'primeiro promovido de dentro da casa', 'assume a 2/11'],
          fonte: 'Fonte: Hasbro, comunicado de 27/10/2026', cred: '' },
    n3: { cred: 'Na TV: Leyline of Anticipation (Wizards Play Network 2026, promo do All Leylines\' Eve). Arte: Alexandr Leskinen.<br>© Wizards of the Coast.' },
    agenda: { itens: [['5/11', 'último dia do All Leylines\' Eve'], ['6/11', 'pré-lançamento de Star Trek'], ['10/11', 'Star Trek no MTG Arena'], ['13/11', 'Star Trek nas lojas']],
              fonte: 'Fonte: Wizards of the Coast', cred: '' },
  },
};
const EP = { card: GIRO.card };   // o kit lê EP.card
