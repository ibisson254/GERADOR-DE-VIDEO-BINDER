# Expedição BINDER · linha do tempo: blocos do episode.json -> eventos com tempo final (s).
# Cada corte/punch/slide é preso à palavra-chave (índice em audio/words.json) e antecipa ANTEC s.
ANTEC = 0.06

def construir(cfg, tw, total, out_start):
    def ws(i):
        while i < len(tw) and tw[i]['cortada']: i += 1
        return max(0.0, tw[min(i, len(tw) - 1)]['s'] - ANTEC)
    ev = []
    blocos = cfg['blocos']
    starts = [ws(b['w']) for b in blocos]
    ab = cfg['abertura']
    ev.append(dict(tipo='abertura', t=0.0, t1=starts[0], silhueta=ab['silhueta_t'] if 'silhueta_t' in ab else ab['corte_silhueta'],
                   titulo=ws(ab['titulo_w'])))
    for k, b in enumerate(blocos):
        t0 = starts[k]; t1 = starts[k + 1] if k + 1 < len(blocos) else out_start
        e = dict(tipo=b['tipo'], t=t0, t1=t1, bloco=k)
        if b['tipo'] == 'respiro': e['som'] = 'ping'
        if b['tipo'] == 'caixa':
            e['som'] = 'bolhas'; e['punch_t'] = ws(b['punch_w'])
        if b['tipo'] == 'lotus':
            ev.append(dict(tipo='lotus_acende', t=ws(b['acende_w']), som='ping'))
        if b['tipo'] == 'fecho':
            e['pergunta_t'] = ws(b['pergunta_w'])
        ev.append(e)
        sub = []
        for x in b.get('eventos', []):
            y = dict(x); y['t'] = ws(x['w']); sub.append(y)
            if 'comparacao' in x: ev.append(dict(tipo='slide_in', t=y['t'], som='whoosh'))
            if x.get('fim_comparacao'): ev.append(dict(tipo='slide_out', t=y['t'], som='whoosh_out'))
        # comparação sem fim explícito sai no fim do bloco (som de saída 0,2 s antes)
        if any('comparacao' in x for x in sub) and not any(x.get('fim_comparacao') for x in sub):
            ev.append(dict(tipo='slide_out', t=t1 - 0.2, som='whoosh_out'))
        e['sub'] = sub
    ev.append(dict(tipo='marca', t=out_start, t1=total))
    return ev
