"""LL-ECO01 · carrossel 7 × 1080×1350 com as mesmas peças do vídeo (campanha.py) sobre o fundo aprovado do kit (motor_padrao.fundo).
Uso: python3 -I campanha.py carrossel <config.json> <pasta_saida>"""
import os, cv2, numpy as np
import campanha as K
from campanha import M, peca_folha, peca_carta, peca_img, matte, caixa, T, render_textos, colar, CW, CH, PRETO

W, H = 1080, 1350

def put(base, P, cx, cy, sc=1.0, ang=0.0):
    rgb, al, off = P; h, w = al.shape
    cx, cy = cx + off[0] * sc, cy + off[1] * sc
    R = cv2.getRotationMatrix2D((w / 2, h / 2), -ang, sc); R[:, 2] += [cx - w / 2, cy - h / 2]
    Mx = np.vstack([R, [0, 0, 1]])
    return K.blend(base.astype(np.float32), rgb, al, Mx, 1.0, (base.shape[1], base.shape[0]))

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
    capa_textos(t)
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
    # capa (23/11, 18:06): o slide da comunidade, refinado, passa a 1.º; o antigo slide 4 sai
    capa = comunidade(M.fundo(3).astype(np.float32), t, c, 0, arrasta=True)
    capa = put(capa, peca_folha(1000, 40, 'creme', 63, 0, t['cr3']), 540, 1300, .95)
    S = [capa] + S[:3] + S[4:]
    for i, s in enumerate(S, 1):
        cv2.imwrite(os.path.join(out, f'LL-ECO01_carrossel_{i:02d}.png'), np.clip(s, 0, 255).astype(np.uint8))
    print('ok', out)


# ------------------------------------------------------------------ capa (pedido do fundador 23/11, 18:06): slide da comunidade como capa
def capa_textos(t):
    t['q_pin'] = caixa(170, 210, K.svg(170, 210, '<path d="M85 12 c-40 0 -70 30 -70 68 c0 50 70 118 70 118 s70 -68 70 -118 c0 -38 -30 -68 -70 -68z" fill="#10B981"/>'
                                         '<circle cx="85" cy="78" r="38" fill="#F2EDE2"/><text x="85" y="98" text-anchor="middle" font-family="AB" font-size="56" fill="#050A10">?</text>'))
    t['gratis'] = caixa(230, 230, K.svg(230, 230, '<polygon points="' + ' '.join(
        f"{115 + (108 if i % 2 == 0 else 86) * np.cos(np.pi * i / 12):.1f},{115 + (108 if i % 2 == 0 else 86) * np.sin(np.pi * i / 12):.1f}" for i in range(24)) +
        '" fill="#FFD84A"/><text x="115" y="132" text-anchor="middle" font-family="AB" font-size="46" fill="#050A10">GRÁTIS</text>'))
    t['nota'] = caixa(420, 120, '<div style="font-family:CB;font-size:58px;line-height:.95;color:#E61E6E;text-align:left;transform:rotate(-4deg)">quem joga<br>perto de você?</div>')
    t['arrasta'] = caixa(420, 80, '<div style="font-family:CB;font-size:50px;color:#050A10;text-align:right;white-space:nowrap">arrasta pro lado <svg width="70" height="34" style="vertical-align:middle"><path d="M4 18 H58 M42 4 L62 18 L42 32" stroke="#E61E6E" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></div>')

def comunidade(b, t, c, dy=0, arrasta=False):
    """slide da comunidade, refinado para capa: ? no alfinete, selo GRÁTIS, nota a marcador; dy desloca tudo (capa 9:16)"""
    fita2 = ((-.94, -1, -40), (.94, -1, 40))
    b = put(b, peca_folha(940, 240, 'creme', 12, -1, t['s3a'], fitas=fita2), 540, 215 + dy, .95)
    b = put(b, peca_carta(c(7029), 420, 1.5), 540, 700 + dy, .92)
    for P, x, y in ((peca_folha(190, 230, 'creme', 13, -5, t['q_pin']), 170, 530), (peca_folha(170, 170, 'creme', 14, 4, t['ic_av']), 170, 765),
                    (peca_folha(170, 170, 'creme', 15, -3, t['ic_av2']), 915, 530), (peca_folha(260, 150, 'creme', 16, 4, t['ic_bal']), 905, 770)):
        b = put(b, P, x, y + dy, .9)
    b = put(b, peca_folha(430, 140, 'creme', 44, -3, t['nota']), 228, 1003 + dy, .66, -2)
    b = put(b, peca_folha(880, 140, 'preto', 18, 1, t['s3b'], claro=True), 540, 1120 + dy, .95)
    b = put(b, matte(lambda x: K.tinta(np.ascontiguousarray(x), t['gratis'], claro=True)), 922, 352 + dy, .76, 12)
    if arrasta:
        b = put(b, peca_folha(430, 90, 'creme', 45, 2, t['arrasta']), 770, 1232 + dy, .85)
    return b

def folha_fundo(base, seed, cy):
    """mesma folha kraft do motor_padrao.fundo(), colada noutra altura (para a capa 9:16)"""
    FW, FH = 1000, 1290
    folha = M.kraft(FW, FH, 0, seed)
    rel = cv2.resize(cv2.cvtColor(M.cp[480:900, 120:960], cv2.COLOR_BGR2GRAY), (FW, FH)).astype(np.float32)
    if seed % 2: rel = rel[::-1]
    folha = np.clip(folha + np.clip(rel - cv2.GaussianBlur(rel, (0, 0), 2), -10, 10)[..., None] * .7, 0, 255).astype(np.uint8)
    return colar(base, folha, K.rasgo_alpha(FW, FH, 16, 9 + seed), 540, cy, -0.4 + 0.15 * (seed % 3))

def capas(cfg, out):
    os.makedirs(out, exist_ok=True)
    t, c = K.pecas(cfg); capa_textos(t)
    t['cred'] = caixa(980, 40, '<div style="font-family:Geist;font-weight:500;font-size:18px;color:#050A10;text-align:center;white-space:nowrap">'
                                'Command Tower (SLD 7029) · Dan Black · © Wizards of the Coast</div>')
    render_textos()
    # 4:5 (1080×1350): 1.º slide do carrossel
    b = comunidade(M.fundo(3).astype(np.float32), t, c, 0, arrasta=True)
    b = put(b, peca_folha(1000, 40, 'creme', 63, 0, t['cred']), 540, 1300, .95)
    cv2.imwrite(os.path.join(out, 'LL-ECO01_capa_4x5_1080x1350.png'), np.clip(b, 0, 255).astype(np.uint8))
    # 9:16 (1080×1920) do Reel, com o conteúdo inteiro dentro do recorte 3:4 da grelha (y 240–1680)
    b = K.muro().astype(np.uint8)
    b = folha_fundo(b, 3, 960).astype(np.float32)
    b = comunidade(b, t, c, 285)
    b = put(b, peca_folha(1000, 40, 'creme', 63, 0, t['cred']), 540, 1585, .95)
    b = np.clip(b, 0, 255).astype(np.uint8)
    cv2.imwrite(os.path.join(out, 'LL-ECO01_capa_reel_1080x1920.png'), b)
    cv2.imwrite(os.path.join(out, 'LL-ECO01_capa_grelha_3x4_previa.png'), b[240:1680])
    print('ok', out)
