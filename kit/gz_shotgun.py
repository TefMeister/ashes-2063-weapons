# How the shotgun goes into GZDoom: which animation files, size, pivot, and which game
# sprite frame shows which Blender frame. Used by gz_export.py. Same shape as gz_revolver.py.
NAME = "shotgun"                             # file names inside the pk3
ACTOR_CLASS = "pumpaction"                   # ⚠️ the GAME's class for this gun, which MODELDEF
                                             # keys on. `pumpaction2` is the Classic shotgun,
                                             # a different weapon with different sprites.
ROOT = "SG_Root"
DIR = r"C:\Users\TD3KX\ashes-2063-weapons\shotgun"
OUT_DIR = DIR + r"\gzdoom"
PK3 = "Ashes2063_shotgun3d_test.pk3"         # the flat build; the VR build overrides this below
MODEL_PATH = "models/ashes2063/shotgun"      # folder inside the pk3

# ---------------------------------------------------------------------------
# Only the frames a sprite letter actually points at are exported. A 194-frame MD3 of a
# gun this size would be tens of megabytes in the repo, and the game can never show a
# frame no letter names. Keep these lists and SPRITES below in step.
# ---------------------------------------------------------------------------
SHOOT_FRAMES = [1, 2, 3, 4, 8, 10, 13, 14, 15, 16, 17, 20, 22, 24, 26, 28, 30]
RELOAD_FRAMES = [28, 30, 32, 34, 36, 38, 40, 41, 44, 50, 56, 58, 61, 64, 68,
                 75, 77, 79, 81, 83, 84, 85, 86, 87, 88]

ANIMS = [
    ("shoot1", DIR + r"\Ashes_2063_EP1_shotgun_shoot1.blend", SHOOT_FRAMES),
    ("reload", DIR + r"\Ashes_2063_EP1_shotgun_reload.blend", RELOAD_FRAMES),
]
# `reload_partial` is deliberately NOT exported: the game's partial reload replays the same
# GRIR letters as the loop in the full one, so it would add frames nothing can show.

# Two builds, exactly as for the revolver (see kit/gz_revolver.py for why):
# - flat: model space is the Blender first-person camera, eye at the origin.
# - vr: real centimetres, hung off the controller; the hand sits at MD3 (30, 0, -5).
if VARIANT == "vr":
    SPACE = "hand"
    UNITS_PER_M = 100
    # A shotgun is held at the WRIST, not at a pistol grip: the trigger hand sits under the
    # receiver, about 6 cm behind its rear face and 3 cm below the bore line in model space.
    # Starting point only — the revolver's took seven wears to settle. [hypothesis 2026-09-19]
    GRIP = (0.0, -0.055, 0.020)
    # The revolver ended up 9 cm below the engine's hand point and a little back; a long gun
    # rests lower in the hand still, so start from the same drop.
    VR_GRIP_DROP = 0.09
    VR_NUDGE_RIGHT, VR_NUDGE_BACK, VR_NUDGE_DOWN = 0.0, 0.03, 0.0
    # The player tilts the controller by instinct while reloading, so keep only part of the
    # whole-gun movement, as the revolver's reload does.
    GUN_MOTION_SCALE = {"reload": 0.4}
    ORIGIN = (GRIP[0] - VR_NUDGE_RIGHT,
              GRIP[1] - 0.30 + VR_NUDGE_BACK,
              GRIP[2] + 0.05 + VR_GRIP_DROP + VR_NUDGE_DOWN)
    PK3 = "Ashes2063_shotgun3d_VR_test.pk3"
else:
    SPACE = "view"
    UNITS_PER_M = 250
    ORIGIN = (0.0, 0.0, 0.0)

# ---------------------------------------------------------------------------
# Sprite frame -> (animation, Blender frame). Read from Actors/Weapons/Shotgun.txt, actor
# `pumpaction`. One sprite letter can only ever show one pose, and this sheet reuses letters:
#
#  - GRIP B and C appear TWICE: once as the recoil settling (GRIP C 4 tics, B 2 tics, right
#    after the shot) and once inside the pump stroke. They are mapped to the RECOIL poses,
#    which last 6 tics against 1 tic each in the stroke. The cost is that the pump stroke
#    starts about three tics late; the gain is that nothing ever jumps backwards.
#  - GRIR A-E are the gun tipping over to be loaded, and ReloadDone plays E D C B A to bring
#    it back. The same poses serve both, which is almost certainly why the artist drew it that way.
#  - GRIR P-Y are ONE shell going in. The game loops them once per shell, so the model needs
#    only one cycle (frames 75-88 of the reload, which is shell two).
# ---------------------------------------------------------------------------
SPRITES = [
    ("GRIZ", "A", "shoot1", 30),                                     # ready

    # FireReal: the shot, then the recoil settling
    ("GRIF", "A", "shoot1", 1), ("GRIF", "B", "shoot1", 2), ("GRIF", "C", "shoot1", 3),
    ("GRIP", "C", "shoot1", 4), ("GRIP", "B", "shoot1", 8),

    # Pump: back, held open while the shell is thrown, then forward
    ("GRIP", "A", "shoot1", 10), ("GRIP", "D", "shoot1", 13), ("GRIP", "E", "shoot1", 14),
    ("GRIP", "F", "shoot1", 15), ("GRIP", "G", "shoot1", 16), ("GRIP", "H", "shoot1", 17),
    ("GRIP", "I", "shoot1", 20), ("GRIP", "J", "shoot1", 22), ("GRIP", "K", "shoot1", 24),
    ("GRIP", "L", "shoot1", 26), ("GRIP", "M", "shoot1", 28),

    # Reload: tipping the gun over (and, reversed, bringing it back)
    ("GRIR", "A", "reload", 28), ("GRIR", "B", "reload", 30), ("GRIR", "C", "reload", 32),
    ("GRIR", "D", "reload", 34), ("GRIR", "E", "reload", 36), ("GRIR", "F", "reload", 38),
    ("GRIR", "Z", "reload", 40), ("GRIR", "H", "reload", 41), ("GRIR", "I", "reload", 44),

    # Reload: the first shell of a dry gun, and the action closing on it
    ("GRIR", "J", "reload", 50), ("GRIR", "K", "reload", 56), ("GRIR", "L", "reload", 58),
    ("GRIR", "M", "reload", 61), ("GRIR", "N", "reload", 64), ("GRIR", "O", "reload", 68),

    # Reload: one shell of the loop, replayed for every shell after the first
    ("GRIR", "P", "reload", 75), ("GRIR", "Q", "reload", 77), ("GRIR", "R", "reload", 79),
    ("GRIR", "S", "reload", 81), ("GRIR", "T", "reload", 83), ("GRIR", "U", "reload", 84),
    ("GRIR", "V", "reload", 85), ("GRIR", "W", "reload", 86), ("GRIR", "X", "reload", 87),
    ("GRIR", "Y", "reload", 88),
]
# Not mapped, so they fall back to the flat sprite: GRIZ B-E and GRIM A-G (the bash), KNIF A-G
# (the knife), and the pickup/spawn frames. Those are separate animations we have not modelled.

# ---------------------------------------------------------------------------
# VR only: ask the engine to aim a long gun down the line between the two hands.
# ⚠️ Needs OUR GZDoomVR build. `TwoHandedAim` does not exist in the stock engine, and a
# ZScript file that names a missing field stops the game from starting at all — so this goes
# in the VR pk3 only, which is already our-engine-only because of the off-hand fields.
# The engine refuses by itself whenever the off hand is not really on the fore-end, so leaving
# this on costs nothing: the worst case is the aiming we already had.
# ---------------------------------------------------------------------------
if VARIANT == "vr":
    EXTRA_LUMPS = {
        "zscript.txt": '''version "4.10"
class TefaTwoHandedHandler : EventHandler
{
	override void WorldTick()
	{
		let pl = players[consoleplayer];
		if (!pl || !pl.mo) return;
		bool longgun = false;
		if (pl.ReadyWeapon)
		{
			Name n = pl.ReadyWeapon.GetClassName();
			// Only the pump shotgun to begin with, so the first headset test is unambiguous.
			// The other Ashes long guns, once each has been tried: FAL, Musket, Ingram,
			// NapalmGun, SawedOff. pumpaction2 is the Classic shotgun (no model of ours yet).
			longgun = (n == 'pumpaction' || n == 'pumpaction2');
		}
		pl.mo.TwoHandedAim = longgun && pl.mo.OffhandValid;
	}
}
''',
        "mapinfo.shotgun": 'GameInfo { AddEventHandlers = "TefaTwoHandedHandler" }\n',
    }
