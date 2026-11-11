import pathlib, json
from playwright.sync_api import sync_playwright
root=pathlib.Path('.').resolve(); d=json.loads((root/'data.js').read_text().strip()[11:-1]); n=int(round(d['T_END']*30))
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920}); pg.goto((root/'index.html').as_uri()); pg.wait_for_timeout(300)
    prev=None; trocas=[]; ruins=[]
    for i in range(n):
        r=pg.evaluate(f"""(()=>{{render({i}/30); const im=document.getElementById('condeimg');
          const vis=document.getElementById('world').style.display!=='none';
          const bb=im.getBoundingClientRect(); const on=vis && bb.right>0 && bb.left<1080 && bb.bottom>0 && bb.top<1920;
          return [im.getAttribute('href'), POSE[Math.max(0,lineAt({i}/30))][6], on, document.getElementById('cam').getAttribute('transform')];}})()""")
        if prev and r[0]!=prev[0]:
            corte = r[1]!=prev[1]
            trocas.append((i, prev[0].split('/')[-1], r[0].split('/')[-1], prev[1], r[1], prev[2], r[2], corte))
            if not corte: ruins.append(i)
        prev=r
    b.close()
for t in trocas: print('quadro %d (%.2fs): %s -> %s | plano %s -> %s | visível antes %s depois %s | corte %s'%(t[0],t[0]/30,*t[1:]))
print('OK: todas as trocas caem num corte' if not ruins else 'FALHA em %s'%ruins)
