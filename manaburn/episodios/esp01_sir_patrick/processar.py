"""Especial Mana & Burn · Obrigado, Sir Patrick
Corta a faixa do Mana (8 falas) e a do Burn (1 fala), divide as falas longas em blocos de legenda
nas pausas reais da voz, monta a linha do tempo calma, gera data.js e trilha_final.wav (-14 LUFS).
uso: python3 processar.py vozes/mana.mp3 vozes/burn.mp3
"""
import sys, json, subprocess, wave
import numpy as np
import musica

SR = 44100
def load(p):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '_v.wav'], check=True)
    w = wave.open('_v.wav'); return np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float32) / 32768

def rms(x, hop):
    return np.sqrt(np.convolve(x ** 2, np.ones(hop) / hop, 'same'))

def apara(seg, thr_rel=0.06):
    """tira o silêncio do começo e do fim (deixa 40 ms de respiro)"""
    e = rms(seg, int(0.01 * SR)); thr = max(0.004, e.max() * thr_rel); v = np.where(e > thr)[0]
    if not len(v): return seg
    a = max(0, v[0] - int(0.04 * SR)); b = min(len(seg), v[-1] + int(0.06 * SR))
    s = seg[a:b].copy(); f = int(0.01 * SR); s[:f] *= np.linspace(0, 1, f); s[-f:] *= np.linspace(1, 0, f)
    return s

def vale(x, t, janela=0.3):
    """ponto de menor energia perto de t (para cortar entre palavras)"""
    a, b = int((t - janela) * SR), int((t + janela) * SR); e = rms(x[a:b], int(0.02 * SR))
    return (a + int(np.argmin(e))) / SR

mana, burn = load(sys.argv[1]), load(sys.argv[2])

# ---- falas do Mana na faixa original (pausas medidas com silencedetect -38 dB) ----
# cada fala: lista de blocos (texto da legenda, início, fim) em segundos da faixa
P = lambda t: vale(mana, t)
M = [
  [("Tem uma carta do *Jean-Luc Picard* prestes a chegar no Magic.", 0.00, 3.50),
   ("E hoje, ela ganhou outro significado.", 3.90, 6.75)],
  [("*Sir Patrick Stewart* morreu aos 86 anos.", 8.35, 11.40)],
  [("Foi a presença dele que deu ao capitão", 12.50, None),
   ("essa combinação rara de *inteligência, firmeza e humanidade*.", None, 18.75)],
  [("Picard não liderava só porque tinha a patente.", 19.60, 22.20),
   ("Liderava porque sabia *ouvir, pensar*", 22.55, 25.25),
   ("e escolher a palavra antes da força.", 25.50, 27.75)],
  [("Em *13 de novembro*, Jean-Luc Picard, Luminary,", 28.60, None),
   ("chega oficialmente a Magic: The Gathering | Star Trek.", None, 35.10)],
  [("Mas o que fica de Patrick Stewart *não cabe numa carta*,", 35.70, None),
   ("nem se mede por raridade.", None, 40.60)],
  [("Fica nas histórias que atravessam gerações.", 41.15, 43.80),
   ("E na ideia de que *a força também pode ser serena*.", 44.60, 47.90)],
  [("Qual memória do Picard você leva com você?", 48.75, len(mana) / SR)],
]
# cortes proporcionais (sem pausa audível): pelo número de sílabas aproximado, encostado no vale de energia
def sil(t): return sum(t.lower().count(v) for v in 'aeiouáéíóúâêôãõ')
for fala in M:
    for k in range(len(fala) - 1):
        if fala[k][2] is None:
            a, b = fala[k][1], fala[k + 1][2]; fr = sil(fala[k][0]) / (sil(fala[k][0]) + sil(fala[k + 1][0]))
            c = P(a + (b - a) * fr)
            fala[k] = (fala[k][0], a, c); fala[k + 1] = (fala[k + 1][0], c, b)

# ---- direção por bloco: plano, o que a TV mostra, texto extra na tela ----
# plano: tv (TV em primeiro plano), tv2 (TV mais perto da carta), wide, cuM, cuB, pull (afasta devagar)
DIR = [
  dict(shot='tv',   tela='revela'),
  dict(shot='tv',   tela='carta'),
  dict(shot='tv',   tela='nome'),
  dict(shot='wide', tela='nome'),
  dict(shot='wide', tela='nome', ovl='virtudes'),
  dict(shot='cuM',  tela='carta'),
  dict(shot='cuB',  tela='carta'),
  dict(shot='wide', tela='carta'),
  dict(shot='tv2',  tela='carta', ovl='data'),
  dict(shot='tv2',  tela='carta', ovl='data'),
  dict(shot='tv',   tela='apaga'),
  dict(shot='tv',   tela='frase'),
  dict(shot='pull', tela='frase'),
  dict(shot='cuM',  tela='frase'),
  dict(shot='cuB',  tela='frase'),          # Burn: "Obrigado, Sir Patrick."
  dict(shot='tv',   tela='obrigado'),       # Mana: a pergunta
]
GAP_LINHA = [0, 0.75, 0.9, 0.55, 0.8, 0.9, 0.45, 1.1]   # pausa antes de cada fala do Mana (nas falas 2..8)
GAP_BLOCO = 0.32                                          # pausa entre blocos da mesma fala
GAP_BURN, GAP_DEPOIS_BURN = 1.0, 0.9

blocos = []   # (quem, texto, áudio)
for i, fala in enumerate(M):
    if i == 7:
        blocos.append(('B', 'Obrigado, *Sir Patrick*.', apara(burn), GAP_BURN))
    for k, (txt, a, b) in enumerate(fala):
        g = (GAP_LINHA[i] if k == 0 else GAP_BLOCO) if (i or k) else 0
        if i == 7 and k == 0: g = GAP_DEPOIS_BURN
        blocos.append(('M', txt, apara(mana[int(a * SR):int(b * SR)]), g))
assert len(blocos) == len(DIR), (len(blocos), len(DIR))

def nivela(seg, alvo=0.10):
    e = rms(seg, int(0.02 * SR)); act = e > max(0.01, e.max() * 0.12)
    r = np.sqrt((seg[act] ** 2).mean()) if act.any() else 1e-3
    return np.tanh(seg * np.clip(alvo / r, 0.4, 6) * 1.4) / 1.4

T0 = 0.55; t = T0; lines = []
for (quem, txt, seg, g), d in zip(blocos, DIR):
    seg = nivela(seg, 0.085 if quem == 'B' else 0.10)       # o Burn fala baixo de propósito
    if lines: t = lines[-1]['start'] + lines[-1]['dur'] + g
    hop = SR // 12; e = np.array([np.sqrt((seg[j:j + hop] ** 2).mean()) for j in range(0, len(seg) - hop // 2, hop)])
    e = np.clip(e / (np.percentile(e, 90) + 1e-6), 0, 1)
    lines.append(dict(who=quem, text=txt, start=round(t, 3), dur=round(len(seg) / SR, 3), env=[round(float(v), 2) for v in e], **d))
    lines[-1]['_seg'] = seg
    print(f"{len(lines):2d} {quem} {t:6.2f}s +{len(seg)/SR:4.2f}s  {d['shot']:5s} {d['tela']:9s} {txt}")

ult = lines[-1]
HOLD_PERGUNTA = 1.6                         # a pergunta fica na TV, legível, antes do clique
T_SLAM = round(ult['start'] + ult['dur'] + HOLD_PERGUNTA, 3)   # TV desliga
T_END = round(T_SLAM + 2.6, 2)              # ponto verde + assinatura BINDER Originals
print(f'TV desliga em {T_SLAM}s · fim {T_END}s')

segs = [l.pop('_seg') for l in lines]
open('data.js', 'w').write('const DATA=' + json.dumps(dict(lines=lines, T_SLAM=T_SLAM, T_END=T_END, ev={'cortes_tv': [], 'destaque': [], 'raiva': [], 'cartas': []}), ensure_ascii=False) + ';')

# ---- mixagem ----
n = int(T_END * SR); voz = np.zeros(n, np.float32)
for l, s in zip(lines, segs):
    a = int(l['start'] * SR); voz[a:a + len(s)] += s[: max(0, n - a)]
pico_a = lines[5]['start']; pico_b = lines[7]['start'] + lines[7]['dur']
mus = musica.trilha(T_END, pico_a, pico_b, t_res=T_SLAM - 0.2, sr=SR)
tt = np.arange(n) / SR
env = np.convolve(np.abs(voz), np.ones(int(0.08 * SR)) / int(0.08 * SR), 'same')
act = np.clip(env / (np.percentile(env[env > 1e-4], 60) + 1e-9), 0, 1)
CR = 100; tc = np.arange(int(T_END * CR) + 1) / CR
alvo = -15 + 9 * (1 - np.interp(tc, tt, act))              # -15 dB com voz, até -6 dB nas pausas
alvo[tc < lines[0]['start']] = -3; alvo[tc >= T_SLAM - 0.2] = 0
g = np.empty_like(alvo); g[0] = alvo[0]
aa, ar = 1 - np.exp(-1 / (CR * 0.08)), 1 - np.exp(-1 / (CR * 0.6))   # desce suave, sobe mais suave
for i in range(1, len(tc)): g[i] = g[i - 1] + (aa if alvo[i] < g[i - 1] else ar) * (alvo[i] - g[i - 1])
gm = 0.30 * 10 ** (np.interp(tt, tc, g) / 20)
# efeitos: só o clique do controle e a TV de tubo a apagar (baixos)
fx = np.zeros(n)
c = int((T_SLAM - 0.16) * SR); k = np.arange(int(0.012 * SR)); fx[c:c + len(k)] += 0.25 * np.sin(2 * np.pi * 2400 * k / SR) * np.exp(-k / (0.002 * SR))
a = int(T_SLAM * SR); k = np.arange(int(0.5 * SR)); f0 = 1500 * np.exp(-k / (0.12 * SR)) + 60
fx[a:a + len(k)] += 0.06 * np.sin(2 * np.pi * np.cumsum(f0) / SR) * np.exp(-k / (0.18 * SR))
mix = mus * gm[:, None] + voz[:, None] * 0.9 + fx[:, None]
mix /= np.max(np.abs(mix)) * 1.05
with wave.open('_mix.wav', 'wb') as o:
    o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR); o.writeframes((mix * 32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', '_mix.wav', '-af', 'loudnorm=I=-14:TP=-2.2:LRA=11', '-ar', '48000', 'trilha_final.wav'], check=True)
print('ok: data.js e trilha_final.wav')
