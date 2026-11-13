# Ficha · Mana & Burn · EP11 · O rodízio de combo (Niv-Mizzet Reborn)

Estado (13/11/2026, 02h10): **vídeo final renderizado e conferido; aguarda aprovação e publicação pelo fundador. Não publicado.** Vozes geradas (Mana depois da recarga de créditos do fundador, "Pode gerar já atualizei o elevenlabs", 02:02).

## Render e controlo de qualidade
- `ManaBurn_Ep11_Rodizio_916.mp4` (não versionado): 1080x1920, 30 fps, 49,6 s (45,7 s + fecho do scanner), −14,4 LUFS, pico −1,4 dBTP. `bordas.py` OK (456 quadros de TV, laterais 10–1068 px). `qc_video.py`: sem problemas mensuráveis; folha de contacto conferida a olho (carta inteira, destaques alinhados, inserts com crédito, "Comenta aí" antes da pancada, fecho presente).
- Capa: `ManaBurn_Ep11_Rodizio_916_capa.jpg` (não versionada).

## Origem
- Pedido do fundador (13/11/2026, 01:52): episódio inspirado num Reel de terceiros ("The 2 Color Conundrum", @bullwark_mtg repostado por @mtg_paradise): um deck de Niv-Mizzet Reborn em que cada carta de duas cores faria parte de um combo infinito (Brago + Strionic Resonator, Savage Ventmaw + Aggravated Assault, Duskmantle Guildmage + Mindcrank, Witherbloom Apprentice + Chain of Smog e uma lista de mais combos).
- Refinamento para o Mana & Burn: não repetimos a vitrine de combos. O "Lê a carta" do Mana desmonta o hype: o Niv só escolhe carta de **exatamente** duas cores, e nos três combos usados a segunda peça é monocolor ou incolor, por isso o Niv entrega meio combo. Nada da edição, texto ou imagem do Reel de origem foi usado.

## Classificação
- Série: Mana & Burn · tarja "RODÍZIO DE COMBO"
- Classe: tendência / reação da comunidade (deck viral) + regra de carta. Estratégia: verificação rápida (Oracle via Scryfall) para todas as regras e combos.
- Auditoria de originalidade (`memoria.py pauta`, 13/11): Niv-Mizzet Reborn e Aggravated Assault, PAUTA LIVRE. Relação temática fraca com MB-EP05 (combo) e ORB-12 (mana infinita): objetos e ângulo diferentes.

## Editorial
- Público: jogador casual e de Commander no Brasil que viu o deck "todo combo" circular.
- Tese: o hype diz "deck infinito"; a carta diz "meio combo". O humor é a promessa da internet, não quem joga de Niv.
- Comparação absurda: rodízio em que o garçom só serve prato de duas cores (o arroz vem, o feijão você busca na cozinha).
- Gancho (0–3 s): "Mano, a internet achou um deck de Commander que é *combo infinito* do começo ao fim!" com o Niv na TV.
- Pergunta (fala 13 = 1.ª linha do comentário fixado): "O Niv virou dez cartas. Quantas vêm pra sua mão? Chuta de 0 a 10." Hipótese (PERFIL, métrica principal): pergunta de número tem barreira menor que A/B e gera mais respostas por 1.000 views que o EP10.
- Ponte para o BINDER: deck de cinco cores → escanear e organizar o deck (funções confirmadas no fecho oficial).

## Roteiro final (14 falas, Burn começa)
1. B [shouting] Mano, a internet achou um deck de Commander que é *combo infinito* do começo ao fim! · tv
2. M [bored] É o *Niv-Mizzet Reborn*. Tá na TV. · cuM
3. B [excited] Ele entra, vira *dez cartas* e te serve uma de *cada par de cores*. Rodízio de combo! · tvtext2 (destaque "reveal the top ten cards")
4. M [deadpan] Lê a carta: uma carta que seja *exatamente* daquelas duas cores. · tvtext (destaque "For each color pair, choose / a card that's exactly those colors")
5. B [outraged] E daí? O *Savage Ventmaw* é vermelho e verde. Ele vem! · cuB + insert Ventmaw
6. M [deadpan] Vem. Mas o combo dele é com *Aggravated Assault*. Que é *só vermelho*. · wide + insert Assault
7. B [shouting] Então troca! *Duskmantle Guildmage* com *Mindcrank*! · push + insert Mindcrank
8. M [tired] Mindcrank é *incolor*. O Niv nem olha. · cuM
9. B [outraged] *Witherbloom Apprentice* com *Chain of Smog*?! · cuB + insert Chain of Smog
10. M [bored] Chain of Smog é *só preta*. O garçom traz o arroz. O *feijão*, você busca na cozinha. · wide
11. B [shouting] Então o deck infinito é *meio combo*?! · tv2
12. M [deadpan] Metade vem no *Niv*. A outra metade vem na *reza*. · cuM
13. B O Niv virou dez cartas. Quantas vêm pra sua mão? Chuta de *0 a 10*. · cuB (point_cam)
14. M [bored] Comenta aí. · cuM (TV desliga)

## TV SAL
- Combômetro 50% = 3 de 6 peças que o Niv acha nos três combos do episódio (Oracle · Scryfall). O Niv-Mizzet Reborn não tem Salt Score próprio acessível nesta sessão (EDHREC bloqueado na rede); a alternativa do playgroup.gg ("59,5% das vitórias marcadas salgadas") foi recusada por incoerência interna na página (242 vs 233 vitórias).
- Placar: "Pares de cores: 10 · cartas viradas: só 10" (Oracle).
- Relógio 10:10 (easter egg: 10 cartas, 10 pares).
- Manchetes: 6 piadas com factos do Oracle (Assault só vermelho desde 2002; Mindcrank incolor; carta de três cores não entra; Niv custa uma mana de cada cor), chamada para o EP10 e teaser do Giro de domingo.

## Fontes (conferidas a 13/11/2026)
- Oracle e impressões: API do Scryfall (`scry/*.json`): Niv-Mizzet Reborn (WAR 208, Raymond Swanland), Savage Ventmaw (DTK 231, Slawomir Maniak), Aggravated Assault (ONS 185, Greg Staples), Mindcrank (NPH 144, Chris Rahn), Chain of Smog (ONS 132, Greg Staples). Cores conferidas pelo campo `color_identity`/`mana_cost`.
- Lógica dos combos conferida pelo texto Oracle: Ventmaw gera {R}{R}{R}{G}{G}{G} por ataque e o Assault custa {3}{R}{R} (sobra 1 por ciclo); Guildmage faz perder 1 por carta no cemitério e o Mindcrank moe por vida perdida; Chain of Smog pode ser copiado pelo alvo e cada cópia dispara o magecraft do Witherbloom Apprentice.
- Reel de origem (referência, não citado no vídeo): ficheiro enviado pelo fundador, 54 s, 13/11/2026.

## Vozes
- ElevenLabs (conector restrito), eleven_v4, 1 geração por faixa. Flow: https://elevenlabs.io/app/flows/toKppksshHSJqbowfiF9
- Burn (Talis, `E9a8LlXPNWtyvvSoZzrb`): gerada, 559 créditos, 29,6 s, 6 pausas = 7 falas → `burn_ep11.mp3`.
- Mana (Erik, `nfiLpQ54jEQninp3nNqL`): 1.ª tentativa falhou por quota (250 de 480); gerada às 02:03 depois da recarga, 480 créditos, 29,8 s → `mana_ep11.mp3`. Cortes conferidos (7 falas cada; a pausa interna depois de "Vem." ficou dentro da fala 6).
- Licença: confirmar que a conta está no plano com licença comercial antes de publicar.

## Pendências
1. Ouvir a pronúncia dos nomes de cartas (Ventmaw, Guildmage, Mindcrank, Witherbloom, Chain of Smog) antes de publicar.
2. Confirmar licença comercial do plano ElevenLabs.
3. Aprovar e publicar; registar a data no registo editorial.
