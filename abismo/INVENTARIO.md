# ABISMO · Inventário e auditoria (15/11/2026)

## Vídeo de referência
EX-01 v3 A «Operação Abyssal» (59,17 s, 1080×1920, 30 fps). Fica fora do Git (regra do repositório) e **não foi modificado**.
Receita completa no ramo `expedicao/01-nauctis`: `expedicao/01-nauctis/episode.json` + `expedicao/template/`.

| Recurso | Onde está | Uso no ABISMO |
|---|---|---|
| Gerador do fundo | `expedicao/template/fundo.py` | importado pelo motor (sem cópia) |
| Música do fundador | `expedicao/kit/auction_of_power.mp3` | cortes por batida |
| Sons | `expedicao/kit/sfx/{descida,glitch,swell}.mp3` | reaproveitados tal como estão |
| Logótipo oficial | `manaburn/logo/logo_mark.png` | canto + assinatura |
| Captura real do scanner | `comum/outro/scan/000–044.jpg` | disponível para assinaturas futuras (não usado nos modelos) |
| Fontes | `/usr/share/fonts/opentype/inter/` | Inter / Inter Display |
| Cartas | Scryfall (API pública) | descarregadas pelo motor; PNG fora do Git |

## Lacunas
- `render.py`/`audio.py` da Expedição são scripts de episódio (não importáveis); o motor ABISMO reescreve só as cenas
  necessárias e importa o fundo. Dependência: o ramo `expedicao/01-nauctis` (o ABISMO foi criado a partir dele).
- Narração: gerar voz custa créditos ElevenLabs → modelos sem voz por defeito.
- Sem imagens de produto selado (caixas) nem de stems separados da música.
- Documentos da EX-01 ainda dizem "licença a registar" para a música; o fundador confirmou que é sua. Fora de `abismo/`, não alterado.
