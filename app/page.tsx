'use client';

import Image from "next/image";
import { useState, useRef, useEffect } from "react";
import PasswordProtection from "./components/PasswordProtection";

export default function Home() {
  const [isDownloading, setIsDownloading] = useState(false);
  const [downloadProgress, setDownloadProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const downloadAbortController = useRef<AbortController | null>(null);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (downloadAbortController.current) {
        downloadAbortController.current.abort();
      }
    };
  }, []);

  const handleDownload = async () => {
    // Prevent multiple simultaneous downloads
    if (isDownloading) return;
    
    // Abort any existing download
    if (downloadAbortController.current) {
      downloadAbortController.current.abort();
    }
    
    setIsDownloading(true);
    setError(null);
    setDownloadProgress(0);
    
    try {
      // Create new abort controller
      downloadAbortController.current = new AbortController();
      
      // Download the executable with progress tracking
      // Add timestamp to bypass cache
      const timestamp = Date.now();
      const response = await fetch(`/api/download?t=${timestamp}`, {
        signal: downloadAbortController.current.signal,
        cache: 'no-store',
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `Download failed: ${response.statusText}`);
      }
      
      // Get content length for progress calculation
      const contentLength = response.headers.get('content-length');
      const total = contentLength ? parseInt(contentLength, 10) : 0;
      
      if (!response.body) {
        throw new Error('No response body');
      }
      
      const reader = response.body.getReader();
      const chunks: Uint8Array[] = [];
      let receivedLength = 0;
      
      // Read stream with progress tracking
      // Use requestAnimationFrame to batch UI updates and prevent browser freezing
      const updateProgress = () => {
        if (total > 0 && receivedLength > 0) {
          const progress = Math.min(99, Math.round((receivedLength / total) * 100));
          setDownloadProgress(progress);
        }
      };
      
      let lastUpdate = 0;
      const UPDATE_INTERVAL = 100; // Update UI every 100ms
      
      while (true) {
        const { done, value } = await reader.read();
        
        if (done) break;
        
        chunks.push(value);
        receivedLength += value.length;
        
        // Throttle progress updates to prevent UI freezing
        const now = Date.now();
        if (now - lastUpdate >= UPDATE_INTERVAL) {
          updateProgress();
          lastUpdate = now;
          // Yield to browser to prevent freezing
          await new Promise(resolve => setTimeout(resolve, 0));
        }
      }
      
      // Final progress update
      setDownloadProgress(100);
      
      // Combine chunks into blob
      const blob = new Blob(chunks, { type: 'application/octet-stream' });
      
      // Get filename from Content-Disposition header or default
      const contentDisposition = response.headers.get('content-disposition');
      let filename = 'YouTubeDownloaderSetup.exe';
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+?)"?$/i);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
      }
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      link.style.display = 'none';
      
      // Trigger download
      document.body.appendChild(link);
      link.click();
      
      // Cleanup after a short delay
      setTimeout(() => {
        if (document.body.contains(link)) {
          document.body.removeChild(link);
        }
        window.URL.revokeObjectURL(url);
        setIsDownloading(false);
      }, 200);
      
    } catch (error: any) {
      // Don't show error if download was aborted
      if (error.name === 'AbortError') {
        setIsDownloading(false);
        setDownloadProgress(0);
        return;
      }
      
      console.error('Download error:', error);
      setError(error.message || 'Download failed. Please try again.');
      setIsDownloading(false);
      setDownloadProgress(0);
    } finally {
      downloadAbortController.current = null;
    }
  };

  return (
    <PasswordProtection>
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        <div className="container mx-auto px-4 py-16">
          <div className="max-w-4xl mx-auto">
            {/* Logo */}
            <div className="flex justify-center mb-12">
              <Image
                src="/logo.png"
                alt="way.tools"
                width={120}
                height={120}
                className="rounded-2xl shadow-lg"
                priority
              />
            </div>

            {/* Main Content */}
            <div className="text-center mb-16">
              <h1 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
                way.tools
              </h1>
              <p className="text-xl text-gray-600 dark:text-gray-300 mb-12">
                Premium tools, simplified.
              </p>
            </div>

            {/* Tool Card */}
            <div className="bg-white dark:bg-gray-800 rounded-3xl shadow-2xl p-8 md:p-12 mb-12">
              <div className="flex flex-col md:flex-row items-center gap-8">
                {/* Tool Icon */}
                <div className="text-8xl md:text-9xl">
                  🎥
                </div>

                {/* Tool Info */}
                <div className="flex-1 text-center md:text-left">
                  <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
                    YouTube Downloader
                  </h2>
                  <p className="text-lg text-gray-600 dark:text-gray-300 leading-relaxed mb-6">
                    Download any YouTube video or audio in your preferred format. 
                    Choose from MP4, WebM, MP3, M4A, WAV, FLAC and more. 
                    Select your desired quality from 1080p to 240p. 
                    Simple, fast, and completely free.
                  </p>
                  <div className="flex flex-wrap gap-2 justify-center md:justify-start">
                    <span className="px-4 py-2 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full text-sm font-medium">
                      MP4 • WebM • MP3
                    </span>
                    <span className="px-4 py-2 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 rounded-full text-sm font-medium">
                      1080p • 720p • 480p
                    </span>
                    <span className="px-4 py-2 bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200 rounded-full text-sm font-medium">
                      Windows Installer
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Download Button */}
            <div className="text-center">
              <button
                onClick={handleDownload}
                disabled={isDownloading}
                className="group relative inline-flex items-center justify-center px-12 py-6 text-xl font-bold text-white bg-gradient-to-r from-blue-600 via-blue-700 to-indigo-700 rounded-2xl shadow-2xl hover:shadow-3xl transform hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none disabled:hover:scale-100"
              >
                <span className="absolute inset-0 w-full h-full bg-gradient-to-r from-blue-700 via-indigo-700 to-purple-700 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></span>
                <span className="relative flex items-center gap-3">
                  {isDownloading ? (
                    <>
                      <svg className="animate-spin h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Downloading... {downloadProgress > 0 && `${downloadProgress}%`}
                    </>
                  ) : (
                    <>
                      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                      </svg>
                      Download Installer
                    </>
                  )}
                </span>
              </button>
              
              {/* Progress Bar */}
              {isDownloading && downloadProgress > 0 && (
                <div className="mt-4 w-full max-w-md mx-auto">
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
                    <div 
                      className="bg-blue-600 h-2.5 rounded-full transition-all duration-300 ease-out"
                      style={{ width: `${downloadProgress}%` }}
                    ></div>
                  </div>
                </div>
              )}
              
              {/* Error Message */}
              {error && (
                <div className="mt-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                  <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
                  <button
                    onClick={() => setError(null)}
                    className="mt-2 text-xs text-red-600 dark:text-red-400 hover:underline"
                  >
                    Dismiss
                  </button>
                </div>
              )}
              
              {!isDownloading && !error && (
                <p className="mt-4 text-sm text-gray-500 dark:text-gray-400">
                  Clean installer • No bloatware • Safe & Secure
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </PasswordProtection>
  );
}
