import re
from typing import List

class TextProcessor:
    """Utility functions for text processing"""
    
    @staticmethod
    def clean_transcript(transcript: str) -> str:
        """Clean and normalize transcript text"""
        # Remove extra whitespace
        transcript = re.sub(r'\s+', ' ', transcript)
        
        # Fix common transcription errors
        transcript = re.sub(r'(\w+)\.(\w+)', r'\1. \2', transcript)  # Add space after period
        
        # Remove non-printable characters
        transcript = ''.join(char for char in transcript if char.isprintable())
        
        return transcript.strip()
    
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 2000) -> List[str]:
        """Split text into manageable chunks"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            current_length += len(word) + 1
            if current_length > chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
            else:
                current_chunk.append(word)
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
    
    @staticmethod
    def format_time(seconds: int) -> str:
        """Format seconds to MM:SS"""
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"