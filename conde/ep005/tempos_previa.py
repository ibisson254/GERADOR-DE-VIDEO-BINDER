"""Conde Ep. 005 · tempos ESTIMADOS por palavra para a prévia sem voz (não substituem o Scribe).
Calibrado no Ep. 004 (words_novo.json): mesma taxa por letra e pausas médias medidas.
Uso (pasta conde/): python3 ep005/tempos_previa.py [roteiro.txt] -> ep005/audio/words_previa.json
"""
import json, sys, os
B = os.path.dirname(os.path.abspath(__file__))

def estimar(texto, k=1.0):  # k: fator global de tempo
    t, out = 0.0, []
    for w in texto.split():
        d = max(0.16, len(w.strip('".,:?')) * 0.0562 + 0.02)
        if w.startswith("Hyalopterous"):
            d = 1.0
        out.append([w, round(t, 3), round(t + d, 3)]); t += d
        t += 0.55 if w.endswith("...") else 0.40 if w.endswith((".", "?")) else 0.26 if w.endswith(":") else 0.19 if w.endswith(",") else 0.076
    return [[a, round(b * k, 3), round(c * k, 3)] for a, b, c in out]

K = 53.8 / 57.3      # fator de calibração medido no Ep. 004

if __name__ == "__main__":
    ref = " ".join(w[0] for w in json.load(open(f"{B}/../ep004/audio/words_novo.json")))
    e = estimar(ref, K)
    print(f"calibração Ep.004: estimado {e[-1][2]:.1f} s · real 53.8 s")
    w = estimar(open(sys.argv[1] if len(sys.argv) > 1 else f"{B}/roteiro.txt").read(), K)
    json.dump(w, open(f"{B}/audio/words_previa.json", "w"), ensure_ascii=False)
    print(f"Ep.005: {len(w)} palavras, narração estimada {w[-1][2]:.1f} s")
