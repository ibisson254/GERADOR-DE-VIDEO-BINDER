// Monta os 5 slides de um carrossel "Artistas de Magic" (padrão Lambe-lambe, 12/11/2026).
const K = (k) => 'cartas/' + k;
const cred = (keys) => keys.map(k => { const c = CRED[k]; return `${c.name} (${c.set}, ${c.year}), nº ${c.num}. Arte: ${c.artist}`; }).join(' · ')
  + '. © Wizards of the Coast. Conteúdo de fã não oficial.';
const CREDITO = (keys, y=1196, h=96) => P({cls:'creditos sombra',x:60,y,w:960,h,r:0,f:'r4',ff:'r4',
  c:`<div class="conteudo" style="font-size:17px;padding:14px 24px">${cred(keys)}</div>`});
const SELO = (x=40,y=36,w=330,h=104,r=-3,fs=40) => P({cls:'selo-azul sombra',x,y,w,h,r,f:'r4',ff:'r4',
  c:`<div class="conteudo" style="height:100%;font-size:${fs}px">ARTISTAS<br>DE MAGIC</div>`});

const nomeLinhas = D.nome.split('<br>').length;
const S = [];

// 1 · capa: gancho + ilustração original + nome
S.push(base(
  P({cls:'pop branco sombra',x:56,y:140,w:968,h:390,r:-1.2,f:'r1',ff:'r2',c:`<div class="reticula"></div>
    <h1 style="font-size:90px;padding:50px 0 0 56px">${D.capa.gancho}</h1>`})
 + SELO(36,40,330,110,-3.5,42)
 + P({cls:'pop sombra',x:76,y:530,w:928,h:410,r:.9,f:'r3',ff:'r1',c:`<div class="ilu">${ILU[ID]}</div>`})
 + F(150,548,140,-28) + F(930,542,140,30)
 + P({cls:'marinho sombra',x:40,y:900,w:1000,h:nomeLinhas>1?262:210,r:-1.4,f:'r2',ff:'r3',c:`
    <div class="nome" style="font-size:${nomeLinhas>1?112:170}px;padding:${nomeLinhas>1?30:26}px 0 0 56px">${D.nome}</div>`})
 + P({cls:'chip sombra',x:620,y:nomeLinhas>1?1128:1078,w:360,h:84,r:-3,f:'r4',ff:'r4',c:`<div class="conteudo" style="height:100%;font-size:36px"><i>≈</i>${D.capa.chip}<i>≈</i></div>`})
 + P({cls:'pop branco sombra',x:70,y:nomeLinhas>1?1196:1150,w:600,h:76,r:1,f:'r4',ff:'r4',c:`<div class="txt" style="font-size:27px;font-weight:700;padding:21px 28px;white-space:nowrap">${D.capa.linha}</div>`})
 + E('arrasta →', 880, 1290, -3, 36)
,1));

// 2 · Quem pintou? carta real + factos
{ const s=D.s2, duas=!!s.carta2;
S.push(base(
  SELO(40,36,280,90,-3,34)
 + (duas ? C(K(s.carta),240,640,370,-5) + C(K(s.carta2),430,800,330,4) : C(K(s.carta),330,660,470,-4))
 + E('Quem pintou?', 790, 150, 3, 50)
 + P({cls:'pop branco sombra',x:600,y:230,w:440,h:150,r:-2,f:'r3',ff:'r4',c:`<div class="marc" style="font-size:${s.marcador.length>14?44:56}px;padding:40px 0 0 28px;white-space:nowrap">${s.marcador}</div><div class="risco" style="position:absolute;left:28px;right:40px;bottom:30px"></div>`})
 + P({cls:'pop branco sombra',x:620,y:420,w:420,h:640,r:1.5,f:'r1',ff:'r2',c:`<div class="txt" style="font-size:33px;padding:46px 40px">${s.texto}</div>`})
 + CREDITO(duas?[s.carta,s.carta2]:[s.carta])
,2)); }

// 3 · número grande + carta
{ const s=D.s3;
S.push(base(
  P({cls:'pop sombra',x:56,y:80,w:968,h:560,r:-1,f:'r1',ff:'r3',c:`<div class="reticula"></div>
    <div style="position:absolute;left:64px;top:56px;font-family:Anton;font-size:72px;color:#15131A;text-transform:uppercase">${s.pre}</div>
    <div style="position:absolute;left:52px;top:118px;font-family:Anton;font-size:330px;line-height:1.1;color:#E0337A;-webkit-text-stroke:5px #15131A">${s.num}</div>
    <div style="position:absolute;left:64px;bottom:44px;font-family:Anton;font-size:72px;color:#15131A;text-transform:uppercase">${s.pos}</div>`})
 + SELO(760,40,250,80,4,30)
 + C(K(s.carta),300,900,330,-4)
 + P({cls:'pop branco sombra',x:540,y:700,w:480,h:440,r:1.8,f:'r3',ff:'r1',c:`<div class="txt" style="font-size:35px;padding:48px 42px">${s.texto}</div>`})
 + CREDITO([s.carta])
,3)); }

// 4 · a história
{ const s=D.s4, duas=!!s.carta2;
S.push(base(
  P({cls:'pop branco sombra',x:56,y:70,w:968,h:310,r:1,f:'r2',ff:'r1',c:`<div class="reticula"></div>
    <h1 style="font-size:112px;padding:48px 0 0 56px">${s.titulo}</h1>`})
 + (duas ? C(K(s.carta),290,760,400,-5) + C(K(s.carta2),790,760,400,5)
         : C(K(s.carta),300,760,440,-3.5))
 + (duas ? P({cls:'pop sombra',x:140,y:1060,w:800,h:110,r:-1.5,f:'r4',ff:'r4',c:`<div class="txt" style="font-size:36px;padding:32px 40px;white-space:nowrap;text-align:center">${s.texto}</div>`})
         : P({cls:'pop sombra',x:580,y:450,w:450,h:640,r:-1.8,f:'r1',ff:'r3',c:`<div class="txt" style="font-size:33px;padding:46px 40px">${s.texto}</div>`}))
 + CREDITO(duas?[s.carta,s.carta2]:[s.carta])
,4)); }

// 5 · pergunta + cartaz BINDER (produto)
S.push(base(
  P({cls:'pop sombra',x:56,y:70,w:968,h:500,r:-1.2,f:'r1',ff:'r2',c:`<div class="reticula"></div>
    <h1 style="font-size:104px;padding:50px 0 0 56px">${D.s5.pergunta}</h1>
    <div class="marc" style="position:absolute;right:56px;bottom:40px;font-size:40px;transform:rotate(-3deg)">responda nos comentários ↓</div>`})
 + P({cls:'binder sombra',x:96,y:630,w:888,h:600,r:.8,f:'r3',ff:'r1',c:`
    <div style="position:absolute;left:64px;top:58px">${BLOGO}</div>
    <div style="position:absolute;left:64px;top:160px;right:64px">
      <div class="titulo" style="font-size:66px">Achou o nome<br>no rodapé?</div>
      <div class="traco" style="margin:30px 0 26px"></div>
      <div class="sub" style="font-size:31px">Aponte a câmera: o BINDER Vision ajuda a identificar a carta e a guardar no seu Binder.</div>
    </div>
    <div class="btn" style="position:absolute;left:64px;bottom:54px;font-size:30px;padding:22px 40px">Beta para Android · link na bio</div>`})
 + F(170,664,150,-30) + F(910,658,150,30)
 + SELO(790,1250,240,76,-4,28)
,5));

document.getElementById('raiz').innerHTML = S.map((h,i)=>`<div class="slide" id="s${i+1}">${h}</div>`).join('');
