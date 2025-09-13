"""
Text-to-Speech API routes.
"""

import time
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models.schemas import TTSRequest, TTSResponse, CapabilitiesResponse, LanguageSupport
from ..dependencies import get_database
from ...database.models import TTSSession
from ...pipelines import TTSPipeline
from ...shared.utils import generate_session_id
from ...shared.exceptions import TTSError
from ...shared.constants import MAX_TEXT_SIZE, SUPPORTED_IMAGE_TYPES, SUPPORTED_AUDIO_TYPES
from config import get_settings

settings = get_settings()
router = APIRouter(prefix="/tts", tags=["Text-to-Speech"])

# Initialize TTS pipeline
tts_pipeline = TTSPipeline()


@router.post("/synthesize", response_model=TTSResponse)
async def synthesize_speech(
    request: TTSRequest,
    db: Session = Depends(get_database)
):
    """
    Generate text-to-speech audio with accessibility features:
    - Adjustable reading speeds (0.5x to 2.0x)
    - Phonics mode for syllable-based pronunciation
    - Multiple language support
    - High-quality audio optimized for dyslexia support
    """
    try:
        # Validate text length
        if len(request.text) > 10000:
            raise HTTPException(
                status_code=400,
                detail="Text too long. Maximum 10,000 characters allowed."
            )
        
        # Prepare input data
        input_data = {
            "text": request.text,
            "speed": request.speed,
            "phonics_mode": request.phonics_mode,
            "language": request.language,
            "output_dir": settings.get_output_path()
        }
        
        # Process TTS synthesis
        start_time = time.time()
        result = await tts_pipeline.analyze_with_timing(input_data)
        processing_time = time.time() - start_time
        
        # Save to database
        session_record = TTSSession(
            session_id=result["session_id"],
            input_text=request.text,
            language=request.language,
            speed=request.speed,
            phonics_mode=request.phonics_mode,
            audio_file_path=result["audio_file_path"],
            audio_duration=result["audio_duration"],
            file_size=result["file_size"],
            processing_time=processing_time,
            model_used=result["settings"]["voice_model"]
        )
        
        db.add(session_record)
        db.commit()
        db.refresh(session_record)
        
        return TTSResponse(
            session_id=result["session_id"],
            audio_file_path=result["audio_file_path"],
            audio_duration=result["audio_duration"],
            file_size=result["file_size"],
            settings_used=result["settings"],
            processing_time=processing_time
        )
        
    except TTSError as e:
        raise HTTPException(status_code=500, detail=f"TTS synthesis failed: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@router.post("/adjust-speed")
async def adjust_audio_speed(
    file_path: str,
    new_speed: float,
    db: Session = Depends(get_database)
):
    """Adjust the speed of existing audio file."""
    try:
        if not (0.5 <= new_speed <= 2.0):
            raise HTTPException(
                status_code=400,
                detail="Speed must be between 0.5 and 2.0"
            )
        
        result = await tts_pipeline.adjust_existing_audio(file_path, new_speed)
        
        return {
            "message": "Audio speed adjusted successfully",
            "original_file": result["original_file"],
            "adjusted_file": result["adjusted_file"],
            "speed_adjustment": result["speed_adjustment"],
            "new_duration": result["new_duration"]
        }
        
    except TTSError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@router.get("/capabilities", response_model=CapabilitiesResponse)
async def get_tts_capabilities():
    """Get TTS service capabilities and supported features."""
    try:
        supported_languages = []
        language_info = tts_pipeline.get_supported_languages()
        
        for code, name in language_info.items():
            supported_languages.append(LanguageSupport(
                code=code,
                name=name,
                tts_supported=True
            ))
        
        return CapabilitiesResponse(
            supported_languages=supported_languages,
            supported_speeds=tts_pipeline.get_supported_speeds(),
            max_file_sizes={
                "text": MAX_TEXT_SIZE,
                "audio": 50 * 1024 * 1024,  # 50MB
                "image": 10 * 1024 * 1024   # 10MB
            },
            supported_formats={
                "audio": list(SUPPORTED_AUDIO_TYPES),
                "image": list(SUPPORTED_IMAGE_TYPES)
            },
            features=[
                "Adjustable reading speeds",
                "Phonics mode",
                "Multi-language support",
                "High-quality audio",
                "Accessibility optimizations",
                "Syllable-based pronunciation",
                "Speed adjustment"
            ]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get capabilities: {e}")


@router.get("/session/{session_id}")
async def get_tts_session(
    session_id: str,
    db: Session = Depends(get_database)
):
    """Retrieve TTS session by ID."""
    session = db.query(TTSSession).filter(
        TTSSession.session_id == session_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="TTS session not found")
    
    return session.to_dict()


@router.get("/sessions")
async def list_tts_sessions(
    limit: int = 50,
    offset: int = 0,
    language: Optional[str] = None,
    db: Session = Depends(get_database)
):
    """List TTS sessions with optional filtering."""
    query = db.query(TTSSession)
    
    if language:
        query = query.filter(TTSSession.language == language)
    
    sessions = query.offset(offset).limit(limit).all()
    return [session.to_dict() for session in sessions]