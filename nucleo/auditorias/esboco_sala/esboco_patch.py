"""Esboço (só cópia de trabalho): mesa de Commander, piso de taco sob o carpete, luz no SVG (fase 2)."""
import sys; p=sys.argv[1]; h=open(p,encoding='utf8').read()
K="// ---------- sala gasta ----------"
assert K in h
add=r'''
// ===== ESBOÇO 07/11 =====
// 1. piso de taco aparecendo onde o carpete encardido acaba (junto ao rodapé)
const tacos = (()=>{ let s=''; for(let x=-400,k=0;x<1480;x+=36,k++){ const c=['#7A4E2A','#8A5A31','#6E4424'][k%3];
  s+=`<path d="M${x} 1012 L${x+36} 1012 L${x+18} 1030 L${x-18} 1030 Z" fill="${c}" stroke="#2A1A0E" stroke-width="2.5"/>`+
     `<path d="M${x+18} 1030 L${x+54} 1030 L${x+36} 1048 L${x} 1048 Z" fill="${['#6E4424','#7A4E2A','#8A5A31'][k%3]}" stroke="#2A1A0E" stroke-width="2.5"/>`; } return s; })();
const bordaCarpete = `<path d="M-400 1046 ${[...Array(48)].map((_,k)=>`L${-400+k*40+20} ${1040+(R(k+300)*10).toFixed(1)} L${-360+k*40} ${1046+(R(k+340)*6).toFixed(1)}`).join(' ')} L1480 1046 L1480 1060 L-400 1060 Z" fill="#6B6145" opacity=".9"/>`;
// 2. mesa de noite de Commander: playmat, 4 decks com sleeves, deckboxes, dados, cartas em jogo (sem cartas reais)
const SLV=['#A8473A','#3F6E9E','#2E2B2A','#4E7A55'];
const mesaCmd = `
 ${[[150,1197,-8],[250,1201,5],[402,1197,-4],[488,1200,8]].map(([x,y,r],i)=>`<g transform="rotate(${r} ${x+18} ${y+12})">
   <rect x="${x}" y="${y+4}" width="36" height="22" rx="3" fill="${SLV[i]}" ${S(3)}/><rect x="${x+2}" y="${y}" width="36" height="22" rx="3" fill="${SLV[i]}" ${S(3)}/>
   <path d="M${x+6} ${y+5} h26" stroke="#F2EBDA" stroke-width="2" opacity=".6"/></g>`).join('')}
 ${[[200,1206,-14],[222,1210,6],[330,1204,-3],[352,1206,10],[440,1210,-7]].map(([x,y,r],i)=>`<g transform="rotate(${r} ${x+9} ${y+12})">
   <rect x="${x}" y="${y}" width="18" height="24" rx="2" fill="#E8DFC4" ${S(2.5)}/><rect x="${x+3}" y="${y+3}" width="12" height="9" fill="${['#C98A45','#4E7392','#8C6BA8','#5E8A4E','#B5543A'][i]}"/></g>`).join('')}
 <rect x="56" y="1150" width="30" height="36" rx="3" fill="#2E2B2A" ${S(3.5)}/><rect x="56" y="1150" width="30" height="9" fill="#10B981" ${S(3)}/>
 <rect x="640" y="1150" width="28" height="34" rx="3" fill="#A8473A" ${S(3.5)} transform="rotate(6 654 1167)"/>
 <path d="M300 1214 l12 -9 l12 9 l-4 13 h-16 Z" fill="#3E9E7A" ${S(2.5)}/><text x="312" y="1224" text-anchor="middle" font-family="Bangers" font-size="11" fill="#F2EBDA">20</text>
 <rect x="372" y="1214" width="12" height="12" rx="2" fill="#E2C25A" ${S(2.5)} transform="rotate(14 378 1220)"/><circle cx="378" cy="1220" r="1.6" fill="#1B1B1B"/>
 <rect x="560" y="1188" width="13" height="13" rx="2" fill="#F2EBDA" ${S(2.5)} transform="rotate(-10 566 1194)"/><circle cx="563" cy="1191" r="1.4" fill="#1B1B1B"/><circle cx="569" cy="1197" r="1.4" fill="#1B1B1B"/>`;
// 3. luz no próprio cenário (fase 2): lâmpada quente, reflexo frio da TV na parede e na dupla, primeiro plano mais escuro
const luzDefs = `<defs>
 <radialGradient id="lzQ" cx="770" cy="190" r="520" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FFD9A0" stop-opacity=".30"/><stop offset="1" stop-color="#FFD9A0" stop-opacity="0"/></radialGradient>
 <radialGradient id="lzTV" cx="850" cy="650" r="420" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#4FE3C9" stop-opacity=".30"/><stop offset=".55" stop-color="#4FE3C9" stop-opacity=".10"/><stop offset="1" stop-color="#4FE3C9" stop-opacity="0"/></radialGradient>
 <linearGradient id="lzF" x1="0" y1="1120" x2="0" y2="1700" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#140C06" stop-opacity="0"/><stop offset="1" stop-color="#140C06" stop-opacity=".42"/></linearGradient>
 <mask id="lzM"><rect x="-400" y="-260" width="1880" height="2200" fill="#fff"/><rect x="636" y="514" width="428" height="274" rx="6" fill="#000"/></mask></defs>`;
const luzQuente = `<rect x="-400" y="-260" width="1880" height="1300" fill="url(#lzQ)" style="mix-blend-mode:screen"/>`;
const luzTV = `<g mask="url(#lzM)"><rect x="-400" y="-260" width="1880" height="1700" fill="url(#lzTV)" style="mix-blend-mode:screen"/></g>`;
const luzFrente = `<rect x="-400" y="1120" width="1880" height="900" fill="url(#lzF)"/>`;
'''
h=h.replace(K, add+K,1)
# taco + borda entram logo depois do rodapé (antes do carpete ficar por cima só a partir de 1046)
h=h.replace('<rect x="-400" y="1012" width="1880" height="820" fill="url(#carpet)"/>',
            '<rect x="-400" y="1012" width="1880" height="820" fill="url(#carpet)"/>${tacos}${bordaCarpete}',1)
h=h.replace("const room = `","const room = `",1)
# os 4 retângulos castanhos antigos dão lugar à mesa de Commander
old="${[[170,1196,-8],[236,1200,6],[420,1196,-4],[480,1198,9]].map(([x,y,r])=>`<rect x=\"${x}\" y=\"${y}\" width=\"40\" height=\"28\" rx=\"3\" fill=\"#6E4A2E\" ${S(3)} transform=\"rotate(${r} ${x+20} ${y+14})\"/>`).join('')}"
assert old in h; h=h.replace(old,"${mesaCmd}",1)
# camadas de luz: quente depois da sala, TV por cima da dupla (fora da tela), primeiro plano por cima da mesa
h=h.replace('<g id="cam"><g filter="url(#rough)">${room}</g>','<g id="cam">${luzDefs}<g filter="url(#rough)">${room}</g>${luzQuente}',1)
k='<g filter="url(#rough)">${table}</g></g>`;'
assert k in h; h=h.replace(k,'${luzTV}<g filter="url(#rough)">${table}</g>${luzFrente}</g>`;',1)
open(p,'w',encoding='utf8').write(h)
# Ajuste testado depois do esboço 1: mesa sobe para fora da faixa das legendas no plano geral.
# Em index.html: <g filter="url(#rough)" transform="translate(-20 -96) scale(1.04)">${table}</g>
