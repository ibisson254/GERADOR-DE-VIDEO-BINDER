from playwright.sync_api import sync_playwright
import json
# fichas para a tela da TV sem zoom (regra de 02/11/2026): texto grande, poucas linhas
S={
'cosmic':('LOJA · EUA',[('n','Cosmic Games'),('s','Illinois'),('b','US$ 7'),('h','pacotes e promos')],'Fonte: TopDeck.gg · 02/11/2026'),
'laluna':('LOJA · ESPANHA',[('n','Laluna'),('s','11/04/2026'),('b','€ 12'),('h','Mox Diamond'),('s','base: 100 jogadores')],'Fonte: TopDeck.gg · 02/11/2026'),
'grande':('FORA DA LOJA',[('n','Gen Con 2026'),('s','precon aleatório'),('n','CommandFest SP'),('s','Precon Clash'),('h','vitória: 20 Tix')],'Fontes: Gamertag Mythras · CCG Eventos'),
'painel':('O OUTRO LADO',[('n','Painel do Commander'),('s','21/10/2025'),('h','precons variam muito de força')],'Fonte: Wizards of the Coast'),
}
H='''<!doctype html><meta charset=utf-8><style>*{box-sizing:border-box}body{margin:0;width:744px;height:1040px;background:transparent;color:#F4F1E8;padding:40px 34px 36px;display:flex;flex-direction:column;font-family:Arial,sans-serif}
.t{align-self:flex-start;background:#FFD84A;color:#050A10;font:800 46px Arial;padding:8px 20px;margin-bottom:34px}
.n,.s,.b,.h,.f{background:rgba(5,10,16,.88);padding:4px 14px;align-self:flex-start;box-decoration-break:clone}.n{font:800 74px/1.06 Arial;margin-top:10px}.s{font:700 54px/1.15 Arial;color:#C8D2E0;margin-bottom:12px}.b{font:800 150px/1.1 Arial;color:#FFD84A}.h{font:800 72px/1.1 Arial;margin-top:12px}
.f{margin-top:auto;font:700 44px/1.15 Arial;color:#D3DAE5}</style>'''
HL={}
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':744,'height':1040})
    for k,(t,rows,f) in S.items():
        pg.set_content(H+f"<div class=t>{t}</div>"+''.join(f"<div class={c}>{x}</div>" for c,x in rows)+f"<div class=f>{f}</div>")
        print(k,pg.evaluate("document.documentElement.scrollHeight"))
        HL[k]=pg.evaluate("[...document.querySelectorAll('.h')].map(e=>{const b=e.getBoundingClientRect();return [b.x/744,b.y/1040,b.width/744,b.height/1040]})[0]")
        pg.screenshot(path=f'esp/slides/{k}.png',omit_background=True)
    pg.set_content(H+"<div class=t>COMENTÁRIOS</div><div class=n>A comunidade falou</div><div class=s>Commander Precon</div>")
    pg.screenshot(path='esp/slides/comu.png',omit_background=True); b.close()
json.dump(HL,open('esp/slides/hl.json','w'))
