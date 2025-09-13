"""
Database models for DyslexiaCare platform.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Float, JSON, Boolean
from sqlalchemy.sql import func
from typing import Dict, Any, Optional

from .connection import Base


class AnalysisSession(Base):
    """
    Database model for tracking analysis sessions.
    Stores input data, analysis results, and metadata for each user interaction.
    """
    __tablename__ = "analysis_sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String(36), unique=True, index=True, nullable=False, 
                       comment="UUID for session identification")
    
    # Input data (JSON field to store flexible input types)
    input_data = Column(JSON, nullable=False, 
                       comment="Original input data (text, file paths, etc.)")
    input_type = Column(String(50), nullable=False, 
                       comment="Type of input: text, audio, handwriting, multimodal")
    
    # Analysis results
    analysis_result = Column(JSON, nullable=False, 
                           comment="Detailed analysis output from pipelines")
    confidence_score = Column(Float, nullable=True, 
                            comment="Confidence score for dyslexia screening (0-1)")
    recommendations = Column(JSON, nullable=True, 
                           comment="List of recommendations based on analysis")
    
    # Processing metadata
    processing_time = Column(Float, nullable=True, 
                           comment="Time taken for analysis in seconds")
    model_versions = Column(JSON, nullable=True, 
                          comment="Versions of AI models used")
    
    # User session info
    user_id = Column(String(100), nullable=True, 
                    comment="Optional user identifier")
    ip_address = Column(String(45), nullable=True, 
                       comment="Client IP address")
    user_agent = Column(Text, nullable=True, 
                       comment="Client user agent string")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), 
                       comment="Session creation timestamp")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), 
                       comment="Last update timestamp")
    
    def __repr__(self):
        return f"<AnalysisSession(id={self.id}, session_id={self.session_id}, " \
               f"confidence={self.confidence_score})>"

    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary for API responses."""
        result = {
            "id": self.id,
            "session_id": self.session_id,
            "input_data": self.input_data,
            "input_type": self.input_type,
            "analysis_result": self.analysis_result,
            "confidence_score": self.confidence_score,
            "recommendations": self.recommendations,
            "processing_time": self.processing_time,
            "model_versions": self.model_versions,
        }
        
        # Handle datetime fields safely
        try:
            result["created_at"] = self.created_at.isoformat()
        except (AttributeError, TypeError):
            result["created_at"] = None
            
        try:
            result["updated_at"] = self.updated_at.isoformat()
        except (AttributeError, TypeError):
            result["updated_at"] = None
            
        return result


class TTSSession(Base):
    """
    Database model for tracking text-to-speech sessions.
    """
    __tablename__ = "tts_sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String(36), unique=True, index=True, nullable=False)
    
    # Input text and settings
    input_text = Column(Text, nullable=False, comment="Original text for TTS")
    language = Column(String(10), nullable=False, default="en", 
                     comment="Language code for TTS")
    speed = Column(Float, nullable=False, default=1.0, 
                  comment="Speech speed multiplier")
    phonics_mode = Column(Boolean, nullable=False, default=False, 
                         comment="Whether phonics mode was enabled")
    
    # Output information
    audio_file_path = Column(String(500), nullable=True, 
                           comment="Path to generated audio file")
    audio_duration = Column(Float, nullable=True, 
                          comment="Duration of generated audio in seconds")
    file_size = Column(Integer, nullable=True, 
                      comment="Size of audio file in bytes")
    
    # Processing metadata
    processing_time = Column(Float, nullable=True, 
                           comment="Time taken for TTS generation")
    model_used = Column(String(100), nullable=True, 
                       comment="TTS model identifier")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<TTSSession(id={self.id}, session_id={self.session_id}, " \
               f"language={self.language})>"

    def to_dict(self) -> Dict[str, Any]:
        """Convert TTS session to dictionary for API responses."""
        result = {
            "id": self.id,
            "session_id": self.session_id,
            "input_text": self.input_text,
            "language": self.language,
            "speed": self.speed,
            "phonics_mode": self.phonics_mode,
            "audio_file_path": self.audio_file_path,
            "audio_duration": self.audio_duration,
            "file_size": self.file_size,
            "processing_time": self.processing_time,
            "model_used": self.model_used,
        }
        
        try:
            result["created_at"] = self.created_at.isoformat()
        except (AttributeError, TypeError):
            result["created_at"] = None
            
        return result


class UserFeedback(Base):
    """
    Database model for storing user feedback on analysis results.
    """
    __tablename__ = "user_feedback"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String(36), index=True, nullable=False, 
                       comment="Related analysis session ID")
    
    # Feedback data
    rating = Column(Integer, nullable=True, 
                   comment="User rating (1-5 scale)")
    feedback_text = Column(Text, nullable=True, 
                         comment="User's written feedback")
    is_helpful = Column(Boolean, nullable=True, 
                       comment="Whether user found analysis helpful")
    accuracy_rating = Column(Integer, nullable=True, 
                           comment="User's assessment of accuracy (1-5)")
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<UserFeedback(id={self.id}, session_id={self.session_id}, " \
               f"rating={self.rating})>"

    def to_dict(self) -> Dict[str, Any]:
        """Convert feedback to dictionary for API responses."""
        result = {
            "id": self.id,
            "session_id": self.session_id,
            "rating": self.rating,
            "feedback_text": self.feedback_text,
            "is_helpful": self.is_helpful,
            "accuracy_rating": self.accuracy_rating,
        }
        
        try:
            result["created_at"] = self.created_at.isoformat()
        except (AttributeError, TypeError):
            result["created_at"] = None
            
        return result