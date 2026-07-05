from .base import BaseAgent
from tools.youtube_tools import YouTubeTools
from typing import Dict, Any

class TranscriptAgent(BaseAgent):
    """Agent responsible for fetching video transcript"""
    
    def __init__(self):
        super().__init__(temperature=0.1)
        self.youtube_tools = YouTubeTools()
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Extract transcript from YouTube URL"""
        print("🎬 Transcript Agent: Fetching video transcript...")
        
        url = state.get("url")
        if not url:
            return {
                "error": "No URL provided",
                "processing_stage": "failed"
            }
        
        # Extract video ID
        video_id = self.youtube_tools.extract_video_id(url)
        if not video_id:
            return {
                "error": "Invalid YouTube URL - could not extract video ID",
                "processing_stage": "failed"
            }
        
        print(f"📹 Video ID: {video_id}")
        
        # Get transcript using yt-dlp method
        transcript_data = self.youtube_tools.get_transcript(url)
        
        # Check for errors
        if not transcript_data:
            return {
                "error": "Could not fetch transcript - no data returned",
                "processing_stage": "failed"
            }
        
        if "error" in transcript_data:
            return {
                "error": f"Transcript fetch failed: {transcript_data['error']}",
                "processing_stage": "failed"
            }
        
        # Success case
        return {
            "video_id": video_id,
            "raw_transcript": transcript_data.get('full', ''),
            "transcript_preview": transcript_data.get('timestamped_preview', ''),
            "processing_stage": "transcript_fetched"
        }