@echo off
cd /d "%~dp0"
setlocal enabledelayedexpansion
set "SHOTGUN=D:\Ashes 2063\3D blender\ashes shotgun\blender\gzdoom\Ashes2063_cube_shotgun_VR_test.pk3"
set "PROBE=D:\Ashes 2063\3D blender\ashes shotgun\blender\gzdoom\Ashes2063_lightprobe_shine.pk3"
echo ============================================================
echo  Ashes 2063 VR - LIGHT PROBE, REAL SHINE (2026-10-08)
echo.
echo  The cube shotgun keeps its own paint, gets a metal shine map,
echo  and an orange test light floats ahead of and above you.
echo.
echo  What to look for: the gun is lit orange from above; the grey
echo  metal catches a soft sheen that MOVES as you turn the gun.
echo  Wood, leather and the gloves should not shine.
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
