# Meta em Curto · motor de edição padrão (desde 19/11/2026)

Padrão aprovado pelo fundador no MC-ESP03 (v4 + capa v2). Regras em `oraculo/CONTEXTO.md` §7.4; lições de custo em `oraculo/PERFIL.md`.
Episódios publicados ou aprovados não se refazem com este motor; o ESP03 mantém o seu `esp03_render.py`.

## Ordem de trabalho (cada passo só depois do anterior)
1. **Dados** abertos e verificados (navegador integrado no PC do fundador se o site usa JavaScript). Cálculos com `oraculo/episodios/esp03_dc500/dados/calcular.py` (Newcombe para diferenças). Capturas em `<pasta>/capturas/` (recortes sem alterações; logótipo de terceiros só com decisão registada).
2. **Cartas** do Scryfall em `<pasta>/cartas/` + `creditos.json`.
3. **`dados/episodio.json`** a partir de `episodio_modelo.json`, com as `frases` da locução (a primeira diz a fonte).
4. **Orçamento da voz:** ≈ 11,8 caracteres por segundo (Antonio de Jesus, atempo 1,10) → 35 s ≈ 390 caracteres no total. `estimate_only` no ElevenLabs e **uma** pergunta ao fundador com o texto final e o custo.
5. **Voz:** uma geração. Depois `python3 -I oraculo/motor/mc_voz.py <pasta> voz.mp3` → `voz_montada.wav` e `voz_tempos` no JSON (alinha as falas às frases pelo tamanho do texto, números lidos por extenso; encurta pausas até ao alvo).
6. **Fotogramas:** `python3 -I oraculo/motor/mc_render.py <raiz> <pasta> stills 0.5 2.4 4 ...` → folha de contacto → corrigir.
7. **Um render:** `... final voz_montada.wav` (vídeo + trilha até ao fim do fecho + loudness −14 LUFS).
8. **Capa:** `... capa` → `CAPA.png`, `CAPA_grelha.png`, `CAPA_grelha_mini.png` (conferir a miniatura).
9. **QC:** `python3 -I comum/qc/qc_video.py MC_FINAL.mp4 --frente tubo` + folha de contacto a olho.

## Cenas disponíveis (`seq`)
| Plano | Argumentos | O que faz |
|---|---|---|
| `gancho` | — | Quadro 0: cartas A e B + captura da matriz/prova + pergunta no topo + selo de fonte |
| `tubo_abertura` | t_voo, t_mergulho | TUBO a falar (LED com a voz), cartas ao lado; a carta A voa para o ecrã e o vídeo mergulha |
| `carta` | lado (A/B/L), número, unidade, posição, [t, `top5`/`matriz`, rótulo] | Carta grande ao centro (troca em rotação 3D), número em caixa; prova opcional a meio |
| `duas` | t da definição | As duas cartas lado a lado com indicador e denominador |
| `tubo` | expressão, [t ecrã «ESCOLHE ≠ GANHA», expressão 2] | TUBO sai do ecrã (zoom-out) e fala; legenda no topo |
| `dif` | — | Painel da diferença: ponto, margem de 95 %, veredito, nota de robustez |
| `pergunta` | — | Cartas frente a frente com a pergunta final |
Ao voltar do `tubo` para um plano de dados, o motor mergulha no ecrã automaticamente.

## O que ainda é específico de episódios «popularidade × desempenho»
As cenas `dif` e `duas` e os campos `iA/iB/dif_*` foram feitos para comparar dois comandantes. Outros tipos de episódio (deck, previsão, campeão) reutilizam o fundo, as legendas, `carta`, `tubo`, `gancho`, a voz e a capa; uma cena nova acrescenta-se aqui, não num motor novo.

## Performance e regressão (26/11/2026, `nucleo/auditorias/2026-11-26_engenharia.md`)
- Brilhos (`glow_box`, `circulo`, flash do mergulho) desfocam só a zona desenhada (`_desfoque_local`), não o quadro inteiro; o render faz **uma** codificação (quadros em bruto direto no grafo que junta o fecho). MC-PAU08 prévia: 105–108 s → 49–51 s; quadros iguais píxel a píxel; fecho idêntico; corpo mais fiel aos quadros compostos (menos uma geração de compressão).
- Antes de integrar qualquer alteração ao motor que não deva mudar a imagem: `python3 -I oraculo/motor/mc_render_regressao.py` (compara com a `HEAD`, todos os episódios com `dados/episodio.json`; `--ref <commit>`, `--passo N`). Sai com erro se algum quadro mudar.
- Paralelizar a composição foi medido e **não** compensou numa máquina de 2 núcleos (o ffmpeg disputa a CPU); não foi adotado.

- **27/11/2026 (MC-EP09 v2):** cenas `mosaico` (gancho: arte dos comandantes de todos os jogadores, scanner apaga até ficar o campeão; `p=[t0,'mosaico',scan0,scan1,zoom,carimbo]`, dados em `D['mosaico']`) e `evento` (mapa Natural Earth com alfinete + cartão da loja/evento; `p=[t0,'evento',t_alfinete,t_cartao]`, `D['evento']`). Deixas de efeitos por episódio em `D['sfx']` (`[tempo|@âncora, nome, ganho, dur?]`; ficheiros opcionais em `D['sfx_banco']`, senão sintetizados), `D['abalos']` e `D['transicoes']`. Episódios sem estas chaves não mudam (regressão ESP03/PAU02/PAU08).
