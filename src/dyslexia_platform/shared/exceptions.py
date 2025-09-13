"""
Custom exceptions for the DyslexiaCare platform.
"""


class DyslexiaCareException(Exception):
    """Base exception for DyslexiaCare platform."""
    pass


class ValidationError(DyslexiaCareException):
    """Raised when input validation fails."""
    pass


class FileProcessingError(DyslexiaCareException):
    """Raised when file processing fails."""
    pass


class ModelLoadError(DyslexiaCareException):
    """Raised when AI model loading fails."""
    pass


class AnalysisError(DyslexiaCareException):
    """Raised when analysis pipeline fails."""
    pass


class DatabaseError(DyslexiaCareException):
    """Raised when database operations fail."""
    pass


class ConfigurationError(DyslexiaCareException):
    """Raised when configuration is invalid."""
    pass


class TTSError(DyslexiaCareException):
    """Raised when text-to-speech processing fails."""
    pass


class OCRError(DyslexiaCareException):
    """Raised when OCR processing fails."""
    pass


class SpeechToTextError(DyslexiaCareException):
    """Raised when speech-to-text processing fails."""
    pass