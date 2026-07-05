from tools.youtube_tools import YouTubeTools
import sys

def test_transcript_fetcher():
    """Test the transcript fetcher with various URLs"""
    
    # Test URLs - these should all have transcripts
    test_urls = [
        "https://www.youtube.com/watch?v=UF8uR6Z6KLc",  # Steve Jobs speech
        "https://youtu.be/7Hk9jct2ozY",                 # Kurzgesagt - Eggs
        "https://www.youtube.com/watch?v=8N9Kq7M4xWk"   # TED Talk
    ]
    
    tools = YouTubeTools()
    
    for url in test_urls:
        print("\n" + "="*60)
        print(f"Testing URL: {url}")
        print("="*60)
        
        # Extract video ID
        video_id = tools.extract_video_id(url)
        print(f"✅ Extracted Video ID: {video_id}")
        
        # Get transcript
        print("📥 Fetching transcript...")
        result = tools.get_transcript(url)
        
        if result and 'full' in result:
            transcript = result['full']
            print(f"✅ Success! Transcript length: {len(transcript)} characters")
            print(f"📝 Preview: {transcript[:300]}...")
            
            # Check if it's valid
            if len(transcript) > 100:
                print("✅ Transcript validation: PASSED (sufficient length)")
            else:
                print("⚠️ Transcript validation: WARNING (very short)")
        else:
            print(f"❌ Failed: {result.get('error', 'Unknown error')}")
        
        print()

if __name__ == "__main__":
    test_transcript_fetcher()