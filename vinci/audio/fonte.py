#!/usr/bin/env python3
"""
A VOZ DA FONTE — sintetizador de trombone com surdina (Vinci / BINDER Originals)

A Fonte é a personagem do outro lado do telefone do Vinci: nunca aparece e nunca
fala palavras. O que se ouve é um metal abafado, com contorno de frase.

Este ficheiro NAO usa nenhum servico pago. Gera os audios por sintese, aqui.
Cada frase nova custa zero: acrescenta-se uma entrada em FRASES e corre-se o script.

Uso:
    python3 fonte.py                 # renderiza todas as frases para ./saida/
    python3 fonte.py --lista         # mostra as frases disponiveis
    python3 fonte.py --so pergunta   # renderiza so uma

Como funciona (resumo honesto):
    1. Um tom de metal (soma de harmonicos, tipo serra) com vibrato leve.
    2. Um filtro passa-banda ressonante cuja frequencia central varre ao longo
       da silaba. Essa varredura e o "ua-ua" da surdina de embolo.
    3. Um contorno de altura por silaba (sobe = pergunta, desce = ma noticia).
    4. Envelope de sopro: ataque curto, corpo, queda.

Nota de direitos: a tecnica (metal com surdina a fazer de fala) e generica e
antiga. Esta voz e desenhada de raiz para o Vinci -- nao imita o motivo sonoro
de nenhuma obra existente.
"""

import argparse
import json
import pathlib
import numpy as np
from scipy.io import wavfile

SR = 44100


# -----------------------------------------------------------------------------
# nucleo de sintese
# -----------------------------------------------------------------------------

def _curva(pontos, n):
    """Interpola uma lista de valores ao longo de n amostras (linear, suave)."""
    pontos = np.asarray(pontos, dtype=float)
    if pontos.size == 1:
        return np.full(n, pontos[0])
    x = np.linspace(0.0, 1.0, pontos.size)
    xi = np.linspace(0.0, 1.0, n)
    bruto = np.interp(xi, x, pontos)
    # suaviza as esquinas da interpolacao linear
    k = max(1, int(SR * 0.012))
    janela = np.hanning(k * 2 + 1)
    janela /= janela.sum()
    return np.convolve(np.pad(bruto, k, mode="edge"), janela, mode="same")[k:-k]


def _metal(f0, n, harmonicos=18, vibrato_hz=5.2, vibrato=0.006):
    """Tom de metal: soma de harmonicos com amplitude 1/k, com vibrato."""
    t = np.arange(n) / SR
    vib = 1.0 + vibrato * np.sin(2 * np.pi * vibrato_hz * t)
    fase = 2 * np.pi * np.cumsum(f0 * vib) / SR
    saida = np.zeros(n)
    for k in range(1, harmonicos + 1):
        if (f0 * k).max() > SR * 0.45:      # evita aliasing
            break
        saida += np.sin(fase * k) / k
    return saida / np.abs(saida).max()


def _wah(x, centro, q=4.2):
    """Passa-banda ressonante com frequencia central variavel (filtro de estado).

    E este varrimento que faz o som parecer fala. Loop por amostra de proposito:
    os clipes sao curtos e assim os coeficientes mudam a cada amostra.
    """
    n = x.size
    saida = np.zeros(n)
    passa_baixo = passa_banda = 0.0
    f = 2.0 * np.sin(np.pi * np.clip(centro, 80.0, SR * 0.45) / SR)
    amortecimento = 1.0 / q
    for i in range(n):
        passa_alto = x[i] - passa_baixo - amortecimento * passa_banda
        passa_banda += f[i] * passa_alto
        passa_baixo += f[i] * passa_banda
        saida[i] = passa_banda
    pico = np.abs(saida).max()
    return saida / pico if pico > 0 else saida


def _envelope(n, ataque=0.035, queda=0.09, sustento=0.85):
    env = np.ones(n)
    a = min(int(SR * ataque), n // 2)
    d = min(int(SR * queda), n // 2)
    env[:a] = np.linspace(0.0, 1.0, a) ** 1.6
    env[n - d:] = np.linspace(1.0, 0.0, d) ** 1.4
    meio = n - a - d
    if meio > 0:
        env[a:a + meio] = np.linspace(1.0, sustento, meio)
    return env


def silaba(dur, notas, wah, forca=1.0):
    """Uma silaba: duracao em segundos, contorno de altura (Hz), contorno do wah (Hz)."""
    n = int(SR * dur)
    f0 = _curva(notas, n)
    centro = _curva(wah, n)
    bruto = _metal(f0, n)
    sopro = np.random.default_rng(7).normal(0, 0.02, n)     # ar na boquilha
    voz = _wah(bruto + sopro, centro)
    return voz * _envelope(n) * forca


def frase(silabas, pausa=0.045):
    """Junta silabas com pequenos intervalos de respiracao."""
    pecas = []
    for i, s in enumerate(silabas):
        pecas.append(s)
        if i < len(silabas) - 1:
            pecas.append(np.zeros(int(SR * pausa)))
    return np.concatenate(pecas)


def telefone(x, corte_baixo=320.0, corte_alto=3200.0, sujidade=0.15):
    """Poe o som dentro da linha telefonica: banda estreita e um pouco de sujidade."""
    from scipy.signal import butter, sosfilt
    sos = butter(4, [corte_baixo, corte_alto], btype="band", fs=SR, output="sos")
    y = sosfilt(sos, x)
    y = np.tanh(y * (1.0 + sujidade * 6)) / np.tanh(1.0 + sujidade * 6)
    return y


def escreve(caminho, x, pico=0.89):
    x = np.asarray(x, dtype=float)
    m = np.abs(x).max()
    if m > 0:
        x = x / m * pico
    rampa = int(SR * 0.006)
    x[:rampa] *= np.linspace(0, 1, rampa)
    x[-rampa:] *= np.linspace(1, 0, rampa)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    wavfile.write(caminho, SR, (x * 32767).astype(np.int16))
    return caminho


# -----------------------------------------------------------------------------
# o vocabulario da Fonte
# -----------------------------------------------------------------------------
# Cada entrada e uma intencao, nao uma palavra. O Vinci responde por cima; o
# espectador monta o resto. Acrescentar uma frase nova aqui nao custa nada.

FRASES = {
    "pergunta": lambda: frase([
        silaba(0.26, [196, 233], [520, 1450]),
        silaba(0.34, [233, 311], [700, 1900]),
    ]),
    "confirma": lambda: frase([
        silaba(0.20, [262, 247], [1200, 620]),
        silaba(0.26, [247, 196], [900, 480]),
    ]),
    "ma_noticia": lambda: frase([
        silaba(0.95, [262, 208, 156, 131], [1500, 900, 520, 360]),
    ]),
    "surpresa": lambda: frase([
        silaba(0.18, [262, 349], [800, 2100]),
        silaba(0.42, [392, 440, 392], [2200, 1500, 1900]),
    ]),
    "ladainha": lambda: frase([
        silaba(0.30, [233, 262], [700, 1600]),
        silaba(0.22, [262, 247], [1500, 900]),
        silaba(0.26, [220, 233], [800, 1700]),
        silaba(0.20, [247, 220], [1400, 760]),
        silaba(0.34, [208, 196, 185], [900, 600, 430]),
        silaba(0.28, [196, 233], [620, 1550]),
    ]),
    "corta_seco": lambda: frase([
        silaba(0.14, [311, 294], [1800, 700], forca=1.1),
    ]),
    "hesita": lambda: frase([
        silaba(0.46, [220, 208, 220], [900, 1250, 820]),
        silaba(0.22, [196, 185], [700, 450]),
    ]),
}


def toque_telefone(toques=2):
    """Toque de telefone antigo: par de tons com campainha a tremer."""
    t = np.arange(int(SR * 2.0)) / SR
    par = np.sin(2 * np.pi * 440 * t) + np.sin(2 * np.pi * 480 * t)
    tremor = 0.5 * (1 + np.sin(2 * np.pi * 20 * t))          # badalo
    um = par * tremor
    silencio = np.zeros(int(SR * 1.6))
    return telefone(np.concatenate([np.concatenate([um, silencio]) for _ in range(toques)]))


def nao_atende(ciclos=5):
    """Ninguem atende: o toque a repetir e a cair. E assim que a serie diz
    'nao confirmado' sem precisar de aviso nenhum."""
    som = toque_telefone(toques=ciclos)
    desvanece = np.linspace(1.0, 0.45, som.size)
    return som * desvanece


def pousa_auscultador():
    """Clique do auscultador a cair no descanso."""
    rng = np.random.default_rng(3)
    n = int(SR * 0.09)
    estalo = rng.normal(0, 1, n) * np.exp(-np.linspace(0, 28, n))
    corpo = np.sin(2 * np.pi * 150 * np.arange(n) / SR) * np.exp(-np.linspace(0, 16, n)) * 0.5
    return telefone(estalo * 0.7 + corpo, corte_baixo=120, corte_alto=5200)


EXTRAS = {
    "telefone_toque": toque_telefone,
    "telefone_nao_atende": nao_atende,
    "telefone_pousa": pousa_auscultador,
}


def main():
    p = argparse.ArgumentParser(description="Gera a voz da Fonte e os sons do telefone.")
    p.add_argument("--saida", default="saida", help="pasta de destino")
    p.add_argument("--so", help="renderiza apenas esta frase")
    p.add_argument("--lista", action="store_true", help="lista as frases disponiveis")
    args = p.parse_args()

    todas = {**{f"fonte_{k}": v for k, v in FRASES.items()}, **EXTRAS}

    if args.lista:
        for nome in todas:
            print(nome)
        return

    destino = pathlib.Path(args.saida)
    feitos = []
    for nome, fabrica in todas.items():
        if args.so and args.so not in nome:
            continue
        som = fabrica()
        if nome.startswith("fonte_"):
            som = telefone(som)                   # a Fonte fala sempre pelo telefone
        caminho = escreve(destino / f"{nome}.wav", som)
        feitos.append((caminho.name, round(som.size / SR, 2)))

    manifesto = destino / "LEIA-ME.json"
    manifesto.write_text(json.dumps({
        "o_que_e": "Voz da Fonte e sons do telefone do Vinci, sintetizados localmente.",
        "custo": "zero creditos; refazer com python3 fonte.py",
        "taxa_amostragem": SR,
        "ficheiros": [{"nome": n, "segundos": s} for n, s in feitos],
        "regra": "A Fonte nunca diz palavras, nunca tem legenda e nunca aparece.",
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    for n, s in feitos:
        print(f"{n:28s} {s:>5.2f}s")


if __name__ == "__main__":
    main()
