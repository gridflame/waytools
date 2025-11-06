import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  // Increase body size limit for large file downloads
  experimental: {
    serverActions: {
      bodySizeLimit: '200mb',
    },
  },
};

export default nextConfig;
