# Ficha · Mana & Burn · Especial · Antes da carta chegar: obrigado, Sir Patrick

> **Estado (29/10/2026, 23:04): versão 1, substituída pela v2 em `../esp02_picard_v2/`. Não publicar.** Guardada para histórico e comparação.

## Classificação
- Série: Mana & Burn · especial de homenagem (tarja "HOMENAGEM")
- Classe: notícia + tendência cultural (morte de Sir Patrick Stewart a 28/10/2026, coincidente com o lançamento de Magic: The Gathering | Star Trek a 13/11/2026)
- Complexidade: alta (tema sensível, notícia do próprio dia)
- Estratégia (constituição §3): investigação aprofundada (5 fontes noticiosas independentes) + fonte primária da Wizards e do Scryfall para a carta e a data

## Editorial
- Proposta de valor: o que Patrick Stewart deu a Picard não cabe numa carta.
- Objetivo: homenagem respeitosa; comentários espontâneos com memórias de Picard. Sem promoção do app (pedido do brief; ver `comum/originals/DECISOES.md`, 29/10/2026).
- Público: comunidade de Magic, fãs de Star Trek, colecionadores.
- Gancho (0–4 s): a carta de Picard aparece do escuro na TV; "Tem uma carta do Jean-Luc Picard prestes a chegar no Magic. E hoje, ela ganhou outro significado."
- Fecho: "Obrigado, Sir Patrick." (Burn, baixo) → pergunta do Mana na TV → TV desliga → ponto verde → BINDER Originals.
- Métrica: comentários com memórias por 1.000 views e partilhas. Sem previsões.

## Fontes
Ver `ficha_fontes.md`.

## Produção
- Guião: `guiao_locucao.md` (16 blocos, PT-BR). Legendas: `legendas.srt` (as mesmas que estão queimadas no vídeo).
- Vozes: ElevenLabs eleven_v4, flow "Mana & Burn — Especial: Obrigado, Sir Patrick". Mana (Erik) narra; Burn (Talis) só diz "Obrigado, Sir Patrick." Áudios descarregados pela própria sessão (sem reenvio manual).
- Cena: `homenagem.html` = desenhos do `manaburn/index.html` (sala, dupla, TV, mesa; sem alteração) + `cena_homenagem.js` (noite: a TV é a única luz; sem TV SAL, sem manchetes, sem putômetro, sem inserts; a tela da TV mostra a carta, o nome e as frases em tipografia; nenhuma foto de Patrick Stewart).
- Carta: PNG oficial do Scryfall (trc/3, sem foil), crédito no topo durante todo o vídeo.
- Música: `musica.py`, composição original sintetizada (Ré maior, 64 BPM, piano esparso, cordas suaves, textura de ar), cresce no meio e resolve em Ré. Sem amostras nem melodia existente; nada de Star Trek.
- Efeitos: só o clique do controle e a TV de tubo a apagar, baixos.
- Montagem: `processar.py` (cortes nas pausas reais da voz, linha do tempo, ducking, -14 LUFS) → `quadros.py` (2 processos) → ffmpeg. `previa.py` e `capa.py` para conferência e capa.

## Riscos e limitações
- Pronúncia dos nomes (Jean-Luc Picard, Sir Patrick Stewart, Luminary, Magic: The Gathering) não foi conferida por transcrição: o envio para o Scribe foi bloqueado pela rede da sessão e não há modelo local. Ouvir antes de publicar.
- Licença das vozes: depende de o plano ElevenLabs com licença comercial estar ativo no momento da geração (29/10/2026, 22:29); não verificável por esta ligação.
- A arte da carta mostra a figura de Picard (ilustração oficial). Não há outra imagem do ator.
- Reuters e AP (links do brief) não abriram; confirmado em CNN, NBC, CBS, NPR e Playbill.

## QC
Ver secção no fim (preenchida a partir do ficheiro final).

## QC medido no ficheiro final (`ManaBurn_Especial_SirPatrick_916.mp4`, 29/10/2026)
| Critério | Alvo | Medido | OK |
|---|---|---|---|
| Resolução / fps | 1080×1920, 30 | 1080×1920, 30/1, 1643 quadros | sim |
| Codecs | H.264 + AAC 48 kHz | h264 + aac 48000 Hz | sim |
| Duração | 45–55 s (brief) | 54,77 s | sim |
| Loudness integrado | −14 ±0,5 LUFS | −14,3 LUFS | sim |
| True peak | < −1 dBFS | −1,6 dBFS | sim |
| cropdetect 24:2:0 | 1080:1920:0:0 | 1636/1643 quadros = 1080:1920:0:0; os 7 restantes são a TV a ligar (0–0,2 s) e a apagar (52,2–52,6 s), preto por desenho | sim |
| Tela da TV inteira nos planos da TV | laterais dentro do quadro | trava de enquadramento do kit (margem 10 px) em todos os planos tv/tv2; conferido em 20 quadros extraídos do ficheiro final | sim |
| Carta inteira, rodapé visível, nada por cima | — | 1,5 / 3,5 / 31 / 35 s | sim |
| Legenda queimada | zona segura | bottom 440 px; 16 blocos; amarelos nos termos-chave | sim |
| Textos de ecrã | legíveis no telemóvel | nome 46 px, frase 44 px, pergunta 40 px na tela da TV; "13 NOVEMBRO 2026" 60 px | sim |
| Mensagem sem som | — | legenda contínua + nome, frase, data e pergunta em texto | sim |
| Publicidade | nenhuma | sem CTA, sem preço, sem app, sem scanner | sim |
| Fecho | TV desliga → ponto verde → assinatura | 52,3 / 53,2 / 54,5 s | sim |
| Pronúncia dos nomes | ouvida | NÃO conferida (ver Riscos) | pendente |

## Entregáveis
- [x] Vídeo · [x] Capa (`ManaBurn_Especial_SirPatrick_916_capa.jpg`) · [x] Legenda · [x] Comentário fixado · [x] Legendas SRT · [x] Guião com tempos · [x] Fontes
