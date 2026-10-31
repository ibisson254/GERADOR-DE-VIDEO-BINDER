"""v4 'Órbita': fundo pintado fixo + discos e anéis em órbita contínua. MP4 4:5, 12 s, loop perfeito."""
import subprocess, sys, shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import build2
from build3 import V, VIVID

ROOT = Path(__file__).parent
OUT = ROOT / "out4"; OUT.mkdir(exist_ok=True)
FPS, SEC = 30, 12
O = "{cx:540,cy:458,px:48,py:48,pw:984,ph:820}"


def html_for(p):
    h = build2.page(p)
    js = (ROOT / "paint.js").read_text() + (ROOT / "anim.js").read_text()
    h = h.replace('<canvas id="c"></canvas>',
                  '<canvas id="c"></canvas><canvas id="m" width="2160" height="2700"></canvas><canvas id="ov" style="mix-blend-mode:multiply"></canvas>')
    start = h.index("<script>"); end = h.index("</script>")
    h = h[:start] + f"""<script>{js}
const O={O};
paint(document.getElementById('c'),{p['seed']},{p['pal']},Object.assign({{skip:true}},O),0);
overlay(document.getElementById('ov'),O,{p['seed']});
const orb=makeOrbit({p['seed']},{p['pal']},O);
window.draw=t=>orb(document.getElementById('m'),t);
draw(0);document.title='done';""" + h[end:]
    return h


def run(name, preview=False):
    p = next(x for x in build2.POSTS if x["file"] == name)
    p = dict(p, pal=[V[k] for k in VIVID[name]])
    h = ROOT / "html4" / f"{name}.html"; h.parent.mkdir(exist_ok=True); h.write_text(html_for(p), encoding="utf-8")
    fr = ROOT / "frames4" / name
    shutil.rmtree(fr, ignore_errors=True); fr.mkdir(parents=True)
    n = FPS * SEC
    idx = [0, n // 4, n // 2, 3 * n // 4] if preview else range(n)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
        pg.goto(f"file://{h}"); pg.wait_for_function("document.title==='done'")
        for i in idx:
            pg.evaluate(f"window.draw({i / n})")
            pg.screenshot(path=str(fr / f"{i:04d}.jpg"), type="jpeg", quality=92)
        b.close()
    Image.open(fr / "0000.jpg").convert("RGB").resize((1080, 1350), Image.LANCZOS).save(OUT / f"{name}.jpg", quality=95)
    if preview:
        ims = [Image.open(fr / f"{i:04d}.jpg").resize((540, 675)) for i in idx]
        s = Image.new("RGB", (1080, 1350)); [s.paste(im, ((k % 2) * 540, (k // 2) * 675)) for k, im in enumerate(ims)]
        s.save(ROOT / "html4" / f"preview-{name}.jpg", quality=85)
    else:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(fr / "%04d.jpg"),
                        "-vf", "scale=1080:1350:flags=lanczos,format=yuv420p", "-c:v", "libx264", "-preset", "slow",
                        "-crf", "19", "-movflags", "+faststart", str(OUT / f"{name}.mp4")], check=True)
    print("ok", name, "preview" if preview else "video")


if __name__ == "__main__":
    args = sys.argv[1:]
    prev = "--preview" in args
    names = [a for a in args if not a.startswith("--")] or list(VIVID)
    for nm in names:
        run(nm, prev)
