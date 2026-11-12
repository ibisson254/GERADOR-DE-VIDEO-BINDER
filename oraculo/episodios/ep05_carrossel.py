# Meta em Curto EP05 · carrossel derivado «guia de bolso do pré-release» (9 slides 1080×1350)
# Uso, a partir da raiz do kit:  python3 -I oraculo/episodios/ep05_carrossel.py . saida/
# Todos os números saem de oraculo/ep05/resultados/*.json e dados/*.csv (os mesmos do vídeo).
# Previsão no formato do Protocolo de Pré-Release (oraculo/PROTOCOLO_PRE_RELEASE.md): grau de certeza 1–5, sem %.
import csv, json, os, sys
from PIL import Image, ImageDraw, ImageFont
K = (sys.argv[1] if len(sys.argv) > 1 else '.').rstrip('/') + '/'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'carrossel_ep05'; os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1350; N = 9
_fc = {}
def F(p, s):
    if (p, s) not in _fc: _fc[(p, s)] = ImageFont.truetype(p, s)
    return _fc[(p, s)]
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'; MONOB = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
COND = '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf'; CONDB = '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf'
INTB = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
BG = (5, 10, 16); EM = (16, 185, 129); PH = (0, 255, 65); WHITE = (236, 241, 245); GREY = (120, 140, 150)
AMBER = (255, 176, 32); NAVY = (15, 23, 42); SRC = (150, 170, 175)
def fit(d, s, path, size, maxw):
    while size > 20 and d.textlength(s, font=F(path, size)) > maxw: size -= 2
    return F(path, size)
def br(v, c=1): return f'{v:.{c}f}'.replace('.', ',')

SD = K + 'oraculo/ep05/'
PR = json.load(open(SD + 'resultados/prob.json')); PO = json.load(open(SD + 'resultados/pools.json'))['pares']
TRO = list(csv.DictReader(open(SD + 'dados/trofeus_sealed_untapped.csv')))
CARTA = Image.open(SD + 'cartas/uss_enterprise_a.png').convert('RGBA')
MASTER = Image.open(K + 'oraculo/assets/tubo_mestra_916.png').convert('RGB')
NAVY = MASTER.getpixel((4, 440))  # fundo dos slides «fora do tubo» = fundo da imagem-mestra
AB = PR['abertura']; SY = PR['sinergia']['T5_jogando']
P_AB, P_T5 = AB['mitica_especifica_6'], SY['bomba_1_copia']; JOGOS = round(1 / (P_AB * P_T5 / 1e4))
assert JOGOS == 96

def tubo(escala):  # personagem inteiro (imagem-mestra, sem regenerar), recorte só em cima e em baixo
    c = MASTER.crop((0, 395, 1080, 1745)); return c.resize((int(1080 * escala), int(1350 * escala)), Image.LANCZOS)

def base(n, titulo, fora=False):
    im = Image.new('RGB', (W, H), NAVY if fora else BG); d = ImageDraw.Draw(im, 'RGBA')
    if not fora:
        for y in range(0, H, 4): d.line((0, y, W, y), fill=(0, 0, 0, 50))
    if titulo:
        d.text((70, 60), '> ' + titulo, font=fit(d, '> ' + titulo, MONOB, 36, W - 140), fill=PH)
        d.line((70, 116, W - 70, 116), fill=EM, width=2)
    d.ellipse((70, 1262, 88, 1280), fill=EM)
    d.text((100, 1271), 'BINDER', font=F(MONOB, 26), fill=EM, anchor='lm')
    d.text((W - 70, 1271), f'META EM CURTO · EP05 · {n}/{N}', font=F(MONO, 24), fill=GREY, anchor='rm')
    return im, d
def fonte(d, linhas, y=None):  # corpo 28 fixo (>= 24 px de letra): quebra a linha em vez de encolher
    f = F(COND, 28); out = []
    for s in linhas:
        cur = ''
        for w in s.split(' '):
            t = (cur + ' ' + w).strip()
            if d.textlength(t, font=f) > W - 140: out.append(cur); cur = w
            else: cur = t
        out.append(cur)
    y = y if y is not None else 1222 - 38 * len(out)
    for i, s in enumerate(out): d.text((70, y + i * 38), s, font=f, fill=SRC)
def carimbo(d, txt, y, col=AMBER, x=None):
    f = F(MONOB, 34); w = d.textlength(txt, font=f) + 40; x = x if x is not None else (W - w) / 2
    d.rounded_rectangle((x, y, x + w, y + 64), 8, outline=col, width=4); d.text((x + w / 2, y + 32), txt, font=f, fill=col, anchor='mm')
def barra(d, y, rot, val, vmax, cor, txt, x0=70, wmax=640, h=64):
    d.text((x0, y - 6), rot, font=fit(d, rot, CONDB, 34, 900), fill=WHITE, anchor='ls')
    d.rectangle((x0, y + 8, x0 + wmax, y + 8 + h), fill=(14, 30, 30))
    d.rectangle((x0, y + 8, x0 + int(wmax * val / vmax), y + 8 + h), fill=cor)
    d.text((x0 + wmax + 24, y + 8 + h / 2), txt, font=F(INTB, 54), fill=cor, anchor='lm')
def medidor(d, y, n, rot):
    d.text((W / 2, y), 'GRAU DE CERTEZA', font=F(MONOB, 30), fill=GREY, anchor='ma')
    x0 = (W - (5 * 90 - 20)) / 2
    for s in range(5): d.rounded_rectangle((x0 + s * 90, y + 50, x0 + s * 90 + 70, y + 96), 8, fill=(EM if s < n else None), outline=EM, width=3)
    d.text((W / 2, y + 118), rot, font=F(MONOB, 34), fill=EM, anchor='ma')
CRED = 'U.S.S. Enterprise-A, Free Spirit · TRK 43 · arte: Evan Shipard · © Wizards of the Coast · Star Trek © CBS'

# 1 · capa (fora do tubo)
im, d = base(1, None, fora=True)
d.text((70, 70), 'PRÉ-RELEASE DE STAR TREK', font=F(MONOB, 34), fill=PH)
for i, s in enumerate(['A bomba que você quer', 'aparece em', f'1 jogo em {JOGOS}.']):
    d.text((70, 130 + i * 92), s, font=fit(d, s, INTB, 84, W - 140), fill=(PH if i == 2 else WHITE))
t = tubo(0.62); im.paste(t, ((W - t.width) // 2, 420))
d = ImageDraw.Draw(im, 'RGBA')
d.text((70, 1180), 'Guia de bolso do TUBO para a mesa  →', font=fit(d, 'Guia de bolso do TUBO para a mesa  →', CONDB, 40, W - 140), fill=EM)
im.save(f'{OUT}/01_capa.png')

# 2 · a bomba
im, d = base(2, 'CONTA 1 · A BOMBA')
cw = 360; ch = int(cw * CARTA.height / CARTA.width); c = CARTA.resize((cw, ch), Image.LANCZOS); im.paste(c, (70, 150), c)
d = ImageDraw.Draw(im, 'RGBA'); x = 470
for y, a, b, col in [(170, f'{br(P_AB)}%', 'de abrir esta mítica\nem 6 boosters', WHITE), (390, f'{br(P_T5)}%', 'de vê-la até o turno 5,\nse abrir', WHITE)]:
    d.text((x, y), a, font=F(INTB, 96), fill=col); d.multiline_text((x, y + 112), b, font=F(CONDB, 34), fill=GREY, spacing=6)
d.text((W / 2, 700), 'juntando as duas:', font=F(MONO, 34), fill=GREY, anchor='ma')
d.text((W / 2, 750), f'1 jogo em {JOGOS}', font=F(INTB, 130), fill=PH, anchor='ma')
d.text((W / 2, 910), 'Não construa o deck em volta dela.', font=fit(d, 'Não construa o deck em volta dela.', CONDB, 44, W - 140), fill=WHITE, anchor='ma')
fonte(d, ['cálculo: colação oficial (Wizards, Collecting Star Trek) + hipergeométrica', 'premissas: taxa igual entre as 25 míticas; 40 cartas, 1 cópia, jogando primeiro', CRED])
im.save(f'{OUT}/02_bomba.png')

# 3 · a estrutura
im, d = base(3, 'CONTA 2 · A ESTRUTURA')
d.text((70, 150), 'Ver até o turno 5 (40 cartas, jogando primeiro):', font=fit(d, 'Ver até o turno 5 (40 cartas, jogando primeiro):', CONDB, 36, W - 140), fill=GREY)
for i, (rot, v, col) in enumerate([('1 carta única', SY['bomba_1_copia'], GREY), ('7 cartas com a mesma função', SY['>=1_de_7'], PH),
                                   ('1 payoff + 8 peças (motor ligado)', SY['unico_payoff_8_peças'], GREY), ('4 payoffs + 8 peças (motor ligado)', SY['4_payoffs_8_peças'], PH)]):
    barra(d, 270 + i * 165 + (40 if i >= 2 else 0), rot, v, 100, col, f'{br(v)}%')
d.text((W / 2, 980), 'Redundância liga o motor.', font=F(INTB, 64), fill=WHITE, anchor='ma')
d.text((W / 2, 1060), 'Carta única é sorte.', font=F(INTB, 64), fill=PH, anchor='ma')
fonte(d, ['cálculo: hipergeométrica, sem mulligan · tabelas em oraculo/ep05/resultados'])
im.save(f'{OUT}/03_estrutura.png')

# 4 · cores e terrenos (listas de troféu)
im, d = base(4, 'CONTA 3 · DUAS CORES, 17 TERRENOS')
n = len(TRO); c2 = [r for r in TRO if len(r['cores']) == 2]; c3 = [r for r in TRO if len(r['cores']) >= 3]
def ok(rs): return sum(1 for r in rs if int(r['recorde'].split('-')[1]) <= 1)
t17 = sum(1 for r in TRO if r['terrenos'] == '17')
assert (n, len(c2), len(c3), ok(c2), ok(c3), t17) == (69, 58, 11, 26, 1, 60), (n, len(c2), len(c3), ok(c2), ok(c3), t17)
d.text((70, 150), f'{n} listas de troféu de Sealed do Arena, 9 coleções:', font=fit(d, f'{n} listas de troféu de Sealed do Arena, 9 coleções:', CONDB, 36, W - 140), fill=GREY)
for i, (rot, v, txt, col) in enumerate([('com 2 cores', len(c2), str(len(c2)), PH), ('com 3 cores ou mais', len(c3), str(len(c3)), GREY), ('com 17 terrenos', t17, str(t17), PH)]):
    barra(d, 280 + i * 150, rot, v, n, col, txt)
d.text((70, 760), f'Até 1 derrota: {ok(c2)} de {len(c2)} com 2 cores.', font=fit(d, 'x' * 40, CONDB, 44, W - 140), fill=WHITE)
d.text((70, 830), f'Até 1 derrota: {ok(c3)} de {len(c3)} com 3 cores.', font=fit(d, 'x' * 40, CONDB, 44, W - 140), fill=WHITE)
carimbo(d, 'PADRÃO, NÃO CAUSA', 930)
fonte(d, ['fonte: Untapped.gg, Sealed Trophy Decks (05/11/2026) · só vencedores, sem grupo de controle', 'coleções anteriores: Star Trek ainda não tem listas de troféu'])
im.save(f'{OUT}/04_cores.png')

# 5 · remoção por par (modelo)
im, d = base(5, 'CONTA 4 · REMOÇÃO')
d.text((70, 140), 'A Wizards pede 5 remoções.', font=F(INTB, 56), fill=WHITE)
d.text((70, 215), 'Remoções no pool, nas cores do par (média):', font=fit(d, 'Remoções no pool, nas cores do par (média):', CONDB, 34, W - 140), fill=GREY)
pares = sorted(PO.values(), key=lambda v: -v['remocao']); x0, wmax = 300, 560; vmax = 6.5
lx = x0 + int(wmax * 5 / vmax); d.line((lx, 312, lx, 320 + 10 * 62), fill=AMBER, width=4); d.text((lx + 10, 940), '5', font=F(MONOB, 30), fill=AMBER, anchor='lt')
for i, v in enumerate(pares):
    y = 320 + i * 62; col = PH if v['remocao'] >= 5 else GREY
    d.text((x0 - 20, y + 25), v['nome'], font=F(CONDB, 36), fill=WHITE, anchor='rm')
    d.rectangle((x0, y + 4, x0 + int(wmax * v['remocao'] / vmax), y + 46), fill=col)
    tx = x0 + int(wmax * v['remocao'] / vmax) + 16; tw = d.textlength(br(v['remocao']), font=F(MONOB, 32))
    d.rectangle((tx - 6, y + 6, tx + tw + 6, y + 44), fill=BG); d.text((tx, y + 25), br(v['remocao']), font=F(MONOB, 32), fill=col, anchor='lm')
carimbo(d, 'MODELO, NÃO JOGO', 1000, x=70)
fonte(d, ['Wizards, guia de pré-release (30/10/2026): "at least five removal spells"', 'modelo: 40 mil pools com a colação oficial; remoção marcada à mão sobre o Oracle'])
im.save(f'{OUT}/05_remocao.png')

# 6 · naves
im, d = base(6, 'CONTA 5 · A NAVE PARADA')
d.text((70, 150), 'Só 5 de 27', font=F(INTB, 120), fill=PH)
d.multiline_text((70, 300), 'remoções comuns e incomuns\nacertam uma nave que não é criatura.', font=F(CONDB, 46), fill=WHITE, spacing=10)
d.text((70, 460), 'Guarde estas para ela:', font=F(MONOB, 34), fill=GREY)
for i, s in enumerate(['70,000 Light-Years from Home', 'Malfunctioning Holodeck', 'Guidance Failure', 'Marooned', 'Rules of Acquisition']):
    d.text((110, 530 + i * 74), '▸ ' + s, font=fit(d, '▸ ' + s, CONDB, 46, W - 200), fill=PH)
fonte(d, ['contagem sobre o texto Oracle (Scryfall, set trk, 05/11/2026)', 'Wizards, guia de pré-release: remoção de artefato "especially valuable"'])
im.save(f'{OUT}/06_naves.png')

# 7 · Draft ≠ Sealed
im, d = base(7, 'AVISO · NÃO COPIE O MUNDIAL')
d.multiline_text((70, 150), 'O Mundial (13–15/11)\né Draft. O pré-release\né Sealed.', font=F(INTB, 72), fill=WHITE, spacing=14)
d.text((70, 470), 'Na coleção anterior, Reality Fracture:', font=fit(d, 'Na coleção anterior, Reality Fracture:', CONDB, 38, W - 140), fill=GREY)
for x, rot, pos, col in [(150, 'DRAFT', '3.º', PH), (630, 'SEALED', '9.º', AMBER)]:
    d.rounded_rectangle((x, 550, x + 300, 850), 18, outline=col, width=4, fill=(10, 24, 24))
    d.text((x + 150, 580), rot, font=F(MONOB, 34), fill=GREY, anchor='ma'); d.text((x + 150, 650), pos, font=F(INTB, 120), fill=col, anchor='ma')
    d.text((x + 150, 800), 'Gruul', font=F(CONDB, 38), fill=WHITE, anchor='ma')
d.text((540, 700), '→', font=F(INTB, 90), fill=GREY, anchor='mm')
d.text((W / 2, 930), 'O ranking de um formato não serve ao outro.', font=fit(d, 'O ranking de um formato não serve ao outro.', CONDB, 44, W - 140), fill=WHITE, anchor='ma')
fonte(d, ['magic.gg, ficha do World Championship 32 · Reality Fracture: note.com (18/10/2026),', 'Draft 17Lands via Portent Lab, Sealed MTGMeta · outro set: método, não prova sobre Star Trek'])
im.save(f'{OUT}/07_draft.png')

# 8 · previsão registrada (fora do tubo)
im, d = base(8, None, fora=True)
d.text((70, 70), 'PREVISÃO REGISTRADA · PR-TRK-01', font=F(MONOB, 34), fill=PH)
d.multiline_text((70, 130), 'Rakdos no top 3 de win rate\ndo Sealed de Star Trek.', font=F(INTB, 64), fill=WHITE, spacing=12)
d.text((70, 300), 'Fonte da auditoria: 17Lands · data: 01/12/2026', font=fit(d, 'Fonte da auditoria: 17Lands · data: 01/12/2026', CONDB, 36, W - 140), fill=GREY)
t = tubo(0.42); im.paste(t, (70, 370)); d = ImageDraw.Draw(im, 'RGBA')
x = 70 + t.width + 30; br_ = PO['BR']['motor_T5']
d.text((x, 420), 'Motor ligado até o T5', font=F(CONDB, 34), fill=GREY)
for i, k in enumerate(['BR', 'WB', 'UB']):
    v = PO[k]; d.text((x, 480 + i * 92), f"{v['nome']} {round(v['motor_T5'])}", font=F(INTB, 64), fill=(PH if k == 'BR' else WHITE))
d.text((x, 770), 'em 100 pools simulados', font=F(CONDB, 30), fill=GREY)
medidor(d, 870, 2, 'BAIXO')
d.text((W / 2, 1040), 'Se eu errar, assumo.', font=F(INTB, 48), fill=WHITE, anchor='ma')
fonte(d, ['modelo: 40 mil pools + notas pré-lançamento (MTG Arena Zone, Draftsim): não é win rate'], 1146)
im.save(f'{OUT}/08_previsao.png')

# 9 · pergunta
im, d = base(9, 'SUA VEZ')
d.multiline_text((W / 2, 170), 'Abriu uma mítica fora\ndo seu melhor par.', font=F(INTB, 72), fill=WHITE, anchor='ma', align='center', spacing=14)
for i, s in enumerate(['A · joga a bomba', 'B · joga a estrutura', 'C · splash']):
    y = 430 + i * 140
    d.rounded_rectangle((140, y, W - 140, y + 108), 54, outline=EM, width=4, fill=(10, 30, 24))
    d.text((W / 2, y + 54), s, font=F(MONOB, 46), fill=EM, anchor='mm')
d.text((W / 2, 880), 'Responda com uma letra.', font=F(CONDB, 40), fill=GREY, anchor='ma')
d.text((W / 2, 960), 'Guarde para a mesa do pré-release.', font=F(CONDB, 44), fill=WHITE, anchor='ma')
d.text((W / 2, 1060), 'Probabilidade calculada. Humanos, imprevisíveis.', font=fit(d, 'Probabilidade calculada. Humanos, imprevisíveis.', MONOB, 34, W - 140), fill=PH, anchor='ma')
d.text((W / 2, 1150), 'META EM CURTO · com TUBO · BINDER Originals', font=F(MONO, 26), fill=GREY, anchor='ma')
im.save(f'{OUT}/09_pergunta.png')
print('ok', OUT)
