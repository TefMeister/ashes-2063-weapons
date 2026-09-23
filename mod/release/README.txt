ASHES 2063 - 3D WEAPONS FOR VR   (version {VERSION}, first release)
=====================================================================

WHAT THIS IS
  An unofficial, non-commercial fan mod that swaps four of Ashes 2063's flat weapon pictures
  for 3D models you hold in your hands in VR:

    - REVOLVER  - 3D model with its shot and reload animations (no hand on it yet).
    - PISTOL    - 3D model in a half-finger leather-gloved hand, with shot and reload animations.
    - SHOTGUN   - 3D model with gloved hands, shot and reload animations, and a real
                  TWO-HANDED grip: your right hand holds the back of the gun and your left
                  hand steers the barrel, and the shots go where the barrel points.
    - LANTERN   - 3D lantern in your LEFT hand, held by its handle, flickering, lighting the
                  room from where your hand is.

  Everything else in the game is unchanged and still uses the game's own pictures.

WHAT THIS IS NOT
  - Not made by, or connected with, the makers of Ashes 2063.
  - Not a finished mod. This is a first release; each weapon will now be improved one at a time.
  - Not a way to get the game. It contains no Ashes 2063 files at all - you need your own copy
    of the free Ashes 2063 standalone pack. All models here were made from scratch.

!! CAUTION !!
  This is unfinished work and it MAY CAUSE SEVERE MOTION SICKNESS AND DISCOMFORT.
  Take breaks, and stop at once if you feel unwell.

---------------------------------------------------------------------
WHAT YOU NEED FIRST
---------------------------------------------------------------------
  1. Ashes 2063, the free standalone pack (version 1.51), from its official ModDB page:
     https://www.moddb.com/mods/ashes-2063/downloads
     The plain, unmodded pack is all you need - no other VR setup.
  2. A PC VR headset through SteamVR (tested on a Quest 3 over Virtual Desktop) and 64-bit Windows.

  This mod brings its OWN VR engine, a changed copy of GZDoomVR (see "The engine" below). If you
  already play Ashes in VR some other way, that setup is left exactly as it is.

---------------------------------------------------------------------
INSTALL
---------------------------------------------------------------------
  1. Open your Ashes 2063 folder - the one that holds the "Resources" folder.
  2. Unzip this download straight into it. You should now see, next to "Resources":
         3DWeapons\                               (the mod)
         Play Ashes 2063 VR - 3D Weapons.bat      (starts it)
  3. That's it. Nothing of your existing game or VR setup is overwritten.

---------------------------------------------------------------------
PLAY
---------------------------------------------------------------------
  1. Put the headset on and start SteamVR FIRST. If SteamVR cannot see the headset, the game
     starts flat on your monitor instead.
  2. Double-click "Play Ashes 2063 VR - 3D Weapons.bat".

  The mod keeps its own settings in 3DWeapons\settings.ini, created on the first launch.
  If you already had Ashes in VR with a gzdoomvr\ashes-vr.ini, your buttons and options are
  copied from it the first time; otherwise the VR defaults are used, which work as they are.

  Every launch also sets the few values the models were tuned with:
    - the gun angle in your hand (openvr_weaponRotate -50; the engine default -40 points the
      guns up), and
    - the two-handed grip settings (works at any distance between your hands).

  The SHOTGUN is two-handed the moment you hold it: bring your left hand forward along the barrel
  and move it to steer. If you would rather two-hand only while holding a button, set
  tefa_grip_required to true in the console, and bind "Grip fore-end + run (VR grip)" in
  Options > Customize Controls > "Ashes 2063 VR (Tefa)" to your left controller's grip button.

---------------------------------------------------------------------
KNOWN ROUGH EDGES
---------------------------------------------------------------------
  - Your left hand is only drawn while it holds the lantern, while it is on the shotgun, and
    briefly during the pistol reload. A free-moving empty left hand is being made and is left
    out until it is right.
  - When you walk, the lantern may trail a little behind your hand.
  - The revolver has no hand on it yet.
  - The other weapons are still the game's flat pictures.

---------------------------------------------------------------------
UNINSTALL
---------------------------------------------------------------------
  Delete the "3DWeapons" folder and "Play Ashes 2063 VR - 3D Weapons.bat". Nothing else was changed.

---------------------------------------------------------------------
THE ENGINE (and its source code)
---------------------------------------------------------------------
  3DWeapons\engine is GZDoomVR by hh79 (https://github.com/hh79/gzdoomvr, tag gvr4.13.2.2),
  licensed GPL-3.0, with our changes added. They let a mod see where your left hand is, draw
  things locked to it (the lantern), and aim and draw a long gun along the line between your
  hands. Our changes, as patches you can apply to the upstream source, and how to build it:
  3DWeapons\source\gzdoomvr-changes\  - also online at
  https://github.com/TefMeister/ashes-2063-weapons/tree/main/engine
  3DWeapons\MANIFEST.txt lists every file in this download with its SHA-256 checksum.

---------------------------------------------------------------------
CREDITS
---------------------------------------------------------------------
  - Ashes 2063 by Vostyok and contributors - the game these weapons are built to match.
  - GZDoomVR by hh79, built on GZDoom by the ZDoom / GZDoom team (Graf Zahl and contributors).
  - Freedoom (the Freedoom project) - the base game data the Ashes pack runs on.
  - Blender (Blender Foundation) - all modelling and animation.
  - Design direction, reference photos, and every in-headset test: Tefa (TefMeister).
    Modelling, animation and engine changes: made with Claude (Anthropic).

  If you should be credited here and are not, or you are a rights holder who wants something
  corrected or removed, email td3kxlvr@proton.me and it will be fixed promptly.

  Project page: https://github.com/TefMeister/ashes-2063-weapons
