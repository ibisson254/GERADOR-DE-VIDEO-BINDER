// ---------- especial: noite na sala, a TV é a única luz ----------
// (a primeira metade do ficheiro, com sala, dupla e TV, vem do index.html do kit sem alterações)
const TVSHOTS=['tv','tv2'];
const C2={x:245,y:703,w:373,h:520}, SCR={x:79,y:682,w:704,h:562}, SCX=SCR.x+SCR.w/2, SCY=SCR.y+SCR.h/2;
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)), ease=x=>x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2;
const easeOut=x=>1-Math.pow(1-x,3);
// primeiro bloco em que cada estado da TV aparece: os fades contam a partir dali
const TELA0={}; LINES.forEach(l=>{ if(!(l.tela in TELA0)) TELA0[l.tela]=l.start; });
function telaState(i,t){ const l=LINES[i], k=l.tela, t0=TELA0[k];
  const st={k, card:0, cardDim:0, txt:0, q:0};
  if(k==='revela'){ st.card=ease(clamp((t-0.35)/3.3)); st.outline=1-clamp((t-2.4)/1.2); }
  else if(k==='carta'){ st.card=1; }
  else if(k==='nome'){ st.card=1-clamp((t-t0)/0.45); st.txt=easeOut(clamp((t-t0-0.25)/0.8)); }
  else if(k==='apaga'){ st.card=1-ease(clamp((t-t0-0.3)/(l.dur+0.2))); }
  else if(k==='frase'){ st.txt=easeOut(clamp((t-t0-0.05)/0.9)); }
  else if(k==='obrigado'){ st.txt=easeOut(clamp((t-t0)/0.7)); st.q=easeOut(clamp((t-(l.start+l.dur+0.15))/0.5)); }
  return st; }
const R2=x=>Math.round(x*20)/20;
// o que passa na tela da TV, em coordenadas do plano da TV (escala 1); g = função de escala para a TV pequena
function telaSVG(st){
  const T=(x,y,s,w,c,txt,ls=0)=>`<text x="${x}" y="${y}" text-anchor="middle" font-family="Geist" font-weight="${w}" font-size="${s}" letter-spacing="${ls}" fill="${c}">${txt}</text>`;
  let s='';
  if(st.outline>0) s+=`<rect x="${C2.x}" y="${C2.y}" width="${C2.w}" height="${C2.h}" rx="16" fill="none" stroke="#C9D6E8" stroke-width="2" opacity="${R2(0.35*st.outline)}"/>`;
  if(st.card>0) s+=`<image href="${EP.card.img}" x="${C2.x}" y="${C2.y}" width="${C2.w}" height="${C2.h}" clip-path="url(#cardclip2)" opacity="${R2(st.card)}"/>`;
  const o=R2(st.txt);
  if(o>0 && st.k==='nome') s+=`<g opacity="${o}">${T(SCX,SCY-22,46,700,'#F4F1E8','SIR PATRICK STEWART',5)}
     <rect x="${SCX-60}" y="${SCY+4}" width="120" height="2" fill="#C9D6E8" opacity=".6"/>${T(SCX,SCY+56,36,500,'#AAB4C3','1940–2026',3)}</g>`;
  if(o>0 && st.k==='frase') s+=`<g opacity="${o}">${T(SCX,SCY-12,44,700,'#F4F1E8','O que fica não cabe')}${T(SCX,SCY+46,44,700,'#F4F1E8','numa carta.')}</g>`;
  if(o>0 && st.k==='obrigado') s+=`<g opacity="${o}">${T(SCX,SCY-40,48,700,'#F4F1E8','OBRIGADO, SIR PATRICK.',3)}</g>
     <g opacity="${R2(st.q)}">${T(SCX,SCY+48,40,500,'#C9D6E8','Qual memória do Picard')}${T(SCX,SCY+100,40,500,'#C9D6E8','você leva com você?')}</g>`;
  // brilho de tubo: leve, por cima de tudo na tela
  s+=`<rect x="${SCR.x}" y="${SCR.y}" width="${SCR.w}" height="${SCR.h}" rx="18" fill="url(#crt)" pointer-events="none"/>`;
  return s; }
const extraDefs = `<defs><radialGradient id="crt" cx="50%" cy="45%" r="70%"><stop offset="0" stop-color="#9FC3FF" stop-opacity=".07"/><stop offset="1" stop-color="#000" stop-opacity=".28"/></radialGradient>
  <radialGradient id="tvglow" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(810 650) scale(620 560)">
   <stop offset="0" stop-color="#8FB4FF" stop-opacity=".30"/><stop offset=".45" stop-color="#6E8FD0" stop-opacity=".12"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
  <mask id="semtv"><rect x="-400" y="-300" width="1900" height="2400" fill="#fff"/><rect x="679" y="545" width="262" height="210" rx="10" fill="#000"/></mask>
  <radialGradient id="noite" cx="50%" cy="46%" r="75%"><stop offset="50%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#000" stop-opacity=".55"/></radialGradient></defs>`;

function shot2Markup(st){
  return `
  <g filter="url(#rough)">
   <rect x="-200" y="-200" width="1480" height="2320" fill="url(#wall)"/><rect x="-200" y="-200" width="1480" height="2320" filter="url(#blotch)" opacity=".8"/>
   <rect x="-200" y="-200" width="1480" height="2320" fill="#2a2418" opacity=".25"/>
   <path d="M300 -200 L300 330" stroke="${K}" stroke-width="3"/><rect x="290" y="324" width="20" height="16" fill="#6B6A63" ${S(3)}/><path d="M282 342 Q282 384 300 388 Q318 384 318 342 Z" fill="#8F8A72" ${S(3.5)}/>
   <path d="M-220 1315 L1300 1315 L1300 2140 L-220 2140 Z" fill="#5A4772" ${S(6)}/>
   <path d="M980 1315 l100 0 l0 60 Z" fill="#E8DFC4" ${S(4)}/>
   ${burnFace(st,858,525,1.12)}
  </g>
  <rect x="-200" y="-200" width="1480" height="2320" fill="#070B14" opacity=".58"/>
  <ellipse cx="430" cy="960" rx="760" ry="520" fill="#8FB4FF" opacity=".10"/>
  <image href="tv_asset.png" x="-24" y="610" width="1126" height="713"/>
  <g filter="url(#rough2)"><rect x="-22" y="612" width="1122" height="709" rx="14" fill="none" ${S(7)}/></g>
  ${telaSVG(st.tela)}`; }

// ---------- montagem ----------
const world=document.getElementById('world'), shot2=document.getElementById('shot2'), fxEl=document.getElementById('fx');
const tvEl=document.getElementById('tv'), dotEl=document.getElementById('dot'), logo=document.getElementById('logo'), sub=document.getElementById('sub');
const ovl=document.getElementById('ovl');
world.innerHTML = defs + extraDefs + `<g id="cam"><g filter="url(#rough)">${room}</g>${tvSmall}<g filter="url(#rough)">${tvSmallLine}</g>
  <g id="tvsmall"></g><g filter="url(#rough)">${couchBack}${couchFront}</g>
  <g id="mana" filter="url(#rough2)"></g><g id="burn" filter="url(#rough2)"></g><g filter="url(#rough)">${table}</g>
  <rect x="-400" y="-300" width="1900" height="2400" fill="#070B14" opacity=".62" mask="url(#semtv)"/>
  <rect x="-400" y="-300" width="1900" height="2400" fill="url(#tvglow)" style="mix-blend-mode:screen"/></g>`;
shot2.innerHTML = defs + extraDefs + '<g id="s2cam"><g id="s2"></g></g>';
fxEl.innerHTML = `<defs><radialGradient id="vig" cx="50%" cy="48%" r="70%"><stop offset="60%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#000" stop-opacity=".45"/></radialGradient></defs>
  ${defs}${extraDefs}<rect width="1080" height="1920" filter="url(#grain)" opacity=".45"/><rect width="1080" height="1920" fill="url(#vig)"/><rect width="1080" height="1920" fill="url(#noite)"/>`;
const tvSmallG=world.querySelector('#tvsmall');
const manaG=world.querySelector('#mana'), burnG=world.querySelector('#burn'), camG=world.querySelector('#cam'), s2=shot2.querySelector('#s2'), s2cam=shot2.querySelector('#s2cam');
const credEl=document.getElementById('cred'); credEl.innerHTML=EP.card.cred;
document.querySelector('#bug .b').textContent='HOMENAGEM';
let CARD_OK=false; { const im=new Image(); im.onload=()=>{CARD_OK=true;}; im.src=EP.card.img; }
window.READY=()=>CARD_OK;

// a TV pequena (planos da sala) mostra o mesmo que a TV grande, reduzida para a tela dela
const SMALL={x:679,y:545,w:262,h:210};
function telaPequena(st){ const s=SMALL.w/SCR.w;
  return `<g transform="translate(${SMALL.x} ${SMALL.y}) scale(${s}) translate(${-SCR.x} ${-SCR.y})">${telaSVG(st)}</g>`; }

function s2Target(k,t){ const sh=LINES[k].shot, l=LINES[k];
  // conta o tempo desde o início da sequência de blocos com o mesmo plano: o movimento é contínuo, sem saltos
  let a=k; while(a>0 && LINES[a-1].shot===sh) a--; let b=k; while(b<LINES.length-1 && LINES[b+1].shot===sh) b++;
  const t0=LINES[a].start, t1=(b+1<LINES.length?LINES[b+1].start:T_SLAM), p=clamp((t-t0)/(t1-t0));
  if(sh==='tv2') return {s:1.12+0.08*ease(p),cx:431,cy:963,tx:540,ty:960};   // aproxima devagar da carta
  return {s:1+0.05*p,cx:432,cy:963,tx:432,ty:963}; }
function s2Cam(i,t){ let c=s2Target(i,t); const l=LINES[i];
  if(i>0 && TVSHOTS.includes(LINES[i-1].shot) && LINES[i-1].shot!==l.shot && t-l.start<0.6){ const a=s2Target(i-1,l.start), q=ease(clamp((t-l.start)/0.6));
    c={s:a.s+(c.s-a.s)*q,cx:a.cx+(c.cx-a.cx)*q,cy:a.cy+(c.cy-a.cy)*q,tx:a.tx+(c.tx-a.tx)*q,ty:a.ty+(c.ty-a.ty)*q}; }
  // trava de enquadramento do kit: a tela inteira da TV cabe sempre na largura (margem de 10 px)
  const FIT=(1080-20)/SCR.w, s=Math.min(c.s,FIT); let cx=c.cx;
  const L=c.tx+s*(SCR.x-cx), R=c.tx+s*(SCR.x+SCR.w-cx);
  if(L<10) cx=SCR.x-(10-c.tx)/s; else if(R>1070) cx=SCR.x+SCR.w-(1070-c.tx)/s;
  return {s,cx,cy:c.cy,tx:c.tx,ty:c.ty}; }
function lineAt(t){let i=-1;LINES.forEach((l,k)=>{if(t>=l.start-0.02)i=k;});return i;}
function mouthFor(k,t){ if(k<0) return 'closed'; const l=LINES[k]; const j=Math.floor((t-l.start)*12);
  if(j<0||j>=l.env.length) return 'closed'; const v=l.env[j]; return v>0.55?'mid':v>0.18?'mid':'closed'; }   // fala contida: boca nunca escancara
function speaking(who,t){ let k=-1; LINES.forEach((l,i)=>{ if(l.who===who && t>=l.start && t<l.start+l.dur) k=i; }); return k; }
function blinking(arr,t){return arr.some(b=>t>=b&&t<b+0.14);}
function camera(t,i){ const sh=LINES[i].shot;
  let a=i; while(a>0 && LINES[a-1].shot===sh) a--; let b=i; while(b<LINES.length-1 && LINES[b+1].shot===sh) b++;
  const t0=LINES[a].start, t1=(b+1<LINES.length?LINES[b+1].start:T_SLAM), p=clamp((t-t0)/(t1-t0));
  const W={s:1,cx:540,cy:675,tx:540,ty:875};
  if(sh==='cuM') return {s:1.45+0.04*p,cx:235,cy:650,tx:520,ty:922};
  if(sh==='cuB') return {s:1.5+0.04*p,cx:485,cy:700,tx:560,ty:832};
  if(sh==='pull'){ const q=ease(p); return {s:1.12-0.12*q,cx:400+140*q,cy:760-85*q,tx:540,ty:1003-128*q}; }
  return {s:1+0.04*p,cx:540,cy:675,tx:540,ty:875};   // wide: aproxima 4% devagar
}
// textos na tela (fora da TV), na faixa entre os créditos e a TV
function ovlHTML(i,t){ const l=LINES[i]; if(!l.ovl) return '';
  if(l.ovl==='virtudes'){ const W=['Inteligência.','Firmeza.','Humanidade.'], at=[0.50,0.68,0.84];
    return W.map((w,k)=>{ const o=easeOut(clamp((t-(l.start+l.dur*at[k]))/0.45)); return `<div class="v" style="opacity:${R2(o)};transform:translateY(${R2((1-o)*14)}px)">${w}</div>`; }).join(''); }
  if(l.ovl==='data'){ let a=i; while(a>0 && LINES[a-1].ovl==='data') a--; const o=easeOut(clamp((t-LINES[a].start-0.2)/0.6));
    return `<div class="d" style="opacity:${R2(o)}">13 NOVEMBRO 2026</div><div class="d2" style="opacity:${R2(o)}">MAGIC: THE GATHERING | STAR TREK</div>`; }
  return ''; }

let last='';
function render(t){
  const i=Math.max(0,lineAt(t)), l=LINES[i], tq=Math.floor(t*12)/12, shot=l.shot;
  const kM=speaking('M',tq), kB=speaking('B',tq);
  const mM=mouthFor(kM,tq), mB=mouthFor(kB,tq);
  const bM=blinking(BLINK_M,tq), bB=blinking(BLINK_B,tq);
  const ts=telaState(i,t), tk=[ts.k,R2(ts.card),R2(ts.txt),R2(ts.q),R2(ts.outline||0)].join();
  const key=[i,mM,mB,bM,bB,shot,tk].join();
  if(key!==last){ last=key;
    if(TVSHOTS.includes(shot)){ shot2.style.display='block'; world.style.display='none';
      s2.innerHTML = shot2Markup({look:'screen',brow:'normal',mouth:mB,blink:bB,bob:false,tela:ts}); }
    else { shot2.style.display='none'; world.style.display='block'; tvSmallG.innerHTML=telaPequena(ts);
      manaG.innerHTML = manaHeadBack()+manaLegs()+manaTorso()+manaHead({look:'tv',brow:'flat',mouth:mM,blink:bM,bob:false})+manaArms('rest',false);
      burnG.innerHTML = burnLegs()+burnTorso()+burnHead({look:'tv',brow:'normal',mouth:mB,blink:bB,bob:false})+burnArms('rest'); }
  }
  if(TVSHOTS.includes(shot)){ const q=s2Cam(i,t); s2cam.setAttribute('transform',`translate(${q.tx} ${q.ty}) scale(${q.s}) translate(${-q.cx} ${-q.cy})`); }
  else { const c=camera(t,i); camG.setAttribute('transform',`translate(${c.tx} ${c.ty}) scale(${c.s}) translate(${-c.cx} ${-c.cy})`); }
  const oh=t<T_SLAM?ovlHTML(i,t):''; if(ovl.dataset.h!==oh){ ovl.innerHTML=oh; ovl.dataset.h=oh; }
  // legenda: o bloco de quem está falando; fica 0,25 s depois da fala
  const ks=[kM,kB].filter(k=>k>=0); const k=ks.length?Math.max(...ks):-1;
  let txt=''; if(k>=0) txt=LINES[k].text; else { const j=lineAt(t); if(j>=0 && t<LINES[j].start+LINES[j].dur+0.25) txt=LINES[j].text; }
  if(t>=T_SLAM) txt='';
  const html=txt.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/\*([^*]+)\*/g,'<span class="k">$1</span>');
  if(sub.dataset.h!==html){ sub.innerHTML=html; sub.dataset.h=html; }
  // liga e desliga a TV (como em todo episódio da série)
  let sx=1, sy=1, br=1, op=1;
  if(t<0.22){ const p=clamp(t/0.22); sy=Math.max(0.006,ease(p)); sx=p<0.35?0.6+p:1; br=1+3*(1-p); }
  if(t>=T_SLAM){ const a=clamp((t-T_SLAM)/0.24), b=clamp((t-T_SLAM-0.24)/0.18);
    sy=Math.max(0.004,1-ease(a)); sx=1-0.985*ease(b); br=1+5*a; op = t>T_SLAM+0.44 ? 0 : 1; }
  tvEl.style.transform=`scale(${sx},${sy})`; tvEl.style.filter=`brightness(${br})`; tvEl.style.opacity=op;
  dotEl.innerHTML=''; logo.style.opacity=0;
  if(t>=T_SLAM+0.30){
    const u=clamp((t-T_SLAM-0.36)/0.22), v=clamp((t-T_SLAM-0.50)/0.38);
    const cy=960-120*ease(u), r=8+22*ease(u), col=u<0.5?'#FFFFFF':'#10B981';
    if(v<0.6) dotEl.innerHTML=`<g opacity="${1-v/0.6}"><circle cx="540" cy="${cy}" r="${r+14*(1-u)}" fill="${col}" opacity=".25"/><circle cx="540" cy="${cy}" r="${r}" fill="${col}"/></g>`;
    if(v>0){ logo.style.opacity=1; drawLogo(v, clamp((t-T_SLAM-0.72)/0.28)); }
  }
  const fade=clamp((t-(T_END-0.45))/0.45); document.body.style.filter = fade>0?`brightness(${1-fade})`:'';
}
const backOut=x=>{const c=1.7;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2);};
// assinatura discreta: símbolo + BINDER Originals (sem CTA do app neste especial)
function drawLogo(v,q){
  const svg=document.getElementById('logosvg'), sc=Math.max(0.03,0.75*backOut(v)), rot=-140*(1-(1-Math.pow(1-v,3)));
  svg.innerHTML=`<g transform="translate(540 860) rotate(${rot}) scale(${sc}) translate(-540 -860)">
      <image href="logo/logo_mark.png" x="390" y="710" width="300" height="300"/></g>
    <text x="540" y="1090" text-anchor="middle" font-family="Geist" font-weight="700" font-size="64" fill="#fff"
      opacity="${q}" transform="translate(0 ${(1-q)*18})">BINDER <tspan fill="#10B981">Originals</tspan></text>`;
  const sh=document.querySelector('#logo .show'); sh.style.opacity=q; sh.style.transform=`translateY(${(1-q)*20}px)`;
}
window.render=render;
