"""Renderiza um intervalo de quadros: python3 quadros.py INICIO FIM (salta os que já existem)"""
import pathlib, sys
from playwright.sync_api import sync_playwright
root = pathlib.Path(__file__).parent.resolve(); FPS = 30
a, b = int(sys.argv[1]), int(sys.argv[2]); frames = root/'frames'; frames.mkdir(exist_ok=True)
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 1080, 'height': 1920})
    pg.on('pageerror', lambda e: print('ERRO:', e, flush=True))
    pg.goto((root/'giro.html').as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400); pg.wait_for_function('window.READY()')
    for i in range(a, b):
        f = frames/f'{i:05d}.jpg'
        if f.exists() and f.stat().st_size > 0: continue
        pg.evaluate(f'render({i / FPS})'); pg.screenshot(path=str(f), type='jpeg', quality=92)
        if i % 200 == 0: print('quadro', i, flush=True)
    br.close()
print('ok', a, b, flush=True)
