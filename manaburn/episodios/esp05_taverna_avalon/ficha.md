# Ficha · Mana & Burn · Especial · «A Nova Aliança» (parceria BINDER × Taverna de Avalon)

## Identificação
- ID editorial: MB-ESP05 (o prompt pedia «reservar o ID correto»; MB-ESP04 já é o especial «Precon em jogo», publicado)
- Estado no registo: CONCLUÍDO (à espera de publicação pelo fundador)
- Aprovação do fundador: «PROMPT DE ENGENHARIA AVANÇADA — ESPECIAL BINDER × TAVERNA DE AVALON» (projeto claude.ai, 26/11/2026 23:42), com a alteração da mesma noite: «use a imagem que te enviei de uma taverna para servir de cenário, use a logo da Avalon da melhor forma possível» e «Pode usar essa imagem mesmo que tenha uma marca d'água, prossiga» (23:46). Pedido de mais informação sobre a loja (27/11, cartão da sessão) e **vozes autorizadas** no cartão seguinte («Autorizo (~970 créditos)»), uma geração por personagem.

## Classificação
- Frente: Mana & Burn · **especial pontual de parceria** (constituição §14). Não é episódio regular nem mudança permanente da série.
- Exceções pontuais (registadas em `nucleo/DECISOES.md`, 27/11/2026): cenário de taverna em vez da sala; figurinos (Burn guerreiro, Mana mago); fecho com «Estamos juntos!» / «Juntos!» em vez da pergunta + «Comenta aí» (a pergunta vai para o comentário fixado); sem TV SAL nem carta.
- Estratégia: verificação rápida com data (dados públicos do MTGDC500).

## Originalidade
- `python3 comum/ferramentas/memoria.py pauta --objeto "Taverna de Avalon" --tema "especial de parceria com loja (Mana & Burn na taverna)"` → **BLOQUEADA** por semelhança de palavras com MB-ESP04 («burn, especial, mana»: o nome da série). Falso positivo: MB-ESP04 trata de precons sem alteração. Avançou por pedido expresso do fundador, registado em `nucleo/DECISOES.md` (27/11/2026).
- Nenhuma linha do registo com Taverna de Avalon, Maricá ou CLM. Relações: MB-ESP04 (outro especial com comunidade); `nucleo/auditorias/2026-11-16_parcerias.md` (a «Taverna De Avalon» aparecia só como nome no DC500).

## Pesquisa
- Fonte principal: MTGDC500. A página da loja responde 401 ao agente (fetch e navegador, 27/11/2026); os quatro números vêm do prompt do fundador (consulta de 26/11/2026). A lista geral de torneios do mesmo site abriu e confirma as etapas 1–6 da CLM15 e a Final Interlojas Duel Commander 500 (28/10/2025). Detalhe em `fontes.md`.
- Pesquisa web sobre a loja (endereço, data de abertura, formatos): sem resultados úteis (27/11/2026). Nada disso entra no vídeo.

## Gancho visual (7 campos)
1. Quadro 0: Mana (chapéu e manto de mago) e Burn (armadura) lado a lado na taverna, estandarte da Taverna de Avalon legível na parede, título «A NOVA ALIANÇA».
2. Objeto: a logo da Taverna de Avalon (original, sem alteração).
3. Legível sem som: título + logo + figurinos dizem «especial medieval com uma loja».
4. Primeira fala: Burn aponta o estandarte: «Mana, essa taverna já tem história!»
5. Número cedo: 20 torneios aos ~4 s.
6. Mudança visual ≤ 3 s: título → 4 plaquinhas → grande plano → pergaminho → grande planos → aproximação ao estandarte → brinde. Exceções: fala 6 (5,6 s, grande plano do Mana com legenda paginada) e fala 10 (4,7 s, agradecimento).
7. Recompensa: o selo «× BINDER Vision · parceira oficial de apoio» ao lado do estandarte.

## Roteiro definitivo
Roteiro-base do fundador, com estas mudanças técnicas: «por lá» → «por aqui» (eles estão dentro da taverna); duas falas novas sobre a loja (pedido do fundador de 27/11: «um pouco mais de informações sobre a loja»); «Juntos!» do Mana no fim, porque o motor exige o mesmo número de falas para os dois. A fala de abertura na sala (v2 do prompt) foi cortada, como o prompt permitia.

| # | Quem | Fala | Plano |
|---|---|---|---|
| 1 | B | Mana, essa taverna já tem história! | geral, aponta o estandarte, título |
| 2 | M | E números também! São 20 torneios registrados, 162 jogadores, 134 decks e 49 comandantes diferentes! | geral, 4 plaquinhas |
| 3 | B | Então já aconteceu muita batalha por aqui! | grande plano Burn, caneca no ar |
| 4 | M | Muita! Teve etapa da CLM, Top 8… e até a Final Interlojas de Duel Commander! | geral, pergaminho |
| 5 | B | Uma taverna de campeões, então! | grande plano Burn |
| 6 | M | A Taverna de Avalon já construiu sua história na comunidade de Magic em Maricá. E agora o BINDER chega pra somar! | grande plano Mana |
| 7 | B | Então essa aliança está oficialmente forjada! | grande plano Burn, aponta a câmara |
| 8 | M | Está! A Taverna de Avalon agora é parceira oficial de apoio do BINDER! | aproximação ao estandarte (1,5 s) + selo |
| 9 | B | Que venham muitos outros duelos! | geral, brinde |
| 10 | M | Taverna de Avalon, muito obrigado pela confiança e pelo apoio. É uma honra caminhar com vocês! | grande plano Mana |
| 11 | B | Estamos juntos! | geral |
| 12 | M | Juntos! | geral → fecho |

## Fontes e evidências
`fontes.md` (o que foi e o que não foi reconferido).

## Produção
- Motor: kit do Mana & Burn (`manaburn/index.html`, `process.py`, `render.py`), numa **cópia** adaptada por `ferramentas/patch_taverna.py` (o kit da série não foi alterado). Cenário e estandarte por `ferramentas/assets.py` (escala uniforme da imagem 675×900 para 1080×1440; faixas de cima, de baixo e laterais com espelho desfocado e escurecido da própria imagem, sem IA). Capa: `ferramentas/capa.html`.
- Figurinos desenhados no mesmo traço SVG dos modelos (rosto, proporções e posições intactos): Burn com malha, peitoral, gorjal, ombreiras, calção de couro e caneca; Mana com chapéu de mago, manto azul com estrelas e cinto, pergaminho.
- Luz: filtro quente nos personagens e sombras de contacto no banco; estandarte com vinheta e brilho de vela.
- Vozes: ElevenLabs eleven_v4, flow «Mana & Burn — MB-ESP05 (A Nova Aliança · Taverna de Avalon)» (`LJA8XCyuzxP3OQcWQJAI`). Burn: Talis (`E9a8LlXPNWtyvvSoZzrb`), 331 créditos, 17,6 s. Mana: Erik (`nfiLpQ54jEQninp3nNqL`), 638 créditos, 37,6 s. **Total 969 créditos**, uma geração cada. Faixas em `faixas_elevenlabs.txt`; corte pelo `tts` (`processar_vozes.py`).
- Trilha e efeitos: os da série (midnight_throttle; som de destaque nas plaquinhas, no pergaminho e no selo). Sem som de TV.
- Para refazer: pasta de trabalho com o kit + `episode.*` desta pasta + `taverna_916_largo.jpg`/`estandarte.png` gerados por `assets.py` a partir dos ficheiros do fundador; `patch_taverna.py index.html`; `processar_vozes.py burn.mp3 mana.mp3`; `render.py`; `juntar_fecho.py kit.mp4 comum/outro/outro_binder_916.mp4 final.mp4`.

## Controlo de qualidade
- `qc_video.py --frente manaburn`: 1080×1920, 30 fps, 47,07 s (43,20 s + fecho), −14,3 LUFS, pico −1,1 dBTP, fecho presente, **sem problemas mensuráveis**.
- Conferência a olho da folha de contacto (1 quadro/s): legendas fora da coluna de botões; estandarte deslocado para dentro da zona segura (1.ª versão invadia a coluna da direita: corrigido); plaquinhas sem tapar rostos nem a logo; legenda «JOGADORES REGISTRADOS» numa linha (corrigido); planos aproximados sem bordas pretas (fundo alargado: corrigido); cortes das vozes alinhados com as pausas da faixa.
- Limitações aceites: a marca d'água do banco de imagens é visível ao centro do cenário (decisão do fundador); nos grandes planos do Burn o estandarte aparece cortado no canto superior direito; os quatro números e o Top 8 da CLM17 não foram reconferidos pela sessão (401).

## Ficheiros finais
- Vídeo: `MB_ESP05_A_Nova_Alianca_916.mp4` (47,07 s) e capa `MB_ESP05_CAPA.jpg`, entregues na conversa do projeto claude.ai a 27/11/2026. Não versionados (regra do estúdio; o cenário tem imagem de terceiros sem licença).

## Pacote de publicação
`legenda.txt`, `comentario_fixado.txt`, `texto_alternativo.txt`, `fontes.md`. Publicar com `utm_campaign=MB-ESP05`. Collab com a loja só se o fundador a convidar.

## Encerramento
- Registo, histórico, decisão e STATUS atualizados nesta sessão.
- Antes de publicar (fundador): decidir se publica com a marca d'água ou compra a licença da imagem (troca sem nova voz: `assets.py` + `render.py` + `juntar_fecho.py`, 0 créditos).

## Handoff
```
HANDOFF · 27/11/2026 00h30 · Claude
Repositório: ibisson254/GERADOR-DE-VIDEO-BINDER · branch main · último commit 33ae1ce (conferido no remoto: sim; workflow validar verde)

Objetivo atual: especial de parceria MB-ESP05 pronto para o fundador publicar.

Conteúdos tocados (comum/REGISTRO_EDITORIAL.md):
- MB-ESP05 · (novo) → CONCLUÍDO

Encerramento:
- MB-ESP05 · memoria.py encerramento: OK
- Vídeo e capa finais: MB_ESP05_A_Nova_Alianca_916.mp4 e MB_ESP05_CAPA.jpg, entregues na conversa do projeto claude.ai (não versionados)

Decisões tomadas nesta sessão:
- Exceções pontuais do especial (cenário, figurinos, fecho) e uso da imagem com marca d'água (registadas em nucleo/DECISOES.md? sim)

Documentos consultados:
- AGENTS.md, STATUS.md, manaburn/LEIA-ME.md, manaburn/PERFIL.md, nucleo/auditorias/2026-11-16_parcerias.md, nucleo/modelos/HANDOFF.md, manaburn/episodios/ep19_robo_imortal/

Alterações realizadas:
- manaburn/episodios/esp05_taverna_avalon/ · pacote completo · commit 33ae1ce
- comum/REGISTRO_EDITORIAL.md, comum/historico.md, nucleo/DECISOES.md, STATUS.md · commit 33ae1ce

Insights (domingo): não se aplica

Tarefas pendentes:
- Publicar com utm_campaign=MB-ESP05 · depende do fundador
- Decidir marca d'água vs licença da imagem (re-render 0 créditos) · depende do fundador
- Reconferir os 4 números e o Top 8 CLM17 no MTGDC500 (a página da loja recusa o agente: 401) · depende do fundador

Próximo passo concreto: fundador escuta o MP4 e publica, ou pede a troca da imagem licenciada.
```
