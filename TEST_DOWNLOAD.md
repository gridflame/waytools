# Testing the Download Feature

## Quick Setup

1. **Copy installer to public folder:**
   ```powershell
   .\copy-installer-to-public.bat
   ```
   
   Or manually:
   ```powershell
   Copy-Item "youtube_downloader\installer\YouTubeDownloaderSetup.exe" -Destination "public\YouTubeDownloaderSetup.exe"
   ```

2. **Start your dev server:**
   ```powershell
   npm run dev
   ```

3. **Test the download:**
   - Go to http://localhost:3000
   - Enter password: `way`
   - Click "Download Installer"
   - The installer should download from `public/YouTubeDownloaderSetup.exe`

## How It Works

The download API (`app/api/download/route.ts`) now:
- ✅ Only looks for `YouTubeDownloaderSetup.exe` (the Inno Setup installer)
- ✅ Checks `public/` folder first (for web serving)
- ✅ Falls back to `youtube_downloader/installer/` (for development)
- ✅ Removed all old methods (GitHub, standalone .exe, etc.)
- ✅ Clean and simple - just serves the installer

## File Locations

- **Installer source**: `youtube_downloader/installer/YouTubeDownloaderSetup.exe`
- **Web download**: `public/YouTubeDownloaderSetup.exe`
- **API serves from**: Either location (whichever exists)

## Testing Checklist

- [ ] Installer exists in `youtube_downloader/installer/`
- [ ] Installer copied to `public/` folder
- [ ] Dev server running
- [ ] Download button works
- [ ] Progress bar shows
- [ ] Installer downloads successfully
- [ ] Installer can be installed on Windows

## Troubleshooting

**"Installer not found" error:**
- Run: `.\copy-installer-to-public.bat`
- Or manually copy the installer to `public/` folder

**Download fails:**
- Check browser console for errors
- Verify file exists: `Test-Path public\YouTubeDownloaderSetup.exe`
- Check file size (should be > 10MB)

**Need to rebuild installer:**
```powershell
cd youtube_downloader
.\build.bat
.\create_installer.bat
cd ..
.\copy-installer-to-public.bat
```

