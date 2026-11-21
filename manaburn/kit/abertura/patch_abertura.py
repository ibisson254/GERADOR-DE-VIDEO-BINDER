"""Abertura de carta (padrão do Mana & Burn desde 21/11/2026, decisão do fundador). Aplica-se uma vez ao kit;
tudo fica desligado sem o campo novo, por isso os episódios antigos saem iguais.

episode.js  EP.abertura = {img, ate, hl:[[x,y,w,h],...], selo:{txt, x, y, rot}, w, top, saida}
            img   PNG da carta falada (745x1040 do Scryfall), inteira, sem nada por cima do texto.
            ate   fração da 1.ª fala em que a carta sai (quando a palavra-chave ou o número do gancho já foi dito).
            hl    linhas de regra a destacar (frações da carta, as mesmas medidas do EP.canais[].hl).
            selo  carimbo com o número do gancho, em frações da carta, sobre a arte (nunca sobre o texto).
            w     largura da carta em px (660 por defeito: inteira entre o crédito do topo e as legendas, também no impacto de 1,06); top (330); saida (0,32 s).
episode.json "abertura": {"ate": <igual ao do episode.js>} — o process.py põe a pancada no quadro 0 e o «zap» na saída.

Comportamento: quadro 0 = carta inteira em grande, linhas destacadas e selo já visíveis (miniatura legível sem som);
0–0,18 s impacto (escala 1,06→1, tremor que decai, pancada); depois aproxima 3 % devagar até `ate`;
em `saida` segundos a carta voa para dentro do ecrã da TV (encolhe até ao tamanho da tela da TV SAL) e o fundo
escurecido some. Não acrescenta tempo ao vídeo: corre por cima da 1.ª fala. Legendas e crédito ficam por cima.
"""
import pathlib
K = pathlib.Path(__file__).resolve().parents[1]   # manaburn/kit
M = K.parent                                      # manaburn/

def troca(txt, a, b, nome):
    assert txt.count(a) == 1, (nome, a[:60], txt.count(a))
    return txt.replace(a, b)

# ---- index.html ----
p = M / 'index.html'; h = p.read_text(encoding='utf8')
if 'EP.abertura' in h:
    print('index.html já tem a abertura')
else:
    h = troca(h, '  <div id="ins"></div>', '  <div id="abertura" style="display:none;position:absolute;left:0;top:0;width:1080px;height:1920px"></div>\n  <div id="ins"></div>', 'dom')
    fn = r'''
// ---------- abertura de carta (padrão desde 21/11/2026, kit/abertura/patch_abertura.py) ----------
const AB = EP.abertura || null; let AB_EL=null, AB_CARD=null, AB_BACK=null, AB_SELO=null, AB_HL=[];
if(AB){ const W=AB.w||660, H=W*1040/744, X0=(1080-W)/2, Y0=AB.top||330; AB_EL=document.getElementById('abertura');
  AB_EL.innerHTML=`<div id="abBack" style="position:absolute;left:0;right:0;top:${AB.fundoTop??200}px;bottom:0;background:rgba(5,10,16,.80);backdrop-filter:blur(5px)"></div>
   <div id="abCard" style="position:absolute;left:${X0}px;top:${Y0}px;width:${W}px;height:${H}px;transform-origin:50% 50%">
    <img src="${AB.img}" style="position:absolute;inset:0;width:100%;height:100%;border-radius:${W*0.045}px;box-shadow:0 18px 0 rgba(0,0,0,.5),0 0 60px rgba(255,216,74,.25)">
    ${(AB.hl||[]).map(r=>`<div class="abhl" style="position:absolute;left:${r[0]*100}%;top:${r[1]*100}%;width:${r[2]*100}%;height:${r[3]*100}%;border:4px solid #FFD84A;border-radius:6px;background:rgba(255,216,74,.22)"></div>`).join('')}
    ${AB.selo?`<div id="abSelo" style="position:absolute;left:${AB.selo.x*100}%;top:${AB.selo.y*100}%;font:400 ${AB.selo.size||70}px/1 Bangers;letter-spacing:2px;color:#FFD84A;background:#C8352B;border:6px solid #050A10;border-radius:12px;padding:6px 18px;white-space:nowrap;transform:rotate(${AB.selo.rot||-6}deg);box-shadow:0 8px 0 rgba(0,0,0,.45)">${AB.selo.txt}</div>`:''}
   </div>`;
  AB_CARD=document.getElementById('abCard'); AB_BACK=document.getElementById('abBack'); AB_SELO=document.getElementById('abSelo'); AB_HL=[...AB_EL.querySelectorAll('.abhl')]; }
function aberturaT1(){ const L0=LINES[0]; return L0.start+L0.dur*(AB.ate||0.45); }
function abertura(t){ if(!AB) return; const T1=aberturaT1(), E=AB.saida||0.32;
  if(t>=T1+E){ AB_EL.style.display='none'; return; } AB_EL.style.display='block';
  const W=AB.w||660, H=W*1040/744, Y0=AB.top||330; let s, dx=0, dy=0, op=1, bg=1;
  if(t<0.18){ const q=ease(clamp(t/0.18)), sh=(1-q)*8; s=1.06-0.06*q; dx=Math.sin(t*95)*sh; dy=Math.cos(t*73)*sh; }
  else s=1+0.03*clamp((t-0.18)/Math.max(0.5,T1-0.18));
  if(t>=T1){ const q=ease(clamp((t-T1)/E)), c=TVSHOTS.includes(POSE[0][6])?s2Cam(0,t):{s:1,cx:432,cy:963,tx:432,ty:963};
    const cxT=c.tx+c.s*(SCR.x+SCR.w/2-c.cx), cyT=c.ty+c.s*(SCR.y+SCR.h/2-c.cy), sT=0.86*SCR.h*c.s/H, s0=1.03;
    s=s0+(sT-s0)*q; dx=(cxT-540)*q; dy=(cyT-(Y0+H/2))*q; bg=1-q; op=q>0.8?1-(q-0.8)/0.2:1; }
  AB_CARD.style.transform=`translate(${dx.toFixed(1)}px,${dy.toFixed(1)}px) scale(${s.toFixed(4)})`; AB_CARD.style.opacity=op; AB_BACK.style.opacity=bg;
  if(AB_SELO){ const q=ease(clamp(t/0.16)); AB_SELO.style.scale=(1.3-0.3*q).toFixed(3); }
  const g=0.55+0.45*Math.abs(Math.sin(t*5)); AB_HL.forEach(e=>e.style.boxShadow=`0 0 ${Math.round(18*g)}px rgba(255,216,74,${(0.7*g).toFixed(2)})`); }
'''
    h = troca(h, 'function render(t){\n', fn + 'function render(t){\n  abertura(t);\n', 'render')
    p.write_text(h, encoding='utf8'); print('abertura aplicada em', p)

# ---- sfx.py: pancada no quadro 0 e zap na saída ----
p = M / 'sfx.py'; s = p.read_text(encoding='utf8')
if 'abertura=None' not in s:
    s = troca(s, "          zaps=(), zaps_leves=()):", "          zaps=(), zaps_leves=(), abertura=None):", 'sfx sig')
    s = troca(s, "    for t in raiva: put(t, thump(sr), 0.15)                          # on_rage_arms_up\n",
              "    for t in raiva: put(t, thump(sr), 0.15)                          # on_rage_arms_up\n"
              "    if abertura is not None:                                         # abertura de carta (21/11/2026)\n"
              "        put(0.0, thump(sr) * 1.2); put(0.02, pop(sr) * 0.8, 0.1)       # impacto no quadro 0\n"
              "        put(max(0, abertura - 0.02), zap(sr), -0.1)                  # a carta entra na TV\n", 'sfx put')
    p.write_text(s, encoding='utf8'); print('abertura no sfx.py')

# ---- process.py: passa o instante de saída ----
p = M / 'process.py'; s = p.read_text(encoding='utf8')
if "EPI.get('abertura')" not in s:
    s = troca(s, "                carta=SFX.get('carta', 'pop'), tv=SFX.get('tv', True), zaps=zaps, zaps_leves=zaps_leves)",
              "                carta=SFX.get('carta', 'pop'), tv=SFX.get('tv', True), zaps=zaps, zaps_leves=zaps_leves,\n"
              "                abertura=(lines[0]['start'] + lines[0]['dur'] * EPI['abertura'].get('ate', 0.45)) if EPI.get('abertura') else None)", 'process')
    p.write_text(s, encoding='utf8'); print('abertura no process.py')
