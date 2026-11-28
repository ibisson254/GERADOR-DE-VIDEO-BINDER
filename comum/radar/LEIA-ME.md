# Radar Editorial Semanal

Decisão do fundador de 26/11/2026 (`nucleo/DECISOES.md`). Regra em `nucleo/SHOWRUNNER.md` §2.4 2a.

**Para que serve:** guardar a escuta da comunidade em três regiões (Brasil, Europa, EUA) **uma vez por semana**, para os episódios seguintes da mesma semana partirem dela em vez de refazerem o levantamento. Não escolhe pautas: a escolha continua no Showrunner (candidatos, ficha de 9 campos, rubrica) e na auditoria de originalidade.

## Regras

- Um ficheiro por semana ISO: `comum/radar/AAAA-Www.md` (ex.: `2026-W48.md`). Cria-o o primeiro episódio da semana; os seguintes acrescentam linhas com data.
- Cada linha tem **fonte com data** e **validade** (por defeito 7 dias; menos para notícias que mudam depressa, como anúncios de banidos e spoilers). Linha vencida não é «agora»: volta-se à fonte antes de a usar.
- Só o que foi lido na sessão. Nada de memória, nada de tendência antiga dada como atual. O que não abriu fica como limitação, não como linha.
- Dados de terceiros com fonte, data, período e amostra (constituição §4). Comentários de seguidores contam como prova de interesse, nunca como única fonte.
- A ficha do episódio cita o ficheiro do radar usado e as linhas que atualizou.
- Não se apagam semanas antigas: são o histórico do que a comunidade discutia.

## Formato v2 e varrimento (desde 28/11/2026, inteligência cultural, `nucleo/DECISOES.md`)

O radar passa a servir para **descobrir**, não só para sustentar a pauta do episódio do dia.

- **Três colunas novas:** **Categoria** (A tendência emergente · B consolidada · C oportunidade editorial · D assunto saturado · E evento com janela · F movimento cultural), **Confiança** (alta/média/baixa + porquê numa frase) e **Janela** (data até quando a oportunidade vale; «sem prazo» quando não vence). «Válido até» continua a ser a validade da *leitura*; «Janela» é a validade da *oportunidade*.
- **Varrimento mínimo de cada semana** (≤ 30 min, gratuito): pelo menos **1 linha por região** (Brasil, Europa, EUA) e **2 linhas fora de combos e torneios** (arte e artistas, colecionismo e produtos, cultura geek/crossovers). Região ou território sem nada lido fica nas Limitações, com a fonte que falhou.
- **Onde procurar** (fonte primária primeiro): anúncios e comunicados da Wizards (magic.wizards.com «Announcements»: créditos, banidos, produtos), calendário `oraculo/previsoes/calendario.yaml`, Scryfall (sets novos, campo `artist`), EDHREC, ICv2 e imprensa especializada, Reddit (r/magicTCG, r/EDH, r/mtgfinance) e Bluesky de artistas **por pesquisa ou navegador** (na cloud não abrem pela shell), Cards Realm/LigaMagic (Brasil; LigaMagic só pelo navegador do PC), lojas e ligas de Portugal (TopDeck, cEDH Stats).
- Uma linha que mereça episódio vira **oportunidade** em `comum/inteligencia/oportunidades/` (avaliação com 10 critérios e porquês). O radar não escolhe pautas.

## Modelo

```
# Radar · AAAA-Www (seg DD/MM a dom DD/MM)

| # | Região | O que se discute | Categoria | Fonte (URL) e data | Evidência (número, citação curta, amostra) | Confiança | Ligação com outras regiões | Ângulos possíveis | Frentes possíveis | Janela | Válido até | Usado em |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Brasil | | | | | | | | | | | |
| 2 | Europa (IT/ES/DE) | | | | | | | | | | | |
| 3 | EUA | | | | | | | | | | | |
| 4 | Cultura (arte, colecionismo, geek) | | | | | | | | | | | |

## Correlações da semana
- <o mesmo assunto em duas ou três regiões, um contraste ou uma causa comum, com os # das linhas>

## Limitações
- <fontes que não abriram na sessão, amostras pequenas>
```
