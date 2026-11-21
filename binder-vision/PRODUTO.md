# BINDER Vision · mapa de funcionalidades

Levantamento de 21/11/2026. Fontes: Supabase (tabelas, funções e migrações do projeto `rfucohyfvjqmfwuqcjrd`), código `ibisson254/aethervault-app` na `main` (a0a85bd, 26/10/2026, versão 2.4.5 = produção v6), `.ai/03_STATE.md` do app, constituição §9 e a campanha «Pare de digitar» (`lambe-lambe/campanhas/2026-11_pare_de_digitar/CAMPANHA.md` §0–§1).

**Existir no código não é o mesmo que poder anunciar.** A coluna «Marketing» manda.

- **ANUNCIÁVEL**: pode aparecer em vídeo e legenda, com gravação real.
- **CONFIRMAR**: existe no código; antes de citar, o fundador confirma no aparelho que funciona na versão da Play.
- **NÃO ANUNCIAR**: existe, mas está congelado ou contradiz a promessa (decisões de 21/10 e 11/11).

## 1. Colecionador (abas: Explorar · Binder · Scan · Chat · Perfil)

| Função | O que faz | Marketing | Notas |
|---|---|---|---|
| **Scanner** (aba Scan) | Aponta a câmera, lê o título (OCR) e compara a imagem com um índice visual no aparelho; o utilizador confirma a impressão | **ANUNCIÁVEL** · porta de entrada | O utilizador confirma; não dizer «entra sozinha». Gravação real: `comum/outro/` |
| Escolha da impressão | Mostra as impressões da carta para escolher a certa | **ANUNCIÁVEL** | Dor real: «qual das 20 versões do Sol Ring é a minha?» |
| **Binder** (coleção) | Cartas com quantidade, condição, foil e valor de referência; total da coleção | **ANUNCIÁVEL** (com «valor de referência») | As linhas «Investido» e «Lucro +15 %» são cálculo provisório: **nunca mostrar** |
| **Exportar para a LigaMagic** | Copia a coleção em lista (Cadastro por Lista) ou CSV (Importar Coleção) | **CONFIRMAR** (falta captura real do menu) | Sem parceria com a LigaMagic; não usar o logótipo |
| Valor de referência | Scryfall em US$ convertido com câmbio fixo (5,60; o scanner usa 6,0) | **ANUNCIÁVEL só como «estimativa/referência»** | O scanner diz «VALOR DE MERCADO»: correção pedida ao arquiteto |
| Decks | Ecrã de decks e detalhe do deck | **CONFIRMAR** | Citável pela constituição §9, mas sem gravação no repositório |
| Lista de desejos | Tabela `wishlist` | **CONFIRMAR** | 0 registos no Supabase a 21/11 |
| Favoritos | Guardar cartas de outros | CONFIRMAR | 20 favoritos no total (21/11) |
| Oráculo (pesquisa) | Pesquisa de cartas por nome para adicionar | CONFIRMAR | |
| Explorar | Feed público de cartas de outros colecionadores, por proximidade | **NÃO ANUNCIAR como argumento** | Base pequena: o feed vazio contradiz a promessa |
| Perfil público, seguidores | Seguir colecionadores; perfil com coleção pública | NÃO ANUNCIAR como argumento | Mesma razão |
| Chat | Conversa 1:1 com texto e imagem | NÃO ANUNCIAR como argumento | Citável pela §9, mas sem base de utilizadores para conversar |
| Trocas | Proposta de troca, reserva e entrega com PIN | **NÃO ANUNCIAR** (congelado a 21/10) | |
| Radar | Sugestões e colecionadores perto | NÃO ANUNCIAR | Depende de localização (P0 de privacidade DSC-1) |
| Insígnias | Early Adopter, Collector, High Roller, Champion | CONFIRMAR | «Early Adopter» pode virar argumento de comunidade beta, se o fundador confirmar a regra de atribuição |
| Bloquear e denunciar, apagar conta | Moderação e privacidade | Não é argumento | Útil para responder a objeções de confiança |
| Login | E-mail, Google ou Discord | Informativo | **Obrigatório antes de ver qualquer ecrã** (`app/_layout.tsx`). O modo visitante está no ramo `feature/zf-01`, sem build confirmado |

## 2. Lojista (Operador)

| Função | O que faz | Marketing |
|---|---|---|
| Arena (loja) | Perfil de loja com morada, WhatsApp, CNPJ, verificação | **NÃO ANUNCIAR** (congelado a 21/10) |
| Inventário da loja | Cartas, selados e acessórios; scanner de loja; exportação LigaMagic | NÃO ANUNCIAR |
| Presença / check-in | Quem está na loja agora | NÃO ANUNCIAR |
| Torneios | Inscrição, lista de espera, emparelhamento suíço, resultados por consenso dos dois jogadores, classificação, campeão e Hall da Fama | NÃO ANUNCIAR |
| Painel | Estatísticas da loja | NÃO ANUNCIAR |

Lojas entram hoje só como **distribuição** (QR no balcão para colecionadores, campanha «Pare de digitar» §6.4), nunca com promessa de funções para a loja.

## 3. Limites a dizer quando perguntarem

- Só Android. Beta: pode haver erros; o fundador responde.
- Valores são referência convertida do dólar, não preço da LigaMagic.
- Precisa de conta (e-mail, Google ou Discord) para usar.
- Cartas em português: por confirmar.

## 4. Para atualizar

Função nova, mudança de estado (ex.: trocas descongeladas, modo visitante na Play) ou correção: mudar esta tabela, com data e fonte, e registar em `nucleo/DECISOES.md`.
