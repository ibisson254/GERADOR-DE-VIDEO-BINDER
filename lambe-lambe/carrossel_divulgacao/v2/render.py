"""Renderiza o carrossel: python3 -I render.py <pasta_v2> <saida>"""
import sys, os, asyncio
from playwright.async_api import async_playwright
from PIL import Image
src, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]); os.makedirs(out, exist_ok=True)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--allow-file-access-from-files"])
        pg = await b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
        await pg.goto("file://" + os.path.join(src, "carrossel.html")); await pg.wait_for_timeout(800)
        await pg.evaluate("document.fonts.ready")
        for i in range(1, 6):
            await pg.evaluate(f"document.querySelectorAll('.slide').forEach(s=>s.classList.remove('on'));document.getElementById('s{i}').classList.add('on')")
            await pg.wait_for_timeout(400)
            f = os.path.join(out, f"_{i}.png")
            await pg.locator(f"#s{i}").screenshot(path=f)
            Image.open(f).convert("RGB").resize((1080, 1350), Image.LANCZOS).save(os.path.join(out, f"binder_lambe_carrossel_{i}.png")); os.remove(f)
        await b.close()
asyncio.run(main())
