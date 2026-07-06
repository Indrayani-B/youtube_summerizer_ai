import streamlit as st
import sys
import os
import traceback
import time  # 👈 Add this missing import

# Add project root to path - more robust method
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Debug sidebar - always show
st.sidebar.write("### 🔍 Debug Info")
st.sidebar.write(f"Project root: {project_root}")
st.sidebar.write(f"Python path: {sys.path[:3]}...")

# Test imports
try:
    from tools.youtube_tools import YouTubeTools
    st.sidebar.success("✅ YouTubeTools imported")
    
    # Test methods
    tools = YouTubeTools()
    test_url = "https://www.youtube.com/watch?v=UF8uR6Z6KLc"
    video_id = tools.extract_video_id(test_url)
    st.sidebar.write(f"✅ extract_video_id test: {video_id}")
    
except Exception as e:
    st.sidebar.error(f"❌ Import error: {str(e)}")
    st.sidebar.code(traceback.format_exc())

try:
    from graph.workflow import VideoSummaryWorkflow
    st.sidebar.success("✅ Workflow imported")
except Exception as e:
    st.sidebar.error(f"❌ Workflow import error: {str(e)}")

# Page config
st.set_page_config(
    page_title="AI YouTube Summarizer",
    page_icon="🎬",
    layout="wide"
)

# Title and description
st.title("🎬 AI YouTube Video Summarizer")
st.markdown("""
Transform any YouTube video into structured notes, insights, and questions using 
**LangGraph Multi-Agent System**. Perfect for lectures, podcasts, and tutorials!
""")

# Sidebar main content
with st.sidebar:
    st.header("⚙️ Settings")
    
    st.subheader("About")
    st.markdown("""
    **How it works:**
    1. 🤖 Transcript Agent - Fetches video transcript
    2. 🧹 Cleaner Agent - Preprocesses text
    3. 📝 Summarizer Agent - Creates summary
    4. 💡 Insight Agent - Extracts key points
    5. ❓ Question Agent - Generates questions
    6. 📊 Report Agent - Compiles final output
    """)
    
    st.subheader("Powered by")
    st.markdown("""
    - LangGraph
    - Groq LLM
    - YouTube API
    - Streamlit
    """)

# Main content
col1, col2 = st.columns([3, 1])

with col1:
    url = st.text_input(
        "🔗 Enter YouTube URL:",
        placeholder="https://youtube.com/watch?v=...",
        value="https://www.youtube.com/watch?v=UF8uR6Z6KLc"  # Default test URL
    )

with col2:
    process_btn = st.button("🚀 Process Video", type="primary", use_container_width=True)

# Initialize session state
if 'result' not in st.session_state:
    st.session_state.result = None
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'error_details' not in st.session_state:
    st.session_state.error_details = None

# Process video
if process_btn and url:
    st.session_state.processing = True
    st.session_state.error_details = None
    
    # Create placeholder for progress
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    error_placeholder = st.empty()
    
    with st.spinner("Processing video..."):
        try:
            # Initialize workflow
            workflow = VideoSummaryWorkflow()
            
            # Process with progress updates
            stages = [
                "📝 Fetching transcript...",
                "🧹 Cleaning text...",
                "📊 Generating summary...",
                "💡 Extracting insights...",
                "❓ Creating questions...",
                "📑 Compiling report..."
            ]
            
            progress_bar = progress_placeholder.progress(0)
            
            # Actually process the video
            result = workflow.process_video(url)
            
            # Update progress bar through stages
            for i, stage in enumerate(stages):
                status_placeholder.info(stage)
                progress_bar.progress((i + 1) / len(stages))
                time.sleep(0.5)  # Small delay for visual effect
            
            progress_bar.empty()
            status_placeholder.empty()
            
            if result.get("error"):
                st.error(f"❌ Error: {result['error']}")
                st.session_state.error_details = result.get("error")
            else:
                st.session_state.result = result
                #st.success("✅ Video processed successfully!")
                
        except Exception as e:
            error_msg = str(e)
            error_trace = traceback.format_exc()
            st.error(f"❌ An error occurred: {error_msg}")
            
            # Show detailed error in expander
            with st.expander("🔍 View Error Details"):
                st.code(error_trace)
            
            st.session_state.error_details = error_msg
        
        st.session_state.processing = False

# Display results
if st.session_state.result and not st.session_state.processing:
    result = st.session_state.result
    
    # Show success message with stats
    st.success(f"✅ Video processed successfully!")
    
    # Show some stats
    col1, col2, col3 = st.columns(3)
    with col1:
        if result.get("summary"):
            st.metric("Summary Length", f"{len(result['summary'])} chars")
    with col2:
        if result.get("insights"):
            st.metric("Insights", "Extracted")
    with col3:
        if result.get("questions"):
            st.metric("Questions", "Generated")
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs([
        "📑 Full Report", 
        "📝 Summary", 
        "💡 Insights", 
        "❓ Questions"
    ])
    
    with tab1:
        st.markdown("## 📑 Complete Report")
        st.markdown(result.get("final_report", "No report available"))
        
        # Download button
        st.download_button(
            label="📥 Download Report",
            data=result.get("final_report", ""),
            file_name="video_summary.md",
            mime="text/markdown"
        )
    
    with tab2:
        st.markdown("### 📝 Video Summary")
        summary = result.get("summary", "No summary available")
        st.markdown(summary)
        
        # Copy button for summary
        if st.button("📋 Copy Summary"):
            st.write("Summary copied to clipboard (simulated)")
    
    with tab3:
        st.markdown("### 💡 Key Insights")
        insights = result.get("insights", "No insights available")
        st.markdown(insights)
    
    with tab4:
        st.markdown("### ❓ Questions & Discussion Points")
        questions = result.get("questions", "No questions available")
        st.markdown(questions)

# Show error details if any
if st.session_state.error_details and not st.session_state.processing:
    with st.expander("🔧 Troubleshooting Tips"):
        st.markdown(f"""
        **Error:** {st.session_state.error_details}
        
        **Common solutions:**
        1. Make sure the video has captions enabled
        2. Try a different video (TED talks work well)
        3. Check your internet connection
        4. Verify the URL is correct
        
        **Test with this working video:**
        ```
        https://www.youtube.com/watch?v=UF8uR6Z6KLc
        ```
        """)

# Footer
st.markdown("---")
st.markdown(
    "Built with LangGraph • Multi-Agent AI System • Final Project",
    help="Each agent performs specialized tasks in the workflow"
)