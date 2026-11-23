"""LL-ECO01 · carrossel 7 × 1080×1350 com as mesmas peças do vídeo (campanha.py) sobre o fundo aprovado do kit (motor_padrao.fundo).
Uso: python3 -I campanha.py carrossel <config.json> <pasta_saida>"""
import os, cv2, numpy as np
import campanha as K
from campanha import M, peca_folha, peca_carta, peca_img, matte, caixa, T, render_textos, colar, CW, CH, PRETO

W, H = 1080, 1350

def put(base, P, cx, cy, sc=1.0):
    rgb, al, off = P; h, w = al.shape
    cx, cy = cx + off[0] * sc, cy + off[1] * sc
    Mx = np.float64([[sc, 0, cx - sc * w / 2], [0, sc, cy - sc * h / 2], [0, 0, 1]])
    return K.blend(base.astype(np.float32), rgb, al, Mx, 1.0, (W, H))

def chave(base, x0, y0, s=.8):
    """chaveamento a marcador (mesmo desenho do vídeo), sem nomes"""
    ov = np.zeros(base.shape[:2], np.float32)
    f = lambda p: (int(x0 + (p[0] - 185) * s), int(y0 + (p[1] - 700) * s))
    for p in K.SLOTS:
        a, b = f((p[0] - 70, p[1] - 32)), f((p[0], p[1] + 32)); cv2.rectangle(ov, a, b, 1.0, 5, cv2.LINE_AA)
    for seg in K.CHAVE:
        for p, q in zip(seg, seg[1:]): cv2.line(ov, f(p), f(q), 1.0, 7, cv2.LINE_AA)
    cv2.circle(ov, f((575, 925)), 15, 1.0, -1, cv2.LINE_AA)
    a = (cv2.GaussianBlur(ov, (0, 0), .8) * .9)[..., None]
    return base * (1 - a) + np.array((22, 18, 14), np.float32) * a

def gerar(cfg, out):
    os.makedirs(out, exist_ok=True)
    t, c = K.pecas(cfg)
    t['c3'] = caixa(560, 220, '<div style="font-family:RB;font-weight:800;font-size:34px;line-height:1.2;color:#050A10;text-align:left">'
                    'Copie a coleção do BINDER em lista ou CSV e importe na <span style="color:#E61E6E">LigaMagic</span>.</div>')
    t['beta'] = caixa(820, 70, T('Beta para Android · Link na bio', 40, PRETO, 'RB', 'font-weight:900;font-style:italic;', w=820))
    t['capa'] = caixa(900, 120, T('Sua coleção. Sua comunidade. <span class="g">Seu jogo.</span>', 40, '#fff', 'RB', 'font-weight:900;font-style:italic;', w=900))
    CRED = ['Lightning Bolt (SLD 901) · Christopher Rush', 'Reliquary Tower (SLD 7104) · Arthur Yuan  ·  Mystical Tutor (SLD 334) · Mateus Manhanini',
            'Ícone LigaMagic: marca dos seus titulares, sem parceria', 'Command Tower (SLD 7029) · Dan Black', 'Lightning Bolt (SLD 83) · Noah Bradley',
            'Generous Gift (SLD 369) · Ayako Ishiguro', '']
    for i, txt in enumerate(CRED):
        t[f'cr{i}'] = caixa(980, 40, f'<div style="font-family:Geist;font-weight:500;font-size:18px;color:#050A10;text-align:center;white-space:nowrap">'
                                     f'{txt}{"" if i in (2, 6) else " · © Wizards of the Coast"}</div>')
    render_textos()
    lig = cv2.imread(cfg['ligamagic']); mg, ma = K.logo_magic(); lb = K.logo_binder()
    fita2 = ((-.94, -1, -40), (.94, -1, 40))
    S = []
    # 1 · capa
    b = M.fundo(0).astype(np.float32)
    b = put(b, peca_folha(900, 270, 'creme', 1, -1.2, t['s1a'], fitas=fita2), 540, 215, .95)
    b = put(b, peca_carta(c(901), 460, -1.5), 540, 650, .9)
    b = put(b, peca_folha(900, 170, 'preto', 2, 1.0, t['s1b'], claro=True), 540, 1040, .95)
    b = put(b, peca_folha(940, 110, 'preto', 40, -.5, t['capa'], claro=True), 540, 1190, .95)
    S.append(b)
    # 2 · coleção
    b = M.fundo(1).astype(np.float32)
    b = put(b, peca_folha(900, 210, 'kraft', 7, 1.2, t['s2a'], fitas=fita2), 540, 200, .95)
    b = put(b, peca_carta(c(7104), 380, -3), 300, 650, 1.0)
    b = put(b, peca_carta(c(334), 380, 3), 780, 660, 1.0)
    b = put(b, peca_folha(860, 130, 'preto', 8, -1, t['s2b'], claro=True), 540, 1080, 1.0)
    S.append(b)
    # 3 · exportação LigaMagic
    b = M.fundo(2).astype(np.float32)
    b = put(b, peca_folha(560, 200, 'kraft', 10, 1.5, t['s2c'], fitas=((.96, -1, 40),)), 540, 260, 1.15)
    b = put(b, peca_img(lig, 300, ang=-4, margem=16, seed=9), 300, 680, 1.0)
    b = put(b, peca_folha(200, 120, 'creme', 41, 0, t['ic_seta']), 560, 640, 1.0)
    b = put(b, peca_folha(600, 260, 'creme', 42, 2, t['c3'], fitas=((0, -1, -6),)), 690, 930, .95)
    S.append(b)
    # 4 · comunidade
    b = M.fundo(3).astype(np.float32)
    b = put(b, peca_folha(940, 240, 'creme', 12, -1, t['s3a'], fitas=fita2), 540, 215, .95)
    b = put(b, peca_carta(c(7029), 420, 1.5), 540, 700, .92)
    for P, x, y in ((peca_folha(170, 210, 'creme', 13, -5, t['ic_pin']), 165, 520), (peca_folha(160, 160, 'creme', 14, 4, t['ic_av']), 170, 760),
                    (peca_folha(160, 160, 'creme', 15, -3, t['ic_av2']), 915, 520), (peca_folha(250, 140, 'creme', 16, 4, t['ic_bal']), 905, 760),
                    (peca_folha(250, 140, 'creme', 17, -4, t['ic_bal2']), 190, 960)):
        b = put(b, P, x, y, .9)
    b = put(b, peca_folha(880, 140, 'preto', 18, 1, t['s3b'], claro=True), 540, 1120, .95)
    S.append(b)
    # 5 · jogo
    b = M.fundo(4).astype(np.float32)
    b = put(b, peca_folha(900, 180, 'kraft', 20, -1.2, t['s4a'], fitas=fita2), 540, 200, .95)
    b = put(b, peca_folha(560, 620, 'kraft', 21, .8), 360, 640, .95)
    b = chave(b, 170, 400, .78)
    b = put(b, peca_carta(c(83), 330, 3), 800, 640, 1.0)
    b = put(b, peca_folha(190, 200, 'creme', 22, -4, t['ic_tro']), 830, 965, .8)
    b = put(b, peca_folha(900, 190, 'preto', 23, .8, t['s4b'], claro=True), 540, 1120, .95)
    S.append(b)
    # 6 · gratuito
    b = M.fundo(5).astype(np.float32)
    b = put(b, peca_folha(840, 150, 'kraft', 28, -2, t['s6a'], fitas=fita2), 540, 190, 1.0)
    b = put(b, peca_folha(840, 150, 'amarelo', 29, 1.5, t['s6b']), 548, 335, 1.0)
    b = put(b, peca_carta(c(369), 420, -2), 540, 790, 1.0)
    S.append(b)
    # 7 · marca + CTA — cartaz verde-esmeralda (pedido do fundador 23/11), logos em etiquetas pretas, selo oficial do Google Play
    pb, pa = K.logo_play()
    b = M.fundo(6).astype(np.float32)
    b = put(b, peca_folha(1000, 1290, 'verde', 24, .4), 540, 677, 1.0)
    b = put(b, peca_folha(860, 110, 'verde', 25, -1, t['s5a'], claro=True), 540, 115, .85)
    b = put(b, peca_folha(960, 270, 'verde', 26, 0, t['s5b'], claro=True), 540, 270, .85)
    b = put(b, peca_img(mg, 430, ma, ang=-1.5, margem=26, fundo=(16, 10, 5), seed=34, fitas=((-1, -1, -40), (1, -1, 40))), 540, 470, .78)
    b = put(b, peca_img(lb, 430, ang=1, margem=22, fundo=(16, 10, 5), seed=35, fitas=((-1, -1, -40), (1, -1, 40))), 540, 715, .78)
    b = put(b, peca_img(lig, 110, ang=-3, margem=8, seed=31), 375, 935, .8)
    b = put(b, peca_folha(380, 100, 'verde', 32, 0, t['s5d'], claro=True), 610, 937, .85)
    b = put(b, matte(lambda x: colar(x, pb, pa, CW / 2, CH / 2, 0, sombra=False)), 540, 1065, .44)
    b = put(b, peca_folha(820, 70, 'verde', 43, 0, t['beta']), 540, 1160, .9)
    b = put(b, peca_folha(900, 110, 'verde', 27, 0, t['s5c'], claro=True), 540, 1240, .95)
    S.append(b)
    for i in range(len(S) - 1):          # o slide 7 já leva a nota de marcas
        S[i] = put(S[i], peca_folha(1000, 40, 'creme', 60 + i, 0, t[f'cr{i}']), 540, 1300, .95)
    for i, s in enumerate(S, 1):
        cv2.imwrite(os.path.join(out, f'LL-ECO01_carrossel_{i:02d}.png'), np.clip(s, 0, 255).astype(np.uint8))
    print('ok', out)
