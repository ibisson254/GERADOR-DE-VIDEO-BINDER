# Conde de Manaforte · O Tribunal Estético · gerador da capa padrão (proposta de 14/11/2026; regras em conde/PERFIL.md «Capa»).
# Mesma estratégia das capas das outras séries (um ponto focal, 3 blocos de texto, a personagem a reagir, faixa fixa,
# tudo no recorte 3:4 da grelha, y 240–1680), traduzida para a linguagem do Conde: papel marfim, gravura a tinta, Lora,
# bordô de selo. A obra é a protagonista: arte inteira, emoldurada como num museu, sem nada por cima.
#
# Ordem de leitura: 1) a obra (o réu) → 2) frase, a acusação, em itálico → 3) foco, o veredito numa palavra, dentro do
# carimbo bordô → 4) o Conde, no medalhão, a reagir → 5) faixa fixa «O TRIBUNAL ESTÉTICO · Nº 00X» + «RÉU DE ANO».
#
# Uso:
#   python3 capa_cm.py --scryfall ice/133 --frase "Pediram um espírito. Veio um" --foco "LÊMURE" \
#                      --expressao desconfiado --processo 5 --saida CM_EP005_CAPA.png
#   (ou --arte caminho.jpg com o art_crop; --ano força o ano do réu). Gera também *_grelha.png.
# Requer Lora (google-fonts) e Pillow.
import argparse, json, pathlib, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

ap = argparse.ArgumentParser()
ap.add_argument('--arte'); ap.add_argument('--scryfall', help='SET/Nº, ex.: ice/133 (usa o art_crop)')
ap.add_argument('--frase', required=True, help='a acusação, 3–7 palavras')
ap.add_argument('--foco', required=True, help='o veredito: 1 palavra')
ap.add_argument('--expressao', default='desconfiado', choices=['neutro', 'desconfiado', 'indignado', 'admirado'])
ap.add_argument('--processo', type=int, required=True); ap.add_argument('--ano', default='')
ap.add_argument('--saida', required=True)
a = ap.parse_args()

W, H = 1080, 1920
INK = (17, 17, 17); PAPER = (244, 240, 230); GREY = (119, 115, 108); BORDO = (118, 47, 50)
here = pathlib.Path(__file__).resolve().parent; tmp = pathlib.Path(tempfile.gettempdir())
GF = '/usr/share/fonts/truetype/google-fonts/'
def F(size, var='Bold', italic=False):
    f = ImageFont.truetype(GF + ('Lora-Italic-Variable.ttf' if italic else 'Lora-Variable.ttf'), size)
    f.set_variation_by_name(var); return f

if a.scryfall:
    sett, num = a.scryfall.split('/')
    info = json.loads(subprocess.run(['curl', '-sS', '-H', 'User-Agent: BinderStudio/1.0', '-H', 'Accept: application/json',
                                      f'https://api.scryfall.com/cards/{sett}/{num}'], capture_output=True, text=True).stdout)
    uri = (info.get('image_uris') or info['card_faces'][0]['image_uris'])['art_crop']
    a.arte = str(tmp / f'{sett}_{num}_art.jpg'); subprocess.run(['curl', '-sS', '-o', a.arte, uri], check=True)
    a.ano = a.ano or info['released_at'][:4]
    print(f"Réu: {info['name']} ({info['set_name']}, {info['released_at'][:4]}), nº {info['collector_number']}. Arte: {info.get('artist')}.")

# --- papel com grão (o mesmo do montador) ---
im = Image.new('RGB', (W, H), PAPER)
n = Image.effect_noise((W // 2, H // 2), 18).resize((W, H), Image.BICUBIC).point(lambda v: 128 + (v - 128) * 0.35)
im = ImageChops.multiply(im, Image.merge('RGB', (n, n, n)).point(lambda v: min(255, v + 120))).convert('RGBA')
d = ImageDraw.Draw(im)

# --- 1) a obra: inteira, emoldurada (moldura dupla a tinta + passe-partout), nada por cima ---
art = Image.open(a.arte).convert('RGB')
AX0, AX1, AY0 = 84, W - 84, 300
aw = AX1 - AX0; ah = round(art.height * aw / art.width)
im.paste(art.resize((aw, ah), Image.LANCZOS), (AX0, AY0))
d.rectangle((AX0 - 4, AY0 - 4, AX1 + 3, AY0 + ah + 3), outline=INK, width=4)
d.rectangle((AX0 - 30, AY0 - 30, AX1 + 29, AY0 + ah + 29), outline=INK, width=6)
d.rectangle((AX0 - 40, AY0 - 40, AX1 + 39, AY0 + ah + 39), outline=INK, width=2)
art_bottom = AY0 + ah + 40

# --- 2) frase: a acusação, itálico, tinta ---
def fit(s, size, maxw, **k):
    while d.textlength(s, font=F(size, **k)) > maxw and size > 30: size -= 2
    return size
fy = art_bottom + 78
d.text((W / 2, fy), a.frase, font=F(fit(a.frase, 64, 940, var='SemiBold Italic', italic=True), 'SemiBold Italic', True),
       fill=INK, anchor='mm')

# --- 4) o Conde no medalhão, a reagir (à esquerda, sob a obra) ---
ex = Image.open(here.parent / 'assets' / f'{a.expressao}.png').convert('RGB')
mw, mh = 250, 288
ex = ex.resize((mw, round(ex.height * mw / ex.width)), Image.LANCZOS); top = max(0, (ex.height - mh) // 3)
ex = ex.crop((0, top, mw, top + mh))
cy = fy + 70 + mh // 2 + 14
mx, my = 70, cy - mh // 2
m = Image.new('L', (mw, mh), 0); ImageDraw.Draw(m).ellipse((0, 0, mw - 1, mh - 1), fill=255)
d.ellipse((mx - 14, my - 14, mx + mw + 13, my + mh + 13), fill=PAPER, outline=INK, width=5)
im.paste(ex, (mx, my), m)
d.ellipse((mx - 3, my - 3, mx + mw + 2, my + mh + 2), outline=INK, width=3)

# --- 3) foco: o veredito, gigante, dentro do carimbo bordô (gasto, inclinado) ---
sw, sh = 640, 270
st = Image.new('RGBA', (sw, sh), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
sd.rounded_rectangle((6, 6, sw - 7, sh - 7), 22, outline=BORDO, width=10)
sd.rounded_rectangle((24, 24, sw - 25, sh - 25), 12, outline=BORDO, width=3)
foco = a.foco.upper(); fs = 170
while sd.textlength(foco, font=F(fs)) > sw - 90 and fs > 60: fs -= 4
sd.text((sw / 2, sh / 2 + 6), foco, font=F(fs), fill=BORDO, anchor='mm')
wear = Image.effect_noise((sw, sh), 55).point(lambda v: 255 if v > 40 else 0)
st.putalpha(ImageChops.multiply(st.getchannel('A'), wear))
st = st.rotate(-7, expand=True, resample=Image.BICUBIC)
im.alpha_composite(st, (W - 50 - st.width, cy - st.height // 2))

# --- 5) faixa fixa da série ---
d = ImageDraw.Draw(im)
d.rectangle((0, 1572, W, 1666), fill=INK); d.line((0, 1580, W, 1580), fill=PAPER, width=1); d.line((0, 1658, W, 1658), fill=PAPER, width=1)
d.text((60, 1619), f'O TRIBUNAL ESTÉTICO  ·  Nº {a.processo:03d}', font=F(40), fill=PAPER, anchor='lm')
if a.ano: d.text((W - 60, 1619), f'réu de {a.ano}', font=F(38, 'SemiBold Italic', True), fill=(214, 160, 150), anchor='rm')

im.convert('RGB').save(a.saida)
im.convert('RGB').crop((0, 240, W, 1680)).save(a.saida.replace('.png', '_grelha.png'))
print(a.saida)
