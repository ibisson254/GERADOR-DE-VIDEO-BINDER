"""MB-EP17 · montagem do React (24/11/2026).
Intercala os blocos do kit (Mana & Burn) com o Reel original de @magicamador e as cartas em tela cheia.
Original: 480x854 (9:16) -> 1080x1920 sem cortes laterais. Áudio original normalizado a -14 LUFS.
uso (na pasta do kit, depois de render.py e de stems_kit.py burn.mp3 mana.mp3):  python3 montar_react.py original.mp4 kit.mp4 outro.mp4 saida.mp4
"""
import sys, json, subprocess, pathlib, shutil, math
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

ORIG, KIT, OUTRO, OUT = sys.argv[1:5]
TMP = pathlib.Path('react_tmp'); shutil.rmtree(TMP, ignore_errors=True); TMP.mkdir()
FPS = 30
FONT = '/mnt/skills/examples/canvas-design/canvas-fonts/GeistMono-Bold.ttf'
d = json.loads(open('data.js').read()[11:-1])
KIT_FIM = round(d['T_SLAM'] + 0.52, 3)

def run(*a):
    subprocess.run(a, check=True)

# áudio original normalizado (dois passos simplificados: loudnorm linear)
run('ffmpeg', '-y', '-loglevel', 'error', '-i', ORIG, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', '-ac', '2', str(TMP / 'orig.wav'))

CRED = ("drawtext=fontfile=%s:text='Partida\\: @magicamador':x=40:y=150:fontsize=34:fontcolor=white:"
        "box=1:boxcolor=0x050A10@0.6:boxborderw=12" % FONT)
VF_ORIG = 'scale=1080:1920:flags=lanczos,setsar=1,fps=30,' + CRED + ',format=yuv420p'
ENC = ['-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', '30',
       '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2']
segs = []
META = []

def kit(a, b):
    p = TMP / f's{len(segs):02d}_kit.mp4'
    run('ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{a}', '-to', f'{b}', '-i', KIT,
        '-vf', 'fps=30,format=yuv420p,setsar=1', '-af', 'aresample=48000,afade=t=in:d=0.03', *ENC, str(p))
    segs.append(p); META.append(('kit', a, b))

def orig(a, b):
    p = TMP / f's{len(segs):02d}_orig.mp4'
    run('ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{a}', '-to', f'{b}', '-i', ORIG, '-ss', f'{a}', '-to', f'{b}', '-i', str(TMP / 'orig.wav'),
        '-map', '0:v', '-map', '1:a', '-vf', VF_ORIG, '-af', 'afade=t=in:d=0.03', *ENC, str(p))
    segs.append(p); META.append(('orig', a, b))

def carta_png(nome, hl=None):
    im = Image.open(f'cards/{nome}.png').convert('RGBA')
    if hl:
        ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); dr = ImageDraw.Draw(ov); W, H = im.size
        for x, y, w, h in hl:
            dr.rectangle([x * W, y * H, (x + w) * W, (y + h) * H], fill=(255, 216, 74, 60), outline=(255, 216, 74, 255), width=4)
        im = Image.alpha_composite(im, ov)
    return im

def insercao(a, b, plano, flip_de=None):
    """Carta em tela cheia sobre o original desfocado; áudio original contínuo.
    plano = [(t_rel, nome, hl)] trocas de destaque; flip_de = carta anterior (flip 0,32 s no início)."""
    fr = TMP / f'fr{len(segs):02d}'; fr.mkdir()
    run('ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{a}', '-to', f'{b}', '-i', ORIG,
        '-vf', 'scale=1080:1920,fps=30,boxblur=24:2,eq=brightness=-0.22:saturation=0.7', str(fr / 'bg_%04d.png'))
    bgs = sorted(fr.glob('bg_*.png')); n = len(bgs)
    CW = 940
    cache = {}
    def carta(nome, hl):
        k = (nome, str(hl))
        if k not in cache:
            im = carta_png(nome, hl); cache[k] = im.resize((CW, round(im.height * CW / im.width)), Image.LANCZOS)
        return cache[k]
    for i, bgp in enumerate(bgs):
        t = i / FPS
        bg = Image.open(bgp).convert('RGBA')
        atual = [p for p in plano if p[0] <= t][-1]
        c = carta(atual[1], atual[2])
        esc = 1.0
        if flip_de and t < 0.32:            # flip no eixo Y: anterior encolhe, nova abre
            f = t / 0.32
            c = carta(flip_de, None) if f < 0.5 else c
            esc = abs(math.cos(math.pi * f))
        elif not flip_de and t < 0.18:       # entrada: pop 0,92 -> 1
            esc = 0.92 + 0.08 * (t / 0.18)
        w = max(2, round(c.width * esc)) if (flip_de and t < 0.32) else round(c.width * esc)
        h = c.height if (flip_de and t < 0.32) else round(c.height * esc)
        cc = c.resize((w, h), Image.BILINEAR) if (w, h) != c.size else c
        sh = Image.new('RGBA', (w + 40, h + 40), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([20, 20, w + 20, h + 20], 30, fill=(0, 0, 0, 150))
        sh = sh.filter(ImageFilter.GaussianBlur(14))
        x = (1080 - w) // 2; y = (1920 - h) // 2 - 40
        bg.alpha_composite(sh, (x - 20, y - 4)); bg.alpha_composite(cc, (x, y))
        bg.convert('RGB').save(fr / f'v_{i:04d}.png')
    p = TMP / f's{len(segs):02d}_ins.mp4'
    run('ffmpeg', '-y', '-loglevel', 'error', '-framerate', '30', '-i', str(fr / 'v_%04d.png'), '-ss', f'{a}', '-to', f'{b}', '-i', str(TMP / 'orig.wav'),
        '-map', '0:v', '-map', '1:a', '-vf', CRED + ',format=yuv420p', '-shortest', *ENC, str(p))
    segs.append(p); META.append(('orig', a, b))

def congela(t, dur):
    """Pausa visual discreta na garrafa: quadro parado com aproximação lenta, pop curto."""
    fr = TMP / 'freeze.png'
    run('ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{t}', '-i', ORIG, '-frames:v', '1', '-vf', 'scale=1080:1920', str(fr))
    p = TMP / f's{len(segs):02d}_freeze.mp4'
    nfr = round(dur * FPS)
    # garrafa por volta de x 0,48 · y 0,66 do quadro (31,0 s)
    vf = (f"zoompan=z='1+0.30*on/{nfr}':x='iw*0.48-iw/zoom/2':y='ih*0.64-ih/zoom/2':d={nfr}:s=1080x1920:fps=30,"
          + CRED + ',format=yuv420p')
    run('ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-i', str(fr), '-f', 'lavfi', '-i',
        f"sine=f=880:d=0.08,afade=t=out:d=0.08,apad=whole_dur={dur},volume=0.25",
        '-vf', vf, '-t', f'{dur}', *ENC, str(p))
    segs.append(p); META.append(('freeze', 0, dur))

VIN_PREV = [[0.07, 0.676, 0.86, 0.06]]
VIN_ALVO = [[0.07, 0.736, 0.86, 0.09]]
OCE_VINC = [[0.05, 0.645, 0.50, 0.036]]
LUZ_TXT = [[0.05, 0.680, 0.90, 0.112]]

# ---- linha do tempo (tempos do original medidos na transcrição Scribe + pausas do áudio) ----
kit(0, 6.40)                                                  # abertura + Burn (gancho) + Mana (ouve a proposta)
orig(0.0, 4.40)                                               # «Galera, vamos fazer uma pequena politicagem…»
insercao(4.40, 6.20, [(0, 'ocelot', None), (0.5, 'ocelot', OCE_VINC)])          # «um bando de ocelote»
insercao(6.20, 8.20, [(0, 'luz', None), (0.6, 'luz', LUZ_TXT)], flip_de='ocelot')  # «encantamento de luz da promessa»
orig(8.20, 17.00)                                             # «Tá dezesseis barra dezesseis… proposta… Diga.»
insercao(17.00, 20.80, [(0, 'vingadora', None), (1.0, 'vingadora', VIN_PREV), (2.6, 'vingadora', VIN_ALVO)])  # «Eu tenho a vingadora…»
orig(20.80, 22.95)                                            # «…no alvo que eu quiser. Correto?»
kit(6.50, 20.25)                                              # Burn «Correto?!» … Mana «dano prevenido não é causado»
orig(22.95, 24.85)                                            # «Hum.» «Qual dos dois cê quer que tira?»
congela(31.00, 0.9)                                           # a garrafa de 51 na mão do jogador
kit(20.30, 30.25)                                             # 51 · Lê o rótulo · roubou a cena · ninguém quer ser o alvo
orig(30.55, 43.60)                                            # «Dezesseis.» «Não tira eu não.» … «defendo com a vingadora»
orig(46.50, 47.80)                                            # «Cê não inventa não.»
kit(30.35, KIT_FIM)                                           # A/B · Comenta aí · TV desliga

# fecho do scanner com a trilha do kit por baixo (como juntar_fecho.py)
dur_f = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', OUTRO]))
p = TMP / f's{len(segs):02d}_outro.mp4'
run('ffmpeg', '-y', '-loglevel', 'error', '-i', OUTRO, '-ss', f'{KIT_FIM}', '-t', f'{dur_f}', '-i', 'trilha_final.wav',
    '-map', '0:v', '-map', '1:a', '-vf', 'fps=30,format=yuv420p,setsar=1', '-af', f'afade=t=out:st={dur_f - 0.45:.3f}:d=0.45', *ENC, str(p))
segs.append(p); META.append(('outro', 0, dur_f))

# ---- áudio: música contínua por baixo de tudo (24/11/2026, pedido do fundador) ----
# Voz+sfx do kit vêm das faixas separadas (stems_kit.py); a música é uma só faixa contínua (musica.mp3),
# com o ducking do kit nos blocos da dupla e mais baixa (-18 dB) por baixo do vídeo do parceiro.
import numpy as np, pyloudnorm
SR = 44100
def wav(path, extra=()):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', path, *extra, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
durs = [float(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v', '-count_frames', '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', str(x)])) / FPS for x in segs]
ini = np.r_[0, np.cumsum(durs)]; N = int(round(ini[-1] * SR))
vf = np.load('_stem_vf.npy'); gk = np.load('_stem_g.npy'); k = float(np.load('_stem_k.npy')[0])
vf = vf / k; gk = gk / k
orig_a = wav(str(TMP / 'orig.wav'))
meter = pyloudnorm.Meter(SR)
alvo = meter.integrated_loudness(vf[:int(d['T_SLAM'] * SR)])
orig_a *= 10 ** ((alvo - meter.integrated_loudness(orig_a)) / 20)     # narrador ao nível das vozes da dupla
voz = np.zeros((N, 2), np.float32); gm = np.zeros(N, np.float32)
REF = 0.42 / k; BAIXO = REF * 10 ** (-18 / 20); PAUSA = REF * 10 ** (-6 / 20)
for (tipo, a, b), t0, du in zip(META, ini, durs):
    s0 = int(round(t0 * SR)); n = int(round(du * SR)); sl = slice(s0, s0 + n)
    if tipo == 'kit':
        ka = int(round(a * SR)); seg = vf[ka:ka + n]; voz[s0:s0 + len(seg)] += seg; gg = gk[ka:ka + n]; gm[s0:s0 + len(gg)] = gg
    elif tipo == 'orig':
        oa = int(round(a * SR)); seg = orig_a[oa:oa + n]; voz[s0:s0 + len(seg)] += seg; gm[sl] = BAIXO
    elif tipo == 'freeze':
        tt = np.arange(int(0.08 * SR)) / SR; pop = (0.25 * np.sin(2 * np.pi * 880 * tt) * (1 - tt / 0.08)).astype(np.float32)
        voz[s0:s0 + len(pop)] += pop[:, None]; gm[sl] = PAUSA
    else:   # fecho do scanner: música cheia, desce no fim
        gm[sl] = REF * np.clip((t0 + du - (s0 + np.arange(n)) / SR) / 0.45, 0, 1)
w = int(0.25 * SR); gm = np.convolve(gm, np.ones(w) / w, 'same').astype(np.float32)   # rampas de 0,25 s entre blocos
gm[-int(0.45 * SR):] *= np.linspace(1, 0, int(0.45 * SR))
lc = [m for (m, t0) in zip(META, ini) if m[0] == 'kit'][-1]
t_kit4 = ini[[i for i, m in enumerate(META) if m[0] == 'kit'][-1]]
t_comenta = t_kit4 + (d['lines'][-1]['start'] - lc[1])
inicio = 125.05 - t_comenta                       # parada seca da música no «Comenta aí» (trilha.MUSIC_BREAK)
mus = wav('musica.mp3', ('-ss', f'{inicio:.3f}', '-t', f'{ini[-1] + 1:.3f}'))[:N]
mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
mix = voz + mus * gm[:, None]
mix /= np.max(np.abs(mix)) * 1.05
import wave
with wave.open(str(TMP / 'mix.wav'), 'wb') as o:
    o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR); o.writeframes((mix * 32767).astype('<i2').tobytes())
print(f'música de {inicio:.2f}s · «Comenta aí» no final a {t_comenta:.2f}s · narrador ajustado a {alvo:.1f} LUFS (pré-mistura)')

lst = TMP / 'lista.txt'; lst.write_text(''.join(f"file '{s.resolve()}'\n" for s in segs))
run('ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', str(lst), '-i', str(TMP / 'mix.wav'),
    '-map', '0:v', '-map', '1:a', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,alimiter=limit=0.85:level=false',
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', '30',
    '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', OUT)
print('ok', OUT)
