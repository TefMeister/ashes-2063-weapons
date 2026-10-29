#!/usr/bin/env python3
"""build_body_test.py -- a rough first body for Ashes 2063 VR, as plain boxes, on the engine's body rig (2026-10-29).

Tefa, 2026-10-29: "build a rough first version of the body, then we'll fix it at some point. main thing is to
get the mechanics and the plumbing and wiring right". So this makes NO attempt at the jacket's creases or the
backpack's buckles: ten boxes (torso, hips, two upper arms, two forearms, two thighs, two shins with boots) in
the jacket / jeans / boot colours of the reference picture, each a separate actor the engine places from the
body rig (engine/body_rig.h, `BodyPart` on an actor) on every rendered frame. The looks come later, in Blender,
with Tefa (PREFERENCES.md: Blender work is done together).

Needs no Blender: the boxes are written straight to MD3 with kit/gz_md3.py.

    python body/build_body_test.py                 # writes body/gzdoom/Ashes2063_body_test.pk3
    python body/build_body_test.py --deploy        # also copies the pk3, the quest-compat engine build and
                                                   # its DLLs to E:/Ashes2063VR-dev/body-test/ (dev PC)

THE MODEL CONVENTION the engine expects for a body part (models.cpp, RenderModel, `bodyPosed`):
    md3 +X = along the part (for a limb: from its upper joint towards the next one; for the torso and hips: the
             body's forward), md3 +Y = the part's left, md3 +Z = the part's up (a limb's up is the side its
             up-hint points to: the front of a leg, the back of the hand for a forearm). Origin = the upper
             joint (neck base for the torso, hip centre for the hips). Units here: CENTIMETRES, MODELDEF Scale 0.01.
"""
import os, sys, struct, zlib, zipfile, shutil, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "kit"))
from gz_md3 import write_md3  # noqa: E402

OUT_DIR = os.path.join(HERE, "gzdoom")
PK3_NAME = "Ashes2063_body_test.pk3"
MODEL_PATH = "models/ashes2063/body"
SKIN = "body_skin.png"
SPRITE = "TBDY"                                  # placeholder sprite name; MODELDEF needs it to exist
MODEL_SCALE = 0.01                               # centimetres -> metres (the rig works in metres)

# Dev PC deploy targets (the game itself stays untouched; the engine runs from its own folder).
DEV_ROOT = "E:/Ashes2063VR-dev"
DEPLOY_DIR = os.path.join(DEV_ROOT, "body-test")
ENGINE_BUILD = os.path.join(DEV_ROOT, "src/gzdoomvr/build-ovr1168/RelWithDebInfo")
STOCK_ENGINE = "D:/ashes2063vr/Ashes 2063 VR/gzdoomvr"       # the DLLs the build folder does not have
GAME_DIR = "D:/ashes2063vr/Ashes 2063 VR"

# Body measurements in centimetres, for a 1.75 m player (the rig scales its JOINTS with vr_body_height; these
# boxes do not scale with it yet -- a taller player gets gaps at the joints, a shorter one overlaps. Later.)
TORSO_LEN = 55; TORSO_HALF_W = 17; TORSO_BACK = 10; TORSO_CHEST = 12
HIP_HALF_W = 15
UPPER_ARM = 32; FOREARM = 27; ARM_R = 5.5; CUFF = 7
THIGH = 45; SHIN = 45; THIGH_R = 8; SHIN_R = 6.5
ANKLE_ABOVE_FLOOR = 8                            # the rig's ankle is this high; the boot fills the gap to the floor
BOOT_HEEL = 6; BOOT_TOE = 18; BOOT_HALF_W = 7

# Colours (R, G, B), from the reference picture, flat: no shading, no wear -- the looks pass comes later.
COLOURS = {
    "jacket": (72, 46, 28),      # worn brown leather
    "knit":   (44, 30, 20),      # ribbed cuffs and waistband
    "jeans":  (30, 34, 52),
    "boot":   (26, 22, 20),
    "strap":  (86, 88, 62),      # olive backpack straps
    "buckle": (120, 118, 108),
    "belt":   (40, 32, 26),
    "mark":   (200, 60, 40),     # a red patch on the LEFT upper arm only: tells left from right in the headset
}
CELL = 8                                          # skin texture: one 8x8 cell per colour, sampled at its centre
MODELDEF_FLAGS = ["DONTCULLBACKFACES", "NOINTERPOLATION"]


# ---------------------------------------------------------------- geometry
def box(x0, x1, y0, y1, z0, z1, colour):
    """One axis-aligned box as 24 vertices (4 per face, outward normal) and 12 triangles, all UVs at the colour cell."""
    verts, tris = [], []
    faces = [  # (normal, four corners counter-clockwise seen from outside)
        ((1, 0, 0),  [(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)]),
        ((-1, 0, 0), [(x0, y1, z0), (x0, y0, z0), (x0, y0, z1), (x0, y1, z1)]),
        ((0, 1, 0),  [(x1, y1, z0), (x0, y1, z0), (x0, y1, z1), (x1, y1, z1)]),
        ((0, -1, 0), [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)]),
        ((0, 0, 1),  [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]),
        ((0, 0, -1), [(x0, y1, z0), (x1, y1, z0), (x1, y0, z0), (x0, y0, z0)]),
    ]
    for n, corners in faces:
        base = len(verts)
        for c in corners:
            verts.append((c, n, colour))
        tris += [(base, base + 1, base + 2), (base, base + 2, base + 3)]
    return verts, tris


def part_torso():
    v, t = [], []
    for b in [
        box(-TORSO_BACK, TORSO_CHEST, -TORSO_HALF_W, TORSO_HALF_W, -TORSO_LEN + 5, 1, "jacket"),
        box(-TORSO_BACK - 0.5, TORSO_CHEST + 0.5, -TORSO_HALF_W - 0.5, TORSO_HALF_W + 0.5, -TORSO_LEN, -TORSO_LEN + 5, "knit"),
        box(TORSO_CHEST, TORSO_CHEST + 1.5, 5, 9, -40, 0, "strap"),          # left strap (md3 +Y is left)
        box(TORSO_CHEST, TORSO_CHEST + 1.5, -9, -5, -40, 0, "strap"),        # right strap
        box(TORSO_CHEST + 1.5, TORSO_CHEST + 2.5, 5, 9, -22, -19, "buckle"),
        box(TORSO_CHEST + 1.5, TORSO_CHEST + 2.5, -9, -5, -22, -19, "buckle"),
    ]:
        v, t = _merge(v, t, b)
    return v, t


def part_hips():
    v, t = [], []
    for b in [
        box(-11, 11, -HIP_HALF_W, HIP_HALF_W, -12, 2, "jeans"),
        box(-11.5, 11.5, -HIP_HALF_W - 0.5, HIP_HALF_W + 0.5, 2, 6, "belt"),
    ]:
        v, t = _merge(v, t, b)
    return v, t


def part_upper_arm(left):
    v, t = [], []
    v, t = _merge(v, t, box(0, UPPER_ARM, -ARM_R, ARM_R, -ARM_R, ARM_R, "jacket"))
    if left:   # the tell-tale: a red patch on the OUTSIDE of the left upper arm. Left arm's outside = its left = md3 +Y... but
        # the rig's up-hint for an upper arm is world up, so md3 +Z is up and +Y is the arm's left; for the LEFT arm,
        # "left" is the outside. If the patch shows up on the RIGHT arm in the headset, flip vr_body_mirror.
        v, t = _merge(v, t, box(10, 20, ARM_R, ARM_R + 0.6, -3, 3, "mark"))
    return v, t


def part_forearm():
    v, t = [], []
    for b in [
        box(0, FOREARM - CUFF, -ARM_R + 0.5, ARM_R - 0.5, -ARM_R + 0.5, ARM_R - 0.5, "jacket"),
        box(FOREARM - CUFF, FOREARM, -ARM_R, ARM_R, -ARM_R, ARM_R, "knit"),
    ]:
        v, t = _merge(v, t, b)
    return v, t


def part_thigh():
    return box(0, THIGH, -THIGH_R, THIGH_R, -THIGH_R, THIGH_R, "jeans")


def part_shin():
    v, t = [], []
    for b in [
        box(0, SHIN, -SHIN_R, SHIN_R, -SHIN_R, SHIN_R, "jeans"),
        # the boot: from a little above the ankle down to the floor (ankle is ANKLE_ABOVE_FLOOR up), heel back, toe forward
        box(SHIN - 7, SHIN + ANKLE_ABOVE_FLOOR, -BOOT_HALF_W, BOOT_HALF_W, -BOOT_HEEL, BOOT_TOE, "boot"),
    ]:
        v, t = _merge(v, t, b)
    return v, t


def _merge(v, t, b):
    bv, bt = b
    base = len(v)
    return v + bv, t + [(a + base, bb + base, c + base) for a, bb, c in bt]


# ---------------------------------------------------------------- skin
def _chunk(tag, data):
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)


def png_rgba(width, height, rows):
    raw = b"".join(b"\x00" + bytes(r) for r in rows)
    return (bytes([0x89]) + b"PNG\r\n" + bytes([0x1A]) + b"\n"
            + _chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
            + _chunk(b"IDAT", zlib.compress(raw, 9)) + _chunk(b"IEND", b""))


def skin_png(names):
    w, h = CELL * len(names), CELL
    rows = []
    for _ in range(h):
        row = []
        for n in names:
            r, g, b = COLOURS[n]
            row += [r, g, b, 255] * CELL
        rows.append(row)
    return png_rgba(w, h, rows)


PIXEL = png_rgba(1, 1, [[0, 0, 0, 0]])           # 1x1 transparent sprite so the sprite name exists


# ---------------------------------------------------------------- pack
PARTS = [  # (BodyPart number, class, md3 name, builder)
    (1, "TefaBodyTorso", "torso", part_torso),
    (2, "TefaBodyHips", "hips", part_hips),
    (3, "TefaBodyUpperArmL", "upper_arm_l", lambda: part_upper_arm(True)),
    (4, "TefaBodyForearmL", "forearm", part_forearm),
    (5, "TefaBodyUpperArmR", "upper_arm_r", lambda: part_upper_arm(False)),
    (6, "TefaBodyForearmR", "forearm", part_forearm),
    (7, "TefaBodyThighL", "thigh", part_thigh),
    (8, "TefaBodyShinL", "shin", part_shin),
    (9, "TefaBodyThighR", "thigh", part_thigh),
    (10, "TefaBodyShinR", "shin", part_shin),
]

ZSCRIPT = '''version "4.10"
// Ashes 2063 VR: a rough first body (plain boxes) placed by the engine's body rig.
// Needs our GZDoomVR build with `BodyPart` on actors (engine/body_rig.h). On any other engine this does not compile.
class TefaBodyPart : Actor
{
	Default { +NOGRAVITY +NOBLOCKMAP +NOINTERACTION +DONTSPLASH +NOTONAUTOMAP }
	States { Spawn: TBDY A -1; Stop; }
}
CLASSES
class TefaBodyHandler : EventHandler
{
	Actor parts[11];
	override void WorldTick()
	{
		static const Class<Actor> kinds[] = { KINDS };
		let pmo = players[consoleplayer].mo;
		if (!pmo) return;
		// The rig only exists while the headset view is on; flat, the parts stay hidden (the pack still loads).
		bool vr = players[consoleplayer].PlayInVR;
		for (int i = 1; i <= 10; i++)
		{
			if (!parts[i])
			{
				parts[i] = Actor.Spawn(kinds[i], pmo.pos);
				parts[i].BodyPart = i;		// the engine draws it as this part of the body, every rendered frame
			}
			parts[i].bInvisible = !vr;
			// Game-side position (sector, light): near the player. The drawing ignores it.
			parts[i].SetOrigin(pmo.pos + (0, 0, pmo.height * 0.5), true);
			parts[i].angle = pmo.angle;
		}
	}
}
'''


def modeldef(cls, md3):
    lines = [f"Model {cls}", "{", f'   Path "{MODEL_PATH}"', f'   Model 0 "{md3}.md3"', f'   Skin 0 "{SKIN}"',
             f"   Scale {MODEL_SCALE} {MODEL_SCALE} {MODEL_SCALE}"] + [f"   {f}" for f in MODELDEF_FLAGS] + \
            [f"   FrameIndex {SPRITE} A 0 0", "}", ""]
    return "\n".join(lines)


def build():
    os.makedirs(OUT_DIR, exist_ok=True)
    names = list(COLOURS)
    pk3 = os.path.join(OUT_DIR, PK3_NAME)
    classes = "".join(f"class {cls} : TefaBodyPart {{}}\n" for _, cls, _, _ in PARTS)
    kinds = ", ".join(['"TefaBodyPart"'] + [f'"{cls}"' for _, cls, _, _ in PARTS])
    zs = ZSCRIPT.replace("CLASSES", classes).replace("KINDS", kinds)
    mdef = "".join(modeldef(cls, md3) for _, cls, md3, _ in PARTS)
    tmp = os.path.join(OUT_DIR, "_md3")
    os.makedirs(tmp, exist_ok=True)
    written = {}
    report = []
    for num, cls, md3, make in PARTS:
        if md3 in written:
            continue
        verts, tris = make()
        frame = [(p, n) for p, n, _ in verts]
        uvs = [((names.index(c) + 0.5) / len(names), 0.5) for _, _, c in verts]
        path = os.path.join(tmp, md3 + ".md3")
        surfaces, nv, nt = write_md3(path, md3, [frame], (tris, uvs), f"{MODEL_PATH}/{SKIN}")
        written[md3] = path
        xs = [p[0] for p, _, _ in verts]
        report.append(f"  {md3:12s} {nv:3d} verts {nt:3d} tris  x {min(xs):6.1f}..{max(xs):6.1f} cm")
    with zipfile.ZipFile(pk3, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("zscript.txt", zs)
        z.writestr("modeldef.body", mdef)
        z.writestr("mapinfo.body", 'GameInfo { AddEventHandlers = "TefaBodyHandler" }\n')
        z.writestr(f"sprites/{SPRITE}A0.png", PIXEL)
        z.writestr(f"{MODEL_PATH}/{SKIN}", skin_png(names))
        for md3, path in written.items():
            z.write(path, f"{MODEL_PATH}/{md3}.md3")
    shutil.rmtree(tmp)
    print(f"wrote {pk3} ({os.path.getsize(pk3)} bytes)")
    print("\n".join(report))
    return pk3


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


LAUNCHER = r'''@echo off
rem Ashes 2063 VR - BODY TEST (dev PC, 2026-10-29): the quest-compat engine build with the body rig, plus the
rem rough box body. Game files stay in the game folder; the engine runs from body-test\engine.
rem   flat check:  "Play Ashes 2063 VR - body test.bat" +vr_mode 0
rem Needs SteamVR running for the headset. vr_body_debug prints the rig's joints to the console, throttled.
setlocal
set "GAME=GAME_DIR"
set "E=%~dp0body-test\engine"
set "B=%~dp0body-test"
for %%F in ("%E%\gzdoom.exe" "%E%\gzdoom.pk3" "%E%\openvr_api.dll" "%B%\PK3_NAME" "%GAME%\Resources\Ashes2063Enriched2_23.pk3") do (
  if not exist %%F ( echo *** NOT FOUND: %%~F & pause & exit /b 1 )
)
"%E%\gzdoom.exe" -iwad "%GAME%\Resources\freedoom-0.12.1\freedoom2.wad" -file "%GAME%\Resources\AshesSAMenu.pk3" "%GAME%\Resources\lightmodepatch.pk3" "%GAME%\Resources\Ashes2063Enriched2_23.pk3" "%GAME%\Resources\Ashes2063EnrichedFDPatch.pk3" "%B%\PK3_NAME" -config "%~dp0ashes-dev-vr.ini" +set language "enu" +vr_mode 10 +set vr_body_debug 1 +logfile "%B%\body-test.log" %*
endlocal
'''


def deploy(pk3):
    eng = os.path.join(DEPLOY_DIR, "engine")
    os.makedirs(eng, exist_ok=True)
    copied = []
    for name in ("gzdoom.exe", "gzdoom.pk3", "gzdoom.pdb", "game_support.pk3", "lights.pk3", "brightmaps.pk3", "game_widescreen_gfx.pk3"):
        src = os.path.join(ENGINE_BUILD, name)
        if os.path.exists(src):
            shutil.copy2(src, eng); copied.append(name)
    for d in ("fm_banks", "soundfonts"):
        src = os.path.join(ENGINE_BUILD, d)
        if os.path.isdir(src) and not os.path.isdir(os.path.join(eng, d)):
            shutil.copytree(src, os.path.join(eng, d))
    for name in ("openvr_api.dll", "zmusic.dll", "openal32.dll", "sndfile.dll"):
        src = os.path.join(STOCK_ENGINE, name)
        if os.path.exists(src):
            shutil.copy2(src, eng); copied.append(name)
    shutil.copy2(pk3, os.path.join(DEPLOY_DIR, PK3_NAME))
    bat = os.path.join(DEV_ROOT, "Play Ashes 2063 VR - body test.bat")
    with open(bat, "w", newline="\r\n") as f:
        f.write(LAUNCHER.replace("GAME_DIR", GAME_DIR.replace("/", "\\")).replace("PK3_NAME", PK3_NAME))
    print(f"deployed to {DEPLOY_DIR}: {', '.join(copied)}, {PK3_NAME}")
    print(f"launcher: {bat}")
    for p in (os.path.join(eng, "gzdoom.exe"), os.path.join(eng, "gzdoom.pk3"), os.path.join(DEPLOY_DIR, PK3_NAME)):
        print(f"  {sha(p)}  {p}")


if __name__ == "__main__":
    out = build()
    if "--deploy" in sys.argv:
        deploy(out)
