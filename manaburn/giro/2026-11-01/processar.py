"""TV SAL · Giro de Domingo · Mana & Burn
Corta as duas faixas do ElevenLabs nas pausas, monta o bate-volta, gera data.js e trilha_final.wav (-14 LUFS).
Base: manaburn/episodios/esp02_picard_v2/processar2.py (cortes, respiro, ritmo, nivelamento, ducking).
Música: manaburn/musica.mp3 ("midnight_throttle"), com a parada seca (125,05 s) no "Comenta aí" e a pancada (126,30 s) a desligar a TV,
como nos Ep. 1 e 2. Bloco 1 (luto): música quase em silêncio e sem efeitos.
uso: python3 processar.py vozes/burn.mp3 vozes/mana.mp3
"""
import sys, json, subprocess, wave, os
import numpy as np

SR = 44100
G = json.load(open('guiao.json', encoding='utf-8'))['falas']
MUSICA = os.environ.get('MUSICA', '../../musica.mp3')
BREAK, SLAM = 125.05, 126.30          # parada seca e pancada na faixa
FECHO = 0.52 + 3.87                   # do desligar da TV até ao fim do fecho do scanner (juntar_fecho.py)

def load(p):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '_v.wav'], check=True)
    w = wave.open('_v.wav'); return np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float32) / 32768
def rms(x, hop): return np.sqrt(np.convolve(x ** 2, np.ones(hop) / hop, 'same'))
def split(x, n):
    e = rms(x, int(.01 * SR))[::int(.01 * SR)]; thr = max(.004, np.percentile(e, 95) * .04); v = e > thr
    gaps = []; i = 0
    while i < len(v):
        if not v[i]:
            j = i
            while j < len(v) and not v[j]: j += 1
            if i > 0 and j < len(v): gaps.append((j - i, i, j))
            i = j
        else: i += 1
    gaps = sorted(sorted(gaps, reverse=True)[: n - 1], key=lambda g: g[1])
    assert len(gaps) == n - 1, (len(gaps), n)
    print('   pausas usadas (s):', [round(g[0] * .01, 2) for g in gaps])
    cuts = [0] + [((a + b) // 2) * int(.01 * SR) for _, a, b in gaps] + [len(x)]
    return [apara(x[cuts[k]:cuts[k + 1]]) for k in range(n)]
def apara(s):
    e = rms(s, int(.01 * SR)); thr = max(.004, e.max() * .05); idx = np.where(e > thr)[0]
    a = max(0, idx[0] - int(.03 * SR)); b = min(len(s), idx[-1] + int(.06 * SR)); s = s[a:b].copy()
    f = int(.008 * SR); s[:f] *= np.linspace(0, 1, f); s[-f:] *= np.linspace(1, 0, f); return s
def encurta(seg, mx):
    hop = int(.01 * SR); fr = rms(seg, hop)[::hop]; thr = max(.008, np.percentile(fr, 95) * .05); v = fr > thr
    idx = np.where(v)[0]; out = []; pos = 0; i = idx[0]; keep = int(mx / .01); xf = int(.008 * SR)
    while i < idx[-1]:
        if not v[i]:
            j = i
            while j < idx[-1] and not v[j]: j += 1
            if j - i > keep + 4:
                a = (i + keep // 2) * hop; b = (j - keep // 2) * hop; head = seg[pos:a].copy(); tail = seg[b:b + xf].copy()
                if len(head) > xf and len(tail) == xf:
                    head[-xf:] = head[-xf:] * np.linspace(1, 0, xf) + tail * np.linspace(0, 1, xf); out.append(head); pos = b + xf
            i = j
        else: i += 1
    out.append(seg[pos:]); return np.concatenate(out)
def tempo(seg, f):
    if abs(f - 1) < .005: return seg
    with wave.open('_s.wav', 'wb') as o:
        o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR); o.writeframes((np.clip(seg, -1, 1) * 32767).astype('<i2').tobytes())
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', '_s.wav', '-af', f'atempo={f}', '-ar', str(SR), '_s2.wav'], check=True)
    w = wave.open('_s2.wav'); return np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float32) / 32768
def nivela(seg, alvo=.11):
    e = rms(seg, int(.02 * SR)); act = e > max(.01, e.max() * .12); r = np.sqrt((seg[act] ** 2).mean()) if act.any() else 1e-3
    return np.tanh(seg * np.clip(alvo / r, .4, 8) * 1.5) / 1.5

B = split(load(sys.argv[1]), sum(f['quem'] == 'B' for f in G))
M = split(load(sys.argv[2]), sum(f['quem'] == 'M' for f in G))
TEMPO = {'B': 1.06, 'M': 1.10}
TEMPO_FALA = {1: 1.0, 2: 1.0, 3: 1.02}     # bloco 1 (luto): Mana no ritmo natural, Burn quase natural
RESPIRO = {1: .30, 2: .22, 10: .20}        # pausas internas máximas por fala (0 = primeira); padrão 0,14
segs = []; ib = im = 0
for n_, f in enumerate(G):
    s = B[ib] if f['quem'] == 'B' else M[im]
    if f['quem'] == 'B': ib += 1
    else: im += 1
    segs.append(nivela(tempo(encurta(s, RESPIRO.get(n_, .14)), TEMPO_FALA.get(n_, TEMPO[f['quem']]))))

# ---- direção: plano, braços (Burn, Mana), olhar, sobrancelhas, tela da TV, faixa, folga antes da fala ----
D = [
 dict(shot='tv',   pB='point_tv', pM='rest',   lB='screen', lM='tv',    bB='up',     bM='flat', tela='abre',   ovl='manchete', gap=0),   # 1 abre
 dict(shot='tv',   pB='rest',     pM='rest',   lB='screen', lM='tv',    bB='normal', bM='flat', tela='n1',     faixa='n1', gap=.20),     # 2 notícia 1
 dict(shot='cuB',  pB='rest',     pM='rest',   lB='cam',    lM='other', bB='angry',  bM='flat', tela='n1',     faixa='n1', gap=.30),
 dict(shot='cuM',  pB='rest',     pM='rest',   lB='other',  lM='cam',   bB='normal', bM='flat', tela='n1',     faixa='n1', gap=.25),
 dict(shot='tv',   pB='point_tv', pM='rest',   lB='screen', lM='tv',    bB='up',     bM='flat', tela='n2',     faixa='n2', gap=.55),     # 5 notícia 2 (respiro depois do luto)
 dict(shot='cuM',  pB='rest',     pM='finger', lB='other',  lM='cam',   bB='normal', bM='up',   tela='n2',     faixa='n2', gap=.12),
 dict(shot='cuB',  pB='arms_up',  pM='rest',   lB='cam',    lM='other', bB='up',     bM='flat', tela='n2',     faixa='n2', gap=.10),
 dict(shot='tv',   pB='rest',     pM='rest',   lB='screen', lM='tv',    bB='normal', bM='flat', tela='n3',     faixa='n3', gap=.22),     # 8 notícia 3
 dict(shot='wide', pB='shrug',    pM='rest',   lB='other',  lM='tv',    bB='up',     bM='flat', tela='n3',     faixa='n3', gap=.10),
 dict(shot='tvtext', pB='rest',   pM='finger', lB='screen', lM='tv',    bB='normal', bM='flat', tela='n3',     faixa='n3', hl=1, gap=.12),
 dict(shot='cuB',  pB='arms_up',  pM='rest',   lB='cam',    lM='other', bB='angry',  bM='flat', tela='n3',     faixa='n3', gap=.08),
 dict(shot='tv',   pB='rest',     pM='chip',   lB='screen', lM='tv',    bB='normal', bM='flat', tela='agenda', gap=.16),                 # 12 agenda
 dict(shot='cuB',  pB='point_cam',pM='rest',   lB='cam',    lM='other', bB='up',     bM='flat', tela='agenda', faixa='voto', gap=.14),
 dict(shot='cuM',  pB='rest',     pM='remote', lB='other',  lM='cam',   bB='normal', bM='up',   tela='agenda', faixa='voto', gap=.16),
]
assert len(D) == len(G)
t = .5; lines = []
for k, (f, d, s) in enumerate(zip(G, D, segs)):
    if lines: t = lines[-1]['start'] + lines[-1]['dur'] + d['gap']
    hop = SR // 12; e = np.array([np.sqrt((s[j:j + hop] ** 2).mean()) for j in range(0, len(s) - hop // 2, hop)])
    e = np.clip(e / (np.percentile(e, 90) + 1e-6), 0, 1)
    lines.append(dict(who=f['quem'], text=f['legenda'], start=round(t, 3), dur=round(len(s) / SR, 3), env=[round(float(v), 2) for v in e], **{k2: v for k2, v in d.items() if k2 != 'gap'}))
    print(f"{k+1:2d} {f['quem']} {t:6.2f}s +{len(s)/SR:4.2f}s {d['shot']:6s} {f['legenda']}")
ult = lines[-1]
T_SLAM = round(ult['start'] + (SLAM - BREAK), 3)      # a pancada da música desliga a TV
T_END = round(T_SLAM + 1.0, 2)                        # o vídeo do kit; o fecho entra em T_SLAM + 0,52 (juntar_fecho.py)
print(f'Comenta aí em {ult["start"]}s · TV desliga em {T_SLAM}s · com fecho: {T_SLAM + FECHO - 7/30:.2f}s')
open('data.js', 'w').write('const DATA=' + json.dumps(dict(lines=lines, T_SLAM=T_SLAM, T_END=T_END), ensure_ascii=False) + ';')

# ---- mixagem (a trilha cobre também o fecho do scanner) ----
TOT = T_SLAM + FECHO + .2
n = int(TOT * SR); voz = np.zeros(n, np.float32)
for l, s in zip(lines, segs):
    a = int(l['start'] * SR); voz[a:a + len(s)] += s[: max(0, n - a)]
OFF = BREAK - ult['start']
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{OFF:.3f}', '-t', f'{TOT:.3f}', '-i', MUSICA, '-ac', '2', '-ar', str(SR), '-f', 's16le', '_mus.raw'], check=True)
mus = np.frombuffer(open('_mus.raw', 'rb').read(), '<i2').astype(np.float32).reshape(-1, 2) / 32768
mus = np.pad(mus, ((0, max(0, n - len(mus))), (0, 0)))[:n]
tt = np.arange(n) / SR
mus *= (np.clip(tt / .35, 0, 1) * np.clip((TOT - tt) / .6, 0, 1))[:, None]
mus = mus / (np.max(np.abs(mus)) + 1e-9) * .9
print(f'   música: {os.path.basename(MUSICA)} de {OFF:.1f}s a {OFF + TOT:.1f}s (parada no "Comenta aí")')
env = np.convolve(np.abs(voz), np.ones(int(.06 * SR)) / int(.06 * SR), 'same')
act = np.clip(env / (np.percentile(env[env > 1e-4], 60) + 1e-9), 0, 1)
CR = 100; tc = np.arange(int(TOT * CR) + 1) / CR
alvo = -14 + 8 * (1 - np.interp(tc, tt, act)); alvo[tc < lines[0]['start']] = 0; alvo[tc >= T_SLAM] = 0
luto0, luto1 = lines[1]['start'] - .25, lines[4]['start'] - .15
alvo[(tc >= luto0) & (tc < luto1)] = -30                     # bloco 1: música quase muda
g = np.empty_like(alvo); g[0] = alvo[0]; aa, ar = 1 - np.exp(-1 / (CR * .04)), 1 - np.exp(-1 / (CR * .35))
for i in range(1, len(tc)): g[i] = g[i - 1] + (aa if alvo[i] < g[i - 1] else ar) * (alvo[i] - g[i - 1])
gm = .34 * 10 ** (np.interp(tt, tc, g) / 20)
mix = mus * gm[:, None] + voz[:, None] * .9
mix /= np.max(np.abs(mix)) * 1.05
with wave.open('_mix.wav', 'wb') as o:
    o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR); o.writeframes((mix * 32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', '_mix.wav', '-af', 'loudnorm=I=-13.6:TP=-2.5:LRA=11,alimiter=limit=0.72:attack=2:release=60:level=false', '-ar', '48000', 'trilha_final.wav'], check=True)
for f in ['_v.wav', '_s.wav', '_s2.wav', '_mus.raw', '_mix.wav']:
    if os.path.exists(f): os.remove(f)
print('ok: data.js e trilha_final.wav')
