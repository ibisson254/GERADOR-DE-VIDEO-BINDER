"""Plano de prova + legenda paginada (MB-EP16 v2, 22/11/2026) · patch OPCIONAL do index.html do Mana & Burn.
Acrescenta dois recursos que só ligam se o episode.js os pedir; sem as chaves, os episódios saem iguais (testado com o MB-EP15):
  EP.prova = {w, top, fundoTop, segs:[{fala, de, img, tipo:'carta'|'tela', hl:[[x,y,w,h]], zoom:{de, alvo:[x,y,w,h], s}, faixa}]}
     plano de evidência: a carta grande, inteira, por cima da sala escurecida. Troca de carta = flip 3D no eixo Y (0,32 s, a
     mesma linguagem da troca de carta do Meta em Curto, reimplementada aqui sem importar código de outra frente); mesma carta =
     só muda o destaque ou a aproximação; «tela» (painel que não é carta) = corte seco.
  EP.legenda_paginas = N: fala com mais de N caracteres aparece em duas páginas (corte na pontuação mais perto do meio),
     cada uma no máximo em duas linhas, com o tempo proporcional ao texto.
  episode.json "sfx_flip" / "sfx_destaque" = [[fala, fração]]: som de carta (flick) e de destaque nos momentos do plano de prova
     (process.py); sem as chaves, a mistura sai igual.
Uso, na pasta do kit:  python3 kit/prova/patch_prova.py index.html   (corrige também o process.py da mesma pasta; recusa um kit que já o tenha)."""
import sys, pathlib
p = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'index.html'); s = p.read_text(encoding='utf-8')
if 'EP.prova' in s: sys.exit('index.html já tem o plano de prova: nada a fazer.')
A = '  <div id="ins"></div>\n'
assert s.count(A) == 1
s = s.replace(A, '  <div id="prova" style="display:none;position:absolute;left:0;top:0;width:1080px;height:1920px"></div>\n' + A)
JS = r'''// ---------- plano de prova (MB-EP16 v2, 22/11/2026, opcional; kit/prova/patch_prova.py) ----------
const PV = EP.prova || null; let PV_EL=null, PV_CARD=null, PV_IMG=null, PV_HL=null, PV_FX=null, PV_BACK=null, PV_W=0, PV_H=0;
if(PV){ PV_EL=document.getElementById('prova'); const W=PV.w||644, H=W*1040/744, X0=(1080-W)/2, Y0=PV.top||330; PV_W=W; PV_H=H;
  PV_EL.innerHTML=`<div id="pvBack" style="position:absolute;left:0;right:0;top:${PV.fundoTop??200}px;bottom:0;background:rgba(5,10,16,.82);backdrop-filter:blur(6px)"></div>
   <div style="position:absolute;left:0;top:${Y0-24}px;width:1080px;height:${H+48}px;overflow:hidden;perspective:1800px">
    <div id="pvCard" style="position:absolute;left:${X0}px;top:24px;width:${W}px;height:${H}px;transform-origin:50% 50%">
     <img id="pvImg" style="position:absolute;inset:0;width:100%;height:100%;border-radius:${W*0.045}px;box-shadow:0 14px 0 rgba(0,0,0,.5)">
     <div id="pvHL" style="position:absolute;inset:0"></div></div></div>
   <div id="pvFx" style="position:absolute;left:60px;right:60px;top:${Y0+H+34}px;text-align:center;font:400 60px/1 Bangers;letter-spacing:2px;color:#FFD84A;-webkit-text-stroke:10px #050A10;paint-order:stroke fill"></div>`;
  PV_CARD=document.getElementById('pvCard'); PV_IMG=document.getElementById('pvImg'); PV_HL=document.getElementById('pvHL');
  PV_FX=document.getElementById('pvFx'); PV_BACK=document.getElementById('pvBack');
  PV.segs.forEach(sg=>{ const im=new Image(); im.src=sg.img; sg._im=im; }); }
const pvTipo=sg=>sg.tipo||'carta';
function pvIni(sg){ const L=LINES[sg.fala]; return L.start+L.dur*(sg.de||0); }
function pvFim(k){ const sg=PV.segs[k], n=PV.segs[k+1], L=LINES[sg.fala];
  const fim=LINES[sg.fala+1]?LINES[sg.fala+1].start:L.start+L.dur+0.2; return (n&&n.fala===sg.fala)?Math.min(pvIni(n),fim):fim; }
function prova(t){ if(!PV) return; let k=-1; PV.segs.forEach((sg,j)=>{ if(t>=pvIni(sg)-0.001 && t<pvFim(j)) k=j; });
  if(k<0 || t>=T_SLAM){ PV_EL.style.display='none'; return; } PV_EL.style.display='block';
  const sg=PV.segs[k], t0=pvIni(sg), dt=t-t0, carta=pvTipo(sg)==='carta';
  let j=k; while(j>0 && Math.abs(pvFim(j-1)-pvIni(PV.segs[j]))<0.02) j--; const tP=pvIni(PV.segs[j]), entra=(j===k);
  let ant=null; for(let m=k-1;m>=0;m--) if(pvTipo(PV.segs[m])==='carta'){ ant=PV.segs[m].img; break; }
  const qin=ease(clamp((t-tP)/0.22)); PV_BACK.style.opacity=qin;
  let img=sg.img, rot=0, sc=0.88+0.12*qin, hlOn=1;
  const flip=carta && ant && ant!==sg.img, FD=0.32, f0=entra?0.14:0;      // ao entrar, a carta anterior aparece 0,14 s e vira
  if(flip){ const q=(dt-f0)/FD; if(q<1){ hlOn=0; if(q<0.5){ img=ant; rot=q<0?0:ease(q*2)*90; } else rot=-90+ease((q-0.5)*2)*90; } }
  if(!carta && !entra){ sc*=0.965+0.035*ease(clamp(dt/0.14)); }        // painel: corte seco com um pequeno «pop»
  let Z=1, dx=0, dy=0;
  if(carta && sg.zoom){ const L=LINES[sg.fala], q=ease(clamp((t-(L.start+L.dur*sg.zoom.de))/0.35)), a=sg.zoom.alvo;
    Z=1+((sg.zoom.s||1.5)-1)*q; const px=(a[0]+a[2]/2-0.5)*PV_W, py=(a[1]+a[3]/2-0.5)*PV_H; dx=-px*(Z-1); dy=-py*(Z-1); }
  if(PV_IMG.getAttribute('src')!==img) PV_IMG.setAttribute('src',img);
  const hk=k+'|'+(hlOn?1:0); if(PV_HL.dataset.k!==hk){ PV_HL.dataset.k=hk;
    PV_HL.innerHTML=hlOn&&carta?(sg.hl||[]).map(r=>`<div class="pvhl" style="position:absolute;left:${r[0]*100}%;top:${r[1]*100}%;width:${r[2]*100}%;height:${r[3]*100}%;border:4px solid #FFD84A;border-radius:6px;background:rgba(255,216,74,.20)"></div>`).join(''):''; }
  const g=0.55+0.45*Math.abs(Math.sin(t*5)); PV_HL.querySelectorAll('.pvhl').forEach(e=>e.style.boxShadow=`0 0 ${Math.round(16*g)}px rgba(255,216,74,${(0.7*g).toFixed(2)})`);
  PV_CARD.style.transform=`translate(${dx.toFixed(1)}px,${dy.toFixed(1)}px) scale(${(sc*Z).toFixed(4)}) rotateY(${rot.toFixed(2)}deg)`;
  PV_CARD.style.opacity=entra?Math.min(1,qin*1.6):1;
  const fx=sg.faixa||''; if(PV_FX.textContent!==fx) PV_FX.textContent=fx; PV_FX.style.opacity=hlOn?qin:0; }
// legenda paginada (opcional): EP.legenda_paginas = N caracteres
function paginaLegenda(txt,t){ const N=EP.legenda_paginas, j=LINES.findIndex(l=>l.text===txt); if(j<0) return txt;
  const pl=txt.replace(/\*/g,''); if(pl.length<=N) return txt;
  const meio=txt.length/2; let cut=-1, best=1e9, cut2=-1, best2=1e9;
  for(let i=1;i<txt.length-1;i++){ if(txt[i]!==' ') continue; const c=txt.slice(0,i).replace(/\*+$/,'').slice(-1);
    if(/[.?!:]/.test(c) && Math.abs(i-meio)<best){ best=Math.abs(i-meio); cut=i; }
    if(/[,;]/.test(c) && Math.abs(i-meio)<best2){ best2=Math.abs(i-meio); cut2=i; } }
  if(cut<0 || best>txt.length*0.3) cut=cut2>=0?cut2:cut; if(cut<0) return txt;
  let a=txt.slice(0,cut).trim(), b=txt.slice(cut).trim(); if((a.split('*').length-1)%2){ a+='*'; b='*'+b; }
  const L=LINES[j], fr=a.replace(/\*/g,'').length/pl.length; return t<L.start+L.dur*fr ? a : b; }
'''
B = 'function render(t){\n'
assert s.count(B) == 1
s = s.replace(B, JS + B)
C = '  abertura(t);\n'
assert s.count(C) == 1
s = s.replace(C, C + '  prova(t);\n')
D = "  if(t>=T_SLAM && !EP.loop) txt='';\n"
assert s.count(D) == 1
s = s.replace(D, D + "  if(EP.legenda_paginas && txt) txt=paginaLegenda(txt,t);\n")
pp = p.parent / 'process.py'; ps = pp.read_text(encoding='utf-8')
E = "ins_t = [round(lines[k]['start'] + lines[k]['dur'] * a, 3) for k, a in INS]\n"
assert ps.count(E) == 1 and 'sfx_flip' not in ps
ps = ps.replace(E, E + "ins_t += [round(lines[k]['start'] + lines[k]['dur'] * a, 3) for k, a in EPI.get('sfx_flip', [])]   # plano de prova (opcional, kit/prova)\n"
                "destaques += [round(lines[k]['start'] + lines[k]['dur'] * a, 3) for k, a in EPI.get('sfx_destaque', [])]\n")
p.write_text(s, encoding='utf-8'); pp.write_text(ps, encoding='utf-8')
print('plano de prova e legenda paginada aplicados em', p, 'e', pp)
