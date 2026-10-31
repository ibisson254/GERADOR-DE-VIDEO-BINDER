"""Recorta o fundo bege liso dos assets do Pequeno Mestre e grava PNGs com transparência.

Uso:  python3 pequeno-mestre/recortar.py            (a partir da raiz do repositório)

Como funciona: a cor do fundo é a mediana da borda da imagem; tudo o que é parecido com
ela e está ligado à borda sai (o contorno escuro das ilustrações trava o preenchimento,
por isso o cordão creme e as listras brancas ficam). Fundos fechados entre braço e corpo
só saem quando o asset os lista em "buracos". Os quadros do kit de fala (B1–B5) são
recortados com a MESMA caixa, para continuarem alinhados ao pixel.
"""
from pathlib import Path

import cv2
import numpy as np
from scipy import ndimage

RAIZ = Path(__file__).resolve().parent / "assets"
SAIDA = RAIZ / "recortes"
MARGEM = 24

# id: (ficheiro de origem, tolerância de cor, grupo de caixa comum, buracos a abrir)
# tolerância: 14 para o menino (listras brancas e cordão creme são próximos do fundo),
# 60 para bichos e móvel (tira também a sombra no chão; o contorno escuro trava).
ASSETS = {
    "A2_corpo_inteiro_leao": ("personagem/A2_corpo_inteiro_leao.jpg", 14, None, True),
    "A4_alegria":            ("personagem/A4_alegria.jpg", 14, None, False),
    "A5_barulho_fones":      ("personagem/A5_barulho_fones.jpg", 14, None, False),
    "B7_foco_bichos":        ("personagem/B7_foco_bichos.jpg", 14, None, False),
    "B1_base_boca_fechada":  ("fala/B1_base_boca_fechada.jpg", 14, "fala", False),
    "B2_boca_entreaberta":   ("fala/B2_boca_entreaberta.jpg", 14, "fala", False),
    "B3_boca_A":             ("fala/B3_boca_A.jpg", 14, "fala", False),
    "B4_boca_O":             ("fala/B4_boca_O.jpg", 14, "fala", False),
    "B5_piscar":             ("fala/B5_piscar.jpg", 14, "fala", False),
    "D1_leao_lado":          ("bichos/D1_leao_lado.jpg", 60, None, False),
    "D1b_leao_frente":       ("bichos/D1b_leao_frente.jpg", 60, None, False),
    "D2_trex":               ("bichos/D2_trex.jpg", 60, None, False),
    "D3_girafa":             ("bichos/D3_girafa.jpg", 60, None, False),
    "D4_tigre":              ("bichos/D4_tigre.jpg", 60, None, False),
    "D5_panda":              ("bichos/D5_panda.jpg", 60, None, False),
    "D6_elefante":           ("bichos/D6_elefante.jpg", 60, None, False),
    "P1_movel_azulejos":     ("cenario/P1_movel_azulejos.jpg", 60, None, False),
}


def alfa(img, tol, abrir_buracos):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(np.float32)
    borda = np.concatenate([lab[:20].reshape(-1, 3), lab[-20:].reshape(-1, 3),
                            lab[:, :20].reshape(-1, 3), lab[:, -20:].reshape(-1, 3)])
    fundo = np.median(borda, axis=0)
    dist = np.linalg.norm(lab - fundo, axis=2)
    parecido = dist < tol
    rot, _ = ndimage.label(parecido)
    na_borda = set(np.unique(np.concatenate([rot[0], rot[-1], rot[:, 0], rot[:, -1]]))) - {0}
    fora = np.isin(rot, list(na_borda))
    if abrir_buracos:
        # bolsões fechados de fundo (ex.: entre braço, cabeça e leão): grandes e quase da cor exata
        quase = dist < 7
        rq, n = ndimage.label(quase & ~fora)
        if n:
            areas = ndimage.sum(np.ones_like(rq), rq, range(1, n + 1))
            for i, a in enumerate(areas, start=1):
                if a > 6000:
                    fora |= ndimage.binary_dilation(rq == i, iterations=2) & parecido
    dentro = ndimage.binary_opening(~fora, iterations=1)
    a = (dentro * 255).astype(np.uint8)
    return cv2.GaussianBlur(a, (3, 3), 0)


def caixa(a):
    ys, xs = np.where(a > 10)
    return xs.min(), ys.min(), xs.max(), ys.max()


def main():
    SAIDA.mkdir(exist_ok=True)
    feitos, grupos = {}, {}
    for nome, (origem, tol, grupo, buracos) in ASSETS.items():
        img = cv2.imread(str(RAIZ / origem))
        a = alfa(img, tol, buracos)
        feitos[nome] = (img, a)
        if grupo:
            x0, y0, x1, y1 = caixa(a)
            g = grupos.get(grupo, (x0, y0, x1, y1))
            grupos[grupo] = (min(g[0], x0), min(g[1], y0), max(g[2], x1), max(g[3], y1))
    for nome, (img, a) in feitos.items():
        grupo = ASSETS[nome][2]
        x0, y0, x1, y1 = grupos[grupo] if grupo else caixa(a)
        h, w = a.shape
        x0, y0 = max(0, x0 - MARGEM), max(0, y0 - MARGEM)
        x1, y1 = min(w, x1 + MARGEM), min(h, y1 + MARGEM)
        rgba = np.dstack([img, a])[y0:y1, x0:x1]
        cv2.imwrite(str(SAIDA / f"{nome}.png"), rgba, [cv2.IMWRITE_PNG_COMPRESSION, 9])
        print(f"{nome}.png  {x1 - x0}x{y1 - y0}  (caixa {x0},{y0})")


if __name__ == "__main__":
    main()
