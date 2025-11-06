@echo off
echo Building way.tools YouTube Downloader Executable...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

REM Copy logo.png from parent directory if it exists
if exist ..\public\logo.png (
    copy ..\public\logo.png logo.png >nul
    echo Copied logo.png
)

REM Convert PNG to ICO if Pillow is available (for Windows icon)
python -c "from PIL import Image; img = Image.open('logo.png'); img.save('logo.ico', format='ICO', sizes=[(256,256), (128,128), (64,64), (48,48), (32,32), (16,16)])" 2>nul
if errorlevel 1 (
    echo Note: Could not create .ico file, using PNG
)

REM Ensure yt-dlp is installed
echo Checking yt-dlp...
python -c "import yt_dlp" 2>nul
if errorlevel 1 (
    echo Installing yt-dlp...
    python -m pip install yt-dlp
)

REM Build executable
echo.
echo Building executable...
echo This will bundle yt-dlp with the application...
if exist logo.ico (
    python -m PyInstaller --onefile --windowed --name "YouTubeDownloader" --icon=logo.ico --add-data "logo.png;." --hidden-import yt_dlp --hidden-import yt_dlp.extractor --hidden-import yt_dlp.downloader --hidden-import yt_dlp.postprocessor --collect-all yt_dlp main.py
) else if exist logo.png (
    python -m PyInstaller --onefile --windowed --name "YouTubeDownloader" --add-data "logo.png;." --hidden-import yt_dlp --hidden-import yt_dlp.extractor --hidden-import yt_dlp.downloader --hidden-import yt_dlp.postprocessor --collect-all yt_dlp main.py
) else (
    python -m PyInstaller --onefile --windowed --name "YouTubeDownloader" --hidden-import yt_dlp --hidden-import yt_dlp.extractor --hidden-import yt_dlp.downloader --hidden-import yt_dlp.postprocessor --collect-all yt_dlp main.py
)

if errorlevel 1 (
    echo Error: Build failed
    pause
    exit /b 1
)

echo.
echo Build complete! Executable is in the 'dist' folder.
echo.
pause

