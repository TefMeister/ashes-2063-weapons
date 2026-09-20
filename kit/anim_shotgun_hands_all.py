# ONE file holding the shotgun, GLOVED HANDS, and EVERY animation on a single timeline.
# Asked for by Tefa, 2026-09-20: "make a new blender file, one with all the animation, and add
# hands to the gun".
#
#   blender --python kit/anim_shotgun_hands_all.py          (watch it build, in a window)
#   blender -b --factory-startup --python kit/run_background.py -- anim_shotgun_hands_all.py
#
# WHY IT RE-USES THE EXISTING ANIMATION FILES RATHER THAN RE-TYPING THEM
# The timing in anim_shotgun_shoot1.py and anim_shotgun_reload.py was read tic-for-tic out of the
# mod's own Actors/Weapons/Shotgun.txt, and the 164-tic dry reload was checked against Tefa's own
# 162-screenshot recording. That is the expensive part and it is already right. So this script
# RUNS those two files, with four of their helpers temporarily replaced so that instead of each
# one clearing the scene and saving its own .blend, they all key into one scene at an offset.
# Nothing in either file is edited. If the timing is corrected there, it is corrected here too.
#
# THE TIMELINE (markers are added, so the ranges are findable in Blender)
#   SHOOT           the shot and the pump stroke that follows
#   RELOAD_FULL     fired dry: cycle the action, then six shells
#   RELOAD_PARTIAL  topping up: no opening cycle, three shells
# A gap of GAP frames sits between them so one animation's last pose cannot bleed into the next.
import sys
import os

# KIT is handed in by run_background.py, which exec()s this file and so leaves __file__ undefined.
# Running this file directly (blender --python ...) defines __file__ instead.
KIT = globals().get("KIT") or os.path.dirname(os.path.abspath(__file__))


def _read(name):
    # utf-8-sig, because several kit files carried a byte-order mark for a while and a BOM read
    # as text is a syntax error the moment the file is exec'd.
    return open(os.path.join(KIT, name), encoding="utf-8-sig").read()


exec(_read("anim_kit.py"))
exec(_read("shotgun_settings.py"))
exec(_read("shotgun_hands.py"))

OUT = os.path.join(KIT, "..", "shotgun", "Ashes_2063_EP1_shotgun_hands_all.blend")
OUT = os.path.abspath(OUT)

# STATIC=True gives the twin where the gun body itself never moves and only its parts do
# (the standing rule: every weapon animation gets a stay-put version as well).
STATIC = globals().get("STATIC", False)
if STATIC:
    OUT = OUT.replace(".blend", "_static.blend")

GAP = 12                      # blank frames between one animation and the next

# ---------------------------------------------------------------------------
# Build the scene ONCE: the gun, the hands, the first-person camera.
# ---------------------------------------------------------------------------
reset_scene()
setup_scene("Shotgun_Hands_All", 1)
_ov, _O = link_model(MODEL, "SHOTGUN")
_cam = fp_view(lens=VIEW_LENS_SG)

_coll = bpy.context.scene.collection
_hand_l, _hand_r = build_hands(_O["SG_Root"], _O["SG_Pump"], _coll, globals())
print("hands built:", _hand_l.name, "->", _hand_l.parent.name,
      "|", _hand_r.name, "->", _hand_r.parent.name)

# ---------------------------------------------------------------------------
# Run each animation file into this one scene, at an offset.
# ---------------------------------------------------------------------------
_real = {"reset_scene": reset_scene, "setup_scene": setup_scene, "link_model": link_model,
         "fp_view": fp_view, "side_view": side_view, "finish": finish, "key": key}
_offset = 0
_end_of_last = 0
_last_globals = {}


def _noop(*a, **k):
    return None


def _link_model_again(*a, **k):
    return _ov, _O


def _fp_view_again(*a, **k):
    return _cam


def _key_offset(obj, frame, **kw):
    return _real["key"](obj, frame + _offset, **kw)


def _finish_capture(path, frame_end):
    global _end_of_last
    _end_of_last = _offset + frame_end


def _without_kit_imports(src):
    """Drop an animation script's own `exec(open(... kit file ...))` lines.

    ⚠️ This is not tidiness, it is the whole thing working. Each animation script re-runs
    anim_kit.py and shotgun_settings.py at its top, which RE-DEFINES key(), finish(),
    reset_scene() and link_model() in its namespace and throws away the replacements handed
    to it. The first run of this driver did exactly that: all three scripts saved over the
    real per-animation .blend files, and every offset came back as zero. The driver has
    already loaded both kit files, so removing these lines loses nothing.
    """
    keep = []
    for line in src.splitlines(True):
        s = line.strip()
        if s.startswith("exec(open(") and ("anim_kit.py" in s or "pixel_kit.py" in s
                                           or "shotgun_settings.py" in s):
            keep.append("# [removed by anim_shotgun_hands_all.py] " + line)
        else:
            keep.append(line)
    return "".join(keep)


def run(script, offset, argv_extra=(), label=""):
    """Run one animation script into the shared scene, starting at `offset`."""
    global _offset, _end_of_last
    _offset = offset
    old_argv = list(sys.argv)
    sys.argv = old_argv + (["--"] if "--" not in old_argv else []) + list(argv_extra)
    g = dict(globals())
    g.update({"reset_scene": _noop, "setup_scene": _noop, "link_model": _link_model_again,
              "fp_view": _fp_view_again, "side_view": _noop, "finish": _finish_capture,
              "key": _key_offset, "STATIC": STATIC, "__name__": "__main__"})
    src = _without_kit_imports(open(os.path.join(KIT, script), encoding="utf-8").read())
    # Belt and braces after the first run overwrote three good files: while another script is
    # running, saving is physically unavailable, whatever it thinks it is calling.
    real_save = bpy.ops.wm.save_as_mainfile

    def _refuse_save(*a, **k):
        raise RuntimeError("a sub-script tried to save its own .blend (%s)" % script)

    bpy.ops.wm.save_as_mainfile = _refuse_save
    global _last_globals
    try:
        exec(compile(src, os.path.join(KIT, script), "exec"), g)
    finally:
        bpy.ops.wm.save_as_mainfile = real_save
        sys.argv = old_argv
    _last_globals = g          # the sub-script's own namespace, for LOAD_WINDOWS and PORT_IN
    mk = bpy.context.scene.timeline_markers.new(label, frame=offset + 1)
    mk.select = False
    print("  %-16s frames %d - %d" % (label, offset + 1, _end_of_last))
    return _end_of_last


# ---------------------------------------------------------------------------
# The trigger hand during a reload.
#
# Tefa, 2026-09-20: "the right hand needs to come off the weapon while left hand holds the front,
# so right hand can insert shells into the gun". So it does exactly that: lets go of the grip as
# the gun tips over, then makes one trip per shell - down out of sight, up with a round, push it
# into the port - and takes the grip back at the end.
#
# The hand is parented to SG_Root, so these are positions RELATIVE TO THE GUN, which is what we
# want: the loading port is on the gun, so the hand meets it wherever the gun is pointing.
# ---------------------------------------------------------------------------
GRIP_CENTRE = (0.026, -0.046, REC_Z - 0.004)    # where the hand's geometry sits when gripping
HOLD_OFF = (0.008, -0.038, -0.004)              # hand sits just behind the shell it is holding
AWAY = (0.055, -0.090, -0.150)                  # off the gun entirely, down by the player's waist


def _hand_at(shell_loc):
    """Where the hand object must sit for its fingers to be on a shell at shell_loc."""
    return tuple(s - g + o for s, g, o in zip(shell_loc, GRIP_CENTRE, HOLD_OFF))


def reload_hand(hand, offset, g, reload_end):
    """Key the trigger hand across one whole reload."""
    wins = [(f0 + offset, ln) for f0, ln in g["LOAD_WINDOWS"]]
    port_in = g["PORT_IN"]
    K = _real["key"]

    K(hand, offset + 1, loc=(0, 0, 0), rot_deg=(0, 0, 0))          # still on the grip

    # Let go while the gun tips over. Two hops, because everything here is stop-motion.
    first = wins[0][0]
    K(hand, max(offset + 2, first - 10), loc=(0.030, -0.050, -0.070), rot_deg=(-10, 0, -6))
    K(hand, max(offset + 3, first - 4), loc=AWAY, rot_deg=(-22, 0, -12))

    # One trip per shell, following the same path the shell itself takes.
    for f0, ln in wins:
        path = [(0.00, (0.030, -0.022, -0.155), (-25, 0, -12)),
                (0.25, (0.020, 0.010, -0.095), (-15, 0, -7)),
                (0.50, (0.010, 0.034, -0.040), (-6, 0, -3)),
                (0.70, port_in, (0, 0, 0)),
                (0.82, (0, port_in[1] + 0.012, port_in[2] + 0.004), (0, 0, 0)),
                (0.95, AWAY, (-22, 0, -12))]          # back down for the next one
        for t, loc, rot in path:
            K(hand, round(f0 + ln * t), loc=_hand_at(loc), rot_deg=rot)

    # Take the grip back as the gun comes down.
    last_end = wins[-1][0] + wins[-1][1]
    K(hand, min(last_end + 3, reload_end - 6), loc=(0.030, -0.050, -0.070), rot_deg=(-10, 0, -6))
    K(hand, reload_end - 2, loc=(0, 0, 0), rot_deg=(0, 0, 0))


f = run("anim_shotgun_shoot1.py", 0, label="SHOOT")
# The trigger hand never leaves the gun while shooting, but it has to be keyed here anyway: keys
# are CONSTANT, so without one at the start of each block it would still be holding whatever pose
# the previous animation left it in.
_real["key"](_hand_r, 1, loc=(0, 0, 0), rot_deg=(0, 0, 0))

start = f + GAP
f = run("anim_shotgun_reload.py", start, label="RELOAD_FULL")
reload_hand(_hand_r, start, _last_globals, f)

start = f + GAP
f = run("anim_shotgun_reload.py", start, argv_extra=["partial"], label="RELOAD_PARTIAL")
reload_hand(_hand_r, start, _last_globals, f)

if STATIC:
    _real["side_view"](_O["SG_Root"], (-0.95, 0.15, 0.13), (0, 0.15, 0.02))

_real["finish"](OUT, f)
print("ALL-IN-ONE saved:", OUT, "| last frame:", f)
