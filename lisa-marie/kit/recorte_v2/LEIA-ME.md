# Recorte v2 da Lisa (21/11/2026)

Evolução das camadas da prova (`../prova_recorte/`), sem redesenhar a personagem e sem arte nova. Continua a ser **arte-conceito** (look 1, 262 px de origem).

- **Cabeça separada do corpo**, com pivô no pescoço (712, 872) e costura suave entre y 812 e 900: a cabeça inclina sem arrastar o tronco.
- **Olhar com direção:** a íris é deslocada dentro da abertura do olho (variantes `c`, `e`, `d`, `cima`), com o espaço vazio reconstruído por inpainting.
- **Bocas v2** (Rhubarb X, A–H): traço de 3 px em tinta quente, interior menos saturado e leve suavização, para parecerem menos um autocolante. Continuam provisórias.
- Pálpebras: as da prova (a elipse do olho fechado continua a ser um limite conhecido).

Uso: `python3 -I camadas_v2.py PASTA_DA_PROVA PASTA_SAIDA`, depois de correr `../prova_recorte/recortar.py` e `camadas.py`. Primeiro uso: LM-EP01.
