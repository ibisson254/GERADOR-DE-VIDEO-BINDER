"""Renderiza com a cena do kit Mana & Burn (mb/index.html) os quadros do sofá e os quadros das falas do Burn e do Mana
usados no PIP das cenas de cartas. Saída: mb_frames/<n>.jpg (n = quadro do vídeo final, 30 fps).
uso: python3 render_mb.py
"""
import json, pathlib
from playwright.sync_api import sync_playwright
FPS = 30
tl = json.load(open('tl.json'))
need = set()
for c in tl['cenas']:
    if c['nome'] in ('sofa1', 'zero', 'sofa2'):
        need.update(range(int(c['a'] * FPS), int(round(c['b'] * FPS)) + 1))
for f in tl['falas']:
    if f['quem'] in 'BM':
        need.update(range(int((f['start'] - 0.1) * FPS), int((f['start'] + f['dur'] + 0.15) * FPS) + 1))
out = pathlib.Path('mb_frames'); out.mkdir(exist_ok=True)
todo = sorted(n for n in need if not (out / f'{n:05d}.jpg').exists())
print('quadros a renderizar:', len(todo), 'de', len(need))
root = pathlib.Path('mb').resolve()
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.on('pageerror', lambda e: print('ERRO:', e))
    pg.goto((root / 'index.html').as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(500)
    pg.wait_for_function('window.READY()')
    for k, n in enumerate(todo):
        pg.evaluate(f'render({n / FPS})'); pg.screenshot(path=str(out / f'{n:05d}.jpg'), type='jpeg', quality=90)
        if k % 300 == 0: print('quadro', k, flush=True)
    b.close()
print('ok')
