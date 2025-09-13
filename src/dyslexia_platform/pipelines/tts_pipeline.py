"""
Text-to-Speech pipeline optimized for accessibility and dyslexia support.

Features: adjustable speed, phonics mode, multiple languages, and 
accessibility-focused audio generation.
"""

import os
import time
import random
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

from .base import AnalysisPipeline
from ..shared.exceptions import TTSError
from ..shared.constants import (
    TTS_DEFAULT_SPEED, TTS_MIN_SPEED, TTS_MAX_SPEED,
    READING_SPEEDS
)
from ..shared.utils import safe_filename, ensure_directory_exists

logger = logging.getLogger(__name__)


class TTSPipeline(AnalysisPipeline):
    """
    Text-to-Speech pipeline optimized for accessibility and learning.
    
    Features:
    - Adjustable reading speeds (0.5x to 2.0x)
    - Phonics mode for syllable-based pronunciation
    - Multiple language support
    - High-quality audio processing
    - Accessibility optimizations
    """
    
    def __init__(self):
        super().__init__("tts_synthesis")
        self.tts_model = None
        self.supported_languages = ["en", "es", "fr", "de"]
        self.output_format = "wav"
    
    async def initialize(self):
        """Initialize TTS models and audio processing."""
        try:
            self.logger.info("Initializing TTS models...")
            
            # TODO: Initialize actual TTS models (Coqui TTS, etc.)
            # For demo/development, using mock models
            self.tts_model = "mock_coqui_tts"
            
            self.model_versions = {
                "tts_engine": "coqui-tts-0.22.0",
                "audio_processor": "pydub-0.25.1",
                "voice_models": {
                    "en": "ljspeech/tacotron2-DDC",
                    "es": "mai/tacotron2-DDC",
                    "fr": "siwis/tacotron2-DDC",
                    "de": "thorsten/tacotron2-DDC"
                }
            }
            
            self.initialized = True
            self.logger.info("TTS models initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize TTS models: {e}")
            raise TTSError(f"TTS initialization failed: {e}")
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate text-to-speech audio with accessibility features.
        
        Args:
            input_data: Dict containing:
                - text: Text to synthesize
                - speed: Reading speed (0.5-2.0, default 1.0)
                - phonics_mode: Enable phonics processing (default False)
                - language: Language code (default "en")
                - output_dir: Output directory (optional)
        """
        text = input_data.get("text", "")
        speed = self._validate_speed(input_data.get("speed", TTS_DEFAULT_SPEED))
        phonics_mode = input_data.get("phonics_mode", False)
        language = input_data.get("language", "en")
        output_dir = input_data.get("output_dir", "src/dyslexia_platform/data/outputs")
        
        if not text.strip():
            raise TTSError("No text provided for synthesis")
        
        if language not in self.supported_languages:
            self.logger.warning(f"Language {language} not supported, using English")
            language = "en"
        
        # Process text for phonics mode if enabled
        processed_text = text
        if phonics_mode:
            processed_text = self._apply_phonics_processing(text)
        
        # Generate audio
        audio_result = await self._synthesize_audio(
            processed_text, speed, language, output_dir
        )
        
        return {
            "original_text": text,
            "processed_text": processed_text,
            "audio_file_path": audio_result["file_path"],
            "audio_duration": audio_result["duration"],
            "file_size": audio_result["file_size"],
            "settings": {
                "speed": speed,
                "phonics_mode": phonics_mode,
                "language": language,
                "voice_model": self.model_versions["voice_models"].get(language)
            },
            "accessibility_features": {
                "syllable_breaks": phonics_mode,
                "adjustable_speed": True,
                "high_contrast_compatible": True,
                "screen_reader_friendly": True
            }
        }
    
    def _validate_speed(self, speed: float) -> float:
        """Validate and clamp speed to acceptable range."""
        if speed < TTS_MIN_SPEED:
            self.logger.warning(f"Speed {speed} too low, using minimum {TTS_MIN_SPEED}")
            return TTS_MIN_SPEED
        elif speed > TTS_MAX_SPEED:
            self.logger.warning(f"Speed {speed} too high, using maximum {TTS_MAX_SPEED}")
            return TTS_MAX_SPEED
        return speed
    
    async def _synthesize_audio(self, text: str, speed: float, 
                              language: str, output_dir: str) -> Dict[str, Any]:
        """Synthesize text to audio with specified parameters."""
        try:
            # Ensure output directory exists
            output_path = ensure_directory_exists(output_dir)
            
            # Generate unique filename
            timestamp = int(time.time())
            safe_text = safe_filename(text[:30])  # Use first 30 chars for filename
            filename = f"tts_{timestamp}_{safe_text}_{language}_{speed}x.{self.output_format}"
            file_path = output_path / filename
            
            # TODO: Implement actual TTS synthesis
            # For demo/development, create mock audio file
            duration = await self._mock_synthesize(str(file_path), text, speed, language)
            
            # Calculate file size
            file_size = file_path.stat().st_size if file_path.exists() else 0
            
            return {
                "file_path": str(file_path),
                "duration": duration,
                "file_size": file_size
            }
            
        except Exception as e:
            self.logger.error(f"Audio synthesis failed: {e}")
            raise TTSError(f"Audio synthesis failed: {e}")
    
    async def _mock_synthesize(self, file_path: str, text: str, 
                             speed: float, language: str) -> float:
        """Mock audio synthesis for demo/development."""
        # Create mock audio file
        with open(file_path, "w") as f:
            f.write(f"# Mock TTS Audio File - Demo Mode\\n")
            f.write(f"# Text: {text}\\n")
            f.write(f"# Language: {language}\\n")
            f.write(f"# Speed: {speed}x\\n")
            f.write(f"# Generated at: {time.ctime()}\\n")
        
        # Calculate mock duration
        word_count = len(text.split())
        base_duration = word_count * 0.6  # ~0.6 seconds per word
        duration = base_duration / speed  # Adjust for speed
        
        return round(duration, 2)
    
    def _apply_phonics_processing(self, text: str) -> str:
        """
        Apply phonics-friendly text processing.
        
        Adds syllable breaks and pronunciation aids for complex words.
        """
        words = text.split()
        processed_words = []
        
        for word in words:
            if len(word) > 6:  # Complex word - add syllable breaks
                processed_word = self._add_syllable_breaks(word)
                processed_words.append(processed_word)
            else:
                processed_words.append(word)
        
        return " ".join(processed_words)
    
    def _add_syllable_breaks(self, word: str) -> str:
        """
        Add syllable breaks to complex words.
        
        Simple heuristic for syllable detection - in production,
        would use a proper syllabification library.
        """
        vowels = "aeiouAEIOU"
        processed = ""
        
        for i, char in enumerate(word):
            processed += char
            
            # Add break after vowel if followed by consonant
            if (char in vowels and 
                i < len(word) - 2 and 
                word[i + 1] not in vowels and
                word[i + 2] in vowels):
                processed += "-"  # Syllable break marker
        
        return processed
    
    async def adjust_existing_audio(self, file_path: str, new_speed: float) -> Dict[str, Any]:
        """
        Adjust the speed of existing audio file.
        
        Args:
            file_path: Path to existing audio file
            new_speed: New speed multiplier
            
        Returns:
            Dict with new file information
        """
        try:
            if not os.path.exists(file_path):
                raise TTSError(f"Audio file not found: {file_path}")
            
            new_speed = self._validate_speed(new_speed)
            
            # Generate new filename
            original_path = Path(file_path)
            new_filename = f"{original_path.stem}_speed_{new_speed}x{original_path.suffix}"
            new_path = original_path.parent / new_filename
            
            # TODO: Implement actual audio speed adjustment using pydub
            # For demo, just copy the file with new name
            await self._mock_adjust_speed(str(original_path), str(new_path), new_speed)
            
            # Calculate new duration
            original_duration = self._get_mock_duration(str(original_path))
            new_duration = original_duration / new_speed
            
            return {
                "original_file": str(original_path),
                "adjusted_file": str(new_path),
                "original_duration": original_duration,
                "new_duration": new_duration,
                "speed_adjustment": new_speed
            }
            
        except Exception as e:
            self.logger.error(f"Audio speed adjustment failed: {e}")
            raise TTSError(f"Speed adjustment failed: {e}")
    
    async def _mock_adjust_speed(self, input_path: str, output_path: str, speed: float):
        """Mock audio speed adjustment for demo."""
        with open(input_path, "r") as src:
            content = src.read()
        
        with open(output_path, "w") as dst:
            dst.write(content + f"\\n# Speed adjusted to: {speed}x")
    
    def _get_mock_duration(self, file_path: str) -> float:
        """Get mock audio duration for demo."""
        try:
            # Extract duration from mock file if possible
            with open(file_path, "r") as f:
                content = f.read()
                if "word_count" in content:
                    # Try to calculate from mock data
                    return random.uniform(3.0, 15.0)
            return random.uniform(5.0, 10.0)
        except:
            return 5.0
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get supported languages and their display names."""
        return {
            "en": "English",
            "es": "Spanish", 
            "fr": "French",
            "de": "German"
        }
    
    def get_supported_speeds(self) -> List[float]:
        """Get list of supported reading speeds."""
        return READING_SPEEDS
    
    def validate_text_length(self, text: str, max_length: int = 10000) -> bool:
        """Validate text length for TTS processing."""
        return len(text) <= max_length