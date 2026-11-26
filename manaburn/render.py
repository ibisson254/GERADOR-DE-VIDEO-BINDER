import pathlib, subprocess, json, sys, os
from playwright.sync_api import sync_playwright
root = pathlib.Path(__file__).parent.resolve()
FPS = 30

# Captura em paralelo (26/11/2026, missão de engenharia): N processos do Chromium, cada um com um bloco contíguo de quadros.
# Antes de capturar, cada processo percorre render(t) desde o quadro 0 sem screenshot (≈3 ms por quadro), para o DOM e as
# imagens chegarem ao bloco no mesmo estado que no render sequencial. Quadros iguais aos do modo antigo (conferido no MB-EP16).
# --workers 1 (ou MB_WORKERS=1) repõe o comportamento anterior; por defeito: núcleos da máquina, até 4.
def _workers(argv):
    w = os.environ.get('MB_WORKERS')
    for a in argv:
        if a.startswith('--workers='): w = a.split('=', 1)[1]
    return max(1, int(w)) if w else max(1, min(4, os.cpu_count() or 1))

def _abrir(p):
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.on('pageerror', lambda e: print('ERRO:', e))
    pg.goto((root/'index.html').as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400)
    pg.wait_for_function('window.READY()')
    return b, pg

def capturar(a, z, frames, aquecer=True):
    """Captura os quadros [a, z) para frames/NNNNN.jpg."""
    with sync_playwright() as p:
        b, pg = _abrir(p)
        if aquecer and a > 0:
            for i in range(a): pg.evaluate(f'render({i / FPS})')
            pg.wait_for_timeout(300)
        for i in range(a, z):
            pg.evaluate(f'render({i / FPS})'); pg.screenshot(path=str(frames/f'{i:05d}.jpg'), type='jpeg', quality=92)
            if i % 300 == 0: print('quadro', i, flush=True)
        b.close()

def _bloco(args): capturar(*args)

if __name__ == '__main__':
    LUZ_POS = '--luz-pos' in sys.argv   # luz já vem do cenário (sala v3, 08/11/2026); luz.py só a pedido
    W = _workers(sys.argv)
    sys.argv = [a for a in sys.argv if a != '--luz-pos' and not a.startswith('--workers=')]
    d = json.loads((root/'data.js').read_text().strip()[11:-1]); T_END = d['T_END']
    out = root/(sys.argv[1] if len(sys.argv) > 1 else 'ManaBurn_Ep1_Q_916.mp4')
    CAPA = float(sys.argv[2]) if len(sys.argv) > 2 else 4.5
    n = int(round(T_END * FPS)); frames = root/'frames'; frames.mkdir(exist_ok=True)
    for f in frames.glob('*.jpg'): f.unlink()
    if W == 1 or n < 120: capturar(0, n, frames, aquecer=False)
    else:
        import multiprocessing as mp
        cortes = [n * k // W for k in range(W + 1)]
        print(f'captura em {W} processos: blocos {cortes}', flush=True)
        with mp.get_context('spawn').Pool(W) as pool: pool.map(_bloco, [(cortes[k], cortes[k + 1], frames) for k in range(W)])
        falta = [i for i in range(n) if not (frames/f'{i:05d}.jpg').exists()]
        if falta: sys.exit(f'quadros em falta: {falta[:10]}')
    subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i',str(frames/'%05d.jpg'),'-i',str(root/'trilha_final.wav'),
      '-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-r',str(FPS),'-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',str(out)],check=True)
    capa = frames/f'{int(CAPA*FPS):05d}.jpg'
    if LUZ_POS:
        sys.path.insert(0, str(root)); import luz, numpy as np
        from PIL import Image
        bruto = out.with_name(out.stem + '_semluz.mp4'); out.replace(bruto)
        luz.aplicar(str(bruto), str(out)); bruto.unlink()
        capa_luz = frames/'capa_luz.png'; Image.fromarray(luz.quadro(np.asarray(Image.open(capa).convert('RGB')))).save(capa_luz); capa = capa_luz
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(capa),'-q:v','2',str(out.with_name(out.stem + '_capa.jpg'))],check=True)
    print('ok', out)
