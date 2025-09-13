"""Shared utilities and common functionality."""

from .constants import *
from .exceptions import *
from .utils import *

__all__ = [
    # Constants
    "APP_NAME", "APP_VERSION", "SUPPORTED_IMAGE_TYPES", "SUPPORTED_AUDIO_TYPES",
    "CONFIDENCE_THRESHOLD_HIGH", "CONFIDENCE_THRESHOLD_MEDIUM", "CONFIDENCE_THRESHOLD_LOW",
    
    # Exceptions
    "DyslexiaCareException", "ValidationError", "FileProcessingError", 
    "ModelLoadError", "AnalysisError", "DatabaseError", "ConfigurationError",
    "TTSError", "OCRError", "SpeechToTextError",
    
    # Utilities
    "generate_session_id", "validate_image_file", "validate_audio_file",
    "ensure_directory_exists", "safe_filename", "get_file_info",
    "setup_logging", "calculate_confidence_score", "sanitize_text"
]