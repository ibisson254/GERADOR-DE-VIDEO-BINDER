"""Gera os slides 1080x1350 do carrossel a partir de carrossel.html (uso: python3 gerar_carrossel.py [pasta_saida])."""
import sys, pathlib
from playwright.sync_api import sync_playwright
R = pathlib.Path(__file__).parent.resolve(); out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else R / 'saida'); out.mkdir(exist_ok=True)
NOMES = ['01_capa', '02_armadilha1_rara', '03_armadilha2_cinco_cores', '04_armadilha3_borg', '05_armadilha4_naves', '06_armadilha5_dilema', '07_veredito', '08_pergunta_binder']
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--allow-file-access-from-files'])
    pg = b.new_page(viewport={'width': 1080, 'height': 1350}); pg.on('pageerror', lambda e: print('ERRO', e))
    pg.goto((R / 'carrossel.html').as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(800)
    for i in range(pg.evaluate('window.N')):
        el = pg.locator(f'#s{i + 1} > .S'); el.scroll_into_view_if_needed(); pg.wait_for_timeout(150)
        f = out / f'{NOMES[i]}.png'; el.screenshot(path=str(f)); print(f.name)
    b.close()
