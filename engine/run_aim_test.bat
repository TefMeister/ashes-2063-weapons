@echo off
rem run_aim_test.bat -- compile and run engine\two_handed_aim_test.cpp against the shipped header.
rem The build tools live at C:\Program Files (x86)\... on the home PC and D:\VSBuildTools on the dev PC.
if exist "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" >nul 2>&1
if exist "D:\VSBuildTools\VC\Auxiliary\Build\vcvars64.bat" call "D:\VSBuildTools\VC\Auxiliary\Build\vcvars64.bat" >nul 2>&1
if not exist "%TEMP%\ashes_aim_test" mkdir "%TEMP%\ashes_aim_test"
cl /nologo /EHsc /W3 /std:c++17 /Fo"%TEMP%\ashes_aim_test\\" /Fe"%TEMP%\ashes_aim_test\two_handed_aim_test.exe" two_handed_aim_test.cpp
if errorlevel 1 exit /b 1
"%TEMP%\ashes_aim_test\two_handed_aim_test.exe"
