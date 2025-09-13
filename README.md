# 🧠 MINDPIECE - AI-Powered Dyslexia Screening Platform

> **Comprehensive dyslexia screening and accessibility learning platform with professional branding and OpenDyslexic accessibility features.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Live-brightgreen)](http://localhost:8502)

**🚀 Live Application**: Frontend at [localhost:8502](http://localhost:8502) | Backend at [localhost:8000](http://localhost:8000)

## 📋 Table of Contents
- [🌟 Features](#-features)
- [⚡ Quick Start](#-quick-start)
- [🔧 Installation](#-installation)
- [🚀 Usage](#-usage)
- [📊 API Documentation](#-api-documentation)
- [🎯 Accessibility](#-accessibility)
- [🤖 AI/ML Pipeline](#-aiml-pipeline)
- [🗄️ Database](#️-database)
- [🌐 Deployment](#-deployment)
- [🧪 Testing](#-testing)
- [📈 Monitoring](#-monitoring)
- [🤝 Contributing](#-contributing)

## 🌟 Features

### 📊 Multi-Modal Dyslexia Screening
- **Text Analysis**: Pattern detection for reading comprehension issues
- **Handwriting OCR**: Advanced handwriting analysis via EasyOCR
- **Speech-to-Text**: Reading fluency assessment using OpenAI Whisper
- **NLP Error Detection**: Levenshtein distance for spelling/reversal patterns
- **Comprehensive Reporting**: Detailed analysis with confidence scoring

### 🔊 Accessibility-First Text-to-Speech
- **Coqui TTS Integration**: High-quality, offline voice synthesis
- **Adjustable Speed**: 0.5x to 2.0x reading speeds
- **Phonics Mode**: Syllable-based pronunciation for learning
- **Multi-language Support**: English, Spanish, French, German
- **Audio Processing**: pydub-powered speed/pitch adjustments

### 🎨 User Experience & Branding
- **Mindpiece Branding**: Professional logo and visual identity
- **OpenDyslexic Font**: Specialized font throughout entire application
- **Pale White Text Theme**: Optimized contrast on dark backgrounds
- **High Contrast Design**: Dark mode optimized for accessibility
- **Chat Interface**: Conversational results presentation
- **Large UI Elements**: Touch and vision-friendly design
- **Voice Navigation Ready**: Structured for screen readers

### 🛠️ Technical Infrastructure
- **FastAPI Backend**: Async, production-grade API server (Port 8000)
- **Streamlit Frontend**: Rapid, Python-native UI development (Port 8502)
- **SQLite Database**: Zero-config, reliable data storage
- **Admin Panel**: Token-protected monitoring and management
- **Pipeline Orchestration**: Modular AI component management

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │     FastAPI     │    │   AI Pipelines  │
│   Frontend      │◄──►│    Backend      │◄──►│                 │
│                 │    │                 │    │ • OCR (EasyOCR) │
│ • OpenDyslexic  │    │ • /api/v1/      │    │ • STT (Whisper) │
│ • Dark Theme    │    │   dyslexia/     │    │ • NLP Analysis  │
│ • File Upload   │    │ • /api/v1/tts/  │    │ • TTS (Coqui)   │
│ • Chat UI       │    │ • /health       │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ SQLite Database │
                       │                 │
                       │ • Sessions      │
                       │ • Analysis      │
                       │ • Feedback      │
                       └─────────────────┘
```

### 🗂️ Project Structure

```
SIH_dex/
├── README.md                 # This file
├── requirements.txt          # All dependencies
├── .env                     # Environment configuration
├── config/
│   ├── __init__.py
│   ├── settings.py          # Centralized configuration
│   └── .env.example         # Configuration template
├── src/
│   └── dyslexia_platform/   # Main application package
│       ├── __init__.py
│       ├── backend/         # FastAPI backend
│       │   ├── main.py      # FastAPI application
│       │   ├── api/         # API routes and dependencies
│       │   └── models/      # Pydantic schemas
│       ├── frontend/        # Streamlit frontend
│       │   └── app.py       # Main frontend application
│       ├── database/        # Database models and connection
│       │   ├── models.py    # SQLAlchemy models
│       │   └── connection.py
│       ├── pipelines/       # AI/ML processing pipelines
│       │   ├── dyslexia_analysis.py
│       │   ├── tts_pipeline.py
│       │   └── base.py
│       ├── shared/          # Shared utilities and constants
│       │   ├── utils.py
│       │   ├── constants.py
│       │   └── exceptions.py
│       └── data/           # Data storage
│           ├── uploads/    # User uploaded files
│           ├── outputs/    # Generated content
│           └── models/     # AI model storage
├── tests/                  # Test suite
├── docs/                   # Documentation
├── scripts/                # Development scripts
│   ├── setup_dev.py       # Development setup
│   ├── run_backend.py     # Start backend server
│   └── run_frontend.py    # Start frontend server
└── logs/                  # Application logs
```

## ⚡ Quick Start

### 🚀 Start the Complete Application

**Backend Server**:
```bash
cd SIH_dex
python -m uvicorn backend.main_simple:app --reload --host localhost --port 8000
```

**Frontend Application**:
```bash
cd SIH_dex
streamlit run src\dyslexia_platform\frontend\app.py --server.port 8502
```

**Access URLs**:
- **Frontend**: http://localhost:8502
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 🖥️ Manual Setup (Development)
```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup environment
cp config/.env.example .env
# Edit .env with your settings

# 5. Start the servers
python scripts/run_backend.py    # Backend server
python scripts/run_frontend.py   # Frontend server (in new terminal)
```

**Access Points:**
- 🌐 **Frontend**: http://localhost:8501
- 📖 **API Docs**: http://localhost:8000/docs
- ⚡ **Health Check**: http://localhost:8000/health
- 📊 **API Info**: http://localhost:8000/api/v1/info

## 🔧 Installation & Current Status

### ✅ Application Status
- **✅ Backend Running**: Port 8000 with all AI pipelines initialized
- **✅ Frontend Running**: Port 8502 with Mindpiece branding
- **✅ Database Connected**: SQLite with session tracking
- **✅ OpenDyslexic Font**: Fully implemented across all UI elements
- **✅ Pale White Theme**: Optimized for accessibility and dyslexia
- **✅ Logo Integration**: Mindpiece brand identity with assets/mindpiece_logo[1].png

### 🎨 Current UI Features
- **Mindpiece Branding**: Professional logo display and app name
- **OpenDyslexic Font**: Applied to all text elements (headers, inputs, buttons, chat)
- **Pale White Color Scheme**: `#f5f5f5` text on dark `#1e1e1e` background
- **Accessibility Optimized**: High contrast, large fonts, touch-friendly elements
- **Responsive Design**: Centered layout with proper spacing and shadows

### System Requirements
- **Python**: 3.8+
- **RAM**: 4GB+ (8GB recommended for AI models)
- **Storage**: 2GB+ free space
- **OS**: Windows 10+, macOS 10.14+, Ubuntu 18.04+

### Dependencies Overview

#### Backend Stack
```
FastAPI          # Web framework
SQLAlchemy       # ORM
EasyOCR          # Handwriting recognition
OpenAI Whisper   # Speech-to-text
Coqui TTS        # Text-to-speech
python-Levenshtein # Text similarity
pydub            # Audio processing
```

#### Frontend Stack
```
Streamlit        # Web interface
requests         # API communication
Pillow           # Image handling
streamlit-chat   # Chat components
```

## 🚀 Usage

### 📊 Dyslexia Screening Workflow

1. **Navigate to Screening Page**
   - Select "📊 Dyslexia Screening" from sidebar

2. **Provide Input Data** (any combination):
   - **Text Sample**: Type or paste reading material
   - **Handwriting Image**: Upload clear handwritten text (PNG/JPG)
   - **Audio Recording**: Upload reading audio (WAV/MP3)

3. **Run Analysis**
   - Click "🔍 Run Analysis"
   - Wait for AI processing (30-60 seconds)

4. **Review Results**
   - View confidence score and risk level
   - Explore detailed analysis sections
   - Read personalized recommendations

### 🔊 Text-to-Speech Generation

1. **Navigate to TTS Page**
   - Select "🔊 Text-to-Speech" from sidebar

2. **Configure Settings**
   - **Text Input**: Enter text to convert
   - **Reading Speed**: Adjust 0.5x - 2.0x
   - **Phonics Mode**: Enable for learning
   - **Language**: Select target language

3. **Generate Audio**
   - Click "🎵 Generate Audio"
   - Download or play generated audio file

### ⚙️ Admin Panel

**Access**: Use admin token `hackathon-admin-2024`

**Features**:
- View platform statistics
- Browse analysis sessions
- Clear session data
- Monitor system health

## 📊 API Documentation

### Core Endpoints

#### 🔍 Dyslexia Screening
```http
POST /api/v1/dyslexia/analyze
Content-Type: multipart/form-data

Parameters:
- text: string (optional)
- audio_file: file (optional)
- handwriting_image: file (optional)
- user_id: string (optional)

Response:
{
  "session_id": "string",
  "analysis_type": "multimodal",
  "confidence_score": 0.75,
  "risk_level": "moderate",
  "analysis": {
    "text_analysis": {...},
    "speech_analysis": {...},
    "ocr_analysis": {...}
  },
  "recommendations": ["string"],
  "screening_summary": "string",
  "processing_time": 2.3
}
```

#### 🔊 Text-to-Speech
```http
POST /api/v1/tts/synthesize
Content-Type: application/json

Body:
{
  "text": "Hello world",
  "speed": 1.0,
  "phonics_mode": false,
  "language": "en"
}

Response:
{
  "session_id": "string",
  "audio_file_path": "string", 
  "audio_duration": 5.2,
  "file_size": 102400,
  "settings_used": {...},
  "processing_time": 1.5
}
```

#### 🛡️ Admin Endpoints
```http
GET /admin/stats
Authorization: Bearer {admin_token}

GET /admin/sessions?limit=100
Authorization: Bearer {admin_token}

DELETE /admin/clear?confirm=true
Authorization: Bearer {admin_token}
```

### Error Handling
- **400**: Bad Request - Invalid input parameters
- **403**: Forbidden - Invalid admin token
- **500**: Internal Server Error - AI processing failed
- **timeout**: Request timeout after 60 seconds

## 🎯 Accessibility Features

### Visual Accessibility
- **OpenDyslexic Font**: Specialized typeface for dyslexic readers
- **High Contrast Colors**: Dark theme with bright accents
- **Large Text**: 16px+ base font size
- **Clear Spacing**: Generous margins and padding

### Interaction Accessibility
- **Keyboard Navigation**: Full keyboard support
- **Screen Reader Friendly**: Semantic HTML structure
- **Touch Friendly**: Large clickable areas (44px+)
- **Loading Indicators**: Clear progress feedback

### Content Accessibility
- **Simple Language**: Clear, concise instructions
- **Visual Hierarchy**: Logical heading structure
- **Error Messages**: Descriptive, actionable feedback
- **Help Text**: Contextual guidance throughout

## 🤖 AI/ML Pipeline Details

### 🔤 OCR Pipeline (EasyOCR)
```python
# Handwriting analysis workflow
1. Image preprocessing and enhancement
2. Text extraction with confidence scoring  
3. Letter reversal detection (b/d, p/q)
4. Writing clarity assessment
5. Recommendation generation
```

### 🎤 Speech-to-Text Pipeline (Whisper)
```python
# Audio analysis workflow
1. Audio file validation and preprocessing
2. Speech transcription using Whisper "small" model
3. Reading speed calculation (WPM)
4. Text comparison with expected content
5. Fluency assessment and scoring
```

### 📝 NLP Analysis Pipeline
```python
# Text pattern analysis
1. Word-level statistics (count, length, complexity)
2. Reversal pattern detection (was/saw, on/no)
3. Spelling error pattern identification
4. Levenshtein distance calculations
5. Confidence scoring based on indicators
```

### 🔊 TTS Pipeline (Coqui)
```python
# Audio generation workflow  
1. Text preprocessing and phonics enhancement
2. Voice synthesis using Tacotron2-DDC model
3. Speed adjustment via frame rate modification
4. Audio export and duration calculation
5. Quality optimization for accessibility
```

## 🗄️ Database Schema

### Sessions Table
```sql
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_data JSON NOT NULL,           -- Original input data
    analysis_result JSON NOT NULL,      -- Analysis output
    confidence_score FLOAT,             -- Screening confidence (0-1)
    recommendations JSON,               -- Generated recommendations  
    audio_file_path VARCHAR(500),       -- TTS output path
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Database Operations
- **Create**: Store analysis sessions
- **Read**: Fetch session history and statistics
- **Update**: Modify session metadata
- **Delete**: Admin cleanup operations

## 🌐 Deployment Options

### 🌟 Streamlit Cloud Deployment (Frontend-Only)

**Quick Deploy to Streamlit Cloud:**

1. **Push to GitHub**: Ensure your repository is on GitHub
2. **Visit Streamlit Cloud**: Go to [share.streamlit.io](https://share.streamlit.io)
3. **Connect Repository**: Link your GitHub repository
4. **Set Main File**: Use `streamlit_app.py` as the main file path
5. **Configure Secrets** (optional): Add API endpoints in secrets

**Required Files for Streamlit Cloud:**
```
streamlit_app.py              # Main app entry point
requirements-streamlit.txt    # Streamlit-specific dependencies
.streamlit/config.toml       # Streamlit configuration
packages.txt                 # System dependencies
```

**Secrets Configuration** (in Streamlit Cloud settings):
```toml
[general]
API_BASE_URL = "https://your-backend-api.herokuapp.com"
DEMO_MODE = "true"
```

**Demo Mode Features:**
- Fully functional frontend without backend dependency
- Simulated AI analysis results for demonstration
- All UI features and accessibility options working
- Perfect for showcasing the platform capabilities

### 🚂 Railway.app Deployment (Full Stack)
```yaml
# railway.toml
[build]
  builder = "NIXPACKS"
  buildCommand = "pip install -r backend/requirements.txt"

[deploy]
  startCommand = "uvicorn backend.main:app --host 0.0.0.0 --port $PORT"
  healthcheckPath = "/health"
  healthcheckTimeout = 300
  restartPolicyType = "ON_FAILURE"
```

### 🌟 Streamlit Cloud Configuration
```toml
# .streamlit/config.toml
[global]
developmentMode = false

[server]
headless = true
enableCORS = false
enableXsrfProtection = false
maxUploadSize = 50

[theme]
primaryColor = "#4CAF50"
backgroundColor = "#1e1e1e"
secondaryBackgroundColor = "#2e2e2e"
textColor = "#ffffff"
```

### 🐳 Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🧪 Testing

### Backend Tests
```bash
# Run API tests
cd backend
pytest tests/ -v

# Test individual components
pytest tests/test_pipelines.py::test_dyslexia_analysis
pytest tests/test_api.py::test_check_dyslexia_endpoint
```

### Frontend Tests
```bash
# Streamlit component testing
cd frontend  
streamlit run app.py --runner.headless true
```

### Integration Tests
```bash
# Full pipeline testing
python tests/integration_test.py
```

## 📈 Monitoring & Analytics

### Health Monitoring
- **Endpoint**: `GET /health`
- **Database connectivity**: SQLAlchemy connection pool
- **AI model status**: Pipeline initialization checks
- **File system**: Upload/output directory permissions

### Usage Analytics  
- **Session tracking**: All analysis sessions logged
- **Performance metrics**: Response times and success rates
- **Error tracking**: Failed requests with detailed logs
- **Admin dashboard**: Real-time platform statistics

### Logs Structure
```
logs/
├── app.log              # Application logs
├── error.log            # Error tracking  
├── access.log           # API access logs
└── pipeline.log         # AI pipeline logs
```

## 🤝 Contributing

### Development Setup
```bash
# Fork and clone repository
git clone https://github.com/your-username/dyslexiacare.git
cd dyslexiacare

# Create feature branch
git checkout -b feature/amazing-feature

# Install development dependencies
pip install -r requirements-dev.txt

# Run pre-commit hooks
pre-commit install
```

### Code Standards
- **Python**: PEP 8 compliance with Black formatting
- **API**: OpenAPI 3.0 documentation required
- **Frontend**: Component-based structure with clear naming
- **Documentation**: Docstrings for all functions and classes

### Pull Request Process
1. Update documentation for any new features
2. Add tests for new functionality
3. Ensure all tests pass locally
4. Update CHANGELOG.md with your changes
5. Submit PR with clear description and screenshots

## 📞 Support & Resources

### Getting Help
- **Issues**: GitHub Issues for bug reports
- **Discussions**: GitHub Discussions for questions
- **Documentation**: Full API docs at `/docs` endpoint
- **Email**: support@dyslexiacare.dev

### Learning Resources
- **Dyslexia Research**: Links to academic papers and studies
- **Accessibility Guidelines**: WCAG 2.1 compliance documentation  
- **AI/ML References**: Model documentation and training data sources
- **Development Guides**: Tutorials for extending the platform

---

## 📋 Recent Updates & Version History

### Version 2.0 - Mindpiece Rebrand (September 2025)
- **🎨 Brand Identity**: Complete rebrand to "MINDPIECE" with professional logo
- **🔤 OpenDyslexic Integration**: Full font implementation across entire application
- **🎨 UI Redesign**: Pale white text theme on dark background for optimal accessibility
- **🐛 Bug Fixes**: Fixed backend syntax errors and API validation issues
- **📱 Responsive Design**: Improved mobile and accessibility features

### Version 1.5 - Accessibility Focus
- **♿ WCAG Compliance**: High contrast themes and large UI elements
- **🔊 Enhanced TTS**: Multi-language support and phonics mode
- **🧠 AI Improvements**: Better dyslexia detection algorithms
- **📊 Analytics**: Comprehensive session tracking and admin panel

### Version 1.0 - Initial Release
- **🚀 MVP Launch**: Core dyslexia screening functionality
- **🤖 AI Pipeline**: OCR, STT, and NLP analysis integration
- **💾 Database**: SQLite-based session management
- **🌐 Web Interface**: Streamlit frontend with FastAPI backend

### Current Status (Live)
- **Backend**: ✅ Running on http://localhost:8000
- **Frontend**: ✅ Running on http://localhost:8502
- **Database**: ✅ SQLite operational with session tracking
- **AI Models**: ✅ All pipelines loaded and functional
- **Accessibility**: ✅ OpenDyslexic font and pale white theme active

---

## 🏆 Hackathon-Ready Features

### ✅ Complete Tech Stack
- ✅ Python-native (no JavaScript complexity)
- ✅ Offline AI models (no API dependencies)
- ✅ SQLite database (zero configuration)
- ✅ One-click setup scripts
- ✅ Comprehensive error handling

### ✅ Demo-Safe Design
- ✅ Admin backdoor for session management
- ✅ Mock data generation capabilities
- ✅ Robust fallback mechanisms
- ✅ Clear visual feedback for all operations
- ✅ Professional UI with accessibility focus

### ✅ Scalability Ready
- ✅ Async FastAPI for high concurrency
- ✅ Modular pipeline architecture
- ✅ Database ORM for easy scaling
- ✅ Docker/Railway deployment configs
- ✅ Monitoring and logging infrastructure

---

**Built with ❤️ for accessible learning and dyslexia awareness**

*This platform represents a comprehensive solution for dyslexia screening and accessibility, designed to be reliable, scalable, and impactful for hackathon presentations and real-world deployment.*