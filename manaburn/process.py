"""Monta a dublagem: corta as duas faixas (Burn e Mana) nas pausas, encaixa as falas em
bate-volta, alinha a parada seca da música com o "Comenta aí", gera data.js e a trilha final.
uso: python3 process.py burn.mp3 mana.mp3
A trilha sai de trilha.py: midnight_throttle por padrão, ou a faixa de "music" no episode.json.
Zapping (25/10): se o episode.js tiver EP.canais, cada canal novo (de: N) ganha o som de troca de canal
no começo da fala N, e o zapping rápido da abertura (flip_a_cada) ganha cliques leves.
"""
import sys, json, subprocess, wave, os, re
import numpy as np
import trilha

SR = 44100
import roteiro
EPI = roteiro.carrega('episode.json')          # esquema 1 (B/M) ou 2 (falas com legenda/tts)
TEXT = {'B': EPI['B'], 'M': EPI['M']}
# folga antes de cada fala (negativo = atropela a anterior, como numa discussão)
GAP = EPI['gap']
MUSIC = EPI.get('music')   # ex.: {"file": "concrete_teeth.mp3", "body_start": 11.15, "slam_src": 10.78, "stop_len": 1.25}

from cortes import load, split

burn = split(load(sys.argv[1]), TEXT['B'])
mana = split(load(sys.argv[2]), TEXT['M'])
# respiro: "respiro_max": 0.16 encurta os silêncios DENTRO de cada fala (entre frases) para no máximo 0,16 s,
# como um corte seco de edição de Reels. A voz e o ritmo das palavras não mudam.
RESP = EPI.get('respiro_max')
def encurta(seg, mx):
    hop = int(0.01 * SR); fr = np.sqrt(np.convolve(seg ** 2, np.ones(hop) / hop, 'same'))[::hop]
    thr = max(0.008, np.percentile(fr, 95) * 0.05); v = fr > thr
    idx = np.where(v)[0]
    if len(idx) < 2: return seg, 0.0
    out = []; pos = 0; i = idx[0]; keep = int(mx / 0.01); xf = int(0.008 * SR); cortado = 0
    while i < idx[-1]:
        if not v[i]:
            j = i
            while j < idx[-1] and not v[j]: j += 1
            if j - i > keep + 4:                                  # silêncio interno longo: fica só mx
                a = (i + keep // 2) * hop; b = (j - keep // 2) * hop
                head = seg[pos:a].copy(); tail = seg[b:b + xf].copy()
                if len(head) > xf and len(tail) == xf:            # emenda com crossfade curto, sem estalo
                    head[-xf:] = head[-xf:] * np.linspace(1, 0, xf) + tail * np.linspace(0, 1, xf)
                    out.append(head); pos = b + xf; cortado += (b - a)
            i = j
        else: i += 1
    out.append(seg[pos:])
    return np.concatenate(out), cortado / SR
if RESP:
    tot = 0
    for lst in (burn, mana):
        for k in range(len(lst)): lst[k], c = encurta(lst[k], RESP); tot += c
    print(f'   respiro: silêncios internos limitados a {RESP}s ({tot:.1f}s a menos)')
# ritmo: "tempo": {"B": 1.05, "M": 1.08} no episode.json acelera as falas sem mudar o tom da voz
TEMPO = EPI.get('tempo', {})
def stretch(seg, f):
    if abs(f - 1) < 0.005: return seg
    with wave.open('_s.wav', 'wb') as o:
        o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR); o.writeframes((np.clip(seg, -1, 1) * 32767).astype('<i2').tobytes())
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', '_s.wav', '-af', f'atempo={f}', '-ar', str(SR), '_s2.wav'], check=True)
    w = wave.open('_s2.wav'); return np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float32) / 32768
burn = [stretch(x, TEMPO.get('B', 1.0)) for x in burn]; mana = [stretch(x, TEMPO.get('M', 1.0)) for x in mana]
if TEMPO: print(f"   ritmo: Burn x{TEMPO.get('B', 1.0)}, Mana x{TEMPO.get('M', 1.0)}")
# nivela cada fala: o Mana fala baixo e calmo, então sobe até ficar no mesmo volume do Burn
def level(seg, target=0.11):
    hop = int(0.02 * SR); fr = np.sqrt(np.convolve(seg ** 2, np.ones(hop) / hop, 'same'))
    act = fr > max(0.01, fr.max() * 0.12)
    rms = np.sqrt((seg[act] ** 2).mean()) if act.any() else 1e-3
    y = seg * np.clip(target / rms, 0.4, 8.0)
    return np.tanh(y * 1.6) / 1.6          # segura os picos sem achatar a voz
burn = [level(x) for x in burn]; mana = [level(x) for x in mana]
order = []
if EPI.get('ordem_livre'):      # Ep. 10 (11/11/2026): segue a ordem das falas do episode.json (duas falas seguidas do mesmo personagem)
    nk = {'B': 0, 'M': 0}; seg_ = {'B': burn, 'M': mana}
    for f in EPI['falas']:
        q = f['quem']; order.append((q, seg_[q][nk[q]], TEXT[q][nk[q]])); nk[q] += 1
else:
    for k in range(len(TEXT['B'])):
        order.append(('B', burn[k], TEXT['B'][k])); order.append(('M', mana[k], TEXT['M'][k]))
LOOP = EPI.get('loop')          # {"apos": fala da pancada (0-based), "quebra": s antes do fim dessa fala em que a música para,
                                #  "gap_pos": silêncio entre a pancada e a fala seguinte, "silencio": s de pancada antes do silêncio, "cauda": s no fim}

t = 0.35; lines = []; T_SLAM = None
for i, (who, seg, txt) in enumerate(order):
    if i: t = lines[-1]['start'] + lines[-1]['dur'] + GAP[i]
    if LOOP and i == LOOP['apos'] + 1:          # a pancada cai depois da fala "apos"; as falas seguintes ficam no silêncio
        L_ = lines[LOOP['apos']]; COMENTA = L_['start'] + L_['dur'] - LOOP.get('quebra', 1.0)
        T_SLAM = trilha.slam_time(MUSIC, COMENTA); t = max(t, T_SLAM + LOOP.get('gap_pos', 0.35))
    dur = len(seg) / SR
    hop = SR // 12; e = np.array([np.sqrt((seg[j:j + hop] ** 2).mean()) for j in range(0, len(seg) - hop // 2, hop)])
    e = np.clip(e / (np.percentile(e, 90) + 1e-6), 0, 1)
    lines.append(dict(who=who, text=txt, start=round(t, 3), dur=round(dur, 3), env=[round(float(v), 2) for v in e]))
    print(f'{i+1:2d} {who} {t:6.2f}s +{dur:4.2f}s  {txt}')

last = lines[-1]
if LOOP:
    assert T_SLAM is not None and lines[LOOP['apos']]['start'] + lines[LOOP['apos']]['dur'] < T_SLAM - 0.05, 'a fala da pancada passou da pancada'
else:
    COMENTA = last['start']
    T_SLAM = trilha.slam_time(MUSIC, COMENTA)
    assert last['start'] + last['dur'] < T_SLAM - 0.05, 'o "Comenta aí" passou da pancada'
OUTRO = EPI.get('outro', {})
T_SCAN = round(T_SLAM + 0.44, 3) if OUTRO.get('scanner') else None   # bloco do scanner logo depois que a TV apaga
SCAN_DUR = OUTRO.get('scanner') or 0
T_END = round(T_SLAM + 2.0 + SCAN_DUR + (OUTRO.get('hold') or 0), 2)
if LOOP: T_END = round(last['start'] + last['dur'] + LOOP.get('cauda', 0.12), 2)   # corte seco para o início
T_OFF = None
if LOOP and LOOP.get('desliga'):   # imagem apaga no fim (fecho do scanner a seguir)
    T_OFF = round(last['start'] + last['dur'] + LOOP['desliga'], 3); T_END = round(T_OFF + 0.70, 2)   # hold: mais tempo para ler a assinatura

# ---------- eventos: os mesmos horários para a imagem (data.js) e para o som ----------
js = open('episode.js', encoding='utf-8').read()
POSES = re.findall(r"\[\s*'([^']*)',\s*'([^']*)',\s*'([^']*)',\s*'([^']*)',\s*'([^']*)',\s*'([^']*)',\s*'([^']*)'\s*\]", js)
shots = [p[6] for p in POSES]
TVS = ('tv', 'tvtext', 'tvtext2', 'tv2')
# zapping: canais novos (de: N = fala N, contando do zero) e o zapping rápido da abertura
DES = [int(x) for x in re.findall(r"\bde:\s*(\d+)", js)]
FLIP = re.search(r"flip_a_cada:\s*([\d.]+)", js)
zaps = [lines[d]['start'] for d in DES if 0 < d < len(lines)]
zaps_leves = []
if FLIP and len(lines) > 1:
    ev_ = float(FLIP.group(1)); k = 1
    while k * ev_ < lines[1]['start'] - 0.15: zaps_leves.append(round(k * ev_, 3)); k += 1
cuts = [lines[k]['start'] for k in range(len(lines)) if shots[k] in TVS and (k == 0 or shots[k - 1] not in TVS)]
cuts = [c for c in cuts if c > 0.2 and all(abs(c - z) > 0.2 for z in zaps)]   # o zap já tem a sua estática
HL = set(re.findall(r"\b(tvtext2?)\s*:\s*\{\s*rects", js))
destaques = [round(lines[k]['start'] + 0.45, 3) for k in range(len(lines)) if shots[k] in HL]   # quando o amarelo acende
SIGLAS = re.compile(r'\b(?:EDHREC|cEDH|EDH|MTG|TV|SAL|US|PNG)\b')
def raivoso(k):   # Burn com os braços para cima, com "?!" ou com palavra em caixa alta
    l = lines[k]; txt = SIGLAS.sub('', l['text'].replace('*', ''))
    return l['who'] == 'B' and (POSES[k][0] == 'arms_up' or '?!' in txt or bool(re.search(r'\b[A-ZÀ-Ý]{3,}\b', txt)))
raiva = [lines[k]['start'] for k in range(len(lines)) if raivoso(k)]
# cartas citadas: só entram (com o som) as que têm PNG em cards/, na ordem de EP.inserts
ins_files = re.findall(r"file:\s*'([^']+)'", js)
INS = [tuple(x) for k, x in enumerate(EPI.get('ins', [])) if k < len(ins_files) and os.path.exists(ins_files[k])]
ins_t = [round(lines[k]['start'] + lines[k]['dur'] * a, 3) for k, a in INS]
sh = next((l['start'] + l['dur'] * 0.6 for l in lines if 'embaralh' in l['text']), None)
EV = dict(cortes_tv=cuts, destaque=destaques, raiva=raiva, cartas=ins_t, zaps=zaps, zaps_leves=zaps_leves)
open('data.js', 'w').write('const DATA=' + json.dumps(dict(lines=lines, T_SLAM=round(T_SLAM, 3), T_END=T_END, T_SCAN=T_SCAN, SCAN_DUR=SCAN_DUR, ev=EV), ensure_ascii=False) + ';')

# ---------- mixagem ----------
n = int(T_END * SR)
voice = np.zeros(n, np.float32)
for l, (_, seg, _) in zip(lines, order):
    a = int(l['start'] * SR); voice[a:a + len(seg)] += seg[:max(0, n - a)]
voice /= np.max(np.abs(voice)) + 1e-9; voice *= 0.85
m, mdesc = trilha.bed(MUSIC, COMENTA, T_SLAM, T_END, SR)
tt = np.arange(n) / SR
MIX = EPI.get('mix')
REF = 0.42                                       # 0 dB da música = o volume da abertura
if MIX:
    # ducking em dB: abertura e fecho em intro_db/fecho_db; nas falas fala_db; nas pausas pausa_db.
    # Desce rápido (40 ms) quando alguém fala e sobe devagar (300 ms) na pausa, para a música não "bombear".
    CR = 100; tc = np.arange(int(T_END * CR) + 1) / CR
    w = int(0.05 * SR); env = np.convolve(np.abs(voice), np.ones(w) / w, 'same')
    envc = np.interp(tc, tt, env); ref = np.percentile(envc[envc > 1e-4], 70) if (envc > 1e-4).any() else 1
    act = np.clip((envc / ref - 0.12) / 0.3, 0, 1)                                   # 1 = alguém falando
    tgt = MIX.get('pausa_db', -6) + (MIX.get('fala_db', -14) - MIX.get('pausa_db', -6)) * act
    tgt[tc < lines[0]['start']] = MIX.get('intro_db', 0)
    gdb = np.empty_like(tgt); gdb[0] = tgt[0]
    aa, ar = 1 - np.exp(-1 / (CR * 0.04)), 1 - np.exp(-1 / (CR * 0.30))
    for i in range(1, len(tc)):
        gdb[i] = gdb[i - 1] + (aa if tgt[i] < gdb[i - 1] else ar) * (tgt[i] - gdb[i - 1])
    gdb[tc >= T_SLAM] = MIX.get('fecho_db', 0)                                      # a pancada entra cheia
    g = REF * 10 ** (np.interp(tt, tc, gdb) / 20)
    mdesc += f" · ducking: intro {MIX.get('intro_db', 0)} dB, falas {MIX.get('fala_db', -14)} dB, pausas {MIX.get('pausa_db', -6)} dB, fecho {MIX.get('fecho_db', 0)} dB"
else:
    env = np.convolve(np.abs(voice), np.ones(int(0.12 * SR)) / int(0.12 * SR), 'same')
    duck = 1 - 0.40 * np.clip(env / (np.percentile(env, 95) + 1e-9), 0, 1)
    g = 0.125 * duck
    op = np.clip((lines[0]['start'] - tt) / 0.25, 0, 1); g = g * (1 - op) + REF * op
    up = np.clip((tt - T_SLAM) / 0.2, 0, 1); g = g * (1 - up) + 0.62 * up
if LOOP:     # sem fade no fim (loop); depois da pancada, silêncio seco
    g *= np.clip(tt / 0.15, 0, 1) * np.clip((T_SLAM + LOOP.get('silencio', 0.5) - tt) / 0.12, 0, 1)
else:
    g *= np.clip(tt / 0.15, 0, 1) * np.clip((T_END - tt) / 0.45, 0, 1)
import sfx
SFX = EPI.get('sfx', {})
fxt = sfx.track(n, SR, lines, T_SLAM, ins_t, cuts, sh,
                destaques=destaques if SFX.get('destaque') else (), raiva=raiva if SFX.get('raiva') else (),
                carta=SFX.get('carta', 'pop'), tv=SFX.get('tv', True), zaps=zaps, zaps_leves=zaps_leves)
if T_OFF is not None:
    co_ = sfx.crt_off(SR); a_ = int(T_OFF * SR); fxt[a_:a_ + len(co_)] += co_[:max(0, n - a_), None] if co_.ndim == 1 else co_[:max(0, n - a_)]
mix = m * g[:, None] + voice[:, None] + fxt
mix /= np.max(np.abs(mix)) * 1.05
with wave.open('_mix.wav', 'wb') as o:
    o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR); o.writeframes((mix * 32767).astype('<i2').tobytes())
np.save('_ganho_musica.npy', np.interp(np.arange(0, T_END, 0.01), tt, g).astype(np.float32))   # para o teste do ducking
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', '_mix.wav', '-af', 'loudnorm=I=-14:TP=-1:LRA=11', '-ar', str(SR), 'trilha_final.wav'], check=True)
print('eventos: ' + ', '.join(f'{k} {len(v)}' for k, v in EV.items()) + (f' · scanner em {T_SCAN}s' if T_SCAN else ''))
print(f'{mdesc} · pancada (TV desliga) em {T_SLAM:.2f}s · fim {T_END}s')
