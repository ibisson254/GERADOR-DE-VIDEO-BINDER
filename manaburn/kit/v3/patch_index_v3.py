"""Ganchos v3 do index.html (Ep. 10, 11/11/2026). Aplica-se uma vez; tudo fica desligado sem os campos novos
do episode.js, por isso os episódios antigos saem iguais.

EP.quadro     lista com uma expressão do Conde por fala (nomes dos PNG em EP.quadroDir). Retrato com moldura
              dourada no lugar do quadro torto. A expressão só muda quando muda o plano (início de cada sequência
              de falas com o mesmo plano), nunca com o quadro à vista.
EP.calendario {ano, mes, dia, semana, loja, frase}: folhinha dos anos 90 no lugar do calendário de 2019.
EP.pilha      {mao: fala}: pilha de terrenos genéricos na mesa à frente do Burn; a partir da fala `mao`, na mão
              do Mana. {lata: true} põe uma lata em cima da pilha.
EP.cams       planos extra para camera(), ex.: {pilha: {s, cx, cy, tx, ty}}.
EP.gancho     {html, fala}: texto grande do gancho desde o primeiro quadro até ao fim da fala `fala`.
EP.marca      {fala: N}: logo do BINDER no canto do ecrã da TV SAL a partir dessa fala.
EP.loop       true: sem o efeito de ligar a TV no início, sem colapso da imagem, ponto, logo nem fade no fim.
              Na pancada só o ecrã da TV da sala apaga (fica a logo); as legendas continuam depois dela.
canal.subir   segundos que o medidor desse canal leva a subir (contador de dano).
"""
import pathlib
p = pathlib.Path(__file__).resolve().parents[2] / 'index.html'
h = p.read_text(encoding='utf8')
if 'EP.quadro' in h:
    raise SystemExit('index.html já tem os ganchos v3')

def troca(a, b, n=1):
    global h
    assert h.count(a) == n, (a[:60], h.count(a))
    h = h.replace(a, b)

# 1. quadro do Conde no lugar do quadro torto (geometria aprovada no especial "Precon em jogo")
a = h.index('<!-- quadro torto com vidro rachado -->'); b = h.index('${fan}', a)
h = h[:a] + "${EP.quadro?quadroConde():`" + h[a:b] + "`}\n " + h[b:]
# 2. folhinha no lugar do calendário de 2019
a = h.index('<!-- calendário velho -->'); b = h.index('<!-- tomada com benjamim -->', a)
h = h[:a] + "${EP.calendario?folhinha(EP.calendario):`" + h[a:b] + "`}\n " + h[b:]

funcs = r'''
// ---------- ganchos v3 (Ep. 10, 11/11/2026): quadro do Conde, folhinha, pilha de terrenos ----------
function quadroConde(){ return `<g transform="rotate(-2 372 420)"><path d="M372 318 L340 346 M372 318 L404 346" stroke="#2A2218" stroke-width="3"/><circle cx="372" cy="316" r="5" fill="#555"/>
  <rect x="296" y="342" width="152" height="166" fill="#7A5A24" stroke="#1B1B1B" stroke-width="5"/><rect x="302" y="348" width="140" height="154" fill="none" stroke="#B8934A" stroke-width="5"/>
  <path d="M300 346 l10 0 M436 504 l-12 0 M300 470 l0 20" stroke="#5A3E18" stroke-width="3"/>
  <image id="condeimg" href="${EP.quadroDir}${EP.quadro[0]}.png" x="312" y="358" width="120" height="134" preserveAspectRatio="xMidYMid slice" opacity=".86"/>
  <rect x="312" y="358" width="120" height="134" fill="#8F855E" opacity=".16"/></g>`; }
function folhinha(c){ const x=34, y=452;
  return `<g transform="rotate(-5 ${x+50} ${y+70})">
  <path d="M${x+50} ${y-14} L${x+30} ${y+2} M${x+50} ${y-14} L${x+70} ${y+2}" stroke="#2A2218" stroke-width="2.5"/><circle cx="${x+50}" cy="${y-15}" r="4" fill="#555"/>
  <rect x="${x}" y="${y}" width="100" height="58" fill="#E9D58A" ${S(3.5)}/>
  <text x="${x+50}" y="${y+22}" text-anchor="middle" font-family="Bangers" font-size="17" letter-spacing="1" fill="#A8473A">${c.loja}</text>
  <text x="${x+50}" y="${y+38}" text-anchor="middle" font-family="Geist" font-weight="700" font-size="9" fill="#5A4A2A">${c.frase}</text>
  <text x="${x+50}" y="${y+51}" text-anchor="middle" font-family="Geist" font-weight="500" font-size="8" fill="#5A4A2A">${c.rodape||''}</text>
  <rect x="${x+12}" y="${y+58}" width="76" height="84" fill="#EFE6CE" ${S(3)}/>
  <text x="${x+50}" y="${y+73}" text-anchor="middle" font-family="Geist" font-weight="700" font-size="10" letter-spacing="1" fill="#2A2218">${c.mes} ${c.ano}</text>
  <text x="${x+50}" y="${y+120}" text-anchor="middle" font-family="Bangers" font-size="50" fill="#2A2218">${c.dia}</text>
  <text x="${x+50}" y="${y+136}" text-anchor="middle" font-family="Geist" font-weight="700" font-size="9" letter-spacing="1" fill="#A8473A">${c.semana}</text>
  <path d="M${x+88} ${y+122} L${x+74} ${y+142} L${x+88} ${y+142} Z" fill="#D6CBAA" ${S(2.5)}/>
  <rect x="${x}" y="${y}" width="100" height="142" fill="#C9B47A" opacity=".18"/></g>`; }
function cartaTerra(x,y,r,k){ const ilha=k%2===0, c=ilha?'#5D86A8':'#B5603E';
  return `<g transform="rotate(${r} ${x} ${y})"><rect x="${x-26}" y="${y-36}" width="52" height="72" rx="4" fill="#EDE3C8" ${S(2.5)}/>
   <rect x="${x-20}" y="${y-28}" width="40" height="36" fill="${c}"/>
   ${ilha?`<path d="M${x-16} ${y-6} q8 -6 16 0 q8 6 16 0" stroke="#EDE3C8" stroke-width="2.5" fill="none"/>`:`<path d="M${x-16} ${y+4} L${x-4} ${y-18} L${x+4} ${y-6} L${x+10} ${y-14} L${x+18} ${y+4} Z" fill="#7A3A22"/>`}
   <rect x="${x-20}" y="${y+14}" width="40" height="5" fill="#C9BE9C"/></g>`; }
function pilhaTerras(cx,base,n,lata){ let s=`<ellipse cx="${cx}" cy="${base+4}" rx="46" ry="10" fill="#2A2218" opacity=".35"/>`;
  for(let k=0;k<n;k++) s+=cartaTerra(cx+(R(k+300)-.5)*14, base-30-k*6, (R(k+400)-.5)*22, k);
  if(lata) s+=`<g transform="rotate(8 ${cx+6} ${base-30-n*6-40})"><rect x="${cx-10}" y="${base-30-n*6-66}" width="32" height="50" rx="5" fill="#C8352B" ${S(3)}/>
    <rect x="${cx-10}" y="${base-30-n*6-50}" width="32" height="12" fill="#F2EBDA"/><ellipse cx="${cx+6}" cy="${base-30-n*6-66}" rx="16" ry="5" fill="#B9B6AA" ${S(2.5)}/></g>`;
  return s; }
function pilhaMarkup(i){ const P=EP.pilha; if(!P) return '';
  if(P.mao!=null && i>=P.mao) return `<g transform="translate(150 862) rotate(-12) scale(.9) translate(-150 -862)">${pilhaTerras(150,900,13,false)}</g>`;
  const x=P.x||440, y=P.y||1140; return `<g transform="translate(${x} ${y}) scale(1.3) translate(${-x} ${-y})">${pilhaTerras(x, y, 16, P.lata)}</g>`; }
'''
troca('const room = `', funcs + '\nconst room = `')

# 3. camadas novas no mundo: ecrã apagado da TV da sala e pilha de terrenos (por cima da mesa)
troca('<g id="tvfx" transform="translate(648.95 290.47) scale(0.373)"></g>${tvSmallCard}',
      '<g id="tvfx" transform="translate(648.95 290.47) scale(0.373)"></g>${tvSmallCard}<g id="tvoffw" transform="translate(648.95 290.47) scale(0.373)"></g>')
troca('<g filter="url(#rough)" transform="translate(-20 -96) scale(1.04)">${table}</g>${luzFrente}</g>`;',
      '<g filter="url(#rough)" transform="translate(-20 -96) scale(1.04)">${table}</g><g id="pilha" filter="url(#rough2)"></g>${luzFrente}</g>`;')

# 4. logo do BINDER no canto do ecrã da TV SAL (EP.marca), nos dois planos
troca('''   <text x="700" y="1212" text-anchor="middle" font-family="Geist" font-weight="700" font-size="22" fill="#9AA3B2">${TVP.clock}</text>
  </g>`; }''',
      '''   <text x="700" y="1212" text-anchor="middle" font-family="Geist" font-weight="700" font-size="22" fill="#9AA3B2">${TVP.clock}</text>
   ${fx.mk?'<image href="logo/logo_mark.png" x="621" y="1168" width="48" height="48" opacity=".95"/>':''}
  </g>`; }''')
troca("live:Math.floor(t*2)%2===0, m:big?Math.round(ease(clamp((t-LINES[i].start)/(i===0&&FX.foco?2.0:0.9)))*10)/10:1}; }",
      "live:Math.floor(t*2)%2===0, mk:!!(EP.marca&&i>=EP.marca.fala), m:big?(su=>Math.round(ease(clamp((t-LINES[i].start)/(su||(i===0&&FX.foco?2.0:0.9))))*(su?60:10))/(su?60:10))(CANAIS&&CANAIS[canalIdx(i)].subir):1}; }")

# 5. planos extra
troca("function camera(t,shot){\n", "function camera(t,shot){\n  if(EP.cams&&EP.cams[shot]) return EP.cams[shot];\n")

# 6. texto do gancho (DOM)
troca('<div id="sub"></div>', '<div id="sub"></div>\n  <div id="gancho" style="display:none;position:absolute;left:60px;right:160px;top:360px;text-align:center;font:400 112px/1.02 Bangers;letter-spacing:2px;color:#FFD84A;-webkit-text-stroke:14px #050A10;paint-order:stroke fill"></div>')

# 7. render: quadro, pilha, ecrã apagado, gancho; loop sem fecho
troca("function render(t){\n  const i=Math.max(0,lineAt(t)), P=POSE[i], tq=Math.floor(t*12)/12, shot=P[6];",
      """function render(t){
  const i=Math.max(0,lineAt(t)), P=POSE[i], tq=Math.floor(t*12)/12, shot=P[6];
  if(EP.quadro){ let r=i; while(r>0&&POSE[r-1][6]===shot) r--; const im=document.getElementById('condeimg'), u=EP.quadroDir+EP.quadro[r]+'.png'; if(im&&im.getAttribute('href')!==u) im.setAttribute('href',u); }
  if(EP.pilha){ const pe=world.querySelector('#pilha'), pk=(EP.pilha.mao!=null&&i>=EP.pilha.mao)?'m':'t'; if(pe.dataset.k!==pk){ pe.innerHTML=pilhaMarkup(i); pe.dataset.k=pk; } }
  if(EP.loop){ const off=world.querySelector('#tvoffw'), a=t>=T_SLAM?clamp((t-T_SLAM)/0.24):0, ok=String(Math.round(a*10));
    if(off.dataset.k!==ok){ off.dataset.k=ok; off.innerHTML=a>0?`<rect x="79" y="682" width="704" height="562" rx="18" fill="#07090C" opacity="${a}"/>`+(EP.marca?`<image href="logo/logo_mark.png" x="621" y="1168" width="48" height="48" opacity="${0.55*a}"/>`:''):''; } }
  if(EP.gancho){ const g=document.getElementById('gancho'), l=LINES[EP.gancho.fala||0], on=t<l.start+l.dur+0.1; if(g.innerHTML!==EP.gancho.html) g.innerHTML=EP.gancho.html; g.style.display=on?'block':'none'; }""")
troca("  if(t>=T_SLAM) txt='';", "  if(t>=T_SLAM && !EP.loop) txt='';")
troca("  if(t<0.22){", "  if(t<0.22 && !EP.loop){")
troca("  if(t>=T_SLAM){ const a=clamp((t-T_SLAM)/0.24), b=clamp((t-T_SLAM-0.24)/0.18);",
      "  if(t>=T_SLAM && !EP.loop){ const a=clamp((t-T_SLAM)/0.24), b=clamp((t-T_SLAM-0.24)/0.18);")
troca("{ const lz=world.querySelector('#luztv'); if(lz) lz.style.opacity = op*Math.min(1,sy); }",
      "{ const lz=world.querySelector('#luztv'); if(lz) lz.style.opacity = EP.loop ? 1-clamp((t-T_SLAM)/0.24) : op*Math.min(1,sy); }")
troca("  if(t>=T_LOGO+0.30){", "  if(t>=T_LOGO+0.30 && !EP.loop){")
troca("const fade=clamp((t-(T_END-0.3))/0.3);", "const fade=EP.loop?0:clamp((t-(T_END-0.3))/0.3);")

p.write_text(h, encoding='utf8')
print('ganchos v3 aplicados em', p)
