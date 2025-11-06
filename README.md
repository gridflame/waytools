# way.tools - Premium Tools, Simplified

A clean, password-protected platform for downloading premium tools. Currently featuring a YouTube downloader with clean installer.

## 🚀 Features

- **Password Protection**: Site-wide password authentication (password: `apple123`)
- **Clean Design**: Minimal, aesthetic single-page interface
- **YouTube Downloader**: Full-featured YouTube video/audio downloader
- **Clean Installer**: No bloatware, just the tool you need
- **Multiple Formats**: MP4, WebM, MP3, M4A, WAV, FLAC
- **Quality Selection**: Choose from 1080p to 240p

## 📋 Prerequisites

- Node.js 18+ and npm
- Python 3.8+ (for building the executable)
- Git (for deployment)

## 🛠️ Local Development

### 1. Install Dependencies

```bash
npm install
```

### 2. Build the YouTube Downloader Executable

```bash
cd youtube_downloader
python build.py
# or on Windows:
build.bat
```

This creates `public/YouTubeDownloader.exe` which is used for downloads.

### 3. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

- Password: `apple123`

## 📦 Building the Executable

The YouTube downloader is built using PyInstaller:

```bash
cd youtube_downloader
python build.py
```

The build process:
1. Installs Python dependencies (yt-dlp, pyinstaller, pillow)
2. Copies logo.png from public folder
3. Converts logo to ICO format for Windows
4. Builds single-file executable
5. Copies to `public/YouTubeDownloader.exe` for web download

## 🚀 Deployment

### Deploy to Vercel

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/waytools.git
   git push -u origin main
   ```

2. **Connect to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Deploy automatically

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.

## 📁 Project Structure

```
.
├── app/
│   ├── api/download/          # Download API endpoint
│   ├── components/            # React components
│   │   └── PasswordProtection.tsx
│   ├── page.tsx               # Main landing page
│   └── layout.tsx             # Root layout
├── public/
│   ├── logo.png               # Site logo
│   └── YouTubeDownloader.exe  # Built executable
├── youtube_downloader/
│   ├── main.py                # YouTube downloader app
│   ├── build.py               # Build script
│   ├── build.bat              # Windows build script
│   └── requirements.txt       # Python dependencies
└── vercel.json                # Vercel configuration
```

## 🎨 Customization

### Change Password

Edit `app/components/PasswordProtection.tsx`:
```typescript
const PASSWORD = 'your-password-here';
```

### Update Logo

Replace `public/logo.png` with your logo (recommended: 512x512px PNG)

### Add More Tools

1. Add tool card in `app/page.tsx`
2. Add download endpoint in `app/api/download/`
3. Build new executable in `youtube_downloader/` or create new folder

## 🔒 Security

- Password is currently client-side only (for demo)
- For production, implement server-side verification
- Consider adding rate limiting
- Use authentication tokens for downloads

## 📝 License

This project uses yt-dlp, which is licensed under the Unlicense.

## ⚠️ Disclaimer

This tool is for personal use only. Please respect YouTube's Terms of Service and copyright laws. Only download videos you have permission to download.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

**way.tools** - Premium Tools, Simplified
