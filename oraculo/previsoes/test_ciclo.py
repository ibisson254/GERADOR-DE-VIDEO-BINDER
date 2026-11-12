#!/usr/bin/env python3
"""Testes do ciclo de previsões do TUBO (oraculo/previsoes/ciclo.py).

  python3 -I oraculo/previsoes/test_ciclo.py

Só biblioteca padrão + PyYAML (o mesmo que o ciclo.py exige). Não acede à internet,
não altera o registo real: testa sobre o registo real em modo leitura e sobre
registos sintéticos escritos em pasta temporária.
"""
import contextlib
import datetime as dt
import io
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import ciclo  # noqa: E402

FALHAS = []


def check(nome, cond, detalhe=""):
    print(("OK   " if cond else "FALHA") + f" {nome}" + (f" · {detalhe}" if detalhe and not cond else ""))
    if not cond:
        FALHAS.append(nome)


def capt(fn, *a):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(*a)
    return buf.getvalue()


# 1 · validar passa no registo real
r = subprocess.run([sys.executable, "-I", str(AQUI / "ciclo.py"), "validar"], capture_output=True, text=True)
check("validar passa no registo real", r.returncode == 0, r.stdout + r.stderr)

# 2 · continuacao mostra TODAS as abertas em qualquer dia da semana
prevs, _ = ciclo.carregar()
abertas = {p["id"] for p in ciclo.abertas(prevs)}
for dia in (dt.date(2026, 11, 11), dt.date(2026, 11, 14), dt.date(2026, 12, 25)):  # quarta, sábado, sexta distante
    saida = capt(ciclo.continuacao, dia)
    em_falta = [i for i in abertas if i not in saida]
    check(f"continuacao {dia} lista todas as abertas ({len(abertas)})", not em_falta, f"em falta: {em_falta}")

# 3 · continuacao destaca as promessas públicas (publicacao: publica)
saida = capt(ciclo.continuacao, dt.date(2026, 11, 12))
publicas = [p["id"] for p in ciclo.abertas(prevs) if p.get("publicacao") == "publica"]
check("continuacao destaca promessas ao público", all(i in saida.split("PRAZO VENCIDO")[0] for i in publicas))

# 4 · segunda e quinta continuam a correr (metodologia intacta)
check("segunda corre", "prestação de contas" in capt(ciclo.segunda, dt.date(2026, 11, 16)))
check("quinta corre", "previsão" in capt(ciclo.quinta, dt.date(2026, 11, 12)))

# 5 · registo sintético malformado: validar acusa, continuacao não rebenta
with tempfile.TemporaryDirectory() as tmp:
    t = Path(tmp)
    (t / "registo.yaml").write_text(textwrap.dedent("""\
        previsoes:
          - id: X-01
            episodio: EP
            data_registo: 2026-11-01
            publicacao: publica
            texto_original: "previsão sem critério"
            grau_certeza: 9
            prazo: 2026-10-01
            conferencias_marcadas: [2026-10-20]
            conferencias:
              - {data: 2026-11-02, estado: REFUTADA, muda_estado: true}
            estado: PENDENTE
          - id: X-01
            estado: ABERTA
        """), encoding="utf-8")
    (t / "calendario.yaml").write_text("eventos: []\n", encoding="utf-8")
    velho = ciclo.AQUI
    ciclo.AQUI = t
    try:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = ciclo.validar()
        v = buf.getvalue()
        check("validar acusa ID repetido", "ID repetido" in v)
        check("validar acusa grau fora de 1-5", "grau_certeza" in v)
        check("validar acusa prazo antes do registo", "prazo antes do registo" in v)
        check("validar acusa conferência marcada antes do registo", "conferência marcada" in v)
        check("validar acusa estado que não bate com a conferência", "não bate" in v)
        check("validar devolve 1 com erros", rc == 1)
        try:
            saida = capt(ciclo.continuacao, dt.date(2026, 11, 12))
            check("continuacao tolera registo malformado", "X-01" in saida)
        except Exception as e:
            check("continuacao tolera registo malformado", False, repr(e))
    finally:
        ciclo.AQUI = velho

# 6 · nenhuma previsão desaparece: fechadas aparecem como histórico
with tempfile.TemporaryDirectory() as tmp:
    t = Path(tmp)
    (t / "registo.yaml").write_text(textwrap.dedent("""\
        previsoes:
          - id: Y-01
            episodio: EP
            data_registo: 2026-10-01
            publicacao: registo
            texto_original: "fechada"
            grau_certeza: 3
            criterio: {fonte: f, confirma: c, refuta: r}
            prazo: 2026-10-10
            conferencias: []
            estado: REFUTADA
        """), encoding="utf-8")
    (t / "calendario.yaml").write_text("eventos: []\n", encoding="utf-8")
    velho = ciclo.AQUI
    ciclo.AQUI = t
    try:
        saida = capt(ciclo.continuacao, dt.date(2026, 11, 12))
        check("fechadas aparecem no histórico da continuacao", "Y-01" in saida and "REFUTADA" in saida)
    finally:
        ciclo.AQUI = velho

print()
if FALHAS:
    print(f"{len(FALHAS)} teste(s) falharam: {FALHAS}")
    sys.exit(1)
print("Todos os testes passaram.")
