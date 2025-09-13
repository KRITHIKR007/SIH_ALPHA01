from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
import os
from datetime import datetime

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, engine
from database.models import Session as DBSession
from database import models
from pipelines.pipeline_connector import DyslexiaPipeline, TTSPipeline

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Dyslexia Screening & Accessibility API",
    description="AI-powered dyslexia screening and text-to-speech accessibility platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Admin token (in production, use proper authentication)
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "hackathon-admin-2024")

# Dependency for database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize pipelines
dyslexia_pipeline = DyslexiaPipeline()
tts_pipeline = TTSPipeline()

# Pydantic models
class DyslexiaAnalysisRequest(BaseModel):
    text: Optional[str] = None
    audio_file: Optional[str] = None
    handwriting_image: Optional[str] = None

class DyslexiaAnalysisResponse(BaseModel):
    session_id: str
    analysis: dict
    recommendations: List[str]
    confidence_score: float

class TTSRequest(BaseModel):
    text: str
    speed: Optional[float] = 1.0
    phonics_mode: Optional[bool] = False
    language: Optional[str] = "en"

class TTSResponse(BaseModel):
    audio_file_path: str
    duration: float
    settings_used: dict

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Dyslexia Screening API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Pipeline 1: Dyslexia Screening
@app.post("/check_dyslexia", response_model=DyslexiaAnalysisResponse)
async def check_dyslexia(
    text: Optional[str] = Form(None),
    audio_file: Optional[UploadFile] = File(None),
    handwriting_image: Optional[UploadFile] = File(None),
    db: SessionLocal = Depends(get_db)
):
    """
    Comprehensive dyslexia screening using multiple input modalities:
    - Text analysis for reading comprehension
    - Audio analysis for speech-to-text comparison
    - Handwriting analysis via OCR
    """
    try:
        # Save uploaded files if provided
        audio_path = None
        image_path = None
        
        if audio_file:
            audio_path = f"uploads/audio_{datetime.now().timestamp()}_{audio_file.filename}"
            os.makedirs("uploads", exist_ok=True)
            with open(audio_path, "wb") as f:
                f.write(await audio_file.read())
        
        if handwriting_image:
            image_path = f"uploads/image_{datetime.now().timestamp()}_{handwriting_image.filename}"
            os.makedirs("uploads", exist_ok=True)
            with open(image_path, "wb") as f:
                f.write(await handwriting_image.read())
        
        # Run dyslexia analysis pipeline
        analysis_result = await dyslexia_pipeline.analyze(
            text=text,
            audio_file_path=audio_path,
            image_file_path=image_path
        )
        
        # Save session to database
        db_session = DBSession(
            input_data={
                "text": text,
                "audio_file": audio_path,
                "image_file": image_path
            },
            analysis_result=analysis_result["analysis"],
            confidence_score=analysis_result["confidence_score"],
            recommendations=analysis_result["recommendations"],
            timestamp=datetime.now()
        )
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        
        return DyslexiaAnalysisResponse(
            session_id=str(db_session.id),
            analysis=analysis_result["analysis"],
            recommendations=analysis_result["recommendations"],
            confidence_score=analysis_result["confidence_score"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# Pipeline 2: Text-to-Speech
@app.post("/tts", response_model=TTSResponse)
async def text_to_speech(
    request: TTSRequest,
    db: SessionLocal = Depends(get_db)
):
    """
    Generate accessibility-focused text-to-speech audio with options for:
    - Adjustable speech speed
    - Phonics mode for learning
    - Multiple language support
    """
    try:
        # Generate TTS audio
        tts_result = await tts_pipeline.synthesize(
            text=request.text,
            speed=request.speed,
            phonics_mode=request.phonics_mode,
            language=request.language
        )
        
        # Log TTS session
        db_session = DBSession(
            input_data={
                "text": request.text,
                "tts_settings": {
                    "speed": request.speed,
                    "phonics_mode": request.phonics_mode,
                    "language": request.language
                }
            },
            analysis_result={"tts_generated": True},
            audio_file_path=tts_result["audio_file_path"],
            timestamp=datetime.now()
        )
        db.add(db_session)
        db.commit()
        
        return TTSResponse(
            audio_file_path=tts_result["audio_file_path"],
            duration=tts_result["duration"],
            settings_used={
                "speed": request.speed,
                "phonics_mode": request.phonics_mode,
                "language": request.language
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")

# Admin endpoints (protected)
def verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid admin token")
    return credentials

@app.get("/admin/sessions")
async def get_all_sessions(
    limit: int = 100,
    credentials: HTTPAuthorizationCredentials = Depends(verify_admin_token),
    db: SessionLocal = Depends(get_db)
):
    """Get all analysis sessions (admin only)"""
    sessions = db.query(DBSession).order_by(DBSession.timestamp.desc()).limit(limit).all()
    return {
        "sessions": [
            {
                "id": session.id,
                "timestamp": session.timestamp.isoformat(),
                "input_data": session.input_data,
                "analysis_result": session.analysis_result,
                "confidence_score": session.confidence_score,
                "recommendations": session.recommendations
            }
            for session in sessions
        ],
        "total": len(sessions)
    }

@app.delete("/admin/clear")
async def clear_sessions(
    confirm: bool = False,
    credentials: HTTPAuthorizationCredentials = Depends(verify_admin_token),
    db: SessionLocal = Depends(get_db)
):
    """Clear all sessions (admin only)"""
    if not confirm:
        raise HTTPException(status_code=400, detail="Must confirm deletion with confirm=true")
    
    deleted_count = db.query(DBSession).count()
    db.query(DBSession).delete()
    db.commit()
    
    return {"message": f"Cleared {deleted_count} sessions"}

@app.get("/admin/stats")
async def get_statistics(
    credentials: HTTPAuthorizationCredentials = Depends(verify_admin_token),
    db: SessionLocal = Depends(get_db)
):
    """Get platform statistics (admin only)"""
    total_sessions = db.query(DBSession).count()
    avg_confidence = db.query(DBSession).filter(DBSession.confidence_score.isnot(None)).all()
    
    return {
        "total_sessions": total_sessions,
        "average_confidence_score": sum(s.confidence_score for s in avg_confidence if s.confidence_score) / len(avg_confidence) if avg_confidence else 0,
        "sessions_today": db.query(DBSession).filter(
            DBSession.timestamp >= datetime.now().date()
        ).count()
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )