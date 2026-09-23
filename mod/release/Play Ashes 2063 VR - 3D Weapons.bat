@echo off
rem Ashes 2063 - 3D Weapons for VR, v{VERSION}. Unofficial fan mod; see 3DWeapons\README.txt.
cd /d "%~dp0"
setlocal
set "W=3DWeapons"
set "CFG=%W%\settings.ini"
echo ============================================================
echo  Ashes 2063 VR - 3D WEAPONS  v{VERSION}
echo.
echo  Revolver, pistol, shotgun (two-handed) and lantern as 3D
echo  models in your hands.
echo.
echo  Put the headset on and start SteamVR FIRST. If SteamVR
echo  cannot see the headset, the game starts on the monitor.
echo.
echo  UNFINISHED WORK: it may cause motion sickness. Take breaks.
echo ============================================================
echo.

set "MISSING="
for %%F in (
  "%W%\engine\gzdoomvr.exe"
  "Resources\freedoom-0.12.1\freedoom2.wad"
  "Resources\AshesSAMenu.pk3"
  "Resources\lightmodepatch.pk3"
  "Resources\Ashes2063Enriched2_23.pk3"
  "Resources\Ashes2063EnrichedFDPatch.pk3"
  "%W%\pk3\1_revolver.pk3"
  "%W%\pk3\2_pistol.pk3"
  "%W%\pk3\3_shotgun.pk3"
  "%W%\pk3\4_lantern.pk3"
) do (
  if not exist %%F (
    set "MISSING=1"
    echo  *** NOT FOUND: %%~F
  )
)
if defined MISSING (
  echo.
  echo  Something is missing, so nothing was started.
  echo  This file has to sit in your Ashes 2063 folder - the one that
  echo  holds the "Resources" folder - next to the "3DWeapons" folder.
  echo  See 3DWeapons\README.txt.
  echo.
  pause
  exit /b 1
)

rem First run: start from your own VR settings, so your buttons and comfort options carry over.
if not exist "%CFG%" if exist "gzdoomvr\ashes-vr.ini" (
  copy /y "gzdoomvr\ashes-vr.ini" "%CFG%" >nul
  echo  First run: copied your VR settings from gzdoomvr\ashes-vr.ini
)
rem The gun angle the models were tuned with, and the two-handed grip settings, every launch.
powershell -NoProfile -ExecutionPolicy Bypass -File "%W%\set-settings.ps1" "%CFG%"

".\%W%\engine\gzdoomvr.exe" -iwad ".\Resources\freedoom-0.12.1\freedoom2.wad" -file ".\Resources\AshesSAMenu.pk3" ".\Resources\lightmodepatch.pk3" ".\Resources\Ashes2063Enriched2_23.pk3" ".\Resources\Ashes2063EnrichedFDPatch.pk3" ".\%W%\pk3\1_revolver.pk3" ".\%W%\pk3\2_pistol.pk3" ".\%W%\pk3\3_shotgun.pk3" ".\%W%\pk3\4_lantern.pk3" -config ".\%CFG%" +set language "enu" +vr_mode 10 +set vr_two_handed_min_sep 0 +set vr_two_handed_max_disagree 180
endlocal
