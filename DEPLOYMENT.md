# Deployment Guide for way.tools

## Quick Start

### 1. Build the YouTube Downloader Executable

Before deploying, you need to build the executable:

```bash
cd youtube_downloader
python build.py
# or on Windows:
build.bat
```

This will:
- Install dependencies (yt-dlp, pyinstaller, pillow)
- Copy logo.png from public folder
- Convert logo to ICO format
- Build the executable
- Copy it to `public/YouTubeDownloader.exe` for web download

### 2. Deploy to Vercel

#### Option A: GitHub Integration (Recommended)

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
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will auto-detect Next.js
   - Click "Deploy"

3. **Note:** The executable needs to be built and committed to the repository in the `public` folder. Since executables are large, consider:
   - Using Git LFS for the .exe file
   - Or building it in a CI/CD pipeline
   - Or hosting the .exe on a separate CDN

#### Option B: Manual Deployment

```bash
npm install
npm run build
vercel deploy
```

### 3. Environment Variables

No environment variables are required. The password is hardcoded in the client component for simplicity.

**Security Note:** For production, consider moving password verification to a server-side API route.

### 4. Post-Deployment

After deployment:
1. Visit your Vercel URL
2. Enter password: `apple123`
3. Test the download functionality

## Updating the Executable

When you update the YouTube downloader:

1. Make changes to `youtube_downloader/main.py`
2. Rebuild: `cd youtube_downloader && python build.py`
3. The build script automatically copies to `public/YouTubeDownloader.exe`
4. Commit and push:
   ```bash
   git add public/YouTubeDownloader.exe
   git commit -m "Update YouTube Downloader"
   git push
   ```
5. Vercel will auto-deploy

## File Structure

```
.
├── app/
│   ├── api/download/route.ts    # Download API endpoint
│   ├── components/
│   │   └── PasswordProtection.tsx # Password gate
│   ├── page.tsx                  # Main landing page
│   └── layout.tsx                # Root layout
├── public/
│   ├── logo.png                  # Site logo
│   └── YouTubeDownloader.exe    # Built executable (from build)
├── youtube_downloader/
│   ├── main.py                   # YouTube downloader app
│   ├── build.py                  # Build script
│   ├── build.bat                 # Windows build script
│   └── requirements.txt          # Python dependencies
├── vercel.json                   # Vercel configuration
└── package.json                  # Next.js dependencies
```

## Troubleshooting

### Executable not found
- Make sure you've run the build script
- Check that `public/YouTubeDownloader.exe` exists
- Verify file size (should be > 10MB)

### Build fails
- Ensure Python 3.8+ is installed
- Run: `pip install -r youtube_downloader/requirements.txt`
- Check that logo.png exists in public folder

### Download fails on Vercel
- Vercel has a 50MB file size limit for serverless functions
- For large files, consider:
  - Using Vercel Blob Storage
  - Hosting on AWS S3 or similar
  - Using a CDN like Cloudflare

## Custom Domain

To use way.tools domain:

1. In Vercel dashboard, go to Project Settings
2. Click "Domains"
3. Add `way.tools` and `www.way.tools`
4. Update DNS records as instructed by Vercel

## Security Considerations

- Password is client-side only (for demo purposes)
- For production, implement server-side password verification
- Consider rate limiting on download endpoint
- Add authentication tokens for downloads

