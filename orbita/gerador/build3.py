"""v3 teste: cores vivas + movimento em loop. Gera JPG estático (t=0) e MP4 4:5 de 8 s."""
import subprocess, sys, shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import build2

ROOT = Path(__file__).parent
OUT = ROOT / "out3"; OUT.mkdir(exist_ok=True)
V = dict(mustard="#F4B414", red="#E3361D", vermilion="#F25C1C", blue="#1F6FD6", prussian="#17509A", teal="#0F9AA0",
         sage="#6FB487", pink="#F58DB3", navy="#1B2A5E", sky="#5EC4EC", olive="#A9BA14", ochre="#EE9A12")
VIVID = {"01-kirk-autografo": ["red", "mustard", "blue", "sky", "pink"],
 "02-khan": ["prussian", "red", "navy", "sky", "mustard"],
 "03-crusher-lcars": ["mustard", "teal", "navy", "pink", "vermilion"],
 "04-enterprise-d": ["vermilion", "prussian", "navy", "mustard", "sky"],
 "05-kirk-classic": ["blue", "mustard", "red", "sage", "pink"],
 "06-crystalline-entity": ["sky", "prussian", "teal", "mustard", "red"],
 "07-crusher-comandante": ["sky", "mustard", "prussian", "pink", "red"],
 "08-kirk-surge-foil": ["pink", "olive", "red", "sky", "blue"],
 "09-crusher-surge-foil": ["ochre", "teal", "navy", "pink", "olive"],
 "10-kirk-normal": ["vermilion", "ochre", "navy", "sage", "blue"]}
FPS, SEC = 30, 8


def run(name):
    p = next(x for x in build2.POSTS if x["file"] == name)
    p = dict(p, pal=[V[k] for k in VIVID[name]])
    html = build2.page(p).replace("document.title=bd.offsetHeight>95?'done-OVER':'done';",
        "document.title='done';window.draw=t=>paint(document.getElementById('c'),%d,%s,{cx:540,cy:458,px:48,py:48,pw:984,ph:820},t);" % (p["seed"], p["pal"]))
    h = ROOT / "html3" / f"{name}.html"; h.parent.mkdir(exist_ok=True); h.write_text(html, encoding="utf-8")
    fr = ROOT / "frames" / name
    shutil.rmtree(fr, ignore_errors=True); fr.mkdir(parents=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
        pg.goto(f"file://{h}"); pg.wait_for_function("document.title==='done'")
        n = FPS * SEC
        for i in range(n):
            pg.evaluate(f"window.draw({i / n})")
            pg.screenshot(path=str(fr / f"{i:04d}.jpg"), type="jpeg", quality=92)
            if i == 0:
                Image.open(fr / "0000.jpg").convert("RGB").resize((1080, 1350), Image.LANCZOS).save(OUT / f"{name}.jpg", quality=95)
        b.close()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(fr / "%04d.jpg"),
                    "-vf", "scale=1080:1350:flags=lanczos,format=yuv420p", "-c:v", "libx264", "-preset", "slow",
                    "-crf", "18", "-movflags", "+faststart", str(OUT / f"{name}.mp4")], check=True)
    print("ok", name)


if __name__ == "__main__":
    for n in sys.argv[1:] or VIVID:
        run(n)
