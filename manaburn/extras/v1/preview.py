import sys, pathlib
from playwright.sync_api import sync_playwright
times = [float(x) for x in sys.argv[1:]] or [1.5]
root = pathlib.Path(__file__).parent
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.on('console', lambda m: print('console:', m.text))
    pg.on('pageerror', lambda e: print('ERRO:', e))
    pg.goto((root / 'index.html').as_uri())
    pg.evaluate('document.fonts.ready')
    pg.wait_for_timeout(300); pg.wait_for_function('window.READY()')
    for t in times:
        pg.evaluate(f'render({t})')
        pg.screenshot(path=str(root / f'prev_{t:05.2f}.png'))
    pass
    b.close()
