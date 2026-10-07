@echo off
cd /d "%~dp0"
setlocal enabledelayedexpansion
set "SHOTGUN=D:\Ashes 2063\3D blender\ashes shotgun\blender\gzdoom\Ashes2063_cube_shotgun_VR_test.pk3"
set "PROBE=D:\Ashes 2063\3D blender\ashes shotgun\blender\gzdoom\Ashes2063_lightprobe_colours.pk3"
echo ============================================================
echo  Ashes 2063 VR - LIGHT PROBE, COLOURS (2026-10-08)
echo.
echo  The cube shotgun is painted with what the engine's lighting
echo  receives, and an orange test light floats ahead of you.
echo.
echo    WHITE  = a light reaches that face       (all good)
echo    YELLOW = that face points away from it   (normal)
echo    RED    = no light list at all for the gun (a VR fault)
echo.
echo  Turn the gun in your hand: faces should flip white/yellow.
echo  Flat screen proof 2026-10-08: mostly white, some yellow.
echo.
echo  PUT THE HEADSET ON AND CONNECT IT FIRST.
echo ============================================================
echo.
set "MISSING="
for %%F in ("%SHOTGUN%" "%PROBE%") do (
  if not exist %%F (
    set "MISSING=1"
    echo  *** NOT FOUND: %%~F
  )
)
if defined MISSING (
  echo.
  echo  A mod file is missing. Nothing was launched.
  pause
  exit /b 1
)
".\gzdoomvr-tefa\gzdoomvr.exe" -iwad ".\Resources\freedoom-0.12.1\freedoom2.wad" -file ".\Resources\AshesSAMenu.pk3" ".\Resources\lightmodepatch.pk3" ".\Resources\Ashes2063Enriched2_23.pk3" ".\Resources\Ashes2063EnrichedFDPatch.pk3" "%SHOTGUN%" "%PROBE%" -config ".\gzdoomvr-tefa\ashes-vr-3dtest.ini" +set language "enu" +vr_mode 10 -skill 3 +map MAP01 +give pumpaction +give shotgunammo 40 +use pumpaction +set vr_two_handed_min_sep 0 +set vr_two_handed_max_disagree 180 +snd_musicvolume 0 %*
endlocal
