import os
from dotenv import load_dotenv
from graph.workflow import VideoSummaryWorkflow
import json

load_dotenv()

class YouTubeSummarizer:
    """Main application class"""
    
    def __init__(self):
        self.workflow = VideoSummaryWorkflow()
    
    def summarize(self, url: str, output_format: str = "text") -> str:
        """Summarize a YouTube video"""
        
        print(f"🎥 Processing video: {url}")
        print("="*50)
        
        # Process through workflow
        result = self.workflow.process_video(url)
        
        # Check for errors
        if result.get("error"):
            return f"❌ Error: {result['error']}"
        
        # Return in requested format
        if output_format == "json":
            return json.dumps(result, indent=2)
        else:
            return result.get("final_report", "No report generated")
    
    def save_report(self, url: str, filename: str = "summary.md"):
        """Save summary to file"""
        report = self.summarize(url)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ Report saved to {filename}")

def main():
    """CLI interface"""
    summarizer = YouTubeSummarizer()
    
    print("🚀 YouTube Video Summarizer with LangGraph")
    print("-"*40)
    
    url = input("Enter YouTube URL: ").strip()
    
    if not url:
        print("❌ No URL provided")
        return
    
    print("\n⏳ Processing... This may take a minute...\n")
    
    result = summarizer.summarize(url)
    print(result)

if __name__ == "__main__":
    main()