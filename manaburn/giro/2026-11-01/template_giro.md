# Template · TV SAL Giro de Domingo (Mana & Burn)

Formato fixo de domingo (21h Lisboa). Criado no nº 1 (01/11/2026). Para a próxima edição: copiar esta pasta para `manaburn/giro/AAAA-MM-DD/`, mudar só o que está em "Muda por semana" e correr os passos.

## Muda por semana
| Ficheiro | O quê |
|---|---|
| `guiao.json` | 14 falas: B abre ("TV SAL, giro de domingo…"), 3 blocos de 3–4 falas (Mana dá o facto, Burn reage), agenda (Mana), pergunta do Burn "Comenta 1, 2 ou 3" (penúltima), "Comenta aí." (Mana, última). `tts` só onde a pronúncia muda (ver `manaburn/episodios/ep09_dack/foneticos.json`). |
| `episode.js` → `GIRO` | `manchete` (0–3 s, legível sem som), `faixas` (nomes dos blocos), `telas.n1` / `n2` (kicker, título 2 linhas, 3 linhas, fonte), `telas.n3.cred` + `cards/main.png` (carta da notícia útil, PNG do Scryfall), `hl` (linha do texto que o Mana lê, medida no PNG), `telas.agenda.itens` |
| `processar.py` → `D` | plano, pose e tela de cada fala; `TEMPO_FALA` / `RESPIRO` se um bloco pedir outro ritmo (ex.: luto) |
| `legenda.txt`, `comentario_fixado.txt`, `alt_text.txt`, `ficha_de_fatos.md` | textos da semana |

## Fica fixo
- Cena: `giro.html` = desenhos do kit (`manaburn/index.html`, via especial Picard v2) + `cena_giro.js`. Telas da TV SAL: `abre` (GIRO DE DOMINGO + 1 2 3), `n1`, `n2` (cartão tipográfico), `n3` (carta com destaque), `agenda`.
- Faixa numerada vermelha no topo durante cada bloco ("1 · NOTÍCIA QUENTE", "2 · DA CASA", "3 · PRA VOCÊ JOGAR", "? · COMENTA 1, 2 OU 3"); escondida no zoom do texto da carta.
- Tarja: "MANA & BURN / TV SAL · GIRO DE DOMINGO".
- Vozes: ElevenLabs eleven_v4, Burn Talis `E9a8LlXPNWtyvvSoZzrb`, Mana Erik `nfiLpQ54jEQninp3nNqL`; uma faixa por personagem com `[long pause]`; 1 geração cada (~1.400 créditos no total no nº 1).
- Música: `manaburn/musica.mp3` (midnight_throttle). Parada seca 125,05 s no "Comenta aí", pancada 126,30 s desliga a TV. Ducking −14 dB sob as falas; bloco sensível pode ir a −30 dB.
- Fecho: TV desliga → ponto verde → `comum/outro/outro_binder_916.mp4` (3,87 s) via `juntar_fecho.py`; a trilha cobre o fecho.
- Duração alvo: 60–75 s com fecho. −14 LUFS.

## Passos (parâmetros reais)
1. `python3 processar.py vozes/burn.mp3 vozes/mana.mp3` → `data.js`, `trilha_final.wav` (imprime tempos e o total com fecho).
2. `python3 previa.py 1.5 9 17 …` → `previa/` (conferir carta inteira, faixa, agenda, legenda na zona segura).
3. `python3 quadros.py 0 N` (N = T_END × 30; dá para dividir em 2 processos) → `frames/`.
4. `ffmpeg -framerate 30 -i frames/%05d.jpg -c:v libx264 -crf 19 -pix_fmt yuv420p kit.mp4`
5. `python3 juntar_fecho.py kit.mp4 ../../../comum/outro/outro_binder_916.mp4 giro_AAAA-MM-DD_final.mp4`
6. QC: `ffmpeg -i final.mp4 -af ebur128 -f null -`, `cropdetect=24:2:0`, quadros em 0 / 3 s / transições / fecho.

Ligações simbólicas locais (não versionadas): `node_modules`, `tv_asset.png`, `logo` → `../../`.

## Esforço estimado por edição
Com a pesquisa feita: ~1h30 (guião 20 min, vozes 5 min, ajuste de telas 20 min, render ~20 min em 2 processos, QC e textos 25 min).
