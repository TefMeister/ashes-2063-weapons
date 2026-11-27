"""Writes the three test launchers for the 2026-11-27 Meshy set (one per episode) into the game folder, and their
shortcuts into the desktop "ashes tests" folder (Tefa: every new Ashes test launcher gets one there).
    python m2_launchers.py
Tefa: "remove all weapons from the game that we have used before, lantern as well": each launcher loads only the new
packs of its own episode (pk3/<episode>/), the new lantern, and the helpers that are not guns (fire lights, VR fixes,
two-handed aim), on our GZDoomVR build (the off-hand lantern needs it). Every first-version weapon of the episode is
given at the start (no upgrades), with plenty of ammunition."""
import glob
import os
import subprocess

OUT = os.path.join("D:" + os.sep, "Ashes 2063", "3D blender", "meshy set 2026-11-27")
GAME = os.path.join("C:" + os.sep, "NonSteam", "Ashes 2063 VR")
TESTS = os.path.join(os.path.expanduser("~"), "Desktop", "doom and ashes stuff", "ashes tests")
HELPERS = [os.path.join("D:" + os.sep, "Ashes 2063", "3D blender", p) for p in (
    r"fire lights\Ashes2063_fire_lights_test.pk3", r"vr fixes\Ashes2063_vr_fixes_test.pk3",
    r"two-handed\Ashes2063_two_handed_VR_test.pk3")]
LANTERN = os.path.join(OUT, "pk3", "lantern", "Ashes2063_m2_lantern_VR_test.pk3")
EPISODES = {
    "ep1": dict(title="Ashes 2063", files=[r".\Resources\Ashes2063Enriched2_23.pk3", r".\Resources\Ashes2063EnrichedFDPatch.pk3"],
                give="Crowbar Glock revolver pumpaction SawedOff Ingram JunkerMusket FAL JACKHAMMER NapalmGun pipebomb "
                     "Lantern LanternFound", start="revolver",
                ammo="NineMilAmmo Shotgunammo Slugammo Falammo NapalmAmmo PipeAmmo fortyfiveAmmo Hammergas Chips"),
    "afterglow": dict(title="Afterglow", files=[r".\Resources\AshesAfterglow1_16.pk3"],
                      give="Crowbar Glock revolver pumpaction SawedOff Ingram M16 JunkerMusket JACKHAMMER NapalmGun "
                           "pipebomb Lazergun KillerPig Lantern", start="M16",
                      ammo="NineMilAmmo Shotgunammo SlugAmmo rifleammo NapalmAmmo PipeAmmo fortyfiveammo Hammergas "
                           "LazerAmmo Chips"),
    "hardreset": dict(title="Hard Reset", files=[r".\Resources\AshesHardReset_105.pk3"],
                      give="Crowbar PolicePistol Leveraction HunterShotgun ModRifle1 NapalmGun pipebomb Xbow "
                           "Thumper BowlBallWeapon", start="PolicePistol",
                      ammo="NineMilammo Hollowpointammo Shotgunammo rifleammo XbowAmmo thumperammo thumperloaded "
                           "BowlingAmmo NapalmAmmo PipeAmmo"),
}


def bat(ep, e):
    packs = HELPERS + [LANTERN] + sorted(glob.glob(os.path.join(OUT, "pk3", ep, "*.pk3")))
    names = sorted(os.path.splitext(os.path.basename(p))[0][3:].replace("_", " ") for p in
                   glob.glob(os.path.join(OUT, "pk3", ep, "*.pk3")))
    lines = ["@echo off", 'cd /d "%~dp0"', "setlocal enabledelayedexpansion",
             "echo ============================================================",
             "echo  %s VR - MESHY SET TEST (2026-11-27)" % e["title"].upper(),
             "echo.",
             "echo  Only the new Meshy cube guns and the new lantern, no hands.",
             "echo  First versions only; the upgrades come later.",
             "echo  In here: " + ", ".join(names) + ".",
             "echo.", "echo  PUT THE HEADSET ON AND CONNECT IT FIRST.",
             "echo ============================================================", "echo.", 'set "MISSING="']
    for p in packs:
        lines += ['if not exist "%s" (set "MISSING=1" & echo  *** NOT FOUND: %s)' % (p, p)]
    lines += ["if defined MISSING (", "  echo.", "  echo  A mod file is missing. Nothing was launched.", "  pause",
              "  exit /b 1", ")"]
    gives = " ".join("+give %s" % w for w in e["give"].split()) + " " + \
        " ".join("+give %s 999" % a for a in e["ammo"].split())
    files = " ".join('"%s"' % f for f in [r".\Resources\AshesSAMenu.pk3", r".\Resources\lightmodepatch.pk3"]
                     + e["files"] + packs)
    lines.append(r'".\gzdoomvr-tefa\gzdoomvr.exe" -iwad ".\Resources\freedoom-0.12.1\freedoom2.wad" -file %s '
                 r'-config ".\gzdoomvr-tefa\ashes-vr-3dtest.ini" +set language "enu" +vr_mode 10 -skill 3 +map MAP01 '
                 r'%s +use %s +set vr_two_handed_min_sep 0 +set vr_two_handed_max_disagree 180 +set vr_weapon_glide 0 '
                 r'%%*' % (files, gives, e["start"]))
    lines.append("endlocal")
    return "\r\n".join(lines) + "\r\n"


def shortcut(target, name):
    lnk = os.path.join(TESTS, name + ".lnk")
    ps = ("$s=(New-Object -ComObject WScript.Shell).CreateShortcut('%s'); $s.TargetPath='%s'; "
          "$s.WorkingDirectory='%s'; $s.Save()" % (lnk, target, GAME))
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)
    return lnk


if __name__ == "__main__":
    for ep, e in EPISODES.items():
        if not glob.glob(os.path.join(OUT, "pk3", ep, "*.pk3")):
            continue
        name = "Play %s VR (meshy set 27-11)" % e["title"]
        path = os.path.join(GAME, name + ".bat")
        with open(path, "w", newline="") as f:
            f.write(bat(ep, e))
        print(path, "->", shortcut(path, "meshy set - " + e["title"]))
