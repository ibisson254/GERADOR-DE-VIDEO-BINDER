// Pregão Magic · Brutal Bass Edition · dados do episódio (PREGAO-EP01, 13/11/2026)
// Todos os números vêm da ficha de verificação (fontes.md). Nada aqui é estimado à mão,
// exceto as conversões para reais, feitas com o câmbio indicado em CAMBIO.
const CAMBIO = { taxa: 5.5606, rotulo: "dólar BCB 11/11/2026: R$ 5,5606" };
const EP = {
  data: "13/11/2026",
  cartas: "../cartas/",
  // marcas musicais medidas em MUSIC_MAP.md (Auction of Power, 112,3 BPM)
  m: { lift: 7.007, drop1: 13.72, hit2: 20.631, brk: 26.55, drop2: 27.487,
       c1: 34.348, c2: 36.055, c3: 37.773, c4: 39.486, fim: 41.198 },
  fontes: {
    stocks: "MTGStocks · Weekly Winners 2026-46 · 13/11/2026 · preço TCGplayer",
    gold: "MTGGoldfish · variação semanal (papel) · 13/11/2026, 15:46 UTC",
  },
  urza:   { k:"urza", nome:"Urza, Chief Artificer", ed:"The Brothers' War Commander", n:"2", arte:"Bartłomiej Gaweł", usd:14.70, pct:+104, fonte:"stocks" },
  uchu:   { k:"uchuulon", nome:"Uchuulon", ed:"Commander Legends: Battle for Baldur's Gate", n:"673", arte:"Sam Burley", usd:9.95, pct:+48, fonte:"stocks" },
  picard: { k:"picard", nome:"Captain Jean-Luc Picard", ed:"Star Trek", n:"7", arte:"Anna Pavleeva", usd:8.99, pct:-46, fonte:"gold" },
  ogt:    { k:"overgrown", nome:"Overgrown Tomb", ed:"Star Trek", n:"289", arte:"Pavel Kolomeyets", usd:6.99, pct:-50, fonte:"gold" },
  wg:     { k:"watery", nome:"Watery Grave", ed:"Star Trek", n:"306", arte:"Raymond Bonilla", usd:8.16, pct:+44, fonte:"gold" },
  parede: ["urza","overgrown","uchuulon","hallowed","picard","watery","blood","steam","breeding","sacred","godless","temple","stomping","urza","watery","picard"],
  shocks: ["hallowed","watery","blood","stomping","temple","godless","overgrown","steam","sacred","breeding"],
};
