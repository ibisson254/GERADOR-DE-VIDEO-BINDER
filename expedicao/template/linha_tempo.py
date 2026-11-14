# Expedição BINDER · linha do tempo v2: blocos do episode.json -> eventos com tempo final (s), presos à grelha da música.
# Cada corte/punch/slide nasce na palavra-chave (índice em audio/words.json, antecipado ANTEC s) e salta para a batida
# mais próxima dentro de [-0,25 s; +0,15 s]; as camadas (respirações) saltam para o tempo forte do compasso mais próximo
# dentro de [-0,6 s; +0,45 s]; o Lotus acende exatamente no drop.
import bisect
ANTEC = 0.06

def construir(cfg, tw, total, out_start, beats=None, drop=None):
    beats = beats or []
    def ws(i):
        while i < len(tw) and tw[i]['cortada']: i += 1
        return max(0.0, tw[min(i, len(tw) - 1)]['s'] - ANTEC)
    def snap(t, lo=-0.25, hi=0.15, every=1):
        cand = [b for j, b in enumerate(beats) if j % every == 0 and t + lo <= b <= t + hi]
        return min(cand, key=lambda b: abs(b - t)) if cand else t
    def sw(i, **k): return snap(ws(i), **k)
    ev = []
    blocos = cfg['blocos']
    starts = []
    for b in blocos:
        if b['tipo'] == 'respiro': starts.append(snap(ws(b['w']), -0.6, 0.45, every=4))
        else: starts.append(sw(b['w']))
    ab = cfg['abertura']
    ev.append(dict(tipo='abertura', t=0.0, t1=starts[0], silhueta=snap(ab['corte_silhueta']), titulo=sw(ab['titulo_w'])))
    for k, b in enumerate(blocos):
        t0 = starts[k]; t1 = starts[k + 1] if k + 1 < len(blocos) else out_start
        e = dict(tipo=b['tipo'], t=t0, t1=t1, bloco=k)
        if b['tipo'] == 'respiro': e['som'] = 'descida'
        if b['tipo'] == 'caixa':
            e['punch_t'] = sw(b['punch_w']); ev.append(dict(tipo='glitch', t=e['punch_t'], som='glitch'))
        if b['tipo'] == 'lotus':
            lit = drop if drop is not None else sw(b['acende_w'])
            ev.append(dict(tipo='lotus_acende', t=lit, som='swell'))
        if b['tipo'] == 'fecho': e['pergunta_t'] = sw(b['pergunta_w'])
        ev.append(e)
        sub = []
        for x in b.get('eventos', []):
            y = dict(x); y['t'] = sw(x['w']); sub.append(y)
            if x.get('som'): ev.append(dict(tipo='som', t=y['t'], som=x['som']))
            if 'comparacao' in x: ev.append(dict(tipo='slide_in', t=y['t']))
            if x.get('fim_comparacao'): ev.append(dict(tipo='slide_out', t=y['t']))
        e['sub'] = sub
    ev.append(dict(tipo='marca', t=out_start, t1=total))
    ev.sort(key=lambda x: x['t'])
    return ev
