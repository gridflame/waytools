@echo off
REM Setup script for GitHub Releases
echo ========================================
echo GitHub Release Setup for way.tools
echo ========================================
echo.

set /p GITHUB_USERNAME="Enter your GitHub username: "
set /p REPO_NAME="Enter repository name (default: waytools): "

if "%REPO_NAME%"=="" set REPO_NAME=waytools

echo.
echo Configuration:
echo   GitHub Username: %GITHUB_USERNAME%
echo   Repository: %REPO_NAME%
echo.

echo Creating .env.local file...
(
echo GITHUB_OWNER=%GITHUB_USERNAME%
echo GITHUB_REPO=%REPO_NAME%
echo GITHUB_RELEASE_TAG=latest
) > .env.local

echo.
echo .env.local created!
echo.
echo Next steps:
echo 1. Create GitHub repository: https://github.com/new
echo    - Name: %REPO_NAME%
echo    - Make it Public
echo.
echo 2. Push your code:
echo    git init
echo    git add .
echo    git commit -m "Initial commit"
echo    git remote add origin https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git
echo    git push -u origin main
echo.
echo 3. Build and create release:
echo    cd youtube_downloader
echo    build.bat
echo    create_installer.bat
echo.
echo 4. Create release on GitHub:
echo    - Go to: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%/releases
echo    - Click "Create a new release"
echo    - Tag: v1.0.0
echo    - Upload: youtube_downloader\installer\YouTubeDownloaderSetup.exe
echo.
echo 5. For Vercel deployment:
echo    - Add environment variables in Vercel dashboard:
echo      GITHUB_OWNER=%GITHUB_USERNAME%
echo      GITHUB_REPO=%REPO_NAME%
echo      GITHUB_RELEASE_TAG=latest
echo.
pause

