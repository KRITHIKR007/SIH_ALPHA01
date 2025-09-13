from sqlalchemy import Column, Integer, String, DateTime, Text, Float, JSON
from sqlalchemy.sql import func
from . import Base

class Session(Base):
    """
    Database model for tracking analysis sessions
    Stores input data, analysis results, and metadata for each user interaction
    """
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Input data (JSON field to store flexible input types)
    input_data = Column(JSON, nullable=False, comment="Original input data (text, file paths, etc.)")
    
    # Analysis results
    analysis_result = Column(JSON, nullable=False, comment="Detailed analysis output from pipelines")
    confidence_score = Column(Float, nullable=True, comment="Confidence score for dyslexia screening (0-1)")
    recommendations = Column(JSON, nullable=True, comment="List of recommendations based on analysis")
    
    # Audio file path (for TTS outputs)
    audio_file_path = Column(String(500), nullable=True, comment="Path to generated audio file")
    
    # Metadata
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), comment="Session creation timestamp")
    
    def __repr__(self):
        return f"<Session(id={self.id}, timestamp={self.timestamp}, confidence={self.confidence_score})>"

    def to_dict(self):
        """Convert session to dictionary for API responses"""
        return {
            "id": self.id,
            "input_data": self.input_data,
            "analysis_result": self.analysis_result,
            "confidence_score": self.confidence_score,
            "recommendations": self.recommendations,
            "audio_file_path": self.audio_file_path,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }