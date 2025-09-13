"""
Constants and configuration values used across the DyslexiaCare platform.
"""

# Application constants
APP_NAME = "DyslexiaCare"
APP_VERSION = "1.0.0"

# Supported file types
SUPPORTED_IMAGE_TYPES = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}
SUPPORTED_AUDIO_TYPES = {".wav", ".mp3", ".flac", ".ogg", ".m4a"}
SUPPORTED_TEXT_TYPES = {".txt", ".md", ".doc", ".docx", ".pdf"}

# Analysis confidence thresholds
CONFIDENCE_THRESHOLD_HIGH = 0.8
CONFIDENCE_THRESHOLD_MEDIUM = 0.6
CONFIDENCE_THRESHOLD_LOW = 0.4

# TTS settings
TTS_DEFAULT_SPEED = 1.0
TTS_MIN_SPEED = 0.5
TTS_MAX_SPEED = 2.0

# OCR settings
OCR_DEFAULT_LANGUAGES = ["en"]
OCR_CONFIDENCE_THRESHOLD = 0.7

# API response codes
HTTP_SUCCESS = 200
HTTP_CREATED = 201
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_INTERNAL_ERROR = 500

# Analysis types
ANALYSIS_TEXT = "text"
ANALYSIS_AUDIO = "audio"
ANALYSIS_HANDWRITING = "handwriting"
ANALYSIS_MULTIMODAL = "multimodal"

# Dyslexia indicators
DYSLEXIA_INDICATORS = {
    "letter_reversals": ["b/d", "p/q", "u/n", "m/w"],
    "word_reversals": ["was/saw", "on/no", "left/felt"],
    "phonetic_errors": ["phone/fone", "enough/enuf"],
    "omissions": "missing_letters",
    "additions": "extra_letters",
    "substitutions": "wrong_letters"
}

# Accessibility features
ACCESSIBILITY_FONTS = ["OpenDyslexic", "Arial", "Verdana", "Comic Sans MS"]
ACCESSIBILITY_THEMES = ["dark", "light", "high_contrast"]
READING_SPEEDS = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]

# File size limits (in bytes)
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_AUDIO_SIZE = 50 * 1024 * 1024  # 50MB
MAX_TEXT_SIZE = 1 * 1024 * 1024    # 1MB

# Database settings
DB_POOL_SIZE = 10
DB_MAX_OVERFLOW = 20
DB_POOL_TIMEOUT = 30

# Logging levels
LOG_LEVELS = {
    "DEBUG": 10,
    "INFO": 20,
    "WARNING": 30,
    "ERROR": 40,
    "CRITICAL": 50
}