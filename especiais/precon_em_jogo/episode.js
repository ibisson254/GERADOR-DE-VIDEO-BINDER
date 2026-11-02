// Especial · A comunidade falou: Precon em jogo (Mana & Burn, crossover pontual). Kit v2 + esp/patch.py (opção EP.quadro, EP.comu, EP.clip).
const EP = {
  id: 'esp_precon_em_jogo',
  bug: 'ESPECIAL DA COMUNIDADE',
  fx: { foco: true, tremor: true, poster: false, celular: true, scanner: false },
  outro: { assinatura: 'Escaneie suas cartas e organize seus decks.' },
  card: { img: 'esp/slides/comu.png', cred: 'Conteúdo de fã não oficial.' },
  quadro: [[0,'neutro'],[3,'desconfiado'],[7,'indignado'],[9,'admirado'],[11,'indignado'],[15,'desconfiado'],[18,'neutro']],
  tvLogo: 'logo/binder_fabricante.png',
  clip: { t0: 0.3, n: 99 },
  subPre: [[0.3,1.6,'*TUBO:* Commander, por diversão.'],[1.6,3.7,'*TUBO:* Fora do meu arquivo, não da minha atenção.']],
  comu: [ {line:2, px:42, q:'Tem que começar a calcular os eventos que envolvem Commander Precon.'},
          {line:3, px:37, q:'1 deck em especial não. Eu digo mais em relação ao formato. Campeonatos de Magic que usam Precons como deck valendo premiação. Hj são resumidos as lojas e não aos campeonatos grandes. E premiações modestas.'} ],
  canais: [
    { de: 0, img: 'esp/clip/099.jpg', ch: 3, cred: 'Na TV: trecho original de Meta em Curto · EP03.' },
    { de: 2, img: 'esp/slides/comu.png', ch: 4, cred: 'Comentários reais de @diegoalencard no @binderthetrade.' },
    { de: 7, hl: { tvtext: { rects: [[0.046, 0.488, 0.866, 0.084]], zoom: 1 } }, img: 'esp/slides/cosmic.png', ch: 5, cred: 'Exemplo de loja. Não vale como regra geral.' },
    { de: 9, hl: { tvtext: { rects: [[0.046, 0.488, 0.672, 0.084]], zoom: 1 } }, img: 'esp/slides/laluna.png', ch: 6, cred: 'Evento de 11/04/2026. Prêmios anunciados pelo organizador.' },
    { de: 11, hl: { tvtext: { rects: [[0.046, 0.493, 0.66, 0.084]], zoom: 1 } }, img: 'esp/slides/grande.png', ch: 7, cred: 'Tix: unidade de prêmio do evento. Grade do CommandFest SP (CCG Eventos).' },
    { de: 15, hl: { tvtext: { rects: [[0.046, 0.397, 0.909, 0.16]], zoom: 1 } }, img: 'esp/slides/painel.png', ch: 8, cred: 'Commander Brackets, atualização de 21/10/2025.' },
  ],
  pose: [
    ['point_tv','x','screen','x','angry','x','tv'],              // 1 B Fora do arquivo
    ['rest','rest','other','cam','normal','flat','cuM'],          // 2 M recorte
    ['point_tv','x','screen','x','angry','x','tv2'],              // 3 B Diego (cartão 1)
    ['point_tv','x','screen','x','up','x','tv2'],                 // 4 M lê (cartão 2)
    ['arms_up','rest','cam','other','angry','flat','cuB'],        // 5 B Papo reto
    ['rest','finger','other','other','normal','up','wide'],       // 6 M regulamento
    ['shrug','rest','other','other','up','flat','wide'],          // 7 B Nem um terreno
    ['point_tv','x','screen','x','normal','x','tvtext'],              // 8 M EUA
    ['shrug','rest','other','other','angry','flat','cuB'],        // 9 B sete dólares
    ['point_tv','x','screen','x','up','x','tvtext'],                  // 10 M Espanha
    ['arms_up','rest','cam','other','up','flat','cuB'],           // 11 B Mox Diamond
    ['point_tv','x','screen','x','normal','x','tvtext'],             // 12 M Gen Con + SP
    ['arms_up','rest','other','other','angry','flat','wide'],     // 13 B Aqui no Brasil
    ['rest','chip','other','other','normal','flat','wide'],       // 14 M circuito
    ['arms_up','rest','cam','other','angry','flat','cuB'],        // 15 B banido
    ['point_tv','x','screen','x','normal','x','tvtext'],              // 16 M painel
    ['shrug','finger','other','other','up','flat','wide'],        // 17 B sorteia
    ['rest','rest','other','cam','normal','flat','cuM'],          // 18 M Valeu, Diego
    ['point_cam','rest','cam','other','angry','flat','cuB'],      // 19 B pergunta
    ['rest','remote','other','cam','normal','up','cuM'],          // 20 M Comenta aí
  ],
  inserts: [],
  hl: {},
  tv: {
    channel: 'TV SAL', clock: '02:11',
    meter: { title: 'COMENTÔMETRO', value: '100%', fill: 1, calc: ['1 comentário', 'virou 1 episódio'],
             levels: [['VIROU PAUTA', '#10B981'], ['LIDO', '#F4B414'], ['IGNORADO', '#FF5A4E']] },
    table: { label: ['DECKS', 'ALTERADOS'], value: '0 DE 4', note: ['regra da', 'caixa fechada'] },
    news: [
      'URGENTE: deck sai da caixa e dispensa upgrade',
      'Terreno básico mantém emprego graças ao regulamento',
      'Caixa de sapato pede vaga em campeonato grande',
      'Pacote de booster é o novo décimo terceiro da mesa',
      'Box League avisa: sou de booster, não me confunda',
      'Mesa de precon: ninguém disse "meu deck é nota 7"',
      'Comentário vira pauta; caixa de comentários pede aumento',
      'Mox Diamond é visto perto de deck de caixa',
    ],
  },
};
