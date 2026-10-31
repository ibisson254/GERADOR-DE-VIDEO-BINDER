// Pintura generativa no espírito das referências (abstração geométrica com aquarela, à Kandinsky).
// Composição original a cada semente: não copia nenhuma obra.
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}

function paint(cv, seed, pal, opts, t=0){
  const PI2=Math.PI*2; let pk=0;
  const mv=a=>{const k=(pk++*0.2357)%1;return [a*Math.sin(PI2*(t+k)), a*Math.cos(PI2*(t+k*1.37))]};
  const pulse=a=>{const k=(pk++*0.311)%1;return 1+a*Math.sin(PI2*(t+k))};
  const W=1080,H=1350,D=2; cv.width=W*D; cv.height=H*D;
  const g=cv.getContext('2d'); g.scale(D,D);
  const R=mulberry32(seed), rr=(a,b)=>a+R()*(b-a), pick=a=>a[Math.floor(R()*a.length)];
  const ink='#171512';
  const hex2=(h,a)=>{const n=parseInt(h.slice(1),16);return `rgba(${n>>16&255},${n>>8&255},${n&255},${a})`};
  const shade=(h,f)=>{const n=parseInt(h.slice(1),16);const c=[n>>16&255,n>>8&255,n&255].map(v=>Math.max(0,Math.min(255,Math.round(v*f))));return `rgb(${c})`};
  const cx=opts.cx, cy=opts.cy;   // centro da carta

  // ---- cartaz (papel) e quadro pintado com sombra
  const X=opts.px,Y=opts.py,PW=opts.pw,PH=opts.ph;
  g.fillStyle='#F2EBDA'; g.fillRect(0,0,W,H);
  g.globalCompositeOperation='multiply';
  for(let i=0;i<14;i++){const x=rr(0,W),y=rr(0,H),r=rr(120,420);const gr=g.createRadialGradient(x,y,0,x,y,r);
    gr.addColorStop(0,`rgba(180,150,105,${rr(.03,.07)})`);gr.addColorStop(1,'rgba(180,150,105,0)');g.fillStyle=gr;g.fillRect(0,0,W,H);}
  g.globalCompositeOperation='source-over';
  g.save();g.shadowColor='rgba(50,32,12,.45)';g.shadowBlur=38;g.shadowOffsetX=10;g.shadowOffsetY=22;g.fillStyle='#F4ECD8';g.fillRect(X,Y,PW,PH);g.restore();
  g.save();g.shadowColor='rgba(50,32,12,.5)';g.shadowBlur=4;g.shadowOffsetY=2;g.fillStyle='#F4ECD8';g.fillRect(X,Y,PW,PH);g.restore();
  g.save();g.beginPath();g.rect(X,Y,PW,PH);g.clip();
  g.globalCompositeOperation='multiply';
  for(let i=0;i<22;i++){const x=rr(X,X+PW),y=rr(Y,Y+PH),r=rr(140,480);const gr=g.createRadialGradient(x,y,0,x,y,r);
    gr.addColorStop(0,`rgba(${rr(150,190)|0},${rr(115,145)|0},${rr(70,95)|0},${rr(.02,.05)})`);gr.addColorStop(1,'rgba(180,140,90,0)');g.fillStyle=gr;g.fillRect(X,Y,PW,PH);}
  // ---- helpers de pincel
  function blobPath(x,y,r,amp,ph,k){g.beginPath();for(let i=0;i<=72;i++){const a=i/72*Math.PI*2;
    const d=r*(1+amp*(Math.sin(a*3+ph[0])*.5+Math.sin(a*5+ph[1])*.3+Math.sin(a*9+ph[2])*.2)+ (k?rr(-.012,.012):0));
    const px=x+Math.cos(a)*d, py=y+Math.sin(a)*d; i?g.lineTo(px,py):g.moveTo(px,py);} g.closePath();}
  function wash(x,y,r,col,a=1){const [dx,dy]=mv(14);x+=dx;y+=dy;r*=pulse(.03);g.save();g.globalCompositeOperation='multiply';const ph=[rr(0,6),rr(0,6),rr(0,6)];
    for(let l=0;l<26;l++){g.fillStyle=hex2(col,.055*a);blobPath(x+rr(-6,6),y+rr(-6,6),r*rr(.86,1.04),.07,ph,1);g.fill();}
    g.strokeStyle=hex2(col,.30*a);g.lineWidth=2.2;blobPath(x,y,r,.07,ph,0);g.stroke();
    for(let i=0;i<r*1.4;i++){const a2=rr(0,6.28),d=Math.sqrt(R())*r*.95;g.fillStyle=hex2(col,rr(.05,.16)*a);g.beginPath();g.arc(x+Math.cos(a2)*d,y+Math.sin(a2)*d,rr(.6,2.4),0,7);g.fill();}
    g.restore();}
  function disc(x,y,r,col,depth=1){if(opts.skip)return;const [dx,dy]=mv(18);x+=dx;y+=dy; // disco chapado com volume e sombra projetada
    g.save();g.shadowColor='rgba(55,35,15,.32)';g.shadowBlur=26*depth;g.shadowOffsetX=7*depth;g.shadowOffsetY=11*depth;
    const ph=[rr(0,6),rr(0,6),rr(0,6)];g.fillStyle=col;blobPath(x,y,r,.012,ph,0);g.fill();g.restore();
    g.save();blobPath(x,y,r,.012,ph,0);g.clip();
    const gr=g.createRadialGradient(x-r*.35,y-r*.4,r*.1,x,y,r*1.15);gr.addColorStop(0,'rgba(255,248,230,.20)');gr.addColorStop(.55,'rgba(255,248,230,0)');gr.addColorStop(1,'rgba(40,20,5,.28)');
    g.fillStyle=gr;g.fillRect(x-r,y-r,2*r,2*r);
    g.globalCompositeOperation='multiply';for(let s=0;s<14;s++){g.strokeStyle=hex2('#6b4a2a',rr(.03,.07));g.lineWidth=rr(6,18);g.beginPath();const yy=y-r+rr(0,2*r);g.moveTo(x-r,yy);g.bezierCurveTo(x-r/2,yy+rr(-20,20),x+r/2,yy+rr(-20,20),x+r,yy+rr(-10,10));g.stroke();}
    g.restore();}
  function rings(x,y,r,cols){if(opts.skip)return;const [dx,dy]=mv(10);x+=dx;y+=dy;r*=pulse(.06);for(let i=0;i<cols.length;i++){g.save();g.globalAlpha=.88;g.strokeStyle=cols[i];g.lineWidth=r/(cols.length*1.9);g.beginPath();g.arc(x,y,r*(1-i/cols.length),0,7);g.stroke();g.restore();}}
  function plane(pts,col,a=.55){const [dx,dy]=mv(9);pts=pts.map(p=>[p[0]+dx,p[1]+dy]);g.save();g.globalCompositeOperation='multiply';g.shadowColor='rgba(55,35,15,.22)';g.shadowBlur=18;g.shadowOffsetX=5;g.shadowOffsetY=8;
    g.fillStyle=hex2(col,a);g.beginPath();pts.forEach((p,i)=>i?g.lineTo(p[0]+rr(-2,2),p[1]+rr(-2,2)):g.moveTo(p[0],p[1]));g.closePath();g.fill();g.restore();}
  function line(x1,y1,x2,y2,w){const n=Math.max(8,Math.hypot(x2-x1,y2-y1)/14);g.save();g.lineCap='round';
    for(let pass=0;pass<2;pass++){g.strokeStyle=pass?'rgba(23,21,18,.9)':'rgba(23,21,18,.18)';let px=x1,py=y1;
      for(let i=1;i<=n;i++){const t=i/n,x=x1+(x2-x1)*t+rr(-.8,.8),y=y1+(y2-y1)*t+rr(-.8,.8);g.lineWidth=pass?w*rr(.75,1.15):w*2.2;g.beginPath();g.moveTo(px,py);g.lineTo(x,y);g.stroke();px=x;py=y;}}
    g.restore();}
  function arc(x,y,r,a0,a1,w,col=ink){if(opts.skip)return;const s0=.18*Math.sin(PI2*(t+(pk++*0.19)%1));a0+=s0;a1+=s0;g.save();g.strokeStyle=col;g.lineWidth=w;g.lineCap='round';g.beginPath();g.arc(x,y,r,a0,a1);g.stroke();g.restore();}
  function checker(x,y,c,rw,s,cols){g.save();g.shadowColor='rgba(55,35,15,.25)';g.shadowBlur=10;g.shadowOffsetY=4;
    for(let i=0;i<c;i++)for(let j=0;j<rw;j++){g.fillStyle=(i+j)%2?pick(cols):'#F3EAD5';g.fillRect(x+i*s,y+j*s,s,s);}g.restore();
    g.strokeStyle=ink;g.lineWidth=1.5;g.strokeRect(x,y,c*s,rw*s);}
  function splat(x,y,spread,n,col){g.save();for(let i=0;i<n;i++){const a=rr(0,6.28),d=Math.pow(R(),1.8)*spread;g.fillStyle=hex2(col,rr(.55,.95));g.beginPath();g.arc(x+Math.cos(a)*d,y+Math.sin(a)*d,rr(.8,6)*(1-d/spread*.6),0,7);g.fill();}g.restore();}
  function dot(x,y,r,col,still){if(!still){const [dx,dy]=mv(9);x+=dx;y+=dy;}g.save();g.shadowColor='rgba(55,35,15,.3)';g.shadowBlur=8;g.shadowOffsetY=3;g.fillStyle=col;g.beginPath();g.arc(x,y,r,0,7);g.fill();g.restore();}
  function stem(x,y1,y2,r,col){const [,dy]=mv(14);line(x,y1+dy,x,y2,2);dot(x,y1+dy,r,col,1);}

  const side=R()<.5?-1:1, L=X, T=Y, Rt=X+PW, B=Y+PH;
  // camada 1: lavagens que cobrem a tela inteira
  wash(L+rr(80,220),T+rr(80,220),rr(260,340),pal[3],.4);
  wash(Rt-rr(80,220),B-rr(80,200),rr(280,360),pal[1],.4);
  wash(cx+side*rr(200,280),cy-rr(120,220),rr(300,360),pal[0],1);
  wash(cx-side*rr(220,300),cy+rr(100,220),rr(220,280),pal[1],.9);
  wash(Rt-rr(60,160),T+rr(60,180),rr(150,210),pal[4],.6);
  wash(L+rr(60,160),B-rr(60,180),rr(150,220),pal[2],.45);
  // camada 2: planos translúcidos
  const bx=cx-side*rr(270,340);
  plane([[bx-60,T+rr(20,80)],[bx+70,T+rr(20,80)],[bx+70,B-rr(40,140)],[bx-60,B-rr(40,140)]],pal[2],.6);
  const tx=cx+side*rr(220,320);
  plane([[tx,T+rr(60,140)],[tx+side*rr(160,230),B-rr(120,260)],[tx-side*rr(60,120),B-rr(60,200)]],pal[3],.42);
  plane([[L,B-rr(160,240)],[L+rr(260,360),B],[L,B]],pal[4],.35);
  // camada 3: discos com volume
  disc(cx+side*rr(270,330),cy-rr(150,230),rr(150,190),pal[0],1.1);
  disc(cx-side*rr(300,360),cy+rr(160,260),rr(90,125),pal[1],.95);
  disc(side>0?L+rr(70,140):Rt-rr(70,140),T+rr(60,140),rr(36,60),pal[4],.8);
  disc(side>0?Rt-rr(60,120):L+rr(60,120),B-rr(60,120),rr(40,70),pal[2],.8);
  rings(cx-side*rr(300,360),cy-rr(190,260),rr(70,100),[pal[2],pal[4],pal[0],'#F3EAD5']);
  rings(cx+side*rr(300,370),cy+rr(220,300),rr(40,60),[pal[1],pal[3],'#F3EAD5']);
  // camada 4: grafismo a tinta, de borda a borda
  for(let i=0;i<4;i++){const x=rr(L+30,Rt-30);line(x,T+rr(0,60),x+rr(-14,14),B-rr(0,140),pick([1.4,2,3.4]));}
  for(let i=0;i<3;i++){const y=rr(T+60,B-60);line(L+rr(0,80),y,Rt-rr(0,80),y+rr(-40,40),pick([1.4,2.2]));}
  line(L+rr(0,120),B-rr(40,160),Rt-rr(0,120),T+rr(30,140),1.8);
  line(L+rr(20,140),T+rr(30,140),Rt-rr(200,380),B-rr(10,80),1.2);
  arc(cx,cy,rr(380,430),rr(3.4,3.9),rr(5.6,6.2),2.2);
  arc(cx+side*rr(260,320),cy-rr(150,230),rr(210,250),rr(0,1),rr(2,3),1.6);
  arc(cx-side*rr(300,360),cy+rr(160,260),rr(140,170),rr(3,4),rr(5,6),1.4);
  checker(cx+side*rr(300,360)-60,B-rr(150,220),5,3,rr(20,26),[pal[0],pal[2],pal[4]]);
  for(let i=0;i<9;i++)dot(rr(L+30,Rt-30),rr(T+30,B-30),rr(5,16),pick([ink,ink,pal[0],pal[2],pal[4]]));
  stem(rr(L+40,Rt-40),T+rr(40,180),B-rr(20,120),rr(9,15),pal[4]);
  splat(cx+side*rr(240,380),rr(cy-40,cy+200),rr(70,120),90,ink);
  splat(cx-side*rr(240,380),rr(T+60,cy-100),rr(60,100),60,pal[0]);
  splat(rr(L+100,Rt-100),B-rr(40,100),rr(50,80),40,pal[1]);
  // profundidade do quadro: luz de cima-esquerda, borda escurecida
  g.globalCompositeOperation='source-over';
  const lt=g.createLinearGradient(L,T,Rt,B);lt.addColorStop(0,'rgba(255,250,235,.10)');lt.addColorStop(1,'rgba(60,35,10,.10)');g.fillStyle=lt;g.fillRect(L,T,PW,PH);
  g.globalCompositeOperation='multiply';
  if(!opts.skip){const vg=g.createRadialGradient(cx,cy,Math.min(PW,PH)*.35,cx,cy,Math.max(PW,PH)*.78);vg.addColorStop(0,'rgba(255,255,255,0)');vg.addColorStop(1,'rgba(110,75,35,.16)');
  g.fillStyle=vg;g.fillRect(L,T,PW,PH);
  const sh=g.createRadialGradient(cx+16,cy+46,60,cx+16,cy+46,440);sh.addColorStop(0,'rgba(60,35,15,.34)');sh.addColorStop(1,'rgba(60,35,15,0)');
  g.fillStyle=sh;g.fillRect(L,T,PW,PH);}
  // trama da tela
  g.globalCompositeOperation='multiply';
  for(let x=L;x<Rt;x+=3){g.fillStyle='rgba(120,90,50,.035)';g.fillRect(x,T,1,PH);}
  for(let y=T;y<B;y+=3){g.fillStyle='rgba(120,90,50,.03)';g.fillRect(L,y,PW,1);}
  g.restore();
  // filete interno e sombra interna da borda (quadro com espessura)
  g.save();g.globalCompositeOperation='multiply';
  [['rgba(40,25,8,.35)',3],['rgba(40,25,8,.15)',9]].forEach(([c,w])=>{g.strokeStyle=c;g.lineWidth=w;g.strokeRect(X+w/2,Y+w/2,PW-w,PH-w);});
  g.restore();
  g.globalCompositeOperation='source-over';
  // ---- grão de tela + fibras
  g.globalCompositeOperation='source-over';
  const id=g.getImageData(0,0,W*D,H*D),d=id.data;
  for(let i=0;i<d.length;i+=4){const n=(R()-.5)*26, wv=((i/4)%(W*D))%6<1?-6:0;d[i]+=n+wv;d[i+1]+=n+wv;d[i+2]+=n+wv;}
  g.putImageData(id,0,0);
  g.globalCompositeOperation='multiply';
  for(let i=0;i<500;i++){g.strokeStyle=`rgba(120,90,50,${rr(.04,.1)})`;g.lineWidth=rr(.4,1);const x=rr(0,W),y=rr(0,H),a=rr(0,6.28),l=rr(4,16);g.beginPath();g.moveTo(x,y);g.lineTo(x+Math.cos(a)*l,y+Math.sin(a)*l);g.stroke();}
  g.globalCompositeOperation='source-over';
}
