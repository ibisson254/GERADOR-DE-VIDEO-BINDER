"""Especial Taverna de Avalon: adapta uma CÓPIA do index.html do kit (não mexe no kit da série).
- Cenário: imagem da taverna (taverna_916.jpg) no lugar da sala; sem sofá, TV pequena e mesinha.
- Estandarte com a logo original da Taverna na parede da direita.
- Figurinos pontuais: Burn guerreiro (armadura, caneca), Mana mago (chapéu, manto, pergaminho).
- Plaquinhas dos números (EP.placas), plano do estandarte (EP.est) e selo da parceria.
"""
import sys, re, pathlib
p = pathlib.Path(sys.argv[1]); s = p.read_text(encoding='utf-8')
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)

# ---------- CSS / DOM ----------
rep('#cred{position:absolute;', '#cred{display:none;position:absolute;')
rep('<div id="ins"></div>', '''<div id="ins"></div>
  <div id="placas" style="position:absolute;inset:0;pointer-events:none"></div>
  <div id="selo" style="position:absolute;left:0;right:0;top:1100px;text-align:center;opacity:0">
    <div style="display:inline-flex;align-items:center;gap:18px;background:rgba(5,10,16,.86);border:2px solid #10B981;border-radius:18px;padding:16px 30px 14px">
      <span style="font:400 54px/1 Bangers;letter-spacing:2px;color:#F2EBDA">×</span>
      <img src="logo/logo_mark.png" style="height:70px">
      <span style="font:700 52px/1 Geist;color:#fff">BINDER <span style="color:#10B981">Vision</span></span></div>
    <div style="margin-top:14px;font:400 40px/1 Bangers;letter-spacing:3px;color:#FFD84A;-webkit-text-stroke:8px #050A10;paint-order:stroke fill">PARCEIRA OFICIAL DE APOIO</div></div>''')
rep('<div id="gancho" style="display:none;position:absolute;left:60px;right:160px;top:360px;text-align:center;font:400 112px/1.02 Bangers;',
    '<div id="gancho" style="display:none;position:absolute;left:56px;width:640px;top:252px;text-align:left;font:400 104px/1.0 Bangers;')

# ---------- cenário: a taverna (coordenadas do mundo = ecrã − 200 px no plano geral) ----------
i0 = s.index('const room = `'); i1 = s.index('`;', i0) + 2
s = s[:i0] + '''const room = `
 <image href="taverna_916_largo.jpg" x="-200" y="-200" width="1480" height="1920" preserveAspectRatio="none"/>`;
// estandarte da Taverna de Avalon (logo original, sem alteração de forma nem de cor) + luz da vela
const estandarte = `<defs><radialGradient id="lzV" cx="420" cy="160" r="700" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FFB25A" stop-opacity=".16"/><stop offset="1" stop-color="#FFB25A" stop-opacity="0"/></radialGradient>
   <radialGradient id="vgE" cx="740" cy="225" r="300" gradientUnits="userSpaceOnUse"><stop offset=".55" stop-color="#1A0E05" stop-opacity="0"/><stop offset="1" stop-color="#1A0E05" stop-opacity=".38"/></radialGradient></defs>
 <g transform="rotate(-1.2 740 10)"><image href="estandarte.png" x="575" y="10" width="330" height="431"/></g>
 <rect x="575" y="10" width="330" height="431" fill="url(#vgE)"/>
 <rect x="-400" y="-300" width="1880" height="2200" fill="url(#lzV)" style="mix-blend-mode:screen"/>`;'''+ s[i1:]

# montagem do mundo: sem TV pequena, sofá nem mesinha; filtro de luz quente nos personagens; sombra de contacto no banco
rep('''world.innerHTML = defs + `<g id="cam">${luzDefs}<g filter="url(#rough)">${room}</g>${luzQuente}${tvSmall}<g filter="url(#rough)">${tvSmallLine}${tvTop}</g><g id="tvfx" transform="translate(648.95 290.47) scale(0.373)"></g>${tvSmallCard}<g id="tvoffw" transform="translate(648.95 290.47) scale(0.373)"></g><g filter="url(#rough)">${couchBack}${couchFront}</g>
  <g id="mana" filter="url(#rough2)"></g><g id="burn" filter="url(#rough2)"></g>${luzTV}<g filter="url(#rough)" transform="translate(-20 -96) scale(1.04)">${table}</g><g id="pilha" filter="url(#rough2)"></g>${luzFrente}</g>`;''',
'''world.innerHTML = defs + `<defs><filter id="quente" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="0.98 0.04 0 0 0.01  0.02 0.86 0 0 0  0 0.02 0.66 0 0  0 0 0 1 0"/></filter>
  <linearGradient id="sombraL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity=".18"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient></defs>
  <g id="cam">${room}${estandarte}<g id="tvfx" style="display:none"></g><g id="tvoffw" style="display:none"></g>
  <ellipse cx="236" cy="918" rx="120" ry="16" fill="#0A0603" opacity=".55"/><ellipse cx="486" cy="918" rx="130" ry="16" fill="#0A0603" opacity=".55"/>
  <ellipse cx="236" cy="1112" rx="105" ry="12" fill="#0A0603" opacity=".5"/><ellipse cx="486" cy="1112" rx="110" ry="12" fill="#0A0603" opacity=".5"/>
  <g filter="url(#quente)"><g id="mana" filter="url(#rough2)"></g><g id="burn" filter="url(#rough2)"></g></g>
  <rect x="140" y="560" width="520" height="560" fill="url(#sombraL)" style="mix-blend-mode:multiply"/>
  <g id="pilha"></g>${luzFrente}</g>`;''')

# ---------- figurinos ----------
star = lambda x, y, r: f'<path d="M{x} {y-r} L{x+r*.3:.1f} {y-r*.3:.1f} L{x+r} {y} L{x+r*.3:.1f} {y+r*.3:.1f} L{x} {y+r} L{x-r*.3:.1f} {y+r*.3:.1f} L{x-r} {y} L{x-r*.3:.1f} {y-r*.3:.1f} Z" fill="#E9C85A"/>'
# Mana: chapéu de mago no lugar do gorro
i0 = s.index('   <path d="M171 484 Q172 402 236 400 Q298 404 300 484 Z"'); i1 = s.index(".join('')}</g>`; }", i0)
s = s[:i0] + f'''   <path d="M182 478 Q196 414 228 376 Q256 346 322 334 Q292 356 285 392 Q276 432 296 478 Z" fill="#3B3F8C" ${{S(6)}}/>
   <path d="M244 374 Q264 354 300 344" stroke="#5A5FB0" stroke-width="6" fill="none"/>
   {star(226,438,12)}{star(266,392,8)}{star(212,410,6)}{star(260,456,6)}
   <path d="M184 458 Q240 446 296 458 L295 478 Q240 468 185 480 Z" fill="#D9B44A" ${{S(4)}}/>
   <path d="M126 480 Q236 454 348 478 Q356 496 334 504 Q236 484 140 506 Q118 500 126 480 Z" fill="#2E3274" ${{S(5)}}/></g>`; }}''' + s[i1+len(".join('')}</g>`; }"):]
# Mana: manto azul com estrelas e cinto
i0 = s.index('function manaTorso(){'); i1 = s.index('function manaHeadBack', i0)
s = s[:i0] + f'''function manaTorso(){{ return `
  <path d="M170 652 Q158 600 200 594 L272 592 Q314 602 302 652 Z" fill="#2B2F6A" ${{S(5)}}/>
  <path d="M162 624 Q236 600 310 620 L322 1004 Q236 1026 148 1004 Z" fill="#3B3F8C" ${{S(6)}}/>
  <path d="M236 610 L236 1016" stroke="#D9B44A" stroke-width="9"/><path d="M236 610 L236 1016" stroke="${{K}}" stroke-width="2" opacity=".4"/>
  <path d="M166 812 Q236 798 310 812 L311 834 Q236 820 165 836 Z" fill="#6E4424" ${{S(3.5)}}/><rect x="224" y="804" width="24" height="26" rx="4" fill="#D9B44A" ${{S(3)}}/>
  {star(194,700,10)}{star(280,736,8)}{star(200,904,9)}{star(286,950,11)}{star(270,868,6)}
  <path d="M222 640 L216 704 M250 640 L256 696" stroke="#D9B44A" stroke-width="3.5"/>`; }}
''' + s[i1:]
rep("const sl='#B98A3A', hand=(x,y,r=19)", "const sl='#3B3F8C', hand=(x,y,r=19)")
# Mana: pergaminho no lugar do pacote de salgadinho
i0 = s.index('  const chips=(x,y)=>'); i1 = s.index('</g>`;', i0) + len('</g>`;')
s = s[:i0] + '''  const chips=(x,y)=>`<g transform="rotate(-10 ${x} ${y})"><rect x="${x-24}" y="${y-46}" width="48" height="92" fill="#E8DAB2" ${S(4)}/>
     <ellipse cx="${x}" cy="${y-46}" rx="30" ry="9" fill="#D2C08E" ${S(3.5)}/><ellipse cx="${x}" cy="${y+46}" rx="30" ry="9" fill="#D2C08E" ${S(3.5)}/>
     <path d="M${x-14} ${y-24} l28 0 M${x-14} ${y-10} l22 0 M${x-14} ${y+4} l28 0 M${x-14} ${y+18} l18 0" stroke="#8A7A58" stroke-width="3"/>
     <circle cx="${x+10}" cy="${y+30}" r="7" fill="#B0362A" ${S(2)}/></g>`;''' + s[i1:]
# Burn: armadura (malha + peitoral + gorjal), calção de couro
i0 = s.index('function burnTorso(){'); i1 = s.index('function burnFace', i0)
s = s[:i0] + '''function burnTorso(){ return `
  <path d="M380 726 Q486 692 590 724 Q618 822 586 908 Q484 928 386 906 Q352 822 380 726 Z" fill="#5E646D" ${S(6)}/>
  ${[...Array(9)].map((_,r)=>[...Array(10)].map((_,c)=>`<path d="M${388+c*22+(r%2)*11} ${734+r*20} q5 6 10 0" stroke="#3F444B" stroke-width="2.5" fill="none"/>`).join('')).join('')}
  <path d="M404 728 Q486 704 566 726 Q588 806 566 886 Q486 906 406 886 Q384 806 404 728 Z" fill="#A9B1BC" ${S(5.5)}/>
  <path d="M486 716 L486 898" stroke="#737B87" stroke-width="5"/>
  <path d="M428 748 Q446 810 436 870" stroke="#E6EAF0" stroke-width="8" fill="none" opacity=".75"/>
  <path d="M486 770 Q470 796 478 818 Q472 806 486 800 Q500 806 494 818 Q502 796 486 770 Z" fill="#D9542C" ${S(3)}/>
  <path d="M410 850 Q486 872 562 850" stroke="#737B87" stroke-width="4" fill="none"/>
  <path d="M456 684 L514 684 L516 724 L454 724 Z" fill="${SKB}" ${S(4)}/>
  <path d="M440 714 Q486 738 532 714 L538 738 Q486 762 434 738 Z" fill="#8E97A3" ${S(4.5)}/>`; }
''' + s[i1:]
rep("function burnLegs(){ const leg=(x1,x2)=>tube([[x1,905],[x2,962]],'#9F8C5E',60)", "function burnLegs(){ const leg=(x1,x2)=>tube([[x1,905],[x2,962]],'#5A4632',60)")
rep("const slc='#A4473B', hand=(x,y,r=21)", "const slc='#6F757E', hand=(x,y,r=21)")
# Burn: caneca no lugar da lata
i0 = s.index('  const can=(x,y)=>'); i1 = s.index('\n', i0)
s = s[:i0] + '''  const can=(x,y)=>`<path d="M${x+18} ${y-18} q26 2 24 22 q-2 18 -24 18" stroke="${K}" stroke-width="12" fill="none"/><path d="M${x+18} ${y-18} q26 2 24 22 q-2 18 -24 18" stroke="#7A4E2A" stroke-width="6" fill="none"/>
     <path d="M${x-22} ${y-28} L${x+20} ${y-28} L${x+18} ${y+30} L${x-20} ${y+30} Z" fill="#8A5A31" ${S(4.5)}/><path d="M${x-22} ${y-16} L${x+20} ${y-16} M${x-21} ${y+18} L${x+19} ${y+18}" stroke="#4A4440" stroke-width="5"/>
     <path d="M${x-26} ${y-28} Q${x-22} ${y-46} ${x-6} ${y-40} Q${x+4} ${y-52} ${x+16} ${y-40} Q${x+28} ${y-40} ${x+24} ${y-28} Z" fill="#F4EEDC" ${S(3.5)}/>`;''' + s[i1:]
# Burn: ombreiras por cima dos braços
rep("    else Rr = tube([[576,742],[600,836],[556,892]],slc,46) + hand(556,892);\n  }\n  return L+Rr; }",
    """    else Rr = tube([[576,742],[600,836],[556,892]],slc,46) + hand(556,892);
  }
  const omb=(x,f)=>`<g transform="translate(${x} 736) scale(${f} 1)"><path d="M-48 10 Q-40 -34 8 -30 Q44 -24 46 8 Q20 26 -48 10 Z" fill="#A9B1BC" ${S(5)}/><path d="M-36 2 Q-10 -12 34 0" stroke="#737B87" stroke-width="4" fill="none"/><path d="M-30 -14 Q-14 -24 6 -22" stroke="#E6EAF0" stroke-width="5" fill="none" opacity=".7"/></g>`;
  return L+Rr+omb(390,-1)+omb(580,1); }""")

# ---------- câmara: plano do estandarte (aproximação lenta) ----------
rep("  if(EP.cams&&EP.cams[shot]) return EP.cams[shot];\n  const W={s:1,cx:540,cy:675,tx:540,ty:875};",
    """  const W={s:1,cx:540,cy:675,tx:540,ty:875};
  if(shot==='est'&&EP.est){ const i=lineAt(t), l=LINES[i], p=ease(clamp((t-l.start)/(EP.est.dur||1.5))), E=EP.est.cam;
    return {s:W.s+(E.s-W.s)*p,cx:W.cx+(E.cx-W.cx)*p,cy:W.cy+(E.cy-W.cy)*p,tx:W.tx+(E.tx-W.tx)*p,ty:W.ty+(E.ty-W.ty)*p}; }
  if(EP.cams&&EP.cams[shot]) return EP.cams[shot];""")

# ---------- plaquinhas dos números + selo da parceria ----------
rep('function render(t){\n  abertura(t);', '''const PLC=document.getElementById('placas'), SELO=document.getElementById('selo');
if(EP.placas) PLC.innerHTML = EP.placas.itens.map((q,k)=>`<div class="plc" style="position:absolute;left:${q.x}px;top:${q.y}px;width:${q.w}px;height:${q.h}px;opacity:0;transform-origin:50% 0">
   ${k<2?`<div style="position:absolute;left:${q.w/2-46}px;top:-30px;width:92px;height:34px;border-left:4px solid #3E3A36;border-right:4px solid #3E3A36;transform:perspective(60px) rotateX(-30deg)"></div>`:''}
   <div style="position:absolute;inset:0;border-radius:10px;background:linear-gradient(180deg,#7C5130,#5E3B22);border:4px solid #221C17;box-shadow:0 10px 0 rgba(0,0,0,.45),inset 0 0 0 5px rgba(255,220,160,.12)"></div>
   <div style="position:absolute;left:0;right:0;top:${Math.round(q.h*0.10)}px;text-align:center;font:400 ${Math.round(q.h*0.52)}px/1 Bangers;letter-spacing:2px;color:#FFD84A;-webkit-text-stroke:6px #050A10;paint-order:stroke fill">${q.n}</div>
   <div style="position:absolute;left:0;right:0;bottom:${Math.round(q.h*0.09)}px;text-align:center;font:700 ${Math.round(Math.min(q.h*0.15,(q.w-28)*1.45/q.r.length))}px/1 Geist;letter-spacing:.5px;white-space:nowrap;color:#F4EEDC">${q.r}</div></div>`).join('')
  + `<div id="plcfonte" style="position:absolute;right:${EP.placas.fonte.right}px;top:${EP.placas.fonte.y}px;font:700 22px/1.2 Geist;color:#F4EEDC;background:rgba(5,10,16,.72);padding:6px 12px;border-radius:6px;opacity:0">${EP.placas.fonte.txt}</div>`;
function placas(t){ if(!EP.placas) return; const P=EP.placas, a=LINES[P.fala], fim=LINES[P.ate].start+LINES[P.ate].dur+0.15;
  const els=PLC.querySelectorAll('.plc'), out=clamp((t-fim)/0.25);
  P.itens.forEach((q,k)=>{ const t0=a.start+a.dur*q.at, u=clamp((t-t0)/0.4), e=backOut(u), on=t>=t0&&t<fim+0.25, el=els[k];
    el.style.opacity=on?Math.min(1,u*3)*(1-out):0; el.style.transform=`translateY(${(1-e)*-160}px) rotate(${(1-e)*-6+(q.rot||0)}deg)`; });
  const f=document.getElementById('plcfonte'), tf=a.start+a.dur*P.itens[0].at; f.style.opacity=(t>=tf&&t<fim+0.25)?Math.min(1,(t-tf)/0.3)*(1-out):0;
  if(EP.selo){ const l=LINES[EP.selo.fala], s0=l.start+l.dur*EP.selo.de, s1=l.start+l.dur-0.1, v=clamp((t-s0)/0.35), w=clamp((t-s1)/0.15);
    SELO.style.opacity=(t>=s0&&t<s1+0.15)?v*(1-w):0; SELO.style.transform=`scale(${0.85+0.15*backOut(v)})`; } }
const PERG=document.createElement('div'); PERG.style.cssText='position:absolute;inset:0;pointer-events:none'; PLC.after(PERG);
if(EP.pergaminho){ const G=EP.pergaminho; PERG.innerHTML=`<div id="perg" style="position:absolute;left:${G.x}px;top:${G.y}px;width:${G.w}px;opacity:0;transform-origin:50% 0">
   <div style="background:linear-gradient(180deg,#EADCB6,#D8C597);border:4px solid #221C17;border-radius:8px;padding:16px 20px 14px;box-shadow:0 10px 0 rgba(0,0,0,.45)">
   <div style="font:400 38px/1 Bangers;letter-spacing:2px;color:#5A2E14;margin-bottom:10px">${G.titulo}</div>
   ${G.linhas.map(l=>`<div style="font:700 23px/1.25 Geist;color:#221C17;margin:6px 0">• ${l}</div>`).join('')}
   <div style="font:500 17px/1.2 Geist;color:#5A4A30;margin-top:10px">${G.fonte}</div></div></div>`; }
function pergaminho(t){ if(!EP.pergaminho) return; const G=EP.pergaminho, l=LINES[G.fala], a=l.start+l.dur*G.de, b=l.start+l.dur+0.1, u=clamp((t-a)/0.35), w=clamp((t-b)/0.2), el=document.getElementById('perg');
  el.style.opacity=(t>=a&&t<b+0.2)?Math.min(1,u*2)*(1-w):0; el.style.transform=`scaleY(${0.2+0.8*backOut(u)})`; }
function render(t){
  pergaminho(t);
  placas(t);
  abertura(t);''')
p.write_text(s, encoding='utf-8')
print('patch aplicado:', p)
