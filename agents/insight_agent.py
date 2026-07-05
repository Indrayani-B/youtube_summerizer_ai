from .base import BaseAgent
from typing import Dict, Any

class InsightAgent(BaseAgent):
    """Agent responsible for extracting key insights"""
    
    def __init__(self):
        super().__init__(model_name= "llama-3.1-8b-instant",temperature=0.4)
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key insights and learning outcomes"""
        print("💡 Insight Agent: Extracting key insights...")
        
        # Check if required data exists
        transcript = state.get("cleaned_transcript")
        summary = state.get("summary")
        
        if not transcript and not summary:
            return {
                "error": "No transcript or summary available for insight extraction",
                "insights": "Unable to generate insights due to missing content.",
                "processing_stage": "insights_failed"
            }
        
        # Prepare content safely
        transcript_preview = transcript[:3000] if transcript else "No transcript available"
        summary_text = summary if summary else "No summary available"
        
        prompt = f"""Based on this video content, extract the KEY INSIGHTS.
        
        VIDEO SUMMARY:
        {summary_text}
        
        FULL TRANSCRIPT EXCERPT:
        {transcript_preview}...
        
        Provide:
        1. 🎯 Main Takeaways (3-5 bullet points)
        2. 💡 Key Ideas Explained
        3. 🔍 Important Details Worth Remembering
        4. 🎓 Learning Outcomes
        
        Make each insight actionable and clear."""
        
        try:
            insights = self.llm.invoke(prompt).content
        except Exception as e:
            print(f"Error generating insights: {e}")
            insights = "Failed to generate insights due to an error."
        
        return {
            "insights": insights,
            "processing_stage": "insights_generated"
        }