// Especial · Antes da carta chegar: obrigado, Sir Patrick
// pose por bloco: [Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano] (o plano vem do data.js)
const EP = {
  card: { img: 'cards/main.png',
          cred: 'Na TV: Jean-Luc Picard, Luminary (Star Trek Commander, 2026), nº 3. Arte: Jason Pastrana.<br>© Wizards of the Coast. Star Trek © CBS. Conteúdo de fã não oficial.' },
  pose: DATA.lines.map(l => ['rest', 'rest', 'tv', 'tv', 'normal', 'flat', l.shot]),
  hl: {},
};
