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

## Regras que valem para todo episódio

- Carta real, inteira, rodapé visível, nada por cima. Crédito: "Na TV: {carta} ({coleção}, {ano}), nº {n}. Arte: {artista}. © Wizards of the Coast."
- A tela inteira da TV cabe sempre na largura do vídeo (zoom máximo ≈1,506, margem de 10 px); `bordas.py` confere.
- Medidor só com dado real e fonte na tela. Bloco do scanner só com gravação real do app.
- Duração livre (constituição §6).
