# Ciclo semanal · Meta em Curto (TUBO)

v1 · 09/11/2026 · pedido do fundador registado em `../nucleo/DECISOES.md` (09/11/2026).

Os dois episódios semanais do TUBO formam um ciclo fechado: **quinta prevê, segunda presta contas.** Toda previsão fica guardada antes de ir ao ar, com o critério e a data de conferência, para que o episódio de segunda saia sem perguntas ao fundador. Não muda nada da identidade (`CONTEXTO.md`). Para coleções novas, o método das previsões é o `PROTOCOLO_PRE_RELEASE.md` (branch `protocolo-pre-release-tubo`, ainda fora da `main`); este documento só define o ritmo.

## 0. Regra geral (10/11/2026)

**Toda previsão do TUBO entra em `previsoes/registo.yaml`**, em qualquer dia e em qualquer peça (episódio, especial, Giro, carrossel, legenda ou comentário fixado), antes de gravar a voz. E **toda produção do TUBO começa por ler o registo**: `python3 -I oraculo/previsoes/ciclo.py continuacao` (igual a `segunda`, serve em qualquer dia). O fundador não tem de dizer que previsões estão abertas nem de que episódio é a continuação: está no registo. Pedidos como «continuação», «prestação de contas» ou o envio de um episódio antigo seguem a secção 3.

## 1. Ficheiros

| Ficheiro | Função |
|---|---|
| `previsoes/registo.yaml` | Registo único de previsões do TUBO: ID, texto original, critério, prazo, conferências, estado. Fonte de verdade. |
| `previsoes/calendario.yaml` | Eventos com data (torneios, lançamentos, prazos de auditoria). Só entra o que tem fonte. |
| `previsoes/ciclo.py` | Gera o briefing: `segunda`, `quinta`, `validar`. Não acede à internet; diz o que pesquisar e onde. |

`comum/historico.md` deixa de repetir a tabela de previsões: aponta para o registo.

## 2. Palavras de arranque

| O fundador escreve | O agente faz |
|---|---|
| `tubo segunda` (ou "episódio de segunda") | `python3 -I oraculo/previsoes/ciclo.py segunda` → secção 3 |
| `tubo quinta` (ou "episódio de quinta") | `python3 -I oraculo/previsoes/ciclo.py quinta` → secção 4 |

Sem data no pedido, usa-se a data do dia (fuso Europe/Lisbon).

## 3. Segunda · Prestação de contas

Objetivo: voltar às previsões de quinta (e às de prazo longo com conferência marcada) e dizer, com dado, como estão.

1. Correr `ciclo.py segunda`. Lista: previsões com prazo vencido (auditoria final), previsões com conferência marcada para a semana (placar parcial) e eventos do fim de semana anterior.
2. Para cada previsão listada, ir às fontes do campo `criterio.fonte` (WebFetch/WebSearch; se a fonte estiver bloqueada, usar `fonte_espelho` quando existir e dizê-lo no ecrã; sem fonte, constituição §11).
3. Atribuir o estado (PENDENTE · CONFIRMADA · PARCIALMENTE CONFIRMADA · REFUTADA · INCONCLUSIVA) **só** com evidência do tipo que o critério aceita. Relato (R) e opinião (O) entram como contexto, nunca mudam estado.
4. Escrever a conferência em `registo.yaml` (`conferencias:` nova linha; o `texto_original` nunca se edita).
5. Roteiro de prestação de contas (secção 5). Previsão pública refutada = «Erro de sistema».
6. Se o fim de semana teve torneio grande sem previsão, a segunda pode juntar uma Leitura da Final ou um Relatório do Meta; a prestação de contas vem primeiro.

Se nada mensurável chegou: o episódio diz isso (placar parcial, estado PENDENTE, grau de certeza igual). Não se estima nada no lugar do dado.

## 4. Quinta · Previsão

Objetivo: antes do fim de semana, prever o que vai ser conferido na segunda seguinte.

1. Correr `ciclo.py quinta`. Lista: eventos de sexta a domingo no `calendario.yaml`, previsões abertas que pedem conferência e o que a quinta tem de pesquisar.
2. Confirmar o calendário do fim de semana na web (magic.gg, calendário do Arena, MTGO, organizadores). Evento novo com fonte entra no `calendario.yaml`.
3. Pesquisar pela ordem: fonte oficial (formatos, listas publicadas, convidados) → dados com amostra (MTGGoldfish, MTGTop8, MTGO, 17Lands/MTGMeta) → análises atribuídas → comunidade.
4. Fechar 1 previsão pública (no vídeo) e até 3 de registo. Cada uma entra em `registo.yaml` **antes** de gravar a voz, com:
   - texto original numa frase verificável;
   - critério: fonte, recorte, o que confirma, o que confirma em parte, o que refuta;
   - prazo: de preferência a segunda seguinte (auditável no episódio de segunda);
   - grau de certeza 1–5 (escala do protocolo §5), nunca em percentagem.
5. `ciclo.py validar` tem de passar. Previsão sem critério não entra (é opinião).

## 5. Formato dos episódios

Estrutura e identidade de `CONTEXTO.md` §7, sem alterações. Peças fixas do ciclo:

- **Segunda:** cabeçalho `ARQUIVO: <ID> · registrada <data> · estado: <ESTADO>`; o texto original no terminal com o carimbo «TEXTO ORIGINAL · NÃO EDITADO»; placar (dado com fonte e data) ou «0 jogos»/«sem dados»; evidência recebida com o tipo (R/O/D/E) e «muda o placar? sim/não»; medidor GRAU DE CERTEZA; próxima conferência.
- **Quinta:** cartão «PREVISÃO REGISTRADA» com ID, critério resumido e data da conferência; o ID vai no comentário fixado.
- Fecho igual em ambos: pergunta competitiva + «Probabilidade calculada. Humanos, imprevisíveis.» + fecho do scanner.

## 6. Previsões de prazo longo

Prazos depois da segunda seguinte (ex.: auditoria de coleção a 01/12) levam `conferencias_marcadas`: uma por segunda até ao prazo. Cada conferência intermédia é «placar parcial», nunca auditoria; o estado só fecha no prazo, salvo se o critério disser outra coisa.
