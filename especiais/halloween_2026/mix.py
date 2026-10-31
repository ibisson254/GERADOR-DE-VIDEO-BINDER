"""Trilha do especial: vozes (linhas/*.wav) + música + efeitos sintetizados, -14 LUFS, pico -1 dBTP.
Música: se existir musica/tema_especial.mp3 (a faixa original pedida ao ElevenLabs), usa-a do início ao fim
com parada seca no "Comenta aí". Senão, trilha TEMPORÁRIA com os temas das três séries (só para a PRÉVIA):
Conde (abertura → categoria 4), TUBO (categoria 5 → fim, com o silêncio da série depois do "Erro de sistema").
uso: python3 mix.py  -> trilha.wav
"""
import json, subprocess, pathlib, numpy as np
SR = 48000; KIT = '/root/repo/'
TL = json.load(open('tl.json')); C = {c['nome']: c for c in TL['cenas']}; FX = {f['id']: f for f in TL['falas']}
N = int(TL['TOTAL'] * SR) + SR
def load(p):
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
def at(buf, x, t, g=1.0):
    i = int(t * SR); j = min(len(buf), i + len(x))
    if j > i: buf[i:j] += x[:j - i] * g
voz = np.zeros(N, np.float32); speech = np.zeros(N, bool)
for f in TL['falas']:
    p = pathlib.Path(f'linhas/{f["id"]}.wav')
    if not p.exists(): continue
    x = load(str(p)); rms = np.sqrt((x ** 2).mean()) + 1e-9; x = x * (0.1 / rms)      # ~-20 dBFS RMS por fala
    at(voz, x, f['start']); i = int(f['start'] * SR); speech[i:i + len(x)] = True

# ---- música
mus = np.zeros(N, np.float32)
def fade(x, a=0.05, b=0.3):
    x = x.copy(); na, nb = int(a * SR), int(b * SR)
    if na: x[:na] *= np.linspace(0, 1, na)
    if nb: x[-nb:] *= np.linspace(1, 0, nb)
    return x
stop = FX['M7']['start']          # parada seca: o "Comenta aí" cai no silêncio
tema = pathlib.Path('musica/tema_especial.mp3')
if tema.exists():
    m = load(str(tema)); at(mus, fade(m[:int(stop * SR)], 0.02, 0.04), 0)
    resto = m[int(stop * SR):]; at(mus, fade(resto[:int((TL['TOTAL'] - TL['FIM_KIT'] + 0.4) * SR)], 0.05, 0.45), TL['FIM_KIT'] - 0.4)
    TEMP = False
else:
    TEMP = True
    conde = load(KIT + 'conde/musica/tema.mp3'); tubo = load(KIT + 'oraculo/musica/tubo_tema.mp3')
    a5 = C['cat5']['a']
    body = conde[:int(40.0 * SR)]; loop = conde[int(4.0 * SR):int(40.0 * SR)]
    seq = np.concatenate([body, loop, loop])[:int((a5 + 0.4) * SR)]
    at(mus, fade(seq, 0.4, 0.5), 0)
    off = FX['T7']['start'] + FX['T7']['dur'] + 0.05 - 29.0        # o silêncio do tema (29,0–30,2 s) segue a revelação
    s0 = max(0.0, a5 - off); seg = tubo[int(s0 * SR):int((stop - off) * SR)]
    at(mus, fade(seg, 0.3, 0.04), off + s0)
    back = tubo[int(30.2 * SR):]; dur_out = TL['TOTAL'] - TL['FIM_KIT'] + 0.4
    at(mus, fade(back[:int(dur_out * SR)], 0.05, 0.45), TL['FIM_KIT'] - 0.4)
# ducking: desce em 40 ms quando há voz, sobe em 300 ms
g_lo, g_hi = 0.12, 0.42; env = np.where(speech, g_lo, g_hi).astype(np.float32)
for f in TL['falas']:
    if f['previa']:     # PRÉVIA: sem voz, a música baixa só um pouco no lugar da fala
        i = int(f['start'] * SR); env[i:i + int(f['dur'] * SR)] = 0.24
env[int(TL['FIM_KIT'] * SR):] = 0.55
k_dn, k_up = 1 - np.exp(-1 / (0.04 * SR)), 1 - np.exp(-1 / (0.3 * SR)); sm = np.empty_like(env); v = env[0]
for i in range(0, N, 64):
    tgt = env[i]; k = k_dn if tgt < v else k_up; v += (tgt - v) * (1 - (1 - k) ** 64); sm[i:i + 64] = v
mus *= sm

# ---- efeitos
rng = np.random.default_rng(3); sfx = np.zeros(N, np.float32)
def t_(d): return np.arange(int(d * SR)) / SR
def noise(d): return rng.standard_normal(int(d * SR)).astype(np.float32)
def lp(x, a): y = np.empty_like(x); v = 0.0
def onepole(x, a):
    y = np.empty_like(x); v = 0.0
    for i in range(len(x)): v += a * (x[i] - v); y[i] = v
    return y
def tum():   # desmagnetização do CRT
    t = t_(0.45); return (np.sin(2 * np.pi * 55 * t) * np.exp(-t * 9) * 0.9 + noise(0.45) * np.exp(-t * 60) * 0.25).astype(np.float32)
def glitch():
    t = t_(0.3); x = noise(0.3) * (np.sign(np.sin(2 * np.pi * 37 * t)) * 0.5 + 0.5); x = np.round(x * 4) / 4
    return (x * np.exp(-t * 6) * 0.35).astype(np.float32)
def stamp():
    t = t_(0.25); x = onepole(noise(0.25), 0.08) * 3 + np.sin(2 * np.pi * 70 * t)
    return (x * np.exp(-t * 22) * 0.8).astype(np.float32)
def static():
    t = t_(0.12); return (noise(0.12) * 0.22 * np.exp(-t * 10)).astype(np.float32)
def whoosh():
    d = 0.4; t = t_(d); x = onepole(noise(d), 0.05) * 4; return (x * np.sin(np.pi * t / d) ** 2 * 0.35).astype(np.float32)
def modem():
    t = t_(0.55); f = np.where((t * 14).astype(int) % 2 == 0, 1200, 2200); return (np.sin(2 * np.pi * f * t) * 0.07).astype(np.float32)
def boom():
    t = t_(1.2); return (np.sin(2 * np.pi * (48 - 10 * t) * t) * np.exp(-t * 3) * 0.9 + onepole(noise(1.2), 0.03) * 2 * np.exp(-t * 5)).astype(np.float32)
at(sfx, boom(), C['titulo']['a']); at(sfx, glitch(), C['abre_d']['a'])
for n in ('sofa1', 'zero', 'sofa2'): at(sfx, static(), C[n]['a'])
for n in ('tubo', 'veredito1', 'veredito2', 'veredito3', 'veredito4', 'fecho_tubo'): at(sfx, tum(), C[n]['a'], 0.8)
for n in ('veredito1', 'veredito2', 'veredito3', 'veredito4'): at(sfx, stamp(), C[n]['a'] + 0.3)
for n in ('cat1', 'cat2', 'cat3', 'cat4'): at(sfx, whoosh(), C[n]['a'] - 0.1)
at(sfx, stamp(), FX['K3']['start'] + 0.2, 1.2); at(sfx, modem(), C['cat5']['a'] + 0.1); at(sfx, glitch(), C['erro']['a'], 1.3)
at(sfx, stamp(), TL['T_SLAM'], 1.4); at(sfx, static(), TL['T_SLAM'] + 0.02, 1.5)
mix = (voz + mus + sfx)[:int(TL['TOTAL'] * SR)]
pcm = (np.clip(mix * 0.7, -1, 1) * 32767).astype(np.int16).tobytes()
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 's16le', '-ar', str(SR), '-ac', '1', '-i', '-', '_mix.wav'], input=pcm, check=True)
def lufs(p):
    e = subprocess.run(['ffmpeg', '-hide_banner', '-i', p, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(e[e.rindex('I:'):].split()[1])
src = '_mix.wav'; g = 0.0
for _ in range(7):      # ganho + limitador a -1,2 dBFS, repetido até ficar a -14 LUFS (±0,2)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', '_mix.wav', '-af', f'volume={g:.2f}dB,alimiter=limit=0.80:attack=3:release=60:level=false',
                    '-ar', str(SR), '-ac', '2', 'trilha.wav'], check=True)
    I = lufs('trilha.wav')
    if abs(I + 14) < 0.2: break
    g += -14 - I
print('ok trilha.wav', round(TL['TOTAL'], 2), 's', '| música TEMPORÁRIA (temas das séries)' if TEMP else '| tema do especial')
