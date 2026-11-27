#!/usr/bin/env python3
"""Controlo de qualidade automático do ficheiro final (nucleo/CHECKLIST_QUALIDADE.md, bloco C).

Mede o que a máquina consegue medir e gera as provas visuais para o olho humano:
  - formato (resolução, fps) contra o formato da frente;
  - duração (com e sem o fecho);
  - loudness integrado e pico verdadeiro (ffmpeg ebur128);
  - presença do fecho comum/outro/outro_binder_916.mp4 no fim (comparação quadro a quadro);
  - lista de cortes (timecodes) para o diagnóstico;
  - folha de contacto com a zona segura do Instagram sobreposta (1 quadro por segundo).

Não substitui o olho: personagens, legendas tapadas e cartas cortadas confere-se na folha de contacto.
Classificação dos problemas: P0 impede publicação, P1 qualidade importante, P2 refinamento.

Uso:
  python3 -I comum/qc/qc_video.py VIDEO.mp4 [--frente manaburn|tubo|conde|orbita|lambe] [--sem-fecho] [--saida PASTA]

Depende só de ffmpeg/ffprobe, numpy e Pillow. Não altera o vídeo.
"""
import argparse, json, os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FECHO = os.path.join(RAIZ, 'comum', 'outro', 'outro_binder_916.mp4')

# Formato por frente (constituição §6). Duração: livre nas séries desde 02/11/2026 (só informativa);
# o Órbita mantém o loop de 12 s. Duração contada sem o fecho.
# Áudio por frente (27/11/2026): lufs None = só informativo (música escolhida no Instagram); pico = máximo do true peak;
# audio True = a frente tem de ter som (voz/trilha), None = vídeo mudo aceite (versão para escolher a música no Instagram).
#   Lambe-lambe: efeitos próprios a pico −6 dBFS e música no Instagram (lambe-lambe/CONTEXTO.md, «Som nos Reels»).
#   Órbita: Reels sem áudio, música no Instagram (series.yaml).  TUBO: 25–35 s sem o fecho (oraculo/PERFIL.md, regra de 16/11).
FRENTES = {
    'manaburn': {'w': 1080, 'h': 1920, 'fps': 30, 'dur': None,     'fecho': True,  'lufs': -14.0, 'pico': -1.0, 'audio': True},
    'tubo':     {'w': 1080, 'h': 1920, 'fps': 30, 'dur': (25, 35), 'fecho': True,  'lufs': -14.0, 'pico': -1.0, 'audio': True},
    'conde':    {'w': 1080, 'h': 1920, 'fps': 30, 'dur': None,     'fecho': True,  'lufs': -14.0, 'pico': -1.0, 'audio': True},
    'orbita':   {'w': 1080, 'h': 1350, 'fps': 30, 'dur': (12, 12), 'fecho': False, 'lufs': None,  'pico': -1.0, 'audio': None},
    'lambe':    {'w': 1080, 'h': 1920, 'fps': 30, 'dur': None,     'fecho': True,  'lufs': None,  'pico': -6.0, 'audio': None},
}
LUFS_TOL = 1.0
SILENCIO_DB, SILENCIO_S = -50, 1.5        # silêncio no corpo de uma frente com voz/trilha (P2: conferir se é intencional)
PRETO_S = 0.3                             # quadros pretos seguidos no corpo (antes do fecho) = P1

# Zona segura aproximada dos Reels em 1080x1920 (interface do Instagram por cima do vídeo).
# Aproximação de trabalho, não especificação oficial: conferir no telemóvel quando o resultado for limite.
ZONA = {'topo': 220, 'base': 380, 'direita': 140}


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(path):
    r = sh(['ffprobe', '-v', 'error', '-show_entries',
            'stream=codec_type,codec_name,pix_fmt,width,height,r_frame_rate,sample_rate,duration:format=duration,size',
            '-of', 'json', path])
    j = json.loads(r.stdout)
    vs = [s for s in j['streams'] if s.get('codec_type') == 'video']
    au = [s for s in j['streams'] if s.get('codec_type') == 'audio']
    s, f = vs[0], j['format']
    n, d = s['r_frame_rate'].split('/')
    a = au[0] if au else {}
    return {'w': s['width'], 'h': s['height'], 'fps': round(int(n) / int(d), 3), 'dur': float(f['duration']),
            'vcodec': s.get('codec_name'), 'pix_fmt': s.get('pix_fmt'), 'vdur': float(s['duration']) if s.get('duration') else None,
            'acodec': a.get('codec_name'), 'arate': int(a['sample_rate']) if a.get('sample_rate') else None,
            'adur': float(a['duration']) if a.get('duration') else None, 'mb': round(int(f.get('size', 0)) / 1e6, 1)}


def loudness(path):
    """loudness integrado, true peak e silêncios (uma só passagem pelo áudio)"""
    r = sh(['ffmpeg', '-hide_banner', '-nostats', '-i', path, '-vn', '-af',
            f'silencedetect=n={SILENCIO_DB}dB:d={SILENCIO_S},ebur128=peak=true', '-f', 'null', '-'])
    txt = r.stderr[r.stderr.rfind('Summary:'):] if 'Summary:' in r.stderr else ''
    i = re.search(r'I:\s+(-?[\d.]+) LUFS', txt)
    p = re.search(r'Peak:\s+(-?[\d.]+|-inf) dBFS', txt)
    sil = [(float(a), float(b)) for a, b in re.findall(r'silence_end: (-?[\d.]+) \| silence_duration: ([\d.]+)', r.stderr)]
    sil = [(round(e - d, 2), round(e, 2)) for e, d in sil]
    if not i:
        return None, None, []  # sem faixa de áudio
    return float(i.group(1)), (float(p.group(1)) if p and p.group(1) != '-inf' else None), sil


def quadros(path, inicio, dur, fps=10, tam=(108, 192)):
    """Quadros em cinzento reduzidos, como matriz numpy (n, h, w)."""
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{inicio:.3f}', '-t', f'{dur:.3f}', '-i', path,
                        '-vf', f'fps={fps},scale={tam[0]}:{tam[1]},format=gray', '-f', 'rawvideo', '-'],
                       capture_output=True)
    a = np.frombuffer(r.stdout, np.uint8)
    n = a.size // (tam[0] * tam[1])
    return a[:n * tam[0] * tam[1]].reshape(n, tam[1], tam[0]).astype(np.float32)


def confere_fecho(path, dur):
    """Compara os últimos segundos do vídeo com o fecho oficial. Devolve (presente, diferença média 0-255, início estimado)."""
    if not os.path.exists(FECHO):
        return None, None, None
    fd = probe(FECHO)['dur']
    ref = quadros(FECHO, 0, fd)
    if dur < fd:
        return False, None, None
    melhor = (1e9, None)
    # procura o alinhamento em janelas de 1/10 s nos últimos 0,5 s de folga
    for k in range(0, 6):
        ini = max(0.0, dur - fd - k * 0.1)
        v = quadros(path, ini, fd)
        n = min(len(v), len(ref))
        if n == 0:
            continue
        diff = float(np.abs(v[:n] - ref[:n]).mean())
        if diff < melhor[0]:
            melhor = (diff, ini)
    # < 12 de diferença média em 0-255: o mesmo fecho (compressão e mistura não o alteram mais do que isso)
    return melhor[0] < 12, round(melhor[0], 2), (round(melhor[1], 2) if melhor[1] is not None else None)


def cortes(path, limiar=0.25):
    """cortes (timecodes) e intervalos de quadros pretos, numa só passagem pelo vídeo"""
    r = sh(['ffmpeg', '-hide_banner', '-i', path, '-an', '-vf',
            f"blackdetect=d={PRETO_S}:pix_th=0.08,select='gt(scene,{limiar})',showinfo", '-f', 'null', '-'])
    cut = [round(float(x), 2) for x in re.findall(r'pts_time:([\d.]+)', r.stderr)]
    preto = [(round(float(a), 2), round(float(b), 2)) for a, b in re.findall(r'black_start:([\d.]+) black_end:([\d.]+)', r.stderr)]
    return cut, preto


def folha(path, dur, saida, w, h):
    """Folha de contacto, 1 quadro por segundo, com a zona segura do Instagram em vermelho translúcido."""
    sw, shh = 216, int(216 * h / w)
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-vf', f'fps=1,scale={sw}:{shh}',
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True)
    a = np.frombuffer(r.stdout, np.uint8)
    n = a.size // (sw * shh * 3)
    fr = a[:n * sw * shh * 3].reshape(n, shh, sw, 3)
    cols = 10
    linhas = (n + cols - 1) // cols
    img = Image.new('RGB', (cols * sw, linhas * (shh + 18)), (20, 20, 20))
    k = sw / w
    for i in range(n):
        q = Image.fromarray(fr[i]).convert('RGBA')
        ov = Image.new('RGBA', q.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        if h == 1920:  # zona segura só faz sentido nos Reels 9:16
            d.rectangle([0, 0, sw, ZONA['topo'] * k], fill=(255, 0, 0, 60))
            d.rectangle([0, shh - ZONA['base'] * k, sw, shh], fill=(255, 0, 0, 60))
            d.rectangle([sw - ZONA['direita'] * k, 0, sw, shh], fill=(255, 0, 0, 60))
        q = Image.alpha_composite(q, ov).convert('RGB')
        x, y = (i % cols) * sw, (i // cols) * (shh + 18)
        img.paste(q, (x, y + 18))
        ImageDraw.Draw(img).text((x + 4, y + 3), f'{i:02d}s', fill=(255, 255, 255))
    img.save(saida)
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('video')
    ap.add_argument('--frente', default='manaburn', choices=sorted(FRENTES))
    ap.add_argument('--sem-fecho', action='store_true', help='exceção registada (especial) ou Órbita')
    ap.add_argument('--saida', default=None)
    a = ap.parse_args()

    if not os.path.isfile(a.video):
        print(f'ficheiro não encontrado: {a.video}'); return 2
    f = FRENTES[a.frente]
    base = os.path.splitext(os.path.basename(a.video))[0]
    out = a.saida or os.path.join(os.path.dirname(os.path.abspath(a.video)), f'qc_{base}')
    os.makedirs(out, exist_ok=True)

    p = probe(a.video)
    lufs, pico, sil = loudness(a.video)
    quer_fecho = f['fecho'] and not a.sem_fecho
    tem_fecho, dif, ini_fecho = confere_fecho(a.video, p['dur']) if quer_fecho else (None, None, None)
    dur_sem = round(ini_fecho, 2) if tem_fecho else round(p['dur'], 2)
    cut, preto = cortes(a.video)
    # o fecho começa num quadro escuro e acaba em fade para preto (comum/outro/LEIA-ME.md): só conta o corpo.
    # Um preto que acaba na entrada do fecho é a transição (ex.: TV a desligar no Mana & Burn), não um defeito.
    fim_corpo = (ini_fecho if tem_fecho else p['dur']) - 0.05
    preto_corpo = [(i, e) for i, e in preto if e < fim_corpo - 0.1]
    sil_corpo = [(i, e) for i, e in sil if i < fim_corpo - 0.3]
    nq = folha(a.video, p['dur'], os.path.join(out, 'folha_contacto.png'), p['w'], p['h'])

    prob = []
    if (p['w'], p['h']) != (f['w'], f['h']):
        prob.append(('P0', f"formato {p['w']}x{p['h']}, a frente pede {f['w']}x{f['h']}"))
    if abs(p['fps'] - f['fps']) > 0.01:
        prob.append(('P1', f"{p['fps']} fps, a frente pede {f['fps']}"))
    if quer_fecho and not tem_fecho:
        prob.append(('P0', f'fecho do scanner não encontrado no fim (diferença média {dif})'))
    if p['vcodec'] != 'h264' or p['pix_fmt'] != 'yuv420p':
        prob.append(('P1', f"vídeo {p['vcodec']}/{p['pix_fmt']}, o padrão do estúdio é h264/yuv420p"))
    if lufs is None:
        if f['audio']:
            prob.append(('P1', 'sem faixa de áudio'))
    else:
        if p['acodec'] != 'aac':
            prob.append(('P2', f"áudio {p['acodec']}, o padrão do estúdio é AAC"))
        if p['vdur'] and p['adur'] and abs(p['vdur'] - p['adur']) > 0.25:
            prob.append(('P1', f"áudio {p['adur']:.2f} s e vídeo {p['vdur']:.2f} s (diferença > 0,25 s: fim cortado ou silêncio a mais)"))
        if f['lufs'] is not None and abs(lufs - f['lufs']) > LUFS_TOL:
            prob.append(('P1', f"loudness {lufs} LUFS, alvo {f['lufs']} ± {LUFS_TOL}"))
        if pico is not None and pico >= f['pico']:
            prob.append(('P1', f"pico verdadeiro {pico} dBFS, máximo < {f['pico']}"))
        if f['audio'] and sil_corpo:
            prob.append(('P2', 'silêncio no corpo (≥ %s s abaixo de %s dB): %s; conferir se é intencional'
                         % (SILENCIO_S, SILENCIO_DB, ', '.join(f'{i}–{e} s' for i, e in sil_corpo))))
    if preto_corpo:
        prob.append(('P1', 'quadros pretos no corpo: ' + ', '.join(f'{i}–{e} s' for i, e in preto_corpo)))
    if f['dur'] and not (f['dur'][0] <= dur_sem <= f['dur'][1]):
        prob.append(('P2', f'{dur_sem} s sem o fecho, perfil pede {f["dur"][0]}–{f["dur"][1]} s '
                           '(P2 se for especial ou formato registado; senão, rever o perfil)'))

    rel = {'video': os.path.basename(a.video), 'frente': a.frente, 'formato': p,
           'duracao_sem_fecho': dur_sem, 'lufs': lufs, 'pico_dbtp': pico,
           'alvo_audio': {'lufs': f['lufs'], 'pico_max': f['pico'], 'som_obrigatorio': f['audio']},
           'silencios_s': sil, 'pretos_s': preto,
           'fecho': {'exigido': quer_fecho, 'presente': tem_fecho, 'diferenca_media': dif, 'inicio_s': ini_fecho},
           'cortes_s': cut, 'quadros_na_folha': nq, 'problemas': prob,
           'zona_segura_aprox_px': ZONA,
           'conferir_a_olho': ['legendas e textos fora da zona vermelha', 'carta inteira, também nos zooms',
                               'nada a tapar fontes ou rodapés', 'personagens inteiros e no modelo',
                               'sem corte lateral']}
    with open(os.path.join(out, 'qc.json'), 'w', encoding='utf-8') as fh:
        json.dump(rel, fh, ensure_ascii=False, indent=2)

    print(f"{rel['video']} · {p['w']}x{p['h']} · {p['fps']} fps · {p['dur']:.2f} s ({dur_sem} s sem fecho) · {p['vcodec']}/{p['pix_fmt']} · {p['mb']} MB")
    alvo = f"alvo {f['lufs']} LUFS" if f['lufs'] is not None else 'loudness só informativo nesta frente'
    print(f"áudio: {lufs} LUFS · pico {pico} dBTP ({alvo}, pico < {f['pico']}) · {p['acodec'] or 'sem áudio'}")
    print(f"fecho: {'presente a partir de ' + str(ini_fecho) + ' s' if tem_fecho else ('não exigido' if not quer_fecho else 'AUSENTE')} (dif. {dif})")
    print(f"cortes: {', '.join(str(c) for c in cut)}")
    for g, t in prob:
        print(f'{g} · {t}')
    if not prob:
        print('Sem problemas mensuráveis. Falta a conferência a olho (folha_contacto.png).')
    print(f'saída: {out}')
    return 1 if any(g == 'P0' for g, _ in prob) else 0


if __name__ == '__main__':
    sys.exit(main())
