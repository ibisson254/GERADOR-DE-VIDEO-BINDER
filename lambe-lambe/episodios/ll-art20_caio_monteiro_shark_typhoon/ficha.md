# Ficha · Lambe-lambe · LL-ART20 · Caio Monteiro: o ilustrador do Rio por trás de Shark Typhoon

## Identificação
- ID editorial: LL-ART20 (LL-ART14–19 reservados à branch `lambe/artistas-carrosseis`)
- Estado no registo: CONCLUÍDO (não publicado; aguarda resposta do artista)
- Origem: missões de produção do fundador de 16/11/2026 (briefing + ordem da fotografia, 18:32); método «episódio pronto primeiro» (`comum/parcerias.md`)

## Classificação
- Frente: Lambe-lambe, série «Artistas de Magic», carrossel 4:5, 7 slides
- Estratégia: motor-padrão; zero créditos (sem ElevenLabs, música, imagem gerada)

## Originalidade
- `memoria.py pauta --objeto "Caio Monteiro" --tema "artista carioca de Shark Typhoon"`: LIVRE (16/11/2026)

## Editorial
- Objetivo: apresentar Caio Monteiro à comunidade brasileira e abrir uma collab com o artista
- Gancho: «O ilustrador do Rio por trás de Shark Typhoon»
- Métrica principal: guardados e partilhas por 1.000 views, contra LL-ART13

## Fotografia e autorizações
- Fotografia fornecida pelo fundador (não versionada).
- **Autorização de publicação da fotografia: PENDENTE.**
- **Publicação da versão com foto (A): BLOQUEADA até autorização expressa.**
- **Plano alternativo: versão sem foto (B).**
- Três pedidos distintos (nenhum implica os outros): (1) uso da foto e da imagem; (2) OK para publicar o conteúdo; (3) collab no Instagram.
- Prazo de resposta: 5 dias (até 21/11/2026). Sem resposta: não se publica automaticamente; o fundador decide.
- Resposta do artista: guardar em `lambe-lambe/autorizacoes/AAAA-MM-DD_caio_monteiro.md`.
- Se não autorizar a foto: versão B. Se recusar a collab: versão B ou A (se a foto for autorizada) com crédito e marcação, sem insinuar parceria.

## Mensagem de envio (o fundador envia por DM a @caiomonteiroart, com a pasta da prévia)
> Oi, Caio! Sou o Ibisson, do BINDER Vision. A gente faz uma série de carrosséis sobre artistas de Magic e preparamos um sobre seu trabalho, começando por Shark Typhoon.
>
> Incluímos uma foto sua na prévia para apresentar o artista junto das cartas. Antes de publicar, queria confirmar se você autoriza o uso dessa fotografia e da sua imagem no carrossel.
>
> Também gostaríamos de convidar você para publicar em collab com a gente. Caso queira corrigir algum crédito ou informação, fazemos os ajustes antes.
>
> Obrigado por compartilhar seu trabalho com a comunidade!

## Produção
- `python3 -I carrossel.py <cartas> <foto> <mask> <saida> [--previa] [--sem-foto]` (cartas do Scryfall conforme `fontes.md`; máscara retangular: o recorte automático juntava o fundo escuro ao boné e ao cabelo, por isso a foto entra em retângulo com borda de papel rasgado, como previsto no briefing).
- Versões renderizadas: A (com foto), A prévia (faixa vertical «PRÉVIA · AGUARDA AUTORIZAÇÃO» no muro direito, fora de cartas e artes), B (sem foto). PNGs entregues ao fundador e **não versionados** (a A contém a foto sem autorização).

## Controlo de qualidade (16/11/2026)
- 1080×1350 em todos os 21 PNGs (3 versões × 7): OK.
- Cartas inteiras, sem deformação; fita só nos cantos de cima; nenhum texto sobre arte, rodapé ou texto de regras: OK.
- Crédito «carta (set nº) · Caio Monteiro · © Wizards of the Coast» em todos os slides (slide 7: nome e set de cada arte junto a ela + «Artes acima: Caio Monteiro · © Wizards of the Coast»): OK.
- Dados com fonte e data (slides 3–6): OK. Percentagem de inclusão retirada (não confirmável hoje; ver `fontes.md`).
- Foto sem deformação, sem sobrepor cartas; versão B sem vestígios da foto; prévia identificada: OK.
- Sem citações do artista, sem bastidores, sem alegação de parceria: OK.
- Limitação: o desgaste da tipografia (padrão do kit) deixa algumas letras falhadas, como nos carrosséis anteriores.

## Pendências
- Fundador: enviar a prévia e a mensagem; registar a resposta.
- Publicar só depois da resposta, com `utm_campaign=LL-ART20` no link da bio se aplicável.

## Ficheiros finais
- Carrossel (vídeo: não se aplica): `versao_A_com_foto/`, `versao_A_previa/`, `versao_B_sem_foto/` (`01_capa.png` … `07_participacao.png`) + `folha_de_contacto_*.jpg`, entregues ao fundador na conversa de 16/11/2026 (`LL-ART20_caio_monteiro.zip`). Recriáveis com `carrossel.py`.
- Capa: `01_capa.png`
