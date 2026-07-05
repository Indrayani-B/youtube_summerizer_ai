import subprocess
import json
import os
import tempfile

class YouTubeTranscriptFetcher:
    """Fetch transcripts using yt-dlp (bypasses YouTube blocks)"""
    
    @staticmethod
    def get_transcript(video_url: str) -> str:
        """Download transcript using yt-dlp"""
        try:
            # Create temp directory for files
            with tempfile.TemporaryDirectory() as temp_dir:
                # Command to download only subtitles
                cmd = [
                    'yt-dlp',
                    '--write-subs',
                    '--sub-lang', 'en',
                    '--skip-download',
                    '--sub-format', 'vtt',
                    '-o', f'{temp_dir}/%(id)s.%(ext)s',
                    video_url
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode != 0:
                    print(f"yt-dlp error: {result.stderr}")
                    return None
                
                # Find the subtitle file
                files = os.listdir(temp_dir)
                vtt_files = [f for f in files if f.endswith('.en.vtt')]
                
                if not vtt_files:
                    return None
                
                # Read and parse VTT file
                vtt_path = os.path.join(temp_dir, vtt_files[0])
                with open(vtt_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse VTT to plain text
                lines = []
                for line in content.split('\n'):
                    # Skip VTT headers and timestamps
                    if line and not line.startswith('WEBVTT') and not line.startswith('NOTE'):
                        if '-->' not in line and not line.strip().isdigit():
                            if line.strip():
                                lines.append(line.strip())
                
                return ' '.join(lines)
                
        except Exception as e:
            print(f"Error fetching transcript: {e}")
            return None