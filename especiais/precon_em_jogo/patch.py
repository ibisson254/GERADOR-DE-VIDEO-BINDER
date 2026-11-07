h=open('index.html',encoding='utf8').read()
# 1. quadro do Conde no lugar do quadro torto (só com EP.quadro)
a=h.index('<!-- quadro torto com vidro rachado -->'); b=h.index('${fan}',a)
h=h[:a]+"${EP.quadro?'':`"+h[a:b]+"`}\n "+h[b:]
frame='<g transform="rotate(-2 372 420)"><path d="M372 318 L340 346 M372 318 L404 346" stroke="#2A2218" stroke-width="3"/><circle cx="372" cy="316" r="5" fill="#555"/><rect x="296" y="342" width="152" height="166" fill="#5A3A1E" stroke="#1B1B1B" stroke-width="5"/><rect x="304" y="350" width="136" height="150" fill="none" stroke="#B8934A" stroke-width="4"/><image id="condeimg" href="esp/conde/neutro.png" x="312" y="358" width="120" height="134" preserveAspectRatio="xMidYMid slice"/></g>'
k='<g id="tvfx" transform="translate(648.95 290.47) scale(0.373)"></g>'
assert k in h; h=h.replace(k,k+"${EP.quadro?`"+frame+"`:''}")
# 2. render: expressão do quadro, frame do clip, cartão da comunidade, legenda do trecho
k="function render(t){\n  const i=Math.max(0,lineAt(t)), P=POSE[i], tq=Math.floor(t*12)/12, shot=P[6];"
assert k in h
h=h.replace(k,k+"""
  if(EP.quadro){ const e=EP.quadro.filter(q=>i>=q[0]).pop()[1], im=document.getElementById('condeimg'), u='esp/conde/'+e+'.png'; if(im.getAttribute('href')!==u) im.setAttribute('href',u); }
  const cm=EP.comu&&EP.comu.find(c=>c.line===i), ce=document.getElementById('comu');
  if(ce){ if(cm){ ce.style.display='block'; const q=ce.querySelector('p'); if(q.dataset.l!==String(i)){ q.textContent='“'+cm.q+'”'; q.style.fontSize=cm.px+'px'; q.dataset.l=i; } } else ce.style.display='none'; }""")
k="const HRi = hlAt(i,shot), cs = canalState(t,i), seed"
assert k in h
h=h.replace(k,"const HRi = hlAt(i,shot), cs = clipState(canalState(t,i),t), seed")
k="function canalState(t,i){"
h=h.replace(k,"function clipState(cs,t){ const C=EP.clip; if(!C||!cs||cs.k!==0) return cs; const n=Math.min(C.n,Math.max(1,Math.floor((t-C.t0)*30)+1)); cs.img='esp/clip/'+String(n).padStart(3,'0')+'.jpg'; return cs; }\n"+k)
k="if(t>=T_SLAM) txt='';"
assert k in h
h=h.replace(k,k+"\n  if(EP.subPre&&t<LINES[0].start-0.05){ const q=EP.subPre.find(s=>t>=s[0]&&t<s[1]); txt=q?q[2]:''; }")
# 3. elemento e estilo do cartão
css='''<style>#comu{display:none;position:absolute;left:66px;right:160px;top:340px;background:#F2EBDA;border:6px solid #1B1B1B;box-shadow:10px 12px 0 rgba(0,0,0,.55);transform:rotate(-1.2deg);padding:30px 34px 34px;font-family:Geist;color:#1B1B1B;z-index:50}
#comu .tag{position:absolute;top:-30px;left:26px;background:#10B981;color:#050A10;font:400 40px Bangers;letter-spacing:2px;padding:4px 18px;border:4px solid #1B1B1B}
#comu .row{display:flex;gap:22px;align-items:center;margin-top:16px}#comu img{width:140px;height:140px;border-radius:50%;border:5px solid #1B1B1B;object-fit:cover}
#comu b{display:block;font-size:40px}#comu span{font-size:27px;color:#55503F}#comu p{line-height:1.26;font-weight:600;margin:24px 0 0}</style>'''
h=h.replace('</head>',css+'</head>',1)
k="const stageEl=document.getElementById('stage')"
assert k in h
h=h.replace(k,"""if(EP.comu){ const o=document.createElement('div'); o.id='comu'; o.innerHTML='<div class="tag">A COMUNIDADE FALOU</div><div class="row"><img src="esp/diego.png"><div><b>@diegoalencard</b><span>comentou no @binderthetrade</span></div></div><p></p>'; document.getElementById('stage').appendChild(o); }
"""+k,1)
open('index.html','w',encoding='utf8').write(h)
p=open('process.py',encoding='utf8').read()
k="t = 0.35; lines = []"; assert k in p
p=p.replace(k,"t = EPI.get('inicio', 0.35); lines = []")
k="mix = m * g[:, None] + voice[:, None] + fxt"; assert k in p
p=p.replace(k,k+"""
if EPI.get('clip'):      # trecho original do TUBO na TV (som original, sem regenerar voz)
    w_ = wave.open(EPI['clip']['wav']); c_ = np.frombuffer(w_.readframes(w_.getnframes()), '<i2').astype(np.float32).reshape(-1, 2) / 32768
    c_ = c_ / (np.max(np.abs(c_)) + 1e-9) * EPI['clip'].get('nivel', 0.8); c_[-int(.05*SR):] *= np.linspace(1, 0, int(.05*SR))[:, None]
    a_ = int(EPI['clip']['t0'] * SR); mix[a_:a_ + len(c_)] += c_""")
open('process.py','w',encoding='utf8').write(p)
