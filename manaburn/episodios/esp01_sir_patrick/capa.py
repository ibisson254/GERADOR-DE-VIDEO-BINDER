"""Capa do Reel: o quadro do nome na TV, com o título no lugar da legenda (legível no feed e na grelha 3:4)."""
import pathlib
from playwright.sync_api import sync_playwright
root = pathlib.Path(__file__).parent.resolve()
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto((root/'homenagem.html').as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400); pg.wait_for_function('window.READY()')
    pg.evaluate('render(10.0)')
    pg.evaluate("""()=>{ const s=document.getElementById('sub'); s.style.bottom='470px'; s.style.fontSize='62px';
      s.innerHTML='Antes da carta chegar:<br><span class="k">obrigado, Sir Patrick.</span>'; s.dataset.h='x'; }""")
    pg.screenshot(path=str(root/'ManaBurn_Especial_SirPatrick_916_capa.jpg'), type='jpeg', quality=92)
    b.close()
print('ok')
