# Kit do carrossel Lambe-lambe (padrão oficial desde 13/11/2026)

Aprovado pelo fundador a 13/11/2026 10:06: «Modelo aceito se torne padrão para carrocel de lambe lambe».

Base: os slides gerados por IA do John Avon (flow ElevenLabs `QUq7zV013KwmsMYP92hI`, ver `carrosseis_artistas/ia/`). Sem gastar créditos novos:
- `modelo_capa.png`, `modelo_editorial.png`: slides do Avon com os textos apagados (`kit.limpar`).
- `mask_pintura_*.png`: onde entra a pintura nova; `compor.pintura` aplica a arte com a pincelada da pintura original.
- `compor.camada` + `compor.aplicar`: textos em HTML (Archivo Black, Barlow Condensed, Rubik, Caveat Brush) impressos sobre o papel.
- `kit_papel.png`, `kit_fita.png`, `compor.colar`/`fita`: papel e fita para colar a carta real.
- Exemplo: `swan_capa.py`, `swan_2.py` (Raymond Swanland).

Regras: arte real da carta com crédito no slide; carta inteira colada no slide 2 (no lugar do retrato da referência); sem fotos nem rostos gerados de pessoas reais. Fontes, `desgaste.png`, cartas e artes não versionadas (ver `carrosseis_artistas/gerador/` v3).

## Padrão de 5 slides + foto do artista na capa (13/11/2026 10:12)
Pedido do fundador: todos os carrosséis do Lambe-lambe têm 5 slides e a capa leva a foto do artista; o fundador pede autorização ao artista antes de publicar e assume a responsabilidade.
A capa sai com o espaço «FOTO DO ARTISTA» (`foto_slot.py`). A foto não é procurada na internet nem gerada por IA: entra só a foto enviada pelo fundador (a que o artista autorizar), com `python3 -I foto_slot.py <capa.png> <saida.png> <foto.jpg>`.

Foto integrada como cartaz (13/11): `python3 -I foto_lambe.py <capa.png> <foto.jpg> <saida.png>` imprime a foto no papel creme (cor reduzida, retícula, rugas, falhas de tinta, borda rasgada) e põe a faixa preta do nome por cima. A foto do Raymond Swanland foi enviada pelo fundador, que pede a autorização ao artista antes de publicar; a foto não é versionada.
