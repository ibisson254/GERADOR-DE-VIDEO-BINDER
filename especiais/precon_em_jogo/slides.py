from playwright.sync_api import sync_playwright
import pathlib
S={
'cosmic':('LOJA · EUA','Cosmic Games','Illinois',[('Deck','só precon, sem alterar'),('Inscrição','US$ 7'),('Prêmio','pacotes e promos')],'Fonte: TopDeck.gg, consulta 02/11/2026'),
'laluna':('LOJA · ESPANHA','Laluna','Premià de Mar · 11/04/2026',[('Deck','precon sem alterar'),('Inscrição','€ 12'),('1.º lugar','Mox Diamond'),('Base','100 jogadores; prêmio pode mudar')],'Fonte: TopDeck.gg, consulta 02/11/2026'),
'grande':('FORA DA LOJA','Gen Con 2026','+ CommandFest SP',[('Gen Con','PreCon Battle: precon aleatório'),('SP','Precon Clash: lista sem alterar'),('Prêmio SP','partic. 10 Tix · vitória 20 Tix')],'Fontes: Gamertag Mythras; CCG Eventos, consulta 02/11/2026'),
'painel':('O OUTRO LADO','Precon é igual?','Painel do Commander',[('Dito em','21/10/2025'),('Ideia','precons variam muito de força')],'Fonte: Wizards of the Coast'),
}
H='''<!doctype html><style>@font-face{font-family:Geist;src:local(Geist)}*{box-sizing:border-box}body{margin:0;width:744px;height:1040px;background:#0F172A;color:#F4F1E8;font-family:Geist,Arial,sans-serif;padding:44px 40px;display:flex;flex-direction:column}
.t{align-self:flex-start;background:#FFD84A;color:#050A10;font:800 34px Arial;padding:8px 20px}h1{font:800 76px/1.02 Arial;margin:30px 0 8px}h2{font:600 38px Arial;color:#9FB0C6;margin:0 0 34px}
.r{border-top:3px solid #33415A;padding:18px 0}.r b{display:block;font:700 32px Arial;color:#FFD84A}.r span{font:700 44px/1.13 Arial}.f{margin-top:auto;font:600 28px/1.2 Arial;color:#C8D0DC}</style>'''
HL={}
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':744,'height':1040})
    for k,(t,h,s,rows,f) in S.items():
        pg.set_content(H+f"<div class=t>{t}</div><h1>{h}</h1><h2>{s}</h2>"+''.join(f"<div class=r><b>{a}</b><span>{c}</span></div>" for a,c in rows)+f"<div class=f>{f}</div>")
        pg.screenshot(path=f'esp/slides/{k}.png')
        r=pg.evaluate("[...document.querySelectorAll('.r')].map(e=>{const b=e.querySelector('span').getBoundingClientRect();return [b.x/744,b.y/1040,b.width/744,b.height/1040]})")
        HL[k]=r; print(k,pg.evaluate("document.documentElement.scrollHeight"))
    # capa de comunidade na TV
    pg.set_content(H+"<div class=t>COMENTÁRIOS</div><h1>A comunidade falou</h1><h2>Commander Precon</h2>")
    pg.screenshot(path='esp/slides/comu.png'); b.close()

import json;json.dump(HL,open('esp/slides/hl.json','w'))
