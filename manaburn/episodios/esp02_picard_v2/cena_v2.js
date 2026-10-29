// ---------- Especial Picard v2: celebração · sala de dia, luz quente ----------
// (a primeira metade do ficheiro, com sala, dupla, TV e mesa, vem do manaburn/index.html do kit sem alterações)
const TVSHOTS=['tv','tv2','tvtext'];
const C2={x:245,y:703,w:373,h:520}, SCR={x:79,y:682,w:704,h:562}, SCX=SCR.x+SCR.w/2, SCY=SCR.y+SCR.h/2;
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)), ease=x=>x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2, easeOut=x=>1-Math.pow(1-x,3);
const R2=x=>Math.round(x*20)/20;
// destaque no Seek out (medido no PNG 744x1040: linhas 835-862, 866-893, 896-923)
const HL=[[0.383,0.802,0.520,0.030],[0.086,0.833,0.817,0.030],[0.086,0.862,0.775,0.030]].map(r=>({x:C2.x+r[0]*C2.w,y:C2.y+r[1]*C2.h,w:r[2]*C2.w,h:r[3]*C2.h}));
const TELA0={}; LINES.forEach((l,k)=>{ if(!(l.tela in TELA0)) TELA0[l.tela]=k; });
const BAN=[['Q, Stacking the Deck','Ep. 1'],['Stasis','Ep. 2'],['The Tabernacle at Pendrell Vale','Ep. 8'],['Dack Fayden, Helping Hand','Ep. 9']];
function telaState(i,t){ const l=LINES[i], k=l.tela, l0=LINES[TELA0[k]], t0=l0.start;
  const st={k, card:1, hl:0, rows:0, stamp:0, txt:0};
  if(l.hl){ let a=i; while(a>0&&LINES[a-1].hl) a--; st.hl=clamp((t-LINES[a].start-0.55)/0.9); }
  if(k==='lista'){ st.card=0; st.rows=clamp((t-t0+0.15)/1.0); const ts=l0.start+l0.dur*0.78; st.stamp=clamp((t-ts)/0.12); st.pop=t>=ts&&t<ts+0.3?1-(t-ts)/0.3:0; }
  if(k==='nome'){ st.card=1-clamp((t-t0)/0.45); st.txt=easeOut(clamp((t-t0-0.2)/0.8)); }
  return st; }
function telaSVG(st){
  const T=(x,y,s,w,c,txt,ls=0,fam='Geist',anchor='middle')=>`<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="${fam}" font-weight="${w}" font-size="${s}" letter-spacing="${ls}" fill="${c}">${txt}</text>`;
  let s='';
  if(st.card>0) s+=`<image href="${EP.card.img}" x="${C2.x}" y="${C2.y}" width="${C2.w}" height="${C2.h}" clip-path="url(#cardclip2)" opacity="${R2(st.card)}"/>`;
  if(st.hl>0) s+=HL.map((r,k)=>{ const p=clamp(st.hl*3-k); return p>0?`<rect x="${r.x-3}" y="${r.y-2}" width="${r.w*p+6}" height="${r.h+4}" rx="4" fill="#FFD84A" opacity=".28"/><rect x="${r.x-3}" y="${r.y-2}" width="${r.w*p+6}" height="${r.h+4}" rx="4" fill="none" stroke="#FFD84A" stroke-width="2.5" filter="url(#glow)"/>`:''; }).join('');
  if(st.k==='lista'){
    const x0=SCR.x+46, y0=SCR.y+78, n=Math.floor(st.rows*(BAN.length+1)+0.001);
    s+=T(SCX,SCR.y+56,40,400,'#FFD84A','LISTA DE BANIMENTO DO BURN',2,'Bangers');
    s+=T(SCX,SCR.y+80,17,500,'#AAB4C3','(opinião dele, não da Wizards)');
    BAN.forEach(([nm,ep],k)=>{ if(k>=n) return; const y=y0+52+k*66;
      s+=T(x0,y,27,700,'#F4F1E8',nm,0,'Geist','start')+T(x0,y+24,16,500,'#9AA3B2',`Mana & Burn ${ep}`,0,'Geist','start');
      s+=`<g transform="rotate(-6 ${SCR.x+SCR.w-112} ${y-8})"><rect x="${SCR.x+SCR.w-186}" y="${y-34}" width="148" height="44" rx="6" fill="none" stroke="#FF5A4E" stroke-width="4"/>${T(SCR.x+SCR.w-112,y-3,30,400,'#FF5A4E','BANIDO',2,'Bangers')}</g>`; });
    if(n>BAN.length){ const y=y0+52+BAN.length*66+14;
      s+=`<rect x="${x0-14}" y="${y-38}" width="${SCR.w-64}" height="64" rx="8" fill="#10B981" opacity=".14"/>`;
      s+=T(x0,y,30,700,'#FFFFFF','Jean-Luc Picard, Luminary',0,'Geist','start')+T(x0,y+22,16,500,'#C9D6E8','capitão da Enterprise',0,'Geist','start');
      if(st.stamp>0){ const sc=1+0.6*(1-st.stamp)+0.15*(st.pop||0);
        s+=`<g opacity="${R2(st.stamp)}" transform="translate(${SCR.x+SCR.w-112} ${y-10}) rotate(-8) scale(${sc.toFixed(2)})"><rect x="-84" y="-30" width="168" height="54" rx="6" fill="#10B981" opacity=".2"/><rect x="-84" y="-30" width="168" height="54" rx="6" fill="none" stroke="#10B981" stroke-width="5"/>${T(0,10,40,400,'#34D399','NUNCA',3,'Bangers')}</g>`; } } }
  const o=R2(st.txt);
  if(o>0 && st.k==='nome') s+=`<g opacity="${o}">${T(SCX,SCY-40,46,700,'#F4F1E8','SIR PATRICK STEWART',5)}
     <rect x="${SCX-60}" y="${SCY-14}" width="120" height="3" fill="#10B981"/>${T(SCX,SCY+34,34,500,'#C9D6E8','1940–2026',3)}${T(SCX,SCY+96,30,500,'#FFD84A','deu vida ao capitão Picard')}</g>`;
  s+=`<rect x="${SCR.x}" y="${SCR.y}" width="${SCR.w}" height="${SCR.h}" rx="18" fill="url(#crt)" pointer-events="none"/>`;
  return s; }
const extraDefs = `<defs><radialGradient id="crt" cx="50%" cy="45%" r="70%"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".05"/><stop offset="1" stop-color="#000" stop-opacity=".18"/></radialGradient>
  <linearGradient id="sol" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFC56E" stop-opacity=".30"/><stop offset=".55" stop-color="#FFB34D" stop-opacity=".08"/><stop offset="1" stop-color="#FFB34D" stop-opacity="0"/></linearGradient>
  <linearGradient id="raio" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFE3A8" stop-opacity="0"/><stop offset=".5" stop-color="#FFE3A8" stop-opacity=".16"/><stop offset="1" stop-color="#FFE3A8" stop-opacity="0"/></linearGradient></defs>`;
// luz de fim de tarde: um véu quente e dois feixes de janela fora de quadro (desenho próprio)
const luz = `<rect x="-400" y="-300" width="1900" height="2400" fill="url(#sol)" style="mix-blend-mode:screen"/>
  <g style="mix-blend-mode:screen"><path d="M-120 -80 L120 -80 L760 1400 L460 1400 Z" fill="url(#raio)"/><path d="M180 -80 L300 -80 L980 1400 L820 1400 Z" fill="url(#raio)" opacity=".7"/></g>`;
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
  ${luz}
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
  <g id="mana" filter="url(#rough2)"></g><g id="burn" filter="url(#rough2)"></g><g filter="url(#rough)">${table}</g>${luz}</g>`;
shot2.innerHTML = defs + extraDefs + '<g id="s2cam"><g id="s2"></g></g>';
fxEl.innerHTML = `<defs><radialGradient id="vig" cx="50%" cy="48%" r="72%"><stop offset="62%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#2A1608" stop-opacity=".35"/></radialGradient></defs>
  ${defs}<rect width="1080" height="1920" filter="url(#grain)" opacity=".45"/><rect width="1080" height="1920" fill="url(#vig)"/>`;
const tvSmallG=world.querySelector('#tvsmall');
const manaG=world.querySelector('#mana'), burnG=world.querySelector('#burn'), camG=world.querySelector('#cam'), s2=shot2.querySelector('#s2'), s2cam=shot2.querySelector('#s2cam');
const credEl=document.getElementById('cred'); credEl.innerHTML=EP.card.cred;
document.querySelector('#bug .b').textContent='ESPECIAL · CAPITÃO PICARD';
let CARD_OK=false; { const im=new Image(); im.onload=()=>{CARD_OK=true;}; im.src=EP.card.img; }
window.READY=()=>CARD_OK;
const SMALL={x:679,y:545,w:262,h:210};
function telaPequena(st){ const s=SMALL.w/SCR.w; return `<g transform="translate(${SMALL.x} ${SMALL.y}) scale(${s}) translate(${-SCR.x} ${-SCR.y})">${telaSVG(st)}</g>`; }

function seq(i){ const sh=LINES[i].shot; let a=i; while(a>0&&LINES[a-1].shot===sh) a--; let b=i; while(b<LINES.length-1&&LINES[b+1].shot===sh) b++;
  return [LINES[a].start, b+1<LINES.length?LINES[b+1].start:T_SLAM]; }
const FIT=(1080-20)/SCR.w;
function s2Target(k,t){ const sh=LINES[k].shot, [t0,t1]=seq(k), p=clamp((t-t0)/(t1-t0));
  if(sh==='tvtext'){ const z=FIT, f=1+0.05*easeOut(p); return {s:z/1.05*f,cx:SCX,cy:SCR.y,tx:540,ty:300}; }   // zoom no texto, tela inteira na largura
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
function ovlHTML(i,t){ const l=LINES[i]; if(!l.ovl) return ''; const o=easeOut(clamp((t-l.start-0.15)/0.45));
  const st=`style="opacity:${R2(o)};transform:translateY(${R2((1-o)*14)}px)"`;
  if(l.ovl==='data') return `<div class="d" ${st}>13 NOVEMBRO 2026</div><div class="d2" ${st}>MAGIC: THE GATHERING | STAR TREK</div>`;
  if(l.ovl==='makeitso'){ const q=easeOut(clamp((t-(l.start+l.dur*0.62))/0.35)); return q>0?`<div class="q" style="opacity:${R2(q)};transform:scale(${(0.9+0.1*q).toFixed(2)})">“Make it so.”</div>`:''; }
  if(l.ovl==='cha'){ const q=easeOut(clamp((t-(l.start+l.dur*0.5))/0.35)); return q>0?`<div class="q" style="opacity:${R2(q)}">“Tea. Earl Grey. Hot.”</div>`:''; }
  if(l.ovl==='numeros'){ const it=[['7','temporadas',0.15],['4','filmes',0.45],['1','série com o nome dele',0.72]];
    return `<div class="nums">`+it.map(([n,w,a])=>{ const q=easeOut(clamp((t-(l.start+l.dur*a))/0.3)); return `<div class="n" style="opacity:${R2(q)};transform:translateY(${R2((1-q)*16)}px)"><b>${n}</b> ${w}</div>`; }).join('')+`</div>`; }
  return ''; }

let last='';
function render(t){
  const i=Math.max(0,lineAt(t)), l=LINES[i], tq=Math.floor(t*12)/12, shot=l.shot;
  const kM=speaking('M',tq), kB=speaking('B',tq), mM=mouthFor(kM,tq), mB=mouthFor(kB,tq);
  const bM=blinking(BLINK_M,tq), bB=blinking(BLINK_B,tq);
  const ts=telaState(i,t), tk=[ts.k,R2(ts.card),R2(ts.hl),R2(ts.rows),R2(ts.stamp),R2(ts.pop||0),R2(ts.txt)].join();
  const bob=x=>x==='open';
  const key=[i,mM,mB,bM,bB,shot,tk].join();
  if(key!==last){ last=key;
    if(TVSHOTS.includes(shot)){ shot2.style.display='block'; world.style.display='none';
      s2.innerHTML = shot2Markup({look:l.lB,brow:l.bB,mouth:mB,blink:bB,bob:bob(mB),tela:ts,point:l.pB==='point_tv'}); }
    else { shot2.style.display='none'; world.style.display='block'; tvSmallG.innerHTML=telaPequena(ts);
      manaG.innerHTML = manaHeadBack()+manaLegs()+manaTorso()+manaHead({look:l.lM,brow:l.bM,mouth:mM,blink:bM,bob:bob(mM)})+manaArms(l.pM,false);
      burnG.innerHTML = burnLegs()+burnTorso()+burnHead({look:l.lB,brow:l.bB,mouth:mB,blink:bB,bob:bob(mB)})+burnArms(l.pB); }
  }
  if(TVSHOTS.includes(shot)){ const q=s2Cam(i,t); s2cam.setAttribute('transform',`translate(${q.tx} ${q.ty}) scale(${q.s}) translate(${-q.cx} ${-q.cy})`); }
  else { const c=camera(t,i); camG.setAttribute('transform',`translate(${c.tx} ${c.ty}) scale(${c.s}) translate(${-c.cx} ${-c.cy})`); }
  const oh=t<T_SLAM?ovlHTML(i,t):''; if(ovl.dataset.h!==oh){ ovl.innerHTML=oh; ovl.dataset.h=oh; }
  const ks=[kM,kB].filter(k=>k>=0); const k=ks.length?Math.max(...ks):-1;
  let txt=''; if(k>=0) txt=LINES[k].text; else { const j=lineAt(t); if(j>=0 && t<LINES[j].start+LINES[j].dur+0.25) txt=LINES[j].text; }
  if(t>=T_SLAM) txt='';
  const html=txt.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/\*([^*]+)\*/g,'<span class="k">$1</span>');
  if(sub.dataset.h!==html){ sub.innerHTML=html; sub.dataset.h=html; }
  // liga a TV como em todo episódio; no "Engage" a imagem encolhe e o ponto parte em velocidade
  let sx=1, sy=1, br=1, op=1;
  if(t<0.22){ const p=clamp(t/0.22); sy=Math.max(0.006,ease(p)); sx=p<0.35?0.6+p:1; br=1+3*(1-p); }
  if(t>=T_SLAM){ const a=clamp((t-T_SLAM)/0.24), b=clamp((t-T_SLAM-0.24)/0.18);
    sy=Math.max(0.004,1-ease(a)); sx=1-0.985*ease(b); br=1+5*a; op = t>T_SLAM+0.44 ? 0 : 1; }
  tvEl.style.transform=`scale(${sx},${sy})`; tvEl.style.filter=`brightness(${br})`; tvEl.style.opacity=op;
  dotEl.innerHTML=''; logo.style.opacity=0;
  if(t>=T_SLAM+0.30){
    const u=clamp((t-T_SLAM-0.36)/0.30), v=clamp((t-T_SLAM-0.70)/0.40);
    // o ponto verde estica e dispara para o alto, deixando um rasto (arrancada)
    const y=960-700*Math.pow(u,2.2), len=20+520*Math.sin(Math.PI*clamp(u*1.1)), col='#10B981';
    if(u<1) dotEl.innerHTML=`<defs><linearGradient id="rasto" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="${col}" stop-opacity="0"/><stop offset="1" stop-color="${col}" stop-opacity=".9"/></linearGradient></defs>
      <rect x="532" y="${y}" width="16" height="${len}" rx="8" fill="url(#rasto)"/><circle cx="540" cy="${y}" r="12" fill="#E9FFF6"/><circle cx="540" cy="${y}" r="26" fill="${col}" opacity=".3"/>`;
    if(v>0){ logo.style.opacity=1; drawLogo(v, clamp((t-T_SLAM-1.0)/0.3)); }
  }
  const fade=clamp((t-(T_END-0.4))/0.4); document.body.style.filter = fade>0?`brightness(${1-fade})`:'';
}
const backOut=x=>{const c=1.7;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2);};
function drawLogo(v,q){
  const svg=document.getElementById('logosvg'), sc=Math.max(0.03,0.75*backOut(v)), rot=-140*(1-(1-Math.pow(1-v,3)));
  svg.innerHTML=`<g transform="translate(540 860) rotate(${rot}) scale(${sc}) translate(-540 -860)"><image href="logo/logo_mark.png" x="390" y="710" width="300" height="300"/></g>
    <text x="540" y="1090" text-anchor="middle" font-family="Geist" font-weight="700" font-size="64" fill="#fff" opacity="${q}" transform="translate(0 ${(1-q)*18})">BINDER <tspan fill="#10B981">Originals</tspan></text>
    <text x="540" y="1160" text-anchor="middle" font-family="Geist" font-weight="500" font-size="34" fill="#C9D6E8" opacity="${q}">Obrigado, capitão.</text>`;
  const sh=document.querySelector('#logo .show'); sh.style.opacity=q; sh.style.transform=`translateY(${(1-q)*20}px)`;
}
window.render=render;
