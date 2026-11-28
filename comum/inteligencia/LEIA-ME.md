# Inteligência cultural · oportunidades editoriais

Criado a 28/11/2026 (`nucleo/DECISOES.md`; diagnóstico e desenho em `nucleo/auditorias/2026-11-28_inteligencia_cultural.md`).

**Para que serve:** decidir **se e quando** uma história merece um conteúdo do BINDER, com o raciocínio à vista. Não é um gerador de pautas: o radar (`comum/radar/`) recolhe sinais, esta pasta avalia as poucas que valem a pena, e **quem escolhe é o fundador**. A escolha entre candidatos de um mesmo episódio continua no `nucleo/SHOWRUNNER.md` §2.4 (rubrica de 7 critérios); a produção continua na ficha da frente.

## Fluxo (≤ 30 min por semana, 0 créditos)

1. **Radar** da semana (`comum/radar/LEIA-ME.md`, formato v2): categoria, confiança e janela em cada linha.
2. **Oportunidade:** uma linha do radar (ou ideia do fundador, ou reserva de uma ficha) que pareça merecer episódio vira `oportunidades/OP-AAAA-Wss-nn.yaml` (copiar um existente). Correr antes `memoria.py pauta` com o objeto central.
3. **Tabela:** `python3 comum/ferramentas/inteligencia.py oportunidades` (e `--detalhe <ID>` para ler os porquês).
4. **Fundador escolhe** uma (estado `escolhida`, nome e data em `decisao`), ou manda esperar/descartar.
5. **Proposta audiovisual** (opcional, `pilotos/<ID>_proposta.md`) → linha no registo com ID da frente → ficha → produção como sempre. Estado da oportunidade passa a `virou-pauta`.
6. **Depois de publicar:** números e atributos no `comum/insights/registo_posts.csv` (colunas de retenção desde 28/11) e, quando houver amostra, `inteligencia.py padroes`.

## A ficha de oportunidade

Campos obrigatórios (o script recusa a ficha sem eles): `id`, `titulo`, `criada`, `estado` (aberta · esperar · escolhida · descartada · virou-pauta), `categoria` (A–F, como no radar), `confianca` (nível + porquê), `frente_sugerida`, `pergunta_central`, `angulo`, `diferenca`, `porque_agora`, `publico`, `evidencias`, `verificar`, `criterios`, `marca`. Opcionais: `janela` (`ate` + `motivo`), `decisao`.

**Evidências:** cada uma com `tipo` (facto · cálculo · opinião · inferência · ausência), `fonte`, `url`, `data_publicacao` (se a página a tiver), `data_coleta` e a `evidencia` em uma frase. A **ausência de evidência** também se regista (tipo `ausência`): é informação, não buraco.

**Os 10 critérios** (missão do fundador de 28/11), cada um com `nota` 1–5 **e** `porque` (nota sem frase é recusada). 5 é sempre o melhor para o BINDER; em `custo_esforco`, 5 = barato.

| Chave | Critério |
|---|---|
| `relevancia_cultural` | Relevância cultural |
| `interesse_audiencia` | Interesse potencial da audiência (sem dados = 3, e diz-se porquê) |
| `originalidade` | Originalidade da abordagem (registo + cobertura existente) |
| `profundidade` | Profundidade narrativa |
| `potencial_visual` | Potencial visual (com objetos reais que se podem mostrar) |
| `fontes` | Disponibilidade de fontes confiáveis |
| `compartilhamento` | Potencial de compartilhamento |
| `longevidade` | Longevidade do assunto |
| `identidade_binder` | Relação com a identidade BINDER (arte, artistas, colecionismo, comunidade) |
| `custo_esforco` | Custo e esforço de produção (5 = barato) |

**Portões** (nenhuma soma compensa): identidade BINDER ≤ 2 → **FORA**; categoria D (saturado) → **FORA**; janela vencida → **FORA**; fontes ≤ 2 → **ESPERAR**. A soma (/50) só ordena dentro do mesmo veredito e aparece sempre ao lado das dez notas. Nem toda oportunidade com potencial de visualizações merece ser publicada: o portão da identidade existe para isso.

**Marca:** `valor` (o que a história constrói para a marca cultural: confiança com artistas, estética, comunidade) e `direitos` (o que se pode e não se pode mostrar). Nenhuma oportunidade comercial nasce aqui; colaborações só pelo fundador (`nucleo/auditorias/2026-11-16_parcerias.md`).

## Padrões de audiência

`python3 comum/ferramentas/inteligencia.py padroes --por tipo_abertura --metrica tempo_medio_s` (atributos: `frente`, `formato`, `tipo_abertura`, `tipo_narrativa`; métricas: as colunas numéricas do registo e `pct_assistida_calc` = tempo médio ÷ duração). Usa a leitura mais recente de cada conteúdo, separa **factos observados** de **leitura**, e abaixo de 2 grupos com n ≥ 3 diz «amostra insuficiente» sem concluir nada. Com amostra, escreve uma **hipótese** e manda testar em 3 episódios comparáveis (constituição §12). Nunca fala de causa.

Valores para os atributos (texto livre curto, sempre os mesmos): `tipo_abertura` = `objeto`, `objeto-contraste`, `numero`, `pergunta`, `personagem`, `comentario`; `tipo_narrativa` = `combo-passo-a-passo`, `torneio-reviravolta`, `documental-linha-do-tempo`, `perfil`, `noticia`, `tribunal`.

## Referências culturais (estética, design, comportamento)

Desde 28/11/2026 o fundador envia referências (Reels, posts, peças) do que a cultura BINDER deve ter. Cada uma vira `referencias/REF-AAAA-MM-DD-nn.yaml`. **Uma referência inspira um princípio; nunca se copia a peça.**

1. **Recebida:** url, data, as palavras do fundador tal como vieram, dimensões prováveis (`estetica`, `design`, `comportamento`, `ritmo`, `som`, `narrativa`, `tom`) e `nao_copiar` (o que é de terceiros). Nada mais: sem ver a peça não se escreve sobre ela.
2. **Vista:** como e quando foi vista (`vista.como`, `vista.em`) e o que se viu, só em factos (`observado`). O Instagram não abre por automação: vê-se pelo vidIQ `vidiq_watch_shortform_content` (10 créditos, só com autorização) ou pela descrição do fundador.
3. **Princípio proposto:** cada princípio tem `etiqueta` (minúsculas-com-hífens, a mesma sempre que a ideia se repete), `dimensao`, `principio` (geral, aplicável com objetos e personagens nossos), `aplicar_em` (frentes) e `teste` (como se prova em 3 episódios comparáveis, constituição §12).
4. **Regra:** `python3 comum/ferramentas/inteligencia.py referencias` marca **RECORRENTE** quando a mesma etiqueta aparece em 3 referências. Só então se propõe ao fundador; se aprovar, a regra entra em `nucleo/DECISOES.md` e no perfil da frente ou na constituição, e a ficha fica `virou-regra` com `decisao.fundador`. O script recusa `virou-regra` sem essa decisão.

Portão de identidade: uma referência que puxe para longe de arte, artistas, colecionismo e comunidade Magic/TCG fica `descartada`, com o porquê.

## Custos e limites

- 0 créditos; só PyYAML (já usado pelo ciclo do TUBO e instalado no workflow `validar`).
- O script não pesquisa: as evidências são lidas na sessão (pesquisa web, agente web-fetch, Scryfall, EDHREC). Na cloud, Reddit, YouTube, Instagram e magic.wizards.com não abrem pela shell (28/11/2026).
- Se o script falhar, os YAML leem-se à mão: a lógica está toda escrita na ficha.

## Testes

`python3 -I comum/ferramentas/test_inteligencia.py` (validação, portões, ordenação, padrões com e sem amostra).
