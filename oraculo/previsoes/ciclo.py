#!/usr/bin/env python3
"""Briefing do ciclo semanal do TUBO (oraculo/CICLO_SEMANAL.md).

Uso:
  python3 -I oraculo/previsoes/ciclo.py continuacao [AAAA-MM-DD]   # qualquer dia: TODAS as previsões abertas + promessas ao público
  python3 -I oraculo/previsoes/ciclo.py segunda [AAAA-MM-DD]       # briefing de prestação de contas (CICLO_SEMANAL.md §3)
  python3 -I oraculo/previsoes/ciclo.py quinta  [AAAA-MM-DD]       # briefing de previsão (§4)
  python3 -I oraculo/previsoes/ciclo.py validar                    # valida o registo (sai 1 se houver erros)

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
    # Tolerante a campos em falta: um registo malformado lista-se na mesma (o `validar` acusa o erro).
    c = p.get("criterio") or {}
    try:
        prazo = f"{d(p['prazo']):%d/%m/%Y}"
    except Exception:
        prazo = f"?? ({p.get('prazo')})"
    return (f"  {p.get('id', '?')} · {p.get('publicacao', '?')} · grau {p.get('grau_certeza', '?')}/5 · prazo {prazo}\n"
            f"    original: {p.get('texto_original', '(FALTA texto_original)')}\n"
            f"    fonte: {c.get('fonte', '(FALTA)')}" + (f"\n    espelho: {c['fonte_espelho']}" if c.get("fonte_espelho") else "") +
            f"\n    confirma: {c.get('confirma', '(FALTA)')} · refuta: {c.get('refuta', '(FALTA)')}")


def ultima_conferencia(p):
    confs = p.get("conferencias") or []
    if not confs:
        return None
    try:
        return max(confs, key=lambda c: d(c["data"]))
    except Exception:
        return confs[-1]


def continuacao(dia):
    """O que o TUBO prometeu ao público e tudo o que está aberto — serve em QUALQUER dia da semana.

    Diferença para `segunda`: não filtra por janela semanal. Toda previsão PENDENTE aparece,
    tenha ou não conferência marcada para breve (CICLO_SEMANAL.md §0)."""
    prevs, evs = carregar()
    ab = abertas(prevs)
    vencidas = [p for p in ab if _prazo_ok(p) and d(p["prazo"]) <= dia]
    proximas = [p for p in ab if p not in vencidas and
                (_prox_conf(p, dia) is not None or
                 (_prazo_ok(p) and d(p["prazo"]) <= dia + dt.timedelta(days=7)))]
    restantes = [p for p in ab if p not in vencidas and p not in proximas]
    publicas = [p for p in ab if p.get("publicacao") == "publica"]
    fechadas = [p for p in prevs if p.get("estado") not in (None, "PENDENTE")]
    print(f"CONTINUAÇÃO {dia:%d/%m/%Y} · todas as previsões abertas (CICLO_SEMANAL.md §0)\n")
    print(f"PROMESSAS AO PÚBLICO (previsões ditas no vídeo/legenda, ainda abertas): {len(publicas)}")
    for p in publicas:
        fala = p.get("fala_no_video")
        print(f"  {p.get('id', '?')}: {fala or p.get('texto_original', '?')}")
    print()
    for titulo, grupo in (("PRAZO VENCIDO (auditoria final em falta)", vencidas),
                          ("CONFERÊNCIA OU PRAZO NOS PRÓXIMOS 7 DIAS", proximas),
                          ("RESTANTES ABERTAS (sem conferência próxima — não desaparecem)", restantes)):
        print(titulo + ":")
        for p in grupo:
            print(linha(p))
            uc = ultima_conferencia(p)
            if uc:
                print(f"    última conferência: {uc.get('data')} · {uc.get('dado', '')}")
            pc = _prox_conf(p, dia, limite=None)
            if pc:
                print(f"    próxima conferência marcada: {pc:%d/%m/%Y}")
        if not grupo:
            print("  nenhuma")
        print()
    print(f"JÁ FECHADAS (histórico, não reabrir): {', '.join(p.get('id', '?') + ' ' + str(p.get('estado')) for p in fechadas) or 'nenhuma'}")
    print("\nToda produção do TUBO começa aqui. Conferência nova: acrescentar linha em registo.yaml")
    print("(nunca editar texto_original) e correr: python3 -I oraculo/previsoes/ciclo.py validar")


def _prazo_ok(p):
    try:
        d(p["prazo"])
        return True
    except Exception:
        return False


def _prox_conf(p, dia, limite=7):
    """Próxima conferência marcada a partir de `dia` (inclusive). `limite` em dias; None = sem limite."""
    datas = []
    for c in p.get("conferencias_marcadas") or []:
        try:
            dc = d(c)
        except Exception:
            continue
        if dc >= dia and (limite is None or dc <= dia + dt.timedelta(days=limite)):
            datas.append(dc)
    return min(datas) if datas else None


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
        for c in p.get("conferencias_marcadas", []) or []:
            try:
                if d(c) < d(p["data_registo"]):
                    erros.append(f"{pid}: conferência marcada {c} antes do registo")
            except Exception:
                erros.append(f"{pid}: conferência marcada com data inválida ({c})")
        ultimo_estado = None
        for c in p.get("conferencias", []) or []:
            if c.get("estado") not in ESTADOS:
                erros.append(f"{pid}: conferência {c.get('data')} com estado inválido")
            if c.get("muda_estado") and c.get("estado") == "PENDENTE":
                erros.append(f"{pid}: conferência {c.get('data')} diz que muda o estado mas fica PENDENTE")
            try:
                if d(c["data"]) < d(p["data_registo"]):
                    erros.append(f"{pid}: conferência {c.get('data')} antes do registo")
            except Exception:
                erros.append(f"{pid}: conferência sem data válida")
            if c.get("muda_estado"):
                ultimo_estado = c.get("estado")
        if ultimo_estado and p.get("estado") != ultimo_estado:
            erros.append(f"{pid}: estado {p.get('estado')} não bate com a última conferência que muda estado ({ultimo_estado})")
    print("\n".join(erros) if erros else f"OK · {len(prevs)} previsões válidas")
    return 1 if erros else 0


if __name__ == "__main__":
    cmd, args = (sys.argv[1] if len(sys.argv) > 1 else ""), sys.argv[2:]
    if cmd == "segunda":
        segunda(hoje(args))
    elif cmd == "quinta":
        quinta(hoje(args))
    elif cmd in ("continuacao", "abertas"):  # qualquer dia: TODAS as abertas, sem filtro semanal
        continuacao(hoje(args))
    elif cmd == "validar":
        sys.exit(validar())
    else:
        print(__doc__)
        sys.exit(2)
