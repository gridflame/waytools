@echo off
REM Code signing script for way.tools installer
REM Requires: Code signing certificate (.pfx file)
REM 
REM Before using:
REM 1. Get a code signing certificate (see CODE_SIGNING_GUIDE.md)
REM 2. Set the certificate path and password below
REM 3. Install Windows SDK (includes signtool.exe)

echo ========================================
echo Code Signing for way.tools Installer
echo ========================================
echo.

REM Configure these variables with your certificate
set CERTIFICATE_FILE=path\to\your\certificate.pfx
set CERTIFICATE_PASSWORD=your-password-here
set TIMESTAMP_SERVER=http://timestamp.digicert.com

REM Check if certificate file exists
if not exist "%CERTIFICATE_FILE%" (
    echo ERROR: Certificate file not found at: %CERTIFICATE_FILE%
    echo.
    echo Please:
    echo 1. Get a code signing certificate (see CODE_SIGNING_GUIDE.md)
    echo 2. Update CERTIFICATE_FILE in this script
    echo 3. Update CERTIFICATE_PASSWORD in this script
    echo.
    pause
    exit /b 1
)

REM Find signtool.exe
set SIGNTOOL=""
if exist "C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe" (
    set SIGNTOOL="C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe"
) else if exist "C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe" (
    set SIGNTOOL="C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe"
) else (
    echo ERROR: signtool.exe not found!
    echo.
    echo Please install Windows SDK from:
    echo https://developer.microsoft.com/windows/downloads/windows-sdk/
    echo.
    pause
    exit /b 1
)

echo Found signtool: %SIGNTOOL%
echo.

REM Sign the executable first
if exist "dist\YouTubeDownloader.exe" (
    echo Signing YouTubeDownloader.exe...
    %SIGNTOOL% sign /f "%CERTIFICATE_FILE%" /p "%CERTIFICATE_PASSWORD%" /t %TIMESTAMP_SERVER% /d "way.tools YouTube Downloader" /du "https://way.tools" "dist\YouTubeDownloader.exe"
    if errorlevel 1 (
        echo ERROR: Failed to sign executable
        pause
        exit /b 1
    )
    echo ✓ Executable signed successfully
    echo.
) else (
    echo WARNING: dist\YouTubeDownloader.exe not found
    echo Please run build.bat first
    echo.
)

REM Sign the installer
if exist "installer\YouTubeDownloaderSetup.exe" (
    echo Signing YouTubeDownloaderSetup.exe...
    %SIGNTOOL% sign /f "%CERTIFICATE_FILE%" /p "%CERTIFICATE_PASSWORD%" /t %TIMESTAMP_SERVER% /d "way.tools YouTube Downloader" /du "https://way.tools" "installer\YouTubeDownloaderSetup.exe"
    if errorlevel 1 (
        echo ERROR: Failed to sign installer
        pause
        exit /b 1
    )
    echo ✓ Installer signed successfully
    echo.
    
    REM Verify signature
    echo Verifying signature...
    %SIGNTOOL% verify /pa "installer\YouTubeDownloaderSetup.exe"
    if errorlevel 1 (
        echo WARNING: Signature verification failed
    ) else (
        echo ✓ Signature verified successfully
    )
    echo.
) else (
    echo ERROR: installer\YouTubeDownloaderSetup.exe not found
    echo Please run create_installer.bat first
    pause
    exit /b 1
)

echo ========================================
echo Code signing complete!
echo ========================================
echo.
echo The installer is now signed and should not trigger browser warnings.
echo.
pause

