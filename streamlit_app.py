"""
DyslexiaCare - AI-Powered Dyslexia Screening Platform
Streamlit Cloud Deployment Version
"""

import streamlit as st
import requests
import io
import base64
from PIL import Image
import json
import time
from datetime import datetime
import os

# Set page configuration
st.set_page_config(
    page_title="MINDPIECE - AI Dyslexia Screening",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "https://your-backend-api.herokuapp.com")
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"

# Custom CSS for OpenDyslexic font and accessibility
def load_custom_css():
    st.markdown("""
    <style>
    /* Import OpenDyslexic font */
    @import url('https://fonts.googleapis.com/css2?family=OpenDyslexic:wght@400;700&display=swap');
    
    /* Dark theme with high contrast */
    .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    
    /* Apply OpenDyslexic font globally */
    html, body, [class*="css"] {
        font-family: 'OpenDyslexic', 'Comic Sans MS', sans-serif !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
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
    }
    
    /* Input fields styling */
    .stTextInput > div > div > input {
        background-color: #2e2e2e !important;
        color: #ffffff !important;
        border: 2px solid #4CAF50 !important;
        font-family: 'OpenDyslexic', sans-serif !important;
        font-size: 16px !important;
    }
    
    /* Text area styling */
    .stTextArea > div > div > textarea {
        background-color: #2e2e2e !important;
        color: #ffffff !important;
        border: 2px solid #4CAF50 !important;
        font-family: 'OpenDyslexic', sans-serif !important;
        font-size: 16px !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #2e2e2e !important;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: #4CAF50 !important;
        font-family: 'OpenDyslexic', sans-serif !important;
    }
    
    /* Success/info boxes */
    .stSuccess {
        background-color: #1b5e20 !important;
        color: #ffffff !important;
    }
    
    .stInfo {
        background-color: #1565c0 !important;
        color: #ffffff !important;
    }
    
    .stWarning {
        background-color: #ef6c00 !important;
        color: #ffffff !important;
    }
    
    .stError {
        background-color: #c62828 !important;
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Demo analysis function for when backend is not available
def demo_analysis(text, analysis_type):
    """Provide demo analysis results when backend is not available"""
    import random
    time.sleep(2)  # Simulate processing time
    
    if analysis_type == "text":
        return {
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
            },
            "session_id": f"demo_{int(time.time())}"
        }
    elif analysis_type == "image":
        return {
            "analysis_result": {
                "overall_score": round(random.uniform(0.4, 0.7), 2),
                "handwriting_indicators": [
                    "Irregular letter formation",
                    "Inconsistent letter sizing",
                    "Spacing difficulties"
                ],
                "recommendations": [
                    "Practice handwriting with guided lines",
                    "Use occupational therapy exercises",
                    "Consider assistive writing tools"
                ],
                "confidence": round(random.uniform(0.6, 0.9), 2)
            },
            "session_id": f"demo_{int(time.time())}"
        }
    elif analysis_type == "audio":
        return {
            "analysis_result": {
                "overall_score": round(random.uniform(0.2, 0.6), 2),
                "speech_indicators": [
                    "Reading fluency below grade level",
                    "Difficulty with word pronunciation",
                    "Slower reading pace"
                ],
                "recommendations": [
                    "Practice reading aloud daily",
                    "Use audiobooks to support comprehension",
                    "Work with speech therapist if available"
                ],
                "confidence": round(random.uniform(0.5, 0.85), 2)
            },
            "session_id": f"demo_{int(time.time())}"
        }

def call_api(endpoint, data=None, files=None):
    """Make API call with fallback to demo mode"""
    if DEMO_MODE:
        return demo_analysis(
            data.get("input_text", "") if data else "",
            endpoint.split("/")[-1]
        )
    
    try:
        url = f"{API_BASE_URL}/api/v1/{endpoint}"
        if files:
            response = requests.post(url, data=data, files=files, timeout=30)
        else:
            response = requests.post(url, json=data, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.warning("Backend API unavailable. Running in demo mode.")
        return demo_analysis(
            data.get("input_text", "") if data else "",
            "text"
        )

def main():
    load_custom_css()
    
    # Header with logo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <h1 style="color: #4CAF50; font-size: 3em; margin-bottom: 0;">🧠 MINDPIECE</h1>
            <h3 style="color: #ffffff; margin-top: 0;">AI-Powered Dyslexia Screening Platform</h3>
        </div>
        """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Analysis Options")
        
        analysis_type = st.selectbox(
            "Choose Analysis Type:",
            ["Text Analysis", "Handwriting Analysis", "Speech Analysis", "Comprehensive Report"]
        )
        
        st.markdown("---")
        st.header("ℹ️ About")
        st.write("""
        **MINDPIECE** provides comprehensive dyslexia screening using advanced AI technology.
        
        Our platform offers:
        - 📝 Text pattern analysis
        - ✍️ Handwriting assessment  
        - 🗣️ Speech fluency evaluation
        - 📊 Detailed reporting
        """)
        
        if DEMO_MODE:
            st.info("🎭 Running in Demo Mode")
    
    # Main content area
    if analysis_type == "Text Analysis":
        st.header("📝 Text Analysis")
        st.write("Analyze text for dyslexia indicators including reading patterns and comprehension markers.")
        
        text_input = st.text_area(
            "Enter text to analyze:",
            height=150,
            placeholder="Type or paste text here for analysis..."
        )
        
        if st.button("🔍 Analyze Text", key="analyze_text"):
            if text_input.strip():
                with st.spinner("Analyzing text patterns..."):
                    result = call_api("analyze/text", {"input_text": text_input})
                    
                if result:
                    display_analysis_results(result, "Text Analysis")
            else:
                st.warning("Please enter some text to analyze.")
    
    elif analysis_type == "Handwriting Analysis":
        st.header("✍️ Handwriting Analysis")
        st.write("Upload an image of handwriting for dyslexia pattern detection.")
        
        uploaded_file = st.file_uploader(
            "Choose a handwriting image:",
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear image of handwritten text"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded handwriting sample", use_column_width=True)
            
            if st.button("🔍 Analyze Handwriting", key="analyze_handwriting"):
                with st.spinner("Analyzing handwriting patterns..."):
                    files = {"file": uploaded_file.getvalue()}
                    result = call_api("analyze/image", files=files)
                    
                if result:
                    display_analysis_results(result, "Handwriting Analysis")
    
    elif analysis_type == "Speech Analysis":
        st.header("🗣️ Speech Analysis")
        st.write("Upload an audio recording for reading fluency assessment.")
        
        uploaded_audio = st.file_uploader(
            "Choose an audio file:",
            type=['wav', 'mp3', 'ogg'],
            help="Upload a recording of reading or speech"
        )
        
        if uploaded_audio is not None:
            st.audio(uploaded_audio, format='audio/wav')
            
            if st.button("🔍 Analyze Speech", key="analyze_speech"):
                with st.spinner("Processing audio and analyzing speech patterns..."):
                    files = {"file": uploaded_audio.getvalue()}
                    result = call_api("analyze/audio", files=files)
                    
                if result:
                    display_analysis_results(result, "Speech Analysis")
    
    elif analysis_type == "Comprehensive Report":
        st.header("📊 Comprehensive Assessment")
        st.write("Complete multi-modal dyslexia screening combining text, handwriting, and speech analysis.")
        
        st.info("🚧 Complete all individual assessments first, then return here for a comprehensive report.")
        
        if st.button("📋 Generate Comprehensive Report"):
            with st.spinner("Generating comprehensive assessment..."):
                # In a real implementation, this would combine results from multiple assessments
                st.success("Feature coming soon! Please complete individual assessments first.")

def display_analysis_results(result, analysis_type):
    """Display analysis results in a user-friendly format"""
    if not result or "analysis_result" not in result:
        st.error("Invalid analysis result received.")
        return
    
    analysis = result["analysis_result"]
    
    st.success(f"✅ {analysis_type} Complete!")
    
    # Overall score
    score = analysis.get("overall_score", 0)
    confidence = analysis.get("confidence", 0)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Overall Risk Score", f"{score:.2f}", help="0.0 = Low Risk, 1.0 = High Risk")
    with col2:
        st.metric("Confidence Level", f"{confidence:.1%}")
    
    # Risk level assessment
    if score < 0.3:
        st.success("✅ Low Risk: No significant dyslexia indicators detected.")
    elif score < 0.6:
        st.warning("⚠️ Moderate Risk: Some dyslexia indicators present. Consider professional assessment.")
    else:
        st.error("🔴 High Risk: Multiple dyslexia indicators detected. Professional evaluation recommended.")
    
    # Indicators found
    indicators_key = "dyslexia_indicators"
    if "handwriting_indicators" in analysis:
        indicators_key = "handwriting_indicators"
    elif "speech_indicators" in analysis:
        indicators_key = "speech_indicators"
    
    if indicators_key in analysis and analysis[indicators_key]:
        st.subheader("🔍 Key Indicators Found:")
        for indicator in analysis[indicators_key]:
            st.write(f"• {indicator}")
    
    # Recommendations
    if "recommendations" in analysis and analysis["recommendations"]:
        st.subheader("💡 Recommendations:")
        for rec in analysis["recommendations"]:
            st.write(f"• {rec}")
    
    # Session information
    if "session_id" in result:
        st.caption(f"Session ID: {result['session_id']}")

# Footer
def show_footer():
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888888;">
        <p>🧠 MINDPIECE - Empowering learning through AI-driven accessibility</p>
        <p>Made with ❤️ for better learning outcomes</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    show_footer()