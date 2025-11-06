import { NextResponse } from 'next/server';
import { readFile, stat } from 'fs/promises';
import { join } from 'path';
import { existsSync } from 'fs';

const INSTALLER_FILENAME = 'YouTubeDownloaderSetup.exe';
const GITHUB_OWNER = process.env.GITHUB_OWNER || 'gridflame';
const GITHUB_REPO = process.env.GITHUB_REPO || 'waytools';
const GITHUB_RELEASE_TAG = process.env.GITHUB_RELEASE_TAG || 'v1.0.0';

async function fetchFromGitHub(): Promise<Response | null> {
  try {
    // GitHub Releases direct download URL format
    const githubUrl = `https://github.com/${GITHUB_OWNER}/${GITHUB_REPO}/releases/download/${GITHUB_RELEASE_TAG}/${INSTALLER_FILENAME}`;
    
    const response = await fetch(githubUrl, {
      headers: {
        'Accept': 'application/octet-stream',
        'User-Agent': 'way.tools-downloader',
      },
    });
    
    if (!response.ok) {
      console.error(`GitHub fetch failed: ${response.status} ${response.statusText}`);
      return null;
    }
    
    // Stream the file from GitHub
    const fileBuffer = await response.arrayBuffer();
    
    return new NextResponse(fileBuffer, {
      headers: {
        'Content-Type': 'application/octet-stream',
        'Content-Disposition': `attachment; filename="${INSTALLER_FILENAME}"`,
        'Content-Length': fileBuffer.byteLength.toString(),
        'Accept-Ranges': 'bytes',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
        'X-Content-Type-Options': 'nosniff',
        'X-Source': 'github-releases',
      },
    });
  } catch (error: any) {
    console.error('GitHub fetch error:', error);
    return null;
  }
}

export async function GET() {
  try {
    // Priority 1: Try local files first (for development)
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
    
    // If local file found, serve it
    if (filePath) {
      const stats = await stat(filePath);
      const fileBuffer = await readFile(filePath);
      
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
          'X-Source': 'local',
        },
      });
    }
    
    // Priority 2: Fetch from GitHub Releases
    const githubResponse = await fetchFromGitHub();
    if (githubResponse) {
      return githubResponse;
    }
    
    // If both fail, return error
    return NextResponse.json(
      { 
        error: 'Installer not found.',
        instruction: 'Please build the installer locally or ensure GitHub release exists.'
      },
      { status: 404 }
    );
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

