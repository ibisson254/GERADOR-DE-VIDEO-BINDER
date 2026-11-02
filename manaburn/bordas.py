"""Teste de bordas: a tela da TV nunca sai do vídeo nas laterais nem sobe por baixo dos créditos (quadro a quadro)."""
import json, pathlib
from playwright.sync_api import sync_playwright
d = json.loads(open('data.js').read().strip()[11:-1]); pts = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto(pathlib.Path('index.html').resolve().as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
    pg.wait_for_function('window.READY()')
    for i in range(int(d['T_SLAM'] * 30)):
        r = pg.evaluate(f"""(()=>{{ render({i / 30}); if(document.getElementById('shot2').style.display!=='block') return null;
          const m=document.getElementById('s2cam').getAttribute('transform').match(/translate\\(([-\\d.]+) ([-\\d.]+)\\) scale\\(([-\\d.]+)\\) translate\\(([-\\d.]+) ([-\\d.]+)\\)/);
          const [tx,ty,s,cx,cy]=m.slice(1).map(Number); return [tx+s*(79+cx), tx+s*(783+cx), ty+s*(682+cy)]; }})()""")
        if r: pts.append(r)
    b.close()
l, rr, top = min(x[0] for x in pts), max(x[1] for x in pts), min(x[2] for x in pts)
print(f'{len(pts)} quadros de TV · laterais entre {l:.0f} e {rr:.0f} px · topo da TV a partir de {top:.0f} px')
print('OK' if l >= 0 and rr <= 1080 and top >= 295 else 'FALHA')
