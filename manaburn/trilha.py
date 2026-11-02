"""Trilha de fundo do Mana & Burn. Dois modos:

- Sem "music" no episode.json (Ep. 1 e 2, midnight_throttle): um trecho contínuo da musica.mp3 cuja
  parada seca (MUSIC_BREAK) cai no "Comenta aí" e cuja pancada (MUSIC_SLAM) desliga a TV.
- Com "music" no episode.json (faixas sem parada no meio, como a concrete_teeth): o corpo toca de
  body_start até o "Comenta aí", corta seco, fica stop_len segundos em silêncio e volta com a
  pancada tirada de slam_src no momento em que a TV desliga. Com "snap" (padrão), o início do
  corpo anda até 0,4 s para o corte cair logo antes de uma batida forte.
"""
import subprocess, wave
import numpy as np

MUSIC_BREAK, MUSIC_SLAM = 125.05, 126.30   # midnight_throttle: parada seca e pancada


def _cut(path, start, dur, sr):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{start:.3f}', '-t', f'{dur:.3f}', '-i', path,
                    '-ac', '2', '-ar', str(sr), '_cut.wav'], check=True)
    w = wave.open('_cut.wav')
    return np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float32).reshape(-1, 2) / 32768


def _snap_start(path, body_start, comenta_start, sr=22050, reach=0.4):
    """Ajusta o início do corpo (até reach s) para o corte seco cair logo antes de uma batida forte
    da música: a parada soa como a banda parando junto, e não como um corte no meio da nota."""
    t = body_start + comenta_start
    a = max(0.0, t - reach - 0.05)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{a:.3f}', '-t', f'{2 * reach + 0.1:.3f}', '-i', path,
                    '-ac', '1', '-ar', str(sr), '_snap.wav'], check=True)
    w = wave.open('_snap.wav'); x = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float32) / 32768
    win, hop = 512, 110
    if len(x) < win * 2:
        return body_start
    S = np.log1p(np.array([np.abs(np.fft.rfft(x[i:i + win] * np.hanning(win))) for i in range(0, len(x) - win, hop)]))
    flux = np.maximum(0, np.diff(S, axis=0)).sum(axis=1)
    onset = a + (np.argmax(flux) + 1) * hop / sr + win / (2 * sr)
    return max(0.0, onset - 0.02 - comenta_start)


def slam_time(cfg, comenta_start):
    """Momento da pancada (TV desliga) no vídeo."""
    if cfg:
        return comenta_start + cfg.get('stop_len', 1.25)
    return MUSIC_SLAM - (MUSIC_BREAK - comenta_start)


def bed(cfg, comenta_start, t_slam, t_end, sr, default_file='musica.mp3'):
    """Devolve (trilha estéreo com t_end segundos, descrição do corte)."""
    n = int(t_end * sr)
    if not cfg:
        start = MUSIC_BREAK - comenta_start
        m = _cut(default_file, start, t_end, sr)
        desc = f'música de {start:.2f}s a {start + t_end:.2f}s'
    else:
        f = cfg.get('file', default_file)
        start = cfg['body_start']
        if cfg.get('snap', True):
            start = _snap_start(f, start, comenta_start)
        body = _cut(f, start, comenta_start, sr)
        fade = int(0.015 * sr)
        body[-fade:] *= np.linspace(1, 0, fade)[:, None]          # corte seco, sem estalo
        hit = _cut(f, cfg['slam_src'], t_end - t_slam, sr)
        m = np.zeros((n, 2), np.float32)
        m[:min(n, len(body))] = body[:n]
        a = int(t_slam * sr)
        m[a:a + len(hit)] = hit[:max(0, n - a)]
        m *= 10 ** (cfg.get('gain_db', 0) / 20)
        desc = (f"{f}: corpo de {start:.2f}s a {start + comenta_start:.2f}s, "
                f"parada seca de {t_slam - comenta_start:.2f}s, pancada a partir de {cfg['slam_src']:.2f}s")
    m = np.pad(m, ((0, max(0, n - len(m))), (0, 0)))[:n]
    return m, desc
