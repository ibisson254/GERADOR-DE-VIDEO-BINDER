#!/usr/bin/env python3
"""EP05 · classificação das 306 cartas do set principal de Star Trek (TRK).
Fonte do texto: Oracle via API do Scryfall (dados/trk_main_oracle.json, extraído a 05/11/2026).
Cada etiqueta sai do texto Oracle por regra (regex) ou de lista manual explícita; nada vem de resultados de jogo,
porque ainda não há jogos de TRK. Notas: dados/notas_limited_trk.csv (MTG Arena Zone, J2SJosh, nov/2026; Draftsim ÷ 2 em 5 cartas)."""
import csv, json, os, re
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARTAS = json.load(open(f'{D}/dados/trk_main_oracle.json'))
NOTA = {r['carta']: float(r['nota_0_5']) for r in csv.DictReader(open(f'{D}/dados/notas_limited_trk.csv'))}
PARES = ['WU', 'UB', 'BR', 'RG', 'GW', 'WB', 'UR', 'BG', 'RW', 'GU']
NOME_PAR = dict(WU='Azorius', UB='Dimir', BR='Rakdos', RG='Gruul', GW='Selesnya', WB='Orzhov', UR='Izzet', BG='Golgari', RW='Boros', GU='Simic')
PLANO = dict(WU='Spacecraft e artífices', UB='Dilemma', BR='Klingons e sacrifício', RG='Landfall', GW='Médicos e marcadores',
             WB='Borg, criaturas artefato', UR='Cientistas, não-criaturas', BG='Cemitério e recursão', RW='Poder total 8+', GU='Strange New Worlds')
# remoção: lista manual a partir do texto Oracle. DURA = responde a uma ameaça grande sem depender da mesa; LEVE = condicional, temporária ou pequena.
DURA = """70,000 Light-Years from Home|Malfunctioning Holodeck|He's Dead, Jim|Impossible Choice|Resistance Is Futile|Eject the Warp Core|Genesis Effect|
Khaaaaaaaaaaaannn!|The Wrath of Khan|Borg Cube|Rules of Acquisition|Guidance Failure""".replace('\n', '').split('|')
LEVE = """Command Decision|Set Phasers to . . .|U.S.S. Excelsior, Cutting Edge|Saavik, Stoic Student|Marooned|Bat'leth|D'Ghor Bloodletter|De-evolve|In the Pale Moonlight|
Armus, Skin of Evil|Planetary Bombardment|Plasma Cascade|Dahar Master|Transporter Malfunction|Khan, Despot by Design|Encounter the Unknown|Common Goal|Amok Time|Locutus, the One Who Speaks|
Engineered Explosives|Crystalline Entity""".replace('\n', '').split('|')
ANTIART = """70,000 Light-Years from Home|Guidance Failure|Malfunctioning Holodeck|Marooned|Perils of the Past|Test of Courage|Dathon and Picard at El-Adrel|Kirk, Commanding Officer|
Rules of Acquisition|Engineered Explosives|Subcommander T'Pol""".replace('\n', '').split('|')
# enablers que a regex não apanha
LANDFALL_E = """Final Frontier|Genesis Device|The Naked Time|Hit It!|U.S.S. Voyager, Lone Wanderer|Captain Kathryn Janeway|Will Riker, First in the Field|David and Carol Marcus, Creators|
Stable Wormhole|Erica Ortegas, Plucky Pilot|Saurian Explorer|Temporal Conqueror|Warp Speed|Captain Pike, Fullness of Time|Genesis Effect|Nog, Ambitious Cadet|Dal R'El, Augment Orphan""".replace('\n', '').split('|')
SPACE_P = """Warp Core|Emergency Holographic Crew|Rutherford, Upgraded Ensign|Zefram Cochrane, Warp Pioneer|Hemmer, Fixing What Is Broken|Lt. Cmdr. Geordi La Forge|Brad Boimler, Eager Ensign|
Federation Resupply|Sulu, Space Swashbuckler|Captain Jean-Luc Picard|Stray from History|Class-F Shuttlecraft""".replace('\n', '').split('|')
SAC_P = """Automated Warfare System|Battle-Scarred Survivalist|Dahar Master|Eject the Warp Core|A Good Day to Die|Planetary Bombardment|General Chang, Cold Warrior|Gowron, Eager for Battle|
Grand Nagus Zek|Khan, Vengeful Heart|L'Rell, Fierce Visionary|Vengeance Mission|Sarcophagus, Ship of the Dead|Targ Wrangler|In the Pale Moonlight|Excalbian Gamemaster|D'Ghor Bloodletter""".replace('\n', '').split('|')
KLINGON_E_X = """Boarding Action|Cha'DIch Investigator|The Duras Sisters|L'Rell, Fierce Visionary|D-7 Battle Cruiser""".split('|')
GRAVE_P = """Vash, Freelance Archaeologist|Sela, Tal Shiar Paradox|Blastoneuron|Hologram Stalker|Nog, Ambitious Cadet|De-evolve|Ravenous Cosmozoan|Relentless Drednok|Photosynthetic Physician|
Daniels, Temporal Agent|Stray from History|Test of Loyalty|Storied Veteran|Amok Time|The Inner Light|Dr. Leonard "Bones" McCoy|Sylvia Tilly, Joy of Discovery|Overflow Submatrix|U.S.S. Reliant, From Hell's Heart|Resistance Is Futile""".replace('\n', '').split('|')
COUNT_P = """Phlox, Unorthodox Doctor|Dominion Supervisor|Federation Field Medic|The Doctor, EMH|Dr. Joseph M'Benga|Dr. McCoy, Surly Surgeon|Brad Boimler, Eager Ensign|Support Mission|Sickbay""".replace('\n', '').split('|')
BORG_P = """Command Subadjunct|Conquest Mission|Primary Unimatrix Adjunct|Assault Drone|Collation Trimatrix|Collective Drone|Death Is Irrelevant|Hive Mind Coprocessor|Organic Avulsion Unit|
Overflow Submatrix|Resistance Is Futile|Borg Cube|Locutus, the One Who Speaks|Antagonist Incorporator""".replace('\n', '').split('|')
SNW_E_X = """Final Frontier|Warp Speed|Genesis Device""".split('|')
def tags(c):
    n, t = c['n'], c['t']; o = re.sub(r' ?\([^)]*\)', '', c['o']); ol = o.lower(); e = set(); p = set(); f = set()
    crit = 'Creature' in t; terreno = 'Land' in t; nave = 'Spacecraft' in t
    if crit: f.add('criatura')
    if n in DURA: f.add('remocao_dura')
    if n in LEVE: f.add('remocao_leve')
    if n in DURA or n in LEVE: f.add('remocao')
    if n in ANTIART: f.add('anti_artefato')
    if re.search(r'draw (a|two|three|x|\w+) cards?|investigate|you draw', ol): f.add('vantagem')
    if 'landcycling' in ol or re.search(r'search your library for a basic|add one mana of any color', ol): f.add('fixacao')
    # 1 Borg / criaturas artefato (WB)
    if 'Artifact Creature' in t or 'Artifact — ' in t and crit: e.add('borg')
    if n in BORG_P: p.add('borg')
    if 'Borg artifact creature token' in o: e.add('borg')
    # 2 Spacecraft (WU)
    if nave: e.add('nave')
    if n in SPACE_P: p.add('nave')
    # 3 Klingons e sacrifício (BR)
    if 'Klingon' in t or n in KLINGON_E_X: e.add('klingon')
    if n in SAC_P: p.add('klingon')
    # 4 não-criaturas (UR): toda mágica não-criatura, não-terreno, conta; naves contam (guia oficial)
    if not crit and not terreno: e.add('naocriatura')
    if 'noncreature spell' in ol and 'target noncreature' not in ol: p.add('naocriatura')
    # 5 Federation
    if 'Federation —' in o: p.add('federation')
    # 6 Dilemma (UB): escolher modos conta (lembrete Oracle)
    if re.search(r'choose (one|two|one or more)\b', ol) and 'nonland card name' not in ol: e.add('dilemma')
    if 'dilemma' in ol: p.add('dilemma')
    # 7 Landfall (RG)
    if 'Landfall' in o: p.add('landfall')
    if n in LANDFALL_E: e.add('landfall')
    # 8 Marcadores (GW)
    if re.search(r'\+1/\+1 counter', o) and n not in ('Sarek, Federation Ambassador',): e.add('marcadores')
    if n in COUNT_P: p.add('marcadores')
    # 9 Cemitério (BG)
    if re.search(r'\bsurveil\b|\bmill\b', ol): e.add('cemiterio')
    if n in GRAVE_P: p.add('cemiterio')
    # 10 Poder total 8 (RW)
    if 'total power 8' in ol: p.add('poder8')
    if re.search(r'creature tokens?|creatures you control get \+', ol) and 'artifact creatures you control' not in ol: e.add('poder8')
    # 11 Strange New Worlds (GU)
    if 'Strange new worlds' in o: p.add('snw')
    if (terreno and 'Basic' not in t) or n in SNW_E_X: e.add('snw')
    # transversais
    if 'beam me up' in ol and n != 'Marooned' and n != 'Scotty, Miracle Worker': e.add('beam')
    if re.search(r'return .* from your graveyard|from your graveyard to', ol): f.add('recursao')
    return e, p, f
for c in CARTAS:
    c['e'], c['pay'], c['f'] = tags(c)
    c['nota'] = NOTA.get(c['n'])
    cc = set(c['ci'])                       # híbridas e ouro: identidade de cor
    c['cores_set'] = cc
    c['terreno'] = 'Land' in c['t']
def cabe(c, par):
    return c['cores_set'] <= set(par)
def do_par(c, par):
    """carta jogável num deck de duas cores `par` (mono, ouro desse par, incolor)."""
    return cabe(c, par) and not c['terreno']
ROTULO = dict(borg='Borg/artefato', nave='Spacecraft', klingon='Klingon/sacrifício', naocriatura='Não-criaturas', federation='Federation', dilemma='Dilemma',
              landfall='Landfall', marcadores='Marcadores', cemiterio='Cemitério', poder8='Poder total 8', snw='Strange New Worlds', beam='Beam me up')
MECH_PAR = dict(WB='borg', WU='nave', BR='klingon', UR='naocriatura', UB='dilemma', RG='landfall', GW='marcadores', BG='cemiterio', RW='poder8', GU='snw')
if __name__ == '__main__':
    import collections
    print(len(CARTAS), collections.Counter(c['r'] for c in CARTAS))
    for k, lab in ROTULO.items():
        E = [c for c in CARTAS if k in c['e']]; P = [c for c in CARTAS if k in c['pay']]
        cu = lambda L: sum(1 for c in L if c['r'] in 'CU')
        print(f'{lab:22s} E={len(E):3d} (C/U {cu(E):3d})  P={len(P):3d} (C/U {cu(P):3d})')
    print('payoffs borg:', [c['n'] for c in CARTAS if 'borg' in c['pay']])
    print('payoffs naocriatura:', [c['n'] for c in CARTAS if 'naocriatura' in c['pay']])
    print('payoffs dilemma:', [c['n'] for c in CARTAS if 'dilemma' in c['pay']])
    print('E dilemma:', [c['n'] for c in CARTAS if 'dilemma' in c['e']])
    print('payoffs landfall:', [c['n'] for c in CARTAS if 'landfall' in c['pay']])
    print('payoffs snw:', [c['n'] for c in CARTAS if 'snw' in c['pay']])
    print('payoffs poder8:', [c['n'] for c in CARTAS if 'poder8' in c['pay']])
    print('E poder8:', [c['n'] for c in CARTAS if 'poder8' in c['e']])
    print('federation:', [c['n'] for c in CARTAS if 'federation' in c['pay']])
    print('E klingon:', [c['n'] for c in CARTAS if 'klingon' in c['e']])
    print('E marcadores:', [c['n'] for c in CARTAS if 'marcadores' in c['e']])
    print('naves:', [(c['n'],c['r']) for c in CARTAS if 'nave' in c['e']])
    print('remocao por cor/raridade:')
    for cor in 'WUBRG':
        L=[c for c in CARTAS if c['cores_set']=={cor} and 'remocao' in c['f']]
        print(cor, len(L), 'C:',[c['n'] for c in L if c['r']=='C'], 'U:',[c['n'] for c in L if c['r']=='U'])
    # tipos de criatura por carta
    import statistics
    T=[]
    for c in CARTAS:
        if 'Creature' in c['t'] and '—' in c['t']:
            T.append(len(c['t'].split('—')[1].split()))
    print('tipos por criatura', statistics.mean(T), collections.Counter(T))
