"""Especial Picard v2 (celebração) · Mana & Burn
Corta as faixas (pausas reais da voz), monta o bate-volta, gera data.js e trilha_final.wav (-14 LUFS).
uso: python3 processar2.py vozes/burn.mp3 vozes/mana.mp3
"""
import sys, json, subprocess, wave
import numpy as np
import musica2

SR = 44100
G = json.load(open('guiao.json', encoding='utf-8'))['falas']

def load(p):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '_v.wav'], check=True)
    w = wave.open('_v.wav'); return np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float32) / 32768
def rms(x, hop): return np.sqrt(np.convolve(x ** 2, np.ones(hop) / hop, 'same'))
def split(x, n):
    """divide nas n-1 pausas mais longas (>= 0,45 s)"""
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
    cuts = [0] + [((a + b) // 2) * int(.01 * SR) for _, a, b in gaps] + [len(x)]
    return [apara(x[cuts[k]:cuts[k + 1]]) for k in range(n)]
def apara(s):
    e = rms(s, int(.01 * SR)); thr = max(.004, e.max() * .05); idx = np.where(e > thr)[0]
    a = max(0, idx[0] - int(.03 * SR)); b = min(len(s), idx[-1] + int(.06 * SR)); s = s[a:b].copy()
    f = int(.008 * SR); s[:f] *= np.linspace(0, 1, f); s[-f:] *= np.linspace(1, 0, f); return s
def encurta(seg, mx):   # silêncios internos no máximo mx (corte seco de edição)
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
TEMPO = {'B': 1.04, 'M': 1.06}
RESPIRO = {12: .75, 15: .38}   # índice da fala (0 = primeira): pausa dramática do banimento e a fala do Sir Patrick
segs = []; ib = im = 0
for n_, f in enumerate(G):
    s = B[ib] if f['quem'] == 'B' else M[im]
    if f['quem'] == 'B': ib += 1
    else: im += 1
    segs.append(nivela(tempo(encurta(s, RESPIRO.get(n_, .22)), TEMPO[f['quem']])))
    if n_ == 12:   # "Isso... NÃO devia ser banido": meio segundo de suspense depois do "Isso"
        x = segs[-1]; e = rms(x, int(.02 * SR)); a0, a1 = int(.25 * SR), int(.9 * SR)
        c = a0 + int(np.argmin(e[a0:a1])); segs[-1] = np.concatenate([x[:c], np.zeros(int(.5 * SR), np.float32), x[c:]])
        print(f'   suspense: +0,5 s em {c / SR:.2f}s da fala 13')

# ---- direção: plano, braços (Burn, Mana), olhar, sobrancelhas, TV, texto de ecrã, folga antes da fala ----
D = [
 dict(shot='tv',     pB='point_tv', pM='rest',   lB='screen', lM='tv',    bB='up',     bM='flat', tela='carta', gap=0),     # 1 gancho
 dict(shot='cuM',    pB='rest',     pM='rest',   lB='other',  lM='cam',   bB='normal', bM='up',   tela='carta', ovl='data', gap=.14),
 dict(shot='wide',   pB='arms_up',  pM='rest',   lB='cam',    lM='other', bB='up',     bM='flat', tela='carta', ovl='makeitso', gap=.12),
 dict(shot='cuM',    pB='rest',     pM='finger', lB='other',  lM='cam',   bB='normal', bM='up',   tela='carta', ovl='cha', gap=.16),
 dict(shot='cuB',    pB='rest',     pM='rest',   lB='cam',    lM='other', bB='up',     bM='flat', tela='carta', gap=.10),   # "Veio refrigerante" (a lata na mão)
 dict(shot='push',   pB='rest',     pM='finger', lB='other',  lM='other', bB='normal', bM='flat', tela='carta', gap=.35),
 dict(shot='cuB',    pB='point_cam',pM='rest',   lB='cam',    lM='other', bB='angry',  bM='flat', tela='carta', gap=.10),
 dict(shot='tvtext', pB='rest',     pM='rest',   lB='screen', lM='tv',    bB='normal', bM='flat', tela='carta', hl=True, gap=.25),  # Lê a carta
 dict(shot='tvtext', pB='rest',     pM='rest',   lB='screen', lM='tv',    bB='up',     bM='flat', tela='carta', hl=True, gap=.10),
 dict(shot='wide',   pB='rest',     pM='finger', lB='other',  lM='other', bB='normal', bM='up',   tela='carta', gap=.18),
 dict(shot='cuB',    pB='rest',     pM='rest',   lB='cam',    lM='other', bB='normal', bM='flat', tela='carta', gap=.45),  # "Vou fazer uma coisa..."
 dict(shot='cuM',    pB='rest',     pM='chip',   lB='other',  lM='other', bB='normal', bM='flat', tela='carta', gap=.30),  # "Pagar a pizza?"
 dict(shot='tv',     pB='point_tv', pM='rest',   lB='screen', lM='tv',    bB='normal', bM='flat', tela='lista', gap=.85),  # O BANIMENTO QUE NÃO ACONTECE
 dict(shot='wide',   pB='rest',     pM='finger', lB='other',  lM='other', bB='normal', bM='up',   tela='lista', gap=.55),
 dict(shot='push',   pB='arms_up',  pM='rest',   lB='cam',    lM='other', bB='up',     bM='flat', tela='carta', ovl='numeros', gap=.20),
 dict(shot='tv2',    pB='rest',     pM='rest',   lB='screen', lM='tv',    bB='normal', bM='flat', tela='nome', gap=.40),   # Sir Patrick
 dict(shot='cuB',    pB='point_cam',pM='rest',   lB='cam',    lM='other', bB='normal', bM='flat', tela='nome', gap=.40),
 dict(shot='cuM',    pB='rest',     pM='rest',   lB='other',  lM='cam',   bB='normal', bM='up',   tela='nome', gap=.20),
 dict(shot='wide',   pB='point_tv', pM='rest',   lB='tv',     lM='tv',    bB='up',     bM='flat', tela='carta', gap=.30),  # "Engage."
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
T_SLAM = round(ult['start'] + ult['dur'] + .15, 3)   # o "Engage" dispara a TV
T_END = round(T_SLAM + 2.9, 2)
print(f'Engage/TV desliga em {T_SLAM}s · fim {T_END}s')
open('data.js', 'w').write('const DATA=' + json.dumps(dict(lines=lines, T_SLAM=T_SLAM, T_END=T_END), ensure_ascii=False) + ';')

# ---- mixagem ----
n = int(T_END * SR); voz = np.zeros(n, np.float32)
for l, s in zip(lines, segs):
    a = int(l['start'] * SR); voz[a:a + len(s)] += s[: max(0, n - a)]
mk = dict(t_ban=lines[12]['start'] - .55, t_ban_fim=lines[13]['start'] + .2, t_swell=lines[14]['start'] - .1,
          t_calma=lines[15]['start'] - .2, t_calma_fim=lines[16]['start'] + lines[16]['dur'], t_engage=ult['start'] + .05)
mus = musica2.trilha(T_END, mk, SR)
tt = np.arange(n) / SR
env = np.convolve(np.abs(voz), np.ones(int(.06 * SR)) / int(.06 * SR), 'same')
act = np.clip(env / (np.percentile(env[env > 1e-4], 60) + 1e-9), 0, 1)
CR = 100; tc = np.arange(int(T_END * CR) + 1) / CR
alvo = -13 + 7 * (1 - np.interp(tc, tt, act)); alvo[tc < lines[0]['start']] = 0; alvo[tc >= ult['start']] = 0
g = np.empty_like(alvo); g[0] = alvo[0]; aa, ar = 1 - np.exp(-1 / (CR * .04)), 1 - np.exp(-1 / (CR * .35))
for i in range(1, len(tc)): g[i] = g[i - 1] + (aa if alvo[i] < g[i - 1] else ar) * (alvo[i] - g[i - 1])
gm = .34 * 10 ** (np.interp(tt, tc, g) / 20)
fx = np.zeros(n)
def put(t0, s, v):
    a = int(t0 * SR); e = min(n, a + len(s)); fx[a:e] += s[: e - a] * v
k = np.arange(int(.35 * SR)); rng = np.random.default_rng(5)
carimbo = (rng.standard_normal(len(k)) * np.exp(-k / (.015 * SR)) + np.sin(2 * np.pi * 90 * k / SR) * np.exp(-k / (.06 * SR)))
put(lines[12]['start'] + lines[12]['dur'] * .78, carimbo, .35)                    # carimbo "NUNCA" na lista
w = np.arange(int(.9 * SR)); f0 = 180 + 1400 * (w / len(w)) ** 2                  # "Engage": arrancada (sobe, sem imitar efeitos da série)
put(T_SLAM + .05, np.sin(2 * np.pi * np.cumsum(f0) / SR) * np.sin(np.pi * w / len(w)) ** 2 * .5 + rng.standard_normal(len(w)) * .05 * np.sin(np.pi * w / len(w)), .22)
mix = mus * gm[:, None] + voz[:, None] * .9 + fx[:, None]
mix /= np.max(np.abs(mix)) * 1.05
with wave.open('_mix.wav', 'wb') as o:
    o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR); o.writeframes((mix * 32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', '_mix.wav', '-af', 'loudnorm=I=-13.4:TP=-3:LRA=11,alimiter=limit=0.70:attack=2:release=60:level=false', '-ar', '48000', 'trilha_final.wav'], check=True)
print('ok: data.js e trilha_final.wav')
