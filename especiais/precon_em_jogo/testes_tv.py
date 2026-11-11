# Testes da TV analógica: quadros consecutivos diferentes, determinismo, limite do vidro. Uso: python3 esp/testes_tv.py (na pasta do kit)
from playwright.sync_api import sync_playwright
import pathlib,hashlib
JS="(t)=>{render(t);const c=document.getElementById(document.getElementById('shot2').style.display==='block'?'ncS':'ncW');return c.toDataURL()}"
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.goto(pathlib.Path('index.html').resolve().as_uri());pg.wait_for_timeout(500);pg.wait_for_function('window.READY()')
    h=[hashlib.md5(pg.evaluate(JS,22+i/30).encode()).hexdigest() for i in range(30)]
    print('30 quadros consecutivos, distintos:',len(set(h)))
    print('determinístico:',hashlib.md5(pg.evaluate(JS,22+3/30).encode()).hexdigest()==h[3] and hashlib.md5(pg.evaluate(JS,22+17/30).encode()).hexdigest()==h[17])
    import time;s=time.time()
    for i in range(60): pg.evaluate(JS,30+i/30)
    print('ms por quadro (com toDataURL):',round((time.time()-s)/60*1000))
    b.close()
