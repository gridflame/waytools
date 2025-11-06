@echo off
REM Copy installer to public folder for testing
echo Copying installer to public folder...

if exist "youtube_downloader\installer\YouTubeDownloaderSetup.exe" (
    copy "youtube_downloader\installer\YouTubeDownloaderSetup.exe" "public\YouTubeDownloaderSetup.exe" /Y
    echo Installer copied successfully!
    echo.
    echo The installer is now available at: public\YouTubeDownloaderSetup.exe
    echo You can now test the download on your website.
) else (
    echo Error: Installer not found!
    echo.
    echo Please create the installer first:
    echo   cd youtube_downloader
    echo   build.bat
    echo   create_installer.bat
    echo.
    pause
    exit /b 1
)

pause

