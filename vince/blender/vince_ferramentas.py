"""Vince Vault · ferramentas do rig (Blender 5.2)

Uso no separador Scripting do Blender (este texto já vem dentro do .blend):
    import bpy
    V = bpy.data.texts["vince_ferramentas.py"].as_module()
    V.aplicar_expressao("confiante", frame=1)
    V.pose("neutra")                             # corpo (v02), depois da expressão
    V.importar_rhubarb(r"C:\\...\\gancho.tsv", frame_inicio=1)

Expressões aprovadas (FICHA_VISUAL §8): neutro, confiante, rindo, furioso,
chocado, desesperado, sarcastico, pensativo, euforico.

Lip sync: gerar o .tsv com o Rhubarb Lip Sync a partir do áudio do ElevenLabs
    rhubarb -f tsv -o gancho.tsv gancho.wav
As formas A–H e X do Rhubarb correspondem às propriedades boca_A … boca_H
do controlo VINCE_rosto (X = boca em repouso).
"""
import bpy

ROSTO = "VINCE_rosto"
OCULOS = "OCULOS_ctrl"
BOCAS_LIPSYNC = ["boca_" + c for c in "ABCDEFGH"]

EXPRESSOES = {
    "neutro":      {},
    "confiante":   {"boca_sorriso": 0.55, "boca_sarcasmo": 0.45, "sobr_E_sobe": 0.35},
    "rindo":       {"boca_riso": 1.0, "sobr_E_sobe": 0.5, "sobr_D_sobe": 0.5,
                    "palpebra_E": 0.4, "palpebra_D": 0.4},
    "furioso":     {"boca_furia": 1.0, "sobr_E_zanga": 1.0, "sobr_D_zanga": 1.0,
                    "sobr_E_sobe": -0.3, "sobr_D_sobe": -0.3,
                    "palpebra_E": 0.2, "palpebra_D": 0.2},
    "chocado":     {"boca_choque": 1.0, "sobr_E_sobe": 1.0, "sobr_D_sobe": 1.0,
                    "sobr_E_zanga": -0.4, "sobr_D_zanga": -0.4},
    "desesperado": {"boca_triste": 1.0, "sobr_E_zanga": -1.0, "sobr_D_zanga": -1.0,
                    "sobr_E_sobe": 0.4, "sobr_D_sobe": 0.4,
                    "palpebra_E": 0.1, "palpebra_D": 0.1},
    "sarcastico":  {"boca_sarcasmo": 1.0, "sobr_E_sobe": 0.8, "sobr_D_sobe": -0.3,
                    "palpebra_E": 0.4, "palpebra_D": 0.45},
    "pensativo":   {"boca_pensativo": 1.0, "sobr_E_sobe": 0.6, "sobr_D_zanga": 0.5,
                    "olhar_x": 0.6, "olhar_z": 0.7},
    "euforico":    {"boca_riso": 1.0, "sobr_E_sobe": 1.0, "sobr_D_sobe": 1.0},
}


def _rosto():
    return bpy.data.objects[ROSTO]


def _atualizar():
    r = _rosto()
    r.update_tag(refresh={"OBJECT", "DATA", "TIME"})
    bpy.context.view_layer.update()
    sc = bpy.context.scene
    sc.frame_set(sc.frame_current)


def _props_float(r):
    return [k for k in r.keys() if isinstance(r[k], float)]


def aplicar_expressao(nome, frame=None, manter_boca=False):
    """Põe a expressão no rosto. Com frame, grava chave nesse frame.
    manter_boca=True deixa as bocas do lip sync intactas."""
    r = _rosto()
    valores = EXPRESSOES[nome]
    for k in _props_float(r):
        if manter_boca and k in BOCAS_LIPSYNC:
            continue
        r[k] = float(valores.get(k, 0.0))
        if frame is not None:
            r.keyframe_insert(data_path=f'["{k}"]', frame=frame)
    _atualizar()


def oculos(no_topete=True, frame=None):
    o = bpy.data.objects[OCULOS]
    o["no_topete"] = 1.0 if no_topete else 0.0
    if frame is not None:
        o.keyframe_insert(data_path='["no_topete"]', frame=frame)
    o.update_tag()
    _atualizar()


def importar_rhubarb(caminho_tsv, frame_inicio=1, fps=None):
    """Lê o .tsv do Rhubarb e grava chaves (constantes) nas bocas A–H."""
    sc = bpy.context.scene
    fps = fps or sc.render.fps / sc.render.fps_base
    r = _rosto()
    linhas = []
    with open(caminho_tsv, encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            t, forma = ln.split("\t")[:2]
            linhas.append((float(t), forma.strip().upper()))
    for t, forma in linhas:
        fr = frame_inicio + round(t * fps)
        for k in BOCAS_LIPSYNC:
            r[k] = 1.0 if k == "boca_" + forma else 0.0
            r.keyframe_insert(data_path=f'["{k}"]', frame=fr)
    # interpolação constante: a boca troca de forma no frame certo, sem papa
    ad = r.animation_data
    if ad and ad.action:
        for fc in _fcurves(ad):
            if any(fc.data_path == f'["{k}"]' for k in BOCAS_LIPSYNC):
                for kp in fc.keyframe_points:
                    kp.interpolation = "CONSTANT"
    if linhas:
        sc.frame_end = max(sc.frame_end, frame_inicio + round(linhas[-1][0] * fps))
    _atualizar()
    return len(linhas)


def _fcurves(ad):
    act = ad.action
    if hasattr(act, "fcurves") and len(getattr(act, "fcurves", [])):
        return list(act.fcurves)
    # ações em camadas (Blender 4.4+)
    out = []
    for layer in getattr(act, "layers", []):
        for strip in layer.strips:
            slot = ad.action_slot
            cb = strip.channelbag(slot) if slot else None
            if cb:
                out.extend(cb.fcurves)
    return out


# ---------------------------------------------------------------- corpo (v02)
# Convenção: "E" = esquerda dele (+X, ossos .L); "D" = direita dele (ossos .R).
import math
from mathutils import Matrix, Vector

RIG = "VINCE_rig"
_SUF = {"E": ".L", "D": ".R"}


def _rig():
    return bpy.data.objects[RIG]


def _girar(osso, eixo, graus):
    """Roda um osso em eixos do mundo (eixo: 'X','Y','Z' ou vetor), a somar à pose."""
    pb = _rig().pose.bones[osso]
    pb.rotation_mode = "QUATERNION"
    m = pb.bone.matrix_local.to_3x3()
    if isinstance(eixo, str):
        R = Matrix.Rotation(math.radians(graus), 3, eixo)
    else:
        R = Matrix.Rotation(math.radians(graus), 3, Vector(eixo).normalized())
    pb.rotation_quaternion = (m.inverted() @ R @ m).to_quaternion() @ pb.rotation_quaternion


def _chave(ossos, frame):
    if frame is None:
        return
    for n in ossos:
        _rig().pose.bones[n].keyframe_insert("rotation_quaternion", frame=frame)


def repouso(frame=None):
    """Volta à pose em A (a pose em que o modelo foi gerado)."""
    r = _rig()
    for pb in r.pose.bones:
        pb.rotation_mode = "QUATERNION"
        pb.rotation_quaternion = (1, 0, 0, 0)
        pb.location = (0, 0, 0)
    _chave([pb.name for pb in r.pose.bones], frame)
    bpy.context.view_layer.update()


# Cada pose: lista de (osso, eixo do mundo, graus). Nos braços, Y positivo no
# lado E baixa o braço; no lado D é o sinal contrário.
POSES = {
    "A": [],
    "neutra": [("upper_arm.L", "Y", 20), ("upper_arm.R", "Y", -20),
               ("forearm.L", "X", -12), ("forearm.R", "X", -12)],
    "braco_ao_lado": [("upper_arm.L", "Y", 20), ("forearm.L", "X", -12),
                   ("upper_arm.R", "Y", 10), ("upper_arm.R", "Z", -35),
                   ("forearm.R", "X", -70), ("head", "Z", 10)],
    "bracos_abertos": [("upper_arm.L", "Y", -25), ("upper_arm.R", "Y", 25),
                       ("forearm.L", "X", -25), ("forearm.R", "X", -25),
                       ("chest", "X", -6)],
    "aceno": [("upper_arm.L", "Y", 20), ("forearm.L", "X", -12),
               ("upper_arm.R", "Y", -15), ("upper_arm.R", "X", -35),
               ("forearm.R", "X", -110), ("head", "Z", 8), ("head", "X", 6)],
}


def pose(nome, frame=None):
    """Aplica uma pose de corpo. Chamar depois de aplicar_expressao()."""
    repouso()
    for osso, eixo, graus in POSES[nome]:
        _girar(osso, eixo, graus)
    _chave([pb.name for pb in _rig().pose.bones], frame)
    bpy.context.view_layer.update()


def piscar(frame, duracao=4):
    """Pestanejo: fecha e abre as duas pálpebras em `duracao` frames."""
    r = _rosto()
    for k in ("palpebra_E", "palpebra_D"):
        base = float(r[k])
        for f, v in ((frame, base), (frame + duracao // 2, 1.0), (frame + duracao, base)):
            r[k] = v
            r.keyframe_insert(data_path=f'["{k}"]', frame=f)
        r[k] = base
    _atualizar()


def olhar(x=0.0, z=0.0, frame=None):
    """Direção do olhar: x de -1 (direita dele) a 1 (esquerda dele); z de -1 a 1."""
    r = _rosto()
    for k, v in (("olhar_x", x), ("olhar_z", z)):
        r[k] = float(v)
        if frame is not None:
            r.keyframe_insert(data_path=f'["{k}"]', frame=frame)
    _atualizar()
