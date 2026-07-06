# graph/workflow.py

from langgraph.graph import StateGraph, END
from typing import Dict, Any, Literal
from .state import VideoState
from agents.transcript_agent import TranscriptAgent
from agents.cleaner_agent import CleanerAgent
from agents.summarizer_agent import SummarizerAgent
from agents.insight_agent import InsightAgent
from agents.question_agent import QuestionAgent
from agents.report_agent import ReportAgent

class VideoSummaryWorkflow:
    """Main LangGraph workflow for video summarization"""
    
    def __init__(self):
        # Initialize agents
        self.transcript_agent = TranscriptAgent()
        self.cleaner_agent = CleanerAgent()
        self.summarizer_agent = SummarizerAgent()
        self.insight_agent = InsightAgent()
        self.question_agent = QuestionAgent()
        self.report_agent = ReportAgent()
        
        # Build graph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Construct the LangGraph workflow"""
        
        # Initialize graph
        workflow = StateGraph(VideoState)
        
        # Add nodes for each agent
        workflow.add_node("transcript_agent", self._run_transcript_agent)
        workflow.add_node("cleaner_agent", self._run_cleaner_agent)
        workflow.add_node("summarizer_agent", self._run_summarizer_agent)
        workflow.add_node("insight_agent", self._run_insight_agent)
        workflow.add_node("question_agent", self._run_question_agent)
        workflow.add_node("report_agent", self._run_report_agent)
        
        # Define edges (flow)
        workflow.set_entry_point("transcript_agent")
        
        # Add conditional routing
        workflow.add_conditional_edges(
            "transcript_agent",
            self._route_after_transcript
        )
        
        workflow.add_conditional_edges(
            "cleaner_agent",
            self._route_after_cleaner
        )
        
        workflow.add_conditional_edges(
            "summarizer_agent",
            self._route_after_summarizer
        )
        
        workflow.add_conditional_edges(
            "insight_agent",
            self._route_after_insight
        )
        
        workflow.add_conditional_edges(
            "question_agent",
            self._route_after_question
        )
        
        workflow.add_edge("report_agent", END)
        
        return workflow.compile()
    
    def _run_transcript_agent(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Run transcript agent"""
        return self.transcript_agent.process(state)
    
    def _run_cleaner_agent(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Run cleaner agent"""
        return self.cleaner_agent.process(state)
    
    def _run_summarizer_agent(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Run summarizer agent"""
        return self.summarizer_agent.process(state)
    
    def _run_insight_agent(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Run insight agent"""
        return self.insight_agent.process(state)
    
    def _run_question_agent(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Run question agent"""
        return self.question_agent.process(state)
    
    def _run_report_agent(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Run report agent"""
        return self.report_agent.process(state)
    
    def _route_after_transcript(self, state: Dict[str, Any]) -> str:
        """Route after transcript agent with better error handling"""
        if state.get("error"):
            error_msg = state.get("error", "Unknown error")
            print(f"❌ Transcript agent error: {error_msg}")
            
            # Create a user-friendly error report
            state["final_report"] = f"""# ❌ Error Processing Video

**Error:** {error_msg}

## Possible Reasons:
- The video may not have captions/transcripts enabled
- YouTube might be blocking automated access
- The video might be private or unavailable

## Suggestions:
1. Try a different video (TED talks, educational content usually work well)
2. Make sure the video has captions enabled
3. Check if you can see "Show transcript" option on YouTube

## Videos That Usually Work:
- TED Talks: https://www.youtube.com/@TED
- Kurzgesagt: https://www.youtube.com/@Kurzgesagt
- CrashCourse: https://www.youtube.com/@crashcourse
"""
            return "report_agent"
        return "cleaner_agent"
    
    def _route_after_cleaner(self, state: Dict[str, Any]) -> str:
        """Route after cleaner agent"""
        if state.get("error"):
            print("❌ Cleaner agent failed, but continuing with original transcript")
            # Use raw transcript if cleaning failed
            state["cleaned_transcript"] = state.get("raw_transcript", "")
        return "summarizer_agent"
    
    def _route_after_summarizer(self, state: Dict[str, Any]) -> str:
        """Route after summarizer agent"""
        if not state.get("summary"):
            print("⚠️ Summarizer agent produced no summary, continuing with placeholder")
            state["summary"] = "Summary generation failed."
        return "insight_agent"
    
    def _route_after_insight(self, state: Dict[str, Any]) -> str:
        """Route after insight agent"""
        if not state.get("insights"):
            print("⚠️ Insight agent produced no insights, continuing with placeholder")
            state["insights"] = "Insight generation failed."
        return "question_agent"
    
    def _route_after_question(self, state: Dict[str, Any]) -> str:
        """Route after question agent"""
        if not state.get("questions"):
            print("⚠️ Question agent produced no questions, continuing with placeholder")
            state["questions"] = "Question generation failed."
        return "report_agent"
    
    def process_video(self, url: str) -> Dict[str, Any]:
        """Process a YouTube video URL through the workflow"""
        initial_state = {
            "url": url,
            "processing_stage": "started",
            "raw_transcript": None,
            "cleaned_transcript": None,
            "summary": None,
            "insights": None,
            "questions": None,
            "final_report": None,
            "error": None
        }
        
        try:
            # Run the graph
            final_state = self.graph.invoke(initial_state)
            return final_state
        except Exception as e:
            print(f"❌ Workflow error: {str(e)}")
            return {
                **initial_state,
                "error": str(e),
                "final_report": f"❌ An error occurred: {str(e)}"
            }