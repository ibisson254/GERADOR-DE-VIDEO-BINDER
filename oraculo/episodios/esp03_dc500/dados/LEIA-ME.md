# MC-ESP03 · dados

- `extracao.csv`: só cabeçalho. Preencher a partir de `../capturas/` (uma linha por comandante, mesmo período e filtros; vazio = o portal não publica, nunca 0).
- `calcular.py`: quota do meta, win rate e conversão com intervalo de Wilson a 95 %, alertas de amostra (≥ 20 listas, ≥ 50 partidas, ≥ 3 torneios, ≤ 50 % num torneio), escolha de A e B pela regra fixada na ficha e veredito. `python3 -I calcular.py extracao.csv` → `resultado.md`. `--teste` corre com dados sintéticos (não publicáveis).
- Teste de robustez de período: uma extração por período (`extracao_<periodo>.csv`) e comparar os vereditos.
