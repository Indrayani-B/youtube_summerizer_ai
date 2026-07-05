from .base import BaseAgent
from typing import Dict, Any
from utils.text_processing import TextProcessor

class SummarizerAgent(BaseAgent):
    """Agent responsible for generating summaries"""
    
    def __init__(self):
        super().__init__(temperature=0.3)
        self.text_processor = TextProcessor()
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive summary"""
        print("📝 Summarizer Agent: Creating summary...")
        
        transcript = state.get("cleaned_transcript")
        if not transcript:
            return {"error": "No cleaned transcript available"}
        
        # Handle long transcripts by chunking
        chunks = self.text_processor.chunk_text(transcript, 4000)
        
        if len(chunks) == 1:
            # Single chunk - generate full summary
            prompt = f"""Create a comprehensive summary of this video transcript.
            
            TRANSCRIPT:
            {transcript}
            
            Generate a well-structured summary with:
            1. Main topic/purpose of the video
            2. Key arguments or points made
            3. Conclusions or takeaways
            
            Format it nicely with clear sections."""
            
            summary = self.llm.invoke(prompt).content
        else:
            # Multiple chunks - generate chunk summaries first
            chunk_summaries = []
            for i, chunk in enumerate(chunks):
                prompt = f"Summarize this part {i+1}/{len(chunks)}: {chunk[:2000]}"
                chunk_summary = self.llm.invoke(prompt).content
                chunk_summaries.append(chunk_summary)
            
            # Combine chunk summaries
            combined = "\n".join(chunk_summaries)
            final_prompt = f"""Combine these section summaries into one coherent video summary:
            
            {combined}
            
            Create a flowing narrative that captures the entire video."""
            
            summary = self.llm.invoke(final_prompt).content
        
        return {
            "summary": summary,
            "processing_stage": "summary_generated"
        }