# Audio Quality Information

## MP3 Bitrate Limits

### Maximum Quality
- **320kbps is the MAXIMUM for MP3 format**
- This is the highest quality MP3 encoding available
- Higher bitrates don't exist for MP3 (the format maxes out at 320kbps)

### YouTube Source Audio Quality
- **YouTube typically provides:**
  - 128kbps AAC (most common)
  - 256kbps AAC (premium/higher quality videos)
  - Sometimes higher for premium content (rare)

### Important Notes

1. **Source Quality Matters:**
   - If YouTube's source is 128kbps AAC, converting to 320kbps MP3 **won't improve quality**
   - You can't add quality that wasn't in the source
   - Converting lossy to lossy (AAC → MP3) always loses some quality

2. **Best Practice:**
   - Use 320kbps for MP3 (maximum possible)
   - The app will use the **best available source** from YouTube
   - Then convert to your selected MP3 bitrate

3. **Format Comparison:**
   - **MP3**: 320kbps max (lossy compression)
   - **M4A/AAC**: Uses YouTube's original quality (typically 128-256kbps)
   - **WAV**: Lossless (huge files, but preserves original quality)
   - **FLAC**: Lossless compression (best quality, smaller than WAV)

## Current Implementation

The app now includes:
- ✅ Audio bitrate selector (320, 256, 192, 128 kbps)
- ✅ Automatically shows when audio formats are selected
- ✅ Uses best available source from YouTube
- ✅ Converts to selected MP3 bitrate

**Default: 320kbps** (best quality for MP3)

## Why 320kbps?

- It's the maximum MP3 supports
- Even if YouTube source is lower, using 320kbps ensures:
  - No additional quality loss during conversion
  - Maximum compatibility with MP3 players
  - Best sound quality possible for MP3 format

For even better quality, use:
- **M4A**: Preserves YouTube's original AAC format
- **FLAC**: Lossless compression (best quality, larger files)

