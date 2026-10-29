@echo off
rem run_body_rig_test.bat -- compile and run engine\body_rig_test.cpp against the shipped body_rig.h.
rem The build tools live at C:\Program Files (x86)\... on the home PC and D:\VSBuildTools on the dev PC.
rem Add --dump to also print every part's pose for the standing case.
if exist "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" >nul 2>&1
if exist "D:\VSBuildTools\VC\Auxiliary\Build\vcvars64.bat" call "D:\VSBuildTools\VC\Auxiliary\Build\vcvars64.bat" >nul 2>&1
if not exist "%TEMP%\ashes_body_test" mkdir "%TEMP%\ashes_body_test"
cl /nologo /EHsc /W3 /std:c++17 /Fo"%TEMP%\ashes_body_test\\" /Fe"%TEMP%\ashes_body_test\body_rig_test.exe" "%~dp0body_rig_test.cpp"
if errorlevel 1 exit /b 1
"%TEMP%\ashes_body_test\body_rig_test.exe" %*
