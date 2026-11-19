# Lisa Marie no Ar · kit de produção

**Estado:** kit de pré-produção reutilizável v0.1 · integrado no repositório a 19/11/2026.  
**Ferramenta principal prevista:** Claude Pro.  
**Sem voz, música ou serviço externo aprovado.**

## 1. Objetivo do kit

Permitir que um episódio seja preparado reutilizando a mesma apresentadora, o mesmo estúdio, a mesma identidade gráfica e os mesmos movimentos. Cada episódio deve trocar apenas: a pauta, o material factual, as imagens autorizadas, os textos e a posição da personagem quando necessário.

## 2. Inventário

| Recurso | Caminho | Estado |
|---|---|---|
| Bíblia editorial | `CONTEXTO.md` | Integrada (19/11), em desenvolvimento |
| Perfil operacional | `PERFIL.md` | Integrado (19/11) |
| Guia visual | `IDENTIDADE_VISUAL.md` | v0.1 integrado (19/11) |
| Imagem-conceito VJ | `referencias/estudo_estudio_vj_2026-11-17.png` | Referência, não master |
| Foto dos óculos | `referencias/referencia_oculos_fundador.jpg` | Referência do fundador |
| Prancha «10 inspirações» + 10 recortes | `referencias/inspiracoes_2026-11-19/` | Conceito (19/11), não master |
| Recorte da prancha | `kit/ferramentas/recortar_prancha.py` | Script |
| Cartela de abertura | `kit/identidade/abertura_serie.svg` | SVG inicial |
| Tarja VJ | `kit/identidade/tarja_vj.svg` | SVG inicial |
| Identificador de canto | `kit/identidade/bug_programa.svg` | SVG inicial |
| Cartela do quadro | `kit/identidade/placa_elas_no_multiverso.svg` | SVG inicial |
| Fundo modular do estúdio | `kit/identidade/estudio_base.svg` | SVG inicial |
| Personagem-mestre transparente | a criar após ficha de modelo | Pendente |
| Folha de poses/expressões | a criar após personagem-mestre | Pendente |
| Cenário modular em camadas | a criar a partir do estudo | Pendente |
| Voz e assinatura sonora | por definir | Pendente / sem autorização de custo |

## 3. Estrutura de pastas recomendada

```text
lisa-marie/
  CONTEXTO.md
  PERFIL.md
  IDENTIDADE_VISUAL.md
  KIT_PRODUCAO.md
  PROMPT_CLAUDE.md
  kit/
    identidade/
      abertura_serie.svg
      tarja_vj.svg
      bug_programa.svg
      placa_elas_no_multiverso.svg
    personagem/
      lisa_marie_master.png       # criar depois da ficha de modelo
      lisa_marie_master.svg       # se o desenho vetorial for viável
      poses/                      # variações controladas
    estudio/
      fundo_estudio.svg           # criar em camadas
      monitores/                  # conteúdos substituíveis
  referencias/
    estudo_estudio_vj_2026-11-17.png
    referencia_oculos_fundador.jpg
    inspiracoes_2026-11-19/       # prancha de 10 looks + recortes
  episodios/
    lm-ep01_<tema>/
      ficha.md
      roteiro.md
      fontes.md
      assets/
      publicacao/
```

Os ficheiros renderizados finais não devem ser versionados no Git. O repositório guarda fontes, scripts, fichas, evidências e recursos mestres conforme a constituição.

## 4. Pipeline mínimo por episódio

1. Classificar o tema pelo router do `nucleo/SHOWRUNNER.md`.
2. Fazer auditoria de originalidade no registo editorial e executar `memoria.py pauta`.
3. Registar a pauta antes de pesquisa aprofundada.
4. Definir tese, público, pergunta de abertura e recompensa final.
5. Reunir fontes primárias e materiais visuais reais; obter autorizações para pessoa, voz, foto ou depoimento.
6. Escrever o guião em blocos VJ: pista → chamada → contexto → evidência → leitura → recompensa → fecho.
7. Montar primeiro o quadro 0 com Magic/TCG visível; só depois compor a abertura da apresentadora.
8. Substituir os conteúdos dos monitores e a tarja do convidado sem reconstruir o estúdio.
9. Montar cortes e movimentos a partir dos elementos existentes; mudança visual ≤3 s, sem cortes laterais.
10. Validar áudio, texto, fontes, autorizações, legibilidade e fecho comum BINDER.
11. Entregar capa, legenda, comentário fixado, texto alternativo, ficha de factos/fontes e ficheiros finais/localização.
12. Atualizar registo, histórico, STATUS e handoff; validar o repositório antes do commit.

## 5. Gramática de edição VJ

- **Abertura:** 0–3 s, assunto real no quadro 0; chamada verbal curta da Lisa.
- **Ponte:** tarja ou sinal de emissão a apresentar a pauta/convidada.
- **Material:** cartas, portefólio, imagem pública autorizada, prova ou arquivo.
- **Regresso da VJ:** comentário ou pergunta que acrescenta interpretação, não repetição.
- **Recompensa:** resposta à pergunta inicial.
- **Fecho:** uma pergunta ou ação; depois, o fecho comum definido na constituição.

Os tempos são guias de montagem, não uma duração obrigatória. A constituição prevalece e permite duração livre por episódio.

## 6. Modelo de guião

```text
QUADRO 0 — imagem real de Magic/TCG ou objeto da história
LISA (chamada): pergunta ou observação concreta
INSERT 1: prova visual correspondente
LISA (contexto): quem/que objeto e por que importa
INSERT 2: fonte, carta, portefólio ou material autorizado
LISA (leitura): interpretação explicitamente identificada
CONVIDADA (se houver): resposta aprovada/autorizada
INSERT 3: pagamento visual do gancho
LISA (fecho): conclusão + uma pergunta
OUTRO: fecho comum BINDER
```

## 7. Regras de economia

- Um cenário-mestre e uma personagem-mestre; não regenerar por episódio.
- Preferir planos 2D, recortes e pequenas translações a animação complexa.
- Reaproveitar tarjas, cartões, fundos e movimentos.
- Não criar uma vinheta longa; a abertura gráfica deve ser curta e não atrasar o quadro 0 de Magic.
- Não gerar imagens de recurso quando uma carta, portefólio ou prova real resolve.
- Não produzir música ou voz paga até autorização explícita.
- Claude Pro pode preparar textos, SVG, HTML/CSS/JS e a lógica dos elementos; confirmar a ferramenta de renderização efetivamente disponível antes de prometer um MP4. Não assumir FFmpeg, ElevenLabs, export de vídeo ou serviços que não tenham sido testados no ambiente.

## 8. Validação de qualidade

- O assunto de Magic/TCG é identificável imediatamente.
- O gancho é pago.
- A cada fala da Lisa corresponde evidência visual real.
- A convidada não é reduzida a pretexto para a mascote.
- Facto, inferência e opinião estão identificados.
- Fontes e datas registadas.
- Uso de imagens, voz e testemunhos autorizado.
- Consistência do modelo, dos óculos, da pelagem e da roupa-base.
- Texto legível em telemóvel; sem cortes laterais.
- Áudio não imita VJs, programas ou jingles conhecidos; direitos comerciais confirmados.
- Fecho comum BINDER incluído.

## 9. Bloqueios atuais

- A imagem VJ atual e a prancha de 10 looks são referência de atmosfera e figurino, não personagem-mestre reutilizável.
- A fotografia fornecida é referência dos óculos; não fornece uma fotografia da gata para reproduzir marcações específicas.
- Voz, fornecedor, música e efeitos finais não estão definidos.
- O modo real de renderização no ambiente Claude Pro precisa de ser testado antes de declarar o kit de vídeo concluído.
- O primeiro episódio e a pauta ainda não foram criados nem registados.
