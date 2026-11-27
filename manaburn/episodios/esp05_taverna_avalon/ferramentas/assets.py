"""Especial Taverna de Avalon: cenário 9:16 a partir da imagem do fundador e estandarte com a logo original."""
import sys, numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageOps
up, out = sys.argv[1], sys.argv[2]
# --- cenário 1080x1920 (coordenadas de ecrã no plano geral) ---
tav = Image.open(f'{up}/8b84753d-image.jpg').convert('RGB')
W, Y0 = 1080, 113
img = tav.resize((W, round(900*W/675)), Image.LANCZOS)          # 1080x1440, só escala uniforme
H = img.height
bg = Image.new('RGB', (W, 1920))
# faixas: espelho desfocado e escurecido da própria imagem (sem IA)
top = img.crop((0, 0, W, Y0)).transpose(Image.FLIP_TOP_BOTTOM).filter(ImageFilter.GaussianBlur(14))
bot = img.crop((0, H-(1920-Y0-H), W, H)).transpose(Image.FLIP_TOP_BOTTOM).filter(ImageFilter.GaussianBlur(18))
bg.paste(top, (0, 0)); bg.paste(bot, (0, Y0+H)); bg.paste(img, (0, Y0))
a = np.asarray(bg).astype(np.float32)
y = np.arange(1920)[:, None]
k = np.ones((1920, 1))
k[:Y0+40] = np.clip((y[:Y0+40]) / (Y0+40), 0, 1)**0.8 * 0.85 + 0.15
fb = Y0 + H - 60
k[fb:] = np.clip(1 - (y[fb:] - fb) / (1920 - fb), 0, 1)**1.2 * 0.85 + 0.15
# costura suave nas emendas
a *= k[..., None]
warm = np.array([5, 10, 16], np.float32)  # preto do BINDER por baixo
a = np.maximum(a, warm * (1 - k[..., None]))
Image.fromarray(a.clip(0, 255).astype(np.uint8)).save(f'{out}/taverna_916.jpg', quality=94)
# --- logo: fundo -> transparência, formas intactas ---
lg = Image.open(f'{up}/f4f2e6ce-image.png').convert('RGBA')
l = np.asarray(lg).astype(np.float32)
lum = l[..., :3].mean(-1); alpha = np.clip((255 - lum) / (255 - 35), 0, 1) * (l[..., 3] / 255)
logo = np.zeros_like(l); logo[..., :3] = 34; logo[..., 3] = alpha * 255   # mesma cor (#222) do original
logo = Image.fromarray(logo.astype(np.uint8)); bb = logo.getchannel('A').point(lambda v: 255 if v>8 else 0).getbbox(); logo = logo.crop(bb)
logo.save(f'{out}/avalon_logo.png')
# --- estandarte: madeira escura + miolo de pergaminho + logo original a preto ---
PW, PH = 360, 400
rng = np.random.default_rng(3)
plank = np.zeros((PH, PW, 3), np.float32)
grain = rng.normal(0, 1, (PH, 1)) ; grain = np.convolve(grain[:, 0], np.ones(9)/9, 'same')[:, None]
xs = np.arange(PW)[None, :]
plank[...] = np.array([74, 46, 26]) + 14*np.sin(xs/7 + grain*3)[..., None] * np.array([1, .7, .4])
board = Image.fromarray(plank.clip(0, 255).astype(np.uint8)).convert('RGBA')
d = ImageDraw.Draw(board)
d.rectangle([0, 0, PW-1, PH-1], outline=(34, 28, 23, 255), width=8)
m = 26
parch = np.zeros((PH-2*m, PW-2*m, 3), np.float32)
pv = rng.normal(0, 1, parch.shape[:2]); pv = np.asarray(Image.fromarray(((pv+3)*40).clip(0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))).astype(np.float32)/255
parch[...] = np.array([232, 218, 184]) - 26*pv[..., None]
yy, xx = np.mgrid[0:parch.shape[0], 0:parch.shape[1]]
cx, cy = parch.shape[1]/2, parch.shape[0]/2
vig = ((xx-cx)/cx)**2 + ((yy-cy)/cy)**2
parch *= (1 - 0.22*np.clip(vig-0.4, 0, 1))[..., None]
pa = Image.fromarray(parch.clip(0, 255).astype(np.uint8)).convert('RGBA')
board.paste(pa, (m, m))
d.rectangle([m-3, m-3, PW-m+2, PH-m+2], outline=(34, 28, 23, 255), width=4)
for (x, y_) in [(12, 12), (PW-13, 12), (12, PH-13), (PW-13, PH-13)]:
    d.ellipse([x-5, y_-5, x+5, y_+5], fill=(150, 140, 120, 255), outline=(34, 28, 23, 255), width=2)
lw = PW - 2*m - 36
lh = round(logo.height * lw / logo.width)
lr = logo.resize((lw, lh), Image.LANCZOS)
board.alpha_composite(lr, ((PW-lw)//2, (PH-lh)//2))
# corrente/haste
full = Image.new('RGBA', (PW, PH+70), (0, 0, 0, 0)); fd = ImageDraw.Draw(full)
fd.line([(PW*0.25, 70), (PW/2, 6)], fill=(60, 56, 52, 255), width=5); fd.line([(PW*0.75, 70), (PW/2, 6)], fill=(60, 56, 52, 255), width=5)
fd.ellipse([PW/2-9, 0, PW/2+9, 18], fill=(80, 74, 66, 255), outline=(34, 28, 23, 255), width=3)
full.alpha_composite(board, (0, 70))
full.save(f'{out}/estandarte.png')
print('ok', bb, full.size)
# --- margem lateral para os planos aproximados (espelho desfocado e escurecido, sem IA) ---
base = Image.open(f'{out}/taverna_916.jpg')
wide = Image.new('RGB', (1480, 1920))
L = base.crop((0, 0, 200, 1920)).transpose(Image.FLIP_LEFT_RIGHT).filter(ImageFilter.GaussianBlur(10))
R = base.crop((880, 0, 1080, 1920)).transpose(Image.FLIP_LEFT_RIGHT).filter(ImageFilter.GaussianBlur(10))
wide.paste(L, (0, 0)); wide.paste(R, (1280, 0)); wide.paste(base, (200, 0))
w = np.asarray(wide).astype(np.float32); xx = np.arange(1480)[None, :]
f = np.ones((1, 1480)); f[:, :200] = 0.55 + 0.45 * (xx[:, :200] / 200); f[:, 1280:] = 0.55 + 0.45 * ((1479 - xx[:, 1280:]) / 200)
Image.fromarray((w * f[..., None]).clip(0, 255).astype(np.uint8)).save(f'{out}/taverna_916_largo.jpg', quality=94)
