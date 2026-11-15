# ABISMO · Nauctis: The Sunken Realm

Kit de produção isolado e reutilizável, exclusivo da edição **Nauctis**, derivado do vídeo de referência aprovado
(EX-01 v3 A, 59,17 s). Não substitui nem altera a identidade de nenhuma outra série. Tudo vive nesta pasta.

## Comando permanente: `ABISMO: CRIAR POSTAGEM`
1. **Pesquisa** (PROCESSO.md §1): o que a comunidade discute sobre Nauctis nos últimos 14 dias (Reddit r/magicTCG e r/EDH,
   EDHREC, MTGGoldfish, Scryfall, Wizards). Até 30 itens, data da recolha registada, sem números inventados.
2. **Verificação**: texto oficial da carta no Scryfall, créditos do artista e fonte de cada afirmação.
3. **Formato** (PROCESSO.md §3): o agente escolhe Story, Reel ou Carrossel e justifica.
4. **Produção**: `abismo/publicacoes/<ID>/post.json` a partir de `modelos/exemplos/`, depois
   `python3 -I abismo/motor/abismo.py abismo/publicacoes/<ID>` (na raiz do repositório).
   **Toda postagem sai com capa** (regra do fundador, 15/11/2026): no Reel o motor gera `saida/<ID>_capa.png` no fim do render
   (texto em `"capa"` do post.json; sem ele usa o `gancho`); no Carrossel o 1.º slide é do tipo `capa`. Só capa: `python3 -I abismo/motor/capa.py abismo/publicacoes/<ID>`.
5. **QC** (PROCESSO.md §4) e **entrega** (PROCESSO.md §5). Linha nova em REGISTRO.md. Nunca publicar automaticamente.

## Conteúdo
| Caminho | O quê |
|---|---|
| `IDENTIDADE.md` / `identidade.json` | especificação visual e sonora (fonte única dos valores usados pelo motor) |
| `INVENTARIO.md` | auditoria do vídeo de referência e dos recursos reaproveitados |
| `PROCESSO.md` | pesquisa, escolha de formato, QC, pacote de entrega |
| `REGISTRO.md` | memória do projeto: uma linha por publicação |
| `kit/` | fundo mestre em placa (9:16 e 4:5) para usos fora do motor |
| `motor/abismo.py` | motor único dos três formatos |
| `motor/capa.py` | capa do Reel 9:16 (essencial no recorte 3:4 da grelha); lê `"capa"` do post.json |
| `modelos/{reel,story,carrossel}.json` | tempos, zonas seguras e sincronia com a música |
| `publicacoes/<ID>/post.json` | conteúdo de cada publicação (renders em `saida/`, fora do Git) |

Custo por publicação: zero (Python, FFmpeg, API pública do Scryfall). Sem voz por defeito; narração só com autorização
do fundador e sem créditos novos.
