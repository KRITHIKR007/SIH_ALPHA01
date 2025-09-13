"""
Pydantic models for API request/response schemas.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class DyslexiaAnalysisRequest(BaseModel):
    """Request model for dyslexia analysis."""
    text: Optional[str] = Field(None, description="Text input for analysis")
    audio_file: Optional[str] = Field(None, description="Path to audio file")
    handwriting_image: Optional[str] = Field(None, description="Path to handwriting image")
    user_id: Optional[str] = Field(None, description="Optional user identifier")
    

class DyslexiaAnalysisResponse(BaseModel):
    """Response model for dyslexia analysis."""
    session_id: str = Field(..., description="Unique session identifier")
    analysis_type: str = Field(..., description="Type of analysis performed")
    analysis: Dict[str, Any] = Field(..., description="Detailed analysis results")
    confidence_score: float = Field(..., description="Overall confidence score (0-1)")
    risk_level: str = Field(..., description="Risk level assessment")
    recommendations: List[str] = Field(..., description="List of recommendations")
    screening_summary: str = Field(..., description="Human-readable summary")
    processing_time: float = Field(..., description="Processing time in seconds")


class TTSRequest(BaseModel):
    """Request model for text-to-speech synthesis."""
    text: str = Field(..., description="Text to synthesize", max_length=10000)
    speed: Optional[float] = Field(1.0, description="Reading speed (0.5-2.0)", ge=0.5, le=2.0)
    phonics_mode: Optional[bool] = Field(False, description="Enable phonics mode")
    language: Optional[str] = Field("en", description="Language code")
    

class TTSResponse(BaseModel):
    """Response model for text-to-speech synthesis."""
    session_id: str = Field(..., description="Unique session identifier")
    audio_file_path: str = Field(..., description="Path to generated audio file")
    audio_duration: float = Field(..., description="Audio duration in seconds")
    file_size: int = Field(..., description="Audio file size in bytes")
    settings_used: Dict[str, Any] = Field(..., description="TTS settings used")
    processing_time: float = Field(..., description="Processing time in seconds")


class SessionResponse(BaseModel):
    """Response model for session information."""
    id: int = Field(..., description="Database session ID")
    session_id: str = Field(..., description="Unique session identifier")
    input_type: str = Field(..., description="Type of input processed")
    confidence_score: Optional[float] = Field(None, description="Analysis confidence score")
    created_at: str = Field(..., description="Session creation timestamp")
    

class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(..., description="Service status")
    timestamp: str = Field(..., description="Current timestamp")
    version: str = Field(..., description="API version")
    

class ErrorResponse(BaseModel):
    """Response model for error cases."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: str = Field(..., description="Error timestamp")


class FeedbackRequest(BaseModel):
    """Request model for user feedback."""
    session_id: str = Field(..., description="Related session ID")
    rating: Optional[int] = Field(None, description="User rating (1-5)", ge=1, le=5)
    feedback_text: Optional[str] = Field(None, description="Written feedback", max_length=1000)
    is_helpful: Optional[bool] = Field(None, description="Whether analysis was helpful")
    accuracy_rating: Optional[int] = Field(None, description="Accuracy assessment (1-5)", ge=1, le=5)


class FeedbackResponse(BaseModel):
    """Response model for feedback submission."""
    id: int = Field(..., description="Feedback ID")
    session_id: str = Field(..., description="Related session ID")
    message: str = Field(..., description="Confirmation message")
    created_at: str = Field(..., description="Feedback timestamp")


class LanguageSupport(BaseModel):
    """Model for supported language information."""
    code: str = Field(..., description="Language code")
    name: str = Field(..., description="Language display name")
    tts_supported: bool = Field(..., description="TTS support available")
    

class CapabilitiesResponse(BaseModel):
    """Response model for API capabilities."""
    supported_languages: List[LanguageSupport] = Field(..., description="Supported languages")
    supported_speeds: List[float] = Field(..., description="Available TTS speeds")
    max_file_sizes: Dict[str, int] = Field(..., description="Maximum file sizes by type")
    supported_formats: Dict[str, List[str]] = Field(..., description="Supported file formats")
    features: List[str] = Field(..., description="Available features")


class BatchAnalysisRequest(BaseModel):
    """Request model for batch analysis."""
    sessions: List[DyslexiaAnalysisRequest] = Field(..., description="List of analysis requests")
    batch_id: Optional[str] = Field(None, description="Optional batch identifier")
    

class BatchAnalysisResponse(BaseModel):
    """Response model for batch analysis."""
    batch_id: str = Field(..., description="Batch identifier")
    total_sessions: int = Field(..., description="Total number of sessions")
    completed_sessions: int = Field(..., description="Number of completed sessions")
    failed_sessions: int = Field(..., description="Number of failed sessions")
    results: List[DyslexiaAnalysisResponse] = Field(..., description="Analysis results")
    processing_time: float = Field(..., description="Total processing time")


class StatisticsResponse(BaseModel):
    """Response model for usage statistics."""
    total_sessions: int = Field(..., description="Total number of sessions")
    analysis_sessions: int = Field(..., description="Number of analysis sessions")
    tts_sessions: int = Field(..., description="Number of TTS sessions")
    average_confidence: float = Field(..., description="Average confidence score")
    most_common_language: str = Field(..., description="Most frequently used language")
    date_range: Dict[str, str] = Field(..., description="Statistics date range")