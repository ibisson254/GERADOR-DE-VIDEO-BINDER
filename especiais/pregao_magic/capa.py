#!/usr/bin/env python3
"""Capa do PREGÃO MAGIC: quadro do título + gancho numérico (1080x1920; grelha 3:4 segura entre y 240 e 1680)."""
import sys, render as R
cv = R.quadro(4.8)
R.texto_c(cv, "▼ −74,7%", 300, 1400, R.F("Black", 92), R.VERM, glow=R.VERM)
R.texto_c(cv, "▲ >3×", 800, 1400, R.F("Black", 92), R.VERDE, glow=R.VERDE)
R.texto_c(cv, "quem sobe, quem cai e por quê", 540, 1540, R.F("SemiBold", 44), R.BRANCO)
cv.convert("RGB").save(sys.argv[1] if len(sys.argv) > 1 else "capa_pregao_magic.png")
