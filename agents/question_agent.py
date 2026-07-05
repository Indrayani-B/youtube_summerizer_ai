from .base import BaseAgent
from typing import Dict, Any

class QuestionAgent(BaseAgent):
    """Agent responsible for generating questions"""
    
    def __init__(self):
        super().__init__(model_name= "llama-3.1-8b-instant",temperature=0.4)
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate different types of questions"""
        print("❓ Question Agent: Generating questions...")
        
        summary = state.get("summary", "")
        insights = state.get("insights", "")
        
        if not summary and not insights:
            return {
                "questions": "No content available to generate questions.",
                "processing_stage": "questions_failed"
            }
        
        prompt = f"""Generate comprehensive questions based on this video content.
        
        VIDEO SUMMARY:
        {summary if summary else "No summary available"}
        
        KEY INSIGHTS:
        {insights if insights else "No insights available"}
        
        Generate these types of questions:
        
        1. 📚 COMPREHENSION QUESTIONS (5 questions)
        - Test basic understanding
        - Should be answerable from the content
        
        2. 💭 DISCUSSION QUESTIONS (3 questions)
        - Thought-provoking
        - Connect ideas to real-world applications
        
        3. ✍️ PRACTICE QUESTIONS (2 questions)
        - Application-based
        - Require synthesis of multiple concepts
        
        4. 🎯 QUIZ QUESTIONS (5 multiple choice)
        - Include 4 options each
        - Mark the correct answer
        
        Format clearly with emojis and sections."""
        
        try:
            questions = self.llm.invoke(prompt).content
        except Exception as e:
            print(f"Error generating questions: {e}")
            questions = "Failed to generate questions due to an error."
        
        return {
            "questions": questions,
            "processing_stage": "questions_generated"
        }