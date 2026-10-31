// Camada em movimento "Órbita": discos em órbitas contínuas à volta da carta e anéis que giram sem parar.
// Velocidade angular constante, uma volta por loop: o último quadro emenda no primeiro.
function makeOrbit(seed, pal, o){
  const D=2, R=mulberry32(seed*7+3), rr=(a,b)=>a+R()*(b-a);
  const hex2=(h,a)=>{const n=parseInt(h.slice(1),16);return `rgba(${n>>16&255},${n>>8&255},${n&255},${a})`};
  const ink='#171512';
  // sprites pintados uma vez (textura fixa, movimento limpo)
  function discSprite(r,col){const c=document.createElement('canvas');c.width=c.height=(r*2+8)*D;const g=c.getContext('2d');g.scale(D,D);
    const x=r+4,y=r+4;g.fillStyle=col;g.beginPath();g.arc(x,y,r,0,7);g.fill();g.save();g.beginPath();g.arc(x,y,r,0,7);g.clip();
    const gr=g.createRadialGradient(x-r*.35,y-r*.4,r*.1,x,y,r*1.15);gr.addColorStop(0,'rgba(255,248,230,.24)');gr.addColorStop(.55,'rgba(255,248,230,0)');gr.addColorStop(1,'rgba(40,20,5,.26)');
    g.fillStyle=gr;g.fillRect(0,0,2*x,2*y);g.globalCompositeOperation='multiply';
    for(let s=0;s<16;s++){g.strokeStyle=hex2('#6b4a2a',rr(.03,.07));g.lineWidth=rr(5,16);g.beginPath();const yy=rr(4,2*r+4);g.moveTo(0,yy);g.bezierCurveTo(r*.6,yy+rr(-16,16),r*1.4,yy+rr(-16,16),2*r+8,yy+rr(-8,8));g.stroke();}
    g.restore();return c;}
  function ringSprite(r,cols){const c=document.createElement('canvas');c.width=c.height=(r*2+20)*D;const g=c.getContext('2d');g.scale(D,D);const x=r+10;
    cols.forEach((col,i)=>{const rad=r*(1-i/cols.length),w=r/(cols.length*1.9);g.strokeStyle=col;g.lineWidth=w;g.lineCap='round';
      const gap=.35+i*.12, st=i*1.7;g.beginPath();g.arc(x,x,rad,st,st+Math.PI*2-gap);g.stroke();
      g.fillStyle=ink;g.beginPath();g.arc(x+Math.cos(st)*rad,x+Math.sin(st)*rad,Math.max(3,w*.28),0,7);g.fill();});
    return c;}
  const cx=o.cx, cy=o.cy, dir=R()<.5?1:-1;
  const bodies=[
    {s:discSprite(rr(140,165),pal[0]), rx:rr(330,370), ry:rr(240,280), a0:rr(0,6.28), w:dir},
    {s:discSprite(rr(82,100),pal[1]),  rx:rr(400,430), ry:rr(310,340), a0:rr(0,6.28), w:-dir},
    {s:discSprite(rr(34,44),pal[4]),   rx:rr(250,290), ry:rr(330,360), a0:rr(0,6.28), w:dir},
    {s:discSprite(rr(16,22),ink),      rx:rr(440,470), ry:rr(200,240), a0:rr(0,6.28), w:-dir},
  ];
  const rings=[
    {s:ringSprite(rr(78,96),[pal[2],pal[4],pal[0],'#F3EAD5']), x:cx-dir*rr(320,360), y:cy-rr(230,270), w:dir},
    {s:ringSprite(rr(48,60),[pal[1],pal[3],'#F3EAD5']),        x:cx+dir*rr(330,370), y:cy+rr(250,290), w:-dir},
  ];
  const ARC_SEG=6, arcR=rr(395,425);
  return function draw(cv,t){
    const g=cv.getContext('2d');g.setTransform(D,0,0,D,0,0);g.clearRect(0,0,1080,1350);
    g.save();g.beginPath();g.rect(o.px,o.py,o.pw,o.ph);g.clip();
    const TAU=Math.PI*2;
    // arco tracejado à volta da carta: 1/6 de volta por loop (padrão de 6 traços = emenda perfeita)
    g.save();g.translate(cx,cy);g.rotate(TAU*t/ARC_SEG);g.strokeStyle='rgba(23,21,18,.85)';g.lineWidth=2;g.lineCap='round';
    for(let i=0;i<ARC_SEG;i++){const a=i*TAU/ARC_SEG;g.beginPath();g.ellipse(0,0,arcR,arcR*.82,0,a,a+TAU/ARC_SEG*.55);g.stroke();}g.restore();
    // anéis girando
    rings.forEach(r=>{g.save();g.translate(r.x,r.y);g.rotate(r.w*TAU*t);g.shadowColor='rgba(55,35,15,.28)';g.shadowBlur=14;g.shadowOffsetY=6;
      const s=r.s.width/D;g.drawImage(r.s,-s/2,-s/2,s,s);g.restore();});
    // discos em órbita
    bodies.forEach(b=>{const a=b.a0+b.w*TAU*t, x=cx+Math.cos(a)*b.rx, y=cy+Math.sin(a)*b.ry, s=b.s.width/D;
      g.save();g.shadowColor='rgba(55,35,15,.34)';g.shadowBlur=26;g.shadowOffsetX=8;g.shadowOffsetY=13;g.drawImage(b.s,x-s/2,y-s/2,s,s);g.restore();});
    g.restore();
  };
}

// película por cima de tudo o que se move: grão de tela fixo, vinheta e sombra de contato da carta
function overlay(cv,o,seed){
  const D=2;cv.width=1080*D;cv.height=1350*D;const g=cv.getContext('2d');g.scale(D,D);const R=mulberry32(seed+99);
  g.save();g.beginPath();g.rect(o.px,o.py,o.pw,o.ph);g.clip();
  const vg=g.createRadialGradient(o.cx,o.cy,Math.min(o.pw,o.ph)*.35,o.cx,o.cy,Math.max(o.pw,o.ph)*.78);vg.addColorStop(0,'rgba(110,75,35,0)');vg.addColorStop(1,'rgba(110,75,35,.16)');
  g.fillStyle=vg;g.fillRect(0,0,1080,1350);
  const sh=g.createRadialGradient(o.cx+16,o.cy+46,60,o.cx+16,o.cy+46,440);sh.addColorStop(0,'rgba(60,35,15,.30)');sh.addColorStop(1,'rgba(60,35,15,0)');
  g.fillStyle=sh;g.fillRect(0,0,1080,1350);
  for(let x=o.px;x<o.px+o.pw;x+=3){g.fillStyle='rgba(120,90,50,.035)';g.fillRect(x,o.py,1,o.ph);}
  for(let y=o.py;y<o.py+o.ph;y+=3){g.fillStyle='rgba(120,90,50,.03)';g.fillRect(o.px,y,o.pw,1);}
  for(let i=0;i<9000;i++){g.fillStyle=`rgba(90,65,35,${(R()*.08).toFixed(3)})`;g.fillRect(o.px+R()*o.pw,o.py+R()*o.ph,R()*1.6+.4,R()*1.6+.4);}
  g.restore();
}
