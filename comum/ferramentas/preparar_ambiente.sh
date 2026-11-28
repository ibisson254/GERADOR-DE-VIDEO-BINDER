#!/bin/sh
# Prepara uma sessão nova (cloud ou PC) para renderizar e validar, num só comando (27/11/2026).
# Antes: cada sessão reinstalava à mão (e o num2words falhava ao compilar o docopt; ver a memória do projeto).
# Uso: sh comum/ferramentas/preparar_ambiente.sh [--sem-fontes]
# Idempotente: só instala o que falta. Não gasta créditos nem toca em ficheiros versionados
# (as fontes vão para lambe-lambe/kit_carrossel/fontes/, que está no .gitignore).
set -e
R="$(cd "$(dirname "$0")/../.." && pwd)"
PY="${PYTHON:-python3}"

echo "· Python: $($PY --version 2>&1)"
if ! $PY -c "import numpy, scipy, PIL, cv2, playwright, yaml, fontTools, brotli, num2words" 2>/dev/null; then
  echo "· a instalar dependências Python (comum/ferramentas/requisitos.txt)"
  $PY -m pip install -q -r "$R/comum/ferramentas/requisitos.txt"
  $PY -m pip install -q --no-deps num2words
fi
$PY -c "import numpy, scipy, PIL, cv2, playwright, yaml, num2words; print('· Python OK (opencv', cv2.__version__ + ')')"

for b in ffmpeg ffprobe; do
  command -v $b >/dev/null 2>&1 && echo "· $b OK" || echo "! $b em falta: instalar pelo sistema (apt install ffmpeg / winget install ffmpeg)"
done

if [ -n "$CHROME" ] && [ -x "$CHROME" ]; then echo "· Chrome: $CHROME (variável CHROME)"
elif [ -x /usr/bin/google-chrome ]; then echo "· Chrome: /usr/bin/google-chrome"
else echo "! Chrome do sistema não encontrado: os kits usam o Chromium do Playwright (python3 -m playwright install chromium) ou CHROME=<caminho>"
fi

if [ -f "$R/lambe-lambe/kit_carrossel/fontes/desgaste.png" ]; then echo "· fontes do Lambe-lambe OK"
elif [ "$1" = "--sem-fontes" ]; then echo "· fontes do Lambe-lambe não instaladas (--sem-fontes)"
elif command -v npm >/dev/null 2>&1; then sh "$R/lambe-lambe/kit_carrossel/preparar_fontes.sh"
else echo "! npm em falta: fontes do Lambe-lambe não instaladas (lambe-lambe/kit_carrossel/preparar_fontes.sh)"
fi
fc-list 2>/dev/null | grep -qi "Noto.*CJK" || echo "! Noto Serif CJK em falta: o kanji do Lambe-lambe (ex.: LL-ART21) sai noutra fonte; apt install fonts-noto-cjk"
echo "· pronto. Validação: python3 -I comum/ferramentas/validar_repo.py && python3 comum/ferramentas/memoria.py validar"
