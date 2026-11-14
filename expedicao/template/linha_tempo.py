# Expedição BINDER · linha do tempo v3: blocos do episode.json -> eventos com tempo final (s), presos à grelha da música.
# Cada corte/chamada/slide nasce na palavra-chave (índice em audio/words.json, antecipado ANTEC s) e salta para a
# batida mais próxima dentro de [-0,25 s; +0,19 s] (a janela cobre sempre uma batida); as camadas saltam para o tempo forte mais próximo dentro de
# [-0,6 s; +0,45 s]; a carta-pagamento acende exatamente no drop. Blocos com palavra cortada nesta versão saem.
ANTEC = 0.06

def construir(cfg, tw, total, versao='A', beats=None, drop=None, fim=None):
    beats = beats or []
    def ws(i):
        while i < len(tw) and tw[i]['cortada']: i += 1
        return max(0.0, tw[min(i, len(tw) - 1)]['s'] - ANTEC)
    def snap(t, lo=-0.25, hi=0.19, every=1):
        cand = [b for j, b in enumerate(beats) if j % every == 0 and t + lo <= b <= t + hi]
        return min(cand, key=lambda b: abs(b - t)) if cand else t
    def sw(i, **k): return snap(ws(i), **k)
    blocos = [(k, b) for k, b in enumerate(cfg['blocos'])
              if not tw[b['w']]['cortada'] and b.get('so_versao', versao) == versao]
    ev = []
    starts = [snap(ws(b['w']), -0.6, 0.45, every=4) if (b['tipo'] == 'respiro' or b.get('entra_camada')) else sw(b['w']) for _, b in blocos]
    fim = fim or []
    ev.append(dict(tipo='abertura', t=0.0, t1=starts[0], flash=cfg['abertura'].get('flash', 0.33)))
    for j, (k, b) in enumerate(blocos):
        t0 = starts[j]; t1 = starts[j + 1] if j + 1 < len(blocos) else (fim[0]['t'] if fim else total)
        e = dict(tipo=b['tipo'], t=t0, t1=t1, bloco=k)
        if b.get('som'): e['som'] = b['som']
        if b['tipo'] == 'lotus':
            ev.append(dict(tipo='lotus_acende', t=drop if drop is not None else sw(b['acende_w']), som='swell'))
        if 'chamada' in b:
            e['chamada_t'] = sw(b['chamada']['w'])
            e['chips_t'] = [sw(c[2]) if len(c) > 2 else e['chamada_t'] for c in b['chamada']['chips']]
        ev.append(e)
        sub = []
        for x in b.get('eventos', []):
            y = dict(x); y['t'] = sw(x['w']); sub.append(y)
            if x.get('som'): ev.append(dict(tipo='som', t=y['t'], som=x['som']))
        e['sub'] = sub
    for f in fim:
        ev.append(dict(f, tipo=f['tipo'], t=f['t'], t1=f['t1'], fim=True))
    ev.sort(key=lambda x: x['t'])
    return ev
