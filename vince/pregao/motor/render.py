"""Renderiza o Pregão Magic quadro a quadro (Playwright + canvas) e envia para o FFmpeg.

Uso:
  python3 render.py quadros 0.0 1.2 3.2 ...      -> PNG soltos em prev/ (inspeção)
  python3 render.py video saida.mp4 [t_fim] [t_ini] -> vídeo sem áudio, 1080x1920, 30 fps (troço opcional)
"""
import subprocess, sys, pathlib
from playwright.sync_api import sync_playwright

AQUI = pathlib.Path(__file__).resolve().parent
FPS = 30


def abrir(p):
    b = p.chromium.launch(args=["--allow-file-access-from-files", "--disable-web-security"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
    pg.goto((AQUI / "pregao.html").as_uri())
    pg.wait_for_function("window.PRONTO === true", timeout=60000)
    return b, pg


def quadro(pg, t):
    pg.evaluate(f"window.render({t:.5f})")
    return pg.locator("#c").screenshot(type="png")


def main():
    modo = sys.argv[1]
    with sync_playwright() as p:
        b, pg = abrir(p)
        if modo == "quadros":
            out = AQUI.parent / "prev"; out.mkdir(exist_ok=True)
            for s in sys.argv[2:]:
                (out / f"q_{float(s):06.2f}.png").write_bytes(quadro(pg, float(s)))
        else:
            saida = sys.argv[2]
            fim = float(sys.argv[3]) if len(sys.argv) > 3 else 41.198
            ini = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
            n = round(fim * FPS); i0 = round(ini * FPS)
            ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS),
                                   "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
                                   "-pix_fmt", "yuv420p", "-r", str(FPS), saida], stdin=subprocess.PIPE)
            for i in range(i0, n):
                ff.stdin.write(quadro(pg, i / FPS))
                if i % 150 == 0:
                    print(f"{i}/{n}", flush=True)
            ff.stdin.close(); ff.wait()
        b.close()


if __name__ == "__main__":
    main()
