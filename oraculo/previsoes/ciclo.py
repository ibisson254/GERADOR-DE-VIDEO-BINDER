#!/usr/bin/env python3
"""Briefing do ciclo semanal do TUBO (oraculo/CICLO_SEMANAL.md).

Uso:
  python3 -I oraculo/previsoes/ciclo.py segunda [AAAA-MM-DD]
  python3 -I oraculo/previsoes/ciclo.py quinta  [AAAA-MM-DD]
  python3 -I oraculo/previsoes/ciclo.py validar

Não acede à internet: diz o que conferir e onde. O agente pesquisa com as ferramentas web.
"""
import sys
import datetime as dt
from pathlib import Path

import yaml

AQUI = Path(__file__).resolve().parent
ESTADOS = {"PENDENTE", "CONFIRMADA", "PARCIALMENTE CONFIRMADA", "REFUTADA", "INCONCLUSIVA"}
CRITERIO = ("fonte", "confirma", "refuta")


def carregar():
    reg = yaml.safe_load((AQUI / "registo.yaml").read_text(encoding="utf-8")) or {}
    cal = yaml.safe_load((AQUI / "calendario.yaml").read_text(encoding="utf-8")) or {}
    return reg.get("previsoes", []) or [], cal.get("eventos", []) or []


def d(x):
    return x if isinstance(x, dt.date) else dt.date.fromisoformat(str(x))


def hoje(args):
    return d(args[0]) if args else dt.date.today()


def abertas(prevs):
    return [p for p in prevs if p.get("estado") == "PENDENTE"]


def linha(p):
    c = p["criterio"]
    return (f"  {p['id']} · {p['publicacao']} · grau {p['grau_certeza']}/5 · prazo {d(p['prazo']):%d/%m/%Y}\n"
            f"    original: {p['texto_original']}\n"
            f"    fonte: {c['fonte']}" + (f"\n    espelho: {c['fonte_espelho']}" if c.get("fonte_espelho") else "") +
            f"\n    confirma: {c['confirma']} · refuta: {c['refuta']}")


def segunda(dia):
    prevs, evs = carregar()
    ini = dia - dt.timedelta(days=7)
    vencidas = [p for p in abertas(prevs) if d(p["prazo"]) <= dia]
    marcadas = [p for p in abertas(prevs) if p not in vencidas and
                any(ini < d(c) <= dia + dt.timedelta(days=1) for c in p.get("conferencias_marcadas", []))]
    quinta = [p for p in prevs if ini <= d(p["data_registo"]) < dia and p not in vencidas + marcadas]
    fim = [e for e in evs if ini <= d(e["fim"]) < dia]
    print(f"SEGUNDA {dia:%d/%m/%Y} · prestação de contas (CICLO_SEMANAL.md §3)\n")
    for titulo, grupo in (("AUDITORIA FINAL (prazo vencido)", vencidas),
                          ("PLACAR PARCIAL (conferência marcada)", marcadas),
                          ("REGISTADAS NA SEMANA (conferir mesmo sem prazo)", quinta)):
        print(titulo + ":")
        print("\n".join(linha(p) for p in grupo) if grupo else "  nenhuma")
        print()
    print("EVENTOS QUE ACABARAM NA SEMANA:")
    print("\n".join(f"  {e['nome']} ({d(e['inicio']):%d/%m}–{d(e['fim']):%d/%m}) · {e['fonte']}" for e in fim) or "  nenhum")
    if not (vencidas or marcadas or quinta):
        print("\nNada a conferir: segunda segue como episódio normal (Leitura da Final / Relatório do Meta).")
    print("\nDepois: conferência nova em registo.yaml (nunca editar texto_original) → roteiro (§5) → validar.")


def quinta(dia):
    prevs, evs = carregar()
    sexta, domingo = dia + dt.timedelta(days=1), dia + dt.timedelta(days=3)
    seg = dia + dt.timedelta(days=4)
    fds = [e for e in evs if d(e["inicio"]) <= domingo and d(e["fim"]) >= sexta]
    print(f"QUINTA {dia:%d/%m/%Y} · previsão (CICLO_SEMANAL.md §4)\n")
    print(f"EVENTOS DE {sexta:%d/%m} A {domingo:%d/%m} (confirmar na web; acrescentar os que faltarem):")
    for e in fds:
        print(f"  {e['nome']} · {', '.join(e.get('formatos', []))} · {e['fonte']}")
        if e.get("notas"):
            print(f"    notas: {e['notas']}")
    if not fds:
        print("  nenhum no calendário: procurar em magic.gg, calendário do Arena, MTGO e organizadores (SCG, Hareruya, RC).")
    print(f"\nPREVISÕES ABERTAS COM CONFERÊNCIA NA SEGUNDA {seg:%d/%m}:")
    cont = [p for p in abertas(prevs) if seg in [d(c) for c in p.get("conferencias_marcadas", [])] or d(p["prazo"]) <= seg]
    print("\n".join(linha(p) for p in cont) or "  nenhuma")
    print("\nPESQUISAR: fonte oficial (formatos, convidados, listas) → dados com amostra → análises atribuídas → comunidade.")
    print(f"FECHAR: 1 previsão pública + até 3 de registo, com prazo de preferência {seg:%d/%m/%Y}, em registo.yaml ANTES da voz.")
    print("Depois: python3 -I oraculo/previsoes/ciclo.py validar")


def validar():
    prevs, _ = carregar()
    erros, ids = [], set()
    for p in prevs:
        pid = p.get("id", "?")
        if pid in ids:
            erros.append(f"{pid}: ID repetido")
        ids.add(pid)
        for k in ("episodio", "data_registo", "publicacao", "texto_original", "grau_certeza", "criterio", "prazo", "estado"):
            if p.get(k) in (None, ""):
                erros.append(f"{pid}: falta {k}")
        g = p.get("grau_certeza")
        if not isinstance(g, int) or not 1 <= g <= 5:
            erros.append(f"{pid}: grau_certeza tem de ser inteiro 1–5")
        if "%" in str(p.get("grau_certeza", "")):
            erros.append(f"{pid}: grau sem percentagem")
        for k in CRITERIO:
            if not (p.get("criterio") or {}).get(k):
                erros.append(f"{pid}: critério sem '{k}' (sem critério é opinião, não previsão)")
        if p.get("estado") not in ESTADOS:
            erros.append(f"{pid}: estado inválido {p.get('estado')}")
        if p.get("publicacao") not in ("publica", "registo"):
            erros.append(f"{pid}: publicacao tem de ser publica ou registo")
        try:
            if d(p["prazo"]) < d(p["data_registo"]):
                erros.append(f"{pid}: prazo antes do registo")
        except Exception:
            erros.append(f"{pid}: datas inválidas")
        for c in p.get("conferencias", []) or []:
            if c.get("estado") not in ESTADOS:
                erros.append(f"{pid}: conferência {c.get('data')} com estado inválido")
            if c.get("muda_estado") and c.get("estado") == "PENDENTE":
                erros.append(f"{pid}: conferência {c.get('data')} diz que muda o estado mas fica PENDENTE")
    print("\n".join(erros) if erros else f"OK · {len(prevs)} previsões válidas")
    return 1 if erros else 0


if __name__ == "__main__":
    cmd, args = (sys.argv[1] if len(sys.argv) > 1 else ""), sys.argv[2:]
    if cmd == "segunda":
        segunda(hoje(args))
    elif cmd == "quinta":
        quinta(hoje(args))
    elif cmd == "validar":
        sys.exit(validar())
    else:
        print(__doc__)
        sys.exit(2)
