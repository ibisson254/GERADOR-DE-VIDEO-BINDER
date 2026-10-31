// ---------- TV SAL · Giro de Domingo (formato fixo) ----------
// Base: desenhos do manaburn/index.html (via especial Picard v2) sem alteração. Esta parte é a única que muda o formato.
// Por semana muda só GIRO (episode.js) e o guião; as telas abaixo (abre, n1, n2, n3, agenda) são fixas.
const TVSHOTS=['tv','tv2','tvtext'];
const C2={x:245,y:703,w:373,h:520}, SCR={x:79,y:682,w:704,h:562}, SCX=SCR.x+SCR.w/2, SCY=SCR.y+SCR.h/2;
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)), ease=x=>x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2, easeOut=x=>1-Math.pow(1-x,3);
const R2=x=>Math.round(x*20)/20;
const HL=(GIRO.hl||[]).map(r=>({x:C2.x+r[0]*C2.w,y:C2.y+r[1]*C2.h,w:r[2]*C2.w,h:r[3]*C2.h}));
const TELA0={}; LINES.forEach((l,k)=>{ if(!(l.tela in TELA0)) TELA0[l.tela]=k; });
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');
function telaState(i,t){ const l=LINES[i], k=l.tela, t0=LINES[TELA0[k]].start;
  const st={k, card:k==='n3'?1:0, hl:0, txt:easeOut(clamp((t-t0)/0.5)), rows:clamp((t-t0)/1.2)};
  if(l.hl){ let a=i; while(a>0&&LINES[a-1].hl) a--; st.hl=clamp((t-LINES[a].start-0.55)/0.9); }
  return st; }
function telaSVG(st){
  const T=(x,y,s,w,c,txt,ls=0,fam='Geist',anchor='middle',op=1)=>`<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="${fam}" font-weight="${w}" font-size="${s}" letter-spacing="${ls}" fill="${c}" opacity="${op}">${esc(txt)}</text>`;
  let s=`<rect x="${SCR.x}" y="${SCR.y}" width="${SCR.w}" height="${SCR.h}" rx="18" fill="#07090D"/>`;
  // faixa fixa do canal pirata
  s+=`<rect x="${SCR.x+28}" y="${SCR.y+26}" width="150" height="38" rx="4" fill="#C8102E"/>`+T(SCR.x+103,SCR.y+56,30,400,'#fff','TV SAL',2,'Bangers');
  s+=`<circle cx="${SCR.x+SCR.w-150}" cy="${SCR.y+45}" r="8" fill="#FF3B30"/>`+T(SCR.x+SCR.w-38,SCR.y+54,24,700,'#F4F1E8','AO VIVO',2,'Geist','end');
  const o=R2(st.txt), G=GIRO.telas[st.k]||{};
  if(st.k==='abre'){
    s+=T(SCX,SCY-40,74,400,'#FFD84A','GIRO DE DOMINGO',4,'Bangers','middle',o);
    s+=T(SCX,SCY+26,32,700,'#F4F1E8',G.sub,3,'Geist','middle',o);
    s+=[1,2,3].map((n,k)=>{ const q=clamp(st.rows*3-k); return `<g opacity="${R2(q)}"><circle cx="${SCX-120+k*120}" cy="${SCY+120}" r="38" fill="none" stroke="#FFD84A" stroke-width="5"/>${T(SCX-120+k*120,SCY+138,52,400,'#FFD84A',String(n),0,'Bangers')}</g>`; }).join('');
  }
  if(st.k==='n1'||st.k==='n2'){
    s+=T(SCR.x+46,SCR.y+128,30,700,'#9AA3B2',G.kicker,3,'Geist','start',o);
    G.titulo.forEach((ln,k)=>{ s+=T(SCR.x+46,SCR.y+196+k*62,54,700,'#F4F1E8',ln,0,'Geist','start',o); });
    const y0=SCR.y+196+G.titulo.length*62+18;
    s+=`<rect x="${SCR.x+46}" y="${y0}" width="120" height="4" fill="${st.k==='n1'?'#9AA3B2':'#10B981'}" opacity="${o}"/>`;
    G.linhas.forEach((ln,k)=>{ const q=R2(clamp(st.rows*G.linhas.length-k)); s+=T(SCR.x+46,y0+56+k*46,32,500,'#C9D6E8',ln,0,'Geist','start',q); });
    s+=T(SCR.x+46,SCR.y+SCR.h-34,22,500,'#7E8796',G.fonte,0,'Geist','start',o);
  }
  if(st.card>0) s+=`<image href="${GIRO.card.img}" x="${C2.x}" y="${C2.y}" width="${C2.w}" height="${C2.h}" clip-path="url(#cardclip2)"/>`;
  if(st.hl>0) s+=HL.map((r,k)=>{ const p=clamp(st.hl*2-k); return p>0?`<rect x="${r.x-3}" y="${r.y-2}" width="${r.w*p+6}" height="${r.h+4}" rx="4" fill="#FFD84A" opacity=".28"/><rect x="${r.x-3}" y="${r.y-2}" width="${r.w*p+6}" height="${r.h+4}" rx="4" fill="none" stroke="#FFD84A" stroke-width="2.5" filter="url(#glow)"/>`:''; }).join('');
  if(st.k==='agenda'){
    s+=T(SCX,SCR.y+140,56,400,'#FFD84A','AGENDA DA SEMANA',3,'Bangers','middle',o);
    G.itens.forEach(([d,w],k)=>{ const q=R2(clamp(st.rows*G.itens.length-k)), y=SCR.y+222+k*82;
      s+=`<g opacity="${q}"><rect x="${SCR.x+46}" y="${y-48}" width="150" height="66" rx="8" fill="#10B981" opacity=".18"/>${T(SCR.x+121,y,42,700,'#34D399',d)}${T(SCR.x+222,y-2,36,700,'#F4F1E8',w,0,'Geist','start')}</g>`; });
    s+=T(SCX,SCR.y+SCR.h-34,22,500,'#7E8796',G.fonte,0,'Geist','middle',o);
  }
  s+=`<rect x="${SCR.x}" y="${SCR.y}" width="${SCR.w}" height="${SCR.h}" rx="18" fill="url(#crt)" pointer-events="none"/>`;
  return s; }
const extraDefs = `<defs><radialGradient id="crt" cx="50%" cy="45%" r="70%"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".05"/><stop offset="1" stop-color="#000" stop-opacity=".18"/></radialGradient></defs>`;
function shot2Markup(st){
  return `
  <g filter="url(#rough)">
   <rect x="-200" y="-200" width="1480" height="2320" fill="url(#wall)"/><rect x="-200" y="-200" width="1480" height="2320" filter="url(#blotch)" opacity=".8"/>
   <rect x="-200" y="-200" width="1480" height="2320" fill="#2a2418" opacity=".18"/>
   <path d="M300 -200 L300 330" stroke="${K}" stroke-width="3"/><rect x="290" y="324" width="20" height="16" fill="#6B6A63" ${S(3)}/><path d="M282 342 Q282 384 300 388 Q318 384 318 342 Z" fill="#EFE6B8" ${S(3.5)}/>
   <path d="M-220 1315 L1300 1315 L1300 2140 L-220 2140 Z" fill="#5A4772" ${S(6)}/>
   <path d="M980 1315 l100 0 l0 60 Z" fill="#E8DFC4" ${S(4)}/>
   ${burnFace(st,858,525,1.12)}
  </g>
  <image href="tv_asset.png" x="-24" y="610" width="1126" height="713"/>
  <g filter="url(#rough2)"><rect x="-22" y="612" width="1122" height="709" rx="14" fill="none" ${S(7)}/></g>
  ${telaSVG(st.tela)}
  ${st.point?`<g filter="url(#rough2)">${tube([[1100,1005],[1010,985],[920,969]],'#A4473B',58)}
   <path d="M894 961 L842 965 Q832 973 842 981 L894 981 Z" fill="${SKB}" ${S(5)}/><circle cx="902" cy="969" r="28" fill="${SKB}" ${S(5)}/></g>`:''}`; }

// ---------- montagem ----------
const world=document.getElementById('world'), shot2=document.getElementById('shot2'), fxEl=document.getElementById('fx');
const tvEl=document.getElementById('tv'), dotEl=document.getElementById('dot'), logo=document.getElementById('logo'), sub=document.getElementById('sub');
const ovl=document.getElementById('ovl');
world.innerHTML = defs + extraDefs + `<g id="cam"><g filter="url(#rough)">${room}</g>${tvSmall}<g filter="url(#rough)">${tvSmallLine}</g>
  <g id="tvsmall"></g><g filter="url(#rough)">${couchBack}${couchFront}</g>
  <g id="mana" filter="url(#rough2)"></g><g id="burn" filter="url(#rough2)"></g><g filter="url(#rough)">${table}</g></g>`;
shot2.innerHTML = defs + extraDefs + '<g id="s2cam"><g id="s2"></g></g>';
fxEl.innerHTML = `<defs><radialGradient id="vig" cx="50%" cy="48%" r="72%"><stop offset="62%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#000" stop-opacity=".35"/></radialGradient></defs>
  ${defs}<rect width="1080" height="1920" filter="url(#grain)" opacity=".45"/><rect width="1080" height="1920" fill="url(#vig)"/>`;
const tvSmallG=world.querySelector('#tvsmall');
const manaG=world.querySelector('#mana'), burnG=world.querySelector('#burn'), camG=world.querySelector('#cam'), s2=shot2.querySelector('#s2'), s2cam=shot2.querySelector('#s2cam');
const credEl=document.getElementById('cred');
document.querySelector('#bug .b').textContent=GIRO.bug;
let CARD_OK=false; { const im=new Image(); im.onload=()=>{CARD_OK=true;}; im.src=GIRO.card.img; }
window.READY=()=>CARD_OK;
const SMALL={x:679,y:545,w:262,h:210};
function telaPequena(st){ const s=SMALL.w/SCR.w; return `<g transform="translate(${SMALL.x} ${SMALL.y}) scale(${s}) translate(${-SCR.x} ${-SCR.y})">${telaSVG(st)}</g>`; }

function seq(i){ const sh=LINES[i].shot; let a=i; while(a>0&&LINES[a-1].shot===sh) a--; let b=i; while(b<LINES.length-1&&LINES[b+1].shot===sh) b++;
  return [LINES[a].start, b+1<LINES.length?LINES[b+1].start:T_SLAM]; }
const FIT=(1080-20)/SCR.w;
function s2Target(k,t){ const sh=LINES[k].shot, [t0,t1]=seq(k), p=clamp((t-t0)/(t1-t0));
  if(sh==='tvtext'){ const z=FIT, f=1+0.05*easeOut(p); return {s:z/1.05*f,cx:SCX,cy:SCR.y,tx:540,ty:300}; }
  if(sh==='tv2') return {s:1.12+0.08*ease(p),cx:431,cy:963,tx:540,ty:960};
  return {s:1+0.06*p,cx:432,cy:963,tx:432,ty:963}; }
function s2Cam(i,t){ let c=s2Target(i,t); const l=LINES[i];
  if(i>0 && TVSHOTS.includes(LINES[i-1].shot) && LINES[i-1].shot!==l.shot && t-l.start<0.4){ const a=s2Target(i-1,l.start), q=ease(clamp((t-l.start)/0.4));
    c={s:a.s+(c.s-a.s)*q,cx:a.cx+(c.cx-a.cx)*q,cy:a.cy+(c.cy-a.cy)*q,tx:a.tx+(c.tx-a.tx)*q,ty:a.ty+(c.ty-a.ty)*q}; }
  const s=Math.min(c.s,FIT); let cx=c.cx; const L=c.tx+s*(SCR.x-cx), R=c.tx+s*(SCR.x+SCR.w-cx);   // trava do kit: tela inteira na largura
  if(L<10) cx=SCR.x-(10-c.tx)/s; else if(R>1070) cx=SCR.x+SCR.w-(1070-c.tx)/s;
  return {s,cx,cy:c.cy,tx:c.tx,ty:c.ty}; }
function lineAt(t){let i=-1;LINES.forEach((l,k)=>{if(t>=l.start-0.02)i=k;});return i;}
function mouthFor(k,t){ if(k<0) return 'closed'; const l=LINES[k]; const j=Math.floor((t-l.start)*12);
  if(j<0||j>=l.env.length) return 'closed'; const v=l.env[j]; return v>0.55?'open':v>0.22?'mid':'closed'; }
function speaking(who,t){ let k=-1; LINES.forEach((l,i)=>{ if(l.who===who && t>=l.start && t<l.start+l.dur) k=i; }); return k; }
function blinking(arr,t){return arr.some(b=>t>=b&&t<b+0.12);}
function camera(t,i){ const sh=LINES[i].shot, [t0,t1]=seq(i), p=clamp((t-t0)/(t1-t0));
  if(sh==='cuM') return {s:1.45+0.03*p,cx:235,cy:650,tx:520,ty:922};
  if(sh==='cuB') return {s:1.5+0.03*p,cx:485,cy:700,tx:560,ty:832};
  if(sh==='push'){ const q=ease(p); return {s:1+0.12*q,cx:540-140*q,cy:675+85*q,tx:540,ty:875+128*q}; }
  return {s:1+0.03*p,cx:540,cy:675,tx:540,ty:875}; }
// faixa numerada (fica o bloco inteiro) + manchete de abertura (legível sem som)
function ovlHTML(i,t){ const l=LINES[i];
  if(l.ovl==='manchete'){ const o=easeOut(clamp((t-0.05)/0.35)); return `<div class="m" style="opacity:${R2(o)}">${GIRO.manchete}</div>`; }
  if(!l.faixa || l.shot==='tvtext') return '';   /* no zoom no texto, nada por cima da carta */
  const f=GIRO.faixas[l.faixa]; let a=i; while(a>0&&LINES[a-1].faixa===l.faixa) a--;
  const o=easeOut(clamp((t-LINES[a].start)/0.3));
  return `<div class="fx" style="opacity:${R2(o)};transform:translateX(${R2((1-o)*-30)}px)"><b>${f[0]}</b><span>${f[1]}</span></div>`; }

let last='';
function render(t){
  const i=Math.max(0,lineAt(t)), l=LINES[i], tq=Math.floor(t*12)/12, shot=l.shot;
  const kM=speaking('M',tq), kB=speaking('B',tq), mM=mouthFor(kM,tq), mB=mouthFor(kB,tq);
  const bM=blinking(BLINK_M,tq), bB=blinking(BLINK_B,tq);
  const ts=telaState(i,t), tk=[ts.k,R2(ts.card),R2(ts.hl),R2(ts.rows),R2(ts.txt)].join();
  const bob=x=>x==='open';
  const key=[i,mM,mB,bM,bB,shot,tk].join();
  if(key!==last){ last=key;
    if(TVSHOTS.includes(shot)){ shot2.style.display='block'; world.style.display='none';
      s2.innerHTML = shot2Markup({look:l.lB,brow:l.bB,mouth:mB,blink:bB,bob:bob(mB),tela:ts,point:l.pB==='point_tv'}); }
    else { shot2.style.display='none'; world.style.display='block'; tvSmallG.innerHTML=telaPequena(ts);
      manaG.innerHTML = manaHeadBack()+manaLegs()+manaTorso()+manaHead({look:l.lM,brow:l.bM,mouth:mM,blink:bM,bob:bob(mM)})+manaArms(l.pM,false);
      burnG.innerHTML = burnLegs()+burnTorso()+burnHead({look:l.lB,brow:l.bB,mouth:mB,blink:bB,bob:bob(mB)})+burnArms(l.pB); }
  }
  const cr=(GIRO.telas[ts.k]||{}).cred||''; if(credEl.dataset.h!==cr){ credEl.innerHTML=cr; credEl.dataset.h=cr; credEl.style.display=cr?'block':'none'; }
  if(TVSHOTS.includes(shot)){ const q=s2Cam(i,t); s2cam.setAttribute('transform',`translate(${q.tx} ${q.ty}) scale(${q.s}) translate(${-q.cx} ${-q.cy})`); }
  else { const c=camera(t,i); camG.setAttribute('transform',`translate(${c.tx} ${c.ty}) scale(${c.s}) translate(${-c.cx} ${-c.cy})`); }
  const oh=t<T_SLAM?ovlHTML(i,t):''; if(ovl.dataset.h!==oh){ ovl.innerHTML=oh; ovl.dataset.h=oh; }
  const ks=[kM,kB].filter(k=>k>=0); const k=ks.length?Math.max(...ks):-1;
  let txt=''; if(k>=0) txt=LINES[k].text; else { const j=lineAt(t); if(j>=0 && t<LINES[j].start+LINES[j].dur+0.25) txt=LINES[j].text; }
  if(t>=T_SLAM) txt='';
  const html=txt.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/\*([^*]+)\*/g,'<span class="k">$1</span>');
  if(sub.dataset.h!==html){ sub.innerHTML=html; sub.dataset.h=html; }
  // TV liga no início; no fim o Mana desliga: a imagem encolhe até virar o ponto, que fica verde (o fecho do scanner entra depois)
  let sx=1, sy=1, br=1, op=1;
  if(t<0.22){ const p=clamp(t/0.22); sy=Math.max(0.006,ease(p)); sx=p<0.35?0.6+p:1; br=1+3*(1-p); }
  if(t>=T_SLAM){ const a=clamp((t-T_SLAM)/0.24), b=clamp((t-T_SLAM-0.24)/0.18);
    sy=Math.max(0.004,1-ease(a)); sx=1-0.985*ease(b); br=1+5*a; op = t>T_SLAM+0.44 ? 0 : 1; }
  tvEl.style.transform=`scale(${sx},${sy})`; tvEl.style.filter=`brightness(${br})`; tvEl.style.opacity=op;
  logo.style.opacity=0; dotEl.innerHTML='';
  if(t>=T_SLAM+0.30){ const g=clamp((t-T_SLAM-0.34)/0.16), col=g>0.5?'#10B981':'#F4F1E8';
    dotEl.innerHTML=`<circle cx="540" cy="960" r="12" fill="${col}"/><circle cx="540" cy="960" r="28" fill="${col}" opacity=".3"/>`; }
}
window.render=render;
