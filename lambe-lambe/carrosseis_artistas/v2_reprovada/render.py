"""Renderiza os carrosséis: python3 -I render.py <pasta> <saida> <id> [<id> ...]"""
import sys, os, asyncio
from playwright.async_api import async_playwright
from PIL import Image
src, out, ids = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]), sys.argv[3:]
os.makedirs(out, exist_ok=True)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg = await b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
        for cid in ids:
            await pg.goto("file://" + os.path.join(src, "artistas.html") + "?c=" + cid)
            await pg.wait_for_selector("body[data-ok]"); await pg.wait_for_timeout(700)
            for i in range(1, 6):
                f = os.path.join(out, f"_{cid}{i}.png")
                await pg.locator(f"#s{i}").screenshot(path=f)
                Image.open(f).convert("RGB").resize((1080, 1350), Image.LANCZOS).save(
                    os.path.join(out, f"artistas_{cid}_{i}.jpg"), quality=95)
                os.remove(f)
        await b.close()
asyncio.run(main())
