@echo off
REM Create Windows installer using Inno Setup
REM Make sure Inno Setup is installed: https://jrsoftware.org/isinfo.php

echo Creating way.tools YouTube Downloader Installer...
echo.

REM Check if Inno Setup is installed
set INNO_SETUP="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist %INNO_SETUP% (
    set INNO_SETUP="C:\Program Files\Inno Setup 6\ISCC.exe"
)

if not exist %INNO_SETUP% (
    echo Error: Inno Setup not found!
    echo Please install Inno Setup from https://jrsoftware.org/isinfo.php
    echo.
    echo Alternatively, you can use the standalone .exe file from the dist folder.
    pause
    exit /b 1
)

REM Make sure dist folder exists
if not exist "dist\YouTubeDownloader.exe" (
    echo Error: YouTubeDownloader.exe not found in dist folder!
    echo Please run build.bat or build.py first.
    pause
    exit /b 1
)

REM Create installer directory
if not exist "installer" mkdir installer

REM Compile installer
echo Compiling installer...
%INNO_SETUP% "create_installer.iss"

if errorlevel 1 (
    echo Error: Installer compilation failed
    pause
    exit /b 1
)

REM Copy installer to public folder for web download
if exist "installer\YouTubeDownloaderSetup.exe" (
    if exist "..\public" (
        copy "installer\YouTubeDownloaderSetup.exe" "..\public\YouTubeDownloaderSetup.exe" >nul
        echo Copied installer to public folder for web download
    )
)

echo.
echo Installer created successfully in the 'installer' folder!
echo File: installer\YouTubeDownloaderSetup.exe
echo.
pause

