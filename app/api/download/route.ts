import { NextResponse } from 'next/server';
import { readFile, stat } from 'fs/promises';
import { join } from 'path';
import { existsSync } from 'fs';

const INSTALLER_FILENAME = 'YouTubeDownloaderSetup.exe';

export async function GET() {
  try {
    // Look for installer in these locations (in order of priority)
    const installerPaths = [
      join(process.cwd(), 'public', INSTALLER_FILENAME),
      join(process.cwd(), 'youtube_downloader', 'installer', INSTALLER_FILENAME),
    ];
    
    let filePath: string | null = null;
    
    // Find the first existing installer
    for (const path of installerPaths) {
      if (existsSync(path)) {
        filePath = path;
        break;
      }
    }
    
    // If no installer found, return error
    if (!filePath) {
      return NextResponse.json(
        { 
          error: 'Installer not found.',
          instruction: 'Please build the installer: cd youtube_downloader && build.bat && create_installer.bat'
        },
        { status: 404 }
      );
    }
    
    // Get file stats and read file
    const stats = await stat(filePath);
    const fileBuffer = await readFile(filePath);
    
    // Return response with proper headers for download
    // Add file hash to prevent caching issues
    const fileHash = stats.size.toString();
    
    return new NextResponse(fileBuffer, {
      headers: {
        'Content-Type': 'application/octet-stream',
        'Content-Disposition': `attachment; filename="${INSTALLER_FILENAME}"`,
        'Content-Length': stats.size.toString(),
        'Accept-Ranges': 'bytes',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
        'X-Content-Type-Options': 'nosniff',
        'X-File-Size': fileHash, // For debugging
      },
    });
  } catch (error: any) {
    console.error('Download error:', error);
    return NextResponse.json(
      { 
        error: 'Failed to download installer',
        details: process.env.NODE_ENV === 'development' ? error.message : undefined
      },
      { status: 500 }
    );
  }
}

