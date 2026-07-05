from .base import BaseAgent
from utils.text_processing import TextProcessor
from typing import Dict, Any

class CleanerAgent(BaseAgent):
    """Agent responsible for cleaning and preprocessing transcript"""
    
    def __init__(self):
        super().__init__(temperature=0.1)
        self.text_processor = TextProcessor()
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and chunk the transcript"""
        print("🧹 Cleaner Agent: Cleaning transcript...")
        
        raw_transcript = state.get("raw_transcript")
        if not raw_transcript:
            print("⚠️ No transcript to clean")
            return {
                "cleaned_transcript": "",
                "processing_stage": "transcript_cleaning_skipped",
                "warning": "No transcript available to clean"
            }
        
        try:
            # Clean the transcript
            cleaned = self.text_processor.clean_transcript(raw_transcript)
            
            # Optional: Use LLM for advanced cleaning if needed
            if len(cleaned) > 10000:  # For very long transcripts
                prompt = f"""Clean this transcript by:
                1. Fixing sentence boundaries
                2. Removing repeated phrases
                3. Correcting obvious transcription errors
                
                Transcript: {cleaned[:5000]}...
                
                Return only the cleaned version."""
                
                cleaned = self.llm.invoke(prompt).content
            
            return {
                "cleaned_transcript": cleaned,
                "processing_stage": "transcript_cleaned"
            }
        except Exception as e:
            print(f"Error cleaning transcript: {e}")
            return {
                "cleaned_transcript": raw_transcript,  # Return original if cleaning fails
                "processing_stage": "transcript_cleaning_failed",
                "warning": f"Cleaning failed: {str(e)}"
            }