# Mana & Burn · gerador da capa padrão (modelo fixo desde 14/11/2026; regras em manaburn/PERFIL.md, secção «Capa»).
# A carta principal do episódio ocupa a largura toda (arte livre em cima); frase + foco por cima do texto de regras;
# um selo vermelho com o dado-chave; faixa fixa da série em baixo. Tudo dentro do recorte 3:4 da grelha (y 240–1680).
#
# Uso:
#   python3 capa_mb.py --scryfall cmd/215 --frase "O DRAGÃO QUE COME" --foco "TERRENO" --selo "−2 POR PANCADA" \
#                      --ep 11 --tag COMMANDER --saida MB_EP11_CAPA.png
#   (ou --carta caminho.png em vez de --scryfall SET/Nº). Gera também *_grelha.png (pré-visualização do recorte).
# Fonte: Bangers (node_modules/@fontsource/bangers); convertida de woff2 automaticamente se faltar o .ttf.
import argparse, json, pathlib, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ap = argparse.ArgumentParser()
ap.add_argument('--carta'); ap.add_argument('--scryfall', help='SET/Nº, ex.: cmd/215')
ap.add_argument('--frase', required=True); ap.add_argument('--foco', required=True)
ap.add_argument('--selo', default=''); ap.add_argument('--ep', required=True); ap.add_argument('--tag', default='')
ap.add_argument('--saida', required=True); ap.add_argument('--selo-y', type=int, default=860)
a = ap.parse_args()
W, H = 1080, 1920
YEL = (255, 216, 74); RED = (226, 59, 46); INK = (18, 14, 12); WHITE = (250, 246, 236)
here = pathlib.Path(__file__).resolve().parent; tmp = pathlib.Path(tempfile.gettempdir())
ttf = tmp / 'Bangers.ttf'
if not ttf.exists():
    from fontTools.ttLib import TTFont   # precisa de fonttools + brotli
    f = TTFont(str(here.parent / 'node_modules/@fontsource/bangers/files/bangers-latin-400-normal.woff2')); f.flavor = None; f.save(str(ttf))
F = lambda s: ImageFont.truetype(str(ttf), s)
if a.scryfall:   # imagem «png» de maior resolução (745×1040) do Scryfall
    sett, num = a.scryfall.split('/')
    info = json.loads(subprocess.run(['curl', '-sS', '-H', 'User-Agent: BinderStudio/1.0', '-H', 'Accept: application/json',
                                      f'https://api.scryfall.com/cards/{sett}/{num}'], capture_output=True, text=True).stdout)
    uri = (info.get('image_uris') or info['card_faces'][0]['image_uris'])['png']
    a.carta = str(tmp / f'{sett}_{num}.png'); subprocess.run(['curl', '-sS', '-o', a.carta, uri], check=True)
    print(f"Carta: {info['name']} ({info['set_name']}), nº {info['collector_number']}. Arte: {info.get('artist')}.")
im = Image.new('RGBA', (W, H), INK + (255,))
c = Image.open(a.carta).convert('RGBA'); c = c.resize((W, int(c.height * W / c.width)), Image.LANCZOS)
im.alpha_composite(c, (0, 210))
g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
for y in range(980, H):   # escurece o texto de regras: as letras vivem aí, a arte fica livre
    gd.line((0, y, W, y), fill=INK + (int(235 * min(1, (y - 980) / 160)),))
top = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(top).rectangle((0, 0, W, 300), fill=INK + (200,))
im.alpha_composite(g); im.alpha_composite(top.filter(ImageFilter.GaussianBlur(30)))
d = ImageDraw.Draw(im)
def fit(s, size, maxw):
    while ImageDraw.Draw(im).textlength(s, font=F(size)) > maxw and size > 40: size -= 4
    return size
def txt(xy, s, size, fill, anchor='mm', stroke=10):
    d.text(xy, s, font=F(size), fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=INK)
txt((W / 2, 1185), a.frase.upper(), fit(a.frase.upper(), 118, 980), WHITE)                     # 1) frase
fs = fit(a.foco.upper(), 290, 1000)
gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(gl).text((W / 2, 1395), a.foco.upper(), font=F(fs), fill=YEL + (190,), anchor='mm')
im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(26))); d = ImageDraw.Draw(im)
txt((W / 2, 1395), a.foco.upper(), fs, YEL, stroke=14)                                          # 2) foco
if a.selo:                                                                                       # 3) selo sobre a arte
    ss = fit(a.selo.upper(), 66, 380); wd = d.textlength(a.selo.upper(), font=F(ss)) + 50
    d.rounded_rectangle((W - 50 - wd, a.selo_y, W - 50, a.selo_y + 100), 20, fill=RED, outline=INK, width=7)
    txt((W - 50 - wd / 2, a.selo_y + 51), a.selo.upper(), ss, WHITE, stroke=5)
d.rectangle((0, 1572, W, H), fill=INK); d.line((0, 1572, W, 1572), fill=YEL, width=6)            # 4) faixa fixa da série
txt((60, 1619), f'MANA & BURN · EP. {a.ep}', 62, YEL, anchor='lm', stroke=0)
if a.tag: txt((W - 60, 1619), a.tag.upper(), 62, WHITE, anchor='rm', stroke=0)
im.convert('RGB').save(a.saida)
im.convert('RGB').crop((0, 240, W, 1680)).save(a.saida.replace('.png', '_grelha.png'))
