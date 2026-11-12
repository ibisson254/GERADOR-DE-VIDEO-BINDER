"""Quadros soltos para conferir: python3 previa.py 1.0 9.0 ..."""
import sys, pathlib
from playwright.sync_api import sync_playwright
root = pathlib.Path(__file__).parent.resolve(); out = root/'previa'; out.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    erros = []; pg.on('pageerror', lambda e: erros.append(str(e)))
    pg.goto((root/'giro.html').as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400); pg.wait_for_function('window.READY()')
    for a in sys.argv[1:]:
        pg.evaluate(f'render({float(a)})'); pg.screenshot(path=str(out/f'q_{float(a):05.2f}.jpg'), type='jpeg', quality=85)
    b.close()
print('erros:', erros or 'nenhum')
