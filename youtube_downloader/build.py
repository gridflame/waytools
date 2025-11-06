"""
Build script for creating YouTube Downloader executable
Run this script to build the .exe file
"""
import subprocess
import sys
import os
import shutil

def main():
    print("Building way.tools YouTube Downloader Executable...")
    print()
    
    # Check if pyinstaller is installed
    try:
        import PyInstaller
        print("PyInstaller found")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("PyInstaller installed successfully")
    
    # Copy logo from parent directory
    logo_src = os.path.join("..", "public", "logo.png")
    if os.path.exists(logo_src) and not os.path.exists("logo.png"):
        shutil.copy(logo_src, "logo.png")
        print("Copied logo.png from parent directory")
    
    # Convert PNG to ICO if possible
    logo_ico = None
    if os.path.exists("logo.png"):
        try:
            from PIL import Image
            img = Image.open("logo.png")
            logo_ico = "logo.ico"
            img.save(logo_ico, format='ICO', sizes=[(256,256), (128,128), (64,64), (48,48), (32,32), (16,16)])
            print("Created logo.ico from logo.png")
        except ImportError:
            print("Pillow not available, skipping ICO conversion")
        except Exception as e:
            print(f"Could not create ICO: {e}")
    
    # Ensure yt-dlp is installed
    try:
        import yt_dlp
        print(f"yt-dlp found: {yt_dlp.version.__version__}")
    except ImportError:
        print("Installing yt-dlp...")
        subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], check=True)
        print("yt-dlp installed")
    
    # Build command - use python -m PyInstaller to ensure it's found
    build_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "YouTubeDownloader",
        "--hidden-import", "yt_dlp",
        "--hidden-import", "yt_dlp.extractor",
        "--hidden-import", "yt_dlp.downloader",
        "--hidden-import", "yt_dlp.postprocessor",
        "--collect-all", "yt_dlp",
    ]
    
    # Add icon if available
    if logo_ico and os.path.exists(logo_ico):
        build_cmd.extend(["--icon", logo_ico])
    
    # Add logo.png to bundle
    if os.path.exists("logo.png"):
        if sys.platform == "win32":
            build_cmd.extend(["--add-data", "logo.png;."])
        else:
            build_cmd.extend(["--add-data", "logo.png:."])
    
    build_cmd.append("main.py")
    
    print("Running PyInstaller...")
    print(f"Command: {' '.join(build_cmd)}")
    subprocess.run(build_cmd, check=True)
    
    # Copy to public folder for web download
    dist_exe = os.path.join("dist", "YouTubeDownloader.exe")
    public_dir = os.path.join("..", "public")
    if os.path.exists(dist_exe) and os.path.exists(public_dir):
        public_exe = os.path.join(public_dir, "YouTubeDownloader.exe")
        shutil.copy(dist_exe, public_exe)
        print(f"\nCopied executable to {public_exe} for web download")
    
    print()
    print("Build complete! Executable is in the 'dist' folder.")
    print("You can now distribute YouTubeDownloader.exe")
    print()
    print("To create an installer:")
    print("  1. Install Inno Setup from https://jrsoftware.org/isinfo.php")
    print("  2. Run: create_installer.bat")
    print("  Or manually compile create_installer.iss with Inno Setup")

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"Error: Build failed - {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nBuild cancelled by user")
        sys.exit(1)

