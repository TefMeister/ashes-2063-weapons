# How the shotgun goes into GZDoom: which animation files, size, pivot, and which game
# sprite frame shows which Blender frame. Used by gz_export.py. Same shape as gz_revolver.py.
NAME = "shotgun"                             # file names inside the pk3
ACTOR_CLASS = "pumpaction"                   # âš ï¸ the GAME's class for this gun, which MODELDEF
                                             # keys on. `pumpaction2` is the Classic shotgun,
                                             # a different weapon with different sprites.
ROOT = "SG_Root"
DIR = r"C:\Users\TD3KX\github-backups\ashes-2063-weapons\shotgun"
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

# âš ï¸ Frame 1 of shoot1 is the SHOT, not the gun at rest -- it is already kicked 8 degrees
# nose-up. The VR build measures everything from the rest pose, so without this line the
# gun sits 8 degrees nose-DOWN in the hand and shoots above where it points.
REST_FRAME = ("shoot1", 30)          # GRIZ A: ready

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
    # Starting point only â€” the revolver's took seven wears to settle. [hypothesis 2026-09-19]
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
# VR only: long guns are ALWAYS held with two hands.
#
# Tefa, 2026-09-20: *"i would actually like â€¦ for there to be no proximity at all, that when
# choosing a long weapon, it automatically switches to two handing. that in this game there is no
# way to fire a long rifle or shotgun with one hand"*. So nothing is conditional any more: pick up
# a long gun and the shot follows the line between your two hands, full stop. No button to press,
# no minimum hand separation, no check that the hands agree with the gun.
# âš ï¸ The price, and it is the deal that was asked for: if the off hand drops to your side, the
# shot follows THAT line. The gun cannot be fired one-handed.
# The grip button below still exists and can be switched back on (`tefa_grip_required 1`), because
# it cost nothing to keep; it is off, so it decides nothing.
#
# âš ï¸ Needs OUR GZDoomVR build. `TwoHandedAim` does not exist in the stock engine, and a
# ZScript file that names a missing field stops the game from starting at all â€” so this goes
# in the VR pk3 only, which is already our-engine-only because of the off-hand fields.
# The engine refuses by itself whenever the off hand is not really on the fore-end, so leaving
# this on costs nothing: the worst case is the aiming we already had.
# ---------------------------------------------------------------------------

# Every Ashes 2063 weapon that is held with two hands. Matched by class name, NOT by `is`, so a
# name that does not exist in the loaded game is simply never true instead of refusing to compile
# [inferred-static 2026-09-19, class names read from Actors/Weapons/*.txt of Ashes2063Enriched2_23].
# `pumpaction2` is the Classic shotgun; Ingram2/3 are the upgraded SMGs and inherit from Ingram,
# which name-matching does not follow, so they are listed.
LONG_GUNS = ["pumpaction", "pumpaction2", "SawedOff", "Ingram", "Ingram2", "Ingram3",
             "JunkerMusket", "FAL", "NapalmGun", "JACKHAMMER"]

# OFF by default: two-handed aiming is automatic for every long gun (Tefa, 2026-09-20). The
# button remains as a way to make it deliberate again, for anyone who wants that.
GRIP_REQUIRED_BY_DEFAULT = False

# The action the grip is bound to. `+user2` is a spare button GZDoom already offers in
# Customize Controls and nothing in Ashes uses [measured 2026-09-19, read from ashes-vr-3dtest.ini].
GRIP_ACTION = "+user2"
# The off-hand grip on a VR controller arrives as this key (gl_openvr.cpp: the secondary hand's
# k_EButton_Grip -> KEY_PAD_LSHOULDER) [inferred-static 2026-09-19].
GRIP_KEY = "LShoulder"
# âš ï¸ That key is already "run" in Ashes VR, so binding it straight to the grip would cost Tefa
# their sprint. The alias below does BOTH at once, and is what the key should be bound to.
GRIP_ALIAS = "+tefagrip"

if VARIANT == "vr":
    _names = " || ".join(f"n == '{c}'" for c in LONG_GUNS)
    EXTRA_LUMPS = {
        "zscript.txt": '''version "4.10"
// Two-handed long guns. Needs our GZDoomVR build (TwoHandedAim, OffhandValid).
class TefaTwoHandedHandler : EventHandler
{
	bool wasGrip, seenState;
	int lastWhy;

	override void WorldTick()
	{
		let pl = players[consoleplayer];
		if (!pl || !pl.mo) return;

		bool longgun = false;
		if (pl.ReadyWeapon)
		{
			Name n = pl.ReadyWeapon.GetClassName();
			longgun = (''' + _names + ''');
		}

		// The grip button, held. NOT the trigger any more -- a long gun is two-handed the moment
		// it is in your hands -- but kept, so it can be made deliberate again with one setting.
		bool grip = (pl.cmd.buttons & BT_USER2) != 0;

		bool needgrip = ''' + ("true" if GRIP_REQUIRED_BY_DEFAULT else "false") + ''';
		let cv = CVar.GetCVar('tefa_grip_required', pl);
		if (cv) needgrip = cv.GetBool();

		// 0 = the shot follows the line between the hands. Anything else says what is missing.
		int why = 0;
		if (!longgun) why = 1;
		else if (!pl.mo.OffhandValid) why = 2;
		else if (needgrip && !grip) why = 3;

		pl.mo.TwoHandedAim = (why == 0);

		let dbg = CVar.GetCVar('tefa_grip_debug', pl);
		if (dbg && dbg.GetBool())
		{
			// Says where things stand the moment it is switched on, then only when it changes.
			if (!seenState || why != lastWhy)
			{
				if (why == 0) Console.Printf("two-handed aim: ON");
				else if (why == 1) Console.Printf("two-handed aim: off (not a two-handed weapon)");
				else if (why == 2) Console.Printf("two-handed aim: off (off hand not tracked)");
				else Console.Printf("two-handed aim: off (grip not held)");
				lastWhy = why;
				seenState = true;
			}
			if (grip != wasGrip)
			{
				if (grip) Console.Printf("grip: HELD");
				else Console.Printf("grip: let go");
			}
		}
		else
		{
			seenState = false;
		}
		wasGrip = grip;
	}
}
''',
        "mapinfo.shotgun": 'GameInfo { AddEventHandlers = "TefaTwoHandedHandler" }\n',
        "cvarinfo.shotgun": (
            "// Two-handed long guns. Both are in Options -> Customize Controls / the console.\n"
            "user bool tefa_grip_required = " + ("true" if GRIP_REQUIRED_BY_DEFAULT else "false") + ";   // 1 = only two-hand while the grip button is held\n"
            "user bool tefa_grip_debug = false;     // say in the console when the grip is seen\n"
        ),
        "keyconf.shotgun": (
            "// The off-hand grip button on a VR controller comes through as \"%s\", which Ashes\n"
            "// already uses for running. This alias does BOTH, so gripping the fore-end costs\n"
            "// nothing: you still run, and the mod is told you are holding on.\n"
            "alias %s \"+speed; %s\"\n"
            "alias -%s \"-speed; -%s\"\n"
            "defaultbind %s %s\n"
            "addkeysection \"Ashes 2063 VR (Tefa)\" TefaAshesVR\n"
            "addmenukey \"Grip fore-end + run (VR grip)\" %s\n"
            "addmenukey \"Grip fore-end only\" %s\n"
        ) % (GRIP_KEY, GRIP_ALIAS, GRIP_ACTION, GRIP_ALIAS[1:], GRIP_ACTION[1:],
             GRIP_KEY, GRIP_ALIAS, GRIP_ALIAS, GRIP_ACTION),
    }
