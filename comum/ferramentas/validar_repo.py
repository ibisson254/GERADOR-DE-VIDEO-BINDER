#!/usr/bin/env python3
"""Relatório de integridade do repositório do Estúdio BINDER.

  python3 -I comum/ferramentas/validar_repo.py [--raiz PASTA]

Verifica o que a máquina consegue verificar, sem alterar nada:
  A. series.yaml: todos os caminhos referidos existem (perfil, identidade, técnico, trilhas, referência, fecho).
  B. Sintaxe de todos os .py do repositório.
  C. Imports locais em falta (módulos do estúdio citados mas sem ficheiro ao lado).
  D. Vídeos versionados fora da exceção do fecho (constituição §7: nunca commitar renders).
  E. Ligações internas quebradas nos .md (apenas caminhos relativos para dentro do repositório).
  F. Padrões de segredos (chaves API, tokens) em ficheiros de texto. Nunca imprime o valor.

Gravidade: P0 = bloqueia (segredos, sintaxe) · P1 = corrigir (caminhos/imports/links quebrados) · P2 = aviso.
Sai com 1 se houver P0 ou P1; 0 caso contrário. Problemas conhecidos e aceites estão em ACEITES.
"""
import argparse
import ast
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

# Limitações conhecidas, documentadas em STATUS.md (episódios publicados não se reabrem).
ACEITES = {
    "oraculo/episodios/ep01_render_v2.py",   # importa `render` (ficou no projeto claude.ai)
    "manaburn/episodios/ep09_dack/process.py",  # importa trilha/roteiro/cortes (motor no projeto claude.ai)
    "conde/montar_ep002.py",                 # caminho absoluto, episódio publicado
}
MODULOS_LOCAIS = {"render", "formatos", "copys", "roteiro", "scryfall", "montar", "lote",
                  "testes", "cortes", "trilha", "bordas", "luz", "patch", "lib"}
SEGREDOS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{30,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]
TEXTO = {".py", ".js", ".md", ".yaml", ".yml", ".txt", ".json", ".html", ".srt", ".csv", ".sh"}


def rel(p, raiz):
    return str(p.relative_to(raiz)).replace("\\", "/")


def caminhos_yaml(no):
    """Extrai valores que parecem caminhos de ficheiro do series.yaml."""
    if isinstance(no, dict):
        for v in no.values():
            yield from caminhos_yaml(v)
    elif isinstance(no, list):
        for v in no:
            yield from caminhos_yaml(v)
    elif isinstance(no, str) and "/" in no and " " not in no and not no.startswith(("http", "Drive:")):
        yield no


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", default=None)
    args = ap.parse_args()
    raiz = Path(args.raiz) if args.raiz else Path(__file__).resolve().parents[2]
    problemas = []  # (gravidade, mensagem)

    def add(grav, msg):
        problemas.append((grav, msg))

    ficheiros = [p for p in raiz.rglob("*") if p.is_file() and ".git" not in p.parts and "node_modules" not in p.parts]

    # A · series.yaml
    sy = raiz / "series.yaml"
    if yaml is None:
        add("P2", "PyYAML indisponível: series.yaml não verificado")
    elif sy.exists():
        dados = yaml.safe_load(sy.read_text(encoding="utf-8"))
        for c in set(caminhos_yaml(dados)):
            if not (raiz / c).exists():
                add("P1", f"series.yaml aponta para caminho inexistente: {c}")
    else:
        add("P1", "series.yaml não encontrado")

    # B + C · Python
    for p in ficheiros:
        if p.suffix != ".py":
            continue
        r = rel(p, raiz)
        txt = p.read_text(encoding="utf-8", errors="replace")
        try:
            ast.parse(txt, filename=r)
        except SyntaxError as e:
            add("P0", f"erro de sintaxe: {r}:{e.lineno}")
            continue
        if r in ACEITES:
            continue
        for m in re.finditer(r"^(?:from|import)\s+([A-Za-z_]\w*)", txt, re.M):
            mod = m.group(1)
            if mod in MODULOS_LOCAIS and not (p.parent / f"{mod}.py").exists():
                add("P1", f"import local em falta: {r} importa '{mod}'")

    # D · vídeos versionados
    for p in ficheiros:
        if p.suffix.lower() in {".mp4", ".mov", ".avi", ".mkv", ".webm"}:
            r = rel(p, raiz)
            if r != "comum/outro/outro_binder_916.mp4":
                add("P1", f"vídeo versionado fora da exceção do fecho: {r}")

    # E · ligações internas nos .md
    re_link = re.compile(r"\]\(([^)#\s]+)(?:#[^)\s]*)?\)")
    for p in ficheiros:
        if p.suffix != ".md":
            continue
        for m in re_link.finditer(p.read_text(encoding="utf-8", errors="replace")):
            alvo = m.group(1)
            if alvo.startswith(("http", "mailto:", "computer:")) or "`" in alvo:
                continue
            destino = (p.parent / alvo).resolve()
            try:
                destino.relative_to(raiz.resolve())
            except ValueError:
                continue
            if not destino.exists():
                add("P1", f"ligação quebrada em {rel(p, raiz)}: {alvo}")

    # F · segredos
    for p in ficheiros:
        if p.suffix.lower() not in TEXTO or rel(p, raiz) == "comum/ferramentas/validar_repo.py":
            continue
        txt = p.read_text(encoding="utf-8", errors="replace")
        for rx in SEGREDOS:
            if rx.search(txt):
                add("P0", f"possível segredo em {rel(p, raiz)} (padrão {rx.pattern[:20]}…); valor não mostrado")
                break

    for grav in ("P0", "P1", "P2"):
        grupo = [m for g, m in problemas if g == grav]
        if grupo:
            print(f"\n{grav} ({len(grupo)}):")
            print("\n".join(f"  - {m}" for m in grupo))
    if not problemas:
        print("OK · nenhum problema encontrado")
    graves = [g for g, _ in problemas if g in ("P0", "P1")]
    print(f"\nResumo: {len(problemas)} problema(s), {len(graves)} grave(s). Aceites documentados: {len(ACEITES)}.")
    return 1 if graves else 0


if __name__ == "__main__":
    sys.exit(main())
