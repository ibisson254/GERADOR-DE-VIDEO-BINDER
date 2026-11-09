"""Vince Vault · caminhada de assinatura (V03, etapas C1 e D1) · Blender 5.2

Uso (o texto vem dentro do .blend):
    import bpy
    A = bpy.data.texts["vince_andar.py"].as_module()
    A.gerar("VINCE_swagger_lugar")                  # ciclo no lugar
    A.gerar("VINCE_swagger_desloca", desloca=True)  # com deslocação (osso root)
    A.usar("VINCE_swagger_lugar")
    A.conferir("VINCE_swagger_desloca")             # deslizamento dos pés, alcance do IK, loop

Rig de pernas (C1): ik_foot.L/R (controlo do pé, no chão, filho de root) ->
roll_heel (pivô no calcanhar) -> roll_toe (pivô na biqueira) -> ik_tgt (alvo do IK
no tornozelo). pole_knee.L/R (polo do joelho) é filho de ik_foot.
Convenção: frente = -Y; esquerda dele = +X (.L). Fase 0 = calcanhar esquerdo a pousar.
"""
import bpy, math
from mathutils import Matrix, Vector, Quaternion

RIG = "VINCE_rig"

# Parâmetros da caminhada (ângulos em graus, distâncias em metros)
P = dict(
    N=42,            # frames do ciclo (30 fps = 1,4 s)
    PASSO=0.42,      # distância que o pé percorre no chão durante o apoio
    APOIO=0.60,      # fração do ciclo com o pé no chão
    PISTA=0.115,     # afastamento lateral de cada pé
    PE_FORA=5.0,     # pontas dos pés para fora
    LEVANTA=0.065,   # altura do pé na passagem
    CALC=13.0,       # ponta levantada ao pousar o calcanhar
    BIQ=34.0,        # calcanhar levantado ao sair
    CALC_FIM=0.09, BIQ_INI=0.34,
    DESCE=0.014, SALTO=0.011, FASE_ALTO=0.32,   # altura da anca
    BALANCO=0.038,   # balanço lateral da anca
    ANCA_GIRO=9.0, ANCA_TOMBO=8.0,
    RECUO=3.5,       # tronco inclinado para trás
    PEITO_GIRO=15.0, PEITO_TOMBO=4.0, ACENTO=0.65,
    QUEIXO=7.0, CABECA_ATRASO=0.08,
    BRACO_E_BAIXA=25.0, BRACO_D_BAIXA=22.0,
    BRACO_E=12.0, BRACO_D=22.0,       # balanço: o direito é o mais solto
    BRACO_ATRAS=7.0,                  # centro do balanço puxado para trás
    ANTEBRACO_E=(3.0, 8.0), ANTEBRACO_D=(2.0, 16.0),
)

def _rig():
    return bpy.data.objects[RIG]

def _q(nome, rots):
    """Rotações em eixos do mundo (com o pai em repouso), aplicadas por ordem."""
    pb = _rig().pose.bones[nome]
    pb.rotation_mode = "QUATERNION"
    m = pb.bone.matrix_local.to_3x3()
    mi = m.inverted()
    q = Quaternion()
    for eixo, graus in rots:
        q = (mi @ Matrix.Rotation(math.radians(graus), 3, eixo) @ m).to_quaternion() @ q
    q.make_compatible(pb.rotation_quaternion)
    pb.rotation_quaternion = q

def _l(nome, vec):
    pb = _rig().pose.bones[nome]
    pb.location = pb.bone.matrix_local.to_3x3().inverted() @ Vector(vec)

def _sm(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)

def _c(fase):
    return math.cos(2 * math.pi * fase)

def _ac(s, e):
    return math.copysign(abs(s) ** e, s)

def _pe(p, par):
    """Pé na fase p (0 = pousa o calcanhar). Devolve y, z, calcanhar, biqueira."""
    S, D = par["PASSO"], par["APOIO"]
    p = p % 1.0
    if p < D:
        y = -S / 2 + S * p / D
        z = 0.0
        calc = -par["CALC"] * (1 - _sm(p / par["CALC_FIM"]))
        biq = par["BIQ"] * _sm((p - par["BIQ_INI"]) / (D - par["BIQ_INI"]))
    else:
        u = (p - D) / (1 - D)
        m = S * (1 - D) / D          # mesma velocidade do chão nas duas pontas
        y0, y1 = S / 2, -S / 2
        y = ((2*u**3 - 3*u**2 + 1) * y0 + (u**3 - 2*u**2 + u) * m
             + (-2*u**3 + 3*u**2) * y1 + (u**3 - u**2) * m)
        z = par["LEVANTA"] * math.sin(math.pi * u) ** 1.5
        biq = par["BIQ"] * (1 - _sm(u / 0.55))
        calc = -par["CALC"] * _sm((u - 0.45) / 0.55)
    return y, z, calc, biq

OSSOS_LOC = ["hips", "ik_foot.L", "ik_foot.R"]
OSSOS_ROT = ["hips", "spine", "chest", "neck", "head", "shoulder.L", "shoulder.R",
             "upper_arm.L", "upper_arm.R", "forearm.L", "forearm.R", "hand.L", "hand.R",
             "ik_foot.L", "ik_foot.R", "roll_heel.L", "roll_heel.R", "roll_toe.L", "roll_toe.R"]

def posar(fase, par=None):
    """Põe o corpo na fase (0..1) do ciclo, sem gravar chaves."""
    par = par or P
    f = fase % 1.0
    # pés
    for suf, s, off in ((".L", 1, 0.0), (".R", -1, 0.5)):
        y, z, calc, biq = _pe(f + off, par)
        _l("ik_foot" + suf, (s * par["PISTA"] - s * 0.12, y, z))
        _q("ik_foot" + suf, [("Z", s * par["PE_FORA"])])
        _q("roll_heel" + suf, [("X", calc)])
        _q("roll_toe" + suf, [("X", biq)])
    # anca: desce ao pousar, sobe na passagem, balança para a perna de apoio
    # o tombo roda em torno da anca de apoio: a anca de apoio mantém a altura, a outra cai
    tombo = -par["ANCA_TOMBO"] * _c(f - 0.31)
    _l("hips", (par["BALANCO"] * _c(f - 0.33), 0.0,
                -par["DESCE"] + par["SALTO"] * math.cos(4 * math.pi * (f - par["FASE_ALTO"]))
                - 0.12 * abs(math.sin(math.radians(tombo)))))
    _q("hips", [("Z", -par["ANCA_GIRO"] * _c(f - 0.02)),
                ("Y", tombo)])
    # tronco: recua, compensa a anca; ombros em contratempo, com acento
    _q("spine", [("X", -par["RECUO"]),
                 ("Z", 0.5 * par["ANCA_GIRO"] * _c(f - 0.02)),
                 ("Y", 0.6 * par["ANCA_TOMBO"] * _c(f - 0.31))])
    giro = par["PEITO_GIRO"] * _ac(_c(f - 0.05), par["ACENTO"])
    _q("chest", [("X", -2.0 + 1.5 * math.cos(4 * math.pi * (f - 0.12))),
                 ("Z", giro),
                 ("Y", (0.4 * par["ANCA_TOMBO"] + par["PEITO_TOMBO"]) * _c(f - 0.34))])
    # cabeça: queixo erguido, fica virada para a frente, com atraso
    total = par["PEITO_GIRO"] - 0.5 * par["ANCA_GIRO"]
    at = par["CABECA_ATRASO"]
    _q("neck", [("Z", -0.45 * total * _c(f - 0.05 - at * 0.6)),
                ("Y", -1.2 * _c(f - 0.34 - at))])
    _q("head", [("X", -par["QUEIXO"] + 1.6 * math.cos(4 * math.pi * (f - 0.14 - at))),
                ("Z", -0.45 * total * _c(f - 0.05 - at)),
                ("Y", -2.2 * _c(f - 0.34 - at))])
    # ombros: acompanham o braço e marcam o tempo
    for suf, s in ((".L", 1), (".R", -1)):
        _q("shoulder" + suf, [("Z", 4.0 * _c(f - 0.03)),
                              ("Y", -s * 1.8 * math.cos(4 * math.pi * (f - 0.42)))])
    # braços assimétricos: o esquerdo contido, o direito solto e com arrasto
    a0, a1 = par["ANTEBRACO_E"]
    _q("upper_arm.L", [("Y", par["BRACO_E_BAIXA"]), ("X", par["BRACO_ATRAS"] + par["BRACO_E"] * _c(f - 0.03))])
    _q("forearm.L", [("X", -(a0 + a1 * (0.5 - 0.5 * _c(f - 0.09))))])
    _q("hand.L", [("X", 4.0 * _c(f - 0.20))])
    b0, b1 = par["ANTEBRACO_D"]
    _q("upper_arm.R", [("Y", -par["BRACO_D_BAIXA"]), ("X", par["BRACO_ATRAS"] - par["BRACO_D"] * _c(f - 0.06)),
                       ("Z", -4.0 * _c(f - 0.06))])
    _q("forearm.R", [("X", -(b0 + b1 * (0.5 + 0.5 * _c(f - 0.14))))])
    _q("hand.R", [("X", -6.0 * _c(f - 0.27))])

def velocidade(par=None):
    """Metros por frame a que o chão passa (e a que o root avança)."""
    par = par or P
    return par["PASSO"] / (par["APOIO"] * par["N"])

def _fcurves(rig):
    ad = rig.animation_data
    act = ad.action
    out = []
    for layer in act.layers:
        for strip in layer.strips:
            cb = strip.channelbag(ad.action_slot)
            if cb:
                out.extend(cb.fcurves)
    return out

def gerar(nome="VINCE_swagger_lugar", desloca=False, frame_inicio=1, **mudar):
    """Cria (ou refaz) a ação com o ciclo. Uma chave por frame; loop por modificador."""
    par = dict(P); par.update(mudar)
    rig = _rig()
    sc = bpy.context.scene
    velha = bpy.data.actions.get(nome)
    if velha:
        bpy.data.actions.remove(velha)
    act = bpy.data.actions.new(nome)
    act.use_fake_user = True
    rig.animation_data_create()
    rig.animation_data.action = act
    for pb in rig.pose.bones:
        pb.rotation_mode = "QUATERNION"
        pb.rotation_quaternion = (1, 0, 0, 0); pb.location = (0, 0, 0)
    N = par["N"]
    for i in range(N + 1):
        fr = frame_inicio + i
        posar(i / N, par)
        for n in OSSOS_LOC:
            rig.pose.bones[n].keyframe_insert("location", frame=fr, group=n)
        for n in OSSOS_ROT:
            rig.pose.bones[n].keyframe_insert("rotation_quaternion", frame=fr, group=n)
    v = velocidade(par)
    root = rig.pose.bones["root"]
    if desloca:
        for i in (0, N):
            _l("root", (0, -v * i, 0))
            root.keyframe_insert("location", frame=frame_inicio + i, group="root")
        root.location = (0, 0, 0)
    for fc in _fcurves(rig):
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
        if fc.data_path.startswith('pose.bones["root"]'):
            fc.extrapolation = "LINEAR"
        else:
            fc.modifiers.new("CYCLES")
        fc.update()
    act["vince_parametros"] = {k: (list(x) if isinstance(x, tuple) else x) for k, x in par.items()}
    sc.frame_start = frame_inicio
    sc.frame_end = frame_inicio + N - 1
    sc.frame_set(frame_inicio)
    return {"acao": nome, "frames": N, "m_por_ciclo": round(v * N, 4), "m_por_s": round(v * sc.render.fps, 3)}

def usar(nome):
    rig = _rig()
    rig.animation_data_create()
    act = bpy.data.actions[nome]
    rig.animation_data.action = act
    if act.slots:
        rig.animation_data.action_slot = act.slots[0]
    for pb in rig.pose.bones:
        pb.location = (0, 0, 0); pb.rotation_quaternion = (1, 0, 0, 0)
    bpy.context.scene.frame_set(bpy.context.scene.frame_start)

def parar():
    """Tira a ação do rig e volta à pose em A."""
    rig = _rig()
    if rig.animation_data:
        rig.animation_data.action = None
    for pb in rig.pose.bones:
        pb.location = (0, 0, 0); pb.rotation_quaternion = (1, 0, 0, 0)
    bpy.context.view_layer.update()

# Pontos de contacto do sapato, em repouso (mundo)
_CONTACTO = {"calc": (0.12, 0.105, 0.0), "biq": (0.135, -0.205, 0.0)}

def conferir(nome, ciclos=2):
    """Mede, na ação dada: deslizamento do pé de apoio (mm por frame, no mundo),
    pé abaixo do chão, alcance do IK e salto no loop."""
    usar(nome)
    rig = _rig(); sc = bpy.context.scene
    act = bpy.data.actions[nome]
    par = dict(P); par.update({k: v for k, v in dict(act.get("vince_parametros", {})).items()})
    N = int(par["N"]); D = par["APOIO"]
    v = velocidade(par)
    desloca = any(fc.data_path.startswith('pose.bones["root"]') for fc in _fcurves(rig))
    mw = rig.matrix_world
    loc = {}
    for suf, s in ((".L", 1), (".R", -1)):
        b = rig.data.bones["foot" + suf]
        for k, pnt in _CONTACTO.items():
            loc[(suf, k)] = b.matrix_local.inverted() @ Vector((s * pnt[0], pnt[1], pnt[2]))
    comp = {}
    for suf in (".L", ".R"):
        comp[suf] = rig.data.bones["thigh" + suf].length + rig.data.bones["shin" + suf].length
    ant = {}; desl = 0.0; desl_onde = None; zmin = 1.0; ext = 0.0; err = 0.0
    f0 = sc.frame_start
    for i in range(ciclos * N + 1):
        sc.frame_set(f0 + i)
        bpy.context.view_layer.update()
        for suf, off in ((".L", 0.0), (".R", 0.5)):
            pb = rig.pose.bones["foot" + suf]
            p = (i / N + off) % 1.0
            pts = {k: mw @ pb.matrix @ loc[(suf, k)] for k in _CONTACTO}
            # no ciclo no lugar, o chão anda: compensar para medir o deslizamento real
            if not desloca:
                for k in pts:
                    pts[k] = pts[k] - Vector((0, v * i, 0))
            zmin = min(zmin, pts["calc"].z, pts["biq"].z)
            activos = []
            if p < D - 1e-6:
                if p < par["BIQ_INI"]:
                    activos.append("calc")
                if p >= par["CALC_FIM"]:
                    activos.append("biq")
            for k in activos:
                chave = (suf, k)
                if chave in ant and ant[chave][0] == i - 1:
                    d = (pts[k] - ant[chave][1]).length
                    if d > desl:
                        desl = d; desl_onde = (suf, k, i)
                ant[chave] = (i, pts[k].copy())
            th = rig.pose.bones["thigh" + suf]; tg = rig.pose.bones["ik_tgt" + suf]
            ext = max(ext, (tg.head - th.head).length / comp[suf])
            err = max(err, (pb.head - tg.head).length)
    # loop: pose do frame 1 contra a do frame N+1
    def foto(fr):
        sc.frame_set(fr); bpy.context.view_layer.update()
        return {pb.name: pb.matrix.copy() for pb in rig.pose.bones if pb.name != "root"}
    a = foto(f0); b = foto(f0 + N)
    dy = Vector((0, -v * N, 0)) if desloca else Vector((0, 0, 0))
    salto = max(((b[n].translation - dy) - a[n].translation).length for n in a)
    sc.frame_set(f0)
    return {"acao": nome, "desloca": desloca,
            "deslize_max_mm_por_frame": round(desl * 1000, 3), "onde": desl_onde,
            "ponto_mais_baixo_mm": round(zmin * 1000, 2),
            "extensao_max_perna": round(ext, 4), "erro_ik_mm": round(err * 1000, 3),
            "salto_loop_mm": round(salto * 1000, 3)}
