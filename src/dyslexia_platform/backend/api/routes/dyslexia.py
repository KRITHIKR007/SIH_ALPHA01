"""
Dyslexia analysis API routes.
"""

import os
import time
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from ..models.schemas import DyslexiaAnalysisRequest, DyslexiaAnalysisResponse
from ..dependencies import get_database
from ...database.models import AnalysisSession
from ...pipelines import DyslexiaAnalysisPipeline
from ...shared.utils import generate_session_id, validate_image_file, validate_audio_file
from ...shared.exceptions import AnalysisError, ValidationError
from config import get_settings

settings = get_settings()
router = APIRouter(prefix="/dyslexia", tags=["Dyslexia Analysis"])

# Initialize pipeline
dyslexia_pipeline = DyslexiaAnalysisPipeline()


@router.post("/analyze", response_model=DyslexiaAnalysisResponse)
async def analyze_dyslexia(
    text: Optional[str] = Form(None),
    audio_file: Optional[UploadFile] = File(None),
    handwriting_image: Optional[UploadFile] = File(None),
    user_id: Optional[str] = Form(None),
    db: Session = Depends(get_database)
):
    """
    Comprehensive dyslexia screening using multiple input modalities:
    - Text analysis for reading comprehension patterns
    - Audio analysis for speech-to-text fluency assessment  
    - Handwriting analysis via OCR for visual processing patterns
    """
    try:
        # Validate inputs
        if not text and not audio_file and not handwriting_image:
            raise HTTPException(
                status_code=400,
                detail="At least one input (text, audio, or handwriting image) is required"
            )
        
        # Prepare input data
        input_data = {}
        file_paths = {}
        
        # Handle text input
        if text and text.strip():
            input_data["text"] = text.strip()
        
        # Handle audio file upload
        if audio_file:
            audio_path = await _save_uploaded_file(
                audio_file, settings.get_upload_path(), "audio"
            )
            validate_audio_file(audio_path)
            input_data["audio_file_path"] = audio_path
            file_paths["audio"] = audio_path
        
        # Handle handwriting image upload  
        if handwriting_image:
            image_path = await _save_uploaded_file(
                handwriting_image, settings.get_upload_path(), "image"
            )
            validate_image_file(image_path)
            input_data["image_file_path"] = image_path
            file_paths["image"] = image_path
        
        # Process analysis
        start_time = time.time()
        result = await dyslexia_pipeline.analyze_with_timing(input_data)
        processing_time = time.time() - start_time
        
        # Save to database
        session_record = AnalysisSession(
            session_id=result["session_id"],
            input_data={
                "text": text,
                "file_paths": file_paths,
                "user_id": user_id
            },
            input_type=result["analysis"]["analysis_type"],
            analysis_result=result["analysis"],
            confidence_score=result["confidence_score"],
            recommendations=result["recommendations"],
            processing_time=processing_time,
            model_versions=result.get("pipeline_metadata", {}).get("model_versions"),
            user_id=user_id
        )
        
        db.add(session_record)
        db.commit()
        db.refresh(session_record)
        
        return DyslexiaAnalysisResponse(
            session_id=result["session_id"],
            analysis_type=result["analysis"]["analysis_type"],
            analysis=result["analysis"],
            confidence_score=result["confidence_score"],
            risk_level=result["risk_level"],
            recommendations=result["recommendations"],
            screening_summary=result["screening_summary"],
            processing_time=processing_time
        )
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except AnalysisError as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@router.get("/session/{session_id}")
async def get_analysis_session(
    session_id: str,
    db: Session = Depends(get_database)
):
    """Retrieve analysis session by ID."""
    session = db.query(AnalysisSession).filter(
        AnalysisSession.session_id == session_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return session.to_dict()


@router.get("/sessions")
async def list_analysis_sessions(
    limit: int = 50,
    offset: int = 0,
    user_id: Optional[str] = None,
    db: Session = Depends(get_database)
):
    """List analysis sessions with optional filtering."""
    query = db.query(AnalysisSession)
    
    if user_id:
        query = query.filter(AnalysisSession.user_id == user_id)
    
    sessions = query.offset(offset).limit(limit).all()
    return [session.to_dict() for session in sessions]


async def _save_uploaded_file(file: UploadFile, upload_dir: str, file_type: str) -> str:
    """Save uploaded file and return the file path."""
    import uuid
    from pathlib import Path
    
    # Generate unique filename
    file_extension = Path(file.filename).suffix if file.filename else ""
    unique_filename = f"{file_type}_{uuid.uuid4()}{file_extension}"
    file_path = Path(upload_dir) / unique_filename
    
    # Ensure upload directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save file
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    
    return str(file_path)