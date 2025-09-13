import asyncio
import os
import time
from typing import Optional, Dict, List, Any
import json
import logging
import random

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DyslexiaPipeline:
    """
    Comprehensive dyslexia screening pipeline combining:
    - OCR for handwriting analysis
    - Speech-to-text for reading assessment
    - NLP analysis for error pattern detection
    """
    
    def __init__(self):
        self.ocr_reader = None
        self.whisper_model = None
        self.initialize_models()
    
    def initialize_models(self):
        """Initialize AI models (mock for demo)"""
        try:
            logger.info("Initializing dyslexia analysis models (demo mode)...")
            
            # Mock initialization
            self.ocr_reader = "mock_ocr_reader"
            self.whisper_model = "mock_whisper_model"
            
            logger.info("Models initialized successfully (demo mode)")
            
        except Exception as e:
            logger.error(f"Failed to initialize models: {e}")
            raise
    
    async def analyze(
        self, 
        text: Optional[str] = None,
        audio_file_path: Optional[str] = None,
        image_file_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Main analysis method that processes multiple input types
        and returns comprehensive dyslexia screening results
        """
        analysis = {
            "text_analysis": {},
            "ocr_analysis": {},
            "speech_analysis": {},
            "error_patterns": {},
            "reading_metrics": {}
        }
        
        confidence_scores = []
        recommendations = []
        
        # Text Analysis
        if text:
            text_result = await self._analyze_text(text)
            analysis["text_analysis"] = text_result
            confidence_scores.append(text_result.get("confidence", 0.5))
            recommendations.extend(text_result.get("recommendations", []))
        
        # OCR Analysis (Handwriting)
        if image_file_path and os.path.exists(image_file_path):
            ocr_result = await self._analyze_handwriting(image_file_path)
            analysis["ocr_analysis"] = ocr_result
            confidence_scores.append(ocr_result.get("confidence", 0.5))
            recommendations.extend(ocr_result.get("recommendations", []))
        
        # Speech Analysis
        if audio_file_path and os.path.exists(audio_file_path):
            speech_result = await self._analyze_speech(audio_file_path, text)
            analysis["speech_analysis"] = speech_result
            confidence_scores.append(speech_result.get("confidence", 0.5))
            recommendations.extend(speech_result.get("recommendations", []))
        
        # Calculate overall confidence
        overall_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.5
        
        # Generate comprehensive recommendations
        comprehensive_recommendations = self._generate_recommendations(analysis, overall_confidence)
        
        return {
            "analysis": analysis,
            "confidence_score": overall_confidence,
            "recommendations": comprehensive_recommendations,
            "screening_summary": self._generate_summary(analysis, overall_confidence)
        }
    
    async def _analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze text input for reading comprehension patterns"""
        try:
            words = text.split()
            word_count = len(words)
            
            # Basic text metrics
            avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0
            complex_words = [word for word in words if len(word) > 7]
            
            # Pattern analysis
            reversals = self._detect_reversals(text)
            spelling_errors = self._detect_spelling_patterns(text)
            
            confidence = 0.7 if len(reversals) > 0 or len(spelling_errors) > 0 else 0.3
            
            recommendations = []
            if len(reversals) > 0:
                recommendations.append("Consider visual processing exercises for letter reversals")
            if avg_word_length < 4:
                recommendations.append("Encourage reading materials with varied vocabulary")
            
            return {
                "word_count": word_count,
                "average_word_length": avg_word_length,
                "complex_words_count": len(complex_words),
                "reversals_detected": reversals,
                "spelling_patterns": spelling_errors,
                "confidence": confidence,
                "recommendations": recommendations
            }
            
        except Exception as e:
            logger.error(f"Text analysis failed: {e}")
            return {"error": str(e), "confidence": 0.5}
    
    async def _analyze_handwriting(self, image_path: str) -> Dict[str, Any]:
        """Analyze handwriting via OCR for dyslexia indicators (mock for demo)"""
        try:
            # Mock OCR analysis
            sample_texts = [
                "The quick brown fox jumps",
                "Once upon a time there was", 
                "Reading is fun and important",
                "Practice makes perfect always"
            ]
            
            extracted_text = random.choice(sample_texts)
            
            # Mock analysis results
            has_reversals = random.choice([True, False, False])  # 33% chance
            letter_reversals = ["Potential reversal detected in handwriting"] if has_reversals else []
            writing_clarity = random.uniform(0.6, 0.95)
            
            confidence = 0.8 if has_reversals else 0.4
            
            recommendations = []
            if has_reversals:
                recommendations.append("Practice letter formation exercises")
            if writing_clarity < 0.7:
                recommendations.append("Work on handwriting clarity and spacing")
            
            return {
                "extracted_text": extracted_text,
                "text_confidence": writing_clarity,
                "letter_reversals": letter_reversals,
                "writing_clarity_score": writing_clarity,
                "confidence": confidence,
                "recommendations": recommendations
            }
            
        except Exception as e:
            logger.error(f"OCR analysis failed: {e}")
            return {"error": str(e), "confidence": 0.5}
    
    async def _analyze_speech(self, audio_path: str, expected_text: Optional[str] = None) -> Dict[str, Any]:
        """Analyze speech for reading fluency and accuracy (mock for demo)"""
        try:
            # Mock speech analysis
            sample_transcriptions = [
                "The quick brown fox jumps over the lazy dog",
                "Reading out loud helps with fluency and comprehension",
                "Practice makes perfect when learning new skills"
            ]
            
            transcribed_text = random.choice(sample_transcriptions)
            
            # Mock metrics
            audio_duration = random.uniform(3.0, 8.0)
            word_count = len(transcribed_text.split())
            reading_speed = random.uniform(80, 150)  # WPM
            
            # Mock accuracy
            accuracy_score = random.uniform(0.75, 0.98)
            if expected_text:
                # Simple mock comparison
                accuracy_score = random.uniform(0.8, 0.95)
            
            confidence = 0.6 if reading_speed < 100 or accuracy_score < 0.8 else 0.3
            
            recommendations = []
            if reading_speed < 100:
                recommendations.append("Practice reading fluency exercises")
            if accuracy_score < 0.8:
                recommendations.append("Work on word recognition and pronunciation")
            
            return {
                "transcribed_text": transcribed_text,
                "reading_speed_wpm": reading_speed,
                "audio_duration": audio_duration,
                "accuracy_score": accuracy_score,
                "confidence": confidence,
                "recommendations": recommendations
            }
            
        except Exception as e:
            logger.error(f"Speech analysis failed: {e}")
            return {"error": str(e), "confidence": 0.5}
    
    def _detect_reversals(self, text: str) -> List[Dict[str, str]]:
        """Detect common letter/word reversals"""
        reversals = []
        reversal_pairs = [
            ('b', 'd'), ('p', 'q'), ('m', 'w'), ('n', 'u'),
            ('was', 'saw'), ('on', 'no'), ('left', 'felt')
        ]
        
        for original, reversed_form in reversal_pairs:
            if reversed_form in text.lower():
                reversals.append({
                    "detected": reversed_form,
                    "should_be": original,
                    "type": "letter" if len(original) == 1 else "word"
                })
        
        return reversals
    
    def _detect_spelling_patterns(self, text: str) -> List[str]:
        """Detect common spelling error patterns associated with dyslexia"""
        patterns = []
        words = text.lower().split()
        
        # Common patterns: doubled letters, phonetic spelling, etc.
        for word in words:
            if len(set(word)) < len(word) * 0.5:  # Too many repeated letters
                patterns.append(f"Possible doubled letters in '{word}'")
        
        return patterns
    
    def _detect_handwriting_reversals(self, ocr_results) -> List[str]:
        """Detect letter reversals in handwritten text"""
        reversals = []
        for result in ocr_results:
            text = result[1].lower()
            if any(char in text for char in ['d', 'b', 'p', 'q']):
                # Simple heuristic - in practice, would need more sophisticated analysis
                reversals.append(f"Potential reversal in: {text}")
        return reversals
    
    def _assess_writing_clarity(self, ocr_results) -> float:
        """Assess clarity of handwritten text based on OCR confidence"""
        if not ocr_results:
            return 0.0
        return sum([result[2] for result in ocr_results]) / len(ocr_results)
    
    def _get_audio_duration(self, audio_path: str) -> float:
        """Get audio duration in seconds (mock)"""
        try:
            # Mock duration between 2-10 seconds
            return random.uniform(2.0, 10.0)
        except:
            return 5.0
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts (mock implementation)"""
        # Simple mock similarity calculation
        if not text1 or not text2:
            return 0.0
        
        # Mock similarity based on length and some words
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if len(words1) == 0 and len(words2) == 0:
            return 1.0
        
        common_words = words1.intersection(words2)
        total_words = words1.union(words2)
        
        return len(common_words) / len(total_words) if total_words else 0.0
    
    def _generate_recommendations(self, analysis: Dict, confidence: float) -> List[str]:
        """Generate comprehensive recommendations based on all analyses"""
        recommendations = []
        
        if confidence > 0.6:
            recommendations.append("Consider consultation with a learning specialist")
            recommendations.append("Implement multi-sensory learning approaches")
        
        if "speech_analysis" in analysis and analysis["speech_analysis"].get("reading_speed_wpm", 0) < 100:
            recommendations.append("Practice daily reading fluency exercises")
        
        if "ocr_analysis" in analysis and analysis["ocr_analysis"].get("letter_reversals", []):
            recommendations.append("Use tactile letter formation activities")
        
        recommendations.append("Consider assistive technology tools")
        recommendations.append("Break complex tasks into smaller steps")
        
        return recommendations
    
    def _generate_summary(self, analysis: Dict, confidence: float) -> str:
        """Generate a human-readable summary of the screening results"""
        risk_level = "High" if confidence > 0.7 else "Medium" if confidence > 0.4 else "Low"
        return f"Screening indicates {risk_level.lower()} likelihood of dyslexia indicators (confidence: {confidence:.2f})"


class TTSPipeline:
    """
    Text-to-Speech pipeline optimized for accessibility and learning
    Features: adjustable speed, phonics mode, multiple languages
    """
    
    def __init__(self):
        self.tts_model = None
        self.initialize_tts()
    
    def initialize_tts(self):
        """Initialize TTS model (mock for demo)"""
        try:
            logger.info("Initializing TTS model (demo mode)...")
            # Mock TTS model
            self.tts_model = "mock_tts_model"
            logger.info("TTS model initialized successfully (demo mode)")
        except Exception as e:
            logger.error(f"Failed to initialize TTS model: {e}")
            raise
    
    async def synthesize(
        self,
        text: str,
        speed: float = 1.0,
        phonics_mode: bool = False,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Generate text-to-speech audio with accessibility features (mock for demo)
        """
        try:
            # Process text for phonics mode
            processed_text = text
            if phonics_mode:
                processed_text = self._apply_phonics_processing(text)
            
            # Generate unique filename
            timestamp = int(time.time())
            output_path = f"outputs/tts_{timestamp}.wav"
            os.makedirs("outputs", exist_ok=True)
            
            # Mock audio file creation (create empty file)
            with open(output_path, "w") as f:
                f.write("# Mock TTS audio file - demo mode")
            
            # Mock duration calculation
            word_count = len(text.split())
            base_duration = word_count * 0.6  # ~0.6 seconds per word
            duration = base_duration / speed  # Adjust for speed
            
            return {
                "audio_file_path": output_path,
                "duration": duration,
                "text_processed": processed_text,
                "settings": {
                    "speed": speed,
                    "phonics_mode": phonics_mode,
                    "language": language
                }
            }
            
        except Exception as e:
            logger.error(f"TTS synthesis failed: {e}")
            raise
    
    def _apply_phonics_processing(self, text: str) -> str:
        """Apply phonics-friendly text processing"""
        # Add pauses between syllables for complex words
        words = text.split()
        processed_words = []
        
        for word in words:
            if len(word) > 6:  # Complex word
                # Simple syllable break heuristic
                processed_word = ""
                for i, char in enumerate(word):
                    processed_word += char
                    if i > 0 and i % 3 == 0 and i < len(word) - 1:
                        processed_word += " "  # Add slight pause
                processed_words.append(processed_word)
            else:
                processed_words.append(word)
        
        return " ".join(processed_words)
    
    async def _adjust_audio_speed(self, audio_path: str, speed: float) -> str:
        """Adjust audio playback speed (mock for demo)"""
        try:
            # Mock speed adjustment - just rename file
            adjusted_path = audio_path.replace(".wav", f"_speed_{speed}.wav")
            
            # Copy the mock file
            with open(audio_path, "r") as src:
                content = src.read()
            
            with open(adjusted_path, "w") as dst:
                dst.write(content + f" (adjusted speed: {speed}x)")
            
            return adjusted_path
            
        except Exception as e:
            logger.error(f"Speed adjustment failed: {e}")
            return audio_path
    
    def _get_audio_duration(self, audio_path: str) -> float:
        """Get audio duration in seconds (mock for demo)"""
        try:
            # Mock duration based on file path/content
            return random.uniform(2.0, 8.0)
        except:
            return 5.0
