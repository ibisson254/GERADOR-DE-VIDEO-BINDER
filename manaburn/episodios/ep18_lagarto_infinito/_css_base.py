import os, pathlib, shutil
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path('.').resolve(); SRC = ROOT / 'cards' / 'src'
u = lambda n: (SRC / n).as_uri()
CSS = """
@font-face{font-family:Bangers;src:url(node_modules/@fontsource/bangers/files/bangers-latin-400-normal.woff2)}
@font-face{font-family:Geist;font-weight:700;src:url(node_modules/geist/dist/fonts/geist-sans/Geist-Bold.woff2)}
@font-face{font-family:Geist;font-weight:500;src:url(node_modules/geist/dist/fonts/geist-sans/Geist-Medium.woff2)}
*{margin:0;padding:0;box-sizing:border-box}
body{width:744px;height:1040px;background:#0F172A;color:#F4F1E8;font-family:Geist;overflow:hidden;position:relative}
.f{position:absolute;inset:18px;border:6px solid #FFD84A;border-radius:18px;overflow:hidden}
.badge{position:absolute;left:30px;top:26px;z-index:3;background:#C8352B;color:#FFD84A;font:400 44px Bangers;letter-spacing:3px;padding:2px 18px;border-radius:6px}
.big{position:absolute;left:0;right:0;text-align:center;font:400 88px/0.95 Bangers;color:#F4F1E8;letter-spacing:1px}
.big em{font-style:normal;color:#FFD84A}
.giant{position:absolute;left:0;right:0;text-align:center;font:400 190px/0.9 Bangers;color:#FFD84A;text-shadow:0 0 30px rgba(255,216,74,.45)}
.sub{position:absolute;left:30px;right:30px;text-align:center;font:700 36px/1.2 Geist;color:#F4F1E8}
.sub em{font-style:normal;color:#FFD84A}
.row{position:absolute;left:44px;right:44px;height:66px;border-radius:10px;background:#16213A;border:3px solid #F4F1E8;font:700 30px/60px Geist;padding-left:18px;color:#F4F1E8;white-space:nowrap}
.row b{color:#FFD84A}
.fonte{position:absolute;left:28px;right:28px;bottom:22px;font:500 24px/1.25 Geist;color:#C9C3B2;z-index:3}
.card{position:absolute;border-radius:12px;box-shadow:0 12px 0 rgba(0,0,0,.45)}
.lbl{position:absolute;text-align:center;font:400 34px/1 Bangers;letter-spacing:1px;color:#F4F1E8}
.stamp{position:absolute;font:400 64px/1 Bangers;color:#FF5A4E;border:6px solid #FF5A4E;border-radius:10px;padding:4px 16px;background:rgba(15,23,42,.86);letter-spacing:2px;white-space:nowrap;z-index:4}
.hlbox{position:absolute;background:rgba(255,216,74,.38);border:3px solid #FFD84A;border-radius:6px;mix-blend-mode:normal}
.seat{position:absolute;width:150px;height:150px;border-radius:50%;border:6px solid #F4F1E8;background:#16213A;text-align:center;font:400 40px/1 Bangers;padding-top:30px}
.seat b{display:block;font-size:56px;color:#FFD84A}
.opt{position:absolute;left:40px;right:40px;height:250px;border:6px solid #F4F1E8;border-radius:18px;background:#16213A}
.opt .l{position:absolute;left:24px;top:22px;font:400 200px/1 Bangers;color:#FFD84A}
.opt .t{position:absolute;left:175px;right:20px;top:50%;transform:translateY(-50%);font:400 66px/0.95 Bangers;color:#F4F1E8}
.full{position:absolute;left:0;top:0;width:744px;height:1040px}
"""
CSS += """
.lv1{position:absolute;left:30px;right:30px;text-align:center;font:400 96px/0.95 Bangers;color:#FFD84A;letter-spacing:1px;text-shadow:0 0 24px rgba(255,216,74,.35)}
.lv2{position:absolute;left:40px;right:40px;text-align:center;font:700 34px/1.22 Geist;color:#F4F1E8}
.lv2 em{font-style:normal;color:#FFD84A}
.ex{position:absolute;right:30px;top:30px;z-index:3;background:#F4F1E8;color:#0F172A;font:700 24px/1 Geist;letter-spacing:2px;padding:8px 14px;border-radius:6px}
.st{position:absolute;width:156px;height:156px;border-radius:50%;border:6px solid #F4F1E8;background:#16213A;text-align:center;font:700 24px/1.1 Geist;padding-top:34px;color:#F4F1E8}
.st b{display:block;font:400 40px/1 Bangers;color:#6FE39A;margin-top:6px;letter-spacing:1px}
.st.dono{border-color:#FFD84A}.st.alvo{border-color:#FF5A4E;border-style:dashed}
"""
