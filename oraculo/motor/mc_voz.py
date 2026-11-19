"""Meta em Curto · montagem da voz (padrão desde 19/11/2026, lição do MC-ESP03).

Não gera voz (isso é no ElevenLabs, uma geração, com autorização do fundador). Pega no(s) MP3 gerado(s), aplica o atempo
da série, encontra as frases pelas pausas (sem transcrição paga), encurta as pausas para caber na duração alvo e escreve
`voz_montada.wav` + os tempos de cada frase em `dados/episodio.json` (`voz_tempos`), que o motor usa para as legendas e cenas.

Uso:
  python3 -I oraculo/motor/mc_voz.py <pasta do episódio> <voz1.mp3> [voz2.mp3 ...]
Os MP3 juntam-se pela ordem dada (ex.: uma frase de abertura e a tomada principal).

No episodio.json:
  "frases": ["NO PORTAL X, DO Y:", "CLOUD: 522 DECKS.", ...]   # texto de cada legenda, pela ordem da locução
  "voz_cfg": {"atempo": 1.10, "alvo_s": 35.0, "pausa": 0.15, "pausa_min": 0.08,
              "pausas_longas": {"9": 0.45, "12": 0.25}}          # índice da frase -> pausa antes dela (corte seco, assinatura)
"""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np

SR = 48000


def carregar(p, atempo):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(p), '-af', f'atempo={atempo}', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def falas(x, limiar_db=-38, min_sil=0.12):
    """Intervalos com voz: janelas de 10 ms acima do limiar, separados por silêncios ≥ min_sil."""
    h = SR // 100; e = np.array([np.sqrt((x[i:i + h] ** 2).mean()) for i in range(0, len(x) - h, h)])
    on = 20 * np.log10(e + 1e-9) > limiar_db; seg, ini, sil = [], None, 0
    for i, o in enumerate(on):
        if o:
            if ini is None: ini = i
            sil = 0
        elif ini is not None:
            sil += 1
            if sil * 0.01 >= min_sil: seg.append([ini * 0.01, (i - sil + 1) * 0.01]); ini, sil = None, 0
    if ini is not None: seg.append([ini * 0.01, len(on) * 0.01])
    return seg


def falado(txt):
    """Comprimento aproximado do que a voz diz: números por extenso em pt-BR (num2words, se instalado), % = «por cento»."""
    import re
    try:
        from num2words import num2words
    except ImportError:
        num2words = None
    def ext(m):
        t = m.group(0).replace('.', '').replace(',', '.')
        try: return num2words(float(t) if '.' in t else int(t), lang='pt_BR') if num2words else 'x' * (4 * len(t))
        except Exception: return 'x' * (4 * len(t))
    return re.sub(r'\d[\d.,]*\d|\d', ext, txt).replace('%', ' por cento')


def alinhar(segs, frases):
    """Agrupa as falas detetadas em len(frases) grupos consecutivos (nunca entre ficheiros diferentes), de modo que a
    duração de cada grupo acompanhe o tamanho do texto da frase. Programação dinâmica; pausas longas pesam a favor do corte."""
    m, n = len(segs), len(frases)
    dur = [b - a for _, (a, b) in segs]; chars = [max(3, len(falado(f))) for f in frases]
    rate = sum(dur) / sum(chars)
    gap = [segs[i + 1][1][0] - segs[i][1][1] if segs[i][0] is segs[i + 1][0] else 99 for i in range(m - 1)]
    INF = float('inf'); C = [[INF] * (m + 1) for _ in range(n + 1)]; P = [[0] * (m + 1) for _ in range(n + 1)]; C[0][0] = 0
    for j in range(1, n + 1):
        for e in range(j, m + 1):
            for s_ in range(j - 1, e):
                if C[j - 1][s_] == INF: continue
                if any(gap[k] == 99 for k in range(s_, e - 1)): continue      # o grupo não pode atravessar ficheiros
                g = segs[e - 1][1][1] - segs[s_][1][0]
                custo = (g - rate * chars[j - 1]) ** 2 - (min(gap[e - 1], 1.0) * 0.5 if e < m else 0)
                if C[j - 1][s_] + custo < C[j][e]: C[j][e] = C[j - 1][s_] + custo; P[j][e] = s_
    if C[n][m] == INF: sys.exit('ERRO: não foi possível alinhar as falas com as frases (rever o texto ou os ficheiros).')
    out, e = [], m
    for j in range(n, 0, -1):
        s_ = P[j][e]; out.append((segs[s_][0], [segs[s_][1][0], segs[e - 1][1][1]])); e = s_
    return out[::-1]


def main():
    pasta = Path(sys.argv[1]); mp3s = sys.argv[2:]
    dj = pasta / 'dados' / 'episodio.json'; D = json.loads(dj.read_text(encoding='utf-8'))
    cfg = {'atempo': 1.10, 'alvo_s': 35.0, 'pausa': 0.15, 'pausa_min': 0.08, 'pausas_longas': {}}; cfg.update(D.get('voz_cfg', {}))
    frases = D['frases']; blocos = []
    for m in mp3s:
        x = carregar(m, cfg['atempo']); fs = falas(x)
        rms = np.sqrt(np.mean(np.concatenate([x[int(a_ * SR):int(b_ * SR)] for a_, b_ in fs]) ** 2)) if fs else 1
        blocos.append([x, fs, rms])
    ref = float(np.median([r for _, _, r in blocos]))
    for bl in blocos: bl[0] = bl[0] * (ref / max(bl[2], 1e-6))       # frases gravadas à parte ficam ao mesmo nível
    segs = [(x, s) for x, fs, _ in blocos for s in fs]
    if len(segs) < len(frases): sys.exit(f'ERRO: só {len(segs)} falas detetadas para {len(frases)} frases. Rever as frases.')
    segs = alinhar(segs, frases)
    pad = 0.02; longas = {int(k): v for k, v in cfg['pausas_longas'].items()}
    voz = sum((b - a + 2 * pad) for _, (a, b) in segs)
    pausa = cfg['pausa']; extra = sum(longas.values()) - pausa * len(longas)
    while voz + pausa * (len(segs) - 1) + extra > cfg['alvo_s'] - 0.15 and pausa > cfg['pausa_min']: pausa = round(pausa - 0.01, 2)
    out, t, tl = [], 0.0, []
    for i, ((x, (a, b)), txt) in enumerate(zip(segs, frases)):
        if i: g = longas.get(i, pausa); out.append(np.zeros(int(g * SR), np.float32)); t += g
        s = x[int(max(0, a - pad) * SR):int(min(len(x) / SR, b + pad) * SR)].copy(); n = int(0.01 * SR)
        s[:n] *= np.linspace(0, 1, n); s[-n:] *= np.linspace(1, 0, n)
        tl.append([round(t, 2), round(t + len(s) / SR, 2), txt]); out.append(s); t += len(s) / SR
    v = np.concatenate(out); dur = len(v) / SR
    w = (v / max(1e-6, np.abs(v).max()) * 0.95 * 32767).astype(np.int16)
    with wave.open(str(pasta / 'voz_montada.wav'), 'wb') as f: f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes(w.tobytes())
    D['voz_tempos'] = tl; D.setdefault('beats', {})['END'] = round(dur + 0.15, 2)
    dj.write_text(json.dumps(D, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'voz_montada.wav: {dur:.2f} s · pausa entre frases {pausa:.2f} s · END {dur + 0.15:.2f} s')
    if dur + 0.15 > cfg['alvo_s']: print(f'AVISO: passa o alvo de {cfg["alvo_s"]} s — encurtar o texto antes de gravar (lição do MC-ESP03).')
    for r in tl: print(r)


if __name__ == '__main__':
    main()
