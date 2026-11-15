# ABISMO · Processo de `ABISMO: CRIAR POSTAGEM`

## 1. Pesquisa de interesse (últimos 14 dias)
Fontes: Reddit r/magicTCG e r/EDH, EDHREC, MTGGoldfish, Scryfall, Wizards (artigos e Card Image Gallery).
Recolher até 30 itens em `publicacoes/<ID>/pesquisa.md`: data da recolha, URL, carta, o que se discute.
Só registar números que a fonte mostra; distinguir **popularidade observada** (ex.: posição no EDHREC, votos visíveis)
de **impressão** do agente. Escolher a carta/tema com mais sinais independentes e que caiba numa única mensagem.

## 2. Verificação
Texto oficial e coleção no Scryfall; artista; tiragens e tratamentos só com fonte oficial. Tudo em `fontes.md`.

## 3. Escolha de formato
| Formato | Quando |
|---|---|
| **Reel** (~20,6 s, 48 batidas) | há uma reviravolta (custo vs condição, comparação com clássico) que ganha com o drop da música |
| **Story** (13,7 s, 32 batidas; 2–3 segmentos) | pergunta rápida à audiência com enquete; novidade do dia |
| **Carrossel** (4:5, 5 slides) | informação densa para guardar (regras, comparação ponto a ponto) |
Registar a justificação em `post.json` → `"porque_formato"`.

## 4. QC
- `ffprobe`: 1080×1920 (ou 1080×1350), 30 fps, H.264/AAC 48 kHz; duração do modelo.
- Áudio: −14 LUFS ±1, pico ≤ −1 dBTP; cortes de música em batidas inteiras.
- Quadros de controlo (`stills`): gancho legível no quadro 0, nada fora das zonas seguras do modelo, crédito visível com a carta,
  nenhuma sobreposição de texto, assinatura com logótipo oficial.
- Factos do ecrã = `fontes.md`. Português do Brasil, "você".

## 5. Pacote de entrega
Vídeo ou slides, capa, `legenda.txt`, `comentario_fixado.txt`, `texto_alternativo.txt`, `fontes.md` (fontes e créditos),
objetivo, formato e duração, porquê o formato, elementos reaproveitados. Linha nova em `REGISTRO.md`. Publicar só o fundador.
