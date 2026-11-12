# Vinci — bíblia da personagem e da série

Frente nova do BINDER Originals (@binderthetrade), **em desenvolvimento**: traço e cenário definidos pelo fundador a 11–12/11/2026; voz, nome público e cadência ainda por decidir. Ler antes de produzir qualquer peça do Vinci. O que estiver marcado **(proposta)** ainda não foi aprovado.

---

## 1. O que é

O Vinci é a frente que fala do **mercado das cartas**: o que subiu, o que caiu, porquê, e o que isso significa para quem tem aquela carta na pasta.

- **Personagem:** meio vendedor de feira, meio corretor. Fala depressa, sabe os números, e o fato é um tamanho acima do que ele consegue pagar.
- **Público:** jogador brasileiro adulto com cartas guardadas.
- **Promessa:** em 40 segundos ficas a saber porque é que aquela carta mudou de preço.
- **Relação com o BINDER Vision:** direta. Quem acabou de ver uma carta subir quer saber quanto vale a pasta dele.

## 2. Fronteiras

| Assunto | Frente |
|---|---|
| Preço como assunto principal, com causa e fonte | **Vinci** |
| Preço como remate cómico no fim de um episódio | Mana & Burn |
| Notícia de mercado da semana | Giro de Domingo |
| Resultado competitivo e metagame | Meta em Curto |
| Arte e artistas | Conde de Manaforte |

## 3. Direção de arte

**Origem do estilo.** Duas referências com papéis diferentes: o método vem de um Reel de ilustrações paradas cortadas a cada 3–6 s, sem animação nenhuma; o traço vem de fichas de character design de animação enviadas pelo fundador. Método de um, desenho do outro.

**Linguagem de forma.** Torso triangular pesado em fato grande de mais, ombros largos e descaídos, pernas curtas e finas, sapatos pequenos, **mãos grandes** (são elas que apontam o painel), cabeça pequena metida entre os ombros, queixo quadrado, sobrancelhas angulares, olheiras, cabelo para trás. Corpo de tubarão, cara de quem não dorme há três semanas.

**Teste de silhueta.** A preto sólido, a figura tem de ser reconhecível e distinta das outras personagens do estúdio. Se não for, o desenho não está certo.

**Linha.** Tinta digital de espessura irregular, traços de construção visíveis, linhas que passam um pouco do canto. Nada de contorno uniforme de vetor.

**Cor.** Chapada, no máximo uma sombra por forma. Sem gradientes, sem brilho, sem textura. Fato cinza-esverdeado, camisa creme, parede verde-acinzentada. **Uma só cor saturada no ecrã de cada vez:** a gravata vermelha; quando o número entra no painel (verde a subir, vermelho a descer), a gravata sai de plano ou escurece.

**Proibido.** 3D, render, CGI, brilho, qualquer semelhança com personagens existentes ou de marca registada. As imagens de referência do fundador incluem uma personagem de marca registada: aproveita-se o princípio de forma, nada do desenho.

## 4. Cenário

Vertical 9:16, de frente, plano fixo de palco. Mesa escura pesada a atravessar o terço inferior, com caneca lascada e papéis. Parede suja em verde-acinzentado. Ao centro da parede, o **painel** numa moldura gasta, tipo painel de estação antiga, **sempre vazio no desenho** — é o gerador que escreve lá a carta, o preço e a variação a partir dos dados. Detalhes de baixo contraste: relógio torto, planta a morrer, tinta a descascar. Na mesa, o telefone.

## 5. O telefone e a Fonte

**O objeto.** Telefone de disco antigo, baquelite escura, auscultador no descanso, fio em espiral a cair da mesa. No centro do disco, onde ia o cartão dos números, uma **etiqueta redonda vazia no desenho**: o símbolo do BINDER é composto ali por cima pelo gerador, a partir do ficheiro oficial da marca. Nunca desenhado nem gerado.

**Quem atende.** A **Fonte**: a personagem que nunca aparece. Quando o Vinci precisa de confirmar um preço, comprar ou vender, pega no telefone e fala com ela.

**Regra central: a Fonte nunca se vê nem se ouve em palavras.** Nem voz, nem legenda, nem silhueta, nem sombra na parede — nunca, nem num especial. Só ouvimos o lado do Vinci, e o metal abafado do outro lado (§6). Três razões:

1. Custa zero: sem segunda voz, sem segundo design, sem créditos por episódio.
2. É mais engraçado: meia conversa obriga o espectador a montar a outra metade.
3. Abre lacuna: "quem é a Fonte?" é a pergunta que segura a série — e que morre no dia em que for respondida.

**O que o telefone faz pela narrativa.** Paga a dúvida: número → objeção → ele pega no telefone → a resposta chega na cara dele → uma frase de resultado. Transforma um boletim de preços numa cena com conflito, sem custo de produção.

**O que o telefone faz pela honestidade.** Toda a cotação que o Vinci diz veio de um telefonema, ou seja, de uma fonte. Quando não há fonte verificada para um número, **a Fonte não atende**: `telefone_nao_atende` é a forma como a série diz *não confirmado*, dentro da ficção, sem aviso colado no fim.

**Limites.** Um telefonema por episódio, no máximo. O telefonema nunca entrega o desfecho antes da explicação. O Vinci só repete fragmentos ("...quanto?", "...tens a certeza?", "...desde quando?"). A Fonte **confirma factos** — preço, data, praça, disponibilidade — e nunca dá dica, palpite ou recomendação de comprar ou vender.

**Easter egg (proposta).** O fio do telefone fica mais enrolado a cada episódio da temporada. Ninguém comenta. Registar em `comum/easter_eggs.md` se for aprovado.

## 6. Som da Fonte

Trombone com surdina de êmbolo a fazer de fala: metal abafado, com contorno de frase e nenhuma palavra. A técnica é antiga e genérica; esta voz é desenhada de raiz para o Vinci e não imita o motivo sonoro de nenhuma obra existente.

**Gerado localmente, custo zero:** `vinci/audio/fonte.py` sintetiza tudo (sem ElevenLabs, sem banco de sons). Frase nova = mais uma entrada no dicionário `FRASES` e correr o script. Ficheiros em `vinci/audio/saida/`.

| Ficheiro | Intenção |
|---|---|
| `fonte_pergunta` | "quê? quanto?" — contorno a subir |
| `fonte_confirma` | confirmação seca, a descer |
| `fonte_ma_noticia` | deslize longo a cair |
| `fonte_surpresa` | salto para cima |
| `fonte_ladainha` | seis sílabas a divagar; o Vinci afasta o auscultador da orelha |
| `fonte_corta_seco` | uma nota curta e seca; desligou |
| `fonte_hesita` | oscila antes de responder |
| `telefone_toque` | toque de telefone antigo |
| `telefone_nao_atende` | o toque a repetir e a cair — *não confirmado* |
| `telefone_pousa` | clique do auscultador no descanso |

## 7. Kit visual (estado)

| Peça | Estado |
|---|---|
| Base do personagem (desenho aprovado, limpo) | Escolhida com o fundador a 12/11; por integrar |
| Cenário com telefone | Escolhido com o fundador a 12/11; por integrar |
| Folha de nove poses | Gerada; por escolher e recortar |
| Bocas (fechada, "a", "o") e olhos (abertos, fechados) | Gerados; por escolher e recortar |
| Recortes PNG com transparência + `ancoras.json` | Por fazer |
| Som da Fonte | **Pronto** (`vinci/audio/`) |

**Poses previstas:** pitch de braços abertos · aponta o painel · choque a recuar · braços cruzados · palma na testa · confidência · contar dinheiro invisível · pegar no auscultador · ao telefone a ouvir.

**Movimento permitido, e só este:** piscar; empurrão de 2% na escala no primeiro quadro de cada pose nova; o número do painel a contar até ao valor final, uma vez por episódio. Tudo o resto é corte.

## 8. Fórmula do episódio (30–45 s)

1. **0–3 s:** o número, no painel e na voz, escrito desde o primeiro quadro.
2. **3–10 s:** que carta é, com o PNG do Scryfall e o crédito no rodapé.
3. **10–20 s:** a causa verificada. Uma só, com fonte e data.
4. **20–30 s:** a objeção e o telefonema à Fonte.
5. **30–40 s:** o que isso quer dizer para quem tem uma na pasta e para quem não tem.
6. **Fecho:** scanner (`comum/outro/outro_binder_916.mp4`).

## 9. Regra que protege a marca e as pessoas

É dinheiro real. **Nunca prever preço, nunca recomendar comprar ou vender, nunca criar urgência falsa.** Relatar o que aconteceu e porquê, com fonte, data e moeda em reais, e dizer quando a informação já pode ter mudado. Linha fixa na legenda: não é conselho de investimento. A personagem é um vendedor; o conteúdo não pode ser.

## 10. Por decidir pelo fundador

1. Voz do Vinci no ElevenLabs (descrição e autorização de créditos).
2. Nome público da série.
3. Cadência e dia de publicação.
4. Easter egg do fio do telefone: entra ou não.
