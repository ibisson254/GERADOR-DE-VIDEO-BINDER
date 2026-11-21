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
- Piloto LM-EP00 (sem voz) em produção desde 21/11; arte da personagem ainda é conceito.

## 10. Fluxo com filmagem urbana (desde 21/11/2026)

Decisão do fundador (`nucleo/DECISOES.md`, 21/11): recorte 2D + Rhubarb + filmagem urbana real. Primeiro uso: LM-EP00 (`episodios/lm-ep00_piloto_mulheres_da_alpha/`).

1. **Pauta e factos** primeiro (`memoria.py pauta`, ficha com o gancho §4.1 e as fontes).
2. **Cartas:** `cartas.py` do episódio (Scryfall, PNG 745×1040, não versionadas, nunca ampliadas).
3. **Camadas da Lisa:** `kit/prova_recorte/` (arte-conceito; trocar pela arte definitiva quando existir).
4. **Fundo:** clipes de `biblioteca_urbana/clipes/` com o nome do `manifesto.csv`. Sem clipe, o motor desenha um fundo provisório assinalado no quadro, e esse vídeo não é publicável.
5. **Música:** só com a licença registada em `biblioteca_urbana/musica.csv`. Sem música, o ficheiro sai só com SFX e a música entra pela biblioteca do Instagram.
6. **Render:** `python3 -I lisa-marie/motor/piloto_lm_ep00.py --camadas DIR --cartas DIR [--musica F.mp3] --saida F.mp4`, com `--previa` para a folha de fotogramas. O motor junta o fecho comum e normaliza a −14 LUFS. Conferir o pico (< −1 dBFS) no ficheiro final.
7. **Troca de carta:** rotação 3D no eixo Y (0,34 s), a mesma técnica do Meta em Curto, reimplementada.

### Direção musical (não é trilha oficial)

Assinatura original a criar: eletrónica alternativa, baixo quente, percussão leve, textura analógica, uma pequena frase de sintetizador e um sinal de emissão próprio. Os anos 90 entram pela energia e pela textura, nunca copiando uma música, um artista ou um jingle. Nada de MTV, programas conhecidos ou música comercial. Até haver trilha aprovada usa-se: (a) SFX originais do motor e (b) faixas de biblioteca com licença registada, como provisórias. «Hazy After Hours» (Mixkit, Alejandro Magaña) no LM-EP00.
