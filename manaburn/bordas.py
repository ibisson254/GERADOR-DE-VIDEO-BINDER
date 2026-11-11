"""Teste de bordas: a tela da TV nunca sai do vídeo nas laterais nem sobe por baixo dos créditos (quadro a quadro)."""
import json, pathlib
from playwright.sync_api import sync_playwright
d = json.loads(open('data.js').read().strip()[11:-1]); pts = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto(pathlib.Path('index.html').resolve().as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
    pg.wait_for_function('window.READY()')
    for i in range(int(d['T_SLAM'] * 30)):
        r = pg.evaluate(f"""(()=>{{ render({i / 30}); const tv=document.getElementById('shot2').style.display==='block';
          const m=document.getElementById(tv?'s2cam':'cam').getAttribute('transform').match(/translate\\(([-\\d.]+) ([-\\d.]+)\\) scale\\(([-\\d.]+)\\) translate\\(([-\\d.]+) ([-\\d.]+)\\)/);
          const [tx,ty,s,cx,cy]=m.slice(1).map(Number); const X=x=>tx+s*(x+cx), Y=y=>ty+s*(y+cy);
          return tv?[X(-24),X(1102),Y(610),Y(1323),1]:[X(640),X(1060),Y(518),Y(784),0]; }})()""")
        pts.append(r)
    b.close()
# regra: é proibido cortar a TV. Em cada quadro, o chassis inteiro está dentro do vídeo ou totalmente fora dele.
ruim = [p for p in pts if not ((p[0] >= 0 and p[1] <= 1080) or p[0] >= 1080 or p[1] <= 0)]
tv = [p for p in pts if p[4]]
print(f'{len(pts)} quadros · {len(tv)} de TV · chassis nos planos da TV entre {min(p[0] for p in tv):.0f} e {max(p[1] for p in tv):.0f} px · quadros com TV cortada: {len(ruim)}')
print('OK' if not ruim and min(p[2] for p in tv) >= 295 else 'FALHA')
