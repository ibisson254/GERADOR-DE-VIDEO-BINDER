# Eventos do ciclo de vida · `episode.completed`

Criado a 28/11/2026 (`nucleo/DECISOES.md`; desenho em `nucleo/auditorias/2026-11-28_integracao_data_binder.md` §6). Ferramenta: `comum/ferramentas/eventos.py` (só biblioteca padrão, 0 créditos, sem rede).

**Para que serve:** quando um episódio fica pronto, o Data Binder fica a saber sem ninguém copiar nada à mão, e o registo editorial passa a CONCLUÍDO no mesmo passo. Não é um segundo sistema de analytics: as métricas continuam em `comum/insights/registo_posts.csv`.

## Fluxo

0. **Vozes autorizadas = publicado** (fundador, 28/11/2026 08:05). No momento em que o fundador autoriza as vozes: `python3 comum/ferramentas/eventos.py vozes <ID> --data <data> --fonte "<palavras dele, data, onde>"`. O registo passa a PUBLICADO (data exata do post por confirmar).

1. Render do vídeo final.
2. `python3 -I comum/qc/qc_video.py VIDEO.mp4 --frente <frente>` → `qc_<video>/qc.json`. P0 bloqueia.
3. **O fundador aprova** e fica escrito na ficha, numa linha própria:
   `- Aprovação final: <nome> · <AAAA-MM-DD ou DD/MM/AAAA>`
   Só o fundador a escreve, ou a sessão copia as palavras dele com a fonte. O modelo nunca aprova: o script recusa nomes como «Claude», «modelo», «agente».
4. `python3 comum/ferramentas/eventos.py concluir <ID> --qc <caminho>/qc.json`
   Confere QC, aprovação e o pacote (`memoria.py encerramento`), grava o evento e passa o registo de APROVADO/EM PRODUÇÃO/CONCLUÍDO a PUBLICADO (um PUBLICADO fica como está). Repetir não duplica.
5. `python3 comum/ferramentas/eventos.py sincronizar --destino <clone do Data Binder>/entradas`
   Entrega os pendentes em `originals_episodios.jsonl`. Se falhar, o evento fica pendente e a tentativa fica registada; corre-se outra vez mais tarde.

## Ficheiros (append-only)

| Ficheiro | Conteúdo |
|---|---|
| `episodios.jsonl` | um evento por linha: event_id (sha256 de episódio + tipo + versão), episode_id, series_id, production_status, approval_status, approved_by, qc_status, created_at, completed_at, video_path, duration_s, format, resolution, fps, creative_attributes, source_branch, event_version |
| `sync.jsonl` | cada tentativa: event_id, estado (`sincronizado` ou `falhou`), em, erro |

Campo sem fonte fica `null` (ex.: `created_at` vem do commit que criou a ficha; `duration_s`, `resolution` e `fps` vêm do qc.json). Nunca se estima.

## Outros comandos

- `eventos.py pendentes`: o que falta sincronizar.
- `eventos.py metricas <ID>`: leituras do `registo_posts.csv` com id, período, fonte e definição de cada métrica; célula vazia sai `null`.
- `eventos.py validar`: campos, ids determinísticos, duplicados, episódio no registo (corre no workflow `validar`).

## Testes

`python3 -I comum/ferramentas/test_eventos.py`: os 10 casos da missão de 28/11 (conclusão normal, duplicado, falha de sync, sem aprovação, QC falhado, reconciliação histórica, métrica ausente, consulta com contexto, validações cruzadas, reexecução). Só mocks.
