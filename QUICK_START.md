# Quick Start Guide - way.tools

## 🚀 Get Started in 3 Steps

### Step 1: Build the Executable
```bash
cd youtube_downloader
python build.py
```
Or on Windows:
```bash
cd youtube_downloader
build.bat
```

### Step 2: Run the Site Locally
```bash
npm install
npm run dev
```

Visit: http://localhost:3000  
Password: `apple123`

### Step 3: Deploy to Vercel

1. Push to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/waytools.git
git push -u origin main
```

2. Connect to Vercel:
   - Go to vercel.com
   - Import your GitHub repo
   - Click Deploy

Done! 🎉

## 📝 What's Included

✅ Password-protected landing page  
✅ Clean, aesthetic design  
✅ YouTube Downloader tool  
✅ Download button for installer  
✅ Logo integration  
✅ Ready for Vercel deployment  

## 🎨 Features

- **Site Password**: `way`
- **Tool**: YouTube Downloader 🎥
- **Formats**: MP4, WebM, MP3, M4A, WAV, FLAC
- **Quality**: 1080p, 720p, 480p, 360p, 240p
- **Installer**: Clean .exe with logo

## 🔧 Troubleshooting

**Executable not found?**
- Make sure you ran the build script
- Check `public/YouTubeDownloader.exe` exists

**Build fails?**
- Install Python 3.8+
- Run: `pip install -r youtube_downloader/requirements.txt`

**Download doesn't work?**
- Check that `public/YouTubeDownloader.exe` exists
- File should be > 10MB if built correctly

## 📦 File Locations

- Site code: `app/`
- Executable build: `youtube_downloader/`
- Built .exe: `public/YouTubeDownloader.exe`
- Logo: `public/logo.png`

---

For detailed docs, see [README.md](./README.md) and [DEPLOYMENT.md](./DEPLOYMENT.md)

