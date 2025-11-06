# YouTube Downloader

A simple, user-friendly YouTube downloader application that can be packaged as a standalone executable (.exe) file.

## Features

- Download YouTube videos in various formats (MP4, WebM, MP3, M4A, WAV, FLAC)
- Choose video quality (1080p, 720p, 480p, etc.)
- Simple GUI interface built with tkinter
- Can be packaged as a single .exe file for easy distribution
- Automatic installation of yt-dlp if not present

## Installation

### Option 1: Use Pre-built Executable

1. Download `YouTubeDownloader.exe` from the `dist` folder
2. Run the executable - no installation required!

### Option 2: Build from Source

#### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

#### Steps

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Build the executable:**
   
   **Windows:**
   ```bash
   build.bat
   ```
   
   **Or manually:**
   ```bash
   python build.py
   ```
   
   **Or using PyInstaller directly:**
   ```bash
   pyinstaller --onefile --windowed --name YouTubeDownloader main.py
   ```

3. The executable will be created in the `dist` folder as `YouTubeDownloader.exe`

## Usage

1. **Run the application:**
   - Double-click `YouTubeDownloader.exe` (if using pre-built)
   - Or run `python main.py` (if running from source)

2. **Enter YouTube URL:**
   - Copy and paste any YouTube video URL into the URL field

3. **Choose download options:**
   - **Format:** Select the desired format (best, mp4, webm, mp3, m4a, wav, flac)
   - **Quality:** Select video quality (best, 1080p, 720p, 480p, etc.)

4. **Select download location:**
   - Use the "Browse" button to choose where to save the file
   - Default is your Downloads folder

5. **Click Download:**
   - The download will start and progress will be shown in the log area
   - You'll be notified when the download completes

## Supported Formats

- **Video:** MP4, WebM, Best available format
- **Audio:** MP3, M4A, WAV, FLAC

## Requirements

- Windows 10 or higher (for .exe)
- Internet connection
- yt-dlp (automatically installed if missing)

## Troubleshooting

### "yt-dlp not found" error
- The application will try to automatically install yt-dlp
- If that fails, manually install it: `pip install yt-dlp`

### Download fails
- Check your internet connection
- Verify the YouTube URL is valid
- Check the log area for error messages
- Make sure you have write permissions to the download folder

### Build fails
- Make sure Python and pip are installed correctly
- Try installing PyInstaller manually: `pip install pyinstaller`
- Make sure you're running the build script from the correct directory

## Technical Details

- **GUI Framework:** tkinter (included with Python)
- **Download Engine:** yt-dlp
- **Packaging:** PyInstaller
- **Python Version:** 3.8+

## License

This project uses yt-dlp, which is licensed under the Unlicense.

## Disclaimer

This tool is for personal use only. Please respect YouTube's Terms of Service and copyright laws. Only download videos you have permission to download.

