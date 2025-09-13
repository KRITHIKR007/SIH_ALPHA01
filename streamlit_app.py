import streamlit as st
import requests
import io
import base64
from PIL import Image
import json
import time
from datetime import datetime
import os

# Configuration for Streamlit Cloud
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"

# Demo analysis function for fallback
def demo_analysis():
    """Provide demo analysis results when backend is not available"""
    import random
    time.sleep(2)  # Simulate processing time
    
    return {
        "session_id": f"demo_{int(time.time())}",
        "analysis_result": {
            "overall_score": round(random.uniform(0.3, 0.8), 2),
            "dyslexia_indicators": [
                "Letter reversals detected (b/d confusion)",
                "Inconsistent spacing patterns",
                "Reading fluency challenges"
            ],
            "recommendations": [
                "Practice with phonics-based reading exercises",
                "Use larger fonts and increased line spacing",
                "Consider text-to-speech tools for assistance"
            ],
            "confidence": round(random.uniform(0.7, 0.95), 2)
        }
    }

def call_api_with_fallback(url, method="GET", **kwargs):
    """Make API call with fallback to demo mode"""
    if DEMO_MODE:
        return demo_analysis()
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=10, **kwargs)
        else:
            response = requests.post(url, timeout=30, **kwargs)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.warning(f"API returned status {response.status_code}. Using demo mode.")
            return demo_analysis()
    except requests.exceptions.RequestException as e:
        st.warning("Backend API unavailable. Running in demo mode.")
        return demo_analysis()

# Set page configuration
st.set_page_config(
    page_title="MINDPIECE - AI Dyslexia Screening",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for OpenDyslexic font and dark theme
def load_custom_css():
    st.markdown("""
    <style>
    /* Import OpenDyslexic font from reliable CDN */
    @import url('https://cdn.jsdelivr.net/npm/opendyslexic@1.0.3/opendyslexic-regular.ttf');
    @font-face {
        font-family: 'OpenDyslexic';
        src: url('https://cdn.jsdelivr.net/gh/antijingoist/open-dyslexic@master/otf/OpenDyslexic-Regular.otf') format('opentype'),
             url('https://www.opendyslexic.org/downloads/OpenDyslexic-Regular.otf') format('opentype');
        font-weight: normal;
        font-style: normal;
        font-display: swap;
    }
    
    /* Dark theme with high contrast */
    .stApp {
        background-color: #1e1e1e;
        color: #f5f5f5;
    }
    
    /* Apply OpenDyslexic font globally */
    html, body, [class*="css"] {
        font-family: 'OpenDyslexic', 'Comic Sans MS', sans-serif !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
        color: #f5f5f5 !important;
    }
    
    /* High contrast buttons */
    .stButton > button {
        background-color: #4CAF50 !important;
        color: white !important;
        border: 2px solid #45a049 !important;
        font-family: 'OpenDyslexic', sans-serif !important;
        font-size: 18px !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background-color: #45a049 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3) !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #2d2d2d !important;
        border-right: 3px solid #4CAF50 !important;
    }
    
    /* Text areas and inputs */
    .stTextArea > div > div > textarea,
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stSelectbox select,
    .stMultiSelect > div > div > div,
    .stNumberInput > div > div > input {
        font-family: 'OpenDyslexic', sans-serif !important;
        font-size: 16px !important;
        background-color: #3d3d3d !important;
        color: #f5f5f5 !important;
        border: 2px solid #555555 !important;
        border-radius: 8px !important;
    }
    
    /* File uploader */
    .stFileUploader > div {
        background-color: #3d3d3d !important;
        border: 2px dashed #4CAF50 !important;
        border-radius: 8px !important;
        padding: 20px !important;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background-color: #2d5a2d !important;
        border-left: 5px solid #4CAF50 !important;
        font-family: 'OpenDyslexic', sans-serif !important;
    }
    
    .stError {
        background-color: #5a2d2d !important;
        border-left: 5px solid #f44336 !important;
        font-family: 'OpenDyslexic', sans-serif !important;
    }
    
    /* Chat-like interface styling */
    .chat-message {
        padding: 15px;
        margin: 10px 0;
        border-radius: 15px;
        font-family: 'OpenDyslexic', sans-serif;
        font-size: 16px;
        line-height: 1.6;
        color: #f5f5f5;
    }
    
    .user-message {
        background-color: #4CAF50;
        color: white;
        margin-left: 20%;
        text-align: right;
    }
    
    .assistant-message {
        background-color: #3d3d3d;
        color: #f5f5f5;
        margin-right: 20%;
        border-left: 4px solid #4CAF50;
    }
    
    /* Audio player styling */
    audio {
        width: 100% !important;
        height: 40px !important;
        background-color: #3d3d3d !important;
        border-radius: 8px !important;
    }
    
    /* Progress indicators */
    .stProgress > div > div > div > div {
        background-color: #4CAF50 !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #f5f5f5 !important;
        font-family: 'OpenDyslexic', sans-serif !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
    }
    
    /* Tabs and navigation */
    .stTabs [data-baseweb="tab-list"] {
        font-family: 'OpenDyslexic', sans-serif !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'OpenDyslexic', sans-serif !important;
        font-size: 16px !important;
    }
    
    /* Labels and captions */
    label, .stMarkdown, .stText, p, span, div {
        font-family: 'OpenDyslexic', sans-serif !important;
        color: #f5f5f5 !important;
    }
    
    /* Sidebar */
    .css-1d391kg p, .css-1d391kg span, .css-1d391kg div {
        font-family: 'OpenDyslexic', sans-serif !important;
        color: #f5f5f5 !important;
    }
    
    /* Logo and App Name Styling */
    .logo-container {
        text-align: center;
        padding: 20px 0;
    }
    
    .app-title {
        font-family: 'OpenDyslexic', sans-serif !important;
        font-size: 3em !important;
        font-weight: bold !important;
        color: #f5f5f5 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
        margin: 10px 0 !important;
    }
    
    .app-subtitle {
        font-family: 'OpenDyslexic', sans-serif !important;
        color: #4CAF50 !important;
        font-size: 1.2em !important;
        margin-top: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Use the configuration from the top of the file
# API_BASE_URL and DEMO_MODE are already defined above
ADMIN_TOKEN = "hackathon-admin-2024"

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = {}

def main():
    load_custom_css()
    
    # Logo and App Header
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image("assets/mindpiece_logo[1].png", width=200)
        except:
            st.markdown("🧠", unsafe_allow_html=True)
        st.markdown('<h1 class="app-title">MINDPIECE</h1>', unsafe_allow_html=True)
        st.markdown('<h3 class="app-subtitle">AI-Powered Dyslexia Screening</h3>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### *Accessible learning support through advanced AI analysis*")
    
    # Check backend connection
    if DEMO_MODE:
        st.info("🎭 Running in Demo Mode - Backend simulation active")
    else:
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                st.success("✅ Backend connected successfully")
            else:
                st.warning("⚠️ Backend connection issues - Falling back to demo mode")
        except requests.exceptions.RequestException:
            st.warning("⚠️ Cannot connect to backend server - Running in demo mode")
    
    # Sidebar navigation
    with st.sidebar:
        st.header("Navigation")
        page = st.selectbox(
            "Choose a feature:",
            ["Home", "Dyslexia Screening", "Text-to-Speech", "Results History", "Admin Panel"],
            index=0
        )
        
        st.markdown("---")
        st.markdown("### Accessibility Features")
        st.markdown("- OpenDyslexic Font")
        st.markdown("- High Contrast Theme")
        st.markdown("- Large Text Size")
        st.markdown("- Voice Navigation Ready")
        
        st.markdown("---")
        st.markdown("### Support")
        st.markdown("Need help? Contact our support team or refer to the user guide.")
    
    # Main content based on selected page
    if page == "Home":
        home_page()
    elif page == "Dyslexia Screening":
        screening_page()
    elif page == "Text-to-Speech":
        tts_page()
    elif page == "Results History":
        results_page()
    elif page == "Admin Panel":
        admin_page()

def home_page():
    """Welcome page with platform overview"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## Welcome to DyslexiaCare!
        
        Our AI-powered platform provides comprehensive dyslexia screening and accessibility tools to support learning for everyone.
        
        ### Key Features:
        
        **Multi-Modal Dyslexia Screening**
        - Text analysis for reading patterns
        - Handwriting analysis via advanced OCR
        - Speech analysis for fluency assessment
        - Comprehensive recommendations
        
        **Accessibility-First Text-to-Speech**
        - Adjustable reading speed
        - Phonics mode for learning
        - High-quality voice synthesis
        - Multiple language support
        
        **🎯 Designed for Accessibility**
        - OpenDyslexic font for better readability
        - High contrast dark theme
        - Large, clear interface elements
        - Voice-friendly navigation
        """)
        
        st.markdown("---")
        
        # Quick start buttons
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🚀 Start Screening", key="quick_screen"):
                st.session_state.page = "📊 Dyslexia Screening"
                st.rerun()
        
        with col_b:
            if st.button("🔊 Try Text-to-Speech", key="quick_tts"):
                st.session_state.page = "🔊 Text-to-Speech"
                st.rerun()
    
    with col2:
        st.markdown("""
        ### 📈 Platform Statistics
        """)
        
        # Platform status
        if DEMO_MODE:
            st.info("🎭 Running in Demo Mode")
        else:
            try:
                response = requests.get(f"{API_BASE_URL}/health", timeout=5)
                if response.status_code == 200:
                    st.success("✅ Platform is online and healthy")
                else:
                    st.warning("⚠️ Platform experiencing issues")
            except:
                st.warning("⚠️ Backend unavailable - Demo mode active")
        
        st.markdown("""
        ### 🎓 Learning Resources
        
        - **User Guide**: Complete walkthrough
        - **Video Tutorials**: Step-by-step demos  
        - **Best Practices**: Tips for effective use
        - **Community Forum**: Connect with others
        """)

def screening_page():
    """Comprehensive dyslexia screening interface"""
    st.header("📊 Dyslexia Screening Analysis")
    st.markdown("### Upload multiple types of input for comprehensive analysis")
    
    # Create tabs for different input methods
    tab1, tab2, tab3 = st.tabs(["📝 Text Input", "🖼️ Handwriting", "🎤 Audio Reading"])
    
    with tab1:
        st.markdown("#### Enter text sample for analysis")
        text_input = st.text_area(
            "Text to analyze:",
            placeholder="Type or paste text here for reading pattern analysis...",
            height=150,
            help="Enter a text sample to analyze reading patterns and potential dyslexia indicators"
        )
    
    with tab2:
        st.markdown("#### Upload handwriting sample")
        image_file = st.file_uploader(
            "Choose handwriting image",
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear image of handwritten text for OCR analysis"
        )
        
        if image_file is not None:
            image = Image.open(image_file)
            st.image(image, caption="Uploaded handwriting sample", use_column_width=True)
    
    with tab3:
        st.markdown("#### Upload audio recording of reading")
        audio_file = st.file_uploader(
            "Choose audio file",
            type=['wav', 'mp3', 'm4a'],
            help="Upload an audio recording of reading aloud for speech analysis"
        )
        
        if audio_file is not None:
            st.audio(audio_file, format="audio/wav")
    
    # Analysis controls
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("🔍 Run Analysis", key="run_screening", type="primary"):
            if text_input or image_file or audio_file:
                run_dyslexia_analysis(text_input, image_file, audio_file)
            else:
                st.error("⚠️ Please provide at least one input type for analysis")
    
    # Display results if available
    if "screening_result" in st.session_state:
        display_screening_results(st.session_state.screening_result)

def tts_page():
    """Text-to-speech interface with accessibility options"""
    st.header("🔊 Accessibility Text-to-Speech")
    st.markdown("### Convert text to natural-sounding speech with learning features")
    
    # Text input
    tts_text = st.text_area(
        "Text to convert to speech:",
        placeholder="Enter text to convert to audio...",
        height=150,
        help="Enter any text to convert to high-quality speech audio"
    )
    
    # TTS Options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        speed = st.slider(
            "🏃 Reading Speed",
            min_value=0.5,
            max_value=2.0,
            value=1.0,
            step=0.1,
            help="Adjust reading speed (0.5 = slow, 2.0 = fast)"
        )
    
    with col2:
        phonics_mode = st.checkbox(
            "🔤 Phonics Mode",
            help="Enable phonics mode for learning pronunciation"
        )
    
    with col3:
        language = st.selectbox(
            "🌍 Language",
            ["en", "es", "fr", "de"],
            help="Select language for text-to-speech"
        )
    
    # Generate audio
    if st.button("🎵 Generate Audio", key="generate_tts", type="primary"):
        if tts_text.strip():
            generate_tts_audio(tts_text, speed, phonics_mode, language)
        else:
            st.error("⚠️ Please enter text to convert to speech")

def results_page():
    """Display analysis history and results"""
    st.header("📈 Analysis Results History")
    st.markdown("### View your previous screening results and track progress")
    
    # Chat-like interface for results
    if st.session_state.chat_history:
        st.markdown("#### 💬 Analysis Conversation")
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>DyslexiaCare:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("📝 No analysis results yet. Complete a screening to see results here.")
    
    # Clear history button
    if st.session_state.chat_history:
        if st.button("🗑️ Clear History", key="clear_history"):
            st.session_state.chat_history = []
            st.session_state.analysis_results = {}
            st.success("✅ History cleared successfully")
            st.rerun()

def admin_page():
    """Admin panel for monitoring and management"""
    st.header("⚙️ Admin Panel")
    st.markdown("### Platform monitoring and data management")
    
    # Admin authentication
    admin_token = st.text_input("🔐 Admin Token", type="password", help="Enter admin token to access panel")
    
    if admin_token == ADMIN_TOKEN:
        st.success("✅ Admin access granted")
        
        # Platform statistics
        try:
            headers = {"Authorization": f"Bearer {admin_token}"}
            response = requests.get(f"{API_BASE_URL}/admin/stats", headers=headers, timeout=10)
            
            if response.status_code == 200:
                stats = response.json()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Sessions", stats.get("total_sessions", 0))
                with col2:
                    st.metric("Average Confidence", f"{stats.get('average_confidence_score', 0):.2f}")
                with col3:
                    st.metric("Sessions Today", stats.get("sessions_today", 0))
        
        except Exception as e:
            st.error(f"❌ Failed to fetch statistics: {e}")
        
        # Session management
        st.markdown("#### 📊 Session Management")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 View Sessions", key="view_sessions"):
                fetch_admin_sessions(admin_token)
        
        with col2:
            if st.button("🗑️ Clear All Sessions", key="clear_sessions", type="secondary"):
                clear_admin_sessions(admin_token)
    
    elif admin_token:
        st.error("❌ Invalid admin token")

def run_dyslexia_analysis(text, image_file, audio_file):
    """Execute dyslexia screening analysis"""
    with st.spinner("🔍 Analyzing inputs... This may take a moment."):
        try:
            # Prepare multipart form data
            files = {}
            data = {}
            
            if text:
                data['text'] = text
            
            if image_file:
                files['handwriting_image'] = image_file.getvalue()
            
            if audio_file:
                files['audio_file'] = audio_file.getvalue()
            
            # API call with fallback
            try:
                if DEMO_MODE:
                    # Use demo mode
                    result = demo_analysis()
                else:
                    # Try real API call
                    response = requests.post(
                        f"{API_BASE_URL}/api/v1/dyslexia/analyze",
                        data=data,
                        files=files if files else None,
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                    else:
                        st.warning("API call failed, using demo mode")
                        result = demo_analysis()
                
                st.session_state.screening_result = result
                
                # Add to chat history
                user_msg = f"Submitted for analysis: "
                if text:
                    user_msg += "text sample, "
                if image_file:
                    user_msg += "handwriting image, "
                if audio_file:
                    user_msg += "audio recording, "
                user_msg = user_msg.rstrip(", ")
                
                st.session_state.chat_history.append({"role": "user", "content": user_msg})
                
                # Assistant response
                analysis_summary = result.get("analysis", {}).get("screening_summary", "Analysis completed successfully.")
                st.session_state.chat_history.append({"role": "assistant", "content": analysis_summary})
                
                st.success("✅ Analysis completed successfully!")
                st.rerun()
                
            except requests.exceptions.RequestException as e:
                st.warning("⚠️ Backend connection failed, using demo mode")
                result = demo_analysis()
                st.session_state.screening_result = result
                st.success("✅ Analysis completed in demo mode!")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error during analysis: {e}")
                
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")

def display_screening_results(result):
    """Display comprehensive screening results"""
    st.markdown("---")
    st.header("📋 Analysis Results")
    
    # Overall summary
    confidence = result.get("confidence_score", 0)
    summary = result.get("screening_summary", "Analysis completed")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"#### {summary}")
        
        # Progress bar for confidence
        st.markdown("**Confidence Score:**")
        st.progress(confidence)
        st.markdown(f"*{confidence:.0%} confidence in screening assessment*")
    
    with col2:
        # Risk level indicator
        if confidence > 0.7:
            st.error("🔴 High Risk Indicators")
        elif confidence > 0.4:
            st.warning("🟡 Medium Risk Indicators")
        else:
            st.success("🟢 Low Risk Indicators")
    
    # Detailed analysis sections
    analysis = result.get("analysis", {})
    
    if analysis.get("text_analysis"):
        with st.expander("📝 Text Analysis Results", expanded=True):
            text_analysis = analysis["text_analysis"]
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Word Count", text_analysis.get("word_count", 0))
            with col2:
                st.metric("Avg Word Length", f"{text_analysis.get('average_word_length', 0):.1f}")
            with col3:
                st.metric("Complex Words", text_analysis.get("complex_words_count", 0))
            
            if text_analysis.get("reversals_detected"):
                st.warning("⚠️ Letter/word reversals detected:")
                for reversal in text_analysis["reversals_detected"]:
                    st.write(f"- Found '{reversal['detected']}' (should be '{reversal['should_be']}')")
    
    if analysis.get("speech_analysis"):
        with st.expander("🎤 Speech Analysis Results", expanded=True):
            speech_analysis = analysis["speech_analysis"]
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Reading Speed", f"{speech_analysis.get('reading_speed_wpm', 0):.0f} WPM")
            with col2:
                st.metric("Accuracy Score", f"{speech_analysis.get('accuracy_score', 0):.0%}")
            
            if speech_analysis.get("transcribed_text"):
                st.markdown("**Transcribed Text:**")
                st.write(speech_analysis["transcribed_text"])
    
    if analysis.get("ocr_analysis"):
        with st.expander("✍️ Handwriting Analysis Results", expanded=True):
            ocr_analysis = analysis["ocr_analysis"]
            
            if ocr_analysis.get("extracted_text"):
                st.markdown("**Extracted Text:**")
                st.write(ocr_analysis["extracted_text"])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("OCR Confidence", f"{ocr_analysis.get('text_confidence', 0):.0%}")
            with col2:
                st.metric("Writing Clarity", f"{ocr_analysis.get('writing_clarity_score', 0):.0%}")
    
    # Recommendations
    recommendations = result.get("recommendations", [])
    if recommendations:
        st.markdown("### 💡 Personalized Recommendations")
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"{i}. {rec}")

def generate_tts_audio(text, speed, phonics_mode, language):
    """Generate text-to-speech audio"""
    with st.spinner("🎵 Generating audio... Please wait."):
        try:
            payload = {
                "text": text,
                "speed": speed,
                "phonics_mode": phonics_mode,
                "language": language
            }
            
            if DEMO_MODE:
                # Demo mode - simulate TTS generation
                time.sleep(2)  # Simulate processing
                result = {
                    "audio_file_path": f"demo_tts_{int(time.time())}.wav",
                    "duration": len(text) * 0.1,  # Simulate duration
                    "settings_used": payload
                }
                st.success("✅ Audio generated successfully! (Demo Mode)")
                st.info("🎭 Demo Mode: In production, actual audio would be generated here")
            else:
                # Real API call
                response = requests.post(
                    f"{API_BASE_URL}/api/v1/tts/synthesize",
                    json=payload,
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Audio generated successfully!")
                else:
                    st.warning("TTS API failed, showing demo result")
                    result = {
                        "audio_file_path": f"demo_tts_{int(time.time())}.wav",
                        "duration": len(text) * 0.1,
                        "settings_used": payload
                    }
            
            # Display results
            st.markdown("#### 🎧 Generated Audio")
            if not DEMO_MODE:
                st.info(f"Audio file generated: {result['audio_file_path']}")
            else:
                st.info("Demo: Audio file would be available for download in production")
            st.write(f"Duration: {result.get('duration', 0):.1f} seconds")
            
            # Settings used
            settings = result.get("settings_used", {})
            st.markdown("**Settings Applied:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"Speed: {settings.get('speed', 1.0)}x")
            with col2:
                st.write(f"Phonics: {'Yes' if settings.get('phonics_mode') else 'No'}")
            with col3:
                st.write(f"Language: {settings.get('language', 'en')}")
            
            # Add to chat history
            st.session_state.chat_history.append({
                "role": "user", 
                "content": f"Generated TTS for: '{text[:50]}...'"
            })
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": f"Audio generated successfully! Duration: {result.get('duration', 0):.1f}s"
            })
                
        except requests.exceptions.RequestException as e:
            st.warning("⚠️ TTS backend unavailable, showing demo result")
            # Fallback demo result
            result = {
                "audio_file_path": f"demo_tts_{int(time.time())}.wav",
                "duration": len(text) * 0.1,
                "settings_used": payload
            }
            st.info("🎭 Demo Mode: Audio generation simulated")
        
        except Exception as e:
            st.error(f"❌ Error generating audio: {e}")

def fetch_admin_sessions(token):
    """Fetch admin session data"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_BASE_URL}/admin/sessions", headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            sessions = data.get("sessions", [])
            
            if sessions:
                st.success(f"✅ Found {len(sessions)} sessions")
                
                for session in sessions[:10]:  # Show last 10
                    with st.expander(f"Session {session['id']} - {session['timestamp'][:10]}"):
                        st.json(session)
            else:
                st.info("📝 No sessions found")
        else:
            st.error(f"❌ Failed to fetch sessions: {response.text}")
    
    except Exception as e:
        st.error(f"❌ Error fetching sessions: {e}")

def clear_admin_sessions(token):
    """Clear all admin sessions"""
    if st.button("⚠️ Confirm Clear All", key="confirm_clear"):
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.delete(
                f"{API_BASE_URL}/admin/clear",
                headers=headers,
                params={"confirm": True},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                st.success(f"✅ {result['message']}")
            else:
                st.error(f"❌ Failed to clear sessions: {response.text}")
        
        except Exception as e:
            st.error(f"❌ Error clearing sessions: {e}")

if __name__ == "__main__":
    main()