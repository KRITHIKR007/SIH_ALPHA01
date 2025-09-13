"""
Dyslexia analysis pipeline for comprehensive screening.

Combines text analysis, OCR handwriting analysis, and speech-to-text
for multi-modal dyslexia screening.
"""

import asyncio
import os
import random
from typing import Optional, Dict, List, Any
import logging

from .base import AnalysisPipeline
from ..shared.exceptions import AnalysisError, OCRError, SpeechToTextError
from ..shared.constants import (
    ANALYSIS_TEXT, ANALYSIS_AUDIO, ANALYSIS_HANDWRITING, ANALYSIS_MULTIMODAL,
    CONFIDENCE_THRESHOLD_HIGH, CONFIDENCE_THRESHOLD_MEDIUM,
    DYSLEXIA_INDICATORS
)

logger = logging.getLogger(__name__)


class DyslexiaAnalysisPipeline(AnalysisPipeline):
    """
    Comprehensive dyslexia screening pipeline combining:
    - Text analysis for reading comprehension patterns
    - OCR for handwriting analysis  
    - Speech-to-text for reading fluency assessment
    - NLP analysis for error pattern detection
    """
    
    def __init__(self):
        super().__init__("dyslexia_analysis")
        self.ocr_reader = None
        self.whisper_model = None
        self.nlp_model = None
    
    async def initialize(self):
        """Initialize AI models for analysis."""
        try:
            self.logger.info("Initializing dyslexia analysis models...")
            
            # TODO: Initialize actual models in production
            # For demo/development, using mock models
            self.ocr_reader = "mock_easyocr_reader"
            self.whisper_model = "mock_whisper_small"
            self.nlp_model = "mock_nlp_model"
            
            self.model_versions = {
                "ocr": "easyocr-1.7.0",
                "whisper": "openai-whisper-20231117", 
                "nlp": "custom-dyslexia-detector-1.0"
            }
            
            self.initialized = True
            self.logger.info("Dyslexia analysis models initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize models: {e}")
            raise AnalysisError(f"Model initialization failed: {e}")
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main analysis method that processes multiple input types
        and returns comprehensive dyslexia screening results.
        """
        text = input_data.get("text")
        audio_file_path = input_data.get("audio_file_path")
        image_file_path = input_data.get("image_file_path")
        
        # Determine analysis type
        analysis_type = self._determine_analysis_type(text, audio_file_path, image_file_path)
        
        analysis = {
            "analysis_type": analysis_type,
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
            try:
                ocr_result = await self._analyze_handwriting(image_file_path)
                analysis["ocr_analysis"] = ocr_result
                confidence_scores.append(ocr_result.get("confidence", 0.5))
                recommendations.extend(ocr_result.get("recommendations", []))
            except Exception as e:
                self.logger.error(f"OCR analysis failed: {e}")
                analysis["ocr_analysis"] = {"error": str(e)}
        
        # Speech Analysis
        if audio_file_path and os.path.exists(audio_file_path):
            try:
                speech_result = await self._analyze_speech(audio_file_path, text)
                analysis["speech_analysis"] = speech_result
                confidence_scores.append(speech_result.get("confidence", 0.5))
                recommendations.extend(speech_result.get("recommendations", []))
            except Exception as e:
                self.logger.error(f"Speech analysis failed: {e}")
                analysis["speech_analysis"] = {"error": str(e)}
        
        # Calculate overall confidence
        overall_confidence = self._calculate_overall_confidence(confidence_scores)
        
        # Generate comprehensive recommendations
        comprehensive_recommendations = self._generate_comprehensive_recommendations(
            analysis, overall_confidence
        )
        
        return {
            "analysis": analysis,
            "confidence_score": overall_confidence,
            "recommendations": comprehensive_recommendations,
            "screening_summary": self._generate_screening_summary(analysis, overall_confidence),
            "risk_level": self._assess_risk_level(overall_confidence)
        }
    
    def _determine_analysis_type(self, text: Optional[str], 
                               audio_path: Optional[str], 
                               image_path: Optional[str]) -> str:
        """Determine the type of analysis based on available inputs."""
        inputs = []
        if text:
            inputs.append(ANALYSIS_TEXT)
        if audio_path:
            inputs.append(ANALYSIS_AUDIO)
        if image_path:
            inputs.append(ANALYSIS_HANDWRITING)
        
        return ANALYSIS_MULTIMODAL if len(inputs) > 1 else inputs[0] if inputs else "unknown"
    
    async def _analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze text input for reading comprehension patterns."""
        try:
            words = text.split()
            word_count = len(words)
            
            if word_count == 0:
                return {"error": "Empty text input", "confidence": 0.0}
            
            # Basic text metrics
            avg_word_length = sum(len(word) for word in words) / word_count
            complex_words = [word for word in words if len(word) > 7]
            sentence_count = text.count('.') + text.count('!') + text.count('?')
            
            # Pattern analysis
            reversals = self._detect_reversals(text)
            spelling_errors = self._detect_spelling_patterns(text)
            phonetic_errors = self._detect_phonetic_errors(text)
            
            # Calculate confidence based on detected patterns
            error_indicators = len(reversals) + len(spelling_errors) + len(phonetic_errors)
            confidence = min(0.9, 0.2 + (error_indicators * 0.2))
            
            recommendations = []
            if reversals:
                recommendations.append("Visual processing exercises may help with letter/word reversals")
            if spelling_errors:
                recommendations.append("Structured spelling practice recommended")
            if phonetic_errors:
                recommendations.append("Phonics-based reading instruction may be beneficial")
            if avg_word_length < 4:
                recommendations.append("Encourage reading materials with varied vocabulary")
            
            return {
                "word_count": word_count,
                "sentence_count": sentence_count,
                "average_word_length": round(avg_word_length, 2),
                "complex_words_count": len(complex_words),
                "reversals_detected": reversals,
                "spelling_patterns": spelling_errors,
                "phonetic_errors": phonetic_errors,
                "confidence": confidence,
                "recommendations": recommendations
            }
            
        except Exception as e:
            self.logger.error(f"Text analysis failed: {e}")
            return {"error": str(e), "confidence": 0.0}
    
    async def _analyze_handwriting(self, image_path: str) -> Dict[str, Any]:
        """Analyze handwriting via OCR for dyslexia indicators."""
        try:
            # Mock OCR analysis for demo/development
            # TODO: Implement actual EasyOCR integration
            
            sample_texts = [
                "The quick brown fox jumps over the lazy dog",
                "Once upon a time there was a brave knight", 
                "Reading is fun and helps us learn new things",
                "Practice makes perfect with daily effort"
            ]
            
            extracted_text = random.choice(sample_texts)
            
            # Mock analysis results
            has_reversals = random.choice([True, False, False])  # 33% chance
            letter_reversals = []
            if has_reversals:
                letter_reversals = random.sample(DYSLEXIA_INDICATORS["letter_reversals"], 
                                               random.randint(1, 2))
            
            writing_clarity = random.uniform(0.6, 0.95)
            letter_formation_score = random.uniform(0.7, 0.95)
            spacing_score = random.uniform(0.6, 0.9)
            
            confidence = 0.7 if has_reversals else 0.3
            
            recommendations = []
            if has_reversals:
                recommendations.append("Practice letter formation exercises")
                recommendations.append("Use multi-sensory writing techniques")
            if writing_clarity < 0.7:
                recommendations.append("Work on handwriting clarity and spacing")
            if letter_formation_score < 0.8:
                recommendations.append("Focus on proper letter formation techniques")
            
            return {
                "extracted_text": extracted_text,
                "text_confidence": writing_clarity,
                "letter_reversals": letter_reversals,
                "writing_clarity_score": round(writing_clarity, 3),
                "letter_formation_score": round(letter_formation_score, 3),
                "spacing_score": round(spacing_score, 3),
                "confidence": confidence,
                "recommendations": recommendations
            }
            
        except Exception as e:
            self.logger.error(f"OCR analysis failed: {e}")
            raise OCRError(f"Handwriting analysis failed: {e}")
    
    async def _analyze_speech(self, audio_path: str, expected_text: Optional[str] = None) -> Dict[str, Any]:
        """Analyze speech for reading fluency and accuracy."""
        try:
            # Mock speech analysis for demo/development
            # TODO: Implement actual Whisper integration
            
            sample_transcriptions = [
                "The quick brown fox jumps over the lazy dog",
                "Reading out loud helps with fluency and comprehension",
                "Practice makes perfect when learning new skills",
                "Every student deserves quality education and support"
            ]
            
            transcribed_text = random.choice(sample_transcriptions)
            
            # Mock metrics
            audio_duration = random.uniform(3.0, 10.0)
            word_count = len(transcribed_text.split())
            reading_speed = word_count / (audio_duration / 60)  # WPM
            
            # Mock fluency metrics
            pauses_count = random.randint(0, 5)
            hesitations = random.randint(0, 3)
            mispronunciations = random.randint(0, 2)
            
            # Mock accuracy
            accuracy_score = random.uniform(0.75, 0.98)
            if expected_text:
                # Simple mock comparison for expected vs actual
                accuracy_score = random.uniform(0.8, 0.95)
            
            # Confidence based on fluency indicators
            fluency_issues = pauses_count + hesitations + mispronunciations
            speed_factor = 1.0 if 100 <= reading_speed <= 200 else 0.7
            accuracy_factor = accuracy_score
            
            confidence = min(0.9, (fluency_issues * 0.1) + (1 - speed_factor) * 0.3 + (1 - accuracy_factor) * 0.4)
            
            recommendations = []
            if reading_speed < 100:
                recommendations.append("Practice reading fluency exercises daily")
            if accuracy_score < 0.85:
                recommendations.append("Work on word recognition and pronunciation")
            if pauses_count > 3:
                recommendations.append("Practice smooth, continuous reading")
            if hesitations > 2:
                recommendations.append("Build confidence through repeated reading of familiar texts")
            
            return {
                "transcribed_text": transcribed_text,
                "audio_duration": round(audio_duration, 2),
                "reading_speed_wpm": round(reading_speed, 1),
                "accuracy_score": round(accuracy_score, 3),
                "pauses_count": pauses_count,
                "hesitations": hesitations,
                "mispronunciations": mispronunciations,
                "confidence": confidence,
                "recommendations": recommendations,
                "expected_text": expected_text
            }
            
        except Exception as e:
            self.logger.error(f"Speech analysis failed: {e}")
            raise SpeechToTextError(f"Speech analysis failed: {e}")
    
    def _detect_reversals(self, text: str) -> List[str]:
        """Detect potential letter and word reversals."""
        reversals = []
        words = text.lower().split()
        
        # Check for common letter reversals
        for word in words:
            for reversal_pair in DYSLEXIA_INDICATORS["letter_reversals"]:
                if "/" in reversal_pair:
                    letters = reversal_pair.split("/")
                    if any(letter in word for letter in letters):
                        reversals.append(f"Potential {reversal_pair} reversal in '{word}'")
        
        # Check for word reversals
        for word in words:
            for reversal_pair in DYSLEXIA_INDICATORS["word_reversals"]:
                if "/" in reversal_pair:
                    word_pair = reversal_pair.split("/")
                    if word in word_pair:
                        reversals.append(f"Potential word reversal: '{word}'")
        
        return reversals
    
    def _detect_spelling_patterns(self, text: str) -> List[str]:
        """Detect dyslexia-related spelling patterns."""
        patterns = []
        words = text.lower().split()
        
        # Look for phonetic spelling patterns
        for word in words:
            # Check for phonetic errors
            for phonetic_pair in DYSLEXIA_INDICATORS["phonetic_errors"]:
                if "/" in phonetic_pair:
                    correct, phonetic = phonetic_pair.split("/")
                    if phonetic in word and correct not in word:
                        patterns.append(f"Phonetic spelling: '{word}' (possibly '{correct}')")
        
        return patterns
    
    def _detect_phonetic_errors(self, text: str) -> List[str]:
        """Detect phonetic processing errors."""
        errors = []
        # This would contain more sophisticated phonetic analysis
        # For demo, return mock results
        if random.random() < 0.3:  # 30% chance of phonetic errors
            errors.append("Possible phonetic processing difficulty detected")
        
        return errors
    
    def _generate_comprehensive_recommendations(self, analysis: Dict[str, Any], 
                                             confidence: float) -> List[str]:
        """Generate comprehensive recommendations based on full analysis."""
        recommendations = []
        
        # Collect all recommendations from individual analyses
        for analysis_type in ["text_analysis", "ocr_analysis", "speech_analysis"]:
            if analysis_type in analysis and "recommendations" in analysis[analysis_type]:
                recommendations.extend(analysis[analysis_type]["recommendations"])
        
        # Add confidence-based recommendations
        if confidence >= CONFIDENCE_THRESHOLD_HIGH:
            recommendations.append("Strong indicators suggest professional dyslexia assessment is recommended")
        elif confidence >= CONFIDENCE_THRESHOLD_MEDIUM:
            recommendations.append("Some indicators present - consider educational support strategies")
        else:
            recommendations.append("Low-level indicators - continue monitoring and supportive practices")
        
        # Add general recommendations
        recommendations.extend([
            "Use multi-sensory learning approaches",
            "Provide extra time for reading and writing tasks",
            "Consider assistive technology tools",
            "Regular practice with structured literacy programs"
        ])
        
        # Remove duplicates while preserving order
        return list(dict.fromkeys(recommendations))
    
    def _generate_screening_summary(self, analysis: Dict[str, Any], confidence: float) -> str:
        """Generate a human-readable summary of the screening results."""
        analysis_types = []
        if analysis.get("text_analysis"):
            analysis_types.append("text")
        if analysis.get("ocr_analysis"):
            analysis_types.append("handwriting")
        if analysis.get("speech_analysis"):
            analysis_types.append("speech")
        
        types_str = ", ".join(analysis_types)
        
        risk_level = self._assess_risk_level(confidence)
        
        return f"Dyslexia screening conducted using {types_str} analysis. " \
               f"Risk level assessed as {risk_level} based on detected patterns and indicators. " \
               f"Confidence score: {confidence:.2f}"
    
    def _assess_risk_level(self, confidence: float) -> str:
        """Assess risk level based on confidence score."""
        if confidence >= CONFIDENCE_THRESHOLD_HIGH:
            return "High"
        elif confidence >= CONFIDENCE_THRESHOLD_MEDIUM:
            return "Moderate" 
        else:
            return "Low"