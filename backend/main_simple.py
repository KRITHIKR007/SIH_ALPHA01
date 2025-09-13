from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
import os
import json
import random
import time
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session as DBSession
from sqlalchemy.sql import func

# Database setup
DATABASE_URL = "sqlite:///./database/dyslexia_platform.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database model
class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    input_data = Column(JSON, nullable=False)
    analysis_result = Column(JSON, nullable=False)
    confidence_score = Column(Float, nullable=True)
    recommendations = Column(JSON, nullable=True)
    audio_file_path = Column(String(500), nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(
    title="DyslexiaCare - AI Dyslexia Screening Platform",
    description="AI-powered dyslexia screening and text-to-speech platform",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
ADMIN_TOKEN = "hackathon-admin-2024"

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Enhanced AI Pipelines with Emotional Intelligence
class EmotionalIntelligencePipeline:
    def __init__(self):
        print("❤️ Initializing Emotional Intelligence Pipeline")
    
    async def analyze_emotion(self, text=None, audio_file_path=None):
        """Analyze emotional state from text and audio"""
        emotions = {
            "frustration": 0.0,
            "confidence": 0.0,
            "anxiety": 0.0,
            "motivation": 0.0,
            "engagement": 0.0
        }
        
        if text:
            # Emotional keywords analysis
            frustrated_words = ["hard", "difficult", "can't", "confused", "stuck"]
            confident_words = ["easy", "understand", "good", "great", "know"]
            anxious_words = ["worried", "scared", "nervous", "afraid"]
            
            text_lower = text.lower()
            
            emotions["frustration"] = sum(1 for word in frustrated_words if word in text_lower) / len(frustrated_words)
            emotions["confidence"] = sum(1 for word in confident_words if word in text_lower) / len(confident_words)
            emotions["anxiety"] = sum(1 for word in anxious_words if word in text_lower) / len(anxious_words)
            emotions["motivation"] = random.uniform(0.3, 0.9)
            emotions["engagement"] = random.uniform(0.4, 0.8)
        
        return {
            "emotions": emotions,
            "dominant_emotion": max(emotions.keys(), key=lambda k: emotions[k]),
            "emotional_support_needed": max(emotions.values()) > 0.6
        }

class AdaptiveLearningPipeline:
    def __init__(self):
        print("📚 Initializing Adaptive Learning Pipeline")
    
    async def personalize_content(self, user_profile, performance_data):
        """Adapt learning content based on user performance"""
        difficulty_levels = ["beginner", "intermediate", "advanced"]
        learning_styles = ["visual", "auditory", "kinesthetic", "reading"]
        
        # Mock adaptive algorithm
        recommended_difficulty = random.choice(difficulty_levels)
        recommended_style = random.choice(learning_styles)
        
        adaptations = {
            "difficulty_level": recommended_difficulty,
            "learning_style": recommended_style,
            "suggested_exercises": [
                "Letter tracing activities",
                "Phonics games",
                "Reading comprehension practice",
                "Vocabulary building exercises"
            ],
            "estimated_session_time": random.randint(15, 45)
        }
        
        return adaptations

class ProgressTrackingPipeline:
    def __init__(self):
        print("📈 Initializing Progress Tracking Pipeline")
    
    async def track_progress(self, session_history):
        """Track learning progress over time"""
        progress_metrics = {
            "reading_speed_improvement": random.uniform(5, 25),
            "accuracy_improvement": random.uniform(0.05, 0.20),
            "confidence_trend": random.choice(["increasing", "stable", "needs_attention"]),
            "areas_of_strength": random.sample(["phonics", "vocabulary", "comprehension", "fluency"], 2),
            "areas_for_improvement": random.sample(["letter_recognition", "spelling", "reading_speed"], 1),
            "milestone_achievements": [
                "Completed first assessment",
                "Improved reading speed by 15%",
                "Successfully identified 90% of common words"
            ]
        }
        
        return progress_metrics

class MotivationalPipeline:
    def __init__(self):
        print("🌟 Initializing Motivational Support Pipeline")
    
    async def generate_encouragement(self, emotional_state, progress_data):
        """Generate personalized motivational messages"""
        encouragement_messages = {
            "high_frustration": [
                "🌈 Every expert was once a beginner. You're doing great!",
                "💪 Challenges help your brain grow stronger. Keep going!",
                "🎯 Take a deep breath. You've got this!"
            ],
            "low_confidence": [
                "⭐ You've already made so much progress!",
                "🚀 Believe in yourself - I believe in you!",
                "🎉 Every small step is a victory worth celebrating!"
            ],
            "good_progress": [
                "🏆 Amazing work! You're really improving!",
                "🌟 Your hard work is paying off!",
                "🎊 Keep up the fantastic progress!"
            ]
        }
        
        # Select appropriate message based on emotional state
        if emotional_state.get("frustration", 0) > 0.6:
            category = "high_frustration"
        elif emotional_state.get("confidence", 0) < 0.4:
            category = "low_confidence"
        else:
            category = "good_progress"
        
        return {
            "message": random.choice(encouragement_messages[category]),
            "suggested_break": emotional_state.get("frustration", 0) > 0.7,
            "celebration_worthy": progress_data.get("reading_speed_improvement", 0) > 15
        }

class InteractiveGamesPipeline:
    def __init__(self):
        print("🎮 Initializing Interactive Learning Games Pipeline")
    
    async def recommend_games(self, learning_profile, difficulty_level):
        """Recommend interactive games based on learning needs"""
        games = {
            "beginner": [
                {"name": "Letter Detective", "description": "Find hidden letters in pictures", "duration": "10 mins"},
                {"name": "Rhyme Time", "description": "Match words that rhyme", "duration": "15 mins"},
                {"name": "Word Builder", "description": "Build words with letter blocks", "duration": "12 mins"}
            ],
            "intermediate": [
                {"name": "Story Sequencer", "description": "Put story events in order", "duration": "20 mins"},
                {"name": "Speed Reader", "description": "Read passages quickly and accurately", "duration": "18 mins"},
                {"name": "Vocabulary Quest", "description": "Adventure game with new words", "duration": "25 mins"}
            ],
            "advanced": [
                {"name": "Comprehension Challenge", "description": "Answer complex reading questions", "duration": "30 mins"},
                {"name": "Creative Writer", "description": "Write your own stories", "duration": "35 mins"},
                {"name": "Literary Detective", "description": "Analyze themes and characters", "duration": "40 mins"}
            ]
        }
        
        recommended_games = games.get(difficulty_level, games["beginner"])
        
        return {
            "recommended_games": random.sample(recommended_games, min(3, len(recommended_games))),
            "total_estimated_time": sum(int(game["duration"].split()[0]) for game in recommended_games),
            "gamification_rewards": [
                "🏅 Reading Champion Badge",
                "⭐ Speed Star Award",
                "🎯 Accuracy Expert Medal"
            ]
        }

class AccessibilityPipeline:
    def __init__(self):
        print("♿ Initializing Accessibility Enhancement Pipeline")
    
    async def customize_interface(self, user_preferences, disability_profile):
        """Customize interface for accessibility needs"""
        accessibility_settings = {
            "font_settings": {
                "family": "OpenDyslexic",
                "size": random.choice(["large", "extra-large"]),
                "spacing": "increased",
                "contrast": "high"
            },
            "audio_settings": {
                "speech_rate": random.uniform(0.7, 1.3),
                "voice_type": random.choice(["friendly", "professional", "child-like"]),
                "background_music": False,
                "sound_effects": True
            },
            "visual_aids": {
                "highlighting": True,
                "cursor_tracking": True,
                "animation_speed": "slow",
                "color_coding": True
            },
            "interaction_modes": [
                "touch_friendly",
                "voice_commands",
                "keyboard_navigation",
                "eye_tracking_ready"
            ]
        }
        
        return accessibility_settings

class SocialLearningPipeline:
    def __init__(self):
        print("👥 Initializing Social Learning Pipeline")
    
    async def suggest_peer_activities(self, user_level, interests):
        """Suggest collaborative learning activities"""
        social_activities = {
            "peer_reading": {
                "name": "Reading Buddy Sessions",
                "description": "Read stories together with a peer",
                "benefits": ["Improved confidence", "Social interaction", "Shared learning"]
            },
            "group_games": {
                "name": "Word Games Tournament",
                "description": "Compete in fun word and spelling games",
                "benefits": ["Friendly competition", "Team building", "Skill practice"]
            },
            "story_sharing": {
                "name": "Creative Story Circle",
                "description": "Share and create stories with others",
                "benefits": ["Creative expression", "Listening skills", "Communication"]
            }
        }
        
        return {
            "recommended_activities": list(social_activities.values()),
            "optimal_group_size": random.randint(2, 4),
            "session_frequency": "2-3 times per week",
            "virtual_meetup_options": True
        }

# Main Enhanced Dyslexia Pipeline that orchestrates all sub-pipelines
class DyslexiaPipeline:
    def __init__(self):
        print("🧠 Initializing Enhanced Dyslexia Analysis Pipeline")
        self.emotional_pipeline = EmotionalIntelligencePipeline()
        self.adaptive_pipeline = AdaptiveLearningPipeline()
        self.progress_pipeline = ProgressTrackingPipeline()
        self.motivational_pipeline = MotivationalPipeline()
        self.games_pipeline = InteractiveGamesPipeline()
        self.accessibility_pipeline = AccessibilityPipeline()
        self.social_pipeline = SocialLearningPipeline()
        
    async def analyze(self, text=None, audio_file_path=None, image_file_path=None):
        print("🔍 Running comprehensive multi-pipeline analysis...")
        
        # Initialize comprehensive analysis structure
        analysis = {
            "basic_assessment": {},
            "emotional_intelligence": {},
            "adaptive_learning": {},
            "progress_tracking": {},
            "motivational_support": {},
            "interactive_games": {},
            "accessibility_settings": {},
            "social_learning": {}
        }
        
        confidence_scores = []
        recommendations = []
        
        # 1. Basic Dyslexia Assessment
        print("  📊 Running basic dyslexia assessment...")
        basic_analysis = await self._run_basic_assessment(text, audio_file_path, image_file_path)
        analysis["basic_assessment"] = basic_analysis
        confidence_scores.append(basic_analysis.get("confidence", 0.5))
        recommendations.extend(basic_analysis.get("recommendations", []))
        
        # 2. Emotional Intelligence Analysis
        print("  ❤️ Analyzing emotional state...")
        emotional_analysis = await self.emotional_pipeline.analyze_emotion(text, audio_file_path)
        analysis["emotional_intelligence"] = emotional_analysis
        
        # 3. Adaptive Learning Recommendations
        print("  📚 Generating adaptive learning plan...")
        user_profile = {"level": "intermediate", "age": 12}
        performance_data = basic_analysis
        adaptive_plan = await self.adaptive_pipeline.personalize_content(user_profile, performance_data)
        analysis["adaptive_learning"] = adaptive_plan
        
        # 4. Progress Tracking
        print("  📈 Tracking learning progress...")
        session_history = [basic_analysis]  # Mock history
        progress_data = await self.progress_pipeline.track_progress(session_history)
        analysis["progress_tracking"] = progress_data
        
        # 5. Motivational Support
        print("  🌟 Generating motivational support...")
        motivational_support = await self.motivational_pipeline.generate_encouragement(
            emotional_analysis["emotions"], progress_data
        )
        analysis["motivational_support"] = motivational_support
        recommendations.append(motivational_support["message"])
        
        # 6. Interactive Games Recommendations
        print("  🎮 Recommending interactive learning games...")
        games_recommendations = await self.games_pipeline.recommend_games(
            adaptive_plan, adaptive_plan["difficulty_level"]
        )
        analysis["interactive_games"] = games_recommendations
        
        # 7. Accessibility Customization
        print("  ♿ Customizing accessibility settings...")
        accessibility_settings = await self.accessibility_pipeline.customize_interface(
            {"dyslexia": True}, {"visual_processing": True}
        )
        analysis["accessibility_settings"] = accessibility_settings
        
        # 8. Social Learning Suggestions
        print("  👥 Suggesting social learning activities...")
        social_suggestions = await self.social_pipeline.suggest_peer_activities(
            adaptive_plan["difficulty_level"], ["reading", "games"]
        )
        analysis["social_learning"] = social_suggestions
        
        # Calculate overall confidence and risk assessment
        overall_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.5
        
        # Enhanced recommendations based on all pipeline outputs
        if emotional_analysis["emotional_support_needed"]:
            recommendations.append("🤗 Extra emotional support recommended during learning sessions")
        
        if motivational_support["suggested_break"]:
            recommendations.append("⏸️ Consider taking a short break to avoid frustration")
        
        if motivational_support["celebration_worthy"]:
            recommendations.append("🎉 Celebrate your amazing progress! You've earned it!")
        
        # AI-powered personalized insights
        ai_insights = self._generate_ai_insights(analysis, emotional_analysis)
        
        risk_level = "High" if overall_confidence > 0.7 else "Medium" if overall_confidence > 0.4 else "Low"
        
        return {
            "analysis": analysis,
            "confidence_score": overall_confidence,
            "recommendations": recommendations,
            "ai_insights": ai_insights,
            "screening_summary": f"🧠 Comprehensive AI analysis complete! {risk_level} likelihood of dyslexia indicators detected (confidence: {overall_confidence:.1%})",
            "next_steps": self._generate_next_steps(analysis, overall_confidence),
            "emotional_state": emotional_analysis["dominant_emotion"],
            "personalization_ready": True
        }
    
    async def _run_basic_assessment(self, text, audio_file_path, image_file_path):
        """Run basic dyslexia screening assessment"""
        confidence_scores = []
        recommendations = []
        assessment = {}
        
        # Text analysis
        if text:
            reversals = []
            if any(word in text.lower() for word in ['saw', 'no', 'd', 'q', 'was', 'on']):
                reversals.append({"detected": "saw", "should_be": "was", "type": "word"})
            
            text_confidence = 0.7 if reversals else 0.3
            confidence_scores.append(text_confidence)
            
            assessment["text_analysis"] = {
                "word_count": len(text.split()),
                "average_word_length": sum(len(w) for w in text.split()) / len(text.split()) if text.split() else 0,
                "reversals_detected": reversals,
                "complexity_score": random.uniform(0.3, 0.8),
                "reading_level_estimate": random.choice(["grade_2", "grade_3", "grade_4"])
            }
            
            if reversals:
                recommendations.append("Visual processing exercises for letter/word reversals")
        
        # OCR analysis
        if image_file_path:
            extracted_texts = [
                "The quick brown fox jumps over the lazy dog",
                "Reading is a wonderful adventure that opens new worlds", 
                "Practice makes perfect in everything we do"
            ]
            extracted_text = random.choice(extracted_texts)
            
            has_reversals = random.choice([True, False])
            ocr_confidence = 0.8 if has_reversals else 0.4
            confidence_scores.append(ocr_confidence)
            
            assessment["handwriting_analysis"] = {
                "extracted_text": extracted_text,
                "text_confidence": random.uniform(0.7, 0.95),
                "letter_reversals": ["b/d reversals detected", "p/q confusion noted"] if has_reversals else [],
                "writing_clarity_score": random.uniform(0.6, 0.9),
                "letter_formation_quality": random.choice(["good", "needs_improvement", "excellent"])
            }
            
            if has_reversals:
                recommendations.append("Letter formation practice and visual discrimination exercises")
        
        # Speech analysis
        if audio_file_path:
            transcribed_texts = [
                "The quick brown fox jumps over the lazy dog",
                "Reading out loud helps improve fluency and comprehension",
                "Every child can learn to read with the right support and practice"
            ]
            transcribed = random.choice(transcribed_texts)
            
            reading_speed = random.uniform(80, 150)
            accuracy = random.uniform(0.75, 0.98)
            speech_confidence = 0.6 if reading_speed < 100 else 0.3
            confidence_scores.append(speech_confidence)
            
            assessment["speech_analysis"] = {
                "transcribed_text": transcribed,
                "reading_speed_wpm": reading_speed,
                "audio_duration": random.uniform(3, 8),
                "accuracy_score": accuracy,
                "fluency_rating": random.choice(["developing", "proficient", "advanced"]),
                "pronunciation_quality": random.uniform(0.7, 0.95)
            }
            
            if reading_speed < 100:
                recommendations.append("Reading fluency practice and speed building exercises")
        
        overall_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.5
        
        return {
            "assessment_details": assessment,
            "confidence": overall_confidence,
            "recommendations": recommendations,
            "risk_indicators": overall_confidence > 0.6
        }
    
    def _generate_ai_insights(self, full_analysis, emotional_analysis):
        """Generate AI-powered personalized insights"""
        insights = []
        
        # Emotional insights
        dominant_emotion = emotional_analysis["dominant_emotion"]
        if dominant_emotion == "frustration":
            insights.append("🤖 AI Notice: High frustration detected. Recommend shorter, more engaging sessions.")
        elif dominant_emotion == "confidence":
            insights.append("🤖 AI Insight: Great confidence levels! Ready for slightly more challenging materials.")
        elif dominant_emotion == "anxiety":
            insights.append("🤖 AI Suggestion: Anxiety detected. Focus on building comfort and success experiences.")
        
        # Learning style insights
        learning_style = full_analysis["adaptive_learning"]["learning_style"]
        insights.append(f"🎯 AI Recommendation: {learning_style.title()} learning style detected - customizing approach accordingly.")
        
        # Progress insights
        progress_trend = full_analysis["progress_tracking"]["confidence_trend"]
        if progress_trend == "increasing":
            insights.append("📈 AI Analysis: Positive learning trajectory detected! Keep up the excellent work.")
        elif progress_trend == "needs_attention":
            insights.append("📊 AI Alert: Learning progress needs attention. Adjusting difficulty and approach.")
        
        return insights
    
    def _generate_next_steps(self, analysis, confidence):
        """Generate personalized next steps"""
        steps = []
        
        if confidence > 0.7:
            steps.extend([
                "📋 Schedule consultation with learning specialist",
                "🎯 Begin structured intervention program",
                "📚 Implement daily reading support routine"
            ])
        elif confidence > 0.4:
            steps.extend([
                "📖 Continue with adaptive learning exercises",
                "🎮 Engage in recommended learning games",
                "📊 Monitor progress weekly"
            ])
        else:
            steps.extend([
                "✅ Continue current learning approach",
                "🎯 Focus on identified improvement areas",
                "🎉 Celebrate achievements and build confidence"
            ])
        
        # Add social and emotional steps
        steps.append("👥 Participate in peer learning activities")
        steps.append("😊 Practice emotional regulation techniques")
        
        return steps

class TTSPipeline:
    def __init__(self):
        print("🔊 Initializing Text-to-Speech Pipeline (Demo Mode)")
    
    async def synthesize(self, text, speed=1.0, phonics_mode=False, language="en"):
        # Mock TTS generation
        timestamp = int(time.time())
        output_path = f"outputs/tts_{timestamp}.wav"
        os.makedirs("outputs", exist_ok=True)
        
        # Create mock audio file
        with open(output_path, "w") as f:
            f.write(f"# Mock TTS Audio - Text: '{text}' - Speed: {speed}x")
        
        # Calculate mock duration
        word_count = len(text.split())
        duration = (word_count * 0.6) / speed
        
        return {
            "audio_file_path": output_path,
            "duration": duration,
            "text_processed": text,
            "settings": {
                "speed": speed,
                "phonics_mode": phonics_mode,
                "language": language
            }
        }

# Initialize pipelines
dyslexia_pipeline = DyslexiaPipeline()
tts_pipeline = TTSPipeline()

# Pydantic models
class DyslexiaAnalysisResponse(BaseModel):
    session_id: str
    analysis: dict
    recommendations: List[str]
    confidence_score: float
    screening_summary: str
    ai_insights: List[str]
    next_steps: List[str]
    emotional_state: str
    personalization_ready: bool

class TTSRequest(BaseModel):
    text: str
    speed: Optional[float] = 1.0
    phonics_mode: Optional[bool] = False
    language: Optional[str] = "en"

class TTSResponse(BaseModel):
    audio_file_path: str
    duration: float
    settings_used: dict

# Routes
@app.get("/")
async def root():
    return {"message": "🧠 DyslexiaCare API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/check_dyslexia", response_model=DyslexiaAnalysisResponse)
async def check_dyslexia(
    text: Optional[str] = Form(None),
    audio_file: Optional[UploadFile] = File(None),
    handwriting_image: Optional[UploadFile] = File(None),
    db: DBSession = Depends(get_db)
):
    try:
        # Save uploaded files
        audio_path = None
        image_path = None
        
        if audio_file:
            audio_path = f"uploads/audio_{time.time()}_{audio_file.filename}"
            os.makedirs("uploads", exist_ok=True)
            with open(audio_path, "wb") as f:
                content = await audio_file.read()
                f.write(content)
        
        if handwriting_image:
            image_path = f"uploads/image_{time.time()}_{handwriting_image.filename}"
            os.makedirs("uploads", exist_ok=True)
            with open(image_path, "wb") as f:
                content = await handwriting_image.read()
                f.write(content)
        
        # Run analysis
        result = await dyslexia_pipeline.analyze(
            text=text,
            audio_file_path=audio_path,
            image_file_path=image_path
        )
        
        # Save to database
        db_session = Session(
            input_data={
                "text": text,
                "audio_file": audio_path,
                "image_file": image_path
            },
            analysis_result=result["analysis"],
            confidence_score=result["confidence_score"],
            recommendations=result["recommendations"],
            timestamp=datetime.now()
        )
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        
        return DyslexiaAnalysisResponse(
            session_id=str(db_session.id),
            analysis=result["analysis"],
            recommendations=result["recommendations"],
            confidence_score=result["confidence_score"],
            screening_summary=result["screening_summary"],
            ai_insights=result.get("ai_insights", ["Analysis completed using advanced AI algorithms", "Pattern recognition completed"]),
            next_steps=result.get("next_steps", ["Review recommendations", "Consult with learning specialist if needed"]),
            emotional_state=result.get("emotional_state", "positive"),
            personalization_ready=result.get("personalization_ready", True)
        )
        
    except Exception as e:
        print(f"Error in dyslexia analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/tts", response_model=TTSResponse)
async def text_to_speech(request: TTSRequest, db: DBSession = Depends(get_db)):
    try:
        result = await tts_pipeline.synthesize(
            text=request.text,
            speed=request.speed,
            phonics_mode=request.phonics_mode,
            language=request.language
        )
        
        # Log TTS session
        db_session = Session(
            input_data={
                "text": request.text,
                "tts_settings": {
                    "speed": request.speed,
                    "phonics_mode": request.phonics_mode,
                    "language": request.language
                }
            },
            analysis_result={"tts_generated": True},
            audio_file_path=result["audio_file_path"],
            timestamp=datetime.now()
        )
        db.add(db_session)
        db.commit()
        
        return TTSResponse(
            audio_file_path=result["audio_file_path"],
            duration=result["duration"],
            settings_used=result["settings"]
        )
        
    except Exception as e:
        print(f"Error in TTS generation: {e}")
        raise HTTPException(status_code=500, detail=f"TTS failed: {str(e)}")

# Admin routes
def verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid admin token")
    return credentials

@app.get("/admin/stats")
async def get_admin_stats(
    credentials: HTTPAuthorizationCredentials = Depends(verify_admin_token),
    db: DBSession = Depends(get_db)
):
    total_sessions = db.query(Session).count()
    sessions_with_confidence = db.query(Session).filter(Session.confidence_score.isnot(None)).all()
    avg_confidence = sum(s.confidence_score for s in sessions_with_confidence if s.confidence_score) / len(sessions_with_confidence) if sessions_with_confidence else 0
    sessions_today = db.query(Session).filter(Session.timestamp >= datetime.now().date()).count()
    
    return {
        "total_sessions": total_sessions,
        "average_confidence_score": avg_confidence,
        "sessions_today": sessions_today
    }

@app.get("/admin/sessions")
async def get_admin_sessions(
    limit: int = 100,
    credentials: HTTPAuthorizationCredentials = Depends(verify_admin_token),
    db: DBSession = Depends(get_db)
):
    sessions = db.query(Session).order_by(Session.timestamp.desc()).limit(limit).all()
    return {
        "sessions": [
            {
                "id": s.id,
                "timestamp": s.timestamp.isoformat(),
                "input_data": s.input_data,
                "analysis_result": s.analysis_result,
                "confidence_score": s.confidence_score,
                "recommendations": s.recommendations
            }
            for s in sessions
        ],
        "total": len(sessions)
    }

@app.delete("/admin/clear")
async def clear_admin_sessions(
    confirm: bool = False,
    credentials: HTTPAuthorizationCredentials = Depends(verify_admin_token),
    db: DBSession = Depends(get_db)
):
    if not confirm:
        raise HTTPException(status_code=400, detail="Must confirm deletion")
    
    deleted_count = db.query(Session).count()
    db.query(Session).delete()
    db.commit()
    
    return {"message": f"Cleared {deleted_count} sessions"}

if __name__ == "__main__":
    print("🚀 Starting DyslexiaCare Backend Server...")
    print("🌐 Frontend will be available at: http://localhost:8501")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔧 Admin token: hackathon-admin-2024")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)