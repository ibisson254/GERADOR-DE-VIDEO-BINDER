// Ilustrações originais (pop art plano) para os cartazes de capa. Nenhuma copia arte de carta.
const TINTA = '#15131A';
const RET = (id, cor) => `<pattern id="${id}" width="10" height="10" patternUnits="userSpaceOnUse"><circle cx="5" cy="5" r="2.1" fill="${cor}"/></pattern>`;
const ILU = {
avon: `<svg viewBox="0 0 940 520" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><defs>${RET('ra','#FF5FA8')}${RET('rb','#7A5CFF')}</defs>
 <rect width="940" height="520" fill="#FFB36B"/><rect y="0" width="940" height="120" fill="#FF8A2A"/><rect y="120" width="940" height="90" fill="#FFA35A"/>
 <circle cx="470" cy="250" r="118" fill="#FFD23F" stroke="${TINTA}" stroke-width="5"/><circle cx="470" cy="250" r="118" fill="url(#ra)" opacity=".35"/>
 <path d="M0 330 L120 210 L210 300 L330 150 L430 290 L520 230 L640 120 L760 280 L850 200 L940 300 L940 380 L0 380Z" fill="#7A5CFF" stroke="${TINTA}" stroke-width="5" stroke-linejoin="round"/>
 <path d="M330 150 L300 192 L330 182 L352 200 L372 178Z M640 120 L606 168 L640 156 L662 176 L690 160Z" fill="#FFF7EA" stroke="${TINTA}" stroke-width="4" stroke-linejoin="round"/>
 <path d="M0 360 L160 280 L280 340 L420 270 L560 340 L700 260 L820 330 L940 290 L940 400 L0 400Z" fill="#23286B" stroke="${TINTA}" stroke-width="5" stroke-linejoin="round"/>
 <path d="M0 330 L120 210 L210 300 L330 150 L430 290 L520 230 L640 120 L760 280 L850 200 L940 300 L940 380 L0 380Z" fill="url(#rb)" opacity=".25"/>
 <rect y="398" width="940" height="122" fill="#6CC9FF" stroke="${TINTA}" stroke-width="5"/>
 <g stroke="#FFF7EA" stroke-width="7" stroke-linecap="round"><line x1="400" y1="430" x2="540" y2="430"/><line x1="420" y1="458" x2="520" y2="458"/><line x1="445" y1="486" x2="495" y2="486"/><line x1="150" y1="445" x2="230" y2="445"/><line x1="720" y1="470" x2="820" y2="470"/></g>
 <path d="M0 520 L0 440 Q90 420 170 460 L230 520Z" fill="${TINTA}"/><path d="M118 432 l10 -42 l12 0 l10 42Z" fill="${TINTA}"/><circle cx="134" cy="384" r="9" fill="${TINTA}"/>
</svg>`,
poole: `<svg viewBox="0 0 940 520" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><defs>${RET('pa','#23286B')}</defs>
 <rect width="940" height="520" fill="#2C6BFF"/><rect width="940" height="520" fill="url(#pa)" opacity=".35"/>
 <g transform="translate(470 260)"><path d="${Array.from({length:32},(_,i)=>{const a=i*Math.PI/16,r=i%2?150:250;return (i?'L':'M')+(r*Math.cos(a)).toFixed(1)+' '+(r*Math.sin(a)*.8).toFixed(1)}).join(' ')}Z" fill="#FFD23F" stroke="${TINTA}" stroke-width="6" stroke-linejoin="round"/></g>
 <text x="470" y="318" text-anchor="middle" font-family="Anton" font-size="190" fill="#FF3D2E" stroke="${TINTA}" stroke-width="6" paint-order="stroke">1993</text>
 <g transform="translate(840 120) rotate(38)"><rect x="-14" y="0" width="28" height="250" rx="10" fill="#FF8A2A" stroke="${TINTA}" stroke-width="5"/><rect x="-18" y="-40" width="36" height="46" fill="#C8CCD6" stroke="${TINTA}" stroke-width="5"/><path d="M-18 -40 Q0 -120 18 -40Z" fill="${TINTA}"/></g>
 <g fill="#FFF7EA" stroke="${TINTA}" stroke-width="4"><path d="M110 90 l12 28 l30 2 l-24 18 l9 30 l-27 -17 l-27 17 l9 -30 l-24 -18 l30 -2Z"/><path d="M150 400 l9 21 l22 2 l-18 13 l7 22 l-20 -12 l-20 12 l7 -22 l-18 -13 l22 -2Z"/><path d="M820 410 l9 21 l22 2 l-18 13 l7 22 l-20 -12 l-20 12 l7 -22 l-18 -13 l22 -2Z"/></g>
</svg>`,
walker: `<svg viewBox="0 0 940 520" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><defs>${RET('wa','#FF3D2E')}${RET('wb','#15131A')}</defs>
 <rect width="940" height="520" fill="#FFD23F"/><rect width="940" height="520" fill="url(#wa)" opacity=".45"/>
 <g transform="translate(470 265)"><path d="${Array.from({length:24},(_,i)=>{const a=i*Math.PI/12,r=i%2?160:(i%4?260:300);return (i?'L':'M')+(r*Math.cos(a)).toFixed(1)+' '+(r*Math.sin(a)*.72).toFixed(1)}).join(' ')}Z" fill="#FF3D2E" stroke="${TINTA}" stroke-width="7" stroke-linejoin="round"/>
 <path d="${Array.from({length:24},(_,i)=>{const a=i*Math.PI/12+.13,r=i%2?120:190;return (i?'L':'M')+(r*Math.cos(a)).toFixed(1)+' '+(r*Math.sin(a)*.72).toFixed(1)}).join(' ')}Z" fill="#FFF7EA" stroke="${TINTA}" stroke-width="6" stroke-linejoin="round"/></g>
 <text x="470" y="325" text-anchor="middle" font-family="Anton" font-size="170" fill="${TINTA}">500+</text>
 <g transform="translate(110 400) rotate(-30)"><path d="M0 0 L40 -10 L60 60 L30 110 L0 60Z" fill="#C8CCD6" stroke="${TINTA}" stroke-width="5"/><line x1="30" y1="40" x2="30" y2="105" stroke="${TINTA}" stroke-width="4"/><rect x="2" y="-120" width="40" height="112" fill="${TINTA}"/></g>
 <g fill="${TINTA}"><circle cx="830" cy="90" r="14"/><circle cx="868" cy="130" r="8"/><circle cx="800" cy="440" r="18"/><circle cx="850" cy="470" r="9"/></g>
</svg>`,
magali: `<svg viewBox="0 0 940 520" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><defs>${RET('ma','#FF3D2E')}</defs>
 <rect width="940" height="520" fill="#23286B"/>
 <circle cx="700" cy="150" r="90" fill="#FFF1D6" stroke="${TINTA}" stroke-width="5"/>
 <path d="M80 520 C160 380 120 300 230 210 C200 320 300 330 290 230 C380 300 330 420 420 360 C410 300 470 260 500 200 C520 300 600 330 560 430 C640 380 650 300 700 300 C720 400 640 470 690 520Z" fill="#FF8A2A" stroke="${TINTA}" stroke-width="6" stroke-linejoin="round"/>
 <path d="M190 520 C230 430 220 380 280 320 C280 400 350 400 350 330 C410 390 380 460 450 440 C460 390 490 360 510 320 C540 400 560 450 540 520Z" fill="#FFD23F" stroke="${TINTA}" stroke-width="5" stroke-linejoin="round"/>
 <path d="M80 520 C160 380 120 300 230 210 C200 320 300 330 290 230 C380 300 330 420 420 360 C410 300 470 260 500 200 C520 300 600 330 560 430 C640 380 650 300 700 300 C720 400 640 470 690 520Z" fill="url(#ma)" opacity=".3"/>
 <g transform="translate(800 330) rotate(25)"><rect x="-12" y="0" width="24" height="210" rx="10" fill="#FF5FA8" stroke="${TINTA}" stroke-width="5"/><rect x="-16" y="-36" width="32" height="40" fill="#C8CCD6" stroke="${TINTA}" stroke-width="5"/><path d="M-16 -36 Q0 -110 16 -36Z" fill="#FF3D2E" stroke="${TINTA}" stroke-width="4"/></g>
 <g fill="#FFF7EA"><circle cx="120" cy="90" r="5"/><circle cx="300" cy="60" r="4"/><circle cx="460" cy="110" r="6"/><circle cx="880" cy="60" r="4"/><circle cx="560" cy="60" r="3"/></g>
</svg>`,
swanland: `<svg viewBox="0 0 940 520" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><defs>${RET('sa','#6CC9FF')}</defs>
 <rect width="940" height="520" fill="#7A5CFF"/><rect width="940" height="520" fill="url(#sa)" opacity=".28"/>
 <g fill="none" stroke-linecap="round">${Array.from({length:7},(_,i)=>`<path d="M${-40+i*20} ${470-i*8} C ${220+i*10} ${120+i*20}, ${560-i*15} ${600-i*30}, ${980} ${90+i*36}" stroke="${['#6CC9FF','#FFF7EA','#FFD23F','#FF5FA8','#6CC9FF','#FFF7EA','#23286B'][i]}" stroke-width="${22-i*2}"/>`).join('')}</g>
 <path d="M470 240 C520 150 640 110 760 120 C700 150 690 170 700 190 C650 180 630 200 640 225 C590 215 560 240 570 265 C540 255 500 260 470 240Z" fill="${TINTA}"/>
 <path d="M470 240 C420 150 300 110 180 120 C240 150 250 170 240 190 C290 180 310 200 300 225 C350 215 380 240 370 265 C400 255 440 260 470 240Z" fill="${TINTA}"/>
 <circle cx="470" cy="250" r="22" fill="#FFD23F" stroke="${TINTA}" stroke-width="6"/>
</svg>`,
seb: `<svg viewBox="0 0 940 520" width="100%" height="100%" preserveAspectRatio="xMidYMid slice"><defs>${RET('ka','#6CC9FF')}</defs>
 <rect width="940" height="520" fill="#23286B"/><rect width="940" height="520" fill="url(#ka)" opacity=".18"/>
 <circle cx="660" cy="170" r="120" fill="#FFF1D6" stroke="${TINTA}" stroke-width="5"/><circle cx="700" cy="140" r="22" fill="#F2DDB5"/><circle cx="620" cy="210" r="14" fill="#F2DDB5"/>
 <g fill="${TINTA}">${[[40,250],[110,200],[180,260],[250,180],[330,240],[790,220],[860,170],[920,240]].map(([x,h])=>`<path d="M${x} ${520-h} L${x-38} 520 L${x+38} 520Z"/>`).join('')}</g>
 <g transform="translate(470 250) rotate(-6)">
  <rect x="-150" y="0" width="300" height="160" fill="#FFF7EA" stroke="${TINTA}" stroke-width="7"/>
  <g transform="rotate(-14 -150 0)"><rect x="-150" y="-52" width="300" height="52" fill="${TINTA}"/>${[0,1,2,3,4].map(i=>`<path d="M${-130+i*60} -52 l30 0 l-24 52 l-30 0Z" fill="#FFF7EA"/>`).join('')}</g>
  <rect x="-150" y="0" width="300" height="40" fill="${TINTA}"/>${[0,1,2,3,4].map(i=>`<path d="M${-130+i*60} 0 l30 0 l-24 40 l-30 0Z" fill="#FFF7EA"/>`).join('')}
  <text x="0" y="118" text-anchor="middle" font-family="Anton" font-size="60" fill="#FF3D2E">CENA 1</text></g>
</svg>`
};
