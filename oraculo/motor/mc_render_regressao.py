# Meta em Curto · teste de regressão do motor (26/11/2026, missão de engenharia).
# Compara, píxel a píxel, os quadros do mc_render.py atual com os de uma versão de referência (por defeito a da main
# remota/HEAD, via git show), em episódios reais. Para alterações que não devem mudar a imagem (performance, limpeza).
#
# Uso (na raiz do repositório):
#   python3 -I oraculo/motor/mc_render_regressao.py                       # todos os episódios com dados/episodio.json, 1 quadro em cada 10
#   python3 -I oraculo/motor/mc_render_regressao.py --passo 3 --ref HEAD~1 oraculo/episodios/pau08_fuguete_tenda
# Sai com código 1 se algum quadro for diferente. Não escreve ficheiros no repositório (a referência vai para /tmp).
import os, sys, glob, time, runpy, subprocess, tempfile
import numpy as np

def carregar(motor, raiz, pasta):
    sys.argv = ['mc_render.py', raiz, pasta, 'regressao']
    cwd = os.getcwd(); os.chdir(pasta)
    try: return runpy.run_path(motor, run_name='regressao')
    finally: os.chdir(cwd)

def main():
    a = sys.argv[1:]; passo, ref = 10, 'HEAD'
    if '--passo' in a: i = a.index('--passo'); passo = int(a[i + 1]); del a[i:i + 2]
    if '--ref' in a: i = a.index('--ref'); ref = a[i + 1]; del a[i:i + 2]
    raiz = os.path.abspath('.')
    pastas = [os.path.abspath(x) for x in a] or sorted(os.path.dirname(os.path.dirname(p)) for p in glob.glob(raiz + '/oraculo/**/dados/episodio.json', recursive=True))
    src = ref if os.path.isfile(ref) else None
    if src is None:
        txt = subprocess.run(['git', 'show', f'{ref}:oraculo/motor/mc_render.py'], capture_output=True, text=True, check=True).stdout
        src = os.path.join(tempfile.mkdtemp(), 'mc_render_ref.py'); open(src, 'w', encoding='utf-8').write(txt)
    atual = raiz + '/oraculo/motor/mc_render.py'; falhas = 0
    for pasta in pastas:
        try: gr, ga = carregar(src, raiz, pasta), carregar(atual, raiz, pasta)
        except Exception as e: print(f'{os.path.relpath(pasta)}: não carrega ({type(e).__name__}: {e}); ignorado'); continue
        if not ga.get('SEQ'): print(f'{os.path.relpath(pasta)}: sem seq (motor antigo do episódio); ignorado'); continue
        nf = int(round(ga['BEAT']['END'] * 30)); tr = ta = 0.0; dif = []
        for i in range(0, nf, passo):
            t = i / 30
            x = time.perf_counter(); fr = np.asarray(gr['frame'](t)); y = time.perf_counter(); fa = np.asarray(ga['frame'](t)); z = time.perf_counter()
            tr += y - x; ta += z - y
            if fr.shape != fa.shape or not np.array_equal(fr, fa): dif.append(round(t, 2))
        n = len(range(0, nf, passo)); falhas += len(dif)
        print(f'{os.path.relpath(pasta)}: {n} quadros · iguais {n - len(dif)} · diferentes {len(dif)} {dif[:8]} · '
              f'ref {tr / n * 1000:.0f} ms/quadro · atual {ta / n * 1000:.0f} ms/quadro')
    sys.exit(1 if falhas else 0)

if __name__ == '__main__': main()
