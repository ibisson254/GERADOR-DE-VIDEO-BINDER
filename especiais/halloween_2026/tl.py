"""Linha do tempo do especial + dados da cena do sofá (kit Mana & Burn).
Lê roteiro.json e linhas.json (vozes.py). Escreve tl.json e mb/data.js + mb/episode.js.
uso: python3 tl.py
"""
import json
R = json.load(open('roteiro.json')); L = json.load(open('linhas.json'))
F = {f['id']: f for f in R['falas']}
GAP = 0.10
# (cena, entrada antes da 1.ª fala, [falas], folga depois, pausa entre falas)
PLANO = [
    ('abre_i', 0.40, ['K0a'], 0.35, 0), ('abre_d', 0.10, ['K0b'], 0.30, 0), ('titulo', 1.50, [], 0, 0),
    ('sofa1', 0.15, ['B1', 'M1'], 0.12, GAP), ('tubo', 0.25, ['T1'], 0.20, 0),
    ('cat1', 0.30, ['B3', 'M2', 'B4', 'M3'], 0.10, GAP), ('veredito1', 0.15, ['T2'], 0.35, 0),
    ('cat2', 0.30, ['M4', 'B5', 'M5'], 0.10, GAP), ('veredito2', 0.15, ['T3'], 0.35, 0),
    ('cat3', 0.30, ['M6', 'B7'], 0.10, GAP), ('veredito3', 0.10, ['T4'], 0.10, 0),
    ('cat4', 0.40, ['K1', 'K2', 'K3'], 0.20, 0.22), ('veredito4', 0.15, ['T5'], 0.30, 0),
    ('cat5', 0.70, ['T6'], 0.05, 0), ('zero', 0.05, ['B8'], 0.15, 0), ('erro', 0.10, ['T7'], 0.45, 0),
    ('fecho_tubo', 0.10, ['T8'], 0.25, 0), ('sofa2', 0.15, ['B9', 'M7'], 0, 0.25),
]
t = 0.0; cenas = []; falas = []
for nome, lead, ids, post, gap in PLANO:
    a = t; t += lead
    for k, i in enumerate(ids):
        if k: t += gap
        falas.append(dict(id=i, quem=F[i]['quem'], cena=nome, start=round(t, 3), dur=L[i]['dur'], previa=L[i]['previa'],
                          legenda=F[i]['legenda'], foco=F[i].get('foco')))
        t += L[i]['dur']
    t += post
    cenas.append(dict(nome=nome, a=round(a, 3), b=round(t, 3)))
T_SLAM = round(falas[-1]['start'] + falas[-1]['dur'] + 0.20, 3)
cenas[-1]['b'] = round(T_SLAM + 0.52, 3)          # corte logo depois de o ponto ficar verde (como no Ep. 09)
FECHO = 3.87
TOTAL = round(cenas[-1]['b'] + FECHO, 3)
tl = dict(cenas=cenas, falas=falas, T_SLAM=T_SLAM, FIM_KIT=cenas[-1]['b'], FECHO=FECHO, TOTAL=TOTAL,
          previa=any(f['previa'] for f in falas))
json.dump(tl, open('tl.json', 'w'), ensure_ascii=False, indent=1)

# ---- cena do sofá: todas as falas do Burn e do Mana (o sofá também alimenta o PIP nas cenas de cartas)
POSE = {  # [Burn, Mana, olharB, olharM, sobrancelhaB, sobrancelhaM, plano]
    'B1': ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'wide'],
    'M1': ['rest', 'rest', 'other', 'cam', 'normal', 'flat', 'cuM'],
    'B8': ['arms_up', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],
    'B9': ['point_cam', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'],
    'M7': ['rest', 'remote', 'other', 'cam', 'normal', 'up', 'cuM'],
}
DEF = {'B': ['shrug', 'rest', 'cam', 'other', 'angry', 'flat', 'cuB'], 'M': ['rest', 'finger', 'other', 'cam', 'normal', 'up', 'cuM']}
mbl = [f for f in falas if f['quem'] in 'BM']
lines = [dict(who=f['quem'], text=f['legenda'], start=f['start'], dur=f['dur'], env=L[f['id']]['env']) for f in mbl]
open('mb/data.js', 'w').write('const DATA=' + json.dumps(dict(lines=lines, T_SLAM=T_SLAM, T_END=T_SLAM + 6)) + ';')
pose = [POSE.get(f['id'], DEF[f['quem']]) for f in mbl]
ep = {
  'id': 'especial_halloween_2026',
  'card': {'img': 'cards/main.png',
           'cred': 'Na TV: Emrakul, the Promised End (Eldritch Moon, 2016), nº 6. Arte: Jaime Jones.<br>© Wizards of the Coast. Conteúdo de fã não oficial.'},
  'pose': pose, 'inserts': [], 'hl': {},
  'tv': {'channel': 'TV SAL', 'clock': '23:59',
         'meter': {'title': 'PUTÔMETRO', 'value': '50%', 'fill': 0.495, 'calc': ['Salt 1,98 ÷ 4', 'EDHREC Top 100', '2026'],
                   'levels': [['QUEBRADO', '#FF5A4E'], ['FORTE', '#F4B414'], ['NORMAL', '#6FB487']]},
         'table': None,
         'news': ['URGENTE: júri do Halloween é um sofá e uma TV de tubo',
                  'Casa de Duskmourn pede para não ser chamada de "imóvel"',
                  'Lua de Innistrad: inquilina de 13 de mana continua lá dentro',
                  'Juiz confirma: fugir da casa não é ação de mana',
                  'Plantão anterior: o ladrão que virou Papai Noel']},
}
open('mb/episode.js', 'w').write('const EP = ' + json.dumps(ep, ensure_ascii=False) + ';')
for c in cenas: print(f"{c['nome']:11} {c['a']:6.2f} → {c['b']:6.2f}  ({c['b'] - c['a']:.2f}s)")
print('T_SLAM', T_SLAM, '| kit até', tl['FIM_KIT'], '| total com fecho', TOTAL, '| PRÉVIA' if tl['previa'] else '')
