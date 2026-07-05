import re
import subprocess
import os
import tempfile
from typing import Optional, Dict
import time
import random

class YouTubeTools:
    """Complete YouTube tools with transcript fetching and video ID extraction"""
    
    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """Extract video ID from various YouTube URL formats"""
        patterns = [
            r'(?:youtube\.com\/watch\?v=)([\w-]+)',  # Standard watch URL
            r'(?:youtu\.be\/)([\w-]+)',              # Short youtu.be URL
            r'(?:youtube\.com\/embed\/)([\w-]+)',     # Embed URL
            r'(?:youtube\.com\/v\/)([\w-]+)',         # Old embed URL
            r'(?:youtube\.com\/shorts\/)([\w-]+)'     # Shorts URL
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        # Try to extract from any URL with video ID pattern
        match = re.search(r'([\w-]{11})', url)
        if match:
            return match.group(1)
            
        return None
    
    @staticmethod
    def get_transcript_with_ytdlp(video_url: str) -> Optional[Dict]:
        """Fetch transcript using yt-dlp (most reliable method)"""
        try:
            print(f"📥 Fetching transcript with yt-dlp for: {video_url}")
            
            # Create temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                # Extract video ID for filename
                video_id = YouTubeTools.extract_video_id(video_url)
                if not video_id:
                    video_id = "temp_video"
                
                # yt-dlp command to download subtitles
                cmd = [
                    'yt-dlp',
                    '--write-subs',
                    '--sub-lang', 'en,en-US,en-GB',  # Try multiple English variants
                    '--sub-format', 'vtt',
                    '--skip-download',  # Don't download video
                    '--quiet',
                    '--no-warnings',
                    '-o', f'{temp_dir}/%(id)s.%(ext)s',
                    video_url
                ]
                
                # Run yt-dlp
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode != 0:
                    print(f"⚠️ yt-dlp warning: {result.stderr}")
                
                # Look for subtitle files
                files = os.listdir(temp_dir)
                vtt_files = [f for f in files if f.endswith('.vtt')]
                
                if not vtt_files:
                    # Try with auto-generated subtitles
                    cmd_auto = [
                        'yt-dlp',
                        '--write-auto-subs',  # Get auto-generated subtitles
                        '--sub-lang', 'en',
                        '--sub-format', 'vtt',
                        '--skip-download',
                        '--quiet',
                        '-o', f'{temp_dir}/%(id)s.%(ext)s',
                        video_url
                    ]
                    
                    result = subprocess.run(cmd_auto, capture_output=True, text=True)
                    files = os.listdir(temp_dir)
                    vtt_files = [f for f in files if f.endswith('.vtt')]
                
                if not vtt_files:
                    return {"error": "No subtitles found for this video"}
                
                # Read the first subtitle file
                vtt_path = os.path.join(temp_dir, vtt_files[0])
                with open(vtt_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse VTT content to plain text
                lines = []
                for line in content.split('\n'):
                    # Skip VTT headers, timestamps, and empty lines
                    if (line and 
                        not line.startswith('WEBVTT') and 
                        not line.startswith('NOTE') and
                        '-->' not in line and
                        not line.strip().isdigit() and
                        not line.startswith('<c>') and
                        line.strip()):
                        # Clean HTML tags if any
                        clean_line = re.sub(r'<[^>]+>', '', line)
                        if clean_line.strip():
                            lines.append(clean_line.strip())
                
                full_transcript = ' '.join(lines)
                
                # Create timestamped preview (first 10 entries)
                timestamped_lines = []
                for i, line in enumerate(lines[:10]):
                    timestamped_lines.append(f"[{i*30//60:02d}:{(i*30)%60:02d}] {line}")
                
                return {
                    'full': full_transcript,
                    'timestamped_preview': '\n'.join(timestamped_lines),
                    'method': 'yt-dlp'
                }
                
        except Exception as e:
            print(f"❌ Error in yt-dlp transcript fetch: {e}")
            return {"error": f"Failed to fetch transcript: {str(e)}"}
    
    @staticmethod
    def get_transcript(video_url: str) -> Optional[Dict]:
        """Main method to get transcript with fallbacks"""
        
        # Method 1: Try yt-dlp first (most reliable)
        print("🔄 Trying yt-dlp method...")
        result = YouTubeTools.get_transcript_with_ytdlp(video_url)
        
        if result and 'full' in result and result['full']:
            print("✅ Successfully fetched transcript with yt-dlp")
            return result
        
        # If yt-dlp fails, return error
        return {"error": "Could not fetch transcript with any method"}
    
    @staticmethod
    def get_video_info(video_url: str) -> Dict:
        """Get basic video information"""
        video_id = YouTubeTools.extract_video_id(video_url)
        return {
            'url': video_url,
            'video_id': video_id,
            'extracted_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }