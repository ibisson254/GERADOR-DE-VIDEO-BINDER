#!/usr/bin/env python3
"""
RECORTAR · Vinci — corta as folhas de modelo em PNG com transparencia.

As folhas vem com fundo branco. O fundo e removido por preenchimento a partir
das bordas, e nao por "tira tudo o que e branco": assim a camisa creme, os olhos
e os brilhos ficam intactos, porque estao fechados dentro do contorno.

Depois cada desenho e isolado por componentes ligados, agrupado em linhas e
colunas, e gravado com o nome que o gerador de video espera.

Uso:
    python3 recortar.py --folha-poses folhas/poses.png --folha-pecas folhas/pecas.png

Saida: vince/kit/v1/*.png + ancoras.json
"""

import argparse
import json
import pathlib
import numpy as np
from PIL import Image
from scipy import ndimage

NOMES_POSES = [
    "vince_pose_pitch", "vince_pose_aponta", "vince_pose_choque",
    "vince_pose_bracos", "vince_pose_testa", "vince_pose_confidencia",
    "vince_pose_dinheiro", "vince_pose_pega_telefone", "vince_pose_ao_telefone",
]
NOMES_PECAS = [
    "vince_cabeca_neutra", "vince_boca_a", "vince_boca_o",
    "vince_olhos_fechados", "vince_olhos_lado",
    "prop_telefone_descanso", "prop_telefone_fora",
]


def tira_fundo(img, tolerancia=26):
    """Alpha a zero no fundo, por preenchimento desde as bordas."""
    rgb = np.array(img.convert("RGB")).astype(np.int16)
    claro = (np.abs(rgb - 255).max(axis=2) <= tolerancia)

    # componentes de "claro" que tocam a borda = fundo; o resto fica
    rotulos, n = ndimage.label(claro)
    if n == 0:
        fundo = np.zeros(claro.shape, bool)
    else:
        borda = set(rotulos[0, :]) | set(rotulos[-1, :]) | set(rotulos[:, 0]) | set(rotulos[:, -1])
        borda.discard(0)
        fundo = np.isin(rotulos, list(borda))

    alpha = np.where(fundo, 0, 255).astype(np.uint8)
    # suaviza a orla um pixel para dentro, para nao ficar serrilhado
    suave = ndimage.uniform_filter(alpha.astype(np.float32), size=3)
    alpha = np.where(alpha == 0, 0, suave).astype(np.uint8)

    out = np.dstack([np.array(img.convert("RGB")), alpha])
    return Image.fromarray(out, "RGBA"), alpha


def caixas(alpha, area_minima=4000):
    """Caixas dos desenhos, agrupadas por linha e ordenadas da esquerda para a direita."""
    rotulos, n = ndimage.label(alpha > 40)
    fatias = ndimage.find_objects(rotulos)
    brutas = []
    for i, fatia in enumerate(fatias, start=1):
        if fatia is None:
            continue
        ys, xs = fatia
        if (ys.stop - ys.start) * (xs.stop - xs.start) < area_minima:
            continue
        if (rotulos[fatia] == i).sum() < area_minima // 3:
            continue
        brutas.append([xs.start, ys.start, xs.stop, ys.stop])

    # junta pedacos que se sobrepoem (ex.: o telefone e a mao que lhe pega)
    mudou = True
    while mudou:
        mudou = False
        for a in range(len(brutas)):
            for b in range(a + 1, len(brutas)):
                x0, y0, x1, y1 = brutas[a]
                u0, v0, u1, v1 = brutas[b]
                folga = 24
                if x0 - folga < u1 and u0 - folga < x1 and y0 - folga < v1 and v0 - folga < y1:
                    brutas[a] = [min(x0, u0), min(y0, v0), max(x1, u1), max(y1, v1)]
                    brutas.pop(b)
                    mudou = True
                    break
            if mudou:
                break

    # agrupa em linhas pelo centro vertical
    brutas.sort(key=lambda c: (c[1] + c[3]) / 2)
    linhas, atual = [], [brutas[0]]
    for c in brutas[1:]:
        centro_atual = sum((k[1] + k[3]) / 2 for k in atual) / len(atual)
        altura = max(k[3] - k[1] for k in atual)
        if abs((c[1] + c[3]) / 2 - centro_atual) < altura * 0.6:
            atual.append(c)
        else:
            linhas.append(atual)
            atual = [c]
    linhas.append(atual)

    ordenadas = []
    for linha in linhas:
        linha.sort(key=lambda c: c[0])
        ordenadas.extend(linha)
    return ordenadas


def corta(caminho_folha, nomes, destino, margem=14):
    img = Image.open(caminho_folha)
    rgba, alpha = tira_fundo(img)
    cxs = caixas(alpha)
    if len(cxs) != len(nomes):
        print(f"  aviso: {caminho_folha.name} deu {len(cxs)} recortes para {len(nomes)} nomes")
    destino.mkdir(parents=True, exist_ok=True)
    feitos = {}
    for nome, (x0, y0, x1, y1) in zip(nomes, cxs):
        caixa = (max(0, x0 - margem), max(0, y0 - margem),
                 min(rgba.width, x1 + margem), min(rgba.height, y1 + margem))
        peca = rgba.crop(caixa)
        peca.save(destino / f"{nome}.png")
        feitos[nome] = {"largura": peca.width, "altura": peca.height,
                        "origem": caminho_folha.name, "caixa_na_folha": list(caixa)}
        print(f"  {nome:30s} {peca.width}x{peca.height}")
    return feitos


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--folha-poses", required=True)
    p.add_argument("--folha-pecas", required=True)
    p.add_argument("--destino", default="kit/v1")
    args = p.parse_args()

    destino = pathlib.Path(args.destino)
    print("poses:")
    feitos = corta(pathlib.Path(args.folha_poses), NOMES_POSES, destino)
    print("pecas:")
    feitos.update(corta(pathlib.Path(args.folha_pecas), NOMES_PECAS, destino))

    (destino / "ancoras.json").write_text(json.dumps({
        "nota": "Caixas medidas no recorte. A boca e os olhos sao colados pela cabeca; "
                "o simbolo do BINDER assenta no centro do disco do telefone.",
        "pecas": feitos,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n{len(feitos)} pecas em {destino}/")


if __name__ == "__main__":
    main()
