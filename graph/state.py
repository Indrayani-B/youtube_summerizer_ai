from typing import TypedDict, Optional, List
from langgraph.graph import MessagesState

class VideoState(TypedDict):
    """State for the YouTube video summarization workflow"""
    
    # Input
    url: str
    video_id: Optional[str]
    
    # Processing stages
    raw_transcript: Optional[str]
    cleaned_transcript: Optional[str]
    summary: Optional[str]
    insights: Optional[str]
    questions: Optional[str]
    final_report: Optional[str]
    
    # Metadata
    video_title: Optional[str]
    video_duration: Optional[int]
    error: Optional[str]
    processing_stage: str  # tracking which agent is working