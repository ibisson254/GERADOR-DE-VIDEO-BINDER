#!/usr/bin/env python3
"""Regressão de imagem entre dois vídeos (antes/depois de mexer num motor), quadro a quadro.

Para qualquer motor: o Meta em Curto tem o seu `oraculo/motor/mc_render_regressao.py` (que renderiza os episódios);
este compara dois ficheiros já renderizados (Mana & Burn, Lambe-lambe, Conde, Abismo...).

Uso:
  python3 -I comum/qc/comparar_videos.py ANTES.mp4 DEPOIS.mp4 [--tol 0] [--json saida.json] [--audio]

Mede: nº de quadros, quadros idênticos (byte a byte depois de descodificar), maior diferença por píxel (0–255),
nº de píxeis diferentes no pior quadro e PSNR mínimo. Com --audio, compara também o PCM (MD5) e a duração.
Sai com código 1 se algum quadro diferir mais do que --tol (0 = tem de ser igual).
Depende de ffmpeg/ffprobe e numpy. Não altera os vídeos.
"""
import argparse, hashlib, json, subprocess, sys
import numpy as np


def dims(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height',
                        '-of', 'csv=p=0', path], capture_output=True, text=True, check=True)
    w, h = r.stdout.strip().split(',')[:2]
    return int(w), int(h)


def quadros(path, w, h):
    """gerador de quadros RGB (h, w, 3) uint8, sem carregar o vídeo inteiro na memória"""
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', path, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    n = w * h * 3
    try:
        while True:
            b = p.stdout.read(n)
            if len(b) < n:
                break
            yield np.frombuffer(b, np.uint8).reshape(h, w, 3)
    finally:                                  # vídeos com nº de quadros diferente: fecha o outro ffmpeg sem ruído
        p.stdout.close(); p.kill(); p.wait()


def pcm_md5(path):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-vn', '-f', 's16le', '-ac', '2', '-ar', '48000', '-'], capture_output=True)
    return hashlib.md5(r.stdout).hexdigest() if r.stdout else None, len(r.stdout) / (48000 * 4)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('antes'); ap.add_argument('depois')
    ap.add_argument('--tol', type=int, default=0, help='maior diferença por píxel aceite (0–255)')
    ap.add_argument('--json'); ap.add_argument('--audio', action='store_true')
    a = ap.parse_args()

    wa, ha = dims(a.antes); wb, hb = dims(a.depois)
    if (wa, ha) != (wb, hb):
        print(f'formatos diferentes: {wa}x{ha} vs {wb}x{hb}'); return 1
    n = iguais = 0; pior = (0, -1, 0); psnr_min = float('inf'); difs = []
    for i, (qa, qb) in enumerate(zip(quadros(a.antes, wa, ha), quadros(a.depois, wb, hb))):
        n += 1
        if np.array_equal(qa, qb):
            iguais += 1; continue
        d = np.abs(qa.astype(np.int16) - qb.astype(np.int16))
        m = int(d.max()); npx = int((d.max(2) > 0).sum())
        mse = float((d.astype(np.float32) ** 2).mean())
        psnr = 10 * np.log10(255 ** 2 / mse) if mse else float('inf')
        psnr_min = min(psnr_min, psnr); difs.append(i)
        if m > pior[0] or (m == pior[0] and npx > pior[2]):
            pior = (m, i, npx)
    na = int(subprocess.run(['ffprobe', '-v', 'error', '-count_packets', '-select_streams', 'v:0', '-show_entries',
                             'stream=nb_read_packets', '-of', 'csv=p=0', a.antes], capture_output=True, text=True).stdout.strip() or 0)
    nb = int(subprocess.run(['ffprobe', '-v', 'error', '-count_packets', '-select_streams', 'v:0', '-show_entries',
                             'stream=nb_read_packets', '-of', 'csv=p=0', a.depois], capture_output=True, text=True).stdout.strip() or 0)
    rel = {'antes': a.antes, 'depois': a.depois, 'quadros': [na, nb], 'comparados': n, 'iguais': iguais,
           'diferentes': n - iguais, 'maior_diferenca_px': pior[0], 'pior_quadro': pior[1], 'pixeis_no_pior': pior[2],
           'psnr_min_db': None if psnr_min == float('inf') else round(psnr_min, 2), 'quadros_diferentes': difs[:50]}
    if a.audio:
        ma, da = pcm_md5(a.antes); mb, db = pcm_md5(a.depois)
        rel['audio'] = {'md5_igual': ma == mb, 'dur_s': [round(da, 3), round(db, 3)]}
    print(f"{n} quadros comparados ({na} vs {nb}) · {iguais} iguais · {n - iguais} diferentes"
          + (f" · pior: quadro {pior[1]}, {pior[2]} píxeis, diferença máx. {pior[0]}, PSNR mín. {rel['psnr_min_db']} dB" if n - iguais else ''))
    if a.audio:
        print(f"áudio: {'igual' if rel['audio']['md5_igual'] else 'DIFERENTE'} ({rel['audio']['dur_s'][0]} s vs {rel['audio']['dur_s'][1]} s)")
    if a.json:
        json.dump(rel, open(a.json, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    falha = na != nb or pior[0] > a.tol or (a.audio and not rel['audio']['md5_igual'])
    print('REGRESSÃO: ' + ('FALHOU' if falha else 'OK') + f' (tolerância {a.tol})')
    return 1 if falha else 0


if __name__ == '__main__':
    sys.exit(main())
