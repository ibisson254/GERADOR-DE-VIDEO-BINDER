import pathlib, subprocess, json, sys
from playwright.sync_api import sync_playwright
root = pathlib.Path(__file__).parent.resolve()
d = json.loads((root/'data.js').read_text()[11:-1]); T_END = d['T_END']; FPS = 30
out = root/(sys.argv[1] if len(sys.argv) > 1 else 'ManaBurn_Ep1_Q_916.mp4')
n = int(round(T_END * FPS)); frames = root/'frames'; frames.mkdir(exist_ok=True)
for f in frames.glob('*.jpg'): f.unlink()
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.on('pageerror', lambda e: print('ERRO:', e))
    pg.goto((root/'index.html').as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400)
    pg.wait_for_function('window.READY()')
    for i in range(n):
        pg.evaluate(f'render({i / FPS})'); pg.screenshot(path=str(frames/f'{i:05d}.jpg'), type='jpeg', quality=92)
        if i % 300 == 0: print('quadro', i, flush=True)
    b.close()
subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i',str(frames/'%05d.jpg'),'-i',str(root/'trilha_final.wav'),
  '-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-r',str(FPS),'-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',str(out)],check=True)
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(frames/f'{int(4.5*FPS):05d}.jpg'),'-q:v','2',str(out.with_name(out.stem + '_capa.jpg'))],check=True)
print('ok', out)
