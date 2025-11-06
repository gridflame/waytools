# GitHub Setup for way.tools Installer Distribution

## Quick Setup Guide

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `waytools` (or your choice)
3. Description: `way.tools YouTube Downloader - Windows installer`
4. Make it **Public** (so releases are accessible)
5. Click **"Create repository"**

### Step 2: Push Your Code to GitHub

```powershell
# Navigate to your project
cd C:\Users\roman\OneDrive\Desktop\rjzeo\my-app

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - way.tools YouTube Downloader"

# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/waytools.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Create First Release (Manual Method)

1. **Build the installer locally first:**
   ```powershell
   cd youtube_downloader
   .\build.bat
   .\create_installer.bat
   ```

2. **Go to GitHub:**
   - Navigate to: `https://github.com/YOUR_USERNAME/waytools`
   - Click **"Releases"** → **"Create a new release"**

3. **Fill in release details:**
   - **Tag version**: `v1.0.0` (create new tag)
   - **Release title**: `way.tools YouTube Downloader v1.0.0`
   - **Description**:
     ```
     Windows installer for way.tools YouTube Downloader
     
     ## Features
     - Download YouTube videos in multiple formats (MP4, WebM, MP3, M4A, WAV, FLAC)
     - Choose quality (1080p, 720p, 480p, etc.)
     - Clean installer with no bloatware
     - Includes yt-dlp bundled - no separate installation needed
     - No popup windows during downloads
     ```

4. **Attach installer:**
   - Drag and drop: `youtube_downloader\installer\YouTubeDownloaderSetup.exe`
   - Or click "Attach binaries" and select the file

5. **Publish:**
   - Click **"Publish release"**

### Step 4: Configure Environment Variables

Update your environment variables (for Vercel or local):

1. **Create `.env.local` file:**
   ```bash
   GITHUB_OWNER=YOUR_USERNAME
   GITHUB_REPO=waytools
   GITHUB_RELEASE_TAG=latest
   ```

2. **For Vercel:**
   - Go to your project settings
   - Click **"Environment Variables"**
   - Add:
     - `GITHUB_OWNER` = `YOUR_USERNAME`
     - `GITHUB_REPO` = `waytools`
     - `GITHUB_RELEASE_TAG` = `latest`

### Step 5: Test the Download

1. Visit your website
2. Click the download button
3. The installer should download from GitHub Releases!

## How It Works

The download API (`app/api/download/route.ts`) now:
1. **First** tries to serve from local files (for development)
2. **Falls back** to GitHub Releases if local file not found
3. Automatically fetches the latest release or specific tag

## Updating Releases

### Method 1: Manual (Recommended for now)

1. Build new installer:
   ```powershell
   cd youtube_downloader
   .\build.bat
   .\create_installer.bat
   ```

2. Create new release on GitHub:
   - Tag: `v1.0.1`, `v1.0.2`, etc.
   - Upload new installer file

### Method 2: Automated (Future)

The `.github/workflows/release.yml` file can automate this:
- When you push a tag like `v1.0.1`, it will:
  - Build the executable
  - Create the installer
  - Upload to GitHub Releases

## Download URLs

Your installer will be available at:
```
https://github.com/YOUR_USERNAME/waytools/releases/download/v1.0.0/YouTubeDownloaderSetup.exe
```

The API will automatically use this URL when local files aren't available.

## Troubleshooting

### "GitHub API error"
- Check that `GITHUB_OWNER` and `GITHUB_REPO` are correct
- Ensure the repository is public
- Verify a release exists

### "Installer not found in release assets"
- Make sure the installer file is named `YouTubeDownloaderSetup.exe`
- Check that it's attached to the release

### Download doesn't work
- Check browser console for errors
- Verify environment variables are set correctly
- Test the GitHub release URL directly in browser

## Next Steps

1. ✅ Create GitHub repository
2. ✅ Push code
3. ✅ Create first release with installer
4. ✅ Set environment variables
5. ✅ Test download
6. ✅ Deploy to Vercel

Your installer is now distributed via GitHub Releases! 🎉
