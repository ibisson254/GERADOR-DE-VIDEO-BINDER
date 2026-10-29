# Meta em Curto EP02 · carrossel derivado (5 slides 1080×1350) + capa 1080×1920
# Correr na pasta de trabalho do EP02 (mesmos ficheiros que ep02_render.py):
#   python3 ep02_carrossel.py /caminho/do/kit
import sys, os
sys.argv = [sys.argv[0], sys.argv[1] if len(sys.argv) > 1 else '../..']
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
import ep02_render as R
from PIL import Image, ImageDraw
W, H = 1080, 1350
F = R.F
def base(n, titulo):
    im = Image.new('RGB', (W, H), R.BG); d = ImageDraw.Draw(im, 'RGBA')
    for y in range(0, H, 4): d.line((0, y, W, y), fill=(0, 0, 0, 50))
    d.text((70, 60), '> ' + titulo, font=F(R.MONOB, 36), fill=R.PH)
    d.line((70, 116, W - 70, 116), fill=R.EM, width=2)
    d.ellipse((70, 1262, 88, 1280), fill=R.EM)
    d.text((100, 1271), 'BINDER', font=F(R.MONOB, 26), fill=R.EM, anchor='lm')
    d.text((W - 70, 1271), f'META EM CURTO · EP02 · {n}/5', font=F(R.MONO, 24), fill=R.GREY, anchor='rm')
    return im, d
def fonte(d, linhas, y=1170):
    for i, s in enumerate(linhas):
        d.text((70, y + i * 40), s, font=R.fit(d, s, R.COND, 30, W - 140), fill=(150, 170, 175))
out = 'carrossel_ep02'; os.makedirs(out, exist_ok=True)
# 1 · fichas dos finalistas
im, d = base(1, 'FINAL · MAGIC SPOTLIGHT: FRACTURE')
d.text((70, 140), 'Standard · 23–25 out 2026 · SCG CON Hartford', font=F(R.MONO, 28), fill=R.EM)
for x, nome, linhas, dest in [(70, 'VON STANGE', [('JUND SACRIFICE', R.PH), ('SEED 3 · 1.º LUGAR', R.WHITE), ('11-0 NO ARRANQUE', R.WHITE), ('SUÍÇO 12-2-1 (1 ID)', R.GREY), ('CAMPEÃO RC CHIBA 2023', R.EM)], True),
                              (560, 'OTT', [('JESKAI ARTIFACTS', R.WHITE), ('SEED 1 · 2.º LUGAR', R.PH), ('MESA À FRENTE NOS', R.WHITE), ('DOIS JOGOS DA FINAL', R.WHITE)], False)]:
    d.rounded_rectangle((x, 210, x + 450, 1110), 18, outline=R.EM, width=3, fill=(8, 20, 18))
    d.text((x + 24, 232), 'FICHA DE JOGADOR', font=F(R.MONOB, 24), fill=R.GREY)
    R.silhueta(d, x + 121, 290, col=(R.PH if dest else R.EM))
    d.text((x + 225, 490), nome, font=R.fit(d, nome, R.INTB, 64, 400), fill=R.WHITE, anchor='ma')
    y = 600
    for s, c in linhas:
        d.text((x + 225, y), s, font=R.fit(d, s, R.CONDB, 34, 400), fill=c, anchor='ma'); y += 70
fonte(d, ['fonte: Star City Games, relato da final (25/10/2026)', 'silhuetas: sem fotos de jogadores, por regra da série'])
im.save(f'{out}/01_finalistas.png')
# 2 · lista completa (principal + reserva)
im, d = base(2, 'LISTA · VON STANGE · JUND SACRIFICE')
L = R.LISTA['von_stange']; grupos = list(L['principal'].items()) + [('RESERVA (15)', L['reserva'])]
cols = [grupos[:4], grupos[4:]]
for ci, col in enumerate(cols):
    x = 70 if ci == 0 else 570; y = 150
    for g, cartas in col:
        d.text((x, y), g, font=F(R.MONOB, 24), fill=R.GREY); y += 36
        for n, nome in cartas:
            key = nome in L['chave']; s = f'{n} {nome}'
            d.text((x, y), s, font=R.fit(d, s, R.CONDB, 28, 460), fill=(R.PH if key else (150, 200, 175))); y += 36
        y += 12
fonte(d, ['fonte: Star City Games, lista do campeão · 60 + 15 cartas', 'a verde: as três cartas do motor'])
im.save(f'{out}/02_lista.png')
# 3 · as três cartas-chave
im, d = base(3, 'AS TRÊS PEÇAS')
for i, k in enumerate(['biotech_specialist', 'the_sackvillebagginses', 'lively_dirge']):
    c = R.CARDS[k]; w = 300; h = int(w * c.height / c.width); c = c.resize((w, h), Image.LANCZOS)
    x = 70 + i * 335; im.paste(c, (x, 170), c)
d = ImageDraw.Draw(im, 'RGBA')
for i, s in enumerate(['Biotech: artefato sacrificado → 2 de dano', 'Sackville: ficha sacrificada → perde 1 de vida',
                       'Dirge: põe 1 carta do deck no cemitério', 'e devolve até 2 criaturas (VM total ≤ 4)']):
    d.text((70, 640 + i * 66), s, font=R.fit(d, s, R.CONDB, 40, W - 140), fill=(R.PH if i == 3 else R.WHITE))
fonte(d, ['texto Oracle via Scryfall (29/10/2026) · Cartas © Wizards of the Coast', 'Biotech Specialist EOE 214, arte Alexandre Honoré',
          'The Sackville-Bagginses HOB 83, arte Denman Rooke', 'Lively Dirge OTJ 93, arte Warren Mahy'], 1040)
im.save(f'{out}/03_pecas.png')
# 4 · a conta do sacrifício
im, d = base(4, 'A CONTA DO SACRIFÍCIO')
c = R.CARDS['treasure']; w = 380; h = int(w * c.height / c.width); c = c.resize((w, h), Image.LANCZOS); im.paste(c, ((W - w) // 2, 160), c)
d = ImageDraw.Draw(im, 'RGBA'); y = 160 + h + 40
for s, col in [('TESOURO = ARTEFATO + FICHA', R.WHITE), ('+2  Biotech Specialist (artefato)', R.EM), ('+1  The Sackville-Bagginses (ficha)', R.EM)]:
    d.text((W / 2, y), s, font=R.fit(d, s, R.MONOB, 40, W - 140), fill=col, anchor='ma'); y += 62
d.text((W / 2, y + 10), '= 3 por Tesouro', font=F(R.INTB, 90), fill=R.PH, anchor='ma')
fonte(d, ['com as duas criaturas em campo · cálculo a partir do texto Oracle', 'Treasure (ficha) THOB 12, arte Leonardo Santanna · © Wizards of the Coast'])
im.save(f'{out}/04_conta.png')
# 5 · a pergunta
im, d = base(5, 'O QUE DECIDIU A FINAL?')
d.text((W / 2, 200), 'Ott ganhou a mesa.', font=F(R.INTB, 72), fill=R.WHITE, anchor='ma')
d.text((W / 2, 300), 'Von Stange contou o dano.', font=F(R.INTB, 72), fill=R.PH, anchor='ma')
d.text((W / 2, 410), 'leitura do TUBO, não regra do jogo', font=F(R.MONO, 30), fill=R.GREY, anchor='ma')
for i, s in enumerate(['A · a mesa do Ott chegou tarde', 'B · o Dirge achou as peças', 'C · a pilotagem do von Stange']):
    y = 520 + i * 130
    d.rounded_rectangle((120, y, W - 120, y + 100), 50, outline=R.EM, width=4, fill=(10, 30, 24))
    d.text((W / 2, y + 50), s, font=R.fit(d, s, R.MONOB, 38, W - 300), fill=R.EM, anchor='mm')
d.text((W / 2, 960), 'GRAU DE CERTEZA', font=F(R.MONOB, 30), fill=R.GREY, anchor='ma')
for i, (lab, n, val) in enumerate([('MOTOR DAS CARTAS', 4, 'ALTO'), ('O QUE DECIDIU A FINAL', 1, 'BAIXO')]):
    y = 1010 + i * 64
    d.text((90, y + 18), lab, font=F(R.CONDB, 30), fill=R.WHITE, anchor='lm')
    for s in range(5): d.rounded_rectangle((560 + s * 66, y, 616 + s * 66, y + 36), 7, fill=(R.EM if s < n else None), outline=R.EM, width=3)
    d.text((W - 80, y + 18), val, font=F(R.MONOB, 30), fill=R.EM, anchor='rm')
fonte(d, ['Responda com uma letra nos comentários · fonte: Star City Games'], 1180)
im.save(f'{out}/05_pergunta.png')
# capa (quadro do gancho, já com OTT / VON STANGE)
R.frame(4.95).convert('RGB').save('EP02_capa.jpg', quality=92)
print('ok')
