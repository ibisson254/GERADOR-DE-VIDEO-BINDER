# Biblioteca urbana · Lisa Marie no Ar

Filmagem real de cidade que serve de fundo à Lisa ilustrada (decisão do fundador de 21/11/2026, `nucleo/DECISOES.md`). Os vídeos ficam **fora do repositório**, numa pasta local passada ao motor com `--clipes`. O `validar_repo.py` acusa qualquer MP4 dentro do repositório, mesmo que esteja ignorado pelo Git. No repositório versionam-se só este ficheiro e o `manifesto.csv`.

## Fonte escolhida: Pexels

Comparação feita a 21/11/2026, a partir das páginas oficiais:

| Critério | Pexels | Mixkit | Pixabay |
|---|---|---|---|
| Uso comercial e redes sociais | Sim, «free for commercial use» (FAQ) | Sim, a Stock Video Free License cobre «Social Media video posts» e «Commercial projects» | Sim, «even for commercial purposes» (FAQ) |
| Atribuição | Não obrigatória | Não obrigatória | Não obrigatória |
| Modificar | Permitido | Permitido | Permitido |
| Vídeo gerado por IA | **Proibido no upload** (regras de upload: «No generative AI content») | O site anuncia também clipes gerados por IA: é preciso verificar clipe a clipe | Há vídeos marcados como «AI generated» na biblioteca |
| Pessoas e marcas | Não mostrar pessoas identificáveis de forma negativa; não sugerir apoio de pessoas ou marcas; marcas retratadas podem continuar protegidas | Limites nos User Terms | Marcas e logótipos retratados não podem ser usados comercialmente em produtos |
| Licença identificável por clipe | Página do vídeo com autor, dimensões e ligação à licença | Página do clipe com a licença do item | Página com «Pixabay Content License» |

**Escolha:** o **Pexels**. Tem licença única e clara, autor identificado em cada página, muitos clipes verticais 4K e é a única das três que proíbe conteúdo gerado por IA no envio, o que cumpre o critério «vídeos reais». O Mixkit fica como alternativa, verificando clipe a clipe que é real e qual a licença. O Pixabay fica como último recurso.

Fontes: pexels.com/license, help.pexels.com («Can I use the photos and videos for a commercial project?», «What are the requirements for uploading videos?»), pexels.com/terms-of-service, mixkit.co/license/modal/videoFree, mixkit.co/terms, pixabay.com/service/license-summary, pixabay.com/service/faq.

## Direção urbana

Cidade contemporânea, viva e ligeiramente noturna: ruas molhadas, luzes de trânsito, reflexos, silhuetas sem rosto. **Nada de cyberpunk, colagem de néons ou fundo de videojogo.** A cidade é ambiente, não a casa da Lisa: nenhum clipe se apresenta como o sítio onde ela vive, e um clipe com cidade reconhecível (ex.: Londres) não se usa como se fosse outra cidade.

Grupos: **A** cidade noturna (ambiente principal) · **B** cidade em movimento (transportes, cruzamentos) · **C** texturas culturais (arte urbana só desfocada e em segundo plano, porque os murais têm direitos dos seus autores).

## Estado (21/11/2026)

11 clipes no `manifesto.csv`. **Usado no LM-EP00:** Pexels 14957612 (rua à chuva com semáforos), enviado pelo fundador a 21/11; falta confirmar o título e o autor na página. Os outros 10 estão selecionados e não descarregados: a rede desta sessão não chega a pexels.com nem aos servidores de vídeo do Pexels, do Mixkit ou do Pixabay. O pedido de download ficou com o fundador. Os metadados (autor, dimensões, duração) vêm da página de cada vídeo. Ao descarregar, confirmar esses dados, preencher a data e trocar o estado para `DESCARREGADO`.

## Como usar

1. Descarregar no Pexels, com o botão «Free download», a versão vertical ou a maior disponível. Gravar na pasta local de clipes (fora do repositório) com o **nome da coluna `ficheiro`**.
2. Atualizar o manifesto: `data_download`, resolução e duração reais, e observações sobre pessoas, matrículas e letreiros vistos no clipe.
3. O motor (`lisa-marie/motor/piloto_lm_ep00.py`) lê os clipes por esse nome. Um clipe em falta é substituído por um fundo provisório desenhado, com o aviso «FUNDO PROVISÓRIO» no quadro, e esse vídeo não é publicável.
4. Tratamento no motor: exposição a 55–78%, saturação a 70–80%, ligeira deriva para a paleta, vinheta e desfoque de 1,5–6 px. A cidade fica sempre atrás da evidência e da Lisa.
5. Nunca versionar os MP4. Créditos opcionais na legenda: «Fundo: <autor> / Pexels».
