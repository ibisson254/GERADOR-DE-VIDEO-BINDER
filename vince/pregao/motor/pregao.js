// Pregão Magic · motor de composição (canvas 1080x1920, determinístico: render(t) desenha o quadro t)
// Componentes reutilizáveis: carta(), etiqueta(), linhaFonte(), preco(), pctGrande(), painel de fecho.
const cv = document.getElementById("c"), X = cv.getContext("2d");
const W = 1080, H = 1920, R = 1040 / 745;
const COR = { bg:"#050A10", ink:"#F2EFE8", mute:"#8C96A6", verde:"#10B981", verde2:"#34D399",
              verm:"#EF4444", verm2:"#F87171", metal:"#B9A27A", slate:"#0F172A", linha:"#1E293B" };
const IMG = {};
let PRONTO = false;

// ---------- utilitários ----------
const cl = (v,a=0,b=1)=>Math.max(a,Math.min(b,v));
const lin = (t,a,b)=>cl((t-a)/(b-a));
const eOut = p=>1-Math.pow(1-p,3), eIn = p=>p*p*p, eIO = p=>p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2;
const eExp = p=>p>=1?1:1-Math.pow(2,-10*p);
const eBack = p=>{const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(p-1,3)+c1*Math.pow(p-1,2)};
const mix = (a,b,p)=>a+(b-a)*p;
function hash(n){ const s=Math.sin(n*127.1)*43758.5453; return s-Math.floor(s); }
const brl = v=>"R$ "+(v*CAMBIO.taxa).toFixed(2).replace(".",",");
const usd = v=>"US$ "+v.toFixed(2).replace(".",",");
const pctS = p=>(p>0?"+":"−")+Math.abs(p)+"%";

function fonte(px,f="DB"){ X.font = `${px}px ${f}`; }
function txt(s,x,y,px,f,cor,al="left",track=0,alpha=1){
  X.save(); X.globalAlpha*=alpha; fonte(px,f); X.fillStyle=cor; X.textBaseline="alphabetic";
  if(track){ X.letterSpacing = track+"px"; }
  X.textAlign=al; X.fillText(s,x,y); X.restore();
}
function larg(s,px,f,track=0){ X.save(); fonte(px,f); if(track) X.letterSpacing=track+"px"; const w=X.measureText(s).width; X.restore(); return w; }
function quebra(s,px,f,maxw){ const ps=s.split(" "),ls=[]; let l=""; for(const p of ps){ const t=l?l+" "+p:p; if(larg(t,px,f)>maxw&&l){ls.push(l);l=p}else l=t } if(l)ls.push(l); return ls; }

// ---------- carta real (imagem Scryfall inteira, nunca cortada nem recolorida) ----------
function carta(k,cx,cy,w,rot=0,alpha=1,sombra=1,blurV=null){
  const im=IMG[k]; if(!im) return; const h=w*R;
  const amostras = blurV ? 7 : 1;
  for(let i=0;i<amostras;i++){
    const f = amostras>1 ? (i/(amostras-1)-0.5) : 0;
    X.save();
    X.globalAlpha = alpha*(amostras>1 ? (i===amostras-1?0.55:0.16) : 1);
    X.translate(cx+(blurV?blurV[0]*f:0), cy+(blurV?blurV[1]*f:0)); X.rotate(rot);
    if(sombra&&i===amostras-1){ X.shadowColor="rgba(0,0,0,.75)"; X.shadowBlur=60*sombra; X.shadowOffsetY=24*sombra; }
    X.drawImage(im,-w/2,-h/2,w,h); X.restore();
  }
}
// moldura vazia com a geometria exata da carta (usada nos match cuts)
function molduraCarta(cx,cy,w,cor,lw,alpha=1){
  const h=w*R, r=w*0.045; X.save(); X.globalAlpha*=alpha; X.strokeStyle=cor; X.lineWidth=lw;
  X.beginPath(); X.roundRect(cx-w/2,cy-h/2,w,h,r); X.stroke(); X.restore();
}

// ---------- componentes editoriais ----------
function fundo(tint=null, tintA=0){
  X.fillStyle=COR.bg; X.fillRect(0,0,W,H);
  const g=X.createRadialGradient(540,860,80,540,960,1250);
  g.addColorStop(0,"rgba(15,23,42,.95)"); g.addColorStop(1,"rgba(5,10,16,1)");
  X.fillStyle=g; X.fillRect(0,0,W,H);
  if(tint&&tintA>0){ X.save(); X.globalAlpha=tintA; const g2=X.createRadialGradient(540,900,0,540,900,1100);
    g2.addColorStop(0,tint); g2.addColorStop(1,"rgba(0,0,0,0)"); X.fillStyle=g2; X.fillRect(0,0,W,H); X.restore(); }
}
function grao(t){ // grão de filme fino, fixo por quadro
  const n=IMG.__grao; if(!n) return; X.save(); X.globalAlpha=0.06; X.globalCompositeOperation="overlay";
  const fr=Math.floor(t*30)%8; X.drawImage(n, (fr%4)*270, Math.floor(fr/4)*480, 270,480, 0,0,W,H); X.restore();
}
function vinheta(a=0.55){ const g=X.createRadialGradient(540,960,500,540,960,1200);
  g.addColorStop(0,"rgba(0,0,0,0)"); g.addColorStop(1,`rgba(0,0,0,${a})`); X.fillStyle=g; X.fillRect(0,0,W,H); }
// régua de secção: rótulo pequeno em maiúsculas com filete metálico
function rotulo(s,x,y,alpha=1,cor=COR.metal){
  txt(s,x,y,30,"DS",cor,"left",7,alpha);
  X.save(); X.globalAlpha*=alpha; X.fillStyle=cor; X.fillRect(x,y+18,64,3); X.restore();
}
// linha de fonte: obrigatória em todo o plano com número (≥ 28 px)
function linhaFonte(linhas,y,alpha=1,al="left",x=70){
  linhas.forEach((l,i)=>txt(l,al==="center"?540:x,y+i*40,28,"DM",COR.mute,al,0,alpha));
}
function fonteDe(d){ return [ (d.fonte==="stocks"?"Fonte: "+EP.fontes.stocks:"Fonte: "+EP.fontes.gold),
  "Em reais: "+CAMBIO.rotulo+" · estimativa, não oferta de compra" ]; }
function pctGrande(p,x,y,px,alpha=1,al="center",escala=1){
  const cor=p>0?COR.verde:COR.verm; X.save(); X.globalAlpha*=alpha; X.translate(x,y); X.scale(escala,escala);
  fonte(px,"D"); X.textAlign=al; X.fillStyle=cor; X.letterSpacing=(-px*0.04)+"px";
  X.shadowColor=cor; X.shadowBlur=px*0.18; X.fillText(pctS(p),0,0); X.restore();
}
function etiqueta(d,x,y,alpha=1,maxw=860){
  txt(d.nome,x,y,52,"DX",COR.ink,"left",0,alpha);
  const l2=`${d.ed} · nº ${d.n}`; const ls=quebra(l2,30,"DM",maxw);
  ls.forEach((l,i)=>txt(l,x,y+46+i*38,30,"DM",COR.mute,"left",0,alpha));
  txt("arte: "+d.arte,x,y+46+ls.length*38,30,"DM",COR.mute,"left",0,alpha);
  return y+46+(ls.length+1)*38;
}
function preco(d,x,y,alpha=1){
  const cor=d.pct>0?COR.verde:COR.verm;
  txt(usd(d.usd),x,y,60,"DX",COR.ink,"left",0,alpha);
  const w1=larg(usd(d.usd),60,"DX");
  txt("≈ "+brl(d.usd),x+w1+28,y,60,"DX",cor,"left",0,alpha);
}
function pilula(s,x,y,cor,alpha=1,px=40){
  const w=larg(s,px,"DX")+44; X.save(); X.globalAlpha*=alpha; X.fillStyle=cor; X.beginPath(); X.roundRect(x,y-px-6,w,px+26,12); X.fill(); X.restore();
  txt(s,x+22,y+4,px,"DX","#04110C","left",0,alpha); return w;
}
function tremor(t,t0,amp=10,dur=0.35){ const p=lin(t,t0,t0+dur); if(p<=0||p>=1) return [0,0];
  const a=amp*(1-p)*(1-p); return [ (hash(t*90)-.5)*2*a, (hash(t*77+3)-.5)*2*a ]; }
function flash(t,t0,cor="#ffffff",dur=0.12,max=0.7){ const p=lin(t,t0,t0+dur); if(p<=0||p>=1) return;
  X.save(); X.globalAlpha=max*(1-p); X.fillStyle=cor; X.fillRect(0,0,W,H); X.restore(); }

// ---------- cenas ----------
function paredeCartas(t,escala,alpha,desfoque=0,deriva=0){
  X.save(); X.globalAlpha=alpha; if(desfoque) X.filter=`blur(${desfoque}px)`;
  X.translate(540,960); X.rotate(-0.12); X.scale(escala,escala);
  const w=300,h=w*R,gx=26,gy=26, cols=4, rows=4;
  for(let c=0;c<cols;c++) for(let r=0;r<rows;r++){
    const k=EP.parede[(c*rows+r)%EP.parede.length];
    const dy=(c%2?1:-1)*deriva;
    const x=(c-(cols-1)/2)*(w+gx), y=(r-(rows-1)/2)*(h+gy)+dy+(c%2?h*0.32:0);
    carta(k,x,y,w,0,1,0.5);
  }
  X.restore();
}

function cenaAbertura(t){ // 0 – 1.56
  fundo();
  const pull = mix(1.16,1.0,eOut(lin(t,0,1.56)));
  const dim = 1-0.62*lin(t,1.02,1.30);
  paredeCartas(t,pull,dim, t>1.02?6*lin(t,1.02,1.25):0, 40*t);
  vinheta(0.65);
  // rótulo editorial (não é logótipo): aparece depois do primeiro quadro
  const a=lin(t,0.18,0.45)*(1-lin(t,1.0,1.15));
  X.save(); X.globalAlpha=a*0.85; X.fillStyle="rgba(5,10,16,.82)"; X.fillRect(0,230,W,150); X.restore();
  rotulo("PREGÃO MAGIC",70,290,a);
  txt("Sexta, "+EP.data+" · semana do Star Trek",70,350,34,"DM",COR.ink,"left",0,a);
  // uma carta atravessa a composição
  if(t>=1.02){
    const p=eExp(lin(t,1.02,1.56));
    const x=mix(-420,540,p), rot=mix(-0.42,0,p), w=mix(640,520,p);
    const v = (1-p)*260;
    carta("urza",x,960,w,rot,1,1, v>8?[v,0]:null);
  }
}

function cenaMatch(t){ // 1.56 – 3.16 : moldura -> estrutura de mercado
  fundo();
  const w0=520, cx=540, cy=960;
  const pa=lin(t,1.56,1.80); // carta some, fica a moldura
  if(pa<1) carta("urza",cx,cy,w0,0,1-eIn(pa),1);
  // moldura cresce até virar a área do gráfico
  const pg=eIO(lin(t,1.76,2.40));
  const x0=mix(cx-w0/2,110,pg), x1=mix(cx+w0/2,970,pg), y0=mix(cy-w0*R/2,470,pg), y1=mix(cy+w0*R/2,1380,pg);
  X.save(); X.strokeStyle=COR.ink; X.globalAlpha=0.9; X.lineWidth=mix(5,3,pg);
  X.beginPath(); X.roundRect(x0,y0,x1-x0,y1-y0,mix(w0*0.045,0,pg)); X.stroke(); X.restore();
  // escala com zero na base (proporção verdadeira): 0 -> y1, US$16 -> y0
  const ys = v=>1380-(v/16)*(1380-470);
  const pgr=lin(t,2.09,2.62);
  for(let i=1;i<4;i++){ const v=i*4, yy=ys(v), ww=(970-110)*eOut(pgr);
    X.save(); X.globalAlpha=0.35*pgr; X.fillStyle=COR.linha; X.fillRect(110,yy,ww,2); X.restore();
    txt("US$ "+v,122,yy-12,26,"DM",COR.mute,"left",0,pgr); }
  // segmento real: há 7 dias (calculado: 14,70 / 2,04) -> 13/11
  const A=[190,ys(14.70/2.04)], B=[890,ys(14.70)];
  const pl=eOut(lin(t,2.35,3.10));
  if(pl>0){ X.save(); X.strokeStyle=COR.verde; X.lineWidth=10; X.lineCap="round"; X.shadowColor=COR.verde; X.shadowBlur=30;
    X.beginPath(); X.moveTo(A[0],A[1]); X.lineTo(mix(A[0],B[0],pl),mix(A[1],B[1],pl)); X.stroke(); X.restore();
    X.save(); X.fillStyle=COR.ink; X.beginPath(); X.arc(A[0],A[1],13,0,7); X.fill(); X.restore();
    txt("há 7 dias",A[0]-10,A[1]+62,30,"DS",COR.mute,"left",0,pl);
    txt("≈ US$ 7,21 (calculado)",A[0]-10,A[1]+100,28,"DM",COR.mute,"left",0,pl);
  }
  if(pl>=0.98){ X.save(); X.fillStyle=COR.verde; X.beginPath(); X.arc(B[0],B[1],16,0,7); X.fill(); X.restore();
    txt("US$ 14,70",B[0],B[1]-36,40,"DX",COR.ink,"right"); }
  rotulo("ALTA DA SEMANA",70,300,lin(t,1.9,2.2));
  txt("Urza, Chief Artificer",70,370,44,"DX",COR.ink,"left",0,lin(t,2.0,2.3));
  linhaFonte(["Fonte: "+EP.fontes.stocks],1460,lin(t,2.3,2.6));
}

function cenaNumero(t){ // 3.16 – 4.67 : impacto +104% -> número vira a moldura da carta
  fundo(COR.verde,0.25*(1-lin(t,3.16,3.9)));
  const [sx,sy]=tremor(t,3.16,16,0.4);
  X.save(); X.translate(sx,sy);
  const zin=lin(t,4.13,4.55);
  const esc = mix(1.22,1.0,eBack(lin(t,3.16,3.40))) * (1+eIn(zin)*14);
  // ancora o zoom no "0" de +104%
  pctGrande(104,540+ eIn(zin)*540,1020+eIn(zin)*40,280,1-lin(t,4.40,4.55),"center",esc);
  const a=lin(t,3.30,3.50)*(1-lin(t,4.10,4.25));
  rotulo("ALTA DA SEMANA",70,300,a);
  txt("em 7 dias",540,1150,64,"DX",COR.ink,"center",0,a);
  txt("Urza, Chief Artificer",540,1235,44,"DS",COR.mute,"center",0,a);
  linhaFonte(["Fonte: "+EP.fontes.stocks],1460,a,"center");
  X.restore();
  flash(t,3.16,"#d1fae5",0.10,0.55);
  // revelação: a carta nasce do zoom, em grande escala
  const pr=lin(t,4.38,4.67);
  if(pr>0){ const w=mix(900,600,eOut(pr)); carta("urza",540,240+600*R/2,w,0,cl(pr*2.5),1); }
}

function cenaUrza(t){ // 4.67 – 7.00 : carta protagonista + identificação
  fundo(COR.verde,0.10);
  const push=mix(1,1.035,lin(t,4.67,7.0));
  const w=600*push; carta("urza",540,240+600*R/2,w,0,1,1);
  const a=lin(t,4.80,5.05);
  const y=etiqueta(EP.urza,70,1180,a);
  txt(pctS(104),930,1180,56,"D",COR.verde,"right",0,lin(t,4.95,5.15));
  const b=lin(t,5.15,5.4);
  preco(EP.urza,70,y+62,b);
  linhaFonte(fonteDe(EP.urza),1440,lin(t,5.3,5.6));
}

function cenaCausa(t){ // 7.00 – 11.54 : porquê, segundo a fonte
  fundo();
  // mudança de escala: a carta encolhe para a coluna da esquerda
  const p=eExp(lin(t,7.0,7.45));
  const w=mix(600,330,p), cx=mix(540,235,p), cy=mix(240+600*R/2,700,p);
  carta("urza",cx,cy,w,0,1,1);
  const a=lin(t,7.2,7.45);
  rotulo("POR QUÊ?",440,400,a);
  txt("Segundo o",440,500,46,"DM",COR.mute,"left",0,a);
  txt("MTGStocks:",440,556,46,"DM",COR.mute,"left",0,a);
  // tipografia cinética: frase entra por blocos, no tempo da música
  const blocos=[["Guias de",7.55],["upgrade",7.78],["do deck",8.04],["dos Borg,",8.31],["do Star Trek,",8.58],["apontaram",9.11],["o Urza.",9.38]];
  let yy=680;
  blocos.forEach(([s,t0],i)=>{ const q=eOut(lin(t,t0,t0+0.22)); if(q<=0) return;
    const cor = s.includes("Borg")||s.includes("Star Trek")? COR.verde2 : COR.ink;
    txt(s,440+(1-q)*40,yy+i*78,66,"DX",cor,"left",0,q); });
  // linha de base: preço continua visível no plano
  const b=lin(t,7.4,7.7);
  txt(usd(14.70),70,1290,48,"DX",COR.ink,"left",0,b);
  txt("≈ "+brl(14.70)+"  ·  +104%",70+larg(usd(14.70),48,"DX")+22,1290,48,"DX",COR.verde,"left",0,b);
  linhaFonte(fonteDe(EP.urza),1420,b);
  // saída: tudo recua para o escuro antes da próxima alta
  const s=lin(t,11.0,11.54); if(s>0){ X.save(); X.globalAlpha=eIn(s)*0.92; X.fillStyle=COR.bg; X.fillRect(0,0,W,H); X.restore(); }
}

function cenaTensao(t){ // 11.54 – 13.72 : contagem antes do drop
  fundo();
  const p=lin(t,11.54,13.72);
  // a próxima carta aproxima-se escondida: só a silhueta iluminada pela borda
  X.save(); X.globalAlpha=0.9; X.filter="blur(22px) brightness(0.25)";
  carta("uchuulon",540,980,mix(380,560,eIn(p)),0,1,0); X.restore();
  // varrimento de luz metálica
  const sx=mix(-300,1380,(t-11.54)%1.07/1.07);
  X.save(); X.globalCompositeOperation="lighter"; const g=X.createLinearGradient(sx-120,0,sx+120,0);
  g.addColorStop(0,"rgba(185,162,122,0)"); g.addColorStop(.5,"rgba(185,162,122,.10)"); g.addColorStop(1,"rgba(185,162,122,0)");
  X.fillStyle=g; X.fillRect(0,0,W,H); X.restore();
  rotulo("PRÓXIMA ALTA",70,300,lin(t,11.6,11.8));
  // dígitos a rodar como num painel mecânico, cada vez mais devagar
  // sem números falsos: o valor só aparece no drop. Pausado, o quadro diz "?"
  const pulso = 0.35+0.25*Math.max(0,Math.sin((t-11.54)/0.534*Math.PI));
  txt("+ ? ? %",540,1030,230,"D",COR.ink,"center",0,(0.3+0.5*p)*pulso/0.6);
  txt("Commander Legends: Battle for Baldur's Gate",540,1180,34,"DM",COR.mute,"center",0,lin(t,12.6,12.9));
}

function cenaUchuDrop(t){ // 13.72 – 16.25
  fundo(COR.verde,0.22*(1-lin(t,13.72,14.6))+0.08);
  const [sx,sy]=tremor(t,13.72,18,0.45); X.save(); X.translate(sx,sy);
  const p=eBack(lin(t,13.72,13.98));
  const w=560*mix(1.45,1,p);
  carta("uchuulon",540,560+560*R/2,w,0,cl(lin(t,13.72,13.78)*1.6+0.2),1);
  pctGrande(48,540,500,210,1,"center",mix(1.3,1,eOut(lin(t,13.72,13.95))));
  X.restore();
  flash(t,13.72,"#ecfdf5",0.12,0.75);
  txt("em 7 dias",540,1440,44,"DX",COR.ink,"center",0,lin(t,14.0,14.25));
  linhaFonte(["Fonte: "+EP.fontes.stocks],1500,lin(t,14.1,14.4),"center");
}

function cenaUchuInfo(t){ // 16.25 – 18.81 : push-in + painel
  fundo(COR.verde,0.08);
  const p=eOut(lin(t,16.25,16.6));
  const w=mix(560,420,p), cy=mix(560+560*R/2,240+420*R/2,p), cx=mix(540,290,p);
  carta("uchuulon",cx,cy,w,0,1,1);
  const a=lin(t,16.45,16.7);
  pctGrande(48,980,420,150,a,"right");
  txt("em 7 dias",980,490,34,"DS",COR.ink,"right",0,a);
  const y=etiqueta(EP.uchu,70,900,a,860);
  preco(EP.uchu,70,y+62,lin(t,16.6,16.85));
  const b=lin(t,16.9,17.15);
  txt("Por quê, segundo o MTGStocks:",70,y+150,32,"DS",COR.metal,"left",0,b);
  const frase=quebra("Dois comandantes do Mystery Booster: Commander Edition pedem ele no deck.",44,"DB",860);
  frase.forEach((l,i)=>txt(l,70,y+206+i*56,44,"DB",COR.ink,"left",0,lin(t,17.0+i*0.12,17.25+i*0.12)));
  linhaFonte(fonteDe(EP.uchu),1450,lin(t,16.7,17.0));
}

function cenaVirada(t){ // 18.81 – 20.63 : seta verde gira e vira vermelha (forma e cor)
  const p=eIO(lin(t,19.34,20.30));
  const corA=[16,185,129], corB=[239,68,68];
  const c=corA.map((v,i)=>Math.round(mix(v,corB[i],p)));
  fundo(`rgb(${c})`,0.18);
  X.save(); X.translate(540,900); X.rotate(Math.PI*p);
  const s=mix(0.6,1,eOut(lin(t,18.81,19.2))); X.scale(s,s);
  X.fillStyle=`rgb(${c})`; X.shadowColor=`rgb(${c})`; X.shadowBlur=60;
  X.beginPath(); X.moveTo(0,-330); X.lineTo(250,-60); X.lineTo(90,-60); X.lineTo(90,300); X.lineTo(-90,300); X.lineTo(-90,-60); X.lineTo(-250,-60); X.closePath(); X.fill();
  X.restore();
  const a=lin(t,18.95,19.2);
  txt("DO OUTRO LADO",540,1390,72,"D",COR.ink,"center",2,a);
  txt("DO PREGÃO",540,1470,72,"D",COR.ink,"center",2,a);
  // a seta acelera para baixo e arrasta o quadro: entrada da queda
  const d=eIn(lin(t,20.30,20.63)); if(d>0){ X.save(); X.fillStyle=COR.bg; X.fillRect(0,0,W,H*d); X.restore(); }
}

function cenaPicard(t){ // 20.63 – 23.10 : queda vertical
  fundo(COR.verm,0.22*(1-lin(t,20.63,21.5))+0.07);
  const [sx,sy]=tremor(t,20.86,14,0.35); X.save(); X.translate(sx,sy);
  const p=lin(t,20.63,20.86); const yq=mix(-180,560+560*R/2,eIn(p));
  const v = p<1? 300*(p):0;
  carta("picard",540,yq,560,0,1,1, v>10?[0,v]:null);
  pctGrande(-46,540,500,210,lin(t,20.86,20.95),"center",mix(1.3,1,eOut(lin(t,20.86,21.1))));
  X.restore();
  flash(t,20.86,"#fee2e2",0.12,0.6);
  txt("em 7 dias",540,1440,44,"DX",COR.ink,"center",0,lin(t,21.1,21.3));
  linhaFonte(["Fonte: "+EP.fontes.gold],1500,lin(t,21.2,21.45),"center");
}

function cenaPicardInfo(t){ // 23.10 – 26.55
  fundo(COR.verm,0.07);
  const p=eOut(lin(t,23.10,23.45));
  const w=mix(560,420,p), cy=mix(560+560*R/2,240+420*R/2,p), cx=mix(540,790,p);
  carta("picard",cx,cy,w,0,1,1);
  const a=lin(t,23.3,23.55);
  pctGrande(-46,70,420,150,a,"left");
  txt("em 7 dias",70,490,34,"DS",COR.ink,"left",0,a);
  const y=etiqueta(EP.picard,70,900,a);
  preco(EP.picard,70,y+62,lin(t,23.45,23.7));
  const b=lin(t,23.8,24.05);
  txt("Contexto:",70,y+150,32,"DS",COR.metal,"left",0,b);
  ["Star Trek chegou às lojas","em 13/11. O número é da","semana do lançamento."].forEach((l,i)=>
    txt(l,70,y+206+i*56,44,"DB",COR.ink,"left",0,lin(t,23.9+i*0.12,24.15+i*0.12)));
  linhaFonte(fonteDe(EP.picard),1450,lin(t,23.6,23.9));
}

function cenaPausa(t){ // 26.55 – 27.49 : silêncio da música = quadro congelado e esvaziado
  cenaPicardInfo(26.54);
  const p=eOut(lin(t,26.55,26.75));
  X.save(); X.globalAlpha=0.94*p; X.fillStyle=COR.bg; X.fillRect(0,0,W,H); X.restore();
  // mira fina: o radar acende em silêncio
  const q=lin(t,26.70,27.35);
  X.save(); X.strokeStyle=COR.metal; X.globalAlpha=0.9*q; X.lineWidth=2;
  X.beginPath(); X.arc(540,900,mix(40,300,eOut(q)),0,Math.PI*2); X.stroke();
  X.fillStyle=COR.metal; X.fillRect(540-mix(0,420,eOut(q)),899,mix(0,840,eOut(q)),2); X.fillRect(539,900-mix(0,420,eOut(q)),2,mix(0,840,eOut(q)));
  X.restore();
  txt("RADAR",540,1460,88,"D",COR.ink,"center",24,lin(t,26.8,27.0));
}

function cenaSplit(t){ // 27.49 – 30.07 : mesma coleção, dois sentidos
  fundo();
  const [sx,sy]=tremor(t,27.49,16,0.4); X.save(); X.translate(sx,sy);
  const p=eExp(lin(t,27.49,27.80));
  const w=400, yL=mix(2400,560+w*R/2,p), yR=mix(-500,560+w*R/2,p);
  X.save(); X.globalAlpha=0.13; X.fillStyle=COR.verm; X.fillRect(0,0,540,H); X.fillStyle=COR.verde; X.fillRect(540,0,540,H); X.restore();
  carta("overgrown",270,yL,w,0,1,1, p<0.9?[0,-180*(1-p)]:null);
  carta("watery",810,yR,w,0,1,1, p<0.9?[0,180*(1-p)]:null);
  X.save(); X.fillStyle=COR.metal; X.fillRect(538,500,4,mix(0,700,p)); X.restore();
  pctGrande(-50,270,500,140,lin(t,27.6,27.7),"center");
  pctGrande(44,810,500,140,lin(t,27.7,27.8),"center");
  X.restore();
  flash(t,27.49,"#ffffff",0.10,0.6);
  const a=lin(t,27.75,28.0);
  txt("MESMA COLEÇÃO.",540,300,58,"D",COR.ink,"center",1,a);
  txt("DOIS SENTIDOS.",540,370,58,"D",COR.metal,"center",1,a);
  txt("Overgrown Tomb",270,1180,36,"DX",COR.ink,"center",0,a);
  txt("Watery Grave",810,1180,36,"DX",COR.ink,"center",0,a);
  txt("Star Trek · em 7 dias",540,1250,32,"DM",COR.mute,"center",0,a);
  linhaFonte(["Fonte: "+EP.fontes.gold],1460,lin(t,28.0,28.3),"center");
}

function cenaShocks(t){ // 30.07 – 31.67 : as 10 shocklands em leque (paralaxe)
  fundo();
  const p=eOut(lin(t,30.07,30.6));
  EP.shocks.forEach((k,i)=>{
    const f=(i-4.5)/4.5; const ang=f*0.62*p; const w=190;
    const cx=540+Math.sin(ang)*620 + (t-30.07)*14*(i%2?1:-1);
    const cy=1440-Math.cos(ang)*620 + (1-p)*500;
    carta(k,cx,cy,w,ang,1,0.6);
  });
  const a=lin(t,30.25,30.5);
  rotulo("NO RADAR",70,300,a);
  txt("Shocklands do Star Trek",70,385,62,"DX",COR.ink,"left",0,a);
  X.save(); X.globalAlpha=a*0.9; X.fillStyle="rgba(5,10,16,.85)"; X.fillRect(40,1240,1000,250); X.restore();
  txt("“A impressão mais barata",70,1320,48,"DB",COR.ink,"left",0,lin(t,30.45,30.7));
  txt("das shocklands.”",70,1380,48,"DB",COR.ink,"left",0,lin(t,30.55,30.8));
  linhaFonte(["MTGStocks, Weekly Winners 2026-46, 13/11/2026 (tradução)"],1450,lin(t,30.6,30.9));
}

function linhaTabela(d,y,a,mostraFonte=false){
  carta(d.k,130,y,120,0,a,0.4);
  txt(d.nome,220,y-40,42,"DX",COR.ink,"left",0,a);
  txt(`${d.ed} · nº ${d.n}`,220,y+2,28,"DM",COR.mute,"left",0,a);
  txt(usd(d.usd)+"  ≈ "+brl(d.usd),220,y+52,38,"DB",COR.ink,"left",0,a);
  txt(pctS(d.pct),930,y+10,62,"D",d.pct>0?COR.verde:COR.verm,"right",0,a);
}
function cenaPrecosRadar(t){ // 31.67 – 34.35
  fundo();
  const a1=eOut(lin(t,31.67,31.9)), a2=eOut(lin(t,31.85,32.08));
  rotulo("NO RADAR · PREÇOS",70,300,a1);
  X.save(); X.translate((1-a1)*-60,0); linhaTabela(EP.ogt,620,a1); X.restore();
  X.save(); X.translate((1-a2)*60,0); linhaTabela(EP.wg,1010,a2); X.restore();
  X.save(); X.globalAlpha=0.5*a2; X.fillStyle=COR.linha; X.fillRect(70,815,850,2); X.restore();
  txt("variação em 7 dias",930,430,28,"DM",COR.mute,"right",0,a1);
  linhaFonte(["Fonte: "+EP.fontes.gold,"Em reais: "+CAMBIO.rotulo+" · estimativa, não oferta de compra"],1330,lin(t,32.0,32.3));
}

function cenaFecho(t){ // 34.35 – 37.77 : painel de fecho, uma linha por acento
  fundo();
  rotulo("FECHAMENTO · "+EP.data,70,300,lin(t,34.35,34.5));
  const linhas=[[EP.urza,34.348],[EP.uchu,34.90],[EP.wg,35.43],[EP.picard,36.055],[EP.ogt,36.60]];
  linhas.forEach(([d,t0],i)=>{ const q=eExp(lin(t,t0,t0+0.25)); if(q<=0) return; const y=440+i*190;
    X.save(); X.globalAlpha=q; X.fillStyle= i%2? "rgba(15,23,42,.6)":"rgba(15,23,42,.9)"; X.fillRect(40,y-80,1000,170); X.restore();
    X.save(); X.translate((1-q)*120,0);
    carta(d.k,120,y+5,104,0,q,0.3);
    txt(d.nome,200,y-14,40,"DX",COR.ink,"left",0,q);
    txt(usd(d.usd)+" ≈ "+brl(d.usd),200,y+40,32,"DM",COR.mute,"left",0,q);
    txt(pctS(d.pct),920,y+22,64,"D",d.pct>0?COR.verde:COR.verm,"right",0,q);
    X.restore(); });
  linhaFonte(["Fontes: MTGStocks e MTGGoldfish, 13/11/2026","Em reais: "+CAMBIO.rotulo,"Não é recomendação de compra ou venda."],1410,lin(t,34.6,34.9));
}

function cenaPasta(t){ // 37.77 – 41.20 : ponte para o BINDER Vision
  fundo();
  paredeCartas(t, mix(0.92,1.0,lin(t,37.77,41.2)), 0.30, 7, 30*(t-37.77));
  vinheta(0.8);
  const [sx,sy]=tremor(t,37.773,10,0.3); X.save(); X.translate(sx,sy);
  const a=eBack(lin(t,37.77,37.98));
  X.save(); X.translate(540,820); X.scale(mix(1.25,1,a),mix(1.25,1,a));
  txt("E A SUA",0,-60,118,"D",COR.ink,"center",-2,cl(a)); txt("PASTA?",0,70,150,"D",COR.verde,"center",-3,cl(a)); X.restore();
  X.restore();
  const b=lin(t,39.49,39.75);
  X.save(); X.globalAlpha=b*0.9; X.fillStyle="rgba(5,10,16,.88)"; X.fillRect(40,1060,1000,360); X.restore();
  txt("Agora você sabe como o mercado",540,1140,44,"DB",COR.ink,"center",0,b);
  txt("se mexeu. Veja o valor de referência",540,1198,44,"DB",COR.ink,"center",0,b);
  txt("da sua coleção no BINDER Vision.",540,1256,44,"DB",COR.ink,"center",0,b);
  txt("Escaneie suas cartas · link na bio",540,1350,34,"DS",COR.verde2,"center",0,lin(t,39.7,39.95));
  // saída para o fecho oficial: corte seco no último acento
}

const CENAS=[[0,1.56,cenaAbertura],[1.56,3.16,cenaMatch],[3.16,4.67,cenaNumero],[4.67,7.007,cenaUrza],
  [7.007,11.54,cenaCausa],[11.54,13.72,cenaTensao],[13.72,16.25,cenaUchuDrop],[16.25,18.81,cenaUchuInfo],
  [18.81,20.631,cenaVirada],[20.631,23.10,cenaPicard],[23.10,26.55,cenaPicardInfo],[26.55,27.487,cenaPausa],
  [27.487,30.07,cenaSplit],[30.07,31.67,cenaShocks],[31.67,34.348,cenaPrecosRadar],[34.348,37.773,cenaFecho],
  [37.773,41.30,cenaPasta]];

function cenaCapa(){
  fundo(COR.verde,0.12);
  paredeCartas(0,1.05,0.28,8,0); vinheta(0.85);
  carta("urza",540,1065,520,-0.05,1,1.2);
  rotulo("PREGÃO MAGIC",70,300,1);
  txt("Fechamento da semana · "+EP.data,70,360,36,"DM",COR.ink);
  pctGrande(104,540,600,190,1,"center");
  X.save(); X.globalAlpha=0.92; X.fillStyle="rgba(5,10,16,.9)"; X.fillRect(40,1440,1000,140); X.restore();
  txt("Altas, quedas e radar do Magic",540,1500,46,"DX",COR.ink,"center");
  txt("Urza +104% · Picard −46% · shocklands do Star Trek",540,1556,32,"DM",COR.mute,"center");
}
window.render = function(t){
  if(t<0){ X.setTransform(1,0,0,1,0,0); X.globalAlpha=1; X.filter="none"; cenaCapa(); return true; }
  X.setTransform(1,0,0,1,0,0); X.globalAlpha=1; X.filter="none"; X.globalCompositeOperation="source-over";
  for(const [a,b,fn] of CENAS){ if(t>=a&&t<b){ fn(t); break; } }
  grao(t);
  return true;
};

// ---------- carregamento ----------
(async function(){
  const ks=new Set([...EP.parede,...EP.shocks,"urza","uchuulon","picard","overgrown","watery"]);
  await Promise.all([...ks].map(k=>new Promise(r=>{ const im=new Image(); im.onload=()=>{IMG[k]=im;r()}; im.onerror=()=>r(); im.src=EP.cartas+k+".png"; })));
  // textura de grão determinística
  const g=document.createElement("canvas"); g.width=1080; g.height=960; const gx=g.getContext("2d"); const id=gx.createImageData(1080,960);
  for(let i=0;i<id.data.length;i+=4){ const v=Math.floor(hash(i*0.37)*255); id.data[i]=id.data[i+1]=id.data[i+2]=v; id.data[i+3]=255; }
  gx.putImageData(id,0,0); IMG.__grao=g;
  await document.fonts.load("900 100px D"); await document.fonts.load("800 100px DX"); await document.fonts.load("700 100px DB");
  await document.fonts.load("600 100px DS"); await document.fonts.load("500 100px DM");
  PRONTO=true; window.PRONTO=true;
})();
