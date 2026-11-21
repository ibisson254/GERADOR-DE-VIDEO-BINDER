# Mana & Burn · kit do gerador v2

Gera os Reels 9:16 (1080x1920, 30 fps) da série Mana & Burn. Identidade: bíblia no Drive ("BINDER Marketing — Série Mana & Burn"). Processo e regras: `PERFIL.md` e `nucleo/`.

**02/11/2026:** o núcleo do kit v2 (projeto claude.ai, `claude/gerador-manaburn/`, versão de 24–25/10) passou para esta pasta. A v1 (24/10) está em `extras/v1/` sem alterações. O v2 é retrocompatível: um `episode.json`/`episode.js` antigo (Ep. 1 a 4) sai igual (conferido pelo autor do v2 com o Ep. 2). O motor que gerou o Giro de domingo (01/11) foi feito noutro chat e não está aqui.

## Arquivos

- `index.html`: a cena (sala, dupla, TV, TV SAL, legendas, fecho). Lê `data.js`, `episode.js` e, se existir, `lote.js`.
- `process.py` + `cortes.py` + `trilha.py` + `sfx.py` + `roteiro.py` + `foneticos.json`: corta as faixas do ElevenLabs, monta o bate-volta, calcula os eventos (cortes para a TV, destaques, indignação do Burn, cartas citadas, zapping), mistura a -14 LUFS e gera `data.js` e `trilha_final.wav`.
- `roteiro.py`: `python3 roteiro.py episode.json` imprime as duas faixas para colar no ElevenLabs (Burn: Talis; Mana: Erik; eleven_v4), com o sanitizador fonético e números por extenso (precisa de `num2words`).
- `render.py` (MP4 + capa), `preview.py` (quadros soltos), `bordas.py` (teste de bordas quadro a quadro).
- `episodios/ep02_stasis/`: `episode.js` e `data.js` do Ep. 2 no esquema v2, para testar o kit sem gerar vozes.
- `musica.mp3` (midnight_throttle), `tv_asset.png`, `logo/`, `cards/`, `node_modules/` (fontes).

Ficaram no projeto claude.ai, sem subir: `montar.py`, `escolher_tomadas.py` + `tomadas.json`, `scryfall.py` + `scry/`, `lote.py` + `lote.json`, `testes.py`, `formatos.py`/`formatos.js`/`copys.py` (carrossel e Stories), `extrair_fecho.py`, episódios 1 e 5 a 7, zapping 01 e as legendas. A faixa `concrete_teeth.mp3` (Ep. 5 a 7) não está em nenhum dos dois.

## Esquema v2 do episode.json

```
{"schema": 2,
 "chamada": "a fada de 530%",
 "falas": [{"quem": "B", "tags": "[shouting]", "legenda": "… *530%*!"},
           {"quem": "M", "tags": "[bored]", "legenda": "…", "tts": "… [laughs] …"}],
 "gap": [...], "ins": [[linha, fração]], "music": {...}, "tempo": {"B": 1.06, "M": 1.12}, "respiro_max": 0.14,
 "mix": {"intro_db": 0, "fala_db": -14, "pausa_db": -6, "fecho_db": 0},
 "sfx": {"tv": true, "destaque": true, "carta": "flick", "raiva": true},
 "outro": {"scanner": 1.5, "hold": 0.8}}
```

As falas alternam Burn e Mana, começando pelo Burn. Na legenda, `*palavra*` fica amarela (#FFD84A).

## episode.js

`id`, `bug` (tarja), `card` (PNG e crédito), `pose` por fala (`[Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano]`; planos `tv`, `tvtext`, `tvtext2`, `tv2`, `wide`, `cuM`, `cuB`, `push`), `inserts`, `hl` (destaques medidos no PNG), `tv` (medidor, placar, manchetes), `poster`, `fx` (`foco`, `tremor`, `poster`, `celular`, `scanner`), `outro`, `canais` (zapping).

## Como rodar

Python 3 (numpy, scipy, Pillow, playwright com Chromium, num2words) e ffmpeg.

1. PNG da carta em `cards/` e `episode.js`/`episode.json` do episódio na raiz desta pasta.
2. `python3 roteiro.py` → vozes no ElevenLabs (com autorização para gastar créditos).
3. `python3 process.py burn.mp3 mana.mp3`
4. `python3 preview.py 1.5 13 16.5` e `python3 bordas.py` (tem de dizer OK).
5. `python3 render.py ManaBurn_EpN_Nome_916.mp4`
6. Fecho do scanner: `comum/outro/outro_binder_916.mp4`. Controlo de qualidade: `python3 -I ../comum/qc/qc_video.py ManaBurn_EpN_Nome_916.mp4 --frente manaburn`.

## Melhorias de 02/11/2026 (auditoria `nucleo/auditorias/2026-11-02_evolucao_visual.md`)

- Legenda com `left: 80px; right: 160px`: sai da coluna de botões do Instagram (P1-5).
- Conta e fonte do medidor da TV SAL a 20 px com contorno (eram 13 px) (P1-3/P1-4).
- Cenário completado com elementos da bíblia: ventilador de pé atrás do sofá, antena com palha de aço e paninho de crochê em cima da TV (auditoria §5).
- Já estavam no v2 e faltaram no Giro: TV a desligar até ao ponto verde da logo (P1-9) e o braço do Burn a apontar a TV nos planos de TV (P1-2); nos planos do sofá a TV fica inteira no quadro (D-1).
- Testado com o Ep. 2: `bordas.py` OK (490 quadros de TV, laterais entre 10 e 1068 px, topo a 300 px) e prévias a 1,5 · 13 · 16,5 · 22 · 30 · 36,95 · 38,3 s.

## Luz padrão (07/11/2026, `nucleo/DECISOES.md`)

- Desde a sala v3 (08/11/2026) a luz vem do próprio cenário no `index.html` (lâmpada quente, reflexo frio da TV, primeiro plano mais escuro). O `render.py` já não passa por `luz.py`; `--luz-pos` liga-o se for preciso.
- O que faz: luz quente, reflexo frio da TV, parede com menos contraste, primeiro plano mais escuro (desfoque só abaixo das legendas), vinheta leve. Não toca na tela da TV, legendas, tarja, áudio nem no fecho.
- A TV é localizada pelo logo verde da TV SAL em cada quadro. Se um episódio mudar o logo ou a sua posição, conferir a folha de contacto: sem logo, o reflexo usa a última posição conhecida.
- Vídeo de outro motor (ex.: Giro): `python3 -I luz.py ENTRADA.mp4 SAIDA.mp4 --ate <início do fecho em s>`.
- Tempo: ~0,35 s por quadro (≈ 6 min por minuto de vídeo).

## Sala v3 (08/11/2026)

Mesa de noite de Commander (decks com sleeves, cartas genéricas, d20, dados, deckboxes) subida 96 px para ficar acima das legendas no plano geral; piso de taco entre rodapé e carpete. Nunca pôr cartas reais na mesa sem crédito.

## Calendário da parede (08/11/2026)

`EP.calendario` muda o ano do calendário velho da parede (por defeito "2019"). Usado no Giro de 08/11 ("1996"), a pedido do fundador.

## Regras que valem para todo episódio

- Carta real, inteira, rodapé visível, nada por cima. Crédito: "Na TV: {carta} ({coleção}, {ano}), nº {n}. Arte: {artista}. © Wizards of the Coast."
- A tela inteira da TV cabe sempre na largura do vídeo (zoom máximo ≈1,506, margem de 10 px); `bordas.py` confere.
- Medidor só com dado real e fonte na tela. Bloco do scanner só com gravação real do app.
- Duração livre (constituição §6).

## TV acesa no quadro 0 (19/11/2026, MB-EP12)

`EP.fx.tv_ligada: true` faz a TV já estar acesa no primeiro quadro (sem a animação de ligar de 0,22 s), para o quadro 0 mostrar a carta («quadro 0 com Magic», checklist E/F). Desligada por defeito: os episódios antigos saem iguais. É o mesmo efeito que os `juntar_fecho.py` do Ep. 9 e do Giro já obtinham cortando os 7 primeiros quadros, mas sem tirar áudio. Com a flag, o `juntar_fecho.py` do episódio usa `T0 = 0` (`manaburn/episodios/ep12_money_burn/juntar_fecho.py`).

## Prévia sem voz (19/11/2026, MB-EP12)

Quando os créditos de voz não estão autorizados: `python3 previa_sem_voz.py` (cópia em `episodios/ep12_money_burn/`) corre o `process.py` sem o alterar, com cada fala em silêncio pela duração prevista (calibrada no MB-EP11) e a boca com envelope sintético. Serve para conferir ritmo, telas e QC; não se publica. Com as vozes, volta-se ao passo 3 (`process.py burn.mp3 mana.mp3`). Nesta sessão o Playwright usou o Chrome do sistema (`executable_path='/usr/bin/google-chrome'`) porque o download do Chromium falhou.


## Troca de tela a meio da fala (20/11/2026, MB-EP14)

`EP.canais[].meio = {at: 0.5, img: 'cards/<tela>_b.png'}` troca a tela da TV pela variante indicada a partir de `at` × duração da fala `de` (ex.: a mesma tela com um carimbo novo). Serve para falas longas manterem a mudança visual ≤ 3 s sem abrir outro canal. A variante deve ter a mesma grelha da tela original, para os destaques (`hl`) continuarem alinhados. As imagens `meio` são pré-carregadas antes do render (`window.READY`). Sem a chave, os episódios saem iguais.

Atenção às frações do `hl` em telas compostas com moldura (`.f{inset:18px}`): somar os 18 px da moldura à posição do elemento antes de dividir por 744 × 1040.

Corte das vozes quando a legenda mostra números em algarismos e a voz os diz por extenso: `episodios/ep14_everything/processar_vozes.py` corta pelo tamanho do `tts` (o `process.py` usa o da legenda e desalinha as falas).

## Kit v3 na `main` (21/11/2026, MB-EP15)

`kit/v3/` veio da branch `manaburn/ep10-97-terrenos` (MB-EP13) e o `index.html` já tem os ganchos aplicados (`patch_index_v3.py` não se volta a correr: recusa um `index.html` que já os tenha). Campos do `episode.js`, todos opcionais: `quadro` + `quadroDir` (retrato do Conde, **padrão** desde 21/11), `calendario` (folhinha), `pilha`, `cams`, `gancho`, `marca`, `loop`, `desliga`, `canais[].subir`. Sem eles, o episódio sai igual ao kit v2 (testado com o Ep. 9). Conferir que as trocas de expressão caem em cortes: `python3 kit/v3/check_quadro.py`. Episódio de referência com o quadro e a TV acesa no quadro 0: `episodios/ep15_felidar/`.

