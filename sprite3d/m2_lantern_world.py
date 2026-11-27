# The 2026-11-27 Meshy lantern on the off hand, with no hand (Tefa: "don't put hands on the weapons just yet, only make
# the guns and lantern"). A gz_world.py profile:
#   blender -b --factory-startup --python <cubekit>/gz_world.py -- m2_lantern_world.py
# It runs the September lantern's own profile (the lantern working folder's gz_cube_hands.py: the off-hand actors, the
# flicker, the light, the event handler) and then changes only what is drawn: the Meshy lantern's body, glass and
# tube take the place of the old models, and the bare left hand is never shown.
import os

M2_OUT = os.path.join("D:" + os.sep, "Ashes 2063", "3D blender", "meshy set 2026-11-27")
LANT = os.path.join("D:" + os.sep, "Ashes 2063", "3D blender", "ashes lantern", "blender")
_here_globals = globals()
_here_globals["PROFILE_DIR"] = LANT
exec(open(os.path.join(LANT, "gz_cube_hands.py"), encoding="utf-8").read(), _here_globals)

CUBE_M = 0.0034
OUT_DIR = os.path.join(M2_OUT, "pk3", "lantern")
os.makedirs(OUT_DIR, exist_ok=True)
PK3 = "Ashes2063_m2_lantern_VR_test.pk3"
MODEL_PATH = "models/ashes2063/m2lantern"
M2_BLEND = os.path.join(M2_OUT, "blend", "m2_lantern.blend")
M2_SKIN = os.path.join(M2_OUT, "blend", "textures", "m2_lantern_palette.png")
# m2_lantern.py: the carry bar's middle, in the blend's metres (forge x, y, z -> blend -y, x, z)
M2_GRIP = (0.5 * CUBE_M, 14.4 * CUBE_M, -19.0 * CUBE_M)
_lv = GLOW_LEVELS


def _m(name, actor, sprite, frames, objects):
    return dict(name=name, actor=actor, sprite=sprite, blend=M2_BLEND, skin="m2_lantern.png", skin_src=M2_SKIN,
                origin=M2_GRIP, rot=LANTERN_ROT, objects=objects, frames=frames)


_hand = [m for m in MODELS if m["actor"] == "TefaLeftHand"]
MODELS = [
    _m("m2_lantern_body", "TefaCubeLanternBody", "CLBD", [["m2_lantern_body"]], ["m2_lantern_body"]),
    _m("m2_lantern_glass", "TefaCubeLanternGlass", "CLGL", [["m2_lantern_glass"]] * _lv, ["m2_lantern_glass"]),
    # the haze and the lightning reuse the tube: an added glow over it that follows the same flicker
    _m("m2_lantern_haze", "TefaCubeLanternHaze", "CLHZ", [["m2_lantern_core"]] * _lv, ["m2_lantern_core"]),
    _m("m2_lantern_core", "TefaCubeLanternCore", "CLCO", [["m2_lantern_core"]] * _lv, ["m2_lantern_core"]),
    _m("m2_lantern_bolts", "TefaCubeLanternBolts", "CLBO", [[]] + [["m2_lantern_core"]] * BOLT_COUNT,
       ["m2_lantern_core"]),
] + _hand                                  # the hand's model stays in the pack only so its actor still has frames

_old = "bool wantHand = tracked && !lit && IsOneHanded(players[consoleplayer]);"
assert _old in ZSCRIPT, "the September profile changed: find where it decides to show the bare hand"
ZSCRIPT = ZSCRIPT.replace(_old, "bool wantHand = false;   // 2026-11-27: no hands for now (Tefa)")
