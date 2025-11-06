# Code Signing Guide for way.tools Installer

## Problem: Browser Security Warnings

Browsers (Chrome, Edge, Firefox) flag unsigned executables as potentially malicious. This is a security feature, not a reflection of your software's safety.

## Why This Happens

1. **No Digital Signature**: The installer isn't digitally signed
2. **Low Download Count**: New files have low reputation scores
3. **Unknown Publisher**: Browsers don't recognize the publisher
4. **SmartScreen/Chrome Warnings**: Windows and Chrome warn about unsigned software

## Immediate Solutions (User-Facing)

### 1. Add Notice on Website ✅ (Already added)
- Users see a warning that the browser alert is normal
- Link to GitHub Releases for verification

### 2. User Instructions
When users see the warning:
- **Chrome**: Click "Keep" → "Download anyway"
- **Edge**: Click "Keep" → "Show more" → "Keep anyway"
- **Windows Defender**: Click "More info" → "Run anyway"

## Proper Solution: Code Signing

To **permanently fix** browser warnings, you need a **Code Signing Certificate**.

### Option 1: Commercial Code Signing Certificate (Recommended)

**Cost**: $200-500/year

**Providers**:
- **DigiCert**: https://www.digicert.com/code-signing/
- **Sectigo** (formerly Comodo): https://sectigo.com/ssl-certificates-tls/code-signing
- **GlobalSign**: https://www.globalsign.com/en/code-signing-certificate

**Steps**:
1. Purchase certificate from provider
2. Complete identity verification (can take 1-3 days)
3. Download certificate
4. Sign the installer (see below)

### Option 2: Self-Signed Certificate (NOT Recommended)

Self-signed certificates **WILL NOT** remove browser warnings. They're only useful for internal testing.

### Option 3: Open Source Certificate (Free)

**Cost**: Free (for open source projects)

**Providers**:
- **SignPath.io**: Free for open source projects
- Check if your project qualifies

## How to Sign the Installer

### Using Inno Setup (Recommended)

1. **Install SignTool** (comes with Windows SDK or Visual Studio)

2. **Add to `create_installer.iss`**:
```inno
[Setup]
SignTool=signtool
SignedUninstaller=yes

[Code]
#define SignToolPath "C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe"
#define CertificateFile "path\to\certificate.pfx"
#define CertificatePassword "your-password"
```

3. **Add signing command**:
```inno
[Setup]
SignTool=signtool sign /f "{#CertificateFile}" /p "{#CertificatePassword}" /t http://timestamp.digicert.com /d "way.tools YouTube Downloader" /du "https://way.tools" $f
```

### Using SignTool Manually

After building the installer:

```powershell
# Sign the installer
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com /d "way.tools YouTube Downloader" /du "https://way.tools" installer\YouTubeDownloaderSetup.exe

# Verify signature
signtool verify /pa installer\YouTubeDownloaderSetup.exe
```

### Sign Both the EXE and Installer

1. **Sign the executable** (YouTubeDownloader.exe):
```powershell
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com /d "way.tools YouTube Downloader" /du "https://way.tools" dist\YouTubeDownloader.exe
```

2. **Then build the installer** (which includes the signed exe)

3. **Sign the installer** (YouTubeDownloaderSetup.exe):
```powershell
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com /d "way.tools YouTube Downloader" /du "https://way.tools" installer\YouTubeDownloaderSetup.exe
```

## Current Workaround

For now, the website includes:
- ✅ Notice explaining the browser warning
- ✅ Link to GitHub Releases for verification
- ✅ Clear messaging that it's safe

Users can:
1. Download from GitHub Releases directly (more trusted)
2. Click through the browser warning (it's safe)
3. Verify the file on GitHub before installing

## Best Practices

1. **Always sign releases** once you have a certificate
2. **Use timestamping** (`/t` flag) so signature doesn't expire
3. **Sign both** the executable and installer
4. **Update Inno Setup script** to auto-sign during build

## Timeline

- **Immediate**: Users see notice, can download from GitHub
- **Short-term**: Consider getting a code signing certificate
- **Long-term**: All installers are signed, no warnings

## Cost-Benefit Analysis

**Cost**: $200-500/year for certificate  
**Benefit**: 
- No browser warnings
- Professional appearance
- Better user trust
- Faster downloads (no reputation delays)

**Recommendation**: If this is a commercial project or you plan to distribute widely, get a certificate. For personal/open-source with low download volume, the current workaround is acceptable.

