"""
Configuration management for DyslexiaCare platform.

Centralized configuration using environment variables and settings.
"""

import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    def __init__(self):
        # Application info
        self.app_name = "DyslexiaCare"
        self.app_version = "1.0.0"
        self.debug = os.getenv("DEBUG", "False").lower() == "true"
        
        # Database configuration
        self.database_url = os.getenv(
            "DATABASE_URL", 
            "sqlite:///./src/dyslexia_platform/data/dyslexia_platform.db"
        )
        
        # Security
        self.admin_token = os.getenv("ADMIN_TOKEN", "hackathon-admin-2024")
        self.secret_key = os.getenv("SECRET_KEY", "your-secret-key-here")
        
        # API Configuration
        self.api_host = os.getenv("API_HOST", "0.0.0.0")
        self.api_port = int(os.getenv("API_PORT", "8000"))
        self.api_reload = os.getenv("API_RELOAD", "True").lower() == "true"
        
        # Frontend Configuration
        self.frontend_port = int(os.getenv("FRONTEND_PORT", "8501"))
        self.api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        
        # AI Model Configuration
        self.whisper_model = os.getenv("WHISPER_MODEL", "small")
        self.ocr_languages = os.getenv("OCR_LANGUAGES", "en")
        self.tts_model = os.getenv(
            "TTS_MODEL", 
            "tts_models/en/ljspeech/tacotron2-DDC"
        )
        
        # File paths
        self.upload_dir = os.getenv("UPLOAD_DIR", "src/dyslexia_platform/data/uploads")
        self.output_dir = os.getenv("OUTPUT_DIR", "src/dyslexia_platform/data/outputs")
        self.models_dir = os.getenv("MODELS_DIR", "src/dyslexia_platform/data/models")
        self.logs_dir = os.getenv("LOGS_DIR", "logs")
        
        # CORS settings
        self.allowed_origins = self._parse_list(os.getenv("ALLOWED_ORIGINS", "*"))

    def _parse_list(self, value: str) -> List[str]:
        """Parse comma-separated string into list."""
        if value == "*":
            return ["*"]
        return [item.strip() for item in value.split(",") if item.strip()]

    def get_upload_path(self) -> Path:
        """Get absolute path for uploads directory."""
        return Path(self.upload_dir).resolve()
    
    def get_output_path(self) -> Path:
        """Get absolute path for outputs directory."""
        return Path(self.output_dir).resolve()
    
    def get_models_path(self) -> Path:
        """Get absolute path for models directory."""
        return Path(self.models_dir).resolve()
    
    def get_logs_path(self) -> Path:
        """Get absolute path for logs directory."""
        return Path(self.logs_dir).resolve()

# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings instance."""
    return settings
