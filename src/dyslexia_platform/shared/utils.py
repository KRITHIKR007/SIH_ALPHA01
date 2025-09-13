"""
Utility functions for the DyslexiaCare platform.
"""

import os
import uuid
import hashlib
import mimetypes
from pathlib import Path
from typing import Optional, Dict, Any, List, Union
from datetime import datetime
import json
import logging

from .constants import (
    SUPPORTED_IMAGE_TYPES, 
    SUPPORTED_AUDIO_TYPES, 
    SUPPORTED_TEXT_TYPES,
    MAX_IMAGE_SIZE,
    MAX_AUDIO_SIZE,
    MAX_TEXT_SIZE
)
from .exceptions import ValidationError, FileProcessingError


def generate_session_id() -> str:
    """Generate a unique session ID."""
    return str(uuid.uuid4())


def generate_file_hash(file_path: str) -> str:
    """Generate SHA-256 hash of a file."""
    hash_sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except Exception as e:
        raise FileProcessingError(f"Failed to generate hash for {file_path}: {e}")


def validate_file_type(file_path: str, allowed_types: set) -> bool:
    """Validate if file type is allowed."""
    file_ext = Path(file_path).suffix.lower()
    return file_ext in allowed_types


def validate_file_size(file_path: str, max_size: int) -> bool:
    """Validate if file size is within limits."""
    try:
        file_size = os.path.getsize(file_path)
        return file_size <= max_size
    except OSError:
        return False


def validate_image_file(file_path: str) -> bool:
    """Validate image file type and size."""
    if not validate_file_type(file_path, SUPPORTED_IMAGE_TYPES):
        raise ValidationError(f"Unsupported image type: {Path(file_path).suffix}")
    
    if not validate_file_size(file_path, MAX_IMAGE_SIZE):
        raise ValidationError(f"Image file too large. Max size: {MAX_IMAGE_SIZE} bytes")
    
    return True


def validate_audio_file(file_path: str) -> bool:
    """Validate audio file type and size."""
    if not validate_file_type(file_path, SUPPORTED_AUDIO_TYPES):
        raise ValidationError(f"Unsupported audio type: {Path(file_path).suffix}")
    
    if not validate_file_size(file_path, MAX_AUDIO_SIZE):
        raise ValidationError(f"Audio file too large. Max size: {MAX_AUDIO_SIZE} bytes")
    
    return True


def validate_text_file(file_path: str) -> bool:
    """Validate text file type and size."""
    if not validate_file_type(file_path, SUPPORTED_TEXT_TYPES):
        raise ValidationError(f"Unsupported text type: {Path(file_path).suffix}")
    
    if not validate_file_size(file_path, MAX_TEXT_SIZE):
        raise ValidationError(f"Text file too large. Max size: {MAX_TEXT_SIZE} bytes")
    
    return True


def ensure_directory_exists(directory_path: Union[str, Path]) -> Path:
    """Ensure directory exists, create if it doesn't."""
    path = Path(directory_path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_filename(filename: str) -> str:
    """Create a safe filename by removing/replacing unsafe characters."""
    # Remove or replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    safe_name = filename
    for char in unsafe_chars:
        safe_name = safe_name.replace(char, '_')
    
    # Limit length
    if len(safe_name) > 255:
        name, ext = os.path.splitext(safe_name)
        safe_name = name[:255-len(ext)] + ext
    
    return safe_name


def get_file_info(file_path: str) -> Dict[str, Any]:
    """Get comprehensive file information."""
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    stat = path.stat()
    mime_type, _ = mimetypes.guess_type(str(path))
    
    return {
        "filename": path.name,
        "size": stat.st_size,
        "extension": path.suffix.lower(),
        "mime_type": mime_type,
        "created": datetime.fromtimestamp(stat.st_ctime),
        "modified": datetime.fromtimestamp(stat.st_mtime),
        "is_file": path.is_file(),
        "is_dir": path.is_dir(),
        "absolute_path": str(path.absolute())
    }


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size = float(size_bytes)
    while size >= 1024 and i < len(size_names) - 1:
        size /= 1024.0
        i += 1
    
    return f"{size:.1f} {size_names[i]}"


def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """Setup logging configuration."""
    logger = logging.getLogger("dyslexia_platform")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        ensure_directory_exists(Path(log_file).parent)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def calculate_confidence_score(results: List[float]) -> float:
    """Calculate overall confidence score from multiple results."""
    if not results:
        return 0.0
    
    # Weighted average with emphasis on consistency
    avg_score = sum(results) / len(results)
    
    # Penalty for high variance
    if len(results) > 1:
        variance = sum((x - avg_score) ** 2 for x in results) / len(results)
        variance_penalty = min(variance * 0.5, 0.3)  # Max penalty of 0.3
        avg_score = max(0.0, avg_score - variance_penalty)
    
    return min(1.0, avg_score)


def sanitize_text(text: str) -> str:
    """Sanitize text input by removing potentially harmful content."""
    if not isinstance(text, str):
        return ""
    
    # Remove null bytes and control characters
    sanitized = text.replace('\x00', '').strip()
    
    # Limit length
    if len(sanitized) > 10000:  # 10KB text limit
        sanitized = sanitized[:10000]
    
    return sanitized


def format_analysis_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Format analysis result for consistent API response."""
    return {
        "session_id": result.get("session_id"),
        "timestamp": datetime.now().isoformat(),
        "analysis_type": result.get("analysis_type"),
        "confidence_score": round(result.get("confidence_score", 0.0), 3),
        "results": result.get("results", {}),
        "recommendations": result.get("recommendations", []),
        "metadata": result.get("metadata", {})
    }