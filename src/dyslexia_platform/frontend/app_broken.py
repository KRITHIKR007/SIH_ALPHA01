import streamlit as st
import requests
import io
import base64
from PIL import Image
import json
import time
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="DyslexiaCare - AI Screening Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# C        # Handle quick navigation from home page
        if 'quick_nav' in st.session_state:
            page = st.session_state['quick_nav']
            del st.session_state['quick_nav']
        else:
            page = st.selectbox(
                "Where would you like to go?",
                ["🏠 Welcome Home", "🔍 Learning Assessment", "🎵 Text to Voice", "📚 My Progress", "⚙️ Settings"],
                index=0
            ) CSS for dyslexia-friendly design
def load_custom_css():
    st.markdown("""
    <style>
    /* Import dyslexia-friendly fonts */
    @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&display=swap');
    
    /* Modern gradient background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #2c3e50;
    }
    
    /* Apply dyslexia-friendly font globally */
    html, body, [class*="css"] {
        font-family: 'Lexend', 'Atkinson Hyperlegible', 'Comic Sans MS', sans-serif !important;
        font-size: 18px !important;
        line-height: 1.8 !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Sophisticated button styling */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        font-family: 'Lexend', sans-serif !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        padding: 14px 28px !important;
        border-radius: 25px !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        letter-spacing: 0.5px !important;
        text-transform: none !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
        background: linear-gradient(45deg, #5a6fd8, #6a4c93) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(0.98) !important;
        transition: all 0.1s ease !important;
    }
    
    /* Sidebar with modern glass effect */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border-right: 3px solid rgba(102, 126, 234, 0.6) !important;
        border-radius: 0 15px 15px 0 !important;
    }
    
    /* Card-like containers */
    .stContainer > div {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 20px !important;
        padding: 25px !important;
        margin: 10px 0 !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Text areas and inputs with modern styling */
    .stTextArea > div > div > textarea,
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div {
        font-family: 'Lexend', sans-serif !important;
        font-size: 16px !important;
        background: rgba(255, 255, 255, 0.9) !important;
        color: #2c3e50 !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 15px !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease !important;
        letter-spacing: 0.5px !important;
    }
    
    .stTextArea > div > div > textarea:focus,
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        outline: none !important;
    }
    
    /* File uploader with attractive styling */
    .stFileUploader > div {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(240, 248, 255, 0.9)) !important;
        border: 3px dashed #667eea !important;
        border-radius: 20px !important;
        padding: 30px !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader > div:hover {
        border-color: #764ba2 !important;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(240, 248, 255, 0.95)) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Success/Error messages with better colors */
    .stSuccess {
        background: linear-gradient(45deg, #48bb78, #38a169) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 15px 20px !important;
        font-family: 'Lexend', sans-serif !important;
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.3) !important;
    }
    
    .stError {
        background: linear-gradient(45deg, #fc8181, #f56565) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 15px 20px !important;
        font-family: 'Lexend', sans-serif !important;
        box-shadow: 0 4px 15px rgba(252, 129, 129, 0.3) !important;
    }
    
    .stWarning {
        background: linear-gradient(45deg, #fbb860, #f6ad55) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 15px 20px !important;
        font-family: 'Lexend', sans-serif !important;
        box-shadow: 0 4px 15px rgba(251, 184, 96, 0.3) !important;
    }
    
    .stInfo {
        background: linear-gradient(45deg, #63b3ed, #4299e1) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 15px 20px !important;
        font-family: 'Lexend', sans-serif !important;
        box-shadow: 0 4px 15px rgba(99, 179, 237, 0.3) !important;
    }
    
    /* Chat-like interface with modern bubbles */
    .chat-message {
        padding: 20px;
        margin: 15px 0;
        border-radius: 25px;
        font-family: 'Lexend', sans-serif;
        font-size: 16px;
        line-height: 1.8;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .user-message {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        margin-left: 15%;
        text-align: right;
        animation: slideInRight 0.5s ease;
    }
    
    .assistant-message {
        background: linear-gradient(45deg, rgba(255, 255, 255, 0.95), rgba(240, 248, 255, 0.95));
        color: #2c3e50;
        margin-right: 15%;
        border-left: 5px solid #667eea;
        animation: slideInLeft 0.5s ease;
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Audio player with modern styling */
    audio {
        width: 100% !important;
        height: 50px !important;
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        border-radius: 25px !important;
        border: none !important;
    }
    
    /* Progress indicators */
    .stProgress > div > div > div > div {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        border-radius: 10px !important;
    }
    
    /* Headers with beautiful styling */
    h1, h2, h3 {
        color: #2c3e50 !important;
        font-family: 'Lexend', sans-serif !important;
        font-weight: 600 !important;
        text-shadow: none !important;
        letter-spacing: 0.5px !important;
    }
    
    h1 {
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem !important;
    }
    
    /* Metrics and stats styling */
    .metric-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(240, 248, 255, 0.9));
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 2px solid rgba(102, 126, 234, 0.2);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        color: white !important;
        border-radius: 15px !important;
        font-family: 'Lexend', sans-serif !important;
        font-weight: 500 !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 15px !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        color: #2c3e50 !important;
        font-family: 'Lexend', sans-serif !important;
        font-weight: 500 !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        color: white !important;
        border-color: transparent !important;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, #5a6fd8, #6a4c93);
    }
    </style>
    """, unsafe_allow_html=True)

# Configuration
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from config.settings import get_settings

settings = get_settings()
API_BASE_URL = settings.api_base_url
ADMIN_TOKEN = "hackathon-admin-2024"

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = {}

def main():
    load_custom_css()
    
    # Header with friendly approach
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 3rem; margin-bottom: 0.5rem;">🌈 DyslexiaCare</h1>
        <h3 style="color: #667eea; font-weight: 400; margin-bottom: 1rem;">Your Friendly Learning Companion</h3>
        <p style="font-size: 1.2rem; color: #666; max-width: 600px; margin: 0 auto; line-height: 1.8;">
            Empowering every learner with AI-powered support, designed especially for dyslexic minds
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation with friendly icons
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h2 style="color: #667eea;">🎯 Your Journey</h2>
        </div>
        """, unsafe_allow_html=True)
        
        page = st.selectbox(
            "Where would you like to go?",
            ["🏠 Welcome Home", "� Learning Assessment", "🎵 Text to Voice", "� My Progress", "⚙️ Settings"],
            index=0
        )
        
        st.markdown("---")
        st.markdown("""
        <div style="padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 15px; margin: 1rem 0;">
            <h4 style="color: #667eea; margin-bottom: 1rem;">💜 Dyslexia-Friendly Features</h4>
            <div style="font-size: 14px; line-height: 2;">
                🔤 <strong>Lexend Font</strong> - Easier reading<br/>
                🌈 <strong>Soft Colors</strong> - Eye-friendly design<br/>
                📏 <strong>Spaced Text</strong> - Better letter recognition<br/>
                🎯 <strong>Simple Navigation</strong> - Clear and intuitive<br/>
                🔊 <strong>Audio Support</strong> - Listen to text
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Reading comfort controls
        st.markdown("### 🎛️ Reading Comfort")
        text_size = st.slider("Text Size", 14, 24, 18, help="Adjust text size for comfortable reading")
        line_spacing = st.slider("Line Spacing", 1.4, 2.2, 1.8, 0.1, help="More space between lines")
        
        # Apply reading comfort settings
        st.markdown(f"""
        <style>
        html, body, [class*="css"] {{
            font-size: {text_size}px !important;
            line-height: {line_spacing} !important;
        }}
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 📞 Support")
        st.markdown("Need help? Contact our support team or refer to the user guide.")
    
    # Main content based on selected page
    if page == "🏠 Welcome Home":
        home_page()
    elif page == "� Learning Assessment":
        screening_page()
    elif page == "🎵 Text to Voice":
        tts_page()
    elif page == "� My Progress":
        results_page()
    elif page == "⚙️ Settings":
        admin_page()

def home_page():
    """Welcome page with encouraging overview"""
    
    # Welcome message with encouragement
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: rgba(255,255,255,0.9); border-radius: 25px; margin: 2rem 0;">
        <h2 style="color: #667eea; margin-bottom: 1rem;">Welcome to Your Learning Journey! 🌟</h2>
        <p style="font-size: 1.3rem; color: #555; line-height: 1.8; max-width: 800px; margin: 0 auto;">
            Every brilliant mind learns differently. You're in the right place to discover your unique learning style 
            and unlock your full potential. Let's explore together! 💪
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards in a more visual layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #667eea; margin-bottom: 1rem;">� Learning Assessment</h3>
            <p style="color: #666; line-height: 1.8;">
                Discover your unique learning patterns through our gentle, AI-powered assessment. 
                Upload text, images, or voice recordings for personalized insights.
            </p>
            <ul style="text-align: left; color: #666; margin-top: 1rem;">
                <li>📝 Text reading analysis</li>
                <li>✍️ Handwriting pattern recognition</li>
                <li>🗣️ Speech fluency assessment</li>
                <li>🎯 Personalized recommendations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card" style="margin-top: 2rem;">
            <h3 style="color: #667eea; margin-bottom: 1rem;">🎵 Text to Voice</h3>
            <p style="color: #666; line-height: 1.8;">
                Turn any text into clear, natural speech. Perfect for learning pronunciation, 
                understanding complex words, or just giving your eyes a rest.
            </p>
            <ul style="text-align: left; color: #666; margin-top: 1rem;">
                <li>🔊 Crystal clear voice synthesis</li>
                <li>⚡ Adjustable reading speed</li>
                <li>📚 Phonics learning mode</li>
                <li>🌍 Multiple language support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #667eea; margin-bottom: 1rem;">💜 Built for You</h3>
            <p style="color: #666; line-height: 1.8;">
                Every feature is designed with dyslexic learners in mind. We use research-backed 
                design principles to make learning comfortable and enjoyable.
            </p>
            <div style="margin-top: 1.5rem;">
                <div style="background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 15px; border-radius: 15px; margin: 10px 0;">
                    <strong>🔤 Lexend Font</strong><br/>
                    Specially designed font that improves reading proficiency by 25%
                </div>
                <div style="background: linear-gradient(45deg, #48bb78, #38a169); color: white; padding: 15px; border-radius: 15px; margin: 10px 0;">
                    <strong>🌈 Gentle Colors</strong><br/>
                    Soft gradients that reduce visual stress and eye strain
                </div>
                <div style="background: linear-gradient(45deg, #63b3ed, #4299e1); color: white; padding: 15px; border-radius: 15px; margin: 10px 0;">
                    <strong>📏 Perfect Spacing</strong><br/>
                    Optimal letter and line spacing for better recognition
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Encouraging call-to-action
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(45deg, rgba(102,126,234,0.1), rgba(118,75,162,0.1)); border-radius: 25px; margin: 2rem 0;">
        <h3 style="color: #667eea; margin-bottom: 1rem;">Ready to Start Your Journey? 🚀</h3>
        <p style="font-size: 1.1rem; color: #666; margin-bottom: 1.5rem;">
            Choose what feels right for you today. There's no pressure, no judgment - just support and understanding.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick start buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔍 Start Assessment", help="Begin your personalized learning assessment"):
            st.session_state['quick_nav'] = '🔍 Learning Assessment'
            st.rerun()
    
    with col2:
        if st.button("🎵 Try Text to Voice", help="Experience our text-to-speech feature"):
            st.session_state['quick_nav'] = '🎵 Text to Voice'
            st.rerun()
    
    with col3:
        if st.button("📚 View Progress", help="Check your learning journey"):
            st.session_state['quick_nav'] = '📚 My Progress'
            st.rerun()
        
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
        
        # Fetch and display stats
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                st.success("✅ Platform is online and healthy")
            else:
                st.warning("⚠️ Platform experiencing issues")
        except:
            st.error("❌ Cannot connect to backend services")
        
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
            
            # API call
            response = requests.post(
                f"{API_BASE_URL}/check_dyslexia",
                data=data,
                files=files if files else None,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
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
            
            else:
                st.error(f"❌ Analysis failed: {response.text}")
        
        except Exception as e:
            st.error(f"❌ Error during analysis: {e}")

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
            
            response = requests.post(
                f"{API_BASE_URL}/tts",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                
                st.success("✅ Audio generated successfully!")
                
                # Display audio player (placeholder - in real implementation would serve the file)
                st.markdown("#### 🎧 Generated Audio")
                st.info(f"Audio file generated: {result['audio_file_path']}")
                st.write(f"Duration: {result['duration']:.1f} seconds")
                
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
                    "content": f"Audio generated successfully! Duration: {result['duration']:.1f}s"
                })
            
            else:
                st.error(f"❌ TTS generation failed: {response.text}")
        
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